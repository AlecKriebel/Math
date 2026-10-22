# WIP: Degenerate versus full MTW

Problem 30000997 / OWR-2042-006. This research packet is provisional, AI-assisted, and not independently reviewed. The global question remains unresolved. No novelty or full-resolution claim is made.

The main target asks whether A3w implies nonnegative cross-curvature for the squared-distance cost on the entire off-cut-locus domain of a complete Riemannian manifold. The original OWR sentence and the completeness convention in its cited paper are distinguished in PUBLIC_SOURCE_GATE.md.

TURN_1.md gives a local geometric separation on an explicit complete surface, which fails global A3w. TURN_2.md constructs compact positively curved candidates but does not establish their global A3w. TURN_3.md proves A3w on an entire equatorial slice of these candidates, while full NNCC fails on that slice. None of these statements resolves the original global implication.

Numerical scripts and outputs, when present, are diagnostics only and do not certify the cut locus, minimizing geodesics, or global tensor signs.

Final status: exhausted after 5/5 author turns. See FINAL_RESULT.md. The original global problem remains unresolved. No publication-ready result or priority claim is made.

Exact algebra replay: run `python3 check_exact.py` with SymPy installed. It checks the encoded curvature, Jacobi series, quartic and finite-witness identities; it does not validate the geometric proof or certify global A3w. Optional numerical probes additionally require NumPy and SciPy and remain noncertifying.
