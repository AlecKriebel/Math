# 5300088: audited convex-core ball-radius research

**Current disposition: unsolved after five substantive routes.** The complete independent adversarial audit accepts the packet as partial research, with no blocking mathematical correction. `RELEASE_CLARIFICATIONS.md` incorporates its two nonblocking clarifications. The frozen author's pending-audit fields describe its original stage; the separate completed audit supplies the current review outcome.

## What is established

The report separates the actual wholly-contained-ball question from global minimum injectivity and pointwise injectivity at a core point. An explicit rank-two screw-Schottky family has full-dimensional cores and interior points with injectivity log(q) but depth at most log((q+1)/(q-1)). It refutes only the stronger pointwise assertion. The report also gives necessary degeneration/escape conditions for potential counterexamples and explains exact gaps in five approaches. No general rank-only bound, full counterexample, novelty, or priority is claimed.

## Read and reproduce

- `submission/PARTIAL.md`: five routes and retained proofs
- `submission/SOURCE_GATE.md`: exact source and theorem hypotheses
- `independent-audit/AUDIT.md`: complete independent mathematical audit
- `RELEASE_CLARIFICATIONS.md`: current empty-core and minimum-bound wording

From this directory:

    python3 -B submission/verify.py
    python3 -B -O submission/verify.py
    python3 -B independent-audit/independent_verify.py
    python3 -B -O independent-audit/independent_verify.py
    python3 -B independent-audit/verify_audit_manifest.py
    python3 -B verify_publication.py

The author controls pass 7,801 assertions; the independent suite passes 55,357 checks. Normal and optimized outputs match their preserved receipts exactly. Finite checks supplement the all-words geometric proof and do not solve the target or re-prove every cited paper. The strict publication manifest rejects altered, missing, extra, and symlinked files; the release preparation separately tested these failure cases.

All 12 frozen author files and all 12 independent-audit files are unchanged. The author manifest SHA-256 is 166b1c2642947993cefe9212ba2d523438168a0ce58372731b1a850cc2021945. The publication manifest binds every distributed file except itself, and the audit manifest independently binds both frozen packets.

## Repository scope and limits

Only this problem's queue Status and Turns change to unsolved and 5/5. Its Findings field, every other row, existing header and links remain unchanged. All other changes are confined to this problem's directory.

This is an AI-assisted unrefereed research record, independently audited by AI. It is not human peer review, formal proof-assistant certification, or certification of an exhaustive literature search. Public verification metadata and bibliographic links are included; third-party PDFs, extracted source text, source screenshots, datasets, and private coordination files are excluded. No merge, release, DOI, or external outreach is requested.
