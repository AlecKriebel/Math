# Independent priority-review packet

REPORT.md contains the scope and bounded conclusion. SOURCE_FIRST_BASELINE.md
was sealed before candidate access; BASELINE_SEAL.json fixes its timestamp and
hash. CANDIDATE_BINDING.json records the immutable PR359 head and all38 file
identities. SOURCE_QUERY_LEDGER.json identifies audited sources and queries.

Public analytical files are bound by PUBLIC_MANIFEST.json. PRIVATE_MANIFEST.json
binds local complete source payloads, raw connector returns, process stdout and
stderr, receipts and source-page renders. Those raw source materials stay private.
CLOSURE.json binds both manifests. This is a local review package, not a public
release or a DOI snapshot.

From a relocated intact namespace, run:

    python3 -B verify_namespace.py

The verifier uses only standard-library reads and hashes. It performs no writes,
downloads, local-module imports, replayed commands or source execution. Full mode
requires the private layer; --public-only explicitly leaves private bytes unchecked.
The closure hash reported by the verifier can be compared with the external final
review receipt. No file in a closed namespace may subsequently be changed.

For the independent limited algebra checks, run:

    python3 -B check_priority_claims.py

Passing hashes and exact algebra do not establish the whole mathematical proof,
literature completeness, universal novelty, or human peer review.
