# Turn 5: the squarefree balanced-network obstruction is not just series-parallel

Substantive author turn **5/5**, 2026-10-02. The final attempt tested whether a non-series-parallel network could supply the missing squarefree multipliers. A Laplacian argument proves that no terminal-proper unit-edge network can do so. This is an obstruction to that multiplication method, not a counterexample to the original knot conjecture. The five-turn author budget is now exhausted with the original problem unresolved.

## 1. The theorem

Let N be a finite connected loopless undirected multigraph with distinct terminals s,t. Edges have unit conductance; parallel edges are counted separately. Let T be its spanning-tree count and S its two-component spanning-forest count separating s from t.

**Theorem.** If T=S=g is squarefree, then N has a unique edge joining s directly to t and this edge is a bridge. In particular, if every edge and vertex of N lies on a simple s-to-t path, then N is a single edge and g=1.

Thus no terminal-proper network of any graph type, planar or nonplanar, can be balanced with a squarefree common count g>1. Unlike turn4's proof, this does not assume series-parallel decomposition.

## 2. Exact Laplacian setup

Ground vertex t and let A be the reduced Laplacian, of order d=|V(N)|−1. It is a positive-definite integer symmetric matrix, and det A=T=g by the matrix-tree theorem. Write e_s for the source coordinate vector. Adding one extra edge between s,t changes A to A+e_s e_s^T. The determinant lemma and deletion/contraction give respectively

    det(A+e_s e_s^T)=det A+adj(A)_{ss},
    T(N+st)=T(N)+S(N).

Therefore adj(A)_{ss}=S=g. Let h=A^{-1}e_s and extend it by h_t=0. Then

    h_s=1,    Ah=e_s.                            (16)

This is the unit-current potential, but the proof needs only the displayed integer matrix equations.

## 3. Squarefree determinant forces integrality of this potential

For each prime ℓ dividing g, the matrix A modulo ℓ has rank exactly d−1. To see this, the Smith normal form expresses det A as a product of invariant factors. Since ℓ occurs to exponent exactly one in g, exactly one invariant factor is divisible by ℓ, and the rank drops by exactly one. Consequently adj(A) modulo ℓ is nonzero of rank one. It is symmetric because A is symmetric.

Over any field a nonzero symmetric rank-one matrix has the form c vv^T for some c≠0 and nonzero vector v. For example, write it as xy^T and use symmetry to conclude that x and y are proportional. Thus the congruence adj(A)_{ss}=g≡0 modℓ implies v_s=0, and the entire s-th column of adj(A) vanishes modulo ℓ. Since g is squarefree, divisibility by every ℓ|g implies

    g divides adj(A)_{js} for every j.

Hence h_j=adj(A)_{js}/g is an integer for every j. If g=1, the same conclusion is immediate and needs no prime divisors. The argument also covers a one-by-one reduced Laplacian in the cases where its hypotheses can hold.

## 4. The integer maximum principle identifies the graph cut

At every vertex v other than s,t, equation(16) says

    Σ_{w adjacent to v}(h_v−h_w)=0,

with multiplicities. The finite maximum principle and boundary values h_s=1,h_t=0 give 0≤h_v≤1: an interior strict maximum above1 or minimum below0 would propagate to all neighbors and then to a boundary vertex, contradicting connectedness. By integrality every h_v is0 or1.

An internal vertex of value1 can have no neighbor of value0, since every summand in its Laplacian equation is nonnegative. An internal vertex of value0 likewise can have no neighbor of value1. Thus every edge crossing between the two potential levels must join s directly to t. The source equation in(16) counts these edges and equals1, so there is exactly one such edge. Removing it separates the nonempty level sets, proving it is a bridge.

A simple path from s to t must cross that bridge at s itself. It cannot first leave s into the same-level part and return to s, because then it would repeat s. Similarly it cannot make an excursion beyond t. Its only possible edges are therefore the single bridge st. If every graph edge and vertex belongs to some simple s-to-t path, there can be no others. Thus N is a single edge and T=S=1, completing the proof.

## 5. Why omitting terminal properness would lose primeness

For any prime p≥3, attach a p-cycle at s and add a bridge st. This network has T=S=p: the cycle contributes p tree choices and the separating forest is obtained by omitting st. Its effective terminal conductance is unchanged from a single edge. It therefore looks like a square multiplier in the tree/forest formula, but every edge of the attached cycle is outside every simple terminal path. Substituting it into a knot's checkerboard graph creates an attached block at a cut vertex. The prime-diagram hypothesis fails; this is the graph version of an inadmissible connected-sum shortcut.

By contrast, turn4's networks with T=S=q² are terminal-proper and preserve the no-cut-vertex condition. Their nonsquarefree count is consistent with the theorem. The squarefree assumption is essential to the arithmetic proof and no extension to arbitrary nonsquarefree g is asserted.

## 6. Final research disposition

The strongest constructive result is the existence of a prime alternating achiral knot of determinant5p^{2e} for every odd prime p and e≥0, together with the primitive-case fourth-power extension and the earlier explicit quadratic family. The four-parameter integer-wheel obstruction is overcome on the prime ray by rational substitutions, so its missing values must never be called knot counterexamples. The new general network obstruction closes the most direct route to multiplying by arbitrary squarefree squares while keeping effective edge conductance unchanged.

The remaining gap is a construction for arbitrary odd sums of two squares outside the stated classes, particularly mixed squarefree bad-prime factors with a general primitive core. A non-balanced substitution, different embedded graph, or another knot construction may still resolve that gap. No full proof, full counterexample, multiplicative closure for arbitrary prime knots, or first-priority claim has been established. **Original Problem12.25: unresolved5/5.**
