# Independent audit: four-deletion/four-insertion neighbors

## Verdict and exact accepted scope

**ACCEPTED, with the named Cooper–Whitlatch characterization as an external theorem.** No mathematical gap or counterexample was found in Sections 2–8 of the reviewed [short-neighbor manuscript](SHORT_NEIGHBOR_THEOREM.md). The accepted claims are:

1. For every successfully pressable symmetric binary matrix A of rank r with more than one successful word, every successful word S has a distinct successful word T with LCS(S,T) ≥ r−4.
2. Consequently every instance with exactly two successful words is connected at the original threshold, in arbitrary ambient dimension.
3. The bound four is sharp, already for a nonsingular 6×6 matrix.

The threshold permits **up to four deletions and up to four insertions**, not four operations in total. This agrees with Conjecture 6, printed p.47 of Bixby–Flint–Miklós, [*Proving the pressing game conjecture on linear graphs*](https://msp.org/involve/2016/9-1/involve-v9-n1-p03-s.pdf), independently inspected for this audit.

The proof does not establish general connectivity. Additional consequences proved in Section 11 below are connectivity with at most three successful words; original-threshold connectivity for nonsingular matrices of rank at most six; and the rank-six extension to a basis of distinct nonzero quotient-coordinate vectors with arbitrary duplicates and zero coordinates. No claim is made for arbitrary ambient rank-six configurations with extra distinct quotient directions.

This is a substantive mathematical review and finite cross-check, not a formal proof-assistant verification or a novelty assessment. The external characterization itself has not been reproved.

## 1. Frozen input and correction history

The complete nine-section manuscript and its supporting mathematical checks were reviewed before this public edition. All six artifacts in its author verification record matched their declared identities. The reviewer did not edit the candidate. This edition preserves the full proof and substantive audit, subject only to the editorial changes described in [publication scope](PUBLICATION_SCOPE.md). The distributed artifacts are identified in [MANIFEST.json](MANIFEST.json).

One wording clarification was requested before freeze: Theorem B should explicitly assume more than one successful word. The frozen version does so. The source's printed page references are also explicit in that version. No substantive proof repair was required.

There is a harmless scope imprecision in the frozen discussion of “more than two” or “three or more” successful words: the no-isolated-word theorem automatically handles exactly three. The originally reviewed text is best read as disclaiming a theorem for the entire unrestricted family of larger languages. This edition clarifies that general connectivity with four or more words remains unproved here. The accepted mathematical argument is unchanged; the precise stronger corollary is recorded below.

## 2. Primary-source verification

The author-hosted [Cooper–Whitlatch manuscript](https://people.math.sc.edu/cooper/uniquely-pressables.pdf) was opened and inspected independently. Its title is *Uniquely Pressable Graphs: Characterization, Enumeration, and Recognition*, dated July 18, 2017. Definition 7 is printed p.10; Theorem 1 is printed p.13. The inspected PDF has 30 pages. The provided research-input PDF has 414,430 bytes and SHA-256 `71f237c935801bdb52b765587a234c3637f7b80210dae1ceeb79c7de8d06ad2f`.

The four conditions used in the candidate match Definition 7: interval supports ending on the diagonal; nondecreasing weights beginning with one; strict growth two columns later when the earlier weight exceeds two; and full-weight propagation after a noninitial odd weight. Theorem 1 identifies that class with connected uniquely pressable ordered graphs.

The translation to the present unit-upper root is sound. Its Gram matrix already admits the identity word. If that full-length word is unique and the graph had two nonempty components, the component subwords could be interleaved in different orders, a contradiction. Nonsingularity excludes zero isolated components. Thus the necessity direction satisfies connectedness; sufficiency comes directly from the theorem. Size one is immediate and size zero is treated separately.

The [arXiv record](https://arxiv.org/abs/1706.07468) and [author-institution publication record](https://pure.gonzaga.edu/p/en/research-outputs/uniquely-pressable-graphs-characterization-enumeration-and-recogn) were also checked. The latter lists the published article in *Advances in Applied Mathematics* 103 (2019), 13–42, DOI [10.1016/j.aam.2018.09.005](https://doi.org/10.1016/j.aam.2018.09.005). The theorem numbering and pages above refer specifically to the inspected author manuscript, not an assumed identical journal layout.

No connectivity theorem from Cooper–Davis is used. The separate [Cooper–Davis arXiv record](https://arxiv.org/abs/1502.07450) has its own version history, including a withdrawn v2; it is not the Cooper–Whitlatch source. No older connectivity assertion is imported into this audit.

Source PDFs and extracted third-party text are research inputs only, excluded from the authored audit payload.

## 3. Rank, ordered roots, and full-state local substitution

At a legal scalar pivot, the current matrix is congruent to diag(1,C+bbᵀ), and the pressed matrix to diag(0,C+bbᵀ). The rank therefore drops by exactly one, so a successful word has length r.

For a nonsingular n×n matrix and a fixed successful order, elimination produces a unique unit-upper U with A=UᵀU. Equivalently, each initial principal minor in that order is one. The column x_j is supported on the first j positions and has final coefficient one.

After pressing the prefix before a contiguous interval I, the full residual restricted to I is U[I,I]ᵀU[I,I]. Pressing all coordinates of I in any successful local order eliminates the same invertible principal block. In block notation, the remaining matrix is D+CᵀB⁻¹C, independently of the scalar elimination order inside B. This equality includes every external coordinate and its cross-terms. The old suffix is consequently legal.

A minimum-length nonunique contiguous root exists because the whole root is nonunique. Its two one-end truncations are unique. For length at most four, any distinct local successful order has deficit at most four. For larger length, the cited characterization applies to both truncations. This is a valid reduction to the overlapping-root lemma; it does not assert that arbitrary noncontiguous changes of a coordinate set lift to full successful words.

## 4. Exhaustiveness of the overlapping-root division

Let the leading truncation H have column weights w_j. Its first noninitial odd-weight index k, if present, is odd, at least three, and forces every later H-column to be full. The trailing truncation forces the final column to be a e₁ plus a suffix of q ones in rows 2 through m.

If q=m−1 and a=1, the full root satisfies all four conditions. If q=m−1 and a=0, even m is the endpoint exchange; odd m with no k remains unique; odd m with finite k is the four-letter relocation. In the last case k≤m−2 because m−1 is even.

For q<m−1, the final column of the trailing root is not full. Hence it and every noninitial trailing column have even weight. A full H-column j≥3 has trailing weight j−1, so only odd j can be full. Once H has a noninitial odd column, its following columns are full; there cannot be a following even index. Thus k is absent or is exactly m−1, with m even in the latter case.

If a=0 and k is absent, H-columns j≥3 are not full. Their unchanged weights and q inherit monotonicity and the two-step growth condition from the trailing root. The initial weight w₂=2 creates no missing strict-growth condition. The complete root is therefore unique.

If a=0 and k=m−1, the trailing penultimate weight is m−2, so monotonicity and q<m−1 force q=m−2. This is precisely the even two-end-block case. If a=1, even m is the second endpoint exchange, and odd m is the inverse-reversal case. Every admissible bit a, final suffix length, parity, and first-odd-weight possibility is covered.

## 5. Endpoint exchange: determinant and parity audit

For T=(m,2,…,m−1,1), all proper prefix sets have the form {2,…,j,m}. The cofactor vector for x₂,…,x_j in the first j rows is z_j: its first entry is one and it annihilates these columns. By triangularity it is unique.

Before k, z_j is the all-ones vector on the first j positions. From k onward it is the all-ones vector on the first k−1 positions. Set d_j=z_j·z_j, α_j=z_j·x_m, and β_j equal to the parity of the tail of x_m beyond j.

Cauchy–Binet gives det Gram(x₂,…,x_j,x_m)=α_j+β_j d_j. The contributing row minors either use all first j rows or replace exactly one of them by a tail row. More than one tail row cannot contribute because the old columns vanish below j. The cofactor normalization is one. Squaring does not change a binary scalar. This also handles j=1.

For the first even case, α_j=1+d_j and β_j≡j, giving 1+d_j(1+j)=1 because d_j is either j mod 2 or zero.

For the second even case, q is even and t=m−q+1 is odd. Before k, α_j=1+L_j and β_j=L_j mod 2, so the determinant is 1+L_j(1+j). Odd j makes the second term zero; even j makes L_j even. If k=m−1, the sole remaining j=m−1 has d_j=0 and α_j=1+(m−t−1)=1. No endpoint or parity exception remains.

The full determinant is one, so the proposed word is successful. It retains the increasing middle m−2 letters and has deficit at most two.

## 6. Even two-end-block exchange: projection audit

Here m is even, k=m−1, a=0, q=m−2. The proposed word is (m−1,m,3,…,m−2,1,2). The first two orthonormal pivot vectors are a=e₁+⋯+e_{m−1} and b=e₁+e₂+e_m.

Each middle x_j has even weight and no e₁ entry. Its residual is x_j+(x_j)₂b. With h=e₁+e_m, this is the old residual after pressing 1,2 plus (x_j)₂h. The vector h is isotropic and perpendicular to the old middle coordinate span, so all middle inner products are preserved. Their new pivot vectors are e_j+λ_jh.

The residual for vertex 1 after the first two presses is e₁+a+b. It has norm one, is perpendicular to h, and has coefficient one at each middle coordinate. It therefore has inner product one with each middle pivot. The number m−4 of those pivots is even, leaving residual norm one. After pressing vertex 1, the remaining scalar pivot is one by nonsingularity.

All claimed projections, pivot norms, and final-rank arguments are valid. The unchanged middle subsequence has length m−4.

## 7. Odd relocation: projection audit

For odd m, a=0, q=m−1 and finite odd k, the first pivots k,k+1,m yield the orthonormal vectors a=e₁+⋯+e_k, b=e_{k+1}, and c=(e₂+⋯+e_m)+e_{k+1}. Their norms and pairwise inner products have the stated parities.

Write h=e₁+c. It is isotropic and has coefficient one on every early-middle position 2,…,k−1. Therefore e_i↦e_i+h preserves dot products on that span: the two cross terms cancel. An early column has even original weight, so the sum of its coefficients after deleting its e₁ component is exactly its original e₁ coefficient. Its image is precisely the claimed projected column. Its pivot vector is thus g_j=e_j+h.

For a late coordinate e_l, l≥k+2, its projection after a,b,c and the early pivots is e_l+c+Σ_{j=2}^{k−1}g_j=e_l+d, with d=e₁+⋯+e_{k−1}. Here k−2 is odd and d is isotropic. Full late columns differ successively by e_l, so the late pivot vectors are e_l+d. These are orthonormal.

Vertex 1 has projection coefficient one against a, every early middle pivot, and every late middle pivot, and zero against b,c. The number of nonzero coefficients is 1+(k−2)+(m−k−2)=m−3, even. Its final norm remains one. The proposed word is therefore successful, including the boundary cases with no late-middle letters. Removing 1,k,k+1,m from both words gives the common subsequence of length m−4.

## 8. Inverse reversal audit

For invertible symmetric B, the kernels of B[S] and B⁻¹[Sᶜ] are isomorphic. If x is supported on S and Bx vanishes on S, then y=Bx is supported on Sᶜ and B⁻¹y vanishes there. The inverse map is y↦B⁻¹y. Thus the two principal submatrices are simultaneously nonsingular.

It follows that a successful word for B reverses to a successful word for B⁻¹. The root V=J U⁻ᵀJ satisfies VᵀV=J(UᵀU)⁻¹J. Its leading and trailing one-end roots are inverse reversals of the opposite truncations of U. Both remain unique. Reversal and relabeling preserve LCS and distinctness.

In the remaining odd case, k is absent. The first m−1 entries of the first row of U⁻¹ are all one. Its final entry is the parity of the first m−1 entries of x_m, namely q=0 mod 2. The last column of V is therefore (0,1,…,1)ᵀ. Since V remains nonunique, the no-k unique alternative is excluded, leaving exactly the odd relocation case already proved. The construction transports back with deficit at most four.

No congruence-invariance assumption about the original coordinate words is used: the word bijection is explicitly inversion plus reversal and relabeling.

## 9. Singular matrices and omitted coordinates: self-contained reconstruction

Let r=rank(A), and let x_v be the image of coordinate e_v in the radical quotient V=F₂ⁿ/ker(A). A successful word S=(s₁,…,s_r) produces an orthonormal basis f₁,…,f_r of V by Gram–Schmidt. Define the full ambient column c_i by c_i(v)=B(x_v,f_i).

Expansion in this basis gives A=Σ_i c_i c_iᵀ. Triangularity gives c_i(s_j)=0 for i>j and c_j(s_j)=1. Hence the exact full state after the first j−1 presses is

M_{j−1}=Σ_{i≥j} c_i c_iᵀ.

For an original nonzero-row vertex v, choose j=max{i:c_i(v)=1}. The set is nonempty because x_v≠0 and the f_i form a basis. Then

M_{j−1}e_v=c_j=M_{j−1}e_{s_j},

and the diagonal at v is one. Pressing v instead of s_j removes exactly the same full rank-one matrix c_jc_jᵀ. Every later full state is unchanged. If v was already in S, its last support index equals its own position, so an omitted v creates no repeated letter and gives a genuine deficit-one neighbor.

Thus every word that omits a nonzero-row coordinate has a neighbor. Otherwise the matrix has exactly r nonzero-row coordinates, since the word has length r. The remaining coordinates are zero and can never become legal. The principal matrix on the nonzero coordinates has rank r and is nonsingular; its successful words coincide with the original words. The full-rank theorem applies.

Equivalently, the last-support layers partition all nonzero-row vertices, and a nonsingleton layer permits a coordinate replacement. The proof is about equality of full matrix trajectories, not merely a selected principal block. It covers isotropic omitted vectors, repeated quotient images, singular matrices, zero coordinates, and differing chosen coordinate sets. Rank zero has only the empty word and never meets the nonunique hypothesis.

## 10. Independent computational checks

The independent checker imports no author search or validation code. Its main success oracle is Gaussian elimination of principal minors and enumeration of nonsingular-principal flags ending at the full matrix rank. This differs from the author's discovery routine, which recursively updates the pressing state. The audit uses direct Schur complements, including all ambient coordinates, for equality of full trajectories. All conditions use explicit exceptions; there are no removable Python assertions.

Complete tested families and exact counts:

- All 33,868 unit-upper roots in orders 0 through 6, including the empty root. Their complete languages contained 1,382,225 successful flags in total. Unique pressability was compared with the cited root class, and every nonunique identity order received a verified local-substitution neighbor. Relabeling reduces an arbitrary chosen successful full-rank order to this identity-root formulation.
- All 30,604 roots in orders 5 through 18 whose two one-end truncations satisfy the characterization. Every nonunique candidate's prescribed exchange was checked by exact principal determinants. Complete word enumeration was additionally performed through order 11. The case counts agree with the author's separate exploratory census wherever compared.
- 174,950 endpoint determinant identities, 1,093 even-block projection cases, and 1,093 direct odd-relocation projection cases. The inverse-odd cases independently verify the transformed root and transported successful word.
- All 33,867 symmetric binary matrices in orders 0 through 5, including singular and nonpressable matrices. Of these, 31,743 were successfully pressable. The check examined all 282,731 successful words, verified 176,898 nontrivial last-support replacements, and checked 132,917 singleton-layer reductions. It also checked all 3,076 exactly-two-word cases. Full Schur-state equality was verified for 2,018 replacements through ambient order four.
- 500 deterministic extra-coordinate fixtures of ranks 1 through 16, each with one through seven additional arbitrary quotient vectors. These included 1,813 nontrivial replacements with full Schur-state comparisons and 437 interval substitutions that retained arbitrary ambient cross-couplings. Seed: 174920261012.
- A separate inverse-complement and fixed-alphabet checker verifies every complementary principal-minor pair and inverse-language bijection for all 1,099 unit-upper roots in orders 1 through 5. It also checks the reversal/nonedge characterization for permutations through order eight.

Negative controls reject a successful proper principal block that does not exhaust the full rank; an invertible alternating matrix with no legal first press; a repeated coordinate; the endpoint determinant formula with its βd term omitted; and reversal without matrix inversion. Degenerate controls verify the singleton empty language at rank zero and the three one-letter words of a rank-one matrix with three identical nonzero coordinates.

The sharp fixture has binary row masks (56,22,14,5,3,1), rank six, and exactly the following successful words (one-based labels):

- (2,5,1,6,3,4)
- (3,4,1,6,2,5)

Their LCS is exactly two, so the deficit is four. It refutes the analogous universal bound of three deletions plus three insertions; it is not a counterexample at the original threshold.

Normal, `-O`, and `-OO` execution results were recorded and checked in the mathematical review. Finite computations support and challenge the symbolic proof; they do not establish its arbitrary-order conclusion by extrapolation.

## 11. Derived corollaries independently verified in this audit

### 11.1 At most three successful words

For a nonunique language the theorem says every vertex of its word graph has a neighbor. A disconnected graph with two or three vertices has an isolated vertex. Hence every successfully pressable instance with at most three successful words is connected at the original threshold, in arbitrary rank and ambient dimension. A single-word graph is connected trivially.

Any counterexample to the general conjecture must therefore have at least four successful words, with every connected component containing at least two. This necessary condition does not prove connectivity for four words.

### 11.2 Nonsingular rank six

Two permutations of the same finite alphabet have no common ordered pair exactly when one is the reversal of the other. Indeed, each pair of letters must occur in opposite order. Thus the graph on any collection of such permutations, joined when LCS≥2, is a complete graph with some disjoint edges removed. With at least three vertices it is connected.

For a nonsingular matrix of order r≥6 with exactly two successful words, those words cannot be reversals: reversal has LCS one, whereas the short-neighbor theorem requires LCS≥r−4≥2. With one word connectivity is trivial. Therefore the LCS≥2 graph is connected for every nonsingular successfully pressable matrix of order r≥6.

When r=6, LCS≥2 is exactly the original four-deletion/four-insertion threshold. Consequently every nonsingular 6×6 instance satisfies the original connectivity conjecture. Combining this with the [already proved arbitrary-ambient rank-at-most-five result](../3100089_positive_connectivity_appendix/STRUCTURAL_LEMMAS.md#4-a-universal-diameter-two-bound-and-the-original-bound-in-rank-at-most-five) gives the nonsingular rank-at-most-six statement. For r>6, the LCS≥2 graph is weaker than the original threshold and yields no general original-threshold connectivity conclusion.

### 11.3 Rank-six basis with duplicates and zero coordinates

Assume the distinct nonzero vectors among the quotient-coordinate images x_v form a basis of the rank-six radical quotient. Equal images mean equal original rows and columns. Every successful word has six independent selected quotient vectors, so it selects exactly one representative from each of the six classes.

The Gram matrix of the six distinct basis vectors is nonsingular. The projected orders are precisely its successful words: the selected scalar pivots agree, and completing six legal pivots exhausts the full ambient rank. Conversely, every successful basis order lifts with any choice of representatives.

Choose one representative per class. The nonsingular rank-six result connects the resulting representative words with LCS≥2. Each original word connects to its representative word by changing one duplicate representative at a time; equal quotient vectors give the same full-state transitions, and each such step retains five letters. Zero coordinates are never pressed.

This proves original-threshold connectivity for arbitrary ambient rank-six matrices whose distinct nonzero quotient-coordinate images form a basis, allowing unlimited duplicates and zero coordinates. The argument does not cover extra distinct quotient directions beyond that basis.

## 12. Remaining limitations

The accepted theorem rules out isolated successful words, not distinct nontrivial connected components. The derived rank-six result uses a common basis alphabet or duplicate classes of such an alphabet; it does not provide an arbitrary coordinate-set exchange theorem. No ordered-flag lifting from unordered matroid exchange, no unrestricted orthogonal-basis interpolation, and no general connectivity theorem is being assumed.

The mathematical acceptance concerns the complete argument reproduced in this edition. The distributed texts are identified by the public manifest. Any later mathematical modification requires review of the changed material. General connectivity remains unresolved by this work.
