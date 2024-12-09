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
ball_mitte_x = random.randint(100, 900)
ball_richtung = 'DOWN_LEFT'
ball_geschwindigkeit = 3

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
zeit1 = pygame.time.get_ticks()
kann_links_bewegen = False
kann_rechts_bewegen = False
game_over = False
spiel_pausieren = False
punkte_stand = 0

# Spiel zurücksetzen
def reset_game():
    global ball_mitte_y, ball_mitte_x, ball_richtung, schlaeger_rand_links, zeit1, kann_links_bewegen, kann_rechts_bewegen, game_over, spiel_pausieren, punkte_stand, loch_breite, schlaeger_laenge
    ball_mitte_y = 150 # Startmittelpunkt y für Ball
    ball_mitte_x =  groesse[0]/2 # Start in X ist die Hälfte von Bildschirm --> (int((random.random() * 100000) % (groesse[0] - 200))) + 100
    ball_richtung = 'DOWN_LEFT' #Bei Start wird der Ball nach unten links gestartet
    schlaeger_rand_links = int(groesse[0] / 2) - int(schlaeger_laenge / 2) # Schläger Position zurücksetzen
    # `#Schlägerrand links
    #Schlägerrand links definiert
    zeit1 = pygame.time.get_ticks() #Zeit vergangen seit start des Spiels
    kann_links_bewegen = False # alles zurücksetzen
    kann_rechts_bewegen = False # alles zurücksetzen
    game_over = False # alles zurücksetzen
    spiel_pausieren = False # alles zurücksetzen
    punkte_stand = 0 # alles zurücksetzen
    loch_breite = 6 * ball_radius  # Lücke zurücksetzen
    schlaeger_laenge = 400  # Balkenbreite zurücksetzen

# Spielbildschirm zeichnen
def draw_screen():
    global loch_rand_links, loch_rand_rechts # Loch ränder definieren
    screen.fill(schwarz) # Bildschirm schwarz ausfüllen
    font = pygame.font.Font(None, 100) # Schrift definieren

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
        punkte_standText = font.render(str(punkte_stand), True, weiss)
        punkte_standRect = punkte_standText.get_rect()
        # Schriftposition definieren
        punkte_standRect.centerx = groesse[0] - 100 
        punkte_standRect.centery = 100
        screen.blit(punkte_standText, punkte_standRect)

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
    global schlaeger_rand_links, zeit1, ball_richtung, ball_mitte_x, ball_mitte_y, punkte_stand, game_over, loch_breite, schlaeger_laenge, ball_geschwindigkeit

    # Berechne die neue Ballgeschwindigkeit basierend auf dem Punktestand
    faktor = punkte_stand / 60.0 if punkte_stand <= 60.0 else 1.0
    temp_ball_geschwindigkeit = ball_geschwindigkeit * (1 + faktor)

    if pygame.time.get_ticks() > (zeit1 + 11):
        # Bewegung des Balls gemäss Punktestand
        if ball_richtung == 'DOWN_LEFT':
            ball_mitte_x -= temp_ball_geschwindigkeit
            ball_mitte_y += temp_ball_geschwindigkeit
        elif ball_richtung == 'DOWN_RIGHT':
            ball_mitte_x += temp_ball_geschwindigkeit
            ball_mitte_y += temp_ball_geschwindigkeit
        elif ball_richtung == 'UP_LEFT':
            ball_mitte_x -= temp_ball_geschwindigkeit
            ball_mitte_y -= temp_ball_geschwindigkeit
        elif ball_richtung == 'UP_RIGHT':
            ball_mitte_x += temp_ball_geschwindigkeit
            ball_mitte_y -= temp_ball_geschwindigkeit

        # Wandkollisionen
        if ball_mitte_x - ball_radius <= 0:  #Wand links: Wenn die linke Kante des Balls (Mittelpunkt minus Radius) die Wand trifft (x<=0)
            ball_richtung = 'DOWN_RIGHT' if 'DOWN' in ball_richtung else 'UP_RIGHT' 
        if ball_mitte_x + ball_radius >= groesse[0]: #Wand Rechts: Wenn die rechte Kante des Balls (Mittelpunkt plus Radius) die Wand trifft (x>=0)
            ball_richtung = 'DOWN_LEFT' if 'DOWN' in ball_richtung else 'UP_LEFT'
        if ball_mitte_y - ball_radius <= 0:  #Obere Wand: Wenn die obere Kante des Balls (Mittelpunkt minus Radius) die Wand trifft (y<=0)
            ball_richtung = 'DOWN_LEFT' if ball_richtung == 'UP_LEFT' else 'DOWN_RIGHT'

        # Schlägerkollisionen
        if ball_mitte_y + ball_radius >= groesse[1] - schlaeger_hoehe: #Wenn die untere Kante des Balls den Schläger berührt (groesse(1) = Höhe des Spielfelds) 
            if schlaeger_rand_links <= ball_mitte_x <= schlaeger_rand_links + schlaeger_laenge: #Wenn der Ball auf dem Schläger ist (Ballmitte zwischen Schlägerrand links und Schlägerand rechts)
                # Treffer auf den Balken
                if loch_rand_links <= ball_mitte_x <= loch_rand_rechts: #Wenn der Ball zwischen die Lochränder (ins Loch) fällt, dann wird ein Punkt dazugezählt
                    # Treffer in der Lücke
                    punkte_stand += 1

                    # Lücke verkleinern in 5er-Schritten
                    if punkte_stand % 5 == 0 and loch_breite > min_loch_breite:  #hier wird geprüft ob der aktuelle punkte_stand durch 5 teilbar ist. Sofern dies der Fall ist und die Loch Breite grösser als die min_lochbreite ist...
                        loch_breite -= ball_radius  # reduziert die Breite um einen Ballradius pro Schritt
                    # Balken verkleinern, wenn Lücke minimal ist
                    if loch_breite == min_loch_breite and punkte_stand % 5 == 0 and schlaeger_laenge > min_schlaeger_laenge:  #Wenn die minimale Lochgrösse erreicht wird und die Punktzahl durch 5 teilbar ist, wird der Code auf der nächsten Zeile ausgeführt. 
                        schlaeger_laenge -= ball_radius * 2  # reduziert Balkenbreite um zwei Ballradien (-= ist eine Kurzschreibweise in Python für: schläger_länge= schläger_länge - ball radius)

                    ball_mitte_y = 150  # Reset Ballhöhe (Wenn der Ball ins Loch fällt, wird der Ball neu positioniert --> Start Werte)
                    ball_mitte_x = random.randint(100, 900)
                    ball_richtung = random.choice(['DOWN_LEFT', 'DOWN_RIGHT'])
                else:
                    # Ball prallt ab (Wenn der Ball den Schläger außerhalb der Lücke trifft, ändert sich seine Richtung, und er wird nach oben abgelenkt.)
                    ball_richtung = 'UP_LEFT' if ball_richtung == 'DOWN_LEFT' else 'UP_RIGHT'  #Ballrichtung nach Schläger berührung: Wenn Ball von rechts kommt, "fliegt" er nach Links weiter und umgekehrt.
            else:
                # Ball fällt außerhalb des Schlägers -> Game Over
                game_over = True
        elif ball_mitte_y + ball_radius >= groesse[1]: #Wenn der Ball den unteren Spielfeldrand berührt 
            # Ball fällt unter den Balken -> Game Over
            game_over = True

        # Schläger bewegen
        if kann_links_bewegen and schlaeger_rand_links > 0:  #kann_links_bewegen prüft ob Schläger nach links bewegt werden darf (also ob die Pfeiltaste liks gedrückt ist)
            schlaeger_rand_links -= schlaeger_geschwindigkeit
        if kann_rechts_bewegen and schlaeger_rand_links + schlaeger_laenge < groesse[0]:
            schlaeger_rand_links += schlaeger_geschwindigkeit

        zeit1 = pygame.time.get_ticks()

# Initialisiere das Spiel
pygame.init()
screen = pygame.display.set_mode(groesse, 0, 32)
pygame.display.set_caption("Pong mit Korb")
reset_game()

# Hauptspiel-Schleife
while True: # Schleife läuft bis das Spiel beendet wird (z.B. durch sys.exit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Wenn das Fenster geschlossen wird (pygame.QUIT), wird das Programm mit sys.exit() beendet.
            sys.exit()
        if event.type == pygame.KEYDOWN: # zeigt alle Events auf, welche durch Tastendruck erfolgen (solange die Taste gedrückt)
            if game_over and event.key == pygame.K_RETURN: #Wenn das Spiel beendet ist (game_over == True) und die Enter-Taste (K_RETURN) gedrückt wird, wird das Spiel zurückgesetzt, indem reset_game() aufgerufen wird
                # Spiel neu starten bei Game Over und Enter-Taste
                reset_game()
            if event.key == pygame.K_ESCAPE:
                spiel_pausieren = not spiel_pausieren
            if event.key == pygame.K_LEFT:
                kann_links_bewegen = True
            if event.key == pygame.K_RIGHT:
                kann_rechts_bewegen = True
        if event.type == pygame.KEYUP:  # zeigt alle Events auf, welche durch Loslassen der Taste erfolgen (Werte verändern sich auf False und Aktion wird gestoppt)
            if event.key == pygame.K_LEFT:
                kann_links_bewegen = False
            if event.key == pygame.K_RIGHT:
                kann_rechts_bewegen = False

    if not spiel_pausieren and not game_over:
        play()
        draw_screen()

    if game_over:
        draw_screen()
