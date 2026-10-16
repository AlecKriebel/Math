# Dynamic Monge–Kantorovich partial audit

This is an explicitly corrected derivative; the original frozen packet is preserved unchanged. See `REPORT.md` for the provenance and `continuation.md` for the imported-proof qualification.

Read `REPORT.md` first. The general target is unresolved; status is exhausted after five approaches. The five mathematical notes contain exact assumptions, proofs, special cases, and remaining gaps. No novelty claim is made.

Run the standard-library checker from any working directory:

    python3 -B check_claims.py
    python3 -B -O check_claims.py
    python3 -B -OO check_claims.py

On the permission-read-only frozen packet under effective UID 1000, add `--require-readonly`. This option tests actual denied directory creation and denied write-opening of each file. An optional `--output PATH` must name a new file outside the packet. The checker does not change its inputs.

Checks are bounded exact arithmetic regressions and integrity controls; they do not replace proof review or establish PDE existence. Source metadata are public; source bodies and private research logs are excluded.
