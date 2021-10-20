import os
import json
import sys
import random
import pygame
from functools import lru_cache
from PIL import Image
try:
    import android
    from android.permissions import request_permissions, Permission
    is_android = True
except ImportError:
    is_android = False


cur_path = os.getcwd()
vars_ = {}
dir_exists = os.path.isdir
encoding_ = sys.getdefaultencoding()
numbers = tuple((1, 2, 3, 4, 5, 6, 7, 8, 9, 0))
str_numbers = tuple(str(x) for x in numbers)


def str_to_int(number: str) -> int:
    return round(float(number))


def random_float(min_number: float, max_number: float) -> float:
    return random.random() * (max_number - min_number) + min_number


def request_android_permissions() -> None:
    if not is_android:
        return
    request_permissions([
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.INTERNET
    ])


def p(*args) -> str:
    return os.path.join(cur_path, *args)


def to_image(pillow_img: Image.Image, alpha=True) -> pygame.Surface:
    result = pygame.image.fromstring(
        pillow_img.tobytes(), pillow_img.size, pillow_img.mode
    )
    return result.convert_alpha() if alpha else result.convert()


def from_image(pygame_image: pygame.Surface, mode: str = 'RGBA', is_flipped: bool = False) -> Image.Image:
    return Image.frombytes(
        mode,
        pygame_image.get_size(),
        pygame.image.tostring(
            pygame_image,
            mode,
            is_flipped
        ),
    )


def file_exists(filename: str) -> bool:
    return os.access(filename, os.F_OK)


def fast_read(filename: str, response_type: type = str, encoding: str = 'utf-8'):
    temp_file = open(filename, 'rb')
    result = temp_file.read()
    temp_file.close()
    return result if not response_type == str else result.decode(encoding)


def fast_write(filename: str, content) -> int:
    temp_file = open(filename, 'w' if type(content) == str else 'wb')
    result = temp_file.write(content)
    temp_file.close()
    return result


def read_json(filename: str) -> dict:
    return json.loads(fast_read(filename))


def write_json(filename: str, json_: dict) -> int:
    return fast_write(filename, json.dumps(json_))


def set_var(var_name: str, var_content: any) -> any:
    vars_[var_name] = var_content
    return var_content


def get_var(var_name: str) -> any:
    return vars_.get(var_name)


def loading_phrase_to_img(phrase: str, font_dir_path: str, space: int = 50, a1: int = 12, a2: int = 4) -> Image.Image:
    phrase_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    font_conf = read_json(os.path.join(font_dir_path, 'letters.json'))
    for i in phrase.upper():
        if i == ' ':
            i = 'space'
        elif i not in font_conf:
            continue
        letter_id = font_conf[i]['id']
        left_backup = phrase_img.size[0]
        if i == 'space':
            phrase_img = phrase_img.crop((
                0,
                0,
                phrase_img.size[0] + space,
                phrase_img.size[1]
            ))
        else:
            phrase_img = phrase_img.crop((
                0,
                0,
                phrase_img.size[0] + font_conf[i]['width'] - a1,
                font_conf[i]['height'] + font_conf[i]['yoffset'] if font_conf[i]['height'] + font_conf[i]['yoffset'] >
                phrase_img.size[1] else phrase_img.size[1]
            ))
            letter_img = Image.open(os.path.join(font_dir_path, f'{font_conf[i]["id"]}.png'))
            phrase_img.paste(letter_img.crop((
                a2,
                0,
                letter_img.size[0] - a2,
                letter_img.size[1]
            )), (left_backup + font_conf[i]['xoffset'], font_conf[i]['yoffset']))
    return phrase_img


def find_nod(a: int, b: int):
    while b:
        a, b = b, a % b
    return a


def round_image(image: Image.Image, border: int) -> Image.Image:
    iw, ih = image.size
    for i in range(border):
        for j in range(border - i):
            image.putpixel((i, j), (0, 0, 0, 0))
        for j in range(i):
            image.putpixel((border - i - 1, ih - j - 1), (0, 0, 0, 0))
        for j in range(border - i):
            image.putpixel((iw - i - 1, j), (0, 0, 0, 0))
        for j in range(i):
            image.putpixel((iw - border + i, ih - j - 1), (0, 0, 0, 0))
    return image


@lru_cache(maxsize=100)
def is_colliding(object_rect: tuple, x: int, y: int) -> bool:
    if object_rect[0] + object_rect[2] > x > object_rect[0] and object_rect[1] + object_rect[3] > y > object_rect[1]:
        return True
    return False


def def_width(is_colliding_: bool) -> int:
    return 0 if is_colliding_ else 5


def random_color(alpha_: bool = False) -> tuple:
    if alpha_:
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def invert_color(color: tuple) -> tuple:
    return tuple(255 - i for i in color)


def random_ball_speed(min_: int = -5, max_: int = 5) -> list:
    x_ = 0
    while x_ == 0:
        x_ = random.randint(min_, max_)
    y_ = 0
    while y_ == 0:
        y_ = random.randint(min_, max_)
    return [x_, y_]
