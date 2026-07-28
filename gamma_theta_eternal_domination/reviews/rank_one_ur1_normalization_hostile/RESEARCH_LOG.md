# Research log: hostile review of rank-one \(ur=1\) normalization

Date: 2026-07-28 (PDT)

- Bound the review to candidate commit
  `84bbe50d4c21a4956930ec84bfa637c6e99e5ec7`.
- Read the accepted C-010, C-064, C-108, and C-150 source proofs in full
  at the frozen hashes recorded in `REVIEW.md`.
- Reconstructed the QQ1 collision \(a=x\) directly.  Confirmed that it is
  a valid private witness, introduces no loop, and is not covered by a
  fresh-\(a\) argument.
- Replayed the private-witness transfer, every possible \(b\)-response
  from \(M_q\), the forced \(U\to R\) response, and both AQ1 paths from
  \(R\) to \(S\).
- Recomputed all four private-marker ridge permutations in the direction
  prescribed by C-064.  Confirmed that the end markers pull back to the
  forbidden \(r\)-responses.
- Enumerated all 32 QQ1 and 128 AQ1 named incidence assignments.  Exactly
  one assignment in each row survives, and it is the candidate's
  saturated normal form.
- Audited the exclusion of \(W\), both \(x\)-side edges, \(bc\), \(up\),
  and \(uq\) with complete one-guard response trees.
- Enumerated all four \(sa,sq\) patterns in the proof of
  \(u\triangleright a\), checked that the completion vertex \(s\) cannot
  collide with another named vertex after saturation, and verified the
  separate C-108 deduction \(a\not\triangleright u\).
- Verified that AQ1 retains the same state \(B\), deletion rank, blocker,
  movers, three non-dominating successors, and private witnesses when
  reinterpreted as QQ1 on \(S=\{a,p,q\}\).
- Audited an arbitrary completion \(d\in C_{ar}\).  All four
  \(dp,dq\) patterns were checked; only the full-hit pattern survives.
- Independently decoded and evaluated `Hslaghb` without importing the
  candidate checker or campaign verifiers.  Reproduced
  \((9,17;3,3,3,4,4)\), the empty triple kernel, deletion rounds
  \(24,21\), and the 101-state four-guard kernel.
- Replayed the candidate strict verifier and the new clean-room strict
  verifier.  Both passed.
- Final verdict: unconditional `PASS` at the exact stated scope.
