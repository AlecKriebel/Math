# Verified publication and tracker status

Verified 2026-10-06T22:42:43-07:00.

The core mathematical target is resolved: the symmetric TSP polytope on N cities has exact real PSD matrix-order complexity 2^Theta(N). Specifically, for all sufficiently large N, it is at least 2^(cN) for some absolute c>0 and at most 2(N-1)+(N-1)(N-2)2^(N-3). The explicit lower transfer is 2^(2a floor(N/4)) from the audited matching exact-lift bound 2^(a n).

This is an explicitly attributed consequence of OpenAI family126's exponential matching theorem and Yannakakis's established reduction, with explicit exact-slack, 2n-city contraction, all-N padding and subset-flow details. It is not a new lower-bound method, independent proof of the matching conjecture or firstness claim. No approximate/hierarchy/complex-PSD conclusion is asserted. The exponential input and follow-on theorem are not claimed Lean-verified; source mathematical audits and finite falsification checks are documented. No conventional human peer review has occurred; AI tools were used extensively.

## Exact reviewed release

The standalone manuscript main.tex and actual six-page publication/paper.pdf compile/reproduce and were visually checked. Two distinct complete-package adversarial reviewers examined candidate-v1 and the repaired candidate-v2; the fresh second review found no substantive issue. The only first-round repair clarified the README's repository/download contents map. Exact reviewed archive and member hashes are in receipts/frozen_candidate_v2.json. Reviews and responses are retained in reviews/; complete-package reviews are outside the immutable upload archives to avoid recursive checksums. Frozen archives remain unchanged; later operational status and receipts are outside that payload.

- [Production Zenodo record](https://zenodo.org/records/23204250)
- [DOI: 10.5281/zenodo.23204250](https://doi.org/10.5281/zenodo.23204250) — HTTP200 resolves to the verified record.
- [Paper PDF](https://zenodo.org/api/records/23204250/files/paper.pdf/content)
- [Standalone source](https://zenodo.org/api/records/23204250/files/tsp-source.zip/content)
- [Verification and reproduction archive](https://zenodo.org/api/records/23204250/files/tsp-verification.zip/content)

The repository deposit tool confirmed submitted/public record23204250, complete metadata and exact intended three-file set/checksums. Independent public API/download verification checked all three SHA256/MD5 values and byte sizes against the frozen reviewed payload. Only Zenodo's accepted omitted-author-affiliation-to-null normalization occurred; no invented affiliation was supplied. Manifest: zenodo-deposit.json. Receipt: receipts/zenodo_inspect_published.json. Public download checks: receipts/public_record_download_verification.json. No GitHub release or duplicate upload pathway was used.

## Tracker

[Spreadsheet target row](https://docs.google.com/spreadsheets/d/1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20/edit?gid=1254632077#gid=1254632077&range=A46:D46). Numeric tab1254632077 resolves to Math Puzzles. Current headers: Original Problem, Solution Chat URL, DOI, Notes. Appended exactly one RAW/INSERT_ROWS row at 'Math Puzzles'!A46:D46 after checking for the exact DOI, depositID and title. Unknown optional chat URL remains blank. Read-back values exactly equal the submitted row; subsequent whole-tab search found matching DOI/depositID only in row46. Receipt: receipts/tracker_verification.json. Raw unrelated tracker metadata and rows stay only in ignored local work/tracker_inspection.

## Checkpoint

Mathematical resolution estimate:100%. Publication/tracker package estimate:100%, with final owned-file repository push being completed. No remaining mathematical, publication, DOI-resolution or tracker action is pending. Future conventional human review and any later upstream correction are outside the completed task; a later correction would require a new explicit reconciliation rather than silently changing the pinned release.
