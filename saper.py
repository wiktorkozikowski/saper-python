import numpy as np
import random as rd
import pygame as pg

pg.init()
window = pg.display.set_mode((1200,1200))

def generate_board(size_x, size_y, x_click, y_click, num_mines):
    board = np.zeros((size_x, size_y), dtype=int)
    all_indices = set(range(size_x * size_y))

    forbidden = set()
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            ni, nj = x_click + dx, y_click + dy
            if 0 <= ni < size_x and 0 <= nj < size_y:
                forbidden.add(ni * size_y + nj)

    available_indices = list(all_indices - forbidden)
    index = rd.sample(available_indices, num_mines)

    for i in index:
        row, col = divmod(i, size_y)
        board[row, col] = -1

    for i in range(size_x):
        for j in range(size_y):
            if board[i][j] == 0:
                count = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < size_x and 0 <= nj < size_y:
                            if board[ni][nj] == -1:
                                count += 1
                board[i][j] = count

    return board

def menu():
    button1 = pg.Rect(450, 350, 200, 50)
    button2 = pg.Rect(450, 450, 200, 50)
    button3 = pg.Rect(450, 550, 200, 50)
    button4 = pg.Rect(600, 650, 120, 50)
    button5 = pg.Rect(370, 650, 120, 50)
    back = pg.Rect(0, 0, 120, 50)
    close = pg.Rect(50, 50, 120, 50)

    button = {
        'menu': [button1, button2, button3, button4, button5],
        'controls': [back, close]
    }
    
    font = pg.font.SysFont('arial', 32)
    
    text = {
        'menu': ['Easy', 'Midium', 'Hard', 'Quit', 'Stats'],
        'controls': ['back', 'close']}

    run = True
    choice = None
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

        for idx, rect in enumerate(button['menu']):

            pg.draw.rect(window, (179, 187, 196), rect, border_radius=10)
            text_surf = font.render(text['menu'][idx], True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=rect.center)
            window.blit(text_surf, text_rect)

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

def game_board(x_size, y_size, revealed_index, board = None):
    rects = []
    cell_size = 36
    color = {'1':[32, 149, 247],'2':[48, 156, 23], '3':[204, 158, 31], '4':[120, 31, 204], '5':[122, 65, 1], '6':[212, 3, 166], '7':[255, 117, 11], '8':[153, 0, 0], }

    board_width = y_size * cell_size + 5  
    board_height = x_size * cell_size + 5   

    offset_x = (1200 - board_width) // 2
    offset_y = (1200 - board_height) // 2

    window.fill((55, 131, 224))

    base = pg.Rect(offset_x - 20, offset_y - 180, board_width + 40, board_height + 200,)
    pg.draw.rect(window, (171, 171, 171), base, border_radius=10)

    base2 = pg.Rect(offset_x, offset_y, board_width, board_height)
    pg.draw.rect(window, (89, 94, 99), base2)

    for i in range(x_size + 1):
        y = offset_y + i * cell_size + 3
        pg.draw.line(window, (0, 0, 0), (offset_x + 5, y), (offset_x + board_width - 5, y), 1)

    for j in range(y_size + 1):
        x = offset_x + j * cell_size + 3
        pg.draw.line(window, (0, 0, 0), (x, offset_y + 5), (x, offset_y + board_height - 5), 1)

    revealed_bool = np.zeros((x_size, y_size), dtype=bool)
    for item in revealed_index:
        if isinstance(item, (list, tuple)) and len(item) == 2:
            revealed_bool[item[0], item[1]] = True

    for i in range(x_size):
        for j in range(y_size):
            if not revealed_bool[i, j]:
                rect = pg.Rect(offset_x + j * cell_size + 5, offset_y + i * cell_size + 5, 32, 32)
                pg.draw.rect(window, (168, 168, 168), rect)
                rects.append((rect, i, j))
            else:
                rect = pg.Rect(offset_x + j * cell_size + 5, offset_y + i * cell_size + 5, 32, 32)
                pg.draw.rect(window, (220, 220, 220), rect)
                rects.append((rect, i, j))

                if board is not None and board[i, j] > 0:
                    num = str(board[i, j])
                    font = pg.font.SysFont('arial', 24)

                    num_color = color.get(num, (0, 0, 0))
                    text_surface = font.render(num, True, num_color)
                    window.blit(text_surface, (rect.x + 7, rect.y + 4))

    pg.display.update()
    return rects

def main_game(choice):
    x_size, y_size, mines = user_choice(choice)
    rev = []
    rects = game_board(x_size, y_size, rev)  
    board_drawn = False
    board = None

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for rect, i, j in rects:
                    if rect.collidepoint(mouse_pos) and not board_drawn:
                        board = generate_board(x_size, y_size, i, j, mines)
                        board_drawn = True
                        print(f"Kliknięto pole ({i}, {j})")
                        print(f"wygenerowano plansze:\n{board}")
                        rev += revealed_map(i, j, board)
                        rects = game_board(x_size, y_size, rev, board)

                    elif rect.collidepoint(mouse_pos):
                        if board[i, j] == -1:
                            print("przegrałeś")
                        elif board[i, j] == 0:
                            print(f"kliknięto w {board[i, j]}")
                            rev += revealed_map(i, j, board)
                            rects = game_board(x_size, y_size, rev, board)
                            print(rev)
                        else:
                            print(f"kliknięto w {board[i, j]}")
                            rev.append([i, j])
                            rects = game_board(x_size, y_size, rev, board)
                            print(rev)

def revealed_map(x_click, y_click, Arr):
    revealed_index = []
    queue = []
    main_point = [x_click, y_click]
    revealed_index.append(main_point)
    queue.append(main_point)

    while queue:
        current = queue.pop(0)
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                neighbor = [current[0] + x, current[1] + y]
                if 0 <= neighbor[0] < Arr.shape[0] and 0 <= neighbor[1] < Arr.shape[1]:
                    if Arr[neighbor[0], neighbor[1]] == 0 and neighbor not in revealed_index:
                        revealed_index.append(neighbor)
                        queue.append(neighbor)
                    elif Arr[neighbor[0], neighbor[1]] > 0 and neighbor not in revealed_index:
                        revealed_index.append(neighbor)

    return revealed_index

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