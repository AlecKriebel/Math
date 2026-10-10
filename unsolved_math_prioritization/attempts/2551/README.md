# KOU-21.42 / 2551: credited prior-literature consequence

Every three-generated torsion-free nilpotent group of class three is self-similar. The existence question therefore has a negative answer, credited to the earlier positive-grading theorem of Dekimpe, Igodt and Pouseele (2003), with the explicit later Dekimpe–Deré restatement and Cornulier rational descent checked. The direct arbitrary-lattice contraction-to-faithful-tree bridge received an independent AI-assisted audit, **PASS**.

The original 2003 proof was unavailable and remains an imported theorem. No independent audit of that proof, novelty, human peer review, or editorial acceptance is claimed. The inspected October 2026 Notebook leaves 21.42 unmarked. The finite exact controls test the example and proof pitfalls, not the universal grading theorem.

## Contents and immutable history

- `author/`: the unchanged eight-file author freeze
- `audit/`: the unchanged eight-file independent audit
- `freezes/`: both original frozen ZIPs, unchanged
- `PUBLICATION_STATUS.json`: current qualified disposition, `already_solved`, 1/5
- `QUEUE_PATCH.json`: exact three-cell queue change and full-file hash pins
- `REPOSITORY_CHECKS.json`: fresh-main and targeted duplicate checks
- `PUBLICATION_MANIFEST.json`, `verify_publication.py`: recursive integrity and replay

Historical author statements saying an independent audit is pending are intentionally preserved in the immutable author freeze. The separate audit and current status record the later PASS. See `author/RESULT.md` and `audit/AUDIT_REPORT.md` for the proof, attribution, and limits.

## Portable normal-mode replay

Use Python 3 with its standard library, without `-O`. From any working directory:

    python3 /path/to/2551/verify_publication.py /path/to/2551 EXPECTED_MANIFEST_SHA256 --queue /path/to/QUEUE.md

Obtain the expected manifest SHA-256 from the draft PR description. The verifier checks every package file and directory, both inner manifests, both ZIPs and every ZIP member, the exact queue restoration, and normal-mode author/audit controls. Omitting `--queue` explicitly leaves queue verification untested. It runs 4,455 author controls, 6,567 independent controls, and five author-freeze mutation controls. Integrity replay is not a formal mathematical proof or a substitute for the imported literature inputs.

Scholarly PDFs, extracts, rendered pages, dataset contents, and private coordination material are excluded. Public source titles/URLs, hashes/sizes, inspection history, and match results are retained. The standalone audit verifier supports optional caller-supplied evidence; those external sources are not downloaded by this package and are not rechecked by portable replay.
