#--------------------------------imports--------------------------------
import pygame
import sys
import random
import os
#-------------------------------variables-------------------------------
score_index_x = 60
score_index_y = 35
high_score_index_x = 95
high_score_index_y = 85
bg_y_pos = 0
sub_x = 480
sub_y = 350
sub_add = 0
game_active = False
spike_list = []
spike_spawn_position = [300, 350, 400, 450, 500, 550, 600]
score = 0
high_score = 0
want_music = 1
high_score_file = 'high_score.txt'
#-------------------------------functions-------------------------------
#comment

def score_display(game_state):
    if game_state == True:
        if score == 0:
            score_surface = my_font.render('Score: 0', False, (255, 0, 0))
            score_rect = score_surface.get_rect(center=(score_index_x, score_index_y))
            screen.blit(score_surface, score_rect)
        else:
            score_surface = my_font.render(f'Score: {score-1}', False, (255, 0, 0))
            score_rect = score_surface.get_rect(center=(score_index_x, score_index_y))
            screen.blit(score_surface, score_rect)
    else:
        if score == 0:
            score_surface = my_font.render('Score: 0', False, (255, 0, 0))
            score_rect = score_surface.get_rect(center=(score_index_x, score_index_y))
            screen.blit(score_surface, score_rect)
        else:
            score_surface = my_font.render(f'Score: {score-1}', False, (255, 0, 0))
            score_rect = score_surface.get_rect(center=(score_index_x, score_index_y))
            screen.blit(score_surface, score_rect)

        try:
            high_score_surface = my_font.render(f'high score: {get_high_score(high_score_file)}', False, (255, 0, 0))
            high_score_rect = high_score_surface.get_rect(center=(high_score_index_x, high_score_index_y))
            screen.blit(high_score_surface, high_score_rect)
        except:
            high_score_surface = my_font.render(f'0', False, (255, 0, 0))
            high_score_rect = high_score_surface.get_rect(center=(high_score_index_x, high_score_index_y))
            screen.blit(high_score_surface, high_score_rect)

def draw_bg():
    screen.blit(bg_surface, (0, bg_y_pos))
    screen.blit(bg_surface, (0, bg_y_pos - 540))


def create_spike():
    random_spike_pos = random.choice(spike_spawn_position)
    first_spike = spike_surface.get_rect(topright=(random_spike_pos-250, -25))
    second_spike = spike_surface.get_rect(topleft=(random_spike_pos, -25))
    return first_spike, second_spike


def move_spike(spikes):
    for spike in spikes:
        spike.centery +=3
    return spikes


def draw_spikes(spikes):
    for spike in spikes:
        if spike.right >= 900:
            screen.blit(spike_surface, spike)
        else:
            spike_flipped = pygame.transform.flip(spike_surface, True, False)
            screen.blit(spike_flipped, spike)


def check_collision(spikes):
    for spike in spikes:
        if spike.collidepoint(sub_x, 365):
            slap.play()
            return False
    return True


def get_high_score(file_name):
    content = ""
    if os.path.isfile(file_name):
        with open(file_name, 'r') as content_file:
            content = content_file.read()

    return content


def set_high_score(file_name):
    if high_score > int(get_high_score(high_score_file)):
        content = open(file_name, 'w')
        to_write = ""
        to_write += str(high_score)
        content.write(to_write)
        content.close()

#------------------------------pygame loop------------------------------
pygame.init()
pygame.display.set_caption("PixelSub")
pygame.display.set_icon(pygame.image.load('icon.ico'))
my_font2 = pygame.font.Font('font2.ttf', 24)
my_font = pygame.font.Font('my_font.ttf', 16)
running = True
screen = pygame.display.set_mode((960, 540))
clock = pygame.time.Clock()
bg_surface = pygame.image.load('bg.png').convert_alpha()
bg_surface = pygame.transform.scale(bg_surface, (960, 540))
sub_surface = pygame.image.load('sub.png').convert_alpha()
sub_surface = pygame.transform.scale(sub_surface, (50, 35))
sub_rect = sub_surface.get_rect(center=(sub_x, 300))
rotated_sub = pygame.image.load('sub flipped.png').convert_alpha()
rotated_sub = pygame.transform.scale(rotated_sub, (50, 35))
press_surface = pygame.image.load('press space.png').convert_alpha()
press_surface = pygame.transform.scale(press_surface, (600, 200))
spike_surface = pygame.image.load('spike.png').convert_alpha()
spike_surface = pygame.transform.scale(spike_surface, (850, 25))
#-------------------------------music files-------------------------------
music = pygame.mixer.music.load('song.mp3')
slap = pygame.mixer.Sound('click.wav')
SPIKESPAWN = pygame.USEREVENT
pygame.time.set_timer(SPIKESPAWN, 600)
#-------------------------------beggining of the loop-------------------------------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                sub_add = 3
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                sub_add = -3
            if event.key == pygame.K_SPACE:
                game_active = True
                score = 0
                slap.play()
            if event.key == pygame.K_ESCAPE:
                game_active = False
                slap.play()
            if event.key == pygame.K_x and game_active == False:
                set_high_score(high_score_file)
                slap.play()
                running = False
            if event.key == pygame.K_m:
                want_music *=-1
                slap.play()
        if game_active == True and event.type == SPIKESPAWN:
            spike_list.extend(create_spike())
            score +=1
    bg_y_pos += 3
    draw_bg()
    if bg_y_pos >= 540:
        bg_y_pos = 0
    spike_list = move_spike(spike_list)
    draw_spikes(spike_list)
    if want_music == 1:
        pygame.mixer.music.play(-1)
    if game_active == False:
        close_surface = my_font.render(f'Press (x) To Exit The Game', False, (255, 0, 0))
        close_rect = close_surface.get_rect(center=(770, 35))
        screen.blit(close_surface, close_rect)
        m_surface = my_font.render(f'Press (m) To Toggle Music', False, (255, 0, 0))
        m_rect = m_surface.get_rect(center=(770, 85))
        screen.blit(m_surface, m_rect)
        dev_surface = my_font2.render(f'Dev: @odai.exe on instagram', False, (0, 100, 255))
        dev_rect = dev_surface.get_rect(center=(760, 490))
        screen.blit(dev_surface, dev_rect)
        screen.blit(press_surface, (175, 190))
        spike_list.clear()
        sub_rect.center = (270, 300)
        score_display(game_active)
        if score > high_score:
            high_score = score -1
        set_high_score(high_score_file)
    if game_active == True:
        x = 0
        if sub_x > 915:
            sub_x = 915
        if sub_x < 5:
            sub_x = 5
        sub_x += sub_add
        if sub_add > 0:
            screen.blit(sub_surface, (sub_x, sub_y))
        if sub_add < 0:
            screen.blit(rotated_sub, (sub_x, sub_y))
        game_active = check_collision(spike_list)
        score_display(game_active)
    pygame.display.update()
    clock.tick(120)
