# Family 090 actual Lean source audit

Checkpoint: 2026-10-06 21:16:38 America/Los_Angeles (2026-10-07 04:16:38 UTC). Upstream was read only at commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

## Verdict and exact checked strength

The actual declaration `OAI.AtomicTriangular.universal_energy_minimum` is in `lean/OAI/Analysis/Triangular/Energy/Universal.lean`. Its definitions and explicit hypotheses match the intended infinite-configuration input: locally finite planar sets, centered-disk density one, every nonnegative smooth completely monotone function of positive squared distance, ENNReal-valued lower ordered-pair disk energy via `Filter.liminf atTop`, and the covolume-one triangular-lattice full nonzero-site series. No semantic weakening or circular assumption was detected in the core proof modules inspected.

This is **not a successful formal build or axiom audit**. The exact theorem import closure was copied and searched, and crucial definitions and transfer mechanisms read. Compatible Mathlib binaries are absent; exact compiler attempts fail before checking any OAI theorem. Therefore neither this follow-on nor the upstream theorem was independently kernel-verified in this effort. The Comparator JSON's permitted axiom set is configuration data, not a completed test result. Endpoint order and absence of lexical `sorry` are partial checks only.

## Exact declaration and semantics

```lean
theorem universal_energy_minimum (g : ℝ → ℝ) (C : Set Plane)
    (hg : AdmissiblePotential g) (_hC : LocallyFinite C) (hd : DensityOne C) :
    latticeEnergy g ≤ energy g C ∧ latticeEnergy g = energy g A
```

`Plane := EuclideanSpace ℝ (Fin 2)`. `LocallyFinite C` requires each intersection with `closedBall 0 R` finite, for all real R. `diskPoints` is that intersection's finset (empty if not finite), and `diskCount` its cardinality. `DensityOne` is convergence of `diskCount(C,R)/(πR²)` to 1 over real R→∞. It is centered-disk density; it is not a translate infimum, Banach density, separation condition, or special local count estimate.

`diskEnergy` is `(diskCount:ENNReal)⁻¹` times the finset sum over all x and all y in `diskPoints.erase x` of `ofReal(g(‖x−y‖²))`. Hence there are no self pairs and every unordered pair occurs twice. `energy` is its ENNReal `liminf`, not an assumed limit. Empty disks have energy zero; density one gives eventual positive cardinality.

`AdmissiblePotential` requires `ContDiffOn ℝ ⊤ g (Ioi 0)`, `g(t)≥0` for t>0, and `(-1)^r iteratedDeriv r g(t)≥0` for every natural r and t>0. It imposes no boundedness, integrability, decay, or finite-series assumption on g. Values at t≤0 do not enter the energy; each sampled squared distance is strictly positive. Derivatives at positive t are local.

`AtomicTriangular.triangularPoint(j,k)=(sqrt b)⁻¹•(j+k/2,kb)` with b=√3/2, so its basis determinant is b/(sqrt b)²=1. The supporting namespace uses the equal scale `sqrt(2/√3)`. `triangularPoint_eq_support` and `A_eq_support` identify the two definitions. `Mixtures.lean` explicitly proves `triangular_det=1`, `triangular_covolume=1`, the Euclidean disk-count asymptotic, and `triangular_densityOne`. No density-one redefinition substitutes for covolume.

The final theorem's `_hC` argument is unused. This is benign: if one centered disk were infinite, all larger intersections would be infinite, `diskPoints` would vanish there, and density one would be impossible. The explicit density hypothesis already entails the needed finite disk points. No hidden spacing or local-count premise is inserted.

## Actual proof route inspected

| Mechanism | Real modules/declarations | Evidence and exact gap |
|---|---|---|
| Density-only Fourier bound | `Energy/Spectral.lean`, `Cutoff.lean`, `Density.lean`: `kernelForm_spectral`, `kernelForm_comparison`, `finite_disk_energy_lp`, `density_lp` | Finite positive measures plus Fourier inversion/Fubini yield the quadratic comparison. LPFunction assumes continuity, f/Fourier integrability, first-moment integrability, and a global bound. A radial 1/T-Lipschitz cutoff equals one on the competitor disk. Error per particle is bounded using firstMoment/(εR); the volume/cardinality ratio tends to (1+ε)², then ε→0. This source argument does not use separation. No kernel build reproduced. |
| Actual Gaussian pair | `Schwartz/GaussianPair.lean`: `largeGaussianPair`, `reciprocalGaussianPair`, `gaussianPair`, `sharp_gaussian_minorants`; `Construction/Normalization.lean` | α≥1 uses actual constructed Schwartz functions with Fourier duality, minorance, positivity, and interpolation. α<1 uses the reciprocal α⁻¹ pair and Gaussian Fourier identity. GaussianPair is constructed, not supplied as an unproved input hypothesis. Deeper enclosure and analytic modules remain uncompiled. |
| Construction and interpolation | `Construction/ConcreteSchur.lean`, `ActualCorrection.lean`, `ActualInput.lean`, `ActualTail.lean`, `ActualInterpolation.lean` | Finite inverse bounds 17 and 5, B-operator bound 340, and A/C/D envelopes imply `splitQ<1`; a Neumann solution supplies the correction and finite/tail equations. Tail coefficients belong to ℓ¹ and carry summability. Actual interpolation is derived at every node, including first derivatives. This is a concrete mechanism, not universal optimality restated as an axiom. Underlying analytic envelope/enclosure claims have not all been individually rechecked. |
| Global signs | `Signs/OrdinaryComparison.lean`, `NearSigns.lean`, `FarSigns.lean`, `Construction/Normalization.lean` | Near [0,29/2], middle [29/2,23], and later ≥23 regions cover every radial parameter ≥0. Deleted-second-derivative estimates plus node jets imply the signs; the exceptional near cell is handled separately. Representative literal certificate and interval transfer modules were inspected, not every generated table proof. |
| Lattice normalization | `Energy/PairPoisson.lean`, `GaussianPoisson.lean`, `Gaussian.lean`: `GaussianPair.sharp_value`, `energy_bound`, `gaussian_energy_bound` | Summability is explicitly available before each tsum transfer/subtraction. Actual-pair Poisson gives latticeEnergy(gaussPot α)=ofReal(p.second(0)−p.first(0)); the density LP theorem yields the lower bound. Deeper spectral atom/theta identities are uncompiled. |
| Mixture/Fatou assembly | `Energy/Mixtures.lean`, `Potentials.lean`: `CM.shifted_mixture`, `shifted_mixture_energy`, `mixture_energy_lower`, `latticeEnergy_shift_iSup`, `universal_from_gaussian_bounds` | Positive shifts ε yield finite positive measures on I=[0,1] and g(ε+t)=∫v^t. Endpoint v=0 contributes zero at positive distance; v=1 is the constant potential with infinite competitor energy. Tonelli over a countable lattice and Fatou over the exact real-radius liminf allow infinite energy. Finite partial sums/continuity remove the shift. The lengthy mixture construction was read principally at its final assembly, not completely rederived or compiled. |
| Lattice attainment | `Energy/Mixtures.lean`: `lattice_energy_upper`, `lattice_energy_lower`, `lattice_energy_eq` | Upper bound is row inclusion in the full nonnegative lattice sum. Lower bound fixes finitely many nonzero displacements of norm ≤M, retains centers in R−M, uses interior-count ratio→1, then takes the supremum over finite sets. The proof covers divergent series. Imported Mathlib lattice counting has not been kernel-reproduced. |

The final theorem invokes `gaussian_energy_bound` for every α>0, then `universal_from_gaussian_bounds`, and transports the exact lattice definitions. It does not assume universal optimality or a Riesz constant.

## Pinned artifacts, versions, and hashes

`reproducibility/formal/source-manifest.json` records SHA256 and size for all 227 reachable OAI modules (8,590,367 bytes). Their exact copies and unchanged mathematical imports are under `reproducibility/formal/pinned`. The original lakefile, manifest, toolchain, README and Apache-2.0 LICENSE are also retained. The only external import family is Mathlib (including six specifically imported analytic/tactic modules).

Selected SHA256:

- `Energy/Universal.lean`: `35765ec2deda6020ae292681a4f56c6d73dfbcbdfbb7baa831e06e52dec82b1d`
- `lean/docs/090.md`: `d349dc455d0c4c6621153f61ca639dd4932f0bbcb8fc5508e2a1805b95f6de26`
- Comparator challenge: `af51979c7baecd3e9852637bbba29eff96cbb09cec84e15eff7d686f1a770616`
- Comparator JSON: `d906406365fb6c3f10692db01c9cda3b0215a011eab39d25ac9dd586bbead6d5`
- Original manifest: `cf6105a25d9dca2f166b241d9191bd12c7e13305890dc9c4d0952351cccc0794`
- Toolchain file: `d5edba4e4b8faad9c1baeadb265716d20d03be4d1a2647dc5e35b0c0325bea7b`

Mathlib pin: `d13f23b723b8a846827a245b89c10fc7d3f11612`. Lean: `leanprover/lean4:v4.34.1`, available compiler identifies arm64-apple-darwin24.6.0, commit `5045d0056413266e57c625dcd7c365b10e377c52`, Release. Lake: `5.0.0-src+5045d00`.

## Reproduced checks and build limitation

Run `python3 audit_sources.py` from `reproducibility/formal`. Receipt is `source-audit-results.json`. The script verifies all copied-source hashes, exact import reachability, absence of an OAI import cycle, and a lexical search for `sorry`, `axiom`, `admit`, `unsafe`, `native_decide`, `run_tac` (zero matches). Such a scan is not a kernel axiom audit. Certificate proofs visibly use `decide +kernel`, but those calculations have not been executed here. All 66,587 literal integer endpoint pairs are ordered lower≤upper; this checks only their well-formedness, not enclosure correctness or global signs.

With LEAN_PATH set to the isolated pinned copy:

1. `lean --version`: success, pinned version above.
2. `lean --root=. OAI/Analysis/Triangular/Energy/Basic.lean`: exit 1, unknown prefix Mathlib.
3. `lean --root=. OAI/Analysis/Triangular/Energy/Universal.lean`: exit 1, imported Gaussian.olean does not exist.

No OAI theorem was elaborated or compiled. There is no successful Comparator run or printed transitive axiom result. Comparator `TriangularEnergy.lean` intentionally contains `sorry`; its JSON points to the real solution and permits only propext, Quot.sound, Classical.choice, with enable_nanoda=false. This configuration does not itself establish success.

Compatible Mathlib was absent; existing v4.19 caches lack the current pinned commit and are incompatible with v4.34.1. The shared volume initially had only 1.7–1.8 GiB free, then briefly became completely full during concurrent research, so root prohibited further build/download growth. No dependencies were downloaded by this task. During the zero-space incident, exactly the 227 hash-matching owned copied sources were temporarily unlinked after retaining manifests/receipts; they were restored byte-for-byte when root reported recovery to 395 MiB. No unrelated files or shared caches/toolchains were removed or modified. No source clone, shared git index, branch, or commit was changed.

A future full formal check requires the exact pinned dependencies in the isolated copy, a build of `OAI.Analysis.Triangular.Energy.Universal`, the configured Comparator, and explicit transitive-axiom inspection/semantic comparison. The current record does not justify claiming completed formal verification. It also does not formalize g(t)=t^(−s/2), periodization, finite minimal energy, Hardin–Saff, or the surface theorem; those need separate handwritten follow-on proofs and dependency checks.
