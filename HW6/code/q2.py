from random import choice
import os
import copy
import random
import math
player, opponent = 'X', 'O'
num_of_iterations = 10000
C = 10000

class GameState:
    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.val = 0
        self.vis = 0
        self.parent = None
        self.children = []
    def __hash__(self):
        return hash(str(self.board))
    def __eq__(self, other):
        if other is None:
            return False
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != other.board[i][j]:
                    return False
        return True

    def get_uct(self):
        if self.vis == 0:
            return float('inf')
        return self.val/self.vis + C * (math.log(self.parent.vis)/self.vis)**0.5
    

def isMovesLeft(board):
    return ('_' in board[0] or '_' in board[1] or '_' in board[2])


def checkWin(board):
    for row in range(3):
        if (board[row][0] == board[row][1] and board[row][1] == board[row][2] and not board[row][0] == '_'):
            return True
    for col in range(3):
        if (board[0][col] == board[1][col] and board[1][col] == board[2][col] and not board[0][col] == '_'):
            return True

    if (board[0][0] == board[1][1] and board[1][1] == board[2][2] and not board[0][0] == '_'):
        return True

    if (board[0][2] == board[1][1] and board[1][1] == board[2][0] and not board[0][2] == '_'):
        return True

    return False

def get_children(gameState):
    children = get_empty_house(gameState.board)
    result = []
    for idx in children:
        childBoard = copy.deepcopy(gameState.board)
        turn = 'X' if gameState.player=='O' else 'X'
        childBoard.board[idx//3, idx%3] = turn
        result.append(gameState(childBoard))
    return result

def makeChildren(gameStateList, root_state):
    ch_indexes = get_empty_house(root_state.board)
    for idx in ch_indexes:
        childBoard = copy.deepcopy(root_state.board)
        turn = 'O' if root_state.player=='X' else 'X'
        childBoard[idx//3][idx % 3] = turn
        gs = GameState(childBoard, turn)
        gs.parent = root_state
        gameStateList.append(gs)
        root_state.children.append(gs)


def selection_process(gameStateList, root_state):
    if len(root_state.children) == 0:
        makeChildren(gameStateList, root_state)
    if len(root_state.children) == 0:
        return root_state
    best = get_best_uct_based(root_state)
    if best.vis == 0:
        return best
    return selection_process(gameStateList, best)

def get_difference(next_move, root_state):
    for i in range(3):
        for j in range(3):
            if next_move.board[i][j] != root_state.board[i][j]:
                return [i, j]


def findBestMove2(board):
    root_state = GameState(board, 'X')
    gameStateList = []
    makeChildren(gameStateList, root_state)
    for i in range(num_of_iterations):
        best = selection_process(gameStateList, root_state)
        simulate(best)
    next_move = get_best_uct_based(root_state)
    return get_difference(next_move, root_state)

def findBestMove(board):
    root_state = GameState(board, 'X')
    gameStateList = []
    makeChildren(gameStateList, root_state)
    num_of_experiments = num_of_iterations//len(root_state.children)
    for child in root_state.children:
        for i in range(num_of_experiments):
            simulate(child)
    next_move = get_best2(root_state.children)
    return get_difference(next_move, root_state)

def get_best2(gameStateList):
    return max(gameStateList, key=lambda x: x.val)


def get_best_uct_based(gameState):
    return max(gameState.children, key=lambda x: x.get_uct())
    # rand_state = random.choices(gameState.children, weights=[gs.get_uct() for gs in gameState.children], k=1)
    # return rand_state[0]   

def simulate(gameState):
    currentState = gameState
    while(isMovesLeft(currentState.board)):
        if(checkWin(currentState.board)):
            winner = checkWhoWin(currentState.board)
            backpropagate(gameState, winner)
            return
        else:
            turn = 'O' if currentState.player == 'X' else 'X'
            empty_spots = get_empty_house(currentState.board)
            idx = random.choice(empty_spots)
            nextBoard = copy.deepcopy(currentState.board)
            nextBoard[idx // 3][idx % 3] = turn
            currentState = GameState(nextBoard, turn)
    backpropagate(gameState, 'T')

def backpropagate(gameState, winner):
    while gameState != None:
        gameState.vis += 1
        if winner == 'O':
            gameState.val += 1
        elif winner == 'X':
            gameState.val -= 1
        gameState = gameState.parent

def checkWhoWin(board):
    for row in range(3):
        if (board[row][0] == board[row][1] and board[row][1] == board[row][2] and not board[row][0] == '_'):
            return board[row][0]
    for col in range(3):
        if (board[0][col] == board[1][col] and board[1][col] == board[2][col] and not board[0][col] == '_'):
            return board[0][col]

    if (board[0][0] == board[1][1] and board[1][1] == board[2][2] and not board[0][0] == '_'):
        return board[0][0]

    if (board[0][2] == board[1][1] and board[1][1] == board[2][0] and not board[0][2] == '_'):
        return board[0][2]

    return False



def get_empty_house(board):
    empty_spots = [i*3+j for i in range(3)
                   for j in range(3) if board[i][j] == "_"]
    return empty_spots

def findRandom(board):
    empty_spots = [i*3+j for i in range(3)
                   for j in range(3) if board[i][j] == "_"]
    idx = choice(empty_spots)
    return[int(idx/3), idx % 3]


def printBoard(board):
    os.system('cls||clear')
    print("\n Player : X , Agent: O \n")
    for i in range(3):
        print(" ", end=" ")
        for j in range(3):
            if(board[i][j] == '_'):
                print(f"[{i*3+j+1}]", end=" ")
            else:
                print(f" {board[i][j]} ", end=" ")

        print()
    print()


if __name__ == "__main__":
    board = [
            ['_', '_', '_'],
            ['_', '_', '_'],
            ['_', '_', '_']
    ]

    turn = 0

    while isMovesLeft(board) and not checkWin(board):
        if(turn == 0):
            printBoard(board)
            print(" Select Your Move :", end=" ")
            tmp = int(input())-1
            userMove = [int(tmp/3),  tmp % 3]
            while((userMove[0] < 0 or userMove[0] > 2) or (userMove[1] < 0 or userMove[1] > 2) or board[userMove[0]][userMove[1]] != "_"):
                print('\n \x1b[0;33;91m' + ' Invalid move ' + '\x1b[0m \n')
                print("Select Your Move :", end=" ")
                tmp = int(input())-1
                userMove = [int(tmp/3),  tmp % 3]
            board[userMove[0]][userMove[1]] = player
            print("Player Move:")
            printBoard(board)
            turn = 1
        else:
            bestMove = findBestMove(board)
            board[bestMove[0]][bestMove[1]] = opponent
            print("Agent Move:")
            printBoard(board)
            turn = 0

    if(checkWin(board)):
        if(turn == 1):
            print('\n \x1b[6;30;42m' + ' Player Wins! ' + '\x1b[0m')

        else:
            print('\n \x1b[6;30;42m' + ' Agent Wins! ' + '\x1b[0m')
    else:
        print('\n \x1b[0;33;96m' + ' Draw! ' + '\x1b[0m')

    input('\n Press Enter to Exit... \n')
