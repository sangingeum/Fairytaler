import json

save_name = "resource"

# Define the data you want to store in the JSON file
data = {"character": [{"name": "Robin", "relationships": {}, "companions": {}, "items": [],
                       "background": "a traveler who was born and raised in a small village nestled deep in a dense forest. When he/she was just a child, his/her village was attacked by a powerful dark wizard, who unleashed a barrage of destructive spells that left the village in ruins. Along with a few survivors, he/she managed to escape the carnage and fled into the wilderness.",
                       "personality": "adventurous",
                       "race": "human",
                       "gender": "male"
                       }
                      ],
        "item": [
                {"name": "Mana potion", "description" : "A potion that restores a creature's magical energy or mana."},
                {"name": "Poisoned dagger", "description": "A dagger that is coated in a poisonous substance, making it especially deadly to enemies."},
                {"name": "Cloak of invisibility", "description": "A magical cloak that makes the wearer invisible, allowing them to move undetected through the world."},
                {"name": "Holy water", "description": "A blessed water that can be used to repel or harm undead creatures, such as vampires or zombies."},
                {"name": "Enchanted bow", "description": "A bow that has been imbued with magical energy, making its arrows more powerful or able to seek out their targets."},
                {"name": "Ring of teleportation", "description": "A magical ring that allows the wearer to teleport to any location they have previously visited."},
                {"name": "Staff of fire", "description": "A powerful staff that can be used to summon flames or unleash devastating fire-based spells."},
                {"name": "Amulet of protection", "description": "An amulet that provides protection against a specific type of harm, such as physical attacks, magical attacks, or curses."},
                {"name": "Book of spells", "description": "A book filled with arcane knowledge and spells, allowing its owner to cast powerful magical spells."},
                {"name": "Potion of transformation", "description": "A potion that can be used to transform the drinker into a different creature or form, such as a dragon, a wolf, a bird or fish."},
                {"name": "Wand of levitation", "description": "A wand that can be used to levitate objects or creatures, allowing them to move through the air."},
                {"name": "Ring of regeneration", "description": "A ring that grants its wearer the ability to heal rapidly from wounds or injuries."},
                {"name": "Boots of speed", "description": "Magical boots that allow their wearer to move faster than normal, making them difficult to catch or evade."},
                {"name": "Scroll of summoning", "description": "A scroll that can be used to summon a creature or object from another realm or dimension."},
                {"name": "Crystal ball", "description": "A magical crystal ball that can be used to scry on distant locations or people, allowing its user to see and hear what is happening elsewhere."},
                {"name": "Helm of night vision", "description": "A helmet that enhances its wearer's ability to see in low light conditions, such as during the night or in underground caverns."},
                {"name": "Staff of elemental control", "description": "A powerful staff that can be used to control elemental forces, such as wind, water, earth, or fire."},
                {"name": "Amulet of flight", "description": "An amulet that grants its wearer the ability to fly, either through magic or by sprouting wings."},
                {"name": "Shield of reflection", "description": "A magical shield that can reflect back harmful spells or attacks, protecting its wielder from harm."},
                 ],
        "background": ["A survivor of a catastrophic event, such as a dragon attack or a magical explosion",
                        "A former member of a notorious band of thieves or pirates",
                        "A veteran of a long-standing conflict between two rival kingdoms or factions",
                        "A former prisoner of an evil sorcerer or demon lord",
                        "A former apprentice of a master craftsman or artisan who taught them a unique skill or trade",
                        "A member of a secret society or underground rebellion, fighting against an oppressive government or ruler",
                        "A cursed individual who has been afflicted with a terrible fate, such as lycanthropy or vampirism",
                        "A scholar or researcher who has dedicated their life to uncovering the mysteries of the world's ancient ruins and artifacts",
                        "A member of a traveling troupe of performers, such as bards or acrobats, who use their talents to entertain and inspire others",
                        "A hermit or recluse who has spent years living in isolation, honing their skills and contemplating the secrets of the universe",
                        "A prodigy of magic, who was born with an innate talent for casting spells and manipulating the elements",
                        "A descendant of an ancient lineage, with a noble heritage and access to powerful artifacts and secrets passed down through the generations",
                        "A survivor of a cursed land or realm, where the very earth and air are tainted with dark magic and malevolent spirits",
                        "A wanderer or nomad, who has traveled far and wide across the world, picking up knowledge and skills from different cultures and civilizations",
                        "A chosen one or prophesized hero, destined to fulfill a great quest or vanquish a terrible evil that threatens the world",
                        "A member of a guild or order of knights, warriors, or mages who uphold a strict code of honor and loyalty to their cause",
                        "An exile or outcast, banished from their homeland or society for a crime or taboo act, seeking redemption or vengeance",
                        "A scholar or historian who studies the lore and mythology of the world's ancient cultures and peoples, unlocking hidden knowledge and power",
                        "A cursed prince or princess, who has been transformed into a beast or monster by a wicked spell and must seek a cure to break the curse.",
                        "A mercenary or hired blade, who offers their services as a warrior or assassin for a price, but may have their own moral code or sense of justice.",
                        "A survivor of a lost civilization or forgotten kingdom, seeking to reclaim their heritage and uncover the secrets of their ancestors.",
                        "A monster hunter or slayer, who has devoted their life to tracking down and defeating the dangerous creatures that roam the land.",
                        "A descendant of a long line of seers or prophets, with the ability to see glimpses of the future or communicate with otherworldly beings.",
                        "A cursed or blessed individual with magical powers that they cannot control, causing chaos and destruction wherever they go.",
                        "A member of a druidic or nature-worshipping society, with a deep connection to the land and its spirits, able to call upon the power of nature in times of need.",
                        "A thief or rogue who operates in the shadows, using their wit and cunning to outsmart their enemies and acquire riches or information.",
                        "A member of a clan or tribe of warriors or hunters, bound by tradition and honor, and fiercely protective of their way of life and people.",

                        ],
        "personality": ["introverted", "extroverted", "optimistic", "pessimistic",
                        "creative", "analytic", "outgoing", "reserved",
                        "organized", "spontaneous", "honest", "deceitful",
                        "empathetic", "self-centered", "assertive", "passive",
                        "perfectionistic", "impulsive", "risk-averse", "sensitive",
                        "competitive", "collaborative", "charismatic", "adventurous"],
        "race": ["human", "elf", "dwarf", "orc", "goblin", "halfling",
                 "dragon", "giant", "merfolk", "centaurs", "minotaurs",
                 "gnome", "fairy", "undead", "demon", "angel", "naga",
                 "feline", "avian", "insectoid", "gargoyle",
                 "reptilian", "dryad", "harpy", "lamia", "kappa", "jinn"],
        "incident": ["fight", "love"]
        }

# Write the data to a JSON file
with open("{}.json".format(save_name), "w") as f:
    json.dump(data, f)

# Import the data from the JSON file into a list
with open("{}.json".format(save_name), "r") as f:
    data_from_file = json.load(f)

print(data_from_file)