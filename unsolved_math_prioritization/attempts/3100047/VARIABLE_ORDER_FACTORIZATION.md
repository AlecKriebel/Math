# Exact factorization along variable-order blocks

Problem: row1747 / 3100047 / AMR-030-0047. Date:12 October2026 UTC.

This is a self-contained structural reduction for nonsingular, successfully pressable symmetric matrices over F_2. It neither proves nor disproves the unrestricted full-length 1/3–2/3 conjecture. No novelty claim is made.

Let A be symmetric and nonsingular on a finite nonempty labeled set E. Let Sigma(A) be its nonempty set of successful pressing permutations, with the uniform distribution. A legal press at v updates the current matrix M to M+(Me_v)(Me_v)^T and requires M_vv=1. For distinct x,y define p_A(x,y)=Pr(x precedes y).

Define the variable-order graph V(A) on E by joining x,y when 0<p_A(x,y)<1. Let its connected components be C_1,...,C_t, initially without an ordering.

**Theorem.** There is a unique order on these components such that every successful word concatenates one ordering of C_1, then one of C_2, and so on. Put S_i=C_1 union ... union C_(i−1), and let B_i be the principal submatrix on C_i of the Schur complement of A[S_i] in A, with B_1=A[C_1]. Then every B_i is symmetric, nonsingular and successfully pressable, and concatenation gives the exact bijection

Sigma(B_1) × ... × Sigma(B_t)  →  Sigma(A).

In particular, under the uniform measure the component words are independent and uniformly distributed. Every cross-component precedence probability is 0 or1, and every within-component probability is exactly that of B_i.

## Proof

First, the fixed block order uses only the permutation family, not pressing. If z lies outside the component of a variable edge uv, its comparisons with u and v are each fixed, since otherwise z would join that component. Those fixed comparisons must place z before both or after both. The alternative u<z<v would force u<v in every word, contradicting variability of uv; the alternative v<z<u gives the opposite contradiction. Propagating along a variable-edge path shows that any outside vertex lies uniformly before all or after all of a component.

For two distinct components C,D, this argument first fixes the relation of each vertex of D to all of C, and then propagates along paths in D, so either all of C precedes all of D in every word, or the reverse. Take any one successful word: its order on the components supplies a total order that then holds in every word. In particular, each component is a contiguous block. This also proves uniqueness of the block order.

We next record the needed exact state property. If S is the set of a legal pressing prefix, then A[S] is nonsingular and, after removing its cleared coordinates, the state on E\S is

R_S = A[E\S] + A[E\S,S] A[S]^{-1} A[S,E\S].

Here is a direct derivation. Put the labels in S first, in their pressing order, and write A=[[P,Q],[Q^T,R]]. Make the current update columns for these presses the rows of a rectangular matrix U=[U_S,U_T]. Cleared earlier coordinates and unit pivots make U_S unit upper triangular. The pressing updates subtract U^TU (equivalently add it in F_2), and all rows and columns in S are then zero. Hence P=U_S^TU_S and Q=U_S^TU_T. In particular P is nonsingular, U_T=U_S^{-T}Q, and U_T^TU_T=Q^T P^{-1}Q. The remaining block is therefore R+Q^TP^{-1}Q, as asserted. This includes the empty prefix with no updates. Thus R_S depends only on the set S, not its successful ordering.

Because every successful word has prefix set S_i at its ith boundary, A[S_i] is nonsingular. The same applies to S_i union C_i. The determinant factorization by this Schur complement gives

det A[S_i union C_i] = det A[S_i] det B_i =1,

so B_i is nonsingular. Symmetry is preserved by Schur complements. The ith block in any successful word presses B_i legally to zero, since its internal pivots depend only on the principal restriction B_i; it uses all |C_i| vertices. Thus Sigma(B_i) is nonempty.

Now fix all other blocks of any successful word and replace block i by any word tau in Sigma(B_i). Every press of tau is legal in the full residual state: its diagonal on C_i is precisely the diagonal obtained by performing the same updates on the principal restriction B_i. Interactions with vertices outside C_i do not enter that diagonal computation. After pressing all of C_i, the full remaining state is R_(S_i union C_i), independently of the selected tau, by the exact state property. Consequently the unchanged suffix remains legal and successful. This proves that every coordinate of the block tuple can be varied freely and independently.

Conversely, every full successful word already has the fixed component order, and its block restrictions are in the respective Sigma(B_i), as shown above. Hence concatenation is a bijection, proving both the Cartesian product and the claimed uniform-distribution factorization. QED.

## Consequences for balance and computational scope

For a nonempty full-length pressing family define

delta(A)=max_(x!=y) min(p_A(x,y),1−p_A(x,y)),

using delta(A)=0 for a singleton ground set. The factorization gives the exact identity

delta(A)=max_i delta(B_i).

Also |Sigma(A)|=product_i |Sigma(B_i)|. Every nonsingleton component contains a variable pair and hence has at least two successful local words. Therefore, if A has more than one successful word and fails the 1/3–2/3 assertion, at least one B_i is a smaller or equal nonunique counterexample. In particular, a vertex-minimal counterexample has connected variable-order graph, a stronger restriction than merely having no universally forced first or last letter.

The variable-order graph of each B_i is exactly the corresponding connected component of V(A), since all within-block probabilities are preserved. Thus this is a genuine reduction to variable-order-connected matrices, rather than a repeatedly enlarging or merely conditional decomposition.

If the conjecture has been rigorously checked for all full-rank pressable matrices of order at most N, then every full-rank pressable matrix whose variable-order components have size at most N satisfies it. This implication is conditional on that separate finite verification; this note does not assert that any particular numerical bound N has been verified. It licenses removing forced or otherwise fixed-order padding from larger searches without changing the probability issue.

## Verification boundary

The proof above is the mathematical argument. The separately retained authored verifier checked the complete state and product statements on explicitly listed and deterministically seeded examples, including forced-prefix/forced-suffix padding with nonsingleton variable cores; VERIFICATION.json records the aggregate check scope. No executable verifier or full per-case record is distributed in this public prose edition. Those checks do not replace the proof or establish the general balance conjecture. No source-author code, copied third-party text, singular omitted-vertex convention, repository mutation, or external publication is involved.
