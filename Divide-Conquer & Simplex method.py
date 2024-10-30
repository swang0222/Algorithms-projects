## Name: Sean Wang
## PID: A16790558

import numpy as np # type: ignore

#########################################################
##############       QUESTION 1 HERE   ##################
#########################################################  

def myMinDistance(P):
    '''
    Input:
        List[Tuple(int, int)] P: an array of Points. Points contain the fields x and y, with (x, y) 
        representing a point in the Cartesian plane.

    Output:
        An int representing the square of the minimum distance between two of the given points. - int
    '''
    # Helper function to calculate the square of the distance between two points
    def dist_sq(p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

    def strip_closest(strip, d):
        min_dist = d  # Initialize the minimum distance as d

        strip.sort(key=lambda point: point[1])

        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and (strip[j][1] - strip[i][1]) ** 2 < min_dist:
                min_dist = min(min_dist, dist_sq(strip[i], strip[j]))
                j += 1

        return min_dist

    def shortest_dist(points_sorted_by_x, points_sorted_by_y):
        n = len(points_sorted_by_x)

        if n <= 3:
            # Base case
            min_dist = float('inf')
            for i in range(n):
                for j in range(i + 1, n):
                    min_dist = min(min_dist, dist_sq(points_sorted_by_x[i], points_sorted_by_x[j]))
            return min_dist

        mid = n // 2
        mid_point = points_sorted_by_x[mid]

        # Divide points in y sorted array
        points_left_of_center = [point for point in points_sorted_by_y if point[0] <= mid_point[0]]
        points_right_of_center = [point for point in points_sorted_by_y if point[0] > mid_point[0]]
        
        dist_left = shortest_dist(points_sorted_by_x[:mid], points_left_of_center)
        dist_right = shortest_dist(points_sorted_by_x[mid:], points_right_of_center)

        dist = min(dist_left, dist_right)

        # Create a strip
        strip = [point for point in points_sorted_by_y if abs(point[0] - mid_point[0]) < dist]

        return min(dist, strip_closest(strip, dist))

    points_sorted_by_x = sorted(P, key=lambda point: point[0])
    points_sorted_by_y = sorted(P, key=lambda point: point[1])

    # Call the recursive function
    return shortest_dist(points_sorted_by_x, points_sorted_by_y)

  
#########################################################
##############       QUESTION 2 HERE   ##################
#########################################################
def mySimplexLP(A, B, C):
    '''
    Implement the Simplex algorithm.

    Input:
        A: an m x n array of integers
        B: an m-item list of integers
        C: an n-item list of integers

    return:
        optimal: array of length n with optimal values for x1, ..., xn
        slack: array of length m with slack variable values for s1, ..., sm
        value: objective value of the optimal solution
    '''
    
    # Convert inputs to numpy arrays
    np_A = np.array(A)

    np_B = np.array(B)

    np_C = np.array(C)
    
    m, n = np_A.shape

    slack_size = m
    
    # Add slack variables to A and adjust C
    slacks_matrix = np.eye(slack_size)

    tableau = np.hstack((np_A, slacks_matrix))

    tableau = np.hstack((tableau, np_B.reshape(-1, 1)))
    
    C_extended = np.hstack((np_C, np.zeros(slack_size)))

    tableau = np.vstack((tableau, np.hstack((-C_extended, [0]))))
    
    # Perform row reduction with pivot row
    def pivot(tableau, row, col):

        tableau[row, :] /= tableau[row, col]

        for r in range(tableau.shape[0]):
            if r != row:
                tableau[r, :] -= tableau[r, col] * tableau[row, :]

    while np.any(tableau[-1, :-1] < 0):
        pivot_col = np.argmin(tableau[-1, :-1])
        # Determine the pivot row
        ratios = np.divide(tableau[:-1, -1], tableau[:-1, pivot_col], out=np.full_like(tableau[:-1, -1], np.inf), where=tableau[:-1, pivot_col] > 0)

        pivot_row = np.argmin(ratios)
        
        pivot(tableau, pivot_row, pivot_col)
    
    # Extract results
    optimal = np.zeros(n)
    slack = np.zeros(m)
    
    # Check the first few n columns to find basic x1 ... xn variables
    for i in range(n):
        # Find columns that have a single 1 in the row (which indicates a basic variable)
        if np.count_nonzero(np.isclose(tableau[:, i], 1)) == 1:
            optimal[i] = tableau[np.isclose(tableau[:, i], 1), -1].sum()
    
    # Check the last few m columns to find basic s1 ... sm variables
    for j in range(n, n + m):
        # Find columns that have a single 1 in the row (which indicates a basic variable)
        if np.count_nonzero(np.isclose(tableau[:, j], 1)) == 1:
            slack[j - n] = tableau[np.isclose(tableau[:, j], 1), -1].sum()
    
    value = tableau[-1, -1]

    optimal = np.round(optimal, 8)

    slack = np.round(slack, 8)
    
    return (optimal.astype(int).tolist(), slack.astype(int).tolist(), value.astype(int))