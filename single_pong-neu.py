import pygame
import sys
import random

# Farben und Spielfeldbedingungen
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (128, 128, 128)
size = [1000, 600]

# Ball-Einstellungen
ball_radius = 25
ball_centre_y = 150
ball_centre_x = (int((random.random() * 100000) % (size[0] - 200))) + 100
ball_direction = 'UP_LEFT'
ball_speed = 5

# Schläger-Einstellungen
hit_bar_speed = 18
hit_bar_length = 300
hit_bar_height = 25
hit_bar_left = int(size[0] / 2) - int(hit_bar_length / 2)

# Loch im Schläger
hole_width = 3 * ball_radius  # Loch ist dreimal so breit wie der Ballradius
hole_start_x = hit_bar_left + (hit_bar_length // 2) - (hole_width // 2)
hole_end_x = hole_start_x + hole_width

# Spielsteuerungsvariablen
time1 = pygame.time.get_ticks() #in Variable time1 wird Zeit gespreichert, welche seit Spielstart verstrichen ist
can_accel_left = False
can_accel_right = False
game_over = False
paused_game = False
score = 0

# Spiel zurücksetzen
def reset_game():
    global ball_centre_y, ball_centre_x, ball_direction, hit_bar_left, time1, can_accel_left, can_accel_right, game_over, paused_game, score
    ball_centre_y = 150
    ball_centre_x = (int((random.random() * 100000) % (size[0] - 200))) + 100
    ball_direction = 'UP_LEFT'
    hit_bar_left = int(size[0] / 2) - int(hit_bar_length / 2)
    time1 = pygame.time.get_ticks()
    can_accel_left = False
    can_accel_right = False
    game_over = False
    paused_game = False
    score = 0

# Spielbildschirm zeichnen
def draw_screen():
    global hole_start_x, hole_end_x
    screen.fill(black)
    font = pygame.font.Font(None, 100)
    scoreText = font.render(str(score), True, white)
    scoreRect = scoreText.get_rect()
    scoreRect.centerx = size[0] - 100
    scoreRect.centery = 100
    screen.blit(scoreText, scoreRect)

    # Ball zeichnen
    pygame.draw.circle(screen, red, (ball_centre_x, ball_centre_y), ball_radius)

    # Schläger zeichnen
    pygame.draw.rect(screen, blue, (hit_bar_left, size[1] - hit_bar_height, hit_bar_length, hit_bar_height))

    # Loch im Schläger hinzufügen
    hole_start_x = hit_bar_left + (hit_bar_length // 2) - (hole_width // 2)
    hole_end_x = hole_start_x + hole_width
    pygame.draw.rect(screen, black, (hole_start_x, size[1] - hit_bar_height, hole_width, hit_bar_height))

    pygame.display.update()

# Hauptspiellogik
def play():
    global hit_bar_left, time1, ball_direction, ball_centre_x, ball_centre_y, score, game_over

    if pygame.time.get_ticks() > (time1 + 11): # Die Bedingung sorgt dafür, dass die Ballbewegung nur alle 11 Millisekunden überprüft wird, um die Bewegung zeitlich zu regulieren.
        # Bewegung und Kollision des Balls
        if ball_direction == 'UP_LEFT':
            if (ball_centre_x - ball_speed) > ball_radius and (ball_centre_y - ball_speed) > ball_radius:
                ball_centre_x -= ball_speed
                ball_centre_y -= ball_speed
            elif (ball_centre_y - ball_speed) > ball_radius:
                ball_direction = 'UP_RIGHT'
            elif (ball_centre_x - ball_speed) > ball_radius:
                ball_direction = 'DOWN_LEFT'
            else:
                ball_direction = 'DOWN_RIGHT'

        elif ball_direction == 'UP_RIGHT':
            if (ball_centre_x + ball_speed) < (size[0] - ball_radius) and (ball_centre_y - ball_speed) > ball_radius:
                ball_centre_x += ball_speed
                ball_centre_y -= ball_speed
            elif (ball_centre_y - ball_speed) > ball_radius:
                ball_direction = 'UP_LEFT'
            elif (ball_centre_x + ball_speed) < (size[0] - ball_radius):
                ball_direction = 'DOWN_RIGHT'
            else:
                ball_direction = 'DOWN_LEFT'

        elif ball_direction == 'DOWN_LEFT':
            if (ball_centre_x - ball_speed) > ball_radius and (ball_centre_y + ball_speed) < (size[1] - ball_radius):
                if (ball_centre_x + ball_radius) >= hit_bar_left and (ball_centre_x - ball_radius) <= (hit_bar_left + hit_bar_length):
                    if hole_start_x <= ball_centre_x <= hole_end_x:
                        if (ball_centre_y + ball_radius) >= (size[1] - hit_bar_height):
                            ball_centre_y = size[1] - ball_radius
                            game_over = True
                        else:
                            ball_centre_x -= ball_speed
                            ball_centre_y += ball_speed
                    else:
                        if (ball_centre_y + ball_speed) < (size[1] - (ball_radius + hit_bar_height)):
                            ball_centre_x -= ball_speed
                            ball_centre_y += ball_speed
                        else:
                            ball_direction = 'UP_LEFT'
                            score += 1
                else:
                    ball_centre_x -= ball_speed
                    ball_centre_y += ball_speed
            elif (ball_centre_x - ball_speed) > ball_radius:
                ball_direction = 'UP_LEFT'
            elif (ball_centre_y + ball_speed) < (size[1] - ball_radius):
                ball_direction = 'DOWN_RIGHT'
            else:
                direction = 'UP_RIGHT'

        elif ball_direction == 'DOWN_RIGHT':
            if (ball_centre_x + ball_speed) < (size[0] - ball_radius) and (ball_centre_y + ball_speed) < (size[1] - ball_radius):
                if (ball_centre_x + ball_radius) >= hit_bar_left and (ball_centre_x - ball_radius) <= (hit_bar_left + hit_bar_length):
                    if hole_start_x <= ball_centre_x <= hole_end_x:
                        if (ball_centre_y + ball_radius) >= (size[1] - hit_bar_height):
                            ball_centre_y = size[1] - ball_radius
                            game_over = True
                        else:
                            ball_centre_x += ball_speed
                            ball_centre_y += ball_speed
                    else:
                        if (ball_centre_y + ball_speed) < (size[1] - (ball_radius + hit_bar_height)):
                            ball_centre_x += ball_speed
                            ball_centre_y += ball_speed
                        else:
                            ball_direction = 'UP_RIGHT'
                            score += 1
                else:
                    ball_centre_x += ball_speed
                    ball_centre_y += ball_speed
            elif (ball_centre_x + ball_speed) < (size[0] - ball_radius):
                ball_direction = 'UP_RIGHT'
            elif (ball_centre_y + ball_speed) < (size[1] - ball_radius):
                ball_direction = 'DOWN_LEFT'
            else:
                direction = 'UP_LEFT'

        if can_accel_left:
            if (hit_bar_left - hit_bar_speed) >= 0:
                hit_bar_left -= hit_bar_speed
        if can_accel_right:
            if (hit_bar_left + hit_bar_length + hit_bar_speed) <= size[0]:
                hit_bar_left += hit_bar_speed

        time1 = pygame.time.get_ticks()

# Initialisiere das Spiel
pygame.init()
screen = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption("Pong mit Schläger mit Loch")
reset_game()

# Hauptspiel-Schleife
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused_game = not paused_game
            if event.key == pygame.K_LEFT:
                can_accel_left = True
            if event.key == pygame.K_RIGHT:
                can_accel_right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                can_accel_left = False
            if event.key == pygame.K_RIGHT:
                can_accel_right = False

    if not paused_game and not game_over:
        play()
        draw_screen()

    if game_over:
        reset_game()
