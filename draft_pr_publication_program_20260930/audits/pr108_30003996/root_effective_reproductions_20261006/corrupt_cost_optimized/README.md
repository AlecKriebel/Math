# PR108 current audit diagnostics v1

The immutable submitted head and original receipts remain in the original
source-authentication archive. This version preserves the mathematical
reduction and adds explicit trivial yes/no endpoints and dense variable
relabeling. It replaces removable Python assertions in both author and old
independent checkers with explicit raising guards, adds verifier-body hashes
to receipts, and binds both checkers to this precise clarified proof.

Run `python3 verify.py` from this directory. Run
`python3 independent_review/independent_checks.py` from this directory for
the separate Prüfer/edge-cut suite. Both may also run with Python `-O`.
These finite diagnostics support the written proof; they do not establish
complexity hardness or novelty by enumeration. Fresh source/model and
arbitrary-tree families are separately preserved in the audit folder.

No novelty, present-open-status, preprint, DOI, merge or closure clearance
is provided by this repaired diagnostic snapshot. Original effort2/5 is
supported by QUEUE and the prose log; no historical structured ledger was
submitted. New central proof-search turns0.
