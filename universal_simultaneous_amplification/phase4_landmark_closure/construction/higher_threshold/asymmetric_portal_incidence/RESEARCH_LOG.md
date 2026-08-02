# Research log: asymmetric portal incidence

## 2026-08-02 10:24 PDT — Program opened

- Created a dedicated folder for the first portal regime not covered by the
  exchangeable multiportal theorem.
- Model in progress: finitely many portal identities, symmetric but
  nonexchangeable portal weights, finitely many blade types, and a general
  nonnegative portal-by-blade incidence matrix.
- First task: derive and independently check the exact multitype stopped
  strong-pair trace under both update rules, then optimize its establishment
  laws at fixed fitness values above `3/2`.
- No literature search or external contact.

## 2026-08-02 10:47 PDT — Exact general trace and rank-one theorem

- Derived the exact rare-mutant trace for `Q` labelled portals and `T`
  blade types.  The phase-type episode retains every nonempty portal subset;
  the parent lifetime law is a genuinely multitype PGF.
- Independently specialized all general rates to the already certified
  exchangeable multiportal formulas.
- Proved a no-go theorem for arbitrary positive, unequal portal loads when
  the blade-incidence matrix has rank one and direct portal edges are
  absent.  The graph remains connected through the strong-pair blades.
- Exact Bd and dB amplification tests reduce to sums of portal functions
  `Phi_B(B)` and `Phi_D(B)`.  Their pointwise sum is the negative of a
  four-term nonnegative polynomial divided by a positive denominator.
  Hence the two establishment tests cannot both be positive for any
  `r>1`.
- The proof uses a stopped finite-chain coupling: fixation is bounded above
  by the branching establishment law.  No independent-genealogy
  domination is used.
- Found an exact warning against a naive typewise extension: at `r=8/5`,
  portal loads `1/100` and `2` favor opposite rules at the special-mark
  tests.  A higher-rank incidence can assign those regimes to different
  blade types, so an additional global multitype argument is necessary.
- Numerical optimization retaining every portal subset found no positive
  simultaneous establishment gap for `Q<=3,T<=3` at `r=8/5`; the optimizer
  collapsed toward an effectively rank-one compromise.  This remains
  evidence only.
- `verify_rank_one_tradeoff.py`: all exact certificates and independent
  subset/count comparisons through `Q=6` pass.
- Broader arbitrary-network portal complement inequality recorded as OPEN.
- No literature search or external contact.

## 2026-08-02 11:09 PDT — independent hostile audit

- Re-derived every portal-episode, successful-child, parent-seeding, and
  parent-death rate from the atomic Bd and dB clocks, including both
  within-pair resolution probabilities.
- Checked the scalar reduction, uniform-initialization entrance factors, and
  the direction of both fixed-point sign tests.  The strictly negative sum of
  portal scores really forces one strict establishment deficit; the stopped
  cutoff then gives only the authorized fixation upper bound.
- Replaced the floating-point subset/count comparison inside the certificate
  with a full exact-rational solve of all `2^Q-1` labelled portal subsets.
  It agrees identically with the independent count recurrence for both rules
  and every `Q=2,...,6`; all symbolic and exact finite checks pass.
- **OPEN:** genuinely higher-rank blade incidence, direct portal networks in
  the nonexchangeable case, positive-proportion portals, and nonseparated
  architectures.  A separate higher-rank search is continuing.
