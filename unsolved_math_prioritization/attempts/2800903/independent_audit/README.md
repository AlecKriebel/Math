# Independent review bundle

See `ACCEPTANCE.md` for the decision and `FULL_AUDIT.md` for the full review. The original problem remains unresolved after five substantive mathematical routes.

The original `../public` packet is immutable input. This bundle supplies an optimization-safe verifier correction and one source-description wording correction without changing that input.

Run:

```sh
python replay_audit.py
python -O replay_audit.py
python -OO replay_audit.py
```

Each command performs the same 30,090 explicit checks and writes the same `AUDIT_CHECKS.json`. All author-verifier baseline and corruption tests run in temporary directories, preserving the frozen files. The replay uses only the standard library and the public packet; no scholarly PDF, network connection, solver, or dataset is required.

`verify_hardened.py` is the frozen verifier plus `VERIFY_HARDENING.patch`; run it in a disposable directory if the adjacent original saved JSON must not be overwritten. The hardened valid output equals the original `verification.json` exactly.

`SOURCE_SCOPE.patch` removes an unsupported planar qualifier from an abstract-only historical reference. `SOURCE_NOTES_corrected.md` shows that single change. All five mathematical proofs are accepted without proof corrections.
