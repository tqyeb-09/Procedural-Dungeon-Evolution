import random
import time
import os
import subprocess
import sys
from copy import deepcopy
import colorama
from colorama import Fore, Style

from baze_date2 import baze_date_inamici, baze_date_abilitati, baze_date_equipments, baze_date_perks, baze_date_grimoires, sanse_grimoire

print_fake = print

def print(*args, **kwargs):
    text_complet = " ".join(str(arg) for arg in args)
    for litera in text_complet:
        sys.stdout.write(litera)
        sys.stdout.flush()
        time.sleep(0.02)
    print_fake(**kwargs)

def curatare_ecran():
    if os.name == 'nt':
        subprocess.run('cls', shell=True)
    else:
        subprocess.run('clear', shell=True)

def verificari_limite_resurse(jucator):
    if jucator["mana"] > jucator["mana_max"]:
        jucator["mana"] = jucator["mana_max"]

    if jucator["stamina"] > jucator["stamina_max"]:
        jucator["stamina"] = jucator["stamina_max"]

    if jucator["mana"] < 0:
        jucator["mana"] = 0
    if jucator["stamina"] < 0:
        jucator["stamina"] = 0

def verificare_cc_jucator(jucator):
    statusuri = jucator.get("statusuri_active", {})

    if "inghetare" in statusuri:
        print(f"\nEști înghețat complet! Îți pierzi tura!")
        time.sleep(1.5)
        return True

    if "anetire" in statusuri:
        print(f"\nEști amețit și nu poți acționa!")
        time.sleep(1.5)
        return True
    return False

def verificare_cc_inamic(inamic):
    statusuri = inamic.get("statusuri_active", {})

    if "inghetare" in statusuri:
        print(f"\n{inamic['nume'].upper()} este înghețat bocnă și își pierde tura!")
        time.sleep(1.5)
        return True

    if "ametire" in statusuri:
        print(f"\n{inamic['nume'].upper()} este amețit și nu poate ataca!")
        time.sleep(1.5)
        return True
    return False

def verificare_moarte_jucator(jucator, inamic):
    if jucator["hp"] < 0:
        print(f"Te-a omorat {inamic['nume'].upper()}-ul")
        return True
    return False

def verificare_moarte_inamic(inamic):
    if inamic["hp"] <= 0:
        print(f"\n{inamic['nume'].upper()}-ul a murit!")
        return True
    return False

def aplicare_efecte_atac_inamic(atac_ales, inamic, jucator, damage_final):
    lifesteal_atac = atac_ales.get("lifesteal", 0)
    aur_furat = atac_ales.get("furat_gold", 0)
    bonus_reduction = atac_ales.get("bonus_red", 0)
    bonus_hp = atac_ales.get("bonus_hp", 0)
    size_slime  = atac_ales.get("size", 0)

    if "crowd_control" in atac_ales:
        detalii_cc = atac_ales["crowd_control"]
        aplica_dot_tinta(
            inamic, 
            jucator, 
            detalii_cc["tip_status"], 
            detalii_cc.get("dmg_tura", 0), 
            detalii_cc["durata_max"], 
            detalii_cc["text"], 
            detalii_cc.get("stat_scalare", "physical_dmg"))
        
        print(f"\n[EFECT] Ai fost lovit! Acum {detalii_cc['text']}")

    if "efect_DoT" in atac_ales:
        detalii_dot = atac_ales["efect_DoT"]
        aplica_dot_tinta(
            inamic, 
            jucator, 
            detalii_dot["tip_status"], 
            detalii_dot.get("dmg_tura", 0), 
            detalii_dot["durata_max"], 
            detalii_dot["text"], 
            detalii_dot.get("stat_scalare", "physical_dmg"))
        
        print(f"\n[STATUS] {detalii_dot['text'].capitalize()}") 

    if lifesteal_atac > 0 and damage_final > 0:
        viata_furata = (damage_final * lifesteal_atac) // 100
        inamic["hp"] += viata_furata
        print(f"({inamic['nume'].upper()}) și-a refăcut {viata_furata} HP prin Lifesteal!")

    if aur_furat > 0:
        if jucator["gold"] >= aur_furat:
            jucator["gold"] -= aur_furat
            print(f"({inamic['nume'].upper()}) ți-a furat {aur_furat} Aur!")
        else:
            print(f"PICKPOCKET! SARAC! Ti-a furat doar {jucator['gold']} GOLD pe care ii mai aveai!")
            jucator["gold"] = 0

    if bonus_reduction > 0:
        inamic["physical_red"] += bonus_reduction
        inamic["magic_red"] += bonus_reduction
        print(f"({inamic['nume'].upper()})-ul și-a mărit armura cu {bonus_reduction}!")

    if bonus_hp > 0:
        inamic["hp"] += bonus_hp
        print(f"({inamic['nume'].upper()})-ul s-a vindecat cu {bonus_hp} HP!")

    if jucator["infection"] >= 5:
        jucator["jucator_transformare"] = True

    if size_slime > 0:
        print(f"({inamic['nume'].upper()})-ul a absorbit energie și a crescut cu {size_slime}%!")
        size = inamic["hp_max"] + (inamic["hp_max"] * size_slime) // 100
        inamic["hp_max"] += size
        inamic["hp"] += size

def atac_inamic_universal(inamic, jucator):

    atac_ales = random.choice(inamic["abilitati"])

    dmg_atac = atac_ales.get("dmg", 0)
    tip_atac = atac_ales.get("tip", "physical")

    jucator["infection"] += atac_ales.get("infection", 0)

    if tip_atac == "physical":
        numitor_fizic = max(1, (jucator["physical_red"] * jucator["red_multiplicativ"]))
        damage_final = (dmg_atac * 100 * 10) // numitor_fizic
    elif tip_atac == "magic":
        numitor_magic = max(1, (jucator["magic_red"] * jucator["red_multiplicativ"]))
        damage_final = (dmg_atac * 100 * 10) // numitor_magic
    else:
        damage_final = 0  

    jucator["hp"] -= damage_final
    if jucator["hp"] < 0:
        jucator["hp"] = 0

    print(f"\n{inamic['nume'].upper()} foloseste {atac_ales['nume']}!")
    print(f"Ti-a dat {damage_final} DMG")

    aplicare_efecte_atac_inamic(atac_ales, inamic, jucator, damage_final)

def aplica_dot_tinta(jucator, tinta, tip_status, dmg_baza, durata, text_mesaj, stat_scalare="physical_dmg"):
    if "statusuri_active" not in tinta:
        tinta["statusuri_active"] = {}

    dmg_final_status = 0
    if dmg_baza > 0:
        putere_stat = jucator.get(stat_scalare, 20)
        dmg_final_status = (dmg_baza * putere_stat) // 20

    tinta["statusuri_active"][tip_status] = {
        "dmg_tura": dmg_final_status,
        "durata": durata,
        "text": text_mesaj
    }

def execute_abilitate_locked(nume_abilitate, jucator, inamic):
    ab = baze_date_abilitati[nume_abilitate]

    if "mana_gain" in ab:
        jucator["mana"] += ab["mana_gain"]
    if "stamina_gain" in ab:
        jucator["stamina"] += ab["stamina_gain"]

    verificari_limite_resurse(jucator)

    multiplicator = ab.get("multiplicator_dmg", 1.0)

    zar_crit = random.randint(1, 100)

    if zar_crit <= jucator["crit_chance"]:
        crit = True
    else:
        crit = False

    if ab["tip"] == "physical":
        numitor_fizic = max(1, inamic.get("physical_red", 1)) * 100
        damage_final = (jucator["physical_dmg"] * multiplicator * jucator["dmg_multiplicativ"] * 10) // numitor_fizic
    else:
        numitor_magic = max(1, inamic.get("magic_red", 1)) * 100
        damage_final = (jucator["magic_dmg"] * multiplicator * jucator["dmg_multiplicativ"] * 10) // numitor_magic

    if crit:
        damage_final *= jucator["crit_dmg"]

    inamic["hp"] -= damage_final
    if inamic["hp"] < 0:
        inamic["hp"] = 0

    print(f"\nAi folosit {ab['nume'].upper()} și ai provocat {damage_final} DMG lui {inamic['nume'].upper()}!")

    if "efect_DoT" in ab:
        detalii_dot = ab["efect_DoT"]
        aplica_dot_tinta(
            jucator, 
            inamic, 
            detalii_dot["tip_status"], 
            detalii_dot.get("dmg_tura", 0), 
            detalii_dot["durata_max"], 
            detalii_dot["text"], 
            detalii_dot.get("stat_scalare", "physical_dmg"))

        print(f"\n [EFECT ACTIVAT] {inamic['nume'].upper()} {detalii_dot['text']}")

    if "crowd_control" in ab:
        detalii_cc = ab["crowd_control"]
        aplica_dot_tinta(
            jucator, 
            inamic, 
            detalii_cc["tip_status"], 
            detalii_cc.get("dmg_tura", 0), 
            detalii_cc["durata_max"], 
            detalii_cc["text"], 
            detalii_cc.get("stat_scalare", "physical_dmg"))
        
        print(f"\n[CC ACTIVAT] {inamic['nume'].upper()} {detalii_cc['text']}")

def efecte_DoT(jucator, inamic):
    for status, detalii in list(jucator.get("statusuri_active", {}).items()):
        if detalii["durata"] > 0:
            dmg = detalii.get("dmg_tura", 0)
            jucator["hp"] -= dmg
            detalii["durata"] -= 1

            print(f"[{status.upper()}] JUCĂTORUL {detalii['text']} (Ture rămase: {detalii['durata']})")
            time.sleep(1.5)

        if detalii["durata"] == 0:
            del jucator["statusuri_active"][status]

    for status, detalii in list(inamic.get("statusuri_active", {}).items()):
        if detalii["durata"] > 0:
            dmg = detalii.get("dmg_tura", 0)
            inamic["hp"] -= dmg
            detalii["durata"] -= 1

            print(f"[{status.upper()}] {inamic['nume'].upper()} {detalii['text']} (Ture rămase: {detalii['durata']})")
            time.sleep(1.5)

        if detalii["durata"] == 0:
            del inamic["statusuri_active"][status]


    if jucator["hp"] < 0:
        jucator["hp"] = 0
    if inamic["hp"] < 0:
        inamic["hp"] = 0

def aplica_cc_tinta(tinta, tip_cc, durata, text_mesaj):
    if "statusuri_active" not in tinta:
        tinta["statusuri_active"] = {}

    tinta["statusuri_active"][tip_cc] = {
        "durata": durata,
        "text": text_mesaj
    }
    print(f"\n[CC ACTIVAT] {tinta['nume'].upper()} {text_mesaj}")

def equipment_efect(inamic, jucator, baze_date_equipments):
    sloturi_ofesive = ["equipment_sabie", "equipment_inel"]

    for slot in sloturi_ofesive:
        nume_item_echipat = jucator.get(slot)

        if nume_item_echipat and nume_item_echipat in baze_date_equipments:
            item_date = baze_date_equipments[nume_item_echipat]

            if "efect_DoT" in item_date:
                detalii_dot = item_date["efect_DoT"]

            aplica_dot_tinta(
                jucator, 
                inamic, 
                detalii_dot["tip_status"], 
                detalii_dot.get("dmg_tura", 0), 
                detalii_dot["durata_max"], 
                detalii_dot["text"], 
                detalii_dot.get("stat_scalare", "physical_dmg")
            )

            print(f"[ECHIPAMENT] Arma ta ({item_date['nume'].upper()}) a aplicat [{detalii_dot['tip_status'].upper()}]!")
            time.sleep(1)

def afiseaza_abilitati(jucator):
    print("\nAlege abilitatea:")

    for index, ab_nume in enumerate(jucator["abilitati"], start=1):
        if ab_nume == "pumn":
            print(f"{index}. PUMN (+15 MANA / +5 STAMINA)")
        elif ab_nume == "fireball":
            print(f"{index}. FIREBALL (-50 MANA)")
        else:
            ab_detalii = baze_date_abilitati[ab_nume]
            nume = ab_detalii["nume"].upper()

            if "mana_cost" in ab_detalii:
                info_cost = f"-{ab_detalii['mana_cost']} MANA"
            else:
                info_cost = f"-{ab_detalii['stamina_cost']} STAMINA"

            print(f"{index}. {nume} ({info_cost})")

def alegere_atac(inamic, jucator, baze_date_abilitati):
    while True:
        afiseaza_abilitati(jucator)

        alegere = input("\n Introduce optiunea: ").strip()

        if inamic["sansa_evaziva"] == True and random.randint(1, 100) <= 30:
            print("Inamicul este agil si s-a ferit de atac")
            time.sleep(1.5)
            break
        else:
            if not alegere.isdigit() or int(alegere) < 1 or int(alegere) > len(jucator["abilitati"]):
                print("Alege o varianta existenta")
                time.sleep(1.5)
                continue

            index_ales = int(alegere) - 1
            ab_aleasa = jucator["abilitati"][index_ales]

            if ab_aleasa in jucator["cooldowns"]:
                print(f"Abilitatea este pe cooldown! (Mai ai de asteptat {jucator['cooldowns'][ab_aleasa]} ture)")
                time.sleep(1.5)
                continue

            detalii_ab = baze_date_abilitati[ab_aleasa]
            cost_mana = detalii_ab.get("mana_cost", 0)
            cost_stamina = detalii_ab.get("stamina_cost", 0)

            if jucator["mana"] < cost_mana:
                print(f"Nu ai destula MANĂ pentru {detalii_ab['nume'].upper()}!")
                time.sleep(1.5)
                continue

            if jucator["stamina"] < cost_stamina:
                print(f"Nu ai destula STAMINĂ pentru {detalii_ab['nume'].upper()}!")
                time.sleep(1.5)
                continue

            jucator["mana"] -= cost_mana
            jucator["stamina"] -= cost_stamina

            if detalii_ab["cooldown_max"] > 0:
                jucator["cooldowns"][ab_aleasa] = detalii_ab["cooldown_max"]

            execute_abilitate_locked(ab_aleasa, jucator, inamic)
            time.sleep(1)
            break

def scurge_cooldowns(jucator):
    for abilitate in list(jucator["cooldowns"].keys()):
        if jucator["cooldowns"][abilitate] > 0:
            jucator["cooldowns"][abilitate] -= 1

        if jucator["cooldowns"][abilitate] == 0:
            del jucator["cooldowns"][abilitate]

def aplicare_perk(jucator, id_perk_ales, baze_date_perks):
    perk = baze_date_perks[id_perk_ales]

    cheie_activare = f"perk_{id_perk_ales}"
    if jucator.get(cheie_activare) == True:
        print(f"\n{Fore.RED}[EXPLOIT BLOCAT] Ai deja acest perk activat! Alege altul.")
        return False
    
    print(f"\n{Fore.GREEN}[PERK ACTIVAT] {perk['nume'].upper()} a fost aplicat cu succes!")

    for cheie, valoare in perk.items():
        if cheie in ["nume", "tip", "raritate"]:
            continue

        if cheie == "bonus_damage":
            jucator["dmg_multiplicativ"] = (jucator["dmg_multiplicativ"] * 110) // 100

        elif cheie == "bonus_red":
            jucator["red_multiplicativ"] = (jucator["red_multiplicativ"] * 110) // 100

        elif cheie == "sansa_inghetare":
            jucator["perk_chill"] = True

        elif cheie.startswith("bonus_"):
            stat_reala = cheie.replace("bonus_", "")
            if stat_reala in jucator:
                jucator[stat_reala] += valoare
                if stat_reala == "hp":
                    jucator["hp_max"] += valoare

    jucator[cheie_activare] = True
    return True

def aplicare_chill_perk(jucator, inamic):
    if jucator["perk_chill"]:
        sansa = random.randint(1, 100)
        if sansa <= 10:
            aplica_cc_tinta(inamic, "inghetare", 1, "este inghetat de la efectul pasiv Chill!")
            time.sleep(1.5)

def primire_loot(jucator, baze_date_grimoires, este_corupta=False):
    gold_castigat = jucator["camera_curenta"] * 3
    jucator["gold"] += gold_castigat
    print(f"Ai primit {gold_castigat} gold. Total: {jucator['gold']} monede.")
    time.sleep(1.5)

    if este_corupta or jucator["camera_curenta"] % 10 == 0:
        zar_drop = random.randint(1, 100)

        grimoires_ordonate = sorted(baze_date_grimoires.items(), key=lambda x: x[1]["sansa"])

        for id_grimoire, date in grimoires_ordonate:
            if zar_drop <= date["sansa"]:
                jucator["grimoires"][id_grimoire] += 1
                print(f"\n[DROP] Ai găsit un [{date['nume'].upper()}] pe corpul inamicului!")
                break

def lupta_camera_afisare(inamic, jucator):
    print(f"\n==== Inamic: {inamic['nume'].upper()} ==== ")
    print(f" HP Inamic: {inamic['hp']}/{inamic["hp_max"]} HP") 
    print("-" * 20)
    print(f"\n Jucator: {jucator['hp']}/{jucator['hp_max']} HP | Mana: {jucator['mana']}/500")
    print("-" * 20)

def lupta_camera(jucator, inamic, este_corupta=False):
    while inamic["hp"] > 0 and jucator["hp"] > 0:
        curatare_ecran()
        lupta_camera_afisare(inamic, jucator)

        if verificare_cc_jucator(jucator): pass
        else:
            alegere_atac(inamic, jucator, baze_date_abilitati)
            equipment_efect(inamic, jucator, baze_date_equipments)
            aplicare_chill_perk(jucator, inamic)

        if verificare_moarte_inamic(inamic): break
        if verificare_cc_inamic(inamic): pass
        else:
            atac_inamic_universal(inamic, jucator)
            time.sleep(1.5)

        if verificare_moarte_jucator(jucator, inamic):
            primire_loot(jucator, baze_date_grimoires, este_corupta)
            break

        efecte_DoT(jucator, inamic)
        scurge_cooldowns(jucator)

        if verificare_moarte_inamic(inamic): 
            primire_loot(jucator, baze_date_grimoires, este_corupta) 
            break
        if verificare_moarte_jucator(jucator, inamic): break