import pygame
import sys
import random

# Farben und Spielfeldbedingungen
weiss = (255, 255, 255)
schwarz = (0, 0, 0)
rot = (255, 0, 0)
blau = (0, 0, 255)
grau = (128, 128, 128)
groesse = [1000, 600]

# Ball-Einstellungen
ball_radius = 25
ball_durchmesser = ball_radius * 2
ball_mitte_y = 150
ball_mitte_x = (int((random.random() * 100000) % (groesse[0] - 200))) + 100
ball_richtung = 'DOWN_LEFT'
ball_geschwindigkeit = 2

# Schläger-Einstellungen
schlaeger_geschwindigkeit = 10
schlaeger_laenge = 400
schlaeger_hoehe = 25
min_schlaeger_laenge = 2 * ball_radius  # Minimale Balkenbreite
schlaeger_rand_links = int(groesse[0] / 2) - int(schlaeger_laenge / 2)

# Loch im Schläger
loch_breite = 6 * ball_radius  # Startgröße: 6-facher Ballradius
min_loch_breite = ball_durchmesser  # Mindestgröße: gleich dem Durchmesser des Balls
loch_rand_links = schlaeger_rand_links + (schlaeger_laenge // 2) - (loch_breite // 2)
loch_rand_rechts = loch_rand_links + loch_breite

# Spielsteuerungsvariablen
time1 = pygame.time.get_ticks()
can_accel_left = False
can_accel_right = False
game_over = False
paused_game = False
score = 0

# Spiel zurücksetzen
def reset_game():
    global ball_mitte_y, ball_mitte_x, ball_richtung, schlaeger_rand_links, time1, can_accel_left, can_accel_right, game_over, paused_game, score, loch_breite, schlaeger_laenge
    ball_mitte_y = 150
    ball_mitte_x = (int((random.random() * 100000) % (groesse[0] - 200))) + 100
    ball_richtung = 'DOWN_LEFT'
    schlaeger_rand_links = int(groesse[0] / 2) - int(schlaeger_laenge / 2)
    time1 = pygame.time.get_ticks()
    can_accel_left = False
    can_accel_right = False
    game_over = False
    paused_game = False
    score = 0
    loch_breite = 6 * ball_radius  # Lücke zurücksetzen
    schlaeger_laenge = 400  # Balkenbreite zurücksetzen

# Spielbildschirm zeichnen
def draw_screen():
    global loch_rand_links, loch_rand_rechts
    screen.fill(schwarz)
    font = pygame.font.Font(None, 100)

    if game_over: 
        # "Game Over"-Nachricht eingefügt
        game_over_text = font.render("Game Over", True, rot)
        game_over_rect = game_over_text.get_rect(center=(groesse[0] // 2, groesse[1] // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        # Neustart-Hinweis
        restart_text = pygame.font.Font(None, 50).render("Press ENTER to restart", True, weiss)
        restart_rect = restart_text.get_rect(center=(groesse[0] // 2, groesse[1] // 2 + 50))
        screen.blit(restart_text, restart_rect)
    else:
        # Punkteanzeige
        scoreText = font.render(str(score), True, weiss)
        scoreRect = scoreText.get_rect()
        scoreRect.centerx = groesse[0] - 100
        scoreRect.centery = 100
        screen.blit(scoreText, scoreRect)

        # Ball zeichnen
        pygame.draw.circle(screen, rot, (ball_mitte_x, ball_mitte_y), ball_radius)

        # Schläger zeichnen
        pygame.draw.rect(screen, blau, (schlaeger_rand_links, groesse[1] - schlaeger_hoehe, schlaeger_laenge, schlaeger_hoehe))

        # Loch im Schläger hinzufügen
        loch_rand_links = schlaeger_rand_links + (schlaeger_laenge // 2) - (loch_breite // 2)
        loch_rand_rechts = loch_rand_links + loch_breite
        pygame.draw.rect(screen, schwarz, (loch_rand_links, groesse[1] - schlaeger_hoehe, loch_breite, schlaeger_hoehe))

        # Korb-Linie zeichnen (direkt über dem unteren Rand)
        basket_line_y = groesse[1] - 5  # Linie knapp über dem Spielfeldrand
        pygame.draw.line(screen, weiss, (loch_rand_links, basket_line_y), (loch_rand_rechts, basket_line_y), 3)

    pygame.display.update()

# Hauptspiellogik
def play():
    global schlaeger_rand_links, time1, ball_richtung, ball_mitte_x, ball_mitte_y, score, game_over, loch_breite, schlaeger_laenge

    if pygame.time.get_ticks() > (time1 + 11): 
        # Bewegung des Balls
        if ball_richtung == 'DOWN_LEFT':
            ball_mitte_x -= ball_geschwindigkeit
            ball_mitte_y += ball_geschwindigkeit
        elif ball_richtung == 'DOWN_RIGHT':
            ball_mitte_x += ball_geschwindigkeit
            ball_mitte_y += ball_geschwindigkeit
        elif ball_richtung == 'UP_LEFT':
            ball_mitte_x -= ball_geschwindigkeit
            ball_mitte_y -= ball_geschwindigkeit
        elif ball_richtung == 'UP_RIGHT':
            ball_mitte_x += ball_geschwindigkeit
            ball_mitte_y -= ball_geschwindigkeit

        # Wandkollisionen
        if ball_mitte_x - ball_radius <= 0:
            ball_richtung = 'DOWN_RIGHT' if 'DOWN' in ball_richtung else 'UP_RIGHT'
        if ball_mitte_x + ball_radius >= groesse[0]:
            ball_richtung = 'DOWN_LEFT' if 'DOWN' in ball_richtung else 'UP_LEFT'
        if ball_mitte_y - ball_radius <= 0:
            ball_richtung = 'DOWN_LEFT' if ball_richtung == 'UP_LEFT' else 'DOWN_RIGHT'

        # Schlägerkollisionen
        if ball_mitte_y + ball_radius >= groesse[1] - schlaeger_hoehe:
            if schlaeger_rand_links <= ball_mitte_x <= schlaeger_rand_links + schlaeger_laenge:
                # Treffer auf den Balken
                if loch_rand_links <= ball_mitte_x <= loch_rand_rechts:
                    # Treffer in der Lücke
                    score += 1

                    # Lücke verkleinern in 5er-Schritten
                    if score % 5 == 0 and loch_breite > min_loch_breite:
                        loch_breite -= ball_radius  # rotuziert die Breite um einen Ballradius pro Schritt
                    # Balken verkleinern, wenn Lücke minimal ist
                    if loch_breite == min_loch_breite and score % 5 == 0 and schlaeger_laenge > min_schlaeger_laenge:
                        schlaeger_laenge -= ball_radius * 2  # rotuziert Balkenbreite um zwei Ballradien

                    ball_mitte_y = 150  # Reset Ballhöhe
                    ball_mitte_x = (int((random.random() * 100000) % (groesse[0] - 200))) + 100
                    ball_richtung = random.choice(['DOWN_LEFT', 'DOWN_RIGHT'])
                else:
                    # Ball prallt ab
                    ball_richtung = 'UP_LEFT' if ball_richtung == 'DOWN_LEFT' else 'UP_RIGHT'
            else:
                # Ball fällt außerhalb des Schlägers -> Game Over
                game_over = True
        elif ball_mitte_y + ball_radius >= groesse[1]:
            # Ball fällt unter den Balken -> Game Over
            game_over = True

        # Schläger bewegen
        if can_accel_left and schlaeger_rand_links > 0:
            schlaeger_rand_links -= schlaeger_geschwindigkeit
        if can_accel_right and schlaeger_rand_links + schlaeger_laenge < groesse[0]:
            schlaeger_rand_links += schlaeger_geschwindigkeit

        time1 = pygame.time.get_ticks()

# Initialisiere das Spiel
pygame.init()
screen = pygame.display.set_mode(groesse, 0, 32)
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
