# KK uniqueness application: target 30005199

Read PROOF_APPLICATION.md, INDEPENDENT_AUDIT.md and ACCEPTANCE.md for the mathematical statement and limits. The current proof includes the exact optional clarification patch. Public source identities and inspection history are in SOURCE_METADATA.json and SOURCE_AUDIT.json. No source PDF, extracted source text, page image, dataset contents, full superseded proof or private coordination material is included. No QUEUE content or modification is part of this delivery.

## External trust and replay

Authenticate BOOTSTRAP.py against the externally supplied SHA-256 before executing it. A hash found only inside a downloaded packet is not an independent trust anchor. The bootstrap fixes the manifest, verifier and control-harness hashes. The manifest binds every other delivered file, including acceptance and all preparation receipts; the external bootstrap hash binds the bootstrap itself.

Copy this flat packet to a fresh directory. Set every file to mode 0444 and the directory to 0555. Run as real UID=EUID=1000. Run the separately authenticated external bootstrap with Python -I -S -B, then with -O and -OO, supplying the packet directory. Adding --controls before the directory invokes the authenticated adversarial harness. Redirect outputs outside the sealed directory.

The validator replays the unchanged nine authored tests and sixteen independent tests through deterministic unittest result collectors, plus actual mathematical code mutants. It compares complete fresh stdout and stderr bytes with exact pinned mode-specific references and recursively exact JSON types, with no output normalization. Actual denied append/create probes supplement permission-mode checks. Hostile-environment output must match the complete baseline byte-for-byte. Before/after hashes bind the whole packet.

PREPARATION_CONTROLS and PREPARATION_RECEIPT are explicitly historical pre-seal evidence. Their older bootstrap describes that stage only. Final evidence is recorded externally after sealing so no receipt needs to contain its own hash. The final externally pinned bootstrap binds these historical receipts too.

## Verification boundary

Fresh finite checks and adversarial delivery checks are not an analytic proof certificate. Historical source inspection is recorded, not rerun by this portable validator. Original full-packet replay, historical clarification-patch application from the omitted base, source-body replay, source-hash recheck, dataset replay and formal proof-assistant verification are NOT_RUN here. The local preparation did apply the exact clarification patch to the preserved authored base and match the accepted result hash; this is distinct from a portable replay without that base.

The accepted ordinary stable-ideal application is credited to Szabó. The separate unitally absorbing path has no initial-1 assertion. The exact OWR convention hold remains and no new proof-search turn was used.
