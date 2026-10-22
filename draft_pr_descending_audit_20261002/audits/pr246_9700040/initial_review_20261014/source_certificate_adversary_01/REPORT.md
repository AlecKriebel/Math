# Independent source-scope and finite-certificate adversarial audit

**PR 246 / 9700040 / AMR-096-0040. Native head `0b4db59eb5515f2d90d8b8df33b6b729b78b48f1`.**

**Disposition:** the explicit simultaneous stationary law and its rational truncation certificate pass this distinct audit family. I found no mandatory mathematical or source-scope correction. The unchanged executable has reproducible precision-display and default-runtime limits; those are qualifications on executable packaging, not counterexamples to the formula or to the existence of an effective finite rational evaluation algorithm. Historical priority and proposer acceptance remain unverified.

This assessment binds the original 20-file packet frozen under `initial_review_20261014/submitted/unsolved_math_prioritization/attempts/9700040/`. The parent-provided live revalidation at 2026-10-15 03:35:47 UTC reports the same open draft head and queue status `claimed_solved`. That status is a claim being audited. I did not change Git state, original inputs, queue/PR/publication/tracker state, or contact any external individual.

## Method and independence

I first read the submitted proof, sources and implementation as hypotheses, fetched primary sources, and saved `INDEPENDENT_RECONSTRUCTION.md` and `CERTIFICATE_DERIVATION.md` before opening inherited review verdicts. These notes reconstruct the exact question, the all-index event class, the RSK counting mechanism, and the certificate independently. Only afterward did I inspect the inherited manifests, verdicts and controls. Agreement with an inherited pass is not the basis for this conclusion.

The analytical work is checkable in those two derivations. `certificate_controls.py` supplies fresh finite falsification controls, `replay_originals.py` replays the original checks without editing them, and `audit_inputs.py` verifies original/native bytes and historical manifest crosslinks. Full receipts, including exact fractions and observed failures, are retained. Finite assertion counts are regression evidence and are not substituted for a universal argument.

## Exact source and descriptive scope

The live [Aldous question](https://www.stat.berkeley.edu/~aldous/Research/OP/left_Hamm.html) defines the finite ordered positive-particle process with velocity equal to position and intensity-one Poisson space–time events moving the nearest particle to the right when one exists. Events beyond the final finite particle do nothing. It states consistency as the number of particles varies and uniqueness of a stationary law, then asks: “Give some (fairly explicit) description of the stationary distribution.”

The natural target is the probability law of the simultaneous ordered configuration. A full family of finite simultaneous joint distributions addresses that target. A multi-time transition formula, an elementary density, or an algorithm fast in all indices is not demanded by the source. Conversely, one-particle marginals, existence alone, simulations, or a representation that leaves the unknown joint rank law unspecified would not give the same coverage.

The candidate's event class is sufficient. For arbitrary finitely many positive indices and thresholds, sort distinct positive thresholds, merge equal thresholds using the smallest associated index, and discard nonpositive thresholds. No monotonicity of indices is needed. An empty conjunction has probability one. Finite inclusion–exclusion of survival-event complements recovers every joint CDF. A single common Poisson construction supplies finite-k consistency and positivity; it is stronger evidence than merely postulating consistent numerical values.

The provided positive sums of factorial determinants, bounded matrix dimension, and explicit rational error furnish a defensible affirmative interpretation of the qualitative request. This is a source-scope judgment with concrete grounds, not evidence that the proposer has accepted the result. The page remains the authoritative statement even when dataset triage or queue descriptions use stronger or looser language.

## Primary-source authentication and limits

All six primary objects in the submitted `source_manifest.json` were independently fetched as raw bytes and match both its byte counts and SHA-256 pins. An initial DNS failure for the published Schur-sampling PDF was transient: the later independent retry succeeded. I also independently hashed the parent's six shared private reading objects; all match. `SOURCE_ACCESS_RECEIPTS.json` records requested/final URLs, actual UTC retrieval times, HTTP metadata, byte counts, SHA-1/SHA-256, selected PDF metadata and inspected-page extraction hashes. `SHARED_SOURCE_PIN_VERIFICATION.json` binds the separate shared-object check and the parent's retrieval receipt.

| Primary object | Material checked | Version/scope limit |
|---|---|---|
| Aldous problem page | Exact finite model, consistency, stationary-law request | Current bytes match the author's October 1 pin; no February 2018 web snapshot was authenticated |
| Aldous–Diaconis, unpublished 1993 notes | Section 4.1, printed 36–38; section 4.2, printed 39; limiting rank representation, coupling, low-index formulas | Dated July 8, 1993; unfinished placeholders and a warning about an inconsistent result prevent treating every surrounding assertion as established |
| Aldous–Diaconis, 1999 article | RSK/LIS identification and Proposition 4; section 5.2 fixed-pile context | Published primary context; its marginal/constant formulas do not by themselves certify historical closure of the later all-law question |
| Okounkov–Reshetikhin | v3 section 2.2.4, equations (7)–(8), skew determinant and containment | Exact arXiv v3 bytes, dated January 31, 2003 |
| Betea et al., published 2018 | Section 6, printed 415–416, equation (6.6), exponential/tableau specialization and Poissonized RSK context | Published 38-page object authenticated; the author's locator “Section 6.3” is imprecise: 6.3 is an equation label, while the relevant section is 6 |
| Aldous–Diaconis, 1995 | Context and object authentication | No hard theorem from this scan is needed for the candidate's finite counting or certificate |

An additional exact arXiv v3 copy of Betea et al. was fetched and pinned as a distinct 26-page object, not silently substituted for the published PDF. The relevant identity agrees. The authoritative primary links and every byte pin are in the receipts. HTTP `Last-Modified` values, some coinciding with retrieval time, are metadata only and are not used to infer publication chronology. Full third-party PDFs, HTML, extracted texts, page images, and provider responses are excluded from this public authored audit folder.

## Strongest verified mathematical statement

Let `D_t(lambda/mu)` be the submitted factorial determinant. For any increasing positive real thresholds `x_1,...,x_m` and positive integer indices `r_1,...,r_m`, the stationary probability of all inequalities `X_(r_j)>x_j` is the submitted equation (3): a positive nested-partition sum with row bounds `r_j-1`, multiplied by `exp(-x_m)`. Its transpose uses determinant dimension `B=max_j(r_j-1)`, independent of terminal size. The same law works for every finite particle projection. For rational thresholds and a prescribed positive rational error, a finite rational certificate can be computed in principle by choosing a sufficiently large terminal-size cutoff.

The mechanism survives reconstruction. On a positive-quadrant unit Poisson field, the longest-chain count in `(0,x]×(0,t]` is the number of pile tops at most `x`. The coordinate change `Y_i(s)=e^s Z_i(e^s)` maps events by `(u,v)->(uv,log v)` with unit Jacobian. It produces the exact velocity and jump rule and is stationary by area-preserving anisotropic scaling. The first k coordinates are autonomous. Local rectangle finiteness and a successive-strip chain construction ensure finite, strictly ordered coordinates and no finite accumulation. The source's known uniqueness or the submitted explicit synchronous coupling identifies the invariant law.

Conditional on Poisson strip counts, the vertical ranks in horizontal order form one uniform permutation. RSK counts a prefix-shape chain by the final insertion-tableau count times the product of skew recording-tableau counts, divided by the total permutation factorial. The Poisson strip probabilities supply the remaining factorials and strip powers. There is no missing binomial factor, independent-prefix assumption, or unproved index-Markov property. Summing unconstrained chains of terminal size n yields exactly `x_m^n/n!`. Positivity and absolute convergence follow. These deductions, rather than finite enumeration alone, support the universal formula.

The 1993 random-rank representation does not already give a specified general joint rank law; the series removes that unknown quantity. The packet correctly credits the known first marginal and two-particle law. Reconstructing those facts does not establish a novel contribution.

## Certificate: normalization, extrema, monotonicity, and termination

Put `x=x_m`, `W_N=sum_(n<=N) w_n`, `T_N=sum_(n<=N)x^n/n!`, where `0<=w_n<=x^n/n!`. If `E` is the true unconstrained omitted raw mass and `F` its constrained portion, then

`P=(W_N+F)/(T_N+E)`, with `0<=F<=E<=R_N` and `0<=W_N<=T_N`.

For `N+2>x`, the ratios after the first omitted term are bounded above by `x/(N+2)<1`, giving the stated geometric `R_N`. Minimizing and maximizing over both unknown tails yields exactly

`W_N/(T_N+R_N) <= P <= (W_N+R_N)/(T_N+R_N)`.

Both endpoints lie in `[0,1]`; their difference is `R_N/(T_N+R_N)`. These endpoints are sharp over the information class `0<=F<=E<=R_N`: the lower uses `(E,F)=(R_N,0)` and the upper `(R_N,R_N)`. They need not be attained by an actual query because the actual exponential tail is fixed and generally smaller than the geometric bound. In particular, constrained omitted mass is bounded by the actual omitted mass before replacing it with `R_N`; treating the normalizer independently or as fixed at `T_N` would lose the correct inequality.

The derivation also establishes nested intervals. With `a=x^(N+1)/(N+1)!` and `k=N+2>x`,

`R_(N+1)/R_N=x(k+1)(k-x)/(k^2(k+1-x))<1`,

`(T_N+R_N)-(T_(N+1)+R_(N+1))=a*x^2/[k(k-x)(k+1-x)]>0`.

Thus the width decreases, the lower endpoint increases, and the upper endpoint decreases for the same event. These are analytic identities, independently checked on exact rational grids in the controls.

A finite cutoff exists effectively for every positive rational x and error. After `N+2>=2x`, omitted terms decrease at least geometrically and `R_N<=2*x^(N+1)/(N+1)!` tends to zero; `T_N>=1`. A rational comparison loop terminates. Finding the cutoff requires no partition computation. Only afterward are finitely many shapes and rational determinants needed. Finite inclusion–exclusion queries can divide an error budget among their terms. Unspecified noncomputable real inputs are outside an executable rational-input claim.

## New controls and complete original replays

`CONTROL_RECEIPTS.json` records **99,955 exact assertions** and complete exact control data. Material controls include:

- 6,561 exact unknown-tail information-class points plus boundary extrema and probability-range controls.
- 7,077 cutoff points checking tail-ratio and enlarged-normalizer identities; 27,808 nested-interval checks for four independently chosen admissible coefficient families.
- Fifteen effective-cutoff queries from `x=1/100` through `101/2` and errors through `10^-40`. For example `x=101/2`, error `10^-40` selects `N=171`; this is a cutoff calculation, not a claim that a large-index determinant evaluation is fast.
- Seventy coefficient comparisons through total point count six against direct permutation enumeration with quadratic LIS evaluation, rational strip widths and nonmonotone indices.
- Seven consistency checks inserting an unused intermediate threshold and seven complete joint-CDF coefficient checks by inclusion–exclusion against direct counting on the same final rectangle.
- Forward Young-lattice path counts checking 1,380 determinant/padding instances and 690 transpose instances, including `t=0`.
- All 120 orders of a query containing repeated and nonpositive thresholds reduce to the same mathematical event. Eleven documented-domain invalid queries are rejected; the exact observed exceptions are retained.

`ORIGINAL_REPLAY_RECEIPTS.json` includes the full parsed outputs of the unchanged author checker and inherited independent checker. Their stdout bytes match the original receipts exactly: **49,618** and **15,580** assertions respectively. The historical 42 coefficient comparisons are also reproduced, with each expected/actual exact fraction retained. This reproduces the claimed finite evidence; it does not authenticate the old review's psychological independence or historical research completeness.

## Executable audit and findings

The dynamic programming correctly implements the transposed formula on its documented nonempty, strictly increasing positive rational threshold domain. It enumerates all shapes of size at most N and length at most B, uses exact `Fraction` elimination, and groups terminal weights by size. Determinants have the fixed dimension B, including the valid empty determinant when B=0. Positive increments and containment match the proof. Exact returned fractions are the certificate.

Let S be the number of enumerated shapes. The routine can inspect on the order of `m*S^2` shape pairs and use dimension-B rational elimination; exact arithmetic costs also grow with numerator/denominator sizes. With fixed B, the shape count grows polynomially with a B-dependent exponent; when B grows with N the unrestricted partition count grows much faster. Both `partitions` and `D` use unbounded caches, so separate queries retain memory. Fixed determinant dimension does not imply efficient evaluation. No favorable runtime bound is claimed, and none is inferred.

| Finding | Evidence and implication | Disposition |
|---|---|---|
| Exact certificate and source coverage | Independent derivation and full law reconstruction above | **No mandatory mathematical correction** |
| Decimal display is not an outward enclosure | For `x=1,r=1,N=18`, both displayed bounds equal `0.36787944117144233` although exact width is `20/6282647653285676001`; the displayed lower exceeds the exact lower. At N=200 the displayed width is zero while the exact width is positive | Correctly labeled `display_only`; optional outward decimal rendering or an explicit display note |
| Unchanged CLI is not uniformly arbitrary precision under default Python settings | Actual `--x 1 --indices 1 --cutoff 1600` fails at the default 4,300-digit integer-to-string limit on Python 3.14.6 | Optional packaging hardening; **must qualify any stronger promotional claim that this unchanged default CLI handles every arbitrary precision request**. Mathematical finite rational evaluation remains valid |
| Recursive enumeration and unbounded caches | `partitions(1000,max_part=1,max_length=1000)` reproduces `RecursionError`; cache sizes and full failure traces retained | Optional iterative enumeration, cache management or runtime documentation; no abstract algorithmic obstruction |
| Query wrapper is narrower than the mathematical event class | Repeated/nonpositive/descending thresholds are rejected; empty module query raises `IndexError`; `True` is accepted as integer index 1 under Python's type hierarchy | Documented sorted-positive CLI domain is honored. Optional normalization/tolerance wrapper and consistent input errors |
| Citation locator | Published Schur-sampling identity is section 6, equation (6.6), printed 415 | Optional editorial correction of “Section 6.3” |

There is no float arithmetic in the raw summation or rational enclosure. The displayed approximation cannot invalidate the exact endpoints as labeled. There is also no promise of a practical finite machine completing all unbounded inputs; the mathematical termination argument describes an effective procedure with finite resources for each fixed input, allowing resource limits to be increased. A direct description of the library/CLI should preserve this distinction.

## Provenance verification and remaining gap

`INPUT_VERIFICATION.json` independently computes plain SHA-1, SHA-256, byte size, and Git blob SHA-1 for every one of the 20 originals. All match intake native identifiers. Each of the 20 native provider bodies is independently base64-decoded, size-checked and byte-compared with its submitted file. All **35** entries across the frozen, publication and review manifests match, as do inherited proof/evaluator/source crosslinks. There are no extra submitted files. The saved transport receipts and live-revalidation input are pinned; this shard does not represent those saved transports as fresh live API fetches.

The exact strongest result is therefore a verified classical-consequence description of all simultaneous finite stationary distributions with an effective rational certificate. No remaining mathematical gap in this audit family has been found. Descriptive explicitness is a reasoned interpretation of a qualitative source request. Historical novelty, an exhaustive priority result, and proposer acceptance are separate unresolved claims and are not inferred from mathematical correctness or the page's continued listing.

For the later distinct priority phase, plausible covering mechanisms are already present in the cited primary literature: the 1993 stationary/random-rank connection, the 1999 RSK and Poissonized marginal determinant formulas, the 2003 general Schur-process weights and restriction structure, and the exponential-specialization/Poissonized RSK framework articulated in Betea et al. These identify concrete places to seek an earlier equivalent all-law description. Generic availability of those ingredients alone does not justify classifying this exact question as historically `already_solved`; a covering source or an explicit equivalence/coverage argument must be checked in that phase. No outside input is needed for this audit conclusion and no outreach was prepared.

`FINAL_AUDIT_MANIFEST.json` binds all public authored artifacts and original inputs, explicitly excluding full third-party reading objects and its own recursive hash. This audit phase is complete; further priority work is a separate task.
