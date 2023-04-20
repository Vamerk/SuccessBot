import sqlite3
import random
from PIL import Image
from loader import dp, bot


async def send_lootbox(user_id):
    chance = random.randrange(0, 100)
    if chance >= 50:
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

    gantel = random.randint(0, 3)
    path = 'Person_image/generate_image'
    cross = random.choices([f'{path}/cross-1.png', f'{path}/cross-2.png', f'{path}/cross-3.png'])[0]
    remen = random.choices([f'{path}/belt-0.png', f'{path}/belt-1.png'])[0]
    undp = random.choices([f'{path}/undp-cc.png', f'{path}/undp-gold.png', f'{path}/undp-russia.png'])[0]
    loot = random.choices([gantel, cross, remen, undp], weights=[90, 2, 5, 3])[0]

    if loot == gantel:
        cur.execute(f"UPDATE inventory SET gantel=gantel+{loot}, lootboxs_s=lootboxs_s-1 WHERE id=?", (user_id,))
        cur.execute(f"UPDATE gameinf SET stamina=stamina+{loot*0.05} WHERE id=?", (user_id,))
        con.commit()
        return f'{loot} гантелей'

    elif loot == cross:
        update_pers_photo(user_id, cross)
        return '👟Кроссовки'

    elif loot == remen:
        update_pers_photo(user_id, remen)
        return '🥇Пояс'

    elif loot == undp:
        update_pers_photo(user_id, undp)
        return '🩲Трусы)'

    else: return 'Ничего((('

    cur.close()
    con.close()


def open_premium_lootbox(user_id):
    con = sqlite3.connect('gamebase.db')
    cur = con.cursor()

    gantel = random.randint(1, 5)
    path = 'Person_image/generate_image'
    cross = random.choices([f'{path}/cross-1.png', f'{path}/cross-2.png', f'{path}/cross-3.png'])[0]
    remen = random.choices([f'{path}/belt-0.png', f'{path}/belt-1.png'])[0]
    undp = random.choices([f'{path}/undp-cc.png', f'{path}/undp-gold.png', f'{path}/undp-russia.png'])[0]
    loot = random.choices([gantel, cross, remen, undp], weights=[50, 12, 20, 18])[0]

    if loot == gantel:
        cur.execute(f"UPDATE inventory SET gantel=gantel+{loot}, lootboxs_p=lootboxs_p-1 WHERE id=?", (user_id,))
        cur.execute(f"UPDATE gameinf SET stamina=stamina+{loot*0.05} WHERE id=?", (user_id,))
        con.commit()
        return f'{loot} гантелей'

    elif loot == cross:
        update_pers_photo(user_id, cross)
        return '👟Кроссовки'

    elif loot == remen:
        update_pers_photo(user_id, remen)
        return '🥇Пояс'

    elif loot == undp:
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
