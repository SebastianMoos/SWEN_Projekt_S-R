def hanoi(n, source, target, auxiliary):
    if n == 1:
        print(f"Bewege Scheibe 1 von {source} nach {target}")
        return
    hanoi(n - 1, source, auxiliary, target)
    print(f"Bewege Scheibe {n} von {source} nach {target}")
    hanoi(n - 1, auxiliary, target, source)

# Beispielaufruf: Verschiebe 3 Scheiben von Stab A nach Stab C mit Hilfe von Stab B
hanoi(3, 'A', 'C', 'B')
# hanoi(3, 'A', 'C', 'B') Das ist ein Kommentar neu 