# 2912 / Kirby 4.36: obstruction audit and stopped proof routes

**Outcome: unresolved.** This attempt gives no proof or counterexample to Kirby 4.36. The deductions below are standard duality and group-cohomology reductions, not a claimed new theorem. Their purpose is to locate the exact remaining obstacle and prevent false positive examples.

## 1. Exact question

Does the full homotopy 2-type determine the homotopy type of a 2-knot complement? Here the data are

\[
(\pi_1X,\pi_2X,k_X),\qquad k_X\in H^3(\pi_1X;\pi_2X),
\]

including the group action and compatibility of the first k-invariant. The question on pp.219–220 of the [2026 Kirby survey](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf) is about **actual complements of embedded 2-spheres in S4**. It does not include a chosen meridian, peripheral map, or boundary identification in the invariant. Passing to a compact exterior does not change the homotopy type.

Lomonaco's [1981 paper](https://userpages.cs.umbc.edu/lomonaco/5knots/Lomonaco-Pacific-Journal-Math.pdf), Section X, Theorems 10.1–10.4, gives the known completeness theorem when both universal covers have zero third homology. Its formulation includes smooth or locally flat PL exteriors. The same section explains the obstruction from a finite amalgam splitting relative to the meridian. The known quasi-aspherical subclass includes spun, twist-spun, fibered and finitely-ended knots.

The word “unmarked” here refers only to the invariant and conclusion as stated in the source. It is not an assertion that meridional data are irrelevant to the proof.

## 2. Route 1: the remaining universal-cover homology

Let \(X\) be an oriented compact 2-knot exterior and let \(G=\pi_1X\). A positive meridian \(\mu\) has infinite order because its image generates \(H_1X\cong\mathbb Z\). Thus the boundary homomorphism identifies
\(\pi_1(\partial X)\cong\mathbb Z\) with \(H=\langle\mu\rangle\le G\).
Put \(R=\mathbb Z[G]\).

For clarity, equivariant cohomology below is a right R-module, and an overline converts it to a left module through the involution \(g\mapsto g^{-1}\). Equivariant Poincaré–Lefschetz duality gives

\[
H_3(\widetilde X;\mathbb Z)
\cong\overline{H^1(X,\partial X;R)}.
\tag{1}
\]

The zero-th cohomology groups of X and its boundary with these coefficients vanish: an element of R fixed by the infinite cyclic subgroup H would have infinite support unless it were zero. The same holds for G. The pair exact sequence therefore identifies

\[
H^1(X,\partial X;R)
\cong
\ker\bigl(H^1(X;R)\longrightarrow H^1(\partial X;R)\bigr).
\]

Degree-one cohomology with a local system depends only on the fundamental group and its coefficient action. Accordingly

\[
\boxed{\quad
H_3(\widetilde X;\mathbb Z)
\cong
\overline{\ker\left(H^1(G;R)\xrightarrow{\mathrm{res}}H^1(H;R)\right)}.
\quad}
\tag{2}
\]

This is a statement about the group **together with its meridional inclusion**. It does not prove that the unmarked 2-type determines this kernel. Nor does an isomorphism between the kernels alone produce a homotopy equivalence.

If a map of exteriors induces isomorphisms on \(\pi_1\) and \(\pi_2\), its lifted map already induces homology isomorphisms in degrees zero, one and two. Knot exteriors have no universal-cover homology above degree three. Hence the remaining homology requirement is that the map on \(H_3\) be an isomorphism. A homology equivalence between the simply connected universal covers is a homotopy equivalence. The quasi-aspherical theorem removes this last requirement by making both groups zero; it cannot be applied when one of them is nonzero.

### A sufficient realization statement, not a solution

Suppose a map of oriented pairs

\[
f:(X,\partial X)\longrightarrow(Y,\partial Y)
\]

has relative degree one and induces isomorphisms on \(\pi_1\) and \(\pi_2\). Then f is a homotopy equivalence.

To prove this, its boundary restriction has degree one. Since both boundaries are \(S^2\times S^1\), the induced integers on \(H^1\) and \(H^2\) have product one, so the boundary map induces an isomorphism on \(\pi_1\). Formula (2), naturality of restriction, and the isomorphisms on group and peripheral subgroup imply that
\(f^*:H^1(Y,\partial Y;R)\to H^1(X,\partial X;R)\)
is an isomorphism, with coefficients transported by \(f_*\).
Naturality of cap product and the degree-one identity give

\[
f_*\bigl([X,\partial X]\cap f^*a\bigr)
=[Y,\partial Y]\cap a.
\]

Using (1), this proves the isomorphism on universal-cover third homology. The preceding homology/Whitehead argument finishes the proof.

**Exact gap.** A bare 2-type isomorphism has not been shown to produce a degree-one map of pairs, a compatible boundary-sphere class, or even the required meridional compatibility. Adding any of these as an unstated hypothesis would replace the original question with a stronger-input problem. This route stops at that realization gap.

## 3. Route 2: a concrete infinite-ended group-pair calculation

The purpose of this calculation is to exhibit the missing third-homology module in a controlled algebraic setting. It does **not** give two knot exteriors with the same 2-type.

Consider

\[
G=\langle a,b,t\mid a^3=b^7=1,\;aba^{-1}=b^2,\;tat^{-1}=a^2\rangle.
\tag{3}
\]

Hillman's [*Four-Manifolds, Geometries and Knots*](https://arxiv.org/abs/math/0212142), Section 14.6, gives this as an example of an infinite-ended 2-knot group. Set

\[
A=\langle a,b\rangle\cong C_7\rtimes C_3,
\quad C=\langle a\rangle\cong C_3,
\quad B=\langle a,t\rangle\cong C_3\rtimes_{-1}\mathbb Z.
\]

Then (3) is the amalgam \(A*_C B\). We calculate for the explicitly specified group pair \((G,\langle t\rangle)\). A use of this calculation for a particular exterior must separately verify that t is its meridian. The abstract presentation and weight-one property alone do not supply that geometric identification.

Let \(R=\mathbb Z[G]\), and write \(R^F\) for invariants under left multiplication by a subgroup F. The group-cohomology Mayer–Vietoris sequence gives

\[
0\longrightarrow R^A\longrightarrow R^C
\longrightarrow H^1(G;R)
\longrightarrow H^1(B;R)\longrightarrow0.
\tag{4}
\]

Indeed \(R^B=R^G=0\), because B is infinite, and \(H^1(A;R)=H^1(C;R)=0\): restricting R to either finite group gives a direct sum of regular modules, whose positive cohomology vanishes.

Restriction \(H^1(B;R)\to H^1(\langle t\rangle;R)\) is injective. To see this, the subgroup \(\langle t\rangle\) has index three in B. Restriction followed by corestriction is multiplication by three. Also \(H^1(B;R)\) is torsion-free as an abelian group: use the normal finite subgroup C and the quotient \(B/C\cong\mathbb Z\). The regular-module vanishing for C identifies this group with
\(H^1(\mathbb Z;R^C)\); decomposing R over left B-orbits makes this a direct sum of copies of \(\mathbb Z\).

It follows from (4) that

\[
\ker\left(H^1(G;R)\to H^1(\langle t\rangle;R)\right)
\cong R^C/R^A.
\tag{5}
\]

This quotient is nonzero and is free as an abelian group. On each right A-coset in G, the C-invariant norm vectors give seven generators, while the A-invariant norm is their sum. Thus each such block is

\[
\mathbb Z^7/\langle(1,1,1,1,1,1,1)\rangle\cong\mathbb Z^6.
\tag{6}
\]

The identity A-coset block is a right permutation module on \(C\backslash A\). Inversion identifies its conjugate left module with the permutation module on \(A/C\); this accounts for the involution convention in (1). After quotienting, its diagonal invariant vector is zero. With cosets represented by \(b^jC\), j modulo 7, the generators act by \(a:j\mapsto2j\) and \(b:j\mapsto j+1\). The checker verifies the order 21 affine group, the seven cosets, their actions, the integral quotient basis and the defining relations.

If X is an actual exterior with group-pair identification \((\pi_1X,\langle\mu\rangle)=(G,\langle t\rangle)\), equations (2) and (5) give its third-cover-homology module, with the stated involution convention. This only describes a possible/known non-quasi-aspherical side of a search. No second exterior, no compatible 2-type isomorphism, and no differing homotopy types were constructed.

**Exact gap.** To refute Kirby 4.36 one needs two actual 2-knot complements with an isomorphism of the complete 2-type and an obstruction to homotopy equivalence. Varying an amalgam presentation, changing a meridian, or writing a different CW complex does not establish those simultaneous geometric requirements. This route stops before that realization and comparison step.

## 4. Current-literature safeguards

- The August 2026 paper [Jabłonowski, *Fundamental Quandles Do Not Determine the First Postnikov Invariant of 2-Knots*](https://arxiv.org/abs/2608.03818), Theorem 4.6, explicitly has inequivalent first k-invariants under every compatible group/module isomorphism. Its examples therefore have **different** homotopy 2-types. They do not refute the present question.
- [Conway–Kasprowski, *4-manifolds with a given boundary*](https://arxiv.org/abs/2510.18836), Theorems 1.1, 1.3 and 2.8, impose surjectivity of boundary \(\pi_1\) onto the manifold group. For a 2-knot exterior, the boundary image is its cyclic meridional subgroup, so that assumption covers only the cyclic group case. It does not solve the remaining noncyclic case.
- The converse “infinitely many ends implies non-quasi-aspherical” is false; González-Acuña–Montesinos's 1983 paper is specifically titled *Quasiaspherical knots with infinitely many ends*. The correct classical criterion retains the meridional finite splitting, as in Lomonaco's Theorem 10.3.
- Neither a difference of k-invariants nor a difference of peripheral markings on the same homotopy type is a same-2-type counterexample. Neither arbitrary 3-complexes nor arbitrary 4-manifolds meet the realization requirement.

## 5. Disposition

Two substantive routes were examined. The first yields a standard sufficient pair-map criterion but cannot construct the required map from unmarked 2-type data. The second computes an explicit nonzero obstruction module but cannot supply two geometrically realized exteriors with matching full 2-types. No new mechanism for closing either gap was found. The appropriate status is **unsolved / stalled**, with two attempts used out of five, rather than an invented resolution.

The exact checker is a finite algebra sanity check for Section 3 only. It cannot prove knot realization, completeness of the 2-type, or a counterexample. The statements in this note require separate adversarial review before any draft PR. Historical novelty is not claimed.
