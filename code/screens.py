import pygame

from support import *

pygame.mixer.pre_init(channels=5)
pygame.init()
pygame.display.set_caption('Tank Battles')
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# def mega_blit():
#     screen_true.blit(pygame.transform.scale(screen, (WIDTH * SCALE, HEIGHT * SCALE)), (0, 0))
#
#
# mega_blit()

clock = pygame.time.Clock()

from functions import *
from level import Level, LevelPreview
from mixer import *
from button import Button

from json import load, dump


def start_screen():
    background = pygame.transform.scale(pygame.image.load(r'../data/images/background1.png'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))

    __btns = [("ИГРАТЬ", level_select_screen), ("КАМПАНИЯ", start_campaign), ("МАГАЗИН", open_shop_screen),
              ("Создать уровень", create_level),
              ("ПАРАМЕТРЫ", open_settings)]

    buttons = [
        Button(screen, WIDTH / 3, 480, __btns[0][0], 40, __btns[0][1], bgcolor=pygame.color.Color(12, 102, 68),
               textcolor="white", point_bg_color="#023822", point_text_color="#AAAAAA", group=True),
        Button(screen, WIDTH / 3 * 2, 480, __btns[1][0], 40, __btns[1][1], bgcolor=pygame.color.Color(12, 102, 68),
               textcolor="white", point_bg_color="#023822", point_text_color="#AAAAAA", group=True),

    ]

    for i in range(1, 4):
        buttons.append(
            Button(screen, WIDTH / 6 * 2 * i - WIDTH // 5 + WIDTH // 39, 650, __btns[i + 1][0], 40, __btns[i + 1][1],
                   bgcolor=pygame.color.Color(12, 102, 68),
                   textcolor="white", point_bg_color="#023822", point_text_color="#AAAAAA", group=True))
    pygame.display.flip()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.rect.collidepoint(ev.pos):
                        btn.pressed()
            elif ev.type == pygame.MOUSEMOTION:
                for btn in buttons:
                    if btn.rect.collidepoint(ev.pos):
                        btn.pointed()
                    else:
                        btn.set_default()

        clock.tick(FPS)

        pygame.display.flip()


def open_settings():
    pass


def open_help_window():
    # помощь в управлении, справка по игре
    print(2)


def none():
    pass


def open_shop_screen():
    with open('../data/config.json') as cnf:
        cnfg = load(cnf)
        pl_tank = cnfg['player_vehicle']

    with open('../data/tanks/1.json', encoding="utf-8") as dt:
        data = load(dt)

    def save():
        cnfg['player_vehicle'] = pl_tank

        with open('../data/config.json', 'w') as cfg2:
            dump(cnfg, cfg2)

    buttons = []
    offset = 30
    shop_screen = pygame.Surface((WIDTH - offset, HEIGHT - 2 * offset - 70))

    def draw_shop_screen():
        screen.fill(BG_COLOR)
        shop_screen.fill(BG_COLOR)
        __width3 = shop_screen.get_width() // 3

        write_text(screen, 0, 20, ["ВЫБОБ ТАНКА"], 0, 60, TITLE_COLOR, x_centered=True)

        for i in range(3):
            pygame.draw.rect(shop_screen, GREEN_COLOR if i != pl_tank else GRAY_COLOR,
                             (__width3 * i, 0, __width3 - offset, shop_screen.get_height()), 3, 3)
            pygame.draw.rect(shop_screen, "#191518",
                             (__width3 * i + 3, 3, __width3 - offset - 6, shop_screen.get_height() - 6))
            write_text(shop_screen, __width3 * i + 30, 20, [data[i]["name"]], 0, 70, "#B7B7B5")
            shop_screen.blit(pygame.transform.scale(load_image(data[i]["image"]["green"], color_key=-1), (170, 170)),
                             (__width3 * i + (__width3 - offset) // 2 - 85, 80))
            write_text(shop_screen, __width3 * i + 18, 280, data[i]["description"], 37, 28, "#B7B7B5")
            write_text(shop_screen, __width3 * i + 18, 370, [f"Перезарядка: {data[i]['reload'] / 1000}"], 0, 28,
                       "#B7B7B5")
            write_text(shop_screen, __width3 * i + 18, 430, data[i]["minuses"], 27, 25, GREEN_COLOR)

            buttons.append(
                Button(shop_screen, __width3 * i + __width3 // 2 - offset // 2, shop_screen.get_height() - 150,
                       "ВЫБРАН" if pl_tank == i else "ВЫБРАТЬ",
                       35, link=none, bgcolor=GREEN_COLOR if pl_tank != i else DARK_GRAY_COLOR,
                       textcolor=GRAY_COLOR if pl_tank != i else GRAY_COLOR, group=True,
                       point_text_color=GRAY_COLOR if pl_tank != i else None,
                       point_bg_color="#0B8E2E" if pl_tank != i else None))

        screen.blit(shop_screen, (offset, HEIGHT - shop_screen.get_height() - offset))

    draw_shop_screen()

    exit_btn = Button(screen, offset, 20, "ВЫХОД", 20 * SCALE, start_screen, bgcolor="#100F0F",
                      textcolor="#F0F0F0", point_bg_color="#000000", point_text_color="#CCCCCC")
    pygame.display.flip()

    pos_offs = (HEIGHT - shop_screen.get_height() - offset)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.MOUSEMOTION:
                for btn in buttons:
                    if btn.rect.collidepoint([ev.pos[0],
                                              ev.pos[1] - pos_offs]):
                        btn.pointed()
                    else:
                        btn.set_default()
                if exit_btn.rect.collidepoint(ev.pos):
                    exit_btn.pointed()
                else:
                    exit_btn.set_default()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.rect.collidepoint([ev.pos[0],
                                              ev.pos[1] - pos_offs]):
                        play_button_sound()
                        pl_tank = buttons.index(btn)
                        save()
                        open_shop_screen()
                if exit_btn.rect.collidepoint(ev.pos):
                    exit_btn.pressed()
        clock.tick(15)

        screen.blit(shop_screen, (offset, HEIGHT - shop_screen.get_height() - offset))
        pygame.display.flip()


def start_campaign():
    def begin_level(level_name):
        screen.fill('black')
        write_text(screen, 0, 400 * SCALE, [level_name.replace(".txt", '')], 0, 50, 'white', x_centered=True)

        pygame.display.flip()
        sleep(2)

    levels = os.listdir(r'../data/levels/')
    for level in levels:
        begin_level(level)
        game(level, mode='campaign')

    begin_level('123')


def level_select_screen():
    screen.fill(pygame.Color(35, 30, 33))
    offset = 0

    levels = os.listdir(r'../data/levels/')
    level_list = {}

    def show_levels(offset=0):
        for i in range(2):
            for j in range(3):
                try:
                    font = pygame.font.Font("../data/fonts/ft40.ttf", 30)

                    lvlname = levels[i * 3 + j + offset]
                    st_rendered = font.render(levels[i * 3 + j + offset][:-4], 1, pygame.Color("white"))
                    st_rect = st_rendered.get_rect()
                    st_rect.x = WIDTH // 4 + WIDTH // 4 * j - st_rect.width // 2
                    st_rect.y = HEIGHT // 3 + HEIGHT // 3 * i - st_rect.height // 2 + 120

                    screen.blit(st_rendered, st_rect)
                    screen.blit(pygame.transform.scale(load_image(
                        f"../data/images/preview_images/{lvlname.replace('.txt', '.png')}"),
                        (180, 180)), (
                        WIDTH // 4 + WIDTH // 4 * j - 90, HEIGHT // 3 + HEIGHT // 3 * i - st_rect.height // 2 - 80))

                    level_list[lvlname] = pygame.Rect(WIDTH // 4 + WIDTH // 4 * j - 90,
                                                      HEIGHT // 3 + HEIGHT // 3 * i - st_rect.height // 2 - 80, 180,
                                                      180 + st_rect.h + 15)

                except IndexError:
                    break

    pointed = False

    while True:
        screen.fill(pygame.Color(35, 30, 33))

        write_text(screen, 0, 70, ['ВЫБЕРИТЕ УРОВЕНЬ'], 10, 45 * SCALE, TITLE_COLOR, x_centered=True)
        if not pointed:
            exit_btn = Button(screen, 100 * SCALE, HEIGHT - 90 * SCALE, "ВЫХОД", 28 * SCALE, start_screen,
                              bgcolor="#100F0F",
                              textcolor="#F0F0F0", point_bg_color="#000000", point_text_color="#CCCCCC")
        else:
            exit_btn = Button(screen, 100 * SCALE, HEIGHT - 90 * SCALE, "ВЫХОД", 28 * SCALE, start_screen,
                              bgcolor="#000000",
                              textcolor="#CCCCCC")
        left_btn = write_text(screen, 25, HEIGHT // 2 - 50, ['<'], 1, 35 * SCALE, TITLE_COLOR)
        right_btn = write_text(screen, WIDTH - 70, HEIGHT // 2 - 50, ['>'], 1, 35 * SCALE, TITLE_COLOR)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                for lvl, cords in level_list.items():
                    if cords.collidepoint(ev.pos):
                        play_button_sound()
                        game(lvl)
                        return
                if exit_btn.rect.collidepoint(ev.pos):
                    exit_btn.pressed()
                if to_rect(left_btn).collidepoint(ev.pos):
                    level_list = {}

                    offset -= 6
                    if offset <= 0:
                        offset = 0
                if to_rect(right_btn).collidepoint(ev.pos):
                    level_list = {}

                    offset += 6
                    if offset > len(levels):
                        offset -= 6
            elif ev.type == pygame.MOUSEMOTION:
                if exit_btn.rect.collidepoint(ev.pos):
                    pointed = True
                    exit_btn.pointed()
                else:
                    exit_btn.set_default()
                    pointed = False
        show_levels(offset)

        pygame.display.flip()
        clock.tick(FPS)


def create_level():
    screen.fill(BG_COLOR)
    x = 30
    y = 100
    w = h = (HEIGHT - y - y // 4) // 16 * 16
    step = h // 16

    write_text(screen, 0, 20, ['СОЗДАТЬ УРОВЕНЬ'], 10, 50, TITLE_COLOR, x_centered=True)
    write_text(screen, (WIDTH - x - w) * 3.3 // 2, y, ['ОБЪЕКТЫ:'], 10, 40, TITLE_COLOR)

    table = [["." for _ in range(16)] for _ in range(16)]
    pos_and_var = {}

    ####################################################################
    # Functions

    def detect_position(pos_x, pos_y):
        position_x = (pos_x - x) // step
        position_y = (pos_y - y) // step
        if (w // step) > position_x >= 0 and (w // step) > position_y >= 0:
            return int(position_x), int(position_y)
        else:
            return None

    def from_tCords_to_aCords(cords: tuple):
        return cords[0] * step + x, cords[1] * step + y

    def draw_table():
        pygame.draw.rect(screen, "white", (x, y, w, h), 1, 1)
        for i in range(1, 16):
            pygame.draw.line(screen, "white", (x, y + step * i), (x + w, y + step * i))
            pygame.draw.line(screen, "white", (x + step * i, y), (x + step * i, y + h))

    def check_player():
        for i in table:
            for j in i:
                if j == "@":
                    return True
        return False

    def save():
        if check_player():
            levels = os.listdir('../data/levels')
            counter = 1
            for lvl in levels:
                if "Мой уровень" in lvl:
                    counter += 1
            filename = f"Мой уровень {counter}.txt"

            with open(f"../data/levels/{filename}", mode="w", encoding="utf-8") as file:
                for i in table:
                    for j in i:
                        file.write(j)
                    file.write("\n")
            onCreate()
            print("Success")

    def apply_chosen():
        if to_rect_from_cords(x, y, w, h).collidepoint([ev.pos[0], ev.pos[1]]):
            pos = detect_position(ev.pos[0] - offset[0] + step // 2, ev.pos[1] - offset[1] + step // 2)
            if pos:
                if table[pos[1]][pos[0]] != ".":
                    objects_set.remove(pos_and_var[pos])
                if choosen and choosen[2] == "0":
                    table[pos[1]][pos[0]] = "."
                    return
                it = choosen if choosen else leading
                objects_set.append((it, pos))
                table[pos[1]][pos[0]] = it[2]
                pos_and_var[pos] = (it, pos)

    ######################################################
    # Variables

    blue_tank = pygame.transform.scale(load_image(fr'../data/images/vehicle_images/1/blue_tank.png', color_key=-1),
                                       (step, step))
    green_tank = pygame.transform.scale(load_image(fr'../data/images/vehicle_images/1/green_tank.png', color_key=-1),
                                        (step, step))
    block = pygame.transform.scale(load_image(fr'../data/images/object_images/metal_box/metal_box.png', color_key=-1),
                                   (step, step))
    trash = pygame.transform.scale(load_image(fr"../data/images/trash_image.png", color_key=-1), (step, step))

    blue_tank_cords = to_rect_from_cords(3 * x + w, y + y + 80, step, step)
    green_tank_cords = to_rect_from_cords(3 * x + w, y + y, step, step)
    block_cords = to_rect_from_cords(3 * x + w, y + y + 160, step, step)
    trash_cords = to_rect_from_cords(3 * x + w, y + y + 240, step, step)

    objects = [
        (green_tank_cords, green_tank, "@"),
        (blue_tank_cords, blue_tank, "$"),
        (block_cords, block, "#"),
        (trash_cords, trash, "0")
    ]
    objects_set = []

    for cords, image, sym in objects:
        screen.blit(image, cords)

    selected_background = pygame.Surface((66, 66))
    selected_background.fill(BG_COLOR)
    pygame.draw.rect(selected_background, pygame.Color(255, 255, 255),
                     (0, 0, selected_background.get_width(), selected_background.get_height()), 3)

    ##################################################
    # Main loop

    pointedExitBtn = False
    leading = None
    try_to_choose = None
    choosen = None
    left_button_down = False
    cords = [0, 0]
    offset = [0, 0]
    while True:
        screen.fill('#231E21')
        draw_table()

        write_text(screen, 0, 20, ['СОЗДАТЬ УРОВЕНЬ'], 10, 50, TITLE_COLOR, x_centered=True)
        write_text(screen, (WIDTH - x - w) * 3.3 // 2, y, ['ОБЪЕКТЫ:'], 10, 40, TITLE_COLOR)

        if not pointedExitBtn:
            exit_btn = Button(screen, 30, 20, "ВЫХОД", 20 * SCALE, start_screen,
                              bgcolor="#100F0F",
                              textcolor="#F0F0F0", point_bg_color="#000000", point_text_color="#CCCCCC")
        else:
            exit_btn = Button(screen, 30, 20, "ВЫХОД", 20 * SCALE, start_screen,
                              bgcolor="#000000",
                              textcolor="#CCCCCC")
        save_btn = Button(screen, (WIDTH - x - w) * 3.3 // 2, HEIGHT - y // 4 - 60, "СОХРАНИТЬ", 20 * SCALE, save,
                          bgcolor=GREEN_COLOR, textcolor="#B7B7B5")

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                left_button_down = True
                if exit_btn.rect.collidepoint(ev.pos):
                    exit_btn.pressed()
                if save_btn.rect.collidepoint(ev.pos):
                    save_btn.pressed()

                for item in objects:
                    if item[0].collidepoint(ev.pos):
                        if not (item[2] == "@" and check_player()):
                            leading = item if item[2] != "0" else None
                            try_to_choose = item
                            offset = [ev.pos[0] - item[0].x, ev.pos[1] - item[0].y]
                            cords = [item[0].x, item[0].y]
                if not leading and not choosen:
                    for i in range(len(objects_set)):
                        aCords = from_tCords_to_aCords(objects_set[i][1])
                        if to_rect_from_cords(*aCords, step, step).collidepoint(ev.pos):
                            leading = objects_set[i][0]
                            cord = objects_set[i][1]
                            offset = [ev.pos[0] - cord[0] * step - x, ev.pos[1] - cord[1] * step - y]
                            cords = aCords
                            objects_set.pop(i)
                            table[cord[1]][cord[0]] = "."
                            break
                if not leading and choosen and not check_player():
                    apply_chosen()

            if ev.type == pygame.MOUSEBUTTONUP:
                left_button_down = False
                for item in objects:
                    if item[0].collidepoint(ev.pos) and try_to_choose:
                        leading = None
                        choosen = item if (not choosen or choosen != item) else None

                if not leading:
                    try_to_choose = None
                    continue
                apply_chosen()

                leading = None
                cords = []
                if not choosen:
                    offset = []

            elif ev.type == pygame.MOUSEMOTION:
                if choosen and left_button_down:
                    if choosen == objects[0]:
                        if check_player():
                            continue
                    apply_chosen()

                if exit_btn.rect.collidepoint(ev.pos):
                    pointedExitBtn = True
                    exit_btn.pointed()
                else:
                    exit_btn.set_default()
                    pointedExitBtn = False

                if leading:
                    cords = [ev.pos[0] - offset[0], ev.pos[1] - offset[1]]

        ################################################
        # Blit

        for obj in objects_set:
            screen.blit(obj[0][1], (obj[1][0] * step + x, y + obj[1][1] * step))

        if choosen:
            screen.blit(selected_background, (choosen[0].x - (selected_background.get_width() - step) // 2,
                                              choosen[0].y - (selected_background.get_height() - step) // 2))

        for coords, image, sym in objects:
            screen.blit(image, coords)

        if leading:
            screen.blit(leading[1], cords)

        pygame.display.flip()
        clock.tick(FPS)


def end_game(result, level, mode='training'):
    con = sqlite3.connect(r'../data/database/db.db')
    cur = con.cursor()

    screen.fill('black')
    write_text(screen, 0, 90 * SCALE, ['Победа!' if result[0] == 'win' else 'Поражение'], 1, 65 * SCALE,
               GREEN_COLOR if result[0] == 'win'
               else 'red', x_centered=True)
    write_text(screen, 0, 180 * SCALE, [f'Уровень: {result[1][3]}'], 1, 40 * SCALE, 'white', x_centered=True)
    write_text(screen, 0, 240 * SCALE, [f'Противников уничтожено: {result[1][1]}'], 1, 40 * SCALE, 'white',
               x_centered=True)
    write_text(screen, 0, 300 * SCALE, [f'Время: {result[1][0]} секунд'], 1, 40 * SCALE, 'white', x_centered=True)

    games = cur.execute(f"""SELECT * FROM battles WHERE level = '{level}' and result = 'win'""").fetchall()

    if result[0] == 'win':
        if games:
            best_time = sorted(games, key=lambda x: x[3])[0][3]

            if float(result[1][0]) < best_time:
                write_text(screen, 0, 360 * SCALE, [f'Новый рекорд!'], 1, 40 * SCALE, 'white', x_centered=True)
            else:
                write_text(screen, 0, 360 * SCALE, [f'Рекордное время: {best_time} секунд'], 1, 40, 'white',
                           x_centered=True)
        else:
            write_text(screen, 0, 360 * SCALE, [f'Новый рекорд!'], 1, 40 * SCALE, 'white', x_centered=True)

    else:
        if games:
            best_time = sorted(games, key=lambda x: x[3])[0][3]
            write_text(screen, 0, 360 * SCALE, [f'Рекордное время: {best_time} секунд'], 1, 40 * SCALE, 'white',
                       x_centered=True)

    con.execute(f"""INSERT into battles (result, killed, time, level) values ('{result[0]}', {result[1][1]}, 
{result[1][0]}, '{result[1][3]}')""")
    con.commit()

    if mode == 'training' or result[0] == 'loose':
        exit_btn = Button(screen, 100 * SCALE, HEIGHT - 90 * SCALE, "ВЫХОД", 28 * SCALE, level_select_screen,
                          bgcolor="#111111",
                          textcolor="#B7B7B7", point_text_color="#AAAAAA", point_bg_color="#070707")
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    terminate()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if exit_btn.rect.collidepoint(ev.pos):
                        set_main_music()
                        set_volume(0.7)
                        exit_btn.pressed()
                        return
                if ev.type == pygame.MOUSEMOTION:
                    if exit_btn.rect.collidepoint(ev.pos):
                        exit_btn.pointed()
                    else:
                        exit_btn.set_default()
            pygame.display.flip()
    else:
        pygame.display.flip()
        return


def game(level, mode='training'):
    pygame.mixer.music.stop()

    level1 = Level(level)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                level1.clicked(ev.pos)
            if ev.type == pygame.MOUSEMOTION:
                level1.motion(ev.pos)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_v:
                    level1.set_pause()
                elif ev.key == pygame.K_ESCAPE:
                    level1.exit = True

        move = level1.run(screen, clock)

        if move:

            if move[0] in ('loose', 'win'):
                if mode == 'training':
                    end_game(move, level)
                else:
                    end_game(move, level, mode='campaign')
                    return
            elif move == 'exit':
                set_main_music()
                set_volume(0.7)
                level_select_screen()


# def congratulation_screen(text):
#     clicks = 0
#
#     prev = 0
#
#     while True:
#         screen.fill('black')
#
#         for ev in pygame.event.get():
#             if ev.type == pygame.QUIT:
#                 terminate()
#             if ev.type == pygame.MOUSEBUTTONDOWN:
#                 clicks += 1
#             if ev.type == pygame.KEYDOWN:
#                 if ev.key == pygame.K_4:
#                     prev = 4
#                 elif ev.key == pygame.K_7:
#                     if prev == 4:
#                         return
#                 else:
#                     prev = 0
#
#         if clicks >= 10:
#             write_text(screen, 0, HEIGHT // 2 + 50,
#                        ['Чтобы пройти дальше, тебе нужно ввести определенную последовательность символов'], 20, 50,
#                        'white', x_centered=True)
#
#         write_text(screen, 0, HEIGHT // 2, text, 20, 50, 'white', x_centered=True)
#         pygame.display.flip()
#         clock.tick(10)

def onCreate():
    levels = os.listdir('../data/levels')

    for level in levels:
        if os.path.isfile(f'../data/images/preview_images/{level.replace(".txt", ".png")}'):
            pass
        else:
            preview = LevelPreview(level).battlefield
            pygame.image.save(preview, f'../data/images/preview_images/{level.replace(".txt", ".png")}')


def main():
    # set_misic(r'../data/sounds/music/main_theme.mp3')
    # congratulation_screen(['Папа, поздравляю тебя с днём рождения!'])
    onCreate()
    set_main_music()
    start_screen()
