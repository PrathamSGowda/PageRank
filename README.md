# Matrix Eigenvalues and Google's PageRank Algorithm
This project implements the **PageRank algorithm** using concepts from **matrix algebra, eigenvalues, and eigenvectors**.
The main objective is to represent webpages as a directed graph, convert the graph into matrices, and use matrix algebra to calculate the importance of each webpage.

## Let's take an example
![Example PageRank Graph](images/graph.png)

We represent the above connection of graph as a matrix \(A\), which is defined as:

![image](images/image1.png)

For the above graph, the matrix is:

![image](images/image2.png)

Here, each row represents the source webpage and each column represents the destination webpage.
