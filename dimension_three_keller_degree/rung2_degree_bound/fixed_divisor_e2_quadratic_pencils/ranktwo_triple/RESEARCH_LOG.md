# Research log: rank-two fixed-divisor triple companion

All timestamps are UTC.

## 2026-07-25T08:49:20Z — provisional branch proof

- Reconstructed the raw \(36\times26\) \(E_7\) system with rank \(8\),
  five legal gauges, and a thirteen-parameter normal complement.
- Derived the constant-pivot \(E_6\) split using
  \(K=9A-12w_4\) and \(M=-3A+8w_4\).
- Closed the apparent generic, resonant, and origin branches in the
  first SymPy certificate.  The theorem remained provisional pending
  hostile audit.

## 2026-07-25T09:00:00Z–09:42:15Z — three gaps found and repaired

- Independent PARI/GP reconstruction found that the generic aligned
  pivot vanished at \(9A=2K,\ B_1=B_3=0\).  A fresh solve closed the
  leaf by two \(E_4\) squares and a \(2\times2\)-minor identity.
- The claimed \(r=0\) obstruction was localized at \(B_3\).  The fresh
  \(B_3=0\) chart has pivot \(144B_4s^2\) and the contradiction
  \([y^4]E_4=4s^4/27\).
- The terminal generic \(E_5\) pivot was localized at \(B_1\).  Global
  literal \(E_5\) rows instead give an exhaustive split on \(a_4\);
  fresh \(E_4\) rows force \(\ell_{32}=\ell_{33}=0\) on both leaves.
- Each repair was added to the primary proof and independently rechecked.

## 2026-07-25T09:46:39Z — audited theorem banked

- Corrected SymPy and independent PARI/GP certificates pass.
- Optimized Python mode is rejected with exit status \(2\).
- Arithmetic-corruption and missing-attestation injections are rejected.
- Hostile verdict: PASS.  The result is exact but not peer reviewed.
- Together with the mixed-companion theorem, this closes both cubic
  companion orbits for the rank-two canonical fixed-divisor pencil.
