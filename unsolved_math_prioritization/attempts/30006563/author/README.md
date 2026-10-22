# Colorings without disjoint color-isomorphic triangles

Problem 30006563 / OWR-14299905-038. Research date: 2026-10-03. Five substantive attempts completed. **The asymptotic problem remains unresolved.** This is an AI-assisted research record containing partial results and exact finite checks, not a claimed solution or a novelty claim.

## Source and exact scope

The primary source is David Conlon's Question 14 in *Combinatorics*, Oberwolfach Report 1/2026, printed page 74, DOI [10.4171/owr/2026/1](https://doi.org/10.4171/owr/2026/1), available from the [official report record](https://publications.mfo.de/handle/mfo/4435). The original PDF page was checked visually. The [catalog URL](https://www.unsolvedmath.com/problems/30006563) returned HTTP 403; live catalog-body verification is not claimed.

Let g(n) be the minimum number of colors in an arbitrary edge-coloring of K_n that has no two vertex-disjoint triangles related by a color-preserving isomorphism. Colors are fixed labels, and multiplicity matters. For triangles, equality of the three-edge color multisets is equivalent to color-isomorphism. Proper edge-coloring is not required.

The report gives a baseline square-root lower bound and n-4 upper bound, then credits Conlon, Fox and Pham with a lower bound c*n^(1/2+epsilon), for unspecified positive constants. It asks whether growth is linear, possibly n-O(1). The stronger lower bound is treated as an attributed announcement; its proof and numerical exponent were not located. Focused current primary-source checks found no full resolution. The [Conlon--Tyomkyn paper](https://www.its.caltech.edu/~dconlon/repeats.pdf) and [Botler et al. paper](https://repositorio.usp.br/directbitstream/89d4649f-9f3e-4281-b3a6-625919d23b5a/3122626.pdf) study proper edge-colorings and do not settle the general question. Current [Conlon](https://www.its.caltech.edu/~dconlon/) and [Fox](https://stanford.edu/~jacobfox/publications) author pages were also checked. This bounded review does not establish historical priority or universal absence of a result.

## Main result proved in this packet

**For every n>=9, g(n)<=n-6.**

This follows from a completely explicit three-color K_9 and an elementary fresh-color vertex extension. The K_9 proof does not depend on a solver. Let A,B each have three vertices, and add z,x,y. Color the edges as follows:

| Edge location | Color |
|---|---:|
| Inside A | 1 |
| Inside B, or between A and B | 0 |
| From z to A or B | 1 |
| From x to A; from x to B | 0; 2 |
| From y to A; from y to B | 1; 2 |
| zx; zy; xy | 1; 0; 2 |

Every triangle of type 000 or 022 contains at least two vertices of B. Every triangle of type 001 or 111 contains at least two vertices of A. Types 002, 011, and 012 all contain x, z, and y respectively. Types 112 and 222 contain {z,x} and {x,y} respectively. Type 122 is absent. This exhausts all ten possible multisets, and each realized type family is intersecting. The complete count and proof are in [Attempt 5](attempts/turn_05.md).

Adding a vertex with a new color on all its incident edges preserves admissibility: every triangle using that color contains this vertex, and its repeated color does not occur in an older triangle. Repeating this operation proves the all-n bound.

This improves only the displayed additive constant in the report. It proves neither linear growth nor n-O(1), and contradicts neither conjecture. No first-discovery claim is made.

## Other rigorous findings

- g(6)=g(7)=2, with a direct two-color construction and proof. See [Attempt 4](attempts/turn_04.md).
- g(8)=g(9)=3, using the explicit upper constructions and an exact, independently replayed Boolean unsatisfiability certificate for two colors on K_8. The lower bound is computer-assisted.
- Every admissible q-coloring satisfies n<=3q^2+q+1 by deleting representatives of non-rainbow types and obtaining a proper induced clique. This is weaker than the source-announced lower bound. See [Attempt 1](attempts/turn_01.md).
- If every non-rainbow type family lacks a common vertex, then q=Omega(n^(2/3)). The restriction is essential. See [Attempt 2](attempts/turn_02.md).
- If the coloring has a monochromatic cut with both sides of size at least two, then q>=n-4. A common monochromatic neighborhood of two vertices has size at most q+2. Uniformly doubling three different blocks always creates a forbidden pair. See [Attempt 3](attempts/turn_03.md).
- The literal next-step two-vertices-per-new-color recursion tested in Attempt 5 fails on all 24 individually feasible row pairs. This rejects only that stated construction rule, not other four-color K_11 colorings.

## Exact-check reproducibility

Python 3 only; no third-party packages, network access, floating-point optimization, or source documents are needed. Run from this directory:

    python3 checks/verify_results.py

This independently reconstructs and verifies the K_9 type table, checks the K_7/K_9 witnesses and extensions on 10, 12 and 16 vertices, validates the complete K_8 clause encoding by a second enumeration, and replays the 571-node UNSAT certificate without running the search algorithm. The K_8 certificate covers 28 edge variables and 5,600 six-literal clauses, one for each equal-count assignment on each pair of disjoint triangles. The sole symmetry assumption fixes the first edge to color zero, justified by globally swapping the two colors.

Optional reproduction of the bounded searches:

    python3 checks/small_two_color.py
    python3 checks/extend_k7.py
    python3 checks/test_pair_amplification.py

These scripts impose a 30-second limit; the recorded instances completed in under one second each. Successful finite checks are not substituted for the all-n proofs. The 80,080 disjoint triangle pairs in the 16-vertex extension are a consistency check only.

## Remaining gap

Neither an unrestricted Omega(n) lower bound nor an o(n)-color construction was found. The five attempts also do not establish or disprove boundedness of n-g(n). A fixed better seed preserves its deficit under the proved extension operation; an infinite amplification theorem would be needed to make that deficit unbounded. The reports identify their missing steps explicitly.

The manifest freezes only authored research, verifier code, and generated finite certificates. No source PDF, screenshot, corpus dump, or private-context record is part of this packet. Independent mathematical review is still required before publication or a correctness claim beyond the scoped results above.
