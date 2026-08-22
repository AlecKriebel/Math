# Independent R2 re-review report

**Manuscript:** *Local Complete-Graph Optimality at Fitness Two and
Strong-Selection Rigidity under Death--Birth Updating*  
**Package:** `paper_i_complete_graph_extremality_referee_package_2026-08-22_r2`  
**Review date:** 2026-08-22  
**Verdict:** **Valid after minor corrections**

## Executive assessment

The mathematical result remains valid. R2 makes no theorem-bearing algebraic
change, preserves every hypothesis, quantifier, equality case, endpoint, and
limitation, and preserves all 406 scientific predicates exactly while moving
them from optimization-elidable `assert` statements to explicit raising
checks. The clean referee command completed with status 0, ran the unit suite
and all 17 advertised verifier/cross-check programs, accepted only hashed
Python artifacts, checked the pinned document bundle, rebuilt all 30 pages,
and reproduced the delivered PDF byte-for-byte.

All five findings from the first review are closed on that authoritative
package-level route. The revised proof-status and helper-reachability wording
is accurate; the Makefile is absent from the standalone package; the
historical repository target remains valid at the declared source commit.

R2 is not yet fully validated as a *multi-entry replay artifact*. Two
advertised lower-level routes remain capable of false-positive certification:

1. a non-Python command that prints the public safety token makes direct
   `replay.sh` return 0 without executing any scientific program; and
2. a timestamp-valid adjacent `.pyc` can execute during both direct replay and
   `bootstrap_replay.sh` while the companion source is unchanged, the source
   AST audit passes, and the documented `shasum -c MANIFEST.sha256` check still
   returns 0 because it does not reject extra files.

These are High-impact defects in the assurance offered by the affected entry
points, but their correction is minor in the journal sense: restrict the
certificate route to the fresh venv interpreter, reject unlisted/cache files
before import, and make all documentation identify the verified-copy launcher
as the sole certified route. No theorem, proof, coefficient, certificate
family, expected value, or PDF conclusion needs revision.

## Scope and independence

The editor's remediation summary, package prose, expected output, hashes, and
prior verdict were treated as claims. Work was performed on the disposable
copy at
`/Users/alec/Documents/Math/complete_graph_extremality_r2_rereview_2026-08-22/work/package`.
No person was contacted, no file was uploaded, and no external system was
changed. Dependency access was limited to pip's configured package source and
the standard Tectonic bundle endpoint used by the delivered build.

The theorem audit combines:

- the first-round first-principles proof audit;
- an R1/R2 source and rendered-page regression audit;
- an independent AST comparison of every migrated scientific condition;
- a fresh run of the independent `fractions.Fraction` checker, which imports
  no delivered module; and
- the complete R2 package replay plus hostile negative controls.

Full evidence is in `records/COMMANDS.log`, `records/STATIC_REPLAY_AUDIT.md`,
`records/ADVERSARIAL_REMEDIATION_AUDIT.md`, and
`records/MATH_PDF_REGRESSION.md`.

## Package identity

| Item | Independently observed result |
|---|---|
| Scientific source commit | `e63cc44748e4084ade67c5ff7dc5d1bf2a872f7c`; commit object exists locally |
| Source archive SHA-256 | `1754bee519537105f192a40d98f83a4b2fd5097897e0632d88ace1e9892d59ed` |
| Manuscript PDF SHA-256 | `22142ee518e75c00d1948b19c210818ec797946df86a5e3272c9d1017800b0f4` |
| Package manifest | 81 payload files, all matched; no unexpected file in frozen package |
| Archive | 71 sorted, unique, regular members; detached and internal manifests matched |
| Source-commit binding | All 69 source-derived payloads matched the declared Git commit byte-for-byte |
| Convenience extraction | Byte-identical to a fresh extraction of the detached archive |
| PDF binding | Top-level and source-tree PDFs byte-identical |
| Final contamination check | Package manifest still status 0 after all review work |

The archive and PDF hashes agree with `README_FIRST.md`, `VERSION.md`, the
detached sidecar, both manifests, and the clean replay transcript.

## R1 finding remediation matrix

| Prior finding | R2 evidence | Result |
|---|---|---|
| F1: optimization could erase scientific checks | All 406 old assertion expressions are identical, in the same order, to the 406 R2 `require` conditions across the same 20 scientific files. R2 has zero AST `Assert` nodes. The launcher rejects inherited optimization; an explicit false condition still failed under `python -O`; `PYTHONOPTIMIZE=1` returned status 2. | **Closed on the authoritative route.** |
| F2: helper reachability was overstated | `CLAIM_CODE_MAP.md` now distinguishes the 17 directly executed programs from three imported modules. It correctly identifies only `solve()` and `matrix_from_edges()` as called and Fisher-route names as merely imported. | **Closed.** |
| F3: inherited overrides and unpinned artifacts | The three shell boundaries clear Python/import/Make overrides. Bootstrap clears the venv and uses `--require-hashes --only-binary=:all: --no-deps`. Exact versions and import origins are checked. A deliberately wrong wheel hash failed with status 1. Tectonic v33 has a fixed digest; a wrong expected digest failed with status 2. | **Closed for the prior defect.** Ordinary trust in the selected host executables and cache implementation remains disclosed. |
| F4: finite checks were worded like analytic proofs | Section 7, Appendix A, `CLAIM_CODE_MAP.md`, and verifier output now say explicitly that the directed and antisymmetric executable ranges are finite consistency checks and that the universal conclusions are analytic manuscript arguments. | **Closed.** |
| F5: stale Make workflow in the standalone package | No `Makefile`, `makefile`, or `GNUmakefile` is shipped. `replay.sh` invokes the unit suite and all 17 programs directly. The historical full-repository target still exists with valid source/destination paths at the declared commit. | **Closed.** |

## Findings remaining after R2

### R2-1 — High code/reproducibility impact: forgeable direct-interpreter token

**Affected interface:** direct `replay.sh`, not the verified package-level
launcher.  
**Locations:** `replay.sh:24-55,62-96`;
`run_all_referee_checks.sh:108-120`.

Direct replay accepts an arbitrary `PYTHON` executable. The preflight accepts
it when stdout contains the public literal `PAPER1_EXECUTION_SAFETY_OK`; every
later verifier call trusts only that same command's exit status. The shipped
negative control tests `/usr/bin/true`, which is silent, so it does not cover a
marker-aware no-op.

Reproduction on the disposable copy:

```sh
PYTHON=/absolute/path/to/fake_python_public_token.sh ./replay.sh
```

The fake command printed the public token and returned 0 for every argv.
`replay.sh` printed 19 token lines and returned **status 0**, although no
Python or scientific verifier ran.

This does not compromise the recorded `run_all_referee_checks.sh` execution:
that route preflights the bootstrap interpreter, constructs a fresh venv, and
overwrites `PYTHON` with that venv's executable. It does falsify the broader
claim that the direct interpreter is “authenticated” and that direct replay's
zero status alone certifies execution.

**Required correction:** make the newly constructed venv interpreter the only
certificate-bearing interpreter; otherwise label arbitrary-`PYTHON` replay as
a development convenience, not an evidentiary route. Remove “authenticated”
unless actual executable identity is bound. Add a token-printing fake-
interpreter negative control.

### R2-2 — High standalone-artifact impact: extra timestamp-valid bytecode is read

**Affected interfaces:** direct `replay.sh` in a reused checkout and
`bootstrap_replay.sh` in a non-clean extraction. The exact-file-set verified
package launcher is insulated.  
**Locations:** `replay.sh:11-15,62-96`;
`verify_execution_safety.py:110-152`;
`bundle_manifest.py:56-72,90-111`.

`PYTHONDONTWRITEBYTECODE=1` prevents new cache writes; it does not prevent
Python from reading an existing valid cache. R2 correctly clears the inherited
`PYTHONPYCACHEPREFIX`, but it neither rejects adjacent `__pycache__`/`.pyc`
files nor relocates reads to a fresh empty cache. The AST audit reads the `.py`
text while later imports may execute a timestamp-valid `.pyc`.

The hostile fixture compiled an imported helper with a marker side effect into
an adjacent timestamp-valid cache while leaving
`verify_direct_flow_screen.py` unchanged at SHA-256
`8be62ba2236d48b9f624e5b6df612a6bcd05534f8a1bd5771b9c7f38368a2eef`.
Both direct replay and a fresh-venv `bootstrap_replay.sh` run reported all
406/418 source checks and returned **status 0**; the marker proved the cached
code executed. The documented standalone command
`shasum -a 256 -c MANIFEST.sha256` also returned **status 0** in the presence
of the extra `.pyc`, because it checks listed files but not exact file-set
equality.

A genuinely fresh archive extraction has no such cache. More strongly, the
referee launcher verifies the exact package file set, rejects symlinks, copies
the cache-free tree into a new directory, and then provisions its interpreter;
the successful authoritative run therefore was not exposed.

**Required correction:** before any project import, require exact regular-file
set equality and reject symlinks, special nodes, `__pycache__`, `*.pyc`, and
`*.pyo`; or always execute from a new exact-manifest copy. A controlled empty
cache prefix is acceptable defense in depth. Plain `shasum -c`, `-B`, and
`PYTHONDONTWRITEBYTECODE` are not no-read guarantees.

### Nonblocking trust boundaries and suggestions

- `BOOTSTRAP_PYTHON`, Tectonic, Poppler, shell utilities, and `PATH` are host
  trust inputs. Versions, resource records, and final byte identity constrain
  honest drift but do not cryptographically attest arbitrary hostile tools.
- The build checks Tectonic's URL-to-content record after compilation rather
  than independently hashing every cached resource before use. The final PDF
  `cmp` is decisive for this frozen package, and the wrong-record negative
  control propagated correctly.
- The lock records every accepted wheel hash but not its filename/platform
  mapping. Pip proved that the macOS arm64 CPython 3.14 wheel is accepted and
  rejects wrong bytes; a filename/hash map would improve static portability
  review.
- Post-install identity checks use exact version and module origin, not hashes
  of every installed file. This is an ordinary local-environment trust
  boundary after the hashed installation.

## Theorem-by-theorem validation

The R2 mathematical source is theorem-equivalent to R1. Of the manuscript
source files, only Section 7's four-line proof-status clarification and the
Appendix A verifier digest changed. Twenty-eight rendered pages are
byte-identical to R1; page 17 contains only the clarification/reflow and page
26 only the new digest. All 30 R2 pages were visually inspected without
clipping, overlap, missing text, font substitution, equation displacement, or
page-count change.

| Claim | Scope and boundary checked | Independent/replay evidence | Assessment |
|---|---|---|---|
| Model and complete baseline, (2.1)-(2.4) | Target-by-source indexing; incoming-column gauge; all `r>0`; `r=1` by continuity | Wrong-orientation negative control differed; independent column rescaling agreed; complete birth/death formula rederived | **Validated** |
| Theorem 1: fitness-two strict local maximum | Fixed `n>=3`; full positive loopless row-stochastic tangent space; neighborhood may depend on `n`; `n=2` ties | Dual/current identity, stationary expansion, sector decomposition, norm conversion and sign checked; independent literal resolvents reproduce every displayed sector at `n=3,4,5` | **Validated within stated local scope** |
| Lemma 6: union-dual ergodicity | Positive off-diagonal kernel; proper nonempty ancestral sets | Shrink/move/grow/self-loop paths checked; exact nonsymmetric dual/forward cases agree | **Validated** |
| Proposition 7: coverage representation | Positive kernel; complete alternation; `rho=m(P)/n` | Boolean mixed differences rederived; four nonsymmetric literal chains agree | **Validated** |
| Lemma 8: rectangular active collision identity | Empty cache; `A:Z->Y`, `R:Y->Z`; `K=RA`, `M=AR`; both stationary laws; uniqueness | Independent exact checks give `n*rho*(nu H)=1` on four nonsymmetric kernels | **Validated** |
| Perturbation and tangent decomposition | Vanishing first variation; three orthogonal multiplicity-free sectors; dimensions sum to `n(n-2)`; symmetric sector absent at `n=3` | Independent mixed directions and literal resolvents agree | **Validated** |
| Theorem 9 / sector positivity | Standard: exact `N=2..9`, analytic `N>=10`; antisymmetric: analytic all `N>=2`; symmetric: exact `N=3..39`, all `40..287`, analytic `N>=288` | No endpoint gap; exact minimum margin remains uniquely at `N=40`; displayed eigenvalues reproduced; R2 bound verifier hash `7a1fa1f579c090cc32668392e67b9eb88e696b51ad602a90d069541e402aa512` is bound in code, TeX, PDF, and both manifests | **Validated** |
| Theorem 2: complete-support strong selection | Fixed positive directed structure; `r -> infinity`; coefficient `E_dir/[n^2(n-2)]`; equality gauge | First-step derivative and SOS rederived; four independent nonsymmetric coefficients agree exactly | **Validated** |
| Corollary 3: no fixed finite universal dB amplifier | Fixed structure; strongly connected noncomplete source theorem plus reducible source-component argument | External result/scope was checked in the first audit; R2 source and citation are unchanged; reducible closure independently derived | **Validated** |
| Proposition 4: undirected support limit | Fixed finite connected undirected graph | First gain/extinction competition checked; path/star and boundary examples agree | **Validated** |
| Theorem 5: weighted triangles | Positive edge weights; every `r>1`; equality only at equal weights | Six-state chain, M-matrix denominator and centered SOS reconstructed; independent full chains include nonuniform, rational-fitness, near-boundary, `r=1`, and support-boundary controls | **Validated** |
| Lemma 11: finite-state perturbation | Finite analytic absorbing system/reachable limiting class | Resolvent/leakage argument checked in its uses; exact derivatives agree | **Validated** |
| Lemma 12: fitness monotonicity | Every kernel and initial set; `r>0`; non-strict | Common-target/common-threshold coupling checked; nonsymmetric examples monotone | **Validated** |
| Proposition 13: support degree must diverge | Growing graph sequence; for each fixed `r>1`, eventual amplification | Quantifier order and `R -> infinity` passage checked analytically; no finite run carries it | **Validated analytically** |
| Theorem 16: two symmetric weighted `K4` families | Only `G13(x)` and `G22(x,y)`; positive parameters; every `r>1`; stated equality cases | Both lumpings, denominator/coefficient signs and domains checked; independent full 14-state examples agree | **Validated within the two stated families** |
| Boundary and nonclaim ledger | `n=2`; `n=3` missing symmetric sector; `r=1`; positive/zero-support boundaries; fixed-`n` and fixed-structure quantifiers | Endpoint calculations pass. Global `r=2` maximality, a uniform radius, growing-family exclusion, and unrestricted weighted-`K4` classification remain expressly open | **Validated; open questions are outside the claims** |

The independent exact checker, SHA-256
`019a599899fa223995ea61ca476e5e841e55bcea3605203f81b593d67f92d578`,
uses only the standard library's `fractions.Fraction` and imports no delivered
module. Its R2 regression run passed four nonsymmetric collision identities,
orientation and column-gauge controls, all displayed Hessian sectors for
`n=3,4,5`, four strong-selection derivatives, triangle and K4 examples, and
the relevant endpoint/monotonicity cases.

## Claim-to-code coverage and execution

Every delivered program was read before the readiness gate was opened. The
authoritative replay used `set -e` direct invocations; a nonzero child would
stop the run.

| Program/helper | Actual role and coverage | Authoritative execution |
|---|---|---|
| `tests/test_exact_markov.py` + `src/exact_markov.py` | Transition rows, complete baseline/lumping, selected strong limits and sign certificates; exact finite regression, not universal proof | 6 tests, status 0 |
| `verification/verify_obstruction.py` | Exact subset solves, selected limits and triangle sign data | Status 0 |
| `phase1_directed/verify_directed_db_strong.py` | Selected `n=3,4` orientation-sensitive coefficient/gauge checks; Section 5 carries universal algebra | Status 0 |
| Triangle derivation, exact-solver cross-check, and independent triangle audit | Six-state elimination, denominator/SOS identities, full subset comparison, hostile finite cases | All 3 status 0 |
| K4 derivation and full-chain cross-check | `G13`/`G22` quotient certificates, 14-state rows and lumpability | Both status 0 |
| `phase3_asymptotic/verify_lumping.py` | General finite lumpability sanity examples; explicitly non-theorem-bearing | Status 0 |
| `verify_r2_determinant.py` | Order-three active determinant; stronger global coefficient remains OPEN | Status 0 |
| `verify_complete_refresh_forest.py` | Triangle refresh determinant and finite screens; arbitrary-order forest positivity remains OPEN | Status 0 |
| `verify_antisymmetric_hessian.py` | Finite recurrence through `n=40` and literal active chains through `n=7`; Appendix A carries all-order proof | Status 0 |
| `verify_true_inverse_rank_symmetric_phase.py` | Exact `N=3..39` solves, every `40..287` margin, analytic-tail polynomial identities | Status 0 |
| `verify_hessian_sectors.py` | Independent delivered orbit reconstruction, `n=3..12` | Status 0 |
| `verify_physical_standard_phase.py` | Standard physical normalization, exact small values and analytic barriers | Status 0 |
| `verify_marked_lift.py` | Marked/active stationarity, collision identities, and counterexamples to stronger open routes | Status 0 |
| `verify_local_complete_hessian.py` | Regular/symmetric supporting slice and barriers | Status 0 |
| `verify_paper_claims.py` | Phase/decomposition/normalization/hash/sign integration guards | Status 0 |
| `verify_resolvent_identities.py` | `solve()` is called by marked lift; guarded examples are not run | Function exercised; main inert |
| `verify_direct_flow_screen.py` | `matrix_from_edges()` is called; guarded screen is not run | Function exercised; main inert |
| `verify_fisher_route.py` | Open/global-route diagnostics imported transitively; no function is called | Module import only; main inert |
| `verify_referee_package.py` + `build.sh` | Exact package/archive/PDF binding and deterministic build | Both status 0; final PDF identical |

The replay reaches every load-bearing verifier. The `OPEN` notices concern
stronger global fitness-two questions that the manuscript explicitly does not
claim; no theorem depends on resolving them.

## Environment, commands, and statuses

| Component | Recorded version |
|---|---|
| Host | macOS 26.5.2, Darwin 25.5.0, arm64 |
| Python | 3.14.6, optimization 0 |
| SymPy | 1.14.0 |
| python-flint | 0.9.0 |
| mpmath | 1.3.0 |
| Tectonic | 0.16.9 |
| Poppler | `pdfinfo`/`pdftoppm` 26.08.0 |
| Git | 2.38.2 |

| Check | Child status/result |
|---|---|
| Recursive delivery/copy and fresh archive-extraction comparisons | 0; no differences |
| Package, detached archive, and internal manifests | 0 |
| 69 payloads versus declared Git commit | 0 |
| R1/R2 406-condition AST migration comparison | 0 |
| Authoritative minimal-environment `run_all_referee_checks.sh` | **0** |
| Unit suite and all 17 direct programs | All 0 |
| Rebuilt PDF versus delivered PDF | `cmp` 0; same SHA-256 |
| Independent exact regression checker | 0; all checks passed |
| Inherited `PYTHONOPTIMIZE=1` | **2**, expected rejection |
| Intentionally changed SymPy wheel hash | **1**, expected rejection |
| Intentionally wrong expected Tectonic bundle digest | **2**, expected rejection |
| `/usr/bin/true` interpreter, package's negative control | Nonzero, expected rejection |
| Public-token fake interpreter through direct `replay.sh` | **0, unexpected false positive** |
| Hostile adjacent `.pyc` through direct replay | **0, unexpected; marker executed** |
| Same hostile `.pyc` through `bootstrap_replay.sh` | **0, unexpected; marker executed** |
| Standalone `shasum -c MANIFEST.sha256` with extra hostile `.pyc` | **0, unexpected acceptance of extra file** |

The complete command transcript, including stdout/stderr and logged wrapper
status, is `records/COMMANDS.log`. Where a hostile wrapper intentionally
converted an expected child failure into an audit success, the table reports
the captured child status rather than the wrapper's final status.

## PDF regression and visual inspection

- R2 remains 30 US-letter pages, PDF 1.5, unencrypted, with no forms or
  JavaScript and the same 22-font inventory as R1.
- Pages 1-16, 18-25, and 27-30 render byte-identically to R1.
- Page 17 adds only the correct finite-check/analytic-proof clarification; the
  declarations still fit cleanly.
- Page 26 changes only the centered symmetric-verifier digest, which fits on
  one line and matches the actual remediated file.
- Every R2 page was rendered with Poppler and visually inspected. No layout or
  content defect was found.

## Proof/software consistency

The proof and the successfully executed, verified-copy software support the
same scoped mathematical claims:

- target/source orientation, normalization and physical norm factors agree;
- finite ranges and analytic tails cover all endpoints without extrapolating
  sampled evidence;
- strictness and equality cases agree with exact literal chains;
- the code's `OPEN` messages align with the manuscript's explicit nonclaims;
- every R1 scientific predicate survived the safety migration unchanged; and
- the rebuilt PDF is exactly the document inspected.

The two remaining findings concern whether *other advertised launch paths*
prove that the checked source was executed. They do not identify a proof/code
disagreement in the authoritative clean run and do not supply a mathematical
counterexample.

## Unresolved assumptions and limits

1. The review assumes the trusted host interpreter, exact-arithmetic libraries,
   operating system, and document tools implement their documented operations.
   No proof assistant or independently verified arithmetic kernel was used.
2. The full cited external article is not re-certified here. Its exact theorem,
   model, hypotheses, and fixed-graph quantifier used by Corollary 3 were
   checked in the first audit; R2 does not change that dependency.
3. The delivered solver exhausts all small symmetric orders and every
   `N=40..287` margin. Independent literal solvers reproduce displayed small
   sectors and the independent audit recomputes the critical finite margins,
   but no second proof-assistant implementation re-solves every small system.
4. Network availability is not archival identity. Missing locked wheels or a
   missing bundle fail closed, but the artifacts are not embedded in the
   package.
5. A deliberately hostile selected interpreter or host tool is outside normal
   reproducibility trust. R2 should nevertheless avoid calling a public stdout
   token “authentication,” because that wording and the observed zero status
   overstate what direct replay establishes.

These limits do not create a missing theorem case. Items 1-4 are ordinary
disclosed trust boundaries; item 5 motivates R2-1.

## Required corrections and verdict

Before calling the artifact fully validated:

1. make the package-level verified-copy launcher or fresh-venv bootstrap the
   sole certified entry point;
2. reject arbitrary `PYTHON` in certificate mode, or clearly label it a
   non-evidentiary development override;
3. perform exact file-set/symlink/special-node checks and reject/cache-isolate
   all bytecode before importing project helpers;
4. add negative controls for a token-printing interpreter and a valid adjacent
   cache; and
5. make `README_FIRST.md`, the paper README, Section 7, `CLAIM_CODE_MAP.md`,
   and bundle metadata name the same certified route.

**Final verdict: valid after minor corrections.**

“Fully validated” is excluded by the two reproduced false-positive direct
entry paths. “Major correction required” would overstate their consequence:
the exact verified-copy run is sound, the repairs are localized, and no
mathematical content changes. “Invalid” is unsupported because no theorem,
proof step, equality case, endpoint, or independent calculation failed.
