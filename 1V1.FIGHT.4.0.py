import random
import time
energie = 0
jucator_viata = 1000
jucator_viata_maxima = 1000
inamic_viata = 1500
inamic_viata_maxima = 1500
sangerare = 0
sangerare_damage = 20
sangerare_ultimata = 0
sangerare_ultimata_damage = 50
jucator_stun = False
inamic_stun = False
rage = False
rage_mesaj = False
berserk = False
while jucator_viata > 0 and inamic_viata > 0:
    print(f"Viata ta: {jucator_viata} Viata inamicului: {inamic_viata}")

    energie += random.choice([10, 20, 30, 40, 50])
    if energie >= 100:
        energie = 100
    print(f"Ai {energie} energie")
    print("Atacuri:")
    print("1.Pumn 10E")
    print("2.Slash 30E")
    print("3.Skull Crusher 50E")
    print("4.Ultimata 100E")

    alegere = int(input("Ce Atac folosesti? "))

    if alegere >= 5 or alegere <= 0:
        print("\nNu ai voie sa faci asta ca sa pastrezi energia")
        energie -= 20

    if energie < 0:
        energie = 0

    if jucator_stun == True:
        print("\nEsti stunned, nu poti ataca tura asta")
        jucator_stun = False
    elif alegere == 1:
        if energie < 10:
            print("\nNu ai destula energie")
        else:
            energie -= 10
            atac_normal = random.randint(1, 5)
            if atac_normal in [1, 2, 3]:
                damage = 30 if rage == True else 20
                inamic_viata -= damage
                print(f"\nLovitura directa! -{damage}HP")
                time.sleep(1)
                print("\nSari in spate")
            elif atac_normal == 4:
                damage = 60 if rage == True else 40
                inamic_viata -= damage
                print(f"\nCritica! -{damage}HP")
                time.sleep(1)
                print("\nTe repozitionezi")
            elif atac_normal == 5:
                print("\nInamicul s-a ferit de atac")
                time.sleep(1)
                print("\nInamicul ataca inapoi")
                time.sleep(1)
                print("\nTe feresti si te dai in spate")
    elif alegere == 2:
        if energie < 30:
            print("\nNu ai destula energie")
        else:
            energie -= 30
            slash = random.randint(1, 3)
            if slash == 1:
                damage = 40 if rage == True else 30
                damage_multi = damage // 2
                inamic_viata -= damage
                sangerare = 3
                print(f"\nAi taiat inamicul! -{damage_multi}HP")
                time.sleep(1)
                print(f"\nTe feresti, si il tai iar! -{damage_multi}HP")
                time.sleep(1)
                print("\nInamicul isi revine si te dai inapoi")
            elif slash == 2:
                damage = 50 if rage == True else 25
                damage_multi = damage // 3
                inamic_viata -= damage
                sangerare = 4
                print(f"\nLansezi un slash de aer -{damage_multi}HP")
                time.sleep(1)
                print("\nInamicul este vulnerabil")
                time.sleep(1)
                print("\nAi sarit spre el")
                time.sleep(2)
                print("\nLansezi un slash de aer in timp ce te apropii in zbor sper el")
                time.sleep(1)
                print(f"\nSlash-ul l-a nimerit! -{damage_multi}HP")
                time.sleep(1)
                print(f"\nImediat dupa, il tai pe piept! -{damage_multi}HP")
                time.sleep(1)
                print("\nInamicul a luat-o razna si te ataca de nicaieri, te feresti si te repozitionezi")
            elif slash == 3:
                print("\nInamicul a anticipat atacul, riposteaza, dar te-ai ferit in timp")
                time.sleep(1)
    elif alegere == 3:
        if energie < 50:
            print("\nNu ai destula energie")
        else:
            energie -= 50
            skull = random.randint(1, 5)
            if skull in [1, 2]:
                damage = 70 if rage == True else 40
                damage_multi = damage // 4
                inamic_viata -= damage
                inamic_stun = True
                time.sleep(1)
                print("\nSari spre inamic")
                time.sleep(1)
                print("\nFentezi atacul, inamicul este deschis")
                time.sleep(1)
                print(f"\nPrinzi o lovitura grea in craniul inamicului! -{damage_multi}HP")
                time.sleep(2)
                print("\nInamicul este ametit, folosesti aceasta oportunitate si mai prinzi 2 pumni!")
                for _ in range(2):
                    print(f"-{damage_multi}HP")
                    time.sleep(0.5)
                time.sleep(1)
                print(f"\nTermini cu un picior in burta inamicului care il arunca departe! -{damage_multi}HP")
            elif skull in [3, 4]:
                damage = 100 if rage == True else 70
                damage_multi = damage // 5
                inamic_viata -= damage
                time.sleep(1)
                print("\nTe apropii in pasi mici spre inamic")
                time.sleep(1)
                print(f"\nInamicul ataca, te feresti, si ii prinzi un uppercut in barbie! -{damage_multi}HP")
                time.sleep(1)
                print("\nInamicul este dezechilibrat")
                time.sleep(1)
                print(f"\nFolosesti aceasta oportunitate si ii prinzi un pumn ficat! -{damage_multi}HP")
                time.sleep(1)
                print("\nIi mai prinzi 3 pumni in fata")
                time.sleep(1)
                for _ in range(3):
                    print(f"-{damage_multi}HP")
                    time.sleep(0.5)
                time.sleep(1)
                print("\nInamicul inca este in picioare si te repozitionezi")
            elif skull == 5:
                time.sleep(1)
                print("\nInamicul s-a asteptat la atacul tau")
                time.sleep(1)
                damage = 50 if berserk == True else 30
                print(f"\nTi-a prins un pumn! -{damage}HP")
                jucator_viata -= damage
    elif alegere == 4:
        if energie < 100:
            print("Nu ai energie suficienta")
        else:
            damage = 150 if rage == True else 100
            energie -= 100
            if inamic_viata <= inamic_viata_maxima * 0.30:
                time.sleep(1)
                print("\nTi sabia sus si te indrepti drept spre inamic")
                time.sleep(1)
                print("\nAjungi la el, te feresti de atacul lui, si ii tai o mana cu sabia")
                time.sleep(1)
                print("\nInamicul o i-a razna si prinde o lovitura, reusesti sa o blochezi dar te trimite zburand in spate si te lovesti de o piatra")
                time.sleep(1)
                print("\nInamicul incearca sa dea follow")
                time.sleep(1)
                print("\nReactionezi in timp, treci pe langa inamic si reusesti si ii ranesti grav picioarele")
                time.sleep(1)
                print("\nInamicul nu se mai poate misca")
                time.sleep(1)
                print("\nLOVITURA DE GRATIE! FLASH SLASH")
                time.sleep(1)
                print("\nTe misti la viteza luminii, inamicul inainte sa observe ce se intampla, vede ca privirea incepe sa i se invarte")
                time.sleep(1)
                print("\nAbia cand capul lui a cazut pe pamant a realizat ca a fost decapitat, si eventual moare")
                time.sleep(2)
                print("\nCand iti bagasei sabia in teaca si incepusei sa pleci, te uiti in spate si vezi ca capul inamicului ca incepe sa creasca la loc")
                time.sleep(1)
                print("\nIN AN INSTANT! Ti-ai scos sabia si i-ai facut corpul praf")
                inamic_viata = 0
            else:
                inamic_viata -= damage
                multihit = damage // 3
                time.sleep(1)
                print("\nSari in aer si lansezi 3 slash uri de aer")
                time.sleep(1)
                print("\nInamicul este distras si se fereste de acele slash uri")
                time.sleep(1)
                print(f"\nIntre timp te furisezi in spatele lui si ii faci o taietura mare pe spate! -{multihit}HP")
                time.sleep(1)
                print("\nInamicul o i-a razna, si da rush fara sa gandeasca la tine")
                time.sleep(2)
                print("\nRamai calm si te feresti de atacurile lui nu prea precise")
                time.sleep(1)
                print(f"\nVezi o deschidere si ii tai pieptul deschis! -{multihit}HP")
                time.sleep(1)
                print("\nInamicul se retrage, dar incepe sa piarda mult sange")
                time.sleep(1)
                print(f"\nAcum tu te apropii spre el, ii pui piedica cumva, si il trimiti zburand cu un front kick! -{multihit}HP")
                time.sleep(1)
                sangerare_ultimata = 4
                print("\nInamicul pierde o gramada de sange")

    if inamic_viata > 0:
        if inamic_stun == True:
            print("\nInamicul este stunned si nu poate ataca")
            inamic_stun = False
        else:
            atac_inamic = random.randint(1, 10)
            if atac_inamic in [1, 2, 3, 4, 5]:
                damage = 50 if berserk == True else 30
                damage_headbutt = damage // 2
                damage_throw = damage // 3
                damage_fists = damage // 18
                time.sleep(1)
                print("\nInamicul incepe sa alerge inspre tine")
                time.sleep(1)
                print("\nTe feresti dar si el se fereste de counter attack-ul tau")
                time.sleep(1)
                print(f"\nTe prinde cu garda jos si iti da 3 pumni in burta")
                time.sleep(1)
                for _ in range(3):
                    print(f"-{damage_fists}HP")
                    time.sleep(1)
                print(f"\nFoloseste aceasta oportunitate si iti baga capul in genunchiul lui! -{damage_headbutt}HP")
                time.sleep(1)
                print(f"\nSi te arunca departe! -{damage_throw}HP")
                jucator_viata -= damage
            elif atac_inamic in [6, 7, 8]:
                damage = 70 if berserk == True else 40
                damage_suplex = damage // 4
                damage_lovitura_finala = damage // 4
                damage_combo = damage // 20
                damage_player = 30 if rage == True else 20
                time.sleep(1)
                print("\nInamicul se apropie incet spre tine cu garda sus")
                time.sleep(1)
                print("\nFenteaza atacul, si te prinde in plasa lui")
                time.sleep(1)
                print(f"\nAjunge rapid in spatele tau si iti da suplex, care te baga cu capul in pamant! -{damage_suplex}HP")
                time.sleep(1)
                print("\nCumva reusesti sa te ridici")
                time.sleep(1)
                print(f"\nEsti ametit dar prinzi inamicul nepregatit si ii prinzi un pumn in fata! -{damage_player}")
                time.sleep(1)
                print("\nInamicul cade, dar se ridica si incepe sa dea rush dupa tine")
                time.sleep(1)
                print("\nInca esti ametit si nu reusesti sa te feresti")
                time.sleep(1)
                print("\nInamicul iti da un combo de pumni")
                time.sleep(1)
                for _ in range(10):
                    print(f"-{damage_combo}HP")
                    time.sleep(0.3)
                time.sleep(1)
                print(f"\nSi da un ultim pumn care te trimite zburand! -{damage_lovitura_finala}HP")
                time.sleep(1)
                jucator_viata -= damage
                inamic_viata -= damage_player
            elif atac_inamic == 9:
                damage = 100 if berserk == True else 70
                damage_zid = damage // 2
                damage_pamant = damage // 2
                jucator_stun = True
                time.sleep(1)
                print("\nInamicul sare cu o viteza ireala spre tine")
                time.sleep(1)
                print("\nTe feresti la limita")
                time.sleep(1)
                print("\nDAR....")
                time.sleep(1)
                print("\nCand te intorci sa vezi ce face inamicul, inamicul te apuca cu palma de fata")
                time.sleep(1)
                print("\nIncerci sa rezisti dar esti fara speranta")
                time.sleep(1)
                print(f"\nInamicul incepe sa iti tareasca capul in pamant! -{damage_pamant}HP")
                time.sleep(1)
                print(f"\nSi dupa te arunca intr-un zid! -{damage_zid}HP")
                time.sleep(1)
                jucator_viata -= damage
            elif atac_inamic == 10:
                if berserk == False:
                    berserk = True
                    damage = 150
                    damage_zburand = damage // 10
                    damage_aer = damage // 10
                    damage_pamant_II = damage // 5
                    damage_picior = damage // 4
                    damage_jucator = 100
                    multihit_jucator = damage_jucator // 20
                    time.sleep(1)
                    print("\nTe indrepti spre inamic")
                    time.sleep(1)
                    print("\nTe feresti de toate atacurile lui")
                    time.sleep(1)
                    print("\nIl ataci din fiecare directie, inamicul este coplesit")
                    time.sleep(1)
                    for _ in range(20):
                        print(f"-{multihit_jucator}HP")
                        time.sleep(0.2)
                    time.sleep(1)
                    print("\nTotusi.. dintr-o data")
                    time.sleep(1)
                    print(f"\nInamicul incepe sa urle si sa emane o aura rosie care te trimite zburand! -{damage_zburand}HP ")
                    time.sleep(1)
                    print("\nInainte ca sa te recupezi de la impact")
                    time.sleep(1)
                    print("\nInamicul sare pe tine")
                    time.sleep(1)
                    print("\nOficial, inamicul a luat-o razna")
                    time.sleep(1)
                    print(f"\nInamicul iti da un picior care te arunca in aer! -{damage_aer}HP")
                    time.sleep(1)
                    print("\nEste atat de rapid incat ajunge deasupra ta in aer")
                    time.sleep(1)
                    print(f"\nIti da o lovitura extrem de puternica si face gaura cu tine in pamant! -{damage_pamant_II}HP")
                    time.sleep(1)
                    print("\nSe teleporteaza jos instant")
                    time.sleep(1)
                    print(f"\nSi iti da un picior care te arunca extrem de departe! -{damage_picior}HP")
                    time.sleep(1)
                    print("\nInainte ca sa intelegi ce se intampla")
                    time.sleep(1)
                    print("\nVezi inamicul cum se teleporteaza in timp ce zbori")
                    time.sleep(1)
                    print(f"\nIti baga piciorul in fata si iti izbeste capul de pamant! -{damage_picior}HP")
                    time.sleep(1)
                    print(f"\nInamicul incepe sa se calmeze dar tot emana aura aia rosie, totusi te trimite zburand departe! -{damage_zburand}")
                    time.sleep(1)
                    inamic_viata -= damage_jucator
                    jucator_viata -= damage
                else:
                    damage = 200
                    damage_jucator = 150
                    time.sleep(1)
                    print(f"\nExchange blows! Pierzi {damage}HP, Inamicul pierde {damage_jucator}HP")
                    time.sleep(1)
                    print("\nTotusi atacurile inamicului sunt mai puternice decat ale tale")
                    time.sleep(1)
                    inamic_viata -= damage_jucator
                    jucator_viata -= damage

    if jucator_viata <= jucator_viata_maxima * 0.30 and rage_mesaj == False:
            rage_mesaj = True
            rage = True
            jucator_stun = False
            print("\nAi intrat in rage mode")

    if sangerare > 0:
        inamic_viata -= sangerare_damage
        print(f"\nInamicul sangereaza! -{sangerare_damage}HP")
        sangerare -= 1

    if sangerare_ultimata > 0:
        inamic_viata -= sangerare_ultimata_damage
        print(f"\nInamicul pierde mult sange! -{sangerare_ultimata_damage}HP")
        sangerare_ultimata -= 1

    if inamic_viata <= 0:
        inamic_viata = 0
        print("\nInamicul a murit")

    if jucator_viata <= 0:
        jucator_viata = 0
        print("\nAi murit")

print(f"\nRezultatele meciului: Viata ta: {jucator_viata}HP  Viata inamicului: {inamic_viata}HP")

if inamic_viata > 0:
   print("\n Tragic bro, cum sa pierzi bro? Baka")
elif jucator_viata == 0 and inamic_viata == 0:
    print("\n Egal, nimeni nu a castiga, nimeni nu a pierdut")
elif jucator_viata > 0:
   print("\n Regele bro, chiar l-ai batut, W MANZ")