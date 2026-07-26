# Research log

## 2026-07-26 UTC

- Received the frozen `D3-BB-21` normal form \(h=pq,R=p^2q\).
- Independently identified a certificate-completeness gap: the initial
  primary implementation did not check the degree-zero \(E_7\) block
  (the possible \(r^3\) terms of \(U,V\)), and the full routine did not
  explicitly replay \(E_9,E_8\).
- Reported both points before issuing a verdict.  The candidate release was
  repaired in both its primary and independent implementations.
- Built a third, dependency-free exact determinant implementation.  It
  verifies the full \(E_7\) rank atlas, \(E_9,E_8,E_7\), raw \(E_6\)
  squares, the complete unit-pivot residual, the decisive \(E_5\)
  coefficient, both resultants, the frozen-family bridge, and the origin
  structural identity.
- Audited both origin charts and confirmed that they use Moh's
  unconditional bounded-degree plane theorem, not the plane Jacobian
  Conjecture.
- Verdict: certified fine-family exclusion; no parent-row or global claim.

## 2026-07-26T09:37:13Z

- Replayed the BB-only hostile wrapper after the shared release gained the
  full BS primary certificate and a warning-safe PARI diagnostic filter.
- Updated the release-contract check to bind the hardened diagnostic
  semantics rather than the superseded literal pattern.
- Final marker remained `D3_BB21_HOSTILE_RELEASE_AUDIT_PASS`; this is the
  first certified release timestamp for the single `D3-BB-21` fine-family
  exclusion.
