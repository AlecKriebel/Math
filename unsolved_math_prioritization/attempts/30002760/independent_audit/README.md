# Adaptive transport approximation independent audit

Decision: accept the original frozen packet as qualified partial results; retain `unsolved`, `5/5`. No required corrections. See AUDIT_REPORT.md for every proof, source scope, acceptance boundary, and checker limitations. CORRECTIONS.md records two optional clarifications only.

Reviewed manifest SHA-256:

`6881ffec2ec0cdf4c44f9aa0a1b5155efe171d31e4b801f21961afaa9166a260`

The original directory has 18 bound files plus its manifest. Nothing in it was edited.

## Replay

Use Python 3's standard library. Set PACKET to the original frozen public directory, then run:

- `python "$PACKET/verify_packet.py"`
- `python -O "$PACKET/verify_packet.py"`
- `python -OO "$PACKET/verify_packet.py"`
- `python independent_controls.py --packet "$PACKET"`
- `python -O independent_controls.py --packet "$PACKET"`
- `python -OO independent_controls.py --packet "$PACKET"`

The three independent outputs should exactly match evidence/independent_normal.json. Their generated case files live in temporary directories and do not modify the packet. The evidence directory contains actual replay receipts and source hashes/extraction results, never source documents or extracted texts.

The original suite checks 37,329 finite controls. The audit's additional controls independently cover all five approaches and fresh claim, malformed-input, and computation mutations. Counts describe finite checks, not a formal proof or exhaustive adversarial guarantee. Full source retrieval is not needed to replay either mathematical checker.

AUDIT_MANIFEST.json binds this source-free audit package. Preserve its externally communicated digest when relying on its integrity.
