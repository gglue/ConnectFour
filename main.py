import math
import signal
import random
import numpy as np
from socket import *
ROW_NUMBER = 6
COLUMN_NUMBER = 7
IP_ADDRESS = 'localhost'
CPU_DEPTH = 5

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
        if playerInput.isdigit() and int(playerInput) < COLUMN_NUMBER and connectFourBoard[0][int(playerInput)] == 0:
            dropToken(connectFourBoard, int(playerInput), token)

            # Check if opponent has won yet
            winCon = checkBoard(connectFourBoard, token)
            if winCon:
                print(f"Player {token} wins because of {winCon}")

            # Switch to other player's turn
            playerTurn = not playerTurn

def onlineVersus():
    """
    This function is used when user wants to play online multiplayer
    :return: null
    """
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
                    if playerInput.isdigit() and int(playerInput) < COLUMN_NUMBER and connectFourBoard[0][int(playerInput)] == 0:
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
                    if playerInput.isdigit() and int(playerInput) < COLUMN_NUMBER and connectFourBoard[0][int(playerInput)] == 0:
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

def aiVersus():
    """
    This function is used when the player wants to versus the minimax AI
    :return: null
    """

    def checkScore(section, token):
        """
        Calculates the heuristic score of a section of the board by counting the number of player pieces
        :param section: List containing four consecutive positions in the ConnectFour grid
        :param token: The token value you're determining the score for
        :return: The heuristic score
        """

        score = 0
        opponentToken = 1
        if token == 1: opponentToken = 2

        # Add score if move will benefit the current player
        if section.count(token) == 4: score += 100
        elif section.count(token) == 3 and section.count(0) == 1: score += 5
        elif section.count(token) == 2 and section.count(0) == 2: score += 2

        # Subtract score if move will harm the current player
        if section.count(opponentToken) == 3 and section.count(0) == 1: score -= 4

        # Return score
        return score

    def scorePosition(board, token):
        """
        Calculates the heuristic score of the entire board
        :param board: The ConnectFour board
        :param token: The token value you're determining the score for
        :return: The total score of the board
        """

        score = 0

        # Add score for center column
        center = [int(x) for x in list(board[:, COLUMN_NUMBER // 2])]
        centerCount = center.count(token)
        score += centerCount * 3

        # Add score for horizontal sections
        for r in range(ROW_NUMBER):
            horizontal = [int(i) for i in list(board[r, :])]
            for c in range(COLUMN_NUMBER - 3):
                section = horizontal[c:c + 4]
                score += checkScore(section, token)

        # Add score for vertical sections
        for c in range(COLUMN_NUMBER):
            column = [int(i) for i in list(board[:, c])]
            for r in range(ROW_NUMBER - 3):
                section = column[r:r + 4]
                score += checkScore(section, token)

        # Add score for right diagonal
        for r in range(ROW_NUMBER - 3):
            for c in range(COLUMN_NUMBER - 3):
                section = [board[r + i][c + i] for i in range(4)]
                score += checkScore(section, token)

        # Add scope for left diagonal
        for r in range(ROW_NUMBER - 3):
            for c in range(COLUMN_NUMBER - 3):
                section = [board[r + 3 - i][c + i] for i in range(4)]
                score += checkScore(section, token)

        # Return total score
        return score

    def getOpenColumns(board):
        """
        Return an array of open columns
        :param board: TheConnectFour board
        :return: An array of open columns
        """
        openColumns = []
        for column in range(COLUMN_NUMBER):
            if board[0][column] == 0: openColumns.append(column)
        return openColumns

    def isTerminal(board):
        """
        Check if current node is a terminal node
        :param board: The ConnectFour board
        :return: A boolean representing if node is terminal
        """
        if checkBoard(board, 1) or checkBoard(board, 2) or len(getOpenColumns(board)) == 0: return True
        else: return False

    def minimax(board, depth, alpha, beta, maximizingPlayer):
        """
        The minimax algorithm used to determine the optimal move for the CPU
        :param board: The ConnectFour board
        :param depth: The maximum depth
        :param alpha: Highest value (infinity)
        :param beta: Lowest value (-infinity)
        :param maximizingPlayer: Start as maximizer or minimizer
        :return: A tuple representing the optimal move and its score value
        """
        # Get remaining open columns
        validLoc = getOpenColumns(board)

        # Return if at terminal node
        isTerm = isTerminal(board)
        if depth == 0 or isTerm:
            if isTerm:
                if checkBoard(board, 2):
                    return None, 100000000000000
                elif checkBoard(board, 1):
                    return None, -10000000000000
                else:  # Game is over, no more valid moves
                    return None, 0
            else:  # Depth is zero
                return None, scorePosition(board, 2)

        # Maximizing player
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(validLoc)

            # Only check for actual playable columns to improve performance
            for col in validLoc:
                boardCopy = board.copy()
                dropToken(boardCopy, col, 2)
                new_score = minimax(boardCopy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        # Minimizing player
        else:
            value = math.inf
            column = random.choice(validLoc)

            # Only check for actual playable columns to improve performance
            for col in validLoc:
                boardCopy = board.copy()
                dropToken(boardCopy, col, 1)
                new_score = minimax(boardCopy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    # Start fresh board
    connectFourBoard = np.zeros((ROW_NUMBER, COLUMN_NUMBER))
    winCon = None
    playerTurn = True

    while not winCon:

        printBoard(connectFourBoard)

        # Player's turn
        if playerTurn:
            print(f"Player's turn")
            # Input validation to place token
            playerInput = input("Enter column number: ")
            if playerInput.isdigit() and int(playerInput) < COLUMN_NUMBER and connectFourBoard[0][int(playerInput)] == 0:
                dropToken(connectFourBoard, int(playerInput), 1)

                # Check if win condition has been met yet
                winCon = checkBoard(connectFourBoard, 1)
                if winCon:
                    printBoard(connectFourBoard)
                    print(f"Player wins because of {winCon}")

        # CPU's turn
        else:
            print(f"Opponent's turn")
            # Use minimax algorithm
            col, minimax_score = minimax(connectFourBoard, CPU_DEPTH, -math.inf, math.inf, True)
            if connectFourBoard[0][col] == 0:
                dropToken(connectFourBoard, col, 2)

                # Check if win condition has been met yet
                winCon = checkBoard(connectFourBoard, 2)
                if winCon:
                    printBoard(connectFourBoard)
                    print(f"CPU wins because of {winCon}")

        # Switch to other player's turn
        playerTurn = not playerTurn

if __name__ == '__main__':
    """
    Main function
    """
    print("Welcome to ConnectFour, please select your mode...\n"
          "1) CPU Opponent\n"
          "2) Local Multiplayer\n"
          "3) Online multiplayer\n")
    choice = int(input("Select the number: "))
    if choice == 1:   aiVersus()
    elif choice == 2: localVersus()
    elif choice == 3: onlineVersus()
    else:             print("Bad selection, exiting.")
    """
    match choice:
        case 1:
            aiVersus()
        case 2:
            localVersus()
        case 3:
            onlineVersus()
        case _:
            print("Bad selection, exiting.")
    """