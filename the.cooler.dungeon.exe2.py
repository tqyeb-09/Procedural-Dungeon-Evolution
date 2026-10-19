import random
import time
import os
import subprocess
import sys
from copy import deepcopy
import json
import colorama
from colorama import Fore, Style

from baze_date2 import baze_date_inamici, baze_date_abilitati, baze_date_equipments, baze_date_perks, baze_date_grimoires, sanse_grimoire, sanse_raritati_perks, sanse_raritati_equipments

from combat2 import lupta_camera, curatare_ecran, aplicare_perk

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
    "dmg_multiplicativ": 100,
    "physical_red": 10, 
    "magic_red" : 5,
    "red_multiplicativ": 100,
    "mana": 500, 
    "mana_max" : 500,
    "stamina": 100, 
    "stamina_max": 100,
    "camera_curenta": 1, 
    "gold": 0,
    "crit_chance": 10, 
    "crit_dmg": 2,
    "infection": 0,
    "jucator_transformare": False,
    "jucator_transformare_verificare": False,
    "jucator_stun": False,
    "statusuri_active": {},
    "abilitati": [
        "pumn", 
        "fireball"
    ],
    "perks": [],
    "cooldowns": {},
    "grimoires": {
        "grimoire_comun": 0,
        "grimoire_rar": 0,
        "grimoire_epic": 0,
        "grimoire_legendar": 0,
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
    jucator["mana"] = 500
    jucator["hp"] += 50
    if jucator["hp"] > jucator["hp_max"]:
        jucator["hp"] = jucator["hp_max"]
    print("\n=== CAMERĂ DE ODREHNĂ ȘI MEDITAȚIE ===")
    print("Găsești un altar vechi plin de energie magică.")
    print("Alege un perk pentru a-ți modifica permanent statisticile:\n")

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

def alegere_perk_shop(jucator, optiuni_alese, baze_date_perks):
    while True:
        alegere = input("Introduce optiunea (1-4): ").strip()

        if alegere in ["1", "2", "3"]:

            index_ales = int(alegere) - 1

            id_perk_ales = optiuni_alese[index_ales]

            if aplicare_perk(jucator, id_perk_ales, baze_date_perks):
                time.sleep(2)
                break
            else:
                time.sleep(2)

        elif alegere == "4":
            print("\nAi refuzat altarul. Mergi mai departe în temniță...")
            time.sleep(1.5)
            break
        else:
            print("\nOpțiune invalidă! Introdu un număr între 1 și 4.")
            time.sleep(1.5)

def camera_regenerare(jucator, baze_date_perks, sanse_raritati_perks):
    curatare_ecran()
    camera_regenerare_afisare(jucator)

    etichete_raritate = raritati()

    optiuni_alese = generare_oferte_perks(baze_date_perks, sanse_raritati_perks)
    afisare_marfa_perks(optiuni_alese, baze_date_perks, etichete_raritate)
    alegere_perk_shop(jucator, optiuni_alese, baze_date_perks)

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
                for prop, val in obiect_vechi.items():
                    if prop.startswith("bonus_"):
                        prop_reala = prop.replace("bonus_", "")
                        if prop_reala in jucator:
                            jucator[prop_reala] -= val
                print(f"\n[DISTRUGERE] Echipamentul vechi a fost distrus!")
                time.sleep(1.5)

            jucator[slot_vizat] = id_obiect_ales
            for prop, val in item.items():
                if prop.startswith("bonus_"):
                    prop_reala = prop.replace("bonus_", "")
                    if prop_reala in jucator:
                        jucator[prop_reala] += val
            print(f"\n[SUCCES] Ai cumpărat și echipat {item['nume'].upper()}!")
            time.sleep(2)
            break

        

        elif alegere == "4":
            print("\nL-ai ignorat si te-ai dus mai departe, cumva a fost ceva ineregula cu stock-ul?")
            time.sleep(1.5)
            break

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

def afisare_intrare_camera(jucator):
    print(f"\n ▲ INTRI ÎN CAMERA {jucator['camera_curenta']} ▲")
    print(f"Bani: {jucator['gold']} GOLD | HP: {jucator['hp']}/{jucator['hp_max']}")
    print("-" * 30)

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
                inamic_curent = genereaza_camera_random(jucator, baze_date_inamici, este_corupta=False)
                lupta_camera(jucator, inamic_curent, este_corupta=False)
            elif jucator["camera_curenta"] % 10 == 0:
                inamic_curent = genereaza_camera_random(jucator, baze_date_inamici, este_corupta=False)
                lupta_camera(jucator, inamic_curent, este_corupta=True)
            else:
                zar_eveniment = random.randint(1, 100)

                if zar_eveniment <= 60:
                    inamic_curent = genereaza_camera_random(jucator, baze_date_inamici, este_corupta=False)
                    lupta_camera(jucator, inamic_curent, este_corupta=False)

                elif zar_eveniment <= 80:
                    camera_regenerare(jucator, baze_date_perks, sanse_raritati_perks)

                else:
                    mystery_shop(jucator, baze_date_equipments, sanse_raritati_equipments)

        if jucator["hp"] > 0:
            if jucator["jucator_stun"]:
                jucator["jucator_stun"] = False
                print("\n[CLEANSE] Te-ai liniștit în timpul tranziției și ți-ai revenit din amețeală (Stun)!")
                time.sleep(1.5)

        if jucator["hp"] > 0:
            jucator["camera_curenta"] += 1
            print(f"Avansezi in camera {jucator['camera_curenta']}")
            salveaza_progresul(jucator)
            time.sleep(2)
        else:
            print("\n GAME OVER! Ai murit în temniță.")
            print(f"Ai ajuns până la Camera {jucator['camera_curenta']}.")
            break