import random
import time
import os
import subprocess
import sys
from copy import deepcopy
import json

jucator = {
    "hp": 200, "hp_max": 200,
    "damage_baza": 20, "red": 10, "gold": 0,
    "mana": 500, "camera_curenta": 1, 
    "lifesteal": 0, "bleed": 0, "poison": 0, "infection": 0,
    "jucator_transformare": False,
    "jucator_transformare_verificare": False,
    "jucator_stun": False,
    "abilitati": ["pumn", "fireball"],
    "perks": [],
    "perk_damage": False,
    "perk_hp": False,
    "perk_lifesteal": False,
    "perk_red": False,
    "perk_chill": False,
    "equipment_cap": False,
    "equipment_picioare": False,
    "equipment_piept": False,
    "equipment_inel": False,
    "equipment_sabie": False
}

def curatare_ecran():
    if os.name == 'nt':
        subprocess.run('cls', shell=True)
    else:
        subprocess.run('clear', shell=True)

print_original = print

def print(*args, **kwargs):
    text_complet = " ".join(str(arg) for arg in args)
    for litera in text_complet:
        sys.stdout.write(litera)
        sys.stdout.flush()
        time.sleep(0.02)
    print_original(**kwargs)

inamic = {}

baze_date_inamici = {
    "zombie": {
        "nume": "zombie", "hp": 130, "red": 10, "sansa_evaziva": False,
        "abilitati": [
            {"nume": "Muscatura", "dmg": 10, "lifesteal": 5, "infection": 1},
            {"nume": "Pumn", "dmg": 15}
        ]
    },
    "skelete": {
        "nume": "skelete", "hp": 100, "red": 7, "sansa_evaziva": False,
        "abilitati": [
            {"nume": "Aruncare Os", "dmg": 10, "stun_jucator": 1},
            {"nume": "Sword Slash", "dmg": 20, "bleed": 3},
            {"nume": "Pumn", "dmg": 15},
            {"nume": "Picior", "dmg": 15}
        ]
    },
    "elf": {
        "nume": "elf", "hp": 90, "red": 9, "sansa_evaziva": True,
        "abilitati": [
            {"nume": "Bow Shot", "dmg": 15},
            {"nume": "Bow Barrage", "dmg": 25},
            {"nume": "Dizzy Arrow", "dmg": 10, "stun_jucator": 1},
            {"nume": "Circular Arrow", "dmg": 20}
        ]
    },
    "goblin": {
        "nume": "goblin", "hp": 110, "red": 8, "sansa_evaziva": True,
        "abilitati": [
            {"nume": "Dagger Slash", "dmg": 15, "bleed": 2},
            {"nume": "Pickpocket", "dmg": 0,"furat_gold": 20},
            {"nume": "Stealth Attack", "dmg": 10, "stun_jucator": 1},
            {"nume": "Flash Attack", "dmg": 20}
        ]
    },
    "slime": {
        "nume": "slime", "hp": 500, "red": 4, "sansa_evaziva": False,
        "abilitati": [
            {"nume": "Acid Shot", "dmg": 15, "poison": 2},
            {"nume": "Mancat", "dmg": 10, "bonus_red": 2, "bonus_hp": 5},
            {"nume": "Dizolva", "dmg": 15, "size": 40}
        ]
    },
}

baze_date_perks = {
    "dmg_perk": {"nume": "dmg_perk", "bonus_damage": 10, "tip": "ofensiv"},
    "hp_perk": {"nume": "hp_perk", "bonus_hp": 30, "tip": "defensiv"},
    "lifesteal_perk": {"nume": "lifesteal_perk", "bonus_lifesteal": 5, "tip": "ofensiv"},
    "red_perk": {"nume": "red_perk", "bonus_red": 3, "tip": "defensiv"},
    "chill_perk": {"nume": "chill_perk", "sansa_inghetare": 10, "tip": "ofensiv"}
}

baze_date_equipments = {
    "casca_de_lemn": {"nume": "casca_de_lemn", "bonus_red": 1, "bonus_hp": 10, "tip": "defensiv", "raritate": "comun", "pret": 20, "slot": "equipment_cap"},
    "iron_chestplate": {"nume": "iron_chestplate", "bonus_red": 3, "bonus_hp": 20, "tip": "defensiv", "raritate": "comun", "pret": 40, "slot": "equipment_piept"},
    "sabie_oase": {"nume": "sabie_oase", "bonus_damage": 15, "efect_sangerare": 2, "tip": "ofensiv", "raritate": "comun", "pret": 35, "slot": "equipment_sabie"},
    "fire_ring": {"nume": "fire_ring", "bonus_damage": 5, "efect_burn": 3, "tip": "ofensiv", "raritate": "comun", "pret": 30, "slot": "equipment_inel"},
    "leather_boots": {"nume": "leather_boots", "bonus_red": 2, "bonus_hp": 15, "tip": "defensiv", "raritate": "comun", "pret": 25, "slot": "equipment_picioare"},
}

def atac_inamic_universal(inamic, jucator):

    atac_ales = random.choice(inamic["abilitati"])

    dmg_atac = atac_ales.get("dmg", 0)
    lifesteal_atac = atac_ales.get("lifesteal", 0)
    aur_furat = atac_ales.get("furat_gold", 0)
    bonus_reduction = atac_ales.get("bonus_red", 0)
    bonus_hp = atac_ales.get("bonus_hp", 0)
    bleed_atac = atac_ales.get("bleed", 0)
    jucator_stun = atac_ales.get("stun_jucator", 0)
    jucator["infection"] += atac_ales.get("infection", 0)
    poison_atac = atac_ales.get("poison", 0)
    size_slime  = atac_ales.get("size", 0)

    damage_final = (dmg_atac * 10) // jucator["red"]

    jucator["hp"] -= damage_final
    if jucator["hp"] < 0:
        jucator["hp"] = 0

    print(f"\n{inamic['nume'].upper()} foloseste {atac_ales['nume']}!")
    print(f"Ti-a dat {damage_final} DMG")

    if lifesteal_atac > 0 and damage_final > 0:
        viata_furata = damage_final // lifesteal_atac
        inamic["hp"] += viata_furata
        print(f"{inamic['nume']}, si a furat {viata_furata}HP!")

    if aur_furat > 0:
        if jucator["gold"] >= aur_furat:
            jucator["gold"] -= aur_furat
            print(f"PICKPOCKET! Ti-a furat {aur_furat} GOLD!")
        else:
            print(f"PICKPOCKET! SARAC! Ti-a furat doar {jucator['gold']} GOLD pe care ii mai aveai")
            jucator["gold"] = 0

    if bleed_atac > 0:
        jucator["bleed"] = bleed_atac
        print(f"Ai fost taiat! Vei Sangera timp de {bleed_atac} ture")

    if bonus_reduction > 0:
        inamic["red"] += bonus_reduction
        print("Slime-ul a devenit mai rezistent")

    if bonus_hp > 0:
        inamic["hp"] += bonus_hp
        print("Slime-ul devine putin mai mare")

    if jucator_stun > 0:
        jucator["jucator_stun"] = True

    if jucator["infection"] >= 5:
        jucator["jucator_transformare"] = True

    if poison_atac > 0:
        jucator["poison"] = poison_atac
        print(f"Ai fost otravit! Efectul se duce in {poison_atac} ture")

    if size_slime > 0:
        print(f"Slime-ul dizolva si creste in dimensiune (SIZE +{size_slime})")
        inamic["hp"] += size_slime

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
        jucator["hp_max"] -= 30
        if jucator["hp_max"] < jucator["hp"]:
            jucator["hp"] = jucator["hp_max"]
        jucator["damage_baza"] += 10
        jucator["jucator_transformare_verificare"] = True
        print("Ai suferit mutatii")
        time.sleep(1)

def genereaza_camera_random(jucator, baze_date_inamici):

    if jucator["camera_curenta"] < 5:
        optiuni = ["zombie", "skelete", "elf"]
    elif jucator["camera_curenta"] < 10:
        optiuni = ["zombie", "skelete", "elf", "goblin",]
    elif jucator["camera_curenta"] == 10:
        optiuni = ["slime"]
    else:
        optiuni = ["zombie", "skelete", "elf", "goblin"]

    id_ales = random.choice(optiuni)    
    inamic_nou = deepcopy(baze_date_inamici[id_ales])
    inamic_nou["burn"] = 0
    inamic_nou["bleed"] = 0
    inamic_nou["inghetat"] = False
    procent_crestere = 1 + (jucator["camera_curenta"] * 0.05)
    inamic_nou["hp"] = int(inamic_nou["hp"] * procent_crestere)
    for atac in inamic_nou["abilitati"]:
        if "dmg" in atac:
            atac["dmg"] += (jucator["camera_curenta"] // 2)

    return inamic_nou

def verificare_stun (jucator):

    if jucator["jucator_stun"] == True:
        print("Esti stunned si nu poti ataca")
        jucator["jucator_stun"] = False
        time.sleep(2)
        return True
    return False

def abilitate_pumn(jucator, inamic):
    jucator["mana"] += 15

    atac = random.randint(1, 5)

    if atac in [1, 2, 3, 4]:
        damage_dat = (jucator["damage_baza"] * 10) // inamic["red"]
        viata_furata = (damage_dat * jucator["lifesteal"]) // 100
        jucator["hp"] += viata_furata
        print(f"Ai furat {viata_furata}HP")
        if jucator["hp"] > jucator["hp_max"]:
            jucator["hp"] = jucator["hp_max"]

        inamic["hp"] -= damage_dat
        if inamic["hp"] < 0:
            inamic["hp"] = 0

        print(f"Lovitura directa! I-ai provocat {damage_dat} DMG lui {inamic['nume'].upper()}")

    elif atac == 5:
        damage_dat = ((jucator["damage_baza"] + 10) * 10) // inamic["red"]
        viata_furata = (damage_dat * jucator["lifesteal"]) // 100
        jucator["hp"] += viata_furata
        print(f"Ai furat {viata_furata}HP")
        inamic["hp"] -= damage_dat
        if inamic["hp"] < 0:
            inamic["hp"] = 0

        print(f"Critica! I-ai provocat {damage_dat} DMG lui {inamic['nume'].upper()}")

def abilitate_fireball(jucator, inamic):

    if jucator["mana"] >= 50:
        jucator["mana"] -= 50
        atac = random.randint(1, 3)

        if atac in [1, 2]:
            damage_dat = ((jucator["damage_baza"] + 10) * 10) // (inamic["red"] if inamic["red"] <= 10 else 10)
            inamic["hp"] -= damage_dat
            if inamic["hp"] < 0:
                inamic["hp"] = 0
            print(f"Ai lansat o bila de foc! I-ai provocat {damage_dat} DMG lui {inamic['nume'].upper()}")
            inamic["burn"] = 3
            print(f"{inamic['nume'].upper()}-ul a luat foc pentru {inamic['burn']} ture")
        elif atac == 3:
            damage_dat = ((jucator["damage_baza"] + 35) * 10) // (inamic["red"] if inamic["red"] <= 10 else 10)
            inamic["hp"] -= damage_dat
            if inamic["hp"] < 0:
                inamic["hp"] = 0
            print(f"Ai lansat mai multe bile de foc! I-ai provocat {damage_dat} DMG lui {inamic['nume'].upper()}")
            inamic["burn"] = 4
            print(f"{inamic['nume'].upper()}-ul a luat foc pentru {inamic['burn']} ture")

def efecte_DoT(jucator, inamic):
    if jucator.get("bleed", 0) > 0:
        jucator["hp"] -= 10
        jucator["bleed"] -= 1
        print(f"Sangerezi! Pierzi  10HP! (Ture ramase: {jucator['bleed']})")
        time.sleep(1.5)

    if inamic.get("bleed", 0) > 0:
        inamic["hp"] -= 10
        inamic["bleed"] -= 1
        print(f"{inamic['nume'].upper()}-ul sangereaza si pierde 10HP! (Ture ramase: {inamic['bleed']})")
        time.sleep(1.5)

    if jucator.get("poison", 0) > 0:
        jucator["hp"] -= 15
        jucator["poison"] -= 1
        print(f"Otrava isi face efectul! Pierzi  15HP! (Ture ramase: {jucator['poison']})")
        time.sleep(1.5)

    if inamic.get("burn", 0) > 0:
        inamic["hp"] -= 15
        inamic["burn"] -= 1
        print(f"{inamic['nume'].upper()}-ul arde in flacari! Pierde 15HP! (Ture ramase: {inamic['burn']}")
        time.sleep(1.5)

    if jucator["hp"] < 0:
        jucator["hp"] = 0
    if inamic["hp"] < 0:
        inamic["hp"] = 0

def primire_loot(jucator):
        gold_castigat = random.randint(15, 35) + (jucator["camera_curenta"] * 2)
        jucator["gold"] += gold_castigat
        print(f"Ai primit {gold_castigat} gold. Total: {jucator['gold']} monede.")
        time.sleep(1.5)

def equipment_efect(inamic, jucator, baze_date_equipments):
    sabie_id = jucator.get("equipment_sabie")
    inel_id = jucator.get("equipment_inel")
    
    bleed_total = 0
    burn_total = 0
    
    if sabie_id in baze_date_equipments:
        bleed_total += baze_date_equipments[sabie_id].get("efect_sangerare", 0)
        burn_total += baze_date_equipments[sabie_id].get("efect_burn", 0)
        
    if inel_id in baze_date_equipments:
        bleed_total += baze_date_equipments[inel_id].get("efect_sangerare", 0)
        burn_total += baze_date_equipments[inel_id].get("efect_burn", 0)
        
    if bleed_total > 0:
        sansa = random.randint(1, 100)
        if sansa <= 20: 
            inamic["bleed"] = bleed_total  
            print(f"\n{inamic['nume'].upper()}-ul sangereaza pentru {bleed_total} ture!")
        else: pass
        
    if burn_total > 0:
        sansa = random.randint(1, 100)
        if sansa <= 20:
            inamic["burn"] = burn_total 
            print(f"\n{inamic['nume'].upper()}-ul arde pentru {burn_total} ture!")
        else: pass

def afiseaza_abilitati():
    print("\nAlege abilitatea:")
    print("1. Pumnn (+15 MANA)")
    print("2. Fireball (-50 MANA)")

def alegere_atac(inamic, jucator):

    while True:
        afiseaza_abilitati()

        alegere = input("\n Introduce optiunea: ").strip()

        if inamic["sansa_evaziva"] == True and random.randint(1, 100) <= 30:
            print("Inamicul este agil si s-a ferit de atac")
            time.sleep(1.5)
            break
        else:
            if alegere == "1":
                abilitate_pumn(jucator, inamic)
                time.sleep(1.5)
                break
            elif alegere == "2":
                abilitate_fireball(jucator, inamic)
                time.sleep(1.5)
                break
            else:
                print("Alege o varianta existenta")
                time.sleep(1.5)

def verificare_moarte_inamic(jucator, inamic):
    if inamic["hp"] <= 0:
        print(f"\n{inamic['nume'].upper()}-ul a murit!")
        primire_loot(jucator)
        return True
    return False

def verificare_inamic_inghetat(inamic):
    if inamic["inghetat"]:
        print("Inamicul este inghetat si nu poate ataca")
        time.sleep(1.5)
        return True
    return False


def lupta_camera(jucator, inamic):
    while inamic["hp"] > 0 and jucator["hp"] > 0:
        curatare_ecran()
        print(f"\n==== Inamic: {inamic['nume'].upper()} ==== ")
        print(f" HP Inamic: {inamic['hp']} HP") 
        print("-" * 20)
        print(f"\n Jucator: {jucator['hp']}/{jucator['hp_max']} HP | Mana: {jucator['mana']}/500")
        print("-" * 20)

        efecte_DoT(jucator, inamic)

        if jucator["hp"] <= 0: 
            print(f"Te-a omorat {inamic['nume'].upper()}-ul")
            break

        if verificare_moarte_inamic(jucator, inamic): break
        if verificare_stun(jucator):
            time.sleep(1.5)
        else:
            alegere_atac(inamic, jucator)
            equipment_efect(inamic, jucator, baze_date_equipments)
            if jucator["perk_chill"]:
                sansa = random.randint(1, 100)
                if sansa <= 10:
                    inamic["inghetat"] = True
                    print("Ai inghetat inamicul")
                    time.sleep(1.5)

        if verificare_moarte_inamic(jucator, inamic): break
        if verificare_inamic_inghetat(inamic): 
            inamic["inghetat"] = False
        else:
            atac_inamic_universal(inamic, jucator)
            time.sleep(1.5)

        if jucator["hp"] <= 0: 
            print(f"Te-a omorat {inamic['nume'].upper()}-ul")
            break

def aplicare_perk(jucator, id_perk_ales, baze_date_perks):
    perk = baze_date_perks[id_perk_ales]

    if "bonus_damage" in perk and not jucator["perk_damage"]:
        jucator["damage_baza"] += perk["bonus_damage"]
        print(f"\n[PERK ACTIVAT] Damage-ul tău de bază a crescut cu +{perk['bonus_damage']}!")
        jucator["perk_damage"] = True

    elif "bonus_hp" in perk and not jucator["perk_hp"]:
        jucator["hp"] += perk["bonus_hp"]
        jucator["hp_max"] += perk["bonus_hp"]
        print(f"\n[PERK ACTIVAT] HP Max a crescut cu +{perk['bonus_hp']}!")
        jucator["perk_hp"] = True

    elif "bonus_lifesteal" in perk and not jucator["perk_lifesteal"]:
        jucator["lifesteal"] += perk["bonus_lifesteal"]
        print(f"\n[PERK ACTIVAT] Lifesteal-ul tău a crescut cu +{perk['bonus_lifesteal']}%!")
        jucator["perk_lifesteal"] = True

    elif "bonus_red" in perk and not jucator["perk_red"]:
        jucator["red"] += perk["bonus_red"]
        print(f"\n[PERK ACTIVAT] Rezistența ta a crescut cu +{perk['bonus_red']}!")
        jucator["perk_red"] = True

    elif "sansa_inghetare" in perk and not jucator["perk_chill"]:
        print(f"\n[PERK ACTIVAT] Ai o sansa sa ingheti inamicul cand ataci!")
        jucator["perk_chill"] = True
    else:
        print("\n[EXPLOIT BLOCAT] Ai deja acest perk activat! Alege altul.")
        return False
    return True

def camera_regenerare(jucator, baze_date_perks):
    curatare_ecran()
    jucator["mana"] = 500
    jucator["hp"] += 50
    if jucator["hp"] > jucator["hp_max"]:
        jucator["hp"] = jucator["hp_max"]
    print("\n=== CAMERĂ DE ODREHNĂ ȘI MEDITAȚIE ===")
    print("Găsești un altar vechi plin de energie magică.")
    print("Alege un perk pentru a-ți modifica permanent statisticile:\n")

    toate_id_urile = list(baze_date_perks.keys())
    optiuni_alese = random.sample(toate_id_urile, 3)

    for i, id_perk in enumerate(optiuni_alese, 1):
        perk = baze_date_perks[id_perk]
        chei_valide = [k for k in perk.keys() if "bonus" in k or "sansa" in k]
        nume_bonus = chei_valide[0] if chei_valide else "tip"
        valoare_bonus = perk[nume_bonus]
        print(f"{i}. {perk['nume'].upper()} -> (+{valoare_bonus} {nume_bonus.replace('_', ' ')}) [{perk['tip'].upper()}]")

    print("4. Refuza (Pleaca mai departe fara perk")

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

def mystery_shop(jucator, baze_date_equipments):
    curatare_ecran()
    print("\n=== SHOP-UL MISTERIOS AL TEMNIȚEI ===")
    print("Un negustor ciudat îți arată trei obiecte acoperite de praf.")
    print(f"Banii tăi: {jucator['gold']} GOLD\n")

    toate_id_urile = list(baze_date_equipments.keys())
    optiuni_shop = random.sample(toate_id_urile, 3)

    for i, id_obiect in enumerate(optiuni_shop, 1):
        item = baze_date_equipments[id_obiect]

        chei_valide = [k for k in item.keys() if "bonus" in k or "efect" in k]
        nume_bonus = chei_valide[0] if chei_valide else "tip"
        valoare_bonus = item[nume_bonus]

        print(f"{i}. {item['nume'].upper()} ({item['slot'].replace('equipment_', '').upper()}) -> Pret: {item['pret']} GOLD | (+{valoare_bonus} {nume_bonus.replace('_', ' ')}) [{item['raritate'].upper()}]")

    print("4. Pleaca din magazin (Refuza marfa)")

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
                obiect_vechi_id = jucator[slot_vizat]
                obiect_vechi = baze_date_equipments[obiect_vechi_id]

                if "bonus_hp" in obiect_vechi:
                    jucator["hp_max"] -= obiect_vechi["bonus_hp"]
                    if jucator["hp"] > jucator["hp_max"]:
                        jucator["hp"] = jucator["hp_max"]
                if "bonus_red" in obiect_vechi:
                    jucator["red"] -= obiect_vechi["bonus_red"]
                if "bonus_damage" in obiect_vechi:
                    jucator["damage_baza"] -= obiect_vechi["bonus_damage"]

                print(f"\n[DISTRUGERE] Echipamentul vechi ({obiect_vechi_id.upper()}) a fost distrus!")
                time.sleep(1.5)

            jucator[slot_vizat] = id_obiect_ales

            if "bonus_hp" in item:
                jucator["hp_max"] += item["bonus_hp"]
                jucator["hp"] += item["bonus_hp"]
            if "bonus_red" in item:
                jucator["red"] += item["bonus_red"]
            if "bonus_damage" in item:
                jucator["damage_baza"] += item["bonus_damage"]

            print(f"\n[SUCCES] Ai cumpărat și echipat {item['nume'].upper()} pe {slot_vizat.replace('equipment_', '').upper()}!")
            time.sleep(2)
            break

        elif alegere == "4":
            print("\nL-ai ignorat si te-ai dus mai departe, cumva a fost ceva ineregula cu stock-ul?")
            time.sleep(1.5)
            break

        else:
            print("\nOpțiune invalidă! Introdu un număr între 1 și 4.")
            time.sleep(1.5)

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

        print(f"\n▲ INTRI ÎN CAMERA {jucator['camera_curenta']} ▲")
        print(f"Bani: {jucator['gold']} GOLD | HP: {jucator['hp']}/{jucator['hp_max']}")
        print("-" * 30)
        time.sleep(1.5)

        if jucator["camera_curenta"] <= 2 or jucator["camera_curenta"] == 10:
            inamic_curent = genereaza_camera_random(jucator, baze_date_inamici)
            lupta_camera(jucator, inamic_curent)
        else:
            zar_eveniment = random.randint(1, 100)

            if zar_eveniment <= 60:
                inamic_curent = genereaza_camera_random(jucator, baze_date_inamici)
                lupta_camera(jucator, inamic_curent)

            elif zar_eveniment <= 80:
                camera_regenerare(jucator, baze_date_perks)

            else:
                mystery_shop(jucator, baze_date_equipments)

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