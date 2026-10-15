# A third-derived pure braid whose closure is not 1-solvable

## Status and precise scope

This is an authored counterexample candidate for problem 30003634 / OWR-15955-011, submitted for an independent mathematical audit. The proof uses established signature and surgery theorems, credited below. It is not a claim of historical priority or human peer review. The finite certificate is exact rational/integer arithmetic; it does not formally verify the imported topological theorems.

**Claim.** Under the ordinary, integral, smooth solvable-filtration conventions of the source, the proposed inclusion fails for (m=3,n=1). Consequently the statement that it holds for every strand number and every (n\ge1) is false. The same counterexample with additional split trivial strands works at (n=1) for every (m\ge3). No assertion is made here about failure at each higher (n).

Let (P_m\le C^m) be the classical pure braid group, included in the group of smooth concordance classes of ordered oriented (m)-strand string links. Products are stacking. Use the ordinary derived series
\[
G^{(0)}=G,\qquad G^{(k+1)}=[G^{(k)},G^{(k)}],\qquad [x,y]=xyx^{-1}y^{-1}.
\]
The symbol (\widehat\beta) denotes the usual oriented braid closure in (S^3). There is no group operation on unbased closed links being used. By definition, a string link is in (F_n^m) when its closure is (n)-solvable. This is not a statement about a topological closure of a subgroup, a power subgroup, a lower-central term, a rational derived series, or a surface braid group.

The (1\)-solution definition used here is a compact smooth oriented (W) with boundary the zero-framed surgery manifold (M_L), such that (H_1(M_L;\mathbb Z)\cong\mathbb Z^m\to H_1(W;\mathbb Z)) is an isomorphism and (H_2(W;\mathbb Z)) has a basis of embedded oriented framed surfaces (L_i,D_i), (1\le i\le r), disjoint except for one positive transverse point (L_i\cap D_i), with both surface fundamental groups mapping into ([\pi_1W,\pi_1W]). This is Otto Definition 2.3 at (n=1). Any extra spin requirement only strengthens the hypothesis and does not affect the obstruction proved below.

## 1. Explicit derived-series certificate

In (B_3=\langle\sigma_1,\sigma_2\mid\sigma_1\sigma_2\sigma_1=\sigma_2\sigma_1\sigma_2\rangle), put
\[
a=\sigma_1^2,\quad b=\sigma_2^2,\quad c=[a,b],\quad d=a^{-1}ca,\quad e=b^{-1}cb,
\]
\[
u=[c,d],\quad v=[d,e],\quad \boxed{\beta=[u,v].}
\]
Both (a,b\) are pure. Hence (c\in P_3^{(1)}). Derived subgroups are characteristic, and in particular normal, so (d,e\in P_3^{(1)}). It follows that (u,v\in P_3^{(2)}), and therefore (\beta\in P_3^{(3)}). This is an actual group expression, not a membership guess based on low-order invariants.

Cancellation of adjacent inverses gives 104 Artin letters. The resulting cyclically alternating expression has 23 pairs
\[
\beta=\prod_{j=1}^{23}\sigma_1^{A_j}\sigma_2^{B_j},
\]
where, in order,
\[
A=(2,-4,2,2,-2,2,-4,2,2,-2,-2,4,-2,-2,4,-2,2,-2,-2,4,-2,-2,2),
\]
\[
B=(2,-2,2,-2,-2,2,2,-2,-2,4,-2,2,-2,2,-2,-2,2,2,-2,-2,2,2,-2).
\]
These lists may be checked simply by substitution in the nested expression. Their sums are both zero; the full expanded word and expression reconstruction are in the certificate and verifier.

For a pure braid, each pairwise linking number of the closure is an additive homomorphism under stacking. Thus every commutator has zero pairwise linking numbers, and (\operatorname{lk}_{ij}(\widehat\beta)=0). The verifier independently follows the strand labels through the 104 crossings and obtains the three linking numbers ((0,0,0)). Each individual component is an unknot: deleting all other strands gives the trivial one-strand pure braid. Thus every component also has Arf invariant zero. These facts are included to fix conventions; Arf invariants are not the final obstruction.

## 2. An exact, non-Meyer signature computation

We use the Goeritz diagram of Erle, *Calculation of the signature of a 3-braid link* (1999), §2, pp. 162–165. The braid orientation is from top to bottom, and its closure uses the standard unknotted exterior closing arcs. The signature convention is the signature of a symmetrized Seifert form, with a positive trefoil having signature (-2).

Here is the entire matrix construction, which avoids a normal-form or floating-point calculation. Put (N=\sum_j|B_j|=48), (t_1=0), (t_{j+1}=t_j+|B_j|), and (s_j=\operatorname{sgn}(B_j)). Indices of the 48 vertices are reduced modulo 48. Start with the zero symmetric matrix (G). For every (j):

1. Add (A_j) to (G_{t_j,t_j}).
2. For (k=0,\ldots,|B_j|-1), put (i=t_j+k), (h=i+1\pmod {48}), and add the (2\times2) block
\[
\begin{pmatrix}-s_j&s_j\\s_j&-s_j\end{pmatrix}
\]
on rows and columns (i,h).

To see why this is the diagram's Goeritz matrix, checkerboard color as in Erle with the unbounded region deleted. The bounded regions are the cyclic string of regions between the second and third braid positions, one per crossing in a (\sigma_2)-block. Each such crossing joins successive regions and contributes exactly the displayed signed edge block. Crossings in the preceding (\sigma_1)-block meet the outside region and the first region of that block; their total contribution is (A_j) to its diagonal. These account for all crossings. For the oriented diagram the exceptional crossings are exactly those in the (\sigma_1)-blocks, so the Goeritz correction is
\[
\mu=\sum_j A_j=0.
\]
Therefore Erle §2.4 and Proposition 2.5 give
\[
\sigma(\widehat\beta)=\operatorname{sign}(G)-\mu.
\]

**Source-indexing qualification.** The off-diagonal line in the printed Proposition 2.3 has an index inconsistent with the block picture immediately below it: the run beginning after (t_j) uses the sign of the current (\sigma_2^{B_j})-block. The construction above is explicitly derived from crossing contributions and agrees with that displayed block picture. It does not silently use the inconsistent index. The relevant page was inspected visually as well as in text.

Exact rational symmetric elimination of (G) gives
\[
(n_+(G),n_-(G),n_0(G))=(23,25,0),\qquad \det G=-7154819319988224.
\]
For a reproducible certificate of this finite statement, `certificate.json` contains all 48 matrix rows and all 48 nonzero scalar Schur-complement pivots. Their signs, in order, are
\[
+--++-++-++---++++-----++--+--++-++----+++----++.
\]
The actual pivot values, rather than only this sign summary, are authoritative in the certificate. Each step is the rational congruence
\[
\begin{pmatrix}p&r^T\\r&H\end{pmatrix}
\sim
(p)\oplus(H-rr^T/p).
\]
The verifier rebuilds the matrix from the nested braid expression, recomputes every pivot, compares every recorded value, counts the signs, and separately computes the determinant by fraction-free Bareiss elimination. These are finite exact identities. Thus
\[
\boxed{\sigma(\widehat\beta)=23-25-0=-2.}
\]

As a second method, using Gambaudo–Ghys Theorem A, the reduced Burau matrices at (-1)
\[
B(\sigma_1)=\begin{pmatrix}1&0\\-1&1\end{pmatrix},\qquad
B(\sigma_2)=\begin{pmatrix}1&1\\0&1\end{pmatrix}
\]
and the rational Meyer form give the same signature. All 104 individual cocycle terms are recorded. The final matrix is
\[
B(\beta)=\begin{pmatrix}
-1401703009468415&3686720931790848\\
2187353096552448&-5753116310519807
\end{pmatrix},\qquad \det B(\beta)=1.
\]
This second calculation is corroboration; the Goeritz argument already determines the signature without Meyer theory.

## 3. Why a 1-solvable algebraically split link has zero ordinary signature

We give the required specialization directly, rather than asserting that link signatures are homomorphisms on the string-link concordance group, or identifying solvability of a zero surgery with a relative solvable cobordism of exteriors.

**Lemma.** If an oriented link (L\) has zero pairwise linking numbers and is (1\)-solvable in the above sense, then (\sigma_L(-1)=0).

**Proof.** Let (W\) be a (1\)-solution, and write (\operatorname{rank}H_2(W;\mathbb Z)=2r). Give (M_L\) the unitary character (\alpha\) sending every meridian to (-1). Because the zero-framed linking matrix is zero, (H_1(M_L;\mathbb Z)=\mathbb Z^m), so this is well defined. The (H_1\)-isomorphism extends (\alpha\) to (W), still through the two-element group.

Use the associated one-dimensional local system (\mathbb Q_\alpha). Choose a finite CW decomposition of (W\) and lifts of its cells to the universal cover. Specializing each cellular boundary matrix through (\alpha\) gives an integer matrix. Its reduction modulo 2 is exactly the ordinary cellular matrix over (\mathbb F_2), because (1=-1) there. Every nonzero minor over (\mathbb F_2\) is an odd, hence nonzero, minor over (\mathbb Q\). Thus for each boundary map,
\[
\operatorname{rank}_{\mathbb Q} d_j^\alpha\ge\operatorname{rank}_{\mathbb F_2}d_j.
\]
The chain dimensions agree, and hence
\[
\dim_{\mathbb Q} H_2(W;\mathbb Q_\alpha)
\le \dim_{\mathbb F_2}H_2(W;\mathbb F_2)=2r.
\]
The equality on the right follows from the universal coefficient theorem: (H_2(W;\mathbb Z)=\mathbb Z^{2r}) and (H_1(W;\mathbb Z)=\mathbb Z^m) has no 2-torsion.

Both (L_i\) and (D_i\) have fundamental group in the commutator subgroup, so their local systems are trivial. They lift to the double cover and give classes in (H_2(W;\mathbb Q_\alpha)). Their twisted intersection matrix is the direct sum of (r\) hyperbolic blocks: distinct surfaces have no intersections, self-intersections are zero by their framings, and a dual pair meets at exactly one point with coefficient (\pm1). Choosing the lift or sign of one member makes each off-diagonal coefficient (+1). In particular, these (2r\) classes are linearly independent. They therefore form a basis, and the twisted signature is zero. The ordinary signature is also zero from the ordinary hyperbolic basis.

For the last step we use the standard surgery/signature formula in Toffoli, *The Atiyah–Patodi–Singer rho invariant and signatures of links* (2022), Remark 4.25, equation (4.21), or equivalently Corollary 4.28. Regard all components of (L\) as one color. The Seifert framing is zero because the pairwise linking numbers vanish, and its framing matrix is the zero matrix. At (\omega=-1), all framing and linking correction terms vanish. With Toffoli's convention,
\[
\rho_\alpha(M_L)= -\sigma_L(-1).
\]
His bounding-manifold formula (1.1) is
\[
\rho_\alpha(M_L)=\sigma(W)-\sigma_\alpha(W)=0.
\]
Therefore (\sigma_L(-1)=0), as required. There is no exclusion here for an Alexander-polynomial zero: the cited surgery formula allows every unit complex number other than 1, and (-1\) is permitted. Reversing the global rho convention would change both displayed signs and leave the vanishing conclusion unchanged. □

The twisted-rank argument also follows as a special case of Cha's published Theorem 8.2, at (n=1,p=2,d=2), but the elementary proof above states the necessary rank comparison and intersection basis explicitly. No assertion about (0.5\)-solvable links is needed.

## 4. Conclusion

Section 1 proves (\beta\in P_3^{(3)}). Section 2 proves (\sigma(\widehat\beta)=-2). If (\beta\in F_1^3), its closure would be 1-solvable, contradicting the lemma. Hence
\[
\boxed{P_3^{(3)}\not\subset F_1^3.}
\]
This is the source question at (n=1). Adding (m-3\) separate trivial strands is a group homomorphism (P_3\to P_m), so it preserves third-derived membership. The resulting closure is a split union with unknots, whose signature remains (-2). The same lemma therefore gives the same failure at (n=1) for every (m\ge3). For (m=1,2), the pure braid groups are trivial or infinite cyclic, so their positive derived terms are trivial; those degenerate strand cases pose no contradiction.

## References used in the proof

- Shelly Harvey, joint work with JungHwan Park and Arunima Ray, *Pure braids, Whitney towers, and 0-solvability*, Oberwolfach Report 50/2017, Question 3, report PDF pp. 34–35. [Report](https://publications.mfo.de/bitstream/handle/mfo/3612/OWR_2017_50.pdf?isAllowed=y&sequence=1)
- Carolyn Otto, *The (n)-solvable filtration of link concordance and Milnor's invariants*, Algebraic & Geometric Topology 14 (2014), 2627–2654, Definition 2.3. [Published PDF](https://msp.org/agt/2014/14-5/agt-v14-n5-p05-s.pdf)
- Dieter Erle, *Calculation of the signature of a 3-braid link*, Kobe Journal of Mathematics 16 (1999), 161–175, §2. [Version of record](https://da.lib.kobe-u.ac.jp/da/kernel/E0003685/E0003685.pdf)
- Jean-Marc Gambaudo and Étienne Ghys, *Braids and Signatures*, Bulletin de la Société Mathématique de France 133 (2005), 541–579, Theorem A, §4.2. [Published PDF](https://www.numdam.org/item/10.24033/bsmf.2496.pdf)
- Enrico Toffoli, *The Atiyah–Patodi–Singer rho invariant and signatures of links*, Proceedings of the Edinburgh Mathematical Society 65 (2022), 404–440, (1.1), (4.21), Corollary 4.28. [Published article PDF](https://epub.uni-regensburg.de/52299/1/the-atiyahpatodisinger-rho-invariant-and-signatures-of-links.pdf)
- Jae Choon Cha, *Hirzebruch-type defects from iterated p-covers*, Journal of the European Mathematical Society 12 (2010), 555–610, Theorem 8.2. [Published PDF](https://ems.press/content/serial-article-files/31720)
