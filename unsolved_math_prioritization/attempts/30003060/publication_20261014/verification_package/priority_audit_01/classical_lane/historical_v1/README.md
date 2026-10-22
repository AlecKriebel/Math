# Historical v1 — immutable audit inputs

These three files are byte-for-byte copies of the first accepted classical-lane script, integer-control output, and decision, preserved before the 2026-10-15 diagnostic-interface repair. MANIFEST.json pins their bytes. Do not treat this historical script as the current executable check.

The original normal-mode run passed 21 cases / 604 orbit blocks. Its mathematical computations and the algebraic proof remain valid. Its acceptance checks used Python assert statements, which optimized Python can remove. The current parent-folder script replaces every such diagnostic acceptance statement with explicit need checks; the repair changes no mathematical operator or accepted output.

The current replay receipts demonstrate normal/optimized equality and deliberate-corruption rejection before acceptance output is written. Historical files are retained for provenance, not for optimized-mode execution.
