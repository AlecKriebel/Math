# Portable referee bundle

The authoritative portable set is the recursive closure of
`work/final_theorem_release/RELEASE_LOCK.json`. It contains 399 files and
478,755,815 bytes. Its canonical content-ledger root is
`072baaa4066569acd31c552149f6afb727323e54b241bdefc98452598309dd61`.

From the project root, verify the exact set and regenerate its ledger with:

```sh
.venv/bin/python -B output/referee/build_referee_bundle.py --check-only
.venv/bin/python -B output/referee/build_referee_bundle.py \
  --ledger output/referee/REFEREE_BUNDLE_CONTENTS.json
```

To make a deterministic ZIP outside the Git history, add:

```sh
.venv/bin/python -B output/referee/build_referee_bundle.py \
  --output archives/k2p_principal_d_plus_referee_release_20260821.zip
```

The ZIP is deliberately derived rather than committed: its uncompressed
evidence is already present in the repository, and the archive exceeds the
ordinary Git hosting per-file limit. Publish the archive SHA-256 printed by
the builder if distributing that derived ZIP.
