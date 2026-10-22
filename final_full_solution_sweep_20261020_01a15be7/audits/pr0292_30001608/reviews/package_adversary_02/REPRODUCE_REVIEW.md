# Reproduce the independent review evidence

Use ordinary Python 3.11 or newer without optimization. These commands run from
the `package_adversary_02` review folder; the independently extracted candidate
is in `extracted/dfc_stability_verification/`.

1. Check the sealed input files and review receipts:

       python3 verify_review.py

2. Replay the complete candidate suite in temporary copies inside this review
   directory (the directory `tmp/` already exists):

       TMPDIR="$PWD/tmp" PYTHONDONTWRITEBYTECODE=1 python3 extracted/dfc_stability_verification/reproduce.py

3. Recompute the new exact mathematical and protocol controls:

       PYTHONDONTWRITEBYTECODE=1 python3 independent_controls.py
       PYTHONDONTWRITEBYTECODE=1 python3 priority_controls.py

   Their JSON should equal `independent_controls.stdout.json` and
   `priority_controls.stdout.json`, respectively. They import no candidate
   program. Their finite checks supplement the separate all-state derivation.

4. Recompute the wrapper validity/negative fixtures:

       PYTHONDONTWRITEBYTECODE=1 python3 wrapper_controls.py

   This writes only the local fixture directory and
   `WRAPPER_MUTATION_RESULTS.json`. The receipt contains a fresh timestamp;
   successful behavior is one valid pass and five deliberate rejections.
   Rewriting a sealed receipt changes its hash, so run the seal check before
   rerunning this stage, or compare in a copy of the review directory.

The recorded source rebuild used the available digest-verified Tectonic 0.17.0
runtime with a private copy of its cached resources, `--only-cached`,
`--untrusted`, and output confined to `rebuild/`. `BUILD_RECHECK.json` records
the exact source hash, command and successful result. Fresh PDF bytes need not
match because build metadata can vary. `PDF_QA_RECHECK.json` records equal full
extracted text and equal PNG hashes for all six pages at 105 dpi; the supplied
and rebuilt render pairs are in `rendered/`.

`PACKAGE_READING_INVENTORY.json` records all 92 extraction files; the candidate
wrapper hashes the 91 payloads other than its own manifest. Original Git object
comparisons are recorded in `INTEGRITY_RECHECK.json`. The source-access receipts
for the new public reaction-network lead include the actual downloaded PDF hash
and its agreement with the public API checksum.

All third-party PDF/text bodies in `private_sources/` and their rendered pages
are private reading material. Do not redistribute them with a public review.
The seal records their identities separately, but default review verification
checks the authored evidence and candidate inputs without requiring private
source bodies. Use `python3 verify_review.py --include-private` for the local
private-reading identity check as well.

No command here publishes a result, edits Git, or contacts an individual.
