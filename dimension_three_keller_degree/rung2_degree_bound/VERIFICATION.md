# Verification record for the quartic working lemmas

**Verification timestamps:** 2026-07-24T23:43:08Z and
2026-07-25T00:10:26Z.

These results are not peer reviewed.  Exact computer checks are evidence
about the algebra encoded in the scripts; they are not evidence that every
geometric hypothesis has been encoded, and they are not a substitute for
peer review.

The derivations, adversarial audits, scripts, and exposition were produced
with AI assistance under human direction.  Every promoted algebraic identity
is retained in an exact reproducible check, but that disclosure and those
checks do not constitute independent peer review.

## Exact checks

The following commands pass:

```text
/usr/bin/python3 verify_quartic_constraints_sympy.py
gp -q verify_quartic_constraints_pari.gp
/usr/bin/python3 verify_quartic_strata_sympy.py
gp -q verify_quartic_strata_pari.gp
/usr/bin/python3 verify_conic_doubleline_sympy.py
gp -q verify_conic_doubleline_pari.gp
```

The SymPy and PARI/GP implementations independently expand:

1. all nine weighted homogeneous coefficients of
   \(\det(I+JH_2+JH_3+JH_4)-1\);
2. the degree-eight and degree-seven determinants used in the primitive
   line-type theorem;
3. the complete discrete generic-degree-three boundary table;
4. the conductor-degree and parity consequences;
5. an exact composite-pencil counterexample to the discarded primitive
   inference; and
6. the quartic shear automorphism showing that rank-one \(JH_4\) does not
   force simultaneous triangularization when \(H_2\ne0\).

They also verify the local complete-intersection branch used to disprove the
discarded claim that every finite conductor exponent is positive.

The second pair independently checks:

1. the degree-eight, degree-seven, and corrected degree-six coefficients in
   the genuine line-image \((1,4)\) theorem;
2. the full degree-six curvature term, all five ramification splitting
   representatives, and the exact degrees-eight-through-five sharpness
   construction in the ramified \((1,4)\) locus;
3. the degree-eight and degree-seven normal-minor coefficients for a
   rational-quartic leading curve;
4. the binary chain-rule factor in the line-image \((2,2)\) theorem;
5. the conic-image adjugate
   \(\operatorname{adj}(JH_4)=2Dn^T\);
6. the full conic degree-seven determinant identity and the tangent and
   square syzygies used in the conic normal form;
7. the rank-two determinant formula with arbitrary, possibly singular,
   constant part and the rank-nine degree-six systems for all three conic
   pencil Jordan types;
8. exact double-line sharpness examples;
9. a concrete gcd-one ramification triple; and
10. the constant Jacobian of the quadratic coordinate change.

## Independent mathematical audits

### Conductor equation

One derivation uses finite duality for the normalization of the Gorenstein
\((4,4)\) complete-intersection curve:
\[
\nu^*\omega_X\simeq\omega_{\bar C}(A).
\]
A separate local check writes a pulled-back dualizing frame as
\(u^{-c_p}du\).  Comparing the coefficient of \(dt\) with the order
\(4m_p\) of \(X_0^4\) gives
\[
c_p=4m_p-e_p+1
\]
at a finite target value and
\[
c_p=4m_p+e_p+1
\]
at target infinity.  The degree calculation
\(\deg A=66-2g=2(33-g)\) independently fixes the global sign.

The adversarial audit found a real error in an earlier draft: the finite
number \(4m_p-e_p+1\) can be zero.  All singular-boundary conclusions are
therefore restricted to generic degree three, where \(e_p\le2\).

### Primitive line-type theorem

The determinant extraction was checked by both exact scripts.  The
power-fibre lemma was audited separately by vertical divisor comparison in
\(\mathbb C(\mathbb P^2)\) and by the valuation obstruction to a nontrivial
power inside a relatively algebraically closed rational subfield.

The audit also found a fatal hypothesis error in an earlier draft:
line-valued image does not imply a primitive parametrization.  The exact
example
\[
(x^4,y^4,0)
\]
forces the relative-algebraic-closedness condition to appear explicitly in
the theorem.  The composite degree factorizations remain open strata.

### Rank-one quartic part

The \(H_2=0\) theorem has two independent components: the published
homogeneous dimension-three triangularization theorem applies to \(JH_3\),
and the nilpotent rank-one perturbation identities force \(JH_4\) into the
same flag.  A second audit checked the rank-two Krylov determinant
\[
\det[a,Ba,B^2a]=a_1^3p^2r
\]
and the common flags in the rank-one case.

For \(H_2\ne0\), the invariant-image-line proposition is verified directly by
the block factorization of \(JF\).  The explicit two-shear example was
checked in both systems and proves that a global simultaneous-triangularization
strategy is false.

### Quadratic-component exit and rational-curve strata

The quadratic-coordinate lemma was derived from the kernel and image of the
constant Hessian and independently audited with arbitrary constants and
linear part.  Both implementations check the triangular Jacobian, and the
degree tracking is explicit:
\[
\deg(F\circ T^{-1})\le4\cdot2=8.
\]

For the \((1,4)\) line-image theorem, one derivation used direct determinant
row replacement and a second recomputed all three coefficients from generic
symbolic matrices.  The Hilbert--Burch resolution was audited with the
arbitrary linear part left unnormalized; this caught the need to retain the
scalar \((L_0)_{3r}\) in degree six.

For the line-image and conic-image \((2,2)\) theorems, the vertical-divisor
argument and the exact matrix/syzygy calculations were performed
independently.  The double-line hypotheses are sharp only for the stated
leading determinant identities; the examples are not asserted to be Keller
maps.

The adversarial audit identified a missing logical bridge between
\(D\)-invariance and algebraicity over \(\mathbb C(p/q)\).  Both notes now
include the homogeneous first-integral lemma proving that bridge through the
constant field of \(D\) and the scaling action.  It also identified the need
to prove relative algebraic closedness separately when there is exactly one
double-line fibre; the conic-pencil determinant classification now covers
that case.  Finally, the audit observed that the first harness version checked
only the conic syzygies, not the entire degree-seven determinant coefficient.
The full generic coefficient is now encoded in both exact scripts.

A separate adversarial audit reconstructed the conic degree-six exclusion
from scratch.  It checked the complete self-adjoint Jordan classification,
the three spaces \(W=\{\operatorname{Jac}(p,q,h):h\text{ linear}\}\), and
the syzygy orientation.  Direct coefficient solving gives rank nine in the
nine entries of the residual constant matrix for each canonical pencil,
which both exact scripts retain as a regression.

The final pair checks the unique-double-line conic branch independently:

1. the two canonical pencil determinants;
2. both complete degree-seven solution families;
3. the forced singular linear part in the \(\ell=0\) branch;
4. the residual degree-six linear-part matrix;
5. all five decisive degree-five coefficients; and
6. the top-degree obstruction in the final rank-two factorization.

An adversarial audit independently reconstructed the invariant rings,
rank-twelve degree-seven operator, degree-six compatibility ideals, affine
normalizations, arbitrary-linear-part conventions, and dominance step.  It
found no algebraic correction.  The proof now explicitly records why the
affine translations preserve the leading pencil and why dominance is needed
to infer that \(\det JG\) itself is constant.

### Ramified line image and rational-quartic image

The Hilbert--Burch shift calculation, local root normalization, degree-six
signs, curvature formulas, and all five line-image splitting
representatives were derived independently and then adversarially checked.
That audit found one genuine error in the first draft: with two \(k=2\)
columns, the \(r^3\) curvature is the quadratic expression on their
**combined** \(r\)-leading syzygy, not the sum of separate expressions.  The
note now retains the cross terms through
\[
N_\gamma=\sum\gamma_iN_i,\qquad [r^3]T_6=C(N_\gamma).
\]

A separate audit checked the rational-quartic normal-minor resolution,
degree-eight and degree-seven identities, arbitrary-linear-part reduction,
and ramified sharpness example.  It found no mathematical correction; the
scope wording was tightened to a birationally parametrized plane quartic and
to the ramification divisor of the displayed basepoint-free parametrization.

## Scope

None of these checks excludes every total-degree-four Keller
counterexample.  The certified universal lower bound therefore remains
total degree \(4\), from Vistoli's published degree-three theorem.
