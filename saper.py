import numpy as np
import random as rd

def generate_board_nad_mines(size, num_mines):

    board = np.zeros((size, size), dtype=int)
    index = rd.sample(range(size * size), num_mines)
    
    for i in index:
        row, col = divmod(i, size) #divmod(a, b) == (a //b, a % b)#
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

def main():
    board = generate_board_nad_mines(10,15)
    complit_board = complite_board(board)
    print(board)
    print()
    print(complit_board)
main()