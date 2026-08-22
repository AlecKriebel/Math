# Portable referee bundle

The authoritative portable set is the recursive closure of
`work/final_theorem_release/RELEASE_LOCK.json`. It contains 374 files and
434,691,278 bytes. Its canonical content-ledger root is
`bbd9a28b801920430b8e5b17553b8feb00f29901fcb4f70cf3fb2b1eca54fd4a`.

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
