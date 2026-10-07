# Research log

## 2026-10-07T04:24:22.228310+00:00 — checkpoint 01: scope and pinned input

Created dedicated project; no same-target folder existed. Read project AGENTS.md, upstream README, local triage and original prime-field theorem. Upstream clone remains read-only at adc7f1241b42e322a6451854ab7e4b4c146bf78a; source files copied under ignored sources/pinned, hashes recorded. Checked current remote head without changing pinned input. Existing shared checkout/index contain extensive unrelated research; they will be preserved, and publication commits will use an isolated index based on remote main. No PR queue consulted or processed.

Five independent internal agents audit prime-field proof, analytic dependencies, extension reduction, construction reduction and feasible implementation. Internal agents are research tools, not external individuals. No external communication occurred.

Strongest verified finding: the main prime-field theorem expressly relies on companion Hecke zero-free Theorem1.2; claimed fixed exponent alone is not certification. Classical extension/construction routes currently conditional. Mathematical resolution estimate 5%; publication package estimate 2%. These are estimates, not evidence. No Zenodo deposit or tracker mutation is authorized until the specified validation conditions are met.

## 2026-10-07T04:29:38.017549+00:00 — checkpoint 02: conditional reductions and adversarial evidence

Independently derived two general-field reductions: q-Frobenius fixed algebra followed by all m trace coordinates; and direct p-Frobenius fixed algebra over an nm-dimensional F_p space. For squarefree degree n, trace version makes at most mn prime calls of degree<=n; direct version at most n. Full squarefree decomposition and inverse coefficient p-Frobenius are explicit. Construction audit proved Shoup variants with oracle degree<=N², N=md; the md-then-factor lift was already published by Rai (2024), and Shoup already gives arbitrary-base construction. No new machinery or independent base breakthrough is claimed. A false blanket nonsquare-to-2^e-binomial rule over F3 was preserved and repaired in the construction audit.

Root independently ran reference tests: 7 families passed, including 377 exhaustive small monic inputs, characteristic two repeated/inseparable examples, m=1, constants/zero and corrupt oracle rejection. Also reproduced seven auxiliary-table examples and numerical finite Gauss/Euler checks plus exact exponent margins. These finite computations do not prove the analytic theorem or certify the prime-field core. No concrete falsification of family142 has emerged; independent analytic audit is still determining its precise remaining proof-validation scope.

Strongest verified result: conditional deterministic polynomial-time complete-factorization and construction reductions, with exact representation and oracle accounting. Mathematical resolution estimate 35%; publication package estimate 8%. Publication remains gated by pivotal dependency and priority validation, not by estimates. No deposit or tracker write occurred.
