# Gradient-constrained Ginzburg–Landau minimizers: accepted partial report

Problem 30005994 / OWR-14298587-009, queue rank 959. **UNSOLVED, 5/5 substantive approaches.**

Read [the complete author report](author/REPORT.md) and [the independent acceptance](audit/ACCEPTANCE.md). The original general C¹ convex-potential question is not resolved. The accepted partial results are the large-parameter range, the zero-angular-mean competitor class, and a supporting-quadratic corollary conditional on a credited recent theorem. Exact negative witnesses obstruct two proposed proof extensions; they are not counterexamples to the minimization problem.

The published N≥4 gradient theorem uses C² convex potentials; the original OWR statement uses C¹. This regularity distinction is not silently removed. [Ignat–Nguyen, arXiv:2609.35398v1](https://arxiv.org/html/2609.35398v1) gives full-H¹ uniqueness for every N≥2 for the standard quartic potential only. Its recorded status at the 7 October 2026 review is a preprint; the complete paper proof is not independently certified here. [Chen–Liu–Wei–Yang](https://arxiv.org/html/2608.15957v1) is credited for the planar precursor. Neither theorem settles arbitrary convex W in N=2,3. No novelty, priority, human peer-review, or proof-assistant claim is made.

## Reproduce from any working directory

Python 3 and SymPy 1.14.0 are needed for the author's exact replay. The independent algebra uses only the standard library. Retain the SHA-256 of PUBLIC_MANIFEST.json from the draft PR as an external anchor, then run:

```sh
python -I -B /path/to/packet/verify_publication.py --manifest-sha256 RETAINED_SHA256
python -I -B -O /path/to/packet/verify_publication.py --manifest-sha256 RETAINED_SHA256
python -I -B /path/to/packet/mutation_tests.py --manifest-sha256 RETAINED_SHA256
```

The wrapper checks exact recursive membership, regular files, original manifests and frozen archives, and archive-to-directory byte equality. It runs the strict audit gate and its 19 controls in both normal and optimized modes; each gate replays the 43 author and 43 independent exact checks in both modes. These checks support the recorded algebra and integrity, not the analytic proofs by themselves.

The original author's verify_packet.py ignores extra directories and can follow same-byte symlinks. The actual original packet has exactly seven regular top-level files and no such entries. All original author and audit bytes are preserved, including historical pending-review wording. The separate acceptance and strict wrapper supply the completed review and exclusion checks. No mathematical correction was needed.

## Frozen objects and publication scope

- AUTHOR_FREEZE.zip: 14,746 bytes, SHA-256 2257767b04521b39bc59ccd62bfc03321d0ec87d81532b35d09d0d98bc263670
- AUDIT_FREEZE.zip: 21,275 bytes, SHA-256 ee4c85b685e93ca46baa8008514dfb124ce6ad80f37d8b18f791c4c5a66a539a
- author/REPORT.md: 15,531 bytes, SHA-256 5a69336298d8a448f4614bed8e0fc291b0d9622afbd8ad86b2b2bb775bd445f5

Only authored mathematical analysis, audit, verifier code, and public-source verification metadata are included. Source PDFs, copied source text or images, dataset contents, private source records, and coordination files are excluded. Dataset/PDF hashes in the frozen metadata record earlier local inspections; this publication does not freshly retrieve those source bytes or certify exhaustive literature/history coverage. Hash manifests are integrity aids, not signatures.

## Publication checkpoint, 7 October 2026 UTC

Five completed mathematical approaches and their precise remaining gaps are preserved in Sections 3–7 of the report. The independent review accepts those scoped conclusions without mathematical changes. Estimated completion: 100% of the bounded five-approach report and audit; no full-target resolution established. This checkpoint adds a portable exclusion/replay gate and mutation controls, and changes only the selected queue row's Status, Turns, and Findings. It does not reopen proof search or add substantive attempt turns.
