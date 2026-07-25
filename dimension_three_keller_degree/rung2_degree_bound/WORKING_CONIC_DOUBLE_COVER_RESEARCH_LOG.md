# Research log: conic double-cover quartic row

## 2026-07-25T04:50:23Z

- Created an isolated analysis for the taxonomy row
  \((e,a,b,\delta,\nu)=(0,1,4,2,2)\), without changing shared working
  theorems or verification records.
- Reconstructed the degree-eight operator on a general 30-coefficient
  cubic.  Exact rank: 16.  Its 14-dimensional kernel is
  \(C_3(x,y)+z(2ax^2,ay^2+bx^2,2by^2)\).
- Solved degree seven against all 18 quadratic coefficients.  Exact rank:
  9.  The only compatibilities are \(bc_9=ac_2=0\), and the full
  nine-parameter affine solution for \(H_2\) was retained.
- Classified the stabilizer zero patterns of \((a,b)\) into
  \((0,0),(1,1),(1,0)\), plus the exact \(x\leftrightarrow y\),
  output-\(1\leftrightarrow3\) involution.
- In the two-nonzero branch, computed the \(13\times18\) degree-six
  system of rank 6.  Six linear cokernel equations exhaust the locus; the
  seventh polynomial cokernel row was given an explicit ideal
  certificate.  Affine gauges kill all four surviving cubic parameters.
  The canonical degree-five coefficient forces the first two columns of
  \(L_0\) to vanish.
- In the one-nonzero branch, computed the \(10\times18\) degree-six
  system of rank 6 and reduced its complete affine slice to five moduli
  \(S,D,P,M,N\) with \(PM=0\).  For \(P\ne0\), exact degree-five and
  degree-four coefficients force a zero column of \(L_0\).  For \(P=0\),
  the coordinate \(U=z+x^2\) turns the full map into a plane
  degree-at-most-four Keller map plus a shear, retaining all
  \(S,D,M,N\).
- Verified every displayed determinant and rank assertion with the new
  exact SymPy regression.

**Checkpoint estimate:** 100% of the conic double-cover normal-form
branches are algebraically covered, conditional only on the already banked
plane degree-at-most-four theorem.  The result is ready for an independent
adversarial audit; it has not been peer reviewed.

## 2026-07-25T05:00:42Z

- Final self-check made every normalization and compatibility converse
  explicit, added the AI-assistance/exact-check disclosure, and confirmed
  that the verifier reconstructs the raw E8, E7, and both E6 coefficient
  operators before specializing to canonical forms.
- Clean rerun:
  `/usr/bin/python3 verify_conic_double_cover_exit_sympy.py` passed.
- No shared document was edited and no commit was created.

## 2026-07-25T05:19:48Z

- A hostile audit independently reconstructed the degree-two-cover
  normalization, stabilizer, raw \(E_8,E_7,E_6\) ranks, affine gauges,
  branch converses, all zero/nonzero intersections, and the lower exits.
- A methodologically independent PARI/GP regression and fail-closed wrapper
  pass.  Fault injection confirmed rejection of a GP diagnostic, trailing
  output, and nonzero exit status.
- The audit found one strengthening: in the \(P=0\) branch, the already
  computed degree-five identity directly forces the first column of
  \(L_0\) to vanish.  The plane-plus-shear factorization remains a valid
  independent structural check but is not needed for exclusion.
- Added a `__debug__` guard to the SymPy verifier so optimized Python cannot
  disable every assertion and still print a pass marker.
- Final hostile-audit result: PASS.  No normalization gap, hidden
  specialization, false plane-Jacobian-conjecture inheritance, or failing
  determinant equation was found.
