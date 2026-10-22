# 30006359: forest consistency varieties

The general conjecture remains unresolved. This packet proves general incidence/saturation lemmas, a rigid group-support case, and an exact bounded proposition for the explicitly normalized source equation systems, including the third expansion in the proof, through rank four. It reproduces previously reported low-rank counts, with full credit to Liu and Lu.

- `RESULT.md`: complete scope, proofs, finite certificate argument and remaining gap
- `SOURCE_GATE.md`: primary-source verification and prior-work checks
- `ATTEMPT_LOG.md`: five substantive approaches and checkpoints
- `verify.py`, `verification.json`, `verification_summary.json`: exact replay and receipts
- `requirements.txt`: tested dependency
- `SHA256SUMS`: frozen author-file hashes

Run `python3 verify.py --check` from this directory, with SymPy 1.14.0 installed. The computation uses exact affine elimination and division only by forms required nonzero; it does not invoke a Gröbner basis or rely on numerical sampling. The 426 cases are finite evidence/proof only for the bounded normalized model, never for the all-rank question.

No downloaded source files, corpus, private context, or third-party correspondence are included. AI-assisted and unrefereed; no novelty, priority, formal-proof-assistant certification, or general solution claim.
