# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newCapsule = successorGameState.getCapsules()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]
        score = successorGameState.getScore()
        result = 0
        nearest_food_manhattan_distance = 10000
        nearest_food_manhattan_distance_factor = 1
        min_of_ghost_manhattan_distance = 10000
        min_of_ghost_manhattan_distance_factor = 0.5
        nearest_capsule_manhattan_distance = 10000
        nearest_capsule_manhattan_distance_factor = 3

        for i in range(len(newGhostStates)):
            ghost_manhattan_distance = manhattanDistance(
                newPos, newGhostStates[i].getPosition())
            if ghost_manhattan_distance < min_of_ghost_manhattan_distance:
                min_of_ghost_manhattan = ghost_manhattan_distance
        for i in range(len(newFood)):
            if nearest_food_manhattan_distance > manhattanDistance(newPos, newFood[i]):
                nearest_food_manhattan_distance = manhattanDistance(newPos, newFood[i])
        for i in range(len(newCapsule)):
            if nearest_capsule_manhattan_distance > manhattanDistance(newPos, newCapsule[i]):
                nearest_capsule_manhattan_distance = manhattanDistance(newPos, newCapsule[i])
        # print(nearest_food_manhattan_distance)
        # print(sum_of_ghost_manhattan_distance)
        # print(score)
        # if nearest_food_manhattan_distance < 2:
        #     nearest_food_manhattan_distance_factor *= 2
        # if nearest_capsule_manhattan_distance < 2:
        #     nearest_capsule_manhattan_distance_factor *= 2
        # if len(newFood) == 1:
        #     nearest_food_manhattan_distance_factor *= 3
        if nearest_food_manhattan_distance != 10000:
            result -= nearest_food_manhattan_distance_factor * nearest_food_manhattan_distance
        if nearest_capsule_manhattan_distance != 10000:
            result -= nearest_capsule_manhattan_distance_factor * nearest_capsule_manhattan_distance
        if min_of_ghost_manhattan_distance != 10000:
            result += min_of_ghost_manhattan_distance_factor * min_of_ghost_manhattan_distance
        # result = min_of_ghost_manhattan_distance*min_of_ghost_manhattan_distance_factor / (nearest_food_manhattan_distance_factor * nearest_food_manhattan_distance)
        # return result
        score_factor = 1
        # result += nearest_capsule_manhattan_distance_factor * nearest_food_manhattan_distance
        # result = nearest_food_manhattan_distance_factor * nearest_food_manhattan_distance + \
        #     sum_of_ghost_manhattan_distance_factor * sum_of_ghost_manhattan_distance
        result += score * score_factor
        if action == "Stop":
            result -= 100
        if min_of_ghost_manhattan_distance < 2:
            result -= 100000
        return result
        # return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.nodesCount = 0


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def max_value(self, gameState, depth):
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), -1
        v = -100000
        helper = v
        for action in gameState.getLegalActions(0):
            self.nodesCount += 1
            v = max(v, self.min_value(gameState.generateSuccessor(0, action), depth, 1))
            if v > helper:
                helper = v
                current_action = action
        return v, current_action
    def min_value(self, gameState, depth, agentIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        v = 100000
        for action in gameState.getLegalActions(agentIndex):
            self.nodesCount += 1
            if agentIndex == gameState.getNumAgents() - 1:
                v = min(v, self.max_value(gameState.generateSuccessor(agentIndex, action), depth + 1)[0])
            else:
                v = min(v, self.min_value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1))
        return v
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        with open('MinimaxAgent.txt', 'a') as f:
            f.write(f"\n {self.nodesCount}")
        maxx = self.max_value(gameState, 0)
        return maxx[1]
        # for action in gameState.getLegalActions(0):
        #     if maxx == self.min_value(gameState.generateSuccessor(0, action), 0, 1):
        #         return action
        # for i in range(len(gameState.getNumAgents())):
            
        # "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def max_value(self, gameState, depth, beta=1000000, alpha=-1000000):
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), -1
        v = -100000
        helper = v
        current_action = "Stop"
        for action in gameState.getLegalActions(0):
            self.nodesCount += 1
            v = max(v, self.min_value(gameState.generateSuccessor(0, action), depth, 1, alpha, beta))
            if v > helper:
                helper = v
                current_action = action
            if v > beta:
                return v, current_action
            alpha = max(alpha, v)
        return v, current_action
    def min_value(self, gameState, depth, agentIndex, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        v = 100000
        for action in gameState.getLegalActions(agentIndex):
            self.nodesCount += 1
            if agentIndex == gameState.getNumAgents() - 1:
                v = min(v, self.max_value(gameState.generateSuccessor(agentIndex, action), depth + 1, beta, alpha)[0])
            else:
                v = min(v, self.min_value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta))
            if v < alpha:
                return v
            beta = min(beta, v)
        return v
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        with open('AlphaBetaAgent.txt', 'a') as f:
            f.write(f"\n {self.nodesCount}")
        maxx = self.max_value(gameState, 0)
        return maxx[1]
        # "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def max_value(self, gameState, depth):
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), -1
        v = -100000
        helper = v
        for action in gameState.getLegalActions(0):
            self.nodesCount += 1
            v = max(v, self.min_value(gameState.generateSuccessor(0, action), depth, 1))
            if v > helper:
                helper = v
                current_action = action
        return v, current_action
    def min_value(self, gameState, depth, agentIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        v = 100000
        for action in gameState.getLegalActions(agentIndex):
            self.nodesCount += 1
            if agentIndex == gameState.getNumAgents() - 1:
                v += self.max_value(gameState.generateSuccessor(agentIndex, action), depth + 1)[0]
            else:
                v += self.min_value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
        return v / gameState.getNumAgents()

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        maxx = self.max_value(gameState, 0)
        return maxx[1]
        # "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
