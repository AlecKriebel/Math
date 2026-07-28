# Research log: full-list cross-ban rank gate

## 2026-07-28 15:42--16:36 PDT

- Reconstructed accepted C-149, C-157, C-163, C-165 and the reviewed
  rank-zero corridor-transfer package at commit `db9c046d`.
- Audited the exact separation between unrestricted family closure and
  deletion witnesses belonging to different color bans.  In particular,
  an unrestricted attack is never treated as a deletion witness for the
  recipient peeling.
- Replayed MMV-001 and confirmed that its three transfer endpoints have
  recipient rank zero, equal to the three source ranks.  This refutes any
  unconditional strict cross-ban descent.
- Scanned the fixed MMV catalog and two accepted equality controls for
  rank-zero witness transfers.  The scan located exactly two observed
  transfers with their witness inside \(B\), both in MMV-027.  The scan
  also exhibited recipient ranks \(0,1,2,3,4\) and surviving recipient
  kernels, falsifying several local monotonicity guesses.  The aggregate
  scan remains `OBSERVED`.
- Built a bounded SAT falsifier for one trapped witness.  The final named
  encoding reported `UNSAT` without proof logs at orders 8--15.  The
  order-16 run was stopped at the five-minute gate and no higher order
  was attempted.  All solver statuses remain `OBSERVED` and are unused
  in the theorem.
- Used ablations only as a proof-discovery aid.  They isolated three
  forced attack mechanisms:
  1. the trapped witness forces the third-anchor edge \(tr\);
  2. the new missed witness must lie outside \(B\);
  3. two further unique attacks force \(uy\) and the unbanned retained
     root swap \(S-u+y\).
- Wrote the complete human proof as Theorem 2.1 in `NOTE.md`.  The proof
  explicitly audits every occupied/unoccupied collision, every move
  edge, the exact rank-zero initial universe, and the distinction between
  a missing palette entry and a graph nonedge.
- Wrote a standalone frozenset-based verifier for MMV-027.  It recomputes
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,4)\), the 122-state
  literal greatest family, all three empty restricted kernels, the two
  private witnesses, the forced escape, and equal source/escape
  color-6 ranks \(0,0\).
- Best-guess completion: trapped-endpoint subgate **100%**; full
  cross-ban rank gate **45%**; complete \(k=3\) proof **49%**; universal
  conjecture resolution **18%**.  These are workload estimates, not
  probabilities that the conjecture is true.
