import pygame
from utils import *


request_android_permissions()


pygame.init()
conf_path = p('config.json')
android_conf_path = '/storage/emulated/0/pynetpong.json'
if file_exists(conf_path):
    conf = read_json(conf_path)
elif is_android and file_exists(android_conf_path):
    conf = read_json(android_conf_path)
else:
    conf = {
        'width': 1024,
        'height': 768,
        'fullscreen': is_android,
        'fps': 60,
        'vsync': False,
        'no_fps_limit': is_android,
        'smooth_fix': False,
        'anti_aliasing': True,
        'show_fps': True,
        'use_gzip': False
    }
    write_json(conf_path, conf)
w, h = conf.get('width'), conf.get('height')
screen = pygame.display.set_mode(
    (w, h),
    (pygame.FULLSCREEN if is_android or conf.get('fullscreen') else 0),
    vsync=conf.get('vsync')
)
if is_android:
    w, h = screen.get_size()
    conf['width'], conf['height'] = w, h
pygame.display.set_caption('Pixelsuft PyNetPong')
pygame.display.set_icon(pygame.image.load(p('images', 'favicon.png')).convert_alpha())
set_var('conf', conf)
set_var('screen', screen)
import main_menu
main_menu.main()
