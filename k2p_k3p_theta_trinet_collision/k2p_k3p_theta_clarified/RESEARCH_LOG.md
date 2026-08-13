# Research log

## 2026-08-13 07:00 PDT

- Confirmed that the focused displayed-tree verifier did not itself perform the five-coordinate Lemma 4.1 convention check described in the clarification note; that check had existed only in the complete suite's separate source-convention step.
- Audited an exact rational proposed check against the source paper's five displayed formulas and the existing convention checker.
- Embedded the check in the focused verifier, replayed the focused and complete exact suites successfully, and refreshed the author-facing audit package.

## 2026-08-12 20:36 PDT

- Created this dedicated clarification directory from the latest public `main` snapshot without overwriting the pre-clarification paper, summary, certificates, or original verifier modules.
- Confirmed the repository is public and located the earlier combined package at commit `ca21a733`.
- Replayed the untouched compact and complete exact verifier suites successfully before editing.
- Confirmed that the figure already assigns `S` to both `p`-arcs and `T` to both `q`-arcs; the defect is textual underspecification and compact-verifier coverage.
- Implemented an exact graph-derived displayed-tree verifier in `Q(sqrt(71))`.
- Verified the four retained-parent monomials, common `K` factor, all sixteen core identities, exact transition matrices, all 64 Fourier coordinates, and all 64 direct-pruning probabilities.
- Added the clarified paper, two-page summary, and compact clarification note; no mathematical witness or conclusion was altered.
