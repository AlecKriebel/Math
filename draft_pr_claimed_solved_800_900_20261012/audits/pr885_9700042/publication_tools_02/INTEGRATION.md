# PR885 portable verification integration

This folder is engineering work. It is neither of the two required new sequential final whole-package reviews. No paper metadata, paper hash, page count or final seal is invented here. Original proof-search effort remains 5/5. No Git, index or remote mutation is performed by these tools.

`portable.py` is the only executable to ship from this engineering folder. It is self-contained and uses Python standard-library modules plus the original packet's required system `patch` utility. Authenticate this startup program independently before executing it. Its own runtime comparison against an externally pinned index is not a substitute for authenticating startup code.

## Portable tree and external trust root

Place all 30 unchanged original files under `source/`, preserving their relative names. Place the exact external `SOURCE_MANIFEST.json` under `root_evidence/SOURCE_MANIFEST.json`. Place `portable.py` at the portable root. Add the actual authored `note.tex`, the original/initial safe audit and priority artifacts, and explanatory documentation only through an explicit authored safe-file allowlist. Do not recursively include this entire engineering folder. Exclude private fixtures/receipts, source bodies, whole corpora, local paths, credentials and the two final reviewer reports. The final reviewer reports sit outside the sealed ZIP.

The caller writes UTF-8 `package_index.json` with exactly these fields:

```json
{"schema":"oriented-flow-9700042-verification-v1","problem_id":"9700042","files":[{"path":"portable.py","bytes":123,"sha256":"64 lowercase hexadecimal characters"}]}
```

The row above is schema notation, not a valid pin. Actual rows enumerate every regular file except `package_index.json` itself. Rows have exactly `path`, integer `bytes` and lowercase hexadecimal `sha256`. Filenames are case-unaliased ASCII safe relative paths. All entries including directories must belong to the derived closed tree. Extra directories, symlinks, FIFOs and device entries are rejected without opening their bodies. JSON files reject duplicate object keys, nonfinite numbers and floating overflow. File rows additionally reject boolean/floating byte counts, duplicates, directory aliases and file/directory collisions.

The SHA-256 of the complete actual index bytes is the required external command argument. Root manifest bytes are additionally pinned to `6b1d1281848190f616f6759f40454183c937b65e65219b893202254be6c3617d`; all 30 original SHA-256 and Git-blob identities, 214,980 total bytes, exact head and 5/5 effort are rechecked before any original code executes.

## CLI

Use a Python version at least 3.11. Every command requires actual interpreter flags `-I -S -B`; optimization may also be selected with `-O`.

```text
python3 -I -S -B portable.py verify INDEX_SHA256 --root PORTABLE_DIRECTORY
python3 -I -S -B -O portable.py verify INDEX_SHA256 --root PORTABLE_DIRECTORY
python3 -I -S -B portable.py verify INDEX_SHA256 --root PORTABLE_DIRECTORY --verify-only
python3 -I -S -B portable.py build INDEX_SHA256 OUTPUT_DIRECTORY/oriented-flow-verification.zip --root PORTABLE_DIRECTORY
python3 -I -S -B portable.py current CURRENT_MANIFEST_SHA256 --root CURRENT_DIRECTORY
python3 -I -S -B portable.py current CURRENT_MANIFEST_SHA256 --root CURRENT_DIRECTORY --verify-only
python3 -I -S -B portable.py source-only --catalog CATALOG --problems PROBLEMS --reports REPORTS
```

`build` requires a fresh output path outside the input tree and an existing output parent. It performs the default complete replay before publishing its ZIP and cannot bypass replay with `--verify-only`. It uses fixed metadata, sorted members, DEFLATE level 9, a closed raw ZIP parser and a second exact in-memory rebuild. Atomic no-clobber publication uses a same-filesystem hard link. Failure does not publish a partial ZIP. Same-runtime reproducibility means the same Python ZIP implementation and zlib; compressed-byte agreement across different runtimes is not promised.

Default `verify`, `build` and `current` authenticate all package bytes before copying exactly the 30 originals to private scratch. Each default command runs the exact original `verify_packet.py` body once through a narrow current launcher, with one direct isolated subprocess and exactly 64 original nested subprocess requests: 20 positive checkers, 20 forced-assertion failures, 20 corrupt-checker preexecution rejections and four patch invocations. The interceptor accepts only the exact reviewed schedule, flags, bootstrap, arguments, hashes, cwd/keyword patterns and patch bytes. It injects actual child `-I -S -B` while preserving requested `[]`, `[-O]`, `[-I]` and `[-I,-O]` separately. Child flags are measured inside each executing interpreter before the unchanged original bootstrap, whose checker compilation remains optimize=0. The direct root's effective flags are measured too.

Root JSON is compared semantically after excluding only the `python` version field. Current and frozen versions and actual root stdout byte/hash are reported separately. Every positive generated JSON and stdout is compared against exact frozen bytes, with author C1's 1,253-byte stdout separately pinned from its 3,971-byte JSON output. Every original scratch file is authenticated again after replay. These are finite diagnostics and byte checks, not theorem or novelty verification. The historical root's accepted JSON/filesystem boundaries are preserved and disclosed in its original artifact audit; only this current outer index has the stricter format boundary.

`--verify-only` authenticates bytes/structure and runs zero archival code. The optional corpus paths must be supplied all together. They may accompany `verify`/`current` or be used with `source-only`, which does not read any archival file at all. All three complete corpora are authenticated before any extraction. The exact 5,104-byte canonical pair and 145-byte statement are then checked. No corpus or primary body is copied or shipped.

Optional `--primary-dir DIRECTORY` authenticates four complete source bodies by fixed names documented in `PRIMARY_SOURCE_PINS.json`: the original Aldous, Deuschel–Zeitouni and van den Berg–Jonasson pins plus the 967,612-byte Basdevant–Gouéré–Théret primary PDF. It can accompany `verify`, `build`, `current` or `source-only`. Bodies must already exist in the selected directory. Hash agreement does not establish theorem interpretation.

## Current publication wrapper

The current root contains the actual `oriented-flow-note.pdf`, actual `note.tex`, `oriented-flow-verification.zip`, a root copy of the identical `portable.py`, a `verification/` portable tree, optional explicitly indexed safe evidence, and two current metadata JSON files. `CURRENT_PUBLICATION.json` must have exactly:

```json
{"schema":"oriented-flow-9700042-current-layout-v1","problem_id":"9700042","portable_prefix":"verification","zip_path":"oriented-flow-verification.zip","pdf_path":"oriented-flow-note.pdf","tex_path":"note.tex"}
```

The portable prefix may use another safe relative directory. The two release asset names and `note.tex` are fixed. Actual `note.tex` must be byte-identical in outer and portable trees. The outer PDF must have PDF magic and is byte-pinned by the outer manifest; PDF rendering, paper claims and mathematical review remain separate work.

`CURRENT_PUBLICATION_MANIFEST.json` has exactly `schema`, `problem_id`, `files`, with schema `oriented-flow-9700042-current-publication-v1`, problem string `9700042`, and the same strict pin-row schema. It enumerates every current-root file except itself. Pass its complete independently computed SHA-256 to `current`. The wrapper authenticates the closed outer tree, typed portable index, fixed originals, tool/TeX copies, ZIP metadata and every member, then recomputes the exact same-runtime ZIP bytes before optional default replay. Neither index nor wrapper claims that arbitrary additional indexed files are safe for publication: the human-authored safe-file allowlist remains necessary.

## Engineering controls and receipts

`engineering_controls.py --controls` creates one private fixture containing only originals, manifest and helper; it never creates a paper. It exercises real CLI malformed input/flags with a Python audit hook that measures zero subprocess launches before rejection, plus bounded raw ZIP controls. All writes remain in `private/` and this folder's explicitly authored receipts. Preserve any failed setup/replay receipt honestly. Do not ship this control program, private fixture or raw replay failure text.

The fixed ZIP epoch is explicitly `2026-10-16T00:00:00Z`. The current wrapper also requires byte-identical `metadata.json` and `zenodo-deposit.json` in outer and portable trees. Metadata has exactly the twelve keys `title`, `upload_type`, `publication_type`, `publication_date`, `version`, `description`, `creators`, `access_right`, `license`, `keywords`, `references`, `related_identifiers`; typed values and the parent's actual title/date/version/publication/preprint/open/license/ORCID are checked. Kit shape is exactly the existing repository convention, with no extra schema field:

```json
{"metadata":"actual parsed metadata.json object, not this placeholder string","files":[{"name":"oriented-flow-note.pdf","path":"oriented-flow-note.pdf"},{"name":"oriented-flow-verification.zip","path":"oriented-flow-verification.zip"}]}
```

The placeholder line describes the schema only and is rejected as input. The actual nested metadata must be a typed object exactly equal to parsed `metadata.json`, including references and related identifiers. This check does not create or upload a deposition.
