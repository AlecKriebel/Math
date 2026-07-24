# Verification record for the quartic working lemmas

**Verification timestamp:** 2026-07-24T23:43:08Z.

These results are not peer reviewed.  Exact computer checks are evidence
about the algebra encoded in the scripts; they are not evidence that every
geometric hypothesis has been encoded, and they are not a substitute for
peer review.

## Exact checks

The following commands pass:

```text
/usr/bin/python3 verify_quartic_constraints_sympy.py
gp -q verify_quartic_constraints_pari.gp
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

## Scope

None of these checks excludes every total-degree-four Keller
counterexample.  The certified universal lower bound therefore remains
total degree \(4\), from Vistoli's published degree-three theorem.
