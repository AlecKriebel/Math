# Independent recent and exact-problem priority audit

PR246 / 9700040 / AMR-096-0040. Candidate head supplied for this assignment: `0b4db59eb5515f2d90d8b8df33b6b729b78b48f1`.

## Finding and its precise limit

I did not locate a primary source published after the February 2018 posting that explicitly gives the stationary all-finite-coordinate law of the exact drift-jump system, or explicitly identifies an existing full joint law as its answer. This is a bounded search finding, not a novelty certificate. The submitted candidate itself says that it is a classical RSK/Schur consequence without a novelty claim. The audit provides no basis for upgrading that to an independently established historical contribution.

The strongest verified prior coverage in this lane is substantial: the July 8, 1993 Aldous–Diaconis notes already define this exact finite-particle process, describe a deterministic rescaling, represent stationary positions through limiting pile-top ranks, give synchronous-coupling uniqueness, and calculate the two-particle density. The 1999 survey connects the first fixed number of pile tops to a recurrent finite-particle process. Neither inspected location gives the candidate's positive all-threshold nested-partition sum with its explicit rational truncation certificate.

Recent papers returned by broader searches do not automatically close this gap. The closest RSK follow-up concerns a bulk scaling limit around a positive spatial location; the target asks about a fixed number of particles next to the boundary at zero. Ordinary stationary Poisson Hammersley configurations have a quantitatively different two-particle law. These distinctions were checked against primary model definitions, rather than inferred from titles.

## Independence and authorized scope

`INITIAL_INDEPENDENT_ASSESSMENT.md` was saved at 2026-10-15T03:52:31.808620+00:00 after reading the original submission and live target page, before reading any inherited review or another priority family's result. No inherited review or other priority-family result was subsequently used. All written artifacts are within this assigned directory. No Git/index/ref operation, provider mutation, classification change, or external individual communication was performed.

The task is a priority/source audit. It does not independently rerun the parent mathematical-validation lane or decide whether the source author's informal explicitness standard is met. The comparison calculations below test model identification only.

## Exact claim tested

For every finite ordered set of positive thresholds and positive particle indices, the candidate supplies the stationary joint survival probabilities by a positive sum over nested Young diagrams, with each diagram constrained by its first-row length; weights are exponential-specialized skew Schur determinants. It identifies the underlying stationary process as

```text
Y_i(s) = exp(s) Z_i(exp(s)),
Z_i(t) = inf {x : L(x,t) >= i}.
```

where L is the longest increasing chain in a unit-Poisson quadrant rectangle. It also gives a rational finite-sum enclosure.

The exact source process has `0 < X_1 < ... < X_k`, deterministic drift `dX_i/ds = X_i`, unit Poisson events in positive space-time, nearest-strictly-right replacement, and no effect for events above `X_k`. A prior source would cover this target if it proves these dynamics or an exact conjugacy, and supplies a simultaneous finite-coordinate law. Existence, individual marginals, large-index asymptotics, or an unrelated Poisson invariant measure do not alone meet that criterion.

## Search performed

The authored `QUERY_LEDGER.json` contains 76 queries with UTC times, discovery URLs, and bounded outcomes. Complete raw returned excerpts remain in private reading storage, outside the authored manifest. Queries cover:

- Exact title, URL identifier, distinctive wording, hyphenation variants, and explicit solution wording.
- First/leftmost/fixed piles, pile tops, rescaled top cards, fixed particle prefixes, and joint/finite-dimensional distributions.
- Drift, exponential or linear drift, time changes, scaling/self-similarity, stationary Hammersley models, and Schur/Plancherel connections.
- Date-filtered post-2018 and 2021–2026 follow-ups, followed by actual primary version-history checks. Search date filters are not treated as bibliographic evidence.

An independent citation-discovery screen obtained the full bounded OpenAlex responses for the exact 1999 survey and the exact 1995 paper, restricted to indexed publication dates from 2018 onward: 90 and 64 records, respectively. Their 144-record union and per-record decisions are in `CITATION_SCREEN.json`. All returned titles and selected available indexed abstracts were screened, and the materially relevant leads below were retrieved from primary repositories. This does not claim that every citing item was read in full or that the index is complete. Duplicate preprint/journal entries remain visible.

Full primary PDFs were downloaded for the recent RSK/particle, t-PNG, weighted-line, thesis, and commentary leads; relevant definitions, theorem statements, and crossreferences were inspected. `SOURCE_PINS.json` records their bytes, retrieval times, and version URLs. Each arXiv version URL was separately fetched and compared with the initially downloaded PDF. Current Berkeley HTTP modification headers were not used to date old manuscripts; their title pages and the problem page supply the content dates.

## Checked distinctions that prevent false priority conclusions

### 1. The same old finite-particle question

[The exact problem page](https://www.stat.berkeley.edu/~aldous/Research/OP/left_Hamm.html) explicitly traces the process to section 4.1 of the unfinished notes and section 5.2 of the 1999 survey. The freshly retrieved notes' title page is dated July 8, 1993. Printed pages 36–39 contain the relevant model and calculations. Thus the 2018 post is not the origin of the mathematical model.

The notes' displayed rescaling is draft material and was not accepted as an independently correct formula merely because it appears there. Their direct process definition agrees with the target. Their limiting-rank representation leaves an unspecified joint rank law at general k. This prior coverage neither establishes the candidate's historical novelty nor constitutes a checked prior appearance of its particular all-threshold determinant formula.

### 2. Bulk RSK limits are not the fixed-left-pile law

Marciniak–Maślanka–Śniady, [arXiv:2005.13824v3](https://arxiv.org/pdf/2005.13824v3), dated December 14, 2022, published in *Advances in Applied Mathematics* 145 (2023), studies RSK on independent uniform inputs. Corollary 1.4, PDF p.7, centers row entries at a fixed `0 < w < 1` and multiplies deviations by `sqrt(n)`, obtaining independent Poisson processes. It allows `w = 1` separately; it does not allow `w = 0`. Section 1.10, pp.11–13, relates this to Aldous–Diaconis's bulk theorem.

For the fixed-left-pile question, the first few top values are of order `1/n`, rather than fluctuations of order `1/sqrt(n)` around fixed `w > 0`. Setting `w = 0` in a theorem that excludes it is an unsupported boundary passage. Therefore this recent primary result is not a checked prior answer for the target law.

### 3. A homogeneous Poisson configuration fails a low-coordinate check

This is an independently reconstructed separation check from the credited 1993 two-particle formula, not a claim of a new result. The source gives

```text
p_2(x1,x2) = exp(-x1) a(x2-x1),
a(u) = sum_{j>=0} q(u,j) [1/(j+1)! - 1/(j+2)!].
```

At `u = 0`, `a(0) = 1/2`, and `X_1` is exponential of rate one. A homogeneous Poisson configuration compatible with that first-particle law would have intensity one and next-gap density `exp(-u)`, whose value at zero is one. The continuous densities differ near zero. Thus ordinary spatially homogeneous Poisson invariance cannot be substituted for the target even at two coordinates.

This rules out an identification of the resulting laws; it does not rule out every imaginable transformation of another process. Any transformation proposed as prior coverage must still be exhibited and checked.

### 4. The candidate's stationary change uses scaling, not spatial translation

For `x = uv` and `s = log(v)`, the inverse map is `u = x exp(-s), v = exp(s)`, and

```text
det( d(u,v) / d(x,s) ) = 1.
```

Between Poisson events a fixed u-coordinate yields `x = u exp(s)`, hence `dx/ds = x`. An event preserves the ordering and replaces the nearest-right coordinate. Events beyond a finite prefix are immaterial. This gives the relevant mechanism to compare against a prior paper.

By contrast, the stationary models in Boyer's thesis, the Poisson–Kirchhoff paper, and Drillick–Lin's Burke theorem use translation invariance and nonzero boundary sources/sinks. The recent t-PNG local-limit theorem moves observation windows to infinity. Their inspected statements do not supply the above scaling construction plus its fixed-prefix joint distribution.

### 5. Backwards TASEP has different rates and state space

Petrov–Saenz's [arXiv:1907.09155v2](https://arxiv.org/pdf/1907.09155v2), section 1.2, has particles on the integer lattice and a hole clock whose rate equals the number of particles to its right. The target has continuous coordinates and unit intensity per spatial location, with deterministic coordinate drift. The authors explicitly distinguish their space-inhomogeneous process from continuous-space Hammersley.

The later [arXiv:2212.01643v2](https://arxiv.org/pdf/2212.01643v2), published in 2024, extends intertwiners and trajectory couplings for TASEP and its deformations. No inspected statement identifies a continuous-space limit with the target or gives its stationary finite-coordinate law. Similar gap-attraction language is insufficient for an exact equivalence.

## Coverage and unresolved priority gap

`SOURCE_COVERAGE.md` gives claim-by-source locations and explicit limitations. The following is supported:

1. Exact-model definition, uniqueness mechanism, rank-based stationary representation, and two-particle law precede 2018.
2. The exact all-coordinate determinant formula/certificate was not located in the inspected recent primary sources or returned exact-problem searches.
3. Several seemingly relevant recent invariant-measure papers concern demonstrably different models or limits; those cannot be cited as an exact prior solution without a new, checked mapping.
4. The absence of a located closure does not establish that the proposed formulation is a novel mathematical contribution.

The exact residual gap is historical and substantive: identify a primary pre-existing statement already giving the full boundary/fixed-prefix law, or identify a new mathematical theorem or mechanism beyond the candidate's acknowledged classical RSK specialization and evaluation certificate. This lane establishes neither. It also does not assess every possible pre-2018 Schur-process specialization; the parent assigned that as a distinct approach family.

The live open-problem list is weak evidence of the literature's current state. Its own introduction says its updates are irregular and may omit relevant work. Continuing inclusion of the page is therefore not affirmative evidence of an unresolved problem, author endorsement, or novelty.

No outside input was sought. Further literature expertise could help resolve implicit coverage or the informal explicitness standard; this is recorded only as a limitation, without preparing outreach.

## Artifacts and completion

The primary reading directory is private and excluded from `AUTHORED_FILE_MANIFEST.json`. Public authored artifacts contain original analysis, queries, bibliography metadata, and hashes only. The manifest and completion receipt fix final bytes and UTC completion. Completion estimate for this assigned bounded recent-priority audit: 100%; the larger historical novelty question remains unresolved.

