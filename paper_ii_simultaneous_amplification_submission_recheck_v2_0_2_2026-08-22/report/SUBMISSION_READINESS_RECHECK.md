# Independent submission-readiness recheck — Paper II v2.0.2

**Manuscript:** *A fitness-independent family of simultaneous amplifiers beyond relative fitness 3/2*

**Package/review date:** 2026-08-22

**Audit basis:** a byte-preserving disposable copy; complete PDF and LaTeX reading; independent mathematical derivation; executable/import inspection before package execution; archive, wheel, Git, and metadata audits; canonical and network-denied clean replays; deterministic rebuild; deliberate mutations; alternative exact and finite-state calculations; and independent hostile reviews.

## Submission recommendation

The revised manuscript and frozen v2.0.2 handoff are ready for scientific submission on content. The prior mathematical error has been replaced by a valid stopped-time argument, including both adjacent boundary states, and every downstream proof use needs exactly the repaired estimate. The verifier no longer relies on removable Python assertions, optimized execution is rejected, deliberately corrupted identities fail closed, dependencies are vendored and hash-pinned for offline Python replay, archive paths/hashes/modes are enforced, and the selected interpreter is used consistently. The prescribed end-to-end run rebuilt both the source archive and the 21-page PDF byte-for-byte.

The package is not yet literal “click submit” material because one private human field remains deliberately unresolved: `[[POSTAL_ADDRESS]]` occurs in the bioRxiv metadata and both journal cover-letter templates. In addition, the current intended-journal instructions ask an unaffiliated author to supply city and country of residence, while the PDF title page currently gives only “Independent Researcher.” These are administrative identity choices that only the author can approve. They do not affect the referee verdict, but they should be resolved before portal submission; depending on the portal's treatment of affiliation data, the city/country may require either portal entry only or a title-page refreeze.

No mathematical, software, packaging, reproducibility, layout, or material exposition defect remains. One nested vendor note points to a development-repository file that is not itself bundled; the same external-tool limitation is stated completely in three included documents. I classify that as optional polish, not a reason to disturb the frozen identities.

## Scope, independence, and evidence handling

- The editing AI's summary, response record, expected output, manifests, hashes, source comments, provenance notes, and author conclusions were treated as claims, not as evidence.
- All 21 PDF pages and all 1,660 LaTeX lines were read, including the abstract, theorem statements, limitations, declarations, data/code statement, AI disclosure, and references.
- Every delivered package-controlled Python and shell entry point and every project import was inspected before package execution.
- The package was executed only after an independent wheel/path/import review. Mutations and builds used disposable copies or temporary directories; `delivered_copy/` remained unchanged by hash and mode.
- No person was contacted and no file was uploaded. Network use was read-only and limited to the stated Git remote, upstream Python release metadata, and a network-denial control; the clean Python replay itself used no index or network.
- Every command, working directory, start/end time, combined output, and exit status is retained in `../logs/commands.tsv` and `../logs/full_transcript.log`, including expected negative controls and auditor mistakes.

## Disposition of the prior findings

| Prior finding | Revised implementation independently checked | Result |
|---|---|---|
| Unstopped pendant expectation could be infinite | Equations (24)–(26) now use upper-strip exit as a common terminal boundary; the bounded committor, stopped trace, and calendar-time estimates are re-derived below | Resolved |
| Adjacent `ell=0` boundary omitted | A resident-hub phase at `ell=0` has no loss, ends by activation/exit, and is grouped with the subsequent mutant-hub phase | Resolved |
| Initial `(h,ell)=(0,m)` not covered by the trace | Activation/loss/exit is treated separately; loss has probability `O(C^-1)` and restarts at `m-1` | Resolved |
| Verification-critical bare `assert` statements | Static AST audit found zero; explicit `require` checks and optimization guards are present in all controlled Python programs | Resolved |
| Optimized execution could print false success | Direct `-O`/`PYTHONOPTIMIZE=1` tests of programs and shell routes fail before a success sentinel | Resolved |
| No mutation regressions | Supplied early/late mutations pass; an independent endpoint mutation also fails in ordinary and optimized modes | Resolved |
| Python dependencies version-pinned but artifact-unfrozen | Upstream-identical pure-Python wheels are bundled, selected with `--no-index`, `--only-binary`, and `--require-hashes`, and have complete valid wheel `RECORD`s | Resolved |
| Archive safety and extracted modes incompletely enforced | Exact path sets, canonical safe regular members, uniqueness, hashes, `0644`/`0755` modes, deterministic metadata, and fresh-extraction identity all pass | Resolved |
| Standalone Git/source binding absent | Annotated tag, peeled commit, all 21 repository-backed blobs, and modes match locally and remotely; unsigned-tag limitation is explicit | Resolved with disclosed authentication boundary |
| Selected bootstrap interpreter not used by release builder | The chosen CPython creates the venv and that venv interpreter is passed through replay, release, and archive generation | Resolved |

## Frozen identity and completeness record

| Item | Independently observed value | Result |
|---|---:|---|
| Convenience/source PDF SHA-256 | `4e86597bb0baff388e8ce7ccf6ffd808f86b5ea846acf6f2188b31016fd2572c` | Exact match |
| Source/certificate archive SHA-256 | `d2145513f8abe295e9e7fab62f062fa9d0f7a6282de95e8155f3db4621485274` | Exact match |
| Transferable referee archive SHA-256 | `2216c6a31545b38d9ca89c9d43c5a309bfcc6c2c1f7ab63ea5fabc171116e1d2` | Exact match |
| Scientific commit | `03e94e877ce10d9d459fd284bd652934cde08bb3` | Exact tag target |
| Annotated tag object | `be3946c051c7f7e2073d6adf81bca31ae750251a` | Local/remote agreement |
| Scientific tag | `simultaneous-amplification-beyond-three-halves-v2.0.2` | Annotated, unsigned, correctly disclosed |
| Wrapper commit | `0dcb450a1081e98d2ae1029d513c8343e5fd4328` | Ancestor of current local/remote `main` |
| Whole-package manifest | 34 exact payloads plus manifest; 35 regular files total | Pass |
| Source archive | 23 unique, sorted, safe regular members | Pass |
| Internal source manifest | Exact other 22-member path set and hashes | Pass |
| Transferable archive | 35 unique, sorted, safe regular members under one top directory | Pass |
| Archive/tree/PDF correspondence | Every byte and executable mode agrees; both PDFs identical | Pass |

The branch advanced after the frozen wrapper commit; local and remote `main` were at `7962e61dc0f9550a640f9637fb5c7c6d074ac20f` during the check. The wrapper commit is in that history, so the stated identity remains accurate. The Git tag is unsigned: exact repository/tag/blob agreement does not independently authenticate the hosting account, author, or a cryptographic signer.

## Runtime and document record

| Component | Observed value |
|---|---|
| Operating system | macOS 26.5.2, build 25F84; Darwin 25.5.0 |
| Architecture | arm64, Apple T6000 |
| Python | CPython 3.14.6 at `/opt/homebrew/bin/python3` |
| SymPy / mpmath | 1.14.0 / 1.3.0 in fresh offline virtual environments |
| Python optimization flag | 0 in successful runs; optimized negative controls rejected |
| Tectonic | 0.16.9 |
| Poppler | 26.08.0 (`pdfinfo`, `pdftoppm`) |
| Git | 2.38.2 |
| PDF | 213,182 bytes; 21 letter pages; PDF 1.5; no encryption, forms, or JavaScript |

Every font is embedded. Text extraction contains no replacement glyph or unresolved `??` marker. Page-by-page raster inspection found no clipping, overlap, missing glyph, malformed equation, broken figure, or illegibility. The convenience PDF and source-tree PDF are byte-identical.

## Command and exit-status summary

The complete record is in the two logs named above. Substantive operations were:

| Operation | Result | Exit-status evidence |
|---|---|---|
| Independent outer/source archive, manifest, path, byte, and mode audit | Pass | 0 |
| Independent wheel member and complete `RECORD` audit | Pass: 92 mpmath and 1,570 SymPy members | 0 |
| Package verifier | Pass: 34 package payloads and 23 archive members | 0 |
| Local and remote tag resolution plus 21 blob/mode comparisons | Pass | 0 |
| PDF metadata, font, text, rendering, and 21-page visual inspection | Pass | 0 |
| Prescribed clean `run_all_referee_checks.sh` with local-only wheels | Pass; approximately 29 seconds in the main audit | 0 |
| Independent operating-system network-denied bootstrap and full rebuild | Pass | 0 |
| Deterministic source archive/PDF rebuild comparison | Exact hashes above | 0 |
| Supplied optimized-mode and early/late mutation regression | Pass | 0 |
| Independent wrong-endpoint mutation, ordinary mode | Correctly rejected; no success sentinel | Inner status 1, expected; enclosing audit status 0 |
| Same streamed mutation under `-O` | Correctly rejected by optimization guard | Inner status 1, expected; enclosing audit status 0 |
| Independent exact response/Sturm/orbit calculations | Pass | 0 |
| Independent finite stochastic chains and weak-cut convergence | Pass | 0 |
| Independent exact-rational stopped-time repair calculation | Pass | 0 |

The logs deliberately retain expected nonzero optimized/mutation/hash/network-denial controls. They also retain harmless auditor setup mistakes (wrong logger argument order, two wrong archive paths, an overstrict first wheel-mode predicate, a base interpreter without SymPy, and a mistyped prior-report path), each immediately corrected. No required operation remains failed or unperformed.

## Central theorem and quantifier ledger

The audited quantifier order is

\[
\exists\{G_t\}_{t\ge1}\;\forall r\in(1,R_{\rm hyb})\;\exists t_0(r)\;
\forall t\ge t_0(r):
\rho_{\rm Bd}(G_t,r)>\rho_{\rm Bd}(K_{|G_t|},r)
\quad\text{and}\quad
\rho_{\rm dB}(G_t,r)>\rho_{\rm dB}(K_{|G_t|},r).
\]

The graph, internal weights, and least-dyadic weak cut are selected before fitness is fixed. The endpoint is excluded, and `t_0` may depend on the fixed interior fitness. With `C=t^4`, `q=t`, and `m=floor(lambda_*t)`, the common response scale is `eta=q/C=t^-3=Theta(n^-3/4)`. The complete detailed ledger, including every scale and computational dependency, is `../work/THEOREM_LEDGER_V202.md`.

## Theorem-by-theorem validation

| Claim or proof component | Independent basis | Location | Result |
|---|---|---|---|
| Model and same-order complete-graph baselines | Direct labelled Bd/dB derivation and exact birth–death products for multiple orders/fitnesses | PDF pp. 2–3, Eqs. (1)–(6) | Verified |
| Definition of simultaneous amplification and `R_sim` | Explicit quantifier reconstruction above | Definition 1, PDF p. 3 | Verified |
| Effective graph and dyadic diagonal | Positivity/connectivity/scales; finite rational absorption systems; compact convergence; exact real-algebraic least-dyadic decision | Lemma 2, PDF pp. 3–4 | Verified |
| Main theorem | All dependencies below plus compact-uniform connected transfer | Theorem 3, PDF p. 5; proof p. 18 | Supported |
| Strong orbit lumping | General automorphism argument plus distinct finite exact orbit-row checks | Lemma 4, PDF p. 5 | Verified |
| Finite weak-cut trace | Fast-state transience; row-oriented `A+B(I-Q_0)^{-1}C_0`; exact local absorption; compact inverse | Proposition 5, PDF pp. 5–6 | Verified |
| Center-module asymptotics | Lemmas 7–11, including the repaired stopped synchronization | Proposition 6, PDF pp. 6–7 and proof p. 16 | Verified |
| Early establishment | Stopped adapted walk, hazard accumulation, product odds, `K^2/C` and `r^{-K}` errors | Lemma 7, PDF pp. 7–8 | Verified |
| Completion and core confinement | Conditional-bias coupling, exponential supermartingales, compensator, nested strips | Lemma 8, PDF pp. 8–9 | Verified |
| Stopped pendant committor/trace | Favorable generator monotonicity under adapted core jumps; exit boundary value one; bounded optional stopping | Lemma 9, Eq. (24), PDF p. 10 | Verified |
| `ell=0` and `(0,m)` boundaries | Two-phase grouping at zero; separate activation/loss/exit restart at full pendant occupancy | Lemma 9, PDF pp. 10–11 | Verified |
| Calendar-time and stopped hitting bounds | `E N=O(m)`, `O(C)` per outcome, Tonelli/random-sum bound, and separate full-occupancy case give `E Sigma=O(Cm)` | Lemma 9, Eqs. (25)–(26), PDF pp. 10–11 | Verified |
| Bd cleanup recursion | Uniform conditional block success, exit charged once, strong Markov recursion without independence | Lemma 9, Eqs. (27)–(30), PDF pp. 11–12 | Verified |
| dB cleanup and pendant initialization | Exact error exponents, hub-deactivation integral, graphical deletion/suppression, renewal | Lemma 9, PDF pp. 12–13 | Verified |
| Reciprocal killed Green bounds | Product odds, stopped Dynkin particle-time, exponential Green tail, integrated hub hazard | Lemma 10, PDF pp. 13–14 | Verified |
| Reciprocal renewal little-`o` bounds | Immigration–death Lyapunov estimate, finite-horizon maximum, nested truncation order, refined renewal | Lemma 11, PDF pp. 14–15 | Verified |
| Gate odds and global sweep | Independent four-rate derivation, exact macro chain with adverse reversals retained, `o(q/C)` sweep error | Proposition 12, PDF pp. 16–17 | Verified |
| First-order response functions | Independent common-scale expansion of center, pair, pendant, denominator, and baseline terms | Proposition 13, PDF p. 17 | Verified |
| Exact tangency and sextic isolation | Independent rational Sturm sequence, exact endpoint signs, minimizer/tangency identities, monotonicity | Lemma 14, PDF p. 18 | Verified |
| Final pointwise fitness diagonal | Eventually `r in I_t`; scaled weak-cut error at most `1/t`; separated limits strictly positive | Theorem proof, PDF p. 18 | Verified |
| Fixed-parameter optimality | Exact feasibility obstruction within the expressly limited first-order fixed-parameter model | Proposition 15, PDF pp. 18–19 | Verified within stated scope |
| Rational-edge specialization | Exact margins, discriminant/root, response sign, and rationality of every chosen weight | Corollary 16, PDF p. 19 | Verified |

### Why the stopped-time repair is valid

Set `tau_up=inf{s:R_s>=2 delta c}`. For each `1<=ell<m`, the worst-rate two-hub-state committor gives up-or-exit/down odds uniformly greater than one. Its value is subharmonic for the actual adapted process because activation and gain rates only improve, deactivation only worsens in the favorable direction, interior core jumps leave it unchanged, and a jump through the upper boundary moves to value one.

The revised trace assigns upper exit terminal level `m`. Before its terminal index, favorable outcomes have fixed positive conditional drift; at `ell=0` a downward move is impossible. Bounded optional stopping at `N wedge k` gives `E N=O(m)`. Every one or two hub phases has conditional probability `Omega(C^-1)` of a pendant outcome or exit and bounded mean duration, yielding `O(C)` calendar time per stopped outcome and therefore `O(Cm)` in total. At `(0,m)`, activation, loss, or exit has bounded mean; loss occurs first with probability `O(C^-1)` and restarts from `m-1`. Thus equation (26) holds for the target `(1,m)` **or** upper exit.

Every regeneration block starts at low deficit, uses this exact stopped target, and charges upper escape through the already-proved confinement estimate. Hence the repair is not circular and no downstream unstopped expectation is used. An independent exact-rational finite-chain solver found all tested stopped means finite and reproduced positive extinction-before-target probability for the superseded unstopped formulation.

## Independent alternative calculations

None of these calculations imported delivered certificate code:

- Exact complete-graph Bd/dB formulas were reproduced for multiple sizes and rational fitnesses.
- A distinct rational hybrid instance reproduced aggregate orbit rows under both update rules.
- A separately implemented 512-state chain reproduced 108 fibres under each rule, both 256-state center intensity tables, and monotone convergence to the weak-cut trace for `epsilon=10^-1,...,10^-4`.
- A standard-library rational Sturm calculation found zero sextic roots in `(1,3/2)` and one in `(3/2,151/100)`, with exact signs `P(3/2)=1/64` and `P(151/100)=-39866792399/10^12`.
- Independent calculations gave `R_hyb=1.5028569127905696267...`, `sigma_*=0.13067728228704837686...`, and `lambda_*=0.75080648303188049230...`.
- Exact rational responses reproduced endpoint margins `232/17361` and `65/12123`.
- Exact finite stopped chains verified the new committor inequality and boundaries and showed the old unstopped target can be missed by extinction with probability `0.370982488222...` in one small example.

## Claim-to-code coverage and execution

| Program or route | Intended coverage | Source-audit and execution result | Exact limitation |
|---|---|---|---|
| `verify_leading_algebra.py` | Sextic, Sturm, tangency, and monotonicity identities | Exact SymPy checks; explicit failures; normal pass; optimized rejection | Checks encoded algebra, not stochastic/asymptotic proofs |
| `verify_hybrid_lumping.py` | Finite labelled/orbit aggregation | Exhaustive 512 masks and 108 fibres at one rational nine-vertex instance; normal pass | Corroborates orientation/aggregation only; arbitrary-size lumpability is analytic |
| `verify_hybrid_coefficients.py` | Gate, response, rational, and phase identities | Exact symbolic/rational checks; normal pass; independent wrong-margin mutation rejected | Reduced stochastic portal rates are inputs |
| `verify_paper_claims.py` | Finite integration and textual regression audit | Exact finite identities plus required repaired-stop markers and forbidden old marker; pass | Explicitly not a proof checker |
| `test_verifier_fail_closed.py` | AST, optimized-mode, early/late mutation, and shell propagation | All supplied regressions pass | Tests software behavior, not theorem truth |
| `verify_referee_package.py` | Whole-package/source archive/PDF/prompt identity | Exact path sets, hashes, modes, archive safety, extraction, and metadata pass | Authenticates bytes against included hashes, not an external signer |
| `verify_git_binding.py` | Tag/commit/blob/mode correspondence | 21 repository-backed members match local and remote tag target | Unsigned tag cannot authenticate authorship/account |
| `bundle_manifest.py` | Deterministic exact-whitelist source archive | Safe modes/paths and deterministic metadata; byte-identical output | Python source bundle does not include external document tools/resources |
| `bootstrap_replay.sh` / `replay.sh` | Fresh offline dependency setup and ordered scientific replay | CPython 3.14.6; two local hash-pinned wheels; fail-closed replay pass | Requires the compatible interpreter to exist |
| `build.sh` / `release_bundle.sh` | Deterministic PDF and archive release | Exact Tectonic/Poppler gates; chosen venv interpreter; both outputs identical | A clean host may need external Tectonic resources, as disclosed |
| `run_all_referee_checks.sh` | Complete package-to-release route | Ordinary and network-denied runs pass; exact identities reproduced | Does not turn finite certificates into an analytic proof |
| Independent audit programs | Alternative archive, wheel, stochastic, response, Sturm, mutation, and stopped-time checks | All corrected executions pass | Finite calculations corroborate; infinite claims were independently derived analytically |

## Proof/software alignment

The proof and software support the same stated boundary without overclaiming. The finite lumping program is described as one finite orientation/aggregation audit; symbolic programs check exact identities already reduced to finite algebra; and the integration verifier is identified as a marker/regression audit. Weak-cut convergence, establishment, cleanup, reciprocal invasion, and global sweep remain analytic manuscript proofs. I did not infer any infinite-size statement from a successful program run.

The repaired text and the integration markers also agree: the old unstopped expression is forbidden, while the shared upper-stop boundary, terminal trace convention, `ell=0` handling, and stopped equation (26) are required. The programs reproduce the same response formulas and hashes used in the manuscript, and independent calculations reproduce them without importing the programs.

## Findings by category

### Mathematical defects

None found in v2.0.2. The prior stopped-time defect and both boundary cases are correctly repaired.

### Code defects

None found. All verification-critical conditions are explicit; controlled programs contain no bare assertion; optimized mode and mutations fail closed.

### Reproducibility and packaging defects

None found. Frozen identities, exact path sets, safe members, hashes, modes, dependency artifacts, Git binding, fresh replay, and deterministic rebuild all pass.

### Exposition issue — optional polish

`source_and_certificates/.../vendor/README.md:27` says the document-tool boundary is described in `submission/ENVIRONMENT.md`, a development-tree file not included in the source archive. The complete same boundary is present in bundled `README_FIRST.md:75–82`, `VERSION.md:20–23`, and `BUNDLE_METADATA.txt:14–15`, and the nested source `README.md:58–61` is also explicit. No instruction, dependency, or limitation is missing. This is a dangling convenience reference only; reopening the archive would create more submission risk than leaving it.

### Human portal gates — resolve before submission

1. Replace `[[POSTAL_ADDRESS]]` in the private `BIORXIV_METADATA.md`, `JMB_COVER_LETTER.md`, or `TPB_COVER_LETTER.md` actually used. The bundled private checklists already mark this as an author-only gate; it is absent from the public referee/source archive.
2. Confirm the city and country to use for the unaffiliated author. The current [Journal of Mathematical Biology instructions](https://link.springer.com/journal/285/submission-guidelines) say the title page should give affiliation city/country and that temporarily unaffiliated authors will have their city and country of residence captured. If portal entry alone suffices, the frozen PDF can remain unchanged; if the technical check requires it on the title page, add the author-approved location and refreeze.
3. Upload the tarball as the portal's first “Online Resource” and supply a concise caption. The same official instructions allow multiple files in `.gz` format, ask that supplementary material be cited as an Online Resource, and request a caption. This is portal labeling; it does not require changing the archive contents.

## Disclosed boundaries and unresolved assumptions

- The annotated Git tag is unsigned. Local/remote resolution and every repository-backed blob/mode were verified, but no signer identity can be authenticated from the package alone.
- Python itself, Tectonic 0.16.9, Poppler 26.08.0, and Tectonic's TeX resources are external. Python certificate replay is offline once CPython 3.14.6 exists; PDF rebuilding on a clean host may require the standard Tectonic resource cache/endpoint. The package states this accurately.
- The upstream SymPy/mpmath projects were not line-by-line security-audited. Their supplied wheels are byte-identical to upstream release artifacts, safe as archives, pure Python, and internally consistent by every wheel `RECORD` hash/size.
- No endpoint result at `r=R_hyb`, uniformity as `r` approaches one, singular or size-dependent response optimization, finite-size usefulness bound, global upper bound on `R_sim`, or complexity bound for the least-dyadic search is claimed. These excluded scopes are not gaps.
- There is no machine-formal proof. Arbitrary-size and asymptotic claims were checked by derivation, with finite calculations used only for independent corroboration.
- The private postal address and unaffiliated city/country are human identity data and were intentionally not inferred. They remain the only pre-upload information gap.

No required mathematical, source-inspection, execution, artifact-identity, alternative-cross-check, or visual-review task is unresolved. Only the human portal fields above remain.

## Supporting audit artifacts

- `../work/THEOREM_LEDGER_V202.md` — detailed hypotheses, scales, strictness, uniformity, quantifiers, and computational dependencies.
- `../independent_checks/math_repair_v202_audit.md` and `math_repair_v202_check.py` — independent analytic and exact-rational repair review.
- `../independent_checks/package_software_v202_audit.md` — archive, wheel, Git, executable, network-denied replay, optimization, mutation, and rebuild audit.
- `../independent_checks/adversarial_submission_v202.md` — hostile cross-domain submission review.
- `../independent_checks/exposition_metadata_v202_audit.md` — independent reader-facing, metadata, declarations, references, and typography review.
- `../logs/commands.tsv` and `../logs/full_transcript.log` — complete command/status/version/output records.
- `../rendered_pages/page-01.png` through `page-21.png` — page-by-page visual evidence.
- `../RESEARCH_LOG.md` — timestamped checkpoints and completion estimates.

## Verdict

**fully validated**
