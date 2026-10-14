"""Exact finite core-graph check of J intersect a^-1 J a; not a cost verifier."""
from collections import deque
import json

graph = {i: {} for i in range(199)}

def add_edge(source, label, target):
    assert label not in graph[source] and -label not in graph[target]
    graph[source][label] = target
    graph[target][-label] = source

# Label 1 is a; labels 2,...,100 are b_1,...,b_99.
for label in range(2, 101):
    add_edge(0, label, 0)
word = []
for label in range(2, 101):
    word.extend((1, label))
word.append(1)
for index, label in enumerate(word):
    add_edge(index, label, (index + 1) % 199)

# This folded graph's loops at 0 generate exactly J. The a-edge goes
# from 0 to 1, so loops at 1 represent a^-1 J a. Product-graph loops
# at (0,1) represent their intersection.
seen = {(0, 1)}
queue = deque(seen)
edges = set()
while queue:
    left, right = queue.popleft()
    for label in graph[left].keys() & graph[right].keys():
        target = graph[left][label], graph[right][label]
        endpoints = tuple(sorted(((left, right), target)))
        edges.add((endpoints, abs(label)))
        if target not in seen:
            seen.add(target)
            queue.append(target)
rank = len(edges) - len(seen) + 1
assert rank == 0
print(json.dumps({"vertices": sorted(seen), "unoriented_edges": sorted(edges),
                  "rank": rank, "intersection": "trivial"}, indent=2))
