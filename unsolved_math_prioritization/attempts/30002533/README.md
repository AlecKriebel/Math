# Problem 30002533: credited prior existential resolution

Rank 723 / OWR-12870-003. Disposition: **already_solved, 1/5 author approaches**.

The original 2014 existential question has a component-safe affirmative deduction from published work. Actual individual primitive Gothic Teichmüller components have rational normalized nonuniformizing Prym exponents outside `{1, 1/2, 1/3, 1/5, 1/7}`. A sequence converges to `3/13`; sufficiently late values lie in `(14/65, 16/65)`. A disconnected volume-weighted average does not establish this claim and is not used as an individual exponent.

Credit belongs to Möller–Torres-Teigell, *Euler characteristics of Gothic Teichmüller curves*, Geometry & Topology 24 (2020), 1149–1210, https://doi.org/10.2140/gt.2020.24.1149, together with the explicitly cited McMullen–Mukamel–Wright, Avila–Eskin–Möller, Eskin–Mirzakhani–Mohammadi, and Bonatti–Eskin–Wilkinson inputs. No novelty or independent human peer-review claim is made.

## Read in this order

1. `safe_freeze/PROOF.md`: original frozen deduction.
2. `independent_audit_corrected/AUDIT.md`: independent AI-assisted hypothesis-by-hypothesis audit, including immersed sheets, the rel-zero and symplecticity argument, invariant-subbundle/exterior-power continuity, and the common arithmetic cover.
3. `safe_freeze/SOURCE_SCOPE.md` and the public source-verification metadata: exact coverage and limitations.

The audit clarifies the original proof's connected-manifold shorthand through local sheets and irreducibility, and preserves the Prym label through invariant-subbundle/exterior-power continuity. These details are part of the accepted reading of the proof.

No named component-specific new fraction, attainment of `3/13`, effective threshold, fixed-surface result, or classification is established. The original Oberwolfach contribution was inspected. The live problem URL returned HTTP 403; the raw statement and AI-report corpora were unavailable. Their exact contents and hashes remain unverified.

## Frozen history and attribution correction

The original author packet is unchanged. Its pending-audit and not-yet-published fields describe the time of that freeze, not this package's current review state. The corrected audit passes the stated existential scope.

The superseded audit incorrectly described its review as human. The current audit explicitly identifies it as AI-assisted. `CORRECTION.diff` and `CORRECTION_RECEIPT.json` record the exact attribution and payload-count corrections; their removed text is historical, not a present attribution. No mathematics or test code changed. The superseded audit body is not redistributed here.

## Reproduce without sources

Run from this directory:

`python3 -B verify_publication.py --expected-manifest-sha256 SHA256_OF_PUBLICATION_MANIFEST`

The external publication digest is recorded in the PR description. The wrapper checks immutable author/audit bindings, the complete publication file set, 156 author arithmetic controls, 20 independent abstract controls, and eight source-free mutation controls. Success exits 0 with `PASS_PORTABLE_ARTIFACT_AND_SUPPLEMENTAL_CHECKS`; source verification remains `NOT_RUN_MISSING_SOURCES` and source retrieval/inspection is not replayed. This is not formal theorem verification.

The original source-complete validators intentionally exit 2 without sources:

`python3 -B safe_freeze/verify.py`

`python3 -B independent_audit_corrected/independent_checks.py --candidate-dir safe_freeze --mutations`

To replay exact PDF-byte checks privately, append `--sources-dir PATH_TO_SEPARATELY_OBTAINED_PDFS` to the independent command. The six public source records give filenames, URLs, sizes and SHA-256 hashes. Successful source-complete replay exits 0 and runs eleven mutation controls, including PDF corruption/missing/symlink controls. PDF hashes check identity, not mathematical truth. The source-complete publication replay succeeded with existing private copies; no new retrieval or scholarly inspection is claimed by that replay.

`python3 -B test_publication_integrity.py` runs disposable-copy publication-corruption tests. The same commands work with `-O`.

This package contains authored analysis/code and public verification metadata only. No PDFs, source extracts, screenshots, raw dataset records or private coordination files are included. The draft changes only this attempt directory and this problem's Status, Turns and previously blank Findings cells in `QUEUE.md`.
