# Research log: three-color full-list coupling

## 2026-07-28 15:40 PDT

- Reconstructed the exact hypotheses and scope of accepted C-149, C-154,
  C-157, C-163, and C-165, including the hostile review of C-165.
- The active hypothesis is that all three single-target color-restricted
  kernels are empty.  For each root color we may therefore choose a retained
  terminal entry of minimum predecessor rank.
- Important scope check: an equality graph with all three kernels empty would
  already have clique-cover gap at this full target, so an equality "control"
  for the entire hypothesis would be a genuine counterexample, not a harmless
  boundary example.
- Derived a candidate rank-zero corridor transfer.  With
  \(S=\{u,v,t\}\), predecessor \(\{v,t,q\}\), terminal
  \(\{v,t,r\}\), secondary color \(v\in Q(r)\), and C-157 witness \(w\)
  missed by \(\{t,q,r\}\), domination forces both \(uw\) and \(vw\).
  Two unique attacks retain \(\{w,t,q\}\) and \(\{w,t,r\}\).
  Arbitrary-state restoration applied to \(\{w,t,q\}\) then forces
  \(v\in Q(q)\cup Q(w)\).
- The known 16-vertex equality control realizes cyclic corridor palette
  transfers while one color remains safe.  Thus palette-transfer incidence
  alone cannot prove survival; the distinguishing datum must be the finite
  deletion rank in each of the other two color bans.
- Current best-guess completion: 20% toward a publishable coupling reduction;
  below 5% toward closing the all-three-empty branch in this lane.

## 2026-07-28 15:52 PDT

- Proved the rank-zero corridor witness ladder.  Besides C-157's missed
  alternate, it forces the retained states \(\{w,t,q\}\) and
  \(\{w,t,r\}\).  The attack at the omitted anchor from the first state
  gives the exact transfer
  \[
     v\in Q(q)\cup Q(w).
  \]
  The proof uses no palette-omission-to-nonedge inference.
- Classified the three selected secondary-color maps.  There are eight
  labeled fixed-point-free maps: two directed 3-cycles and six
  2-cycle-with-tail maps.  This is the complete finite color bookkeeping
  for three nonsingleton rank-zero corridor rows.
- Identified the exact unresolved implication.  A transfer endpoint outside
  \(B=N_{\overline G}(x)\) gives a retained state of finite rank in the
  recipient color ban, but the named unrestricted-family attacks give no
  strict comparison between ranks from different bans.  A transfer endpoint
  inside \(B\) is banned and has no restricted rank at all.
- Replayed two sharp controls.  The 16-vertex equality graph has cyclic
  terminal palettes and two exact witness transfers, while its third color
  has a 150-state safe kernel.  MMV-001 has all three kernels empty and the
  complete witness-mover 3-cycle, but has the unique dominating pair
  \(\{8,9\}\) and \(\gamma=2\).
- A discovery-only SAT encoding returned unlogged `UNSAT` at orders 10--15;
  order 16 was stopped at the five-minute cap.  These rows are frozen as
  `OBSERVED` and are not used as a theorem or finite exclusion.
- Strict replay of both controls and the color-map count passes with result
  SHA-256
  `80128eebfe49204b33ed56ab1676e25a093e93c4a39b018afde913d9cf749c1a`.
- Best-guess completion: 100% for this bounded coupling checkpoint; 35%
  toward eliminating the all-rank-zero nonsingleton-corridor subcase; about
  7% toward closing the full all-three-empty branch from this lane.  These
  are workload estimates, not probabilities.
