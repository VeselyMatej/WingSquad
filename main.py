from tkinter import Button

import pygame
import random
import os
import sys

# spusteni pygame
pygame.init()

# obrazovka
width = 700
height = 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("WingSquad")

# definovani barev
blue = (50, 50, 255)
white = (255, 255, 255)
purple = (255, 0, 245)
black = (0, 0, 0)
grey = (105, 105, 105)
slate = (119, 136, 153)
yellow = (204, 204, 0)
red = (255, 0, 0)
darkred = (139, 0, 0)

# FPS
fps = 60
clock = pygame.time.Clock()

# získání cesty k souborům
def resource_path(relative_path):
    try:
        # PyInstaller - docasna slozka
        base_path = sys._MEIPASS
    except Exception:
        # Pokud nefunguje
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)


# Cesty k souborum
bg_music_path = resource_path('media/bg_music.wav')
hit_sound_path = resource_path('media/hit.mp3')
font_path = resource_path('fonts/ww2_font.otf')

# Inicializace Pygame
pygame.init()

# Nacteni hudby a zvuku
pygame.mixer.music.load(bg_music_path)
pygame.mixer.music.play(-1, 0.0)

hit_sound = pygame.mixer.Sound(hit_sound_path)


# čara
pygame.draw.line(screen, slate, (0, 80), (width, 80), 20)

# nastaveni fontu
custom_font = pygame.font.Font(font_path, 105)
custom_font2 = pygame.font.Font(font_path, 110)
custom_font3 = pygame.font.Font(font_path, 30)
custom_font4 = pygame.font.Font(font_path, 20)
custom_font_pause = pygame.font.Font(font_path, 120)

# font, barva, a umisteni textu
custom_text = custom_font.render("WingSquad", True, grey)
custom_text_rect = custom_text.get_rect()
custom_text_rect.center = (width // 2, 65)
# 2.
custom_text2 = custom_font2.render("WingSquad", True, slate)
custom_text2_rect = custom_text2.get_rect()
custom_text2_rect.center = (width // 2, 62)
# 3. - score
custom_text3 = custom_font3.render("SCORE; ", True, yellow)
custom_text3_rect = custom_text3.get_rect()
custom_text3_rect.center = (60, 155)
# 4. - pause
pause_text = custom_font_pause.render("PAUSED", True, black)
pause_text_rect = pause_text.get_rect()
pause_text_rect.center = (width // 2, height // 2)
# 5. - GAME OVER
gameover_text = custom_font_pause.render("GAME OVER", True, darkred)
gameover_text_rect = gameover_text.get_rect()
gameover_text_rect.center = (width // 2, height // 2)
# 6. - BULLETS
custom_text4 = custom_font4.render("AMMO; ", True, yellow)
custom_text4_rect = custom_text4.get_rect()
custom_text4_rect.center = (38, 183)

# barva screenu
screen.fill(blue)

# importovani obrazku
spitfire_image = pygame.image.load(resource_path("img/spitfire_mini.png"))
spitfire_rect = spitfire_image.get_rect()
spitfire_rect.center = (width // 2, 810)
# BUTTONS
start_button = pygame.image.load(resource_path("img/start_button.png"))
start_button_rect = start_button.get_rect()
start_button_rect.center = (160, 650)
# 2
quit_button = pygame.image.load(resource_path("img/quit_button.png"))
quit_button_rect = quit_button.get_rect()
quit_button_rect.center = (520, 650)
# 5
restart_button = pygame.image.load(resource_path("img/restart_button.png"))
restart_button_rect = restart_button.get_rect()
restart_button_rect.center = (160, 650)
# 4
pause_button = pygame.image.load(resource_path("img/pause_button.png"))
pause_button_rect = pause_button.get_rect()
pause_button_rect.center = (675, 160)
# 5
music_button = pygame.image.load(resource_path("img/music_button.png"))
music_button_rect = music_button.get_rect()
music_button_rect.center = (625, 160)
# 6 NEPRATELSKA LETADLA
mess_image = pygame.image.load(resource_path("img/messerschmit_mini.png"))
enemies = []
# 7 refill bullets
refill_ammo = pygame.image.load(resource_path("img/ammo_refill.png"))
ammo = []
# 8
htp_button = pygame.image.load(resource_path("img/htp_button.png"))
htp_button_rect = htp_button.get_rect()
htp_button_rect.center = (650, 201)
# 9
htp_screen = pygame.image.load(resource_path("img/htp_screen.png"))
htp_screen_rect = htp_screen.get_rect()
htp_screen_rect.center = (width // 2, height // 2)
# 10
x_button = pygame.image.load(resource_path("img/x_button.png"))
x_button_rect = x_button.get_rect()
x_button_rect.center = (560, 290)
# 11
continue_button = pygame.image.load(resource_path("img/continue_button.png"))
continue_button_rect = continue_button.get_rect()
continue_button_rect.center = (340, 665)


# bullets
bullet_image = pygame.image.load(resource_path("img/bullet.png"))
bullet_image_rect = bullet_image.get_rect()
bullets = []
bullet_speed = 13
bullet_width = bullet_image.get_width()
bullet_height = bullet_image.get_height()
bullet_spawn_delay = fps // 3
bullet_counter = 0

# herni stav
game_started = False
paused = False
game_over = False
music_paus = False
can_shoot = False
htp_screen_show = False
score = 0
enemy_spawn_delay = 100
enemy_counter = 0
ammo_spawn_delay = 100
ammo_counter = 0
ammo_amount = 40

# aktualizace score
def update_score():
    return custom_font3.render(f"SCORE; {score}", True, yellow)
# aktualizace ammo
def update_ammo():
    return custom_font4.render(f"AMMO; {ammo_amount}", True, yellow)


custom_text3 = update_score()  # Score
custom_text4 = update_ammo()   # ammo



# hlavni herni cyklus
lets_continue = True

while lets_continue:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos) and not game_started:
                game_started = True
            if quit_button_rect.collidepoint(event.pos):
                lets_continue = False
                pygame.quit()
                sys.exit()
            if restart_button_rect.collidepoint(event.pos):
                game_started = True
                game_over = False
                paused = False
                score = 0
                ammo_amount = 40
                spitfire_rect.center = (width // 2, 810)
                enemies.clear()
                bullets.clear()
                custom_text3 = update_score()  # Score
                custom_text4 = update_ammo()  # ammo
            if pause_button_rect.collidepoint(event.pos):
                 if game_started and not game_over:
                    paused = not paused
            if music_button_rect.collidepoint(event.pos):
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                    music_paus = True
                else:
                    pygame.mixer.music.unpause()
                    music_paus = False
            if continue_button_rect.collidepoint(event.pos):
                paused = not paused
            if htp_button_rect.collidepoint(event.pos):
                htp_screen_show = not htp_screen_show
            if x_button_rect.collidepoint(event.pos):
                htp_screen_show = not htp_screen_show

    keys = pygame.key.get_pressed()
    if game_started and not paused and not game_over:
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and spitfire_rect.left > 0:
            spitfire_rect.x -= 4
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and spitfire_rect.right < width:
            spitfire_rect.x += 4
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and spitfire_rect.top > 200:
            spitfire_rect.y -= 1.5
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and spitfire_rect.bottom < height:
            spitfire_rect.y += 1.5


    # bullets  - strelba
    if (keys[pygame.K_SPACE]) and not game_over:
        if ammo_amount >= 2:
            bullet_counter += 1.5
            if bullet_counter >= bullet_spawn_delay:
                left_bullet = pygame.Rect(spitfire_rect.x + 10, spitfire_rect.y, bullet_width, bullet_height)
                right_bullet = pygame.Rect(spitfire_rect.x + spitfire_rect.width - 20, spitfire_rect.y, bullet_width, bullet_height)
                bullets.append(left_bullet)
                bullets.append(right_bullet)
                bullet_counter = 0
                ammo_amount -= 2
                custom_text3 = update_score()  # Score
                custom_text4 = update_ammo()  # ammo

    # pohyb bullets
    if not paused and game_started and not game_over:
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.bottom < 200:
                bullets.remove(bullet)

    # spawnovani nepratel
    if game_started and not paused and not game_over:
        enemy_counter += 2.5
        if enemy_counter >= enemy_spawn_delay and not paused:
            enemy_x = random.randint(0, width - mess_image.get_width())
            enemy_y = random.randint(70, 140)
            enemies.append(pygame.Rect(enemy_x, enemy_y, mess_image.get_width(), mess_image.get_height()))
            enemy_counter = 0

    #spawnovani ammo
    if game_started and not paused and not game_over:
        ammo_counter += 0.5
        if ammo_counter >= ammo_spawn_delay and not paused:
            ammo_x = random.randint(0, width - refill_ammo.get_width())
            ammo_y = random.randint(70, 140)
            ammo.append(pygame.Rect(ammo_x, ammo_y, refill_ammo.get_width(), refill_ammo.get_height()))
            ammo_counter = 0

    # pohyb nepřátelských letadel
    if game_started and not paused and not game_over:
        for enemy in enemies[:]:
            enemy.y += 3

            if enemy.top > height:
                enemies.remove(enemy)
                score = score -1
                custom_text3 = update_score()
    #pohyb ammo
    if game_started and not paused and not game_over:
        for ammo_rect in ammo[:]:
            ammo_rect.y += 3

            if ammo_rect.top > height:
                ammo.remove(ammo_rect)

            #KOLIZE letadel
            spitfire_mask = pygame.mask.from_surface(spitfire_image)

            for enemy in enemies[:]:
                enemy_mask = pygame.mask.from_surface(mess_image)

                offset_x = enemy.x - spitfire_rect.x
                offset_y = enemy.y - spitfire_rect.y

                if spitfire_mask.overlap(enemy_mask, (offset_x, offset_y)):
                    game_over = not game_over



    # kolize
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                custom_text3 = update_score()
                if not music_paus:
                    hit_sound.set_volume(0.05)
                    hit_sound.play()


    for ammo_rect in ammo[:]:
        if spitfire_rect.colliderect(ammo_rect):
            ammo.remove(ammo_rect)
            ammo_amount += 20
            custom_text4 = update_ammo()

    # vyplneni obrazovky
    screen.fill(blue)

    # blitting textu
    screen.blit(custom_text, custom_text_rect)
    screen.blit(custom_text2, custom_text2_rect)
    screen.blit(custom_text3, custom_text3_rect)
    screen.blit(custom_text4, custom_text4_rect)

    # blitting bullets
    for bullet in bullets:
        screen.blit(bullet_image, bullet)

    # blitting obrazku
    screen.blit(spitfire_image, spitfire_rect)
    for enemy in enemies:
        screen.blit(mess_image, enemy)
    for ammo_rect in ammo:
        screen.blit(refill_ammo, ammo_rect)

    # hudba
    if game_started:
        pygame.mixer.music.set_volume(0.2)

    # blitting buttonu
    if not game_started:
        screen.blit(start_button, start_button_rect)
    if not game_started:
        screen.blit(quit_button, quit_button_rect)
    if paused or game_over:
        screen.blit(restart_button, restart_button_rect)
        screen.blit(quit_button, quit_button_rect)
    if paused:
        screen.blit(pause_text, pause_text_rect)
        screen.blit(continue_button, continue_button_rect)
    screen.blit(pause_button, pause_button_rect)
    screen.blit(music_button, music_button_rect)
    screen.blit(htp_button, htp_button_rect)


    if game_over:
        screen.blit(gameover_text, gameover_text_rect)
        # pygame.draw.line(screen, darkred, (0, 430), (width, 430), 20)
        # pygame.draw.line(screen, darkred, (0, 548), (width, 548), 20)

    if htp_screen_show:
        screen.blit(htp_screen, htp_screen_rect)
        screen.blit(x_button, x_button_rect)

    # čary
    pygame.draw.line(screen, slate, (0, 120), (width, 120), 10)
    pygame.draw.line(screen, grey, (0, 130), (width, 130), 5)
    if music_paus:
        pygame.draw.line(screen, darkred, (605, 176), (645, 143), 7)

    # refreshing obrazovky
    pygame.display.update()

    # fps
    clock.tick(fps)

# ukonceni pygame
pygame.quit()
