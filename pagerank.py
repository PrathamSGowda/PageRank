import numpy as np

#initializing a page vector
def init_pagevector(n):
    return np.ones(n)/n

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
            if graph[source][destination] == 1:
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

def solve_eigenvec(matrix):
    A = gauss_elim(matrix)
    n = len(A)
    x = np.zeros(n)
    x[n-1] = 1
    for i in range(n- 2, -1,-1): # Back Substitution
        sum = 0
        for j in range(i+1,n):
            sum += A[i][j] * x[j]
        if abs(A[i][j])>1e-12:
            x[i] = -sum/A[i][i]
    return x

def normalize(vec):
    total = np.sum(vec)
    if total == 0:
        return vec
    return vec/total

def calc_pagerank(G):
    n = len(G)
    A = G - np.eye(n) #G-I

    eigenvec = solve_eigenvec(A) #(G-I)r = 0
    pagerank = normalize(eigenvec)#pagerank values should now add up to 1
    return pagerank

# for testing purposes only

graph = np.array([
    [0, 1, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [1, 0, 0, 1, 0],
    [1, 0, 0, 0, 1],
    [0, 0, 1, 1, 0]
])

M = transition_matrix(graph)
print("Transition Matrix : ")
print(M)

G = google_matrix(M)
print("\nGoogle Matrix : ")
print(G)

A = G - np.eye(len(G)) #G-I
print("\nG - I:")
print(A)

#Gaussian elimination
A_reduced = gauss_elim(A)
print("\nAfter Gaussian Elimination:")
print(A_reduced)

eigenvec = solve_eigenvec(A)

print("\nEigenvector:")
print(eigenvec)

# Normalize
pagerank = normalize(eigenvec)
print("\nPageRank:")
print(pagerank)

print("\nSum of PageRank:")
print(np.sum(pagerank))
