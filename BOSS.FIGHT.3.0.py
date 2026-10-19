import random
import time
inamic_viata = 500
inamic_viata_maxima = 500
jucator_viata = 200
jucator_stun = False
dizzy = 0
burn = 0
burn_damage = 15
damage_boost_duration = 0
berserk = False
berserk_mesaj = False
sangerare = 0
sangerare_damage = 10
energie = 0
sangerare_inamic = 0
sangerare_inamic_damage = 30
energie_maxima = 300
while inamic_viata > 0 and jucator_viata > 0:
    print(f"Viata ta: {jucator_viata} Viata inamicului: {inamic_viata}")
    print("Atacuri:")
    print("1.Basic attack")
    print("2.Jawbreaker")
    print("3.Fireball")
    print("4.Damage boost")
    print("5.Ultimate")
    alegere = int(input("\nCe atac folosesti? "))


    energie_necesara = energie_maxima - energie

    if energie > energie_maxima:
        energie = 300

    print(f"\n Ai {energie} energie")

    if burn > 0:
        inamic_viata = inamic_viata - burn_damage
        burn = burn - 1
        print(f"\nInamicul arde, si pierde {burn_damage}HP. Efectul se duce in {burn} ture")

    if sangerare_inamic > 0:
        inamic_viata = inamic_viata - sangerare_inamic_damage
        sangerare_inamic = sangerare_inamic - 1
        print(f"\n Inamicul pierde mult sange si pierde {sangerare_inamic_damage}HP. Sangerarea se opreste in {sangerare_inamic} ture")
    
    if sangerare > 0:
        jucator_viata = jucator_viata - sangerare_damage
        sangerare = sangerare - 1
        print(f"\nSangerezi! Ai pierdut {sangerare_damage}HP. Efectul se duce in {sangerare} ture")
    
    if dizzy > 0:
        dizzy = dizzy - 1
        print(f"\nInamicul este ametit, Efectul se duce in {dizzy} ture")

    if damage_boost_duration > 0:
        damage_boost_duration = damage_boost_duration - 1
        print(f"\n Boost ul de damage se duce in {damage_boost_duration}")

    if alegere == 1:
        if jucator_stun == True:
            print("\nEsti stunned, nu poti ataca")
            jucator_stun = False
        else:
            if dizzy > 0:
                atac_normal = random.randint(1, 4)
                if atac_normal == 1 or atac_normal == 2 or atac_normal == 3:
                    damage = 30 if damage_boost_duration > 0 else 20
                    inamic_viata = inamic_viata - damage
                    print(f"\nLovitura directa! -{damage}HP")
                    energie = energie + damage
                elif atac_normal == 4:
                    damage = 60 if damage_boost_duration > 0 else 40
                    inamic_viata = inamic_viata - damage
                    print(f"\nCritica! -{damage}HP")
                    energie = energie + damage
            else:
                atac_normal = random.randint(1, 5)

                if atac_normal == 1 or atac_normal == 2 or atac_normal == 3:
                    damage = 30 if damage_boost_duration > 0 else 20
                    inamic_viata = inamic_viata - damage
                    print(f"\nLovitura directa! -{damage}HP")
                    energie = energie + damage
                elif atac_normal == 4:
                    damage = 60 if damage_boost_duration > 0 else 40
                    inamic_viata = inamic_viata - damage
                    print(f"\nCritica! -{damage}HP")
                    energie = energie + damage
                elif atac_normal == 5:
                    print("\nInamicul s-a ferit de atac")

    elif alegere == 2:
        if jucator_stun == True:
            print("\nEsti stunned, nu poti ataca")
            jucator_stun = False
        else:
            if dizzy > 0:
                jawbreaker = random.randint(1, 2)

                if jawbreaker == 1:
                    damage = 45 if damage_boost_duration > 0 else 30
                    inamic_viata = inamic_viata - damage
                    print(f"\nJAWBREAKER! -{damage}HP")
                    energie = energie + damage
                elif jawbreaker == 2:
                    damage = 60 if damage_boost_duration > 0 else 40
                    inamic_viata = inamic_viata - damage
                    dizzy = 3
                    print(f"\nPHOA, i-ai dat-o bine rau! -{damage}HP")
                    print("\nAi ametit inamicul")
                    energie = energie + damage
            else:
                jawbreaker = random.randint(1, 5)

                if jawbreaker == 1 or jawbreaker == 3:
                    damage = 45 if damage_boost_duration > 0 else 30
                    inamic_viata = inamic_viata - damage
                    print(f"\nJAWBREAKER! -{damage}HP")
                    energie = energie + damage
                elif jawbreaker == 2 or jawbreaker == 4:
                    damage = 60 if damage_boost_duration > 0 else 40
                    inamic_viata = inamic_viata - damage
                    dizzy = 3
                    print(f"\nPHOA, i-ai dat-o bine rau! -{damage}HP")
                    print(f"\nAi ametit inamicul, efectul se duce in {dizzy} ture")
                    energie = energie + damage
                elif jawbreaker == 5:
                    print("\nInamicul s-a ferit de atac")

    elif alegere == 3:
        if jucator_stun == True:
            print("\nEsti stunned, nu poti ataca")
            jucator_stun = False
        else:
            damage = 15 if damage_boost_duration > 0 else 10
            inamic_viata = inamic_viata - damage
            burn = 3
            print(f"\nFIREBALL! -{damage}HP")
            energie = energie + damage

    elif alegere == 4:
        if jucator_stun == True:
            print("\nEsti stunned, nu poti ataca")
            jucator_stun = False
        else:
            damage_boost_duration = 3
            print(f"\nDamage boost activat! Vei da x1.5 damage pentru {damage_boost_duration} ture")

    elif alegere == 5:
        if jucator_stun == True:
            print("\nEsti stunned, nu poti ataca")
            jucator_stun = False
        elif energie == 300:
            damage = 150 if damage_boost_duration > 0 else 100
            if inamic_viata <= inamic_viata_maxima * 0.30:
                print("\n Ai sarit in spate si ai aruncat 3 slash uri spre inamic")
                time.sleep(1)
                print("\n -10HP")
                time.sleep(1)
                print("\n -10HP")
                time.sleep(1)
                print("\n -10HP")
                time.sleep(2)
                print("\n Inamicul este vulnerabil")
                time.sleep(1)
                print("\n Ai sarit spre el")
                time.sleep(1)
                print("\n I-ai taiat toate membrele!")
                time.sleep(1)
                print("\n ULTIMATA, DECAPITARE, i-ai taiat capul inamicului")
                inamic_viata = 0
            else:
                inamic_viata = inamic_viata - damage   
                print("\n Ai sarit in spate si ai aruncat 3 slash uri spre inamic")
                time.sleep(1)
                print("\n -10HP")
                time.sleep(1)
                print("\n -10HP")
                time.sleep(1)
                print("\n -10HP")
                time.sleep(2)
                print("\n Inamicul este vulnerabil")
                time.sleep(1)
                print("\n Ai sarit spre el")
                time.sleep(1)
                print("\n Ai facut 2 slash uri pieptul inamicului! -50HP")
                time.sleep(1)
                print("\n I-ai pus piedica, in timp ce el cade il tai si il arunci cu piciorul! -70HP")
                sangerare_inamic = 3
        else:
            print(f"Nu ai destula energie. Mai ai nevoie de {energie_necesara} energie")

    if inamic_viata <= inamic_viata_maxima * 0.50 and berserk_mesaj == False:
        berserk_mesaj = True
        berserk = True
        print("\nInamicul a intrat in BERSERK")

    if inamic_viata > 0:
        if dizzy > 0:
            inamic_atac = random.randint(1, 3)

            if inamic_atac == 1:
                damage = 40 if berserk == True else 20
                jucator_viata = jucator_viata - damage
                print(f"\nLovitura directa! Ai pierdut {damage}HP")
            elif inamic_atac == 2 or inamic_atac == 3:
                print("\nInamicul a ratat atacul")
        else:
            inamic_atac = random.randint(1, 5)
            if inamic_atac == 1 or inamic_atac == 2 or inamic_atac == 3:
                damage = 30 if berserk == True else 15
                jucator_viata = jucator_viata - damage
                print(f"\nLovitura normala! Ai pierdut {damage}HP")
            elif inamic_atac == 4:
                jucator_stun = True
                damage = 20 if berserk == True else 10
                jucator_viata = jucator_viata - damage
                print(f"\nInamicul ti-a dat stun, si ai pierdut {damage}HP")
            elif inamic_atac == 5:
                sangerare = 3
                damage = 20 if berserk == True else 10
                jucator_viata = jucator_viata - damage
                print(f"\nInamicul te-a taiat, si ai pierdut {damage}HP")
    else:
        print("\nInamicul a murit")

    if inamic_viata < 0:
            inamic_viata = 0

    if jucator_viata < 0:
            jucator_viata = 0

print(f"\n Rezultatul meciului: Viata ta: {jucator_viata}, Viata inamicului: {inamic_viata}")

if inamic_viata > 0:
   print("\n Tragic bro, cum sa pierzi bro? Baka")
elif jucator_viata == 0 and inamic_viata == 0:
    print("\n Egal, nimeni nu a castiga, nimeni nu a pierdut")
elif jucator_viata > 0:
   print("\n Regele bro, chiar l-ai batut, W MANZ")