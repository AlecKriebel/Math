# Independent audit of Function Theory Problem 1.39

**Target:** 2301039 / AMR-022-1039, queue rank 564.  
**Review date:** 4 October 2026 UTC.  
**Reviewer:** a separate AI review worker, uninvolved in preparing the frozen author packet. This is not human peer review or formal proof-assistant verification.

## Verdict

**PASS for the corrected scoped packet only.** The unchanged author packet must be accompanied by [REVIEWER_CORRECTION.md](REVIEWER_CORRECTION.md) and this audit. One displayed inequality in Proposition 4 is false when denominator zeros cancel at the origin. The author already mentions the missing bounded correction in the following prose, and the separate correction now supplies its exact value and a full proof. All theorem conclusions survive.

**Original problem disposition: unsolved, 5/5.** Neither sharp constant has been determined; there is no positive-index admissible example, no improved unrestricted bound, and no full resolution. Do not use a different queue status to describe the scoped results. The five-route budget is exhausted as an investigation budget, but the queue status remains `unsolved` and the turns cell remains `5/5`.

The frozen packet alone, if presented without the correction, does not receive an unqualified PASS. Publication of a corrected bundle is a parent decision; no file was published and no repository or queue state was changed by this review.

## 1. Frozen identity and reproducibility

Author directory: `../public/`. Its `SHA256SUMS` has SHA-256

    27fa158bea7288368c1e1b5b275f72b4e78ca7166bfda923c9ab90e77da41eae

This is exactly the value specified in the review assignment. All 11 files listed in it passed SHA-256 verification. `AUTHOR_MANIFEST.sha256` is a byte-identical copy of that manifest for the audit record. In particular:

- `PROOF.md`: `3f4b852db08bf2f361cec2c4139cefc2c6ea954567566a98a186c3761839e236`
- `MODULAR_OBSTRUCTION.md`: `96318992fa9e8dbdbfa3283f1a527f1c5ab8bfb6588cf5ad9b5e526575041b43`
- `STATUS.json`: `a2905b92e57660827ed9845e0fe6ac531ff98a60f4fc3f8dac3f9344780c9d43`

I read the complete proof, modular note, source gate, research log, status, README, scripts, and stored outputs. I independently reran both scripts with Python 3.12.14 and SymPy 1.14.0, redirecting output only to this audit directory. Both outputs match the frozen outputs byte-for-byte:

- `VERIFICATION.replay.json`: 119 labeled exact controls; SHA-256 `27f7a2be3f3fde028888554e7ecd0940663cdc8ee55b93d38133b668baf91274`.
- `MODULAR_VERIFICATION.replay.txt`: 12 labeled exact controls; SHA-256 `dcd92ce724c90cb6d0983f0c2cc5914ea39c4d6009aa42eef0b4c0c87995cefe`.

Thus all 131 advertised controls reproduce. They check finite identities and inequalities, not Jensen's theorem, infinite products, asymptotic uniformity, contraction mapping, or Rouché's theorem. Those arguments were separately reviewed below.

The independent correction verifier checks 324 exact monomial cases, including complete and incomplete origin cancellation. It also records the counterexample to the original display. This is a regression control for the correction, not a new research approach or a universal proof by sampling.

## 2. Exact problem and historical scope

I retrieved [Hayman and Lingham, arXiv:1809.07200v2](https://arxiv.org/pdf/1809.07200v2#page=20) and checked its equation (1.8), Problem 1.39, and the adjacent update on printed page 19, including visual inspection of the reading copy's page image. The packet correctly retains the finite-alpha hypothesis, the analytic versus meromorphic distinction, and both sharpness questions. The reported constants are 2 and 7, attributed there to Shea and Sons. The 2018 update is only a historical reporting statement.

The [Houston Journal of Mathematics issue index](https://www.math.uh.edu/~hjm/vol12-2.html) confirms the authors, issue, and pages 249–266. This review's attempt to open the [linked original article](https://www.math.uh.edu/~hjm/restricted/archive/v012n2/0249SHEA.pdf) was unsuccessful. I did not inspect or verify that proof. The author's earlier claim of HTTP 403 is its retrieval record; this review's web tool reported a retrieval error rather than an independently exposed HTTP status.

The local Hayman–Lingham PDF hashes to `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`, agreeing with `SOURCE_MANIFEST.json`. The Nadi reading copy hashes to `bf876597cd579948591b63b57373f69411426bb494e8e5c0e28993b1a81fd72e`, also agreeing. Reading copies and full extracts are not included in this audit deliverable.

## 3. Main proof review

### Proposition 1: reciprocal and divisor reduction

**Pass.** A zero-free meromorphic f has a holomorphic reciprocal u, with pole orders of f becoming zero orders of u. Conversely a nonzero holomorphic u gives a zero-free meromorphic reciprocal. The standard exclusion of the identically-infinite object from meromorphic functions is understood.

Away from zeros of u, the identity f′−1=−(u′+u²)/u² is correct. At a zero of u of order m, the term u′ has leading order m−1 and u² has order 2m; cancellation is impossible. Thus the required zero divisor is exactly the divisor stated. The explicit requirement that u′+u² not be identically zero also correctly excludes derivative-identically-one examples.

Jensen's formula with the stipulated origin term gives the exact characteristic identity T(r,1/u)=T(r,u)−log|c|, including k>0 at zero. Integrable logarithmic singularities on exceptional circles do not invalidate the identity. Therefore alpha is preserved. The controls f=2/(m z^m) are genuinely admissible and show why demanding a globally zero-free Riccati expression would incorrectly remove multiple poles.

### Proposition 2: the quotient F/F′

**Pass.** Exponentiating a primitive of u is globally valid on the disk and produces zero-free F. The identities F′=uF and F″=(u′+u²)F prove the forward divisor assertion. Conversely the nonzero numerator prevents cancellation at zeros of F′, and f′=1−FF″/(F′)² proves omission at every ordinary point. The order drop m to m−1 in differentiating F′ is exact. In the analytic case, all three functions F,F′,F″ must be zero-free.

The packet correctly targets the characteristic of F′/F. No implication from growth of F alone to the required logarithmic characteristic is established or claimed.

### Proposition 3: the omitted-primitive parametrization

**Pass.** Simple poles of q with negative integer residues have exponential monodromy one. Residue sums over a closed path involve only finitely many enclosed poles, even when poles accumulate toward the unit circle. The resulting H has precisely the prescribed poles and no zeros; 1/H is holomorphic and has a single-valued primitive J.

At a pole of H of order m, J−J(p) has exact order m+1. Therefore the exceptional choice C+J(p)=0 produces a simple zero of f, rather than a harmless pole cancellation. This validates omission of −C on the entire image J(D), including images of poles. Conversely q=(f′−1)/f has the stated residues and no other zeros or poles, and f/H extends nonvanishingly through every pole. The converse differentiation is valid there by holomorphic continuation.

Existence of an omitted value for an arbitrary chosen J is not automatic. The theorem states a conditional parametrization and the packet explicitly retains that unsolved construction requirement.

### Proposition 4: bounded characteristic

**Pass only with the separate correction.** The displayed estimate on lines 96–97 is false as written. For g=z and h=2z, its proposed right-hand side is log r, while T(r,g/h)=0, for every 1/2<r<1.

If k is the zero order of h at zero and p is the pole order of g/h there, the missing term is (k−p)log(1/r). With that term, the counting comparison and Jensen equality are exact. The term is bounded for r≥1/2 and tends to zero. The corrected proof establishes T=O(1), so all bounded-quotient and rational conclusions are unchanged. The separate artifact gives the complete proof and is required in the PASS bundle.

### Theorem 5: polynomial-exponential Cayley family

**Pass.** For degree d≥2, the scaled Cayley asymptotic is uniform on each fixed bounded y interval. The limiting argument sweeps an interval of length dπ, so its real part is strictly positive on some finite subinterval. Integrating over the corresponding arc of length proportional to 1−r yields a lower bound proportional to (1−r)^(1−d), which dominates logarithmic growth. No global positivity assumption is being made.

For affine P, the mean Poisson kernel is one and the conjugate kernel is odd. Its absolute integral has the stated factor 2/π, giving alpha=|Im a|/π. The bounded-error estimate is uniform in r and correctly covers arbitrary real parts and the constant case.

When Im a≠0, choosing the sign of n as in the proof puts the approximate logarithmic roots a linear distance into the right half-plane. The radius K log|n| is smaller than that distance. The same analytic logarithm on Re(w+1)>1 works for all disks; the map is a self-map with derivative tending uniformly to zero. Banach's theorem applies. Although successive disks can overlap, distinctness follows from the common logarithmic equation and differing integers n, exactly as the author argues. The positive real-a control satisfies |f′|>1 and alpha=0. The finite-alpha target hypothesis is essential to excluding the degree≥2 branch and is present.

## 4. Modular obstruction review

**Pass with the stated imported classical identities.** I independently checked the [DLMF nome convention](https://dlmf.nist.gov/23.15), [series and product in 23.17.4 and 23.17.7](https://dlmf.nist.gov/23.17), and [the parity transformation table in 23.18.1–3](https://dlmf.nist.gov/23.18). They match the formulas used. In particular the third matrix sends lambda to 1/lambda, and the nome is exp(πiτ), not exp(2πiτ).

The product has no vanishing factors for 0<|q|<1 and its deviations are locally summable. It proves holomorphy and nonvanishing. The inversion identity then proves omission of 1. No surjectivity result is hidden in this step.

For h itself, the disk derivative chain factor is (τ+i)²/(2i). Its leading coefficient becomes 8π, with the positive sign used in the note. The chosen w_n gives exactly the prescribed complex phase. On every fixed compact set in the local variable, Im τ tends to infinity uniformly, the q-error is O(n^−2), and the quadratic factor tends uniformly to one. Rouché applies on the stated circle because the limiting exponential minus one has exactly one simple zero there. The half-plane disks are disjoint and Cayley is injective, proving infinitely many distinct derivative preimages.

For rational R with a zero at a puncture, its local order m is positive. In all three cusp coordinates the composite P has a zero of exactly that order at zero. Other rational poles do not interfere once the half-plane height is sufficiently large. The full Möbius denominator, its nonzero leading coefficient, K, and beta are correct. The expansion of the derivative is locally uniform with error O((log n)/n+n^(−2/m)). Integer m ensures translation periodicity in the exponential. The chosen radius 1/(2m) isolates a single limiting root and makes the distinctness argument valid.

Under disk-automorphism precomposition, the correct inverse coordinate is used. A conformal Möbius map from the half-plane onto the disk cannot be affine; its reciprocal derivative therefore retains a genuinely quadratic leading term. This supplies a new coordinate calculation, rather than assuming derivative omission is invariant.

For the separate h/h′ candidate, symmetry gives h(0)=1/2 and h″(0)=0. The product derivative bound is valid: discarded terms are positive, the negative terms are bounded in the unfavorable direction, and the remaining positive-coefficient series is increasing. The exact rational lower bound 32129/65025 is positive. Thus h′(0)≠0 and the quotient derivative is exactly one at the center. The argument is properly limited to this normalization.

The proved rational family is precisely the algebraically specified family in the note. The stronger claim about every zero-free rational composition is expressly conditional on surjectivity and is not included in this PASS verdict.

## 5. Other sources and provenance limits

I inspected the relevant statements of [Nadi, arXiv:2609.05835v1](https://arxiv.org/pdf/2609.05835v1). Its finite-alpha corollary still contains a derivative-zero Valiron deficiency; omission of the value 1 does not set that term to zero. Its Theorem 2.5 does quote the modular characteristic asymptotic appearing in the packet. That quotation is accurately identified as context only. I have not verified Tsuji's original proof or independently audited the whole Nadi paper; neither is needed for the reviewed elementary or modular-obstruction conclusions.

The [Gunsul publisher text](https://onlinelibrary.wiley.com/doi/10.1155/2011/537478) confirms the additional small-logarithmic-derivative requirement defining the narrower class, and Theorem 5.2 is stated for that class. This substantiates the packet's warning against silently applying it to all target functions. It is not an imported unconditional theorem here.

The repository-history searches in `SOURCE_GATE.md` remain an author-reported provenance ledger. I did not rerun all remote PR, branch, commit, code, or tree searches. The local queue-change proposal and frozen status are consistent with `unsolved`, `5/5`, and status/turn-only edits, but this review does not certify a current remote queue row. Neither bounded historical searches nor this audit establish exhaustive novelty, priority, or current openness in the mathematical literature.

## 6. Remaining mathematical gaps and release conditions

The missing result is substantive: determine either supremum, produce an admissible positive-index example of the relevant size, or establish a better universal bound. None of the equivalent parametrizations supplies this, and exclusion of the tested families does not imply that every admissible function has index zero. The author's five approach records keep these gaps visible.

The corrected scoped packet may be described as reviewed reductions and construction-family obstructions. It must not be described as a solution, a new verification of the original historical bounds, a novelty certification, or a formally verified proof. The subjective 12% planning estimate is not a mathematical measure.

Conditions of this PASS:

1. Preserve the frozen author bytes and their original manifest.
2. Include `REVIEWER_CORRECTION.md` prominently with the proof and this audit, bound by the audit manifest.
3. Preserve the source limitations, conditional surjectivity boundary, and finite-alpha hypothesis.
4. Preserve the queue disposition `unsolved`, `5/5` and the distinction between 131 finite controls and analytic proof review.

No further defect requiring a change to the stated mathematical conclusions was found. The audit manifest binds the correction, full review, source-manifest copy, rerun outputs, and correction regression control.
