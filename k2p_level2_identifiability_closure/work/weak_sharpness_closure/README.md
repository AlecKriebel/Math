# Weak-tree-child sharpness certificate

This directory gives an exact graph-derived proof that the strong
tree-child hypothesis is sharp for K2P on the principal positive domain,
indeed already on the strict continuous-time cone.

Run:

```sh
../../.venv/bin/python -B verify_weak_sharpness.py
```

The deterministic output is `weak_sharpness_certificate.json`.  The proof
and replay are deliberately independent of the four-port descriptor and
rank pickles.
