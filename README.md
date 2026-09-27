# Matrix Eigenvalues and Google's PageRank Algorithm
This project implements the **PageRank algorithm** using concepts from **matrix algebra, eigenvalues, and eigenvectors**.
The main objective is to represent webpages as a directed graph, convert the graph into matrices, and use matrix algebra to calculate the importance of each webpage.

## Let's take an example
![Example PageRank Graph](images/graph.png)

We represent the above connection of graph as a matrix \(A\), which is defined as:

$$
A_{ij} =
\begin{cases}
1, & \text{if webpage } i \text{ has a link to webpage } j\\
0, & \text{otherwise}
\end{cases}
$$

For the above graph, the matrix is:

$$
A =
\begin{bmatrix}
0 & 1 & 1 & 0 \\
0 & 0 & 1 & 0 \\
1 & 0 & 0 & 1 \\
0 & 0 & 0 & 0
\end{bmatrix}
$$

Here, each row represents the source webpage and each column represents the destination webpage.
