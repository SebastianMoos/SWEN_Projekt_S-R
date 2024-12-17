# README für Projekt "Single Pong" 

## 1 Beschreibung Projekt/Spiel 
### Was war die Aufgabe des Projekts? 
Die Aufgabe des Projektes war ein Spiel zu erarbeiten um den Lernstoff im Fach SWEN anzuwenden.  
Im Rahmen des Masterstudiums WInf wollten wir ein Spiel mit unseren Ideen optimieren.
### Um was geht es in diesem Projekt?
In diesem Projekt geht es um eine Variante des Spieles "Pong"   
Wir haben das Spiel interaktiver, interessanter gestaltet. Deshalb nennen wir das Spiel "Poing".  

Das Spiel ist so aufgebaut, dass ein Einzelspieler es spielen kann.  
Es wird folgendermassen gespielt:  
Die Aufgabe ist es den roten Ball mit dem "Loch" im Schläger zu fangen. Dazu drückt man zum Starten des Spiels die "RETURN-TASTE". Zur Bewegung des Schlägers werden die Pfeiltasen "links" und "rechts" verwendet.
Dabei gelten folgende Regeln: 
Wenn der Ball gefangen wird dann gibt es einen Punkt. Der Ball kann mit dem Schläger zurückgeschlagen werden.
Wenn der Ball den Schläger nicht trifft, dann ist es "Game over".  
Punktestand.  
Pro gefangener Ball gibt es einen Punkt. Wenn der Punktestand 5 / 20 / 15 / 20 / 25 Punkte erreicht   
dann wird das Loch im Schläger kleiner und das Spiel schwieriger. 
Ebenfalls wird die Ballgeschwindigkeit abhängig vom Punktestand schneller. 
Wenn der Spieler die Punktestand von 25 erreicht hat, dann wird zusätzlich der Schläger in Abhängigkeit der Punktzahl kürzer.

### Mögliche Erweiterung des Spiels 
Für das Spiel sind verschiedene Erweiterungen denkbar. Beispielsweise ein Mehrspieler-Modus, die Implementierung einer Highscore-Anzeige oder das Hinzufügen von Hindernissen. 

## 2 Spielsteuerung 

Das Spiel wird wie folgt gesteuert: 
- Pfeiltaste links: Schläger nach links bewegen
- Pfeiltaste rechts: Schläger nach rechts bewegen
- ESC: Spiel pausieren
- ENTER: Neustart nach Game Over 


## 3 Technische Details und Files 

Das Projekt besteht aus folgenden Files: 

- README.md
- single_pong-neu.py (Spiel Single Pong)
- single_pong-neu_Backup261124.py (Backup File, welches den Stand vom 26.11.2024 enthält)
