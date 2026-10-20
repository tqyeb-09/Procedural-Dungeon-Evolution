# The Evolution of my Procedual Dungeon Game

Welcome to my core programming showcase! This repository tracks my evolution from the early days when I started programming up to the present day.

## My Code Optimization & Refactoring Timeline

### 🔹 Day 1: The Logical Foundation (`1V1 FIGHT.py`)
*   **Procedural Mechanics:** Began with hardcoded states variables (`jucator_viata = 100`, `inamic_viata = 200`) managed inside a basic dynamic `while` loop.
*   **Input Type Casting:** Utilized `int(input))` after `print` to change the user texts into a number, so it can check my options.
*   **Control Flow:** Utilized direct user inputs via terminal conditioning (`if/elif/else`) to handle the main combat moves (Normal Attack/ Special Attack, Heal) and dynamic cooldown systems (`cooldown_speciala`).
*   **Terminal Visual Formatting:** Utilized `f-strings` for clean dynamic text output to avoid tiring formatting like `str() + "HP"`, manually injecting `\n` to make the terminal more readable.

### 🔹 Day 2: Advanced State Mechanics & Turn-Based Engine (`BOSS.FIGHT.2.0.py`)
*   **Dynamic RNG Integration:** Imported the `random` module to add chances to the game. Implemented a 20% critical strike chance calculation (`random.randint(1, 5)`) on standard actions.
*   **Status Effect Framework (CC * DoT):** Created effects that last multiple turns. Introduced Crowd Control (`inamic_inghetat` stun that bypasses enemy turns) and Damage over Time (`inamic_in_flacari` that states the number of turns that the enemy is taking damage from the effect and `damage_flacari` that states the damage of the effect).
*   **Healing over Time (HoT):** Developed a tracking buffer for the player status pool, handling turn by turn health regeneration (`healing_duration`).
*   **Randomized Enemy Attacks:** Upgraded enemy behavior from static counters to a dynamic move pool selection machine (Basic Attack, Devastating Blow, and Vampirism/Lifesteal actions).
*   **Turn-State Reset Pipelines:** Integrated an automated cooldown/duration decrement logic layer executing cleanly at the termination of each active game loop interval.

### 🔹 Day 4: Structural Transition: Mechanics Testing (`Dodge.exe.py`)
*   **The Dodge Probability Engine:** Transformed standard turn combat into a probabilistic mechanics framework. There's a 20% chance (`random.randint(1, 5)`) where hits are completely nullified if the entity triggers the evasion mechanic.
*   **Bleed Effect (DoT):** Designed a tracking algorithm for physical attacks over multiple turns for both entities (`sangerare_inamic`, `sangerare_jucator`). Applied a damage layer that ticks down round by round.
*   **RNG on Crowd Control (RNG/CC):** Made a stun effect that triggers only on critical attacks that have a 20% chance (`randon.randint(1, 5)`).
*   **Early Defensive Programming Boundaries:** Introduced a boundary protection for entities hit points. Forcing negative integers directly to `0` for proper visual integrity during end-game status report.

### 🔹 Day 6: Resource Management, Cutscenes & Phase Transitions (`BOSS.FIGHT.3.0.py`)
*   **Advanced AI Phase Transition (Berserk Mode):** Implemented an automated health threshold trigger (50% max hp) that transitions the boss into a `berserk` state. Utilized inline conditional statements (`X if berserk else Y`) to dynamically scale damage multipliers.
*   **State-Driven AI Attack Restriction:** Introduced a complex `dizzy` (disorientation) status modifier. When active, it forces the enemy AI to mutate its state machine, shrinking its available random attack vector selection from a pool of 5 to a restricted pool of 3 weaker actions.
*   **Cinematic Pacing Engine:** Integrated the `time` module to break standard loops and construct artificial suspense intervals. Executed structured text-based cinematic cuts (`time.sleep()`) during heavy damage abilities to alter the game feeling and user immersion.
*   **Energy Mechanic:** Added an energy system with a threshold (`energie = 300`), where the ultimate ability costs energy to use. The loop checks if you have enough energy before letting you cast the ability.

### 🔹 Day 7-8: Advanced Combat Mechanics & Boss Phases (`1v1.FIGHT.4.0.py`)
*   **Dynamic Energy Economy:** Integrated randomized energy regeneration using `random.choice()` and capped the maximum resource at `energy = 100` and every move costs energy.
*   **Illegal Action Penalties:** Implemented a system that actively penalizes invalid moves or bad choices (`if alegere >= or alegere <= 0`) by draining `20` energy from the player's pool.
*   **Reactive Player Rage Mode:** Added a low-health check (`jucator_viata <= 0.30 * jucator_viata_maxima`) that activates `rage = True`, scaling up player damage when entering a critical survival state. Also added `rage_mesaj = False` that turns into `rage_mesaj = True` when the rage mode activates, so the `print()` where it tells that you entered rage mode shows up only once per fight in terminal.
*   **Multi-Phase Boss Evolution:** Implemented a boss phase change; landing on a specific threat roll (`atack_inamic == 10`) that triggers `berserk = True`, altering the boss's attack pool, increasing its damage output.
*   **Layered Bleed Effect:** Expanded Damage over Time tracking by splitting bleed effects into two independent variables (`sangerare` and `sangerare_ultimata`) that ticks down separately
