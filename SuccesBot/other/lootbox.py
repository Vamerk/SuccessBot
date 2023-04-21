import sqlite3
import random
from PIL import Image
from Person import Inventory, Person



async def send_lootbox(user_id):
    chance = random.randrange(0, 100)
    if chance >= 1:
        con = sqlite3.connect('gamebase.db')
        cur = con.cursor()

        lootbox_type_chance = random.randrange(0, 100)
        if lootbox_type_chance >= 90:
            cur.execute("UPDATE inventory SET lootboxs_p=lootboxs_p+1 WHERE id=?", (user_id,))
            con.commit()
            return 2
        else:
            cur.execute("UPDATE inventory SET lootboxs_s=lootboxs_s+1 WHERE id=?", (user_id,))
            con.commit()
            return 1

        cur.close()
        con.close()
    return 0


def open_standart_lootbox(user_id):
    con = sqlite3.connect('gamebase.db')
    cur = con.cursor()

    invent = Inventory(user_id)

    pers = Person(user_id)
    lvl = pers.Level()

    gantel = random.randint(0, 2)
    path = 'Person_image/generate_image'
    cross = random.choices([f'{path}/cross-1.png', f'{path}/cross-2.png', f'{path}/cross-3.png'])[0]
    remen = random.choices([f'{path}/belt-0.png', f'{path}/belt-1.png'])[0]
    undp = random.choices([f'{path}/undp-cc.png', f'{path}/undp-gold.png', f'{path}/undp-russia.png'])[0]
    preloot = [gantel]
    ves = [90]
    if invent.sneakers() == 0:
        preloot.append(cross)
        ves.append(2)
    if invent.belt() == 0:
        preloot.append(remen)
        ves.append(5)
    if invent.undp() == 0:
        preloot.append(undp)
        ves.append(3)
    loot = random.choices(preloot, weights=ves)[0]

    if loot == gantel:
        cur.execute(f"UPDATE inventory SET gantel=gantel+{loot}, lootboxs_s=lootboxs_s WHERE id=?", (user_id,))
        cur.execute(f"UPDATE gameinf SET stamina=stamina+{loot * 0.05} WHERE id=?", (user_id,))
        con.commit()
        return f'{loot} гантелей'

    elif loot == cross:
        cur.execute(f"UPDATE inventory SET cross=cross+1 WHERE id=?", (user_id,))
        cur.execute(f"UPDATE gameinf SET health=health+{2 * lvl + 5} WHERE id=?", (user_id,))
        con.commit()
        update_pers_photo(user_id, cross)
        return '👟Кроссовки'

    elif loot == remen:
        cur.execute(f"UPDATE inventory SET remen=remen+1 WHERE id=?", (user_id,))
        cur.execute(f"UPDATE gameinf SET stamina=stamina+{2 * lvl + 5} WHERE id=?", (user_id,))
        con.commit()
        update_pers_photo(user_id, remen)
        return '🥇Пояс'

    elif loot == undp:
        cur.execute(f"UPDATE inventory SET undp=undp+1 WHERE id=?", (user_id,))
        cur.execute(f"UPDATE gameinf SET stamina=stamina+{1.5 * lvl + 3}, health=health+{1.5 * lvl + 3}  WHERE id=?", (user_id,))
        con.commit()
        update_pers_photo(user_id, undp)
        return '🩲Трусы)'

    else:
        return 'Ничего((('

    cur.close()
    con.close()


def open_premium_lootbox(user_id):
    con = sqlite3.connect('gamebase.db')
    cur = con.cursor()

    invent = Inventory(user_id)

    pers = Person(user_id)
    lvl = pers.Level()

    gantel = random.randint(3, 10)
    path = 'Person_image/generate_image'
    cross = random.choices([f'{path}/cross-1.png', f'{path}/cross-2.png', f'{path}/cross-3.png'])[0]
    remen = random.choices([f'{path}/belt-0.png', f'{path}/belt-1.png'])[0]
    undp = random.choices([f'{path}/undp-cc.png', f'{path}/undp-gold.png', f'{path}/undp-russia.png'])[0]
    preloot = [gantel]
    ves = [50]
    if invent.sneakers() == 0:
        preloot.append(cross)
        ves.append(12)
    if invent.belt() == 0:
        preloot.append(remen)
        ves.append(20)
    if invent.undp() == 0:
        preloot.append(undp)
        ves.append(18)
    loot = random.choices(preloot, weights=ves)[0]


    if loot == gantel:
        cur.execute(f"UPDATE inventory SET gantel=gantel+{loot}, lootboxs_s=lootboxs_s WHERE id=?", (user_id,))
        cur.execute(f"UPDATE gameinf SET stamina=stamina+{loot * 0.05} WHERE id=?", (user_id,))
        con.commit()
        return f'{loot} гантелей'

    elif loot == cross:
        cur.execute(f"UPDATE inventory SET cross=cross+1 WHERE id=?", (user_id,))
        cur.execute(f"UPDATE gameinf SET health=health+{2 * lvl + 5} WHERE id=?", (user_id,))
        con.commit()
        update_pers_photo(user_id, cross)
        return '👟Кроссовки'

    elif loot == remen:
        cur.execute(f"UPDATE inventory SET remen=remen+1 WHERE id=?", (user_id,))
        cur.execute(f"UPDATE gameinf SET stamina=stamina+{2 * lvl + 5} WHERE id=?", (user_id,))
        con.commit()
        update_pers_photo(user_id, remen)
        return '🥇Пояс'

    elif loot == undp:
        cur.execute(f"UPDATE inventory SET undp=undp+1 WHERE id=?", (user_id,))
        cur.execute(f"UPDATE gameinf SET stamina=stamina+{1.5 * lvl + 3}, health=health+{1.5 * lvl + 3}  WHERE id=?",
                    (user_id,))
        con.commit()
        update_pers_photo(user_id, undp)
        return '🩲Трусы)'

    else:
        return 'Ничего((('

    cur.close()
    con.close()


def update_pers_photo(user_id, new_image):
    path = 'Person_image/user_image'
    new_img = Image.open(new_image)
    pers_img = Image.open(f'{path}/user-{user_id}.png')
    pers_img.paste(new_img, (0, 0), mask=new_img)
    pers_img.save(f'{path}/user-{user_id}.png')
    print("Успех")
