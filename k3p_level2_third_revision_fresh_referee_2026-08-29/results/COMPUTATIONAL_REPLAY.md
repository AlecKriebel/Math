# Computational replay and isolation audit

## Execution boundary

All credited package execution used a byte-preserving copy at
`package_copy/`; the delivered package was never an execution working
directory.  A tested macOS `sandbox-exec` profile denied network access,
standard credential locations, the live source repository, the referee result
tree, `/Users/Shared`, `/Volumes`, `/private/tmp`, and writes outside the
single copied run workspace.  Positive controls allowed the pinned interpreter,
its four modules, and a system subprocess.  The profile is
`logs/offline_credential_free.sb`, SHA-256
`8daf2a82cde2cee9e99cb3500ba5cce90cc8388fdff33e047342d8dd6c1cf4a3`.

A referee-owned supervisor created no-replace transcripts, an inode-bound
single-run lock, external before/after package and virtual-environment
inventories, a six-hour hard wall, and full-process-tree termination on
signals.  The supplied runner already blocks on each child; the long
regeneration was launched **once** and awaited through that same process.  It
was not polled by invoking another runner and was not restarted.

The credited runtime was:

- macOS 26.5.2, arm64;
- Python 3.14.6, interpreter SHA-256
  `b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf`;
- mpmath 1.3.0, networkx 3.5, numpy 2.5.2, sympy 1.14.0;
- requirements SHA-256
  `5a731eb61d5928e5b724c065e64d64af03804d25e25b49928f369d9d6b4da95b`;
- `PYTHONHASHSEED=0`, `PYTHONNOUSERSITE=1`,
  `PYTHONDONTWRITEBYTECODE=1`, `LANG=LC_ALL=C`, `TZ=UTC`, and umask `0022`.

The exact environment record is line 1 of
`package_copy/review_runs/20260829T172726.410212Z/regenerate/transcript.log`.
The external supervisor found the sealed package and shared virtual
environment unchanged before/after.

## Package integrity and plan

The initial checker found 624 sealed payload files (160,624,411 bytes) and 595
inner core members (159,918,762 bytes), checked file modes, and found no
symlinks.  The proof-source and package-builder commit is
`738b662aa9c4e6201277f60b249afd4de9bcd9d6`.  The outer manifest and checksum
ledger SHA-256 values are
`950eea1a281b58fd1139ceb0e7f1a645d41a8d1f5a9a5dbe60060e41cd5e07a2`
and
`58121c10dff3d3b1ca6a626d2bbe5d8c0abd73b624e039ddc06363703f91fd54`.

The supplied plan mode reconstructed exactly 55 portable regeneration
commands, with no package or environment drift.  Static census distinguished
4 portable verify commands, 55 portable regeneration commands, 56 native
regeneration commands, and 59 commands in combined `all` mode.  The sole
portable omission is the Git-bound, nonmathematical release-engineering
mutation suite.

## Bounded verifier phase

Each of the four verify command bodies passed.  The integrated mathematical
gate performed 20/20 fresh child replays and returned `CERTIFIED`; its report is
`package_copy/review_runs/20260829T162640.838120Z/verify/integrated_fresh_report.json`,
SHA-256
`9cdd9c78f9725012f21a3d3ffb77a4b8b093da11d50283e97ed81be47f161fc6`.

The supplied top-level runner nevertheless returned `FAIL`, because ten
byte-identical regenerated JSON files changed mode from sealed `0644` to
`0600`.  This first phase used an earlier sandbox whose host-read boundary was
broader than described, so it is corroborative mathematical replay, not the
basis for the final isolation claim.  The policy was hardened and tested before
the long run.

## Exact-once 55-command regeneration

The regeneration began at `2026-08-29T17:27:24Z` and ended at
`2026-08-29T19:51:38Z`.  External elapsed time was 8,654.143 seconds; the sum of
the 55 child timings was 8,648.514 seconds.  **Every command body and required
sentinel passed.**  The main expensive steps were:

| Command | Seconds | Result |
|---|---:|---|
| graph-derived cut-topology regeneration | 282.710 | PASS |
| complete 405,216-presentation four-port producer | 764.278 | PASS |
| 133-row non-four anchor producer | 178.923 | PASS |
| complete restoration producer | 603.529 | PASS |
| hour-scale one-/two-port probe producer | 2,842.743 | PASS |
| semantic replay of all 574,535 probe rows | 369.945 | PASS |
| probe mutation suite | 180.905 | PASS |
| 20-child integrated fresh replay | 2,997.875 | PASS |
| 27 classification mutations | 14.731 | PASS |

The internal transcript is
`package_copy/review_runs/20260829T172726.410212Z/regenerate/transcript.log`
(102,036 bytes, SHA-256
`297dcac7a8df8d4a5663e66469c41df3f96c1694446d42118a3fe3e62a989862`).
The external transcript is
`logs/supervisor_regenerate_20260829T172724.243510Z.log` (SHA-256
`14a78aab5b9e8dc19108fc0def8f2694385b26492472239cbf0e390e597003b3`).
The final integrated report is
`package_copy/review_runs/20260829T172726.410212Z/regenerate/integrated_fresh_report.json`,
SHA-256
`75413e1593b3c96a954a9e5d6eac88e69fdc6a204e6c7d19d83ab83251baa786`.

### Official runner result: FAIL

After those 55 passes, the runner correctly failed its final inventory gate.
Eleven files changed only from mode `0644` to `0600`, with identical byte
counts and SHA-256 values:

1. `bridge_fibre/primary_exact_evidence.json`
2. `cut_recovery/strong_crossbridge/topology_regeneration/CUT_TOPOLOGY_REGENERATION_REPORT.json`
3. `four_port_atlas/primary_exact_evidence.json`
4. `marginals/primary_exact_evidence.json`
5. `model_domain/primary_exact_evidence.json`
6. `reproducibility/primary_gate_report.json`
7. `reproducibility/strong_class_cut_transfer_gate_report.json`
8. `three_port/primary_exact_evidence.json`
9. `topology/primary_cherry_evidence.json`
10. `topology/primary_double_theta_evidence.json`
11. `topology/primary_rooting_census_evidence.json`

The cause is visible in the package source: `verify_primary.py:79-88`,
`verify_cut_topology_regeneration.py:185-194`, and
`strong_cut_transfer_gate.py:373-381` create replacement files with
`tempfile.NamedTemporaryFile`, whose private `0600` mode survives the atomic
replace.  The runner explicitly inventories modes
(`referee_tools/run_active_verifiers.py:45-78`) and rejects every undeclared
change (`:593-611`).  Thus the runner's `FAIL` is correct and the package's
claim that the extracted portable regeneration completes successfully is
false as delivered.  The mathematical byte outputs did reproduce.

A repair is small: assign the intended canonical mode to the temporary file
before replacement (or preserve the old destination mode), then add a clean
mode-preservation control and rebuild the outer mode seal.  The full long
producer need not be used to debug the primitive, but a final release claim
requires one successful top-level regeneration after repair.

## Independent referee computations

Seven referee-owned checks ran without importing package code and passed in
40.455 seconds.  Their suite report is
`independent_checks/results/fresh_spots_20260829/SUITE_REPORT.json`, SHA-256
`f5ed017d3a040889af9c559198302229dd0a0bceba884a5dc526035d67930386`.
They checked:

- inverse Fourier, principal and CT domains, exact six-dimensional cherry
  inverse, all six tree--sunlet circuit pullbacks, and 5,000 strict trials;
- all six `H_14` permutation pullbacks, rank 14, a nonzero gradient,
  irreducibility, the common strict-CT point, and smoothness;
- bridge anchor ranks/determinants for degrees 3--16, exact gauge cancellation,
  and 2,000 capped principal/CT gluing trials;
- representative exact four-port quartic/rank witnesses and positive
  saturation divisors for all five directed-rank exception types;
- the full 36,824-row restoration and 574,535-row probe census, plus five
  independently reconstructed semantic probe rows;
- literal Krawczyk self-inclusion, interval rank 15 on both boxes, physical
  margins, and the declared slice-only uniqueness scope; and
- an independent closed-form count of all 808,642 balanced words and an exact
  derivation of the displayed-tree 5x5 minor.

The spot-check scripts were referee code written for the preceding revision
and executed afresh against this package; their paths and SHA-256 values are
recorded in the suite report.  They are independent of package modules but are
representative tests, not replacements for the full enumerations.

## Git-bound release-engineering suite

The excluded suite was reproduced once in a clean, detached, self-contained
partial Git checkout at commit `738b662...9d6`, with no alternates or remote
dependency.  Under a separate network-denied profile, all 32 hostile packaging
mutations were rejected and all 11 controls passed in 7.118 seconds.  The
fresh pretty report was byte-identical to the sealed report.  See
`results/RELEASE_ENGINEERING_REPLAY.json`; transcript SHA-256 is
`dbcd714c19dc38a998edb029c90396e9472c7425244e0d968e3d6b9f571ed1da`.

This is release engineering, not evidence for a mathematical lemma.

## Source archives and PDF builds

An independent canonical ZIP implementation reconstructed both delivered
source archives byte-identically from the exact commit's Git blobs. The
article and supplement archives contain 23 and 1 TeX/Bib source members,
respectively, with zero mismatch. Under a network-denied sandbox, the
supplement's one package-command invocation performed its required two internal
Tectonic builds and both matched the delivered PDF exactly.

The article command was invoked once and was not relaunched. It stopped before
either internal build completed because the initial referee sandbox omitted a
SystemConfiguration Mach lookup required during Tectonic initialization. This
is recorded as **inconclusive**, not PASS and not an observed source/PDF
mismatch. The exact tool/cache hashes, attempt seals, transcripts, prior
same-source corroboration, and static limitations are in
`results/SOURCE_ARCHIVE_REPRODUCTION.md`.

The package pins the Tectonic executable but not its resource bundle/cache,
inherits the caller's full environment, and does not deliver sealed
final-commit reproduction reports/transcripts. These are reproducibility
limitations independent of the mathematical replay.

## Cut-certificate fidelity mutation

A fresh coherent payload mutation replaced all eight nonfinal implication
`claim` strings in `K3P_DIRECTED_CUT_INCLUSION_EVIDENCE.json` with one
semantically false placeholder while preserving IDs, edges, and the final
conclusion.  Both ordinary and optimized advertised semantic verifiers passed
the resealed mutant, each reporting 204 directions, 15 proof steps, and 39
mutations.  Evidence:
`independent_checks/results/c1_claim_fidelity/REPORT.json`, SHA-256
`390b88f81a04b631cc41a67ab4ad18ad7c7881bc47b744e19341cd23a956dc17`.

This does not refute the handwritten cut proof, which was independently found
sound and whose finite primitives all replayed.  It does show that the
certificate/verifier claim of semantic binding is stronger than the code.
