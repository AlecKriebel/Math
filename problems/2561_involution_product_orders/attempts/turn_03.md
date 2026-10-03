# Attempt 3: exact small-class counterexample search and extension certificates

Date: 2026-10-03. Third substantive attempt. Goal: find a color symmetry not respecting conjugation, outside the already settled characteristic-two transvection family. This is a modest exact search, not a large exhaustive search over groups. Six complete class graphs, at most105 vertices, were used.

## Exact finite criterion and exhaustive algorithm

For an explicit involution class D={d_0,...,d_{m-1}}, form two tables:

    M[i,j]=order(d_i d_j),
    C[i,j]=index(d_i d_j d_i).

The first includes diagonal color1. It determines the colored graph. The second records conjugation. By Attempt1, a permutation f extends exactly when

    f(C[i,j])=C[f(i),f(j)] for all i,j.

Since L acts transitively on D and its conjugations already extend, it is enough to test every M-automorphism fixing vertex0. We exhaust that stabilizer by paired partition refinement. Corresponding cells of two copies of the graph are split using the complete count vector of each edge color into each current cell. Any isomorphism must preserve these signatures, so incompatible branches can be rejected. When a cell is not singleton, fix its first source vertex and try every target in the paired cell. This partitions the remaining possible bijections with no omissions. At a discrete partition, directly check every entry of M and every entry of C. Thus refinement is only a safe pruning device, not an assumed completeness oracle.

The standard-library program checks closure of conjugation in D, injectivity of the involution-to-conjugation action, each accepted color isomorphism, and each accepted conjugation identity. No external group package or numerical tolerance is used.

## Results, all complete

- A5, double transpositions:15 vertices; colors2,3,5; stabilizer8; full graph group120.
- A6, double transpositions:45 vertices; colors2,3,4,5; stabilizer32; full graph group1440.
- PSL2(7), involutions:21 vertices; colors2,3,4; stabilizer16; full graph group336.
- PSL2(11), involutions:55 vertices; colors2,3,5,6; stabilizer24; full graph group1320.
- A7, double transpositions:105 vertices; colors2,3,4,5,6; stabilizer48; full graph group5040.
- A8, fixed-point-free involutions:105 vertices; colors2,3,4; stabilizer384; full graph group40320.

Every enumerated stabilizer automorphism satisfies every conjugation identity. Hence these exact finite instances satisfy21.52. A6's group order1440 correctly includes its exceptional outer automorphisms: testing only permutations of six underlying letters would have missed half the graph symmetries.

Runtime of the six searches was about53 seconds total; the largest had709 search nodes. The search sizes are tiny compared with all105! vertex permutations. No run hit its node/time limit; limits would be recorded as incomplete rather than counted as a certificate. Machine-dependent seconds are not mathematical output.

## Construction correctness

For A_n the class is generated directly from all matchings on subsets of the required support size, not by sampling. The listed cycle types are even and do not split into two A_n conjugacy classes: centralizing a transposition from one of the matched pairs is an odd permutation. For PSL2(p), p=7,11, we enumerate determinant-one trace-zero2x2 matrices modulo signs through their faithful projective-line action. A noncentral lift of a projective involution squares to-I and has trace0; conversely every enumerated matrix gives a projective involution. The familiar unique involution class can also be seen by conjugacy of matrices with polynomialX^2+1 in PGL2 and splitting the determinant of a conjugator by a centralizer element; the determinant norms from the quadratic centralizer are surjective. Thus these are full classes, not selected subgraphs.

## What the search does not show

No counterexample was found in these six classes. This is not evidence of a universal theorem by extrapolation. The checker is a transparent computational proof of the stated instances only, and must be independently replayed/audited before acceptance. It does not test all A8 involutions (the other class has210 vertices), higher alternating groups, other Lie-type families, or sporadic groups. Historical novelty is not asserted; these small automorphism groups are natural classical objects, and related graph results predate the Notebook question.

The next attempt seeks a structural sufficient criterion recoverable from one vertex's commuting neighborhood, rather than increasing the brute-force range.
