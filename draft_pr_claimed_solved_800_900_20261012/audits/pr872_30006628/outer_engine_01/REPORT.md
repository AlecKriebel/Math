# PR872 current outer verifier implementation

The implementation is ready for parent integration and tests on the actual assembled publication tree. This is an authoring and focused software-validation result, not final package acceptance or an independent mathematical or priority decision.

## Interface and trust

Run Python 3.10 or later with `-I -S -B`, optionally adding `-O`, followed by `verify_current_publication.py OUTER_MANIFEST_SHA256`. `--root` selects the directory containing the current root wrapper and `PUBLICATION_MANIFEST.json`; the default is the script directory. `--full` forwards finite replay to the authenticated inner verifier. Supply `--catalog`, `--problems`, `--reports`, and `--pdf-dir` together or omit all four. Supplied source locations require `--full` and are forwarded as absolute paths without resolving leaf aliases.

The caller must authenticate startup script bytes and the outer manifest pin using a separately trusted receipt before executing any downloaded script. A manifest that merely contains its own verifier hash is not an independent trust anchor. Once running, the wrapper also checks that its own bytes match the externally authenticated root copy before it executes inner code.

A selected root or its outside ancestors may resolve through aliases, as in the canonical inner verifier. Aliases, FIFOs and other nonregular entries inside the selected package are rejected before payload reads. No guarantees against a hostile actor continuously replacing filesystem objects during execution are claimed.

## Implemented consistency checks

- Strict JSON rejects duplicate keys and nonfinite numbers. Inventory rows have exact schemas, bounded integer byte counts, SHA256 pins, safe relative paths, no duplicates or file/directory collisions, and bounded total payload size. Closed-tree traversal also rejects unlisted files and unlisted empty directories.
- The exact current outer schema is `random-property-t-current-publication-v1`, problem `30006628`; its manifest excludes itself. Outer counts are dynamic. An externally sealed later `PUBLICATION_RECEIPT.json` can be added without changing the verifier.
- The current preprint directory contains exactly the requested 11 core files. Nine duplicated preprint/portable files, including the flat inner PDF, metadata and package index, must agree byte for byte.
- Current wrapper metadata, preprint metadata, deposit metadata and portable metadata must agree. Deposit filenames and relative upload paths match the two instructed PDF/ZIP entries exactly; the deposit object has exactly `metadata` and `files` fields.
- The portable index has its own exact schema and closed authenticated member set. The frozen source manifest pin is `4589f9b70e9a65ae67356544b5ad59644290902bb9b3df80406710a22559e3f8`, identifying PR872 head `e3d77731b45b5f463df46e769faa01d65fe193ec`. All 15 originals are authenticated by byte counts, SHA256 and Git blob identifiers. The 13 unreplaced root copies must equal those frozen originals; the original README and manifest remain unchanged within portable `source/`.
- The verification ZIP must contain exactly the sorted portable members, with byte-identical contents. New members must have Unix regular 100644 metadata, no encryption, permitted UTF8 flags only, deflate compression, the builder's fixed date, and no extra fields or comments. Declared sizes are checked before bounded reads. The legacy archives inside portable source are opaque here; their implicit regular 0600 metadata is handled by the authenticated inner checker, not by the new-archive rule.
- The wrapper creates a complete disposable snapshot from authenticated in-memory portable bytes and executes its verified inner verifier with isolated flags, the authenticated index hash, and optional `--full`. Optimized mode propagates. It neither imports code from the input tree nor executes the historical outer wrapper. No Git, network, queue, PDF or metadata mutation is implemented.

PASS reports dynamic outer and portable counts, original count 15, preserved root count 13, and the inner result. Its scope explicitly excludes mathematical proof and priority certification.

## Focused validation

The public harness creates and removes a minimal synthetic outer fixture using the current canonical inner code, current note/support copies, the frozen 15 originals, and their three archives. This deliberately omits the final package's audit-evidence assembly, so it is not a candidate publication artifact. Temporary files, including nested child replays, are confined to the harness's ignored private work directory.

The final run passed six positive runs and 36 intended rejections across ordinary and optimized Python 3.14.6. Positive runs comprise default verification, full relocated finite replay, and a resealed additional publication receipt in each mode. Each full run checked 14 exact original positive/negative diagnostic receipts and reported no historical-wrapper execution. These are repeated finite diagnostics, not new asymptotic or proof validation.

The 18 intended rejection cases in each mode cover wrong external pin, duplicate JSON key, boolean byte count, unsafe path, unlisted file, unlisted empty directory, missing file, leaf symlink, FIFO before read, altered inner verifier before execution, metadata mismatch, changed preserved original, inconsistent duplicated README, executable ZIP metadata, reverse ZIP order, altered ZIP member, partial optional inputs, and source inputs without `--full`. The altered verifier's side-effect marker was not created. Guards use explicit exceptions rather than assertions.

The final wrapper SHA256 is `57b78a4813329b5964f94879b3fbff796d2e0d1e1298f3889b804117ec06d8fe`.

## Remaining work and limits

The parent must integrate the template, read it, and run it against the real final assembly, including the separately supplied-source positive path if desired. Two fresh final package adversaries are outside this task. No second Python runtime, full final audit-evidence assembly, true publication-receipt metadata, ZIP rebuild reproducibility, mathematical theorem, source-priority coverage, PDF layout, Zenodo upload or sheet operation is certified by this subtask. No core publication files were modified, and no external outreach occurred.
