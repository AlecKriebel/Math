# Initial surreal set-model partial results

Problem 30003322 / OWR-15181-014, rank 664. **Unsolved, 5/5.**

Start with [the controlling release addendum](RELEASE_ADDENDUM.md), then read [the complete authored results](author/RESULTS.md) and [the independent mathematical audit](audit/AUDIT.md). All C1–C4 clarifications and the stronger nonsaturation limitation are binding for this draft. Both universal set-model converses remain unresolved; no novelty or independence conclusion is claimed.

The `author/` and `audit/` directories preserve every frozen byte. Historical audit-pending/exhausted/no-remote-write language remains archival; the addendum states the current interpretation. `PUBLICATION_PROVENANCE.json` records current repository gates and independently replayed public-dataset hashes without redistributing the corpus or source documents.

## Portable verification

Run from any working directory using Python 3.10+ and only the standard library:

    python3 /path/to/this/verify_release.py

The verifier rejects missing, extra, changed, symlinked, duplicate, and escaping-path files; checks both frozen manifests and the controlling correction binding; and replays author and audit controls. The finite tests are not a formal verification of the infinite or universal claims. The release manifest records SHA-256 hashes and byte counts of all other release files; its own hash is recorded separately in the publication receipt.

Only authored mathematics, code, audits, and public verification metadata are distributed. The queue edit changes only this row's Status from queued to unsolved and Turns from 0/5 to 5/5, retaining all other bytes including existing header text and links. No release, DOI, merge, or external outreach is part of this draft.
