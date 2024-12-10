# Farben und Spielfeldbedingungen
groesse = [1000, 600]

# Schläger-Einstellungen
schlaeger_laenge = 400
schlaeger_rand_links = int(groesse[0] / 2) - int(schlaeger_laenge / 2)

# Loch im Schläger
loch_breite = 6 * ball_radius  # Startgröße: 6-facher Ballradius
min_loch_breite = ball_durchmesser  # Mindestgröße: gleich dem Durchmesser des Balls
loch_rand_links = schlaeger_rand_links + (schlaeger_laenge // 2) - (loch_breite // 2)
loch_rand_rechts = loch_rand_links + loch_breite