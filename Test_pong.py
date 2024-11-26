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
ball_diameter = ball_radius * 2
ball_centre_y = 150
ball_centre_x = (int((random.random() * 100000) % (size[0] - 200))) + 100
ball_direction = 'DOWN_LEFT'
ball_speed = 2

# Schläger-Einstellungen
hit_bar_speed = 18
hit_bar_length = 400
hit_bar_height = 25
min_hit_bar_length = 2 * ball_radius  # Minimale Balkenbreite
hit_bar_left = int(size[0] / 2) - int(hit_bar_length / 2)

# Loch im Schläger
hole_width = 6 * ball_radius  # Startgröße: 6-facher Ballradius
min_hole_width = ball_diameter  # Mindestgröße: gleich dem Durchmesser des Balls
hole_start_x = hit_bar_left + (hit_bar_length // 2) - (hole_width // 2)
hole_end_x = hole_start_x + hole_width

# Spielsteuerungsvariablen
time1 = pygame.time.get_ticks()
can_accel_left = False
can_accel_right = False
game_over = False
paused_game = False
score = 0

# Spiel zurücksetzen
def reset_game():
    global ball_centre_y, ball_centre_x, ball_direction, hit_bar_left, time1, can_accel_left, can_accel_right, game_over, paused_game, score, hole_width, hit_bar_length
    ball_centre_y = 150
    ball_centre_x = (int((random.random() * 100000) % (size[0] - 200))) + 100
    ball_direction = 'DOWN_LEFT'
    hit_bar_left = int(size[0] / 2) - int(hit_bar_length / 2)
    time1 = pygame.time.get_ticks()
    can_accel_left = False
    can_accel_right = False
    game_over = False
    paused_game = False
    score = 0
    hole_width = 6 * ball_radius  # Lücke zurücksetzen
    hit_bar_length = 400  # Balkenbreite zurücksetzen

# Spielbildschirm zeichnen
def draw_screen():
    global hole_start_x, hole_end_x
    screen.fill(black)
    font = pygame.font.Font(None, 100)

    if game_over:
        # "Game Over"-Nachricht
        game_over_text = font.render("Game Over", True, red)
        game_over_rect = game_over_text.get_rect(center=(size[0] // 2, size[1] // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        # Neustart-Hinweis
        restart_text = pygame.font.Font(None, 50).render("Press ENTER to restart", True, white)
        restart_rect = restart_text.get_rect(center=(size[0] // 2, size[1] // 2 + 50))
        screen.blit(restart_text, restart_rect)
    else:
        # Punkteanzeige
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

        # Korb-Linie zeichnen (direkt über dem unteren Rand)
        basket_line_y = size[1] - 5  # Linie knapp über dem Spielfeldrand
        pygame.draw.line(screen, white, (hole_start_x, basket_line_y), (hole_end_x, basket_line_y), 3)

    pygame.display.update()

# Hauptspiellogik
def play():
    global hit_bar_left, time1, ball_direction, ball_centre_x, ball_centre_y, score, game_over, hole_width, hit_bar_length

    if pygame.time.get_ticks() > (time1 + 11): 
        # Bewegung des Balls
        if ball_direction == 'DOWN_LEFT':
            ball_centre_x -= ball_speed
            ball_centre_y += ball_speed
        elif ball_direction == 'DOWN_RIGHT':
            ball_centre_x += ball_speed
            ball_centre_y += ball_speed
        elif ball_direction == 'UP_LEFT':
            ball_centre_x -= ball_speed
            ball_centre_y -= ball_speed
        elif ball_direction == 'UP_RIGHT':
            ball_centre_x += ball_speed
            ball_centre_y -= ball_speed

        # Wandkollisionen
        if ball_centre_x - ball_radius <= 0:
            ball_direction = 'DOWN_RIGHT' if 'DOWN' in ball_direction else 'UP_RIGHT'
        if ball_centre_x + ball_radius >= size[0]:
            ball_direction = 'DOWN_LEFT' if 'DOWN' in ball_direction else 'UP_LEFT'
        if ball_centre_y - ball_radius <= 0:
            ball_direction = 'DOWN_LEFT' if ball_direction == 'UP_LEFT' else 'DOWN_RIGHT'

        # Schlägerkollisionen
        if ball_centre_y + ball_radius >= size[1] - hit_bar_height:
            if hit_bar_left <= ball_centre_x <= hit_bar_left + hit_bar_length:
                # Treffer auf den Balken
                if hole_start_x <= ball_centre_x <= hole_end_x:
                    # Treffer in der Lücke
                    score += 1

                    # Lücke verkleinern in 5er-Schritten
                    if score % 5 == 0 and hole_width > min_hole_width:
                        hole_width -= ball_radius  # Reduziert die Breite um einen Ballradius pro Schritt
                    # Balken verkleinern, wenn Lücke minimal ist
                    if hole_width == min_hole_width and score % 5 == 0 and hit_bar_length > min_hit_bar_length:
                        hit_bar_length -= ball_radius * 2  # Reduziert Balkenbreite um zwei Ballradien

                    ball_centre_y = 150  # Reset Ballhöhe
                    ball_centre_x = (int((random.random() * 100000) % (size[0] - 200))) + 100
                    ball_direction = random.choice(['DOWN_LEFT', 'DOWN_RIGHT'])
                else:
                    # Ball prallt ab
                    ball_direction = 'UP_LEFT' if ball_direction == 'DOWN_LEFT' else 'UP_RIGHT'
            else:
                # Ball fällt außerhalb des Schlägers -> Game Over
                game_over = True
        elif ball_centre_y + ball_radius >= size[1]:
            # Ball fällt unter den Balken -> Game Over
            game_over = True

        # Schläger bewegen
        if can_accel_left and hit_bar_left > 0:
            hit_bar_left -= hit_bar_speed
        if can_accel_right and hit_bar_left + hit_bar_length < size[0]:
            hit_bar_left += hit_bar_speed

        time1 = pygame.time.get_ticks()

# Initialisiere das Spiel
pygame.init()
screen = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption("Pong mit Korb")
reset_game()

# Hauptspiel-Schleife
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_RETURN:
                # Spiel neu starten bei Game Over und Enter-Taste
                reset_game()
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
        draw_screen()
