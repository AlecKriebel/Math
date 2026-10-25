# Independent analytic review — Zenodo 23180194

**Conclusion: SUPPORTED_AT_STATED_SCOPE.** No substantive mathematical defect was found in the published seven-page argument. The sufficient implication is supported by a direct measure-theoretic reconstruction, not inferred from the finite verification programs. This is an independent AI-assisted analytic review, not human peer review or a formal proof certificate. Publication decisions and the independent scope/adversarial gates remain the parent task's responsibility.

## Exact edition and scope

The record is **10.5281/zenodo.23180194**, *Measure-only preserving Markov transports characterize mass-stationarity*, version **1.0**, published **6 October 2026**. The manuscript's printed date agrees. The actual public PDF has seven pages and SHA-256 `3503e9351da854e882cd8ce26f1450482b44e1f5e547b06224875c3b55b391f3`; the verification ZIP has SHA-256 `6007977e60dd4464e0c62309ad694697d4f927bae407531b0bee5285e80fa8a9`. There is no additional reader PDF. Both assets, API metadata and all 19 extracted files independently rehash unchanged after review/replay; see `final_source_integrity.json`.

All seven actual manuscript pages were read before the supplied test programs or any current sibling mathematical finding. Critical displayed equations and their surrounding arguments on pages 4–6 were also checked visually. The mathematical support scripts were read in full before their replay. The dedicated historical `PRIORITY_NOTE.md` was not read.

The hypotheses are essential and precise:

- G is locally compact, second countable, Hausdorff and Abelian.
- The ambient space is arbitrary measurable, with a jointly measurable group action.
- Q is sigma-finite; it need not be a probability measure.
- ξ is a covariant measurable locally finite Radon measure, nonzero Q-almost everywhere.
- Every tested kernel is a row-mass-one Markov kernel, covariant and pointwise ξ-preserving, whose dependence on the state is measurable through ξ alone.
- The hypothesis tests **the full ambient law**, against every nonnegative measurable function of ω. It does not merely test the marginal law of ξ.

The claimed new implication is full ambient invariance under those kernels ⇒ joint Campbell/Mecke reversal. The Palm equivalence, equivalence with mass-stationarity, and converse transport invariance are credited primary imports. A non-sigma-finite pushforward law of ξ, infinite total mass of ξ, and infinite Q are permitted. There is no claim for non-Abelian groups, non-locally-finite measures, the zero-measure case under the source definition, or a smaller deterministic/Cox allocation test class.

## Independent reconstruction of the universal argument

### 1. Measurability and sigma-finiteness

For an LCSC Hausdorff space the locally finite Radon-measure space with vague Borel/evaluation sigma-field is standard Borel. Its translation action is jointly continuous. Consequently the canonical period graph `{(μ,t): θ_t μ=μ}` is Borel, and its pullback J in Ω×G is measurable. This uses standard Borel structure on the canonical measure space, never on Ω.

The Campbell kernel measure `c(dω,dt)=Q(dω) ξω(dt)` is sigma-finite. Partition Ω into countably many finite-Q sets D_j, take a compact exhaustion C_n of G, and intersect the first coordinate with `{ξ(C_n)≤k}`. These product sets cover Ω×G and have c-mass at most kQ(D_j). The reversal R(ω,t)=(θ_tω,−t) is a measurable involution, so its pushforward is sigma-finite as well. No disintegration over ξ or sigma-finiteness of its marginal law is invoked.

### 2. The local kernels are legal Markov tests

For symmetric compact C containing a neighborhood of zero, the printed coefficient

`a(μ;s,t)=1_C(t−s)/[(1+μ(s+C))(1+μ(t+C))]`

is measurable, symmetric in s,t, and covariant under simultaneous translation. Compactness and local finiteness make the denominators finite; its μ-row integral is bounded by μ(s+C)/(1+μ(s+C))<1. An R0-invariant canonical gate b preserves this symmetry. Adding the remaining holding probability gives a nonnegative probability kernel depending only on μ and s. Tonelli applied to the symmetric jump measure `a_b(μ;s,t) μ(ds) μ(dt)` proves μ-preservation, including infinite μ(G).

The weighting `m=a(ξ;0,t)c` has first marginal at most Q. For a Q-integrable nonnegative test f, invariance of the Markov kernel yields equation (10). The incoming jump integral is bounded by the full invariant expectation, and the outgoing one by Qf, so subtracting the common holding integral is legitimate. There is no `∞−∞` operation.

### 3. Oriented gates recover reversal off the period set

For a canonical measurable set A, let F_A consist of pairs whose initial measure lies in A and whose translated measure does not. For a spatial Borel B, F=F_A∩(M×B) and R0F are disjoint. The gate `1_F+1_R0F` is therefore a legal invariant indicator. Test equation (10) with `f=1_D 1_A(ξ)` for finite-Q D.

On F the shifted test vanishes; on R0F the unshifted test vanishes. After applying R to the surviving incoming term, the two remaining integrals are exactly the masses of `(D×B)∩ρ⁻¹F_A` under m and R*m. This preserves arbitrary ambient information through D; no factorization of D through ξ is required.

For fixed A, those restrictions are finite on each D_j×G and agree on every rectangle there. Finite-measure uniqueness extends the equality to the product sigma-field, even if the ambient sigma-field is not countably generated. A countable separating family of canonical measure sets, with complements, covers Jᶜ by the F_A pieces. Disjointification then gives equality on all measurable subsets of Jᶜ.

The weight is R-invariant and strictly positive on Ω×C. Integrating truncated reciprocal weights against the equal weighted measures and using monotone convergence removes it. Repeating on an increasing symmetric compact neighborhood exhaustion gives the full unweighted reversal off J. A single small neighborhood is insufficient in general; the manuscript explicitly uses the exhaustion.

### 4. Period transports recover the information invisible to measure changes

For fixed μ, H=H_μ is a closed subgroup, and Abelianity gives `H_(θ_s μ)=H`. The kernel κ_B is the normalized restriction of μ to H∩B, with a holding fallback if that mass is zero. Its measurable definition uses the canonical Borel period graph and ordinary kernel integration. It does not require measurable choices of Haar normalizations across subgroups.

To verify preservation, fix this one μ and choose any Haar measure on H. Each restriction `(θ_s μ)|H` is H-invariant and Radon, hence equals c_s times that Haar measure, with finite c_s≥0. Finiteness follows by evaluating on a compact H-neighborhood of positive finite Haar mass. If β=λ_H(H∩B)=0, all rows hold. If β>0, every positive-normalizer displacement row is the same probability ν_B; the positive set E of starting locations is measurable and H-invariant. Both μ and μ restricted to E are H-invariant. Tonelli therefore shows that displacement on E preserves μ|E, while holding preserves μ|Eᶜ. This also covers mixed zero/positive normalizers in a single measure.

All κ_B-displacements are periods, including the zero fallback. They leave ξ and w_B(ξ) fixed but may change the ambient state. Apply the full invariance hypothesis to `w_B(ξ) f(ω)`. Its finite positive factor cancels normalization pointwise; on the zero branch both weighted sides vanish. This establishes equation (14) with nonnegative extended integrals and no integrability subtraction.

The restriction μ|H is zero or a Haar multiple. Since H is Abelian, inversion preserves this measure and w_−B=w_B. Applying (14) with −B gives rectangle reversal on J. Relatively compact B extend by exhaustion. The finite-c-mass product cover already constructed supplies finite blocks for the rectangle-to-product extension. Thus c|J=(R*c)|J. Hidden marks are retained because f remains an arbitrary function of ω.

### 5. Completion, support and inherited hypotheses

The off-period and period pieces give c=R*c, precisely the full ambient Mecke identity. The original 2009 paper's displayed equation (2.7) and surrounding sufficiency statement explicitly apply on the general measurable-flow space with sigma-finite Q and Q(ξ=0)=0. Its Theorem 6.3 then identifies the same mass-stationarity sampling identity; its Theorem 4.1 supplies the converse invariance. Pointwise preserving kernels in this note satisfy the primary theorem's almost-everywhere balancing hypothesis for the reconstructed stationary measure.

Support at the origin is a consequence, not a missing hypothesis: the reversal mass of `{0∉supp ξ}×G` is zero since ξ charges its own support. Thus the integral of `1_S ξ(C_n)` vanishes for every n. Nonzeroness and exhaustion imply Q(S)=0. For the mass-sampling formula, λ(∂C)=0 ensures almost every r lies in int C, so C−r contains a neighborhood of the supported origin and its ξ-mass is positive. The chosen zero-denominator branch does not change that conclusion.

## Boundary tests and falsification attempts

`fresh_controls.py` was written and run **before** reading or running the released verification code. It uses exact rational arithmetic and no submitted imports. Its **352 assertions** check finite cyclic examples with unequal atoms, missing atoms, nontrivial periods, constant measures, zero measures, and isolated atoms. It verifies stochastic row sums, pointwise mass preservation, covariance, gated tests, normalized period kernels, and exact constraint ranks for the full marked orbit.

The marked orbit has all n distinct ambient phases even when ξ has fewer distinct translated values. For μ=(0,1,0,1,0,1), off-period tests have constraint rank 3, while adding period tests gives rank 5 and the unique nonzero Palm-law ray. For a constant four-state measure the ranks are 0 and 3 respectively. Thus the checks do not silently collapse hidden periodic states. The mixed-normalizer case explicitly holds at a zero-mass starting phase and moves mass at supported phases, while preserving μ.

Negative controls reject nonsymmetric C and an unoriented gate. A point mass on one hidden phase fails an otherwise legal period-shift test for the constant measure. All-zero μ imposes no such law constraint in this finite control, consistent with the theorem's explicit exclusion rather than an accidental extension.

The first diagnostic used only a fixed local C and asserted global uniqueness for an isolated atom. That overstrong control failed. Including the full finite group, the terminal member of a compact exhaustion, restores the intended conclusion. This is recorded as a limitation of the initial control and positive evidence that the manuscript's exhaustion step matters; no manuscript repair or changed theorem hypothesis was needed.

For an analytic infinite-mass check, take G=R, Ω=R with translation action, Q=Lebesgue measure, and ξ equal to Lebesgue measure at every state. This is covariant. Any measure-only invariant Markov kernel is convolution by a fixed probability distribution, so Tonelli and translation invariance preserve Q. The pushforward Q◦ξ⁻¹ is infinite mass at a single measure and is not sigma-finite. The conclusion still holds. This directly checks the claimed distinction between sigma-finite ambient Q and a possibly non-sigma-finite canonical marginal. The same proof works with an arbitrary measurable independent mark space carrying a probability measure; it uses no standard Borel assumption on that space.

## Released replay and source custody

The full finite verifier was inspected before execution. It checks a strict file manifest, disallows optimized Python, and runs three mathematical control scripts with `-E -B`, comparing complete output bytes to the released expected values. It neither edits the published source nor pretends to prove the analytic theorem.

Replay succeeded with Python 3.14.6 and SymPy 1.14.0:

- turn1: 18,814 assertions;
- turn2: 75,172 assertions;
- noncyclic/marked controls: 186,869 assertions;
- total: **280,855** assertions, with all expected output hashes matching.

`published_replay.json` reports `PASS_FINITE_CONTROLS_AND_PACKAGE_HASHES` and explicitly sets analytic theorem verification and formal machine proof to false. Some released controls concern ancillary Cox constructions; these are not promoted to claims of this seven-page paper or used to expand its theorem. All 19 extracted files, original assets and metadata were rehashed unchanged afterward.

## Primary interfaces, attribution and remaining limits

The directly inspected primary PDF is Last–Thorisson's official electronic reprint [arXiv:0906.2062v1](https://arxiv.org/pdf/0906.2062v1), SHA-256 `0a4c4813cef44e99c232d0687aa704554248675c621755be85568d0588999719`. Sections 2–3 supply the ambient definitions, equation (2.7) supplies Mecke/Palm equivalence, Theorem 4.1 supplies transport invariance, Definition 6.1 and Theorem 6.3 supply mass-stationarity, and Section 7 distinguishes the bounded weighted-kernel theorem from the measure-only Markov question. Their hypotheses match the manuscript. The 1967 original Mecke body was not independently reread; the explicit general-ambient import is the 2009 primary formulation.

The author-version [arXiv:1405.7566v2](https://arxiv.org/pdf/1405.7566v2), Section 6/Theorem 6, was checked for its positive density and line-integrability/half-line hypotheses. The [official Oberwolfach report](https://ems.press/content/serial-article-files/46189), Thorisson pp. 2692–2694, was checked for the all-Markov framing. These contextual checks do not certify that no later work exists. The 2011 final COSA body was unavailable in the present acquisition and is not load-bearing here; the full final 2015 journal body and unacquired lectures were not checked. A bounded scope/priority review is a separate gate.

The main contribution, if the scope gate agrees, is the derivation of **full ambient** reversal from **measure-only Markov** tests, especially the period treatment without disintegration or measurable Haar selection. It should not be described as establishing the older Palm equivalences or solving every Cox/allocation question. No follow-up conjecture is recommended by this analytic review.

## Independence and exposure

The paper was fully read, the argument independently reconstructed, and fresh controls completed before the supplied replay. A provisional analytic conclusion was recorded at 75% before receiving any sibling mathematical findings. Coordination with the scope agent concerned raw primary-source paths/hashes only. No current sibling report/code or dedicated historical priority/review verdict body was read.

The manuscript itself contains historical literature-search and AI-assistance statements. The necessary authored `CLAIM_SCOPE.md` includes ancillary Cox-claim withdrawals and prior verification status; the checker source contains expected historical output counts. These incidental exposures are disclosed and were not used as evidence that the present theorem is correct. The file named `verification/independent_review/independent_check.py` was read as executable mathematical support, not as an opinion report.

No original sources, website, spreadsheet, Git state or public record were changed. No external person was contacted. The review's conclusion is bounded to this exact edition, argument, primary interfaces and recorded checks.
