# Independent mathematical and primary-source audit: problem 9900008

Date: 2026-10-07.

## Verdict

**Mathematical PASS for the precise frozen counterexample.** No mathematical repair is required. A nonzero locally finite diffuse measure on R², viewed from its light line, is invariant under every measurable, pointwise-covariant, measure-preserving allocation of its original state but is not mass-stationary.

**Source/presentation PASS only with the accompanying `CREDIT_ADDENDUM.md`.** The frozen source discussion omits an important established product-lift attribution. The added credit is required wherever the candidate is presented as a contribution. Neither this audit nor its successful mathematical check certifies novelty, historical priority, human peer review, or a formal machine proof.

The proof was audited in full, independently of earlier review verdicts. All original files remain unchanged. This review performs no publication.

## 1. Exact material reviewed

The immutable author archive is:

- `DIFFUSE_MASS_9900008_AUTHOR_SAFE_FREEZE.zip`
- 18,611 bytes
- SHA-256 `bd2a43c1d0de12ea87ba217b3b5316a00e008d1b547992d7bdd038ff695aed9b`

The principal mathematical input is:

- `PROOF.md`, 11,562 bytes
- SHA-256 `d700c5af20ff7a0dcafcabfeb2b78a35dcd740169318aafb8af2ab4eaba86331`

The principal source-scope input is:

- `SOURCE_AUDIT.md`, 6,258 bytes
- SHA-256 `8b3bd2646c060edfbdf05a658e5fee37f13fa5f1f83e3614ee74eb35a1f4b2e0`

Every one of the archive's eight uncompressed members was compared byte-for-byte against the recovered input directory. All match. Every manifest entry verifies. `REVIEW_METADATA.json` records all member hashes and sizes, new primary-source retrieval pins, and supplementary execution results.

The review covers the complete proof, source scope relevant to its mathematical claim, its public prior-work citation, and the relationship between its analytic argument and finite checker. It does not independently rerun the private dataset-corpus eligibility gate, all historical repository searches, or an exhaustive literature search. Historical metadata is not silently promoted into newly verified evidence.

## 2. Source question and tested class

Thorisson's *Some Open Probability Problems*, Section 4, defines allocations by a measurable displacement of the observed pair and asks in Problem 4.1 whether diffuseness suffices without stationary independent background. The downloaded original's pp. 5–6 were read and visually inspected. Its statement does not impose freeness, full support, absolute continuity, or finite total mass. [Original author-source PDF](https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf).

Last–Thorisson (2009), Section 2 and Example 3.4, provide the ambient measurable flow and pointwise allocation covariance. Definition 6.1 and Remark 6.2 give the joint mass-resampling test. Problem 7.5 is the diffuse allocation question; Problem 7.3 instead concerns preserving transport kernels. The relevant definitions and surrounding sections were read, and printed p. 24 was visually checked. [Primary electronic reprint](https://arxiv.org/pdf/0906.2062).

These sources permit the state model used in the candidate. The ambient group is R² with its usual topology, Borel sets, and planar Haar measure. The law under examination need not itself be translation-stationary: mass-stationarity is the proposed conclusion, not an input stationarity condition on that law.

Take the first coordinate as horizontal, and use

    θ_t η(B) = η(B+t).

For a pointwise-covariant allocation, setting π(ω)=τ_ω(0) yields

    τ_ω(s) = s + π(θ_s ω).

This follows directly by substituting t=s in covariance. Conversely this formula gives covariance for every state and every pair of translations, using the group law. It neither assumes nor implies injectivity on arbitrary configurations. The preserving condition is the equality of measures τ_*ξ=ξ. The distributional condition separately tests the shifted state θ_{τ(0)}ω. Conflating those two equalities would invalidate an argument, but the candidate does not do so.

## 3. Model and measurable structure

Let

    ν = Σ_{n∈Z} δ_n + 2Σ_{n∈Z} δ_{n+1/2},
    μ = λ₁ ⊗ ν,
    Ω = R/Z,
    θ_(a,b)u = u+b mod 1,
    ξ(u) = μ_u := θ_(0,u)μ,
    Q = δ_0.

The additional random element X has one value and trivial action.

### 3.1 Local finiteness and diffuseness

A bounded rectangle intersects finitely many horizontal support lines, each in a horizontal interval of finite length. Its measure is therefore finite. Covering a compact set by such a rectangle proves local finiteness. The countable sum of line-length measures is Borel and Radon; alternatively this follows from local finiteness of the sum of Radon measures. Every singleton has zero horizontal Lebesgue mass. Thus μ is diffuse although singular with respect to planar Lebesgue measure. The support is exactly R×(Z/2), it contains the origin, and μ is nonzero.

No conclusion relies on a finite total mass. The measure has infinite total mass but finite mass in every compact set. The distinction between diffuse and absolutely continuous is essential and is respected.

### 3.2 Action, phase, and observability

The circle action is continuous, hence jointly Borel. The flow-adaptation equation follows from θ_sθ_t=θ_{s+t} and horizontal invariance of μ.

For f continuous with compact support on R², put F(y)=∫f(x,y)dx. Then F is continuous with compact support, and

    ∫f dμ_u = Σ_n F(n-u) + 2Σ_n F(n+1/2-u).

Locally in u only finitely many summands are nonzero, with a common finite bound on the index range. This proves vague continuity of u↦μ_u. The line-density pattern distinguishes u modulo 1: the density-1 support family determines the phase. Thus the map is injective. It is a homeomorphism from compact Ω onto its image in the Hausdorff space of Radon measures. Consequently the Borel state is fully observable from ξ, and σ(ξ)=B(Ω).

This also disposes of a canonical-state-space objection. Any allocation defined on the whole canonical measure space restricts to one of the allocations audited here. The orbit itself is an invariant compact Borel subset. No unseen horizontal coordinate or auxiliary source of randomness is retained in Ω.

The exact stabilizer of each state is R×Z. Having this nondiscrete stabilizer is allowed by the question and is the cause of the obstruction, rather than a missing hypothesis.

## 4. Universal preserving-allocation argument

Fix an arbitrary measurable allocation satisfying pointwise covariance. Write

    π(0)=(a₀,b₀),   π(1/2)=(a₁,b₁).

For every real x and integer n,

    θ_(x,n)0 = 0,
    θ_(x,n+1/2)0 = 1/2.

Therefore covariance forces

    τ_0(x,n) = (x+a₀,n+b₀),
    τ_0(x,n+1/2) = (x+a₁,n+1/2+b₁).

These identities hold for all x, not merely almost every x. Each source line is carried to one complete target line by a horizontal translation. Within one source family, distinct integer translates have distinct target heights. Different source families are allowed to collide at this stage.

For any Borel target set A, changing variables along the horizontal coordinate gives exactly

    τ_{0*}μ = λ₁ ⊗ [Σ_n δ_{n+b₀} + 2Σ_n δ_{n+1/2+b₁}].

This is an equality of measures, not an approximation by finite windows. No derivative, monotonicity, invertibility, or continuity of the allocation has been used.

### 4.1 All noninjective possibilities are covered

If τ is preserving, test the preceding equality on [0,1)×{r}, for each r in [0,1). There is exactly one integer n satisfying n+b₀=r when r is the residue of b₀, and none otherwise. The analogous statement holds for the second family. Thus, denoting residues modulo 1 by brackets,

    1{[b₀]=r} + 2·1{[1/2+b₁]=r}
      = 1{r=0} + 2·1{r=1/2}.

This direct finite-segment test justifies the candidate's per-period equality without pushing an infinite measure onto a compact quotient.

Positivity excludes target residues outside {0,1/2}. If both families land on the same target residue, that target receives mass 3 per horizontal unit, which is impossible. If the residues are swapped, the target at 0 receives mass 2 rather than 1. The only case is

    b₀ ∈ Z and b₁ ∈ Z.

One cannot make the heavy target from two light lines. Unit-period covariance makes the map n↦n+b₀ a translate of Z, so a specified target line receives at most one light source line. Trying to send two light lines there violates covariance; trying to split a line violates horizontal covariance.

Hence π(0)∈R×Z, and θ_{π(0)}0=0. The re-rooted measure and the entire observed state are identical to their originals, pointwise on the only Q-supported state. Therefore every preserving allocation leaves Q invariant.

The proof uses only preservation at u=0. It is valid when preservation is required Q-almost surely, as well as under the stronger everywhere-preserving convention. Measurable allocations depending only on ξ are included because σ(ξ)=B(Ω). Identity is an admissible allocation, so the premise is not vacuous.

### 4.2 Why a null root cannot be reassigned freely

It is true that μ({0})=0. However, changing τ_0(0) while retaining covariance changes τ_0(x,0) for every horizontal x, and likewise the image of every density-1 line. Those unit segments have positive mass. The preservation equations therefore constrain the root image. Arbitrary changes on a singleton are not permissible equivariant allocations.

This argument uses the source's pointwise covariance convention. It makes no claim for a different convention in which allocations are equivalence classes modulo spatial null sets and no covariant root representative is specified.

## 5. Failure of the full mass-stationarity requirement

Take C=[0,1)², and let U be independent uniform in C. This is an allowed relatively compact Borel set with positive Haar measure and Haar-null boundary. The shifted window C-U has horizontal length 1 and, except for irrelevant boundary choices, contains one light line at vertical coordinate 0 and one heavy line at coordinate +1/2 or -1/2. Thus

    μ(C-U)=3.

Conditional mass-uniform selection of V in C-U gives light-root probability 1/3 and heavy-root probability 2/3. Horizontal displacement has no effect on the state, while a heavy displacement changes the phase to 1/2 modulo 1.

The evaluation

    H(η)=η([0,1)×{0})

is measurable in the evaluation sigma-algebra for locally finite measures. It equals 1 under Q. After resampling, it equals 2 with probability 2/3. Therefore

    P(H(θ_Vξ)=2)=2/3 ≠ 0=P(H(ξ)=2).

The two first marginals already disagree. In particular the required joint laws of (θ_Vξ,U+V) and (ξ,U) cannot agree. The proof neither replaces the joint definition by a marginal sufficiency claim nor relies solely on a comparison with a guessed Palm law.

### 5.1 Optional Palm calculation

Under uniform phase measure P on Ω, vertical translations preserve P, and the intensity is μ_u([0,1)²)=3. Integrating f(θ_tu) against μ_u(dt) over the unit square and then against P(du) gives f(0)+2f(1/2): sampling a light line roots at phase 0, and sampling a heavy line roots at phase 1/2. The normalized Palm distribution is therefore (δ_0+2δ_{1/2})/3. This agrees with the direct witness above. Its role is a consistency check, not a substitute for the joint-law failure.

## 6. Explicit check of the transport-kernel boundary

The candidate correctly excludes the stronger Markov-kernel premise. This can be verified analytically for its exact model.

Define an invariant kernel through the rooted phase v=u+s₂:

- If v=0 modulo 1, send all mass from s to s+(0,1/2).
- If v=1/2 modulo 1, send half to s-(0,1/2) and retain half at s.
- At all other phases, retain the mass at s.

This is a measurable Markov kernel. Its definition through rooted phase makes it pointwise covariant. At each phase u, a light line of weight 1 moves to the corresponding heavy line; the heavy line sends weight 1 back to the light line and retains weight 1. Each target therefore receives exactly its original mass, so the kernel preserves μ_u for every u.

At Q's root the kernel always moves the phase to 1/2. Thus Q fails this particular preserving Markov test. It does not satisfy the premise of the all-Markov characterization problem. This check is independent of a finite-state program and demonstrates concretely why the allocation result cannot be promoted to the kernel question.

## 7. Source credit and bounded literature scope

The accompanying addendum is mandatory: the Lebesgue-product device is already explicit in Last–Thorisson's 2015 v2 Section 8. Proposition 1 addresses preservation/reflection of mass-stationarity under that lift; Theorem 8 uses added stationary backgrounds. The present periodic model is not stated in those inspected sections. Mathematical validity and priority are separate questions. [Primary manuscript](https://arxiv.org/pdf/1405.7566v2).

The frozen proof's mathematical distinction from positive-density and background-randomized results is correct. Theorem 6 in that manuscript assumes a positive density field with additional line-integrability conditions; the current μ is singular. Theorem 7 tests independent stationary backgrounds, a larger class than the original-state allocations considered here.

Last–Thorisson's 2023 paper, Section 8 and Remark 8.1, supplies a related horizontal-line/invariant-direction obstruction for balancing two different measures. It supports the relevance of this mechanism, but is not a theorem identifying the submitted allocation-invariance law. [Primary v2 manuscript](https://arxiv.org/pdf/2112.13053v2).

Khezeli–Mellick's 2024 v2 Theorems 1.1–1.2 were inspected. The candidate has a nontrivial invariant direction and charges translates of that direction, so the relevant extra hypotheses in those factor/balancing results do not give a contradiction. Those results concern a different allocation existence problem. [Primary v2 manuscript](https://arxiv.org/pdf/2303.05137v2).

The exact cited `TURN_3.md` at commit `7d244eed5d7ddd89d5c540aecfa72490b7b30073` was independently read through the connected repository tool. It explicitly distinguishes an atomic `(1,2)` allocation/Markov class-separation control from Cox-projected tests and from its separately scoped positive results. The frozen proof appropriately credits that atomic control. This fresh check verifies that particular cited passage, not the full history of PR 284 or all neighboring results. [Pinned prior authored record](https://github.com/AlecKriebel/Math/blob/7d244eed5d7ddd89d5c540aecfa72490b7b30073/unsolved_math_prioritization/attempts/30001080/TURN_3.md).

All five newly downloaded mathematical PDFs have the exact same byte counts and SHA-256 values reported in the frozen metadata. Thus the source correction concerns interpretation and attribution, not a changed source edition. The 2015 PDF carries an arXiv v2 revision label of 17 July 2015 and a different internal typesetting date, 24 April 2019; it is identified by version and hash. This audit does not certify final-publisher identity or current publication status of every cited preprint.

## 8. Supplementary executable checks

The frozen verifier was read before execution. Its checks exhaust nine quotient label cases, test 530 rational unit windows and 361 rational translation pairs, reject 18 corrupted certificates, and check two unequal-weight variants. All passed on this review's rerun.

Both `--self-test` and `--integrity` passed under ordinary Python, `-O`, `-I`, and `-I -O`: eight successful executions. All seven manifested payload files passed integrity. Exact output hashes are recorded in `REVIEW_METADATA.json`; a full self-test output is supplied as `checker_rerun.json`.

Those checks are useful regression and arithmetic controls only. The continuous family of all measurable allocations is covered by the analytic covariance argument in Section 4, and the joint distributional failure by Section 5. No finite sample enumeration proves either universal claim.

## 9. Final acceptance and exclusions

The frozen proof establishes a negative answer to the literal background-free diffuse implication, already on R², under the primary pointwise-covariant definition. Its construction, noninjective-allocation analysis, root evaluation, and direct mass-stationarity witness are sound.

The accepted presentation consists of the unchanged frozen proof together with `CREDIT_ADDENDUM.md`. No mathematical correction patch is needed. The addendum corrects the incomplete credit for an existing product-lift method.

Acceptance excludes:

- an assertion that the product-lift method, negative implication, or particular example is globally novel;
- free-action or no-invariant-direction variants;
- a one-dimensional diffuse counterexample;
- positive-density or full-support variants;
- independent-stationary-background allocation tests;
- all-Markov or Cox-projected allocation characterization claims;
- human peer review, formal proof-assistant certification, or exhaustive prior-art clearance.

Only authored audit text, public links, and verification metadata belong in this review's distributable files. Downloaded papers, extracted text, and rendered source pages are excluded.
