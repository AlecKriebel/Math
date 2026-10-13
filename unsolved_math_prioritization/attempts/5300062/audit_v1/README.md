# Independent audit packet for problem 5300062

Start with AUDIT.md. The original author freeze needs the three exact changes in
CORRECTIONS.md / REPORT_MANDATORY.patch. The mathematical claim remains a scoped
C-infinity interior partial result; the general problem remains UNSOLVED, 5/5.
This packet does not grant v2 acceptance before a revised freeze is checked.

Requirements: Python 3 and mpmath 1.3.0. No other third-party package is needed.

Run from any location:

    python -B verify.py --expected-manifest EXTERNALLY_RETAINED_SHA256

The expected digest is supplied in the independent audit receipt, outside this
packet. The verifier checks strict inventory and hashes and replays independent
controls to exact retained result bytes. Neither integrity nor finite numerical
controls constitute a formal proof.

Optional full-source revalidation:

    python -B code/source_checks.py --catalog CATALOG --problems PROBLEMS --research RESEARCH --dataset-manifest PINNED_MANIFEST --review REVIEWS_2 --attempt-tree ATTEMPTS_TREE --source-dir PDF_DIRECTORY

Those inputs are not redistributed. The program emits only hashes, byte counts,
match results, and scope information. Exact source checks are retained under
results/source_checks.json; source URLs and inspection limits are in
SOURCE_AUDIT.json.

Optional destructive-control replay, performed only in temporary copies:

    python -B code/integrity_controls.py --author AUTHOR_SAFE_DIRECTORY --audit AUDIT_SAFE_DIRECTORY

The archive excludes scholarly source bytes, extracts, page images, corpus
contents, raw repository snapshots and private coordination material. The
original author ZIP is separately identified in AUTHOR_BINDING.json and was
not altered. No remote writes were performed.
