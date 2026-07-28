# Research log: hostile review of nonsingleton terminals

## 2026-07-28 PDT

- Froze commit `8a77c68c` and verified every candidate-manifest hash.
- Read the accepted C-149 source and checked the restricted-universe and
  synchronous deletion-rank conventions against the candidate proof.
- Audited the direct-root/nonroot split, every role collision, ban
  nonmembership, and the use of a rank-zero deletion-witness attack.
- Confirmed that Corollary 2.2 is conditional on three selected traces whose
  final predecessors have rank zero; it makes no positive-rank existence
  claim and leaves anchor restoration open.
- Wrote a clean-room packed-bitmask replay.  It independently recovered
  \((\gamma,\alpha,\gamma^\infty,\theta)=(3,3,3,3)\), the 304-state literal
  greatest family, all three restricted peelings and ranks, the cyclic
  palettes, exact moves, missed witnesses, diamonds, and occupancy audit.
- Exhausted 8,192 direct-root seven-vertex completions, 1,024 nonroot
  seven-vertex completions, and 131,072 nonroot eight-vertex completions.
  The weakened local premise occurred nonvacuously, including 64
  two-secondary rows, with no conclusion failure.
- Verdict: unconditional PASS on the reviewed bytes.  The all-three-empty
  nonsingleton branch remains open.
