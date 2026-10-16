# Truncated Hadamard simplices: credited partial prior resolution

**PARTIAL. Static official Lean statement/provenance inspection only. No Lean build, kernel axiom audit, author script or downloaded proof-code execution.**

Read current/AUDIT.md for the full accepted audit of all seventeen written proof arguments in Nikita Lebedev, arXiv:2609.32950v1. The smallest nonintegral dimension is 11. Smoothness holds exactly when m > (d-1)n/2 and m/n is not an odd integer. Every member in the strict upper range is normal, including nonsmooth resonances; further sufficient normality bands are accepted. The complete normality classification remains unresolved. The region outside these positive bands contains known negative examples and families and must not be described as entirely open. The marked Hadamard simplex and all affine degree lattices remain part of the hypotheses. No new substantive proof-search turn or novelty claim is introduced.

All nine accepted public audit files are preserved byte-for-byte under current/. Source titles, public URLs, hashes, byte counts, public status and retrieval/inspection history are metadata only. Source documents, manuscript text, downloaded companion contents, datasets and private coordination are excluded. current/verify_audit_packet.py is preserved historical code and its replay is NOT_RUN in this publication stage; the fresh runner is verify_publication.py. current/VERIFICATION_RECEIPT.json, current/AUDIT_MANIFEST.json and current/EXACT_CHECK_RESULTS.json describe historical accepted evidence. Historical source inspection is not a fresh source replay.

## Public reproduction and trust

Authenticate BOOTSTRAP.py against the independent SHA-256 in the reviewed PR description before executing it. Keep that authenticated copy outside the packet. Set every packet file to mode 0444 and every packet directory to 0555. Use actual UID=EUID=1000, Python 3.10 or later, and only the standard library:

- python -I -S -B /trusted/BOOTSTRAP.py /path/to/packet
- python -I -S -B -O /trusted/BOOTSTRAP.py /path/to/packet
- python -I -S -B -OO /trusted/BOOTSTRAP.py /path/to/packet

Add --controls before the packet argument to run full integrity, schema, exact-output and hostile-import controls. References for every interpreter mode bind complete raw stdout and stderr, recursive exact JSON types and values, all 35 diagnostic identities and 496 invocations, eight intended mathematical mutation rejections and one separately labeled injected-failure control. Six negative-predicate checks embedded in the 496 invocations are identified separately; they are not extra tests or a proof certificate. Empty, skipped and expected-failure reports cannot replace positive success. Detailed labeled errors are required for intended rejection. No private source or accepted ZIP is needed to reproduce these public checks.

Every delivered byte is authenticated: the independently pinned bootstrap binds the manifest and executable verifier/control harness; the manifest binds all remaining files, including acceptance, references and historical/pre-seal receipts. The verifier also compares the packet bootstrap to that external pin. No final receipt is included in its own authenticated inventory. PREPARATION_* files are historical pre-seal evidence. Final sealed replay receipts remain external, with pins in the PR description, avoiding circular hashing.

Read-only create/append probes are actual EACCES tests under UID/EUID 1000, and whole-packet snapshots are unchanged. Unix read-only modes are an accidental-write barrier, not kernel immutability or protection against intentional owner chmod. The standard-library interpreter is trusted, not authenticated.

NOT_RUN: historical audit-harness replay, new source search, excluded source-body replay, dataset replay, Lean build, Lean kernel axiom audit, downloaded companion execution and author mutation controls. The author's 29 mutation outcomes remain unverified static metadata. Our eight mathematical mutations apply only to our authored checker, never to the downloaded companion. No QUEUE or unrelated file changes are included.
