# Exact-source scope and dependency audit: PR 838 / problem 10000036

Audit date: 14 October 2026 Pacific / 15 October 2026 UTC. Frozen PR head: `ed2de7249953ba0c1afad253adca9b820d7297c5`. Frozen author proof SHA-256: `c31b7a1cd6a3af04807b20d58f23d79f9d07cf4eb87df26187498f3260f9891d`.

**Decision: PASS for exact historical source scope and the cited dependency statements.** No mathematical scope correction to the author's Section 1 theorem is required. Conditional on that theorem passing the separate mathematical audits, ordinary nonuniform finite energy answers the full historical bond-percolation question. This is neither a proof acceptance nor a novelty/current-openness certificate.

This audit did not attempt a new construction. Original effort remains 3/5. It made no Git, index, branch, PR, queue, publication-service, or other service mutation and no external communication. All audit outputs stay in this dedicated folder.

## Independence and identity

The complete supplied descriptor, including its prior report, and the full frozen author proof, source list, and source manifest were read first. `INITIAL_SOURCE_INTERPRETATION.md` was saved at 2026-10-15T06:20:56.789163+00:00 before reading either old acceptance report. Old reviews were read afterward as historical records and were not used as proof certificates. No other fresh-family audit conclusions were read.

All six parent-retrieved public PDFs match the author's original byte-size and SHA-256 pins. The proof and source list also match the frozen source manifest. The initial descriptor's declared review hash was independently recomputed and matched to a read-only SQLite query of record 10000036. Both original raw dataset files match the local dataset manifest at revision `37e53eabe540fb458758e198be61634bd02ee008`; no raw record corpus or dataset was copied into public outputs. The matching review hash is `0f157faedf19230d980dca9da4b20d61008e0e2536d8c4eb785f4027df3d1778`.

These checks authenticate the supplied local record. They do not authenticate a live UnsolvedMath page or a present-day open-status claim. See `CURATED_RECORD_IDENTITY_CHECK.json` and `SOURCE_PIN_CHECKS.json`.

## Exact original target and its reconstruction

The literal item is transcribed once in `INITIAL_SOURCE_INTERPRETATION.md`. It appears as Open problem 8.15 on printed and PDF page 61 of the archived Saint-Flour notes. The paragraph immediately preceding it attributes the question jointly to the author, Olle, and Oded; it does not supply a formal BHS citation at that line. Its wording agrees with BHS Question 1.1. The archive file is 1,101,523 bytes, SHA-256 `aaab65b3acf65f4d21657da94464e9d5edb93969a4c353805099a220a0717cfe`. The PDF's creation metadata is from 2013, and the archive replay is dated 2020. Neither is a 2026 open-status determination. [Saint-Flour archive](https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf).

The exact interpretation supported jointly by the source context and the explicit BHS/BT antecedents is as follows.

| Issue | Checked evidence | Scope of the target / comparison with candidate |
|---|---|---|
| Bond or site | Saint-Flour Section 8.2 and Definition 8.9, p.59; BHS pp.1-2; BT Section 1.4, pp.4-5 | An edge law on the nearest-neighbor lattice. An external site construction or an internal site-thinning statement is not by itself a solution. The candidate is an external bond law. |
| Invariance | Saint-Flour Definition 8.9, p.59; BHS p.2 | The law is invariant under every graph automorphism, including translations, reflections, and coordinate permutations. Translation invariance alone would not match. The candidate states the full group. |
| Finite energy | BHS p.2 after Question 1.1; BT arXiv p.3 after Question 1 | For every edge, both conditional state probabilities given all other output edge states are positive almost surely. The definition imposes no common positive lower bound. The candidate asserts exactly this. |
| Dimension | The Saint-Flour sentence leaves d unqualified; BHS's surrounding motivation and BT's lattice setup use d >= 2 | The candidate proves its claimed theorem separately for every integer d >= 2, covering both an existential-in-d reading and a dimension-by-dimension reading of the historical question. d=1 is excluded and has no one-ended spanning-tree input here. |
| Almost sure percolation | The question concerns an infinite component of the realized X; BHS p.2 explicitly allows finite components in the motivating insertion-tolerant example | Almost every X has at least one infinite component. It does not require the origin or all vertices to lie in an infinite component almost surely. The candidate's unique infinite component is stronger than required. |
| Internal threshold | BHS p.1 defines Bernoulli bond percolation on the realized graph and its critical value by positive probability of any infinite cluster | For almost every X, fresh independent Bernoulli bond thinning fails to percolate at every p<1. X itself percolates at p=1. The candidate makes this quenched statement explicitly and also identifies the threshold of its infinite component. |
| Other requirements | None in item 8.15 | Mixing, ergodicity, uniqueness, and an internal site threshold are additional candidate assertions, not omitted target requirements. No FKG, finite dependence, finitary coding, or uniform-energy assertion belongs to the checked wording. |

The notes' Section 4.2, pp.32-33, initially discusses a rooted event and then defines p_c(G) on connected graphs. Applying that isolated discussion literally to require the origin to percolate almost surely would conflict with ordinary finite energy on a finite-degree lattice: a finite-energy law gives the finite pattern isolating the origin positive probability. The matching BHS question and its explicit allowance of finite components remove that ambiguity. Likewise, for disconnected X the unrooted graph definition in BHS p.1 is the relevant extension. This is a source-context inference, not additional wording printed in item 8.15.

The ordinary energy interpretation is explicit in [BHS arXiv v1](https://arxiv.org/pdf/math/9906002v1), p.2 and [BT arXiv v1](https://arxiv.org/pdf/1505.06069v1), p.3. A full-text search of the Saint-Flour notes found no local uniform conditional bound or alternate finite-energy definition; the short item alone does not define the term. It would therefore be incorrect to reclassify this as an unresolved mandatory uniform-energy component of the original question. The author's ordinary-energy qualifier is an honest clarification, not a retreat to a special case.

## Fixed-density sprinkling is a different hypothesis class

BHS Conjecture 1.2 / Theorem 1.3 and BT Theorem 1 concern a fixed everywhere-percolating edge subgraph A and the superposition Y=A union omega, where omega is independent Bernoulli percolation of one fixed positive density. BT Theorem 1(ii) states p_c(Y)<1 almost surely. BT then poses the general finite-energy threshold-one question separately as Question 1. The arXiv text explicitly emphasizes the special role of independent sprinkling. [BHS](https://arxiv.org/pdf/math/9906002v1), pp.1-2; [BT](https://arxiv.org/pdf/1505.06069v1), pp.1-3.

The candidate does not preserve every original tree edge: each has positive deletion probability. Its non-tree insertion probabilities depend on the hidden entire tree and do not share a demonstrated fixed positive density. Conditional independence of the output edges given T does not supply BT's fixed-base, fixed-density sprinkling representation. Thus the cited sprinkling theorem does not directly apply. No conclusion about the stronger uniform-energy question follows from this distinction alone.

## Dependency audit

| Dependency | Exact checked statement and use | Finding |
|---|---|---|
| Timar, arXiv 1805.10690v1, Theorem 1, pp.1-2 | An ergodic amenable unimodular random graph that is one-ended almost surely admits a factor-of-iid one-ended spanning tree. The factor is defined measurably and equivariantly with respect to isomorphisms. | Its stated hypotheses cover deterministic rooted nearest-neighbor Z^d, d>=2. This supplies a connected, fully invariant tree input. The author's separate iid-factor argument supplies translation mixing; the tree theorem is not being quoted as a theorem about the final perturbation. |
| Timar, Corollary 2, p.2 | A quasi-transitive unimodular graph is amenable and one-ended exactly when it admits an invariant one-ended spanning tree. | Supports existence and full invariance. Theorem 1 supplies the stronger factor information needed by the claimed mixing route. |
| Pemantle, math/0404043v1, Theorems 2.3 and 4.3, printed pp.5 and 20 / PDF pp.6 and 21 | The exhaustion limit exists; for 2<=d<=4 it is a one-ended tree. | Supports the separate low-dimensional input. Full automorphism invariance follows from uniform finite-tree laws and exhaustion independence: applying any lattice automorphism maps an exhaustion to another exhaustion with the same limiting law. Theorem 2.3 alone only calls its general-dimensional limit a forest. |
| Pemantle, high dimensions | The uniform spanning forest has infinitely many components for d>=5. | It cannot replace T in the displayed path-dependent kernel: cross-component endpoints would lack a finite tree path. The author explicitly avoids this invalid substitution. |
| BHS / BT | Source formulation, finite-energy convention, and contrast with independent sprinkling. | They are not imported as a theorem proving this candidate's full conclusion. |
| HM | A close site-percolation antecedent for the summable environment-dependent flip mechanism. | Appropriate acknowledgement; not a black-box bond-threshold-one theorem. |

Checked theorem numbering in this table is for the pinned arXiv versions, not silently for a different published layout. The [Timar arXiv record](https://arxiv.org/abs/1805.10690) confirms the 2019 ECP publication metadata; the [Pemantle arXiv record](https://arxiv.org/abs/math/0404043) confirms the 1991 journal publication. This audit checks the quoted statements and their hypothesis fit, not new proofs of the external established theorems. The main perturbation, measurability, posterior finite energy, all-vertex cut events, uniqueness, and quenched thinning argument remain the separate mathematical auditors' responsibility.

## What HM establishes, and what it does not establish here

HM was published in 2009; its arXiv deposit is from 2010. The freshly retrieved [journal EMIS PDF](https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/1446/1446-4872-1-PB.pdf) is 165,957 bytes, SHA-256 `ddbf7afb7874e41839426dc0158d473ae369ae593334f77021dbdef26f2c0c1d`. It is a different file from the pinned 166,246-byte arXiv PDF; both were kept distinct. Published Definition 1.1, p.43, distinguishes ordinary and uniform site finite energy. Proposition 2.1 and Section 2, pp.44-45, build an ordinary-energy site coexistence example from one-ended UST geometry and summable flips. Printed p.46 explains why the pre-flip X-hat graph has internal threshold one; it does not state that the post-flip finite-energy X-bar graph has threshold one.

Consequently, that paragraph alone cannot be cited as a complete prior solution of the historical bond question. Nor does it prove absence of an easy reduction or of another prior resolution. Turning a site law into the graph induced by open vertices does not automatically preserve finite energy of each bond coordinate. The candidate acknowledges the close mechanism and adds explicit bypass suppression in its bond construction. Assessing the novelty of that addition requires the deferred priority audit, after mathematical clearance. No new HM-based construction was attempted here.

## Access and version limits

My ordinary GET of the current Saint-Flour author URL returned 404, and my archive GET timed out. I inspected the parent's fresh successful public archive retrieval, verified its exact original pin, and recorded that dependence. BHS, BT, and HM arXiv GETs succeeded independently and match the original pins.

Ordinary publisher/DOI routes for BHS, BT, and Timar did not provide inspectable final PDFs in this audit: BHS DOI returned 403; BT Project Euclid returned HTML, its old Euclid route failed, the tried Numdam article path returned 404, and the imstat route returned HTML; Timar's Project Euclid route returned HTML. No access challenge was bypassed. Search-indexed primary publisher passages corroborated BT's final pp.998-999, but index snippets are not a rendered final-PDF inspection. Exact BT theorem/question/energy statements in this audit are therefore grounded in pinned arXiv v1. The existence of the DOI and journal metadata is distinguished from access to its full final contents. No final-version equality is asserted without comparison.

## Mandatory scope wording for promotion

There is no required correction to the frozen Section 1 mathematical claim on this audit's scope. Any later status or publication text must retain the following qualifications:

1. Say **ordinary nonuniform finite energy**, and spell out strict positivity given all other output bond states. Do not claim uniform finite energy or infer marginal failure of uniform energy merely from the hidden-tree rates.
2. Say that almost every realized X has an infinite component and that its independent Bernoulli bond threshold is one. Preserve **full automorphism invariance**, d>=2, and the **quenched** quantifiers. Do not replace the target with a site law, a rooted-a.s. property, or an everywhere-percolating condition.
3. Attribute the historical question to Saint-Flour item 8.15 with BHS Question 1.1 as its earlier explicit formulation. Give arXiv version/page locations where that is what was inspected; do not report a successful current author or BT final-PDF inspection.
4. Treat an affirmative answer to the checked historical question as conditional on mathematical clearance. This source audit supplies no present-day openness, novelty, first-resolution, or publication-acceptance conclusion. Old acceptance reports and dataset open labels do not resolve those separate questions.
5. Retain HM credit and distinguish its pre-flip threshold statement from the post-flip finite-energy law. Do not promote either a direct-HM-resolution claim or a no-prior-resolution claim from this limited antecedent check.

These are mandatory reporting boundaries; the author already states the main mathematical boundaries correctly. No author files were edited.

## Disposition

The exact-source gate clears for the historical ordinary-energy bond target, and the cited tree-existence inputs have the required stated scope. Mathematical acceptance remains delegated to the independent mathematical audits. Current priority and the historical record of any later solution remain open audit work, with no external outreach planned. Public outputs are listed by checksum in `PUBLIC_MANIFEST.json`; raw PDFs, raw data, extracted source text, renders, and replays are ignored and excluded.
