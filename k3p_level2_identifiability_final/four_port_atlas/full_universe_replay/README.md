# Active full four-port replay

This directory closes the finite-universe boundary that was absent from the
first referee package.  The producer begins at the primitive cycle/four-theta
grammar, constructs all six rigid sources, 2,814 targets, and 24 labelled port
permutations, and visits all 405,216 directed presentations.  It does not open
the frozen companion ledger, the frozen 14-orbit lock, or the unavailable
cloud descriptor corpus.

The independent verifier and coherent mutation suite are kept separate from
the producing implementation.  The verifier imports neither the producer nor
the atlas compiler.  It reconstructs every primitive graph and K3P map from
literal definitions before checking the sealed artifacts.  Generated
artifacts live in `artifacts/`; the exact proof boundary is recorded in
`PROOF_BOUNDARY.md`.

Focused production command:

```sh
../../.venv/bin/python -B generate_full_four_port_replay.py
```

Independent verification command:

```sh
../../.venv/bin/python -B verify_full_four_port_replay.py
```

Focused coherent mutation command:

```sh
../../.venv/bin/python -B test_full_four_port_mutations.py
```

The exact output census must derive 27,834 post-topology presentations, 2,540
fully routed restoration obligations, and 40 complete non-equivalence
presentations before the `38 + 2` / fourteen-orbit quotient is checked.  Both
producer and verifier refuse optimized Python execution.
