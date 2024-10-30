## Name: Sean Wang
## PID: A16790558


from typing import List, Tuple

#######################################################
##############       QUESTION 1 HERE   ################
#######################################################

def myEDD(P, D):
    '''
    Implement EDD(earliest due date) function under here.
    Input:
    List P, List D
        List P: A list of processing time of job J_1, ... J_n
        List D: A list of due dates of each job, J_1, ... J_n

    Input constraints: 2<N<=10

    return:
    (Schedule, lMax): A pair of the following elements in the exact order:
        0:  Schedule:  List containing Optimal schedule of Jobs. The size of schedule should be N. 
                Each tuple inside schedule should contain:
                    1. index of job(job index should start at 1 NOT 0!) 
                    2. C_j of the job (completion time)
                    3. L_j of the job (Lateness)
        1:  lMax: maximum lateness from the schedule
    '''

    n = len(D)

    IDs = list()
    for i in range(n):
        IDs.append(i + 1)

    for i in range(1, n):
        j = i
        while j > 0 and D[j] < D[j - 1]:
            # Swap elements in D
            D[j], D[j - 1] = D[j - 1], D[j]
            # Swap elements in P
            P[j], P[j - 1] = P[j - 1], P[j]
            # Swap elements in IDs
            IDs[j], IDs[j - 1] = IDs[j - 1], IDs[j]
            j -= 1

    result = list()

    for i in range(n):
        result.append((IDs[i], sum(P[:i + 1]), sum(P[:i + 1]) - D[i]))

    return (result, max([row[2] for row in result]))

#########################################################
##############       QUESTION 2 HERE   ##################
#########################################################
def myListScheduling(P, m):

    '''
    Implement ListScheduling function under here and return the optimal schedule.

    Input:
    List P: A list of processing time of jobs J_1 ,...., J_n 
    int m: number of parallel and identical processors

    return:
    List[List[Tuple[int, int]] sol: The optimal schedule for each job on each processor.
        The i-th index of the outermost list must contain the schedule of jobs for the (i+1)-th processor. 
        (Since processors start from 1 and list indices start from 0).
        Each pair inside this schedule must contain the following:
            1. index of job (job index starts at 1 NOT 0!) - int
            2. completion time of the job on that respective processor - int

            Note:  the start time of job J_j is the completion time of job J_j−1 on processor Pi.  
                  The start time for the first job on each processor is always 0. 
  
    '''

    result: List[List[Tuple[int, int]]] = [[] for _ in range(m)]

    row_sums = [0] * m

    for i in range(len(P)):
        min_sum = min(row_sums)
        min_index = row_sums.index(min_sum)
        result[min_index].append((i + 1, min_sum + P[i]))
        row_sums[min_index] += P[i]

    
    return result
    
def myLPT(P, m):

    '''

    Implement LPT function under here and return the optimal schedule.

    Input:
    List P: A list of processing time of jobs J_1 ,...., J_n 
    int m: number of parallel and identical processors 

    return:
    List[List[Tuple[int, int]] sol: The optimal schedule for each job on each processor.
        The i-th index of the outermost list must contain the schedule of jobs for the (i+1)-th processor.
        (Since processors start from 1 and list indices start from 0).
        Each pair inside this schedule must contain the following:
            1. index of job (job index starts at 1 NOT 0!) - int
            2. completion time of the job on that respective processor - int
            
            Note:  the start time of job J_j is the completion time of job J_j−1 on processor Pi.  
                  The start time for the first job on each processor is always 0. 
  
    '''
    n = len(P)

    IDs = list()
    for i in range(n):
        IDs.append((P[i], i + 1))
    

    IDs.sort(key=lambda x: (-x[0], x[1]))

    result: List[List[Tuple[int, int]]] = [[] for _ in range(m)]

    row_sums = [0] * m

    for i in range(len(P)):
        min_sum = min(row_sums)
        min_index = row_sums.index(min_sum)
        result[min_index].append((IDs[i][1], min_sum + IDs[i][0]))
        row_sums[min_index] += IDs[i][0]

    return result

def mySPT(P, m):

    '''
    Implement SPT function under here and return the optimal schedule.

    Input:
    List P: A list of processing time of jobs J_1 ,...., J_n 
    int m: number of parallel and identical processors 

    return:
    List[List[Tuple[int, int]] sol: The optimal schedule for each job on each processor.
        The i-th index of the outermost list must contain the schedule of jobs for the (i+1)-th processor,
        (Since processors start from 1 and list indices start from 0).
        Each pair inside this schedule must contain the following:
            1. index of job (job index starts at 1 NOT 0!) - int
            2. completion time of the job on that respective processor - int
            
            Note:  the start time of job J_j is the completion time of job J_j−1 on processor Pi.  
                  The start time for the first job on each processor is always 0. 
  
    '''

    n = len(P)

    IDs = list()
    for i in range(n):
        IDs.append((P[i], i + 1))

    IDs.sort()

    result: List[List[Tuple[int, int]]] = [[] for _ in range(m)]

    row_sums = [0] * m

    for i in range(len(P)):
        min_sum = min(row_sums)
        min_index = row_sums.index(min_sum)
        result[min_index].append((IDs[i][1], min_sum + IDs[i][0]))
        row_sums[min_index] += IDs[i][0]

    
    return result
