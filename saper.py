import numpy as np
import random as rd
import pygame as pg

def generate_board(size_x, size_y, num_mines):

    board = np.zeros((size_x, size_y), dtype=int)
    index = rd.sample(range(size_x * size_y), num_mines)
    
    for i in index:
        row, col = divmod(i, size_y) #divmod(a, b) == (a //b, a % b)#
        board[row, col] = -1
    return board

def complite_board(board):
    size = board.shape[0]
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                count = 0
                # Sprawdzamy wszystkie sąsiednie pola (8 kierunków)
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue  # pomijamy środek, czyli samo pole
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < size and 0 <= nj < size:
                            if board[ni][nj] == -1:
                                count += 1
                board[i][j] = count
    return board

pg.init()
window = pg.display.set_mode((1200,1200))

button1 = pg.Rect(200, 200, 200, 50)
button2 = pg.Rect(200, 300, 200, 50)
button3 = pg.Rect(200, 400, 200, 50)
button4 = pg.Rect(350, 500, 120, 50)
button5 = pg.Rect(120, 500, 120, 50)
back = pg.Rect(0, 0, 120, 50)
close = pg.Rect(50, 50, 120, 50)

button = {
    'menu': [button1, button2, button3, button4, button5],
    'controls': [back, close]
}

text = {
    'menu': [button1, button2, button3, button4, button5],
    'controls': [back, close]
}
FONT = pg.font.SysFont('arial', 30)


def menu():
    run = True
    hoise = None
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                choice = 'quit'
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for idx, buton in enumerate(button['menu']):
                    if buton.collidepoint(mouse_pos):
                        if idx == 0:
                            choice = 'easy'
                            run = False
                        elif idx == 1:
                            choice = 'medium'
                            run = False
                        elif idx == 2:
                            choice = 'hard'
                            run = False
                        elif idx == 3:
                            choice = 'quit'
                            run = False
                        elif idx == 4:
                            choice = 'stats'
                            run = False

        window.fill((55, 131, 224))
        for _ in button['menu']:
            pg.draw.rect(window, (179, 187, 196), _, border_radius=10)
        pg.display.update()
    return choice

def user_choice(choice):
    if choice == 'quit':
        return None, None, None
    elif choice == 'easy':
        print("Wybrano EASY")
        return 9, 9, 10
    
    elif choice == 'medium':
        print("Wybrano MEDIUM")
        return 16, 16, 40
    elif choice == 'hard':
        print("Wybrano HARD")
        return 16, 30, 99
    elif choice == 'stats':
        print("Wybrano STATS")
        return None, None, None

def game_board(x_size, y_size):
    rects = []
    board_width = x_size * 36 + 5 
    board_height = y_size * 36 + 5
    offset_x = (1200 - board_height)//2
    offset_y = (1200 - board_width)//2

    window.fill((55, 131, 224))
    base = pg.Rect(offset_x, offset_y, board_height, board_width)
    pg.draw.rect(window, (89, 94, 99), base)

    for i in range(y_size):
        for j in range(x_size):
            rect = pg.Rect(offset_x + i*36 + 5, offset_y + j*36 + 5, 32, 32)
            pg.draw.rect(window, (168, 168, 168), rect)
            rects.append((rect, i, j))
    pg.display.update()
    return rects
       
def main_game(choice):
    x_size, y_size, mines = user_choice(choice)
    rects = game_board(x_size, y_size)  # rysowanie i zapis prostokątów

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for rect, i, j in rects:
                    if rect.collidepoint(mouse_pos):
                        print(f"Kliknięto pole ({i}, {j})")
                        # logika gry

    

def main():
    run = True
    while run:
        choice = menu()
        if choice == 'quit':
            run = False
        elif choice == 'stats':
            print('in progres')
        else:
            main_game(choice)

                   
main()