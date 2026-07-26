"""Independent decoded-candidate verifier for the order-12, parameter-4 slice.

This package deliberately imports neither the synthesis encoders nor either
of the campaign's general-purpose eternal-domination verifiers.
"""

from .checker import (
    ANCHOR,
    K,
    N,
    Candidate,
    CandidateFormatError,
    Graph,
    anchored_four_color_search,
    canonical_edges_bytes,
    check_eternal_family,
    graph6_sha256,
    load_candidate,
    parse_candidate,
    verify_candidate,
)

__all__ = [
    "ANCHOR",
    "K",
    "N",
    "Candidate",
    "CandidateFormatError",
    "Graph",
    "anchored_four_color_search",
    "canonical_edges_bytes",
    "check_eternal_family",
    "graph6_sha256",
    "load_candidate",
    "parse_candidate",
    "verify_candidate",
]
