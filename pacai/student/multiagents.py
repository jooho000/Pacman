import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core import distance

class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Useful information you can extract.
        newPosition = successorGameState.getPacmanPosition()
        oldPosition = currentGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScore = successorGameState.getScore()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***
        foods = newFood.asList()
        if len(foods) == 0:
            return 99999

        score = 1000
        
        for ghost in newGhostStates:
            isBrave = ghost.isBraveGhost()
            ghostPosition = ghost.getPosition()

            if isBrave:
                if distance.manhattan(newPosition, ghostPosition) < 2:
                    score -= 99999
        
        newFoodCount = newFood.count()
        oldFoodCount = oldFood.count()
        newFoodDistances = []
        for food in foods:
            newFoodDistances.append(1 / distance.manhattan(newPosition, food))
        score += max(newFoodDistances)

        if newPosition == oldPosition:
            score -= 1000

        if newFoodCount <= oldFoodCount:
            score += 1000
        else:
            score -= 1000
        
        return newScore + score


class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
        self.evalFunction = self.getEvaluationFunction()
    
    def getAction(self, gameState):
        result = self.getValue(gameState, 0, 0)

        return result[1]

    def getValue(self, gameState, index, depth):

        # terminal state
        if len(gameState.getLegalActions(index)) == 0 or depth == self.getTreeDepth():
            return self.evalFunction(gameState), ""
        
        # max case
        if index == 0:
            return self.maxValue(gameState, index, depth)
        
        # min case
        else:
            return self.minValue(gameState, index, depth)
    
    def maxValue(self, gameState, index, depth):
        actions = gameState.getLegalActions(index)
        actions.remove('Stop')
        maxVal = -99999
        maxAction = ""

        for action in actions:
            successor = gameState.generateSuccessor(index, action)
            successorIndex = index + 1
            successorDepth = depth

            # if pacman update depth and index
            if successorIndex + 1 >= gameState.getNumAgents():
                successorIndex = 0
                successorDepth += 1
            
            currVal = self.getValue(successor, successorIndex, successorDepth)[0]
            # currVal += self.evalFunction(successor)

            if currVal > maxVal:
                maxVal = currVal
                maxAction = action
        
        return maxVal, maxAction
    
    def minValue(self, gameState, index, depth):
        actions = gameState.getLegalActions(index)
        minVal = 99999
        minAction = ""

        for action in actions:
            successor = gameState.generateSuccessor(index, action)
            successorIndex = index + 1
            successorDepth = depth
        
        # if pacman
        if successorIndex + 1 >= gameState.getNumAgents():
            successorIndex = 0
            successorDepth += 1
        
        currVal = self.getValue(successor, successorIndex, successorDepth)[0]
        # currVal += self.evalFunction(successor)

        if currVal < minVal:
            minVal = currVal
            minAction = action
        
        return minVal, minAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
        self.evalFunction = self.getEvaluationFunction()

    def getAction(self, gameState):
        action = self.getValue(gameState, 0, 0, -99999, 99999)

        return action[1]
    
    def getValue(self, gameState, index, depth, alpha, beta):

        if len(gameState.getLegalActions(index)) == 0 or depth == self.getTreeDepth():
            return self.evalFunction(gameState), ""
        
        if index == 0:
            return self.getMax(gameState, index, depth, alpha, beta)
        else:
            return self.getMin(gameState, index, depth, alpha, beta)
    
    def getMax(self, gameState, index, depth, alpha, beta):
        actions = gameState.getLegalActions(index)
        actions.remove('Stop')
        maxVal = -99999
        maxAction = ""

        for action in actions:
            successor = gameState.generateSuccessor(index, action)
            successorIndex = index + 1
            successorDepth = depth

            # if pacman update depth and index
            if successorIndex + 1 >= gameState.getNumAgents():
                successorIndex = 0
                successorDepth += 1
            
            currVal = self.getValue(successor, successorIndex, successorDepth, alpha, beta)[0]

            if currVal > maxVal:
                maxVal = currVal
                maxAction = action
            
            alpha = max(alpha, maxVal)

            # pruning
            if maxVal > beta:
                return maxAction, maxVal
        
        return maxVal, maxAction
    
    def getMin(self, gameState, index, depth, alpha, beta):
        actions = gameState.getLegalActions(index)
        minVal = 99999
        minAction = ""

        for action in actions:
            successor = gameState.generateSuccessor(index, action)
            successorIndex = index + 1
            successorDepth = depth
        
        # if pacman
        if successorIndex + 1 >= gameState.getNumAgents():
            successorIndex = 0
            successorDepth += 1
        
        currVal = self.getValue(successor, successorIndex, successorDepth, alpha, beta)[0]

        if currVal < minVal:
            minVal = currVal
            minAction = action
        
        beta = min(beta, minVal)

        # pruning
        if minVal < alpha:
            return minVal, minAction
        
        return minVal, minAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
        self.evalFunction = self.getEvaluationFunction()

    def getAction(self, gameState):
        result = self.getValue(gameState, 0, 0)
        return result[1]
    
    def getValue(self, gameState, index, depth):

        # terminal state
        if len(gameState.getLegalActions(index)) == 0 or depth == self.getTreeDepth():
            return self.evalFunction(gameState), ""
        
        # max case
        if index == 0:
            return self.maxValue(gameState, index, depth)
        
        # chance case
        else:
            return self.expectedValue(gameState, index, depth)
    
    def maxValue(self, gameState, index, depth):
        actions = gameState.getLegalActions(index)
        actions.remove('Stop')
        maxVal = -999999
        maxAction = ""

        for action in actions:
            successor = gameState.generateSuccessor(index, action)
            successorIndex = index + 1
            successorDepth = depth

            # if pacman update depth and index
            if successorIndex == gameState.getNumAgents():
                successorIndex = 0
                successorDepth += 1
            
            currVal = self.getValue(successor, successorIndex, successorDepth)[0]
            # currVal += self.evalFunction(successor)

            if currVal > maxVal:
                maxVal = currVal
                maxAction = action
        
        return maxVal, maxAction
    
    def expectedValue(self, gameState, index, depth):
        actions = gameState.getLegalActions(index)
        expectedVal = 0
        expectedAction = ""

        for action in actions:
            successor = gameState.generateSuccessor(index, action)
            successorIndex = index + 1
            successorDepth = depth

            # if pacman update depth and index
            if successorIndex == gameState.getNumAgents():
                successorIndex = 0
                successorDepth += 1
            
            currVal = self.getValue(successor, successorIndex, successorDepth)[0]
            expectedVal += float(currVal / len(actions))
        
        return expectedVal, expectedAction


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """
    pacmanPosition = currentGameState.getPacmanPosition()
    currentFoods = currentGameState.getFood()
    currentScore = currentGameState.getScore()
    ghostStates = currentGameState.getGhostStates()
    capsulePositions = currentGameState.getCapsules()
    # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

    # goal state
    foods = currentFoods.asList()
    if len(foods) == 0:
        return 99999

    for ghost in ghostStates:
        isBrave = ghost.isBraveGhost()
        ghostPosition = ghost.getPosition()

        if isBrave:
            # run away
            if distance.manhattan(pacmanPosition, ghostPosition) < 2:
                return -99999
        else:
            # incentivizes to eat ghost if possible
            if ghostPosition == pacmanPosition:
                currentScore += 99999
    
    foodDistances = []
    for food in foods:
        foodDistances.append(distance.manhattan(pacmanPosition, food))
    # closer pacman gets to a food less points deducted form score
    currentScore -= min(foodDistances)

    currentScore -= len(capsulePositions) * 999

    return currentScore

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
