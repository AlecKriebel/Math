# Independent adversarial review — Zenodo 23445342

**Disposition: PASS within the precise published hypotheses.** No substantive mathematical defect was found. This is an independent AI adversarial review, not conventional human peer review, a journal-acceptance recommendation, or a novelty/priority certificate.

Review completed on 2026-10-25 UTC. The immutable target is *Coarse endpoint concentration at every diverging scale for one-dimensional space-time random walks*, v1.0, manuscript dated 18 October 2026, eleven pages. The strongest verified claim is Theorem 1 with its full environmental tail quantifiers. There is no identified remaining proof gap in that claim. Historical originality and earlier anticipation remain unresolved.

## Exact source binding and reading scope

- Published PDF: `coarse_endpoint_concentration.pdf`, SHA256 `7514e0e456811651fdfb4f2f890f3fe81646d0346789057b561e075ad553bbe6`.
- Published supporting archive: `coarse_endpoint_verification.zip`, SHA256 `3a4ab05e434138db12d90dbfd1efebae0f101de36a5d674cc56ed04c8595236d`.
- Fresh public receipt: `sources/receipt.json`, SHA256 `010a7bdd25575b8b3c63f3126a38797a8451d44998af4e0f9980e9d4df2d3f2c`, acquired 2026-10-25T00:36:56.624840+00:00.
- Mathematical TeX: `sources/published-source/main.tex`, SHA256 `cb9163437ab912588f8cdbcc10965badeb5a68aef6efb242884a61f4d4fbbfad`.

Read all eleven published PDF pages, all six sections and every proof; checked the complete current TeX, the 336-line original `verification/submission/PROOF.md`, all nine executable finite checker implementations, and the portable authentication/replay runner. The earlier proof's introductory workflow/status language was encountered but not relied upon. Archived reviewer reports, verdicts, priority ledgers, and historical status files were not consulted. The package contains such files, so authentication of their bytes must not be confused with adopting their opinions.

An independent child checked the original Berger contribution's model and quantifiers, then was reassigned by the parent. I independently completed the official final-publication binding and read the entire two-page contribution. The child did not claim a complete main-proof review; my own all-page/proof review supplies that work. No sibling review opinions were read before this mathematical conclusion.

## Verified statement and exact boundaries

Fix one law for independent, identically distributed space-time coordinates `p_(s,x)` with `0<p<1` almost surely. A walk starts at zero and takes nearest-neighbor steps on Z, right with the local probability. For every deterministic positive real sequence `M_N → ∞`, every fixed ε>0 and K>0, the full ℓ1 discrepancy between quenched and averaged time-N endpoint masses on consecutive deterministic half-open intervals of length M_N exceeds ε with environmental probability at most `C_(ε,K) N^(-K)` eventually. The estimate is uniform in each deterministic alignment. Constants may depend on the fixed law; the eventual threshold may depend on the scale sequence.

The result is not a pointwise heat-kernel approximation, an uncoarsened total-variation convergence assertion, or a concentration assertion about a single sampled trajectory. “Quenched endpoint law” is itself random as the environment varies; the outer probability is over environments. No rate of divergence, monotonicity, integrality of the target scale, symmetry of drift, uniform ellipticity, or inverse probability moment is used.

The claim does not supply law-uniform constants as the law degenerates toward arrows, does not cover static or correlated environments, and does not assert simultaneous control of environment-chosen partitions. Starts used in the coalescing comparison have the same parity. These restrictions are essential to the actual argument, rather than cosmetic qualifications.

## Proof attack and verification

### 1. Replica return and occupation estimates (pages 3–4)

The parameters satisfy `a=q(1-q)>0`, `δ=E[p(1-p)]>0`, `σ²=a−δ≥0`, and `a≤1/4`. Shared-site opposite replica steps have probability δ; distinct sites have probability a because they use independent fresh coordinates. Thus the averaged half-difference chain really has the two claimed rates, even when the original annealed walk is biased.

I checked the first-return generating-function identity, its square-root branch and denominator bound. Monotonicity of return probabilities is justified by reversibility and positivity of the transition operator: holding at least 1/2 makes `2P−Id` a self-adjoint Markov contraction. This legitimate spectral step supplies the coefficient estimate that a generating-function upper bound alone would not imply.

The backward-profile boundary recurrence is correct; its coefficient `1−2δ−a` is nonnegative. It proves the needed maximum at zero, so the conditional estimate holds for an arbitrary frozen old endpoint law. This is stronger than only an unconditional return estimate and is exactly what the proof uses.

Ordered overlap moments are valid without independent overlaps. The previous overlaps are measurable in the conditioning filtration; zero time gaps use `I_t≤1`, and the final conditional sum costs at most the partial Green sum. Selecting a fixed moment order after selecting K makes the occupation tail superpolynomial. No growing-order moment bound is silently needed.

### 2. Environmental martingales and coarse expectation (pages 4–6)

The layer-exposure increment and conditional variance are exact, with cross terms removed only for independent variables within the fresh layer. The Lipschitz estimate uses a physical separation of two, preserving nearest-neighbor parity. The exponential supermartingale applies to the joint event of large deviation and small predictable variation; conditioning the martingale law on that future event would have been invalid, and the paper does not do so.

I verified the bounded-range maximal estimate, its use for an entire path segment, and the conditional-range bounded-differences argument. The Fourier heat-kernel estimates use the binomial parity lattice; they do not assume aperiodicity on Z. Interval gradients telescope along that lattice. Their maximum-times-ℓ1 estimate yields the displayed squared-gradient bound. Splitting the time sum at `(M+1)^2` gives the claimed logarithm, including `M≫sqrt(n)` and time-zero semigroup terms.

The window count and outside-window expectation are uniform in real alignment. For fixed B, the expectation upper bound tends to zero whenever n and M separately diverge; taking B large only afterwards is valid. This double-limit step imposes no hidden relative growth condition on M.

### 3. Auxiliary polynomial scale (pages 6–7)

This step is used at a separate deterministic integer scale, not at the possibly very slowly growing target scale. The dyadic blocks cover precisely the exposed time indices; bounding an incomplete deterministic interval by a longer one is permissible. The common overlap failure is charged once before the sign-test union bound.

For `d=γ−1/4`, the entropy margin is `5d/4>0`, the boundary-variance margin is `3d/4>0`, and `r/M` tends to zero uniformly over allowed M. These are strict margins for every fixed γ>1/4. The final application chooses γ=5/16, so no limiting endpoint γ=1/4 is claimed.

The periodic boundary majorant includes the drift shift vh and arbitrary real alignment. The residue-class argument uses `M/gcd(2,M)` on the binomial index, correctly distinguishing physical parity from ordinary residues. Its expectation tends to zero. Comparing each endpoint to the real center `X_m+vh` gives the full ℓ1 restoration constants. Equality with a boundary is included in the bad set, so half-open cells do not create an exception.

### 4. Old-law mass and same-parity coalescence (pages 7–8)

The soft interval majorants have mean `O(N^(-1/8) log N)`, smaller than `N^(-1/32)`. Their variance exponent is −7/32, giving a positive tail exponent 5/32 after using the shrinking threshold. A union over O(N) prescribed intervals preserves superpolynomial decay.

In a fixed environment, independent transition coins until meeting and common coins thereafter preserve both quenched marginals. Averaging is performed after defining that coupling. Before meeting, different sites use fresh independent environment values, so the positive half-gap is a homogeneous symmetric lazy walk with rate a. Same-parity paths cannot cross without meeting. Reflection with holding steps gives the stated survival sum and the correct factor of two for full ℓ1 distance. Opposite parity would fail and is not used.

Within an auxiliary cell, both the old quenched law and the annealed conditional replacement live on the same reachable parity sites. Null annealed cells have zero quenched mass. The replacement preserves cell mass and its ℓ1 distance from the annealed law equals the old coarse discrepancy exactly. Kernel contraction, coalescence, and Jensen's inequality therefore give equation (18). Each translated future kernel sees only a deterministic change of target alignment, to which the uniform expectation estimate applies.

### 5. Moving strips and closure (pages 9–10)

This is the most delicate step and survives direct falsification attempts. The killed path remains inside a deterministic moving tube before each transition variable is consulted. The environment at a killed destination is not used. Thus changing a strip has no influence on starts outside the stated J_k in either the original or altered environment. Merely keeping endpoints in a tube would not suffice; the paper kills at the first exit and bounds a maximum over the whole segment.

Strip input vectors consist of disjoint deterministic coordinate sets. They remain independent for irrational drift and independent of the old environment. The proof does not assume independence of endpoint masses, path cones, or kernels from different starts.

Each affected row changes by at most two in ℓ1, even for subprobability kernels. Consequently the actual nonlinear norm has coordinate oscillation at most `2w_k`. A start belongs to at most six influence intervals, so `Σw_k²≤6 max w_k`; conditional bounded differences gives the stated exponent. Relevant inputs can be restricted to finitely many reachable coordinates. The old-mass event is measurable before the fresh segment.

The killed loss is nonnegative, and its exact ℓ1 mass is D. Its conditional expected value is uniformly at most `d_N`, allowing both restoration and conditional expectation transfer. The final ε allocation is sufficient. The terms `exp(−c N^(1/32))` and `exp(−c(log N)^2)` dominate every inverse power. Only the deterministic expectation term needs an eventual threshold depending on the target scale sequence. This is precisely why an arbitrarily slow or nonmonotone diverging M_N is allowed.

## Reproduction and independent controls

The published portable runner authenticated all 92 finite package members, including native historical pins, then executed isolated copies of eight standard-library programs and one optional SymPy 1.14.0 program. All exited zero, with no stderr, and output schemas/counts were validated: **376,506 finite assertion instances** in total. These are repeated parameter instances, not 376,506 independent mathematical results. The replay is recorded in `published-replay.json`; its scope is finite identities and excluded-boundary controls, not proof of infinite-time limits.

I wrote `fresh_controls.py` without importing any archive checker. It passed **75,943 checks**, including:

- 6,858 fully enumerated path cases with three genuinely irrational drifts, using exact arithmetic in Q(sqrt(2)); these check consulted-variable tube geometry and strip influence without floating-point boundary decisions.
- 1,536 complete environment/functional cases for the actual killed coarse ℓ1 norm under biased iid two-atom environments. Exact strip-by-strip Doob exposure verified 516 conditional range bounds, the variance decomposition, and the squared influence bounds. This checks the nonlinear functional, not only a linear surrogate.
- 553 general unimodal probability sequences and 24,885 residue inequalities, beyond binomial examples.
- A negative control with a strictly elliptic but globally correlated environment: its time-32 coarse discrepancy is `143740020097336951/144115188075855872 > 0.9`. This is outside the theorem and demonstrates why ellipticity alone is insufficient.
- Exact strict exponent margins arbitrarily close to the auxiliary γ=1/4 boundary, and an exit-and-return control distinguishing pathwise killing from endpoint-only restriction.

The new exact-floor routine initially failed its own integer-boundary self-test; the bracketing condition was corrected before any accepted mathematical run. This was a reviewer harness error, not a paper defect. The fresh checks were rerun under Python optimization; explicit runtime checks remain active rather than disappearing with assertions. Neither finite successes nor the number of checks are used as substitutes for the analytic proof.

## Primary-source relation and remaining gaps

The main proof imports no unproved research theorem from the cited literature: the necessary probability, heat-kernel, replica and coupling inputs are established in the manuscript. The functional-analytic spectral argument uses the standard spectral theorem for a bounded self-adjoint operator; its operator hypotheses are checked above.

For the historical comparison I read Berger's entire contribution in both the MFO original and [official EMS final PDF](https://ems.press/content/serial-article-files/46239), final printed pages 2151–2152. Its model refreshes the space-time iid nearest-neighbor elliptic environment. Theorem 1 uses deterministic diverging coarse scales and full sum-of-absolute-differences with a faster-than-every-power environmental tail in spatial dimensions at least two. The following conjecture denies the corresponding one-dimensional statement. The paper's one-dimensional affirmative assertion matches that comparison. I visually checked the final displayed equation, since text extraction omitted its absolute-value bars. The report's notation has a harmless missing superscript in its lattice reference for general dimension; it causes no one-dimensional model mismatch. This confirms what conjecture is being contradicted, not when it was first contradicted.

`source-bindings.json` records both primary PDF hashes and exact read scope. I did not conduct an exhaustive literature or originality review. The manuscript's four older-source access gaps remain a disclosed historical limitation; this review neither closes them nor treats the earlier audit's access history as independently established. No claim of firstness, independent discovery, new method, present-day open status, or publication priority is approved by this verdict.

## Final gate

**PASS for correctness and reproducibility at the exact published scope.** Strongest verified result: all deterministic diverging real coarse scales, uniform deterministic alignment, superpolynomial environmental fixed-ε tails for each fixed strictly elliptic iid space-time nearest-neighbor law on Z. Exact mathematical gap found: none. Remaining nonmathematical gap: historical originality/anticipation is unresolved, and there is no conventional human peer review. No manuscript repair, publication, Git, spreadsheet or outreach action was taken.
