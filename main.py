import sys
import pygame
import numpy as np
import random
import copy

# Game Constants
width, height = 600, 600
background_colour = (247, 243, 234)
rows, columns = 3, 3
square_size = width // columns
line_colour, line_width = (82, 82, 75), 15
offset = 50
x_colour, x_width = (0, 210, 210), 20
o_colour, o_width, radius = (255, 32, 143), 15, square_size // 4
win_color, message_color = (248, 254, 18), (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("TIC TAC TOE")

class Board:
    def __init__(self):
        self.squares = np.zeros((rows, columns))
        self.marked_slots = 0

    def final_state(self):
        for i in range(rows):
            if self.squares[i][0] == self.squares[i][1] == self.squares[i][2] != 0:
                return self.squares[i][0]
        for j in range(columns):
            if self.squares[0][j] == self.squares[1][j] == self.squares[2][j] != 0:
                return self.squares[0][j]
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]
        if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0:
            return self.squares[1][1]
        return 0

    def marking_square(self, row, column, player):
        self.squares[row][column] = player
        self.marked_slots += 1

    def empty_square(self, row, column):
        return self.squares[row][column] == 0

    def get_empty_squares(self):
        return [(i, j) for i in range(rows) for j in range(columns) if self.empty_square(i, j)]

    def checking_full(self):
        return self.marked_slots == 9

class AI:
    def __init__(self, level=1, player=2):
        self.level, self.player = level, player

    @staticmethod
    def random(board):
        return random.choice(board.get_empty_squares())

    def minimax(self, board, maximizing):
        case = board.final_state()
        if case == 1: return 1, None
        if case == 2: return -1, None
        if board.checking_full(): return 0, None

        if maximizing:
            max_eval, best_move = -100, None
            for (row, col) in board.get_empty_squares():
                temp_board = copy.deepcopy(board)
                temp_board.marking_square(row, col, 1)
                evaluation = self.minimax(temp_board, False)[0]
                if evaluation > max_eval:
                    max_eval, best_move = evaluation, (row, col)
            return max_eval, best_move
        else:
            min_eval, best_move = 100, None
            for (row, col) in board.get_empty_squares():
                temp_board = copy.deepcopy(board)
                temp_board.marking_square(row, col, self.player)
                evaluation = self.minimax(temp_board, True)[0]
                if evaluation < min_eval:
                    min_eval, best_move = evaluation, (row, col)
            return min_eval, best_move

    def evaluation(self, board):
        return self.random(board) if self.level == 0 else self.minimax(board, False)[1]

class Game:
    def __init__(self):
        self.board, self.player = Board(), 1
        self.running, self.game_mode = True, 'ai'
        self.ai = AI(level=1, player=2)
        self.show_lines()

    def show_lines(self):
        screen.fill(background_colour)
        for i in range(1, columns):
            pygame.draw.line(screen, line_colour, (i * square_size, 0), (i * square_size, height), line_width)
        for i in range(1, rows):
            pygame.draw.line(screen, line_colour, (0, i * square_size), (width, i * square_size), line_width)

    def draw_figure(self, row, column):
        if self.player == 1:
            pygame.draw.line(screen, x_colour, (column * square_size + offset, row * square_size + offset),
                             (column * square_size + square_size - offset, row * square_size + square_size - offset), x_width)
            pygame.draw.line(screen, x_colour, (column * square_size + offset, row * square_size + square_size - offset),
                             (column * square_size + square_size - offset, row * square_size + offset), x_width)
        else:
            pygame.draw.circle(screen, o_colour, (column * square_size + square_size // 2, row * square_size + square_size // 2),
                               radius, o_width)

    def game_over(self):
        winner = self.board.final_state()
        if winner or self.board.checking_full():
            display_winner(winner)
            pygame.time.delay(2000)
            self.reset()

    def reset(self):
        self.__init__()

    def make_move(self, row, column):
        if self.board.empty_square(row, column) and self.running:
            self.board.marking_square(row, column, self.player)
            self.draw_figure(row, column)
            self.game_over()
            self.player = 3 - self.player

    def ai_move(self):
        if self.player == 2 and self.running:
            row, column = self.ai.evaluation(self.board)
            self.make_move(row, column)

def display_winner(winner):
    font = pygame.font.Font(None, 60)
    text = font.render("Player X wins!" if winner == 1 else "Player O wins!" if winner == 2 else "Draw!", True, message_color)
    screen.blit(text, text.get_rect(center=(width // 2, height // 2)))
    pygame.display.update()

def main():
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.make_move(event.pos[1] // square_size, event.pos[0] // square_size)
            if game.game_mode == 'ai' and game.player == 2:
                game.ai_move()
        pygame.display.update()

if __name__ == "__main__":
    main()
