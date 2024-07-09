import pygame
import random
import sys

pygame.init()

screen_width = 800
screen_height = 600

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Avoid the Blocks")

player_size = 50
player_pos = [screen_width // 2, screen_height - 2 * player_size]
player_speed = 10

enemy_size = 50
enemy_pos = [random.randint(0, screen_width - enemy_size), 0]
enemy_speed = 10

clock = pygame.time.Clock()

font = pygame.font.SysFont("monospace", 35)

def detect_collision(player_pos, enemy_pos):
    p_x, p_y = player_pos
    e_x, e_y = enemy_pos

    if (e_x < p_x < e_x + enemy_size or e_x < p_x + player_size < e_x + enemy_size) and \
       (e_y < p_y < e_y + enemy_size or e_y < p_y + player_size < e_y + enemy_size):
        return True
    return False

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, screen_width - enemy_size)
        enemy_list.append([x_pos, 0])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, blue, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < screen_height:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def check_collisions(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos):
            return True
    return False

def game_over_screen(score):
    screen.fill(black)
    game_over_text = font.render("Game Over!", True, red)
    score_text = font.render("Score: " + str(score), True, red)
    screen.blit(game_over_text, (screen_width / 2 - game_over_text.get_width() / 2, screen_height / 2 - game_over_text.get_height() / 2))
    screen.blit(score_text, (screen_width / 2 - score_text.get_width() / 2, screen_height / 2 + game_over_text.get_height()))
    pygame.display.update()
    pygame.time.wait(2000)

def main():
    running = True
    score = 0
    enemy_list = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] and player_pos[1] > 0:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < screen_height - player_size:
            player_pos[1] += player_speed

        screen.fill(white)

        drop_enemies(enemy_list)
        score = update_enemy_positions(enemy_list, score)
        draw_enemies(enemy_list)

        if check_collisions(enemy_list, player_pos):
            game_over_screen(score)
            main()

        pygame.draw.rect(screen, red, (player_pos[0], player_pos[1], player_size, player_size))

        score_text = font.render("Score: " + str(score), True, black)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(30)

main()
