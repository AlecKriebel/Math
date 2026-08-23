# Independent R3 re-review report

**Manuscript:** *Local Complete-Graph Optimality at Fitness Two and
Strong-Selection Rigidity under Death--Birth Updating*  
**Package:** `paper_i_complete_graph_extremality_referee_package_2026-08-22_r3`  
**Review date:** 2026-08-23\
**Verdict:** **Fully validated**

## Executive assessment

R3 closes the two reproducibility defects left by the R2 review without
changing the mathematics. The package-root `run_all_referee_checks.sh` is now
the only route represented as certifying package identity and execution of the
delivered source. It rejects inherited `PYTHON`, reconstructs a fresh source
tree from verified regular archive bytes, compares exact regular-file and
implied-directory inventories before project import, rejects links, special
nodes, cache directories and bytecode, and directs every later project import
to a fresh private empty cache prefix.

The certified command was run in a stripped environment with an absolute
Python 3.14.6 path and private home, cache, and temporary directories. It
returned status 0. It rejected all six advertised hostile cases for their
intended reasons, installed only hash-accepted wheels, ran six unit tests and
all 17 directly invoked verifier/cross-check programs, kept the controlled
project cache empty, accepted the pinned Tectonic resource record, rebuilt all
30 pages, and reproduced the delivered PDF byte-for-byte at SHA-256
`5d2bc6cfa9d02b21e816d3dd30252d067e23b51ecd0c58bb8c3cfb116ab937bd`.

The R2-to-R3 regression is scientifically null. All theorem-bearing LaTeX
except Section 7's operational reproducibility prose is byte-identical; all 20
scientific-check programs and all 406 scientific predicates are byte-identical.
No hypothesis, quantifier, formula, equality case, endpoint, exact margin,
eigenvalue, limitation, nonclaim, or certificate hash changed. A separate
standard-library `fractions.Fraction` implementation, importing no delivered
module, again passed nonsymmetric collision, orientation/gauge, Hessian-sector,
strong-selection, triangle, weighted-`K_4`, monotonicity, and endpoint checks.

One low-priority test-hardening opportunity remains. The malicious-bytecode
fixture writes `PYCACHE_EXECUTED` relative to the caller's working directory,
whereas the launcher searches for that marker only below the contaminated
tree. The valid bytecode is still rejected by its unique exact-tree diagnostic
before any project import, and static call-order inspection independently
establishes that it is not executed. This marker-location issue therefore does
not reopen the R2 bypass or defeat any R3 claim. Rooting the marker beside the
fixture would make the defense-in-depth assertion self-observing under every
caller directory.

## Scope and independence

The editor's summary, package documentation, expected messages, manifests,
and prior conclusions were treated as claims. Review work used the isolated
copy at
`/Users/alec/Documents/Math/complete_graph_extremality_r3_rereview_2026-08-23/work/package`.
The original R3 delivery remained unchanged and compared recursively equal to
the review copy both before and after testing.

No person was contacted, no artifact was uploaded, and no external system was
changed. Network retrieval was limited to the configured Python artifact
source and Tectonic's standard resource endpoint during the package's own
reproduction procedure. All hostile mutations were confined to disposable
copies. Delivered Python was not executed or imported until independent static
reviewers cleared the pre-execution gate.

The assessment combines:

- the original first-principles proof and software audit;
- the R2 re-review and its reproduced fake-interpreter and timestamp-bytecode
  defects;
- an exhaustive R2/R3 source, scientific-predicate, PDF-text, and rendered-page
  regression;
- an independent static trace of the R3 certified route and every pre-import
  boundary;
- a fresh certified replay under a stripped environment;
- expanded independent hostile-node and timestamp-bytecode tests; and
- a fresh run of the independent exact rational checker.

Primary evidence is preserved in `records/COMMANDS.log`,
`records/STATIC_CERTIFIED_ROUTE_AUDIT.md`,
`records/static_certified_route_commands.log`,
`records/MATH_PDF_REGRESSION.md`, and
`records/MATH_PDF_REGRESSION_COMMANDS.log`.

## Frozen identity

| Item | Independently observed result |
|---|---|
| Scientific source commit | `b9a415f763e82d9cc45c83de96c895b109e158a4`; local commit object exists |
| Source archive SHA-256 | `12a8c89b77aa898e9c16a1efdf93e77f35ea3cee3eed93ad34c7f497eaad3eb0` |
| Manuscript PDF SHA-256 | `5d2bc6cfa9d02b21e816d3dd30252d067e23b51ecd0c58bb8c3cfb116ab937bd` |
| Whole package | 83 manifested payloads plus the manifest: exactly 84 regular files and 26 implied directories |
| Source tree | 72 manifested payloads plus the manifest: exactly 73 regular files and 25 implied directories |
| Archive | 73 sorted, unique, canonical, regular members; no directory, link, or special-node members |
| Source-commit binding | All 71 source-derived payloads match the declared commit byte-for-byte; the additional payload is generated bundle metadata |
| Convenience extraction | Exact file/directory inventory and bytes agree with the archive |
| PDF binding | Top-level PDF, nested source-tree PDF, and rebuilt PDF are byte-identical |
| Final contamination check | Review copy still recursively equals the original delivery; independent identity check remains status 0 |

The archive and PDF values agree with the actual files, both manifests, the
detached sidecar, `README_FIRST.md`, `VERSION.md`, and the certified transcript.

## R2-to-R3 remediation matrix

| R2 requirement | R3 evidence | Assessment |
|---|---|---|
| Make package root the sole certified route | All public documentation and Section 7 name only package-root `run_all_referee_checks.sh`. Bare `replay.sh` rejects with status 2; bootstrap requires an explicit mode and labels development status noncertifying. | **Closed.** |
| Reject arbitrary `PYTHON` | The package launcher, bootstrap, and replay test variable presence, so even an empty setting is rejected before invocation. Replay derives its interpreter only from the private runtime. The token-printing fixture is required not to run. | **Closed.** |
| Check exact file and directory sets before project import | Independent static tracing confirms package verification, verified-byte extraction, and the bootstrap's standard-library-only source audit precede every project import. Both regular files and implied directories must match. | **Closed.** |
| Reject links, special nodes, bytecode, caches, and unexpected nodes | `lstat`/no-follow scans reject symlinks, every nonregular/non-directory mode, case-insensitive `__pycache__`, `.pyc`, `.pyo`, extra files, and extra directories. Independent tests added a Unix socket, mixed-case cache name, and uppercase `.PYC`; all failed closed. | **Closed.** |
| Prevent inherited/adjacent bytecode execution | Every process that may import project modules uses `-B` and a fresh command-line `-X pycache_prefix=...`; the prefix is checked empty before and after use. An independently built timestamp-valid hostile cache was rejected before import. | **Closed.** |
| Exercise six specific hostile controls | Fake token interpreter, valid timestamp cache, extra file, extra empty directory, symlink, and FIFO each produced nonzero status and its intended diagnostic before the positive replay. | **Closed.** Optional marker-location hardening noted below. |

The five findings predating R2 also remain closed: all 406 scientific
conditions use fail-closed `require` calls; inherited import/build overrides
are sanitized; dependency wheels and document resources are bound; helper
reach and finite-versus-analytic wording are accurate; and no Make workflow is
shipped in the standalone R3 package.

## Certified route and failure semantics

| Stage | What was verified | Import/cache consequence |
|---|---|---|
| Package boundary | Rejects `PYTHON` and nonzero optimization; clears Python/import/Make overrides; requires exact Python and document-tool versions. | No project import. Explicit `BOOTSTRAP_PYTHON` and selected host tools are disclosed trust inputs. |
| Package verifier | Scans exact outer nodes and hashes, validates detached archive checksum, requires safe/sorted/unique/regular tar members, validates the internal manifest and convenience extraction. | Standard library only under isolated Python. |
| Verified extraction | Writes already verified payload bytes to a fresh mode-0700 source directory, normalizes modes, and rescans exact nodes. | It does not recursively copy an ambient tree. |
| Certified bootstrap preflight | Rechecks exact source files, directories, hashes, runtime, and all bundled Python ASTs directly from the verified manifest. | The safety script imports no project module; the manifest helper is not loaded on this branch. |
| Private environment | Creates a fresh mode-0700 runtime, virtual environment, setup cache, and final empty cache; installs with `--require-hashes --only-binary=:all: --no-deps`. | Dependency and source checks run under isolated Python with a command-line private prefix. |
| Internal replay | Rejects other argument shapes and `PYTHON`, derives the fresh interpreter from its runtime argument, rechecks safety/dependencies, and invokes unit tests plus 17 programs directly under `set -eu`. | Every project import has `-B -X pycache_prefix=<fresh>`; final cache must remain empty. |
| Document build | Requires Tectonic 0.16.9 and Poppler 26.08.0, checks the v33 resource record, rebuilds, inspects, and renders the PDF. | Final `cmp` and SHA-256 bind the build to the delivered PDF. |
| Final verification | Rechecks the original package after the full run. | Any positive-path child failure propagates nonzero. |

There is no output-token parser on the scientific programs. The old public
token has been retained only as hostile input that must be rejected before its
executable is invoked.

## Hostile-control results

### Shipped controls in the certified command

| Control | Observed result |
|---|---|
| Intentional false scientific condition | Nonzero propagated to package root; intended marker present |
| Explicit false condition under `python -O` | Remained active and failed |
| Inherited `PYTHONOPTIMIZE=1` | Rejected explicitly before replay |
| Token-printing fake `PYTHON` | Rejected before invocation; public token absent |
| Timestamp-valid adjacent malicious bytecode | Rejected as forbidden cache contamination before project import |
| Extra regular file | Rejected by exact node-set mismatch |
| Extra empty directory | Rejected by exact node-set mismatch |
| Symlink | Rejected by no-follow symlink branch |
| FIFO | Rejected as a special node without blocking |

The six advertised interface/tree hostile controls are the final six rows
beginning with the fake interpreter. All ran before the uncontaminated
positive bootstrap.

### Independent extensions

| Independent case | Child status/result |
|---|---|
| Empty inherited `PYTHON` | 2, intended rejection |
| Bare replay without the internal argument | 2, intended rejection |
| Bootstrap without an explicit mode | 2, intended usage rejection |
| Package extra file / empty directory | 1 / 1, intended exact-set diagnostics |
| Package symlink / FIFO / Unix socket | 1 / 1 / 1, intended type diagnostics |
| Package uppercase `.PYC` / mixed-case `__PyCaChE__` | 1 / 1, intended bytecode/cache diagnostics |
| Independently constructed valid timestamp cache in source tree | 1, intended pre-import cache diagnostic; no marker executed |
| Same cache deliberately imported with the scanner bypassed | Executed its harmless marker, proving that the rejected fixture was genuinely loadable |

No false-positive certified status was found.

## Low-priority test-hardening suggestion

**S1 — negative-control marker location (low, nonblocking).**

`submission/create_tree_negative_control.py:26` embeds
`open("PYCACHE_EXECUTED", "w").close()`, so deliberate execution writes to
the process's current directory. `run_all_referee_checks.sh:166` searches only
below `negative_tree`. A controlled import from a separate directory confirmed
`marker_in_caller=yes` and `marker_in_negative_tree=no`.

This does not invalidate the current control or certified ordering:

- bootstrap failed with the exact cache-rejection diagnostic;
- static inspection establishes that the scanner imports no project module;
- the positive replay uses a different verified tree and private cache; and
- the independent demonstration confirms that the cache itself is valid.

For stronger future-regression observability, make the hostile statement write
beside `__file__` and broaden the `find` name accordingly, or pass an explicit
marker path rooted below the disposable extraction. This is recommended before
submission if making another tiny package revision is inexpensive, but it is
not required to repair a mathematical or certified-route defect.

## Theorem-by-theorem validation

The R3 mathematical content is theorem-equivalent to the already audited R2
content. The table records both the exact scope and the independent/replay
evidence retained in R3.

| Claim | Scope and boundary checked | Independent/replay evidence | Assessment |
|---|---|---|---|
| Model and complete baseline, (2.1)-(2.4) | Target-by-source indexing; incoming-column gauge; all `r>0`; `r=1` by continuity | Wrong-orientation control differed; independent incoming-column rescaling agreed; complete birth/death formula rederived | **Validated** |
| Theorem 1: fitness-two strict local maximum | Fixed `n>=3`; full positive loopless row-stochastic tangent space; neighborhood may depend on `n`; `n=2` ties | Union dual, stationary collision expansion, three-sector decomposition, norm conversion and sign checked; independent literal resolvents reproduce every displayed sector for `n=3,4,5` | **Validated within stated local scope** |
| Lemma 6: union-dual ergodicity | Positive off-diagonal kernel; proper nonempty ancestral sets | Shrink/move/grow/self-loop paths checked; exact nonsymmetric dual/forward cases agree | **Validated** |
| Proposition 7: coverage representation | Positive kernel; complete alternation; `rho=m(P)/n` | Boolean mixed differences rederived; four nonsymmetric literal chains agree | **Validated** |
| Lemma 8: active collision identity | Empty-cache boundary; `A:Z->Y`, `R:Y->Z`; `K=RA`, `M=AR`; both stationary laws; uniqueness | Independent exact checks give `n*rho*(nu H)=1` on four nonsymmetric kernels | **Validated** |
| Perturbation and tangent decomposition | Vanishing first variation; three orthogonal multiplicity-free sectors; dimensions total `n(n-2)`; symmetric sector absent at `n=3` | Independent literal active-chain resolvents and displayed physical normalizations agree | **Validated** |
| Theorem 9 / sector positivity | Standard: exact `N=2..9`, analytic `N>=10`; antisymmetric: analytic all `N>=2`; symmetric: exact `N=3..39`, all `40..287`, analytic `N>=288` | No endpoint gap; exact minimum remains at `N=40`; displayed eigenvalues reproduced; verifier hash `7a1fa1f579c090cc32668392e67b9eb88e696b51ad602a90d069541e402aa512` agrees across source, TeX, PDF, and manifests | **Validated** |
| Theorem 2: complete-support strong selection | Fixed positive directed structure; `r -> infinity`; coefficient `E_dir/[n^2(n-2)]`; equality gauge | First-step derivative and sum of squares rederived; four nonsymmetric independent coefficients agree exactly | **Validated** |
| Corollary 3: no fixed finite universal dB amplifier | Fixed structure; strongly connected noncomplete cited theorem plus reducible source-component argument | Cited result/model/scope checked in first audit; R3 source and citation unchanged; reducible closure independently derived | **Validated** |
| Proposition 4: undirected support limit | Fixed finite connected undirected graph | First-gain/extinction argument checked; path/star and boundary examples agree | **Validated** |
| Theorem 5: weighted triangles | Positive weights; every `r>1`; equality only at equal weights | Six-state chain, positive denominator and centered sum of squares reconstructed; independent full chains cover nonuniform, rational-fitness, near-boundary, `r=1`, and support-boundary controls | **Validated** |
| Lemma 11: finite-state perturbation | Finite analytic absorbing system or bounded reachable limiting class | Resolvent/leakage argument checked in use; exact derivatives agree | **Validated** |
| Lemma 12: fitness monotonicity | Every kernel and initial set; `r>0`; non-strict | Common-target/common-threshold coupling checked; nonsymmetric exact examples monotone | **Validated** |
| Proposition 13: support degree must diverge | Growing undirected graph sequence; for each fixed `r>1`, eventual amplification | Quantifier order and `R -> infinity` passage checked analytically; no finite run is used to carry it | **Validated analytically** |
| Theorem 16: two symmetric weighted `K_4` families | Only `G13(x)` and `G22(x,y)`; positive parameters; every `r>1`; stated equality cases | Both lumpings, denominator/coefficient signs and domains checked; independent full 14-state examples agree | **Validated within the stated families** |
| Boundary and nonclaim ledger | `n=2`; missing symmetric sector at `n=3`; `r=1`; positive/zero-support boundaries; fixed-`n` and fixed-structure quantifiers | Endpoint calculations pass. Global `r=2` maximality, uniform radius, growing-family exclusion, and unrestricted weighted-`K_4` classification remain expressly open | **Validated; open questions are outside the claims** |

The independent checker has SHA-256
`019a599899fa223995ea61ca476e5e841e55bcea3605203f81b593d67f92d578`.
It uses only `fractions.Fraction` and imports no delivered module. Its R3 run
finished status 0 with all exact checks passing.

## Claim-to-code coverage and execution

Every delivered program was inspected before the readiness gate. The certified
replay invokes its children directly under `set -eu`; a nonzero child would
stop the run.

| Program/helper | Actual scope | Certified execution |
|---|---|---|
| `tests/test_exact_markov.py` + `src/exact_markov.py` | Transition rows, complete baseline/lumping, selected strong limits and signs | 6 tests, status 0 |
| `verification/verify_obstruction.py` | Exact subset solves, selected limits, triangle sign data | Status 0 |
| `phase1_directed/verify_directed_db_strong.py` | Selected `n=3,4` coefficient/orientation/gauge checks; Section 5 carries universal algebra | Status 0 |
| Triangle derivation, exact-solver cross-check, and independent audit | Six-state elimination, denominator/SOS identities, full-subset comparisons | All 3 status 0 |
| Weighted-`K_4` derivation and full-chain cross-check | `G13`/`G22` quotient certificates, 14-state rows, lumpability | Both status 0 |
| `phase3_asymptotic/verify_lumping.py` | Finite sanity examples; explicitly non-theorem-bearing | Status 0 |
| `verify_r2_determinant.py` | Order-three active determinant; stronger global coefficient remains OPEN | Status 0 |
| `verify_complete_refresh_forest.py` | Triangle refresh determinant and finite screens; arbitrary-order forest statement remains OPEN | Status 0 |
| `verify_antisymmetric_hessian.py` | Finite recurrence through `n=40`, literal chains through `n=7`; Appendix A carries all-order proof | Status 0 |
| `verify_true_inverse_rank_symmetric_phase.py` | Exact `N=3..39`, every `40..287` margin, analytic-tail identities | Status 0 |
| `verify_hessian_sectors.py` | Independent orbit reconstruction for `n=3..12` | Status 0 |
| `verify_physical_standard_phase.py` | Standard physical normalization, small values, analytic barriers | Status 0 |
| `verify_marked_lift.py` | Marked/active stationarity, collision identities, counterexamples to stronger open routes | Status 0 |
| `verify_local_complete_hessian.py` | Regular/symmetric supporting slice and barriers | Status 0 |
| `verify_paper_claims.py` | Phase, decomposition, normalization, hash, sign, and disclosure integration guards | Status 0 |
| `verify_resolvent_identities.py` | `solve()` called repeatedly by marked lift; guarded examples not run | Function exercised; main inert |
| `verify_direct_flow_screen.py` | `matrix_from_edges()` called; guarded finite screen not run | Function exercised; main inert |
| `verify_fisher_route.py` | Open-route module imported transitively; no function or witness main called | Import only; main inert |
| Package verifier and `build.sh` | Exact identity/extraction/PDF binding and deterministic build | Status 0; rebuilt PDF identical |

The 17 direct programs are byte-identical to R2. The three helper descriptions
correctly distinguish function call, module import, and guarded-main nonreach.
The replay's `OPEN` notices concern stronger global questions expressly outside
the paper's claims.

## Environment, commands, and statuses

| Component | Recorded version |
|---|---|
| Host | macOS 26.5.2, Darwin 25.5.0, arm64 |
| Python | 3.14.6, optimization 0 |
| SymPy | 1.14.0 |
| python-flint | 0.9.0 |
| mpmath | 1.3.0 |
| Tectonic | 0.16.9 |
| Poppler | `pdfinfo` and `pdftoppm` 26.08.0 |
| Git | 2.38.2 |

The authoritative command, run from the audit root, was:

```sh
env -i \
  HOME=/Users/alec/Documents/Math/complete_graph_extremality_r3_rereview_2026-08-23/work/clean_home \
  TMPDIR=/Users/alec/Documents/Math/complete_graph_extremality_r3_rereview_2026-08-23/work/replay_tmp \
  XDG_CACHE_HOME=/Users/alec/Documents/Math/complete_graph_extremality_r3_rereview_2026-08-23/work/xdg_cache \
  PATH=/opt/homebrew/bin:/usr/bin:/bin LANG=C LC_ALL=C TZ=UTC \
  BOOTSTRAP_PYTHON=/opt/homebrew/bin/python3 \
  ./work/package/run_all_referee_checks.sh
```

Its recorded child status was 0.

| Check | Recorded result |
|---|---|
| Original delivery versus isolated review copy, before and after testing | `diff -qr` status 0 |
| Independent exact package/archive/convenience inventories | Status 0 |
| Whole-package, detached archive, and internal manifests | Status 0 |
| 71 source-derived payloads versus declared Git commit | Status 0 |
| R2/R3 mathematical and 406-predicate regression | No scientific difference |
| Certified stripped-environment `run_all_referee_checks.sh` | **Status 0** |
| Unit suite and all 17 direct programs | All status 0 |
| Shipped hostile controls | All expected nonzero children with intended diagnostics |
| Independent extended hostile controls | Status 0 wrapper; all expected child rejections observed |
| Rebuilt PDF versus delivered PDF | `cmp` status 0; identical SHA-256 |
| Independent exact rational checker | Status 0; all checks passed |
| Final independent identity/contamination check | Status 0 |

The full transcript records two corrected audit-harness errors rather than
silently dropping them: an initial system-manifest command used the parent
directory instead of the package directory, and the first extra socket/fixture
demonstrations encountered path-length/import-path errors. Corrected reruns are
separately labeled and passed. Neither error involved a package failure.

## PDF regression and visual inspection

- R3 is a 30-page US-letter PDF 1.5, unencrypted, with no form or JavaScript.
- Pages 1--16 and 27--30 are pixel- and extracted-text-identical to R2.
- Pages 17--26 reflow solely because Section 7 now explains the certified
  package route and data-availability boundary at greater length. Appendix A's
  source itself is byte-identical.
- The same 22 font entries and fixed creation metadata are retained.
- Every R3 page and every changed R2 page was rendered and inspected. No
  clipping, overflow, collision, missing glyph, orphaned heading, blank page,
  broken path, or unreadable URL was found.
- The displayed symmetric-sector verifier hash and exact minimum margin are
  unchanged and agree with the delivered verifier.

## Proof/software consistency

The manuscript proof and the software independently support the same scoped
claims:

- target/source orientation, gauge invariance, normalization, and physical
  norm factors agree;
- finite ranges and analytic tails meet at every endpoint without extending a
  quantifier from sampled or numerical evidence;
- strictness and equality cases agree with literal exact chains;
- all three Hessian sectors agree between manuscript formulas, delivered
  exact checks, and an independent active-chain implementation;
- helper reachability and the role of open exploratory checks are accurately
  stated;
- every R2 scientific predicate is preserved byte-for-byte; and
- the exact PDF inspected is the one reproduced by the certified source.

No proof/code contradiction, uncovered theorem case, or scientific regression
was found.

## Assumptions and limits

1. The review assumes a stable private package copy during a run. Like ordinary
   reproducibility tooling, the scripts are not designed to defeat a
   same-user process racing file replacement between a scan and later use.
   Fresh mode-0700 extraction and runtime directories substantially narrow
   this boundary.
2. `BOOTSTRAP_PYTHON`, the host shell/core utilities, Tectonic, Poppler, and
   `PATH` remain host trust inputs. Exact versions, resource records, isolated
   execution, and final byte identity constrain honest drift but do not attest
   an arbitrarily malicious executable.
3. The exact-arithmetic libraries and host arithmetic are trusted; no proof
   assistant or independently verified arithmetic kernel was used.
4. The cited noncomplete-support theorem used by Corollary 3 was checked for
   statement, model, hypotheses, and fixed-graph scope in the original audit,
   not independently reproved here. R3 does not change that dependency.
5. Locked wheels and document resources are retrievable dependencies rather
   than vendored artifacts. Wrong bytes fail closed; future unavailability
   could prevent replay without changing frozen identity.
6. Bootstrap development mode and the internal replay argument are ordinary
   lower-stage interfaces. A user can invoke them manually, but their status is
   repeatedly and accurately documented as noncertifying.
7. Tectonic's content record is checked after resource use; the final
   byte-for-byte PDF comparison is decisive for this frozen manuscript.

These are disclosed trust boundaries, not missing theorem cases or reproduced
false-positive certified paths.

## Verdict

**Final verdict: fully validated.**

R3 repairs both R2 entry-path defects on the sole certified route, preserves
the validated mathematical content exactly, passes the complete clean replay,
rejects every stated and independently extended hostile case, and reproduces
the inspected PDF exactly. The marker-location issue is a low-priority
defense-in-depth test improvement; independent static ordering and dynamic
diagnostics already establish the property it was intended to observe, so it
does not warrant a correction-level verdict.

Accordingly, **valid after minor corrections** would overstate the consequence
of S1, while **major correction required** and **invalid** are unsupported by
the mathematical, software, and reproduction evidence.
