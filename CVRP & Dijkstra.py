from copy import deepcopy
import math
import numpy as np
import heapq

## Name:
## PID:

#######################################################
##############       QUESTION 1 HERE   ################
#######################################################

def mySavings(S):
  '''
    TODO:

    Write an algorithm that calculates the Savings Heuristic Matrix from the shortest path graph.

    Input:
      List[List[int]] S: the shortest path matrix

    Return:
      List[List[int]] savings: the Savings Heuristic Matrix

  '''

  n = len(S)

  savings = np.zeros((n,n))

  for i in range(1, n):
    for j in range(i + 1, n):
      savings[i][j] = S[0][i] + S[0][j] - S[i][j]

  return savings.astype(int).tolist()
  

  

def myCVRP(S, Q):
  '''
    TODO:

    Write an algorithm that runs the CVRP algorithm from the shortest path graph.

    Input:
      List[List[int]] S: the shortest path matrix
      List[int] Q: Q[0] is the total capacity and for j >= 1, Q[j] is the demand of vertex j 
        (i.e.  A -> 1, B -> 2, C -> 3, and so on).

    Return:
      List[Tuple[List[int], int, int]] solution: a list containing information of each CVRP tour. The tuple
        contains a list of the path, the total capacity for this path, and the total length of this path.
        Thus, if there are 3 paths:
          O - A - E - O (capacity 70, length 8)
          O - C - D - O (capacity 30, length 10)
          O - B - O  (capacity 10, length 4)
        Within the first tuple, it will contain
	        1. a list [1,5]
          2. the capacity 70
          3. the length 8
        This continues for the 2 other paths, and all of these tuples are stored in the outer list.

   NOTE: Recall, vertices start at 1, not 0. Ie. A -> 1, B -> 2, C -> 3, and so on.
   NOTE: The order of the tours in this list does not matter and you will receive full points as long 
      as all the tours are present in this list.
   
   Hint: You may want to call mySavings from this function.
  '''
  
  S = np.array(S)

  n = S.shape[0]

  savings = np.array(mySavings(S))

  tours = {i: [i] for i in range(1, n)}
  demands = {i: Q[i] for i in range(1, n)}
  lengths = {i: S[0, i] + S[i, 0] for i in range(1, n)}

  sorted_savings = sorted([(i, j, savings[i, j]) for i in range(1, n) for j in range(i + 1, n) if savings[i ,j] > 0],
                          key=lambda x: x[2], reverse=True)
  
  capacity = Q[0]

  visited = set()

  for i, j, _ in sorted_savings:
    if (i not in visited and j not in visited and demands[i] + demands[j] <= capacity):
      new_tour = tours[i] + tours[j]
      new_demand = demands[i] + demands[j]
      new_length = lengths[i] + lengths[j] - (S[i,0] + S[0 ,j] + S[i,j])

      tours[i] = new_tour
      demands[i] = new_demand
      lengths[i] = new_length

      for k in new_tour:
        tours[k] = new_tour
        demands[k] = new_demand
        lengths[k] = new_length
        visited.add(k)

  unique_tours = set(tuple(t) for t in tours.values())

  unique_tours = [list(t) for t in unique_tours]

  result = []

  for tour in unique_tours:
    demand = sum(Q[i] for i in tour)
    length = S[0, tour[0]] + S[0, tour[-1]] + sum(S[tour[i], tour[i + 1]] for i in range(len(tour) - 1))
    result.append((tour, demand, length))

  return result
    
  

def mySavingsLength (S, Q):  
  '''
    TODO:
    
    Write an algorithm that calculates the length of the Savings Heuristic
    
    Input:
      List[List[int]] S: the shortest path matrix
      List[int] Q: Q[0] is the total capacity and for j >= 1, Q[j] is the demand of vertex j 
        (i.e.  A -> 1, B -> 2, C -> 3, and so on).
    
    Return:
      int savingsLength: sum of the lengths of all tours after CVRP

    Hint: You may want to call myCVRP from this function
  '''

  tours = myCVRP(S, Q)

  total_length = sum(tour[2] for tour in tours)

  return total_length
  


def myRoundTripLength (S, Q):
  '''
    TODO:
    
    Write an algorithm that calculates the length of the Round Trip
    
    Input:
      List[List[int]] S: the shortest path matrix
      List[int] Q: Q[0] is the total capacity and for j >= 1, Q[j] is the demand of vertex j 
        (i.e.  A -> 1, B -> 2, C -> 3, and so on).
    
    Return:
      int roundTripLength: sum of the lengths of all roundtrips before CVRP

    Hint: You may want to call myCVRP from this function
  '''

  n = len(S)

  total_length = 0

  for i in range(1, n):
    total_length += 2 * S[0][i]

  return total_length
  
 
#########################################################
##############       QUESTION 2 HERE   ##################
#########################################################
def myDijkstra(vertices, edges): 
  '''
    TODO:

    Write an algorithm that runs Dijkstra's Algorithm on a Directed Graph to solve the Single Source Shortest Path Problem.
    The source vertex is always vertex 0.

    Input:
        vertices: Vector of the first n non-negative integers representing the n vertices of G.
        edges: A vector containing edges in G in the form of tuples where each tuple is of the form [i, j, c(i, j)],
            corresponding to the directed edge from vertex i to vertex j with weight c(i, j).


    return:
        sol: A tuple of the following elements in the exact order:
            0:  shortestPath: List of lists containing the shortest path from source vertex to vertex i at index i.
            1:  shortestPathLength: A vector that contains the shortest distance from source vertex to vertex i at index i.

    Some Helper functions that might help you modularize the code:
        - myInitialize(n, s) : calculates Initialize (as explained in class) from a given source node (s) given the number of nodes (n).

        - myRelax(distance, edges, u) : Gives an updated distance vector after `Relax`-ing (as explained in class) all edges
          going out from u.

    Note: These functions are recommended however we won't be grading your implementations of the
          above stated functions

  '''   
  def myInitialize(n, s):
  
      distance = [float('inf')] * n

      distance[s] = 0

      shortest_path = [[] for _ in range(n)]

      shortest_path[s] = [s]

      return distance, shortest_path

  def myRelax(distance, shortest_path, edges, u):
      for edge in edges:
          
          if edge[0] == u:
              
              v = edge[1]

              weight = edge[2]

              if distance[u] + weight < distance[v]:
                  
                  distance[v] = distance[u] + weight

                  shortest_path[v] = shortest_path[u] + [v]

      return distance, shortest_path

  n = len(vertices)

  source = 0

  distance, shortest_path = myInitialize(n, source)
  
  visited = [False] * n

  priority_queue = [(0, source)]  # (distance, vertex)

  while priority_queue:
      _, u = heapq.heappop(priority_queue)

      if visited[u]:
          continue
      
      visited[u] = True

      distance, shortest_path = myRelax(distance, shortest_path, edges, u)

      for edge in edges:
          if edge[0] == u:
              v = edge[1]
              if not visited[v]:
                  heapq.heappush(priority_queue, (distance[v], v))

  return shortest_path, distance
