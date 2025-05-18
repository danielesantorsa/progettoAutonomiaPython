import pygame
import sys

class InterfacciaDiGioco:
    def __init__(self):
        # Inizializza la libreria pygame
        pygame.init()

        # Imposta dimensioni della finestra
        self.larghezza_finestra = 800
        self.altezza_finestra = 600
        self.schermo = pygame.display.set_mode((self.larghezza_finestra, self.altezza_finestra))
        pygame.display.set_caption("Battaglia Navale")

        # Colori RGB usati per disegnare
        self.colore_sfondo = (0, 0, 64)
        self.colore_griglia = (255, 255, 255)
        self.colore_barca = (160, 160, 160)
        self.colore_colpo = (255, 0, 0)
        self.colore_mancato = (0, 255, 0)

        # Crea due griglie 10x10: una per i colpi (attacco), una per le proprie barche
        self.dimensione_cella = 30  # dimensione di ogni casella
        self.griglia_attacchi = [[0 for _ in range(10)] for _ in range(10)]  # sinistra
        self.griglia_mia = [[0 for _ in range(10)] for _ in range(10)]       # destra

        # Variabili di stato
        self.font = pygame.font.SysFont(None, 28)
        self.fase_piazzamento = True                # all'inizio si piazzano le barche
        self.barche_da_posizionare = 5              # numero di barche da piazzare
        self.messaggio = "Posiziona 5 barche nella griglia di destra"

    def disegna_griglia(self, griglia, offset_x, offset_y, è_mia=False):
        """
        Disegna una griglia 10x10 partendo da una posizione (offset_x, offset_y)
        Se è_mia=True, disegna le barche piazzate
        """
        for riga in range(10):
            for colonna in range(10):
                # Calcola le coordinate della cella da disegnare
                x = offset_x + colonna * self.dimensione_cella
                y = offset_y + riga * self.dimensione_cella

                # Crea un rettangolo per ogni cella
                rect = pygame.Rect(x, y, self.dimensione_cella, self.dimensione_cella)

                # Disegna il bordo della cella
                pygame.draw.rect(self.schermo, self.colore_griglia, rect, 1)

                # Stato della cella: 1 = barca/colpito, 2 = mancato
                stato = griglia[riga][colonna]
                if stato == 1:
                    if è_mia:
                        pygame.draw.rect(self.schermo, self.colore_barca, rect)  # barca piazzata
                    else:
                        pygame.draw.circle(self.schermo, self.colore_colpo, rect.center, 10)  # colpito
                elif stato == 2:
                    pygame.draw.circle(self.schermo, self.colore_mancato, rect.center, 10)  # mancato

    def gestisci_click(self, posizione):
        """
        Gestisce il click del mouse in base alla fase:
        - Fase piazzamento: piazza barche nella griglia di destra
        - Fase attacco: colpisce griglia di sinistra
        """
        x, y = posizione

        # Offset delle due griglie
        offset_attacco_x = 50
        offset_mia_x = 450
        offset_y = 100

        # --- FASE 1: PIAZZAMENTO BARCHE ---
        if self.fase_piazzamento:
            # Controlla se il click è nella griglia di destra
            if offset_mia_x <= x < offset_mia_x + 10 * self.dimensione_cella and \
               offset_y <= y < offset_y + 10 * self.dimensione_cella:

                colonna = (x - offset_mia_x) // self.dimensione_cella
                riga = (y - offset_y) // self.dimensione_cella

                # Se la cella è vuota, piazza una barca (1)
                if self.griglia_mia[riga][colonna] == 0:
                    self.griglia_mia[riga][colonna] = 1
                    self.barche_da_posizionare -= 1
                    print(f"Barca piazzata in ({colonna}, {riga})")

                    # Se ho finito di piazzare, passo alla fase attacco
                    if self.barche_da_posizionare == 0:
                        self.fase_piazzamento = False
                        self.messaggio = "Barche piazzate! Attacca nella griglia a sinistra"
                else:
                    print("Hai già piazzato una barca lì")

        # --- FASE 2: ATTACCO ---
        else:
            # Controlla se il click è nella griglia di sinistra
            if offset_attacco_x <= x < offset_attacco_x + 10 * self.dimensione_cella and \
               offset_y <= y < offset_y + 10 * self.dimensione_cella:

                colonna = (x - offset_attacco_x) // self.dimensione_cella
                riga = (y - offset_y) // self.dimensione_cella

                # Se la cella non è già stata colpita, registra il colpo
                if self.griglia_attacchi[riga][colonna] == 0:
                    self.griglia_attacchi[riga][colonna] = 1  # simula colpito
                    print(f"Attacco su ({colonna}, {riga})")
                    self.messaggio = f"Attacco su ({colonna}, {riga}) inviato"
                else:
                    self.messaggio = "Hai già colpito lì!"

    def mostra_messaggio(self):
        """
        Mostra un messaggio testuale sopra le griglie
        """
        testo = self.font.render(self.messaggio, True, (255, 255, 255))
        self.schermo.blit(testo, (20, 20))

    def run(self):
        """
        Ciclo principale del gioco (Pygame)
        """
        in_esecuzione = True
        while in_esecuzione:
            # Gestione eventi (es. click o chiusura finestra)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    in_esecuzione = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    self.gestisci_click(evento.pos)

            # Riempie lo sfondo
            self.schermo.fill(self.colore_sfondo)

            # Mostra messaggio in alto
            self.mostra_messaggio()

            # Disegna le due griglie
            self.disegna_griglia(self.griglia_attacchi, 50, 100)           # Griglia attacco (sinistra)
            self.disegna_griglia(self.griglia_mia, 450, 100, è_mia=True)   # Griglia mia (destra)

            # Aggiorna lo schermo
            pygame.display.flip()

        # Esce dal gioco
        pygame.quit()
        sys.exit()

# Avvia il gioco
if __name__ == "__main__":
    gioco = InterfacciaDiGioco()
    gioco.run()
