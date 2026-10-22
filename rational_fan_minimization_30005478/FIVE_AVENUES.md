# Final five-avenue account

Status: editorial synthesis of the final research state, to be checked in package review. This is not the superseded provisional working log. The accepted result remains UNSOLVED, five research avenues completed, with a substantial partial classification.

1. **Subspace-lattice closure.** Rational sums and intersections are computable, but this work proves neither finiteness of the generated lattice nor that it contains an optimum. No terminating algorithm follows from this avenue.
2. **Rank/shrunk-subspace optimization.** The objective is a maximum of individual rank expressions, not a sum. A sum-rank algorithm cannot be substituted without a theorem justifying the change. No such theorem is claimed.
3. **Schubert/quiver arithmetic.** Fixed-dimension threshold feasibility is projective determinantal rational-point feasibility. The final anchor and loopless-quiver constructions establish the converse reduction, using the explicitly rational Veronese inverse. Hence there is an effective finite-oracle equivalence with rational-point feasibility for projective algebraic sets over Q, not necessarily irreducible. This supersedes the earlier provisional absence of a converse reduction. See projective_equivalence.md and independent_reduction_audit.md, Sections 1–4.
4. **Exact examples and failed relaxations.** The unpadded four-plane example alone does not separate minima, but the final padded construction has real minimum 6 and rational minimum 7. The six maximal cones give a genuine nonpure rational simplicial fan. This supersedes the earlier provisional absence of an arithmetic gap. See arithmetic_gap.md and independent_reduction_audit.md, Section 5.
5. **Effective certificates.** A rational candidate basis gives exact-rank upper-bound certificates. The finite symbolic checks included here verify displayed data and cannot prove termination of rational witness searches or certify every negative rational incidence instance. Real feasibility cannot replace rational feasibility, as the gap proves. No complete unconditional certificate procedure is claimed.

## Provenance and editorial scope

The five headings and unsuccessful-route limitations derive from the authored working analysis; that provisional log is deliberately not reproduced. Final positive claims derive from the two final proof reports and their independent PASS audit. Source identity and bounded literature-search findings are in SOURCE_GATE.md. This synthesis omits unaudited low-dimensional algorithms and unrelated elementary optimization lemmas. It does not promote provisional statements into accepted theorems.

No general algorithm, undecidability result, polynomial-time reduction, or extension to pure, balanced, or tropical-realizable fans is asserted.
