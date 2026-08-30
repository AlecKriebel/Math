# Fresh K2P-SAME R6 referee log

## 2026-08-29T12:36:14-0700 — review opened (2%)

- Scope: a complete fresh adversarial review of
  `K2P_Principal_D_Plus_Referee_Package_20260829.zip` under the previously
  supplied referee protocol.
- The editor's submission-ready statement, 41/41 replay claim, archive
  hashes, commit, tag, and R5 repair claims are assertions to be checked.
- Source ZIP SHA-256 independently matches the asserted
  `fef886379d9682586920a9f1112465dccab75267dbdd87a5b87b38dc4dbea513`;
  this is identity evidence only.
- ZIP safety scan: 495 regular members, one top-level root, 483,751,133
  uncompressed bytes, and no absolute, traversal, backslash, or duplicate
  member names.
- Pristine and disposable extractions each contain 495 files. Authoritative
  package files will remain unmodified; all producer executions will occur in
  the disposable copy.
- Long scripts will be launched once and blocked on until completion.
- No external contact is authorized or planned.
- Best-guess completion: 2%.

## 2026-08-29T12:49:30-0700 — preliminary gates and first fresh defect (18%)

- Independent complete-tree inventories agree for the pristine and disposable
  extractions: 495 regular files, 483,751,133 bytes, no symlinks, inventory
  payload SHA-256
  `fa20f31760755fcf619212d638748d3928e162e9b650e84a12b56495c3708446`.
- A clean external Python 3.14.6 environment was built with NetworkX 3.5 and
  SymPy 1.14.0. The portable-bundle gate and frozen release-lock gate pass:
  408 files, 479,383,009 bytes, content root
  `ed3beb4fca8338a3b97c7e5a0ff2bb58460ee7a244ea030bb7d3f837b5563d73`,
  231 outer locked files, and no declared blockers.
- The first static-source run with only the external environment failed
  `CROSSWALK_PATH_MISSING:.venv/bin/python`. This is preserved as a
  noncontrolling environment-setup failure: the documented package protocol
  requires a local `.venv` for this gate. After creating that environment in
  the disposable copy, the static source audit passes.
- The PDF double-build/omission gate, theorem crosswalk gate, revised-bundle
  producer, and independently implemented revised-bundle checker all pass.
- Fresh defect R6-F1: the current, non-historical
  `proof_compression_submission/probe/PROBE_WORD_THEOREM.md` asserts that its
  current coverage artifact has file SHA-256 `3791e4bb...` and logical payload
  `1d424802...`. The actual sealed
  `PROBE_WORD_COVERAGE.json` has file SHA-256 `c2e32b37...` and valid payload
  `d66b2824...`; the machine crosswalk binds the latter. A fresh execution of
  `verify_probe_word_theorem.py --check` passes on the current artifact and
  independently confirms 176 anchors, 29,964 one-port rows, 544,571 two-port
  rows, and 67,741 transports. Thus this is presently an internal
  authority/provenance inconsistency, not a counterexample to the word
  theorem. Its final severity remains under review.
- Best-guess completion: 18%.

## 2026-08-29T16:28:23-0700 — compact and adversarial gates (62%)

- The unified quick replay passes all 23 layers in 420.921 seconds with
  1,390,886,912 bytes peak RSS. Compression verification, the seven-command
  old/new replay, all 11 compression mutations, and all 12 telemetry tests
  pass.
- The 37-case crosswalk/revised-bundle mutation suite passes in 3,768.434
  seconds; all resealed duplicate-name, noncanonical-compression, omission,
  telemetry, metadata, PDF, frozen-evidence, and optimized-mode attacks were
  rejected.
- Two clean relocations were extracted under different parent and project
  names and run with the same external environment and caller-owned external
  reports. Alpha passed 25/25 in 4,324.256 seconds. A simultaneous beta run
  reached the twenty-third outer gate but then failed from host temporary-disk
  exhaustion while cloning the last direct-terminal mutant; this resource
  failure is preserved as noncontrolling evidence.
- Beta was rerun once serially, without changing its source tree, and passed
  25/25 in 4,213.676 seconds. Alpha and beta reports are byte-identical:
  9,146 bytes, SHA-256
  `0bc92a5f1f8328b6ce51945233a5152f5a28e96a99f538568bf9d057f92a8a55`.
  Pre/post inventories for both relocations are identical, with no symlinks,
  bytecode caches, additions, omissions, or changed source bytes.
- Independent computational review reconstructed raw4 (405,216) and theta2
  (2,946,240) primitive partitions and roots, verified restoration/probe joins,
  checked 432 exact rational physical inequalities, and confirmed the raw4
  12-case and theta2 10-case complete-ledger semantic attacks reached the
  production independent verifier with zero survivors or drift.
- Review-generated disposable copies and duplicate rebuilt archives were
  removed after their inventories and hashes were sealed; they are not
  recoverable, but contain no unique source or user data.
- R6-F1 remains the sole established blocker. No mathematical counterexample
  or computational-classification failure has been found.
- Best-guess completion: 62%.

## 2026-08-29T18:43:00-0700 — final disposition and evidence seal (100%)

- The fresh full replay passed all 41 layers in 6,309.976 seconds with
  2,548,711,424 bytes peak RSS. Its report SHA-256 is
  `23c78f94072a993cad954d9e72615bd01acaf8f5842722ffecd133d631556b74`.
- Both controlling clean relocation runs passed 25/25 release-mutation gates,
  produced byte-identical external reports, and left their source inventories
  unchanged. The first parallel beta attempt failed only from host temporary
  disk exhaustion and was not treated as scientific evidence; its single
  serial control rerun passed.
- Independent mathematical, computational, provenance, archive, source/PDF,
  and R5-repair audits all pass within their stated evidence boundaries. No
  theorem counterexample or central finite-classification defect was found.
- Sole blocker R6-F1: the current C09 word-theorem narrative prints obsolete
  file and logical-payload digests for its current coverage JSON. The actual
  coverage artifact replays successfully. This is a reproducibility/current-
  authority inconsistency, not a failure of C09's mathematical/computational
  claim.
- Final scientific recommendation: HOLD. Mathematics PASS; computational
  evidence PASS; reproducibility FAIL; human metadata PASS; release readiness
  HOLD. All C01--C13 are PASS; package-consistency row P01 is FAIL.
- The final report and companion ledgers received independent adversarial and
  exact-fact checks. No authoritative package file was edited and no person
  was contacted.
- Best-guess completion: 100%.
