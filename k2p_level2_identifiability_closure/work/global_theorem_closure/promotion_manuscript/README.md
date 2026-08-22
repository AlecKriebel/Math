# K2P theorem promotion manuscript

This directory contains the promoted theorem layer for the principal
positive-eigenvalue K2P domain.  It does not modify
`work/final_theorem_release`.

Files:

- `K2P_SAME_PROMOTION_MANUSCRIPT.md`: final theorem statements and proof.
- `QUANTIFIER_AUDIT.md`: hypothesis, quantifier, and overclaim audit.
- `PROBE_PROMOTION_PLACEHOLDER.json`: frozen machine-readable probe values;
  the historical filename is retained so the guard interface does not drift.
- `verify_promotion_gate.py`: verifies 23 earlier proof inputs, the three
  completed probe artifacts, six raw probe ledgers, ten pass gates, and eight
  zero gates.
- `RESEARCH_LOG.md`: checkpoint record.

Run:

```text
python3 work/global_theorem_closure/promotion_manuscript/verify_promotion_gate.py
```

The required result is canonical JSON with `"status":"PASS"`.  Any missing
file, byte-hash drift, payload mismatch, nonzero gate, unfilled token, or
manuscript reversion to a pending state makes the guard fail closed.

The promoted classification concerns only

\[
\mathcal D_+=\{0<s<1,\ 0<g<1,\ g>2s-1\}
\]

and its explicitly stated strict continuous-time subdomain.  It makes no
mixed-sign claim.
