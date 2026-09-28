# Minimal Flask backend: serves the page and runs the PageRank maths from pagerank.py
import numpy as np
from flask import Flask, render_template, request, jsonify

import pagerank as pr

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json(silent=True) or {}
    labels = data.get("labels", [])
    graph = data.get("graph", [])

    # ---- validate input ----
    n = len(labels)
    if n == 0:
        return jsonify(error="Add at least one page before calculating."), 400
    if len(graph) != n or any(not isinstance(row, list) or len(row) != n for row in graph):
        return jsonify(error="The adjacency matrix must be square (one row and column per page)."), 400
    if any(v not in (0, 1) for row in graph for v in row):
        return jsonify(error="The adjacency matrix may only contain 0 and 1."), 400

    # graph[source][destination] = 1 means source links to destination
    graph = np.array(graph, dtype=float)

    # ---- the PageRank pipeline, exactly in the order of the original code ----
    outgoing = pr.total_node_connections(graph)   # links leaving each page
    M = pr.transition_matrix(graph)               # M[destination][source]
    G = pr.google_matrix(M)                       # G = dM + ((1-d)/n)J
    ranks = pr.calc_pagerank(G)                   # solves (G - I)r = 0, then normalises

    # order of pages from highest to lowest PageRank
    order = [int(i) for i in np.argsort(-ranks, kind="stable")]

    return jsonify(
        adjacency=graph.tolist(),
        outgoing=outgoing.tolist(),
        transition=M.tolist(),
        google=G.tolist(),
        pagerank=ranks.tolist(),
        order=order,
        damping=0.85,
    )


if __name__ == "__main__":
    app.run(debug=True)
