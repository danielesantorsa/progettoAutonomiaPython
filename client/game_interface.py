import pygame
import sys

class InterfacciaDiGioco:
    def __init__(self):
        # Inizializza pygame
        pygame.init()

        # Dimensioni finestra
        self.larghezza_finestra = 800
        self.altezza_finestra = 600
        self.schermo = pygame.display.set_mode((self.larghezza_finestra, self.altezza_finestra))
        pygame.display.set_caption("Battaglia Navale")

        # Colori
        self.colore_sfondo = (0, 0, 64)
        self.colore_griglia = (255, 255, 255)
        self.colore_colpo = (255, 0, 0)
        self.colore_mancato = (0, 255, 0)

        # Griglia
        self.dimensione_cella = 30
        self.griglia_mia = [[0 for _ in range(10)] for _ in range(10)]
        self.griglia_nemica = [[0 for _ in range(10)] for _ in range(10)]

        # Messaggio
        self.font = pygame.font.SysFont(None, 28)
        self.messaggio = "Clicca sulla griglia di destra per sparare"

    def disegna_griglia(self, griglia, offset_x, offset_y):
        for riga in range(10):
            for colonna in range(10):
                x = offset_x + colonna * self.dimensione_cella
                y = offset_y + riga * self.dimensione_cella
                rect = pygame.Rect(x, y, self.dimensione_cella, self.dimensione_cella)
                pygame.draw.rect(self.schermo, self.colore_griglia, rect, 1)

                stato = griglia[riga][colonna]
                if stato == 1:
                    pygame.draw.circle(self.schermo, self.colore_colpo, rect.center, 10)
                elif stato == 2:
                    pygame.draw.circle(self.schermo, self.colore_mancato, rect.center, 10)

    def gestisci_click(self, posizione):
        # Coordinate del clic
        x, y = posizione

        # Coordinate griglia nemica (a destra)
        griglia_offset_x = 450
        griglia_offset_y = 100

        if griglia_offset_x <= x < griglia_offset_x + 10 * self.dimensione_cella and \
           griglia_offset_y <= y < griglia_offset_y + 10 * self.dimensione_cella:
            colonna = (x - griglia_offset_x) // self.dimensione_cella
            riga = (y - griglia_offset_y) // self.dimensione_cella

            # Aggiorna per esempio come "colpo" (stato 1)
            if self.griglia_nemica[riga][colonna] == 0:
                self.griglia_nemica[riga][colonna] = 1
                print(f"Hai sparato in posizione: ({colonna}, {riga})")

    def mostra_messaggio(self):
        testo = self.font.render(self.messaggio, True, (255, 255, 255))
        self.schermo.blit(testo, (20, 20))

    def run(self):
        in_esecuzione = True
        while in_esecuzione:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    in_esecuzione = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    self.gestisci_click(evento.pos)

            # Sfondo
            self.schermo.fill(self.colore_sfondo)

            # Mostra messaggio
            self.mostra_messaggio()

            # Disegna le due griglie
            self.disegna_griglia(self.griglia_mia, 50, 100)        # a sinistra
            self.disegna_griglia(self.griglia_nemica, 450, 100)    # a destra

            # Aggiorna lo schermo
            pygame.display.flip()

        pygame.quit()
        sys.exit()

# Avvio del gioco
if __name__ == "__main__":
    gioco = InterfacciaDiGioco()
    gioco.run()
