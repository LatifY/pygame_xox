import pygame_widgets
import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import time as t

# pygame setup
pygame.init()

header_font = pygame.font.SysFont("arial", 30, True)
credit_font = pygame.font.SysFont("arial", 14)
tile_font = pygame.font.SysFont("arial", 60, True)


screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("oxo")
clock = pygame.time.Clock()
running = True
dt = 0

start = True

# slider = Slider(screen, 0, 0, 100, 10, min=3, max=10, step=1)
# output = TextBox(screen, 20, 30, 40, 40, fontSize=10)


def render_text(font, text, x, y):
    text = font.render(text, True, (0, 0, 0))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


class Table:
    def __init__(self):
        self.w = 3
        self.tiles = [["" for _ in range(self.w)] for _ in range(self.w)]
        self.rects = [["" for _ in range(self.w)] for _ in range(self.w)]
        self.gap = 3
        self.tile_border = int(15 / self.w)
        self.table_offset = 80
        self.turn = "X"
        self.finished = False
        self.winner = ""
        self.is_draw = False
        self.click_count = 0


    def draw(self):
        size = (screen.get_width() - (2 * self.table_offset) -
                ((self.w - 1) * self.gap)) / self.w
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles)):
                y_cord = self.table_offset + (y * size)
                x_cord = self.table_offset + (x * size)
                x_cord += self.gap * x
                y_cord += self.gap * y

                pygame.draw.rect(screen, "black", (x_cord, y_cord, size, size))
                self.rects[y][x] = pygame.draw.rect(
                    screen, "white", (x_cord + self.tile_border, y_cord + self.tile_border, size - (self.tile_border * 2), size - (self.tile_border * 2)))
                render_text(
                    pygame.font.SysFont("arial", int(size / 2.2), True), self.tiles[y][x], x_cord + size / 2, y_cord + size / 2)

    def put(self, y, x):
        if (self.tiles[y][x] != ""):
            return
        if(self.winner != "" or self.is_draw):return
        self.click_count+=1
        self.tiles[y][x] = self.turn
        self.turn = "X" if self.turn == "O" else "O"
        winner = self.check_winner()
        if(winner != None):
            self.winner = winner
        if(winner == None and self.click_count >= self.w**2):
            self.is_draw = True

    def check_winner(self):
        size = len(self.tiles)

        for row in range(size):
            for col in range(size - 2):
                if self.tiles[row][col] == self.tiles[row][col+1] == self.tiles[row][col+2] and self.tiles[row][col] != "":
                    return self.tiles[row][col]

        for col in range(size):
            for row in range(size - 2):
                if self.tiles[row][col] == self.tiles[row+1][col] == self.tiles[row+2][col] and self.tiles[row][col] != "":
                    return self.tiles[row][col]

        for row in range(size - 2):
            for col in range(size - 2):
                if self.tiles[row][col] == self.tiles[row+1][col+1] == self.tiles[row+2][col+2] and self.tiles[row][col] != "":
                    return self.tiles[row][col]

        for row in range(size - 2):
            for col in range(2, size):
                if self.tiles[row][col] == self.tiles[row+1][col-1] == self.tiles[row+2][col-2] and self.tiles[row][col] != "":
                    return self.tiles[row][col]
        return None


table = Table()

def display_menu():
    render_text(header_font, "OXO", screen.get_width() / 2, screen.get_height() / 2)
    render_text(header_font, "press 'space' to start", screen.get_width() / 2, screen.get_height() / 2 + 30)

while running:
    # poll for events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and start == False:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            for y in range(len(table.rects)):
                for x in range(len(table.rects)):
                    if (table.rects[y][x].collidepoint(mouse_pos)):
                        table.put(y, x)
                        break
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            start = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            table = Table()
    screen.fill("white")

    # output.setText(slider.getValue())

    pygame_widgets.update(events)

    if (start == False):
        header_text = table.turn
        if(table.winner != ""):
            header_text = ("'" + table.winner + "' WON!")
        elif(table.is_draw):
            header_text = "DRAW!"
        render_text(header_font, header_text, screen.get_width()/2, 30)

        
        if(table.winner != "" or table.is_draw):
            render_text(credit_font, "press 'r' to reset", screen.get_width() / 2, 60)

        table.draw()
    else:
        display_menu()

    render_text(credit_font, "made by latif",
                    screen.get_width()/2, screen.get_height() - 20)
        
    pygame.display.flip()

    dt = clock.tick(120) / 1000

pygame.quit()
