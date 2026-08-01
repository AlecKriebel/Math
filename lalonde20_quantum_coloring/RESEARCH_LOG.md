# Research log

## 2026-08-01T09:49:01-07:00 — initialization

- Created a dedicated worktree at `/Users/alec/Documents/Math-lalonde20`, based
  exactly on `origin/main` at commit `36b6e944`.  The ordinary `main` worktree
  was already heavily active and dirty, so using it would have risked
  disturbing unrelated research.  This worktree is detached only because Git
  forbids checking out `main` twice; publication checkpoints will be linear
  descendants of `origin/main` and pushed directly to `main` when safe.
- Created this dedicated problem folder.  All project artifacts will remain
  inside it.
- Recorded the exact graph and the required finite-dimensional projector
  formulation in the project README.
- Started three independent work streams: structural operator-algebra
  reductions, adversarial counterexample search, and exact trace/SOS or
  classification certificates.
- Hardware audit: Apple M1 Pro, 10 CPU cores, 16 GiB RAM.  The data volume has
  about 26 GiB free and is 95% occupied, so searches must avoid large moment
  matrices or uncontrolled checkpoint output.  More RAM would materially help
  high-degree NPA/SOS searches, but the first reductions will be kept small.
- Status: open.  Neither `chi_q(H)=4` nor `chi_q(H)=5` is asserted.

