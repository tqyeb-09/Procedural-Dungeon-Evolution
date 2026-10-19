# Personajul tău (Denis)
jucator_viata = 100
inamic_viata = 200
cooldown_speciala = 0
while jucator_viata > 0 and inamic_viata > 0:
    print(f"\n--- Viata ta: {jucator_viata} , Viata inamicului: {inamic_viata}")
    print("Alege atacul:")
    print("1.Atac normal:")
    print("2.Atac special")
    print("3 Heal")

    # Aici intervine int(input()) pentru a citi alegerea ta
    alegere = int(input("Introduce numarul actiunii: "))

    if alegere == 1:
        inamic_viata = inamic_viata - 25
    elif alegere == 2:
        if cooldown_speciala == 0:
            inamic_viata = inamic_viata - 50
            print("Atac mortal")
            cooldown_speciala = 2
        else:                               
            print(f"\n Cooldown bro, trebuie sa astepti inca {cooldown_speciala} ture.")
    elif alegere == 3:
        jucator_viata = jucator_viata + 40
    if inamic_viata > 0:
        jucator_viata = jucator_viata - 30
    if cooldown_speciala > 0:
        cooldown_speciala = cooldown_speciala - 1

print(f"\n Rezultatul meciului: Viata ta: {jucator_viata}, Viata inamicului: {inamic_viata}")

if inamic_viata > 0:
   print("\n Tragic bro, cum sa pierzi bro? Baka")
elif jucator_viata > 0:
   print("\n Regele bro, chiar l-ai batut, W MANZ")