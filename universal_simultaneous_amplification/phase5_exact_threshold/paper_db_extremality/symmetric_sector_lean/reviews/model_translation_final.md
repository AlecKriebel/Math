# Independent final model-to-statement review

UTC: 2026-09-14T14:59:02.262779+00:00

**Finding: the Stage 3 principal identity matches the manuscript's genuine active-chain quadratic expression. No translation error or unsupported mathematical assumption was found.** An independent compilation of `PhysicalIdentity.lean` succeeded. A separate query records the exact statements and transitive axioms of 18 model/bridge results in `reports/model_translation_axioms.log`; the final aggregate clean-build audit remains a separate check.

## Independence and inspected sources

This reviewer did not author the stochastic-model, stationary-current, orbit-moment, physical-inverse, coefficient-feature, reward, or physical-identity modules reviewed here. The review began from Sections 3–4 and Appendix A of the manuscript and compared the definitions and theorem statements directly, treating the manuscript and verifiers as claims. The reviewer previously authored `BlockActions.lean` and `Contraction.lean`; those helper modules were independently reviewed by `finite_audit` (see the corresponding independent review reports). This disclosure matters because the physical coefficient-action proof imports the checked generic selector helpers.

Inspected source hashes are listed below. Local sources were not modified as part of this review.

## Principal statement audit

The theorem is:

```lean
SymmetricSector.Active.R2_eq_frobeniusSq_mul_reducedScalar
  {n : ℕ} (hn : 4 ≤ n)
  {δ : Matrix (Fin n) (Fin n) ℝ} (hδ : SymmetricBalanced δ) :
  R2 δ = frobeniusSq δ * (reducedScalar (n - 1) : ℝ)
```

`SymmetricBalanced` requires zero diagonal, symmetry, and zero row sums; zero column sums are separately deduced from symmetry. The perturbation entries are arbitrary real numbers, not restricted to rational matrices or a finite set of examples. `frobeniusSq` is the sum of the squares of all ordered matrix entries, exactly the squared Frobenius norm used in the paper. The identity includes the zero perturbation and does not divide by its norm. The population domain `n≥4` is exactly the scalar domain `N=n−1≥3`.

The theorem has no positivity premise, no prescribed value for the scalar, no assumed feature representation or moment identity, and no assumed invertibility of either matrix. `R2` is defined independently from the scalar by the actual nested expression `ν₀ Δ G Δ G q`. It is the coefficient denoted R^(2) in (4.6), so no factor of two for a second derivative is silently inserted or omitted.

## Orientation, sampling, and normalizations

* `State n` consists of a nonempty cache B and a target v outside B. The intermediate `sampled` constructor also accepts an empty pre-sampling cache, which is needed after stopping a singleton. It inserts a sampled source distinct from the current target and always produces a valid nonempty active state.
* `kernel P y z` has the manuscript's two moves with source state in the row and destination state in the column. Continue has weight 1/2 and samples from row P_v. Stop has weight 1/(2|B|), chooses w in B, erases w, then samples from row P_w. Thus row laws act on the right and column observables are acted on by `mulVec`. `kernel_affine` proves that `perturbation δ = kernel δ` is the exact affine variation at the complete kernel.
* `complete n` has zero diagonal and off-diagonal value 1/(n−1). Its row sums and denominator positivity are proved on n≥2. The retarget denominator is positive because the active cache is nonempty.
* `nu0(B,v)=|B|/[n(n−1)2^(n−2)]`, equal to (3.17) under N=n−1. Its normalization is proved by double-counting subset memberships, and its stationarity is proved by actual incoming-transition enumeration.
* `q=H−center`, H=1/|B|, and `center=Σν₀H`. The theorem `center_eq_c₀` identifies this actual mean with the printed constant using a concrete rank Poisson equation and the independently proved stationarity and normalization. `green` is precisely the inverse of `I−K0+1ν0`, with the stationary row repeated in every matrix row, not its transpose.

## Invertibility and the two Green applications

`ActiveInverse` supplies all physical inverse assumptions. The chain is nonnegative and stochastic; ν₀ is strictly positive, normalized, and stationary. The stationary energy sum of any harmonic function vanishes, forcing equality across every positive transition. Concrete continue moves fill a cache, and a concrete stop move connects any two different full-cache targets. Therefore every harmonic function is constant. The centered matrix has trivial kernel and is invertible. No reversibility, irreducibility axiom, spectral assumption, or numerical inverse is imported.

The actual rank action has upward rate (N−k)/(2N) and downward rate (k−1)/(2N). `Gradients.gradient_terminal` proves the upper boundary equation from the actual recurrence and binomial normalization. `rankPotential_poisson` therefore covers all physical ranks, not merely the interior. Subtracting the proved stationary mean identifies the first actual Green response. Applying the perturbation kills the additive constant and gives the A.15 source with positive signs `d_k x/2 + d_(k−1) z/(2k)`.

`ChannelFeatures` defines the real feature associated to an actual rational channel vector by zero extension. It proves the coefficient action in the physical direction and the intertwining `K0 F(c)=F(coefficientK c)` directly. `coefficientK` is the operator whose transpose is the printed block matrix H. The inverse-defined coefficient solution is proved to solve `(I−coefficientK)c=source` using the previously proved coefficient invertibility. Transporting this equation through the intertwining yields the actual second Poisson equation. The feature has zero ν₀-mean, proved using actual fixed-rank subset sums. The final `green_perturbation_green_q` theorem consequently identifies the second true Green response with this feature, using the actual centered inverse's uniqueness.

## Feature degeneracies and endpoints

This addresses the main danger identified in the earlier model review: the features are not assumed to form an independent basis. At rank one, z=0 is proved. At full rank N, both x and z vanish. `K0_coefficientFeature` uses these identities to handle absent coordinates. At rank N−1 the features are linearly dependent; the proof never infers coefficient equality from function equality and therefore remains valid there, including N=3. Good coefficients are exactly ranks 1,…,N−1 and bad coefficients exactly 2,…,N−1. Empty cache terms enter reindexed sums only after their contribution is proved zero.

The separate theorem `symmetricBalanced_three_eq_zero` proves every admissible 3×3 perturbation vanishes, and `R2_symmetricBalanced_three` proves its genuine active quadratic expression is zero. This is correctly separated from the positive scalar range. In particular S_3 corresponds to n=4, not n=3.

## Actual current, orbit counts, and reward

`Incoming` enumerates actual predecessors. Its continue contributions have rank factors k and k−1; its stop contributions have old-target counts N−k and N−k+1 after cancellation of the rank/retarget factors. Their sum gives the labeled current `(ν₀Δ)(B,v)=x(B,v)/[n2^(N−1)]`, including the physical boundaries. The stronger general incoming-kernel identity is linear in an arbitrary P, and its specialization is the signed derivative used here.

`OrbitMoments` counts actual subsets containing prescribed distinct labels by a proved bijection, with explicit zero for k below the number of prescribed labels. The x² expansion has diagonal sum R_v and off-diagonal sum −R_v. For xz, the two coincidence sums total −2R_v and the all-distinct sum is +2R_v. Consequently the mixed coefficient has the negative sign in A.17a. `target_orbit_current` and `nu0_perturbation_feature_orbits` use these counted sums and sum the actual row norms to the full Frobenius square.

`Reward` proves the Pascal simplifications and finite support endpoints, yielding the exact A.16 rewards: good coefficient binom(N−2,k−1)/[2^(N−1)(N+1)] and bad coefficient −binom(N−3,k−2)/[2^(N−2)(N+1)]. The factor of two in the mixed orbit moment is absorbed into the bad denominator. `nu0_perturbation_coeff_feature` proves the full actual-current pairing with these rewards for arbitrary rational coefficient vectors. Combining it with the second Green identification proves the principal A.17 identity without a scalar fit or finite-population extrapolation.

## Trust receipt and exact remaining scope

The inspected bridge path uses ordinary kernel proofs and printed transitive dependencies limited to `propext`, `Classical.choice`, and `Quot.sound`. No project-specific axiom or compiler-trust computation is used. Source and transitive axiom checks do not substitute for the statement comparison above. A final coordinated clean build and complete principal target list should be checked before promotion. During this receipt run, the audit runner's formatting option `pp.width` was found invalid for Lean 4.19 and corrected to `format.width`. The initial query exited unsuccessfully; the corrected model, block-action, and contraction receipts were rerun and all exited successfully. This was an audit-orchestration defect, not a mathematical proof gap.

Stage 3's scalar-to-physical identity has no remaining mathematical or formal translation gap in this checkpoint. All-order positivity of the scalar is a separate result to be composed with this identity; this review does not infer it from the identity alone. Coverage/collision representation as fixation, analytic stationary perturbation and its fixation interpretation, tangent-space decomposition, the other two sectors, and the full local-optimality theorem are outside this audited component. No global conjecture, uniform-in-n neighborhood, or biological applicability claim follows from this review.

## Inspected source SHA-256

- `Active.lean`: `9de104e21e3a29354159ffd516fe5ac57f94de1dc88c5112120df2364280a34c`
- `MarkovInverse.lean`: `9543c0d92a731fd1bc537a0739d45bab59dc02d3e216f9d9a6599b64dab7baed`
- `ActiveInverse.lean`: `bbb7372556811221eea8ea0e5606ee3a422117764834f36eedf00394f7ddc5bf`
- `Gradients.lean`: `1cd6d3cd36c6a0e3fdcafc22e4e9d4f9e16f2e788f1b0819b4d17cf5af364949`
- `PhysicalBridge.lean`: `65af210785624be46ac1d8975d49a54d02f5616b09111d8ed7f535785109280e`
- `ChannelFeatures.lean`: `85f8be8bb6b61867719bf89b693f122cad97760b4ac3bf3a73948dfa7236ec78`
- `OrbitMoments.lean`: `0e954625e0ee3863a621014376490c7bd66926bea69d6763c0e77105953c7129`
- `Incoming.lean`: `e696d2ef2c2fbfe1a594ea20a282227cb67467b5f248523dcd6c1178876b0955`
- `Reward.lean`: `53b90968f8eca3524b785141999b8c5ed947f23fd40c97bb381d3c7ab1bb9755`
- `PhysicalIdentity.lean`: `4be4a2779cdb708760533a802e226c40223862d07e7fbf9b939da9386758d3f6`
