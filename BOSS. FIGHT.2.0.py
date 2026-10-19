import random
inamic_viata = 200
jucator_viata = 100
inamic_in_flacari = 0
cooldown_fireball = 0
damage_flacari = 10
inamic_inghetat = False
cooldown_icicles = 0
healing_duration = 0
cooldown_healing = 0
healing_effect = 20
while jucator_viata > 0 and inamic_viata > 0:
        print(f"\n--- Viata ta: {jucator_viata} , Viata inamicului: {inamic_viata}")
        print("Alege atacul:")
        print("1.Atac normal:")
        print("2.Fireball")
        print("3.Icicles")
        print("4.Healing spell")

        alegere = int(input("Ce vei folosi? "))

        if alegere == 1:
                critica = random.randint(1, 5)
                if critica < 5:
                        inamic_viata = inamic_viata - 10
                        print("\n Lovitura directa! -10HP")
                elif critica == 5:
                        inamic_viata = inamic_viata - 30
                        print("\n PAU! Critica! -30HP")
        elif alegere == 2:
                if cooldown_fireball == 0:
                    inamic_viata = inamic_viata - 10
                    inamic_in_flacari = 3
                    print("\n Inamicul este in flacari")
                    cooldown_fireball = 2
                else:
                        print(f"\n Fireball-ul este pe cooldown, trebuie sa astepti {cooldown_fireball} ture pana il poti folosi iar")

        elif alegere == 3:
                if cooldown_icicles == 0:
                    inamic_viata = inamic_viata - 15
                    inamic_inghetat = True
                    print("\n Inamicul este inghetat pentru o tura")
                    cooldown_icicles = 2
                else:
                       print(f"\n Icicles este pe cooldown, trebuie sa astepti {cooldown_icicles} ture pana il poti folosi iar")

        elif alegere == 4:
                if cooldown_healing == 0:
                    jucator_viata = jucator_viata + 10
                    healing_duration = 2
                    print("\n Vindecare")
                    cooldown_healing = 2
                else:
                       print(f"\n Healing spell-ul este pe cooldown, trebuie sa astepti {cooldown_healing} ture pana il poti folosi iar")

        if inamic_viata > 0:
                if inamic_inghetat == True:
                    print("\n Inamicul este inghetat si nu poate ataca tura asta")
                    inamic_inghetat = False
                else:
                        atac_random = random.randint(1, 3)

                        if atac_random == 1:
                              jucator_viata = jucator_viata - 20
                              print("\n Inamicul a folosit un atac normal! -20HP")
                        elif atac_random == 2:
                              jucator_viata = jucator_viata - 35
                              print("\n Inamicul a folosit un atac DEVASTATOR! -35HP")
                        elif atac_random == 3:
                              jucator_viata = jucator_viata - 10
                              inamic_viata = inamic_viata + 30
                              print("\n Inamicul a folosit Vampirism! -10HP si +30HEAL")

        if inamic_in_flacari > 0:
               inamic_viata = inamic_viata - damage_flacari
               inamic_in_flacari = inamic_in_flacari - 1
               print(f"\n Inamicul arde! Pierde {damage_flacari} HP ")

        if healing_duration > 0:
               jucator_viata = jucator_viata + healing_effect
               healing_duration = healing_duration - 1
               print(f" \n Healing! Vindeci {healing_effect} HP")

        if cooldown_healing > 0:
              cooldown_healing = cooldown_healing - 1

        if cooldown_fireball > 0:
              cooldown_fireball = cooldown_fireball - 1

        if cooldown_icicles > 0:
              cooldown_icicles = cooldown_icicles - 1

print(f"\n Rezultatul meciului: Viata ta: {jucator_viata}, Viata inamicului: {inamic_viata}")

if inamic_viata > 0:
   print("\n Tragic bro, cum sa pierzi bro? Baka")
elif jucator_viata > 0:
   print("\n Regele bro, chiar l-ai batut, W MANZ")