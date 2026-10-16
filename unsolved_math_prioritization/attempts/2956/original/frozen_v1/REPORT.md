# KP-4.80: finite torsion in the exotic mapping-class kernel

**Problem identifier:** 2956 / KP-4.80.  
**Assessment date:** 8 October 2026.  
**Result:** rigorous partial reductions and construction obstructions; both existence questions remain unresolved in this report. Five mathematical approaches were carried out. Source recovery, literature searches, and finite checks are not counted as approaches. No novelty claim is made for the reductions below.

## 1. Exact target and conventions

Fix a smooth, closed, connected, simply connected four-manifold (X). Write
\[
 \mathcal E(X)=\ker\bigl(\pi_0\operatorname{Diff}(X)
          \longrightarrow\pi_0\operatorname{Homeo}(X)\bigr).
\]
Here paths in the diffeomorphism group give smooth isotopies; paths in the homeomorphism group give topological isotopies. The question is existential in both (X) and an integer (m>2):

1. Does some such (X) have a class (a\in\mathcal E(X)) of **exact finite order (m>2)**?
2. Does some such (X) have a **finite subgroup of cardinality (m>2)** in \(\mathcal E(X)\)?

These are different questions. A subgroup \((\mathbb Z/2)^2\) answers the second with (m=4), although all its nonidentity elements have order two. Infinite-order classes answer neither. The order is taken in a mapping-class group: (a^m=1) means that a representative's (m)-th power is smoothly isotopic to the identity. It does not require an order-(m) representative diffeomorphism.

The authoritative normalization is Problem 4.80, printed and PDF page 256, in the 2026 author manuscript of [K3]. That page was inspected visually as well as through text extraction. The local record's malformed `ordern`, `subgroupker`, `4manifold`, and exponent `n,-1` are extraction defects. The last exponent is (n-1). The book additionally singles out \((\mathbb Z/2)^2\), the two necks in (K3\#K3\#K3), and \((\mathbb Z/2)^{n-1}\) for (n) K3 summands. This is the K3-list problem number, not the different Problem 4.80 in the older K2 list.

A simply connected manifold is orientable; choose an orientation. Every element of \(\mathcal E(X)\) preserves it. On the orientation-preserving mapping-class group define
\[
 \rho_X:\pi_0\operatorname{Diff}^+(X)\longrightarrow O(H_2(X;\mathbb Z),Q_X).
\]
The topological isotopy classification cited in [K3], and used explicitly in [KM] and [B], identifies
\[
                 \mathcal E(X)=\ker\rho_X.                 \tag{1}
\]
This identification is an imported four-dimensional theorem, not a consequence of the definition alone. We never apply it to a nonsimply-connected manifold or silently to isotopies relative to several boundary components. The orientation restriction matters, including when (H_2(X)=0).

For comparison, the symplectic-to-smooth kernel
\(\ker(\pi_0\operatorname{Symp}(X,\omega)\to\pi_0\operatorname{Diff}(X))\)
is a different group. A nontrivial symplectic class in that kernel is the identity in the group occurring in this problem.

## 2. Verified source position

[KM, Theorem 1.1] supplies a nontrivial neck twist on (K3\#K3). A collar twist is represented by
\[
       (s,y)\longmapsto (s,\alpha(s)y),\qquad
       \alpha:[0,1]\longrightarrow SO(4),
\]
where \(\alpha\) is constant at the identity near the endpoints and represents the generator of \(\pi_1SO(4)=\mathbb Z/2\). Its square is smoothly isotopic to the identity by a based nullhomotopy of the squared loop. It acts trivially on homology, so (1) puts it in \(\mathcal E\). The nontriviality theorem makes its order exactly two. [JL] proves survival after adjoining one (S^2\times S^2), not after adjoining a third K3.

The following later results were checked for their actual domains and conclusions:

- [T, Theorem 1.2], a November 2025 preprint, proves nontriviality of the **boundary** twist of punctured (K3\#K3). It is not a theorem about the neck in closed \(\#^3K3\).
- [L, Theorem 1.1], May 2026 version, expresses many boundary twists as commutators in the full relative smooth mapping-class group. Its Section 4.5 distinguishes abelianization of that full group from abelianization of the relative Torelli group. A commutator can still have order two; this result supplies neither higher torsion nor triviality of the twist.
- [LS, Theorem 1.6 and Corollary 1.7], August 2026 version, constructs homotopy-coherent \(\mathbb Z/2\)-actions from nontrivial neck twists. It does not construct a new order-(m>2) class or establish independence of several twists.
- [BT, Theorem 1.1], published 7 September 2026, gives surjections from certain Torelli groups to a free abelian group of infinite rank. Such a surjection is evidence for infinite-order classes; it does not supply finite torsion in its domain.
- [B, Section 7] computes puncture-capping kernels and a spin extension for a manifold homeomorphic to K3. [K, Section 7.1] separates known order-two neck mapping classes from their failure of genuine Nielsen realization.

No full affirmative or negative resolution of either exact target was verified in the inspected sources or the bounded current search. This is not a claim that every unpublished or unindexed result has been excluded. Only the specific results listed as imported dependencies below are used in the proofs.

## 3. Approach 1: symmetric connected-sum necks

### 3.1 Construction

Let (M) be a smooth closed oriented simply connected four-manifold and let (n\ge2). Realize
\[
 X_n=\#^n M
\]
by attaching (n) identical punctured copies of (M) to the (n) boundary spheres of
\[
 P_n=S^4\setminus\bigcup_{i=1}^n\operatorname{int}(B_i^4).
\]
Let (t_i\in\pi_0\operatorname{Diff}^+(X_n)) be the neck twist around the (i)-th punctured summand, supported in a collar in (P_n). Let (N_n(M)=\langle t_1,\ldots,t_n\rangle).

The attempt is to enlarge the known order-two example by using different summands, rather than assuming that nontriviality survives another connected sum. The following theorem isolates exactly how much independence remains to prove.

### 3.2 The neck subgroup theorem

**Theorem 1.** In the construction above:

(a) (N_n(M)\) is an elementary abelian two-group contained in \(\mathcal E(X_n)\).

(b) The relation \(t_1t_2\cdots t_n=1\) holds, and diffeomorphisms of (X_n) permute the (t_i) by every permutation of their labels.

(c) If (n) is odd, then
\[
 N_n(M)\cong\{1\}\quad\hbox{or}\quad(\mathbb Z/2)^{n-1}.
\]
If (n) is even, the only possibilities are
\[
 N_n(M)\cong\{1\},\quad\mathbb Z/2,\quad
                      (\mathbb Z/2)^{n-1}.
\]
Repeated entries in this list when (n=2) are understood as one possibility. The theorem lists permitted possibilities; it does not assert that all are realized.

**Proof.** Disjoint collar supports give pairwise commuting representatives. Each twist has square smoothly isotopic to the identity, by the local (SO(4))-loop construction. The Mayer–Vietoris identification
\(H_2(X_n;\mathbb Z)=\bigoplus_i H_2(M;\mathbb Z)\)
can be represented away from the collars, so each twist acts trivially on (H_2). The manifold (X_n) is simply connected by van Kampen. Equation (1) proves (a).

For the relation, use the circle action on
\(S^4\subset\mathbb R^5\) that rotates one coordinate two-plane and fixes its orthogonal three-plane. The fixed set in (S^4) is (S^2). Choose (n) small disjoint invariant round balls centered on that fixed (S^2). On each boundary sphere the resulting loop is, in oriented local coordinates, one full rotation of a two-plane in \(\mathbb R^4\); it represents the generator of \(\pi_1SO(4)\).

Restrict the action loop to (P_n). Make each member of this loop the identity near the boundary by inserting the inverse rotation in each collar, cut off to zero toward its interior. This produces a path in \(\operatorname{Diff}(P_n,\partial P_n)\) starting at the identity. At the end the ambient action has completed a full turn and is the identity, while the collar corrections are one twist on each boundary. Thus their product is isotopic to the identity relative to the boundary. The possible inverse convention does not matter because the twist class has exponent two. Extending this isotopy by the identity on the punctured (M)'s proves \(\prod_i t_i=1\) in the closed manifold.

Any permutation of the (n) parameterized balls in an oriented connected four-manifold can be carried out by an orientation-preserving ambient diffeomorphism: move their centers along disjoint moving paths, carry sufficiently small balls along those paths by isotopy extension, and adjust the final oriented frames, using path-connectedness of (SO(4)). Apply this in (S^4), and exchange the identical punctured (M)-summands using their fixed identifications. It gives a diffeomorphism of (X_n) whose conjugation sends (t_i) to (t_{\sigma(i)}). No assertion that the chosen diffeomorphisms form an actual action of (S_n) is required. This proves (b).

Work additively over \(\mathbb F_2\). The surjection
\[
 F:\mathbb F_2^n\longrightarrow N_n(M),\qquad e_i\longmapsto t_i
\]
has a permutation-invariant kernel (R\) containing the diagonal vector
\(d=e_1+\cdots+e_n\).
Let
\(A=\{(x_i):\sum_i x_i=0\}\), the even-weight subspace.
If (R\) contains a vector (v\notin\{0,d\}\), choose (i,j\) with (v_i\ne v_j\). Then
\[
          v+(ij)v=e_i+e_j\in R.
\]
Permutation invariance now puts every (e_i+e_j\) in (R\). These vectors span (A\), so (A\subset R\).

If (n\) is odd, (d\notin A\), and (A+\langle d\rangle=\mathbb F_2^n\). Consequently (R\) is either \(\langle d\rangle\) or all of \(\mathbb F_2^n\). The quotient dimensions are (n-1\) and zero.

If (n\) is even, (d\in A\). The same argument shows that (R\) is one of \(\langle d\rangle\), (A\), or \(\mathbb F_2^n\), yielding quotient dimensions (n-1,1,0\). This proves (c). ∎

**Corollary 2 (the three-K3 reduction).** For the standard summand-neck twists on (X=K3\#K3\#K3\), nontriviality of any one of the three leaf-neck classes is equivalent to the subgroup being \((\mathbb Z/2)^2\). In the standard linear connected-sum picture, the two indicated necks are the twists around the first and third summands. They generate that group exactly when either one is nontrivial.

**Proof.** Theorem 1 with (n=3\) leaves only dimensions zero and two. In the two-dimensional quotient, the images of (e_1,e_2,e_3\) are its three distinct nonzero vectors. In particular (t_1,t_3\) are independent and generate it. ∎

**Corollary 3 (a scalar-detection restriction).** If (n\) is odd and \(\psi:N_n(M)\to A'\) is a homomorphism to an abelian group that is unchanged by the summand-permuting conjugations, then \(\psi=0\).

**Proof.** All \(\psi(t_i)\) equal a value (a\). Since (t_i^2=1\), (2a=0\). The product relation gives (na=0\), and odd (n\) implies (na=a\). Hence (a=0\). ∎

The invariance assumption is essential. A non-invariant vector-valued detector could distinguish the generators of a nontrivial elementary abelian subgroup. This corollary is not a claim that every gauge invariant satisfies those assumptions.

**Outcome and exact gap.** There is no need to prove three independent statements about the two generators and their product in \(\#^3K3\). A single nontriviality proof suffices. But this report does not prove that nontriviality. Extending the known (K3\#K3\) twist to a third K3 may kill its class; extension by the identity does not in general induce an injective homomorphism on mapping classes. Theorem 1 also shows why this family, even if successful, supplies a finite subgroup and never an element of order greater than two.

## 4. Approach 2: nonequivariant families Bauer–Furuta detection

The attempted detector is the product calculation actually used for the two-K3 twist, applied to the new necks.

The imported inputs from [KM, Sections 4–5] are the nonequivariant Bauer–Furuta value \(\eta\in\pi_1^S\) for K3, its connected-sum product formula, and the families formula for a neck with fiber (U\#V\). With the indicated spin choice it gives
\[
 \eta\,\operatorname{BF}(U)\operatorname{BF}(V)
          \quad\text{if }\sigma(U)\equiv16\pmod{32},
\]
and zero if \(\sigma(U)\equiv0\pmod{32}\). Choosing the other lift of the monodromy to the spin bundle interchanges the roles of (U\) and (V\). We use the same spin-family conventions as [KM]; a nonzero invariant of one chosen spin family by itself must not be confused with a complete test of its underlying unstructured family.

Put (U=\#^aK3\), (V=\#^bK3\), with (a,b\ge1\), (a+b=n\). Then
\[
 \operatorname{BF}(U)=\eta^a,\qquad
 \operatorname{BF}(V)=\eta^b,\qquad
 \sigma(U)=-16a.
\]
Thus the first spin choice has invariant \(\eta^{n+1}\) when (a\) is odd and zero when (a\) is even. The other choice has the analogous expression governed by the parity of (b\).

The classical stable-stem inputs are \(\eta^3\ne0\), of order two in \(\pi_3^S\cong\mathbb Z/24\), and \(\pi_4^S=0\), hence \(\eta^4=0\). The first is explicitly used in [KM]; the fourth stem is also recorded in [IWX]. It follows algebraically that
\[
 \eta^{n+1}=0\qquad(n\ge3).
\]
For (n=2\), both side parities are odd and both spin choices have nonzero \(\eta^3\), recovering the numerical obstruction in [KM]. For (n=3\), both spin-family invariants of every standard leaf neck are zero. For larger (n\), the same product method gives zero regardless of side parity.

This is a calculation of the stated invariant, not a calculation of the mapping class. It does **not** prove the twist trivial. The calculation explains precisely why simply repeating the nonequivariant proof cannot establish the missing nontriviality in Corollary 2.

An independent elementary obstruction also limits integer-valued additive invariants. If \(h:G\to\mathbb Z\) is a homomorphism and (g^m=1\), then (m h(g)=0\), so (h(g)=0\). More generally, a homomorphism to \(\mathbb Z/r\) sends an element of order (m\) to one whose order divides \(\gcd(m,r)\). In particular all odd torsion is invisible to an additive \(\mathbb Z/2\)-valued invariant. Conversely, a nonzero \(\mathbb Z/r\)-value does not prove the class has finite order: reduction \(\mathbb Z\to\mathbb Z/r\) is an immediate counterexample. A finite-power isotopy is separately necessary.

**Outcome and exact gap.** The direct nonequivariant detector vanishes at the first new K3 case. A refined, for example equivariant, calculation would have to detect the actual closed neck class and handle both spin choices appropriately. [T] does use equivariant methods, but its punctured-boundary theorem does not furnish the required closed-neck calculation. No such refined computation is asserted here.

## 5. Approach 3: puncturing, capping, and the spin extension

This approach attempts to obtain higher finite subgroups from the numerous boundary rotations of a multiply punctured manifold and then close it up.

Write (M_r(X)=\pi_0\operatorname{Diff}^+(X^{(r)},\partial)\), where (X^{(r)}\) is obtained by removing (r\) disjoint open balls and diffeomorphisms are the identity near every boundary component. Let (c_r:M_r(X)\to M_0(X)\) extend by the identity over the missing balls.

The disk-embedding restriction fibration and its exact homotopy sequence give, when (X\) is simply connected and spin,
\[
 \pi_1\operatorname{Diff}^+(X)\longrightarrow
 (\mathbb Z/2)^r\longrightarrow M_r(X)
 \stackrel{c_r}{\longrightarrow} M_0(X)\longrightarrow1.       \tag{2}
\]
Here the middle group is the fundamental group of the ordered framed-point configuration space; its generators map to boundary twists. The first map has image either zero or the diagonal \(\mathbb Z/2\). These are imported fibration/capping facts in [B, Proposition 7.1 and Section 7]; the geometric inputs are isotopy extension and the identification of small disk embeddings with framed points. They imply
\[
 \ker c_r\cong(\mathbb Z/2)^r
 \quad\text{or}\quad(\mathbb Z/2)^r/\Delta(\mathbb Z/2).       \tag{3}
\]
For a homotopy K3 surface the evaluation map for one frame is zero [KM, Proposition 2.1; B, Theorem 7.2], and thus \(\ker c_r\cong(\mathbb Z/2)^r\).

These are indeed finite subgroups larger than two in **relative smooth capping kernels**. But they were constructed to lie in \(\ker c_r\): the map to the closed smooth mapping-class group sends every generator and their entire subgroup to the identity. This particular closing-up construction therefore produces no nontrivial element of \(\mathcal E(X)\).

It would also be incorrect to identify the whole group in (3) with the relative smooth-to-topological kernel. With several boundary components, requiring isotopies to fix all boundaries is a different condition. Equation (1) was a theorem for closed manifolds; no multi-boundary identification of that kind is being used here.

The one-puncture case gives a useful further test. If \(\ker c_1=\langle\delta\rangle\cong\mathbb Z/2\), boundary twists are central, so
\[
        1\longrightarrow\langle\delta\rangle\longrightarrow
        M_1(X)\longrightarrow M_0(X)\longrightarrow1          \tag{4}
\]
is a central extension. Centrality follows by sliding the twisting collar inside the neighborhood where any boundary-fixing diffeomorphism is the identity.

**Lemma 4 (finite-order lifting arithmetic).** For a central extension (4), if (a\in M_0(X)\) has exact order (m\), then every lift \(\widetilde a\) has finite order (m\) or (2m\), determined by \(\widetilde a^m=1\) or \(\delta\). Conversely, a finite-order \(\widetilde a\) has image order obtained by dividing its order by (1\) or (2\).

**Proof.** The image of \(\widetilde a^m\) is the identity, so \(\widetilde a^m\in\{1,\delta\}\), and \(\widetilde a^{2m}=1\). The order of the image divides the order upstairs. If \(\widetilde a^m=\delta\ne1\), the upstairs order is a divisor of (2m\), a multiple of (m\), and not (m\), so it equals (2m\). Conversely restrict (c_1\) to the finite cyclic subgroup generated by \(\widetilde a\) and use the kernel-order formula. ∎

Thus an order-four relative class can merely project to an order-two closed class. Merely enlarging orders in a spin double cover is not enough.

There is an even sharper obstruction for (X\) homeomorphic to K3. [B, Theorem 7.7] identifies the extension class of (4) as \(\rho_X^*w_2(H^+)\). Its restriction to \(\mathcal E(X)=\ker\rho_X\) is zero, because that representation is trivial there. Consequently the restricted central extension splits:
\[
        c_1^{-1}(\mathcal E(X))\cong
                        \mathcal E(X)\times\mathbb Z/2.      \tag{5}
\]
This is a noncanonical abstract group splitting, not a smooth group action. In a direct product with \(\mathbb Z/2\), the order of \((a,\epsilon)\) is the least common multiple of the two coordinate orders. In particular, if all finite-order elements of \(\mathcal E(X)\) had order at most two, (5) could not introduce an order-four element above it. The spin-extension construction cannot manufacture the desired cyclic torsion out of boundary twists alone.

**Outcome and exact gap.** The many relative boundary rotations disappear under ordinary capping. Gluing nontrivial four-manifold caps instead of balls changes the target and could preserve classes, but requires a nontriviality/injectivity theorem not furnished by (2). For the K3 neck construction that is exactly the geometric difficulty retained in Corollary 2, not an automatic consequence of a relative theorem.

## 6. Approach 4: finite Coxeter groups from two-sphere twists

Unlike neck twists, twists around ((-2)\)-spheres naturally make higher cyclic orders through braid relations. This gives a genuinely different candidate source of finite groups. The calculation below tests whether their homology actions can cancel.

For a ((-2)\)-sphere with class (v\), the imported local facts are that its smooth twist \(T_v\) has order two and that its homology action is the Picard–Lefschetz reflection
\[
                   r_v(x)=x+(x\cdot v)v.                    \tag{6}
\]
For standard Lagrangian (A_r\)-configurations, adjacent twists obey the braid relation and disjoint twists commute. The square isotopy and formula (6) are given in [S, Proposition 1.1 and introductory formula (0.2)] and [AB, Proposition 3]; the braid construction is explained in [S, Section 1]. We restrict to this standard configuration, not arbitrary immersed or singular spheres.

**Proposition 5.** Suppose a symplectic four-manifold contains Lagrangian spheres (S_1,\ldots,S_r\) in the standard (A_r\)-chain configuration: adjacent spheres intersect transversely once and nonadjacent spheres are disjoint. In the smooth mapping-class group the subgroup generated by their twists is isomorphic to (S_{r+1}\), and its action on (H_2\) is faithful. If the manifold is also closed and simply connected, this subgroup intersects \(\mathcal E\) trivially.

**Proof.** Orient the spheres successively so that adjacent intersection numbers are (+1\). Their intersection matrix is the negative Cartan matrix of (A_r\), with diagonal (-2\), adjacent entries (1\), and other entries zero. It is negative definite, hence the classes (v_i=[S_i]\) are linearly independent over \(\mathbb Q\).

The local relations give a surjection from the Coxeter presentation of (S_{r+1}\) to the subgroup generated by the smooth twists. On the span of the (v_i\), identify (v_i\) with (e_i-e_{i+1}\) inside the sum-zero subspace of \(\mathbb Q^{r+1}\), using the negative standard inner product. Formula (6) then identifies (r_{v_i}\) with the adjacent transposition \((i,i+1)\).

The permutation representation of (S_{r+1}\) on the sum-zero subspace is faithful: a permutation fixing every difference (e_i-e_j\) is the identity. Therefore the composite of the surjection to the smooth twist subgroup and its homology action is faithful. The surjection cannot have a nontrivial kernel, and neither can the homology action of the resulting subgroup. The last assertion follows from (1). ∎

For the smallest candidate (r=2\), relative to (v_1,v_2\),
\[
 r_{v_1}=\begin{pmatrix}-1&1\\0&1\end{pmatrix},\qquad
 r_{v_2}=\begin{pmatrix}1&0\\1&-1\end{pmatrix},\qquad
 r_{v_1}r_{v_2}=\begin{pmatrix}0&-1\\1&-1\end{pmatrix}.
\]
The product has order three, but its homology action is not the identity. The desired torsion has been produced in the ambient smooth mapping-class group, not in its exotic kernel.

A natural repair is to choose two sphere twists with equal homology reflections, hoping their product enters the kernel while retaining a braid relation. It does not work with the standard one-intersection geometry:

**Lemma 6.** If (u^2=v^2=-2\) in a nondegenerate rational intersection space and (r_u=r_v\), then (u=\pm v\). In particular \(|u\cdot v|=2\), so spheres representing them cannot intersect transversely in exactly one point.

**Proof.** The (-1\)-eigenspace of (r_u\) is the line \(\mathbb Q u\), and similarly for (v\). Equality of reflections gives (u=\lambda v\). Comparing squares gives \(\lambda^2=1\). A single transverse intersection has algebraic intersection number (+1\) or (-1\), contradicting absolute value two. ∎

For completeness, the abstract strategy itself is valid: if distinct involutions (a,b\) have \(\rho(a)=\rho(b)\), then (ab\in\ker\rho\); if in addition (aba=bab\), then \((ab)^3=1\), and (ab\ne1\) makes its order three. Lemma 6 shows why ordinary (A_2\) sphere geometry cannot supply both conditions. It does not rule out some other geometric realization of the abstract relations.

**Outcome and exact gap.** Standard (A_r\) finite twist groups inject into homology. Homologically invisible products of homologous sphere twists require different relations/geometric configurations, and no finite-power isotopy for such a product has been established here. Passing instead to symplectic classes of squared twists does not help, since those squares are smoothly trivial.

## 7. Approach 5: actual periodic diffeomorphisms and fixed-point constraints

This route attempts the stronger construction of a finite group of genuinely periodic diffeomorphisms acting trivially on homology. Such a construction still needs faithful passage to smooth mapping classes; a nonidentity periodic map can be smoothly isotopic to the identity.

### 7.1 Localization and free actions fail

**Lemma 7.** A finite-order diffeomorphism of a connected manifold which is the identity on a nonempty open set is the identity everywhere.

**Proof.** Average a Riemannian metric over the finite cyclic group. The diffeomorphism becomes an isometry. At a point of the given open set it fixes the point and has identity derivative. An isometry is determined by that point and derivative: the exponential-map identity first makes it the identity on a normal neighborhood, and continuation along paths on a connected manifold gives the conclusion. ∎

Thus a nontrivial twist supported in a proper collar cannot itself become a genuinely periodic map while retaining that support. Its finite order as a mapping class is consistent with Lemma 7 because only an isotopy of its square to the identity was constructed.

**Lemma 8.** Every orientation-preserving homologically trivial diffeomorphism of a smooth closed simply connected four-manifold has a fixed point.

**Proof.** Here (H_1=H_3=0\), while (H_0,H_4\) each have rank one. Its Lefschetz number is
\[
                        L(f)=2+b_2(X)>0.
\]
The Lefschetz fixed-point theorem gives a fixed point. ∎

In particular, free deck transformations or freely acting cyclic groups cannot directly give the desired homologically trivial periodic representatives. This obstruction holds before any gauge theory is used.

### 7.2 Even periodic groups on the K3 sums are excluded

The periodic rigidity theorem of Matumoto and Ruberman, in the form stated and used in [K, proof of Proposition 7.1], says that a simply connected closed spin four-manifold with nonzero signature admits no nonidentity homologically trivial locally linear involution. Smooth involutions are included. We use this only for actual involutions, not for elements of order two in a mapping-class group.

**Proposition 9.** If (X\) is smooth, closed, simply connected, spin, and \(\sigma(X)\ne0\), a finite subgroup of \(\operatorname{Diff}^+(X)\) all of whose elements act trivially on (H_2(X;\mathbb Z)\) has odd cardinality. In particular no nontrivial elementary abelian two-subgroup of \(\mathcal E(X)\) can be realized faithfully by diffeomorphisms.

**Proof.** If the finite diffeomorphism group had even order, Cauchy's theorem would provide a nonidentity element of order two. This is a homologically trivial smooth involution, contradicting the stated rigidity theorem. A faithful realization of an elementary abelian two-subgroup in \(\mathcal E\) would be such an even-order group. ∎

For \(X_n=\#^nK3\), the hypotheses hold: the manifold is simply connected and spin, and \(\sigma(X_n)=-16n\ne0\). Thus a positive answer from Theorem 1 would necessarily be a non-realizable finite subgroup. This is entirely compatible with the already known order-two case and the homotopy-coherent actions in [LS]. It is a limitation of this **periodic construction route**, not a negative answer to KP-4.80.

For the single K3 surface, [CK, Corollary A] excludes all nonidentity homologically trivial finite symplectic symmetries, of any finite order, for its standard orientation. This closes the symplectic-periodic subroute there. It does not apply to arbitrary smooth maps, to mapping classes with no periodic representative, or automatically to connected sums of K3s.

**Outcome and exact gap.** The periodic route requires fixed points, cannot retain proper collar support, and cannot realize even-order homologically trivial groups on K3 sums. An odd-order non-symplectic smooth action on a suitable manifold would remain a possible stronger route, but neither such an action with a nontrivial smooth mapping class nor a general exclusion was constructed here. The original question is broader and can be answered by non-realizable finite mapping-class subgroups.

## 8. What has and has not been established

The main self-contained geometric/algebraic partial result is Theorem 1. Its immediate consequence for the proposed three-K3 example is a sharp dichotomy: the standard neck subgroup is trivial or a Klein four-group. There is no intermediate order-two subgroup for these standard symmetric generators. Showing one standard neck nontrivial would therefore settle the finite-subgroup existence question.

The unresolved statement is explicit:
\[
 [t]\ne1\quad\text{in}\quad
 \pi_0\operatorname{Diff}^+(K3\#K3\#K3),
\]
where (t\) twists about the neck separating one K3 from the other two. It is not implied here by a nontrivial punctured boundary twist, by stabilization with (S^2\times S^2\), by homotopy-coherent realizability, or by an invariant that has just been calculated to vanish.

The cyclic-order question has a different remaining requirement: exhibit a class in \(\mathcal E(X)\) with a finite-power smooth isotopy and an exact order greater than two. The neck family cannot do this because it has exponent two. The standard finite (A_r\) sphere-twist family cannot do it because homology is faithful on that subgroup. Neither obstruction excludes other constructions.

Accordingly, the justified status is **partial result / unresolved**, with **five completed mathematical approaches**. There is no proof of the original existence assertions, no proof of their negations, and no verified prior complete solution claimed.

## 9. Imported dependencies and proof boundaries

The elementary group arguments, permutation-module classification, collar-action relation, reflection calculations, capping-order arithmetic, and Lefschetz/isometry deductions are proved above. The following inputs are imported:

1. Closed simply connected topological isotopy classification, for (1). It is explicitly cited by [K3] and used in [KM] and [B]. It is not reproved here.
2. Isotopy extension and local disk/frame-space facts, together with \(\pi_1SO(4)=\mathbb Z/2\). The collar proof uses only a full rotation of one real two-plane. The capping exact sequence and diagonal alternatives are those of [B, Section 7].
3. [KM] nontriviality on two K3s, the families gluing formula and the K3 Bauer–Furuta value; [IWX] the fourth stable stem. These are not rederived analytically or by the executable checks.
4. [B, Theorems 7.2 and 7.7] for the homotopy-K3 capping extension and its restriction. Central-extension classification by (H^2\) is used to obtain (5).
5. The local two-sphere twist square, Picard–Lefschetz formula, and standard Lagrangian braid relations from [S] and [AB]. No arbitrary sphere configuration is assumed to satisfy them.
6. Lefschetz's fixed-point theorem, rigidity of isometries, and Cauchy's theorem in the periodic-route deductions.
7. The Matumoto–Ruberman periodic involution theorem, checked through its explicit application in the primary paper [K, Proposition 7.1], and [CK, Corollary A]. The original AMS landing-page retrieval for Ruberman was unavailable; no independent proof audit of that imported theorem is claimed.

[T], [L], [LS], [JL], and [BT] enter the scope/current-literature discussion; none is promoted to a missing closed-neck nonvanishing theorem. Their analytical proofs were not independently reproduced.

## 10. Reproducible exact checks

Run with Python 3 and the standard library:

    python verify_exact.py --output recomputed.json
    diff -u EXACT_CHECKS.json recomputed.json

The program computes, rather than hard-codes, the permutation-invariant subspaces of \(\mathbb F_2^n\) containing the diagonal for (2\le n\le8\). It starts at the diagonal and exhaustively adjoins outside vectors, closes under adjacent transpositions, and takes linear spans. This is exhaustive among invariant superspaces: every such superspace is reachable by adjoining generators. It checks exactly the quotient-rank alternatives proved in Theorem 1 and computes the number of invariant scalar \(\mathbb F_2\)-characters. It also prints the four-element quotient for (n=3\).

Separately it generates exact integer reflection matrices for (A_r\), (1\le r\le5\), checks form preservation, squares and braid relations, exhaustively closes the generated matrix group, and checks orders \((r+1)!\) and Coxeter-element orders (r+1\). These are finite algebra checks of the homology representation, not evidence that an unprovided geometric configuration exists.

The Bauer–Furuta section of the output is labeled as arithmetic conditional on imported formulas and \(\eta^4=0\); it does not compute stable stems or a gauge invariant from a triangulation. The K3 Euler characteristics/signatures are arithmetic checks only. No finite computation can replace the missing smooth-isotopy/non-isotopy argument here.

## References

- **[K3]** R. İnanç Baykur, Robion C. Kirby, and Daniel Ruberman, *K3: A New Problem List in Low-Dimensional Topology*, 2026 author preliminary manuscript, Problem 4.80, p. 256. [Author manuscript](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).
- **[KM]** P. B. Kronheimer and T. S. Mrowka, *The Dehn twist on a sum of two K3 surfaces*, Mathematical Research Letters 27 (2020), 1767–1783. [DOI](https://doi.org/10.4310/MRL.2020.v27.n6.a8); [author version](https://arxiv.org/abs/2001.08771).
- **[JL]** Jianfeng Lin, *Isotopy of the Dehn twist on K3 # K3 after a single stabilization*, Geometry & Topology 27 (2023), 1987–2012. [Author version](https://arxiv.org/abs/2003.03925).
- **[B]** David Baraglia, *On the mapping class groups of simply-connected smooth 4-manifolds*, arXiv:2310.18819v1. [Author version](https://arxiv.org/abs/2310.18819).
- **[T]** Scotty Tilton, *The Boundary Dehn Twist on a Punctured Connected Sum of Two K3 Surfaces is Nontrivial in the Smooth Mapping Class Group*, arXiv:2511.16804v1, November 2025. [Preprint](https://arxiv.org/abs/2511.16804).
- **[L]** Ayodeji Lindblad, *Boundary Dehn twists are often commutators*, arXiv:2604.13194v2, 27 May 2026. [Preprint](https://arxiv.org/abs/2604.13194).
- **[LS]** Yujie Lin and Yi Sha, *On the Homotopy Coherent Nielsen Realization Problem for K3-Type 4-Manifolds*, arXiv:2606.24482v2, 26 August 2026. [Preprint](https://arxiv.org/abs/2606.24482).
- **[BT]** David Baraglia and Joshua Tomlin, *Exotic diffeomorphisms of 4-manifolds with b+ = 2*, The Quarterly Journal of Mathematics, published 7 September 2026. [DOI](https://doi.org/10.1093/qmath/haag031).
- **[S]** Paul Seidel, *Lectures on four-dimensional Dehn twists*, arXiv:math/0309012v3; published in Lecture Notes in Mathematics 1938 (2008), 231–267. [Author version](https://arxiv.org/abs/math/0309012).
- **[AB]** Mihail Arabadji and R. İnanç Baykur, *Nielsen realization in dimension four and projective twists*, Advances in Mathematics 463 (2025), 110112; inspected arXiv:2304.10399v3. [Author version](https://arxiv.org/abs/2304.10399).
- **[K]** Hokuto Konno, *Dehn twists and the Nielsen realization problem for spin 4-manifolds*, Algebraic & Geometric Topology 24 (2024), 1739–1753; inspected arXiv:2203.11631v4. [Author version](https://arxiv.org/abs/2203.11631).
- **[CK]** Weimin Chen and Sławomir Kwasik, *Symplectic symmetries of 4-manifolds*, Topology 46 (2007), 103–128; inspected arXiv:0709.1708v1. [Author version](https://arxiv.org/abs/0709.1708); [DOI](https://doi.org/10.1016/j.top.2006.12.003).
- **[IWX]** Daniel C. Isaksen, Guozhen Wang, and Zhouli Xu, *Stable homotopy groups of spheres*, Proceedings of the National Academy of Sciences 117 (2020), 24757–24763; inspected arXiv:2001.04247v1. [Author version](https://arxiv.org/abs/2001.04247); [DOI](https://doi.org/10.1073/pnas.2012335117).
