# Verification record for the quartic working lemmas

**Verification timestamps:** 2026-07-24T23:43:08Z,
2026-07-25T00:10:26Z, 2026-07-25T01:40:55Z, and
2026-07-25T02:04:55Z, 2026-07-25T02:48:29Z, and
2026-07-25T03:19:56Z, 2026-07-25T06:06:25Z,
2026-07-25T06:11:00Z, and 2026-07-25T06:18:12Z.

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
/usr/bin/python3 verify_rank_one_quotient_sympy.py
gp -q verify_rank_one_quotient_pari.gp
/usr/bin/python3 verify_rank_one_primitive_exit_sympy.py
gp -q verify_rank_one_primitive_exit_pari.gp
/usr/bin/python3 verify_rank_one_composite_exit_sympy.py
gp -q verify_rank_one_composite_exit_pari.gp
gp -q verify_quartic_curve_taxonomy_pari.gp
/usr/bin/python3 verify_nodal_cubic_exit_sympy.py
gp -q verify_nodal_cubic_exit_pari.gp
/usr/bin/python3 verify_scalar_aligned_nodal_sympy.py
gp -q verify_scalar_aligned_nodal_pari.gp
/usr/bin/python3 verify_line22_doubleline_sympy.py
/usr/bin/python3 verify_fixed_conic_row_sympy.py
gp -q verify_fixed_conic_row_pari.gp
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

The quotient-cubic extension treats arbitrary \(H_2\).  Its first exact pair
checks that the degree-seven coefficient is
\(\operatorname{Jac}(P,Q,h)\) and that the exceptional
\(P=L^3,\ h=L(\alpha P+\beta Q)\) form satisfies it.  The primitive-exit
pair then checks the generic degree-six identity
\[
D(K)=3x^2E_6
\]
and the corrected pure-power degree-five identity
\[
D(9x^2U-2\mu S^2-12\mu x^3\ell_0)=9x^2E_5
\]
with an arbitrary linear part.  The composite-exit pair checks the binary
degree-six syzygy and the corrected degree-five syzygy
\[
a v_1-b v_2+cU_z=0.
\]

An independent adversarial derivation reconstructed the field, divisor,
Hilbert--Burch, coordinate, plane-fibre, and Ax--Grothendieck steps.  It
caught two genuine arbitrary-linear-part omissions: the
\(-12\mu x^3\ell_0\) correction in the primitive pure-power branch and the
\((v_1,v_2)\) terms in the composite branch.  Both corrections were encoded
before promotion.  Under a primitive projected cubic pencil, the complete
rank-one-leading stratum is now excluded; for a fixed-component-free
nonprimitive pencil, only the explicit common-ramification locus remains.

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

### Curve-image taxonomy and the complete nodal row

The curve-image taxonomy was reconstructed independently from de Bondt's
minimal-pair factorization.  The audit checked the fixed polynomial gcd,
equal-degree homogeneous minimal pair, relation \(e+ab=4\), every
factorization \(b=\delta\nu\), and the composed base scheme.  It found no
missing row.  It corrected overstatements about which earlier line rows had
been excluded and identified the conic double-cover row with the
two-double-line form
\[
\operatorname{Ver}(p^2,q^2).
\]
The PARI regression checks only the displayed nodal representative,
adjugate, degree-eight tangent form, and degree-seven normal minor; the
taxonomy audit is the independent method.

For the transverse nodal cubic, the SymPy and PARI regressions expand the
entire determinant through degree five.  A separate adversarial calculation
started with a general eighteen-coefficient \(H_2\) and general nine-entry
\(L_0\), rather than substituting the claimed answer.  It independently
found ranks sixteen and nine and reproduced
\[
H_2=\frac13(uA_p+vA_q)+\frac r2D^2A,
\]
\[
\det L_0=\frac49(\alpha^3+\beta^3)(\alpha v-\beta u)^2,
\]
and the square factor in degree five.  The latter forces
\((u,v)=3\lambda(\alpha,\beta)\), hence makes the displayed determinant
zero.  This excludes the full transverse nodal branch; the cuspidal and
scalar-aligned branches are not part of that calculation.

For the scalar-aligned branch, the new SymPy regression starts with an
arbitrary twelve-coefficient binary cubic \(V\), arbitrary
eighteen-coefficient \(H_2\), and the unspecialized marked-point parameter
\(h=p+kq\).  It checks the \(15\times30\) degree-seven system and four
polynomial left-null certificates.  The PARI regression independently
re-expands the determinant and those four coefficient combinations.

The adversarial audit began again from Jacobian columns and obtained
\[
E_7=\operatorname{tr}(\operatorname{adj}(JH_4)JH_2)
   +\operatorname{tr}(\operatorname{adj}(JH_3)JH_4).
\]
It confirmed that no polarization term was omitted, that the four
certificates are division-free at every specialization of \(k\), and that
the Hilbert--Burch shifts admit no syzygy below coefficient degree two.
The compatibility equations force \(\alpha=\beta=0\); the same
no-low-syzygy statement then forces \(\partial_rH_2=0\).  The audit
independently checked the omitted \(h=q\) chart and the final
degree-at-most-four plane Keller block plus shear.  No scope correction was
needed.  Combining this with the transverse calculation excludes the
entire nodal row.  The two cuspidal placements are treated separately
below and are now both closed.

### Binary fixed-divisor conic

The SymPy regression begins with
\[
H_4=h(p,q)(p^2,pq,q^2)^T
\]
and a completely general cubic, quadratic, and linear part.  It checks the
top normal and both degree-six branch polynomials, then retains the decisive
raw lower-identity solve for every residual tangent orbit: split scalar,
split opposite, split zero, double scalar, double semisimple, double
nilpotent (including its zero branch parameter), and double zero.

The PARI/GP regression independently expands the top identities and both
scalar-tangent degree-two-square endgames.  A separate adversarial audit
reconstructed all seven branches from the raw Jacobian columns.  It checked
the constant degree-five obstructions, the specialization-safe square
certificates, the semisimple system's constant \(9\times9\) minor \(32768\),
and the nilpotent branch in which two columns of \(L_0\) become
proportional.  The audit's crucial correction was one of scope, not algebra:
the proof excludes precisely the binary condition
\(\iota_kB_h=0\), rather than every quadratic fixed divisor.  The companion
nonbinary theorem below subsequently closes the other five parabolic normal
forms.

### Unique-double-line line charts

The focused SymPy regression checks the conditional degree-seven equations
for both canonical quadratic pencils, both displayed outer double-cover
charts, and both cubic branches.  The adversarial audit confirmed every
sign, kernel, and image calculation but disproved exhaustiveness of the
simultaneous normalization.  For
\(\langle x^2,yz\rangle\), the outer critical pair and the companion cubic
carry relative-position parameters.  The note now retains the calculations
only as conditional charts and records an exact missed configuration with
vanishing degrees eight and seven.  That earlier conditional package alone
made no exclusion claim; the following scope-corrected package closes one
complete joint-moduli chart without claiming the remaining row.

### Finite-outer-critical unique-double-line chart

At 2026-07-25T06:06:25Z the scope-corrected supplied checks and independent
hostile reconstructions passed:

```text
/usr/bin/python3 verify_line_22_finite_outer_critical_sympy.py
./run_verify_line_22_finite_outer_critical_pari.sh
/usr/bin/python3 verify_line_22_fg_resonance_sympy.py
./run_verify_line_22_fg_resonance_pari.sh
/usr/bin/python3 audit_line22_fg/audit_fg_chart_exact.py
/usr/bin/python3 audit_line22_fg/audit_outer_infinity.py
./audit_line22_fg/test_supplied_python_optimized.sh
./audit_line22_fg/test_supplied_runner.sh
```

For \(p=x^2,q=yz\), the two theorem notes retain the full simultaneous
moduli
\[
H_4=((p-aq)^2,(p-bq)^2,0),\qquad
(H_3)_3=x(p-cq),\qquad a\ne b.
\]
The open raw \(E_7\) stratification, the \(c=0\) noncritical and
marked-critical branches, and both resonance divisors
\[
3ab-2ac-bc=0,\qquad 3ab-ac-2bc=0
\]
all end in a singular linear part.  The finite-chart raw kernels,
specialization-safe rank minors, square compatibilities, and common
\(E_5\) column-kernel exit were independently reconstructed.

The audit rejected the earlier full-row scope.  The pencil stabilizer only
scales \(p/q\), hence fixes infinity, and the missing chart
\[
H_4=((p-aq)^2,q^2,0)
\]
has its own resonances \(c=3a\) and \(2c=3a\).  The audit records exact
leading-order witnesses to the omission.  Thus the promoted theorem closes
only the chart with both outer critical points and the companion finite;
the projective-infinity charts remain active.  Optimized-Python and forged
GP-diagnostic tests now fail closed.

### Marked-critical infinity orbit

At 2026-07-25T06:11:00Z all supplied and hostile-audit checks passed:

```text
cd line22_marked_critical_infinity
/usr/bin/python3 verify_line22_marked_critical_infinity_sympy.py
./verify_line22_marked_critical_infinity_pari_strict.sh
/usr/bin/python3 audit_hostile/audit_exact_reconstruct.py
./audit_hostile/test_python_guard.sh
./audit_hostile/test_runner_faults.sh
```

For the single orbit
\[
H_4=(x^4,y^2z^2,0),\qquad (H_3)_3=x^3,
\]
the raw \(E_7\) matrix has rank \(8\) and nullity \(18\), with a complete
four-direction affine quotient.  The rank-\(4\) \(E_6\) converse splits
into four specialization-safe \((A,C)\) leaves.  Cubes, squares, and in the
last resonant leaf the division-free identity
\[
\det L_0=\frac{\ell_{31}}3[x^2]E_2
\]
force a singular linear part in every case.

The hostile audit independently reconstructed the target-shear effects on
\(H_2,L_0\), all zero specializations, the extra harmless \(K=0\)
products, and every lower exit.  It also fault-tested the Python guard and
strict GP wrapper.  This removes only \((a,c)=(0,0)\) from the
outer-critical-infinity chart; all neighboring moduli remain open.

### Complete fixed-divisor conic row

At 2026-07-25T04:03:51Z the complete nonbinary regression passed with

```text
/usr/bin/python3 verify_nonbinary_fixed_conic_sympy.py
gp -q verify_nonbinary_fixed_conic_pari.gp
```

The binary companion regressions were rerun in the same clean state:

```text
/usr/bin/python3 verify_fixed_conic_row_sympy.py
gp -q verify_fixed_conic_row_pari.gp
```

The nonbinary SymPy implementation checks the general adjugate and kernel
identities, all five raw degree-seven compatibility systems, their
translation-normalized tangent forms and complete quadratic kernels, and
the division-free degree-six singular-linear-part exits.  PARI/GP
independently re-expands the same determinant identities.

A separate adversarial audit reconstructed the parabolic classification
into exactly seven normal forms, independently checked the three final raw
radicals and their converses, verified every affine translation sign and
the reused six-parameter quadratic kernel, and reproduced each triangular
degree-six table.  It also confirmed the scope distinction: the five
nonbinary branches admit no Keller map, while the binary theorem says
Keller implies automorphism.  Together the two notes exclude the entire
fixed-divisor conic row
\[
(e,a,b,\delta,\nu)=(2,1,2,2,1).
\]

### Transverse cuspidal cubic

At 2026-07-25T04:07:17Z both exact regressions passed:

```text
/usr/bin/python3 verify_cuspidal_cubic_exit_sympy.py
gp -q verify_cuspidal_cubic_exit_pari.gp
```

The SymPy regression reconstructs the ramified normal and Hilbert--Burch
syzygies for
\[
H_4=r(p^2q,p^3,q^3)^T,
\]
the full degree-seven and degree-six coefficient systems and ranks, the
complete quadratic solution, and every lower factor.  PARI/GP independently
expands the determinants, checks the parameterized solutions, and verifies
all final homogeneous coefficients and \(\det L_0\).

An independent audit first reconstructed the projective and transverse
normalization, then used a fresh coefficient dictionary rather than the
scripts' extraction path.  It reproduced the degree-seven rank \(14\), the
three compatibility entries, the four-dimensional kernel, the degree-six
rank \(8\), its one-dimensional linear-part nullspace, and the degree-five
and degree-three factors.  It also checked the PARI source for reserved
symbols and false-pass paths.  The conclusion excludes exactly the
transverse cuspidal branch.  The following independently audited theorem
closes the complementary scalar-aligned branch.

### Scalar-aligned cuspidal cubic

At 2026-07-25T04:36:50Z both exact regressions passed:

```text
/usr/bin/python3 verify_scalar_aligned_cusp_sympy.py
gp -q verify_scalar_aligned_cusp_pari.gp
```

The SymPy regression reconstructs the three raw degree-seven systems and
their branch radicals, all complete tangent-leaf quadratic families, the
binary-leaf degree-six ranks \(7,6,7\), and every constant obstruction.
PARI/GP independently expands the normalized leaves and reproduces the
same lower coefficients.

The adversarial audit independently proved that the embedded cusp's
stabilizer is diagonal and has exactly the cusp, flex, and general
marked-point orbits.  It printed the raw compatibility systems, verified
every forcing order and converse, checked the quadratic-kernel dimensions,
and reproduced the constants
\[
-12,\qquad -48,\qquad 12,\qquad 24.
\]
No specialization or relative-position modulus is omitted.  Together with
the transverse theorem, this excludes the entire cuspidal-cubic taxonomy
row.

### Nonbinary fixed-cubic line stratum

At 2026-07-25T04:41:47Z both exact regressions passed:

```text
/usr/bin/python3 verify_fixed_cubic_line_sympy.py
./verify_fixed_cubic_line_pari_strict.sh
```

The SymPy regression checks the rank-one adjugate identity, both
logarithmic derivation formulas, the exact degree-eight/degree-seven
polarization, the complete exceptional invariant space for \(h=pr^2\),
and both residual orbit exits.  PARI/GP independently expands the
normalized determinant identities.  The strict wrapper rejects every GP
diagnostic and requires a unique pass marker.

The adversarial audit independently reconstructed the factor-multiplicity
classification, proved that the nonzero exceptional invariant has exactly
the \(qr\) and \(pr\) stabilizer orbits, repeated the raw degree-six and
degree-five normalizations, and checked the plane-field birational exit.
It also injected a diagnostic, extra output, and nonzero status into the GP
wrapper; all three false-pass attempts were rejected.  This excludes
exactly
\[
H_4=h(p,q,r)(p,q,0)^T,\qquad h\notin\mathbb C[p,q].
\]
The binary cubic fixed-divisor locus remains.

### Conic double cover

At 2026-07-25T05:19:48Z both exact implementations passed:

```text
/usr/bin/python3 verify_conic_double_cover_exit_sympy.py
./audit_conic_double_cover_hostile/audit_conic_double_cover_pari_strict.sh
```

The SymPy regression starts with all \(30\) cubic, \(18\) quadratic, and
\(9\) linear coefficients.  It reconstructs the rank-\(16\) degree-eight
kernel, rank-\(9\) degree-seven solve, both constant rank-\(6\)
degree-six systems, every affine gauge, the full \(PM=0\) slice, and the
degree-five/degree-four exits.  A `__debug__` guard prevents optimized
Python from disabling its assertions.

The hostile audit independently reconstructed the degree-two-cover
normalization, stabilizer quotient, ranks, kernels, gauge converses, and
every zero/nonzero specialization.  Its PARI/GP implementation reproduces
the decisive identities from raw Jacobian determinants; the strict wrapper
rejects diagnostics, trailing output, and nonzero status.  The audit found
the strengthening
\[
P=0\Longrightarrow
E_5=-4\ell_{31}x^4y+8\ell_{21}x^2y^3-4\ell_{11}y^5,
\]
so that branch directly forces a zero first column of \(L_0\).  No omitted
branch or failing equation was found.  This excludes the complete row
\[
(e,a,b,\delta,\nu)=(0,1,4,2,2).
\]

### Nonbinary fixed-quadratic line double cover

At 2026-07-25T05:38:33Z the supplied exact implementations and the
independent hostile reconstruction passed:

```text
cd fixed_quadratic_line_doublecover
/usr/bin/python3 verify_nonbinary_fixed_quadratic_line_sympy.py
./verify_nonbinary_fixed_quadratic_line_pari_strict.sh
./audit_hostile/audit_reconstruct_pari_strict.sh
```

The supplied checks reconstruct the general adjugate and logarithmic
derivation, both raw exceptional orbit systems, every lower
specialization, and the final determinant vanishings.  The hostile audit
independently proves the global square rehomogenization and full stabilizer
exhaustion.  Its raw coefficient matrices have constant ranks
\[
E_6:10,14,\qquad E_5:4,6,
\]
and it verifies the \(K\ne0\) lower ranks \(4,3\), the literal
divisibilities \(M\mid\det L_0\), \(M_*\mid\det L_0\), and
\[
a[pr]E_2-[p]E_1=M_*^2.
\]
Optimized-Python and GP-diagnostic fault injection both fail closed.  This
excludes exactly the nonbinary part of
\[
(e,a,b,\delta,\nu)=(2,1,2,1,2);
\]
the binary fixed quadratic remains.

### Transverse fixed-linear line triple cover

At 2026-07-25T05:47:58Z the supplied implementations and independent
hostile reconstruction passed:

```text
cd fixed_linear_line_triplecover
/usr/bin/python3 verify_nonbinary_fixed_linear_line_sympy.py
./verify_nonbinary_fixed_linear_line_pari_strict.sh
./audit_hostile/audit_reconstruct_pari_strict.sh
```

The checks retain eight independent coefficients for a completely general
pair of binary cubics.  They reproduce
\[
\nabla(rA)\times\nabla(rB)=p^6s(ab'-a'b)(-1,-t,3s)
\]
and, for a degree-\(d\) homogeneous form,
\[
D(G)=p^{d+5}s(ab'-a'b)(4sg_s-dg).
\]
They also reconstruct both raw determinant polarizations and the complete
degree-two and degree-three eigenvalue tables.  The hostile audit verifies
that the nonunit Wronskian cancels in the integral domain, no cubic-cover
modulus is normalized away, and generic degree descends through the
plane-field base change.  Optimized Python and injected GP failures are
rejected.  This excludes exactly the transverse/nonbinary part of
\[
(e,a,b,\delta,\nu)=(1,1,3,1,3);
\]
the binary fixed line remains.

### Horizontal fixed-linear primitive cubic pencil

At 2026-07-25T06:18:12Z the exact and hostile-audit checks passed:

```text
cd fixed_linear_cubic_pencil
/usr/bin/python3 verify_horizontal_fixed_linear_cubic_pencil_sympy.py
./verify_horizontal_fixed_linear_cubic_pencil_pari_strict.sh
./audit_hostile/audit_finite_field_strict.sh
./audit_hostile/audit_supplied_runners.sh
```

For
\[
H_4=h(p,q,0),\qquad \deg h=1,\quad\deg p=\deg q=3,
\]
with \((p,q)\) a minimal coprime pencil and no pencil member divisible by
\(h\), a homogeneous normal first integral \(G\) of degree \(d\) gives
\[
\frac{G^4}{(hp)^d}=R(q/p).
\]
Valuation along \(h=0\) forces \(4v_h(G)=d\), impossible for \(d=2,3\).
The degree-eight and degree-seven Keller identities therefore kill the
cubic and quadratic third components, after which the plane-fibre exit
makes the map an automorphism.

The independent audit reconstructed the minimality/relative-closure
argument, scaling descent, divisor valuation, determinant polarizations,
and plane exit.  A dependency-free finite-field implementation checked
the low-degree kernels and both top coefficients; strict runners reject
optimized Python, GP diagnostics, trailing output, and nonzero exits.

The theorem is sharp only at the top identities.  On the vertical locus
\(p=h^m r\), the valuation acquires the term
\[
m\,\operatorname{ord}_{\infty}R,
\]
and explicit primitive examples retain nonzero quadratic or cubic normal
first integrals.  Those witnesses are not Keller maps, and the vertical
locus remains active.

### Unified fixed-divisor verticality principle

At 2026-07-25T06:54:01Z the supplied checks, independent reconstruction,
and fault tests passed:

```text
cd fixed_divisor_verticality
/usr/bin/python3 verify_fixed_divisor_verticality_sympy.py
./verify_fixed_divisor_verticality_pari_strict.sh
/usr/bin/python3 audit_hostile/audit_reconstruct_modp.py
./audit_hostile/test_supplied_runners.sh
```

For every primitive quartic line-pencil leading form
\[
H_4=(hp,hq,0),\qquad
\deg h=e,\quad\deg p=\deg q=4-e,\quad1\le e\le3,
\]
the degree-eight identity and scaling descent give
\[
G_3^4/(hp)^3=R(q/p).
\]
At a horizontal prime \(f^m\mid h\), all finite and infinite pencil
factors have valuation zero, so \(4v_f(G_3)=3m\).  This is impossible for
\(m=1,2,3\); the cubic normal component vanishes and the audited
quadratic-component theorem gives an automorphism.

The independent checker uses dependency-free finite-field arithmetic and
also tests a degeneration where another factor of \(h\) is shared with a
pencil member.  The hostile audit verified the relative-closure descent,
\(E_8\) orientation, all three row corollaries, and the complete
fixed-quadratic all-vertical frontier.  The strict runners reject
optimized Python, explicit algebra failures, PARI diagnostics, trailing
output, and nonzero exits.

### Rank-one-restriction line-\((2,2)\) open orbit

At 2026-07-25T07:02:00Z the supplied checks, guard suite, and clean-room
audit passed:

```text
cd line22_rankone_restriction
/usr/bin/python3 verify_rankone_restriction_sympy.py
./verify_rankone_restriction_pari_strict.sh
./test_verifier_guards.sh
/usr/bin/python3 audit_hostile/audit_rankone_exact.py
```

For \(p=x^2,q=y^2+xz\), the source stabilizer induces the full Borel
fixing the marked double-line value.  On the unmarked-critical normal
form
\[
H_4=((p-q)^2,(p+q)^2,0),\qquad
(H_3)_3=x(p-cq),
\]
the exact open \(E_7\) minor has zero set \(c(c^2-9)=0\), and eight
explicit kernel directions give the matching upper rank bound.  After the
complete affine/target gauge, \(E_6\) has a full ten-variable forcing
minor and \(E_5\) forces both remaining columns of the linear part to
vanish.

The clean-room audit independently recovered the stabilizer, six joint
orbits, all exceptional raw ranks, the dependent translation jet, and
alternate \(E_7,E_6,E_5\) minors.  The strict wrapper uses an exact output
whitelist and the guard suite injects optimized Python, diagnostic,
unexpected-output, missing-output, and nonzero-exit failures.  The
theorem excludes exactly \(c(c^2-9)\ne0\); it does not claim the marked
or exceptional frontier.

### Binary fixed-cubic line row

At 2026-07-25T06:55:00Z the promoted verifiers and two clean-room hostile
reconstructions passed:

```text
cd ..
/usr/bin/python3 -u verify_binary_fixed_cubic_complete.py
gp -q verify_binary_fixed_cubic_complete_pari.gp
/usr/bin/python3 -u audit_binary_fixed_cubic_hostile/audit_orbits_lower_exact.py
/usr/bin/python3 -u audit_binary_fixed_cubic_hostile/audit_exceptional_branches_exact.py
./audit_binary_fixed_cubic_hostile/test_fail_closed.sh
```

For \(H_4=h(p,q)(p,q,0)\) with binary cubic \(h\), the verification
enumerates all squarefree, double-root, and triple-root stabilizer orbits
of the binary cubic normal component.  It certifies the local root-order
formula, every raw tangent splitting, all parameter pivots, the
\(\rho=2,3,4\) exceptional branches, and the complete lower-syzygy
kernel.  The only four zero-normal lower leaves end in the exact constants
\[
-24/5,\qquad-15/2,\qquad3/2,\qquad-12.
\]

The hostile scripts independently assert every raw \(E_6\) rank, both
conjugate algebraic branches, and a converse row reduction for the
delicate \(t4\) branch.  They also verify the degree bounds in all
coordinate exits and inject false identities to test fail-closed
behavior.  No Keller-compatible leaf remains.  Combined with the audited
nonbinary theorem, this closes the full fixed-cubic line taxonomy row.

### Outer-infinity finite companions in line-\((2,2)\)

At 2026-07-25T07:01:00Z the supplied symbolic, direct-determinant, and
fault-injection checks passed, followed by an independent hostile audit:

```text
cd line22_outer_infinity_remaining
/usr/bin/python3 verify_line22_outer_infinity_remaining_sympy.py
./verify_line22_outer_infinity_remaining_pari_strict.sh
./test_fail_closed.sh
```

For \(p=x^2,q=yz\),
\[
H_4=((p-aq)^2,q^2,0),\qquad
(H_3)_3=x(p-cq),
\]
the common-scaling quotient is \(\mathbb P^1_{[a:c]}\) plus the fixed
origin.  The verifier reconstructs raw ranks \(18,14,14,16,18\) on the
generic locus, the two resonances, and the two projective endpoints.
Every complete lower solve makes columns two and three of the linear part
proportional; the \(K=0\) resonance branches are closed by explicit
\(E_4\) squares without cancellation.

The hostile audit independently checked the orbit quotient, target
shears, all maximal minors, kernel dimensions, lower converse ranks, and
zero specializations.  Combined with the separately audited origin, this
excludes every finite companion in the chart.  It does not include the
companion-at-infinity form \(xq\).

### All-vertical fixed-quadratic top obstruction

At 2026-07-25T08:05:00Z the exact reconstruction and independent hostile
audit passed:

```text
cd fixed_divisor_verticality/all_vertical_top_obstruction
/usr/bin/python3 verify_top_obstruction_sympy.py
cd audit_hostile
./audit_exact_pari_strict.sh
/usr/bin/python3 -u audit_reconstruct_mod101.py
./test_audit_guards.sh
```

The same-fibre valuation identity eliminates the genuine
\(h=\ell^2,p=\ell m\) and split
\(h=\ell_1\ell_2\) all-vertical shapes.  In the remaining \(p=h\) shape,
divisor parity forces a unique double-line member, and exact normal-form
and kernel reconstruction leaves precisely
\[
\langle x^2,yz\rangle,\quad\langle x^3,xyz\rangle,
\qquad
\langle x^2,y^2+xz\rangle,\quad
\langle x^3,x(y^2+xz)\rangle.
\]

The hostile audit independently checked the field descent, divisor
pullback, minimality exception, canonical normalizations, kernel ranks, and
quadratic-component exit.  It rejected characteristics \(5\) and \(11\)
after spurious modular kernels appeared; only exact characteristic-zero
and a dependency-free modulo-\(101\) rank certificate are retained.

### Rank-one exceptional \(c=0\) and marked mixed orbits

At 2026-07-25T08:38:00Z the supplied reconstructions and independent
hostile audits passed:

```text
cd line22_rankone_restriction/unmarked_triple_c0
/usr/bin/python3 -u verify_unmarked_triple_sympy.py
cd audit_hostile
./verify_hostile_pari_strict.sh

cd ../../marked_mixed_orbits
/usr/bin/python3 -u verify_marked_mixed_sympy.py
cd audit_hostile
./verify_marked_mixed_pari_strict.sh
./test_fail_closed.sh
```

For the unmarked triple \(c=0\), exact square and cubic compatibility
syzygies force \(w_2=w_3\) and \(w_1=0\).  A constant lower solve then
zeros the second column of \(L\).

For the marked critical pair \(H_4=(p^2,q^2,0)\), the two mixed companions
\(xq\) and \(x(p-q)\) each have a complete five-gauge/three-normal raw
kernel.  Parameter-free \(E_6/E_5\) pivots remain nonzero at
\(w_2=w_3\), and both complete solutions zero the second column of \(L\).
The hostile audit independently reconstructed the orbit ledger, gauges,
all converses, and the collision specialization.

### Fixed-divisor \(e=2\) mixed companions

At 2026-07-25T08:52:17Z the supplied exact certificate and independent
hostile reconstruction passed:

```text
cd fixed_divisor_e2_quadratic_pencils
/usr/bin/python3 verify_mixed_orbits_sympy.py
cd audit_hostile
./verify_mixed_orbits_pari_strict.sh
./test_fail_closed.sh
```

For each canonical unique-double-line pencil
\[
\langle x^2,yz\rangle,\qquad
\langle x^2,y^2+xz\rangle,
\]
the mixed companion \(R=xq\) has a complete raw kernel.  Constant
\(E_6\) pivots split every normal branch.  The rank-two pencil exits by
cube syzygies or four literal determinant coefficients; the rank-one
pencil exits by a \(D^3\) syzygy, the exact resultant
\(-250C^9\), or one of four exhaustive zero-normal charts.

The PARI audit independently reconstructed every matrix and explicitly
verified that cross-multiplication preserves the two polynomial syzygies
at the apparent \(w_4=C\) denominator resonance.  The theorem is scoped
only to the two fixed-divisor \(e=2\) mixed companions.

## Scope

None of these checks excludes every total-degree-four Keller
counterexample.  The certified universal lower bound therefore remains
total degree \(4\), from Vistoli's published degree-three theorem.
