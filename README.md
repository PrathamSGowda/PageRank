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

## Counting Outgoing Connections
Before constructing the transition matrix, we need to find the total number of outgoing connections from each webpage.
This can be calculated by adding the elements of each row of the a matrix \(A\).

![image](images/image3.png)

This tells us that A and C have 2 outgoing connections, B has 1 and D has 0 outgoing connection.

## Transition Matrix
The number of outgoing connections tells us how the probability is distributed when a user follows links from a webpage. This is represented by 
a Transition Matrix \(M\), which is defined as: 

![image](images/image4.png)

where:

- $L_i$ = number of outgoing links from webpage $i$
- $n$ = total number of webpages

The transition matrix for our example graph is:

![image](images/image5.png)

Here, each column represents the source webpage and each row represents the destination webpage.

## Google Matrix
The transition matrix assumes that the user always follows one of the available links. However, in the PageRank algorithm, a user can also randomly jump to any webpage.

To model this, we introduce a **damping factor** \(d\) = 0.85.

This means that:

- 85% of the time the user follows a link.
- 15% of the time the user randomly jumps to another webpage.

The Google Matrix is defined as : 

![image](images/image6.png)

where:

- \(G\) = Google matrix
- \(M\) = transition matrix
- \(d\) = damping factor
- \(n\) = number of webpages
- \(J\) = matrix containing only ones

For our example : 

![image](images/image7.png)
