# Finite-subgroup realization on a smooth four-manifold

Problem 2960 / KP-4.84. Research date: 8 October 2026.

## Outcome

**Partial results; the existence problem is unresolved by this report.** Five distinct mathematical approaches are developed below. They yield explicit realizations for substantial standard subgroups, conditional lifting criteria, and obstruction criteria. No approach establishes the required property for the entire smooth mapping class group of one closed four-manifold. No claim of a new solution, a universal negative result, or novel publication-level theorem is made.

The strongest positive result proved here is a realization theorem for every finite subgroup of the standard product-and-factor-swap subgroup on a product of two closed surfaces. The principal missing step is control of smooth isotopy classes outside that subgroup, including finite subgroups involving the homotopically trivial kernel. A separate exact algebraic example proves why a torsion-free kernel and a realized quotient do not alone fill that gap.

## 1. Source normalization and the actual quantifiers

Let

\[
D_X=\operatorname{Diff}^{+}(X),\qquad
M_X=\pi_0 D_X,\qquad q_X:D_X\longrightarrow M_X.
\]

The target property is

\[
\mathcal R(X):\quad
\forall\, G\leq M_X\text{ finite},\quad
\exists\,s_G:G\longrightarrow D_X\text{ a group homomorphism},\quad
q_Xs_G=\iota_G.
\tag{1}
\]

KP-4.84 asks whether **there exists** a closed oriented smooth four-manifold with property (1). The same manifold must work for every finite subgroup, while the chosen action may depend on that subgroup. The section equation makes every resulting action faithful. Neither a single action simultaneously containing all finite subgroups nor a section over the entire, possibly infinite, mapping class group is required.

The actual 2026 K3 preliminary book, Problem 4.84 on printed/PDF page 259, was retrieved and visually inspected. Its group is \(\pi_0\operatorname{Diff}^{+}(X)\), with **smooth isotopy**, and its remark defines realization by the section equation. The commonly supplied AIM URL is a four-page workshop summary and is not the problem-list source. The local corpus's OCR spacing defects do not change the quantifiers. [S1, S2]

There is no simply-connected, symplectic, nonzero-signature, or nontrivial-finite-subgroup hypothesis. In particular, a manifold with torsion-free smooth mapping class group would be a legitimate witness, since its only finite subgroup is trivial. This observation does not produce such a manifold.

We use connected candidates. This loses no nonempty disconnected witness: the smooth mapping classes of a connected component embed into those of a finite disjoint union by extending maps by the identity. A section over such an embedded subgroup cannot permute components, because its prescribed mapping classes do not permute them. Restricting the section to the selected component proves (1) there.

### Three problems that must be distinguished

1. The target: lifting a prescribed subgroup of **smooth** mapping classes.
2. Topological-class realization: lifting finite subgroups of \(\pi_0\operatorname{Homeo}^{+}(X)\) to smooth diffeomorphisms.
3. Homological realization: lifting finite subgroups of the image of \(D_X\) on homology.

A smooth action solving problem 2 or 3 can land in different smooth isotopy classes from the ones prescribed in problem 1. Conversely, a subgroup in a homology quotient need not itself lift to a finite subgroup of \(M_X\). All uses below retain these distinctions.

## 2. Current-source readiness, before the five approaches

The following are source checks, not mathematical attempt counts.

- **Lee:** Proposition 3.1 gives smooth lifts of the entire *topological* mapping class group for \(\mathbb{CP}^2\), \(S^2\times S^2\), and \(\mathbb{CP}^2\#\overline{\mathbb{CP}}^2\). The definition of \(\mathrm{Mod}\) in that paper is explicitly \(\pi_0\mathrm{Homeo}^{+}\). Thus its positive results cannot be substituted for (1). [S3]
- **Baraglia:** Theorem 1.4 splits the homology-image extension at the **smooth mapping-class** level for \(\#_n\mathbb{CP}^2\). Theorem 1.6 gives nonrealizable \((\mathbb Z/2)^4\) subgroups for the stated simply-connected connected sums with at least four signed projective-plane summands. This demonstrates that a mapping-class-level splitting is not a diffeomorphism-level splitting. The arXiv manuscript is v1; its record now identifies the 2026 journal publication. [S4]
- **Lee–Lewis–Raman:** The 2025 cyclic del Pezzo paper again defines its mapping class group topologically. Its results concern specified finite-order classes, with additional irreducibility and homological hypotheses. It supplies neither all finite subgroups nor all smooth mapping classes. [S5]
- **Pesikoff, May 2026:** The paper concerns homological realization for \(\#_n\mathbb{CP}^2\), with positive constructions and strong nonrealizability results. Its introduction explicitly distinguishes the known mapping-class-level splitting from realization by periodic diffeomorphisms. [S6]
- **Lin–Sha, v2, August 2026:** Theorem 1.4 obstructs even homotopy-coherent realization for the specified order-two classes on K3-type manifolds and their blow-ups. Here K3-type includes \(b_1=0\), \(b_2^+=3\), \(b_2^-=19\), and a unique spin Spin\(^c\) structure. Theorem 1.6 constructs homotopy-coherent realizations for nontrivial order-two neck twists; Corollary 1.7 distinguishes these from genuine actions under its spin and signature assumptions. Thus a map \(BG\to B\mathrm{Diff}(X)\) is not a replacement for (1). [S7]
- **Kerckhoff:** Finite subgroups of the extended mapping class group of a closed surface of genus at least two admit hyperbolic-isometry realizations. We use this exact surface theorem as an input, never as an unproved assertion about all mapping classes of a four-dimensional product. [S8]

The bounded current-source search did not verify a complete positive or negative answer to KP-4.84. The 2026 K3 source retains the question. This is a bounded literature finding, not a proof of universal novelty or a guarantee against unindexed work.

## 3. Approach 1: eliminate exotic complements on a small rational candidate

### 3.1 An unconditional splitting for the homology quotient of CP2

Put \(X=\mathbb{CP}^2\) with its complex orientation. Every orientation-preserving diffeomorphism acts on \(H_2(X;\mathbb Z)\cong\mathbb Z\) by \(+1\) or \(-1\). Complex conjugation \(c\) is orientation preserving in complex dimension two, acts by \(-1\) on \(H_2\), and satisfies \(c^2=1\). Consequently,

\[
M_X=K\rtimes\langle\bar c\rangle,
\qquad K=\ker(M_X\to\{\pm1\}),\quad \bar c=[c],
\tag{2}
\]

with \(\langle\bar c\rangle\cong C_2\). This is a statement about a quotient of the unknown smooth mapping class group, not a computation of that entire group.

Let \(\sigma(k)=\bar c k\bar c^{-1}\). For every \(k\in K\),

\[
(k\bar c)^2=k\sigma(k).
\tag{3}
\]

Suppose, as an unproved additional hypothesis, that \(K\) is torsion-free. Then every finite subgroup \(F\leq M_X\) maps injectively to \(C_2\), since \(F\cap K=1\). Thus \(F=1\) or \(F=\langle k\bar c\rangle\) with \(k\sigma(k)=1\).

For \(h\in K\),

\[
h\bar c h^{-1}=h\sigma(h)^{-1}\bar c.
\tag{4}
\]

Therefore, if every solution of \(k\sigma(k)=1\) has the form \(k=h\sigma(h)^{-1}\), every finite subgroup is conjugate to the standard \(\langle\bar c\rangle\). Choose a diffeomorphism \(H\) in the component \(h\). The genuine involution \(HcH^{-1}\) then realizes the prescribed subgroup. This proves:

**Proposition 1.** CP2 has property (1) if its homological smooth kernel is torsion-free and every \(C_2\)-cocycle for the conjugation action \(\sigma\) is a coboundary.

Both hypotheses are substantive. The second is the triviality of the nonabelian pointed set \(H^1(C_2,K)\); it is not implied by absence of torsion in \(K\). Nor do we claim that it is necessary for realization: a nonstandard complement could have its own genuine smooth action.

### 3.2 A general sufficient averaging criterion

**Proposition 2.** Let \(q:D\to M\) be a surjective group homomorphism, and suppose

\[
M=V\rtimes A,
\]

where \(V\) is the additive group of a rational vector space. Suppose that for every finite \(B\leq A\), the standard subgroup \(\{0\}\rtimes B\leq M\) has a lift through \(q\). Then every finite subgroup of \(M\) has a lift through \(q\).

**Proof.** A finite subgroup \(F\leq M\) intersects torsion-free \(V\) trivially. Its projection \(B\leq A\) is finite and the projection \(F\to B\) is an isomorphism. Thus

\[
F=\{(z(b),b):b\in B\},\qquad
z(ab)=z(a)+a z(b).
\]

Set \(v=|B|^{-1}\sum_{b\in B}z(b)\). For \(a\in B\), reindexing the sum gives

\[
a v=|B|^{-1}\sum_b(z(ab)-z(a))=v-z(a).
\]

Hence \(z(a)=v-av\), and

\[
F=(v,1)(\{0\}\rtimes B)(-v,1).
\]

Choose any \(d\in D\) with \(q(d)=(v,1)\), and conjugate the assumed lift of \(B\) by \(d\). This lifts \(F\) with its actual prescribed inclusion. \(\square\)

For CP2 this would apply if its kernel in (2) were a uniquely divisible abelian group. No such structural assertion is established here. Averaging in a general nonabelian diffeomorphism or mapping-class kernel is not defined.

### 3.3 Exact countermodel to an insufficient shortcut

The following algebraic construction shows that a torsion-free kernel and an actual realization of a quotient can coexist with a nonliftable finite subgroup. It is not claimed to be the diffeomorphism group of any manifold.

Let

\[
M=\mathbb Z\rtimes C_2,
\qquad (n,e)(m,d)=(n+(-1)^e m,e+d).
\]

Its projection to \(C_2\) has torsion-free kernel \(\mathbb Z\). Define

\[
D=(\mathbb Z\times C_2)\rtimes C_2,
\]

where the last involution acts by \((n,z)\mapsto(-n,z+n\bmod2)\). This is an automorphism of order two, so the semidirect product is a group. Explicitly,

\[
(n,z,e)(m,w,d)=
(n+(-1)^e m,z+w+em\bmod2,e+d\bmod2).
\tag{5}
\]

The map \(q:D\to M\), \(q(n,z,e)=(n,e)\), is surjective. The standard quotient complement \(\langle(0,1)\rangle\leq M\) lifts via \((0,0,1)\in D\), which is an involution. But the other reflection \((1,1)\in M\) has precisely the two lifts \((1,z,1)\), and both square to \((0,1,0)\ne1\). Its order-two subgroup has no section through \(q\).

This rules out the proposed deduction “realize the homology quotient and prove the smooth kernel torsion-free; then automatically all finite smooth subgroups are realized.” A further complement-control or direct realization argument is indispensable.

**Exact gap for approach 1:** Neither the required torsion statement nor the cocycle/complement statement has been established for the smooth kernel of CP2. Lee's topological theorem does not supply them.

## 4. Approach 2: linear and affine geometry on the four-torus

Let \(T^4=\mathbb R^4/\mathbb Z^4\), oriented in the usual way. Every \(A\in\mathrm{SL}(4,\mathbb Z)\) induces

\[
L_A([x])=[Ax].
\]

These maps obey \(L_A L_B=L_{AB}\), so they form a genuine action of the entire arithmetic group. The resulting homomorphism

\[
\lambda:\mathrm{SL}(4,\mathbb Z)\longrightarrow M_{T^4}
\]

is injective: the action on \(H_1(T^4;\mathbb Z)\) recovers \(A\), and a smoothly isotopic-to-identity map acts trivially on homology. The homology-action map \(p:M_{T^4}\to\mathrm{SL}(4,\mathbb Z)\) satisfies \(p\lambda=1\). Hence

\[
M_{T^4}=K_T\rtimes\mathrm{SL}(4,\mathbb Z),
\qquad K_T=\ker p.
\tag{6}
\]

**Proposition 3.** Every finite subgroup of \(\lambda(\mathrm{SL}(4,\mathbb Z))\), and every conjugate of such a subgroup in \(M_{T^4}\), is realized on the same smooth four-torus.

**Proof.** Restrict \(A\mapsto L_A\) to the relevant finite subgroup; for a conjugate, choose any diffeomorphism in the conjugating component and conjugate the action. The homology calculation verifies that the prescribed smooth mapping classes are obtained. \(\square\)

This proof realizes many groups of different orders on one four-manifold. For example, the companion matrix

\[
A=\begin{pmatrix}
0&0&0&-1\\1&0&0&-1\\0&1&0&-1\\0&0&1&-1
\end{pmatrix}
\]

has determinant one and order five. The orientation-preserving signed permutation matrices form a group of order \(2^3\cdot4!=192\), all realized linearly.

For any finite \(B\leq\mathrm{SL}(4,\mathbb Z)\), define

\[
Q_B=\sum_{b\in B}b^Tb.
\]

This is positive definite, and \(a^TQ_Ba=Q_B\) for every \(a\in B\), by reindexing the finite sum. It gives an invariant flat metric on the torus. In the displayed order-five example,

\[
Q_B=\begin{pmatrix}
8&-2&-2&-2\\-2&8&-2&-2\\-2&-2&8&-2\\-2&-2&-2&8
\end{pmatrix},\qquad\det Q_B=2000.
\]

Translations do not provide missing smooth mapping classes: \([x]\mapsto[x+tv]\), \(0\leq t\leq1\), isotopes a translation to the identity. Therefore an affine map and its linear part have the same smooth mapping class. Permitting arbitrary affine actions may change the action itself, but does not expand the subgroup \(\lambda(\mathrm{SL}(4,\mathbb Z))\) in (6).

For a general finite \(F\leq M_{T^4}\), the projected finite group \(p(F)\) is indeed linearly realizable. That observation alone does not realize \(F\): it may have nontrivial intersection with \(K_T\), or be a nonstandard complement above its image. Even proving \(K_T\) torsion-free would leave the complement issue exhibited in (5).

**Exact gap for approach 2:** We have not proved that every finite smooth mapping-class subgroup of \(T^4\) is conjugate to a linear one, or otherwise supplied actions in its prescribed components. No computation of \(K_T\) is claimed.

## 5. Approach 3: product surfaces and simultaneous factor-swap realization

This approach transports the full surface Nielsen theorem into a large, explicitly identified four-dimensional subgroup, including finite groups that interchange the factors.

Let \(\Sigma_g\) be a closed oriented surface of genus \(g\geq2\), and write

\[
\Gamma_g=\pi_0\operatorname{Diff}(\Sigma_g)
\]

for its extended mapping class group. For equal factors define

\[
W_g=(\Gamma_g\times\Gamma_g)\rtimes\langle\tau\rangle,
\qquad \tau(a,b)\tau^{-1}=(b,a),\quad\tau^2=1.
\]

Product diffeomorphisms and the actual swap \(\tau(x,y)=(y,x)\) define an injective homomorphism from \(W_g\) into the full smooth mapping class group of \(X=\Sigma_g\times\Sigma_g\).

To verify injectivity, a swapped element interchanges the two nonzero direct summands of \(H_1(X;\mathbb Z)\), so cannot be smoothly isotopic to the identity. For an unswapped element, its action on \(\pi_1(X)=\pi_1\Sigma_g\times\pi_1\Sigma_g\), up to inner automorphism, records the outer automorphisms of each factor. The surface Dehn–Nielsen–Baer identification makes each surface mapping class trivial when that outer automorphism is trivial. This establishes injectivity without assuming a classification of all diffeomorphisms of the product.

The sign of a product diffeomorphism is the product of the orientation signs of its two factors. The swap itself is orientation preserving, since \((-1)^{2\cdot2}=1\). Let \(W_g^+\) be the kernel of that product-sign homomorphism.

**Theorem 4 (standard product-subgroup realization).** Every finite subgroup of \(W_g^+\leq M_X\) is realized by orientation-preserving diffeomorphisms of \(X\). For unequal genera \(g,h\geq2\), every finite subgroup of the orientation-preserving standard subgroup of \(\Gamma_g\times\Gamma_h\) is likewise realized on \(\Sigma_g\times\Sigma_h\).

**Proof for unequal factors, and for groups without swaps.** Let \(F\) be the finite subgroup and \(B_i\) its two coordinate images. Each \(B_i\) is finite. Kerckhoff's theorem supplies homomorphisms

\[
r_i:B_i\longrightarrow\operatorname{Diff}(\Sigma_i)
\]

whose mapping classes are the prescribed inclusions. Restrict the product homomorphism \(r_1\times r_2\) to \(F\). The induced four-dimensional mapping classes are exactly \(F\), by the definition and injectivity of the standard subgroup. Each resulting map has the required orientation sign. \(\square\)

The swapped case cannot be handled merely by taking the subgroup generated by all first and second coordinate entries: even a finite subgroup of a wreath product may have entries generating an infinite group in the ambient factor. Instead we conjugate first.

**Algebraic lemma.** Let \(\Gamma\) be any group and \(F\leq(\Gamma\times\Gamma)\rtimes C_2\) be finite with nontrivial swap image. Then \(F\) is conjugate to a subgroup of \((B\times B)\rtimes C_2\) for some finite subgroup \(B\leq\Gamma\).

**Proof.** Set \(H=F\cap(\Gamma\times\Gamma)\), and let \(B_1,B_2\) be its coordinate projections. These are finite. Choose

\[
t=(a,b)\tau\in F.
\]

Because \(H\trianglelefteq F\), conjugation by \(t\) gives

\[
aB_2a^{-1}=B_1,\qquad bB_1b^{-1}=B_2.
\tag{7}
\]

Also \(t^2=(ab,ba)\in H\), so \(ab\in B_1\). Conjugate by \(c=(1,a)\). Direct multiplication gives

\[
cHc^{-1}\leq B_1\times B_1,
\qquad ctc^{-1}=(1,ab)\tau.
\tag{8}
\]

Since \(F=H\sqcup Ht\), equations (8) imply

\[
cFc^{-1}\leq (B_1\times B_1)\rtimes C_2.
\]

Take \(B=B_1\). \(\square\)

**Completion of the swapped case.** Apply the lemma with \(\Gamma=\Gamma_g\). Realize the finite subgroup \(B\) on one fixed copy of \(\Sigma_g\) by Kerckhoff, obtaining \(r:B\to\operatorname{Diff}(\Sigma_g)\). On its square the formulas

\[
(b_1,b_2)(x,y)=(r(b_1)x,r(b_2)y),\qquad
\tau(x,y)=(y,x)
\]

define a genuine action of \(B\wr C_2\); the conjugation relation with \(\tau\) holds exactly. Restrict to \(cFc^{-1}\).

Choose a diffeomorphism \(C\) representing the product mapping class \(c\). Conjugating this restricted action by \(C^{-1}\) realizes the original prescribed subgroup \(F\). If \(c\) is orientation reversing on the product, conjugation by \(C\) still preserves orientation signs. The subgroup \(W_g^+\) is normal, and the restricted action has the orientation signs of its mapping classes. Thus the final realization lies in \(\operatorname{Diff}^{+}(X)\). \(\square\)

**Exact gap for approach 3:** The standard subgroup is not asserted to equal \(M_X\), and we have not shown that every finite subgroup of \(M_X\) is conjugate into it. Control of induced outer automorphisms of \(\pi_1(X)\) alone would leave the kernel of the smooth-isotopy-to-homotopy map. This theorem therefore realizes all finite subgroups of a specific large subgroup, not all finite subgroups in the target question.

## 6. Approach 4: fixed points in the space of metrics

Let \(\mathscr{M}(X)\) be the space of smooth Riemannian metrics and \(D_0\) the identity component of \(D_X\). The quotient

\[
\mathscr{T}_{\rm met}(X)=\mathscr{M}(X)/D_0
\]

carries an action of \(M_X\). Use inverse pullback for a left action. For a metric \(h\), write \(I_h=\operatorname{Isom}^{+}(X,h)\).

**Proposition 5 (exact metric criterion).** A finite subgroup \(G\leq M_X\) is realizable if and only if there is a metric \(h\) such that:

1. its orbit \([h]\in\mathscr T_{\rm met}(X)\) is fixed by \(G\); and
2. the exact sequence

\[
1\longrightarrow I_h\cap D_0
\longrightarrow E_{h,G}:=I_h\cap q_X^{-1}(G)
\stackrel{q_X}{\longrightarrow}G\longrightarrow1
\tag{9}
\]

has a group-theoretic section.

**Proof.** If \(s:G\to D_X\) is a realization, average any metric \(h_0\):

\[
h=\sum_{g\in G}s(g)^*h_0.
\]

It is positive definite and invariant. Thus \(s(G)\leq I_h\), providing both the fixed orbit and the section in (9).

Conversely, a section of (9), followed by inclusion into \(D_X\), is exactly a realization. It remains to justify exactness on the right when the orbit is fixed. For each prescribed mapping class represented by \(f\), equality of its metric orbit with \([h]\) implies, in pullback notation, \(f^*h=d^*h\) for some \(d\in D_0\). Then \(fd^{-1}\) is an isometry in the same mapping class, since

\[
(fd^{-1})^*h=(d^{-1})^*f^*h=h.
\]

Hence the displayed map onto \(G\) is surjective. Its kernel is exactly \(I_h\cap D_0\). \(\square\)

If \(I_h\cap D_0=1\), condition 2 is automatic. This yields a useful sufficient route: find a fixed orbit whose isometries have no nontrivial identity-isotopic elements. It does not justify discarding condition 2 in general.

A concrete compact Lie group extension explains the distinction. Inside the unit quaternions,

\[
\operatorname{Pin}(2)=S^1\cup jS^1,
\qquad jzj^{-1}=\bar z.
\]

The component quotient is \(C_2\), but every element of the nonidentity component squares to \(-1\):

\[
(jz)^2=-1.
\]

Thus \(1\to S^1\to\operatorname{Pin}(2)\to C_2\to1\) does not split. A fixed point for a quotient action, by itself, is not an abstract reason for a stabilizer-component extension to split. We do not assert that this particular extension occurs as (9) for a four-manifold.

The convexity and contractibility of \(\mathscr M(X)\) also do not finish the argument. The finite group in the problem acts on the quotient of metrics by \(D_0\), not by an already supplied finite group of diffeomorphisms on \(\mathscr M(X)\). Averaging arbitrary component representatives fails to reindex the sum: their products need agree only up to a diffeomorphism in \(D_0\), which need not preserve the metric.

**Exact gap for approach 4:** No universal finite-group fixed-point theorem on \(\mathscr T_{\rm met}(X)\), with the needed stabilizer splitting, has been established for any chosen closed four-manifold. The existence of homotopy-coherent realizations does not remove this exact-group-law requirement.

## 7. Approach 5: force a global fixed point and obstruct its tangent representation

This is a negative approach: if every candidate were forced to have an unrepresentable finite mapping-class subgroup, no witness could exist. The following obstruction is rigorous but does not cover every candidate.

**Lemma 6.** Let a finite \(p\)-group \(P\) act smoothly on a compact manifold \(X\). Then

\[
\chi(X^P)\equiv\chi(X)\pmod p.
\tag{10}
\]

**Proof.** Use a finite equivariant triangulation, available for finite smooth group actions by Illman's theorem [S9], and barycentrically subdivide so that a simplex preserved setwise is fixed pointwise. The simplices not fixed by all of \(P\) occur in orbits whose cardinalities are powers of \(p\) greater than one. Their total contribution to the alternating simplex count is divisible by \(p\). The remaining simplices triangulate \(X^P\), proving (10). \(\square\)

If \(p\nmid\chi(X)\), equation (10) forces \(X^P\ne\varnothing\).

**Lemma 7.** For an effective finite group action by orientation-preserving diffeomorphisms on a connected four-manifold, a common fixed point gives a faithful real representation into \(\mathrm{SO}(4)\).

**Proof.** Average a metric over the actual finite action. At a common fixed point \(x\), differentiation gives an orthogonal orientation-preserving representation on \(T_xX\). An isometry fixing \(x\) with identity derivative fixes a neighborhood through the exponential map. An isometry on a connected Riemannian manifold is determined by its value and derivative at one point, so that element is globally the identity. Effectiveness makes the representation faithful. \(\square\)

**Theorem 8.** Suppose a connected closed oriented smooth four-manifold \(X\) has property (1). For every prime \(p\nmid\chi(X)\):

- an elementary abelian subgroup \((C_2)^r\leq M_X\), when \(p=2\), has \(r\leq3\);
- an elementary abelian subgroup \((C_p)^r\leq M_X\), when \(p\) is odd, has \(r\leq2\).

**Proof.** Realize the prescribed subgroup using (1). The action is effective. Lemma 6 provides a common fixed point, and Lemma 7 embeds it into \(\mathrm{SO}(4)\).

For \(p=2\), commuting orthogonal involutions are commuting symmetric matrices and are simultaneously diagonalizable over \(\mathbb R\). They lie in the group of diagonal sign matrices with determinant one. That group has exactly \(2^3\) elements, so a faithful elementary abelian subgroup has rank at most three.

For odd \(p\), complexifying a real representation of the abelian group decomposes it into characters. Every nontrivial real irreducible constituent is a two-dimensional rotation plane corresponding to a conjugate pair of complex characters; the only one-dimensional real character is trivial. A four-dimensional real representation therefore has at most two independent nontrivial characters. Faithfulness requires those characters to span the dual of \((C_p)^r\), giving \(r\leq2\). \(\square\)

For example, when \(\chi(X)\) is odd, the presence of \((C_2)^4\) in \(M_X\) alone rules out (1). When \(p\) is odd and does not divide \(\chi(X)\), a rank-three elementary abelian \(p\)-subgroup rules it out. This conclusion is about an actually established subgroup of the smooth mapping class group; a subgroup merely visible in a homology quotient is not enough.

Using Baraglia's mapping-class-level splitting, the diagonal sign subgroup \((C_2)^n\) in the homology automorphism group of \(\#_n\mathbb{CP}^2\) injects into its smooth mapping class group. For odd \(n\geq5\), its Euler characteristic \(n+2\) is odd, so Theorem 8 obstructs (1). This is only a restricted rederivation of already-known nonrealizability; Baraglia's theorem covers substantially more. It is not a new resolution of those cases.

### Why a local-support construction is not a universal obstruction

A useful independent boundary check is that a finite-order diffeomorphism of a connected manifold which equals the identity on a nonempty open set is globally the identity. Average a metric over its finite cyclic action and use the isometry argument in Lemma 7. Thus a nontrivial periodic diffeomorphism cannot have support confined to a ball with nonempty exterior.

But a finite-order *mapping class* can have a supported representative of infinite order as a diffeomorphism. Another representative in the same component could have global support and be periodic. Consequently the local-support lemma cannot prove either that the smooth mapping class group has no torsion or that a supported finite-order mapping class is nonrealizable. The missing passage from components to exact periodic representatives is precisely the original issue.

**Exact gap for approach 5:** No argument produces an elementary abelian subgroup exceeding the above bounds in every possible \(M_X\). In particular, the Euler-characteristic condition fails for all primes on \(T^4\), where \(\chi=0\), and asymmetry of a manifold would not by itself prove the absence of torsion in its mapping class group. This approach supplies necessary conditions and specific exclusions, not the universal negative quantifier.

## 8. Five-approach accounting and final boundary

The five counted approaches are:

1. **Small rational candidate and complement elimination:** equations (2)–(5), the conditional CP2 criterion, rational averaging theorem, and exact countermodel.
2. **Flat torus construction:** an explicit global linear section, finite invariant metrics, and the exact affine limitation.
3. **Product-surface geometry:** independent surface realizations plus the finite wreath-subgroup conjugation argument, including orientation and swaps.
4. **Metric fixed-point method:** an exact necessary-and-sufficient criterion retaining the stabilizer-extension problem, and a nonsplitting compact-group model.
5. **Fixed-point representation obstruction:** Euler congruence, faithful tangent representation, and sharp elementary-abelian rank bounds under the stated hypotheses.

These are mathematical constructions and deductions. Source retrieval, literature comparison, corpus checks, source inspection, exact finite tests, and any subsequent audit are counted as zero additional approaches. The overlap in identifying smooth kernels is a common remaining obstacle; the constructions and proposed routes above are different.

The full target remains open in this report. In particular, none of the following substitutions is licensed:

- topological isotopy for smooth isotopy;
- homology-image finite groups for prescribed finite smooth mapping-class subgroups;
- a homotopy-coherent action for a genuine action;
- periodic-diffeomorphism rigidity for torsion-freeness of mapping classes;
- a realized standard subgroup for the whole smooth mapping class group;
- a torsion-free kernel for vanishing complement obstructions;
- many counterexample manifolds for counterexamples on every manifold.

No global queue file is changed by this research packet.

## 9. Verification and reproducibility

Run `python exact_checks.py` in this directory. The accompanying JSON records exact integer and finite-group checks:

- order five and determinant one for the displayed torus matrix;
- its positive definite invariant Gram matrix and determinant 2000;
- closure of all 192 orientation-preserving signed permutation matrices, checking 36,864 products;
- 8,000 exact associativity samples and both obstructed lifts in the algebraic countermodel;
- all 112 subgroups of \(S_3\wr C_2\), including verification of the conjugation formula on its 52 subgroups with a swap;
- 4,096 sign-character systems confirming the orientation-preserving rank-three bound.

The proofs establish the general statements. These finite tests only guard their displayed formulas and bounded algebraic instances. They do not compute a smooth mapping class group, establish any missing kernel hypothesis, or decide KP-4.84. No floating-point inference is used.

`SOURCE_METADATA.json` records public-source identities, byte counts, hashes, version/status and inspection scope without source text. `MANIFEST.sha256.json` freezes the authored public packet; copied papers, source extracts, dataset rows and private coordination material are excluded.

## References

- **S1.** R. İnanç Baykur, Robion C. Kirby and Daniel Ruberman, *K3: A New Problem List in Low-Dimensional Topology*, 2026 preliminary book, Problem 4.84, p. 259. https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf
- **S2.** *K3: A new problem list in low-dimensional topology*, AIM workshop summary, four pages. https://aimath.org/pastworkshops/kirbylistrep.pdf
- **S3.** Seraphina Eun Bi Lee, *The Nielsen realization problem for high degree del Pezzo surfaces*, arXiv:2112.13500v2 (2023), definitions in §1 and Proposition 3.1. https://arxiv.org/abs/2112.13500v2
- **S4.** David Baraglia, *On the mapping class groups of simply connected smooth 4-manifolds*, Algebraic & Geometric Topology 26 (2026), 1635–1653; manuscript arXiv:2310.18819v1, Theorems 1.4 and 1.6. https://arxiv.org/abs/2310.18819 ; https://doi.org/10.2140/agt.2026.26.1635
- **S5.** Seraphina Eun Bi Lee, Tudur Lewis and Sidhanth Raman, *Cyclic Nielsen realization for del Pezzo surfaces*, arXiv:2504.17235v1 (2025), §1. https://arxiv.org/abs/2504.17235v1
- **S6.** Ethan Pesikoff, *Homological Nielsen realization for the manifolds #n CP2*, arXiv:2605.27537v1 (26 May 2026), introduction and Theorem 1.1. https://arxiv.org/abs/2605.27537v1
- **S7.** Yujie Lin and Yi Sha, *On the Homotopy Coherent Nielsen Realization Problem for K3-Type 4-Manifolds*, arXiv:2606.24482v2 (26 August 2026), Definition 1.3, Theorems 1.4 and 1.6, Corollary 1.7. https://arxiv.org/abs/2606.24482v2
- **S8.** Steven P. Kerckhoff, *The Nielsen realization problem*, Annals of Mathematics 117 (1983), 235–265, Theorem 5 and introductory conventions for the extended group. https://annals.math.princeton.edu/1983/117-2/p02 ; https://people.math.harvard.edu/~ctm/home/text/others/kerckhoff/nielsen/nielsen.pdf
- **S9.** Sören Illman, *Smooth equivariant triangulations of G-manifolds for G a finite group*, Mathematische Annalen 233 (1978), 199–220. https://eudml.org/doc/163108 ; https://doi.org/10.1007/BF01405351
