from utils.datastructures.priority_queue import PriorityQueue
from game.components import *
from random import seed
from random import random
import heapq
import math


def greedy_best_first_search(initial_state, is_goal, heuristic, visitor):
    """Greedy Best First Search Algorithm

    Keyword arguments:\\
    * initial_state -- starting state of problem.\\
    * heuristic -- a heuristic estimate to goal h(n)

    Return variables:\\
    * None in case of no goal found.\\
    * state -- goal state found.\\
    * nodes_expanded -- final number of expanded nodes to reach goal.\\
    * max_search_depth -- Maximum depth reached where goal resides.
    """
    # Build minimum heap based on heuristic as key.
    frontier = PriorityQueue('min', heuristic)
    frontier.append(initial_state)
    # Build dictionary for O(1) lookups.
    frontier_config = {}
    frontier_config[initial_state] = True
    # Build set of already explored states.
    explored = set()
    # Variables for algorithm evaluation purposes.
    nodes_expanded = 0
    max_search_depth = 0

    while frontier:
        state = frontier.pop()
        explored.add(state)
        # Goal Test: stop algorithm when goal is reached.
        if is_goal(state):
            return (state, nodes_expanded, max_search_depth)

        nodes_expanded += 1
        for neighbor in visitor.visit(state):
            # Add state to explored states if doesn't already exists.
            if neighbor not in explored and neighbor not in frontier_config:
                frontier.append(neighbor)
                frontier_config[neighbor] = True
                if neighbor.cost > max_search_depth:
                    max_search_depth = neighbor.cost
            # If state is not explored but in frontier, update it's key if less.
            elif neighbor in frontier:
                if heuristic(neighbor) < frontier[neighbor]:
                    frontier.__delitem__(neighbor)
                    frontier.append(neighbor)
    return None


def a_star_search(initial_state, is_goal, heuristic, visitor):
    """A* search Algorithm is greedy best-first graph search with f(n) = g(n)+h(n).

    Keyword arguments:\\
    * initial_state -- starting state of problem.\\
    * heuristic -- a heuristic estimate to goal h(n)\\
    * cost -- a cost function for a state.

    Return variables:\\
    * None in case of no goal found.\\
    * state -- goal state found.\\
    * nodes_expanded -- final number of expanded nodes to reach goal.\\
    * max_search_depth -- Maximum depth reached where goal resides.
    """
    return greedy_best_first_search(initial_state, is_goal, lambda x: x.cost_from_root() + heuristic(x), visitor)


def real_time_a_star_search(initial_state, is_goal, heuristic, visitor):
    """ An informed search that used to reduce the execution time of A*.

        Args:
            initial_state : Starting state of problem.
            heuristic : A heuristic estimate to goal h(n).
            cost : A cost function for a state.

        Returns:
            current_state : A state that eventually will be the goal state.
    """

    visited_states_to_heuristic = {}
    current_state = initial_state
    FIRST_BEST_STATE_INDEX = 2
    SECOND_BEST_TOTAL_COST_INDEX = 0
    seed(1)
    i = 0
    while(not is_goal(current_state)):
        print(current_state.get_owned_territories("Swidan"))
        print("iteration ", i)
        i += 1
        total_cost_to_state = []

        # Expand the current state
        for neighbour in visitor.visit(current_state):

            # If the neighbour exists in the visited_states dictionary, then stored heuristic value in the dictionary is used
            # and added to the cost from the current state to the neighbour to get the total cost
            if neighbour in visited_states_to_heuristic.keys():
                neighbour_total_cost = visited_states_to_heuristic[neighbour] + current_state.cost_to(neighbour)

            # Else, then calculate the heuristic value of the neighbour
            # and add it to the cost from the current state to the neighbour to get the total cost
            else:
                neighbour_total_cost = heuristic(neighbour) + current_state.cost_to(neighbour)

            # Store the neighbours & their total cost in a min heap
            # Use random() for tie breaking
            heapq.heappush(total_cost_to_state,
                           (neighbour_total_cost, random(), neighbour))

        temp_state = heapq.heappop(total_cost_to_state)[FIRST_BEST_STATE_INDEX]

        # Store the current state associated with it the second best total cost value
        visited_states_to_heuristic[current_state] = heapq.heappop(
            total_cost_to_state)[SECOND_BEST_TOTAL_COST_INDEX]

        # Choose the state with the minimum total cost to be the new current state
        current_state = temp_state

    return current_state


def minimax_alpha_beta_pruning(initial_state, current_player_name, opposition_player_name, visitor):
    def minimize(state, alpha, beta):
        state.player_name = opposition_player_name
        if state.is_goal():
            # state.calculate_utility()
            return None, 1

        minChild, minUtility = None, math.inf

        for child in visitor.visit(state):
            child, utility = maximize(child, alpha, beta)

            if utility < minUtility:
                minChild, minUtility = child, utility
            if minUtility <= alpha:
                break
            if minUtility < beta:
                beta = minUtility

        return minChild, minUtility

    def maximize(state, alpha, beta):
        state.player_name = current_player_name
        if state.is_goal():
            state.calculate_utility()
            return None, 1

        maxChild, maxUtility = None, -math.inf

        for child in visitor.visit(state):
            child, utility = minimize(child, alpha, beta)

            if utility > maxUtility:
                maxChild, maxUtility = child, utility
            if maxUtility >= beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility

        return maxChild, maxUtility

    player_name = initial_state.player_name
    child, utility = maximize(initial_state, -math.inf, math.inf)

    return child
