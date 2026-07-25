"""Independent post-run checker for the one-vertex-extension campaign.

This package intentionally does not import the extension search engine or
either eternal-domination evaluator.  Its public API is exposed lazily so
that importing the strict graph routines does not pull in SQLite audit code.
"""

from .graph import Graph, Graph6Error, find_isomorphism, graphs_are_isomorphic

__all__ = [
    "Graph",
    "Graph6Error",
    "find_isomorphism",
    "graphs_are_isomorphic",
]
