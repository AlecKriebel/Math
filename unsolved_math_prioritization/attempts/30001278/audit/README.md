# Independent audit packet

Read `AUDIT_REPORT.md` for the complete verdict and `VERDICT.json` for the claim-by-claim summary. All five mathematical arguments are accepted within their stated partial or conditional scopes. The problem is not marked solved.

`AUTHOR_BINDING.json` and the exact `AUTHOR_MANIFEST.json` copy identify the untouched original. `AUDIT_MANIFEST.json` hashes the independent audit deliverables. `SOURCE_CHECK.json` and `CORPUS_CHECK.json` contain public verification metadata only.

## Reproduction

Run the standalone new mathematical controls:

```
python3 -B independent_controls.py
python3 -B -O independent_controls.py
```

Both reproduce `INDEPENDENT_RESULTS.json` exactly.

With the frozen source-free author packet and its original archive available, reproduce the audit's packet and corruption controls:

```
python3 -B packet_controls.py --packet /path/to/original/public --archive /path/to/ramification_30001278_author.tar.gz
```

The input archive and manifest are externally authenticated before author code is imported. The script checks the archive members and every author payload hash, runs both author programs in normal and optimized modes in an isolated temporary copy, and performs authored dummy corruption tests. Its output reproduces `ADVERSARIAL_RESULTS.json`.

The controls are bounded checks, not a proof assistant, general local-field enumerator, or malicious-code sandbox. No internet access or source fixtures are needed to run them.

## Optional patch

`OPTIONAL_CLI_HARDENING.patch` is a tested, nonmathematical change to the main verifier's treatment of a direct symlink-root path. It includes the new manifest entry. It does not alter a proof or repair changed-byte acceptance. `HARDENING_RESULTS.json` records the new anchor and actual normal/optimized outcomes.

Apply only to a separate copy of the original, for example with `patch -p1 -i /path/to/OPTIONAL_CLI_HARDENING.patch` while in that copy. This creates a new author manifest identity. The original frozen input must remain unchanged.
