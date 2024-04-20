"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""
from pacai.util.priorityQueue import PriorityQueue

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    """
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    print(problem.getVisitHistory())
    """
    myStack = []
    visited = []

    if problem.isGoal(problem.startingState()):
        return []

    myStack.append((problem.startingState(), []))

    while True:

        if len(myStack) == 0:
            return []

        coordinates, path = myStack.pop()
        if coordinates not in visited:

            visited.append(coordinates)
            
            if problem.isGoal(coordinates):
                return path
            else:
                successors = problem.successorStates(coordinates)
                for state in successors:
                    temp = path.copy()
                    temp.append(state[1])
                    myStack.append((state[0], temp))


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    myQueue = []
    visited = []

    if problem.isGoal(problem.startingState()):
        return []

    myQueue.append((problem.startingState(), []))

    while True:

        if len(myQueue) == 0:
            return []

        coordinates, path = myQueue.pop(0)
        if coordinates not in visited:

            visited.append(coordinates)
            
            if problem.isGoal(coordinates):
                return path
            else:
                successors = problem.successorStates(coordinates)
                for state in successors:
                    temp = path.copy()
                    temp.append(state[1])
                    myQueue.append((state[0], temp))


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    myPrioQueue = PriorityQueue()
    visited = []

    if problem.isGoal(problem.startingState()):
        return []

    myPrioQueue.push((problem.startingState(), [], 0), 0)

    while not myPrioQueue.isEmpty():

        coordinates, path, cost = myPrioQueue.pop()
        if coordinates not in visited:

            visited.append(coordinates)
            
            if problem.isGoal(coordinates):
                return path
            else:
                successors = problem.successorStates(coordinates)
                for state in successors:
                    newPath = path.copy()
                    newPath.append(state[1])
                    newCost = cost + state[2]
                    myPrioQueue.push((state[0], newPath, newCost), newCost)
    
    return []

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    myPrioQueue = PriorityQueue()
    visited = []

    if problem.isGoal(problem.startingState()):
        return []

    myPrioQueue.push((problem.startingState(), [], 0), 0)

    while not myPrioQueue.isEmpty():

        coordinates, path, cost = myPrioQueue.pop()
        if coordinates not in visited:

            visited.append(coordinates)
            
            if problem.isGoal(coordinates):
                return path
            else:
                successors = problem.successorStates(coordinates)
                for state in successors:
                    newPath = path.copy()
                    newPath.append(state[1])
                    newCost = cost + state[2]
                    heur = heuristic(coordinates, problem) + cost
                    myPrioQueue.push((state[0], newPath, newCost), heur)
    
    return []
