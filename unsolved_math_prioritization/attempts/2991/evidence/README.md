# Full-bundle audit packet: KP-4.115 / 2991

Verdict: part (a) accepted; part (b) unresolved. Combined disposition: unsolved, 5/5 substantive approaches. No novelty claim. Original freeze unchanged.

## Contents

- `AUDIT_REPORT.md`: full mathematical acceptance and bounded disposition.
- `SOURCE_REVIEW.md`: independent primary-source audit of relative doubling and efficient homological triples.
- `VERIFICATION_METADATA.json`: public source hashes and dataset counts/hashes, without source or dataset bodies.
- `candidate/`: exact nine-file original read-only freeze.
- `prior_review/SECOND_INDEPENDENT_PART_A_AUDIT.md`: later part-(a) acceptance, outside the original freeze.
- `receipts/`: final normal, `-O`, and `-OO` harness receipts.
- `audit_exact.py`: full original-candidate integrity envelope, arithmetic oracle and mutation/CLI replay.
- `verify_envelope.py`: read-only verification of every delivered member against the externally pinned publication envelope.
- `PUBLICATION_ENVELOPE.json`: complete packet bindings, excluding only itself. Obtain its expected SHA-256 from the separate delivery receipt rather than trusting a value inside the same envelope.

No publication or queue modification is performed by either checker. Runtime logs, mutation trees, primary-source documents, dataset contents and private coordination material are excluded.

## Replay

First verify the packet using the externally supplied digest:

    python verify_envelope.py /path/to/packet EXPECTED_ENVELOPE_SHA256

The full acceptance replay requires actual UID and EUID 1000, candidate directory mode `0555`, every candidate file mode `0444`, and an existing empty output directory outside both the candidate and packet. The archive records those modes. Some safe-extraction libraries deliberately add owner write access; use an extraction option preserving recorded permissions, or restore the stated modes on a disposable extracted copy before replay. A Git checkout may likewise not preserve read-only modes.

    mkdir /tmp/trisection-audit-normal
    python audit_exact.py /path/to/packet/candidate /tmp/trisection-audit-normal

Repeat with `python -O` and `python -OO`, giving each invocation a different existing empty external directory. Each invocation itself runs the original checker under all three optimization modes and writes its receipt, logs and disposable mutation copies only beneath the explicitly requested output directory. It never changes candidate bytes or permissions.

A successful native `candidate/verify_exact.py` result authenticates only the pinned proof and finite arithmetic; it does not authenticate the report or metadata. Use the full envelope for whole-packet integrity. Neither executable certifies smooth-topological theorems. The mathematical proofs and exact source dependencies remain necessary.
