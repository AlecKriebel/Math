# Primary formulation and separated interpretations

## 1. Conventions actually printed in the source

Ayoub's contribution to OWR 31/2009 occupies printed pages 1760–1762. Its opening sets characteristic zero and rational coefficients. On smooth schemes the object is the sheafification

\[
F_X^p=a_{\mathrm{Nis}}[U\longmapsto CH^p(U\times X)\otimes\mathbf Q].
\]

The typography is a tilde over `CH`, not a subscript `g`. The étale version agrees in the stated rational homotopy-invariant setting. The functor `Alb` is the left adjoint to the inclusion of 1-motivic sheaves. The report calls its value on a smooth scheme the Albanese **scheme**, and keeps the 0-motivic subcategory. Example 4 identifies \(\pi_0F_X^p\) with the rational Néron–Severi sheaf. Conjecture 5 then prints the full \(\operatorname{Alb}(F_X^p)(\mathbf C)\) comparison, without a connected-component superscript. [OWR]

The referenced detailed paper separately defines \(F^0=\ker(F\to\pi_0F)\), permits a semi-abelian group scheme with a finitely generated component group, and constructs Alb in that category. Thus neither the rational coefficients nor the Albanese convention silently removes a nonzero rational lattice. [ABV, §§1.3.1–1.3.2, Proposition 1.3.11]

Walker defines, for a quasi-projective complex variety and a cycle dimension \(r\ge0\),

\[
J_r^{\mathrm{mor}}(X)=\operatorname{Ext}^1_{\mathrm{IMHS}}
 (\mathbf Z(0),L_rH_{2r+1}(X)).
\]

Its map starts on algebraically trivial cycles. For projective varieties it factors through rational equivalence and is surjective. [W, Definition 5.2, Theorem 5.7] For a smooth equidimensional \(X\) of dimension \(d\), the matching index is \(r=d-p\).

## 2. An elementary obstruction to the literal full-object formula

**Proposition.** With the report's full Albanese functor and rational coefficients, its printed formula fails for \(X=\mathbf P^1_{\mathbf C}\), \(p=1\).

**Proof.** For every smooth complex scheme \(U\), the projective bundle formula gives

\[
CH^1(U\times\mathbf P^1)_{\mathbf Q}
=\operatorname{Pic}(U)_{\mathbf Q}\oplus
  H^0(U,\underline{\mathbf Q})[\mathcal O(1)].
\]

The presheaf \(U\mapsto\operatorname{Pic}(U)\) sheafifies to zero in the Zariski topology: each line bundle is trivial on an open cover. Therefore it also sheafifies to zero in the Nisnevich and étale topologies. The second summand already is the constant sheaf with its degree-transfer structure. Hence

\[
F_{\mathbf P^1}^1\simeq\underline{\mathbf Q}.
\]

The constant rational sheaf is 0-motivic, hence 1-motivic. A reflector onto a full subcategory is the identity on objects of that subcategory. Consequently

\[
\operatorname{Alb}(F_{\mathbf P^1}^1)(\mathbf C)=\mathbf Q.
\]

The corresponding cycle dimension is zero. The zero-cycle comparison gives \(L_0H_1(\mathbf P^1)=H_1(\mathbf P^1,\mathbf Z)=0\), so \(J_0^{\mathrm{mor}}(\mathbf P^1)=0\). Rationalizing the right-hand side leaves zero. Thus even an abstract group isomorphism is impossible. ∎

This defect is in the printed primary wording as well as in the catalogue. It is not a finding about an intended connected version. It also does not depend on an omitted smoothness, properness, or quasi-projectivity hypothesis: the example has all of them.

**General component calculation.** For any \(F\) in the rational homotopy-invariant category,

\[
\pi_0\operatorname{Alb}(F)\simeq\pi_0F.
\]

Indeed, for every 0-motivic object \(D\), the successive adjunctions identify both objects' Hom functors with \(\operatorname{Hom}(F,D)\). Yoneda proves the identity. Applied to the Chow sheaf, this retains \(NS^p(X)_{\mathbf Q}\); passing to Alb is not passing to algebraically trivial cycles.

## 3. The coefficient issue is independent

Even after taking a connected part, comparing a rational sheaf's points with an integral Jacobian's points is not the same question. For an elliptic curve \(E/\mathbf C\), \(E(\mathbf C)\) has nonzero \(n\)-torsion for all \(n>1\), whereas \(E(\mathbf C)\otimes\mathbf Q\) is torsion-free. They cannot be isomorphic as groups. A rational comparison must rationalize both sides; an integral comparison must be formulated in the integral étale 1-motivic category over \(\mathbf C\).

## 4. The explicit repaired question investigated here

For a smooth connected projective complex variety \(X\), set

\[
A_X^p=\operatorname{Alb}(F_X^p)^0,
\qquad
W_X^p=J_{d-p}^{\mathrm{mor}}(X)\otimes\mathbf Q.
\]

Does there exist a canonical isomorphism

\[
A_X^p(\mathbf C)\simeq W_X^p
\]

compatible with the two maps from \(CH^p(X)_{\mathrm{alg}}\otimes\mathbf Q\) and with correspondences?

This is a deliberately stated candidate repair, not an assertion that it uniquely captures the author's intention. The comparison is not proved in arbitrary codimension. Extensions to singular or nonproper varieties require additional choices and arguments. The original sheaf example is introduced for smooth \(X\), while the short conjecture says algebraic variety; that broader scope is not repaired by guessing an operational Chow group or a compactly supported motive.

The later finite-dimensional Walker intermediate Jacobian is a different object from the full morphic target. `MATHEMATICS.md`, Approach 5, quantifies that distinction.


## 5. The two connected constructions do agree here, by a separate proof

**Proposition.** Over \(\mathbf C\), with rational coefficients and the Chow sheaf just defined, the canonical map

\[
\operatorname{Alb}((F_X^p)^0)\longrightarrow
\operatorname{Alb}(F_X^p)^0
\]

is an isomorphism. This is an equality of 1-motivic sheaves, not merely of their groups of complex points.

**Proof.** Put \(D=\underline{NS^p(X)_{\mathbf Q}}\). The component calculation and [ABV, Theorem 3.1.4] give an exact sequence

\[
0\to(F_X^p)^0\to F_X^p\xrightarrow{q}D\to0.
\]

This sequence splits, although not canonically. Choose a rational vector-space basis of \(NS^p(X)_{\mathbf Q}\) and lift every basis vector to \(CH^p(X)_{\mathbf Q}\). Each lift defines a morphism of sheaves with transfers \(\underline{\mathbf Q}\to F_X^p\), since \(\underline{\mathbf Q}=\mathbf Q_{\mathrm{tr}}(\operatorname{Spec}\mathbf C)\) and the transfers Yoneda lemma identifies these morphisms with \(F_X^p(\mathbf C)=CH^p(X)_{\mathbf Q}\). Taking their direct sum gives a section of \(q\). No finite-generation hypothesis on \(NS^p\) is needed.

Thus \(F_X^p\simeq(F_X^p)^0\oplus D\). Under this splitting, applying \(\pi_0\) and using that \(\pi_0(q)\) is an isomorphism proves \(\pi_0((F_X^p)^0)=0\). Applying the additive reflector Alb gives

\[
\operatorname{Alb}(F_X^p)\simeq
\operatorname{Alb}((F_X^p)^0)\oplus D.
\]

The first summand has zero component sheaf, by \(\pi_0\operatorname{Alb}=\pi_0\). Hence it is the kernel of the canonical component map on \(\operatorname{Alb}(F_X^p)\). The resulting isomorphism is induced by the original inclusion \((F_X^p)^0\hookrightarrow F_X^p\); it is therefore canonical despite the auxiliary choice of splitting. ∎

This argument uses an algebraically closed base and rational component coefficients. It is not a license to commute a general left adjoint with kernels over arbitrary bases or with integral coefficients. It removes one ambiguity in the candidate repair; it does not compare that repaired object with Walker's target.
