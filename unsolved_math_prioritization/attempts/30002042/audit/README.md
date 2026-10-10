# Independent acceptance packet: 30002042

Read `AUDIT.md` for the reasoning and `ACCEPTANCE.json` for the precise acceptance boundary. This is an accepted scoped partial after five approaches, not a full solution of general finiteness.

The original author archive, bootstrap, and external manifest remain separate immutable inputs. Verify their hashes against `ACCEPTANCE.json`, then run:

    python -I -S -B replay_controls.py AUTHOR_BOOTSTRAP.py AUTHOR_SAFE_FREEZE.zip AUTHOR_EXTERNAL_MANIFEST.json
    python -I -S -B -O replay_controls.py AUTHOR_BOOTSTRAP.py AUTHOR_SAFE_FREEZE.zip AUTHOR_EXTERNAL_MANIFEST.json
    python -I -S -B independent_math.py
    python -I -S -B -O independent_math.py

The longer supplied artifact filenames may be substituted. No network or external mathematical package is needed. The replay script checks exact embedded trust anchors before running author code. Both scripts were independently inspected and actually run in normal and optimized modes. The saved JSON outputs record those executions.

`SOURCE_BYTE_CHECKS.json` records fresh primary-PDF retrieval and exact matching. `INPUT_VERIFICATION.json` binds the full corpus comparison without publishing its contents. No raw third-party document, dataset, rendered source image, or private coordination file is included.
