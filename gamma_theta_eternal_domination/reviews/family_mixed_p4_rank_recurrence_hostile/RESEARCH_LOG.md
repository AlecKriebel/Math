# Research log: hostile family mixed-\(P_4\) rank-recurrence audit

Date: 2026-07-28 PDT

- Bound the review to frozen commit
  `0017e89b00d7d8314cec5d4f3e5cd6358ea6f4a4`.
- Read the complete candidate note, manifest, observed results, and research
  log.
- Reconstructed accepted C-058, C-064, C-070, C-108, C-145, C-146,
  C-148, and C-151 at the exact scopes used, together with their hostile
  reviews.
- Checked the synchronous rank convention at \(h=1\) and at arbitrary
  positive finite rank.
- Reconstructed the single-hit collision exclusions, exact ridge list
  transport, C-146 star comparison, C-151 one-defect terminal, every named
  target, all eight fresh multi-hit cells, all C-145 directions, and the
  completion-clique alternative.
- Found no substantive mathematical flaw.
- Found two missing dependency bindings and one citation-scope ambiguity:
  C-064 is required for the exchanged-role step, C-058 is used by
  arbitrary-state restoration, and the rank-zero terminal should cite
  C-151 Lemma 1.1 explicitly.
- Wrote and ran a clean-room symbolic bookkeeping checker.  It returned
  `PASS_BOOKKEEPING_ONLY`.
- Replayed all three C-148 local-kernel checkers, the C-146 rank controls,
  and the discovery-only order-\(7\) through order-\(11\) SAT runs.
- Left all candidate files untouched.
- Final frozen-package verdict:
  `FAIL_PENDING_NONSUBSTANTIVE_PROOF_BINDING_CORRECTIONS`.
