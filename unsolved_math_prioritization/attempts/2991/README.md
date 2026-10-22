# Kirby Problem 4.115: accepted part (a), unresolved part (b)

Target 2991, rank 1053. Combined disposition: **unsolved, 5/5 approaches**.

Start with `ACCEPTANCE.md`. The construction answers part (a): diffeomorphic but non-isotopic minimal balanced (3,1) trisections on the untwisted spin of L(8,3), even allowing sector permutations. Its fundamental group is C8. It does not answer the simply connected/non-diffeomorphic part (b), and no novelty claim is made.

## Contents

- `evidence/candidate/`: exact original nine-file freeze, including the complete proof, full report and first independent audit.
- `evidence/prior_review/`: exact later second independent part-(a) audit.
- `evidence/AUDIT_REPORT.md`: complete five-approach mathematical acceptance.
- `evidence/SOURCE_REVIEW.md`, `VERIFICATION_METADATA.json`, `receipts/`, `audit_exact.py`, `verify_envelope.py` and `PUBLICATION_ENVELOPE.json`: exact original full-bundle audit evidence.
- `source_free_audit.tar.gz`: exact original audit archive; its 20 files and four directories are compared in memory with `evidence/` without extraction.
- `BOOTSTRAP.py`, `verify_publication.py`, `mutation_tests.py` and `PUBLICATION_MANIFEST.json`: the authored publication verification layer.

Historical candidate wording is retained unchanged and reconciled by the later acceptance. The first review remains inside the original freeze, and the second remains outside it.

## Trusted replay

Obtain the expected BOOTSTRAP.py SHA-256 from the separately reviewed draft PR or commit verification receipt, and compare it before running that file. A hash computed only from the same untrusted packet is not an external trust anchor. The authenticated bootstrap pins the exact manifest and verifier. The manifest binds the payload; its external bootstrap pin completes the binding of every delivered file.

Run as actual UID/EUID 1000, with a working Python standard library:

    python -I -S -B /absolute/path/to/packet/BOOTSTRAP.py /absolute/path/to/packet
    python -I -S -B -O /absolute/path/to/packet/BOOTSTRAP.py /absolute/path/to/packet
    python -I -S -B -OO /absolute/path/to/packet/BOOTSTRAP.py /absolute/path/to/packet

The wrapper never modifies the supplied packet. It materializes authenticated evidence in a disposable external directory, freezes inputs to 0444/0555, checks real denied writes and runs the independent harness from a read-only working directory. The harness writes only to its explicit empty external output directory. Only disposable copies are thawed for cleanup. A Git checkout need not preserve read-only permission bits.

Run the publication trust-boundary controls with the same isolation flags and optimization modes:

    python -I -S -B /absolute/path/to/packet/mutation_tests.py --root /absolute/path/to/packet --bootstrap-sha256 EXPECTED_EXTERNAL_SHA256

The controls authenticate the bootstrap before loading the verifier, reject malformed manifests and substituted evidence, and replay a read-only relocation with a hostile Python import environment. Negative controls are created only in disposable copies.

## Interpretation

Each independent harness run contains 72 native calls and 16 whole-candidate integrity rejections. Three native calls intentionally accept a changed report to demonstrate that the original checker binds only the proof. These are scope probes, never integrity passes. The outer envelope binds the report and every other file.

Complete historical receipt comparison excludes only absolute-path-dependent traceback byte counts; each fresh count must equal its actual stream length. Source and corpus checks are explicitly NOT_RUN in this portable replay. Existing historical source/corpus metadata is not a fresh download or source inspection, a machine proof of geometric theorems, or a novelty finding.

No primary-source bodies, dataset bodies or private coordination material are included. No queue changes, publication, merge, release or external communication is performed by the verification code.
