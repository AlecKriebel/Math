# Hostile audit log: conic double-cover exit

**Scope:** Independently reconstruct and attack the claimed conic
double-cover theorem without changing its note or verifier.

**2026-07-25T05:09:14Z — Audit opened**

- Confirmed the target worktree is on `main`.
- Recorded theorem/verifier SHA-256 hashes:
  `7f979b0164e91602f0d43ced447c57b1f8903962b844e28063abb3a0af56c31c`
  and
  `f8587ad8f127f7e8e0cfe855e2b8338d0ac15f2e1652e533f328350459c5e02f`.
- The supplied verifier exits successfully under `/usr/bin/python3`.
- Independent hand reconstruction gives the degree-eight rank decomposition
  \(7+6+3=16\), with a 14-dimensional cubic kernel.
- The degree-seven coefficient matrix is constant of rank nine; its
  homogeneous kernel is precisely the nine binary-quadratic coefficients.
- Both degree-six coefficient matrices are constant, not merely
  generically constant-rank: the two-nonzero matrix has rank six and kernel
  dimension twelve, and the one-nonzero matrix has rank six and kernel
  dimension twelve at every specialization.
- No counterexample has been found to the forcing equations.
- Strengthening/documentation point: on the one-nonzero \(P=0\) slice, the
  already displayed \(E_5\) formula forces the first column of \(L_0\) to
  vanish.  The plane-plus-shear exit is correct but unnecessary there.

**Checkpoint estimate:** 65% of the hostile audit complete.

**2026-07-25T05:18:21Z — Hostile audit complete**

- A methodologically independent PARI/GP regression now reconstructs the
  decisive identities from raw Jacobian determinants.  Its SHA-256 is
  `bed2c80f1b73dcc92aac81e21148bf6cfa4584feea4a240dfef2e655c5985b33`.
- The strict launcher accepts only the unique final sentinel
  `AUDIT_CONIC_DOUBLE_COVER_PARI_PASS_7E4A91`.  A separate self-test
  confirmed rejection of an injected GP diagnostic, trailing output, and a
  nonzero GP exit.
- The degree-two-cover normalization is exhaustive: Riemann--Hurwitz gives
  two distinct simple ramification points and two distinct branch values;
  independent source and target projectivities reduce the cover to
  \([x:y]\mapsto[x^2:y^2]\).  Coprimality removes any residual scalar form.
- The affine translation/shear action on the cubic layer is exactly
  \(\xi H_{4,x}+\eta H_{4,y}+(\mu x+\nu y)T_2\).  The displayed choices hit
  the claimed slices without division.  Constant degree-six matrices and
  12-dimensional displayed solution spaces prove all converses, including
  \(P=M=0\).
- The splits \(ac_2=bc_9=0\) and \(PM=0\) include all zero/nonzero
  specializations.  No rank jump occurs at an intersection.
- Both plane-plus-shear arguments use only the established low-degree plane
  theorem, not the plane Jacobian conjecture.  In this theorem the projected
  plane maps are over \(\mathbb C\); no \(\mathbb C(U)\) step is actually
  needed.  The standard low-degree input is nevertheless stable under
  algebraic base change to \(\overline{\mathbb C(U)}\).
- Documentation strengthening: setting \(P=0\) in the exact \(E_5\) table
  gives
  \[
  E_5=-4\ell_{31}x^4y+8\ell_{21}x^2y^3-4\ell_{11}y^5,
  \]
  so the first column of \(L_0\) vanishes.  This branch is directly
  impossible and does not require a plane exit.
- Verifier hardening issue: the supplied Python verifier uses bare
  `assert` statements throughout.  Running it with `PYTHONOPTIMIZE=1`
  disables every check but still prints `PASS`.  The documented ordinary
  invocation is sound, but an explicit `__debug__` guard or non-assert
  checks are needed for fail-closed operation.

**Final result:** PASS for the mathematical theorem and branch exhaustion,
within the stated taxonomy/factorization input.  No counterexample or
failing equation was found.

**Checkpoint estimate:** 100% of this conic double-cover hostile audit
complete.
