# Research log: tractable open Erdős problems for AI

## 2026-07-24T15:31:20-07:00 — project opened

- Goal: identify and rank ten currently open Erdős problems that are unusually
  tractable for independent AI-led attacks.
- Explicit exclusion: Erdős Problem #84.
- Scope boundary: candidate identification and verification only; do not attempt
  to solve any selected problem.
- Selection priorities: current open status, self-contained statement, low
  prerequisite burden, a crisp success criterion, and plausible elementary or
  finite/computational lines of attack. Prestige and prize value are not
  selection criteria.
- Repository note: the default checkout contained unrelated work, so this
  effort is isolated in the existing `main` worktree.
- Checkpoint estimate: 5% complete.

## 2026-07-24T15:41:00-07:00 — database-wide first pass

- Checked the current `teorth/erdosproblems` database snapshot at commit
  `1fddae4643fac0308db2e557876b78072e30f2e1` (2026-07-23): 1,217 indexed
  problems, including 609 marked open, 9 decidable, 27 falsifiable, and 7
  verifiable.
- Cached the live pages for all database-open problems and separately screened
  every finite-status problem. The finite labels describe certificate type,
  not practical search size.
- Split independent screens across decidable problems, finite-witness problems,
  and quiet ordinary-open problems. No proof search was performed.
- Checkpoint estimate: 35% complete.

## 2026-07-24T15:49:00-07:00 — freshness and competition audit

- Removed #1199: arXiv:2607.17333, first submitted 2026-07-19 and revised
  2026-07-23, states a full affirmative solution while the database still
  labels the problem open.
- Removed #475 despite its intrinsic finite-field tractability because a public
  GPT-5.5 proof-candidate/certificate package appeared in May 2026.
- Downgraded several otherwise attractive targets after finding recent public
  work: #23 has a June 2026 computer-assisted preprint through the first 40
  multiples of five; #273 has an active July exact-cover search; #864 has fresh
  exact data and a newly seeded agent task; #1212 has a July 21 Lean/AI partial.
- Retained quiet seeded tasks only when no investigator or proof claim is
  visible; a public problem listing alone is not treated as an active race.
- Checkpoint estimate: 70% complete.

## 2026-07-24T15:53:02-07:00 — finalist merge

- The strongest finalist types are now: finite counterexample or construction
  certificates (#106, #7, #128); focused construction problems with one known
  gap (#156, #197); and narrowly residual structural problems (#944, #1016,
  #624).
- Final ranking still awaits two skeptical screens of quiet graph/number-theory
  candidates and a comparison of #944, #123, and #778 against the bottom tier.
- Checkpoint estimate: 82% complete.

## 2026-07-24T15:57:54-07:00 — shortlist fixed

- Fixed the ranked ten as #106, #7, #197, #156, #128, #864, #1016, #624,
  #273, and #19. Problem #944 is the first alternate.
- The last freshness audit removed #123 after confirming that the live page
  now records a July 2026 accepted Lean proof. It also downgraded #944 because
  a June 2026 paper is actively attacking its first open subcase.
- Wrote `SHORTLIST.md` with the exact completion criterion, tractability
  rationale, and first-mover warning for every selection. The document states
  explicitly that relative tractability is not a promise of solvability.
- Checkpoint estimate: 95% complete.

## 2026-07-24T15:59:00-07:00 — verification complete

- Re-read the final shortlist for statement fidelity and ensured that it
  contains identification and dispatch criteria only, not attempted proofs.
- Checked every web citation in `SHORTLIST.md`; all 16 distinct targets
  returned HTTP 200.
- Confirmed that the ignored source cache will not be committed and that all
  persistent files are confined to this effort's dedicated folder.
- Checkpoint estimate: 100% complete.
