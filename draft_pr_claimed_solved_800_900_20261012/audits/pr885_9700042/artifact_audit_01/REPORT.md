# Independent frozen-artifact audit: PR 885 / problem 9700042

Verdict: **PASS for authenticity and finite reproducibility of the assigned original packet.** This verdict does not accept the mathematical theorem, external premises, novelty, or priority. No artifact fix is required for the exact frozen package; the validation boundaries below must remain explicit.

The 30 original regular files, totaling 214,980 bytes, match the external source manifest and the actual Git tree/blob bytes at head `4b1ef9bbeb723a4171949a6c3934db98962ac615`, prefix `unsolved_math_prioritization/attempts/9700042/`. Every Git mode is 100644. The external manifest SHA-256 is `6b1d1281848190f616f6759f40454183c937b65e65219b893202254be6c3617d`. Authentication before, during, and after replay agrees exactly. Original effort remains **5/5**. Live PR eligibility was supplied by the parent's previously captured gate; this audit independently checked its assigned exact Git head, not current remote PR state.

## What was reviewed and replayed

Before executing packet code, I fully read `verify_packet.py`, all its helpers and embedded subprocess bootstrap, both author resume checkers, and the three included review checkers. Their executed code imports only Python standard-library modules. I also read the authoritative packet manifest, README, frozen root replay receipt, both actual patches, and the three historical audit manifests. The original files were never edited.

The inventory has 29 payload records plus the manifest itself, totaling 30 original files. Its 25 declared authored-artifact relocations have matching sizes and SHA-256 values. The accepted-revision SHA agrees with the actual revised C4 file. Historical audit inventories have different meanings: audit A has 24 historical records, of which 16 are represented by identical packet payload bytes and eight are omitted inspection material; audit B has seven authored historical records, all represented; C1 has 15 historical records, 12 represented and three omitted. These counts compare byte identities, not whether historical paths still exist. The current README and packet manifest explicitly disclose omissions and relocations. Audit B separately lists three public-source download records; source bodies are not packet payloads. No missing source body or duplicate historical snapshot was silently treated as an included file.

Both actual patches were independently applied with the system `/usr/bin/patch`, version `patch 2.0-12u11-Apple`, using `--batch --fuzz=0`. Resulting bytes equal the frozen revised artifacts:

| Patch | Revised bytes | Revised SHA-256 |
| --- | ---: | --- |
| C1 clarification | 11,102 | `fe586532ef2430956aacf26e007b674915b0ae6293ce75d1e05a5abf8b098002` |
| C4 clarification | 20,646 | `8da7cf366948e8d4fc63e3399cc4fe804ed786ea99b01479619efbdbacfedf3a` |

Changing a real required context line makes each zero-fuzz patch fail. The independent receipts record actual patch stdout sizes and hashes separately from normalized path text.

## Direct and nested execution

Two clean, unwrapped invocations of the original verifier script passed from an unrelated audit-owned working directory: `python3 -I -S -B` and `python3 -I -S -B -O`. Neither invocation uses an observer or altered root source. Both returned exit 0 and empty stderr. Actual root stdout is **9,202 bytes**, SHA-256 `26f10d4d514494afabdeba78bf4d037cbd5a1c7f2c79125ce72478c65a03dedb`. Its parsed JSON matches the frozen replay receipt except `python`: current 3.14.6 versus frozen 3.12.14. Therefore I do not claim the root stdout is byte-identical to the 9,203-byte frozen receipt.

A separate clean observed pair executes the exact authenticated root code and records every actual subprocess command without changing child arguments. Each observed replay contains **64 child calls**: 20 successful checker runs, 20 forced-assertion failures, 20 corrupt-checker hash rejections before execution, and four patch calls (two genuine applications plus two damaged-context failures). The optimized observed root has effective interpreter optimize=1; checker ASTs are still compiled with optimize=0. An additional earlier observed baseline also completed successfully and is retained as supporting evidence. The clean final pair is the count basis; interrupted attempts are recorded separately.

I also independently replayed all five checker sources in four modes, giving **20 positive runs and 20 forced-assertion failures**, plus four separate child-prefix flag probes. Direct independent runs add `-S -B` to each mode and report `sys.flags` from inside the same executing child. All generated JSON files match frozen bytes in every mode:

| Checker | Generated JSON bytes | Actual stdout bytes | Frozen/actual JSON SHA-256 |
| --- | ---: | ---: | --- |
| Author C1 | 3,971 | 1,253 | `022566a4288c89010aa15923c84cc802e9cb0627937eed44144e818905df3b08` |
| Author C4 | 628 | 628 | `c6665c65efbab00cbda08a0b4151be5d076bdf89d6a453dc6a3997174c88c57f` |
| C1 audit | 4,291 | 4,291 | `52202ecc5149d7086787457d3d5f9832ec9123a58f4e1798438b70ba78b8dbc0` |
| Audit A | 472 | 472 | `d084520403d85d0c020cd5753ec34ca380da03f93cd72420850d83fbc02b8a0e` |
| Audit B | 398 | 398 | `97f2e3a7c56da99144525b3b49784e5e89d9d2eab6c96b87a85c73e486e436a6` |

Author C1's stdout deliberately omits coordinate-count details. Its actual stdout SHA-256 is `28676c0051f922b388d2d0f56287c964917ae5c99814f203c6644aa133f56f41`, distinct from its generated JSON hash. All other checker stdout hashes equal their generated JSON hashes. Receipts label those byte streams separately.

Requested flags and effective flags are distinct. The unchanged root requests child prefixes `[]`, `[-O]`, `[-I]`, and `[-I,-O]`; it does **not** pass `-S` or `-B`. Separate same-interpreter/prefix probes report respectively `(optimize, isolated, no_site, dont_write_bytecode)` = `(0,0,0,0)`, `(1,0,0,0)`, `(0,1,0,0)`, and `(1,1,0,0)`. Those are explicitly separate probes, not instrumentation inside the unchanged root children. The independent suite's same-process measurements instead include no_site=1 and dont_write_bytecode=1 in every mode because it explicitly adds `-S -B`. Parent interpreter isolation is not inherited automatically. All positive checker code is compiled with optimize=0; inserted forced assertions fail even when the executing interpreter has optimize=1. Static assertion-statement counts are 3, 16, 9, 0, and 10 respectively; audit A uses explicit `require` checks rather than assertion statements.

## Bounded controls and accepted format boundaries

Twenty small fixture controls were run on fresh own copies and removed immediately. Bad SHA, Git-blob, and byte-count pins; wrong inventory container/path types; missing files; extra regular files; altered proof bytes; a listed payload symlink; and an expected file replaced by a directory are rejected. Actual patch-context failures, forced assertions, and corrupt-source failures are also rejected by the replay suites.

The following are **accepted boundaries of the root helper**, observed and not hidden:

- Its path enumeration uses `is_file()`, so extra empty directories, an extra dangling symlink, and an extra FIFO are ignored. The FIFO is never opened.
- The manifest itself is read but is neither a listed payload nor checked for being a symlink. Replacing it with a symlink to identical own-fixture bytes is accepted.
- Duplicate payload records are accepted; the returned payload-record count rises from 29 to 30 although there are still 29 unique payload paths. Duplicate JSON keys follow standard `json.loads` last-value behavior.
- Metadata such as accepted-revision SHA and turn count is not schema-validated by `authenticate`; changing only those fields or manifest whitespace can pass its internal checks.

These are reasons to treat the root verifier as a replay integrity helper for an externally authenticated package, not as a typed manifest validator, complete filesystem-entry validator, self-authenticating trust root, or hostile-code sandbox. For this exact original packet, independent external-manifest and actual-Git authentication pins the manifest bytes, confirms unique correct inventory metadata and 5/5 effort, and rejects nonregular original entries. No altered fixture is being promoted as an authenticated original. Future hardening could add a typed unique-path schema, explicit self-file/type checks and strict filesystem-entry policy; no candidate file was changed here.

## Resource incident and evidence handling

The shared filesystem temporarily refused even small writes with ENOSPC. One observed optimized run failed while saving a child stderr; the first independent checker had executed its positive and forced-failure processes but could not save its first receipt. Two contemporaneous unwrapped direct roots reported a first patch-output mismatch. Those direct errors did not themselves print ENOSPC: their resource attribution is an inference from concurrent confirmed ENOSPC and later clean passes of the same unchanged originals. Initial failure receipts are retained and normalized in `ENVIRONMENT_INCIDENTS.json`. Setup attempts that failed before root launch are not counted as root replays. After write recovery, all complete clean suites passed. No original byte or effort count changed.

Raw child process bytes are retained privately under audit-owned raw-receipt folders. Public receipts keep actual raw byte counts and SHA-256 hashes, with path-normalized text explicitly labeled. `PUBLIC_MANIFEST.json` is an explicit allowlist of authored safe files, excludes itself for self-reference, and does not permit recursive inclusion. No source PDF/HTML, screenshot/render, raw corpus copy, credentials, private absolute paths, or temporary source copy is in that public allowlist.

The strongest verified result is exact source identity plus reproducibility of these finite diagnostics and patch transformations. The remaining mathematical and priority questions belong to independent proof and literature audits; a finite pass cannot settle them.
