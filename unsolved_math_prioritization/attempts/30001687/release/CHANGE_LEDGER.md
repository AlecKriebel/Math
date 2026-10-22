# Corrected-release change ledger

Disposition remains **unsolved, 5/5**. These are corrections and proof clarifications from the independent review, not a sixth proof-search route or a new spectral result. The weak-coupling claim remains Theta(1/lambda), without a limiting coefficient claim.

## Inputs preserved in full

- Initial author manifest: `2d657668c7f2b47f4429714e3e597baee441f32f58f262dc7bfb9d62dc5b4d8d`, preserved with every bound author file in `original_author/`.
- Original audit manifest: `c7ef85a28c07d72abc9e2fa2cbbba309d385b31077c58325a0fdcaa2e5350d08`, preserved with all seven bound audit files in `audit/original/`.
- Neither original directory was edited. Byte comparisons passed for every preserved file, including both original manifests.

## Exact author-file changes

1. `PROOF.md`
   - Makes the finite-gap collection nonempty (`m>=1`).
   - Explicitly requires a one-sided C1 extension of both hull endpoints and all gap endpoints, and gaps lying in the hull.
   - Gives the finite `2m*m!` ratio argument and explains the zero-gap exception.
   - Proves the blocker formula with correct handling of ties: candidate distances need not equal every individual bridge in a fixed tie order, but their infimum gives the thickness.
   - Adds a separately written proof of exact exhaustion by actual gaps of one fixed Cantor set with its exact hull. Does not identify numerical periodic covers with those fillers or assert uniform parameter control.
   - Includes the audit's one-gap nonuniformity control and states that its different sets are not truncations of one spectral family.
   - Requires a bijection of gaps and corresponding endpoints, inducing a bijection onto all presentations, in the sufficient comparison.
   - Explicitly labels the nine free-operator checks as floating-point rather than exact.
2. `README.md`
   - Separates exact controls from floating-point calibrations and spectral diagnostics.
   - Explains archive preservation, pending corrected-release binding review, and the two new manifests.
   - Supplies audit reproduction commands adapted to the archive layout; the original audit README remains unchanged.
3. `RESULT.json`
   - Refines the remaining gap to distinguish the proved generic true-gap identity from the unproved spectral identification and uniform coupling comparison.
   - Renames the nine-period calibration count to `floating_point_free_operator_periods`.
   - Records the original audit's conditional disposition, pending new binding review, source manifest hashes, and correction list.

`SOURCES.md`, `RESEARCH_LOG.md`, `compute_controls.py`, and `control_results.json` are byte-identical to the original author freeze. In particular, the historical research log and its original review-pending statement are preserved; this ledger and the current metadata record the later corrections. No numerical algorithm, numerical output, original source conclusion, or five-route count changed.

`CORRECTIONS.diff` is the exact unified diff of all changed author files. It contains no omitted author-file changes.

## Checks performed

- The current author script reproduced the frozen numerical JSON byte for byte.
- The original independent audit script, with its original manifest guard and explicitly supplied original-author directory, reproduced its frozen JSON byte for byte.
- Original and archived author/audit manifests verified successfully.
- These are replays of existing controls. They neither certify infinite-spectrum numerical values nor establish the conjecture.

## Hash reconciliation

- `README.md` (changed): original `ec045382930699d6b43f1a31a47a028d94c99a55499e2d42cb4721172b247523`; current `8bea50d68b833e2922d3d5fd4faa410f201d7aee4a65d8bb280fc3db9db375e8`.
- `PROOF.md` (changed): original `bf3c0cfec40939c76fcbabc421cd0c510a44dfaf5fe36d7302ed11fb7ed40cb1`; current `13118ab132d2b389f6b0879b73ac2f525039295d6d39b195d1210ae60b07cc3a`.
- `SOURCES.md` (unchanged): original `69b9e9ebf5ce67efc430f1e5eb85464850d60ef39c3cec26dea9f636502790b0`; current `69b9e9ebf5ce67efc430f1e5eb85464850d60ef39c3cec26dea9f636502790b0`.
- `RESEARCH_LOG.md` (unchanged): original `715f0e3be18fd7baa35b7c2423e3bed8c5a68e630cfbadb0aef4437ba12433d7`; current `715f0e3be18fd7baa35b7c2423e3bed8c5a68e630cfbadb0aef4437ba12433d7`.
- `RESULT.json` (changed): original `b536fe605daeaab3929c6a2fcc58385c3049d2b1c42d584dae6311d749715b7b`; current `dad5fa5c7c7902f7e0f76bf7d90e85dc27db2efaa7b9c41c340f5351ccad043a`.
- `compute_controls.py` (unchanged): original `82591a391943e7a3cefac63c80dea3ec805832c9e3d48f43b6cca0744704b3b5`; current `82591a391943e7a3cefac63c80dea3ec805832c9e3d48f43b6cca0744704b3b5`.
- `control_results.json` (unchanged): original `2a885270841fefd17cbd6c2a148cbcd0fd3d75a359552bf84845722a4b37a55e`; current `2a885270841fefd17cbd6c2a148cbcd0fd3d75a359552bf84845722a4b37a55e`.

The corrected seven-file author manifest is `AUTHOR_SHA256SUMS`. The full corrected-release manifest is `SHA256SUMS`; it covers the seven current author files, complete preserved author and audit archives, both change records, and release metadata. Its own digest is supplied separately for the binding review. Only authored research, audit, code, computed results, and integrity records are included. No source PDF, full-text extract, source screenshot, catalogue corpus, or private coordination inventory is included. No remote write has been performed.
