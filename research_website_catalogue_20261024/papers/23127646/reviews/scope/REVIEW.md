# Acquisition and scope review — Zenodo 23127646

**Disposition: PASS_SCOPE_ONLY. Mathematical clearance remains pending.**

Title: *Non-symmetry of biconstrained two-step reachability*. Author: Alec Kriebel, ORCID 0009-0001-9320-500X. Zenodo version 1.0, published 3 October 2026; the four-page manuscript prints the same date. Inventory row 49.

This review checks source identity, complete content scope, original definitions, attribution and candidate website wording. It is not a substitute for the separately assigned analytic and adversarial proof reviews. No website or promotion artifact was created, and no mathematical verifier was executed.

## Source custody and reading coverage

The fresh public record has exactly two published assets. Both were downloaded from their Zenodo API content URLs and matched the record's MD5 and byte counts. SHA256 bindings:

- `biconstrained_asymmetry.pdf`: 67,359 bytes; `35ddcd2a64bf0906fadcf762b913dfd9369941784ca0da87d97a3e9080ea80e4`.
- `biconstrained-asymmetry-verification.zip`: 198,015 bytes; `5415f48f702ab2e234376b73c4853043b1b7601316392ff4750123eb66339d81`.

The main PDF matches the queue-bound original. All four pages and the entire corresponding source TeX were read, including the proof, limitations, references and AI/review disclosure. The ZIP was safely extracted with member CRC verification and per-member hashes. All 86 files declared by its outer manifest match their stated byte counts and SHA256; the actual file set is exactly those 86 plus `MANIFEST.json`. No symlinks or additional reader PDFs occur. See `sources/receipt.json`, `sources/extraction-integrity.json` and this review's `package-integrity.json`.

The mathematical source includes the elementary proof, an exact replay harness, graph/set controls and rational linear-programming/support controls. The complete harness and the two `controls/*.py` files were inspected. The harness references six earlier checkers and expected outputs; these are historical assertions, not newly reproduced results. This assignment executed only acquisition, extraction, byte/manifest checks and document rendering. It did not execute the harness or any mathematical checker.

## Exact mathematical model

The graph is finite and simple. Its vertex set is partitioned into nonempty stable sets A, B and C; no A–C edges are present. For x,y in (0,1], every a in A has at least x|B| neighbors in B, every b in B at least x|A| neighbors in A and y|C| neighbors in C, and every c in C at least y|B| neighbors in B. All four inequalities are part of the model.

For each admissible graph, take the maximum over c in C of the fraction of A reachable through B. Each reached vertex counts once, irrespective of path multiplicity. The function ψ(x,y) is the infimum of that maximum over all finite admissible graphs and partitions. This is a universal guarantee, not an average, a fixed graph's value or the maximum number of paths. The infimum is defined without assuming an extremizing graph exists.

Theorem 1 claims

`|ψ(13/27,14/27) − ψ(14/27,13/27)| ≥ 1/108`.

The result does not specify which of the two values is greater.

Theorem 2 claims that, for every rational θ in (0,1),

`ψ(1−θ,θ) = 1−θ/d(θ)`,

with attainment by an ordinary finite graph. The invariant d(θ) minimizes the unweighted maximum row degree over finite binary matrices M with nonempty row and column sets, distinct columns, and strictly positive rational probability vectors b,q satisfying `Mq=θ1` and `Mᵀb=θ1`. Rows may repeat; the matrix may be rectangular. This invariant is not the earlier paper's minimum order of a square nonsingular regular weighted bipartite graph.

The rational and strict-positivity restrictions are material to the stated construction: rational weights permit exact finite blowups, and positive middle weights preserve the combinatorial paths and imply incomparable distinct column supports. θ=0, θ=1 and irrational θ are outside Theorem 2's stated domain.

## Proof structure and exact contribution boundary

The submitted lower-bound argument treats a graph whose maximum reachability F is below one. A missed pair forces complementary middle neighborhoods and exact boundary degree equalities. Grouping C by distinct middle neighborhoods gives a regular template. The nonempty disjoint missed A-classes and the B-to-A constraint bound their smallest mass t by `t Δ(M) ≤ θ`, hence the claimed universal lower bound. Additional A vertices are retained.

For the upper direction, a minimizing template supplies A-types of mass θ/d and a possible residual type. The residual has nonnegative mass; when its mass vanishes it is omitted. The proof checks all four weighted degrees and uses incomparable supports to make each C-type miss exactly one A-type. Rational blowup supplies finite graphs. This is the argument the independent mathematical gates must assess; integrity checks and finite controls cannot establish its universal quantifiers.

The inherited seven-type template and its complement have regularities 13/27 and 14/27. The manuscript uses them only to place d(13/27) and d(14/27) in {1,2,3,4}. The formula then forces an absolute gap through integer arithmetic. The explicitly described graphs have part sizes (108,27,27) and yield upper bounds 95/108 and 47/54 in the respective orientations. Two unequal upper bounds alone would not imply that the universal infima differ. Candidate wording preserves this distinction.

No exact minimum d, exact ψ-value, ordering of the pair, full off-boundary classification or stronger sharp numerical gap is asserted. The result is not a resolution of the separate Caccetta–Häggkvist or second-neighborhood conjectures discussed in the predecessor's introduction.

## Fresh primary-source interfaces and attribution

Fresh primary PDFs and hashes are recorded in `primary-references.json`; retained raw files are under the ignored `cache/primary-sources/` directory.

Seymour's contribution in *Oberwolfach Reports* 1/2019, printed pp. 46–47, explicitly asks the biconstrained symmetry question on p. 47. Its four directional degree conditions match this manuscript. Source: https://ems.press/content/serial-article-files/46780, DOI 10.4171/OWR/2019/1.

The published Chudnovsky–Hompe–Scott–Seymour–Spirkl paper, *Electronic Journal of Combinatorics* 29(2) (2022), #P2.47, was checked at the relevant passages, not read in full. Its pp. 4–6 define the same finite model; §2 provides the weighted framework. Theorem 2.3 establishes symmetry for φ, with the following paragraph leaving the ψ analogue unresolved. Figure 1 on p. 6 was rendered and visually inspected; its top two rows give the manuscript's seven-type template and displayed weights. The p. 71 discussion explicitly calls that template 13/27-regular. Theorem 12.2 on p. 72 concerns the equivalence of minimal-value statements ψ(x,y)=x and ψ(y,x)=x, not general symmetry. Source: https://www.combinatorics.org/ojs/index.php/eljc/article/download/v29i2p47/pdf/, DOI 10.37236/8451.

The same authors' arXiv v3 PDF was acquired and hashed as another primary edition, but substantive attribution checks used the published edition. The cited 2019 Hompe senior thesis was not acquired here. This bounded source check establishes the named question and inherited objects; it does not certify worldwide priority, absence of a later result or current openness. The manuscript's proof is presented as elementary; it does not import an optimization theorem as a substitute for its universal boundary argument.

## Independence and incidental exposure

No current sibling report or dedicated historical verdict body was read. The archive's dedicated priority reports, `audits/` opinions and `reference/review/ADVERSARIAL_REVIEW.md` were retained and hashed without reading their conclusions.

Necessary source material was not opinion-free: `reference/SOURCE_SCOPE.md` contains historical priority/eligibility remarks; the manuscript describes earlier AI audits; checker comments and the replay harness contain historical success labels and expected counts. These incidental claims were encountered while locating definitions, credits and support structure. They were not accepted as mathematical or priority evidence. The scope review does not claim strict blindness to all historical status language.

## Candidate content and remaining gate

`abstract-source.tex` preserves the entire abstract from the published source. `abstract.txt` is its full readable transcription; `candidate-content.json` preserves all 109 whitespace-delimited words, mathematical formulas, dates, DOI and both download assets. It contains a plain-language explanation, exact-scope summary and explicit predecessor credit for possible later use after clearance. No extensive verification replay is proposed for the public page.

Status wording should remain an unrefereed, extensively AI-assisted preprint. Neither external human peer review nor formal proof-assistant verification is claimed. No follow-up is proposed: merely listing the unevaluated minima or ordering would not establish a worthwhile new project with confirmed significance and unresolved status.

**Strongest completed result:** complete fresh source custody, exact asset/abstract inventory, and a source-grounded scope/attribution map suitable for the independent proof reviewers and later editorial preparation.

**Exact remaining gap:** the universal proof and its finite controls still require separate analytic and adversarial validation. PASS_SCOPE_ONLY authorizes no theorem promotion. No mathematical defect is asserted or ruled out by this scope disposition.
