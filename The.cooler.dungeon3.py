import random
import time
import os
import subprocess
import sys
from copy import deepcopy
import json
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

from combat3 import lupta_camera, curatare_ecran, aplicare_perk

colorama.init(autoreset=True)

print_original = print

def print(*args, **kwargs):
    text_complet = " ".join(str(arg) for arg in args)
    for litera in text_complet:
        sys.stdout.write(litera)
        sys.stdout.flush()
        time.sleep(0.02)
    print_original(**kwargs)

jucator = {
    "hp": 200, 
    "hp_max": 200,
    "physical_dmg": 20, 
    "magic_dmg": 20,
    "armor_pen": 0,
    "magic_pen": 0,
    "dmg_multiplicativ": 100,
    "physical_red": 10, 
    "magic_red" : 5,
    "red_multiplicativ": 100,
    "nivel": 0,
    "exp": 0,
    "exp_necesar": 100,
    "luck": 0,
    "lifesteal": 0,
    "omnivamp": 0,
    "mana": 500, 
    "mana_max" : 500,
    "stamina": 100, 
    "stamina_max": 100,
    "camera_curenta": 1, 
    "gold": 0,
    "crit_chance": 10, 
    "crit_dmg": 200,
    "freezing_chance": 0,
    "infection": 0,
    "jucator_transformare": False,
    "jucator_transformare_verificare": False,
    "jucator_stun": False,
    "statusuri_active": {},
    "abilitati": [
        "pumn", 
        "fireball"
    ],
    "pasive": [],
    "perks": [],
    "deals": [],
    "cooldowns": {},
    "pasive_recharge_rate": {},
    "grimoires": {
        "grimoire_comun": 0,
        "grimoire_rar": 0,
        "grimoire_epic": 0,
        "grimoire_legendar": 0,
    },
    "materiale": {},
    "equipments": {
        "head": {"id": "witch_hat", "level": 0, "iron_ingot_needed": 2, "glass_needed": 1},
        "ring": {"id": "stone_ring", "level": 0, "iron_ingot_needed": 2, "glass_needed": 1}
    },
    "perk_chill": False,
    "equipment_cap": False,
    "equipment_picioare": False,
    "equipment_piept": False,
    "equipment_inel": False,
    "equipment_sabie": False
}

inamic = {}

def afisare_inventar_grimoire(jucator, toate_grimoire_urile):
    print("\n=== INVENTAR GRIMOIRE-URI ===")

    for index, cheie in enumerate(toate_grimoire_urile, start=1):
        nume_curat = cheie.replace("_", " ").upper()
        cantitate = jucator["grimoires"][cheie]
        print(f"{index}. {nume_curat} (Deții: {cantitate})")

    optiune_iesire = len(toate_grimoire_urile) + 1
    print(f"{optiune_iesire}. Înapoi")

    return optiune_iesire

def deschidere_grimoire(jucator, grimoire_ales, baze_date_abilitati, sanse_grimoire):
    jucator["grimoires"][grimoire_ales] -= 1
    print(f"\n[DESCHIDERE] Esti coplesit de {grimoire_ales.replace('_', ' ').upper()}... si lesini")
    time.sleep(4)
    print("Te trezesti si simti puterea din grimoire cum circula prin tine")
    time.sleep(1)

    procente_grimoire = sanse_grimoire[grimoire_ales]
    lista_raritati = list(procente_grimoire.keys())
    lista_sanse = list(procente_grimoire.values())
    raritate_cautata = random.choices(lista_raritati, weights=lista_sanse, k=1)[0]

    optiuni_abilitati = [
        id_ab for id_ab, date in baze_date_abilitati.items()
        if date.get("raritate") == raritate_cautata and id_ab not in jucator["abilitati"]
    ]

    if not optiuni_abilitati:
        print(f"\n[INFO] Ai nimerit raritatea [{raritate_cautata.upper()}], dar știi deja toate tehnicile din ea!")
        print("-> Energia reziduală îți oferă în schimb 50 GOLD!")
        jucator["gold"] += 50
    else:
        abilitate_noua = random.choice(optiuni_abilitati)
        jucator["abilitati"].append(abilitate_noua)
        nume_ab_print = baze_date_abilitati[abilitate_noua]["nume"].upper()
        print(f"\n✨ REVELAȚIE! ({raritate_cautata.upper()}) Creierul tău a asimilat: {nume_ab_print}! ✨")

    time.sleep(3)

def meniu_grimoire(jucator, baze_date_abilitati, sanse_grimoire):
    while True:
        curatare_ecran()
        toate_grimoire_urile = list(jucator["grimoires"].keys())

        optiune_iesire = afisare_inventar_grimoire(jucator, toate_grimoire_urile)

        alegere = input(f"\nAlege o opțiune (1-{optiune_iesire}): ").strip()
        if alegere == str(optiune_iesire):
            break

        if not alegere.isdigit() or int(alegere) < 1 or int(alegere) > len(toate_grimoire_urile):
            print("Opțiune invalidă! Introdu un număr corespunzător grimoire-urilor.")
            time.sleep(1.5)
            continue

        index_ales = int(alegere) - 1
        grimoire_ales = toate_grimoire_urile[index_ales]

        if jucator["grimoires"][grimoire_ales] <= 0:
            print(f"\n Nu deții niciun {grimoire_ales.replace('_', ' ').upper()}!")
            time.sleep(1.5)
            continue

        deschidere_grimoire(jucator, grimoire_ales, baze_date_abilitati, sanse_grimoire)

def meniu_inventar(jucator):
    while True:
        curatare_ecran()
        print("\n" + "="*60)
        print(f"🎒 INVENTAR CENTRALIZAT & STATISTICI: {jucator.get('nume', 'Eroul Principal').upper()} 🎒")
        print("="*60)

        print("\n📊 STATISTICI DE BAZĂ:")
        print(f"  • ❤️ HP Actual: {jucator['hp']} / {jucator['hp_max']}")
        print(f"  • 🧪 MANA Actuală: {jucator['mana']} / {jucator['mana_max']}")
        print(f"  • 💰 GOLD Deținut: {jucator['gold']} monede")
        print(f"  • 📍 Cameră Curentă: Camera {jucator['camera_curenta']}")
        print("-" * 50)

        print("\n ECHIPAMENT PURTAT (EQUIPMENT):")
        if "equipments" in jucator and jucator["equipments"]:
            for slot, item in jucator["equipments"].items():
                print(f"  • [{slot.upper()}]: {item['id'].upper()} (+{item.get('level', 0)})")
        else:
            print(" Nu deții niciun echipament în RAM.")
        print("-" * 50)

        print("\n MATERIALE DE CRAFTING & UPGRADE:")
        if jucator.get("materiale"):
            are_materiale = False
            for material, cantitate in jucator["materiale"].items():
                if cantitate > 0:
                    print(f"  • {material.upper()}: {cantitate} bucăți")
                    are_materiale = True
            if not are_materiale:
                print("  • Rucsacul de resurse este complet gol.")
        else:
            print(" Nu există structura de materiale în inventar.")
        print("-" * 50)

        print("\n ABILITĂȚI ȘI TIPURI DE EFECTE:")
        print("   Abilități Active în Sloturi:")
        if "abilitati" in jucator and jucator["abilitati"]:
            for ab in jucator["abilitati"]:
                print(f"    - 🔥 {ab.upper()}")
        else:
            print("    - Fără abilități active.")
            
        print("  Pasive Active:")
        if "pasive" in jucator and jucator["pasive"]:
            for pasiva in jucator["pasive"]:
                print(f"    - ✨ {pasiva.get('nume', pasiva).upper()}")
        else:
            print(" - Fără efecte pasive active.")
        print("-" * 50)

        print("\n PERKS & DEALS ACTIVE:")
        if "pasive" in jucator and jucator["pasive"]:
            print(f" Perks: {', '.join([str(p).upper() for p in jucator['perks']])}")
        else:
            print(" Nu ai pasive active")

        print("\n PERKS & DEALS ACTIVE:")
        perks_list = jucator.get("perks", [])
        print(f"  • Perks active: {', '.join([str(p).upper() for p in perks_list]) if perks_list else 'Fără binecuvântări'}")
        
        deals_list = jucator.get("deals", [])
        print(f"  • Deals încheiate: {', '.join([str(d).upper() for d in deals_list]) if deals_list else 'Fără pacte active'}")
        print("="*60)

        print("  1. Închide inventarul și revino în temniță")
        print("-" * 60)

        optiune = input("Alege acțiunea: ").strip()
        if optiune == "1":
            print("\nÎnchizi rucsacul...")
            break

def salveaza_progresul(jucator, nume_fisier="salvare_joc.json"):
    try:
        with open(nume_fisier, "w", encoding="utf-8") as fisier:
            json.dump(jucator, fisier, indent=4)
        print("\n[SALVARE] Progresul tău a fost salvat cu succes!")
    except Exception as e:
        print(f"\n[EROARE] Nu s-a putut salva jocul: {e}")

def incarca_progresul(nume_fisier="salvare_joc.json"):
    try:
        with open(nume_fisier, "r" ,encoding="utf-8") as fisier:
            date_jucator = json.load(fisier)
        print("\n[ÎNCĂRCARE] Bine ai revenit! Progresul a fost încărcat.")
        return date_jucator
    except FileNotFoundError:
        print("\n[INFO] Nu s-a găsit nicio salvare anterioară. Începe o aventură nouă!")
        return None

def transformare_jucator(jucator):
    if jucator["jucator_transformare"] and not jucator["jucator_transformare_verificare"]:
        jucator["hp_max"] -= (jucator["hp_max"] * 30) // 100
        if jucator["hp_max"] < jucator["hp"]:
            jucator["hp"] = jucator["hp_max"]
        jucator["physical_dmg"] = (jucator["physical_dmg"] * 120) // 100
        jucator["magic_dmg"] = (jucator["magic_dmg"] * 110) // 100
        jucator["jucator_transformare_verificare"] = True
        print("Ai suferit mutatii")
        time.sleep(1)

def genereaza_camera_random(jucator, baze_date_inamici, este_corupta=False):
    optiuni = [id_inamic for id_inamic, date in baze_date_inamici.items()
               if date["camera_minima"] <= jucator["camera_curenta"] <= date["camera_maxima"]]

    id_ales = random.choice(optiuni)    
    inamic_nou = deepcopy(baze_date_inamici[id_ales])
    inamic_nou["statusuri_active"] = {}
    procent_crestere = 1 + (jucator["camera_curenta"] * 0.05)
    inamic_nou["hp"] = int(inamic_nou["hp"] * procent_crestere)
    inamic_nou["hp_max"] = int(inamic_nou["hp_max"] * procent_crestere)

    for atac in inamic_nou["abilitati"]:
        if "dmg" in atac:
            atac["dmg"] += (jucator["camera_curenta"] // 2)

    if este_corupta:
        inamic_nou["hp"] = (inamic_nou["hp"] * 200) // 100
        for atac in inamic_nou["abilitati"]:
            if "dmg" in atac:
                atac["dmg"] = (atac["dmg"] * 150) // 100

        inamic_nou["nume"] = f" corrupted_{inamic_nou['nume']}"

    return inamic_nou

def camera_corupta():
    curatare_ecran()
    print("\n  AERUL DEVINE GREU ȘI CORUPT... CAMERA ESTE BLESTEMATĂ! ")
    print("Simți o prezență malefică uriașă care păzește un Grimoire secret...")
    time.sleep(2.5)

def camera_regenerare_afisare(jucator):
    noroc_jucator = jucator.get("luck", 0)

    factor_noroc = max(0.5, 1 + (noroc_jucator / 100))

    regenerare_mana = int((jucator["camera_curenta"] * setari_echilibru["scala_regenerare_mana"]) * factor_noroc)
    jucator["mana"] += regenerare_mana
    if jucator["mana"] > jucator["mana_max"]: 
        jucator["mana"] = jucator["mana_max"]

    regenerare_stamina = int((jucator["camera_curenta"] * setari_echilibru["scala_regenerare_stamina"]) * factor_noroc)
    jucator["stamina"] += regenerare_stamina
    if jucator["stamina"] > jucator["stamina_max"]: 
        jucator["stamina"] = jucator["stamina_max"]

    regenerare_hp = int((jucator["camera_curenta"] * setari_echilibru["scala_regenerare_hp"]) * factor_noroc)
    jucator["hp"] += regenerare_hp
    if jucator["hp"] > jucator["hp_max"]: 
        jucator["hp"] = jucator["hp_max"]

    print("\n=== CAMERĂ DE ODREHNĂ ȘI MEDITAȚIE ===")
    print("Găsești un altar vechi plin de energie magică.")

    if noroc_jucator > 0:
        print(f"✨ Norocul tău a amplificat energia altarului cu {int(noroc_jucator)}%!")

    print(f"Altarul ți-a restaurat: +{regenerare_hp} HP | +{regenerare_mana} MANA | +{regenerare_stamina} STAMINA")

def generare_oferte_perks(baze_date_perks, sanse_raritati_perks):
    lista_raritati = list(sanse_raritati_perks.keys())
    ponderi_sanse = list(sanse_raritati_perks.values())
    optiuni_alese = []

    while len(optiuni_alese) < 3:
        raritate_aleasa = random.choices(lista_raritati, weights=ponderi_sanse, k=1)[0]
        perk_valide = [id_p for id_p, date in baze_date_perks.items() if date.get("raritate") == raritate_aleasa]

        if perk_valide:
            perk_ales = random.choice(perk_valide)
            if perk_ales not in optiuni_alese:
                optiuni_alese.append(perk_ales)

    return optiuni_alese

def afisare_marfa_perks(optiuni_alese, baze_date_perks, etichete_raritate):
    for i, id_perk in enumerate(optiuni_alese, start=1):
        perk = baze_date_perks[id_perk]
        chei_valide = [k for k in perk.keys() if "bonus" in k or "sansa" in k]
        nume_bonus = chei_valide[0] if chei_valide else "tip"
        valoare_bonus = perk[nume_bonus]

        rar_text = etichete_raritate.get(perk.get("raritate", "comun"), "⚪ COMUN")
        print(f"{i}. [{rar_text}{Fore.RESET}] {perk['nume'].upper()} -> (+{valoare_bonus} {nume_bonus.replace('_', ' ')}) [{perk['tip'].upper()}]")

    print("4. Refuza (Pleaca mai departe fara perk")

def alegere_perk(jucator, optiuni_alese, baze_date_perks):
    while True:
        alegere = input("Introduce optiunea (1-3): ").strip()

        if alegere in ["1", "2", "3"]:

            index_ales = int(alegere) - 1

            id_perk_ales = optiuni_alese[index_ales]

            if aplicare_perk(jucator, id_perk_ales, baze_date_perks):
                time.sleep(2)
                break
            else:
                time.sleep(2)
        else:
            print("\nOpțiune invalidă! Introdu un număr între 1 și 3.")
            time.sleep(1.5)

def verifica_spawn_deal_misterios(jucator):
    noroc = jucator.get("luck", 0)

    sansa_angel = min(25, max(2, 10 + (noroc // 4)))
    sansa_devil = min(25, max(2, 10 - (noroc // 8)))

    zar_eveniment = random.randint(1, 100)

    if zar_eveniment <= sansa_angel:
        return "angel", sansa_angel
    elif zar_eveniment <= (sansa_angel + sansa_devil):
        return "devil", sansa_devil
    else:
        return None, 0 

def executa_tranzactie_deal(jucator, oferta, tip_deal, scade_bonus=False):
    if tip_deal == "angel":
        if "cost_gold" in oferta:
            cost_aur = oferta["cost_gold"]
            if jucator["gold"] < cost_aur:
                print(f"Aur insuficient! Îți trebuie {cost_aur} GOLD, dar ai doar {jucator['gold']}.")
                return False
            jucator["gold"] -= cost_aur

    else:
        for k_pay, v_pay in oferta["pay_off"].items():
            stat_real = k_pay.replace("pay_", "")

            if stat_real == "hp_max" and jucator["hp_max"] <= v_pay:
                print(" Pact refuzat! Forța ta vitală este prea scăzută pentru acest sacrificiu!")
                return False
            elif jucator.get(stat_real, 0) < v_pay:
                print(f" Demonul îți cere {v_pay} {stat_real.upper()}, dar tu ai doar {jucator.get(stat_real, 0)}.")
                return False
                

        for k_pay, v_pay in oferta["pay_off"].items():
            stat_real = k_pay.replace("pay_", "")
            jucator[stat_real] -= v_pay
            if stat_real == "hp_max" and jucator["hp"] > jucator["hp_max"]:
                jucator["hp"] = jucator["hp_max"]

    for k_bonus, val_bonus in oferta.items():
        if k_bonus.startswith("bonus_"):
            if k_bonus.endswith("_multiplicativ"):
                stat_real = k_bonus.replace("bonus_", "").replace("_multiplicativ", "")
                if scade_bonus:
                    jucator[stat_real] = jucator[stat_real] - (jucator[stat_real] * val_bonus) // 100
                    print(f"📉 [DEZACHIPARE] {stat_real.upper()} a scăzut multiplicativ conform formulei.")
                else:
                    jucator[stat_real] = jucator[stat_real] + (jucator[stat_real] * val_bonus) // 100
                    print(f"📈 [ECHIPARE] {stat_real.upper()} a crescut multiplicativ conform formulei.")

            else:
                stat_real = k_bonus.replace("bonus_", "")

                if scade_bonus:
                    jucator[stat_real] -= val_bonus
                else:
                    jucator[stat_real] += val_bonus

    return True

def afisare_deal_misterios(jucator, tip_deal, sansa_afisata, id_uri_oferte, oferte_disponibile):
    if tip_deal == "angel":
        print(f"O LUMINĂ SFÂNTĂ INUNDĂ ÎNCĂPEREA... ANGEL DEAL (Sansa: {sansa_afisata}%)! ✨")
    else:
        print(f"🔥 AERUL DEVINE APĂSĂTOR ȘI MIROASE A SULF... DEVIL DEAL (Sansa: {sansa_afisata}%)! 🔥")
    print("="*60)
    print(f"STATUSUL TĂU: HP: {jucator['hp']}/{jucator['hp_max']} | Gold: {jucator['gold']} | Luck: {jucator['luck']}")
    print("-" * 60)

    for i, id_oferta in enumerate(id_uri_oferte, start=1):
        oferta = oferte_disponibile[id_oferta]
        beneficii = [f"+{v} {k.replace('bonus_', '').upper()}" for k, v in oferta.items() if k.startswith("bonus_")]
        costuri = [f"-{v} {k.replace('pay_', '').upper()}" for k, v in oferta["pay_off"].items()] if "pay_off" in oferta else [f"{oferta.get('cost_gold', 100)} GOLD"]

        print(f"{i}. {id_oferta.upper()}\n   🎁 Beneficii: [{', '.join(beneficii)}]\n   ❌ Cost: [{', '.join(costuri)}]\n" + "-"*40)

    print(f"{len(id_uri_oferte) + 1}. Refuză pactul și mergi mai departe.\n" + "-"*60)

def obtinere_alegere_jucator_deal(jucator, id_uri_oferte, oferte_disponibile, tip_deal):
    while True:
        alegere = input("Alege o opțiune (1-3): ").strip()
        
        if alegere in ["1", "2"]:
            idx = int(alegere) - 1
            id_ales = id_uri_oferte[idx]
            oferta = oferte_disponibile[id_ales]
            
            if executa_tranzactie_deal(jucator, oferta, tip_deal):
                print(f"\n🎉 Parteneriat incheiat cu succes! Ai dobandit: {id_ales.upper()}!")
                jucator["deals"].append(id_ales)
                time.sleep(2)
                return True
            else:
                time.sleep(1)
                continue
                
        elif alegere == "3":
            print("\nAi refuzat fortele mistice si mergi mai departe...")
            time.sleep(1.5)
            return True
        else:
            print("Optiune invalida. Incearca din nou.")

def camera_deal_misterioasa(jucator, baze_date_deals):
    tip_deal, sansa_afisata = verifica_spawn_deal_misterios(jucator)
    if tip_deal is None:
        return False

    oferte_disponibile = baze_date_deals[tip_deal]
    id_uri_oferte = list(oferte_disponibile.keys())

    afisare_deal_misterios(jucator, tip_deal, sansa_afisata, id_uri_oferte, oferte_disponibile)

    return obtinere_alegere_jucator_deal(jucator, id_uri_oferte, oferte_disponibile, tip_deal)

def camera_regenerare(jucator, baze_date_deals):
    curatare_ecran()
    camera_regenerare_afisare(jucator)
    camera_deal_misterioasa(jucator, baze_date_deals)

def level_up(jucator, baze_date_perks, sanse_raritati_perks):
    if jucator["exp"] < jucator["exp_necesar"]:
        return False

    jucator["nivel"] += 1
    jucator["exp"] -= jucator["exp_necesar"]
    jucator["exp_necesar"] = (jucator["exp_necesar"] * 110) // 100

    print("\n" + "⚡"*20)
    print(f"🎉 LEVEL UP! Ai atins Nivelul {jucator['nivel']}! 🎉")
    print("⚡"*20)

    jucator["hp_max"] += 10
    jucator["mana_max"] += 20
    jucator["stamina_max"] += 5
    print(f"Staturi noi: {jucator["hp_max"]}Hp Max, {jucator["mana_max"]}Mana Max, {jucator["stamina_max"]}Stamina Max")

    if jucator["nivel"] % 5 == 0:
        jucator["physical_red"] += 1
        jucator["magic_red"] += 1
        print("🛡️ Bonus de rezistență minor: +1 Physical/Magic Reduction!")

    if jucator["nivel"] in baze_date_milestones:
        date_milestone = baze_date_milestones[jucator["nivel"]]

        executa_tranzactie_deal(jucator, date_milestone, "angel")
        print(date_milestone["text"])
        print("-" * 60)

    etichete_raritate = raritati()

    optiuni_alese = generare_oferte_perks(baze_date_perks, sanse_raritati_perks)
    afisare_marfa_perks(optiuni_alese, baze_date_perks, etichete_raritate)
    alegere_perk(jucator, optiuni_alese, baze_date_perks)

def mystery_shop_afisare(jucator):
    print("\n=== SHOP-UL MISTERIOS AL TEMNIȚEI ===")
    print("Un negustor ciudat îți arată trei obiecte acoperite de praf.")
    print(f"Banii tăi: {jucator['gold']} GOLD\n")

def raritati():
    etichete_raritate = {
        "comun": f"{Fore.WHITE}{Style.BRIGHT}⚪ COMUN",
        "rar": f"{Fore.BLUE}{Style.BRIGHT}🔵 RAR",
        "epic": f"{Fore.MAGENTA}{Style.BRIGHT}🟣 EPIC",
        "legendar": f"{Fore.YELLOW}{Style.BRIGHT}🟡 LEGENDAR",
        "mythic": f"{Fore.RED}{Style.BRIGHT}🔴 Mythic"
    }
    return etichete_raritate

def generare_oferte_shop(baze_date_equipments, sanse_raritati_equipments):
    lista_raritati = list(sanse_raritati_equipments.keys())
    ponderi_sanse = list(sanse_raritati_equipments.values())

    optiuni_shop = []

    while len(optiuni_shop) < 3:
        raritate_aleasa = random.choices(lista_raritati, weights=ponderi_sanse, k=1)[0]
        equipments_valide = [id_eq for id_eq, date in baze_date_equipments.items() if date.get("raritate") == raritate_aleasa]
        
        if equipments_valide:
            equipment_ales = random.choice(equipments_valide)
            if equipment_ales not in optiuni_shop:
                optiuni_shop.append(equipment_ales)

    return optiuni_shop

def afisare_marfa_shop(optiuni_shop, baze_date_equipments, etichete_raritate):
    for i, id_eq in enumerate(optiuni_shop, start=1):
        equipment = baze_date_equipments[id_eq]

        chei_valide = [k for k in equipment.keys() if "bonus" in k or "sansa" in k]
        text_toate_bonusuri = ""
        if chei_valide:
            bucati_bonus = []
            for nume_bonus in chei_valide:
                valoare_bonus = equipment[nume_bonus]
                nume_curat = nume_bonus.replace('_', ' ')
                bucati_bonus.append(f"+{valoare_bonus} {nume_curat}")
            text_toate_bonusuri = " | " + " + ".join(bucati_bonus)

        rar_text = etichete_raritate.get(equipment.get("raritate", "comun"), "⚪ COMUN")
        slot_curat = equipment["slot"].replace('equipment_', '').upper()

        print(f"{i}. {equipment['nume'].upper()} ({slot_curat}) -> Pret: {equipment['pret']} GOLD{text_toate_bonusuri} [{rar_text}]")

    print("4. Pleaca din magazin (Refuza marfa)")

def alegere_equipment(jucator, optiuni_shop, baze_date_equipments):
    while True:
        alegere = input("Introduce optiunea (1-4): ").strip()

        if alegere in ["1", "2", "3"]:
            index_ales = int(alegere) - 1

            id_obiect_ales = optiuni_shop[index_ales]
            item = baze_date_equipments[id_obiect_ales]

            if jucator["gold"] < item["pret"]:
                print(f"\n[EȘEC] Nu ai destul gold! Îți trebuie {item['pret']} GOLD. (Ai: {jucator['gold']})")
                time.sleep(2)
                continue

            jucator["gold"] -= item["pret"]
            slot_vizat = item["slot"]

            if jucator[slot_vizat] != False:
                obiect_vechi = baze_date_equipments[jucator[slot_vizat]]
                executa_tranzactie_deal(jucator, obiect_vechi, "angel", scade_bonus=True)
                print(f"\n[DISTRUGERE] Echipamentul vechi a fost distrus!")
                time.sleep(1.5)

            jucator[slot_vizat] = id_obiect_ales
            executa_tranzactie_deal(jucator, item, "angel")
            print(f"\n[SUCCES] Ai cumpărat și echipat {item['nume'].upper()}!")
            time.sleep(2)
            return True

        elif alegere == "4":
            print("\nL-ai ignorat si te-ai dus mai departe, cumva a fost ceva ineregula cu stock-ul?")
            time.sleep(1.5)
            return True

        else:
            print("\nOpțiune invalidă! Introdu un număr între 1 și 4.")
            time.sleep(1.5)

def mystery_shop(jucator, baze_date_equipments, sanse_raritati_equipments):
    curatare_ecran()
    mystery_shop_afisare(jucator)
    etichete_raritate = raritati()

    optiuni_shop = generare_oferte_shop(baze_date_equipments, sanse_raritati_equipments)
    afisare_marfa_shop(optiuni_shop, baze_date_equipments, etichete_raritate)

    alegere_equipment(jucator, optiuni_shop, baze_date_equipments)

def afisare_pregatire_main(jucator):
    print(f"\n=== MENIU PREGĂTIRE (Înainte de Camera {jucator['camera_curenta']}) ===")
    print(f"Bani: {jucator['gold']} GOLD | HP: {jucator['hp']}/{jucator['hp_max']}")
    print("-" * 30)
    print("1. Avansează în următoarea cameră")
    print("2. Deschide Grimoire-uri")
    print("3. Deschide inventarul")

def afisare_intrare_camera(jucator):
    print(f"\n ▲ INTRI ÎN CAMERA {jucator['camera_curenta']} ▲")
    print(f"Bani: {jucator['gold']} GOLD | HP: {jucator['hp']}/{jucator['hp_max']}")
    print("-" * 30)

def afiseaza_meniu_upgrade_blacksmith(jucator, mapare_sloturi):
    print("\n" + "="*50)
    print("🔨 FIERĂRIE: UPGRADE ECHIPAMENT PURTAT 🔨")
    print("="*50)

    for tasta, slot in mapare_sloturi.items():
        item = jucator["equipment"][slot]
        print(f"{tasta}. Upgradează {slot.upper()}: {item['id'].upper()} (+{item['level']})")

    tasta_iesire = len(mapare_sloturi) + 1
    print(f"{len(mapare_sloturi) + 1}. Iesire shop")
    print("-" * 50)
    return tasta_iesire

def cauta_reteta_upgrade(id_obiect, baze_date_blacksmith):
    for k, v in baze_date_blacksmith.items():
        if v["nume_obiect"].lower() == id_obiect.lower():
            return v
    return None

def verifica_materiale_upgrade(jucator, cerinte_upgrade):
    for material, cantitate_necesara in cerinte_upgrade.items():
        material_real = material.replace("_needed", "")
        cantitate_detinuta = jucator["materiale"].get(material_real, 0)

        if cantitate_detinuta < cantitate_necesara:
            print(f"❌ Lipsă resurse: Ai nevoie de {cantitate_necesara}x {material_real.upper()}, dar deții doar {cantitate_detinuta}!")
            return False
    return True

def retrage_materiale_upgrade(jucator, cerinte_upgrade):
    for k_needed, cantitate_necesara in cerinte_upgrade.items():
        material_real = k_needed.replace("_needed", "")
        jucator["materiale"][material_real] -= cantitate_necesara

def aplica_tranzactie_upgrade(jucator, reteta_gasita, obiect_purtat, nivel_actual):
    id_obiect = obiect_purtat["id"]

    obiect_scalat_vechi = calculeaza_atribute_upgrade_brut(reteta_gasita, nivel_actual)
    executa_tranzactie_deal(jucator, obiect_scalat_vechi, "angel", scade_bonus=True)

    obiect_purtat["level"] += 1
    noul_nivel = obiect_purtat["level"]

    obiect_scalat_nou = calculeaza_atribute_upgrade_brut(reteta_gasita, noul_nivel)
    executa_tranzactie_deal(jucator, obiect_scalat_nou, "angel")

    print(f"\n🔥 BUM! Fierarul izbește cu ciocanul! {id_obiect.upper()} a fost upgradat la +{noul_nivel}!")
    print(f"✨ Statisticile obiectului au crescut dinamic cu +25% în starea ta!")

def equipment_upgrade_blacksmith(jucator, baze_date_blacksmith):
    mapare_sloturi = {
        "1": "head",
        "2": "ring"
    }
    tasta_iesire = afiseaza_meniu_upgrade_blacksmith(jucator, mapare_sloturi)
    alegere = input("Ce slot vrei să bagi în cuptorul fierarului? ").strip()

    if alegere == str(tasta_iesire):
        print("\nTe întorci la meniul principal al fierăriei...")
        return True

    if alegere not in mapare_sloturi:
        print("❌ Opțiune invalidă!")
        return False

    slot_vizat = mapare_sloturi[alegere]
    obiect_purtat = jucator["equipment"][slot_vizat]
    nivel_actual = obiect_purtat["level"]

    if nivel_actual >= 5:
        print(f"❌ {obiect_purtat.upper()} este deja la nivelul maxim (+5)!")
        return False

    reteta_gasita = cauta_reteta_upgrade(obiect_purtat["id"], baze_date_blacksmith)

    if reteta_gasita == None:
        print("❌ Acest obiect nu poate fi upgradat!")
        return False

    cerinte_upgrade = reteta_gasita["upgrades"]
    if not verifica_materiale_upgrade(jucator, cerinte_upgrade):
        print("❌ Upgrade eșuat. Strânge mai multe materiale din dungeon.")
        return False

    retrage_materiale_upgrade(jucator, cerinte_upgrade)

    aplica_tranzactie_upgrade(jucator, reteta_gasita, obiect_purtat, nivel_actual)

    return True

def calculeaza_atribute_upgrade_brut(reteta_item, nivel):
    obiect_simulat = {"bonusuri": {}}
    multiplicator = 100 + (nivel * 25)

    for k,v in reteta_item["bonusuri"].items():
        obiect_simulat["bonusuri"][k] = (v * multiplicator) // 100

    return obiect_simulat

def afisare_camera_blacksmith(jucator):
    print("\n" + "="*60)
    print("🔨 AMBIENTUL DEVINE FIERBINTE... AI INTRAT ÎN COVĂCIA FIERARULUI! 🔨")
    print("="*60)

    print("📋 INVENTARUL TĂU DE MATERIALE:")
    materiale = jucator.get("materiale", {})

    if materiale:
        for mat, cant in materiale.items():
            print(f"  • {mat.upper()}: {cant} bucăți")
    else:
        print("  • (Inventarul tău de materiale este gol)")

    print("-" * 60)

def genereaza_oferta_fierar(baze_date_blacksmith):
    toate_cheile = list(baze_date_blacksmith.items())
    numar_obiecte_alese = min(5, len(toate_cheile))
    chei_selectate = random.sample(toate_cheile, k=numar_obiecte_alese)

    mapare_oferta_curenta = {}
    for i, cheie_veche in enumerate(chei_selectate, start=1):
        mapare_oferta_curenta[str(i)] = baze_date_blacksmith[cheie_veche]

    return mapare_oferta_curenta

def afisare_oferte_fierar(mapare_oferta_curenta):
    print("🔨 OFERTA FIERARULUI DE ASTĂZI (Echipamente disponibile):")
    for optiune, reteta in mapare_oferta_curenta.items():
        print(f"  {optiune}. {reteta['text']}")

    urmatoarea_tasta_libera = len(mapare_oferta_curenta) + 1
    return urmatoarea_tasta_libera

def proceseaza_pasive_si_active(jucator, reteta):
    if "passives" not in reteta:
        return
    for ab in reteta["passives"]:
        nume_ab = ab["nume"]

        if ab["tip_abilitate"] == "passive":
            if "pasive" not in jucator:
                jucator["pasive"] = []

            if ab not in jucator["pasive"]:
                jucator["pasive"].append(ab)
                print(f"✨ PASIVĂ ACTIVATĂ: '{nume_ab.upper()}' rulează acum în fundal!")
        else:
            if "abilitati" not in jucator:
                jucator["abilitati"] = []

            if ab not in jucator["abilitati"]:
                jucator["abilitati"].append(ab)
                print(f"⚡ ABILITATE ACTIVĂ: '{nume_ab.upper()}' a fost adăugată în meniu!")\
                
def craft_equipment_blacksmith(jucator, baze_date_blacksmith):
    print("\n" + "="*60)
    mapare_oferta_curenta = genereaza_oferta_fierar(baze_date_blacksmith)
    afisare_oferte_fierar(mapare_oferta_curenta)

    tasta_inapoi = str(len(mapare_oferta_curenta) + 1)

    while True:
        alegere_craft = input("Alege ce rețetă vrei să forjezi (sau tasta de înapoi): ").strip()

        if alegere_craft == tasta_inapoi:
            print("\nTe întorci la meniul principal al fierăriei...")
            return True

        if alegere_craft in mapare_oferta_curenta:
            reteta = mapare_oferta_curenta[alegere_craft]

            if not verifica_materiale_upgrade(jucator, reteta["cerinte"]):
                print("❌ Încearcă altă rețetă sau apasă tasta de înapoi.")
                continue

            retrage_materiale_upgrade(jucator, reteta["cerinte"])

            executa_tranzactie_deal(jucator, reteta, "angel")

            proceseaza_pasive_si_active(jucator, reteta)

            print(f"\n🔨 BUM! Fierarul izbește cu ciocanul și craftează: {reteta['nume_obiect'].upper()}! ✨")
            input("\nApasă Enter pentru a continua...")
        else:
            print("❌ Rețetă invalidă! Introdu un număr corect din meniu.")

def camera_blacksmith(jucator, baze_date_blacksmith):
    departamente = {
        "1": {"text": "🔨 CRAFTEAZĂ un echipament nou (Deschide Taraba)", "actiune": "craft"},
        "2": {"text": "🔥 UPGRADEAZĂ un echipament purtat (Deschide Cuptorul)", "actiune": "upgrade"}
    }

    tasta_iesire = str(len(departamente) + 1)

    while True:
        afisare_camera_blacksmith(jucator)
        print("Alege ce acțiune vrei să execute fierarul:")

        for tasta, date in departamente.items():
            print(f"  {tasta}. {date['text']}")
        print(f"  {tasta_iesire}. 🚪 Părăsește fierăria.\n" + "-" * 60)

        alegere = input("Alege ce vrei să forjezi: ").strip()

        if alegere == tasta_iesire:
            print("\nIeși din fierărie... Căldura cuptorului se stinge în spatele tău.")
            return True

        elif alegere in departamente:
            actiune_vizata = departamente["alegere"]["actiune"]

            if actiune_vizata == "craft":
                craft_equipment_blacksmith(jucator, baze_date_blacksmith)

            elif actiune_vizata == "upgrade":
                equipment_upgrade_blacksmith(jucator, baze_date_blacksmith)
                input("\nApasă Enter pentru a te întoarce la fierar...")
        else:
            print("❌ Opțiune invalidă!")

if __name__ == "__main__":
    curatare_ecran()
    print("=== BINE AI VENIT ÎN TEMNIȚĂ ===")
    print("1. Joc Nou")
    print("2. Continuă (Încarcă Salvare)")

    optiune = input("\nAlege (1-2): ").strip()
    if optiune == "2":
        salvare_gasita = incarca_progresul()
        if salvare_gasita:
            jucator = salvare_gasita
            time.sleep(2)

    time.sleep(1)

    while jucator["hp"] > 0:
        curatare_ecran()
        transformare_jucator(jucator)

        afisare_pregatire_main(jucator)
        optiune_meniu = input("Alege optiunea (1-2): ").strip()

        if optiune_meniu == "2":
            meniu_grimoire(jucator, baze_date_abilitati, sanse_grimoire)
            continue

        if optiune_meniu == "3":
            meniu_inventar(jucator)
            continue

        curatare_ecran()
        afisare_intrare_camera(jucator)
        time.sleep(1.5)

        zar_coruptie = random.randint(1, 100)
        if zar_coruptie <= 10 and jucator["camera_curenta"] % 10 != 0:
            camera_corupta()
            inamic_curent = genereaza_camera_random(jucator, baze_date_inamici, este_corupta=True)
            lupta_camera(jucator, inamic_curent, este_corupta=True)
        else:
            if jucator["camera_curenta"] <= 2:
                inamic_curent = genereaza_camera_random(jucator, baze_date_inamici)
                lupta_camera(jucator, inamic_curent)
            elif jucator["camera_curenta"] % 10 == 0:
                inamic_curent = genereaza_camera_random(jucator, baze_date_inamici)
                lupta_camera(jucator, inamic_curent, este_corupta=True)
            else:
                zar_eveniment = random.randint(1, 100)

                if zar_eveniment <= 60:
                    inamic_curent = genereaza_camera_random(jucator, baze_date_inamici)
                    lupta_camera(jucator, inamic_curent)

                elif zar_eveniment <= 75:
                    camera_regenerare(jucator, baze_date_perks, sanse_raritati_perks)

                elif zar_eveniment <= 90:
                    camera_blacksmith(jucator, baze_date_blacksmith)

                else:
                    mystery_shop(jucator, baze_date_equipments, sanse_raritati_equipments)

        if jucator["hp"] > 0:
            level_up(jucator, baze_date_perks, sanse_raritati_perks)
            jucator["camera_curenta"] += 1
            print(f"Avansezi in camera {jucator['camera_curenta']}")
            salveaza_progresul(jucator)
            time.sleep(2)

            if jucator["jucator_stun"]:
                jucator["jucator_stun"] = False
                print("\n[CLEANSE] Te-ai liniștit în timpul tranziției și ți-ai revenit din amețeală (Stun)!")
                time.sleep(1.5)
        else:
            print("\n GAME OVER! Ai murit în temniță.")
            print(f"Ai ajuns până la Camera {jucator['camera_curenta']}.")
            break