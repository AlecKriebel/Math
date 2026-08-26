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

Both mutation runners require a caller-owned output path outside the project
source tree. Each suite first reproduces its stored production certificate
byte for byte. Its report stores the exact full expected/observed diagnostic,
exception type, and exit code for every rejection; tracebacks, import errors,
timeouts, signals, other non-one exits, PASS tokens, and success artifacts
cannot qualify a case. The sealed bytes are independent of checkout paths and
supported Python traceback formatting.
Resealing either canonical mutation certificate requires the explicit
`--allow-authoritative-output` flag, which licenses only that runner's exact
canonical path. The relocation test also proves that two named extractions
produce identical semantics reports without changing source bytes and rejects
direct, ordinary, and symlink-resolved source collisions for both runners.
Final report publication uses an fsynced same-directory temporary file and
atomic replacement. Pre-existing output is removed before optimized or helper
imports, and source hardlinks and output symlinks are rejected.

```sh
.venv/bin/python -B work/quartet_separation_closure/verify_quartet_logic.py
.venv/bin/python -B work/quartet_separation_closure/test_quartet_semantics_mutations.py --output /tmp/k2p-quartet-semantics-mutations.json
.venv/bin/python -B work/quartet_separation_closure/test_quartet_semantics_relocation.py
.venv/bin/python -B work/quartet_separation_closure/verify_quartet_terminal_bindings.py
.venv/bin/python -B work/quartet_separation_closure/test_quartet_terminal_binding_mutations.py --output /tmp/k2p-quartet-terminal-binding-mutations.json
```
