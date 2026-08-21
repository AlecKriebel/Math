# Research log

## 2026-07-25T10:36:00Z — audit opened

- Began a from-scratch audit of
  `../ABSTRACT_BINARY_QUARTIC_HB_E6.md`.
- Kept the audit separate from the candidate note and did not import its
  SymPy verifier.
- Flagged the initial high-risk points: \(R=0\), height two after gcd
  removal, possible \(\delta=5\), dependence of the two gradient columns,
  the wedge scalar, the two \(\delta=2\) rows, all \(E_6\) signs, and the
  arbitrary-linear-part \(\delta=0\) exit.

## 2026-07-25T10:49:00Z — proof reconstruction

- Proved \(\delta\le4\) directly from constant independence, so the reduced
  ideal is proper; gcd one then forces height two.
- Recovered the syzygy-degree window \(d+1\le e_i\le d+3\).  The upper
  bound uses independence of both gradient columns, a step only implicit in
  the candidate.
- Recovered \(k_1+k_2=\delta\) twice: from the wedge determinant and from
  the Hilbert--Burch degree sum.
- Derived the power-fibre result from the two exact Euler identities
  \(3RS_p-4SR_p=qJ(S,R)\) and
  \(3RS_q-4SR_q=-pJ(S,R)\), then checked scalar normalization.
- Reconstructed the weight-six determinant term by term and found the
  candidate signs correct.

## 2026-07-25T10:59:04Z — exact replay and verdict

- Completed the independent PARI/GP certificate.
- Strict run passed all identities, all six Hilbert--Burch/nullity shapes,
  the \(R=0\) separation, the power fibre, and the \(\delta=0\) exit.
- Fourteen fault injections all failed closed.
- Verdict: **PASS**, with two nonfatal exposition recommendations recorded
  in `REPORT.md`.
- Estimated completion of this bounded audit task: **100%**.
