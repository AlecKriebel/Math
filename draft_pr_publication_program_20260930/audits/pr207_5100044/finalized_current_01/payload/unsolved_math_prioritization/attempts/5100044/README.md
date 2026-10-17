# Focal-inversion area products: attributed verification

For strictly nested nondegenerate confocal ellipses, signed orbit area times signed focal-inverse polygon area is constant when the **least collision period is N=4n**. This covers every admitted coprime winding, including stars, and either original focus. Unit-circle inversion acts on vertices; consecutive inverse vertices are joined by straight segments. The two focal inverse areas agree. Reversal preserves the product; r traversals of an admitted primitive cycle multiply it by r squared.

The original arXiv table does not explicitly impose least period. The stronger reading admitting arbitrary repeated lists of length 4n is false. The theorem and this limitation are already in [Ferudun's preprint](https://doi.org/10.5281/zenodo.23093706). The local/cyclic Jacobi and Landen mechanisms are classical. This is an attributed verification, with no theorem/method novelty, firstness, causal independence, simultaneity, or current-openness claim.

Read [PROOF.md](PROOF.md), [SOURCES.md](SOURCES.md), and the alternate [published telescoping verification note source](../../../draft_pr_publication_program_20260930/audits/pr207_5100044/publication_package_v1/focal_inversion_area.tex). Published verification note: [10.5281/zenodo.23428090](https://doi.org/10.5281/zenodo.23428090). The exact four-file deposit and tracker 'Math Puzzles'!A134:D134 were verified from actual service readbacks. Two new independent AI whole-package reviews were accepted by Root with no required repairs; this remains unrefereed and has no conventional human peer review or proof-assistant formalization. AI tools were used extensively; this work is unrefereed.

Install the pinned packages in [requirements.txt](requirements.txt), then run:

```text
python verify.py
python -O verify.py
python independent_review/independent_check.py
python -O independent_review/independent_check.py
```

The first program certifies finite exact identities; the second propagates Euclidean reflected rays and gives finite numerical diagnostics. Neither is a full analytic or interval certificate. Both use explicit runtime checks under optimization and default to JSON on stdout. Optional `--output NEW_FILE` refuses an existing destination.

[PUBLICATION_STATUS.md](PUBLICATION_STATUS.md) records the completed package reviews and verified publication. The ledger cells `claimed_solved`, `1/5` are preserved historical state, with model/effort and author-turn counts unverified. The original 20-file, 61,131-byte [submitted archive](../../../draft_pr_publication_program_20260930/audits/pr207_5100044/submitted_snapshot/) remains unchanged; current corrections and runs are dated 16 October 2026.
