# client/game_interface.py
import pygame
import sys

class GameInterface:
    def __init__(self, client):
        pygame.init()
        self.client = client
        self.client.set_gui(self)
        self.width, self.height = 400, 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Battaglia Navale")
        self.clock = pygame.time.Clock()
        self.cell_size = 40
        self.my_grid = [[0 for _ in range(10)] for _ in range(10)]
        self.turn = False
        self.player_id = None
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.client.close()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and self.turn:
                    x, y = pygame.mouse.get_pos()
                    grid_x = x // self.cell_size
                    grid_y = y // self.cell_size
                    print(f"Clic su ({grid_x}, {grid_y})")
                    self.client.send_move(grid_x, grid_y)
                    self.turn = False

            self.screen.fill((0, 0, 128))
            self.draw_grid()
            pygame.display.flip()
            self.clock.tick(30)

    def draw_grid(self):
        for x in range(10):
            for y in range(10):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                color = (255, 255, 255)
                if self.my_grid[y][x] == 1:
                    color = (255, 0, 0)  # Hit
                pygame.draw.rect(self.screen, color, rect, 1)

    def handle_server_message(self, message):
        if message.startswith("START"):
            _, player = message.split()
            self.player_id = int(player)
            self.turn = True if self.player_id == 1 else False
            print(f"Inizio gioco! Sono Player {self.player_id}")

        elif message.startswith("MOVE"):
            _, x, y = message.split()
            x, y = int(x), int(y)
            self.my_grid[y][x] = 1
            self.turn = True  # Dopo aver ricevuto mossa avversario

        elif message == "NOT_YOUR_TURN":
            print("Non è il tuo turno!")

        elif message == "OTHER_PLAYER_LEFT":
            print("L'altro giocatore ha lasciato. Fine partita.")
            self.running = False
