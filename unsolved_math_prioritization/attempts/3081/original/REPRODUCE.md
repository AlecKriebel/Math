# Reproduction scope

1. Extract the safe ZIP into a new directory, without adding files to it.
2. Run `python3 -B checker.py` and `python3 -B -O checker.py` from any working directory, addressing the script by its absolute path if necessary.
3. Run `python3 -B self_test.py`. It uses fresh temporary copies outside the package and tests both interpreter modes.
4. To verify the private complete corpora, supply their local files explicitly:

    python3 -B checker.py --catalog /path/to/catalog.json --problems /path/to/problems.json --reports /path/to/research_results.json

All three inputs are required together. The verifier checks complete-file byte counts/hashes, exact unique ID 3081 records, problem-number agreement, catalog rank 926, report absence, and the unprojected pair serialization. It prints only verification status and public hashes, never records. Private inputs are not required for geometry checks.

To reverify source bytes already downloaded with authorization, use `--source-dir /path/to/source-files`; filenames must be the metadata names. This hashes inputs, without copying, uploading, or printing their text. Live content may change; a mismatch establishes different bytes, not that the original inspection was false.

The mathematical checker enumerates all triangles of the eight-point balanced certificate, tests all 256 colorings for the known discrepancy and almost-empty bounds, tests the parametric blocker examples for k = 1 through 15, and verifies the exact thinning identity across all 256 point subsets. These finite tests supplement, and do not replace, the written all-k proof.

Tamper tests include an altered member, missing member, unexpected member, a re-sealed false interior-point certificate, and a re-sealed duplicate-point/degenerate geometry certificate. Re-sealing updates the internal manifest so the last two tests must fail on mathematical validation. This is not protection against an adversary rewriting both proof and checker; the external ZIP hash and independent audit establish the trust boundary.
