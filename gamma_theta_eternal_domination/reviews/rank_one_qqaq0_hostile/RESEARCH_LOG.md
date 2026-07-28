# Research log: hostile review of rank-one QQ0/AQ0

## 2026-07-28 PDT

- Froze the review target at candidate commit
  `0ddef53f381fa7858e1c6db55f96126b30db5c5b`.
- Confirmed all candidate-manifest hashes and verified that the tracked
  candidate bytes are unchanged from that commit.
- Read the complete accepted C-010, C-108, and C-150 proof sources and
  their hostile reviews.
- Reconstructed the rank-one deletion semantics and both private-witness
  incidence tables.
- Audited all 21 named vertex pairs, every possible named collision, all
  target occupancies, and every one-guard move.
- Checked that the independent-completion split is \(s=t\) versus
  \(s\ne t\); \(s=g\) is impossible because \(gy_g\) is an edge.
- Checked all three possible responders \(x,p,z\) at the decisive attack
  on \(y_p\).
- Confirmed that every graph nonedge comes from independence, the
  private-witness property, or the row hypothesis; no omitted family
  successor is treated as a graph nonedge.
- Reran the candidate strict checker: `PASS`.
- Wrote a clean-room checker scanning all 2,097,152 seven-vertex graph
  masks.  It recovered 32 QQ0 and 32 AQ0 assignments and found no failed
  proof branch.
- Verdict: `UNCONDITIONAL PASS`.
