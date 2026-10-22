# Independent PR888 verification-tool review 01

Review scope: the newly authored `portable.py` authentication, format, packaging, and finite replay mechanisms for problem 30005079 only. This is not mathematical acceptance, a novelty assessment, a final-paper review, or whole-package clearance. Original effort remains 1/5.

Disposition: **no blocking defect identified in the frozen tool within this scope**, with the resource-limited supplementary test and the trust/race boundaries below explicitly retained. No engineering code or original source was changed by this reviewer.

## Frozen target and independence

Before reading the tool body or the engineering control report, I froze an attack plan and this target:

- `portable.py`: 44,752 bytes, SHA256 `bcaac73bf1620098e0d24f2a2cb9399613567be6018b99329c0a58b6e0101910`.
- External immutable original-source manifest: SHA256 `49a72d6bf90d3a74be69ed855c7a9cfc0f3b1d83a4e4e3ce997c0ca7c07d1cbc`.
- Original PR head: `a7571ddbbbe2de3600b96bd7ccccf86e4d5748e7`.

I read the entire new tool, both entire original checker bodies, and the entire original driver before executing any of them. I independently recomputed all 21 source lengths, SHA256 hashes, and Git blob object hashes against the external manifest; all matched, totaling 98,055 bytes. This checks the bytes against externally supplied pins, rather than deriving authority from a new package's own inventory. I did not newly acquire the original commit from GitHub. The two checker ASTs each contain 13 `assert` statements.

My own fixture was assembled in this review's private directory from those original bytes, the independently frozen tool snapshot, and the explicit format fixture assets. Its package index SHA256 is `9725edf2a5d398515bf0ea9b521cfde6ea2182797b5699292784ce583fcc05ba`. Its 29-member ZIP was 65,829 bytes. The tool snapshot was authenticated before every actual wrapper CLI launch. The fixture is explicitly not a publication artifact.

The independent provisional assessment was saved at 2026-10-16T05:38:46.679044+00:00, before reading the engineer's controls. Only afterward did I read `engineering_controls.py` and its receipt. Those describe 33 in-process controls and one actual CLI control; none are counted as my executions.

## Actual execution record

The main and supplementary independent receipts contain **42 actual wrapper CLI invocations across 41 distinct labels**. Of those invocations, 41 met their expected outcomes, including one repeated default-source-corruption rejection. One expected-success hostile-environment full replay could not complete because of ENOSPC during setup/materialization. An additional direct CLI launch of the unchanged original driver under actual `-O` rejected optimization as expected. A separate instrumented source-only observation is explicitly in-process and is not counted as a CLI invocation.

Four full replays passed: normal verify, outer-optimized verify, a fresh default outside-output build, and fresh outer-optimized current-publication verification. Each full replay genuinely launches the original root once and launches six real checker children: two positive, two deliberately defective, and two changed-code preexecution controls. Thus these four observed replays contain four root launches and 24 checker-child launches. Each also performs three separate in-process damaged-context patch controls. The patch controls are not described as child launches.

For normal replay, the measured original root and checker optimization levels were 0. For both optimized verify and optimized current, the original root measured actual optimization 0, and all six checker children measured actual optimization 1. Root and children measured isolation, no-site, no-bytecode, ignore-environment, and safe-path flags as enabled. The original root's requested nested flag list is recorded separately from the launcher's effective flags and measured child flags. Neither `sys.flags` nor historical execution records are spoofed.

Both unchanged original checker sources are compiled with `optimize=0`, preserving their 13 assertions, even when their actual child interpreters run with `-O`. The first negative child deliberately makes the original exact-integration assertion false; the second damages the original candidate input and fails its original candidate-hash assertion. Both have genuine `AssertionError` failures after their original-execution markers. Each corrupt-code child fails its preexecution SHA256 guard and does not create that marker. The two positive children produce byte-exact original result files and expected stdout with empty stderr. All four edition hashes and the three forward and reverse patch transitions remain checked by the unchanged original driver; there is no invented replay of historical editions.

The direct original-root optimized rejection independently confirms why the harness must run that root with actual optimization 0. Running the original root directly with actual `-O` does not succeed.

## Boundary controls and mechanisms

| Boundary | Independently observed evidence |
|---|---|
| Strict JSON and schema | Actual CLI rejects duplicate keys, overflowing floating numbers, boolean byte counts, extra inventory fields, traversal paths, directory-case aliases, extra metadata keys, wrong title, extra creator fields, wrong ORCID, a third deposit asset, and altered dependency byte types. |
| Ordinary closed trees | Actual CLI rejects a symlink file and an unlisted empty directory. Static inspection also rejects symlink directories, nonregular entries, missing/unlisted files, duplicate names, file/directory collisions, and directory spelling aliases. |
| Independent original authority | Reindexing changed original checker bytes does not bypass the external original manifest and per-file hashes. A default-replay request rejects a checker containing a private execution canary before it can run; the canary is absent. |
| Native source-only route | Actual optimized CLI authenticates all three full native corpora and returns the exact 5,415-byte pair with SHA256 `6bbb2826e583f9ccbbb38411ce780e865c0b9564b74bf9f6eca5250f4b06e083`, the exact 126-byte statement, and absent target report. A bad third corpus is rejected. |
| Full-corpus guard order | A separate instrumented call records all three completed streaming authentications before the first parsing read. Archival input/replay entry points and subprocess execution were replaced by failing guards; none were reached. This observation is not mislabeled as a CLI run. |
| Explicit dependencies | Local SymPy 1.14.0 and mpmath 1.3.0 wheel byte/SHA256 pins independently match the frozen constants. Actual CLI rejects mutated wheel bytes and missing wheels. No download, installation, or installed-site runtime is used. |
| Default build policy | A fresh build outside the input tree performs a real replay. Missing dependencies fail, with no output or authentication-only fallback. `build --verify-only` is rejected by the actual CLI. An existing output is rejected and its bytes remain unchanged. |
| Physical output containment | Actual CLI rejects output in an indexed nested directory, its case alias, and its actual `/System/Volumes/Data` firmlink alias. It also rejects a symlinked output ancestor. These tests omit dependencies deliberately, and the containment error precedes the missing-dependency error. |
| Raw ZIP structure | Actual current CLI rejects a trailer, local/central disagreement, symlink Unix mode, wrong timestamp, and a coherent ZIP with an extra byte inside the first member's declared DEFLATE region. Python's ordinary ZIP reader successfully reads the unchanged payloads of that last fixture; the independent exact-consumption check rejects it. |
| Copied publication objects | Actual current CLI rejects disagreements between outer and portable TeX and between outer and portable metadata. The tool fixes the 12 metadata keys, title, sole creator/ORCID, and exactly two deposit asset names/paths. |

The raw ZIP code explicitly checks contiguous local records from offset zero, contiguous central records, one terminal EOCD, sorted exact member names, matching raw local and central metadata, Unix regular-file modes, generated timestamp, no extras/comments, bounded decompression, CRC/content through the ordinary reader, and complete raw-DEFLATE consumption. It also rebuilds generated bytes with the same ZIP implementation and zlib runtime. This is a meaningful defense against a representation accepted by a permissive ZIP reader.

The output preflight enumerates the root and every indexed input directory, compares `(st_dev, st_ino)` with the proposed output parent's entire ancestor chain, and runs before optional replay, scratch creation, or output creation. Final publication of an output uses a fresh exclusive temporary file and a no-overwrite hard link. The code order establishes preflight-before-replay; absence of leftover temporary files by itself would not prove that no transient file was created.

## Exact limitations and remaining gap

1. **Resource-limited supplementary test:** a first private wheel-copy setup hit ENOSPC, then a requested hostile-environment full replay returned ENOSPC before it could establish success. Both failures are in the research log and receipts. I removed only my partial owned wheel copy and used an immutable hard link for unchanged SymPy. The outer authentication-only hostile-path test subsequently passed, with hostile startup hooks and fake modules unexecuted. The separate hostile-environment *full* replay remains unestablished; the earlier four full replays and their actual isolation measurements stand independently.
2. **Trusted interpreter boundary:** the selected CPython 3.14.6 interpreter, standard library, native extensions, and standard-library bytecode are trusted and are not byte-pinned by this tool. Explicit authenticated wheels are copied privately and imported directly as ZIPs under `-I -S -B`. Wheel imports and measured flags were exercised; upstream wheel provenance was supplied, not newly re-fetched by this reviewer.
3. **Filesystem race boundary:** checks resist the tested static symlink, case, and firmlink aliases, but they do not constitute an OS sandbox or an atomic directory-descriptor design. Concurrent adversarial changes to parent directories between checks and later path operations remain a TOCTOU boundary. Do not claim race-proof containment or resistance to a malicious OS/runtime.
4. **Runtime-specific ZIP bytes:** exact rebuild is only for the same input bytes, Python ZIP implementation, and zlib runtime. Cross-runtime compressed-byte equality is not claimed.
5. **Paper and mathematics:** current-publication verification authenticates bytes, enforces copied-object equality, and checks only a `%PDF-` PDF prefix. It does not parse a PDF or establish TeX/PDF semantic agreement, theorems, priority, novelty, or human review. My current-publication fixture deliberately contains a tiny prefix-only PDF fixture. A final preprint, its rendered PDF, its content, and whole-package clearance require the parent's subsequent independent reviews.
6. **Finite coverage:** successful adversarial controls are reproducible evidence for these mechanisms, not a proof that every malformed input is rejected and not a mathematical formal proof. Primary-source PDF theorem content was not re-reviewed in this tool audit, and the PDF marker was not rerun.

## Artifacts and privacy

`SAFE_MANIFEST.json` is the sole explicit release allowlist for this review and intentionally excludes itself from its member hash list. The safe receipts redact local workspace/interpreter path prefixes while preserving flags, measured outputs, hashes, case labels, error categories, and the failed expectation. Safe reproduction code differs from exact executed code only by replacement of a single supplied local workspace path with a path derived from the review location; this is documented with both code hashes. Exact executed scripts, unredacted receipts, all fixtures, original/native bodies, PDFs, wheels, and temporary data remain private and are not allowlisted. No Git/index/ref/config/remote/PR/queue/Zenodo/GWS write or external communication was performed.

Final completion estimate for this scoped verification-tool review: 100%. The broader discovery/publication goal is not assigned this percentage.
