import random
import time
import os
import subprocess
import sys
from copy import deepcopy
import colorama
from colorama import Fore, Style

from baze_date3 import (
    baze_date_inamici, 
    baze_date_abilitati, 
    baze_date_equipments, 
    baze_date_perks, 
    baze_date_grimoires, 
    sanse_grimoire, 
    sanse_raritati_perks, 
    sanse_raritati_equipments, 
    baze_date_deals, 
    setari_echilibru, 
    baze_date_milestones,
    baze_date_blacksmith
)

def print_type(text: str, delay: float = 0.005, end: str = "\n", animate: bool = True):
    text_complet = str(text)

    if not animate or delay <= 0:
        sys.stdout.write(text_complet + end)
        sys.stdout.flush()
        return
    for litera in text_complet:
        sys.stdout.write(litera)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()

def curatare_ecran():
    comanda = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run(comanda, shell=True)

def verificari_limite_resurse(entitate: dict):
    resurse = [("hp", "hp_max"), ("mana", "mana_max"), ("stamina", "stamina_max")]

    for resursa, resura_max in resurse:
        if resursa in entitate and resura_max in entitate:
            entitate[resursa] = max(0, min(entitate[resursa], entitate[resura_max]))

def verificare_cc(entitate: dict, este_jucator: bool = True) -> bool:
    statusuri = entitate.get("statusuri_active", {})
    nume_entitate = "Jucatorul" if este_jucator else entitate.get('nume', 'Inamic').upper()

    config_cc = {
        "inghetare": (
            Fore.CYAN,
            "Esti inghetat complet! Iti pierzi tura!"
            f"[{nume_entitate}] este inghetat bocna si isi pierde tura!"
        ),
        "ametire": (
            Fore.YELLOW, 
            "Esti ametit si nu poti actiona!", 
            f"[{nume_entitate}] este ametit si nu poate ataca!"
        )
    }

    for cc_efect, (culoare, mesaj_jucator, mesaj_inamic) in config_cc.items():
        if cc_efect in statusuri:
            mesaj = mesaj_jucator if este_jucator else mesaj_inamic
            print_type(f"\n{culoare}{mesaj}{Style.RESET_ALL}")
            return True
    
    return False

def verificare_moarte(entitate: dict, este_jucator: bool = True, oponent: dict = None) -> bool:
    if entitate["hp"] <= 0:
        if este_jucator:
            nume_oponent = oponent.get('nume', "INAMIC").upper() if oponent else "INAMIC"
            print_type(f"Te-a omorat {nume_oponent}-ul")
        else:
            nume_inamic = entitate.get('nume', "INAMIC").upper()
            print_type(f"\n{nume_inamic}-ul a murit!")

        return True
    
    return False    

def _executa_lifesteal(valoare: int, inamic: dict, jucator: dict, damage_final: int):
    if damage_final > 0:
        viata_furata = (damage_final * valoare) // 100
        inamic["hp"] = inamic.get("hp", 0) + viata_furata
        verificari_limite_resurse(inamic)
        print_type(f"[{inamic.get('nume', 'INAMIC').upper()}] si-a refacut {viata_furata} HP prin Lifesteal!")

def _executa_furt_gold(valoare: int, inamic: dict, jucator: dict, damage_final: int):
    aur_jucator = jucator.get("gold", 0)
    if aur_jucator >= valoare:
        jucator["gold"] -= valoare
        print_type(f"[{inamic.get('nume', 'INAMIC').upper()}] ti-a furat {valoare} Aur!")
    else:
        print_type(f"PICKPOCKET! SARAC! Ti-a furat doar {aur_jucator} GOLD pe care ii mai aveai!")
        jucator["gold"] = 0

def _executa_bonus_red(valoare: int, inamic: dict, jucator: dict, damage_final: int):
    inamic["physical_red"] = inamic.get("physical_red", 0) + valoare
    inamic["magic_red"] = inamic.get("magic_red", 0) + valoare
    print_type(f"[{inamic.get('nume', 'INAMIC').upper()}] si-a marit armura cu {valoare}!")

def _executa_bonus_hp(valoare: int, inamic: dict, jucator: dict, damage_final: int):
    inamic["hp"] = inamic.get("hp", 0) + valoare
    verificari_limite_resurse(inamic)
    print_type(f"[{inamic.get('nume', 'INAMIC').upper()}] s-a vindecat cu {valoare} HP!")

def _executa_size_slime(valoare: int, inamic: dict, jucator: dict, damage_final: int):
    hp_maxim = inamic.get("hp_max", 100)
    bonus_size = (hp_maxim * valoare) // 100

    inamic["hp_max"] = hp_maxim + bonus_size
    inamic["hp"] = inamic.get("hp", 0) + bonus_size
    verificari_limite_resurse(inamic)
    print_type(f"[{inamic.get('nume', 'INAMIC').upper()}]-ul a absorbit energie si a crescut cu {valoare}%!")

INAMIC_MECANICI = {
    "lifesteal": _executa_lifesteal,
    "furat_gold": _executa_furt_gold,
    "bonus_red": _executa_bonus_red,
    "bonus_hp": _executa_bonus_hp,
    "size": _executa_size_slime
}

def proceseaza_efecte(atac_date: dict, inamic: dict, jucator: dict, damage_final: int):
    for cheie_mecanica, functie_mecanica in INAMIC_MECANICI.items():
        if cheie_mecanica in atac_date and atac_date[cheie_mecanica] > 0:
            valoare_efect = int(atac_date[cheie_mecanica])
            functie_mecanica(valoare_efect, inamic, jucator, damage_final)
    
def aplica_dot_tinta(
        attacker: dict, 
        attacked: dict, 
        tip_status: str, 
        dmg_baza: int, durata: int, 
        text_mesaj: str, 
        stat_scalare: str = "physical_dmg", 
        val_stat_implicita: int = 20
        ):
    statusuri = attacked.setdefault("statusuri_active", {})

    dmg_final_status = 0
    if dmg_baza > 0:
        putere_stat = int(attacker.get(stat_scalare, val_stat_implicita))
        dmg_final_status = (dmg_baza * putere_stat) // 20

    statusuri[tip_status] = {
        "dmg_tura": int(dmg_final_status),
        "durata": int(durata),
        "text": str(text_mesaj)
    }

def aplicare_statusuri(atac_date: dict, attacker: dict, attacked: dict):
    tipuri_efecte = [
        ("crowd_control", "\n[EFECT] Ai fost lovit! Acum {}"), 
        ("efect_DoT", "\n[STATUS] {}")
        ]
    
    for cheie_efect, format_text in tipuri_efecte:
        if cheie_efect in atac_date:
            detalii = atac_date[cheie_efect]
            aplica_dot_tinta(
                attacked, 
                attacker, 
                detalii["tip_status"], 
                detalii.get("dmg_tura", 0), 
                detalii["durata_max"], 
                detalii["text"], 
                detalii.get("stat_scalare", "physical_dmg")
            )
        
            text_final = detalii.get("text", "").capitalize()
            print_type(format_text.format(text_final))

def _aplica_reducere_scut(scut_curent: int, damage_final: int) -> tuple[int, int]:
    damage_ramas = max(0, damage_final - scut_curent)
    scut_nou = max(0, scut_curent - damage_final)
    return damage_ramas, scut_nou

def _absoarbe_scut(pasiva_dict: dict, damage_final: int, entitate_nume: str) -> int:
    cheie_valoare = pasiva_dict.get("nume", "")
    scut_curent = pasiva_dict.get(cheie_valoare, 0)

    if scut_curent > 0:
        damage_ramas, scut_nou = _aplica_reducere_scut(scut_curent, damage_final)
        pasiva_dict[cheie_valoare] = scut_nou

        print_type(f" 🛡️  • {entitate_nume}-ul a absorbit atacul! Scut rămas: {scut_nou} HP.\n")
        damage_final = int(damage_ramas)

    return damage_final

def _loveste_scut(entitate: dict, damage_final: int) -> int:
    nume = entitate.get('nume', None)
    if not nume:
        nume = "Jucator"
    if "pasive" in entitate:
        for pasiva in entitate["pasive"]:
            nume_p = pasiva.get("nume", "")

            if nume_p.endswith("_shield"):
                damage_final = _absoarbe_scut(pasiva, damage_final, nume)

                if damage_final <= 0:
                    break

    return damage_final

def damage_dat(
        attacker: dict, 
        attacked: dict, 
        multiplicator: float, 
        stat_penetrare: str = "armor_pen", 
        stat_rezistenta: str = "physical_red", 
        stat_dmg: str = "physical_dmg", 
        is_true_damage: bool = False,
        este_jucator: bool = True,
        ) -> int:
    
    damage_final = 0
    baza_dmg = int(attacker.get(stat_dmg, 20))
    multiplicativ = int(attacker.get("dmg_multiplicativ", 100))

    if not is_true_damage:
        pen_curent = min(60, attacker.get(stat_penetrare, 0))
        rezistenta_tinta = max(1, attacked.get(stat_rezistenta, 10))
        
        rezistenta_ramasa = max(1, rezistenta_tinta * (100 - pen_curent) // 100)

        damage_calculat = int(baza_dmg * multiplicator * multiplicativ) // (rezistenta_ramasa * 10)
        damage_final = damage_calculat
    else:
        baza_fizic = int(attacker.get("physical_dmg", 20))
        baza_magic = int(attacker.get("magic_dmg", 0))

        true_damage = (baza_fizic + baza_magic) // 2

        damage_calculat_true = (true_damage * multiplicator * multiplicativ) // 10
        damage_final = int(damage_calculat_true)

    if este_jucator:
        pass
    else:
        damage_final = (damage_final // 100)

    return max(1, damage_final)

def atac_inamic_universal(inamic: dict, jucator: dict):
    atac_ales = random.choice(inamic["abilitati"])

    dmg_atac = int(atac_ales.get("dmg", 0))
    tip_atac = str(atac_ales.get("tip", "physical")).lower()

    jucator["infection"] = max(0, jucator.get("infection", 0) + atac_ales.get("infection", 0))

    if tip_atac == "physical":
        damage_final = damage_dat(
            inamic,
            jucator,
            1.0,
            "physical_dmg",
            "physical_red",
            este_jucator=False
        )
    elif tip_atac == "magic":
        damage_final = damage_dat(
            inamic,
            jucator,
            1.0,
            "magic_dmg",
            "magic_red",
            este_jucator=False
        )
    else:
        damage_final = max(0, dmg_atac)

    damage_final = _loveste_scut(jucator, damage_final)

    jucator["hp"] -= damage_final
    verificari_limite_resurse(jucator)

    print_type(f"\n {inamic.get('nume', 'INAMIC').upper()} foloseste {atac_ales.get('nume', 'Abilitate')}!\n")
    print_type(f" Ti-a dat {damage_final} DMG\n")

    aplicare_statusuri(atac_ales, inamic, jucator)
    proceseaza_efecte(atac_ales, inamic, jucator, damage_final)

    if jucator.get("infection", 0) >= 5:
        jucator["jucator_transformare"] = True

def aplica_mecanica_vampirism(jucator: dict, damage_final: int, tip_atac: str) -> None:
    if damage_final <= 0:
        return

    tipuri_vampirism = [
        ("physical", "🩸 LIFESTEAL", "lifesteal")
        ("", "🔮 OMNIVAMP", "omnivamp")
    ]

    viata_recuperata = 0
    mesaje_active = []
    tip_atac_curat = str(tip_atac).lower()

    for tip_valid, text, cheie_stat in tipuri_vampirism:
        if not tip_valid or tip_atac_curat == tip_valid:
            procent = int(jucator.get(cheie_stat, 0))
            if procent > 0:
                viata_recuperata += (damage_final * procent) // 100
                mesaje_active.append(text)

    if viata_recuperata == 0 and (jucator.get("lifesteal", 0) > 0 or jucator.get("omnivamp", 0) > 0):
        viata_recuperata = 1

    if viata_recuperata > 0:
        max_hp = jucator.get("hp_max", 200)
        jucator["hp"] = min(max_hp, jucator["hp"] + viata_recuperata)

        mesaj_final = " + ". join(mesaje_active) if mesaje_active else "🧬 VAMPIRISM"

        verificari_limite_resurse(jucator)
        print_type(f"{mesaj_final}: Ai absorbit forța inamicului și te-ai vindecat cu +{viata_recuperata} HP!\n")

def consuma_mana_stamina(entitate: dict, ab: dict) -> None:
    resurse_config = {
        "mana_cost": ("mana", -1),
        "stamina_cost": ("stamina", -1),
        "mana_gain": ("mana", 1),
        "stamina_gain": ("stamina", 1)
    }
    for cheie, (resursa, multiplicator) in resurse_config.items():
        valoare = int(ab.get(cheie, 0))

        if valoare > 0:
            entitate.setdefault(resursa, 0)
            entitate[resursa] += valoare * multiplicator

    verificari_limite_resurse(entitate)

def verificare_crit(entitate: dict) -> bool:
    stat_brut = entitate.get("crit_chance", 0)
    sansa_critica = int(max(0, min(stat_brut, 100)))

    zar_crit = random.randint(1, 100)
    return zar_crit <= sansa_critica

def verificare_inghetare(entitate: dict) -> bool:
    stat_brut = entitate.get("freezing_chance", 0)
    sansa_inghetare = int(max(0, min(stat_brut, 100)))

    zar_inghetare = random.randint(1, 100)
    return zar_inghetare <= sansa_inghetare

def abilitati_defensive(entitate: dict, abilitate: dict, nume_abilitate: str):
    durata_buff = abilitate.get("duration_max", 1)
    stat_scalare = abilitate.get("stat_scalare", "physical_red")
    procent = abilitate.get("procent_scalare", 0)

    if stat_scalare in entitate and procent > 0:
        valoare_baza = entitate[stat_scalare]

        bonus_procentual = (valoare_baza * procent) // 100

        if bonus_procentual > 0:
            entitate.setdefault("buffuri_active", {})[nume_abilitate] = {
                "stat": stat_scalare,
                "valoare": bonus_procentual,
                "durata_ramasa": durata_buff
            }

            entitate[stat_scalare] += bonus_procentual
            print_type(f"\n  • 🛡️ [{nume_abilitate.upper()}] ACTIVAT! +{bonus_procentual} {stat_scalare} ({procent}% din baza ta).")

def execute_abilitate_locked(jucator: dict, inamic: dict, nume_abilitate: str):
    ab = baze_date_abilitati[nume_abilitate]

    consuma_mana_stamina(jucator, ab)

    verificari_limite_resurse(jucator)

    multiplicator = ab.get("multiplicator_dmg", 1.0)

    crit = verificare_crit(jucator)
    inghetat = verificare_inghetare(jucator)

    if ab["tip"] == "physical":
        damage_final = damage_dat(jucator, inamic, multiplicator, este_jucator=True)
    elif ab["tip"] == "magic":
        damage_final = damage_dat(jucator, inamic, multiplicator, "magic_pen", "magic_red", "magic_dmg", este_jucator=True)
    elif ab["tip"] == "true":
        damage_final = damage_dat(jucator, inamic, multiplicator, is_true_damage=True, este_jucator=True)
    elif ab["tip"] == "defensive":
        damage_final = 0
        abilitati_defensive(jucator, ab, nume_abilitate)

    if crit:
        damage_final = (damage_final * jucator["crit_dmg"]) // 100
        print_type(f"✨ LOVITURĂ CRITICĂ! Daunele au fost amplificate cu x{jucator['crit_dmg'] // 100}!")

    if inghetat:
        aplica_cc_tinta(
            inamic,
            "inghetare",
            1,
            "este înghețat de la efectul pasiv Chill!"
        )
        time.sleep(1)

    damage_final = _loveste_scut(inamic, damage_final)

    inamic["hp"] -= damage_final
    aplica_mecanica_vampirism(jucator, damage_final, ab["tip"])
    
    verificari_limite_resurse(inamic)

    print_type(f"\nAi folosit {ab['nume'].upper()} și ai provocat {damage_final} DMG lui {inamic['nume'].upper()}!")

    aplicare_statusuri(ab, jucator, inamic)

def efecte_DoT(entitate: dict, este_jucator: bool):
    for status, detalii in list(entitate.get("statusuri_active", {}).items()):
        if detalii["durata"] > 0:
            dmg = detalii.get("dmg_tura", 0)
            entitate["hp"] -= dmg
            detalii["durata"] -= 1

            subiect = "Tu" if este_jucator else f"{entitate['nume'].upper()}"
            print_type(f"[{status.upper()}] {subiect} {detalii['text']} (Ture rămase: {detalii['durata']})")
            time.sleep(1.5)

        if detalii["durata"] == 0:
            entitate["statusuri_active"].pop(status, None)

    verificari_limite_resurse(entitate)

def aplica_cc_tinta(entitate: dict, tip_cc: str, durata: int, text_mesaj: str):
    entitate.setdefault("statusuri_active", {})

    entitate["statusuri_active"][tip_cc] = {
        "durata": durata,
        "text": text_mesaj
    }
    print_type(f"\n⚡ [CC ACTIVAT] {entitate['nume'].upper()} {text_mesaj.capitalize()}")

def aplica_statistici(entitate: dict, cheie: str, valoare: int):
    stat_reala = cheie.replace("bonus_", "")

    if stat_reala.endswith("_multiplicativ"):
        if stat_reala in entitate:
            multiplicator_procentual = 100 + valoare
            entitate[stat_reala] = (entitate[stat_reala] * multiplicator_procentual) // 100
    else:
        if stat_reala in entitate:
            entitate[stat_reala] += valoare

def aplicare_perk(entitate: dict, efecte: dict, id_ales: str = None, prefix_anti_exploit: str = "perk") -> bool:
    if id_ales and prefix_anti_exploit:
        cheie_activare = f"{prefix_anti_exploit}_{id_ales}"
        if entitate.get(cheie_activare) == True:
            print_type(f"\n{Fore.RED}[EXPLOIT BLOCAT] Acest efect ({cheie_activare}) este deja activat!")
            return False
        
        entitate[cheie_activare] = True

    if "nume" in efecte:
        print_type(f"\n{Fore.GREEN}[EFECT APLICAT] {efecte['nume'].upper()} a fost procesat cu succes!")

    for cheie, valoare in efecte.items():
        if isinstance(valoare, (str, list)):
            continue

        aplica_statistici(entitate, cheie, valoare)

    entitate[cheie_activare] = True
    return True

def equipment_efect(attacker: dict, attacked: dict, baze_date_equipments: dict, este_jucator: bool):
    sloturi_ofesive = ["equipment_sabie", "equipment_inel"]

    for slot in sloturi_ofesive:
        nume_item_echipat = attacker.get(slot)

        if nume_item_echipat and nume_item_echipat in baze_date_equipments:
            item_date = baze_date_equipments[nume_item_echipat]

            if "efect_DoT" in item_date:
                detalii_dot = deepcopy(item_date["efect_DoT"])

            aplica_dot_tinta(
                attacker, 
                attacked, 
                detalii_dot["tip_status"], 
                detalii_dot.get("dmg_tura", 0), 
                detalii_dot["durata_max"], 
                detalii_dot["text"], 
                detalii_dot.get("stat_scalare", "physical_dmg")
            )
            nume = "Arma ta" if este_jucator else f"Arma lui {attacker.get('nume', 'Inamic').upper()}"
            print_type(f"[ECHIPAMENT] {nume} ({item_date['nume'].upper()}) a aplicat [{detalii_dot['tip_status'].upper()}]!")
            time.sleep(1)

def afiseaza_abilitati(jucator: dict, baze_date_abilitati: dict):
    costuri = ["mana_cost", "stamina_cost"]
    print_type("\nAlege abilitatea:")

    for index, ab_nume in enumerate(jucator["abilitati"], start=1):
        if ab_nume in baze_date_abilitati:
            ab_detalii = baze_date_abilitati[ab_nume]
            nume = ab_detalii["nume"].upper()

            info_cost = "COST ZERO"
            for tip_cost in costuri:
                if tip_cost in ab_detalii:
                    valoare = ab_detalii[tip_cost]
                    nume_resursa = tip_cost.split('_')[0].upper()
                    info_cost = f"-{valoare} {nume_resursa}"
                    break

            print_type(f"{index}. {nume} ({info_cost})")

def alegere_atac(jucator: dict, inamic: dict, baze_date_abilitati: dict):
    while True:
        afiseaza_abilitati(jucator, baze_date_abilitati)
        alegere = input("\n Introduce optiunea: ").strip()

        if not alegere.isdigit():
            print_type("Nemernic! Baga numar")
            time.sleep(1)
            continue

        index_ales = int(alegere) - 1

        if index_ales < 0 or index_ales >= len(jucator["abilitati"]):
            print_type("Alege o varianta existenta din lista!")
            time.sleep(1)
            continue

        ab_aleasa = jucator["abilitati"][index_ales]

        if ab_aleasa in jucator.get("cooldowns", {}):
            ture_ramase = jucator["cooldowns"][ab_aleasa]
            if ture_ramase > 0:
                print_type(f"Abilitatea este pe cooldown! (Mai ai de asteptat {ture_ramase} ture)")
                time.sleep(1)
                continue

        if ab_aleasa not in baze_date_abilitati:
            print_type("Eroare: Abilitatea nu exista in baza de date!")
            continue

        detalii_ab = baze_date_abilitati[ab_aleasa]
        nume_ab = detalii_ab.get("nume", ab_aleasa).upper()

        cost_mana = detalii_ab.get("mana_cost", 0)
        cost_stamina = detalii_ab.get("stamina_cost", 0)

        resurse_verificare = {
            "mana": cost_mana,
            "stamina": cost_stamina
        }

        are_resurse = True
        for resursa, cost in resurse_verificare.items():
            if jucator.get(resursa, 0) < cost:
                print_type(f"Nu ai destula {resursa.upper()} pentru {nume_ab}!")
                time.sleep(1)
                break
        if not are_resurse:
            continue
        for resursa, cost in resurse_verificare.items():
            jucator[resursa] -= cost

        if detalii_ab["cooldown_max"] > 0:
            jucator["cooldowns"][ab_aleasa] = detalii_ab["cooldown_max"]

        execute_abilitate_locked(jucator, inamic, ab_aleasa)
        time.sleep(1)
        break

def scurge_cooldown_abilitati(jucator: dict):
    for abilitate, ture in list(jucator.get("cooldowns", {}).items()):
        if ture > 0:
            ture -= 1
            jucator["cooldowns"][abilitate] = ture
            print_type(f"Cooldown ramas pentru {abilitate.upper()}: {ture} ture")

        if ture == 0:
            jucator["cooldowns"].pop(abilitate, None)
    
def scurge_durata_abilitati_buff(jucator: dict):
    if "buffuri_active" in jucator:
        for nume_buff, date_buff in list(jucator["buffuri_active"].items()):
            date_buff["durata_ramasa"] -= 1
            runde_ramase = date_buff["durata_ramasa"]

            if runde_ramase <= 0:
                stat_modificat = date_buff["stat"]
                valoare_retrasa = date_buff["valoare"]

                jucator[stat_modificat] -= valoare_retrasa
                jucator["buffuri_active"].pop(nume_buff, None)

                print_type(f"⏳ ✘ [STATUS] Efectul [{nume_buff.upper()}] a expirat! Statisticile pentru {stat_modificat} au revenit la normal.")
                time.sleep(1)
            else:
                print_type(f"■ Buff-ul [{nume_buff.upper()}] mai are {runde_ramase} runde active.")
                time.sleep(1)

def _conditie_scut_spart(jucator: dict, nume_p: int) -> bool:
    return jucator.get(nume_p, 0) == 0

CONDITII_PASIVE = {
    "scut_distrus": _conditie_scut_spart
}

def scurge_recharge_time(jucator: dict):
    for nume_p in list(jucator["pasive_recharge_rate"]):
        pasiva_activa = next((p for p in jucator.get("pasive", []) if p.get("nume") == nume_p), None)

        if pasiva_activa:
            conditie = pasiva_activa.get("cu_conditie", False)

            if conditie:
                tip_conditie = pasiva_activa.get("tip_conditie", "scut_distrus")
                functie_verificare = CONDITII_PASIVE.get(tip_conditie)

                if functie_verificare:
                    poate_scadea = functie_verificare(jucator, nume_p)
                else:
                    poate_scadea = True
            else:
                poate_scadea = True

            if poate_scadea:
                jucator["pasive_recharge_rate"][nume_p] -= 1

                if jucator["pasive_recharge_rate"][nume_p] <= 0:
                    jucator["pasive_recharge_rate"].pop(nume_p, None)
                    print_type(f"⚡ [PASIVĂ] Reincarcarea pentru {nume_p.upper()} s-a terminat! Pasiva este din nou pregatita.")

def _activare_scut(jucator: dict, pasiva: dict, nume_p: str):
    jucator[nume_p] = pasiva.get("flat_shield", 0)
    print(f"  • 🛡️ [{nume_p.upper()}] Scut activat: {jucator[nume_p]} HP.")

MECANICI_ACTIVARE = {
    "flat_shield": _activare_scut
}

def activeaza_pasive_lupte(jucator: dict):
    print("\n SE ACTIVEAZĂ EFECTE PASIVE DIN ECHIPAMENTE:")

    jucator.setdefault("pasive_recharge_rate", {})

    if "pasive" in jucator and jucator["pasive"]:
        for pasiva in jucator["pasive"]:
            nume_pasiva = pasiva.get("nume", "")
            recharge = pasiva.get("recharge_time", 0)

            if jucator["pasive_recharge_rate"].get(nume_pasiva, 0) == 0:
                pasiva_activata = False

                for cheie_mecanica, functie_pornire in MECANICI_ACTIVARE.items():
                    if cheie_mecanica in pasiva:
                        functie_pornire(jucator, pasiva, nume_pasiva)
                        pasiva_activata = True

                if pasiva_activata and recharge > 0:    
                    jucator["pasive_recharge_rate"][nume_pasiva] = recharge
                    print(f" • [{nume_pasiva.upper()}] a intrat în cooldown pentru {recharge} runde.")
            else:
                ture_ramase = jucator["pasive_recharge_rate"][nume_pasiva]
                print(f" • [{nume_pasiva.upper()}] se reîncarcă! (Mai are {ture_ramase} ture)")

def primire_loot(jucator: dict, baze_date_grimoires: dict, inamic: dict, este_corupta: bool = False):
    gold_baza = 10
    gold_castigat = (gold_baza + jucator["camera_curenta"] * 3)
    jucator["gold"] += gold_castigat
    print(f"Ai primit {gold_castigat} gold. Total: {jucator['gold']} monede.")
    time.sleep(1.5)

    proceseaza_loot_monstru(jucator, inamic)

    if este_corupta or jucator["camera_curenta"] % 10 == 0:
        zar_drop = random.randint(1, 100)

        grimoires_ordonate = sorted(
            baze_date_grimoires.items(), 
            key=lambda x: x[1]["sansa"],
            reverse=True
            )

        for id_grimoire, date in grimoires_ordonate:
            if zar_drop <= date["sansa"]:
                jucator.setdefault("grimoires", {})
                jucator["grimoires"][id_grimoire] = jucator["grimoires"].get(id_grimoire, 0) + 1
                print_type(f"\n✨ [DROP] Ai găsit un [{date.get('nume', id_grimoire).upper()}] pe corpul inamicului!")
                time.sleep(1)
                break

def proceseaza_loot_monstru(jucator: dict, inamic: dict):
    materiale_drop = inamic.get("materiale", {})

    jucator.setdefault("materiale", {})

    for nume_material, lista_sanse in materiale_drop.items():
        cantitate_totala_castigata = 0

        for optiune in lista_sanse:
            zar = random.randint(1, 100)
            if zar <= optiune.get("sansa", 0):
                cantitate_totala_castigata += optiune.get("cantitate", 0)

        if cantitate_totala_castigata > 0:
            jucator["materiale"][nume_material] = jucator["materiale"].get(nume_material, 0) + cantitate_totala_castigata
            print_type(f" LOOT: Monstrul a dropat {cantitate_totala_castigata}x {nume_material.upper()}!")

def lupta_camera_afisare(jucator: dict, inamic: dict):
    hp_jucator = jucator.get("hp", 100)
    hp_max_jucator = jucator.get("hp_max", 100)

    mana_jucator = jucator.get("mana", 0)
    mana_max_jucator = jucator.get("mana_max", 0)

    stamina_jucator = jucator.get("stamina", 0)
    stamina_max_jucator = jucator.get("stamina_max", 0)

    hp_inamic = inamic.get("hp", 100)
    hp_max_inamic = inamic.get("hp_max", 100)

    print(f"\n==== Inamic: {inamic['nume'].upper()} ==== ")
    print(f" HP Inamic: {hp_inamic}/{hp_max_inamic} HP") 
    print("-" * 20)

    print(f"\n Jucator: {hp_jucator}/{hp_max_jucator} HP | "
          f"Mana: {mana_jucator}/{mana_max_jucator} MP | "
          f"Stamina: {stamina_jucator}/{stamina_max_jucator} ST")
    print("-" * 20)

def lupta_camera(jucator: dict, inamic: dict, este_corupta: bool = False):
    while inamic["hp"] > 0 and jucator["hp"] > 0:
        curatare_ecran()
        lupta_camera_afisare(jucator, inamic)

        if verificare_cc(jucator): 
            pass
        else:
            alegere_atac(jucator, inamic, baze_date_abilitati)
            equipment_efect(jucator, inamic, baze_date_equipments, este_jucator=True)

        if verificare_moarte(inamic): 
            primire_loot(jucator, baze_date_grimoires, inamic, este_corupta)
            break
        if verificare_cc(inamic): 
            pass
        else:
            atac_inamic_universal(inamic, jucator)
            time.sleep(1.5)

        if verificare_moarte(jucator):
            break

        scurge_cooldown_abilitati(jucator)
        scurge_durata_abilitati_buff(jucator)
        scurge_recharge_time(jucator)
        efecte_DoT(jucator, este_jucator=True)
        efecte_DoT(inamic, este_jucator=False)

        if verificare_moarte(inamic): 
            primire_loot(jucator, baze_date_grimoires, inamic, este_corupta) 
            break
        if verificare_moarte(jucator): 
            break