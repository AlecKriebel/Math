# Reproduction

From the project root, the release check uses only the Python standard
library:

```sh
bash reviews/direct_anchor_probe_closure/verify.sh
```

To regenerate every certificate, use an environment containing SymPy:

```sh
PYTHON=../.venv/bin/python bash reviews/direct_anchor_probe_closure/verify_regenerate.sh
```

The regeneration is deliberately bounded to the 62 direct anchors and their
forced one-/two-port extensions.  It does not enumerate network generators or
arbitrary topologies.
