# Hostile-review checklist: \(\kappa=16\) exclusion

The auditor should try to break, rather than summarize,
`DELTA2_KAPPA16_EXCLUSION.md`.

1. Reconstruct the exact-\(\delta=2\) open condition
   \(\operatorname{Res}(h,R)=-2(a+d)^2\) and verify that no common-root
   or constant-dependent branch was silently retained.
2. Reconstruct the \(\mathcal M_1\) kernel
   \((5p+q,-p-5q,3(a-d))\), the two \(\mathcal M_0\) generators \(pN,qN\),
   and the integrated family with the factor \(k/2\).
3. Check that the lower family retains every binary \(H_3,H_2\)
   coefficient and all nine entries of \(L\).
4. Recompute \([r^3]E_6\), including both endpoint coefficients.
5. Audit the two exceptional mutations \(a=-2d\) and \(d=-2a\) in the
   proof that \(m=n=x_5=y_5=0\).  No generic-rank argument may replace
   these divisor checks.
6. Verify that the \(E_6\) kernel is parameterized without division by
   \(a-d\), especially at \(a=d\).
7. On \(\lambda=0\), verify both rank-covering minors and the literal
   zero third column of \(L\).
8. On \(\lambda(a-d)\ne0\), inspect the triangular source change and
   prove \(\deg_{p,q}(P,Q)\le4\) after substitution.  Confirm that the
   cited plane theorem is unconditional in degree four after base change,
   that generic degree descends, and that the birational Keller theorem
   yields a polynomial automorphism.  Reject any hidden appeal to the
   full plane Jacobian Conjecture.
9. On \(a=d\), reconstruct the rank-six \(E_5\) solve, its pivot
   determinant, and \([r]E_4=72a\lambda^2(p+q)^3\).
10. Fault-inject the strict wrapper: optimized Python, a sign mutation in
    (25), extra PARI output, and a nonzero PARI exit must all be rejected.

The audit report should distinguish algebra checked by CAS from the
field-theoretic plane exit, and should state explicitly whether the
candidate theorem is safe to promote.
