# Kourovka 21.139: geometric reduction and exact remaining obstruction

Date: 2026-10-17 UTC. Status: **partial results; unrestricted question unresolved**.

Author metadata: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.

This approach was developed independently before reading other approach files. It uses primary literature, internal subagent falsification, and explicit proofs. No outside communication was initiated. No novelty claim is made for standard retraction or free-product arguments.

## 1. Exact target and notation

Write

\[
 b_i(H)=\dim_{\mathbb Q}H_i(H;\mathbb Q),\qquad
 \operatorname{vb}_i(G)=\sup_{[G:L]<\infty}b_i(L).
\]

The target is the implication

\[
G\text{ hyperbolic and virtually compact special},\quad
\operatorname{vb}_2(G)<\infty
\quad\Longrightarrow\quad
G\text{ virtually free or virtually a closed surface group}.
\tag{K}
\]

All finite-index subgroups occur in the supremum. Boundedness along one chosen sequence, or vanishing of a normalized limit, is insufficient. Finite and virtually cyclic groups satisfy the virtually-free conclusion. “Surface” means closed and aspherical in the non-elementary hyperbolic case. Nonorientable surfaces are handled by passing to the orientation cover.

Success would require an argument for every hyperbolic virtually compact special group. Establishing the result only for graphs of free groups with cyclic edge groups, or only after an additional homological positivity assumption, does not solve (K).

## 2. Sources checked

The downloaded primary sources and hashes are recorded in [sources_geometry/manifest.json](/Users/alec/Documents/Math/kourovka_descending_20261017/problems/21_139/sources_geometry/manifest.json).

- Henry Wilton, *Surface groups among cubulated hyperbolic and one-relator groups*, [arXiv:2406.02121v3](https://arxiv.org/html/2406.02121v3), 22 January 2026. Theorem A gives a one-ended quasiconvex subgroup of infinite index unless a cubulated hyperbolic group is free or a surface group. Section 4 constructs such subgroups by cuts. It does **not** assert positive virtual second homology.
- G. N. Arzhantseva, *On quasiconvex subgroups of word hyperbolic groups*, Geometriae Dedicata 87 (2001), 191–208, [author manuscript](https://www.mat.univie.ac.at/~arjantseva/Abs/quasi.pdf), Theorem 1: a quasiconvex infinite-index subgroup of a non-elementary torsion-free hyperbolic group can be enlarged to a quasiconvex free product with an infinite cyclic group.
- F. Haglund and D. T. Wise, *Special cube complexes*, [corrected author manuscript](https://www.imo.universite-paris-saclay.fr/~frederic.haglund/special%28corrected%29.pdf). Proposition 6.5 and the proof of Theorem 7.3 construct the virtual retraction. Corollary 3.9 gives inheritance by locally convex subcomplexes; Remark 3.12 handles subdivision. Proposition 7.2 supplies compact convex cores of quasiconvex subgroups.
- Jonathan Fruchter and Ismael Morales, *Virtual homology of limit groups and profinite rigidity of direct products*, [arXiv:2209.14925v3](https://arxiv.org/pdf/2209.14925v3), 21 May 2024. Theorem A/3.5 treats finitely generated residually free groups and HGFC groups. Section 3 already uses free-product amplification and virtual retractions. The amplification mechanism below is consequently **not a new discovery**.
- Dawid Kielak and Marco Linton, *Virtually Free-by-Cyclic Groups*, [published primary source](https://link.springer.com/article/10.1007/s00039-024-00687-6), 2024. Lemma 5.5 and Proposition 5.6 give an alternative precise combination route. Theorem 1.1 is relevant to the two-dimensional remainder.

Here HGFC means a hyperbolic fundamental group of a finite graph of finitely generated free groups with cyclic edge groups. This class is much smaller than all hyperbolic compact special groups.

## 3. Finite-index and retraction bookkeeping

### Lemma 3.1: commensurability of the supremum

If \(S\le G\) has finite index, then \(\operatorname{vb}_i(S)=\operatorname{vb}_i(G)\) over \(\mathbb Q\).

Indeed every finite-index subgroup of \(S\) has finite index in \(G\), giving one inequality. For an arbitrary finite-index \(L\le G\), put \(T=L\cap S\). Restriction followed by cohomological transfer is multiplication by \([L:T]\), so restriction on rational cohomology is injective. Thus \(b_i(L)\le b_i(T)\le\operatorname{vb}_i(S)\), giving the other inequality. The groups used here have finite-dimensional homology in each relevant degree; equivalently one may use homological transfer directly.

It is therefore legitimate to replace the initial group by a torsion-free compact special finite-index subgroup. A virtual conclusion for that subgroup is a virtual conclusion for the original group.

### Lemma 3.2: virtual Betti bounds pass to quasiconvex subgroups

Suppose \(G\) is hyperbolic virtually compact special and \(A\le G\) is quasiconvex. Then

\[
\operatorname{vb}_i(A)\le \operatorname{vb}_i(G).
\]

First pass to a compact special finite-index subgroup and intersect \(A\) with it; Lemma 3.1 preserves the two suprema. The virtual-retraction theorem provides \(G'\le G\) of finite index containing \(A\), with a retraction \(r:G'\to A\). For **each** finite-index \(T\le A\), the pullback \(r^{-1}(T)\) has finite index in \(G\) and retracts onto \(T\). The inclusion on homology is injective since the composite with the retraction is the identity. This proves the claimed bound for every \(T\), not only for a selected family.

This lemma applies to all hyperplane groups and their finite-index subgroups. Infinite index is not required for inheritance.

## 4. Verified amplification theorem

### Proposition 4.1

If \(G\) is hyperbolic virtually compact special and contains an infinite-index quasiconvex subgroup \(A\) with \(\operatorname{vb}_2(A)>0\), then

\[
\operatorname{vb}_2(G)=\infty.
\]

More precisely, there are a finite-index subgroup \(G'\le G\), a positive integer \(a\), and subgroups \(G_n\le G'\), for every \(n\ge1\), satisfying

\[
[G:G_n]=[G:G']n,\qquad b_2(G_n)\ge na.
\tag{4.1}
\]

**Proof.** Choose a finite-index subgroup of \(A\) with positive second Betti number. Intersect it with a torsion-free compact special finite-index subgroup of \(G\). Denote the resulting ambient group by \(S\) and the resulting quasiconvex infinite-index subgroup by \(A_0\). Rational transfer ensures

\[
a=b_2(A_0)>0.
\]

The ambient group \(S\) is non-elementary: a torsion-free elementary hyperbolic group is trivial or infinite cyclic and has no subgroup with positive second homology. Arzhantseva's Theorem 1 now gives \(t\in S\) such that

\[
K=\langle A_0,t\rangle=A_0*\langle t\rangle
\]

is quasiconvex. Apply the virtual-retraction theorem **once**, obtaining a finite-index \(G'\le S\) and a retraction \(r:G'\to K\).

Let \(\phi_n:K\to\mathbb Z/n\mathbb Z\) kill \(A_0\) and send \(t\) to \(1\). Its kernel has the explicit decomposition

\[
K_n=\ker\phi_n\cong
\left(*_{j=0}^{n-1}t^jA_0t^{-j}\right)*\langle t^n\rangle.
\]

For example, a classifying space is the cyclic cover of \(BA_0\vee S^1\): it has \(n\) copies of \(BA_0\) connected around a cycle. Homology of a wedge in degree two therefore gives

\[
b_2(K_n)=n\,b_2(A_0)=na.
\]

Set \(G_n=r^{-1}(K_n)\). Since \(r\) is onto, \([G':G_n]=n\). Its restriction retracts \(G_n\) onto \(K_n\), so \(b_2(G_n)\ge b_2(K_n)\). This proves (4.1). ∎

The identical proof works in every degree \(i\ge2\).

### Adversarial checks on Proposition 4.1

- The independent falsification subagent found no remaining combination or transfer gap. It independently checked the cyclic-cover decomposition and identified the one-retraction construction.
- Infinite index is essential. Taking \(A=G\) for a closed orientable hyperbolic surface group gives \(b_2=1\) in every finite cover and contradicts the conclusion without that hypothesis.
- No malnormality hypothesis is needed. Arzhantseva supplies a suitable element; there is no need to prescribe an arbitrary loxodromic element and hope that it works.
- The resulting sequence need not be residual. With factorial values of \(n\), the pullbacks can be nested, but their intersection contains the kernel of \(G'\to K\to\mathbb Z\), including \(A_0\). Positive normalized growth in this sequence does not imply a positive second \(L^2\)-Betti number.
- Ordinary homology of an arbitrary subgroup does not automatically inject into ambient homology. The explicitly constructed retraction is indispensable.

### Corollary 4.2: exact obstruction for a bounded group

If \(\operatorname{vb}_2(G)<\infty\), then

\[
\operatorname{vb}_2(A)=0
\quad\text{for every infinite-index quasiconvex }A\le G.
\tag{4.2}
\]

In particular, such a subgroup cannot be a non-free HGFC group, or be virtually a non-free hyperbolic finitely generated residually free group: the checked Fruchter–Morales classification gives positive virtual second homology in those cases. An infinite-index quasiconvex closed surface subgroup is likewise impossible.

## 5. The positivity gap is equivalent to the main problem

Consider the statement

\[
\text{(P): every one-ended hyperbolic virtually compact special group has }
\operatorname{vb}_2>0.
\]

Statement (P) would imply (K). Pass to a compact special finite-index subgroup \(S\) of a putative counterexample to (K). If \(S\) is neither free nor a surface group, Wilton's Theorem A supplies a one-ended infinite-index quasiconvex subgroup \(A\). Such a subgroup is again hyperbolic virtually compact special. Statement (P) and Proposition 4.1 then contradict boundedness.

Conversely, (K) implies (P). A one-ended group with \(\operatorname{vb}_2=0\) would be virtually free or virtually surface by (K). An infinite virtually free group has zero, two, or infinitely many ends, never one. A virtually closed hyperbolic surface group has a finite-index orientable surface group, whose second Betti number is one. Both alternatives are impossible.

Thus (P) is **equivalent to the full question**, given the checked Wilton and retraction/combination theorems. Replacing the original question by (P) does not solve its central difficulty.

The specific unjustified step to avoid is

\[
\text{one-ended} \quad\not\Longrightarrow\quad
\text{a supplied nonzero class in }H_2(-;\mathbb Q).
\]

One-endedness controls splittings, rather than directly supplying a rational two-cycle. Even a closed nonorientable hyperbolic surface has zero ordinary rational \(H_2\); its orientation cover is needed. The stronger virtual positivity conclusion for arbitrary cubulated groups is exactly the gap here.

## 6. An audited conditional reduction to cohomological dimension two

The following proof is a conditional equivalence, not a proof of the original problem and not a novelty claim. The independent fresh audit in `reviews/partial_adversary_oct24.md` accepts it, with the precise mid-hyperplane cutting convention below. The original zero-homology assertion (Z2) remains unproved.

Define

\[
\text{(Z2): if }G\text{ is hyperbolic compact special},\quad
\operatorname{cd}_{\mathbb Q}G\le2,\quad
\operatorname{vb}_2(G)=0,\quad\text{then }G\text{ is free}.
\]

**Audited conditional reduction:** (K) is equivalent to (Z2).

### Cutting lemma

Let \(X\) be a finite nonpositively curved special cube complex with embedded two-sided hyperplanes. If every hyperplane of \(X\) has free fundamental group, then \(\pi_1X\) admits a finite classifying complex of dimension at most two. In particular,

\[
\operatorname{cd}_{\mathbb Z}(\pi_1X)\le2.
\tag{6.1}
\]

**Detailed mechanism.** Use subdivision when needed to make the midcube cuts explicit subcomplexes and the original cubes embedded. No finite-index change is used in this lemma. Embeddedness and two-sidedness are part of its hypotheses. If the older Haglund–Wise convention for “special” is used, choose its finite two-sided special cover **before** applying the lemma. In the later zero-homology freeness argument it suffices to prove this cover free, since the original group is torsion-free and virtually free. That argument does not assert that a finite two-dimensional classifying complex descends across a finite index.

List the finitely many original hyperplanes. Cut at their zero-width midplanes by duplicating the two boundary sides, carrying out all components in the current pieces. Replacing each gluing by a product collar gives the associated graph of spaces. Use these midplane cuts throughout; removing entire open cubical carriers is a different convention and is not used in the terminal-chamber argument. Subdivide the half-cube corners to be subcomplexes. Cut along the specified midplanes one at a time. Cutting a nonpositively curved cube complex along an embedded two-sided hyperplane gives locally convex pieces and a graph-of-spaces decomposition with injective attaching maps, as in Wilton's Section 1.1. To see the injectivity for later cuts directly, lift the current piece to the universal cover of \(X\). It is an intersection of closed convex halfspaces. A component of a later cutting space lifts to the intersection of that convex set with an elevation of the corresponding original hyperplane. This intersection is convex in the elevation. Thus the cutting space is locally convex in its original hyperplane and its fundamental group injects into the original free hyperplane group. Compactness gives finite generation, so every edge group is a finite-rank free group.

After cutting along every original hyperplane, the pieces are the vertex chambers. A chamber is the cubical cone on the link of its original vertex: inside each incident cube take its corner bounded by the relevant midplanes. The common cone vertex and the compatible coordinate contractions give a contraction of the entire chamber. Thus every terminal vertex group is trivial.

Reverse the finite cutting hierarchy. Replace terminal pieces by points and each free edge group by a finite graph. If the vertex groups already have classifying spaces of dimension at most two, realize each original injective edge homomorphism by a map from its edge graph to the appropriate vertex classifying space, and attach the graph times an interval using these maps. Van Kampen gives precisely the original graph-of-groups fundamental group. Its universal cover has a Bass–Serre tree of contractible vertex spaces and contractible edge mapping cylinders. The subspace over any finite subtree is contractible up to homotopy, by removing leaves; every sphere is contained in the subspace over some finite subtree and is null-homotopic. Consequently the universal cover is contractible. This constructs a finite aspherical complex of dimension at most two at each reversed step. Induction yields the required finite two-dimensional classifying space for \(\pi_1X\), proving (6.1).

**Independent checks completed, 24 October 2026:** the fresh adversary verified the midplane/corner convention, convex-intersection injectivity, terminal trivial stabilizers, reverse tree-of-spaces asphericity, and both directions of the equivalence. The finite-dimensional-model conclusion is asserted for the specified complex itself; no descent of a finite two-dimensional model across a finite extension is asserted. These checks concern the reduction and do not prove (Z2).

### (Z2) would force zero virtual second homology to characterize free groups in all dimensions

Assume (Z2). Induct on the dimension \(d\) of a compact special cube complex \(X\) with hyperbolic fundamental group \(G\) and \(\operatorname{vb}_2(G)=0\). If necessary first choose a finite special cover with two-sided hyperplanes, of the same dimension. It is enough to prove its fundamental group free: the original torsion-free group would then be virtually free and hence free. Thus at the inductive step the cutting lemma's two-sidedness assumption is available without changing the dimension parameter.

For \(d\le1\), \(G\) is free. For \(d>1\), each hyperplane \(J\) has dimension at most \(d-1\). It is compact and nonpositively curved; after subdivision it is a locally convex subcomplex of a special cube complex, hence special by Haglund–Wise Corollary 3.9. Its fundamental group is quasiconvex in the hyperbolic ambient group. Lemma 3.2 gives \(\operatorname{vb}_2(\pi_1J)=0\). The induction hypothesis says \(\pi_1J\) is free. The cutting lemma gives \(\operatorname{cd}_{\mathbb Q}G\le2\); now apply (Z2) to conclude \(G\) is free.

For a virtually compact special group, apply this to a compact special finite-index subgroup to obtain virtual freeness.

### Deduction of (K) and converse

Given bounded \(\operatorname{vb}_2(G)\), pass to compact special \(S\le G\). Unless \(S\) is free or surface, Wilton produces a one-ended infinite-index quasiconvex \(A\). Corollary 4.2 gives \(\operatorname{vb}_2(A)=0\). Compact special cores, or passage to a compact special finite-index subgroup, and the preceding dimension induction make \(A\) virtually free. That contradicts one-endedness. Hence (K) follows.

Conversely, (K) applied to a group in (Z2) makes it virtually free or virtually surface. The latter has positive virtual second homology. In the former case torsion-freeness and the Stallings–Swan theorem make it free. Thus (K) implies (Z2).

The unresolved content is still (Z2). The reduction identifies a precise two-dimensional zero-homology remainder; it does not prove that remainder.

## 7. Attempts at creating the initial class, and why they fail

| Mechanism | Checkable observation | Exact obstruction/status |
|---|---|---|
| Quasiconvex free products | Proposition 4.1 gives arbitrarily many independent copies of an existing two-class. | It creates no initial two-class if all factors have zero \(H_2\). Verified amplification, blocked for positivity. |
| Closed surface subgroup | A quasiconvex surface has a finite orientable cover with \(b_2=1\), so an infinite-index such subgroup proves unboundedness. | Wilton's new theorem provides one-endedness, not a surface subgroup. Requesting a surface at this point is an additional unsupported claim. |
| Double over a commutator | Abstractly, if \(w\in[A,A]\) has infinite order and \(H_2(A;\mathbb Q)=0\), Mayer–Vietoris for \(D=A*_{\langle w\rangle}A\) gives a nonzero \(H_2(D;\mathbb Q)\): the edge class maps to zero in both vertex abelianizations. | There is no construction embedding this abstract double in the original \(G\). A virtual retraction onto \(A\) does not supply a second copy sharing the desired cyclic subgroup. Blocked at the embedding step. |
| Double a cut cube complex | Cutting a hyperplane gives locally convex pieces and injective edge groups. | Gluing two copies along the same side can fold the normal directions, destroying local isometry. No automatic immersion or subgroup embedding follows. Blocked without a concrete opposite-side construction. |
| Mayer–Vietoris in a hierarchy | For a graph of groups, \(\bigoplus H_2(C_e)\to\bigoplus H_2(A_v)\to H_2(G)\to\bigoplus H_1(C_e)\to\bigoplus H_1(A_v)\). | One needs a verified kernel of the final map or surviving vertex classes. One-endedness alone does not give either; noncyclic edge groups add homology that can kill vertex classes. Blocked without quantified ranks. |
| An arbitrary immersed complex with a two-cycle | A two-cycle in a compact complex is an explicit homology artifact. | A general immersion of cube complexes need not be a local isometry, need not be \(\pi_1\)-injective, and need not yield a virtual retract. The required full-link/convexity conditions must be checked. |
| Stronger virtual positivity statement | Statement (P) would complete the Wilton route. | Section 5 proves (P) is equivalent to (K). Repackaging it is not progress on its proof. |

The abstract-double row is a useful falsifiable construction target. Any new proposal must specify the two subgroup copies, their intersection, the injective amalgam map, and quasiconvexity. None is currently provided.

## 8. Two-dimensional restrictions that are actually proved

Suppose \(G\) is non-elementary hyperbolic compact special and \(\operatorname{cd}_{\mathbb Q}G\le2\). Its compact special classifying complex is finite, and rational homology vanishes above degree two, including in finite covers. Quasiconvex nonabelian free subgroups, virtual retractions, and finite-index pullbacks imply \(\operatorname{vb}_1(G)=\infty\). For every finite-index \(L\le G\),

\[
b_2(L)=[G:L]\chi(G)+b_1(L)-1.
\tag{8.1}
\]

If \(\chi(G)>0\), arbitrarily large indices force \(b_2(L)\to\infty\). If \(\chi(G)=0\), unbounded \(b_1(L)\) does so. Thus a non-elementary two-dimensional group with bounded virtual second Betti number must have \(\chi(G)<0\). In particular, non-elementary hyperbolic finitely-generated-free-by-cyclic groups are excluded from boundedness: their mapping tori have \(\chi=0\).

If \(\operatorname{vb}_2(G)=0\), (8.1) becomes the exact equality

\[
b_1(L)-1=-[G:L]\chi(G)
\quad\text{for every finite-index }L\le G.
\tag{8.2}
\]

This is a necessary condition, not a proof of freeness. Vanishing second \(L^2\)-Betti number alone does not turn (8.2) into a classification. Kielak–Linton Theorem 1.1 reduces the two-dimensional case with vanishing second \(L^2\)-Betti number to virtual free-by-cyclic structure, but its free kernel need not be finitely generated. The infinite-rank-kernel case is not disposed of by the \(\chi=0\) mapping-torus calculation.

## 9. Strongest verified result and remaining work

**Verified:** rational virtual-Betti bounds pass to quasiconvex subgroups; positive virtual second homology of a single infinite-index quasiconvex subgroup amplifies to arbitrarily large second Betti numbers in finite-index ambient subgroups, with the explicit index bound (4.1). This is an established mechanism, checked here with exact quantifiers and an independent adversarial review.

**Audited additional reduction:** the unrestricted question is equivalent to the zero-virtual-second-homology freeness assertion (Z2) in rational cohomological dimension at most two. The local cutting lemma and equivalence passed the fresh 24 October adversarial review under the stated midplane convention; (Z2) remains unproved.

**Remaining gap:** no proof has been found that a one-ended hyperbolic compact special group, even in the zero-virtual-homology two-dimensional remainder, has a finite-index subgroup with nonzero rational second homology. No counterexample to the unrestricted statement has been constructed. The full problem remains unresolved in this effort.

Research-goal completion estimate at this checkpoint: **18%**. The geometric reduction/audit subtask is **100%** complete after the fresh 24 October review. The separate coordinator estimate for full-problem discovery is 15%; neither estimate expresses confidence that the original question is solved. These estimates concern progress, not mathematical confidence or a claim of resolution.
