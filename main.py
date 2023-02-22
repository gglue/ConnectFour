import signal

import numpy as np
from socket import *
ROW_NUMBER = 6
COLUMN_NUMBER = 7
IP_ADDRESS = 'localhost'

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
    if columnNumber > COLUMN_NUMBER - 1:
        return None
    currentRow = ROW_NUMBER - 1
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

def checkBoard(board, player):
    """
    This function checks the entire ConnectFour board for a win condition
    :param player: The player who placed the token
    :param board: The ConnectFour board
    :return: A boolean variable representing whether a win condition was found or not
    """
    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            winCon = checkWinCondition(board, x, y, player)
            if winCon:
                return winCon

def localVersus():
    """
    This function is used when user wants to play local multiplayer
    :return: null
    """

    # Start fresh board
    connectFourBoard = np.zeros((ROW_NUMBER, COLUMN_NUMBER))
    winCon = None
    playerTurn = True

    while not winCon:
        # Change token value depending on player turn
        if playerTurn:
            token = 1
        else:
            token = 2

        printBoard(connectFourBoard)
        print(f"Player {token}'s turn")

        # Input validation to place token
        playerInput = input("Enter column number: ")
        if playerInput.isdigit() and int(playerInput) < COLUMN_NUMBER:
            dropToken(connectFourBoard, int(playerInput), token)

            # Check if opponent has won yet
            winCon = checkBoard(connectFourBoard, token)
            if winCon:
                print(f"Player {token} wins because of {winCon}")

            # Switch to other player's turn
            playerTurn = not playerTurn


def onlineVersus():

    def handler(signum, frame):
        """This function is the signal handler for a SIGINT signal"""

        print("Interrupt received, shutting down...")

        # Drop all inventory before exit
        userSocket.close()

        # Exit program
        quit()

    """
    This function is used when user wants to play multiplayer online
    :return:
    """
    # Set user address info
    userSocket = socket(AF_INET, SOCK_DGRAM)
    userPort = int(input("Please enter your desired port number: "))
    userSocket.bind((IP_ADDRESS, userPort))

    # Create a signal for interruption
    signal.signal(signal.SIGINT, handler)

    print("Are you hosting or are you connecting?")
    print("1. Connecting")
    print("2. Hosting")
    playerNumber = int(input("Select your answer (#): "))

    # Player 1 goes second
    if playerNumber == 1:
        opponentPort = int(input("Please enter opponent's port number: "))
        userSocket.sendto("Connected".encode(), (IP_ADDRESS, opponentPort))

        # Start fresh board
        connectFourBoard = np.zeros((ROW_NUMBER, COLUMN_NUMBER))
        winCon = None
        printBoard(connectFourBoard)

        while not winCon:
            # Get opponent's input
            print(f"Opponent's turn, please wait")
            message, clientAddress = userSocket.recvfrom(2048)
            userMessage = message.decode()
            dropToken(connectFourBoard, int(userMessage), 2)

            # Check if opponent has won yet
            printBoard(connectFourBoard)
            winCon = checkBoard(connectFourBoard, 2)
            if winCon:
                print(f"Player 2 wins because of {winCon}")
                break

            # If opponent has not won, let player play his turn
            else:
                # Input validation to place token
                while True:
                    playerInput = (input("It's your turn; Enter column number: "))
                    if playerInput.isdigit() and int(playerInput) < COLUMN_NUMBER:
                        break

                # Drop token and send input to opponent
                dropToken(connectFourBoard, int(playerInput), 1)
                printBoard(connectFourBoard)
                userSocket.sendto(playerInput.encode(), (IP_ADDRESS, opponentPort))

                # Check for win condition
                winCon = checkBoard(connectFourBoard, 1)
                if winCon:
                    print(f"Player 1 wins because of {winCon}")
                    break

    # Player 2 goes first
    else:
        # Gets opponent's ip address and port for future communication
        print(f"You are hosting on {userSocket.getsockname()}")
        message, clientAddress = userSocket.recvfrom(2048)
        opponentPort = clientAddress[1]
        userMessage = message.decode()

        if "Connected" in userMessage:

            # Start fresh board
            connectFourBoard = np.zeros((ROW_NUMBER, COLUMN_NUMBER))
            winCon = None
            printBoard(connectFourBoard)

            while not winCon:
                # Input validation to place token
                while True:
                    playerInput = (input("It's your turn; Enter column number: "))
                    if playerInput.isdigit() and int(playerInput) < COLUMN_NUMBER:
                        break

                # Drop token and send input to opponent
                dropToken(connectFourBoard, int(playerInput), 2)
                printBoard(connectFourBoard)
                userSocket.sendto(playerInput.encode(), (IP_ADDRESS, opponentPort))

                # Check for win condition
                winCon = checkBoard(connectFourBoard, 2)
                if winCon:
                    print(f"Player 2 wins because of {winCon}")
                    break

                # If no win condition, it's the opponent's turn
                else:
                    # Get opponent's input
                    print(f"Opponent's turn, please wait")
                    message, clientAddress = userSocket.recvfrom(2048)
                    userMessage = message.decode()
                    dropToken(connectFourBoard, int(userMessage), 1)

                    # Check if opponent has won yet
                    printBoard(connectFourBoard)
                    winCon = checkBoard(connectFourBoard, 1)
                    if winCon:
                        print(f"Player 1 wins because of {winCon}")
                        break

if __name__ == '__main__':
    """
    Main function
    """
    onlineVersus()