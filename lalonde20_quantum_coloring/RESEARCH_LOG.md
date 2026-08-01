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

## 2026-08-01T10:08:00-07:00 — fixed-color core rigidity

- Derived an exact rational four-square identity in the $3r$-dimensional
  fixed-color corner. Faithfulness of matrix trace forces all four factors to
  vanish.
- Walsh inversion yields the operator anticommutator system
  `A={B,C}`, `B={A,C}`, `C={A,B}`. Its support blocks are unitary and a
  block-diagonal gauge puts vertices 1 through 13 into the scalar sign-frame
  pattern tensored with an arbitrary multiplicity space.
- This replaces the inherited rank-one classification with a direct
  higher-rank theorem and makes no transversality assumption.

## 2026-08-01T10:19:00-07:00 — exhaustive tail classification

- Corrected an initially tempting but incomplete graph-of-an-operator
  parameterization. The exhaustive tail parameter is an arbitrary
  $J$-invariant $r$-plane $M\subset K\oplus K$.
- Recorded an explicit non-graph invariant plane at $r=2$, confirming that
  degenerate branches are real and must be retained.
- Reduced all six tail-tail edges to five identity pullbacks and one
  `-J` pullback.

## 2026-08-01T10:28:00-07:00 — exact obstruction and all-n theorem

- Same-vertex orthogonality between two colors forces a three-block skew
  overlap matrix. Exact compression by the six tail frames flips $M_c$ and
  $M_d^\perp$ in both directions.
- Splitting each invariant plane into the $+i$ and $-i$ sectors of $J$
  produces pairwise orthogonal physical sector spaces across colors.
- The two packing inequalities sum to `3nr <= 2nr`, excluding a quantum
  $n$-coloring of $G_{19}\vee K_{n-3}$ for every $n\ge3$.
- Combined with an explicit classical coloring, this proves
  `chi_q(G_19 join K_(n-3)) = n+1`; in particular, `chi_q(H)=5`.

## 2026-08-01T10:42:50-07:00 — independent hostile audits

- Independent agents rederived the SOS coefficients, Walsh signs, unitary
  core, exhaustive tail moduli, cross-color orientation, all six compression
  signs, and the final sector count. No mathematical gap was found.
- A separate exact standard-library verifier was built from different
  trace-SOS bookkeeping. It independently decodes graph6, enumerates the
  triangles, checks the noncommutative identities and clique-ideal witness,
  row-reduces the cross-color kernel, and replays the tail compressions.
- Numerical searches were retained only as exploratory source code. The
  theorem and certificates have no floating-point dependency.

## 2026-08-01T10:53:24-07:00 — publication and priority checkpoint

- Compiled and visually inspected the seven-page self-contained paper and an
  exactly two-page technical summary. Corrected all render defects found in
  the first pass and removed the temporary page images afterward.
- Both independent obstruction verifiers, the graph verifier, and both LaTeX
  builds pass from the clean project folder.
- Performed the narrow priority audit only after the exact result was fixed.
  The June 2026 Lalonde preprint states this full finite-dimensional equality
  as a conjecture; exact-checksum and exact-family searches found no later
  resolution. This is not treated as an exhaustive priority guarantee.
- No external communication was initiated. The next publication action, if
  desired, remains with the human author.

## 2026-08-01T12:15:25-07:00 — adversarial-review presentation revision

- Scrutinized seven post-proof presentation suggestions individually and
  recorded their disposition in `publication/reviewer_suggestion_audit.md`.
- Added named authorship and affiliation without inventing a public email;
  adopted a more precise title; cited the projector/strategy equivalence;
  expanded the tail-complement and final cross-color inner-product steps; and
  added foundational and `G_13` references.
- Renamed the joined family from the overloaded `G_n` to `J_n` inside this
  note, reserving `G_19` for the fixed base graph.
- Added an immutable pre-revision commit and both certificate hashes, plus an
  explicit AI-assistance and non-peer-review disclosure.
- Deliberately did not add a GitHub Action, following the author's instruction.
  No workflow files were changed and no individual was contacted.
- Replayed all three exact verifier commands. Both LaTeX documents compile;
  the eight-page paper and two-page summary were rendered page by page and
  visually inspected after correcting the only overfull hash lines.
