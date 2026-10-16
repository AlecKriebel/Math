# PR246 / 9700040 — independent RSK joint-law adversary

**Disposition: PASS for the assigned combinatorial-probability family. No mandatory mathematical correction found.** One optional bibliographic correction is listed below. This is conditional on the separate dynamics/uniqueness identification of the stationary configuration and does not certify source-level explicitness or historical priority.

Input: original native head `0b4db59eb5515f2d90d8b8df33b6b729b78b48f1`, as revalidated at 2026-10-15T03:35:47Z; open draft PR246 and `claimed_solved` are claims under audit. Original proof SHA256 `c6e7d751931637e0f119cf6ba8adf71462adb321825be5df39f3f67f2ea61dc0`. All 20 submitted files independently match the supplied native byte counts, SHA256 hashes, and Git blob SHA1 identifiers; see INPUT_VERIFICATION.json. No Git operations were used.

## Independence and evidence order

The read-only `INDEPENDENT_RECONSTRUCTION_20261015T0338Z.md` was created at **2026-10-15T03:39:06.027832Z**, before any file under the original `independent_review` directory was opened. Its SHA256 is `5ddd4a3e5b9461f92fda332822cbdc5660e170ca526bac529226a6c7e4045c12`; RECONSTRUCTION_SEAL.json records this ordering, and INPUT_VERIFICATION.json confirms the file remains unchanged. Original PROOF.md and primary sources were read first. The reconstruction derives the strip conditioning, permutation normalization, tableau-block count, determinant specialization, convergence, arbitrary query conventions, and low-index density independently of the inherited verdict.

The inherited review and receipts were read only after that freeze. New controls subsequently used direct label assignments, inverse RSK and permutation-matrix growth diagrams, rather than importing either checker or the author evaluator. The original modules are imported only in the explicitly labelled reproduction and 42-coefficient comparison stage.

## Strongest verified theorem

Let a unit-intensity Poisson process occupy the positive quadrant. Write L(x) for its longest strictly increasing northeast chain in `(0,x] × (0,1]`, and `Z_r=inf{x:L(x)≥r}`. For every finite `0=x_0<x_1<...<x_m` and every positive integer list `r_1,...,r_m`, with **no ordering condition on the indices**, the exact simultaneous survival probability is

`P(Z_(r_j)>x_j for all j) = exp(-x_m) Σ D_1(λ^m/∅) ∏ D_(x_j-x_(j-1))(λ^j/λ^(j-1))`,

where `∅=λ^0⊆λ^1⊆...⊆λ^m`, each `λ^j_1≤r_j-1`, and

`D_t(λ/μ)=det[h_(λ_i-μ_j-i+j)(t)]`, `h_k(t)=t^k/k!` for `k≥0` and zero for `k<0`.

The determinant is padded to any dimension at least both partition lengths and is assigned zero for failed containment. The infinite sum has nonnegative terms, is absolutely convergent, and has unrestricted terminal-size-n mass exactly `x_m^n/n!` before the exponential prefactor. Transposing all partitions preserves every D and permits fixed dimension `B=max(r_j-1)`, independent of terminal size. For `B=0`, only the empty chain contributes and the answer is `exp(-x_m)`.

Every arbitrary finite real-threshold query is covered after sorting positive thresholds with their attached indices, retaining the smallest index at repeated thresholds, and removing thresholds at most zero. If no positive threshold remains, the probability is 1. Inclusion–exclusion recovers every finite joint distribution. For rational thresholds the finite truncated raw sums are rational, with the Poisson exponential tail giving a computable deterministic error tending to zero. This theorem concerns simultaneous coordinates, and supplies no multi-time expression or particle-index Markov property.

Identifying `(Z_r)` with the unique invariant law of the exact drift–jump process is the outstanding dependency of this role. The parent audit assigned that theorem to a distinct family. Nothing in these counting arguments assumes it.

## Core adversarial checks of the proof

### Strip conditioning and the two factorial families

Disjoint spatial strips have independent Poisson counts `d_j` of means `Δ_j`. Conditional on these counts, sorting by u leaves independent uniform v marks. Their relative ranks form a uniform permutation of n letters, independently of the conditioned u data. Prefix cut `n_j=Σ_(i≤j)d_i` corresponds to the rectangle ending at `x_j`.

For a fixed nested chain of prefix shapes, the recording tableau's consecutive label blocks are counted by `∏ f^(λ^j/λ^(j-1))`. There is no multinomial label choice: each block has its forced consecutive set of labels. Conversely, nested initial shapes are order ideals, so any such block tableaux assemble into a valid recording tableau. The final insertion tableau is free, contributing `f^(λ^m)`; dividing by `n!` is the uniform-permutation probability. The independent Poisson count probability then adds `exp(-x_m)∏ Δ_j^(d_j)/d_j!`. Both the global `n!` and each separate `d_j!` are necessary, and both appear in the proposed determinant factors.

The independent exact controls check every actual three-prefix chain and every weak cut `0≤a≤b≤n≤7`, including empty middle or exterior blocks. Their 2,459 chain entries match both the tableau count and the determinant/Poisson factorial weight exactly.

### Exponential specialization, signs, padding, and transpose

The claimed specialization is correct with the stated parameter, rather than a square-root or Poisson parameter substituted accidentally. An independent reconstruction takes q equal variables `t/q`: distinct-label semistandard tableaux contribute `binomial(q,d)f^(λ/μ)(t/q)^d`, while repeated-label assignments vanish as `q→∞` for fixed skew shape. Thus the Schur limit is `t^d f^(λ/μ)/d!`. The complete-symmetric generating function tends coefficientwise from `(1-tz/q)^(-q)` to `exp(tz)`, so skew Jacobi–Trudi yields exactly the factorial determinant. Each determinant monomial has degree `|λ|-|μ|`, since the permutation offsets cancel.

Padding by one extra zero gives a final row with zeros to its left and final entry one; expansion returns the original determinant. Repeating proves arbitrary zero-padding invariance. Transpose sends each standard skew tableau to another standard skew tableau and preserves containment and size, so D is unchanged. Equal shapes have D=1, including at t=0; unequal contained shapes have D_0=0. The noncontainment convention is consistent with the skew determinant. New controls include all these cases, extra padding by one and three, positive rational parameters, zero, and a negative parameter as an algebraic stress test only.

### Arbitrary query orders and edge cases

The shape bound must follow the index attached to its sorted threshold. An increasing-index assumption would unnecessarily remove valid queries; none enters the proof. A later stricter row bound simply constrains all earlier subshapes. For example a middle index 1 forces the middle and earlier shapes empty; indices `(4,1,2)` then leave the exact column series involving only the last strip length. All 64 triples of indices in `{1,2,3,4}^3` were checked at every weak three-block cut through size seven. Repeated thresholds use the smallest index because it is the strongest survival event for ordered particles. Nonpositive thresholds are vacuous. An empty positive-threshold list is separately assigned probability one, avoiding an undefined `x_m`.

The mathematical preprocessing rule is distinct from the author command-line domain: stationary_law.py documents and enforces nonempty, strictly increasing, positive rational thresholds. It need not accept raw duplicate, negative, or unsorted queries to implement the documented canonical formula. This distinction is accurately acknowledged in the inherited review.

### Normalization, absolute convergence, and differentiating the low-index series

At fixed counts, summing the tableau product over all chains counts all `n!` permutations. Summing over count allocations gives `Σ_(Σd=n)∏Δ_j^(d_j)/d_j!=x_m^n/n!`. Constraints only remove nonnegative terms. This supplies normalization, absolute convergence, and the exponential-tail domination for all terminal sizes. There is no reliance on numerical convergence or an interchange of conditionally convergent sums. Fixed B constrains dimension, while the number of partitions still grows with cutoff; no efficiency theorem is claimed.

For indices `(1,2)` at `0<x<y`, the first shape is empty and the last is a column, giving `S(x,y)=exp(-y)F(y-x)`, where `F(z)=Σ z^n/(n!)²` is entire. All its derivatives converge uniformly on compact sets, justifying the two partial derivatives inside the open wedge. The mixed derivative is

`p_2(x,y)=exp(-y)Σ_(n≥0)(n+1)(y-x)^n/[n!(n+2)!]`.

Under `z=y-x`, the Jacobian is one and this factors as `exp(-x)a(z)`. Tonelli and the gamma integral give `∫a(z)dz=Σ(n+1)/(n+2)!=1` by telescoping, so the gap law is normalized and independent of `Z_1`. The argument proves independence of the first position and first gap; it makes no assertion of general independent gaps. The coefficient identity and integral telescoping were checked exactly through n=79. Analytic entire-function and normalization arguments cover all n. The expression agrees with the already published-in-the-notes equations (46)–(48) and is not a new low-index result.

## Original reproduction and complete receipt comparison

The unchanged source files were copied into two isolated subdirectories under this role's directory. `reproductions/author/verify_exact.py` was executed with its unchanged `stationary_law.py`; `reproductions/independent/independent_checks.py` was executed separately. Both exit codes were zero, and stderr was empty. Actual execution metadata, copied source hashes, stdout and stderr are preserved. Runtime was CPython 3.14.6; no packages were installed, and no scientific library was required.

The **entire parsed objects and receipt bytes** are equal to the original artifacts, not merely the assertion totals. REPRODUCTION_COMPARISON.json retains every parsed receipt, recursive differences (empty), exact raw coefficients, exact enclosure fractions, display-only floating values, input thresholds/indices, category maps, maximum sizes, status, and limitations. It also records that the original receipts have no explicit dependency field; INPUT_VERIFICATION.json audits the actual script imports instead of inventing a receipt field.

| Original checker | Counted exact assertions | Full parsed receipt | Byte equality |
|---|---:|---|---|
| Author | 49,618 | Equal | Equal |
| Original independent | 15,580 | Equal | Equal |

Author categories reproduce as: 1,347 skew determinant checks, 1,347 transposes, 449 padding, 8 RS normalizers, 46,233 time-sweep/prefix checks, 141 joint-prefix counts, 36 Poisson coefficients, 9 first-particle laws, 9 two-particle survival laws, 30 density coefficients, and three each for nested certificates, certificate width, and probability bounds. All three example enclosures, including the nonmonotone index example, match exactly.

The independent receipt reproduces all 13 categories: 690 determinant/cell-poset, 690 transpose/cell-poset, 167 padding, 8 tableau normalizers, 5,913 sweep/direct-LIS, 5,039 exact log-time geometry, 504 three-prefix arbitrary-index counts, 7 independent Poisson normalizers, 42 coefficient bounds, 1,944 rational enclosure cases, 27 exponential-tail checks, 540 tail-ratio checks, and 9 Jacobians. Its six coefficient arrays, all thresholds, and exact scope string match.

The separately asserted **42 coefficient comparisons** were actually reconstructed: six independent raw arrays at thresholds `1/3,5/6,3/2`, degrees 0 through 6, were compared with the unchanged author evaluator. Every rational coefficient agrees. The full five-field summary is equal to AUTHOR_COMPARISON.json, including evaluator hash and author receipt byte identity. All 42 pairwise values remain in REPRODUCTION_COMPARISON.json.

## New independent controls and limits

`controls/growth_inverse_rsk_controls.py` imports no author or inherited-review module. It passed **88,173 counted exact checks**, with full stdout, stderr and execution metadata preserved. It builds standard tableaux by direct enumeration of cell-label assignments, reverses RSK to recover every permutation through n=7, and independently reconstructs all prefix shapes with Fomin local rules on the permutation matrix. A quadratic direct LIS calculation checks every prefix first row. Fraction-free integer Bareiss elimination checks factorial determinants against the direct skew label counts. This is distinct from both the author row-insertion/corner recursion and the inherited cell-poset dynamic program/Leibniz determinant.

The exact category map is in `controls/growth_inverse_rsk_stdout.json`; central counts are 5,914 inverse-RSK pairs/permutations across sizes 0 through 7, 46,233 growth-first-row/LIS comparisons, 2,459 complete prefix-chain weights, 7,680 arbitrary-index constraints, and 5,244 raw/canonical query equivalences. The retained coefficient examples use strip lengths `2/7,3/5,5/6`, distinct from both original suites. No stochastic simulation or floating arithmetic enters these controls.

These are finite checks. They do not establish the unbounded-size theorem by themselves, and do not test all real thresholds or all unbounded indices. The frozen proof reconstruction supplies that argument. The gap remaining for this role is its external theorem dependency on the process identification, not an unproved central combinatorial claim. No route was declared successful by transferring that difficulty to another unsupported combinatorial conjecture.

## Primary-source verification and optional finding

Read directly from the original source URLs before inherited verdicts:

- [Aldous–Diaconis 1999](https://www.stat.berkeley.edu/~aldous/Papers/me86.pdf), section 2.1 and Proposition 4, printed 418–419: permutation RSK, tableau pairs, and first-row increasing-subsequence identification.
- [Okounkov–Reshetikhin, arXiv math/0107056v3](https://arxiv.org/pdf/math/0107056v3), dated 31 January 2003, section 2.2.4, equations (7)–(8): precisely the skew Jacobi–Trudi sign convention and containment condition used here.
- [Betea et al., published author-hosted PDF](https://www.math.umb.edu/~vuletic/Site/Research_files/PSASP.pdf), **Section 6**, printed 415, equation (6.6), with Poissonized RSK discussion on 415–416: correct skew exponential specialization and parameter convention.
- [Aldous–Diaconis 1993 notes](https://www.stat.berkeley.edu/~aldous/Research/OP/patience.pdf), printed 39, equations (46)–(48): matching known two-particle density and first-gap factorization.

All four exact PDF byte hashes match the submitted source pins. Three were directly downloaded within this role. The Schur sampling PDF was directly opened/read with the web reader first; its separate local download failed because of host DNS, so the exact primary bytes independently retrieved by the parent were rehashed and inspected locally. This resolved the byte-verification limitation; the earlier failure is transparently preserved. PRIMARY_SOURCE_PINS.json records URLs, sizes, hashes, actual access provenance, and pin matches. Full source PDFs and extracted reading pages are excluded from the public authored-file manifest.

**Optional finding RSK-O1 (citation locator only):** SOURCES.md item 4 and the inherited review call this “Section6.3.” The published PDF has **Section 6**, and its `(6.3)` is an equation about parameter summability; the desired specialization is `(6.6)` on printed 415, which the packet otherwise locates correctly. Change the section locator to “Section 6, equation (6.6), printed page 415.” This does not affect correctness or source availability. The frozen reconstruction preserved the original section locator in its source-reading note; this report supplies the correction without changing the immutable checkpoint.

## Mandatory findings, residual scope, and publication boundary

There are **no mandatory findings in this assigned family**. The strongest verified conclusion is the conditional all-query simultaneous Poisson-RSK law stated above, together with positivity, normalization, absolute convergence, fixed determinant dimension, and the justified low-index density/gap result. Its exact application to the invariant drift–jump distribution depends on the distinct dynamics/uniqueness audit. The precise rational enclosure is also reviewed by the separately assigned certificate family; this role verified its tail domination and reproduced all supplied certificate checks.

Historical priority and the adequacy of the source's descriptive request remain separate questions. No historical novelty conclusion follows from proof brevity, classical ingredients, the open-page listing, or the inherited pass. No source, QUEUE, PR, paper, tracker, publication artifact, Git index, branch, ref, or checkout was changed. No outside individual was contacted. The parent was sent progress and results within this audit's authorized agent coordination only. This role's assigned work is complete; completion estimate **100% for this family**, not for the larger PR audit.
