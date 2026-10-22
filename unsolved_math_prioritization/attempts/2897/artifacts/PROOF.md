# Kirby Problem 4.21: rigorous partial results and the unresolved cross-section step

## 1. Question, conventions, and result

For a connected closed topological 4-manifold (M), ask whether there are compact codimension-zero submanifolds (Y,Z) with

\[
M=Y\cup_\Sigma Z,\qquad \partial Y=\partial Z=\Sigma,\qquad
Y\text{ smoothable},\qquad \widetilde H_*(Z;\mathbb Z)=0,
\]

where the common boundary is a locally flat integral homology 3-sphere. Call this property (P(M)). No orientability or simple-connectivity hypothesis is silently added. Statements below using an integral intersection form explicitly assume orientation. All homology groups are integral unless a coefficient ring is displayed.

The source is Problem 4.21, pp. 206–207, of Baykur–Kirby–Ruberman, *K3: A New Problem List in Low-Dimensional Topology*, author's preliminary version [K3]. Its remarks identify the earlier numbering as Kirby 1997, Problem 4.74. The 2026 problem list states the simply-connected positive case and a negative compact-with-boundary analogue.

**Outcome: partial progress only.** The general closed-manifold assertion is neither proved nor disproved here. Five approaches are developed below. The elementary propositions are proved in full; named deep theorems are explicitly imported, with the exact source and hypotheses. No novelty is claimed.

The substantive conclusions are:

1. Smoothable manifolds and all integral homology 4-spheres have (P); (P) is closed under connected sum.
2. Requiring the interface to be (S^3) is exactly the more restrictive connected-sum situation described in Proposition 3.
3. Freedman's construction and classification give (P) for all simply-connected closed 4-manifolds.
4. Almost-smoothness leaves a specific finite cross-section problem, not just a missing assertion of global smoothability.
5. The compact slice-disk obstruction can occur inside a closed integral homology 4-sphere which has (P). Thus it cannot establish a closed counterexample by inheritance.
6. A cyclic-cover lattice test reproduces the Friedl–Hambleton–Melvin–Teichner obstruction to smoothability, but does not obstruct (P).

## 2. Attempt 1: coordinate balls, homology spheres, and connected sums

### Proposition 1: immediate positive classes

If (M) is smoothable, then (P(M)). If (M) is an integral homology 4-sphere, then (P(M)), irrespective of its fundamental group or smoothability.

**Proof.** In the first case fix a smoothing, take a small smoothly embedded closed 4-ball (B\subset M), and put (Z=B), (Y=M\setminus\operatorname{int} B).

In the second case take a closed coordinate ball (B) for the topological manifold. Set (Y=B), with its standard smooth structure transported by the chart, and (Z=M\setminus\operatorname{int} B). The boundary is locally flat and is (S^3). The local orientation map

\[
H_4(M)\longrightarrow H_4(M,Z)\cong H_4(B,S^3)
\]

is an isomorphism (\mathbb Z\to\mathbb Z). The long exact sequence of the pair, excision, and (H_i(M)=0) for (0<i<4) give (H_i(Z)=0) for every (i>0). The complement is connected, since a path crossing a coordinate ball can be rerouted along its connected boundary. Thus (Z) is acyclic. \(\square\)

This observation rules out an obstruction based solely on a complicated perfect fundamental group of a homology sphere.

### Proposition 2: connected-sum closure

If (P(M_1)) and (P(M_2)), then (P(M_1\#M_2)).

**Proof.** Write (M_i=Y_i\cup_{\Sigma_i}Z_i). Perform the connected sum inside smooth coordinate balls in the interiors of the (Y_i). The result contains the smooth manifold (Y_1\#Y_2), with two boundary components (\Sigma_1,\Sigma_2), and the two acyclic pieces (Z_1,Z_2).

Choose a smooth embedded arc in (Y_1\#Y_2) from (\Sigma_1) to (\Sigma_2), meeting the boundary normally. Transfer a closed tubular neighborhood of the arc from the smooth piece to (Z_1\sqcup Z_2). This attaches a single 1-handle between two different components. After rounding corners the new smooth complement remains a compact smooth manifold. The other piece is the boundary-connected sum (Z_1\natural Z_2); it deformation retracts, up to homotopy equivalence, onto (Z_1) and (Z_2) joined by an interval, so it is acyclic. Its boundary is (\Sigma_1\#\Sigma_2), an integral homology sphere. Collars on the two original sides ensure local flatness. \(\square\)

### Proposition 3: the (S^3)-interface characterization

A connected closed (M) has a decomposition as above with (\Sigma\cong S^3) if and only if

\[
M\cong N\# H
\]

for some smoothable closed 4-manifold (N) and some integral homology 4-sphere (H).

**Proof.** Given the decomposition, cap the smooth (Y) by a smooth ball and cap (Z) by a topological ball. The capped first piece (N) is smooth; the capped second piece (H) is a homology sphere by Mayer–Vietoris. In dimension three a boundary homeomorphism is isotopic to a diffeomorphism after choosing the compatible smooth structures, so the smooth cap is legitimate. Removing the two cap balls recovers the connected sum and the original gluing. Conversely, take (Y=N\setminus\operatorname{int}B^4) and (Z=H\setminus\operatorname{int}B^4) in the connected-sum construction. Proposition 1 gives acyclicity of (Z). \(\square\)

**Limit of the approach.** These arguments do not express every closed 4-manifold as a connected sum of these positive classes. If (M) is simply connected and has an (S^3)-interface, van Kampen applied to (N\#H) forces both (N,H) to be simply connected. Then (H\cong S^4) by the topological 4-dimensional Poincaré theorem. Consequently (M) is smoothable. The topological (E_8)-manifold has signature 8 and even form; it is spin and cannot be smooth by Rokhlin's theorem. It does have (P) by the next section, but cannot use (S^3) as its interface. Replacing a homology sphere by a sphere loses essential generality.

## 3. Attempt 2: Freedman's form-and-cap construction

The imported results are Freedman [F], Theorem 1.4′ (p. 367) and Theorem 1.5 with its existence and uniqueness proofs (pp. 368–371), together with Quinn's almost-smoothability [Q] when applying the classification to an arbitrary topological manifold.

- Every integral homology 3-sphere bounds a compact contractible topological 4-manifold.
- Simply-connected closed oriented topological 4-manifolds are classified by the unimodular integral intersection form and the Kirby–Siebenmann invariant. The admissible Kirby–Siebenmann values are both choices for an odd form; for an even form the value is fixed by the signature divided by eight, modulo two.
- The representatives in this classification may be constructed from a smooth 0- and 2-handlebody and a contractible topological cap.

For clarity, the last assertion is part of the **construction**, not a consequence of the classification invariant alone. Here are its relevant steps. Realize a symmetric unimodular matrix by the linking/framing matrix of a framed link in (S^3), and let (W) be its 2-handlebody. Then (\pi_1W=1), (H_2W) carries the prescribed form, and (H_1(\partial W)\cong\operatorname{coker}Q=0). The connected oriented boundary is therefore an integral homology sphere. Cap it by Freedman's contractible manifold (C). Van Kampen gives (\pi_1(W\cup C)=1), and Mayer–Vietoris identifies its intersection form with that of (W).

One must also obtain the required Kirby–Siebenmann value. In the even case the signature fixes it. For an odd form, Freedman's proof changes the knotting of a characteristic attaching component by an Arf-one knot while preserving the linking/framing matrix. The boundary Rokhlin invariant changes, providing both Kirby–Siebenmann types; see the characteristic-surface calculation on p. 371 of [F]. Thus a representative with the invariants of the given (M) is obtained. Classification supplies a homeomorphism to (M). Transporting (W,C) gives (P(M)), with (Z) actually contractible.

**Limit of the approach.** The classification invoked here requires simple connectivity. Reconstructing a matrix does not preserve an arbitrary fundamental group, its action on (\pi_2), or the equivariant intersection pairing. Proposition 2 enlarges the positive class to connected sums with smoothable manifolds and homology spheres, but does not remove this hypothesis.

### A known nonorientable positive example

The nonorientable star partner \(\ast\mathbb{RP}^4\) also admits such a decomposition. The construction recalled in Ruberman–Stern [RS, p. 376] is

\[
\ast\mathbb{RP}^4=(\Sigma/\tau\,\widetilde\times I)\cup_\Sigma C,
\]

where \(C\) is contractible and \(\tau\) is a free smooth orientation-preserving involution on an integral homology 3-sphere. The first piece is the smooth twisted interval bundle over \(\Sigma/\tau\); its boundary is \(\Sigma\). Thus the displayed construction directly has \(P\). For example, their Lemma 2.1 and §3 provide \(\Sigma(5,9,13)\) and the involution from its circle action. This is a known special construction, not a classification of all nonorientable manifolds or a general extension of the simply-connected proof.

## 4. Attempt 3: isolate the nonsmooth point

Quinn [Q, Corollary 2.2.3, p. 508] gives a smooth structure on (M\setminus\{p\}). This is strictly weaker than the compact smooth-complement conclusion required here.

### Lemma 4: homology of a punctured acyclic piece

Let (Z) be a compact connected acyclic topological 4-manifold, and let (p\in\operatorname{int}Z). Then

\[
H_i(Z\setminus\{p\})\cong H_i(S^3)
\]

for every (i), and the inclusion (\partial Z\hookrightarrow Z\setminus\{p\}) is a homology isomorphism. In particular, (\partial Z) is a connected integral homology 3-sphere.

**Proof.** Acyclicity and the universal coefficient theorem give (H^1(Z;\mathbb Z/2)=0), so (Z) is orientable. Poincaré–Lefschetz duality gives (H_i(Z,\partial Z)\cong H^{4-i}(Z)), which is (\mathbb Z) for (i=4) and zero otherwise. The pair sequence then gives the asserted homology of the boundary. Excision at (p) gives (H_i(Z,Z\setminus\{p\})=\mathbb Z) for (i=4) and zero otherwise. Its pair sequence proves the homology assertion for the puncture. Finally remove a small coordinate ball about (p). The oriented relative fundamental class of the resulting compact manifold has boundary equal to the difference of the two boundary fundamental classes. Hence (\partial Z) maps to a generator of the puncture's (H_3\cong\mathbb Z), not to a proper multiple. All other nonzero homology is (H_0). \(\square\)

There is also a converse under the local-manifold setup used in this approach. Suppose (Z) is compact with nonempty boundary, (p\in\operatorname{int}Z), and (E=Z\setminus\{p\}) has the homology of (S^3). Require that a small linking sphere about (p) represent a generator of (H_3(E)). In the pair sequence the map (H_4(Z,E)=\mathbb Z\to H_3(E)=\mathbb Z) is then an isomorphism, and (Z) is acyclic. The generator condition is essential to this converse; the abstract homology groups alone do not specify that map.

**Exact missing step.** In some smoothing of (M\setminus\{p\}), find a compact smooth codimension-zero (Y), with connected boundary, such that the other side (Z\setminus\{p\}) has the homology of (S^3), with the small linking sphere a generator. This would finish the problem by the converse and duality. Smooth exhaustion alone supplies compact smooth submanifolds, but supplies neither the vanishing of (H_1,H_2) of the complementary end neighborhood nor the required (H_3)-map. A coordinate ball about (p) supplies a topologically correct cross-section, but its boundary need not be smooth for the punctured smoothing. Confusing these two constructions is the unproved step.

This is a precise sufficient missing statement; no equivalence for every fixed punctured smoothing is claimed.

## 5. Attempt 4: ordinary homology and cyclic-cover lattice obstructions

### Lemma 5: what a proposed decomposition preserves

For (M=Y\cup_\Sigma Z) as in the question, inclusion induces

\[
H_1(Y)\cong H_1(M),\qquad H_2(Y)\cong H_2(M).
\]

If (M) is oriented, it also gives (H_3(Y)\cong H_3(M)), preserves the integral intersection form on the free part of (H_2), and (\chi(Y)=\chi(M)-1).

**Proof.** In the Mayer–Vietoris sequence, (H_1\Sigma=H_2\Sigma=0), all positive homology of (Z) vanishes, and the map on (H_0\Sigma) into (H_0Y\oplus H_0Z) is injective. This proves the first two isomorphisms. In the oriented case (H_4M\to H_3\Sigma) is the isomorphism that sends the fundamental class to the separating hypersurface class. Exactness gives the (H_3)-isomorphism. The absolute-to-relative identification (H_2(Y)\cong H_2(Y,\Sigma)), and naturality of intersection pairings under gluing a homology ball, identify the forms. Euler characteristic additivity gives the last assertion because (\chi Z=1), (\chi\Sigma=0). \(\square\)

The (H_3) statement is deliberately not made for a nonorientable (M).

Ordinary homology thus gives necessary conditions but no contradiction. Also, acyclicity of (Z) says only that the abelianization of (\pi_1Z) is zero. It does not say (\pi_1Z=1); replacing it by a contractible piece is not justified in general.

A more serious test uses Friedl–Hambleton–Melvin–Teichner [FHMT]. Set (\Lambda=\mathbb Z[x,x^{-1}]), (t=x+x^{-1}), and consider their Hermitian matrix

\[
L=\begin{pmatrix}
1+t+t^2&t+t^2&1+t&t\\
t+t^2&1+t+t^2&t&1+t\\
1+t&t&2&0\\
t&1+t&0&2
\end{pmatrix}.
\]

Their closed oriented (M_L) has (\pi_1=\mathbb Z), this equivariant form, and zero Kirby–Siebenmann invariant. Its (n)-fold cyclic cover has ordinary positive definite unimodular form (L_n) of rank (4n), obtained by reducing modulo (x^n-1) and taking the coefficient of the identity. For (n\ge3) it is nonstandard [FHMT, Theorem 1.2; proof in §2].

Here is the elementary nonstandardness calculation. Let (N=1+x+\cdots+x^{n-1}) and (w=N(e_3+e_4)). On the integral basis (x^je_i), the pairings with (w) are 5 for (i=1,2) and 2 for (i=3,4), while the respective basis norms have these same parities. Therefore (w) is characteristic. Moreover,

\[
w^2=4n,\qquad (w,e_1)=5,\qquad e_1^2=3\quad(n\ge3).
\]

The characteristic vector (w'=w-2e_1) has

\[
(w')^2=4n-4\cdot5+4\cdot3=4n-8<4n.
\]

For the standard positive diagonal lattice of rank (4n), a characteristic vector has every coordinate odd and therefore norm at least (4n). Thus (L_n) is not standard. The included exact-arithmetic program checks these identities, symmetry, determinant and positivity for (1\le n\le12); the symbolic argument, not the finite checks, proves the assertion for every (n\ge3).

**Why this does not disprove (P(M_L)).** If (P(M_L)), the restriction of any cyclic cover to (Z) is trivial: every homomorphism (\pi_1Z\to\mathbb Z/n) factors through (H_1Z=0). The same holds for (\Sigma). Thus the lifted smooth complement has (n) homology-sphere boundary components and the cover is completed by (n) topological acyclic pieces. The lifted complement is connected because (H_1Y\to H_1M_L) is an isomorphism. Mayer–Vietoris identifies its (H_2) form with (L_n).

Donaldson's closed-manifold diagonalization theorem cannot be applied to that smooth manifold with boundary. To obtain a closed smooth manifold with the same form one would need smooth acyclic caps for those boundary components, which the proposed decomposition does not provide. Merely being nonsmoothable, even with zero Kirby–Siebenmann invariant and an explicit definite-cover obstruction, is not a counterexample to (P).

## 6. Attempt 5: the compact knot obstruction and failure of inheritance

For a compact manifold (X) with boundary, consider the analogous assertion that (X=A\cup_\Sigma Z), with (Z) acyclic in the interior, (A) smoothable, and (\partial A=\partial X\sqcup\Sigma). This assertion is false.

Use a knot (K\subset S^3) that is topologically slice but does not bound a smooth disk in any smooth rational homology 4-ball with boundary (S^3). Such knots are supplied by [FHMT, Corollary 1.4], whose complete proof is in §4, using the lattice obstruction of §2 and the Kirby construction on pp. 9–11. This published source avoids relying on the unpublished knot example mentioned in [K3]. Let (D\subset B^4) be a locally flat slice disk and let (X=B^4\setminus\operatorname{int}\nu D) be its exterior. Then

\[
H_*(X)\cong H_*(S^1),\qquad \partial X=S^3_0(K)=:N,
\]

and the meridian generates (H_1X\cong\mathbb Z). The disk-exterior homology follows either from relative Alexander duality or by splitting (B^4) into the normal disk bundle (D^2\times D^2) and its exterior, whose intersection has homotopy type (D^2\times S^1); the pair sequence identifies its meridian generator. The boundary description uses the zero-framing induced by the slice disk.

Suppose such a decomposition existed and fix a smoothing of (A). Boundary parametrizations may be taken smooth up to isotopy by the uniqueness and compatibility of smooth structures on 3-manifolds. Mayer–Vietoris yields

\[
H_1(A)=\mathbb Z,\qquad H_2(A)=0,\qquad H_3(A)=\mathbb Z,
\]

with (H_1N\to H_1A) an isomorphism and (H_3\Sigma\to H_3A) an isomorphism.

Attach to the (N)-boundary the smooth dual 2-handle for reversing the zero surgery on (K). Its attaching circle is the meridian and its outgoing boundary is (S^3). The relative 2-handle generator maps isomorphically to (H_1A), so the resulting cobordism (C) has (H_1C=H_2C=0) and (H_3C=\mathbb Z). Its two boundary components are (S^3) and (\Sigma); their fundamental classes generate (H_3C), with opposite signs. Cap the (S^3) boundary by a smooth ball. The result (A') is a smooth acyclic manifold bounded by the same oriented (\Sigma) as (A).

Now glue (A) to (-A') along (\Sigma). Mayer–Vietoris, including the isomorphism on (H_3\Sigma), shows that the result (B) has the homology of (S^1), with (\partial B=N) and meridian generating (H_1B). Attach the same dual 2-handle once more. It kills that generator and creates no (H_2); the result is a smooth integral homology 4-ball (V) with boundary (S^3). The cocore is a smooth properly embedded disk. By the inverse-surgery description its boundary is the original (K\subset S^3). This contradicts the choice of (K). Therefore (X) is a compact counterexample.

### Proposition 6: this compact obstruction embeds in a positive closed example

The compact (X) just constructed embeds as a codimension-zero submanifold of a closed integral homology 4-sphere. That closed manifold has (P) by Proposition 1.

**Proof.** Form the oriented double (D(X)=X\cup_N(-X)). The map (H_1N\to H_1X) is an isomorphism, and (H_*(N)=H_*(S^1\times S^2)). Mayer–Vietoris gives

\[
H_*(D(X))\cong H_*(S^1\times S^3).
\]

Explicitly, the degree-one map is the diagonal inclusion (\mathbb Z\to\mathbb Z^2), whose cokernel is (\mathbb Z) and whose kernel is zero; (H_2N=\mathbb Z) supplies (H_3D(X)=\mathbb Z), and (H_3N=\mathbb Z) supplies the oriented top homology.

Choose a locally flat embedded loop in the interior of the second copy (-X) representing the generator of (H_1D(X)). Such a loop can be made smooth in a punctured smoothing; a 1-dimensional loop can be embedded by general position in dimension four. Its oriented rank-three normal bundle over (S^1) is trivial. Perform surgery there, replacing (S^1\times\operatorname{int}B^3) by (B^2\times S^2). Call the resulting closed oriented manifold (H). This operation is disjoint from the first copy (X), so that copy remains embedded.

The complement of the loop has the same fundamental group as (D(X)), by general position in codimension three. Van Kampen says the surgery quotients this fundamental group by the normal closure of the loop. Its abelianization is consequently (H_1D(X)/\langle[\gamma]\rangle=0). Also, Euler characteristic increases by two, since the removed (S^1\times B^3) and its boundary have Euler characteristic zero and the inserted (B^2\times S^2) has Euler characteristic two. Hence (\chi(H)=2). Integral Poincaré duality and the universal coefficient theorem give (H_3H=0) and show (H_2H\cong H^2H\cong\operatorname{Hom}(H_2H,\mathbb Z)), so (H_2H) is free. The Euler characteristic then gives its rank as zero. Thus (H) is an integral homology 4-sphere. \(\square\)

**Limit of the approach.** This is not a counterexample to the closed problem. Indeed it proves that the compact obstruction survives as a submanifold inside a closed manifold satisfying the desired property. A decomposition of the ambient closed manifold need not restrict to one of (X); its interface may cross (N=\partial X). Any promotion of the compact obstruction would need an additional theorem controlling all possible interfaces, which is absent here.

## 7. Remaining question

For arbitrary non-simply-connected closed topological 4-manifolds, none of these methods constructs the required smoothable complement or excludes all such complements. The missing finite acyclic-neighborhood construction in §4, or a genuinely closed obstruction overcoming the cap issue in §5, is the unresolved step. The inspected 2026 primary problem list still poses the question; the literature search found no verified later general theorem. This is a bounded literature finding, not a proof that no unlocated result exists.

## References

[K3] R. İnanç Baykur, Robion C. Kirby, Daniel Ruberman, *K3: A New Problem List in Low-Dimensional Topology*, author's preliminary version, Problem 4.21 and remarks, pp. 206–207. [Author-hosted PDF](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).

[F] Michael Hartley Freedman, *The topology of four-dimensional manifolds*, Journal of Differential Geometry 17 (1982), 357–453. Theorems 1.4′ and 1.5, pp. 367–371. [DOI](https://doi.org/10.4310/jdg/1214437136); [author-hosted scan](https://www.maths.gla.ac.uk/~mpowell/1982_The%20topology%20of%20four-dimensional%20manifolds.pdf).

[Q] Frank Quinn, *Ends of maps. III: Dimensions 4 and 5*, Journal of Differential Geometry 17 (1982), 503–521. Corollary 2.2.3, p. 508, and its handle-straightening argument, pp. 506–508. [DOI](https://doi.org/10.4310/jdg/1214437139); [author-hosted scan](https://www.maths.gla.ac.uk/~mpowell/1982_Ends%20of%20maps%20III.pdf).

[FHMT] Stefan Friedl, Ian Hambleton, Paul Melvin, Peter Teichner, *Non-smoothable four-manifolds with infinite cyclic fundamental group*, arXiv:math/0611077v2 (10 March 2007). Theorem 1.2, Corollary 1.4, and proofs in §§2 and 4. [Versioned primary preprint](https://arxiv.org/abs/math/0611077v2).

[RS] Daniel Ruberman and Ronald J. Stern, *A fake smooth CP² # RP⁴*, Mathematical Research Letters 4 (1997), 375–378. Construction on p. 376 and Lemma 2.1. [DOI](https://doi.org/10.4310/MRL.1997.v4.n3.a6); [author-hosted paper](https://bpb-us-e2.wpmucdn.com/faculty.sites.uci.edu/dist/3/246/files/2011/03/41_FakeCP2RP4_MRL.pdf).
