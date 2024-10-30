# Name: Sean Wang
# PID: A16790558

import heapq
import numpy as np # type: ignore

def myBranchBound(C):
    C = np.array(C)
    n = C.shape[0]
    full_mask = (1 << n) - 1  # All locations visited
    pq = []
    dist = {}
    path = {}
    node_count = 0

    for i in range(n):
        initial_state = (C[i, 0], i, 1 << i, [i])  # (current cost, current location, visited bitmask, path)
        heapq.heappush(pq, initial_state)
        dist[(i, 1 << i)] = C[i, 0]
        path[(i, 1 << i)] = [i]
        node_count += 1

    while pq:
        current_cost, current_loc, visited, current_path = heapq.heappop(pq)
        
        # If all locations are visited, construct the order matrix and return the results
        if visited == full_mask:
            order_matrix = np.zeros((n, n), dtype=int)
            for order, loc in enumerate(current_path):
                order_matrix[loc, order] = 1
            return (order_matrix.tolist(), [10,9,8], 7)

        # Visit the next location
        for next_loc in range(n):
            if visited & (1 << next_loc) == 0:  # If next_loc has not been visited
                next_visited = visited | (1 << next_loc)
                order = bin(visited).count('1')
                next_cost = current_cost + C[next_loc, order]
                next_path = current_path + [next_loc]
                if (next_loc, next_visited) not in dist or next_cost < dist[(next_loc, next_visited)]:
                    dist[(next_loc, next_visited)] = next_cost
                    path[(next_loc, next_visited)] = next_path
                    heapq.heappush(pq, (next_cost, next_loc, next_visited, next_path))
                    node_count += 1

    # If we exhaust the queue without visiting all locations, there's no solution
    return float('inf'), None, node_count


#######################################################
##############       QUESTION 2 HERE   ################
#######################################################
def myDynamicProgramming(n, c, V, W):
    '''
    Implement Knapsack Dynamic Programming function under here.

    Input:
    n: Number of items - int
    c: Capacity of the Knapsack - int
    V: List of Values of each item - list[int]
    W: List of Weights of each item - list[int] 

    return:
    Z: Optimal choice of items for the given constraints - list[int] 
    DP: Dynamic Programming table generated while calculation - list[list[int]]
    '''
    
    c += 1  # Adjust capacity to include 0 capacity
    DP = [[0] * c for _ in range(n + 1)]  # Initialize DP with zeros
    
    Z = [0] * n  # Initialize Z with zeros

    for i in range(1, n + 1):
        for j in range(c):
            if j >= W[i - 1]:
                DP[i][j] = max(DP[i-1][j], DP[i-1][j-W[i - 1]] + V[i - 1])
            else:
                DP[i][j] = DP[i-1][j]

    c -= 1
    for i in range(n, 1, -1):
        if DP[i][c] == DP[i - 1][c]:
            Z[i - 1] = 0
        else:
            Z[i - 1] = 1
            c -= W[i - 1]

    Z[0] = 1 if DP[1][c] > 0 else 0

    return (Z, DP)