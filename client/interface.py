import pygame
import sys
#import sys per interrompere il programma in modo pulito

class interfacciaDiGioco:
    def __init__(self):
        
        #inizializzazione pygame
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

        # gestione degli errori 
        

         
