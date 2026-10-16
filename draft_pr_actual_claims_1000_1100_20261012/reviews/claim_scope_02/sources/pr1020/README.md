# Arithmetic K(pi,1): credited prior-resolution audit

Read ACCEPTANCE.md and all four complete authored mathematical documents in first_audit/ and second_audit/. The exact OWR-1586-003 conjecture is accepted under its original p-odd-or-totally-imaginary convention, with every explicit correction retained. The catalogue has a SOURCE_SCOPE qualification. An unrestricted real-field p=2 statement is neither marked solved nor classified open. Credit Schmidt and Labute–Mináč; zero new proof-search turns and no novelty claim.

All eight selected accepted input files are unchanged, including historical manifests and public source-verification metadata. The first manifest records a then-pending second review; the second manifest and acceptance report record its subsequent completion. The separate local-condition clarification controls the p-adic Kummer-denominator correction. The historical pdf_signature_valid field means header detection only, as corrected by the second review. No cryptographic signature or publisher-PDF identity claim is made.

## Public reproduction and independent trust

Obtain the fixed BOOTSTRAP.py SHA-256 from the reviewed PR description, authenticate it before execution, and copy that authenticated file outside this packet. The trust anchor must come from that independent reviewed channel, not a freshly calculated hash chosen from an untrusted download. Set every packet file to mode 0444 and every packet directory to 0555. Use actual UID=EUID=1000:

    python -I -S -B /trusted/BOOTSTRAP.py --controls /path/to/packet
    python -I -S -B -O /trusted/BOOTSTRAP.py --controls /path/to/packet
    python -I -S -B -OO /trusted/BOOTSTRAP.py --controls /path/to/packet

Without --controls, the same authenticated bootstrap runs the positive document/scope verifier. The external bootstrap binds the manifest, verifier and rejection harness. The manifest binds every other delivered file, including accepted audits, metadata, declarations, code, pre-seal receipts and exact raw stdout/stderr references. It excludes only itself and the bootstrap, whose hashes are bound outward. Final receipts remain outside this inventory to avoid circularity and are externally pinned in the PR description.

Complete mode-specific stdout/stderr bytes and recursive exact JSON types, values, counts and identities must match. Empty, malformed, changed, skipped, expected-failure and mismatched-mode outputs fail closed. Controls have fixed intended rejection reasons. Physical create, append-open and unlink denials are exercised with UID/EUID1000 and before/after whole-packet hashes. Hostile current-directory and Python environment imports must produce complete baseline equality. The interpreter and standard library remain trusted; permission modes are an accidental-write barrier, not protection against root or deliberate owner chmod.

These are document/scope/integrity controls, not mathematical proof tests. No finite mathematical example count is manufactured for this proof/source audit. The mathematical acceptance rests on the authored arguments and independent review, relative to their precisely stated standard imports. Source-body, historical retrieval/inspection, excluded-material, dataset, full foundational proof, formal proof assistant, publisher-PDF, cryptographic PDF-signature and computational mathematical-proof replays are NOT_RUN. No source theorem is computationally certified. No source bodies, datasets, private sources, private personal or coordination material, or identifying metadata for excluded private material are delivered. No QUEUE or unrelated path changes.
