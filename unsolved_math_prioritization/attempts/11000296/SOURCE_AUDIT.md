# Exact target and proof-dependency audit

## 1. Source and edition correspondence

The queue pins Farb's author-hosted *Problems on Mapping Class Groups and Related Topics*, Chapter 20 by Bridson and Vogtmann. The surrounding text on printed page 329 identifies the second Morita cycle in `H_8(Out(F_6);Q)` and the natural map from `Out(F_n)` to `GL(n,Z)`. Question 5.4 is on printed page 330, PDF page 337. Its subscript 8 is visible on the rendered primary page; neither an isolated OCR `H8` nor a cohomology-section heading changes its homological meaning.

KMP's introduction cites the question under a different edition's numbering, Question 32. We match the mathematical class, degree, rank, coefficients and map rather than identifying question numbers across editions. The queue's source locator remains Question 5.4. The dual cohomology question in another chapter is related, but is not bundled into this record.

KMP is arXiv v1, submitted 11 September 2026, ten pages; the downloaded PDF's internal date is 14 September. Its author page calls it a preprint on the audit date, 1 October 2026. KMP's introduction says “Theorem 5.1” where Section 5 has Definition 5.1. This internal label does not affect the theorem's statement or proof.

## 2. The specific Morita class, including its Aut lift

Conant–Hatcher–Kassabov–Vogtmann (CHKV), published Section 5.1, Proposition 5.4 on page 781 and Remark 9.5 on pages 798–799, give the necessary identification. The author's earlier PDF instead numbers these Section 4.1, Proposition 4.4 and Remark 8.5; KMP uses that earlier numbering. Both complete editions were checked.

CHKV constructs the original Morita class by assembling two top classes of rank-one graph groups. Inserting a based tree piece produces a lift to `Aut`, whose projection to `Out` is the original class. Its abelian subgroup consists of left multiplication of each of four moving basis elements by one fixed generator and right multiplication by a second fixed generator. The remark identifies this assembly with the original Morita class. Generator and orientation choices can multiply the displayed class by a nonzero rational scalar; this cannot change nonvanishing.

Using KMP's indexing, let `F_6=<x_1,...,x_6>`. The eight commuting automorphisms are

`lambda_i: x_i -> x_5 x_i`, `rho_i: x_i -> x_i x_6`, for `1<=i<=4`, fixing all other generators.

For different moving indices the operations commute because both fixed multipliers stay fixed. At the same index, left and right multiplication commute. Thus they define `phi: Z^8 -> Aut(F_6)`, and `phi_*[Z^8]` is the CHKV lift of `mu_2` up to the harmless choice of generator just noted.

Inner automorphisms act trivially on abelianization. If `q:Aut(F_6)->Out(F_6)` and `ab=p o q`, then

`ab_* phi_*[Z^8] = p_* q_* phi_*[Z^8]`.

Nonvanishing of the left side is consequently the exact source answer, not merely nonvanishing of a potentially different Aut class.

## 3. A completely specified block convention

With column vectors and ordered basis `(x_5,x_6,x_1,x_2,x_3,x_4)`, the abelianized subgroup is

`U = { [[I_2,B],[0,I_4]] : B in Mat_(2,4)(Z) }`.

The eight generators run through every entry of B, so `Z^8 -> U` is an isomorphism. It fixes the rank-two summand and the rank-four quotient pointwise. This is the full unipotent radical of the standard parabolic `P_(2,4)`.

KMP Section 5.1 displays `P_(4,2)` for the same automorphisms. Rather than assume a row/column convention, our check uses the explicit `P_(2,4)` matrices above and applies KMP Proposition 4.3 with `a=2,b=4`. That proposition treats both orders and has exactly the same conclusion. No comparison between a representation and its contragredient is needed. This block-order issue introduces no missing hypothesis in the actual specialization.

## 4. The nonzero pairing in KMP's proof

All groups here have rational coefficients. Write `nu_n=n(n-1)/2`, so `nu_2=1`, `nu_4=6`, `nu_6=15`. For even n the rational dualizing module of `GL_n(Z)` is `St_n tensor det`, not untwisted `St_n`. Let `t_n` be the Bieri–Eckmann dual of `1 in H^0(GL_n(Z);Q)`.

The Ash–Miller–Patzt (AMP) Hopf algebra with determinant-twisted Steinberg coefficients contains `t_2,t_4`, with bidegrees `(2,1)` and `(4,6)`. Their product lies in `(6,7)`, and its dual has cohomological degree `15-7=8`, with **trivial** coefficients. The twist occurs in the dualizing module and is not an extra twist on the target question.

AMP Theorem A, Lemma 2.4 and Proposition 4.2 give the product/coproduct compatibility, sign convention and primitiveness. Primitiveness also follows directly from the degree bound: for positive a,b, `nu_a+nu_b=nu_(a+b)-ab < nu_(a+b)`, so the top-degree class has no reduced coproduct component. For the product, the component in ranks `(2,4)` is exactly

`Delta_(2,4)(t_2 t_4)=t_2 tensor t_4`.

The reverse tensor occupies different ranks `(4,2)`, and the endpoint terms have rank zero in one factor. Thus there is no cancellation. The total sign exponent is `(nu_2+2)(nu_4+4)=3*10`, even; nonvanishing does not hinge on it because the rank components are different.

KMP Section 3 proves that this coproduct is Bieri–Eckmann dual to restriction to `P_(2,4)` followed by integration over `U`. Its ingredients are the apartment projection/Reeder restriction map (Theorem 3.3 and Lemma 3.4), the parabolic extension and Shapiro map, and Theorem 3.5(i). The parabolic orientation character from U is `det(A)^4 det(C)^(-2)=1`, since A,C are integral invertible matrices. Both Levi factors are even-rank, as required by the untwisted-cohomology case.

KMP Lemma 2.4 identifies top-degree restriction to U with this fiber integration, up to sign; Lemma 4.4 dualizes it. Thus the class `BE^-1(t_2 t_4)` evaluates nontrivially (with normalization, up to sign 1) on the image of `[U] in H_8(GL_6(Z);Q)`. Proposition 4.3(i) states the resulting injectivity. Its additional congruence assumption applies only when a=b, so it imposes no restriction on `(2,4)`.

This checks the complete specialization of KMP's argument. The general Bieri–Eckmann, Borel–Serre and Reeder theorems are credited inputs, not newly proved here. KMP's ten-page argument was read in full, and AMP's relevant product, coproduct, compatibility and primitive-class arguments were checked in its full primary PDF. This packet does not purport to independently reprove every classical duality theorem or the complete homology of GL_6.

## 5. Boundaries and controls

- KMP Theorem A has `k>=2` for nonzero images in GL. For k=1, a=b=2 and the repeated primitive class has odd total degree; the cancellation is consistent with the stated zero target homology. We do not extend the image conclusion to k=1.
- Stable vanishing, or vanishing after stabilization, concerns another map/rank and gives no obstruction to this unstable degree-eight class.
- This is rational group homology; no integral primitivity, torsion conclusion or mapping-class-group image is asserted.
- The elementary checker verifies commuting free-group automorphisms, independent matrix coordinates, parameter specialization and graded signs. It is not a computational certification of duality or the cited homological nonvanishing theorem.
- The unsuccessful first download labeled as a 2004 Conant–Vogtmann paper was identified from its first page as an unrelated Leininger article and excluded. No claim here uses it. CHKV and KMP provide the exact class identification needed.
