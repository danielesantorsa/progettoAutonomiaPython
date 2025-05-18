import pygame
import sys

class InterfacciaDiGioco:
    def __init__(self):
        # Inizializzazione pygame
        pygame.init()

        # Imposta le dimensioni della finestra
        self.larghezza_finestra = 800
        self.altezza_finestra = 600
        self.schermo = pygame.display.set_mode((self.larghezza_finestra, self.altezza_finestra))

        # Imposta il titolo della finestra
        pygame.display.set_caption("Battaglia Navale")

        # Colori
        self.colore_sfondo = (0, 0, 0)
        self.colore_testo = (255, 255, 255)

        # Oggetto player
        self.player = pygame.Rect(300, 250, 50, 50)

    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Riempie lo sfondo
            self.schermo.fill(self.colore_sfondo)

            # Disegna il player
            pygame.draw.rect(self.schermo, (255, 0, 0), self.player)

            key = pygame.key.get_pressed()
            if key[pygame.k_a] == True:
                self.player.move_ip_(-1, 0)
                                                                                                                   

            # Aggiorna lo schermo
            pygame.display.update()

        pygame.quit()
        sys.exit()

# Avvio del gioco
if __name__ == "__main__":
    gioco = InterfacciaDiGioco()
    gioco.run()
