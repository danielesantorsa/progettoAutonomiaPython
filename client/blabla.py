#disattivazione scheda audio
import os
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
import sys

class Gioco:
    def __init__(self):
        # Inizializza Pygame
        pygame.init()

        # Dimensioni della finestra
        self.larghezza = 800
        self.altezza = 600
        self.schermo = pygame.display.set_mode((self.larghezza, self.altezza))

        # Titolo della finestra
        pygame.display.set_caption("Battaglia Navale")

        # Colore di sfondo
        self.colore_sfondo = (0, 0, 128)

        # Variabile di controllo per il ciclo principale
        self.in_esecuzione = True

    def avvia(self):
        # Ciclo principale del gioco
        while self.in_esecuzione:
            self.gestisci_eventi()
            self.aggiorna()
            self.disegna()

        # Pulizia finale
        pygame.quit()
        sys.exit()

    def gestisci_eventi(self):
        # Gestione degli eventi
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.in_esecuzione = False

    def aggiorna(self):
        # Logica del gioco (da implementare)
        pass

    def disegna(self):
        # Riempie lo sfondo
        self.schermo.fill(self.colore_sfondo)

        # Aggiorna lo schermo
        pygame.display.flip()

# Avvio del gioco
if __name__ == "__main__":
    gioco = Gioco()
    gioco.avvia()
