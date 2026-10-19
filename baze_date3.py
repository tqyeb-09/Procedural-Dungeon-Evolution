import random

baze_date_inamici = {
    "zombie": {
        "nume": "zombie", 
        "hp": 130, 
        "hp_max": 130, 
        "physical_red": 15, 
        "magic_red": 8, 
        "sansa_evaziva": False,
        "camera_minima": 1, 
        "camera_maxima": 9,
        "materiale": {
            "iron_ingot": [
                {"sansa": 75, "cantitate": 1},
                {"sansa": 50, "cantitate": 2},
                {"sansa": 30, "cantitate": 3}
            ],
            "glass": [
                {"sansa": 60, "cantitate": 1},
                {"sansa": 20, "cantitate": 2},
            ]
        },
        "abilitati": [
            {
                "nume": "Muscatura", 
                "dmg": 10, 
                "tip": "physical", 
                "lifesteal": 20, 
                "infection": 1
            },
            {
                "nume": "Pumn", 
                "dmg": 15, 
                "tip": "physical"
            }
        ]
    },
    "skelete": {
        "nume": "skelete", 
        "hp": 100, 
        "hp_max": 100, 
        "physical_red": 5, 
        "magic_red": 10, 
        "sansa_evaziva": False,
        "camera_minima": 1, 
        "camera_maxima": 9,
        "abilitati": [
            {
                "nume": "Aruncare Os", 
                "dmg": 10, 
                "tip": "physical", 
                "crowd_control": {
                    "tip_cc": "ametire", 
                    "durata_max": 1, 
                    "text": "esti ametit"
                }
            },
            {
                "nume": "Sword Slash", 
                "dmg": 20, 
                "tip": "physical", 
                "efect_DoT": {
                    "tip_status": "bleed", 
                    "dmg_tura": 10, 
                    "durata_max": 3, 
                    "stat_scalare": "physical_dmg",
                    "text": "sangerezi"
                }
            },
            {
                "nume": "Pumn", 
                "dmg": 15, 
                "tip": "physical"
            },
            {
                "nume": "Picior", 
                "dmg": 15, 
                "tip": "physical"
            }
        ]
    },
    "elf": {
        "nume": "elf", 
        "hp": 90, 
        "hp_max": 90, 
        "physical_red": 7, 
        "magic_red": 15, 
        "sansa_evaziva": True,
        "camera_minima": 3, 
        "camera_maxima": 9,
        "abilitati": [
            {
                "nume": "Bow Shot", 
                "dmg": 15, "tip": 
                "physical"
            },
            {
                "nume": "Bow Barrage", 
                "dmg": 25, 
                "tip": "physical"
            },
            {
                "nume": "Dizzy Arrow", 
                "dmg": 10, 
                "tip": "physical", 
                "crowd_control": {
                    "tip_cc": "ametire", 
                    "durata_max": 1, 
                    "text": "esti ametit"
                }
            },
            {
                "nume": "Circular Arrow", 
                "dmg": 20, 
                "tip": "physical"
            }
        ]
    },
    "goblin": {
        "nume": "goblin", 
        "hp": 110, 
        "hp_max": 110, 
        "physical_red": 8, 
        "magic_red": 8, 
        "sansa_evaziva": True,
        "camera_minima": 5, 
        "camera_maxima": 9,
        "abilitati": [
            {
                "nume": "Dagger Slash", 
                "dmg": 15, 
                "tip": "physical", 
                "efect_DoT": {
                    "tip_status": "bleed", 
                    "dmg_tura": 15, 
                    "durata_max": 2, 
                    "stat_scalare": "physical_dmg",
                    "text": "sangerezi"
                }
            },
            {
                "nume": "Pickpocket", 
                "furat_gold": 20
            },
            {
                "nume": "Stealth Attack", 
                "dmg": 10, 
                "tip": "physical", 
                "crowd_control": {
                    "tip_cc": "ametire", 
                    "durata_max": 1, 
                    "text": "esti ametit"
                }
            },
            {
                "nume": "Flash Attack", 
                "dmg": 20, 
                "tip": "physical"
            }
        ]
    },
    "slime": {
        "nume": "slime", 
        "hp": 500, 
        "hp_max": 500, 
        "physical_red": 30, 
        "magic_red": 4, 
        "sansa_evaziva": False,
        "camera_minima": 10, 
        "camera_maxima": 10,
        "abilitati": [
            {
                "nume": "Acid Shot", 
                "dmg": 15, 
                "tip": "magic", 
                "efect_DoT": {
                    "tip_status": "poison", 
                    "dmg_tura": 20, 
                    "durata_max": 2, 
                    "stat_scalare": "magic_dmg",
                    "text": "esti otravit"
                }
            },
            {
                "nume": "Mancat", 
                "dmg": 10, 
                "tip": "physical", 
                "bonus_red": 2, 
                "bonus_hp": 5
            },
            {
                "nume": "Dizolva", 
                "dmg": 15, 
                "tip": "magic", 
                "size": 10
            }
        ]
    },
}

baze_date_abilitati = {
    "pumn": {
        "nume": "pumn", 
        "tip": "physical", 
        "stamina_gain": 5, 
        "mana_gain": 15, 
        "cooldown_max": 0, 
        "raritate": "comun",
        "multiplicator_dmg": 1,   
        },
    "fireball": {
        "nume": "fireball", 
        "tip": "magic", 
        "mana_cost": 50, 
        "cooldown_max": 2, 
        "raritate": "comun",
        "multiplicator_dmg": 2,
        "efect_DoT": {
            "tip_status": "burn",
            "dmg_tura": 10,
            "durata_max": 3,
            "stat_scalare": "magic_dmg",
            "text": "este in flacari!"
        }
    },
    "air_slashes": {
        "nume": "air slashes", 
        "tip": "physical", 
        "stamina_cost": 15, 
        "cooldown_max": 3, 
        "raritate": "comun",
        "multiplicator_dmg": 2.5,
        "efect_DoT": {
            "tip_status": "bleed",
            "dmg_tura": 15,
            "durata_max": 3,
            "stat_scalare": "physical_dmg",
            "text": "sangereaza"        
        }
    },
    "icicles": {
        "nume": "icicles", 
        "tip": "magic", 
        "mana_cost": 60, 
        "cooldown_max": 4, 
        "raritate": "comun",
        "multiplicator_dmg": 2,
        "crowd_control": {
            "tip_cc": "inghetare",
            "durata_max": 1,
            "inghetat": True,
            "text": "este inghetat"
        },
    },
    "eruption": {
        "nume": "eruption", 
        "tip": "magic", 
        "mana_cost": 75, 
        "cooldown_max": 3, 
        "raritate": "rar",
        "multiplicator_dmg": 3.5,
        "efect_DoT": {
            "tip_status": "melt",
            "dmg_tura": 30,
            "durata_max": 2,
            "stat_scalare": "magic_dmg",
            "text": "se topeste de la temperatura"
            }

        },
    "soul_drain": {
        "nume": "soul_drain",
        "tip": "true", 
        "mana_cost": 100, 
        "cooldown_max": 6, 
        "raritate": "rar",
        "multiplicator_dmg": 0.2,
        "efect_special": {
            "tip_special": "lifesteal",
            "hp_steal": 100,
            "stat_scalare": None,
            "text": "isi pierde energia vitala si slabeste si primesti energia lui vitala"
        }
    }
    }

baze_date_equipments = {
    "casca_de_lemn": {
        "nume": "casca_de_lemn", 
        "bonus_physical_red": 1, 
        "bonus_hp": 10, 
        "tip": "defensiv", 
        "raritate": "comun", 
        "pret": 20, 
        "slot": "equipment_cap"
        },
    "iron_chestplate": {
        "nume": "iron_chestplate", 
        "bonus_physical_red": 3, 
        "bonus_hp": 20, 
        "tip": "defensiv", 
        "raritate": "comun", 
        "pret": 40, 
        "slot": "equipment_piept"
        },
    "sabie_oase": {
        "nume": "sabie_oase", 
        "bonus_physical_dmg": 15, 
        "tip": "ofensiv", 
        "raritate": "comun", 
        "pret": 35, 
        "slot": "equipment_sabie",
        "efect_DoT": {
            "tip_status": "bleed", 
            "dmg_tura": 2, 
            "durata_max": 3,
            "stat_scalare": "physical_dmg",
            "text": "sangereaza de la taietura sabiei de oase"
            },
        },
    "fire_ring": {
        "nume": "fire_ring", 
        "bonus_magic_dmg": 5, 
        "tip": "ofensiv", 
        "raritate": "comun", 
        "pret": 30, 
        "slot": "equipment_inel",
        "efect_DoT": {
            "tip_status": "burn", 
            "dmg_tura": 3, 
            "durata_max": 3,
            "stat_scalare": "magic_dmg",
            "text": "este cuprins in faclari de la activarea inelului de foc"
            },
        },
    "leather_boots": {
        "nume": "leather_boots", 
        "bonus_physical_red": 2, 
        "bonus_hp": 15, 
        "tip": "defensiv", 
        "raritate": "comun", 
        "pret": 25, 
        "slot": "equipment_picioare"
        },
}

sanse_raritati_equipments = {
    "comun": 50,
    "rar": 30,
    "epic": 15,
    "legendar": 4,
    "mythic": 1
}

baze_date_grimoires = {
    "grimoire_comun": {
        "sansa": 50,
        "nume": "Grimoire comun", 
        "raritate": "comun"
    },
    "grimoire_rar": {
        "sansa": 80,
        "nume": "Grimoire rar", 
        "raritate": "rar"
    },
    "grimoire_epic": {
        "sansa": 95,
        "nume": "Grimoire epic", 
        "raritate": "epic"
    },
    "grimoire_legendar": {
        "sansa": 100,
        "nume": "Grimoire legendar", 
        "raritate": "legendar"
    }
    }

sanse_grimoire = {
    "grimoire_comun": {
        "comun": 70,
        "rar": 25,
        "epic": 4,
        "legendar": 1
    },
    "grimoire_rar": {
        "comun": 30,
        "rar": 50,
        "epic": 15,
        "legendar": 5
    },
    "grimoire_epic": {
        "comun": 10,
        "rar": 25,
        "epic": 50,
        "legendar": 15
    },
    "grimoire_legendar": {
        "comun": 0,
        "rar": 10,
        "epic": 50,
        "legendar": 40
    }
}

baze_date_perks = {
    "dmg_perk": {
        "nume": "dmg_perk", 
        "bonus_dmg_multiplicativ": 10,
        "raritate": "comun",
        "tip": "ofensiv"
    },
    "hp_perk": {
        "nume": "hp_perk", 
        "bonus_hp": 30,
        "bonus_hp_max": 30,
        "raritate": "comun",
        "tip": "defensiv"
    },
    "lifesteal_perk": {
        "nume": "lifesteal_perk", 
        "bonus_lifesteal": 5,
        "raritate": "comun",
        "tip": "ofensiv"
    },
    "red_perk": {
        "nume": "red_perk", 
        "bonus_red_multiplicativ": 10,
        "raritate": "comun",
        "tip": "defensiv"
    },
    "chill_perk": {
        "nume": "chill_perk",
        "bonus_freezing_chance": 10,
        "raritate": "comun",
        "tip": "ofensiv"
    }
}

sanse_raritati_perks = {
    "comun": 60,
    "rar": 25,
    "epic": 12,
    "legendar": 3
}

baze_date_deals = {
    "angel": {
        "blessing": {
            "bonus_hp_max": 50,
            "bonus_dmg_multiplicativ": 10,
            "bonus_red_multiplicativ": 20,
            "bonus_luck": 20,
            "cost_gold": 150,
            "bonus_mana_max": 100
        },
        "heavenly_pact": {
            "bonus_hp_max": 30,
            "bonus_physical_red": 1,
            "bonus_magic_red": 1,
            "bonus_crit_chance": 10,
            "bonus_crit_damage": 0.20,
            "cost_gold": 100,
            "bonus_stamina_max": 50
        }
    },
    "devil": {
        "devils_eye": {
            "bonus_physical_dmg": 15,
            "bonus_magic_dmg": 10,
            "bonus_crit_chance": 5,
            "pay_off": {
                "pay_hp_max": 40,
            }
        },
        "curse": {
            "bonus_dmg_multiplicativ": 20,
            "bonus_lifesteal": 10,
            "bonus_omnivamp": 5,
            "pay_off": {
                "pay_hp_max": 20,
                "pay_physical_red": 2,
                "pay_magic_red": 3,
                "pay_luck": 15
            }
        }
    }
}

setari_echilibru = {
    "scala_regenerare_mana": 10,
    "scala_regenerare_stamina": 3,
    "scala_regenerare_hp": 5
}

baze_date_milestones = {
    5: {
        "bonus_hp_max_multiplicativ": 10, 
        "text": " Milestone Nivel 5: Vitalitatea ta a fost amplificată cu 10%!"
    },
    10: {
        "bonus_dmg_multiplicativ": 10, 
        "bonus_red_multiplicativ": 10, 
        "text": f" Milestone Nivel 10: Forța ofensivă și defensivă au crescut cu 10%!"
    },
    20: {
        "bonus_crit_chance": 10, 
        "bonus_crit_dmg": 20, 
        "text": f" Milestone Nivel 20: Șansa de critic +10% și Dauna critică +20%!"
    },
    25: {
        "bonus_luck": 30, 
        "text": "Milestone Nivel 25: +30 luck!"
    },
    50: {
        "bonus_hp_max_multiplicativ": 10,
        "bonus_dmg_multiplicativ": 10,
        "bonus_red_multiplicativ": 10,
        "bonus_crit_chance": 10,
        "bonus_crit_dmg": 30,
        "bonus_luck_multiplicativ": 10,
        "bonus_lifesteal": 10,
        "bonus_omnivamp": 10,
        "text": " MILESTONE MAXIM (Nivel 50): Ai atins statutul de Divinitate! Toate statisticile au crescut masiv!"
    }
}

baze_date_blacksmith = {
    "1": {
        "nume_obiect": "Witch Hat",
        "tip": "hat",
        "cerinte": {
            "glass": 5, 
            "iron_ingot": 2
            },
        "bonusuri": {
            "bonus_magic_dmg": 10, 
            "bonus_magic_red": 2
            },
        "upgrades": {
            "iron_ingot_needed": 2,
            "glass_needed": 1
        },
        "text": "Crafteaza Witch's Hat (+10 Magic DMG, +2 Magic Reduction) [Cost: 5x Glass, 2x Iron Ingot]"
    },
    "2": {
        "nume_obiect": "Stone Ring",
        "tip": "ring",
        "cerinte": {
            "glass": 3, 
            "iron_ingot": 6
            },
        "bonusuri": {
            "bonus_magic_dmg": 5, 
            "bonus_red_multiplicativ": 10
            },
        "passives": [
            {
                "nume": "stone_shield",
                "tip_abilitate": "passive",
                "recharge_time": 3,
                "flat_shield": 10,
                "cu_conditie": True,
                "stat_scalare": "hp_max"
            },
            {
                "nume": "iron_skin",
                "tip_abilitate": "active",
                "tip": "defensive",
                "cooldown_max": 6,
                "duration_max": 3,
                "mana_cost": 30,
                "procent_scalare": 50,
                "stat_scalare": "physical_red"
            }
        ],
        "upgrades": {
            "iron_ingot_needed": 1,
            "glass_needed": 3
        },
        "text": "🪨 Forjează Stone Ring (+5 MAGIC DMG, +10% RED MULT) [Cost: 3x Glass, 6x Iron Ingot]"
    }
}