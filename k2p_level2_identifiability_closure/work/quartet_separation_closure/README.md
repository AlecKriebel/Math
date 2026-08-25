# Displayed-quartet semantic and terminal gates

This directory binds every promoted `displayed_quartet_mismatch` record to a
literal pointwise K2P zero-versus-strict-positive invariant. Under the fixed
character order `(0,C,G,T)` and spectrum `(1,s,g,s)`, the equal nonzero sector
is `{C,T}` and the singleton sector is `{G}`.

`verify_quartet_logic.py` derives the tree pullbacks from the Klein-four group
law. It checks all six canonical `F`/`J` formulas, 24 leaf permutations, the
identity and global `C<->T` transports, all seven nonempty displayed sets, all
21 unequal unordered pairs, and the formulas printed in the proof sources.

`verify_quartet_terminal_bindings.py` then streams every quartet terminal in
the raw4, theta2, theta2 dummy-restoration, cycle, restoration, and one-/two-
port probe layers. It binds 4,414,710 row references and all 888 per-layer
certificate IDs to actual leaf-labelled Fourier coordinates, with no missing
or dangling certificates. The large topology ledgers remain byte-identical;
their independent graph replayers supply the row-to-split-set premise, while
this verifier supplies the split-set-to-literal-algebra conclusion.

Run:

```sh
.venv/bin/python -B work/quartet_separation_closure/verify_quartet_logic.py
.venv/bin/python -B work/quartet_separation_closure/test_quartet_semantics_mutations.py
.venv/bin/python -B work/quartet_separation_closure/verify_quartet_terminal_bindings.py
.venv/bin/python -B work/quartet_separation_closure/test_quartet_terminal_binding_mutations.py
```
