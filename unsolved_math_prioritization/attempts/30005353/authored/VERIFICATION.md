# Exact supplemental verification

All three scripts use only Python's standard library. Run them in ordinary Python mode from the packet root:

    python3 checks/verify.py
    python3 checks/degree_checks.py
    python3 checks/deletion_checks.py

## Moore-space controls

For p=2,3,5,7,9, the constructor forms the specified simplicial complex and its barycentric subdivision. It checks the full face counts, exact triangle-boundary ranks over F₂ and a prime dividing p, and explicit presentation reductions after a spanning-tree collapse. Elementary Tietze eliminations reduce the full triangle presentation to a cyclic presentation with relator length p, the omitted-triangle presentation to one free generator, and that presentation plus the six-edge base cycle to the empty presentation.

For p=2 and p=3, all 729 and 1,161 simple cycles of length at most five are enumerated and evaluated against a nontrivial mod-p cocycle. Every value vanishes; the six-edge base has nonzero value. This is a finite homology control, not an exhaustive π₁-optimization algorithm. The cost fields in the receipt evaluate the formulas proved in PROOF.md; their optimality is justified by that proof, not by enumerating all attaching families.

The even-p example is a negative control against the false statement that all triangular boundaries form an F₂ basis. The full p=3 presentation is a negative control against identifying an F₂ basis with normal generators.

## Degree-reduction controls

Seventeen deterministic connected graph cases and 51 expansions (L=1,2,4) check maximum degree three, preservation of graph cycle rank, the lifted-cycle length inequalities, and exact minimum F₂-basis cost inequalities via exhaustive simple-cycle enumeration and binary Gaussian elimination.

For all 222 expanded simple cycles, the checker verifies that an external subdivided path is either unused or completely traversed, and that the projected original edge set is Eulerian. Twenty-one cases project to non-simple walks, providing a direct control against silently assuming the projection is simple. Fifty-one lifted fundamental families reduce to trivial presentations by exact Tietze elimination. No general aπ optimum is computed.

## Deletion upper-bound controls

Sixty-one graph cases yield 340 rank-reducing deletion steps. The checker verifies that recorded cycles are simple, retired paths are disjoint and contain only cyclic edges, each cycle obeys the charge bound, the reversed family is weakly fundamental, and the final presentation reduces to the trivial one. It includes a plain cycle and two cycles joined by a long bridge path.

The finite samples do not prove the universal logarithmic bound; the complete argument is in PROOF.md. None of these tests is formal proof-assistant verification, a literature audit, or independent mathematical review.
