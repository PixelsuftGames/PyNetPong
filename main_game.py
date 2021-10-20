import time
import pygame
from fps_clock import FPS
from socket_tools import *
from utils import *


def main(is_server: bool, host: str = None, port: int = None) -> None:
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
    bg_music: pygame.mixer.Sound = get_var('bg_music')
    res_nod = find_nod(w, h)
    res_division = (round(w / res_nod), round(h / res_nod))
    use_16_9_bg = res_division[0] / res_division[1] >= 10 / 7
    bg_img = Image.open(p('images', 'bg_16_9.png' if use_16_9_bg else 'bg_4_3.png')).resize((w, h))
    pg_bg_img = to_image(bg_img, False)
    fps_font = pygame.font.Font(p('fonts', 'segoescb.ttf'), 25)
    label_font = pygame.font.Font(p('fonts', 'segoescb.ttf'), 25)
    player_size = [20, 50]
    ball_radius = 20
    ball_d = ball_radius * 2
    player_pos = [5, 0]
    player2_pos = [w - 5 - player_size[0], 0]
    num = int(not is_server)
    ball_pos = [half_w_, half_h_]
    s1, s2 = 0, 0
    ball_speed = [random.choice((1, -1)), random.choice((1, -1))]

    def to_w(size: any) -> int:
        return round(size / w * info[0]['w'])

    def to_h(size: any) -> int:
        return round(size / h * info[0]['h'])

    def from_w(size: any) -> int:
        return round(size * w / info[0]['w'])

    def from_h(size: any) -> int:
        return round(size * h / info[0]['h'])

    def round_tuple(not_rounded: any) -> tuple:
        return tuple(round(i) for i in not_rounded)

    def respawn_ball_thread() -> None:
        time.sleep(1)
        ball_speed[0] = random.choice((1, -1))
        ball_speed[1] = random.choice((1, -1))
        ball_pos[0] = half_w_
        ball_pos[1] = half_h_

    def respawn_ball() -> None:
        ball_speed[0] = 0
        ball_speed[1] = 0
        ball_pos[0] = half_w_
        ball_pos[1] = half_h_
        Thread(target=respawn_ball_thread).start()

    if is_server:
        info[1]['l_'] = True
    else:
        while not info[0]['l_']:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    kill_all()
                    sys.exit(0)
        pre_ball = (from_w(ball_radius), from_h(ball_radius), from_w(ball_d), from_h(ball_d))

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
            elif event.type == pygame.MOUSEMOTION:
                x, y = last_x, last_y = pygame.mouse.get_pos()
                if is_server:
                    info[1]['y'] = y
                else:
                    info[1]['y'] = to_h(y)
                player_pos[1] = y
        if not clock.try_tick():
            continue
        screen.blit(pg_bg_img, (0, 0))

        if is_server:
            pygame.draw.rect(
                screen, (255, 255, 255), (player2_pos[0], info[0]['y'], 20, player_size[1]), border_radius=5
            )
            pygame.draw.rect(
                screen, (255, 255, 255), (player_pos[0], player_pos[1], player_size[0], player_size[1]), border_radius=5
            )
            ball_pos[0] += ball_speed[0] * clock.delta / 5
            ball_pos[1] += ball_speed[1] * clock.delta / 5
            info[1]['bx'], info[1]['by'] = round_tuple(ball_pos)
            if ball_pos[1] <= ball_radius:
                ball_speed[1] = -ball_speed[1]
            if ball_pos[1] >= h - ball_radius:
                ball_speed[1] = -ball_speed[1]
            if ball_pos[1] + ball_radius > player_pos[1] and ball_pos[1] - ball_radius < player_pos[1] + player_size[1]:
                if ball_pos[0] + ball_radius > player_pos[0] and\
                        ball_pos[0] - ball_radius < player_pos[0] + player_size[0]:
                    ball_speed[0] = -ball_speed[0] * random_float(0.9, 1.15)
                    ball_speed[1] *= random_float(0.9, 1.15)
            if ball_pos[1] + ball_radius > info[0]['y'] and ball_pos[1] - ball_radius < info[0]['y'] + player_size[1]:
                if ball_pos[0] + ball_radius > player2_pos[0] and\
                        ball_pos[0] - ball_radius < player2_pos[0] + player_size[0]:
                    ball_speed[0] = -ball_speed[0] * random_float(0.9, 1.15)
                    ball_speed[1] *= random_float(0.9, 1.15)
            if ball_pos[0] <= -ball_radius:
                s1 += 1
                info[1]['s1'] = s1
                respawn_ball()
            if ball_pos[0] >= w + ball_radius:
                s2 += 1
                info[1]['s2'] = s2
                respawn_ball()
            pygame.draw.circle(screen, (255, 255, 255), ball_pos, ball_radius)
            score_surf = label_font.render(f'{s1}:{s2}', aa, (0, 0, 0))
        else:
            pygame.draw.rect(
                screen, (255, 255, 255), (from_w(5), from_h(info[0]['y']),
                                          from_w(player_size[0]), from_h(player_size[1])), border_radius=5
            )
            pygame.draw.rect(
                screen, (255, 255, 255), (w - 5 - from_w(player_size[0]),
                                          from_h(player_pos[1]), from_w(player_size[0]),
                                          from_h(player_size[1])), border_radius=5
            )
            pygame.draw.ellipse(
                screen, (255, 255, 255),
                (from_w(info[0]['bx']) - pre_ball[0], from_h(info[0]['by']) - from_h(ball_radius) - pre_ball[1],
                 pre_ball[2], pre_ball[3]),
                width=0
            )
            score_surf = label_font.render(f'{info[0]["s1"]}:{info[0]["s2"]}', aa, (0, 0, 0))
        screen.blit(score_surf, (w - score_surf.get_size()[0], 0))

        if show_fps:
            cur_fps = clock.get_int_fps()
            screen.blit(fps_font.render(
                f'FPS: {cur_fps}', aa, (0, 255, 255) if cur_fps > clock.fps - 10 else (255, 0, 0)
            ), (0, 0))
        pygame.display.flip()
