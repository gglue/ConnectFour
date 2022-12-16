import numpy as np

ROW_NUMBER = 6
COLUMN_NUMBER = 7
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

def checkWinCondition(board, r, c, player):
    """
    This function checks if a player has achieved a win condition
    :param player: The player who placed the token
    :param board: The ConnectFour board
    :param r: Row value
    :param c: Column value
    :return: Boolean variable representing if there is a win condition
    """

    # Check own value
    startingScore = 0
    if board[r,c] == player: startingScore = 1

    # Values to keep track on neighbors
    columnWin = startingScore
    rowLeftWin = startingScore
    rowRightWin = startingScore
    diagonalBLWin = startingScore
    diagonalBRWin = startingScore

    # Check for column win on the bottom only
    if (r + 3) <= ROW_NUMBER - 1:
        for neighbor in range(1,4):
            if board[r + neighbor, c] == player: columnWin += 1

    # Check for row wins for the right side
    if (c + 3) <= COLUMN_NUMBER - 1:
        for neighbor in range(1,4):
            if board[r, c + neighbor] == player: rowRightWin += 1

    # Check for row wins for the left side
    if (c - 3) >= 0:
        for neighbor in range(1,4):
            if board[r, c - neighbor] == player: rowLeftWin += 1

    # Check for diagonal win for bottom left quadrant
    if (c - 3) >= 0 and (r + 3) <= ROW_NUMBER - 1:
        for neighbor in range(1,4):
            if board[r + neighbor, c - neighbor] == player: diagonalBLWin += 1

    # Check for diagonal win for bottom right quadrant
    if (c + 3) <= COLUMN_NUMBER - 1 and (r + 3) <= ROW_NUMBER - 1:
        for neighbor in range(1,4):
            if board[r + neighbor, c + neighbor] == player: diagonalBRWin += 1

    if columnWin == 4: return 'column'
    if rowLeftWin == 4: return 'rowLeft'
    if rowRightWin == 4: return 'rowRight'
    if diagonalBLWin == 4: return 'bottomLeft'
    if diagonalBRWin == 4: return 'bottomRight'
    return None


if __name__ == '__main__':
    """
    Main function
    """
    connectFourBoard = np.zeros((6,7))

    playerTurn = True
    winCon = None
    printBoard(connectFourBoard)
    while not winCon:
        if playerTurn:
            token = 1
        else:
            token = 2
        playerInput = int(input("Enter column number"))
        dropToken(connectFourBoard, playerInput, token)
        for x in range(connectFourBoard.shape[0]):
            for y in range(connectFourBoard.shape[1]):
                winCon = checkWinCondition(connectFourBoard,x,y,token)
                if winCon:
                    print(winCon)
                    break
        playerTurn = not playerTurn
        printBoard(connectFourBoard)