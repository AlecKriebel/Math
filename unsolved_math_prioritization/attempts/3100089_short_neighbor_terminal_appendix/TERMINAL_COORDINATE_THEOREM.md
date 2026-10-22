# Terminal black coordinates and necessary component-separation signatures

## Status and scope

This note proves a sharp terminal-position theorem for arbitrary successfully pressable symmetric binary matrices. It then derives an explicit necessary coordinate pattern for two distinct components of the successful-word graph at the auxiliary threshold LCS at least two.

It does not prove the general Bixby–Flint–Miklós conjecture, one-vector component preservation, or connectivity at LCS at least two in arbitrary rank. No novelty claim is made. The original conjecture uses LCS at least r−4, meaning four deletions and four insertions.

All matrices and vectors are over F₂. Pressing a diagonal-one coordinate v replaces A by A+(Ae_v)(Ae_v)ᵀ. A successful word clears the entire matrix. Write d=diag(A) and r=rank(A).

We use the accepted full-state trajectory/fiber and last-support replacement results in the published [full-state trajectory and last-support replacement lemmas](../3100089_positive_connectivity_appendix/STRUCTURAL_LEMMAS.md). We also use the established existence theorem that a bicolored graph with a black vertex in every nontrivial connected component has a successful pressing word. Isolated white vertices may be ignored. This is Theorem 4 of Bixby, Flint, and Miklós, *Proving the pressing game conjecture on linear graphs*, Involve 9:1 (2016), in the publisher PDF https://msp.org/involve/2016/9-1/involve-v9-n1-p03-s.pdf. Only this existence theorem is imported; no external connectivity result is used.

## 1. A sharp theorem for a black coordinate forced to the end

**Theorem 1.** Suppose A has a successful word and A_vv=1. The following are equivalent:

1. In every successful word containing v, the letter v is last.
2. Ae_v=d.
3. The quotient image x_v is the canonical vector w characterized by B(w,z)=B(z,z) for every z in the radical quotient.

If Ae_v≠d, the proof constructs a successful word that contains v and has at least one subsequent letter. A black coordinate can always be included in a successful word, by last-support replacement, so assertion 1 is not vacuous.

### The easy implications

In any orthonormal trajectory basis f₁,…,fᵣ, the canonical vector is w=Σfᵢ. Thus a coordinate representing w has coefficient one at every position. Its last-support layer is r in every trajectory, and it can occur only at the final position. The column identity Ae_v=d is precisely B(x_v,x_u)=B(x_u,x_u) for every original coordinate u. Since the coordinate images span the quotient, this is equivalent to x_v=w.

### Constructing a nonterminal occurrence when Ae_v≠d

Set c=Ae_v and H=A+ccᵀ, the full matrix obtained by legally pressing v. Its diagonal is d+c. Because Ae_v≠d, H has at least one diagonal-one coordinate. The row and column of v in H are zero.

Let C be the union of all nontrivial all-white connected components of H. Thus H[C] is alternating, and H has zero cross entries between C and its complement O. The coordinate v belongs to O. Put b=c|C and z=c|O. Since A=H+ccᵀ,

- A[C]=H[C]+bbᵀ and diag(A[C])=b;
- A[C,O]=bzᵀ;
- z_v=1.

The principal matrix A[C] is successfully pressable. To justify this carefully, suppose an off-diagonal connected component K of A[C] had all diagonal entries zero and a nonzero row. Then b is zero on K. Its entries within K and from K to C\K are consequently the same in A[C] and H[C]. Its entries to O are zero because the cross block is bzᵀ. Hence K would be a nontrivial all-white component of the original A. Such a component cannot be changed by presses in other components and has no legal first press, contradicting successful pressability of A. Therefore every nontrivial component of A[C] has a black vertex, and the cited existence theorem applies. Isolated white coordinates cause no difficulty.

Choose any successful word U=(u₁,…,u_q) on A[C]. Perform these same presses in the full matrix. At each stage, let B be the current C-by-C block. Inductively the cross block is diag(B)zᵀ. Indeed, this is true initially; if p is the next legal C pivot, its cross row is zᵀ because B_pp=1. Pressing p replaces the cross column factor diag(B) by diag(B)+Be_p, exactly the new diagonal. Simultaneously it adds zzᵀ to the O-by-O block.

Consequently all U presses remain legal in the full matrix, and after j of them the O block is A[O]+(j mod 2)zzᵀ. At the end the C block and its cross block are zero.

There are two cases.

**q even.** After U, the O block is still A[O]. The coordinate v is black, with column z on O. Press v. The remaining O block becomes A[O]+zzᵀ=H[O]. Thus the prefix (U,v) leaves exactly H[O], with C cleared.

**q odd.** Replace the final letter u_q of U by v. Just before that final press, q−1 is even, so the O block is A[O] and v is black with column z on O. On C, the column of v is diag(B), because z_v=1. The successful final press u_q clears the entire remaining C block, so B=(Be_{u_q})(Be_{u_q})ᵀ; taking diagonals gives diag(B)=Be_{u_q}. Hence the full columns of v and u_q are identical: both equal (diag(B),z). Replacing u_q by v is legal and gives precisely the same full next matrix. The prefix (u₁,…,u_{q−1},v) therefore leaves exactly H[O], with C cleared.

In both cases the remaining H[O] has no nontrivial all-white connected component, by the definition of C. It is pressable by the cited existence theorem. Moreover it has a black coordinate, because H had one and C contains only white coordinates. Hence every successful continuation on H[O] is nonempty. Appending one gives a successful full word in which v is not last. This proves the contrapositive of 1⇒2 and completes the theorem.

The case C empty is covered by q=0: press v first, then complete the nonzero pressable H. The construction never presses any coordinate twice: C and O are disjoint, v is isolated after its press, and the continuation is chosen from the remaining full state.

## 2. Consequences and boundary cases

The canonical vector has norm r modulo two. Thus a black coordinate forced to be last can occur only in odd rank. In even positive rank, every initially black coordinate occurs nonterminally in at least one successful word.

In rank one, every black coordinate represents the canonical vector and every successful word has one letter, so all three assertions hold. In rank zero there is no black coordinate to which the theorem applies.

The black hypothesis is essential. In the unique-word path configuration x₀=e₀ and xᵢ=eᵢ₋₁+eᵢ for i≥1, the final coordinate is initially white and is forced to the final position, yet does not represent the canonical vector in general.

## 3. A necessary signature for separation at LCS at least two

Let r≥3. Define K₂(A) to have all successful words as vertices, with an edge between distinct words when LCS is at least two. This auxiliary graph uses a rank-dependent deletion allowance r−2. In rank six its edge condition coincides with the original BFM condition; in other ranks the two thresholds should not be conflated.

Fix a successful first label a, and suppose a word T belongs to a component D of K₂(A) different from the component containing words starting with a.

First, all words starting with one fixed successful first label b belong to a single K₂(A) component. After pressing b, the successful suffixes have rank r−1≥2. The accepted shared-letter diameter-two theorem connects these suffixes by edges retaining one letter; prepending b supplies a second common letter.

Second, every successful word that contains a before its last position belongs to the a-first component. If such a word has a later letter t, take any word starting with a. The residual coordinate of t after a is nonzero: otherwise x_t is 0 or x_a, making it impossible for both a and t to appear in one successful word. Last-support replacement within the suffix of the a-first word inserts t there. The resulting a-first word shares the ordered pair (a,t) with the given word.

Let f₁,…,fᵣ be the orthonormal trajectory basis of T, and write

x_a=Σ cᵢfᵢ.

Last-support replacement inserts a into T without leaving its component, since it preserves r−1≥2 positions. Hence cᵣ=1: any earlier last-support position would create a nonterminal occurrence of a in D.

Now fix a nonempty proper prefix of T, of length k. Every successful completion of that prefix is in D, because all share T's first label. Thus in the residual matrix a can only occur last. Whenever its residual norm is one, Theorem 1 says that its residual quotient vector is canonical. In the fixed residual basis this gives the implication

Σ_{i>k} cᵢ=1  ⇒  c_{k+1}=⋯=cᵣ=1,     1≤k<r.          (★)

Since a is initially black, Σcᵢ=1. It is not the global canonical vector: a successful word starts with it and r≥3, whereas a canonical coordinate can occur only last.

**Proposition 2.** Under this component-separation hypothesis, the coordinate string of a in every D trajectory has exactly one of these forms:

- (0,1,…,1), possible only when r is even; or
- (1,0,…,0,1,…,1), with a nonempty zero run and a positive even-length final run of ones.

**Proof.** The all-ones string is excluded as just explained. Let j be its last zero. If j=1, all later entries are one, and initial odd norm forces r even. If j≥2, every suffix beginning at positions 2 through j contains a zero, so (★) forces each of those suffixes to have even parity. Taking differences shows c₂=⋯=c_j=0. The suffix beginning at j consists of its zero followed by r−j ones, so r−j is even. Finally initial odd parity forces c₁=1. Since cᵣ=1, the final even one-run is positive. ∎

For rank six there are only three possible signatures:

011111, 101111, 100011.

For odd r, in particular, any successful first labels drawn from different K₂(A) components have inner product one. For even r, a cross-component pair with inner product zero must sum to the global canonical vector, by the first signature.

The signatures are necessary conditions only. We have not shown that they contradict simultaneous realizability of two components.

## 4. Exact residual for the original task

For rank six, it remains to exclude two K₂(A) components whose cross-component successful first labels satisfy Proposition 2 in every opposite trajectory. The theorem does not yet supply that exclusion.

For arbitrary rank, the original problem still asks for connectivity at LCS at least r−4. The universal one-norm-one-vector component-preservation statement remains equivalent to that conjecture via the accepted [coordinate-rich connectivity theorem](../3100089_positive_connectivity_appendix/INTER_FIBER_LEMMAS.md#3-connectivity-when-every-norm-one-quotient-vector-is-a-vertex). Nothing here removes arbitrary synthetic-letter excursions, and there is no bounded projection assertion.

The terminal-coordinate theorem and separation signatures are rigorous structural restrictions, rather than finite evidence extrapolated to a full solution.

## 5. A constructive bounded bridge when the signature fails

The proof of Proposition 2 also yields a positive statement. Fix successful words S,T of rank r≥3 and let a be the first letter of S. If the coordinate string of x_a in T's trajectory is not one of the two exceptional forms in Proposition 2, then S and T are joined by a path of at most four K₂(A) edges.

If a's last-support position is less than r, replace that position in T by a. This costs at most one edge and produces a nonterminal occurrence. Otherwise, the failure of the signature gives a nonempty proper prefix after which a has norm one but is not canonical. Apply Theorem 1 to that residual matrix and prepend the fixed prefix, obtaining a word W containing a nonterminally. Both T and W have the same first label, so the shared-letter diameter-two construction on their suffixes connects them using at most two K₂(A) edges.

Choose a letter t after a in W. Replace a suitable suffix position of S by t using last-support replacement, obtaining S′. Then W and S′ share (a,t), while S′ and S differ in at most one position. Thus at most two more edges finish the path. If T already starts with a, the fixed-first-letter diameter-two bound applies directly. Repeated vertices or identity steps may simply be omitted.

This is a bound for the auxiliary two-common-letter graph, not a four-deletion/four-insertion bound in ranks greater than six.
