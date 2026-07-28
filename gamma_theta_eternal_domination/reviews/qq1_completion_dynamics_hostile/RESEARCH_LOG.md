# Research log: hostile QQ1 completion-dynamics audit

Date: 2026-07-28 (PDT)

- Froze the candidate at commit `02cab3f6` and verified every candidate
  artifact against `CANDIDATE_MANIFEST.json`.
- Read the accepted C-010, C-064, C-108, C-143, C-146, C-158, and C-161
  source theorems and bound each candidate invocation to its exact
  hypotheses.
- Reconstructed the canonical seven-vertex QQ1 incidence and checked that
  every completion vertex is distinct from the named core.
- Verified that C-143, rather than static independence, forces both
  completion edges \(db,dc\).
- Replayed the cold-witness proof branch by branch.  The C-064
  transposition is \((r\ w)\), fixes \(u,d\), and transports the exact
  singleton list \(\{d\}\); the excluded state \(A=\{u,x,d\}\) is used
  only as a family omission.
- Exhausted all 64 cold-witness incidence assignments.  They partition
  into 32 cases where \(J_d\) misses \(r\), 16 cases with no response at
  \(u\), and 16 cases reaching the terminal no-response attack at \(d\)
  from \(U\).
- Checked every hot-witness collision, all three possible \(b,c\)-side
  patterns, and the exact conditional repair square.  The repair branch
  genuinely requires \(ud\notin E(G)\).
- Re-derived the C-146 distance-two comparison, both mixed-state
  rank-at-most-two attacks, and the unique top rank triple
  \((3,2,2)\).
- Wrote a clean-room graph6 decoder, exact five-parameter evaluator,
  greatest-kernel evaluator, activity checker, and symbolic audit.  It
  reproduces both controls, their 284/285-state kernels, canonical
  incidence, and rank vector \((1,2,2,3)\).
- Verdict: unconditional `PASS`.  The external hot-witness layer remains
  open and no conjecture-resolution claim is made.
