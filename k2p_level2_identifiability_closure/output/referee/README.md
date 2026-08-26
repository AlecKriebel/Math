# Portable referee bundle

The authoritative portable set is the recursive closure of
`work/final_theorem_release/RELEASE_LOCK.json`. It contains 406 files and
479,324,605 bytes. Its canonical content-ledger root is
`d4385855fd9d8387080a8e789613114f047fd93aaad9a78e86924d1a29b25c3e`.

## Entry-point names

This release uses the current entry points below.  It intentionally does not
ship duplicate wrappers under legacy or conventional handoff names.  A
reviewer encountering one of those names should use this exact mapping:

| Legacy or conventional name | Current release authority or command |
|---|---|
| `START_HERE.md` | this file, followed by `work/final_theorem_release/README.md` |
| `setup_environment.sh` | the explicit virtual-environment commands under **Referee commands** in the release README |
| `verify_handoff.py` | `output/referee/build_referee_bundle.py --check-only`, then `work/final_theorem_release/build_release_lock.py --check --require-ready` and `work/final_theorem_release/verify_final_theorem_release.py --quick` |
| `test_handoff_mutations.py` | `work/final_theorem_release/run_release_mutations.py` |
| `run_all_verifiers.py` | `work/final_theorem_release/verify_final_theorem_release.py --full` |
| `SUBMISSION_BINDING.json` | `work/final_theorem_release/RELEASE_LOCK.json` for theorem authority and `output/referee/REFEREE_BUNDLE_CONTENTS.json` for portable-file closure |

These are name mappings, not claims that the absent legacy filenames were
executed.  The current commands are the only supported referee protocol.

## Independence boundary

The package supplies independent primitive regeneration, exact graph-relation
checks, symbolic certificate replay, and complete verifier-facing ledger
mutations.  It does not claim a second all-family orbit partition that avoids
both the submitted primitive atlas and canonicalizer, or a second symbolic
engine that independently re-expands every higher-degree polynomial body.
Those are possible stronger audits, not hidden premises of the submitted
theorem.

From the project root, verify the exact set and regenerate its ledger with:

```sh
.venv/bin/python -B output/referee/build_referee_bundle.py --check-only
.venv/bin/python -B output/referee/build_referee_bundle.py \
  --ledger output/referee/REFEREE_BUNDLE_CONTENTS.json
```

To make a deterministic ZIP outside the Git history, add:

```sh
.venv/bin/python -B output/referee/build_referee_bundle.py \
  --output archives/k2p_principal_d_plus_referee_release_20260826.zip
```

The ZIP is deliberately derived rather than committed: its uncompressed
evidence is already present in the repository, and the archive exceeds the
ordinary Git hosting per-file limit. Publish the archive SHA-256 printed by
the builder if distributing that derived ZIP.
