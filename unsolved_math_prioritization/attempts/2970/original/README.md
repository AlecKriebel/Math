# KP-4.94 / 2970: Horikawa surface equivalence

**Partial/unresolved, five mathematical approaches.** Neither diffeomorphism nor canonical symplectomorphism is settled for any odd-r pair.

- `REPORT.md`: normalized problem, complete proofs of restricted results, and exact missing hypotheses.
- `CHECKS.md`: optimization, fail-closed mutation, and genuine read-only execution checks.
- `SOURCE_AUDIT.md`: primary-source scope and version distinctions.
- `source_manifest.json`: public bibliographic and PDF-verification metadata only.
- `attempts.json`: the five distinct approaches and their outcomes.
- `verify.py`: deterministic standard-library exact-arithmetic checks.
- `verification_results.json`: output of the checked script.
- `MANIFEST.sha256`: frozen public-file hashes, excluding itself.

Run `python verify.py` from this directory. To compare the saved output: `python verify.py > /tmp/horikawa_verification.json && cmp verification_results.json /tmp/horikawa_verification.json`.

The finite group computation does not encode the Horikawa monodromy. Parameter spot checks supplement the symbolic proofs and are not substitutes for them. No copied source documents or source text are included.
