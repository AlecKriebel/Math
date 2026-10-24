# Independent computational and adversarial certificate review

Review date: 2026-10-24. Target: *Free spanning-forest degree can decrease under squaring*, version 1.0.0, dated 2026-10-22; supplied paper DOI identity 10.5281/zenodo.23575190. This review binds the local published-release files and does not independently authenticate DOI resolution.

**Verdict: PASS for the deposited finite certificate and its finite-support-to-free-exhaustion transfer.** No mathematical gap was found in those claims. The strict numerical separation follows once the paper's separately reviewed exact value for G is supplied. No claim of an exact value for the square, optimal currents, firstness, proof-assistant certification, or independent human refereeing is certified here.

## Scope and independence

The deposited source and verifiers were inspected before executing copies. The independent reconstruction uses tuple words for the rooted tree, an all-zero end, and a test of every unordered vertex pair for a common neighbor. It imports no deposited graph or verification routines. Divergence is calculated from per-vertex lists of signed contributions. This is an independent implementation with a materially different graph representation, not a blind audit: the deposited verifier was first read for execution safety. No earlier inventory assessments or earlier independent review implementations were read.

Only files within `reviews/certificate/` were written. Published files were not edited. No Git operations, external contact, or original floating-point witness generator was used. A separate adversarial subagent tested the entire real certificate and the deposited checker.

## Exact computational evidence

`independent_words.py` with Python isolation and without site packages reconstructs the radius-ten ball and validates:

- 3,070 vertices and all 19,931 unordered edges of J = G[W]^2, including exact ordering.
- Every root neighbor of the infinite simple square H = G^2, not a chosen subset.
- Every one of 797,240 exact integer current numerators, 122,800 divergence equations, 40 energy numerators, and the total sum of squares.
- A current has divergence +10^9 at its stated target, -10^9 at the root, and zero at every other vertex. Its unit normalization is 10^9.
- The total energy is exactly 3208526010913748780/10^18 = 3.20852601091374878.
- The difference 321/100 minus this total is exactly 73699454312561/50000000000000000 > 0. No floating-point comparison is used.
- Each of the 3,070 vertices has degree 8 in the infinite G and degree 40 in the infinite H, computed using unrestricted neighbors.
- All 15 scientific members recorded in the supplied source manifest match both byte sizes and SHA-256 digests.

The certificate identity is SHA-256 `6573c55f2998f4576a050a0757ca74f1cae9cadfa96ec61c69b181c530f79c4f`, with 165,241 compressed bytes and 4,460,799 decoded JSON bytes.

The full root-neighbor index list is `1..22, 24, 25, 30..45`. Its disjoint geometric classes are:

| Class | Indices | Count |
|---|---|---:|
| Four ancestors | 1, 4, 10, 22 | 4 |
| Descendants at depth one | 2, 3 | 2 |
| Descendants at depth two | 6, 7, 8, 9 | 4 |
| Descendants at depth three | 14..21 | 8 |
| Descendants at depth four | 30..45 | 16 |
| Sibling | 5 | 1 |
| Uncle | 11 | 1 |
| Sibling's children | 12, 13 | 2 |
| Uncle's children | 24, 25 | 2 |

The four ancestors and thirty descendants do not overlap the six side-branch vertices. This independently reproduces the paper's count of forty.

## Boundary attack

The calculation builds infinite G-neighbor sets first, then restricts endpoints to W, and constructs J by testing every unordered pair for adjacency or a common neighbor inside W. Separately it builds H[W] using intermediate vertices outside W as well. Every J edge is an actual H edge; in this particular ball the independently enumerated H[W] and J are equal. The proof needs only J ⊆ H, so this additional equality is not an assumed premise.

Small-radius tests expose the expected incompleteness: radii 0, 1, 2, 3 give square root degrees 0, 3, 9, 21, respectively. Radius 4 is the first tested ball containing all forty root neighbors; radius 5 also contains them. Thus a too-small certificate would not silently certify the full sum. Radius 10 comfortably contains all root-edge witnesses.

## Why the bound is free, not wired

Let a verified row define a flow θ on J by dividing its numerators by 10^9. The exact incidence equations make θ a unit flow between its target v and the root o. For any sufficiently large connected induced graph H_n in a free exhaustion of H, every vertex and edge of J lies in H_n. Extend θ by zero to all other edges of H_n. At a vertex in W its divergence is unchanged; at every new vertex it is zero. Its energy is unchanged. Finite Thomson gives

R_{H_n}(o,v) ≤ E(θ).

Taking the decreasing free resistance limit gives R_H^F(o,v) ≤ E(θ). The finite Kirchhoff identity, passed through the free weak limit, gives P(ov belongs to FUSF(H)) = R_H^F(o,v) because each edge has unit conductance. Summing these forty inequalities gives the claimed expected-degree upper bound. This involves a finite sum and finitely supported flows, so no interchange involving an infinite edge sum is hidden.

The distinction is substantive. On the 3-regular tree, finite free resistance across an edge is 1. An arbitrary square-summable infinite unit flow can instead put 2/3 on that edge and send 1/3 to infinity on each terminal side in opposite directions, splitting equally at every branch. Each side contributes (1/3)^2 Σ_{k≥1}2^-k = 1/9; total energy is 4/9 + 1/9 + 1/9 = 2/3. Such an infinite escape flow would not prove a free upper bound below 1. The deposited rows have finite support and zero divergence at every boundary vertex other than their designated terminal, preventing precisely that failure.

## Equation and metadata consistency

The theorem, abstract, certificate specification, README, frozen result JSON, and Zenodo preparation metadata agree on degrees 8 and 40, the exact G value (24−√2)/7, the square upper bound, denominator, vertex/edge counts, and b_F = expected degree/2 − 1. The square result is consistently an upper bound, not an equality. The metadata describes the package as an unrefereed preprint with extensive AI involvement and explicitly excludes priority guarantees and a claim about the unimodular subclass.

The unchanged seven-page `paper.pdf` was text-extracted with Poppler and every page was rendered at 95 dpi and visually inspected. The displayed abstract and Theorem 1, recurrences (5), (6), (10), (11), resistance formulas (7)–(9), certificate identities (12)–(13), Lemma 2, and final 1/200 comparison agree with the editable source and verified constants. No clipped or overlapping formula, missing mathematical glyph, or incorrect exponent was observed. The source/metadata description of a seven-page preprint is accurate. Extracted text, PDF metadata, and all page renders are retained under `pdf_inspection/`; text extraction alone is not claimed to preserve equation layout.

`check_algebra.py` independently verifies the displayed fixed-point and resistance algebra in the exact field Q(√2), including 3R_tree + 5R_grandparent = (24−√2)/7. These algebra checks are not a replacement for proving the all-depth recurrences or convergence; those belong to the parallel analytic review.

The decisive comparison is exact: (73/50)^2 > 2 implies (24−√2)/7 > 161/50, while the certificate total is <321/100. Therefore the paper's b_F gap is strictly >1/200. The certificate actually gives a stronger lower bound near 0.00900745437 when combined with the exact G value. This decimal is explanatory only; the verification uses integer/rational arithmetic.

The reviewed preparation metadata still uses phrases such as “proposed deposit” and provenance states that preparation did not allocate a DOI. Those are historical preparation-status statements, not a contradiction of the scientific equations. A current website should use actual published-record status and preserve the original dated artifact rather than quietly rewrite it.

## Deposited replay

`replay_deposited.py` copies the inspected scripts and inert certificate into this review folder. It runs both `verify_currents.py` and `check_reductions.py`, normally and with `-O`, using `-I -S -B`. All four runs exit successfully without stderr, and their stdout is byte-for-byte identical to CURRENT_RESULTS.json or REDUCTION_RESULTS.json. The checks survive Python optimization because they do not rely on removable assertions.

The finite branch/global-elimination diagnostic outputs are thereby reproduced. This is replay evidence, not a new proof of every-depth recurrence or infinite-limit identity.

## Adversarial parser testing

The separate hostile-parser report, runnable tests, and full case-by-case results are retained under `hostile_parser/`. All **161/161 expected outcomes** passed: 145 rejections and 16 genuine/permissive acceptances. No tested input falsely certified corrupted mathematics.

All twenty altered-file subprocess cases were rejected by the compressed-file SHA-256 check before parsing. Direct checks, intentionally bypassing that identity gate, rejected substantive changes to currents, source rows, edge sets/order/orientations, targets, energies, and denominators. A changed current with honestly recomputed energies still failed divergence. A divergence-preserving circulation around a real triangle with recomputed energies failed the certificate-specific fixed total. Genuine normal and optimized executions passed.

The audit found bounded schema/API leniencies: the direct parser keeps the final duplicate JSON key, `vertices=3070.0` passes numerical equality, unused metadata is ignored, and the internal helper can accept invalid denominator arguments when invoked outside its normal caller. The genuine JSON contains no duplicate keys or nonstandard numeric constants; the supported whole-certificate checker fixes a positive exact integer denominator and validates the mathematical data. All modified-file versions fail the pin. These are reasons to avoid claiming universal strict-JSON validation or a generic public flow API, not blockers for this deposited certificate.

## Reproduction

From this folder, using Python 3.10 or later and the standard library:

```
python3 -I -S -B independent_words.py
python3 -I -S -B replay_deposited.py
python3 -I -S -B check_algebra.py
```

The first command prints fresh timestamped independent results and checks the exact original source manifest; the second creates or refreshes private replay copies and compares outputs to the frozen results; the third checks algebra exactly. No dependency installation or network access is required.

## Remaining limits

The verified result is a finite feasible-flow certificate plus a written transfer to the infinite free forest under standard finite Thomson, Kirchhoff, and free-limit facts. It does not compute the exact resistance or expected degree of H, establish current optimality, prove firstness, independently verify every cited external source, authenticate DOI availability, or supply human peer review. The all-depth derivation of the exact G value is subject to the separate analytic audit. No unresolved gap in the certificate or transfer was identified.

Final checkpoint: 2026-10-24T22:53:00.276769+00:00. Completion estimate: **100% of assigned review scope**. This estimate does not measure confidence in the broader research theorem. **PASS**, with the limits above.
