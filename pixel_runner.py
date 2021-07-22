import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obs_list):
    if obs_list:
        for obstacle_rect in obs_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
            else: screen.blit(fly_surf, obstacle_rect)
        
        obs_list = [obstacle for obstacle in obs_list if obstacle.x > -100]
        
        return obs_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index +=0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Pixel Runner')
clock = pygame.time.Clock()
font = pygame.font.Font('runner\Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('runner\graphics\Sky.png').convert()
ground_surface = pygame.image.load('runner\graphics\ground.png').convert()

# Obstacles
snail_frame_1 = pygame.image.load('runner\graphics\snail\snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('runner\graphics\snail\snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('runner\graphics\Fly\Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('runner\graphics\Fly\Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_list = []

player_walk1 = pygame.image.load('runner\graphics\player\player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('runner\graphics\player\player_walk_2.png').convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0
player_jump = pygame.image.load('runner\graphics\player\jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

player_stand = pygame.image.load('runner\graphics\player\player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = font.render('Pixel Runner', False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = font.render('Press space to run', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400, 340))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >=300:
                    player_gravity = -20

            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >=300:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20
        
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)

        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_list.append(snail_surf.get_rect(bottomright = (randint(900,1500), 300)))
            else:
                obstacle_list.append(fly_surf.get_rect(bottomright = (randint(900, 1500), 210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface, (0,300))

        score = display_score()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

        # Obstacle Movement
        obstacle_list = obstacle_movement(obstacle_list)
        # Game Mechanics
        game_active = collisions(player_rect, obstacle_list)

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        obstacle_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0

        score_message = font.render(f'Your score: {score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        
        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)