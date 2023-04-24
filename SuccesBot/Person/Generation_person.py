import sqlite3
from PIL import Image
import random

name = open('data/Names.txt').readlines()


class NewPerson():
    def __init__(self, user_id):
        random_Name = name[random.randint(1, 363)]
        con = sqlite3.connect('gamebase.db', timeout=10)
        cursor = con.cursor()
        cursor.execute(
            f'UPDATE gameinf SET status = 1, name = "{random_Name}", money = 100, class = 1, health = 100, stamina = 25, level = 1 WHERE id = ?',
            (user_id,))
        con.commit()
        cursor.close()
        con.close()

        path = 'Person_image/generate_image'
        head_img_mas = [f'{path}/head-1.png', f'{path}/head-2.png', f'{path}/head-3.png', f'{path}/head-4.png',
                        f'{path}/head-5.png', f'{path}/head-6.png', f'{path}/head-7.png']
        body_img_mas = [f'{path}/body-1.png', f'{path}/body-2.png', f'{path}/body-3.png', f'{path}/body-4.png']
        hand_img_mas = [f'{path}/hand-1.png', f'{path}/hand-2.png', f'{path}/hand-3.png']
        leg_img_mas = [f'{path}/leg-1.png', f'{path}/leg-2.png', f'{path}/leg-3.png', f'{path}/leg-4.png']
        undp_img_mas = [f'{path}/undp-1.png', f'{path}/undp-2.png', f'{path}/undp-3.png',
                        f'{path}/undp-5.png']

        fon_img = Image.open(f'{path}/fon.png')
        head_img = Image.open(random.choice(head_img_mas))
        body_img = Image.open(random.choice(body_img_mas))
        hand_img = Image.open(random.choice(hand_img_mas))
        leg_img = Image.open(random.choice(leg_img_mas))
        undp_img = Image.open(random.choice(undp_img_mas))

        person_img = Image.new('RGB', (200, 300))

        person_img.paste(fon_img, (0, 0))
        person_img.paste(head_img, (0, 0), mask=head_img)
        person_img.paste(body_img, (0, 0), mask=body_img)
        person_img.paste(hand_img, (0, 0), mask=hand_img)
        person_img.paste(leg_img, (0, 0), mask=leg_img)
        person_img.paste(undp_img, (0, 0), mask=undp_img)

        person_img.save(f'Person_image/user_image/user-{user_id}.png')
        print('Создан персонаж')
