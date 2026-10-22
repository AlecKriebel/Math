# Independent contact-process partial-result audit

Problem 30004594 / OWR-4990373-008, rank 780.

Verdict: **PASS_RETAINED_PARTIALS_FULL_AUDIT**. Original problem: **UNSOLVED, 5/5**. No mandatory mathematical correction. No novelty, formal-verification, human-peer-review or external-acceptance claim.

Read FULL_AUDIT.md for the complete analytic review and CORRECTIONS.md for publication qualifications. The frozen author package was not modified.

## Portable finite replay

Python 3.10 or later, standard library only:

    python audit_math.py --output replay.json --author-results author_replay.json
    cmp replay.json independent_math_results.json
    python verify_audit_manifest.py

The replay has 875,433 exact assertions, including 343,400 internal Bareiss exact-division assertions. It builds and solves the finite chain independently of the author implementation and checks all 511 unreduced equations. It does not prove infinite-volume threshold separation. Run in a temporary copy if you want to keep this directory identical to its frozen manifest.

author_replay.json is the author's 72,940-control output, reproduced byte-for-byte by executing the original frozen verifier. The frozen author's code must be supplied separately to repeat that replay.

## Provenance replay with separately supplied inputs

audit_provenance.py verifies the exact author ZIP, manifest and files; complete corpus files; catalog; pinned public repository responses; and stored scholarly PDFs. The inputs are intentionally excluded from this safe audit package. The required arguments are listed by:

    python audit_provenance.py --help

The remote-evidence directory must contain the public responses named manifest_remote.json, queue_remote.py, root_remote.json, commit_remote.json, prior_prs_remote.json and prior_commits_remote.json. The original author directory supplies its source PDFs and complete recorded prioritization tree. These are read-only inputs. Corpus, source and repository inspection conclusions are recorded as hashes, byte counts, identifiers and match results, without copied source text or dataset records.

source_retrieval_audit.json documents fresh public-source checks and the timestamp-dependent supplementary PDF bytes. provenance_results.json records complete-file verification and the successfully recalculated descriptor review hash. AUDIT_STATUS.json records the later reviewed disposition.

This archive contains only authored audit prose and code, exact finite-control outputs and public verification metadata. It excludes PDFs, extracts, images, raw corpora and coordination records. No remote writes were performed.
