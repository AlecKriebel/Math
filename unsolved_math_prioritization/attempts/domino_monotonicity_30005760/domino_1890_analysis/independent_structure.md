# Literal domino class: structural reduction and a low-inversion injection

This is an authored partial result, not a solution of the full fixed-inversion monotonicity problem. The class is exactly

\[
D=\operatorname{Av}(1324)\cap\operatorname{Grid}([\operatorname{Av}(132)\mid\operatorname{Av}(231)]),
\]

with a position split, ungridded counting, and empty cells allowed. Write \(d_{n,k}=|D\cap S_n\cap\{\operatorname{inv}=k\}|\).

## Result

1. For every \(n,k\ge0\) with \(k\le n\), \(d_{n,k}\le d_{n+1,k}\).
2. For \(n\ge k+2\), equality holds: \(d_{n,k}=d_{n+1,k}\).

The first assertion uses the published Linusson–Verkama injection as explicitly restated in Theorems 6.1 and 6.3 of Claesson–Linusson–Ulfarsson–Verkama, *Inversion Monotonicity in Subclasses of the 1324-Avoiders*, arXiv:2604.01143v1, https://arxiv.org/abs/2604.01143v1. The cited statements identify their originals as Theorems 8 and 19 of Linusson–Verkama, *Enumerating 1324-Avoiders with Few Inversions*, Electronic Journal of Combinatorics 32.3 (2025), P3.44. The retrieved 2026 text was inspected at Sections 2 and 6. This note does not independently reprove the published injection.

The second assertion and the auxiliary class reductions below are self-contained. No complete finite basis for D is needed for either assertion.

## 1. A useful subclass inclusion

**Lemma.** \(\operatorname{Av}(1324,4231)\subseteq D\).

**Proof.** Suppose a 1324-avoider has no legal split. Let \(e\) be the earliest ending position of a 132 occurrence, and let \(s\) be the latest starting position of a 231 occurrence. A legal split after position \(t\) is equivalent to \(s\le t<e\), with the obvious conventions when a type of occurrence is absent. Thus failure implies \(e\le s\).

Choose entries \(x,y,z\), in that position order, forming 132 with \(z\) at position \(e\), and entries \(w,v,u\) forming 231 with \(w\) at position \(s\). Hence \(x<z<y\) and \(u<w<v\). The entry \(v\) is after \(z\); if \(v>y\), then \(x,y,z,v\) form 1324. Therefore \(v<y\). The four entries \(y,w,v,u\), in that order, form 4231. This also covers \(e=s\), where \(z=w\). ∎

## 2. Decomposable members and the singleton insertion

Every permutation has a unique decomposition into nonempty sum-indecomposable components. A decomposable 1324-avoider has the unique form

\[
\pi=\alpha\oplus\operatorname{id}_m\oplus\beta,\qquad m\ge0,
\]

where \(\alpha\) is its first component, \(\beta\) is its last component, \(\alpha\) avoids 132, and \(\beta\) avoids 213. All interior components are singletons: an inversion in an interior component, together with an entry in an earlier and a later component, would form 1324. Similarly, a 132 in the first component or a 213 in the last component would extend to 1324. Conversely, these conditions prohibit every possible occurrence of 1324 across components.

**Lemma.** Such a permutation belongs to D if and only if \(\beta\) avoids 4231.

**Proof.** First, membership in D is equivalent to the existence of a split of \(\beta\) into an increasing prefix followed by a 231-avoiding suffix. If a valid split of \(\pi\) occurs before \(\beta\), then all of \(\beta\) avoids 231, so use its empty increasing prefix. If the split occurs inside \(\beta\), every earlier-component entry is below every entry of \(\beta\); an inversion in the included prefix of \(\beta\) would therefore create a 132 in the prefix of \(\pi\). Conversely, combining \(\alpha\), the middle singletons, and an increasing prefix of \(\beta\) produces a 132-avoiding prefix.

It remains to prove that for a 213-avoider \(\beta\), admitting such an increasing-prefix/231-suffix split is equivalent to avoiding 4231. A 4231 occurrence makes the split impossible: to remove its 231 suffix from the right cell, the left cell must include the first two entries of the occurrence, which form a descent. Conversely, take the longest increasing prefix of \(\beta\), of length \(r\). If \(r<|\beta|\), then its last entry \(b\) exceeds the next entry \(c\). Avoidance of 213 forces every entry after \(c\) to lie below \(b\), since otherwise \(b,c\), and that entry form 213. If the remaining suffix contains a 231 occurrence, preceding it with \(b\) yields 4231. Therefore absence of 4231 makes the maximal increasing-prefix split valid. ∎

Define, on decomposable members,

\[
\widetilde f(\alpha\oplus\operatorname{id}_m\oplus\beta)
=\alpha\oplus\operatorname{id}_{m+1}\oplus\beta.
\]

This preserves D and the inversion count, increases length by one, and is injective. Its image consists exactly of the members of D with at least three components. The inverse deletes the second component, which is a singleton. This description applies also when either or both endpoint components are singletons.

## 3. Inversion graphs and cycle rank

The inversion graph of \(\pi\in S_N\) has positions as vertices and an edge \(ij\) for each inversion. Its connected components are exactly the direct-sum components of \(\pi\).

Here is an elementary justification of the nontrivial direction. If \(i<j\) is an inversion edge, each position \(t\) strictly between them is adjacent to at least one of \(i,j\): either \(\pi_t<\pi_i\) or \(\pi_t>\pi_j\). Consequently every connected component occupies an interval of positions. Distinct components have no inversion edges between them, so their value sets are likewise intervals ordered from low to high. They therefore give exactly the sum decomposition.

If \(\pi\) has \(k\) inversions and \(r\) sum components, its graph's cycle rank is

\[
\nu(\pi)=k-N+r\ge0.
\]

In particular \(r\ge N-k\). Every occurrence of a pattern induces its inversion graph on the selected vertices, and cycle rank cannot decrease when passing from a subgraph to the entire graph. The graph of 4231 has four vertices, five edges, and one component, so its cycle rank is two. Therefore

\[
\nu(\pi)\le1\quad\Longrightarrow\quad\pi\text{ avoids }4231.
\]

This is stronger than the special case that a tree inversion graph contains no triangle and hence its permutation avoids 321.

## 4. The published injection and its image components

We invoke exactly these two results, as restated in the cited 2026 source:

- If a 1324-avoider of length n has at most \(2n-7\) inversions, it is decomposable or almost decomposable. Here almost decomposable means indecomposable but made decomposable by deleting one of its first entry, last entry, minimum, or maximum.
- There is one injective map f on the union of all decomposable and almost-decomposable 1324-avoiders. It increases length by one, preserves inversions and 1324-avoidance, and agrees with \(\widetilde f\) on decomposable inputs. The particular boundary-deletion priority is the one specified in the source.

**Image-component observation.** If \(\pi\) is an indecomposable input in the domain of f, then \(f(\pi)\) has at most two components.

Indeed, if the image had at least three components, its second component would be a singleton. Delete that singleton to obtain a decomposable 1324-avoider \(\tau\) of length n. The formula for f on decomposable inputs gives \(f(\tau)=f(\pi)\), contrary to injectivity since \(\tau\) is decomposable and \(\pi\) is not. This argument uses the injection's full 1324-avoiding domain, not an unproved claim that f preserves D in general.

## 5. Proof of monotonicity for k at most n

Assume \(n\ge7\) and \(k\le n\). Then \(k\le2n-7\), so f is defined on every member of \(D\cap S_n\) with k inversions.

For decomposable inputs, Section 2 shows that f preserves D. For an indecomposable input, put \(\rho=f(\pi)\). It has length \(N=n+1\), k inversions, and at most two components. Consequently

\[
\nu(\rho)=k-(n+1)+r\le n-(n+1)+2=1.
\]

Thus \(\rho\) avoids 4231. It also avoids 1324 by the source theorem, so Section 1 implies \(\rho\in D\). Restricting the single global injection f therefore proves \(d_{n,k}\le d_{n+1,k}\) for this range. There are no collisions between decomposable and indecomposable inputs because the source theorem supplies one injection on their union.

The remaining cases \(0\le n\le6\), \(0\le k\le n\), are exhaustively verified by `independent_smallcase_check.py`, with output `independent_smallcase_results.json`. The checker examines every permutation of each size through seven, uses the literal definition of D with every cut including both empty-cell cuts, and counts inversions directly. It does not assume a finite basis or a generating-tree rule. The relevant rows, with entries listed for k=0 through n and unavailable inversion counts treated as zero, are:

- n=0: (1).
- n=1: (1, 0).
- n=2: (1, 1, 0).
- n=3: (1, 2, 2, 1).
- n=4: (1, 2, 5, 6, 5).
- n=5: (1, 2, 5, 10, 16, 19).
- n=6: (1, 2, 5, 10, 20, 31, 48).
- n=7: (1, 2, 5, 10, 20, 35, 58, 89).

These rows establish every required finite inequality. Together with the preceding proof, they establish assertion 1.

## 6. Exact stabilization

If \(n\ge k+2\), every length-n permutation with k inversions has at least two components, so \(\widetilde f\) applies to every member of \(D_{n,k}\). Every length-(n+1) permutation with k inversions has at least three components, and Section 2 gives an inverse on the entirety of \(D_{n+1,k}\). Thus \(\widetilde f\) is a bijection and \(d_{n,k}=d_{n+1,k}\).

A further structural consequence, not needed for the injection proof, is that the limiting inversion series factors as the inversion series of indecomposable 132-avoiders times that of indecomposable (213,4231)-avoiders. Reverse complement identifies the latter with indecomposable (132,4231)-avoiders. The first factor is the partition series. The second is enumerated in Proposition 7.6 of the cited 2026 source. This observation is an exact limiting reduction, not a full-length monotonicity theorem.

## 7. Remaining limitation

No conclusion for the entire range \(k>n\) is established here. In particular, one must not claim that the published f preserves D without restriction: the explicit literal-class obstruction

\[
4723516\longmapsto42835167
\]

has input in D and output outside D (both have eleven inversions). The output contains 25341 in positions 2,3,4,5,6. The independent exploratory script `independent_f_test.py` reproduces this obstruction and agrees with the separate enumeration through size nine. This is an obstruction to transferring that particular injection wholesale, not a counterexample to inversion monotonicity of D.
