import numpy as np

"""
    Calculates the total number of outgoing connections 
    a webpage has.

    Args:
        graph:
            the matrix containing connection information
            between webpages. Each row represents a source
            webpage, while each column represents a destination
            webpage.
    
    Returns:
        An array containing the number of outgoing connections
        of each webpage.
"""
def total_node_connections(graph):

    return np.sum(graph, axis = 1)

"""
    Constructs the transition matrix. Each column contains the
    probability of going from one webpage to another, while each
    row represents a destination webpage.

    Args:
        graph:
            the matrix containing connection information
            between webpages. Each row represents a source
            webpage, while each column represents a destination
            webpage.

    Returns:
        The transition matrix.
"""
def transition_matrix(graph):

    n = len(graph)
    M = np.zeros((n,n))

    outgoing_connections = total_node_connections(graph)

    for source in range(n):
        for destination in range(n):

            # handles dangling webpages
            if outgoing_connections[source] == 0:
                M[destination][source] = 1 / n

            elif graph[source][destination] == 1:
                M[destination][source] = 1 / outgoing_connections[source]

    return M

"""
    Constructs the Google matrix. (introduces the damping factor d)

    Args:
        M: The transition matrix which was computed earlier.

    Returns:
        The Google matrix.
"""
def google_matrix(M):

    n = len(M)
    d = 0.85 #damping factor

    G = d * M + ((1 - d) / n) * np.ones((n,n))

    return G

"""
    Performs Gaussian elimination to reduce the given matrix to 
    row-echelon form.

    Args:
        matrix: The matrix to be reduced.

    Returns:
        The row-echelon form of the matrix.
"""
def gauss_elim(matrix):
    A = matrix.astype(float).copy()
    rows,cols = A.shape
    row = 0
    for col in range(cols):
        pivot = row + np.argmax(np.abs(A[row:,col])) #Finds largest pivot(avoids division by zero and rounding errors)
        if abs(A[pivot,col])<1e-12: #ignores cols where pivot is almost zero
            continue
        A[[row,pivot]] = A[[pivot,row]] #swapping rows

        for i in range(row +1 ,rows):
            if abs(A[i, col]) < 1e-12:
                continue
            factor = A[i,col]/A[row,col]
            A[i]=A[i] - factor*A[row]
        
        #Above loop is for removing elements below pivot
        row += 1

        if row == rows:
            break
    return A

"""
    Solves for the eigenvector using Gaussian elimination
    and back substitution.

    Args:
        matrix: The matrix representing the eigenvalue system.

    Returns:
        The eigenvector obtained after back substitution.
"""

def solve_eigenvec(matrix):
    A = gauss_elim(matrix)
    n = len(A)
    x = np.zeros(n)
    x[n-1] = 1

    for i in range(n - 2, -1, -1):  
        sum = 0

        for j in range(i + 1, n):
            sum += A[i][j] * x[j]

        if abs(A[i][i]) > 1e-12:
            x[i] = -sum / A[i][i]

    return x
"""
    Normalizes an eigenvector so that the sum of its elements is 1.

    Args:
        vec: The eigenvector to be normalized.

    Returns:
        The normalized eigenvector.
"""
def normalize(vec):
    total = np.sum(vec)
    if total == 0:
        return vec
    return vec/total

"""
    Calculates the PageRank vector by finding the eigenvector of 
    the eigenvalue 1 of the Google matrix.

    Args:
        G: The Google matrix.

    Returns:
        The normalized PageRank vector.
"""
def calc_pagerank(G):
    n = len(G)
    A = G - np.eye(n) #G-I

    eigenvec = solve_eigenvec(A) #(G-I)r = 0
    pagerank = normalize(eigenvec) #pagerank values should now add up to 1
    return pagerank