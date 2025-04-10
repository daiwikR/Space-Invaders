import pygame
import random
import math
import sys

pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders - Matrix of Enemies")

player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
player_bullet_img = pygame.image.load("bullet.png")

player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
player_bullet_img = pygame.transform.scale(player_bullet_img, (10, 20))

player_width = player_img.get_width()
player_height = player_img.get_height()
player_x = (SCREEN_WIDTH - player_width) // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 5

player_bullet_speed = 10
player_bullets = []

ENEMY_SIZE = 50
ENEMY_BULLET_SPEED = 7

enemy_bullets = []
enemy_bullet_cooldown = 2000
last_enemy_shot_time = 0
enemy_direction = 1
enemy_speed_x = 2
enemy_descend_amount = 10

def spawn_enemies(level):
    enemy_rows = min(3 + (level - 1) // 3, 5)
    enemy_columns = min(6 + level, 10)
    spacing_x = 10
    spacing_y = 10
    total_width = enemy_columns * ENEMY_SIZE + (enemy_columns - 1) * spacing_x
    start_x = (SCREEN_WIDTH - total_width) // 2
    start_y = 50
    new_enemies = []
    for row in range(enemy_rows):
        for col in range(enemy_columns):
            x_pos = start_x + col * (ENEMY_SIZE + spacing_x)
            y_pos = start_y + row * (ENEMY_SIZE + spacing_y)
            new_enemies.append({'x': x_pos, 'y': y_pos, 'alive': True})
    return new_enemies

score = 0
level = 1
max_level = 10
game_over = False

font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 72)

def reset_level(lvl):
    global enemies, enemy_direction, enemy_speed_x, enemy_descend_amount, enemy_bullet_cooldown, enemy_bullets
    enemies = spawn_enemies(lvl)
    enemy_direction = 1
    enemy_speed_x = 2 + lvl
    enemy_descend_amount = 10 + 2 * lvl
    enemy_bullet_cooldown = max(500, 2000 - (lvl - 1) * 150)
    enemy_bullets = []

def draw_text(text, x, y, font_obj, color=(255, 255, 255)):
    img = font_obj.render(text, True, color)
    screen.blit(img, (x, y))

def is_collision(x1, y1, x2, y2, threshold=27):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) < threshold

reset_level(level)

running = True
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                sys.exit()
            elif event.key == pygame.K_SPACE and not game_over:
                bullet_x = player_x + player_width // 2 - 5
                bullet_y = player_y
                player_bullets.append({'x': bullet_x, 'y': bullet_y})
    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
    player_x = max(0, min(player_x, SCREEN_WIDTH - player_width))
    for b in player_bullets[:]:
        b['y'] -= player_bullet_speed
        if b['y'] < 0:
            player_bullets.remove(b)
    for bullet in enemy_bullets[:]:
        bullet['y'] += ENEMY_BULLET_SPEED
        if bullet['y'] > SCREEN_HEIGHT:
            enemy_bullets.remove(bullet)
            continue
        bullet_center_x = bullet['x'] + 5
        bullet_center_y = bullet['y'] + 10
        player_center_x = player_x + player_width // 2
        player_center_y = player_y + player_height // 2
        if is_collision(bullet_center_x, bullet_center_y, player_center_x, player_center_y, threshold=25):
            game_over = True
    alive_enemies = [e for e in enemies if e['alive']]
    if alive_enemies:
        leftmost_x = min(e['x'] for e in alive_enemies)
        rightmost_x = max(e['x'] for e in alive_enemies)
        if leftmost_x < 0 or rightmost_x > SCREEN_WIDTH - ENEMY_SIZE:
            enemy_direction *= -1
            for e in alive_enemies:
                e['y'] += enemy_descend_amount
        for e in alive_enemies:
            e['x'] += enemy_direction * enemy_speed_x
        for e in alive_enemies:
            if e['y'] + ENEMY_SIZE >= SCREEN_HEIGHT - 50:
                game_over = True
                break
    current_time = pygame.time.get_ticks()
    if not game_over and alive_enemies and (current_time - last_enemy_shot_time > enemy_bullet_cooldown):
        shoot_probability = 0.1 + (level - 1) * 0.03
        for enemy in alive_enemies:
            if random.random() < shoot_probability:
                enemy_bullets.append({'x': enemy['x'] + ENEMY_SIZE // 2 - 5, 'y': enemy['y'] + ENEMY_SIZE})
        last_enemy_shot_time = current_time
    for b in player_bullets[:]:
        bullet_cx = b['x'] + 5
        bullet_cy = b['y'] + 10
        for e in enemies:
            if e['alive']:
                enemy_center_x = e['x'] + ENEMY_SIZE // 2
                enemy_center_y = e['y'] + ENEMY_SIZE // 2
                if is_collision(bullet_cx, bullet_cy, enemy_center_x, enemy_center_y, 25):
                    e['alive'] = False
                    score += 1
                    if b in player_bullets:
                        player_bullets.remove(b)
                    break
    if all(not e['alive'] for e in enemies) and not game_over:
        level += 1
        if level > max_level:
            level = 1
        reset_level(level)
        player_bullets.clear()
        enemy_bullets.clear()
    for e in enemies:
        if e['alive']:
            screen.blit(enemy_img, (e['x'], e['y']))
    for bullet in enemy_bullets:
        pygame.draw.rect(screen, (255, 0, 0), (bullet['x'], bullet['y'], 10, 20))
    for b in player_bullets:
        screen.blit(player_bullet_img, (b['x'], b['y']))
    screen.blit(player_img, (player_x, player_y))
    draw_text(f"Score: {score}   Level: {level}", 10, 10, font)
    if game_over:
        draw_text("GAME OVER", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, big_font, (255, 0, 0))
    pygame.display.flip()
pygame.quit()
sys.exit()
