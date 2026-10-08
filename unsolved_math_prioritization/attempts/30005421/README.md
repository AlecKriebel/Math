# Wild-quiver expansion: credited prior-result application

The complete original target is accepted as an application of Markus Reineke's published Theorem 2.4, forward implication. Zero new proof-search turns; no novelty claim. Start with ACCEPTANCE.md, PROOF_APPLICATION.md and INDEPENDENT_AUDIT.md.

## Canonical portable verification

Use Python 3 with only its standard library. Independently authenticate the SHA-256 of BOOTSTRAP.py against the external review or PR record before executing it. Copy that authenticated bootstrap outside the candidate packet. Set the packet directory to 0555 and every file to 0444, then run as actual UID=EUID=1000:

    python -I -S -B /trusted/BOOTSTRAP.py /path/to/packet
    python -I -S -B -O /trusted/BOOTSTRAP.py /path/to/packet
    python -I -S -B -OO /trusted/BOOTSTRAP.py /path/to/packet

For the full adversarial delivery tests, add --controls before the packet path. Each invocation writes only to standard output and standard error; the controls create disposable test copies outside the packet. No network, source bodies, datasets or third-party packages are required.

The fixed external bootstrap authenticates the verifier, controls code and publication manifest. The manifest authenticates all other files, including acceptance and included preparation receipts. A replacement manifest supplied by the candidate cannot replace this external trust anchor. Byte identities of the full packet are recorded before and after every verification. Physical failed file-append and directory-create attempts establish read-only behavior.

## Evidence stages

REFERENCE_CAPTURE.json and mode-specific reference stdout/stderr are fresh checker runs captured before sealing. PREPARATION_CONTROLS_* and PREPARATION_RECEIPT.json, when present, are explicitly pre-final-seal evidence. PREPARATION_STAGE.json identifies that earlier bootstrap and manifest. The final manifest binds those historical receipts; final all-mode validation is recorded outside the packet to avoid a circular self-hash. Final external receipt pins are supplied in the review/PR record.

INDEPENDENT_TEST_RESULTS.json, AUDIT_MANIFEST.json, INPUT_PACKET_MANIFEST.json and ORIGINAL_CHECKER_LIMITATION.json are preserved audit-era records, with their own narrower historical inventories. Neither historical manifest is a complete manifest of this publication packet. HISTORICAL_ACCEPTANCE_REPORT.md retains the original acceptance and its earlier checker discussion. The omitted original script cannot be replayed here. The unchanged audit's original run_independent_suite.py entry is included for convenience; canonical delivery verification uses the externally authenticated bootstrap and direct per-mutant reference matching.

Public source documents, extracted source text, dataset contents, private sources, private coordination material, the original assert-only checker and the full legacy archive are excluded. Public-source metadata and prior inspection history are included without claiming new source retrieval by the packaging step.
