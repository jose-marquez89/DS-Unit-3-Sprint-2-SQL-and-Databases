import os
import sqlite3

path = os.path.join(os.path.dirname(__file__), "rpg_db.sqlite3")
conn = sqlite3.connect(path)
conn.row_factory = sqlite3.Row

c = conn.cursor()

# How many total characters are there?
q1 = """
SELECT COUNT(DISTINCT charactercreator_character.name)
FROM charactercreator_character;
"""
r1 = c.execute(q1).fetchall()

print(f"Total Characters: {r1[0][0]}")

# How many total items?
q2 = """
SELECT COUNT(DISTINCT armory_item.name) as UniqueItems
FROM armory_item;
"""
r2 = c.execute(q2).fetchall()

print(f"Total Items: {r2[0][0]}")

# How many items are weapons?
q3 = """
SELECT COUNT(*) as TotalWeapons
FROM armory_item JOIN armory_weapon
ON armory_item.item_id = armory_weapon.item_ptr_id;
"""
r3 = c.execute(q3).fetchall()

print(f"Total Weapon Items: {r3[0][0]}\n")
print("SUBCLASSES:")
print("==========")

char_types = ['mage', 'thief', 'cleric', 'fighter']
# How many total subclasses?
for char_type in char_types:

    query = f"""
SELECT
COUNT(DISTINCT charactercreator_{char_type}.character_ptr_id) AS {char_type}s
FROM charactercreator_{char_type};
    """
    result = c.execute(query).fetchall()

    print(f"\tTotal {char_type.title()}: {result[0][0]}")

necro_q = """
SELECT
COUNT(DISTINCT charactercreator_necromancer.mage_ptr_id) AS nmncrs
FROM charactercreator_necromancer;
"""
necro_r = c.execute(query).fetchall()

print(f"\tTotal Necromancer: {necro_r[0][0]}")

# How many items does each character have (first 20 rows)
q5 = """
SELECT
  charactercreator_character_inventory.character_id,
  count(distinct charactercreator_character_inventory.item_id) as ItemTotal
FROM charactercreator_character_inventory
GROUP BY charactercreator_character_inventory.character_id
LIMIT 20;
"""
r5 = c.execute(q5)

header = "Character ID | Item Total"
print("\n" + header)
for row in r5:
    for i in range(len(row)):
        if i == 0:
            print(str(row[i]).ljust(13), end='| ')
        else:
            print(str(row[i]))

# How many items does each character have (first 20 rows)
q6 = """
SELECT
  charactercreator_character_inventory.character_id,
  count(distinct charactercreator_character_inventory.item_id) as WeaponTotal,
  armory_weapon.item_ptr_id
FROM charactercreator_character_inventory, armory_weapon
WHERE charactercreator_character_inventory.item_id = armory_weapon.item_ptr_id
GROUP BY charactercreator_character_inventory.character_id
LIMIT 20;
"""
r6 = c.execute(q6)

header = "Character ID | Weapon Total | Item ID"
print("\n" + header)
for row in r5:
    for i in range(len(row)):
        if i == 0 or i == 1:
            print(str(row[i]).ljust(13), end='| ')
        else:
            print(str(row[i]))
