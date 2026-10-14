# A genuine relative chamber and its adjoint homological maps

14 October 2026. PASS2, Roberts Problem 1.7 / 10400007. This is a bounded construction, not a full ambient knot invariant. PASS1 is preserved.

## Outcome

The full-configuration Euler obstruction can be evaded by a precisely specified relative group. A separated two-puncture chamber supplies an actual degree-one local-system factor, together with an ordinary-homology insertion and an adjoint Borel–Moore restriction/contraction. The construction has correct support and variance. It does not yet implement the nontrivial plat crossing or remove the chosen chamber, so it is not a new intrinsic Jones construction.

## 1. Spaces, coefficients, and the relative pair

In an open disc containing \(2n+2\) punctures choose disjoint open subdiscs \(A,B\), with exactly \(2n\) old punctures in \(A\) and two new punctures in \(B\). Write

\[
X=\operatorname{UConf}_{n+1}(D\setminus P),\quad
M=\operatorname{UConf}_{n}(A\setminus P_A),\quad
N=B\setminus\{p_+,p_-\}.
\]

The configurations with exactly \(n\) points in \(A\) and one in \(B\) form an open subset

\[
Y=M\times N\overset j\hookrightarrow X.
\]

The product decomposition is canonical after choosing the regions: their locations distinguish the two groups of unordered particles. Put \(Z=X\setminus Y\), which is closed. Use the rank-one standard character local system over \(k=\mathbb Q(Q,D)\), with puncture monodromy \(Q\) and exchange monodromy \(D\). Its restriction splits as

\[
j^*\mathcal L=\mathcal L_M\boxtimes\mathcal L_N.
\]

Indeed particles in the disjoint discs cannot exchange, and a loop in either subdisc has zero winding around punctures in the other. The local factor \(\mathcal L_N\) has monodromy \(Q\) around each puncture. All statements also hold over \(\mathbb Q(Q)\) after \(D=-Q^{-1}\), since \(Q-1\) remains invertible.

For the closed subset \(Z\), the Borel–Moore localization sequence gives

\[
H_*^{\rm BM}(X,Z;\mathcal L)\cong H_*^{\rm BM}(Y;j^*\mathcal L).
\]

Here relative Borel–Moore homology uses the cone/quotient of the proper closed-subset inclusion. The identification with the open complement is the standard localization property; it is not a claim that arbitrary open inclusions admit covariant Borel–Moore pushforward.

## 2. The local two-puncture computation

The space \(N\) retracts onto a wedge of two circles \(a,b\). Its twisted cellular complex is

\[
0\longrightarrow k^2\xrightarrow{(Q-1,\,Q-1)}k\longrightarrow0.
\]

Since \(Q-1\) is invertible,

\[
H_1(N;\mathcal L_N)=k\langle e_a-e_b\rangle,
\qquad H_i(N;\mathcal L_N)=0\ (i\ne1).
\]

The same assertion holds with dual coefficients, replacing \(Q\) by \(Q^{-1}\). A compact representative of the generator is the based figure-eight path \(ab^{-1}\), equipped with its parallel coefficient: its total monodromy is one and its chain is \(e_a-e_b\).

The oriented real two-manifold \(N\) has finite type. Poincaré duality therefore gives \(H_1^{\rm BM}(N;\mathcal L_N)=k\), with no other Borel–Moore groups. Fix the compact dual-coefficient generator \(\gamma\in H_1(N;\mathcal L_N^\vee)\) specified above. The perfect ordinary/Borel–Moore intersection pairing determines a unique \(\eta\in H_1^{\rm BM}(N;\mathcal L_N)\) with

\[
\langle\eta,\gamma\rangle_N=1.
\]

This normalization is over the field \(k\). Over \(\mathbb Z[Q^{\pm1},D^{\pm1}]\), the local \(H_0\) contains the nonzero quotient by \(Q-1\); one must not claim the same concentrated one-dimensional calculation integrally.

## 3. Actual maps and a worked relation

Künneth and localization give a genuine isomorphism

\[
H_{n+1}^{\rm BM}(X,Z;\mathcal L)
\cong H_n^{\rm BM}(M;\mathcal L_M)\otimes k\eta.
\]

Thus define

\[
p_n:H_{n+1}^{\rm BM}(X;\mathcal L)
\xrightarrow{\mathrm{restriction}}H_{n+1}^{\rm BM}(Y;\mathcal L_M\boxtimes\mathcal L_N)
\xrightarrow{\eta\mapsto1}H_n^{\rm BM}(M;\mathcal L_M).
\]

In the opposite variance define the ordinary-homology insertion

\[
s_n:H_n(M;\mathcal L_M^\vee)\longrightarrow H_{n+1}(X;\mathcal L^\vee),
\qquad s_n(b)=(-1)^n j_*(b\times\gamma).
\]

The sign uses the usual product orientation: the intersection of \(\alpha\times\eta\) with \(b\times\gamma\) has the factor \((-1)^n\), from interchanging the one-dimensional local tangent block with the old \(n\)-dimensional block. Equivalently the sign convention can be fixed by requiring the adjunction below.

There is no nonproper pushforward hidden here. Ordinary singular cycles are finite chains with compact images, so \(j_*\) is available for the ordinary cycle. On the Borel–Moore side we only **restrict** to the open set and contract its one-dimensional local factor. These maps obey

\[
\boxed{\langle p_n(a),b\rangle_M=\langle a,s_n(b)\rangle_X.}
\]

To prove this, restrict the intersection to \(Y\), which contains the support of \(j_*(b\times\gamma)\). Under Künneth write the restriction as \(\alpha\otimes\eta\). The product-intersection formula gives \((-1)^n\langle\alpha,b\rangle_M\langle\eta,\gamma\rangle_N\); the explicit sign in \(s_n\) cancels it. Since \(\langle\eta,\gamma\rangle_N=1\), this is exactly the displayed identity.

Within the relative group the identification is also explicit:

\[
\alpha\longmapsto\alpha\times\eta,
\qquad
\alpha\times\eta\longmapsto\alpha.
\]

These are inverse maps for that relative group. They are not inverse maps between the full groups of \(M\) and \(X\), and no such claim is needed or valid here. In particular, this construction genuinely avoids the PASS1 Euler obstruction by changing the retained object.

## 4. Why this is not yet plat stabilization or ambient descent

The extra-particle chamber is an isolated factor. The standard nontrivial plat stabilization uses the crossing \(\sigma_{2n}\), mixing an old puncture with a new puncture. It does not preserve the separated-region product. One may compose \(s_n\) with the braid-induced isomorphism and compose \(p_n\) with its adjoint inverse, but that formal composition does not establish the required transport of both distinguished classes.

Concretely, the outstanding statement would identify the restriction/contraction of the crossed fork class with the old fork class, with exactly the needed scalar, and then prove compatibility when the local ball moves, when presentations change elsewhere, and when two move sequences describe the same ambient geometry. Independence of the chosen subdiscs and of generator lifts is also missing. A scalar equality on one torus class would not by itself prove all these identities.

Bigelow's existing stabilization proof already compares the isolated added edge/circle factor and then uses its skein and plat-move relations to handle the crossing. The local product calculation here is not advertised as superseding that theorem or Lawrence's tangle functor. [Bigelow, Lemma 5.6](https://web.math.ucsb.edu/~bigelow/publications/06.pdf)

The exact advance of this bounded attempt is narrower: it supplies the relative pair, coefficient splitting, dual cycle, support-correct maps, and an adjunction that a future geometric descent could use. No knot-pair invariant is extracted from it in this pass. No obstruction to other relative/correspondence constructions follows.
