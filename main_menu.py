import pygame
import socket
import main_game
from fps_clock import FPS
from socket_tools import *
from utils import *


def main() -> None:
    conf: dict = get_var('conf')
    w: int = conf.get('width')
    h: int = conf.get('height')
    show_fps: bool = conf.get('show_fps')
    aa: bool = conf.get('anti_aliasing')
    half_w = w / 2
    half_h = h / 2
    half_w_ = round(w / 2)
    half_h_ = round(h / 2)
    screen: pygame.Surface = get_var('screen')
    clock = FPS(conf.get('fps'), no_limit=conf.get('no_fps_limit'), smooth_fix=conf.get('smooth_fix'))
    bg_music_fn = p('sounds', random.choice(os.listdir(p('sounds'))))
    bg_music = pygame.mixer.Sound(bg_music_fn)
    set_var('bg_music', bg_music)
    bg_music.play(loops=-1)
    res_nod = find_nod(w, h)
    res_division = (round(w / res_nod), round(h / res_nod))
    use_16_9_bg = res_division[0] / res_division[1] >= 10 / 7
    bg_img = Image.open(p('images', 'bg_16_9.png' if use_16_9_bg else 'bg_4_3.png')).resize((w, h))
    pg_bg_img = to_image(bg_img, False)
    fps_font = pygame.font.Font(p('fonts', 'segoescb.ttf'), 25)
    label_font = pygame.font.Font(p('fonts', 'segoescb.ttf'), 25)
    need_ip_surface = label_font.render(
        f'IP: {", ".join(get_hosts())}', aa, (0, 0, 0)
    )

    inputs = {
        'host': socket.gethostbyname(socket.gethostname()),
        'port': '1337'
    }
    cur_input = ''

    button1_rect = (half_w_ - 100, 50, 200, 100)
    button1_text = label_font.render(
        'Connect', aa, (0, 0, 0)
    )
    button1_text_rect = (round(half_w - button1_text.get_size()[0] / 2), round(100 - button1_text.get_size()[1] / 2))

    button2_rect = (half_w_ - 100, 200, 200, 100)
    button2_text = label_font.render(
        'Run server', aa, (0, 0, 0)
    )
    button2_text_rect = (round(half_w - button2_text.get_size()[0] / 2), round(250 - button2_text.get_size()[1] / 2))
    button2_visible = True

    watermark_factor = 20
    watermark_color = random_color()
    watermark_text = label_font.render(
        'Pixelsuft, 2021', aa, random_color()
    )
    watermark_text_rect = (
        w - watermark_text.get_size()[0] - watermark_factor, h - watermark_text.get_size()[1] - watermark_factor
    )
    watermark_bg_rect = (
        w - watermark_text.get_size()[0] - watermark_factor,
        h - watermark_text.get_size()[1] - watermark_factor,
        watermark_text.get_size()[0],
        watermark_text.get_size()[1]
    )
    watermark_bg_color = invert_color(watermark_color)

    last_x, last_y = pygame.mouse.get_pos()
    is_down = False
    used_color = (0, 255, 0)
    unused_color = (0, 150, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                kill_all()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = last_x, last_y = pygame.mouse.get_pos()
                is_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = last_x, last_y = pygame.mouse.get_pos()
                is_down = False
                if is_colliding(button1_rect, x, y):
                    cur_input = ''
                    if button2_visible:
                        connect_server(inputs['host'], int(inputs['port']))
                        main_game.main(False, inputs['host'], int(inputs['port']))
                        continue
                    if sock[0]:
                        main_game.main(True, inputs['host'], int(inputs['port']))
                        continue
                    continue
                if is_colliding(button2_rect, x, y) and button2_visible:
                    button2_visible = False
                    cur_input = ''
                    button1_text = label_font.render(
                        'Launch', aa, (0, 0, 0)
                    )
                    button1_text_rect = (
                        round(half_w - button1_text.get_size()[0] / 2), round(100 - button1_text.get_size()[1] / 2)
                    )
                    run_server(inputs['host'], int(inputs['port']))
                    continue
                if x < half_w and button2_visible:
                    if 325 > y > 275:
                        cur_input = 'host'
                        pygame.key.start_text_input()
                        continue
                    if 375 > y > 325:
                        cur_input = 'port'
                        pygame.key.start_text_input()
                        continue
                    cur_input = ''
                    pygame.key.stop_text_input()
                    continue
                cur_input = ''
                pygame.key.stop_text_input()
            elif event.type == pygame.MOUSEMOTION:
                x, y = last_x, last_y = pygame.mouse.get_pos()
            elif event.type == pygame.KEYDOWN:
                if not cur_input:
                    continue
                if cur_input == 'host':
                    if event.key == pygame.K_BACKSPACE:
                        if len(inputs['host']) > 0:
                            inputs['host'] = inputs['host'][:-1]
                        continue
                    if event.unicode not in str_numbers + tuple('.'):
                        continue
                    inputs['host'] += event.unicode
                    continue
                if cur_input == 'port':
                    if event.key == pygame.K_BACKSPACE:
                        if len(inputs['port']) > 0:
                            inputs['port'] = inputs['port'][:-1]
                        continue
                    if event.unicode not in str_numbers:
                        continue
                    inputs['port'] += event.unicode
                    continue
        if not clock.try_tick():
            continue
        screen.blit(pg_bg_img, (0, 0))

        pygame.draw.rect(
            screen,
            used_color if is_down and is_colliding(button1_rect, last_x, last_y) else unused_color,
            button1_rect,
            border_radius=5,
            width=def_width(is_colliding(button1_rect, last_x, last_y))
        )
        screen.blit(button1_text, button1_text_rect)

        if button2_visible:
            pygame.draw.rect(
                screen,
                used_color if is_down and is_colliding(button2_rect, last_x, last_y) else unused_color,
                button2_rect,
                border_radius=5,
                width=def_width(is_colliding(button2_rect, last_x, last_y))
            )
            screen.blit(button2_text, button2_text_rect)

        screen.blit(label_font.render(
            f'Host: {inputs["host"]}' + ('|' if cur_input == 'host' else ''), aa, (0, 0, 0)
        ), (0, 300))

        screen.blit(label_font.render(
            f'Port: {inputs["port"]}' + ('|' if cur_input == 'port' else ''), aa, (0, 0, 0)
        ), (0, 325))

        screen.blit(need_ip_surface, (0, 350))

        pygame.draw.rect(screen, watermark_bg_color, watermark_bg_rect, border_radius=5)
        screen.blit(watermark_text, watermark_text_rect)

        if show_fps:
            cur_fps = clock.get_int_fps()
            screen.blit(fps_font.render(
                f'FPS: {cur_fps}', aa, (0, 255, 255) if cur_fps > clock.fps - 10 else (255, 0, 0)
            ), (0, 0))
        pygame.display.flip()
