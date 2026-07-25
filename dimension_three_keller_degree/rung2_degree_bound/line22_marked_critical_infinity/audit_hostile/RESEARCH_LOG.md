# Research log: hostile audit of marked-critical infinity orbit

## 2026-07-25T06:00:54Z — audit opened (5%)

- Scope fixed to the single joint orbit
  `H4=(p^2,q^2,0)`, `(H3)_3=x^3` for `p=x^2,q=yz`.
- Read the provisional theorem, SymPy certificate, PARI/GP reconstruction,
  and strict runner completely.
- Audit targets: complete `E7` quotient/gauges, raw `E6` radical and
  converse, the four `(A,C)` leaves, lower effects of target shears,
  the `K=0` resonant `E2` identity, every zero specialization, and
  fail-closed behavior.
- The theorem and global documents will not be edited.

## 2026-07-25T06:09:28Z — exact reconstruction passed (85%)

- Reconstructed raw `E7` rank `8`, nullity `18`, and an independent
  18-parameter kernel consisting of the 14 gauge-fixed parameters plus
  two target shears and two translations.
- Reconstructed the complete raw `E6` table.  Its lower-unknown matrix has
  constant rank `4`; the two squares kill `w3,w5`, and exact
  back-substitution leaves only the six `A*v_i` products and
  `C*w1,C*w2`.
- Verified every one of the four `(A,C)` cases, including `B=0`, `w0=0`,
  `u4=0`, `r1=0`, `r2=0`, `ell31=0`, and both `K` leaves.
- Verified the first-component target shear acts on all layers by
  `H3_1 -> H3_1+lambda*x^3`,
  `H2_1 -> H2_1+lambda*W`, and
  `row_1(L0) -> row_1(L0)+lambda*row_3(L0)`, while preserving
  `det(L0)`.
- In the `K=0` leaf, confirmed the division-free identity
  `det(L0)=ell31*[x^2]E2/3`.  Also found two omitted but harmless `E4`
  products `r1*Q=r2*Q=0`, where
  `Q=9*C*r4+24*ell31-36*u0-32*w0^2`.
- The SymPy optimized-mode guard works.  The strict GP runner rejected
  injected diagnostics, extra output, a wrong sentinel, and nonzero exit
  status.
- Current verdict: theorem PASS; only exposition and certificate-coverage
  corrections remain.

## 2026-07-25T06:12:04Z — audit complete (100%)

- Wrote `REPORT.md` with explicit theorem/scope verdicts, the complete
  rank/kernel and branch reconstruction, target-shear coordinate ledger,
  zero-specialization audit, exact guard results, and five corrections.
- Re-ran both supplied CAS verifiers, the independent exact
  reconstruction, the optimized-mode test, and all strict-runner fault
  modes successfully.
- Confirmed the result removes only the marked-critical triple point
  `(a,c)=(0,0)` from the corrected infinity-chart frontier.
- The theorem and global documents remain untouched.
