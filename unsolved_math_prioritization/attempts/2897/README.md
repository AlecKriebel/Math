# Kirby Problem 4.21 (ID 2897): five-attempt investigation

**Status: unsolved after five substantive attempts.** The rigorous special cases and reductions do not resolve the general closed topological 4-manifold question.

## Start here

**[Read CORRECTION.md](CORRECTION.md) before using the original proof.** The independent audit found that a linking-sphere generator condition in the punctured-manifold criterion is automatic, rather than an extra essential hypothesis. The correction includes the complete duality proof and states the simplified remaining gap. It also notes that the compact counterexample already embeds in standard S⁴.

- [Preserved original proof](artifacts/PROOF.md)
- [Five mathematical attempts](artifacts/RESEARCH_LOG.md)
- [Primary-source gate and limitations](artifacts/SOURCE_GATE.md)
- [Full independent mathematical audit](audit/INDEPENDENT_AUDIT.md)
- [Audit findings and status](audit/AUDIT_STATUS.json)
- [Independent exact lattice verification](audit/verify_independently.py)
- [Audited original-file fingerprints](audit/AUDITED_ARTIFACTS.json)

The original eight authored files are preserved unchanged. Their `partial_progress` label describes the proved limited scope; it does not mean the full problem is solved. Original status metadata saying the audit is pending is historical; the completed audit is linked above.

## Reproduce

From this directory:

```sh
(cd artifacts && sha256sum -c SHA256SUMS)
(cd audit && sha256sum -c SHA256SUMS)
python3 artifacts/verify.py > /tmp/kp421-authored.json
cmp artifacts/verification.json /tmp/kp421-authored.json
python3 audit/verify_independently.py > /tmp/kp421-independent.json
cmp audit/independent_verification.json /tmp/kp421-independent.json
sha256sum -c PUBLICATION_SHA256SUMS
```

Both programs use the Python standard library. They check exact finite lattice identities, not topological theorem validity or a solution of the problem. The symbolic all-n argument and the topological proofs are in the documents. Source PDFs and whole-book extractions are not redistributed.
