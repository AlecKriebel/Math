# Full-length pressing balance: structural reductions and bounded theorems

Problem: row 1747, 3100047 / AMR-030-0047. Research date: 12 October 2026 UTC.

## Outcome and exact scope

The general 1/3–2/3 conjecture is **not resolved here**. This report proves structural reductions, the balance assertion for the autonomous/V-poset subclass (using a clearly identified primary-source characterization as an external input), and exact obstructions to several tempting reductions. No novelty claim is made. It does not claim a counterexample to the full-length conjecture and does not transfer singular-matrix omission conventions to that conjecture.

Throughout, A is a symmetric nonsingular n by n matrix over F_2, n>=2, with at least one successful pressing word. A legal press of i has current diagonal M_ii=1 and replaces M by M+(Me_i)(Me_i)^T. Every successful word is a permutation of the n vertex labels, because each press lowers rank by exactly one. Write Sigma(A) for this finite nonempty set, use its uniform distribution, and put p_A(x,y)=Pr(x precedes y). A balanced pair has p_A(x,y) in [1/3,2/3]. Only nonunique Sigma(A) is at issue.

Main bounded conclusions:

1. The successful words partition into disjoint instructional-Cholesky classes, each exactly a linear-extension family. Those classes are precisely the components under legal adjacent transpositions, and also under two-total-edit one-letter relocations.
2. If there is only one such class, the conjecture holds. The external Cooper–Gartland–Whitlatch characterization reduces this case to V-posets; the balance proof for that recursively defined class is elementary and supplied below.
3. Reversing words gives a bijection Sigma(A) to Sigma(A^{-1}); hence p_A(x,y)+p_(A^{-1})(x,y)=1. If A=A^{-1}, every distinct pair has probability 1/2.
4. Principal-nonsingular subsets form a symmetric-exchange system, but their flags need not form a greedoid or a single poset-extension family. Explicit nonsingular examples demonstrate both failures.
5. Any counterexample must have a transitive strict >2/3 majority order. A vertex-minimal counterexample is connected, has no universally forced first or last vertex, and has at least two instructional classes. These are necessary conditions, not a proof that no counterexample exists.

No computational search for a general counterexample is a prerequisite of these conclusions.

## 1. Primary-source boundary

The direct probability-question source is Joshua Cooper's author-maintained *Combinatorial Problems I Like*, Matroids/Lattices/Posets section: https://people.math.sc.edu/cooper/combprob.html . It asks whether nonuniquely pressable graphs have a pair whose precedence probability is between one third and two thirds. The linked Cooper–Whitlatch paper, https://arxiv.org/abs/1706.07468, concerns unique pressability; it is not substituted for the direct probability statement. The source wording does not settle how to compare omitted vertices in singular cases. We avoid that ambiguity by the full-rank hypothesis.

A relevant additional primary source is Joshua Cooper, Peter Gartland, Hays Whitlatch, *A New Characterization of V-Posets*, https://arxiv.org/abs/1810.07276 . The official metadata identifies v2, revised 14 November 2018. The downloaded v2 PDF displays a typeset date of 3 May 2019; that is not treated as a later arXiv revision. An author-hosted snapshot, https://people.math.sc.edu/cooper/VPosets.pdf, instead displays 16 October 2018. These distinct byte streams are pinned separately in SOURCE_METADATA.json.

Relevant v2 locations (physical pages, starting at 1): pages 2–3 define full rank and instructional Cholesky roots/posets and expressly restrict the poset discussion to full rank; page 5 contains Lemma 4 and Definition 6; page 14 contains Definition 10 and Theorems 2–3; page 18 explains the disjoint-family interpretation and warn that arbitrary posets cannot simply be realized alone. Lemma 4 supplies a union of linear-extension families, not a single family in general. Definition 6 defines autonomy using equality Sigma(G)=LE(Poset(G)). Theorems 2–3 identify autonomous posets with V-posets; v2 attributes the recursive characterization used in Theorem 2 to Hasebe–Tsujie, Theorem 4.3, unlike the older author snapshot.

The autonomy characterization is a named external theorem here, not represented as independently re-proved or fully audited. A source check identifies a nonessential cardinality equality in its Lemma 8 that fails for two independent looped vertices: the full graph has two successful words, whereas deleting one after pressing it leaves only one. Restricting to extensions beginning with the chosen vertex repairs that local step. We do not cite that equality or the paper's typographically incomplete forbidden-bowtie definition as proof ingredients. Sections 2–7 below give complete elementary proofs of our actual reductions, balance lemma, and examples. Source text and PDFs are separately retained research inputs and are not distributed in this public prose edition.

## 2. Feasible flags and the correct poset decomposition

For a set S of labels, write A[S] for the principal submatrix, and count the empty determinant as 1. A word pi=(v_1,...,v_n) is successful exactly when every leading set S_k={v_1,...,v_k} has det A[S_k]=1. Indeed, symmetric scalar-pivot elimination writes each leading determinant as the product of its successive pivots. Over F_2 the permitted pivots are precisely the nonzero scalars, all equal to 1. This also proves that a successful prefix's residual matrix depends on its set of labels, by the Schur complement formula.

Fix a successful word. At the moment vertex v is pressed, let c_v be the current column at v, indexed by all original labels. Define U_vw=(c_v)_w, so the ROW of U labeled v is c_v^T. At the end the original A is the sum of the removed rank-one matrices; therefore A=U^T U. Cleared earlier columns imply U_vw=0 whenever w occurs before v, and U_vv=1. Thus U is unit upper triangular when its rows and columns are placed in the successful order.

A nonsingular unit-upper-triangular Cholesky root in a fixed order is unique. For a block decomposition with the first vertex first, write

U = [[1, u], [0, V]].

The first row of A=U^TU forces u, and the remaining block forces V^TV=C+u^Tu. Induction proves uniqueness. The same calculation proves existence of the root exactly when each leading pivot equals 1.

Let P_U be the partial order generated by the strict arcs v before w for U_vw=1 with v!=w. The original successful word makes this digraph acyclic. A permutation tau lies in LE(P_U) precisely when U is upper triangular in order tau. Then A=U^TU proves tau successful, and uniqueness proves that tau produces exactly the same label-indexed root U. Conversely a word producing U must place all those arcs forward, so it lies in LE(P_U).

Consequently

Sigma(A) = disjoint union over realized U of LE(P_U).

Distinct roots cannot have a common linear extension, because uniqueness applies in that extension's order. They also cannot give the same partial order, for that would give common extensions. This proves the stated partition without presuming that a union of poset-extension families is itself one such family.

### 2.1 Exactly what adjacent exchange accomplishes

In a current residual matrix, consecutive presses x,y can be swapped if and only if x,y are both black and M_xy=0. If x then y is legal, the diagonal before pressing y equals M_yy+M_xy. If both orders are legal, M_xx=M_yy=1 and M_xy=0 follows. Conversely, with those three values, the two rank-one updates commute and have the same final residual matrix. The two instruction rows are unchanged, including entries at all labels outside the pair. Thus the label-indexed U is unchanged.

Any two linear extensions of a fixed finite poset are connected by adjacent swaps of incomparable elements. Here is the usual direct proof: move the first letter of the target extension leftward through the current extension. Every letter crossed is incomparable with it, since a comparison in either direction would contradict one of the two extensions. Repeat after fixing that first letter. The process terminates after finitely many swaps.

By the preceding paragraph, all these swaps are legal within LE(P_U). It follows that the connected components of Sigma(A) under successful adjacent transpositions are EXACTLY the classes LE(P_U).

### 2.2 A successful one-letter relocation is entirely commuting

Suppose two successful words have the form

prefix, a, b_1,...,b_k, suffix
and
prefix, b_1,...,b_k, a, suffix.

Work after the common prefix. Let B be the principal matrix on b_1,...,b_k, let v record their incidences with a, and let a's current diagonal be alpha. The first word gives alpha=1. The second gives every leading principal minor of B equal to 1, so B=R^TR for a unit upper triangular R. Write v=R^T z.

For j=1,...,k, let B_j, R_j, v_j, z_j be the leading restrictions. Upper triangularity gives v_j=R_j^T z_j. The first word makes the principal determinant on {a,b_1,...,b_j} equal to 1, while det B_j=1. Its scalar Schur complement is therefore

1 = alpha + v_j^T B_j^{-1}v_j
  = 1 + z_j^T z_j
  = 1 + sum_(i=1)^j z_i.

All sums are in F_2. Subtracting consecutive equalities forces every z_i=0, so v=0. Hence a is nonadjacent to every b_i in this residual state. Pressing any b_i leaves a black and its entire column unchanged; pressing a leaves all b_i instruction columns unchanged. Moving a past the block can therefore be achieved by legal adjacent commutations, with the identical suffix residual state.

Two distinct permutations have longest common subsequence n−1 if and only if one is obtained from the other by relocating a single letter: delete the unique omitted letter from each common subsequence and reinsert it. Therefore the successful-word graph at TWO total insert/delete edits has exactly the same components as the adjacent-swap graph, hence exactly the instructional classes.

This is a sufficient exchange mechanism for the balanced-pair conclusion below. It is far stronger than the separate eight-total-edit connectivity problem; connectivity at eight edits does not imply it.

## 3. Balance for V-posets and autonomous pressing families

Define a V-poset recursively, starting from a singleton and using disjoint unions, adding a global least element, or adding a global greatest element. We prove:

**Theorem.** Every V-poset with more than one linear extension has a balanced pair under its uniform linear-extension measure.

### 3.1 Uniform shuffles preserve internal distributions

For a disjoint union P=P_1+...+P_t, a linear extension consists of one extension of each component, together with a word of component labels having fixed multiplicities n_i=|P_i|. Every tuple of internal extensions admits exactly n!/(n_1!...n_t!) shuffles. Consequently each internal extension is uniform, independent of the shuffle pattern; an internal pair retains exactly its component probability. The relative restriction to any two components is a uniform shuffle of their uniform internal words, since each two-component pattern has the same number of completions by the other components.

### 3.2 Two fixed chains always supply a balanced pair

Consider a uniform shuffle of fixed words a_1,...,a_p and b_1,...,b_q with p>=q>=1. Put

Q_k = Pr(a_k precedes b_1)
    = product_(i=0)^(k-1) (p-i)/(p+q-i),   1<=k<=p.

The event is exactly that the first k letters in the two-word shuffle all come from the a-word. Thus the formula follows by sampling the next component label without replacement.

If Q_1<=2/3, then Q_1=p/(p+q)>=1/2 and we are done. Otherwise let k be the first index with Q_k<=2/3. Such an index occurs at or before p−q+1, since the final factor of Q_(p−q+1) equals q/(2q)=1/2, and every earlier factor is at most 1. If k>1, then

Q_k/Q_(k−1) = (p−k+1)/(p+q−k+1) >= 1/2,

because k<=p−q+1. Minimality gives Q_(k−1)>2/3, and hence Q_k>1/3. In all cases some Q_k belongs to [1/3,2/3]. This includes the endpoint p=q and the case q=1.

### 3.3 Recursive proof

Induct on the recursive construction. Adjoining a global least or greatest element simply inserts a fixed first or last letter, preserving all other pair probabilities and the number of extensions. In a disjoint union, if any component has more than one extension, apply induction there and the uniform-shuffle lemma. Otherwise each component has a unique extension, hence is a chain: if a finite poset has an incomparable pair, each orientation can be extended to a total order, giving distinct extensions. If there is more than one component, use the two-chain lemma on any two component words, whose relative shuffle is uniform. If there is only one component and it has one extension, the theorem's nonunique hypothesis does not apply. This completes the proof.

The constant cannot be improved uniformly even in this subclass. The union of a two-element chain a_1<a_2 and a singleton b has exactly three extensions; its nontrivial pair probabilities are 1/3 and 2/3. It is realized by the full-rank block-diagonal pressing matrix with rows (3,1,4), whose successes are (0,1,2), (0,2,1), (2,0,1).

**Autonomous pressing corollary.** By the external Cooper–Gartland–Whitlatch Theorems 2–3, an autonomous instructional poset is a V-poset. Thus any full-rank pressable A with exactly one instructional class and more than one successful word has a balanced pair. Equivalently, the same conclusion follows whenever the successful-word graph is connected by adjacent transpositions, or by two-total-edit relocations, by Section 2.

No assumption that EVERY instructional poset in a multiple-class graph is autonomous is made. That would be false: the source expressly distinguishes arbitrary generated posets from autonomous ones. Nor is a balanced pair in one class assumed to remain balanced after averaging over other classes.

## 4. Inverse reversal, proved without a missing-minor caveat

We need the following elementary complementary-principal nonsingularity fact. Let A be invertible on E, let S subset E and T=E\S. Then A[S] is nonsingular if and only if A^{-1}[T] is nonsingular. To see this, a vector x supported on S with (Ax)|_S=0 corresponds bijectively, under y=Ax, to a vector y supported on T with (A^{-1}y)|_T=0. A is invertible, so this is a bijection of the two kernels. Empty-set cases obey the same convention.

For a successful word pi, the leading sets of its reversal are precisely complements of leading sets of pi, in reverse size order. Apply the fact above to every such set. The reversal of pi is successful for A^{-1}, and applying the argument again proves a bijection. It follows that

p_(A^{-1})(x,y) = 1−p_A(x,y).

In particular balance existence, the count of successful words, and uniqueness are invariant under inversion. If A=A^{-1}, reversal acts within Sigma(A), so every distinct pair has probability 1/2. An example beyond the identity is the connected 4 by 4 matrix with rows (13,14,11,7); its square is I, it has successful words, and the exact verifier confirms the reversal pairing. This statement still requires successful pressability: an invertible alternating matrix can be self-inverse and have no legal first press.

## 5. Principal nonsingularity has symmetric exchange, but its ordered flags do not inherit greedoid exchange

Let D(A)={X subset E: A[X] is nonsingular}. We prove its symmetric exchange property directly, without using that property as a theorem about pressing words.

For X in D(A), order X first and write A=[[P,Q],[Q^T,R]]. Define its principal pivot transform

A*X = [[P^{-1},P^{-1}Q],[Q^TP^{-1},R+Q^TP^{-1}Q]].

It is symmetric. For any S subset E,

S in D(A*X) if and only if X symmetric-difference S is in D(A).

A kernel proof avoids a determinant-identity citation. For y=Ax, form the pivoted input z=(y_X,x_(E\X)) and output w=(x_X,y_(E\X)); solving the first block equation yields w=(A*X)z. The conditions that z be supported on S and w vanish on S are exactly that x be supported on X symmetric-difference S and y vanish on that same set. Because P is invertible, the pivot correspondence is bijective, so the principal kernels vanish simultaneously.

Now take X,Y in D(A) and e in X symmetric-difference Y. Put B=A*X and D=X symmetric-difference Y, so B[D] is nonsingular. If B_ee=1, then {e} is feasible, giving X symmetric-difference {e} in D(A). Otherwise B_ee=0, and nonsingularity of B[D] supplies f in D\{e} with B_ef=1. The 2 by 2 principal matrix on {e,f} has determinant 1, regardless of B_ff. Hence X symmetric-difference {e,f} lies in D(A). This is the delta-matroid symmetric-exchange axiom, with the usual convention f=e in the one-element case.

This exchange theorem does NOT give accessibility or valid ordered intermediate flags. Two exact examples locate the failure.

### 5.1 Raw feasible sets can be inaccessible

Take the full-rank symmetric matrix with row masks (3,5,2), namely

[[1,1,0],[1,0,1],[0,1,0]].

It has the successful word (0,1,2). The set {1,2} has principal matrix [[0,1],[1,0]], which is nonsingular, but neither singleton {1} nor {2} is nonsingular. Thus D(A) is not accessible even though A is fully pressable. Its feasible sets cannot simply be regarded as the prefix sets of successful scalar pressing words.

### 5.2 Even successful-prefix sets need not be a greedoid

Take the nonsingular matrix with row masks (11,7,2,1), namely

[[1,1,0,1],[1,1,1,0],[0,1,0,0],[1,0,0,0]].

Only 0 and 1 are initially black. Pressing 0 leaves row masks (0,12,2,10), whose only black vertex is 3. Pressing 3 then leaves (0,6,2,0), so 1 then 2 is forced. Symmetrically, pressing 1 forces 2, then 0, then 3. Thus the complete successful set is exactly

(0,3,1,2), (1,2,0,3).

Let F be the family of sets that occur as prefixes of successful words. X={0,3} and Y={1} lie in F with |X|>|Y|. Neither Y union {0}={0,1} nor Y union {3}={1,3} lies in F: the only successful two-element prefix sets are {0,3} and {1,2}. This violates greedoid augmentation even after all unsuccessfully extendable prefixes have been removed.

The same example is not the set of linear extensions of any single poset. The common precedence relations of its two words are only 0<3 and 1<2. Those two disjoint chains have six linear extensions, not two. Every poset with exactly the two displayed words as extensions would have to equal their common precedence relation: an incomparable pair can appear in either order in some extension. Therefore no such poset exists. It has two instructional classes, each a singleton. Its pair (0,1) is balanced at 1/2, so this is an obstruction to a reduction, not to the conjecture.

## 6. Further necessary conditions and failed stronger shortcuts

### 6.1 Strong-majority total order

For any probability distribution on permutations, suppose no pair is balanced. Orient x toward y if p(x,y)>2/3; each pair has exactly one direction. A directed triangle x→y→z→x is impossible: each total order satisfies at most two of its three comparisons, so their three probabilities sum to at most 2, whereas each would exceed 2/3. A tournament without directed triangles is transitive (a shortest directed cycle of length greater than three would have a chord producing a shorter cycle). Thus a hypothetical counterexample has a well-defined strict total majority order.

This does not prove that the majority order is itself successful, or that it is the only successful word.

### 6.2 Disjoint unions and forced ends

For block-diagonal pressing matrices, presses in distinct blocks do not interact. Successful words are exactly shuffles of block-successful words. Uniformity and the shuffle counting argument of Section 3 apply. If a block has a balanced pair, that pair stays balanced globally. If all blocks have unique successful words and there are at least two blocks, the two-chain shuffle proof gives a balanced pair. Consequently, assuming counterexamples exist, one with a minimum number of vertices must be connected in its underlying graph: every smaller nonunique block would satisfy the conjecture by minimality.

If all successful words start with the same vertex, deleting that first press gives a bijection to the successful words of its nonsingular residual matrix. All remaining pair probabilities are unchanged. A nonunique instance with a forced first vertex therefore cannot be vertex-minimal. Apply inverse reversal for the same conclusion about a forced last vertex. Together with Section 3, a vertex-minimal counterexample must be connected, have at least two possible first and last letters, and have at least two instructional classes.

### 6.3 Not every pair of competing first presses is balanced

A tempting stronger claim is false: even adjacent initially black vertices that can each start a successful word need not form a balanced pair. The nonsingular symmetric rows (13,10,5,3) have exactly the four successful words

(0,3,2,1), (1,2,3,0), (1,3,2,0), (2,1,3,0).

Vertices 0 and 2 are initially black, adjacent, and each occurs first. Nonetheless p(0,2)=1/4. Other pairs are balanced; for example p(1,2)=1/2. The exact verifier independently replays this example.

### 6.4 Short-edit connectivity alone cannot establish probability balance

As an abstract example, take four permutations on six letters: the identity and its three separate adjacent swaps (0,1), (2,3), (4,5). Their graph under two-total-edit moves is connected, a star centered at the identity. Every varying precedence probability is 1/4 or 3/4; all other comparisons are fixed. Hence there is no balanced pair. This four-word family is NOT claimed to arise from pressing: indeed it violates the commuting completion properties of pressing. It shows why connectivity without the extra algebraic/class structure is logically insufficient.

## 7. Exact remaining mathematical obstacle

For realized roots U, let m_U=|LE(P_U)| and p_U(x,y) be the uniform probability inside that class. The exact global formula is

p_A(x,y) = sum_U m_U p_U(x,y) / sum_U m_U.

The unresolved step is a theorem controlling this mixture for instructional roots of one symmetric nonsingular matrix. An arbitrary poset conjecture does not immediately settle it; autonomous/V-poset classification addresses only one class, and even a conditional balanced pair in a selected class need not survive weighting. The genuine symmetric-exchange property acts on unordered sets and has the explicit flag-lifting obstructions in Section 5. The separate four-deletion/four-insertion connectivity work does not control the above class weights.

The results in this packet are therefore bounded theorems and rigorously identified obstructions. They neither prove the full conjecture nor supply a counterexample to it.
