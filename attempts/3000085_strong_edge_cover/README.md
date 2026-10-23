# Frozen audit: strongly minimal edge covers

Row 1905, ID 3000085. Disposition: already_solved; one audited disposition turn.
This is an original authored audit/exposition of Dominic van der Zypen’s existing 2022 counterexample, not a new manuscript or new theorem claim. See MATHEMATICAL_AUDIT.md for the complete credited proof and citations. The three reviewed mathematical reports are preserved byte-for-byte.

The later published 3-uniform result is cited only at statement level and is not independently audited here. The 1992 original full text and historical Egres wiki were not inspected. SOURCE_METADATA.json records prior retrieval/inspection history and hashes, not a new retrieval. No third-party source documents or extracts, datasets, private paths, or private coordination are included.

## Reproduction

Run `python3 -B validate.py` and `python3 -O -B validate.py` from this directory. Both check the exact file inventory, hashes and sizes, transformation provenance, and rerun the finite regression in an isolated temporary directory with byte-exact stdout, stderr, and result comparison. Run `python3 -B mutation_tests.py` or its `-O` variant for adversarial controls. No network is needed; regression execution installs a Python audit hook rejecting socket events, and the hook is tested by a synthetic audit event, without creating a socket. This is a reproducibility safeguard, not an OS security sandbox for hostile code.

The regression covers 65,812 families and 64,824 covers: 64,764 deletion witnesses, 56 merge-witness covers, and four finite singleton exceptions. This is finite bookkeeping, NOT verification of the infinite theorem.

## Checker-only hardening addendum

The retained INDEPENDENT_REVIEW.md describes the earlier checker’s intentional refusal under -O. That historical statement remains accurate for regression.original.txt, not the hardened regression.py. The only checker changes replace all seven assertions with explicit conditional AssertionError raises and remove that refusal guard. CHECKER_TRANSFORMATION.json and transformation_check.py certify the entire module AST matches exactly this transformation; the main routine and output generation are unchanged. Normal and optimized execution now genuinely run all checks. The original checker is retained as an authored-code text snapshot, not executed as the package validator.

MANIFEST.json inventories every payload file except itself. The external frozen receipt authenticates the manifest and ZIP, avoiding a self-hash cycle. Hash validation does not establish mathematical correctness or protect against an attacker replacing both package and external receipt. No publication or queue edits were performed during packaging.

## Manifest symlink preflight correction

An independent package inspection found that the first validator read MANIFEST.json before rejecting nonregular directory entries. The corrected validator performs lstat checks on every root entry, including the manifest, before reading any file content. Controlled tests point the manifest symlink at a harmless temporary JSON file and instrument both pathlib content-read methods: normal and optimized validation reject it with zero manifest content reads. No sensitive target or real socket is used. These checks assume a quiescent package directory; they do not claim race-resistant protection against concurrent filesystem replacement. The mathematical files and checker transformation are unchanged.
