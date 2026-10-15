# 6800007: a cohomological classification candidate

**Status: complete candidate for independent adversarial review; not yet a verified solution or a novelty claim.**

The proposed result concerns a fixed smooth real 3-manifold and homotopies **through totally real immersions**. This is the convention used in Falbel–Veloso's later Proposition 8.1. It does not classify embeddings, proper immersions, contact structures up to equivalence, or images modulo diffeomorphisms. The flag manifold is the ordered complex flag variety with its integrable complex structure, not its nearly Kähler almost complex structure.

## 1. Statement

Let \(M\) be a connected smooth, second-countable real 3-manifold without boundary. Compactness and orientability are not assumed; maps and homotopies are not required to be proper. All cohomology groups below have ordinary integral coefficients, except where \(\mathbb Z/2\) is indicated. Set

\[
A=H^1(M;\mathbb Z),\quad B=H^2(M;\mathbb Z),\quad C=H^3(M;\mathbb Z),
\qquad \delta=\beta(w_1(TM))\in B,
\]

where \(\beta\) is the Bockstein for \(0\to\mathbb Z\xrightarrow{2}\mathbb Z\to\mathbb Z/2\to0\).
Define the index set

\[
\mathcal X_M=\{(x,y)\in B^2:-4x-2y=\delta\}.
\tag{1}
\]

For each \((x,y)\in\mathcal X_M\), define the homomorphism

\[
D_{x,y}:A\oplus A\longrightarrow A\oplus C,
\qquad
D_{x,y}(p,q)=\left(-4p-2q,\ (2x+y)\smile p+(x+2y)\smile q\right).
\tag{2}
\]

**Candidate theorem.** Totally real regular-homotopy classes of immersions
\(M\to F=SL(3,\mathbb C)/B_{\mathrm{upper}}\)
are partitioned by \(\mathcal X_M\). For each index, its fiber is a torsor for

\[
C\ \oplus\ \operatorname{coker}D_{x,y}.
\tag{3}
\]

In particular, choosing one reference class in each nonempty fiber gives a noncanonical bijection with the disjoint union of the groups in (3). There is no preferred zero immersion in a fiber. The indices are the first Chern classes of the first and second ordered tautological quotient lines. No Weyl-group permutation is being divided out.

A consequence is the existence criterion

\[
\operatorname{Imm}_{\mathrm{TR}}(M,F)\ne\varnothing
\quad\Longleftrightarrow\quad
\delta\in2B
\quad\Longleftrightarrow\quad
w_1(TM)^2=0\in H^2(M;\mathbb Z/2).
\tag{4}
\]

Thus every orientable 3-manifold is covered. The formula also retains the obstruction and torsion information for nonorientable manifolds. A disconnected manifold is treated componentwise.

## 2. Prior results and scope of the proposed contribution

The original [Morgan–Pansu problem list](https://www.imo.universite-paris-saclay.fr/~pansu/problems_MTDG.tex), Question 7, already states that Gromov's h-principle applies. Accordingly the analytic-to-formal reduction below is not new. The [2018 arXiv paper](https://arxiv.org/abs/1804.11096) and the [2020 published paper](https://doi.org/10.1007/s10711-020-00528-4) must be distinguished: the later [author-provided manuscript](https://www.researchgate.net/publication/340658748_Flag_structures_on_real_3-manifolds), Section 8.1, Proposition 8.1, already treats the three-sphere and its extra integer of totally real regular-homotopy classes over a nonzero underlying homotopy class. That special case is credited to Falbel–Veloso, not claimed as new here.

General primary/secondary classifications of maps from three-dimensional complexes into homogeneous spaces are also prior work; see Koshkin, [*Homotopy classification of maps into homogeneous spaces*](https://arxiv.org/abs/0808.0024), Theorem 3. No general obstruction-theory method is claimed as new.

The proposed additional step is the explicit integral cokernel (2), including the action of homotopies of the line-bundle data. Merely listing a formal frame bundle or the classes over a fixed map would not perform this step. The argument uses standard bundle classification and the parametric h-principle. Whether this exact formulation already occurs elsewhere remains a separate literature question.

## 3. The h-principle and the formal problem

A real-linear map \(L:T_mM\to T_zF\) is totally real precisely when its complexification

\[
L_{\mathbb C}:T_mM\otimes_{\mathbb R}\mathbb C\longrightarrow T_zF
\]

is a complex-linear isomorphism. Therefore formal totally real immersion data are a map \(f:M\to F\) and a complex bundle isomorphism

\[
TM\otimes\mathbb C\simeq f^*TF.
\tag{5}
\]

The parametric totally real immersion h-principle identifies regular-homotopy classes of actual immersions with homotopy classes of these formal data. Its applicability here can also be seen from the open ample first-order relation: after fixing two independent derivative columns, the allowed third column is the complement of their complex span in \(\mathbb C^3\). This is a connected complement of real codimension two and has the whole principal affine slice as its convex hull. Slices with dependent fixed columns are empty. The same argument applies to any chosen principal direction and is local in target coordinates. The open ample parametric h-principle applies to closed as well as open source manifolds; no embedding or properness condition is included.

For the classical totally real h-principle and its uses, see Forstnerič, [*On totally real embeddings into* \(\mathbb C^n\)](https://users.fmf.uni-lj.si/forstneric/papers/1986Expositiones.pdf), Theorem 1.1 and Section 2, and Borrelli, [*On totally real isotopy classes*](https://doi.org/10.1155/S1073792802105125), Section 2. Forstnerič's Theorem 1.4 explicitly assumes a compact **orientable** 3-manifold. Its orientability assumption must not be silently removed.

## 4. A simultaneous bundle-classifying-space model

Write \(T^2\subset SU(3)\) for the diagonal determinant-one torus. Orthogonal decomposition identifies the complex flag manifold with \(SU(3)/T^2\). Over \(BT^2\) there are three universal ordered complex lines \(L_1,L_2,L_3\), with a specified trivialization of their product. Thus

\[
c_1(L_1)+c_1(L_2)+c_1(L_3)=0.
\]

There are two relevant representations of \(T^2\):

\[
E_0=L_1\oplus L_2\oplus L_3,
\qquad
E_\rho=(L_1^*\otimes L_2)\oplus(L_1^*\otimes L_3)\oplus(L_2^*\otimes L_3).
\tag{6}
\]

The first has its specified determinant trivialization and defines
\(b_0:BT^2\to BSU(3)\). Its homotopy fiber is \(SU(3)/T^2\).
The second defines \(b_\rho:BT^2\to BU(3)\). Restricted to this fiber, it is the holomorphic tangent bundle of the flag variety: at the standard flag, the quotient of \(\mathfrak{sl}_3(\mathbb C)\) by the upper triangular subalgebra consists of the three lower matrix entries, of weights \(t_j/t_i\) for \(i<j\).

Fix a classifying map \(\tau:M\to BU(3)\) for \(TM\otimes\mathbb C\). The space of formal data (5) is consequently modeled by the homotopy fiber over \((*,\tau)\) of

\[
\operatorname{Map}(M,BT^2)
\xrightarrow{(b_0,b_\rho)}
\operatorname{Map}(M,BSU(3))\times\operatorname{Map}(M,BU(3)).
\tag{7}
\]

A point of this homotopy fiber consists of line-bundle data, an \(SU(3)\)-trivialization of \(E_0\) up to homotopy, and an isomorphism of \(E_\rho\) with \(TM\otimes\mathbb C\) up to homotopy. The specified determinant in the first factor is important: replacing it by a free \(U(3)\)-trivialization would add a spurious invariant.

## 5. Components of the source and target of (7)

Every smooth 3-manifold has the homotopy type of a CW complex of dimension at most three. The arguments below are dimension bounds on cells and also apply when the CW complex is infinite.

Complex rank-three bundles on such a complex are classified by \(c_1\). This follows from the determinant fibration with fiber \(BSU(3)\), which is 3-connected. Likewise every \(SU(3)\)-bundle on \(M\) is trivial. Components of \(\operatorname{Map}(M,BT^2)\) are pairs \((x,y)\in B^2\), corresponding to

\[
(x_1,x_2,x_3)=(x,y,-x-y).
\]

For (6),

\[
c_1(E_\rho)=\sum_{i<j}(x_j-x_i)=2(x_3-x_1)=-4x-2y.
\tag{8}
\]

The determinant of \(TM\otimes\mathbb C\) is the complexification of the orientation line of \(TM\). Its transition signs give
\(c_1(TM\otimes\mathbb C)=\beta(w_1(TM))=\delta\).
It follows that the component \((x,y)\) has a nonempty fiber in (7) exactly when (1) holds. This proves existence for every admissible index, before counting its formal homotopy classes.

The coefficient exact sequence gives \(\delta\in2B\) if and only if its mod-two reduction vanishes. The standard Bockstein identity
\(\rho_2\beta(w_1)=Sq^1w_1=w_1^2\)
then proves (4).

## 6. The two loop groups, including their integral coordinates

At a component of the source of (7),

\[
\pi_1\operatorname{Map}(M,BT^2)=A\oplus A.
\tag{9}
\]

A loop is represented by three line bundles on \(M\times S^1\) whose Chern classes are
\(x_i+h_i t\), where \(t\) generates \(H^1(S^1;\mathbb Z)\),
\(h_1=p,h_2=q,h_3=-p-q\).

For the target, the loop groups are

\[
\pi_1\operatorname{Map}(M,BSU(3))\simeq C,
\qquad
\pi_1(\operatorname{Map}(M,BU(3)),\tau)\simeq A\oplus C.
\tag{10}
\]

Here are integral coordinates and their justification, so that torsion is not discarded by a rational Chern-character computation. A loop in the second mapping space clutches a rank-three bundle \(V\) on \(M\times S^1\) with its fixed identification to \(E=TM\otimes\mathbb C\) at \(t=0\). Take the relative stable virtual difference

\[
\xi=[V]-[\operatorname{pr}_M^*E].
\]

The two coordinates are the slant products

\[
(c_1(\xi)/[S^1],\ -c_2(\xi)/[S^1])\in A\oplus C.
\tag{11}
\]

Stabilization from \(BU(3)\) is sufficiently connected for these loop classes: the relative domain has dimension four and a homotopy has dimension five. In these dimensions stable complex bundles are classified by \(c_1,c_2\). Indeed the map to \(K(\mathbb Z,2)\times K(\mathbb Z,4)\) defined by these classes induces isomorphisms of homotopy groups through dimension five. The relevant groups are \(\pi_2=\mathbb Z\), \(\pi_4=\mathbb Z\), and zero in dimensions one, three, and five; \(c_2\) detects a generator on \(S^4\). Relative obstruction theory therefore gives the asserted bijection, including integral torsion. These low homotopy groups can equivalently be obtained from unitary stabilization and \(SU(2)\to SU(3)\to S^5\).

Addition of relative classes makes (11) additive: the possible cross term in \(c_2\) is the product of two classes \(h t\), which is zero since \(t^2=0\). For the \(BSU(3)\) factor the first coordinate is absent, and the coordinate is \(-c_2/[S^1]\). Thus both groups in (10) are abelian. Using the virtual difference in (11), rather than the Chern classes of \(V\) alone, is essential when \(E\) is nontrivial.

## 7. The monodromy calculation

The image of (9) in the first group of (10) is

\[
a=\sum_{i=1}^3 x_i\smile h_i.
\tag{12}
\]

To check the sign and normalization directly, the coefficient of \(t\) in
\(c_2(\bigoplus L_i)\) on the product is
\(\sum_{i<j}(x_i h_j+x_j h_i)=-\sum_i x_i h_i\), since both sums of classes vanish. The coordinate in (10) uses its negative.

For the second bundle in (6), put \(r_{ij}=x_j-x_i\) and \(k_{ij}=h_j-h_i\). Its loop has first coordinate

\[
k=\sum_{i<j}k_{ij}=2(h_3-h_1).
\tag{13}
\]

Its second coordinate is

\[
b=\sum_{i<j}r_{ij}\smile k_{ij}.
\tag{14}
\]

For completeness, (14) remains true when \(\delta\ne0\). The coefficient of \(t\) in the ordinary \(c_2(V)\) is \(\delta k-\sum r_{ij}k_{ij}\). For the virtual difference \(V-E\), the formula

\[
c_2(V-E)=c_2(V)-c_1(V)c_1(E)+c_1(E)^2-c_2(E)
\]

subtracts precisely the term \(\delta k\). Taking the negative slant product gives (14), with no division by two and no loss of torsion.

The elementary identity

\[
\sum_{i<j}(x_j-x_i)(h_j-h_i)
=3\sum_i x_i h_i-(\sum_i x_i)(\sum_i h_i)
=3a
\tag{15}
\]

therefore identifies the image of the loop group as

\[
\{(a,k,3a):p,q\in A\}\subset C\oplus A\oplus C.
\tag{16}
\]

The products in (12)–(15) are cup products; degree-two classes commute with degree-one classes, so these polynomial identities hold over integral cohomology, including torsion.

## 8. Why this quotient gives the entire classification

For a map of spaces \(X\to Y\), the components of its homotopy fiber lying over a fixed component of \(X\) mapping to the chosen component of \(Y\) form the orbit set of \(\pi_1(Y)\), with stabilizer the image of \(\pi_1(X)\), after a reference point and path are chosen. This is the exact sequence of a homotopy fiber at \(\pi_1\) and \(\pi_0\). It accounts for homotopies of the base data, not just homotopies over a fixed map. In (7), \(\pi_1(Y)\) is abelian by (10), so the orbit set is a torsor for its quotient group.

Consequently the fiber over \((x,y)\) is a torsor for

\[
(C\oplus A\oplus C)/\{(a,k,3a)\}.
\]

The integral automorphism \((u,m,v)\mapsto(v-3u,m,u)\) takes (16) to \((0,k,a)\). Substituting \(x_3=-x-y\) and \(h_3=-p-q\) yields

\[
k=-4p-2q,
\qquad
a=(2x+y)\smile p+(x+2y)\smile q.
\]

This is exactly (2)–(3). Sections 3–5 show both that every listed fiber is nonempty and that every actual immersion belongs to one of them. The homotopy-fiber argument shows that two entries are identified exactly by the stated action. This proves the candidate theorem, subject to the independent review of the standard homotopy and h-principle inputs and their use above.

## 9. Checks and illustrations

### The three-sphere

Here \(A=B=0\), \(C=\mathbb Z\), and the classification is a torsor for \(\mathbb Z^2\). One integer records the underlying homotopy class in \(\pi_3(F)\); the second records the formal derivative. This recovers the already-known sphere calculation, rather than constituting a new contribution in that case.

### \(S^2\times S^1\)

Choose generators with positive product. Then \(x=n,y=-2n\) for \(n\in\mathbb Z\). The relation matrix for (2), using \(r=2p+q\), is

\[
\begin{pmatrix}0&-2\\6n&-3n\end{pmatrix}.
\]

For \(n\ne0\), let \(g=\gcd(2,3n)\). The fiber is a torsor for
\(\mathbb Z\oplus\mathbb Z/g\oplus\mathbb Z/(12|n|/g)\).
For \(n=0\), it is a torsor for \(\mathbb Z^2\oplus\mathbb Z/2\).
The finite components reflect the monodromy quotient and would be missed by counting framings over one fixed underlying map.

### \(\mathbb{RP}^2\times S^1\)

The orientation class restricts to the generator on \(\mathbb{RP}^2\), whose square is nonzero. Thus (4) forbids any totally real immersion into the complex flag manifold. This example explains why a statement about all real 3-manifolds cannot silently use the orientable parallelizability theorem.

## 10. Verification boundary

The attached exact checker verifies the root-weight identities, the virtual-Chern-class cancellation, the relation matrices and Smith invariants in modest test ranges, and a torsion coefficient model. Such computations do not prove the h-principle, bundle classification, or the homotopy-fiber orbit theorem. Those are mathematical inputs explicitly identified in the proof. Independent review must in particular test the nontrivial-target-bundle loop coordinates in Section 6, the integral torsion terms in Section 7, the global monodromy quotient in Section 8, and the stated noncompact scope.
