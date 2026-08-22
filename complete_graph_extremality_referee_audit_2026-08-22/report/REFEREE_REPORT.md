# Independent referee report

Date: 2026-08-22  
Manuscript: *Complete-graph extremality for death--Birth updating: a
fitness-two local theorem and strong-selection obstructions*  
Audited delivery: `paper_i_complete_graph_extremality_referee_package_2026-08-22`

## Executive conclusion

**Verdict: valid after minor corrections.**

I found no mathematical error, missing population-size interval, incorrect
normalization, failed equality case, or counterexample to a stated theorem.
The package is internally byte-consistent; all source-derived payloads also
match the claimed local Git commit.  The mandatory replay, run under Python
3.14.6 with assertions explicitly enabled in a credential-free environment,
completed with exit status 0.  Every named verifier passed, and the rebuilt
30-page PDF was byte-identical to the delivered PDF.

The reason not to assign **fully validated** is a real certification defect in
the launcher.  Bootstrap version checks and most scientific checks are bare
Python `assert` statements, but the launcher neither rejects an optimized
interpreter nor clears `PYTHONOPTIMIZE`.  I reproduced the failure mode: with
`PYTHONOPTIMIZE=1`, an explicit false assertion disappeared and the complete
referee command still exited 0 while printing its PASS/PROVED messages.  The
mathematics survives this defect because it was checked independently and the
evidentiary replay was sanitized, but the distributed command should not claim
to be a reliable certificate until it fails closed under optimization and
other inherited build/import overrides.

## Scope and method

The manuscript, expected output, stored hashes, source comments, and package
audit language were treated as hypotheses.  The audit proceeded in this order:

1. copied the delivery to a disposable tree and independently verified its
   manifests, archive, PDF, and claimed source commit;
2. read and visually inspected all 30 compiled pages, then read all LaTeX
   sections, appendices, and references;
3. reconstructed the theorem/quantifier ledger;
4. derived the model, duality, collision, perturbation, tangent-sector,
   strong-selection, triangle, and weighted-`K_4` arguments independently;
5. inspected the entire mandatory shell/Python invocation and import graph
   before executing delivered code;
6. ran the mandatory replay in a clean environment;
7. ran a separately written standard-library exact checker, with no delivered
   imports, on nonsymmetric kernels, literal active chains, all displayed
   Hessian sectors, strong-selection derivatives, and low-order examples; and
8. performed a separate adversarial proof/code-alignment review.

The detailed theorem ledger is in `report/THEOREM_LEDGER.md`; derivations and
independent calculations are in `records/fitness_two_local_audit.md`,
`records/strong_selection_low_order_audit.md`, and
`records/independent_crosschecks.md`.  The separate hostile review is
`records/adversarial_falsification.md`.

## Package identity and environment

### Identity

| Item | Independent result |
|---|---|
| Package manifest | 80 payload files matched; exit 0 |
| Detached archive | SHA-256 `b1b7b7c4c9393ee4fa85eeacd54cefc4bcc94a3eca759d500c9ee6a362eddd2b`; exit 0 |
| Internal archive manifest | 70 regular-file members matched; exit 0 |
| Fresh extraction | Byte/name-identical to the convenience extraction; exit 0 |
| Convenience versus archived PDF | Byte-identical; exit 0 |
| PDF | SHA-256 `a6bda621b764ca8ee86658f6b68de0245790b84315eb77a6cc7ca45f7953bd2d` |
| Claimed source commit | `3652cfda20a3edad1b4e9ca75a4e5536f6f7f5ba` exists locally; all 68 source-derived payloads match its blobs |
| PDF inspection | 30 letter pages; no encryption, form, or JavaScript; no visual clipping, overlap, missing glyph, or broken figure |

The two archive-only metadata files are bound by the archive/package checks.
The package checker itself string-binds the commit identifier but does not
compare Git blobs; the last row above was an additional independent check.

### Environment

| Component | Observed version/state |
|---|---|
| Host | macOS 26.5.2 (25F84), Darwin 25.5.0, arm64 Apple M1 Pro, 16 GiB |
| Python | `/opt/homebrew/bin/python3`, 3.14.6; `sys.flags.optimize=0` for the evidentiary run |
| Python dependencies | SymPy 1.14.0; python-flint 0.9.0; mpmath 1.3.0 |
| Tectonic | 0.16.9 |
| Poppler | 26.08.0 (`pdfinfo`, `pdftoppm`, `pdftotext`) |
| Git | 2.38.2 |
| Replay isolation | `env -i`; fresh HOME/TMP/cache; no `PYTHONOPTIMIZE`, `PYTHONPATH`, `MAKEFLAGS`, credential variables, or inherited shell environment |
| Network used | uncredentialed PyPI for pinned packages; Tectonic's standard resource bundle; PLOS pages/PDFs for the cited-source check |

### Critical commands and statuses

| Label | Purpose | Status |
|---|---|---:|
| `verify-whole-package-manifest` | independent package hashes | 0 |
| `verify-detached-archive-checksum` | detached tar hash | 0 |
| `verify-internal-extracted-manifest` | internal hashes | 0 |
| `compare-delivered-and-independent-extractions` | byte/name identity | 0 |
| `compare-convenience-and-archived-pdfs` | PDF identity | 0 |
| `compare-archive-payload-to-source-commit` | 68 blob comparisons | 0 |
| `sanitized_python_preflight` | Python 3.14.6, optimize 0, no unsafe overrides/credentials | 0 |
| `official_full_replay` | mandatory one-command audit | **0** |
| `optimized_mode_preflight` | reproduce erased `assert False` | **0**, demonstrating the defect |
| `diagnostic_optimized_full_replay` | test full launcher with assertions disabled | **0**, demonstrating the defect |
| independent triangle, `K_4`, boundary, asymptotic, and cross-check runs | alternate exact implementations | 0 after one documented development-time checker failure and one interrupted slow scratch attempt |

The complete argv, output, and status transcript is
`records/COMMANDS.log` (final SHA-256
`f8f7873cb91029a033eaf609a5de8a807a4785c5c7aa0aed68f6e72eb21d788e`).
Independent scratch commands, versions, hashes, and statuses are also summarized in
`records/strong_selection_low_order_commands.log` and
`records/independent_crosschecks.log`.  Two wrapper-usage/path mistakes exited
127 and 1 before any scientific action; both are retained in the log.  They
were corrected immediately and have no bearing on the replay.

## Theorem-by-theorem validation

| Claim | Location and exact scope | Independent mathematical result | Computational result | Status |
|---|---|---|---|---|
| Model orientation and baseline | p. 4--5, (2.1)--(2.4), all `r>0` | Target-by-source indexing, incoming raw-column gauge, dB transition, and complete birth/death ratios rederived; `r=1` limit is `1/n` | Nonsymmetric orientation negative control and column rescaling passed exactly | **Validated** |
| Theorem 1: fitness-two local maximum | p. 5, fixed `n>=3`; `n`-dependent neighborhood | Dual/current identity, stationary perturbation, first-variation cancellation, sector decomposition, norm conversion, and fixation sign rederived | Complete replay plus independent literal active resolvent for every displayed sector at `n=3,4,5` | **Validated within stated local scope** |
| Lemma 6: union-dual ergodicity | p. 7, positive off-diagonal kernel | Explicit shrink, move, grow, and self-loop paths verify irreducibility/aperiodicity on proper nonempty sets | Exact nonsymmetric `n=3,4` dual/forward checks agree | **Validated** |
| Proposition 7: coverage | pp. 7--8, positive kernel | Boolean mixed-difference identity and `rho=E|A|/n` derived directly | Nonsymmetric literal chains agree exactly | **Validated** |
| Lemma 8: rectangular active collision identity | pp. 8--9 | Empty cache, singleton stop, `A:Z->Y`, `R:Y->Z`, `K=RA`, `M=AR`, both stationary currents, uniqueness, and the conditional factor checked | Four nonsymmetric kernels give `n*rho*(nu H)=1` exactly | **Validated** |
| Perturbation/decomposition | pp. 10--11, (4.1)--(4.10) | Group-inverse ordering, zero linear term, three orthogonal irreducibles, dimensions/multiplicities, and physical norms checked | Mixed directed symbolic perturbation and literal resolvents agree | **Validated** |
| Theorem 9 / Lemmas 14--15: sector positivity | p. 11; Appendix A | Standard ranges `N=2..9` and `N>=10`; antisymmetric all `N>=2`; symmetric `N=3..39`, every `40..287`, and `N>=288` checked with no endpoint gap | Exact finite replay passed; minimum margin is uniquely at `N=40`; hash `b4d45a83ce5f21a1fd3e09403b376e071330290a01affff64711574b69e024bc`; displayed eigenvalues all reproduced | **Validated** |
| Theorem 2: complete-support strong selection | p. 6, fixed positive complete support and fixed `W`, `r->infinity` | First-step derivative gives `E_dir/[n^2(n-2)]`; scale invariance and equality gauge derived | Independent nonsymmetric `n=3,4` epsilon derivatives agree exactly | **Validated** |
| Corollary 3: fixed-graph obstruction | p. 6 | Cited strongly connected theorem checked against source and proof; reducible source-SCC closure derived separately | Directed cycle and complete-support controls agree | **Validated** |
| Proposition 4: undirected support limit | p. 6, fixed connected undirected graph | First gain/extinction competition and monotone limiting chain give the stated support-degree average and deficit | Path/star and boundary examples pass | **Validated** |
| Theorem 5: positive weighted triangles | p. 6 and p. 15, positive edges, `r>1` | Six-state system, M-matrix denominator, centered SOS, strictness/equality reconstructed | Independent symbolic elimination and full subset chains pass, including near-boundary/neutral controls | **Validated** |
| Lemma 11: finite-state perturbation | pp. 12--13 | Finite analytic resolvent and reachable-class leakage argument checked in each use | Exact derivatives agree with literal chains | **Validated** |
| Lemma 12: fitness monotonicity | p. 16, all kernels and initial sets, `r>0` | Common-target/common-threshold inclusion coupling is valid; conclusion correctly non-strict | Nonsymmetric monotonicity examples and fitness-independent cycle control pass | **Validated** |
| Proposition 13: support degree must diverge | p. 16, graph sequence and fixed-`r` eventual amplification | Quantifier order, `limsup<=1/R`, `R->infinity`, and probability consequence checked | No finite computation carries this quantifier | **Validated analytically** |
| Theorem 16: two symmetric weighted `K_4` families | pp. 27--28, only `G_13(x)` and `G_22(x,y)`, positive parameters, `r>1` | Both lumpings, denominators, 123-term positive `P_22`, `(g,d,t)` certificate, domains, and equality classes reconstructed | Independent symbolic derivation and literal 14-state samples pass | **Validated within the two stated families** |
| Boundary/nonclaim ledger | pp. 5--6, 11--16, 27--28 | `n=2`, absent symmetric sector at `n=3`, `r=1`, positive/zero-support boundaries, and fixed-structure quantifiers checked | Exact endpoint examples pass | **Validated; open global questions remain outside the claims** |

### Key mathematical checks

For raw edge weights `w_uv`, target `v` is the row of the normalized kernel,
`P_vu=w_uv/sum_z w_zv`.  Thus multiplying all weights entering a fixed target
by a positive constant leaves the chain unchanged.  The dB probability is

`r P_vS / [1+(r-1)P_vS]`,

which gives the complete formula (2.4) from the one-dimensional birth/death
ratio.  An independently normalized wrong-orientation kernel gave a different
fixation probability, providing a useful negative control.

At fitness two, if `L` is geometric with `Pr(L=l)=2^-l`, then

`1-E[(1-x)^L]=1-(1-x)/(1+x)=2x/(1+x)`.

The union dual therefore has the exact hit duality.  Its mixed coverage
difference is the indicator of `A cap S=empty` and `T subset A`, with the
stated sign.  The rectangular current calculation gives `nu H=1/m(P)` and
therefore `rho=m(P)/n`.  Direct exact calculations on four nonsymmetric
kernels independently produced `n*rho*nuH=1`.

At the complete kernel, stationary differentiation gives
`nu_1=nu_0 Delta G` and `nu_2=nu_0 Delta G Delta G`; rank averaging gives
`S Delta S=0`, hence the first variation vanishes.  The independently built
active resolvent reproduced the Frobenius-normalized eigenvalues

| `n` | standard | symmetric-balanced | antisymmetric-balanced |
|---:|---:|---:|---:|
| 3 | `1/11` | absent | `1/9` |
| 4 | `87/640` | `3/208` | `57/640` |
| 5 | `8585/57314` | `359/26660` | `143/2100` |

The independently recomputed symmetric phase margin is uniquely minimized at
`N=40` and equals

`639304267467075678841 / 115369588296792467144716`.

The separate exact checker has SHA-256
`019a599899fa223995ea61ca476e5e841e55bcea3605203f81b593d67f92d578`.

For strong selection, direct differentiation at `epsilon=1/r=0` gives the
paper's coefficient, using

`(sum x_i)(sum 1/x_i)-m^2 = sum_{i<j}(x_i-x_j)^2/(x_i x_j)`.

The cited noncomplete-support result has the same directed weighted dB model,
uniform initialization, strong-connectivity hypothesis, and fixed-graph
quantifier used by the manuscript.  Its published Theorem 1 supplies eventual
strict suppression for each noncomplete strongly connected graph; the
manuscript handles reducible supports separately.  See the
[PLOS Computational Biology article](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1007494).

## Claim-to-code coverage and execution

Every program below was read before execution.  “Exit 0” refers to the clean,
assertion-enabled official replay.

| Program/helper | Actual checked role | Exactness/coverage assessment | Execution |
|---|---|---|---|
| `tests/test_exact_markov.py` + `src/exact_markov.py` | transition rows, complete baseline/lumping, selected limits/certificates | Exact SymPy; finite regression suite, not universal proof | 6 tests, exit 0 |
| `verification/verify_obstruction.py` | exact subset solves, limits, triangle sign data | Exact; selected orders/examples | exit 0 |
| `phase1_directed/verify_directed_db_strong.py` | orientation-sensitive directed coefficient and column gauge | Exact; three nonuniform examples plus controls; universal theorem remains manuscript algebra | exit 0 |
| `phase2_triangle/derive_certificate.py` | six-state elimination and SOS certificate | Exact symbolic theorem certificate | exit 0 |
| `phase2_triangle/crosscheck_exact_solver.py` | full subset-chain comparison | Exact but imports the derivation and shared Markov helper; useful cross-check, not wholly independent | exit 0 |
| `phase2_triangle/audit/independent_triangle_audit.py` | determinant/SOS identities and deterministic hostile cases | Exact identities plus finite cases | exit 0 |
| `phase2_n4/derive_lumped_certificates.py` | `G_13`/`G_22` lumped certificates | Exact symbolic theorem certificates | exit 0 |
| `phase2_n4/crosscheck_full_chain.py` | 14-state full-chain/lumpability comparison | Exact; shares delivered helpers with derivation | exit 0 |
| `phase3_asymptotic/verify_lumping.py` | unrelated/general lumpability sanity examples | Exact finite checks; explicitly non-theorem-bearing | exit 0 |
| `r2_determinant/verify_r2_determinant.py` | order-three active determinant | Exact at stated finite order; global coefficient remains OPEN | exit 0 |
| `r2_determinant/verify_complete_refresh_forest.py` | triangle refresh determinant and finite screens | Exact identities/finite screens; arbitrary-order forest positivity remains OPEN | exit 0 |
| `r2_determinant/verify_antisymmetric_hessian.py` | rank recurrence and small literal active checks | Exact for checked ranges; all-order conclusion ultimately uses Appendix A's analytic coupling | exit 0 |
| `r2_determinant/verify_true_inverse_rank_symmetric_phase.py` | small exact solves, all `N=40..287` margins, analytic-tail polynomial identities | Exact rational/SymPy, endpoints exhaustive | exit 0 |
| `r2_determinant/verify_hessian_sectors.py` | independent delivered orbit reconstruction, `n=3..12` | Exact finite cross-sector check | exit 0 |
| `r2_standard_physical_phase/verify_physical_standard_phase.py` | standard physical normalization, small exact values, analytic barriers | Exact; finite and symbolic analytic ingredients are separated | exit 0 |
| `r2_marked_lift_v2/verify_marked_lift.py` | marked/active stationarity, collision, counterexamples to stronger routes | Exact; correctly leaves global fitness-two claim OPEN | exit 0 |
| `r2_regular_sector/verify_local_complete_hessian.py` | regular/symmetric local slice and barriers | Exact; supporting slice rather than sole full theorem proof | exit 0 |
| `paper_db_extremality/verify_paper_claims.py` | phase typing, decomposition, normalization, hash/source guards, sign bridge | Exact arithmetic plus hard-coded/string integration guards; a consistency audit, not independent proof | exit 0 |
| `verify_resolvent_identities.py` | linear solver used by marked lift | `solve()` called; guarded standalone examples not run | function exercised; main not executed |
| `verify_direct_flow_screen.py` | graph constructor used by marked lift | only `matrix_from_edges()` called; guarded finite screen not run | function exercised; main not executed |
| `verify_fisher_route.py` | open/global-route diagnostics | imported names are not called on replay path; guarded witness suite not run | module loaded only; main not executed |
| `verify_referee_package.py` and `build.sh` | manifests/archive/PDF binding and deterministic build | explicit failures for integrity; PDF byte comparison decisive | exit 0 |

The replay reaches every load-bearing theorem verifier.  The three imported
helper modules are not equivalent to three executed audit suites; only the two
functions identified in the table are used.  The skipped guarded mains concern
open/global exploratory routes and no stated theorem depends on them.

## Findings

### F1 — High reproducibility/code severity: optimization erases certification

**Locations.** `submission/bootstrap_replay.sh:10-13,23-34`;
representative scientific checks at `phase2_triangle/derive_certificate.py:163-186`,
`r2_determinant/verify_true_inverse_rank_symmetric_phase.py:204-349`, and
`paper_db_extremality/verify_paper_claims.py:67-296`; outer launcher
`run_all_referee_checks.sh`.

**Reasoning.** The bootstrap version checks and most scientific success
conditions are bare `assert` statements.  Neither the bootstrap nor the outer
launcher checks `sys.flags.optimize` or removes `PYTHONOPTIMIZE`.  Optimized
Python compiles these statements away, while unconditional PASS/PROVED prints
remain reachable.

**Reproduction.** The logged `optimized_mode_preflight` used Python 3.14.6
with `PYTHONOPTIMIZE=1`; `assert False` vanished and the program printed
`PASS_AFTER_ERASED_ASSERT`, exit 0.  The logged
`diagnostic_optimized_full_replay` then ran the delivered one-command launcher
under the same setting and also exited 0 with final PASS output.

**Required correction.** At the outermost entry point, explicitly reject
`sys.flags.optimize != 0`, clear/import-sanitize `PYTHONOPTIMIZE`, `PYTHONPATH`,
and `MAKEFLAGS`, and replace theorem-bearing `assert` statements with explicit
exceptions/check functions.  A negative-control test should prove that a
deliberately false scientific check produces a nonzero top-level status.

### F2 — Medium/low code-coverage and exposition issue: imported helper mains are inert

**Locations.** `CLAIM_CODE_MAP.md:23-31`;
`verify_marked_lift.py:24-29,491-555`;
`verify_direct_flow_screen.py:17-22,99-118`;
`verify_fisher_route.py:773-808`;
`verify_resolvent_identities.py:151-170`.

The claim map says three modules are reached as imported helpers.  Literally
they are import-reachable, but replay calls only `solve()` from the resolvent
module and `matrix_from_edges()` from the direct-flow module.  It does not run
the direct-flow screen, Fisher/witness suite, or resolvent standalone examples.
This does not weaken a manuscript theorem: those guarded suites concern
finite/open global routes, and the manuscript explicitly leaves global
fitness-two maximality open.  The map should nevertheless state function-level
reachability, or the suites should be invoked if their results are intended to
be part of the advertised replay.

### F3 — Medium/low reproducibility issue: inherited flags and unpinned artifacts

**Locations.** `replay.sh:29-52`, `bootstrap_replay.sh:19-21`,
`requirements.txt:1-3`, `README_FIRST.md:51-56`.

`MAKEFLAGS` can weaken Make failure behavior and direct Python invocations can
inherit `PYTHONPATH`.  Package versions are pinned, but wheel/sdist hashes are
not; Tectonic resources are also fetched rather than content-pinned.  The
sanitized audit avoided the flag/import risk, and the final PDF byte comparison
detects rendering drift, but exact dependency provenance still trusts the
configured endpoints.  Clear inherited overrides and provide a hashed lock or
preseeded verified artifacts for a stronger archival certificate.

### F4 — Low proof-status wording issue: finite code is not the all-order proof

**Locations.** `verify_antisymmetric_hessian.py:148-157`,
`verify_directed_db_strong.py:130-203`, and the corresponding statements in
Sections 4--5/Appendix A.

The antisymmetric program checks its recurrence through a finite range and
literal active chains through `n=7`, then prints an all-order PROVED message.
Likewise, the directed program tests selected examples while the theorem is
universal.  The universal conclusions are valid because the manuscript's
analytic coupling/recurrence and first-step derivations were independently
checked; they are not consequences of finite program output alone.  Output
and documentation should say “checked analytic certificate ingredients; see
proof” rather than allowing the executable to appear to quantify over all
orders/weightings.

### F5 — Low maintenance issue: unused legacy Make target is not archive-safe

`Makefile:29-31` defines `paper1` using an omitted legacy path.  The mandatory
replay does not call it and `build.sh` is the valid document entry point, so
this has no evidentiary impact.  Remove or repair the stale target.

## Boundary cases and stated limitations

- `n=2`: the normalized loopless kernel space is a singleton and fixation is
  `1/2` for every positive weighting and fitness; the singular `1/(n-2)`
  theorem correctly starts at `n=3`.
- `n=3`: the symmetric-balanced dimension is `n(n-3)/2=0`; standard and
  antisymmetric sectors cover the tangent space.
- `r=1`: uniform-singleton average fixation is `1/n`; all strict low-order
  classifications correctly assume `r>1`.
- Zero support: Theorem 2 correctly assumes positive complete support.  The
  cited noncomplete theorem covers strongly connected missing-edge supports;
  the source-SCC argument covers reducible supports; Proposition 4 covers
  connected undirected missing-edge supports.  A zero incoming degree is
  outside the model.
- The local theorem is for each fixed `n` and supplies no explicit or uniform
  radius.
- Strong-selection results hold for a fixed structure as `r->infinity`; they
  are not uniform over a growing family.
- The paper does not prove global maximality at fitness two, exclude growing
  amplifying families, or classify unrestricted weighted `K_4` graphs.
- All OPEN notices in replay concern these stronger nonclaims; no theorem
  relies on their resolution.

## Unresolved assumptions and limits of this audit

1. As in any machine-assisted exact calculation, the runs assume the Python
   interpreter, SymPy, python-flint, and integer/rational hardware/software
   implement their documented operations correctly.  No proof assistant or
   independently verified arithmetic kernel was used.
2. The delivered exact solver covers every small symmetric order
   `N=3..39`, and its source and construction were inspected.  Independent
   literal active solvers reproduced the displayed `n=4,5` symmetric cases and
   an independent audit recomputed all `N=40..287` margins, but a wholly
   separate second implementation did not re-solve all 37 small systems.
3. The cited noncomplete-support theorem and its supplement were read and its
   proof was reconstructed, but this audit does not formally re-certify the
   entire external article beyond the result used here.
4. Dependency artifacts were version-pinned rather than hash-pinned, as noted
   in F3.

These are disclosed trust limits, not identified gaps in a manuscript proof.
The open global fitness-two questions listed above are outside the claimed
scope and are not unresolved obligations of this paper.

## Proof/software consistency assessment

The mathematical proof, theorem statements, exact finite certificates, and
compiled PDF support the same scoped claims.  In particular:

- finite exact ranges and analytic tails meet without endpoint gaps;
- no sampled or floating-point experiment is used to carry an infinite
  quantifier;
- orientation, normalizations, physical norm factors, strictness, and equality
  classes agree between prose and literal chains;
- code OPEN notices align with explicit manuscript nonclaims; and
- the rebuilt PDF is byte-identical to the inspected PDF.

The software is best understood as an exact certificate/regression suite for
the finite algebra and analytic ingredients, not a standalone formal proof of
every universal sentence.  Under assertions-enabled sanitized execution it
supports the manuscript claims.  Under arbitrary inherited execution it is
not a trustworthy certificate because of F1.

## Process note

All scientific work was confined to the disposable audit folder, no person was
contacted, and no package payload was intentionally changed.  One process
deviation occurred: an initial research-log checkpoint commit (`9beb2bbd`) was
pushed to the existing `origin/main` while following the repository's standing
research-workflow instruction, before the request's stricter no-external-change
constraint was reconciled.  It contained only audit identity/log scaffolding,
not manuscript/package changes or credentials.  No further external write was
made.  This does not affect the scientific verdict but is disclosed because
the requested operating constraint was stricter.

## Verdict

**Valid after minor corrections.**

The central results, proofs, equality cases, ranges, and stated limitations are
independently supported.  The required corrections are localized to replay
hardening and precise code-coverage/proof-status wording; they do not require
a new mathematical idea or a change to any theorem.
