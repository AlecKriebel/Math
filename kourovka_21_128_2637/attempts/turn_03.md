# Turn 3 of 5: reject a concrete minimal-Euler-index common-cover candidate

## Target and result
Turn 1 makes relative indices (42,5) the first possible pair for a common subgroup of K_F and K_H. Construct a natural five-sheet subgroup V of K_H and test it against the transfer obstruction from turn 2. The answer is b1(V)=0. Thus this V is not isomorphic to any finite-index subgroup of K_F, including one of index 42. This does not classify all five-sheet subgroups of K_H.

## Explicit permutation certificate
Use the set Omega=(Z/60)x{0,1,2,3,4}, of size 300. The following four permutations of five letters are written as image lists:

g1=[0,1,2,3,4],
g2=[1,2,3,4,0],
g3=[0,2,1,4,3],
g4=[2,1,0,4,3].

For each generator si of G_H, define its action T_i on Omega by

T_i(l,x)=(l+1, g_i^{-1}(x)) when l is even,
T_i(l,x)=(l+1, g_i(x)) when l is odd.

Here l+1 is taken modulo 60. The use of parity is well-defined because 60 is even. Each T_i is invertible. Direct exact permutation multiplication verifies every defining braid relation of the 5-3-3 Artin presentation and the central relation (s1 s2 s3 s4)^15=1. These are all seven relators used in the group presentation, so the action defines a homomorphism G_H -> Sym(Omega). The supplied code uses a right-action convention: traverse a word from left to right, applying the next displayed permutation to the current point.

The orbit of (0,0) has all 300 points. Its stabilizer V therefore has index 300 in G_H. Every word of length sum a moves the first coordinate by a mod 60, so an element fixing (0,0) is in K_H. Since [G_H:K_H]=60, [K_H:V]=5. Torsion-freeness follows from V<=K_H; no appeal to finite permutation-group torsion-freeness is made.

The construction is motivated by the two A5 factors in the projective H4 Coxeter quotient, but its validity depends only on the displayed permutations and the verified presentation relations, not on an identification of that quotient.

## Exact rational homology via a modular maximal-rank certificate
Lift the seven relators at every point of Omega. The resulting presentation-cover chain complex has

C0=Q^300, C1=Q^1200, C2=Q^2100.

The graph is connected, so rank_Q(d1)=299. The script verifies d1*d2=0 over Z. Thus rank_Q(d2)<=1200-299=901.

Sparse Gaussian elimination modulo the prime 101 gives rank_F101(d2)=901. A nonzero 901-square minor modulo 101 is also nonzero over Q, so rank_Q(d2)>=901. Combining both bounds proves rank_Q(d2)=901, and therefore

b1(V)=1200-299-901=0.

This use of modular arithmetic is a proof of rational vanishing, not a probabilistic rank estimate: the modular rank equals the independent upper bound. The deterministic script checks closure of every lifted relator, connectedness, and all column boundary sums, then computes the rank. It does not claim an integral homology calculation.

Reproduce with: python checks/five_sheet_h4.py.

The complete image lists, ranks, field prime and scope limitation are stored in checks/five_sheet_h4_results.json.

## Obstruction and exact remaining gap
Every finite-index U<=K_F has b1(U)>=3 by turn 2. Consequently V cannot be such a U up to isomorphism. Its Euler characteristic is -210, exactly equal to that of a hypothetical index-42 subgroup of K_F, so this calculation demonstrates that the Euler index equation alone can admit a candidate that homology then rejects.

What remains is not merely the computation of this V: an arbitrary common subgroup may correspond to a different index-five subgroup or to relative indices (42s,5s) with s>1. Nothing here excludes those cases. Further finite-index subgroups of V may have positive first homology.
