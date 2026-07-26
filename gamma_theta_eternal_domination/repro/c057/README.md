# Replaying accepted claim C-057

Claim C-057 is a certified finite template exclusion:

> Relative to C-050 and the accepted inputs of C-055, no order-13
> counterexample with common parameter three has a hub-free induced \(C_9\)
> in its complement.

Together with C-053, this leaves the overlapping complement-\(C_5\) and
complement-\(C_7\) branches.  It does not complete the parameter-three slice,
exclude every order-13 graph, raise the lower bound to 14, or resolve the
universal conjecture.

From the campaign directory, run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONWARNINGS=error \
python3 -B -W error repro/c057/replay.py
```

The expected verdict is:

```text
VERIFIED_C057_HOLE9_TEMPLATE_EXCLUSION_BINDINGS_AND_PROOFS
```

The replay checks every hash-bound theorem, instance, proof, verifier, and
review artifact; preserves the original production attempt as
`RETRYABLE_NONCLAIM`; reruns the independent certificate verifier and all 24
hostile corruptions; rebuilds and replays both proof checkers through the
external code audit; and independently reconstructs the complete formula and
coloring bank through the mathematical coverage audit.  It invokes no SAT
solver.
