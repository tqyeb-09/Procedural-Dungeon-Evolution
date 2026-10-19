import random
import time
import os
import subprocess
import sys
jucator = {
    "frenzy": False,
    "jucator_stun": 0,
    "inamic_stun": False,
    "bloodlust": False,
    "energie": 0,
    "damage_reduction": 1,
    "burn": 0,
    "burn_damage": 60,
    "burn_jucator": 0,
    "burn_jucator_damage": 20,
    "sangerare": 0,
    "sangerare_jucator": 0,
    "sangerare_jucator_damage": 10,
    "sangerare_damage": 40,
    "inventar": {
        "sabie" : 1,
        "potiune_viata" : 3
    },
    "jucator_viata": 200,
    "jucator_viata_maxima": 400,
    "jucator_viata_maxima_cap": False,
    "jucator_gold": 0,
    "camera_curenta": "camera_1",
    "nivel": 1,
    "damage_baza": 25,
    "damage_final": 0,
    "damage_final_jucator": 0,
    "inamic_damage": 0,
    "inamic_damage_redus": 0
}

harta = {
    "camera_1": {
        "descriere": "Ai intrat in dungeon, si vezi un goblin",
        "directia": {
            "fata": "camera_2",
            "spate": "iesire_dungeon"
        }
    },

    "camera_2": {
        "descriere": "Avansezi in urmatoarea camera si vezi un orc masiv",
        "directia": {
            "fata": "camera_3",
            "spate": "camera_1"
        }
    },

    "camera_3": {
        "descriere": "Avansezi in urmatoarea camera si dai de un skelete",
        "directia": {
            "fata": "camera_4",
            "spate": "camera_2"
        }
    },

    "camera_4": {
        "descriere": "Ai intrat intr-o camera goala, dintr-o data o runa de pe jos incepe sa se ridice in aer si se inconjuara cu piatra, s-a format un golem de piatra",
        "directia": {
            "fata": "camera_5",
            "spate": "camera_3"
        }
    },

    "camera_5": {
        "descriere": """Avansezi in ultima camera, totusi este putin mai diferita cu un craniu la usa ei
                        Intri in camera
                        La inceput arata normal dar incepe un cutremur
                        Pamantul crapa si iese lava din el
                        Din lava apare un demon""",
        "directia": {
            "fata": "camera_comori",
            "spate": "camera_4"
        }
    },

    "camera_secreta": {
        "descriere": """Fiends core ul incepe sa straluceasca.
                        Inchizi ochii
                        Ii deschizi incet si realizezi ca ai fost teleportat
                        Ai dat de o hydra cu 9 capete""",
        "directie": {
            "fata": "camera_comori"
        } 
    },

    "camera_comori": {
        "descriere": "Felicitari ai terminat definitiv dungeonul si ai gasit comoara cea mare",
        "directie": {}
    }
}

baza_date_inamici = {
    "camera_1": {"nume": "goblin", "viata": 150, "damage_reduction": 1, "viata_maxima": 150},
    "camera_2": {"nume": "orc", "viata": 300, "damage_reduction": 2, "viata_maxima": 300},
    "camera_3": {"nume": "skelete", "viata": 200, "damage_reduction": 0.5, "viata_maxima": 200},
    "camera_4": {"nume": "golem", "viata": 400, "damage_reduction": 2.5, "viata_maxima": 400},
    "camera_5": {"nume": "demon", "viata": 500, "damage_reduction": 1.5, "viata_maxima": 500},
}

inamic = {}

def curata_ecran():
    if os.name == 'nt':
        subprocess.run('cls', shell=True)
    else:
        subprocess.run('clear', shell=True)

def limite_viata():
    if jucator["jucator_viata"] < 0:
        jucator["jucator_viata"] = 0
    if inamic["viata"] < 0:
        inamic["viata"] = 0

print_original = print

def print(*args, **kwargs):

    text_complet = " ".join(str(arg) for arg in args)

    for litera in text_complet:
        sys.stdout.write(litera)
        sys.stdout.flush()
        time.sleep(0.02)

    print_original(**kwargs)
    
def intrare_camera_secreta():
    if jucator["inventar"].get("fiends_core", 0):
        jucator["camera_curenta"] = "camera_secreta"

def calculeaza_energie():
    return random.choice([20, 25, 30, 35, 40])

def limita_energie():
    if jucator["energie"] > 100:
        jucator["energie"] = 100

def afiseaza_abilitati():
    limita_energie()
    print(f"\nJucator viata: {jucator["jucator_viata"]}HP   Inamic viata: {inamic["viata"]}HP")
    print(f"\nAi {jucator["energie"]} energie")
    print("\nAtacuri:")
    print("\n1.Pumn (+10E/-30E)")
    if jucator["nivel"] >= 2:
        print("\n2. Slash (-40E)")
    else:
        print("\n2. [BLOCAT] ??? (Deblocat la Nivel 2)")
    if jucator["nivel"] >= 3:
        print("\n3. Skull Crusher (-60E)")
    else:
        print("\n3. [BLOCAT] ??? (Deblocat la Nivel 3)")
    if jucator["nivel"] >= 5:
        print("\n4. Inferno (-100E)")
    else:
        print("\n4. [BLOCAT] ??? (Deblocat la Nivel 5)")

def alegere_atac():
    curata_ecran()
    afiseaza_abilitati()

    alegere = input("\nAlege abilitatea (1-4): ").strip().lower()

    if alegere == "1":
        atac_normal()
    elif alegere == "2":
        atac_slash()
    elif alegere == "3":
        skull_crusher()
    elif alegere == "4":
        inferno()
    else:
        print("\nAi ezitat si ai pierdut tura")
    
        
def atac_normal():

    if jucator["jucator_stun"]:
        time.sleep(1)
        print("\nEsti stunned si nu poti ataca")
        time.sleep(2)
        jucator["jucator_stun"] = False
        return
    
    while True:
        print("\n1.Basic Attack(+10E)")
        print("\n2.Charged Attack(-30E)")
        alegere = input("\nCe varianta vrei sa folosesti? ")

        if alegere == "2" and jucator["energie"] >= 30:
            jucator["energie"] -= 30
            damage = (jucator["damage_baza"] + 40) if jucator["frenzy"] else (jucator["damage_baza"] + 20)
            jucator["damage_final"] = damage // inamic["damage_reduction"]
            buffuri_echipamente()
            time.sleep(1)
            print("\nTe apropii de inamic")
            time.sleep(1)
            print("\nFentezi")
            time.sleep(1)
            print("\nInamicul este prins cu garda jos")
            time.sleep(1)
            print(f"\nCHARGED ATTACK! -{jucator["damage_final_jucator"]}HP")
            time.sleep(1)
            inamic["viata"] -= jucator["damage_final_jucator"]
            break

        elif alegere == "1":
            jucator["energie"] += 10
            limita_energie()
            atac = random.randint(1, 5)

        else:
            print("Alege o varianta disponibila")
            return

        if atac in [1, 2, 3]:
            damage = (jucator["damage_baza"] + 15) if jucator["frenzy"] else jucator["damage_baza"]
            jucator["damage_final"] = damage // inamic["damage_reduction"]
            buffuri_echipamente()
            time.sleep(1)
            print("\nTe apropii de inamic")
            time.sleep(1)
            print("\nFentezi")
            time.sleep(1)
            print("\nInamicul este prins cu garda jos")
            time.sleep(0.5)
            print(f"\nLovitura directa! -{jucator["damage_final_jucator"]}HP")
            time.sleep(1)
            print("\nTe dai in spate")
            time.sleep(3)
            inamic["viata"] -= jucator["damage_final_jucator"]
            break
        elif atac == 4:
            damage = (jucator["damage_baza"] + 35) if jucator["frenzy"] else (jucator["damage_baza"] + 10)
            jucator["damage_final"] = damage // inamic["damage_reduction"]
            buffuri_echipamente()
            time.sleep(1)
            print("\nIncepi sa alergi spre inamic")
            time.sleep(1)
            print("\nCand ajungi la el, inamicul ataca, te feresti")
            time.sleep(1)
            print("\nSi...")
            time.sleep(0.5)
            print(f"\nCritica! -{jucator["damage_final_jucator"]}HP")
            time.sleep(1)
            print("\nTe repozitionezi")
            time.sleep(3)
            inamic["viata"] -= jucator["damage_final_jucator"]
            break
        elif atac == 5:
            jucator["inamic_damage"] = (jucator["damage_baza"] + 5) if jucator["bloodlust"] else (jucator["damage_baza"] - 5)
            buffuri_echipamente()
            time.sleep(1)
            print("\nTe indrepti spre inamic cu viteza maxima")
            time.sleep(1)
            print("\nIncerci sa coplesesti inamicul cu viteza ta")
            time.sleep(1)
            print("\nDAR...")
            time.sleep(1)
            print("\nInamicul ti-a anticipat miscarea")
            time.sleep(1)
            print(f"\nLovitura directa! Inamicul te-a prins, -{jucator["inamic_damage_redus"]}HP")
            time.sleep(3)
            jucator["jucator_viata"] -= jucator["inamic_damage_redus"]
            break
    
def atac_slash():

    if jucator["nivel"] < 2:
        print("\ninca nu ai deblocat acest skill")
        time.sleep(1)
        alegere_atac()
        return

    if jucator["jucator_stun"]:
        time.sleep(1)
        print("\nEsti stunned si nu poti ataca")
        time.sleep(1)
        jucator["jucator_stun"] = False
        return

    if not jucator["inventar"].get("sabie", 0):
        print("\nNu mai ai sabia, ti-ai pierdut-o in corpul inamicului")
        return
        
    else:

        if jucator["energie"] >= 30:
            jucator["energie"] -= 30
            atac = random.randint(1, 10)

            if atac in [1, 2, 3, 4]:
                damage = (jucator["damage_baza"] + 35) if jucator["frenzy"] else (jucator["damage_baza"] + 20)
                jucator["inamic_damage"] = (jucator["damage_baza"] + 15) if jucator["bloodlust"] else jucator["damage_baza"]
                jucator["damage_final"] = damage // inamic["damage_reduction"]
                buffuri_echipamente()
                time.sleep(1)
                print("\nTi sabia sus, si incepi sa te indrepti spre inamic")
                time.sleep(1)
                print(f"\nInamicul blocheaza sabia cu propriul brat! -{jucator["damage_final_jucator"]}HP")
                time.sleep(1)
                print("\nEsti socat si confuz")
                time.sleep(1)
                print(f"\nPana sa intelegi ce se intampla, inamicul iti da un pumn care te trimite zburand! -{jucator["inamic_damage_redus"]}HP")
                time.sleep(1)
                jucator["sangerare"] = 3 if jucator["frenzy"] else 2
                print(f"\nInamicul sangereaza pentru {jucator["sangerare"]}")
                time.sleep(3)
                inamic["viata"] -= jucator["damage_final_jucator"]
                jucator["jucator_viata"] -= jucator["inamic_damage_redus"]
            elif atac in [5, 6, 7]:
                damage = (jucator["damage_baza"] + 55) if jucator["frenzy"] else (jucator["damage_baza"] + 35)
                jucator["damage_final"] = damage // inamic["damage_reduction"]
                buffuri_echipamente()
                multihit = jucator["damage_final_jucator"] // 9
                hit = jucator["damage_final_jucator"] // 3
                time.sleep(1)
                print("\nSari in aer si lansezi 3 slash-uri de aer")
                time.sleep(1)
                print("\nToata atentia inamicului este pe acele slash-uri, dar nu observa ca eu am disparut")
                time.sleep(1)
                print(f"\nDintr-o data! Apar langa inamic fara ca el sa observe si il tai pe piept! -{hit}HP")
                time.sleep(1)
                print("\nSi-a luat focusul de pe slash-uri pe tine, SI...")
                time.sleep(1)
                for _ in range(3):
                    print(f"-{multihit}HP")
                    time.sleep(0.3)
                time.sleep(1)
                print(f"\nIi dai un front kick in burta care il trimite zburand! -{hit}HP")
                time.sleep(1)
                jucator["sangerare"] = 4 if jucator["frenzy"] else 3
                print(f"Inamicul sangereaza pentru {jucator["sangerare"]}")
                inamic["viata"] -= jucator["damage_final_jucator"]
                time.sleep(3)
            elif atac in [8, 9]:
                damage = (jucator["damage_baza"] + 75) if jucator["frenzy"] else (jucator["damage_baza"] + 50)
                jucator["damage_final"] = damage // inamic["damage_reduction"]
                buffuri_echipamente()
                back_slash = jucator["damage_final_jucator"] // 3
                time.sleep(1)
                print("\nTe apropii usor de inamic")
                time.sleep(1)
                print("\nInamicul isi pierde rabdarea si incepe sa te atace")
                time.sleep(1)
                print("\nTe feresti, si contraataci")
                time.sleep(1)
                print("\nInamicul se fereste si el, contraataca, dar tu ai sarit peste el")
                time.sleep(1)
                print(f"\nInainte sa inteleaga unde ai disparut, Il tai pe spate! -{back_slash}")
                time.sleep(1)
                print(f"\nSe intoarce fara sa gandeasca, il apuci de fata si ii izbesti capul de pamant! -{back_slash}")
                time.sleep(1)
                print(f"\nInamicul se ridica dar il tai rapid! -{back_slash}HP")
                time.sleep(1)
                print("\nTe retragi in spate")
                time.sleep(1)
                jucator["sangerare"] = 5 if jucator["frenzy"] else 4
                print(f"\nInamicul sangereaza pentru {jucator["sangerare"]}")
                time.sleep(3)
                inamic["viata"] -= jucator["damage_final_jucator"]
            elif atac == 10:
                damage = (jucator["damage_baza"] + 175) if jucator["frenzy"] else (jucator["damage_baza"] + 125)
                jucator["damage_final"] = damage // inamic["damage_reduction"]
                buffuri_echipamente()
                damage_swing = jucator["damage_final_jucator"] // 4
                damage_barrage = jucator["damage_final_jucator"] // 64
                damage_thrust = jucator["damage_final_jucator"] // 2
                time.sleep(1)
                print("\nTii sabia sus indreptata cu varful spre inamic")
                time.sleep(1)
                print("\nIncepi sa dai rush spre inamic")
                time.sleep(1)
                print("\nInamicul stie ca nu are cum sa blocheze acest atac deci trebuie sa se fereasca")
                time.sleep(1)
                print("\nInamicul reuseste sa se fereasca, dar...")
                time.sleep(1)
                print("\nInamicul a picat in plasa ta, dai un swing extrem de rapid fix un ai dat predict ca inamicul se va feri")
                time.sleep(1)
                print(f"\nI-ai facut o rana adanca la piept! -{damage_swing}HP")
                time.sleep(1)
                print("\nIi dai un barrage de slash-uri cat timp este vulnerabil")
                time.sleep(1)
                for _ in range (16):
                    print(f"-{damage_barrage}HP")
                    time.sleep(0.25)
                time.sleep(1)
                print(f"\nSi termini cu un thrust! -{damage_thrust}HP")
                time.sleep(1)
                print("\nTotusi...")
                time.sleep(1)
                print("\nInamicul pune mana pe sabia ta si incepe te loveasca cu celelalt pumn")
                time.sleep(1)
                print("\nTe feresti in timp si te retragi, dar.. ti-ai pierdut sabia")
                time.sleep(1)
                jucator["sangerare"] = 6 if jucator["frenzy"] == True else 5
                print(f"\nInamicul sangereaza pentru {jucator["sangerare"]}")
                time.sleep(1)
                print("\nAi ramas fara sabie")
                del jucator["inventar"]["sabie"]
                time.sleep(3)
                inamic["viata"] -= jucator["damage_final_jucator"]
        else: 
            print("\nNu ai destula putere nici macar sa ti sabia in mana dreapta")
            time.sleep(1)
            print("\nInamicul realizeaza imediat asta si profita de moment")
            time.sleep(1)
            return

def skull_crusher():

    if jucator["nivel"] < 3:
        print("inca nu ai deblocat acest skill")
        time.sleep(1)
        alegere_atac()
        return
    
    if jucator["jucator_stun"]:
        time.sleep(1)
        print("Esti stunned si nu poti ataca")
        time.sleep(1)
        jucator["jucator_stun"] = False
        return
    else:
        if jucator["energie"] >= 50:
            jucator["energie"] -= 50
            atac = random.randint(1, 10)

            if atac in [1, 2, 3, 4, 5]:
                damage = (jucator["damage_baza"] + 55) if jucator["frenzy"] else (jucator["damage_baza"] + 35)
                jucator["damage_final"] = damage // inamic["damage_reduction"]
                buffuri_echipamente()
                damage_barrage = jucator["damage_final_jucator"] // 25
                damage_burta = jucator["damage_final_jucator"] // 10
                time.sleep(1)
                print("\nIncepi sa alergi spre inamic")
                time.sleep(1)
                print("\nNu ii dai timp sa reactioneze, ii dai un barrage de pumni continuu in garda")
                time.sleep(1)
                for _ in range(10):
                    print(f"-{damage_barrage}HP")
                    time.sleep(0.1)
                time.sleep(1)
                print(f"\nIi prinzi un pumn in burta! -{damage_burta}HP")
                time.sleep(1)
                print(f"\nIi dai un pumn in cap, dar nu cade! -{damage_burta}")
                time.sleep(1)
                print(f"\nObservi ca nu mai ai timp si ii dai un front kick ca sa il arunci departe! -{damage_burta}")
                time.sleep(3)
                inamic["viata"] -= jucator["damage_final_jucator"]
            elif atac in [6, 7, 8, 9]:
                damage = (jucator["damage_baza"] + 75) if jucator["frenzy"] else (jucator["damage_baza"] + 50)
                jucator["damage_final"] = damage // inamic["damage_reduction"]
                buffuri_echipamente()
                damage_pumn = jucator["damage_final_jucator"] // 2
                time.sleep(1)
                print("\nSari in aer spre inamic, si dai un downslam in pamant")
                time.sleep(1)
                print("\nInamicul se fereste in timp dar nu stie unde sunt de la praf")
                time.sleep(1)
                print("\nInamicul se uita peste tot, dar dintr-o data")
                time.sleep(1)
                print("\nApare un pumn fix din acel praf")
                time.sleep(1)
                print(f"\nPOWW! -{damage_pumn}HP")
                time.sleep(1)
                print("\nInamicul cade pe jos")
                time.sleep(1)
                print("\nInamicul este ametit, si imediat dupa te vede in aer cum te apropii sa ii dai un downslam fix in cap")
                time.sleep(1)
                print(f"\nOI OI, wait, wait, wait")
                time.sleep(1)
                print(f"\n-{damage_pumn}HP")
                time.sleep(1)
                print("\nL-ai facut una cu pamantul")
                time.sleep(3)
                jucator["inamic_stun"] = 1
                inamic["viata"] -= jucator["damage_final_jucator"]
            elif atac == 10:
                damage = (jucator["damage_baza"] + 95) if jucator["frenzy"] else (jucator["damage_baza"] + 65)
                jucator["damage_final"] = damage // inamic["damage_reduction"]
                buffuri_echipamente()
                damage_suplex = jucator["damage_final_jucator"] // 5
                time.sleep(1)
                print("\nTe apropii de el in pasi mici")
                time.sleep(1)
                print("\nDintr-o data... dispari")
                time.sleep(1)
                print("\nInamicul inainte sa realizeze ca ai disparut simte ceva in spatele capului sau si urmatoarea secunda")
                time.sleep(1)
                print(f"\nCapul i-a fost bagat in pamant! -{damage_suplex}HP")
                time.sleep(1)
                print("\nInamicul incearca sa reziste, dar..")
                time.sleep(1)
                print("\nIncepi sa ii dai suplexuri multiple")
                time.sleep(1)
                for _ in range(4):
                    print(f"Suplex! -{damage_suplex}HP")
                    time.sleep(3)
                print("\nInamicul pare ca si-a pierdut constiinta deocamdata")
                jucator["inamic_stun"] = 2
                inamic["viata"] -= jucator["damage_final_jucator"]
        else:
            print("\nTe indrepti spre inamic, dar esti prea equizat ca sa mai folosesti acele miscari")
            time.sleep(1)
            print("\nInamicul observa, si nu va lasa aceasta oportunitate sa scape")
            time.sleep(1)
            return

def inferno():

    if jucator["nivel"] < 5:
        print("\nInca nu ai deblocat acest skill")
        time.sleep(1)
        alegere_atac()
        return

    if jucator["jucator_stun"]:
        time.sleep(1)
        print("\nEsti stunned si nu poti ataca")
        time.sleep(1)
        jucator["jucator_stun"] = 0
        return
    else:
        limita_energie()
        if jucator["energie"] >= 100:
            jucator["energie"] = 0
            if inamic["viata"] <= inamic["viata_maxima"] * 0.30:
                input("\nIi poti da execute, apasa orice ca sa continui")
                time.sleep(1)
                print("\nIncepi sa alergi spre inamic")
                time.sleep(1)
                print("\nDintr-o data, schimbi directia si incepi sa te invarti in jurul lui")
                time.sleep(1)
                print("\nNu lasi inamicul sa se apropie si il ti departe cu vraji de foc")
                time.sleep(1)
                print("\nAi strans destul timp")
                time.sleep(1)
                print("\nAbilitate speciala Fire Cage")
                time.sleep(1)
                print("\nInamicul este prins inauntru")
                time.sleep(1)
                print("\nDin adancul pamantului unde lava fierbe")
                time.sleep(1)
                print("\nPacatul iese la suprafata si te sterge")
                time.sleep(1)
                print("\nSolul si viata in scrum se transforma")
                time.sleep(1)
                print("\nInferno se naste in flacari fara forma")
                time.sleep(1)
                print("\nULTIMATA! INFERNO!")
                time.sleep(3)
                inamic["viata"] = 0
            else:
                damage = (jucator["damage_baza"] + 175) if jucator["frenzy"] else (jucator["damage_baza"] + 125)
                jucator["damage_final"] = damage // inamic["damage_reduction"]
                buffuri_echipamente()
                time.sleep(1)
                print("\nTe apropii incet")
                time.sleep(1)
                print("\nTii o mana in spate si creezi o sabie de foc")
                time.sleep(1)
                print("\nDintr-o data te teleportezi la inamic si dai swing")
                time.sleep(1)
                print("\nInamicul abia se fereste de atac la limita dar tot este ars de sabia de foc")
                time.sleep(1)
                print("\nTe retragi putin in spate si bagi sabia de foc in pamant")
                time.sleep(1)
                print("\nDintr-o data se aude un sunet de sub pamant")
                time.sleep(1)
                print("\nInainte ca inamicul sa observe ce se intampla, sunetul ajunge sub picioare lui si pamant se ridica")
                time.sleep(1)
                print("\nInamicul incearca sa se fereasca dar nu reuseste in timp")
                time.sleep(1)
                print(f"\nInamicul este lovit de explozia de sub pamant! -{jucator["inamic_damage_redus"]}HP")
                time.sleep(1)
                print("\nInamicul este lasat inconstient si imping de explozie in aer")
                time.sleep(1)
                print("\nInamicul cade pe pamant, dar nu se misca")
                time.sleep(3)
                jucator["burn"] = 3
                print(f"Inamicul este in flacari pentru {jucator["burn"]} ture")
                jucator["inamic_stun"] = 1
                inamic["viata"] -= jucator["damage_final_jucator"]
        else:
            print("\nNu ai destula putere sa invoci flacarile infernale")
            time.sleep(1)
            print("\nInamicul profita de moment si te ataca")
            time.sleep(1)
            return

def accesare_inventar():

    while True:
        time.sleep(1)
        print("\n==== Se deschide inventarul ====")
        time.sleep(1)
        if jucator["inventar"] == {}:
            print("\nInventarul este gol")
            break

        for obiect, cantitate in jucator["inventar"].items():
            if cantitate > 0:
                print(f" {obiect} x{cantitate}")
                time.sleep(0.5)

        comanda = input("\nScrie ce item vrei sa folosesti. Daca vrei sa continui aventura apasa: ENTER ").lower().strip()

        if comanda == "":
            print("\nAi inchis inventarul")
            time.sleep(1)
            break

        elif comanda == "potiune de viata" or comanda == "potiune":
            if jucator["inventar"].get("potiune_viata", 0) > 0:
                jucator["jucator_viata"] += 150
                jucator["inventar"]["potiune_viata"] -= 1
                if jucator["jucator_viata"] > jucator["jucator_viata_maxima"]:
                    jucator["jucator_viata"] = jucator["jucator_viata_maxima"]
                print(f"\nAi baut potiunea de viata. Acum ai {jucator["jucator_viata"]}HP")
                if jucator["frenzy"] == True:
                    jucator["frenzy"] = False
                    print("\nTe-ai calmat")
                time.sleep(2)
            else:
                print("\nNu ai nicio potiune de viata in inventar! Poti cumpara o potiune de la shop daca ai destul gold, sau ca drop de la inamici")
                time.sleep(1)

        elif comanda == "sabie":
            if jucator["inventar"].get("sabie", 0) > 0:
                print("\nAi sabia pregatita si o poti folosi")
                time.sleep(2)
            else:
                print("\nAi pierdut sabia. Totusi o poti recupera de la inamici, sau o poti cumpara de la shop ")
                time.sleep(1)

        else:
            print("\nNu ai asa ceva in inventar")
            time.sleep(1)

def genereaza_drop():

    curata_ecran()

    drop_sansa = random.randint(1, 100)

    if drop_sansa <= 75 and jucator["camera_curenta"] == "camera_1":
        jucator["jucator_gold"] += 30
        print(f"\nInamicul a dropat gold. Ai {jucator["jucator_gold"]} gold")
        time.sleep(1)
    elif drop_sansa <= 80 and jucator["camera_curenta"] == "camera_2":
        jucator["jucator_gold"] += 50
        print(f"\nInamicul a dropat gold. Ai {jucator["jucator_gold"]} gold")
        time.sleep(1)
    elif drop_sansa <= 85 and jucator["camera_curenta"] == "camera_3":
        jucator["jucator_gold"] += 75
        print(f"\nInamicul a dropat gold. Ai {jucator["jucator_gold"]} gold")
        time.sleep(1)
    elif drop_sansa <= 90 and jucator["camera_curenta"] == "camera_4":
        jucator["jucator_gold"] += 100
        print(f"\nInamicul a dropat gold. Ai {jucator["jucator_gold"]} gold")
        time.sleep(1)

    drop_sansa = random.randint(1, 100)

    if  (drop_sansa <= 40 and jucator["camera_curenta"] == "camera_1") or \
        (drop_sansa <= 50 and jucator["camera_curenta"] == "camera_2") or \
        (drop_sansa <= 60 and jucator["camera_curenta"] == "camera_3") or \
        (drop_sansa <= 70 and jucator["camera_curenta"] == "camera_4"):
        
            jucator["inventar"]["potiune_viata"] += 1
            print("\nInamicul a dropat o potiune de viata")
            time.sleep(1)

    drop_sansa = random.randint(1, 100)

    if drop_sansa <= 30 and jucator["camera_curenta"] == "camera_1":
        print("\nDrop RAR! 30%")
        time.sleep(1)
        print("\nAi primit goblin dagger de la goblin")
        time.sleep(1)
        print("\nAi equipat goblin dagger si vei da cu 10% mai mult damage")
        jucator["inventar"]["goblin_dagger"] = 1
        time.sleep(1)

    if drop_sansa <= 25 and jucator["camera_curenta"] == "camera_2":
        print("\nDrop EPIC! 25%")
        time.sleep(1)
        print("\nAi primit shoulder armor de la orc")
        time.sleep(1)
        print("\nAi equipat shoulder armor si primesti cu 15% mai putin damage")
        jucator["inventar"]["shoulder_armor"] = 1
        time.sleep(1)

    if drop_sansa <= 15 and jucator["camera_curenta"] == "camera_3":
        print("\nDrop LEGENDAR! 15%")
        time.sleep(1)
        print("\nAi primit bone sword de la skeleton")
        time.sleep(1)
        print("\nAi equipat bone sword si dai cu 20% mai mult damage")
        jucator["inventar"]["bone_sword"] = 1
        time.sleep(1)

    if drop_sansa <= 10 and jucator["camera_curenta"] == "camera_4":
        print("\nDrop MYTHIC! 10%")
        time.sleep(1)
        print("\nAi primit golem's rune de la golem")
        time.sleep(1)
        print("\nAi equipat golem's rune si primesti cu 40% mai putin damage")
        jucator["inventar"]["golems_rune"] = 1
        time.sleep(1)

    if drop_sansa <= 5 and jucator["camera_curenta"] == "camera_5":
        print("\nDROP SECRET! 5%")
        time.sleep(1)
        print("\nAI PRIMIT FIEND CORE DE LA FIEND")
        time.sleep(1)
        print("\nACHIVEMENT UNLOCKED: SECRET DROP")
        jucator["inventar"]["fiends_core"] = 1
        time.sleep(1)

def accesare_shop():

    while True:

        curata_ecran()

        print(f"\nAi {jucator["jucator_gold"]} gold")
        print("\nOptiuni:")
        print("Enter to EXIT") 
        print("1.Potiune de viata 10G")
        print("2.Sabie 30G")
        print("3.Goblin dagger 50G")
        print("4.Shoulder armor 60G")
        print("5.Bone sword 80G")
        print("6.Golem's rune 100G")

        alegere = input("\nCe vrei sa cumperi? ")

        if alegere == "1":
            if jucator["jucator_gold"] < 10:
                time.sleep(1)
                print("\nNu ai destul gold")
                time.sleep(1)
            else:
                time.sleep(1)
                jucator["jucator_gold"] -= 10
                print("\nAi cumparat o potiune de viata")
                time.sleep(1)
                jucator["inventar"]["potiune_viata"] += 1
                print(f"\nAi {jucator["inventar"]["potiune_viata"]} potiuni de viata")
                time.sleep(1)

        elif alegere == "2":
            if jucator["inventar"].get("sabie", 0):
                time.sleep(1)
                print("\nDeja ai o sabie nu mai poti adauga inca una")
                time.sleep(1)
            else:
                if jucator["jucator_gold"] < 30:
                    time.sleep(1)
                    print("\nNu ai destul gold")
                    time.sleep(1)
                else:
                    time.sleep(1)
                    jucator["jucator_gold"] -= 30
                    print("\nAi cumparat o sabie")
                    time.sleep(1)
                    jucator["inventar"]["sabie"] = 1
                    print("\nAi equipat sabia")
                    time.sleep(1)

        elif alegere == "3":
            if jucator["inventar"].get("goblin_dagger", 0):
                time.sleep(1)
                print("\nDeja ai aceste equipment nu mai poti lua inca unul")
                time.sleep(1)
            else:
                if jucator["jucator_gold"] < 50:
                    time.sleep(1)
                    print("\nNu ai destul gold")
                    time.sleep(1)
                else:
                    time.sleep(1)
                    jucator["jucator_gold"] -= 50
                    print("\nAi cumparat goblin dagger")
                    time.sleep(1)
                    jucator["inventar"]["goblin_dagger"] = 1
                    print("\nAi equipat goblin dagger-ul")
                    time.sleep(1)

        elif alegere == "4":
            if jucator["inventar"].get("shoulder_armor", 0):
                time.sleep(1)
                print("\nDeja ai aceste equipment nu mai poti lua inca unul")
                time.sleep(1)
            else:
                if jucator["jucator_gold"] < 60:
                    time.sleep(1)
                    print("\nNu ai destul gold")
                    time.sleep(1)
                else:
                    time.sleep(1)
                    jucator["jucator_gold"] -= 60
                    print("\nAi cumparat shoulder armor")
                    time.sleep(1)
                    jucator["inventar"]["shoulder_armor"] = 1
                    print("\nAi equipat shoulder armor-ul")
                    time.sleep(1)

        elif alegere == "5":
                    if jucator["inventar"].get("bone_sword", 0):
                        time.sleep(1)
                        print("\nDeja ai aceste equipment nu mai poti lua inca unul")
                        time.sleep(1)
                    else:
                        if jucator["jucator_gold"] < 80:
                            time.sleep(1)
                            print("\nNu ai destul gold")
                            time.sleep(1)
                        else:
                            time.sleep(1)
                            jucator["jucator_gold"] -= 80
                            print("\nAi cumparat bone sword")
                            time.sleep(1)
                            jucator["inventar"]["bone_sword"] = 1
                            print("\nAi equipat bone sword-ul")
                            time.sleep(1)

        elif alegere == "6":
                    if jucator["inventar"].get("golems_rune", 0):
                        time.sleep(1)
                        print("\nDeja ai aceste equipment nu mai poti lua inca unul")
                        time.sleep(1)
                    else:
                        if jucator["jucator_gold"] < 100:
                            time.sleep(1)
                            print("\nNu ai destul gold")
                            time.sleep(1)
                        else:
                            time.sleep(1)
                            jucator["jucator_gold"] -= 100
                            print("\nAi cumparat golem's rune")
                            time.sleep(1)
                            jucator["inventar"]["golems_rune"] = 1
                            print("\nAi equipat golem's rune-ul")
                            time.sleep(1)

        elif alegere == "":
            break

        else:
            print("\nOptiune invalida! Apasa pe o optiune valida")
        
def buffuri_echipamente():

    jucator["damage_final_jucator"] = jucator["damage_final"]
    jucator["inamic_damage_redus"] = jucator["inamic_damage"]

    if jucator["inventar"].get("goblin_dagger", 0) > 0:
        jucator["damage_final_jucator"] += (jucator["damage_final_jucator"] * 10) // 100

    if jucator["inventar"].get("bone_sword", 0) > 0:
        jucator["damage_final_jucator"] += (jucator["damage_final_jucator"] * 20) // 100

    if jucator["inventar"].get("shoulder_armor", 0) > 0:
        jucator["inamic_damage_redus"] -= (jucator["inamic_damage_redus"] * 15) // 100

    if jucator["inventar"].get("golems_rune", 0) > 0:
        jucator["inamic_damage_redus"] -= (jucator["inamic_damage_redus"] * 40) // 100

    if jucator["inventar"].get("fiends_core", 0) > 0:
        jucator["damage_final_jucator"] += (jucator["damage_final_jucator"] * 20) // 100
        jucator["inamic_damage_redus"] -= (jucator["inamic_damage_redus"] * 50) // 100

        if not jucator["jucator_viata_maxima_cap"]:
            jucator["jucator_viata"] *= 2
            jucator["jucator_viata_maxima"] *= 2
            jucator["jucator_viata_maxima_cap"] = True

def efecte_DoT():
    if jucator.get("sangerare", 0) > 0:
        damage = jucator["sangerare_damage"]
        inamic["viata"] -= damage
        print(f"\nInamicul sangereaza! pierde {damage}HP")
        time.sleep(1)
        jucator["sangerare"] -= 1

    if jucator.get("burn", 0) > 0:
        damage = jucator["burn_damage"]
        inamic["viata"] -= damage
        print(f"\nInamicul este in flacari! pierde {damage}HP")
        time.sleep(1)
        jucator["burn"] -= 1

    if jucator.get("sangerare_jucator", 0) > 0:
        damage = jucator["sangerare_jucator_damage"]
        jucator["jucator_viata"] -= damage
        print(f"\nSangerezi! Ai pierdut {damage}HP")
        time.sleep(1)
        jucator["sangerare_jucator"] -= 1

    if jucator.get("burn_jucator", 0) > 0:
        damage = jucator["burn_jucator_damage"]
        jucator["jucator_viata"] -= damage
        print(f"\nEsti in flacari! pierzi {damage}HP")
        time.sleep(1)
        jucator["burn_jucator"] -= 1

def activare_mod():

    if jucator["jucator_viata"] <= (jucator["jucator_viata_maxima"] * 30) // 100 and jucator["frenzy"] == False:
        jucator["frenzy"] = True
        time.sleep(1)
        print("\nAi intrat in frenzy mode")
        time.sleep(1)

    if inamic["nume"] != "demon":
        return

    if inamic["viata"] <= (inamic["viata_maxima"] * 50) // 100 and jucator["bloodlust"] == False:
        jucator["bloodlust"] = True
        time.sleep(1)
        print("\nInamicul a intrat in bloodlust mode")
        time.sleep(1)

def goblin_atac():

    if jucator["inamic_stun"]:
        time.sleep(1)
        print("\nInamicul este stunned si nu va ataca tura asta")
        time.sleep(2)
    else:
        atac_random = random.randint(1, 5)

        if atac_random in [1, 2]:
            jucator["inamic_damage"] = jucator["damage_baza"] - 5
            buffuri_echipamente()
            stab_damage = jucator["inamic_damage_redus"] // 3
            time.sleep(1)
            print("\nGoblinul incepe sa alerge inspre tine tintand cu dagger-ul lui spre tine")
            time.sleep(1)
            print("\nTe feresti, dar ai cazut in plasa lui")
            time.sleep(1)
            print("\nIti da 3 stab uri")
            time.sleep(1)
            for _ in range(3):
                print(f"STAB! -{stab_damage}")
                time.sleep(0.5)
            print("\nSi se retrage in spate")
            time.sleep(3)
            jucator["sangerare_jucator"] = 3
            jucator["jucator_viata"] -= jucator["inamic_damage_redus"]

        elif atac_random in [3, 4]:
            jucator["inamic_damage"] = jucator["damage_baza"]
            buffuri_echipamente()
            damage_pamant = jucator["inamic_damage_redus"] // 2
            damage_barrage = jucator["inamic_damage_redus"] // 40
            damage_barrage_finisher = jucator["inamic_damage_redus"] // 4
            time.sleep(1)
            print("\nGoblinul foloseste stealth")
            time.sleep(1)
            print("\nTe uiti in toate directile dar nu exista nicio urma de el")
            time.sleep(1)
            print("\nDintr-o data, apare in spatele tau, fara dagger ul lui ca nu poate folosi stealth cu dagger ul")
            time.sleep(1)
            print(f"\nTe intorci rapid, dar iti apuca fata cu palma si iti baga capul in pamant! -{damage_pamant}HP")
            time.sleep(1)
            print("\nTe ridica din pamant si iti mai da un barrage de pumni")
            for _ in range(10):
                print(f"-{damage_barrage}HP")
                time.sleep(0.2)
            time.sleep(1)
            print(f"\n-{damage_barrage_finisher}HP")
            time.sleep(1)
            print("\nGoblinul te-a trimis zburand")
            time.sleep(3)
            jucator["jucator_viata"] -= jucator["inamic_damage_redus"]

        elif atac_random == 5:
            jucator["inamic_damage"] = jucator["damage_baza"] + 10
            jucator["damage_final"] = jucator["damage_baza"] + 15
            buffuri_echipamente()
            genunchi_damage = jucator["damage_final_jucator"] // 8
            aruncare_damage = jucator["inamic_damage_redus"] // 2
            time.sleep(1)
            print("\nGoblinul arunca dagger ul inspre tine")
            time.sleep(1)
            print("\nTe feresti, dar... dagger ul a fost doar o momeala")
            time.sleep(1)
            print(f"\nGoblinul iti sare in fata si iti da un axe kick direct in cap! -{jucator["inamic_damage_redus"]}HP")
            time.sleep(1)
            print("\nNu te prabusesti, il prinzi, ii dai niste genunchi in burta")
            time.sleep(1)
            for _ in range(4):
                print(f"-{genunchi_damage}HP")
                time.sleep(0.5)
            time.sleep(1)
            print(f"\nSi il arunci intr-un zid! -{aruncare_damage}HP")
            time.sleep(3)
            inamic["viata"] -= jucator["damage_final_jucator"]
            jucator["jucator_viata"] -= jucator["inamic_damage_redus"]

def orc_atac():

    if jucator["inamic_stun"]:
        time.sleep(1)
        print("\nInamicul nu isi poate lua stun")
        time.sleep(2)

    atac_random = random.randint(1, 5)

    if atac_random in [1, 2, 3]:
        time.sleep(1)
        print("\nOrcul alearga spre tine (Tot incet)")
        time.sleep(2)
        print("\nTe feresti de toate atacurile lui")
        time.sleep(1)
        print("\nSi te repozitionezi")
        time.sleep(3)

    elif atac_random == 4:
        jucator["inamic_damage"] = jucator["damage_baza"] + 25
        buffuri_echipamente()
        damage_pamant = jucator["inamic_damage_redus"] // 8
        damage_zid = jucator["inamic_damage_redus"] // 4
        time.sleep(1.5)
        print("\nOrcul incepe sa se apropie spre tine")
        time.sleep(1.5)
        print("\nEste destul de mare si incet")
        time.sleep(1)
        print("\nDin aceasta cauza il subestimezi")
        time.sleep(1)
        print("\nIncerci sa il coplesesti cu viteza ta")
        time.sleep(1.5)
        print("\nOrcul surprinzator are reflexe bune si te prinde de picior")
        time.sleep(1.5)
        print("\nIncepe sa te dea de pamant stanga dreapta")
        time.sleep(1.5)
        for _ in range(4):
            print(f"-{damage_pamant}HP")
            time.sleep(1)
        print(f"\nSi te arunca intr-un zid! -{damage_zid}HP")
        time.sleep(3)
        jucator["jucator_stun"] = True
        jucator["jucator_viata"] -= jucator["inamic_damage_redus"]

    elif atac_random == 5:
        jucator["inamic_damage"] = jucator["damage_baza"] + 35
        buffuri_echipamente()
        time.sleep(1)
        print("\nOrcul sare in aer")
        time.sleep(1)
        print("\nSe apropie de tine, si da un downslam in pamant")
        time.sleep(1)
        print("\nL-ai pierdut din cauza prafului, te uiti in jur dar nu il poti localiza")
        time.sleep(1)
        print("\nUn pumn apare din perdeaua de praf")
        time.sleep(1)
        print(f"\nTe nimereste si te trimite zburand! -{jucator["inamic_damage_redus"]}HP")
        time.sleep(3)
        jucator["jucator_viata"] -= jucator["inamic_damage_redus"]

def skelete_atac():

    if jucator["inamic_stun"]:
            time.sleep(1)
            print("\nInamicul este stunned si nu va ataca tura asta")
            time.sleep(2)
    else:
        atac_random = random.randint(1, 5)

        if atac_random in [1, 2]:
            jucator["inamic_damage"] = jucator["damage_baza"] + 15
            buffuri_echipamente()
            time.sleep(1)
            print("\nSkeletele incepe sa se apropie")
            time.sleep(1)
            print("\nSi da swing uri")
            time.sleep(1)
            print("\nTe feresti de ele")
            time.sleep(1)
            print("\nDAR...")
            time.sleep(1)
            print("\nNu te-ai asteptat ca skeletele sa isi desprinda propiul brat si sa il arunce direct spre tine")
            time.sleep(1)
            print("\nNu te poti feri in timp. Nu il poti bloca in timp")
            time.sleep(1)
            print(f"\nTi-a intrat sabia direct in piept! -{jucator["inamic_damage_redus"]}HP")
            time.sleep(1)
            print("\nSkeletele are o abilitate speciala si isi cheama inapoi bratul")
            time.sleep(3)
            jucator["jucator_viata"] -= jucator["inamic_damage_redus"]
            jucator["sangerare_jucator"] = 3

        elif atac_random in [3, 4]:
            jucator["inamic_damage"] = jucator["damage_baza"] + 20
            buffuri_echipamente()
            multi = jucator["inamic_damage_redus"] // 10
            time.sleep(1)
            print("\nSkeletele incepe sa se dezmembreze")
            time.sleep(1)
            print("\nAbilitatea lui ii permite sa isi controleze oasele")
            time.sleep(1)
            print("\nIncepe sa te atace din fiecare directie")
            time.sleep(1)
            print("\nNu poti tine pasul")
            time.sleep(1)
            print("\nChiar daca ii spargi oasele, ele au o abilitate de regenare destul de rapida")
            time.sleep(1)
            for _ in range(10):
                print(f"POW! -{multi}HP")
                time.sleep(0.4)
            time.sleep(1)
            print("\nInamicul se uneste inapoi")
            time.sleep(3)
            jucator["jucator_viata"] -= jucator["inamic_damage_redus"]

        elif atac_random == 5:
            jucator["inamic_damage"] = jucator["damage_baza"] + 50
            buffuri_echipamente()
            multi = jucator["inamic_damage_redus"] // 40
            hit = jucator["inamic_damage_redus"] // 2
            time.sleep(1)
            print("\nSkeletele incepe sa se comporte ciudat")
            time.sleep(1)
            print("\nPare ca face o incantatie")
            time.sleep(1)
            print("\nTrebuie sa il opresc acum")
            time.sleep(1)
            print("\nPREA TARZIU! ULTIMATA, BONE SWARM")
            time.sleep(1)
            print("\nSkeletele s-a transformat intr-o tornada de oase")
            time.sleep(1)
            print("\nPentru ca ai incercat sa il opresti ai fost prins direct in ea")
            time.sleep(1)
            for _ in range(20):
                print(f"-{multi}HP")
                time.sleep(0.2)
            time.sleep(1)
            print(f"\nTornada te arunca intr-un zid si esti prea ametit ca sa te mai poti misca! -{hit}HP")
            time.sleep(1)
            print("\nSkeletele si-a revenit la forma initiala")
            time.sleep(3)
            jucator["jucator_viata"] -= jucator["inamic_damage_redus"]
            jucator["jucator_stun"] = 1

def golem_atac():

    if jucator["inamic_stun"]:
        time.sleep(1)
        print("\nInamicul nu isi poate lua stun")
        time.sleep(2)

    atac_random = random.randint(1, 5)

    if atac_random in [1, 4]:
        time.sleep(1)
        print("\nGolem-ul este prea incet si te feresti de toate atacurile lui")
        time.sleep(3)

    elif atac_random == 5:
        jucator["inamic_damage"] = jucator["damage_baza"] + 125
        buffuri_echipamente()
        hit = jucator["inamic_damage_redus"] // 3
        time.sleep(1)
        print("\nGolem-ul da cu pumnii in pamant")
        time.sleep(1)
        print("\nToata camera este plina de praf")
        time.sleep(1)
        print("\nNu poti vedea dar golem-ul vede perfect cu ochii lui albi")
        time.sleep(1.5)
        print(f"\nDe nicaieri ceva gigantic te striveste si te da de pamant! -{hit}HP")
        time.sleep(1.5)
        print("\nPana sa apuci sa iti revi de la impact vezi ceva gigantic care urmeaza sa te striveasca in pamant")
        time.sleep(1.5)
        print(f"\nSTOMP! -{hit}HP")
        time.sleep(1.5)
        print(f"\nGolem-ul se apuca si te ridica din pamant si te arunca departe intr-un zid! -{hit}HP")
        time.sleep(1.5)
        print("\nEsti ametit si nu mai poti ataca")
        time.sleep(3)
        jucator["jucator_viata"] -= jucator["inamic_damage_redus"]
        jucator["jucator_stun"] = 1

def fiend_atac():

    if jucator["inamic_stun"]:
        time.sleep(1)
        print("\nInamicul nu isi poate lua stun")
        time.sleep(2)

    atac_random = random.randint(1, 10)

    if atac_random in [1, 2, 3, 4]:

        jucator["inamic_damage"] = (jucator["damage_baza"] + 75) if jucator["bloodlust"] == True else (jucator["damage_baza"] + 45)
        buffuri_echipamente()
        hit = jucator["inamic_damage_redus"] // 2
        time.sleep(1)
        print("\nDemonul se apropie spre tine")
        time.sleep(1)
        print("\nDintr-o data dispare si vezi cum ti se invarte privirea")
        time.sleep(1)
        print(f"\nDemonul te-a bagat cu capul in pamant! -{hit}HP")
        time.sleep(1)
        print(f"\nTe scoate din pamant, te arunca intr-un zid si lanseaza o bila de foc! -{hit}HP")
        time.sleep(1)
        jucator["burn_jucator"] = 3
        print("Esti in flacari!")
        time.sleep(3)
        jucator["jucator_viata"] -= jucator["inamic_damage_redus"]


    elif atac_random in [5, 6, 7]:

        jucator["inamic_damage"] = (jucator["damage_baza"] + 90) if jucator["bloodlust"] == True else (jucator["damage_baza"] + 50)
        buffuri_echipamente()
        hit = jucator["inamic_damage_redus"] // 2
        time.sleep(1)
        print("\nDemonul incepe sa alerge inspre tine")
        time.sleep(1)
        print("\nSare in aer si incepe sa traga cu bile de foc")
        time.sleep(1)
        print(f"\nTe feresti usor de ele dar pana sa observi pamantul a explodat sub picioarele tale! -{hit}HP")
        time.sleep(1)
        print("\nEsti aruncat de explozie")
        time.sleep(1)
        print(f"\nDemonul te prinde din aer si iti dai un downslam fix in pamant! -{hit}HP")
        time.sleep(3)
        print("\nInainte ca demonul sa mai atace din nou, reusesti sa iti revi")
        jucator["jucator_viata"] -= jucator["inamic_damage_redus"]

    elif atac_random in [8, 9]:
        jucator["inamic_damage"] = (jucator["damage_baza"] + 100) if jucator["bloodlust"] == True else (jucator["damage_baza"] + 55)
        buffuri_echipamente()
        hit = jucator["inamic_damage_redus"] // 10
        time.sleep(1)
        print("\nDemonul foloseste o abilitate")
        time.sleep(1)
        print("\nFOG OF WAR!")
        time.sleep(1)
        print("\nDin locatia lui incepe sa apara un fum rosu si totul incepe sa se incetoseze")
        time.sleep(1)
        print("\nTe uiti in toate directiile, dar... nu vezi nimic")
        time.sleep(1)
        print("\nDupa auzi ceva de sub pamant")
        time.sleep(1)
        print("\nDemonul doar a trimis ceva sa faca sunet sub pamant si ai picat in plasa lui")
        time.sleep(1)
        print("\nAi cazut pe niste un cerc de ritual")
        time.sleep(1)
        print("\nDe abia cand il observi pamantul explodeaza")
        time.sleep(1)
        print("\nDe fapt peste tot sunt mine plantate")
        time.sleep(1)
        print("\nSi sari dintr-una in alta")
        time.sleep(1)
        for _ in range(5):
            print(f"-{hit}HP")
            time.sleep(2)
        print("\nUltima te arunca fix in mainile demonului, si te apuca de gat")
        time.sleep(1)
        print("Te strange de gat")
        for _ in range(4):
            print(f"-{hit}HP")
            time.sleep(0.3)
        print(f"\nSi te arunca intr-un zid! -{hit}HP")
        time.sleep(3)
        jucator["jucator_viata"] -= jucator["inamic_damage_redus"]
        jucator["burn_jucator"] = 2
        
    elif atac_random == 10:

        jucator["inamic_damage"] = (jucator["damage_baza"] + 175) if jucator["bloodlust"] == True else (jucator["damage_baza"] + 100)
        jucator["damage_final"] = (jucator["damage_baza"] + 125) if jucator["frenzy"] == True else (jucator["damage_baza"] + 75)
        buffuri_echipamente()
        time.sleep(1)
        print("\nDemonul incepe sa faca o incantatie")
        time.sleep(1)
        print("\nIncepi sa alergi sa il opresti")
        time.sleep(1)
        print("\nDar nu reusesti la timp si te opresti cand vezi ce a invocat")
        time.sleep(1)
        print("\nDemonul a invocat hound dogs")
        time.sleep(1)
        print("\nDemonul incepe sa faca o alta incantatie si hound dogs incep sa alerge spre tine")
        time.sleep(1)
        print("\nElimini cainii destul de rapid dar nu indeajuns de rapid ca sa ii opresti incantatia")
        time.sleep(1)
        print("\nDEMON SWORD! WORLD ENDER")
        time.sleep(1)
        print("\nTe uiti inspaimantat la sabia aia ca si cum ar fi vie (PS este vie)")
        time.sleep(1)
        print("\nDemonul reuseste sa te injungie cu sabia si simti cum se ofileste viata din tine")
        time.sleep(1)
        print(f"\nCa sa nu iti fure sabia toata energia vitala! -{jucator["inamic_damage_redus"]}HP")
        time.sleep(1.5)
        print("\nLAVA ERUPTION! fix sub picioarele tale")
        time.sleep(1)
        print("\nDemonul a scapat sabia si a ramas in tine")
        time.sleep(1)
        print("\nO scoti din piept si o distrugi! DECAY!")
        time.sleep(1)
        print(f"\nSabia se sfarama si bosul pare ca a suferit si el (Sabia batea ca o inima) -{jucator["damage_final_jucator"]}HP")
        time.sleep(1)
        print("\nTi-ai folosit prea mult puterea si sabia ti-a furat energia vitala incat nu te mai poti misca")
        time.sleep(1)
        print("\nTotusi si demonul si-a folosit prea mult puterea si nici el nu se poate misca")
        time.sleep(3)
        jucator["jucator_viata"] -= jucator["inamic_damage_redus"]
        inamic["viata"] -= jucator["damage_final_jucator"]
        jucator["jucator_stun"] = True
        jucator["inamic_stun"] = True

print("====== Ai intrat in dungeon =======")

while True:

    if jucator["jucator_viata"] <= 0:
        print("\nAi murit si ai pierdut dungeon ul")
        break

    numar_camera = jucator["camera_curenta"]
    date_camera = harta[numar_camera]

    if jucator["camera_curenta"] == "camera_1":

        accesare_inventar()

        inamic = baza_date_inamici[numar_camera]

        if inamic["viata"] > 0:
            print(date_camera["descriere"])
            time.sleep(2)

            while jucator["jucator_viata"] > 0 and inamic["viata"] > 0:
                jucator["energie"] += calculeaza_energie()
                alegere_atac()
                if inamic["viata"] > 0:
                    goblin_atac()
                limite_viata()
                efecte_DoT()
                activare_mod()

                if jucator["jucator_viata"] <= 0: break

                if inamic["viata"] <= 0:
                    print("Inamicul a murit")
                    time.sleep(1.5)
                    genereaza_drop()
                    jucator["nivel"] += 1
                    jucator["jucator_stun"] = False
                    break

        else:
            print("\nCamera este goala, obviously? Te asteptai ca goblinul sa se respawneze sau ce?")

    elif jucator["camera_curenta"] == "camera_2":
        accesare_inventar()
        
        inamic = baza_date_inamici[numar_camera]
        
        if inamic["viata"] > 0:
            print(date_camera["descriere"])
            time.sleep(2)

            accesare_shop()
        
            while jucator["jucator_viata"] > 0 and inamic["viata"] > 0:
                jucator["energie"] += calculeaza_energie()
                alegere_atac()
                if inamic["viata"] > 0:
                    orc_atac()
                limite_viata()
                efecte_DoT()
                activare_mod()

                if jucator["jucator_viata"] <= 0: break

                if inamic["viata"] <= 0:
                    print("Inamicul a murit")
                    time.sleep(1.5)
                    genereaza_drop()
                    jucator["nivel"] += 1
                    jucator["jucator_stun"] = False
                    break
        
        else:
            print("\nCamera este goala, obviously? Te asteptai ca orcul sa se respawneze sau ce?")

    elif jucator["camera_curenta"] == "camera_3":

        accesare_inventar()
        
        inamic = baza_date_inamici[numar_camera]
        
        if inamic["viata"] > 0:
            print(date_camera["descriere"])
            time.sleep(2)

            accesare_shop()
        
            while jucator["jucator_viata"] > 0 and inamic["viata"] > 0:
                jucator["energie"] += calculeaza_energie()
                alegere_atac()
                if inamic["viata"] > 0:
                    skelete_atac()
                limite_viata()
                efecte_DoT()
                activare_mod()

                if jucator["jucator_viata"] <= 0: break

                if inamic["viata"] <= 0:
                    print("Inamicul a murit")
                    time.sleep(1.5)
                    genereaza_drop()
                    jucator["nivel"] += 2
                    jucator["jucator_stun"] = False
                    break
        
        else:
            print("\nCamera este goala, obviously? Te asteptai ca skeletele sa se respawneze sau ce?")

    elif jucator["camera_curenta"] == "camera_4":

        accesare_inventar()
            
        inamic = baza_date_inamici[numar_camera]
                
        if inamic["viata"] > 0:
            print(date_camera["descriere"])
            time.sleep(2)
        
            accesare_shop()
                
            while jucator["jucator_viata"] > 0 and inamic["viata"] > 0:
                jucator["energie"] += calculeaza_energie()
                alegere_atac()
                if inamic["viata"] > 0:
                    golem_atac()
                limite_viata()     
                activare_mod()
                efecte_DoT()

                if jucator["jucator_viata"] <= 0: break

                if inamic["viata"] <= 0:
                    print("Inamicul a murit")
                    time.sleep(1.5)
                    genereaza_drop()
                    print("MAX LEVEL REACHED")
                    jucator["jucator_stun"] = False
                    break
                
        else:
            print("\nCamera este goala, obviously? Te asteptai ca golemul sa se respawneze sau ce?")

    elif jucator["camera_curenta"] == "camera_5":

        accesare_inventar()
                
        inamic = baza_date_inamici[numar_camera]
                    
        if inamic["viata"] > 0:
            print(date_camera["descriere"])
            time.sleep(2)
            
            accesare_shop()
                    
            while jucator["jucator_viata"] > 0 and inamic["viata"] > 0:
                jucator["energie"] += calculeaza_energie()
                alegere_atac()
                if inamic["viata"] > 0: 
                    fiend_atac()
                limite_viata()
                efecte_DoT()  
                    
                if jucator["jucator_viata"] <= 0: break
            
                activare_mod()

                if inamic["viata"] <= 0:
                    print("Inamicul a murit")
                    time.sleep(1.5)
                    genereaza_drop()
                    print("MAX LEVEL REACHED")
                    jucator["jucator_stun"] = False
                    break

    elif jucator["camera_curenta"] == "camera_comori":
        print(date_camera["descriere"])

    if numar_camera == "iesire_dungeon":
        print("\nAi fugit ca un loser din dungeon! Hai pa")
        break

    alegere = input("\nIncotro vrei sa te duci? ").lower().strip()

    if alegere in date_camera["directia"]:
        jucator["camera_curenta"] = date_camera["directia"][alegere]
    else:
        print("\nNu poti merge incolo")