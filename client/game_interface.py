import pygame
import sys

class InterfacciaDiGioco:
    def __init__(self):
        pygame.init()

        # Finestra
        self.larghezza_finestra = 800
        self.altezza_finestra = 600
        self.schermo = pygame.display.set_mode((self.larghezza_finestra, self.altezza_finestra))
        pygame.display.set_caption("Battaglia Navale")

        # Colori
        self.colore_sfondo = (0, 0, 64)
        self.colore_griglia = (255, 255, 255)
        self.colore_barca = (160, 160, 160)
        self.colore_colpo = (255, 0, 0)
        self.colore_mancato = (0, 255, 0)

        # Griglie
        self.dimensione_cella = 30
        self.griglia_attacchi = [[0 for _ in range(10)] for _ in range(10)]
        self.griglia_mia = [[0 for _ in range(10)] for _ in range(10)]

        # Stato
        self.font = pygame.font.SysFont(None, 28)
        self.fase_piazzamento = True
        self.barche_da_posizionare = 5
        self.messaggio = "Posiziona 5 barche nella griglia di destra"

    def disegna_griglia(self, griglia, offset_x, offset_y, è_mia=False):
        for riga in range(10):
            for colonna in range(10):
                x = offset_x + colonna * self.dimensione_cella
                y = offset_y + riga * self.dimensione_cella
                rect = pygame.Rect(x, y, self.dimensione_cella, self.dimensione_cella)
                pygame.draw.rect(self.schermo, self.colore_griglia, rect, 1)

                stato = griglia[riga][colonna]
                if stato == 1:
                    if è_mia:
                        pygame.draw.rect(self.schermo, self.colore_barca, rect)
                    else:
                        pygame.draw.circle(self.schermo, self.colore_colpo, rect.center, 10)
                elif stato == 2:
                    pygame.draw.circle(self.schermo, self.colore_mancato, rect.center, 10)

    def gestisci_click(self, posizione):
        x, y = posizione

        # Offset griglie
        offset_attacco_x = 50
        offset_mia_x = 450
        offset_y = 100

        # --- FASE PIAZZAMENTO ---
        if self.fase_piazzamento:
            if offset_mia_x <= x < offset_mia_x + 10 * self.dimensione_cella and \
               offset_y <= y < offset_y + 10 * self.dimensione_cella:

                colonna = (x - offset_mia_x) // self.dimensione_cella
                riga = (y - offset_y) // self.dimensione_cella

                if self.griglia_mia[riga][colonna] == 0:
                    self.griglia_mia[riga][colonna] = 1
                    self.barche_da_posizionare -= 1
                    print(f"Barca piazzata in ({colonna}, {riga})")
                    if self.barche_da_posizionare == 0:
                        self.fase_piazzamento = False
                        self.messaggio = "Barche piazzate! Attacca nella griglia a sinistra"
                else:
                    print("Già piazzata una barca lì")

        # --- FASE ATTACCO ---
        else:
            if offset_attacco_x <= x < offset_attacco_x + 10 * self.dimensione_cella and \
               offset_y <= y < offset_y + 10 * self.dimensione_cella:

                colonna = (x - offset_attacco_x) // self.dimensione_cella
                riga = (y - offset_y) // self.dimensione_cella

                if self.griglia_attacchi[riga][colonna] == 0:
                    self.griglia_attacchi[riga][colonna] = 1
                    print(f"Attacco su ({colonna}, {riga})")
                    # Qui potresti inviare la mossa al server (es: client.send_move(colonna, riga))
                    self.messaggio = f"Attacco su ({colonna}, {riga}) inviato"
                else:
                    self.messaggio = "Hai già colpito lì!"

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

            # Messaggio
            self.mostra_messaggio()

            # Disegna griglie
            self.disegna_griglia(self.griglia_attacchi, 50, 100)        # attacco (sinistra)
            self.disegna_griglia(self.griglia_mia, 450, 100, è_mia=True)  # mia griglia (destra)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

# Avvio
if __name__ == "__main__":
    gioco = InterfacciaDiGioco()
    gioco.run()
