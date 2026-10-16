# Reproduce the independent audit

This source-free supplement audits the original eight-file bundle without changing it. AUDIT.md contains the mathematical review and an explicit published-input sequence proving that the universal slope set is not closed. The full classification remains unresolved by this work.

Use Python 3.11 or later and the standard library. Run as a nonroot user. In the commands below, ORIGINAL_BUNDLE means the directory containing the frozen original eight files.

```
python -B independent_audit.py ORIGINAL_BUNDLE --manifest-sha256 7d5d62eaa2d96d5f67383b8f0f7d9ec1888c337f7ff8982d55c0a9fc9f0b97ca --verifier-sha256 3367e41ffb5e711c436dae352b9786d93295687c053e0090e24c1f4ac1efb41e
python -B independent_controls.py ORIGINAL_BUNDLE --manifest-sha256 7d5d62eaa2d96d5f67383b8f0f7d9ec1888c337f7ff8982d55c0a9fc9f0b97ca --verifier-sha256 3367e41ffb5e711c436dae352b9786d93295687c053e0090e24c1f4ac1efb41e
```

The controls harness runs the author and independent arithmetic suites in normal, -O, and -OO modes. It creates and removes temporary mutated and read-only copies. The original directory is not edited. Outputs go to stdout.

Verify this supplement using its externally supplied manifest pin:

```
python -B verify.py . --manifest-sha256 AUDIT_MANIFEST_PIN
```

The included verifier is byte-identical to the independently pinned original verifier. Check its external SHA-256 before executing it. A fresh hash of an untrusted manifest is not an external trust anchor. Hash verification establishes byte identity, not mathematical truth.

VALIDATION.json contains the independent controls result. SOURCE_REVIEW.json contains public-source metadata and inspection status only. ORIGINAL_FREEZE.json records original file hashes and sizes. Neither source PDFs nor their extracted text are bundled. Rechecking live manuscript status later may produce a different answer; status observations here are dated 2026-10-08.
