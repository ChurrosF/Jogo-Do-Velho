import pygame
import sys  
import numpy as np

from constants import *


# PYGAME SETUP

pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('JOGO DO VELHO')


# CONSOLE BOARD

class Board:

    def __init__(self):
        self.board = np.zeros( (ROWS, COLS) )

    def mark_square(self, row, col, player):
        self.board[row][col] = player

    def isboardfull(self):
        # Return True if board full, else return False

        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == 0:
                    return False
        return True            

    def check_win(self):

        # Check if there's any win and return a win line direction

        for row in range(ROWS):
            for col in range(COLS):

                # Horizontal win
                if self.board[row][0] == self.board[row][1] == self.board[row][2] != 0:
                    return 'h'

                # Vertical win
                elif self.board[0][col] == self.board[1][col] == self.board[2][col] != 0:
                    return 'v'

                # Desc Diagonal win
                elif self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
                    return 'desc'

                # Asc Diagonal win
                elif self.board[2][0] == self.board[1][1] == self.board[0][2] != 0:
                    return 'asc'
        return False   


# GAME SETTINGS AND GRAPHIC BOARD

class Game:

    def __init__(self):
        self.player = 1
        self.gameover = False
        self.board = Board()
        self.draw_board()


    def draw_board(self):

        # BACKGROUND
        screen.fill(BG_COLOR)

        # HORIZONTAL LINES 1 and 2
        pygame.draw.line(screen, LINE_COLOR, (0, SQ_SIZE), (WIDTH, SQ_SIZE), LINE_THICKNESS)
        pygame.draw.line(screen, LINE_COLOR, (0, SQ_SIZE * 2), (WIDTH, SQ_SIZE * 2), LINE_THICKNESS)

        # VERTICAL LINES 1 and 2
        pygame.draw.line(screen, LINE_COLOR, (SQ_SIZE, 0), (SQ_SIZE, HEIGHT), LINE_THICKNESS)
        pygame.draw.line(screen, LINE_COLOR, (SQ_SIZE * 2, 0), (SQ_SIZE * 2, HEIGHT), LINE_THICKNESS)


    def draw_figs(self, row, col):
        
        # Func for drawing players figures
        cerveja_img = pygame.image.load(cerveja_path).convert_alpha()
        cigarro_img = pygame.image.load(cigarro_path).convert_alpha()

        if self.player == 1:
            screen.blit(cerveja_img, (col * SQ_SIZE, row * SQ_SIZE))
        elif self.player == 2:
            screen.blit(cigarro_img, (col * SQ_SIZE, row * SQ_SIZE))


    def draw_winline(self, row, col):
        
        taco_img = pygame.image.load(taco_path)

        # Changing the size of the winning line

        if self.board.check_win() == 'h':

            screen.blit(taco_img, (0, SQ_SIZE * row))
            
        elif self.board.check_win() == 'v':

            taco_img = pygame.transform.rotate(taco_img, 90)

            screen.blit(taco_img, (SQ_SIZE * col, 0))

        elif self.board.check_win() == 'asc':
            
            taco_img = pygame.transform.rotate(taco_img, 45)
            taco_img = pygame.transform.smoothscale(taco_img, (SQ_SIZE * 3.75, SQ_SIZE * 3.75))

            xorigin = -SQ_SIZE / 4
            yorigin = -SQ_SIZE * 0.45

            screen.blit(taco_img, (xorigin, yorigin))

        elif self.board.check_win() == 'desc':

            taco_img = pygame.transform.rotate(taco_img, -45)
            taco_img = pygame.transform.smoothscale(taco_img, (SQ_SIZE * 3.75, SQ_SIZE * 3.75))

            xorigin = -SQ_SIZE * 0.45
            yorigin = -SQ_SIZE * 0.4

            screen.blit(taco_img, (xorigin, yorigin))
 

    def next_turn(self):
        self.player = self.player % 2 + 1


    def make_move(self, row, col):

        board = self.board.board

        # Marca o tabuleiro do console, marca o quadrado clicado na tela e passa o turno
        if board[row][col] == 0:
            self.board.mark_square(row, col, self.player)
            self.draw_figs(row, col)
            self.next_turn()


# --- MAIN ---

def main():

    game = Game()

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                mx, my = pygame.mouse.get_pos()

                clk_col = mx // SQ_SIZE
                clk_row = my // SQ_SIZE


                if not game.gameover:

                    game.make_move(clk_row, clk_col)

                    if game.board.check_win():
                        game.draw_winline(clk_row, clk_col)
                        game.gameover = True

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    game.draw_board()
                    game.board.board = np.zeros( (ROWS, COLS) )
                    game.player = 1
                    game.gameover = False
                        
    
        pygame.display.update()


main()
