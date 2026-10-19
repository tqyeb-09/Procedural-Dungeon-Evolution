import random
inamic_viata = 250
jucator_viata = 100
sangerare_inamic = 0
sangerare_jucator = 0
inamic_stun = False
while jucator_viata > 0 and inamic_viata > 0:
    print(f"\n Viata ta: {jucator_viata}  Viata inamicului: {inamic_viata} ")
    print("Atac normal")
    print("Atac special")
    alegere = int(input("Ce folosesti: "))

    if alegere == 1:
        atac_dodge = random.randint(1, 5)

        if atac_dodge == 1 or atac_dodge == 3 or atac_dodge == 4:
            inamic_viata = inamic_viata - 20
            print("\n Ai dat o lovitura normala! -20HP")
        elif atac_dodge == 2:
            inamic_viata = inamic_viata - 40
            inamic_stun = True
            print("\n Ai dat critica! -40HP")
        elif atac_dodge == 5:
            print("\n Inamicul a dat dodge la atac")

    if alegere == 2:
        atac_dodge = random.randint(1, 5)
        
        if atac_dodge == 1 or atac_dodge == 2 or atac_dodge == 3 or atac_dodge == 4:
                inamic_viata = inamic_viata - 15
                print("\n Ai taiat inamicul -15HP, Inamicul a inceput sa sangereze!")
                sangerare_inamic = 3
        elif atac_dodge == 5:
                print("\n Inamicul a dat dodge la atac")

    if inamic_viata > 0:
        if inamic_stun == True:
            print("\n Inamicul este ametit si nu va ataca tura asta")
            inamic_stun = False
        else:
            atac_random = random.randint(1, 3)

            if atac_random == 1:
                jucator_viata = jucator_viata - 10
                print("\n Inamicul a folosit ghearele! -10HP Si te-a facut sa sangerezi")
                sangerare_jucator = 3
            elif atac_random == 2:
                jucator_viata = jucator_viata - 20
                print("\n Inamicul a folosit atac devastator! -20HP")
            elif atac_random == 3:
                jucator_viata = jucator_viata - 5
                inamic_viata = inamic_viata + 15
                print("\n Inamicul a folosit lifesteal -5HP! Si si-a luat +15HP")

    if sangerare_inamic > 0:
         inamic_viata = inamic_viata - 10
         sangerare_inamic = sangerare_inamic - 1
         print("\n Inamicul sangereaza! -10HP")

    if sangerare_jucator > 0:
         jucator_viata = jucator_viata - 5
         sangerare_jucator = sangerare_jucator - 1
         print("\n Sangerezi! -5HP")

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