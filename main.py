import numpy as np

def printBoard(board):
    """
    This function prints the string representation of the board
    :param board: The ConnectFour board
    :return: null
    """
    for row in board:
        first = True
        for column in row:
            if first:
                first = False
                print(f'|  {displayToken(column)}  |', end='')
            else:
                print(f'  {displayToken(column)}  |', end='')
        print("")

def dropToken(board, columnNumber, player):
    """
    This function drops a token onto the ConnectFour board
    :param board: The ConnectFour board
    :param columnNumber: The column where the token is dropped
    :param player: Which player dropped the token
    :return: The row where the token is dropped
    """
    currentRow = 5
    for row in reversed(board):
        if row[columnNumber] == 0:
            row[columnNumber] = player
            return currentRow
        else:
            currentRow -= 1

def displayToken(value):
    """
    This function returns the string representation of the given value
    :param value: The value of the column of the ConnectFour board
    :return: The string representation of the value
    """
    # Player 1
    if value == 1:
        return 'X'

    # Player 2
    elif value == 2:
        return 'O'

    # Empty
    else:
        return ' '

if __name__ == '__main__':
    """
    Main function
    """
    connectFourBoard = np.zeros((6,7))
    print(dropToken(connectFourBoard, 0, 1))
    print(dropToken(connectFourBoard, 0, 1))
    print(dropToken(connectFourBoard, 0, 1))
    print(dropToken(connectFourBoard, 0, 1))
    printBoard(connectFourBoard)
