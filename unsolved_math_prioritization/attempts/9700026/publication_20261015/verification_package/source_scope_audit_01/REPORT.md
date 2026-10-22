# PR880 source and target-scope audit

Audit family: independent source/model/target adversary. Exact target: **9700026 / AMR-096-0026**. Frozen head: `fba74a301786f9648e48722e76f440097b0746c2`. Completed UTC: 2026-10-15T09:34:31.713358+00:00.

## Decision

**PASS for the bounded source/target interpretation, conditional on the separately assigned analytic proof check.** The persistence claim in `source/author/PROOF.md` addresses the actual hard weighted-Voronoi area ODE displayed in the 2007 notes. Its region `alpha>1, beta>2alpha` lies inside the literal collapse alternative in Conjecture 32(a), including `(alpha,beta)=(2,8)`. The exact-ID imported statement retains that alternative. Therefore, if the claimed all-positive-weight persistence theorem is valid, it refutes the literal 2007/catalog conjunction and does not merely defeat an exceptional symmetric equilibrium.

No source-based falsification of that narrowly stated refutation was found. This family does **not** certify analytic correctness, current global novelty, the intended corrected conjecture, or complete resolution of all questions attached to this model. It found a concrete bibliographic error in the prior imported report: the 2012 paper does not discuss the displayed frozen-city dynamical system as that report claims.

## Independence and actual primary reading

`INDEPENDENT_SOURCE_MEMO.md` was saved before reading inherited author mathematics, source verdicts, the exact catalog record, or the exact prior report. It independently fixed the model and success criteria. Only afterward were the unchanged author proof, author source audit, author public metadata, and package wrapper read for scope comparison. Earlier acceptance reports were not used as source authority.

Primary sources were the [2007 technical notes](https://www.stat.berkeley.edu/~aldous/Research/OP/cities-notes.pdf), [version-pinned 2012 paper](https://arxiv.org/abs/1209.5120v1), and live [author problem page](https://www.stat.berkeley.edu/~aldous/Research/OP/cities.html). The author page was opened on 15 October 2026 and its two document links followed. The arXiv version page identifies v1, submitted 23 September 2012. This authenticates the document relationship, not a later-literature status claim.

Reading was explicit: 2007 printed/PDF pages 1-9 and 39-41 were read completely in layout text; the entire 41-page extract was searched for model, exponent, general-position, notation, and associated-system restrictions. Complete pages 2, 4, and 40 were rendered and visually inspected. The entire 11-page 2012 layout extract, including discussion and references, was read; model pages 2-3 and the plot-only page 8 were rendered and inspected. No claim is made to have read every proof on 2007 pages 10-38.

| Primary PDF | Bytes | SHA-256 |
|---|---:|---|
| 2007 notes, internally dated 25 April 2007, 41 pages | 295226 | `9cfbe9da2660fcea7e44d7ef013cb7a8a1604ff54a9e7734e71ef76959c38b89` |
| arXiv:1209.5120v1, 11 pages | 398185 | `eeecb371b6e6c2860c01e1b73d812468b619ddb7e3c4cd1d0e3affc056e8a077` |

The served arXiv PDF has internal creation metadata from November 2024, while its visible header and version URL identify the 2012 v1. The byte pin, rather than assumed historical PDF-generation bytes, identifies what was actually checked. PDFs, extracts, renders, raw records, and raw corpora are private and excluded from the public allowlist.

## Exact model and claim boundary

For fixed finite sites `x_i` in `D=[0,1]^2` and a probability vector `z`, define `A_i(z)` as the planar area where `z_i^alpha |y-x_i|^(-beta)` attains the **maximum** over cities. The deterministic system on printed page 40 is `z_i'=A_i(z)-z_i`. A common factor `c0` cancels from the maximizing cells. The initial coordinates are positive, and the sites and initial values are qualified by an undefined general-position condition. Sites remain fixed.

The full 2007 model declaration on page 2 allows `alpha>0, beta>0`; its focus on `alpha<1` does not restrict the declared domain. Page 4 separately discusses `alpha>1` and includes it in the proposed unbalanced region. The complete Conjecture 32 on page 40 has:

- (a) vertex collapse under `alpha>1 OR 0<beta<2alpha`;
- (b) convergence of all coordinates to positive limits independent of the initial vector under `0<alpha<1 AND beta>2alpha`.

There is no exponent normalization, no requirement `beta<=2alpha` attached to the `alpha>1` alternative, and no defined genericity condition that silently supplies such a parameter restriction. The source's disjunction is literal and agrees with the imported record.

This is a hard allocation model. The separate probability-proportional-to-influence variant is explicitly mentioned as a different, unstudied variant on 2007 page 6. Substituting influence-sum shares would change the problem.

The full stochastic process differs: new cities can be founded, the immigrant chooses the maximizing city only after deciding against founding a city, and the number of sites changes. On 2007 page 7 the existing-city increment probability is an integral of `I/(1+I)` over its hard cell, not exactly its area. Page 40 introduces the fixed-city ODE through an informal approximation and time normalization. It does not prove a theorem equating the deterministic claim with the stochastic process.

The 2012 paper declares `0<alpha<=1, beta>0` on page 2, retains the hard maximum, presents heuristic long-time arguments and simulations, and discusses the critical `alpha=1` case. It does not state Conjecture 32 or the frozen finite-city ODE. Its page-3 comment about `alpha>1` does not amend the earlier notes. Consequently the offered `(2,8)` counterexample is outside the 2012 paper's declared parameter domain and should not be advertised as refuting that paper's stochastic predictions.

## General position, invariance, and boundary checks

Distinct sites give pairwise ties on circles or lines, hence on zero-area sets. The genericity phrase occurs once in the 2007 text and has no formal definition. A proof for every finite collection of distinct interior sites and every strictly positive initial vector covers any ordinary nonempty generic subset of this class. Such a theorem defeats a genericity objection; a symmetric equilibrium alone would leave that objection open. Restricting to interior sites is legitimate for a universal statement allowing sites anywhere in the square. Repeated sites, initial zero weights, and the trivial `n=1` case are not required for the offered counterexample.

The cells depend only on `q=alpha/beta`. Equivalently, the influence for `(2,8)` is the fourth power of the influence for `(1/2,2)`, so the maximizers and vector fields agree exactly, with no time change. Yet the first pair falls under 32(a) and the second under 32(b). This is an immediate source-level inconsistency between the two unrestricted predictions. It does not by itself decide which prediction fails; the offered persistence theorem supplies the claimed direct refutation of (a). This observation is already present in the inherited package and is not claimed here as a new contribution.

| Assertion | Effect of the offered persistence theorem if valid |
|---|---|
| Literal 32(a), `alpha>1` with `beta>2alpha` | Refuted for `n>=2`, including an open generic class |
| Literal catalog conjunction (a) and (b) | False because (a) is false |
| Collapse restricted to `0<beta<2alpha` | Not settled |
| Critical line `beta=2alpha` | Not settled; (a) still asserts collapse there when `alpha>1` |
| `alpha=1, beta>2alpha` | Outside both 32(a) and 32(b); no conclusion here |
| Positive convergence, unique limit, initial-condition independence | Not established by persistence alone |
| Stochastic city-founding process or 2007 Conjecture 1 | Not refuted or proved by this ODE result |
| Current literature priority or novelty | Not checked by this family |

## Exact-ID catalog and prior-report authentication

The unchanged root corpora were hashed in full and filtered only for exact numeric ID `9700026` and its report key `AMR-096-0026`. There is exactly one catalog match, one complete problem-record match, and one report-key match. Their full private canonical pair uses Python's default `json.dumps([complete_matching_record, reports.get(problem_number,{})], sort_keys=True)` followed by UTF-8 encoding. Its length is **4,409 bytes** and SHA-256 is **`7b18458d71482e2c4e1c62601be1824eba6ad6243c78135d90d1b75223e8e193`**, exactly the catalog `review_hash`. The statement's UTF-8 SHA-256 is **`5544971834bd618005b3fdf611f753b4cf41bab24b857d0e96a7a067ee3f7b7e`**, exactly its catalog binding. No fields were projected out of the pair.

| Corpus locator | Complete records | Bytes | SHA-256 |
|---|---:|---:|---|
| `unsolved_math_prioritization/catalog.json` | 15458 | 21735099 | `891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566` |
| `unsolved_math_prioritization/cache/problems.json` | 15458 | 68931837 | `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf` |
| `unsolved_math_prioritization/cache/research_results.json` | 6701 | 80334822 | `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b` |

The problem record explicitly requests the same general-position, positive-weight, two-part stability dichotomy, including the unrestricted `alpha>1` disjunct. Its provenance points to `cities.html`, the technical notes, and Conjecture 32. The complete prior report classifies it OPEN-TRIAGE, treats the transcription as faithful, reports literature searches without an identified resolution, and requests proofs of both branches. It contains no authored mathematical proof or counterexample. Its negative-search claims are hypotheses, not novelty evidence. Its sentence attributing discussion of this dynamical system to the 2012 paper is unsupported by the full paper. None of this invalidates the primary 2007 transcription.

These are historical root metadata locators; the cached local status `queued, 0/5` is not the original PR queue. The parent-specified frozen PR provenance is `claimed_solved, 2/5`. This audit made no queue/status edits and is not a fresh proof attempt.

## Reproducible checks and exact remaining gap

`check_source_scope.py` uses only the Python standard library. It reads private originals without printing their contents, verifies the three full corpus pins and counts, selects the exact ID, reconstructs the full pair, checks both catalog bindings, checks the two primary PDF pins, verifies the complete source freeze, and checks the exponent/parameter arithmetic with exact rational numbers. `CHECK_RESULTS.json` records **18/18 passing checks**. The freeze has exactly **40 files / 276,581 bytes**, all matching the supplied manifest SHA-256 **`b0b0cdc72798cfcffc5fefeec1de30ff422f54bde83d0f8a91fd2e6a87311d8b`**.

Run from the workspace using the saved script with `--workspace /Users/alec/Documents/Math --audit /Users/alec/Documents/Math/draft_pr_claimed_solved_800_900_20261012/audits/pr880_9700026`. The checks prove identities and finite algebra. They cannot replace human reading, the analytic persistence proof, or a priority campaign.

The exact remaining gate is separate independent verification of the analytic theorem for this ODE, followed only if it passes by the parent-authorized deeper priority audit. Within this family, source/model/target fidelity is complete (100%); full-problem resolution and current novelty are not certified. No Git/PR/Zenodo/sheet mutation, publication, outreach, or new central proof search was performed.
