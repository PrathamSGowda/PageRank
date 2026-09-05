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

    n = len(graph);
    M = np.zeros((n,n))

    outgoing_connections = total_node_connections(graph)

    for source in range(n):
        for destination in range(n):
            if graph[source][destination] == 1:
                M[destination][source] = 1 / outgoing_connections[source]

    return M;

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


# for testing purposes only

graph = np.array([
    [0, 1, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [1, 0, 0, 1, 0],
    [1, 0, 0, 0, 1],
    [0, 0, 1, 1, 0]
])

M = transition_matrix(graph)
print(M)

G = google_matrix(M)
print(G)
