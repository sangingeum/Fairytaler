import json

save_name = "resource"

# Define the data you want to store in the JSON file
data = {"character": [],
        "consumables": [
                {"name": "Mana potion", "description" : "A potion that restores a creature's magical energy or mana."},
                {"name": "Holy water", "description": "A blessed water that can be used to repel or harm undead creatures, such as vampires or zombies."},
                {"name": "Potion of transformation", "description": "A potion that can be used to transform the drinker into a different creature or form, such as a dragon, a wolf, a bird or fish."},
                {"name": "Scroll of summoning", "description": "A scroll that can be used to summon a creature or object from another realm or dimension."},
                {"name": "Crystal ball", "description": "A magical crystal ball that can be used to scry on distant locations or people, allowing its user to see and hear what is happening elsewhere."},
                 ],
        "equipments": [

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