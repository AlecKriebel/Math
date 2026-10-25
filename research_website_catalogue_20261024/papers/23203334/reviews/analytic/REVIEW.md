# Analytic review — Zenodo 23203334

**Verdict: no substantive mathematical defect identified in the stated finite-species extension.** The published global conclusion is supported by the inspected analytic chain, including its dependence on the pinned OpenAI one-species manuscript. This is an ordinary mathematical review, not a formal certificate or independent external human peer review. The independence limitation described below must accompany this verdict.

## Identity, coverage, and independence limitation

The reviewed paper is *Signed impulse estimates and global smooth solutions for finite multispecies relativistic Vlasov–Maxwell*, dated 6 October 2026. Its published ten-page PDF has SHA256 `8cfaa828abfe5f91626527a79679c503bb37cb081fb258de68ef7f776a74e046`; the source archive has SHA256 `6b90c4116ba596ee56567be0d540c1866e5f4fdf18bd62f13c489c6ca996849e`; main TeX has SHA256 `9d72d239677c1066ba22ffbea8ff36f26251a2eae532921bd5e8e12b5f9fdb8c`.

All ten published pages, the complete main TeX, all five mathematical supplements, and all three submitted algebra checkers were read. A fresh standalone source build succeeds, with exact extracted-text equality on all ten corresponding PDF pages. The PDF binaries differ; the rebuilt hash is `b7aeaebdf5e0812aaa83538755cfd3bc5568a3fd251aba018ad6c2130b3ef504`.

All ten pinned upstream section files were freshly acquired from the connected GitHub primary source and match the published manifest hashes. Nine were read in full: setup, retarded, occupation, direct, cancellation, direction, selection, closure, and continuation. The introduction was acquired and hash-checked but was not required as a proof dependency. The 49-page upstream PDF acquired separately by the scope reviewer matches the pinned PDF hash. Only primary-source files and acquisition receipts were used from that review directory, never its opinions. The exact Luk–Strain continuation statement and Bouchut–Golse–Pallard division-lemma/derivative interfaces were checked directly.

The supplied mathematical support is not a blind source: `SUPPLEMENT_OCCUPATION_AUDIT.md` contains historical audit status and favorable conditional assessments alongside its derivations. Reading it as required mathematical support exposed those paragraphs before my final conclusion. This was disclosed to the parent immediately. Other supplements also describe their historical partial status. Those assessments were not used as evidence; the underlying inequalities were reconstructed from the primary sources. No separate historical, archived, or current sibling review body was opened. The independent reconstruction's conclusion was frozen in `independent_conclusion.json` before report completion. It would be inaccurate to call this review wholly blind to historical assessments.

## Exact claim and model boundary

Theorem 1.1 concerns three spatial and three momentum dimensions in flat space, with the classical collisionless relativistic Vlasov–Maxwell equations in rationalized units. The species list is fixed and finite, every mass is strictly positive, and charges are arbitrary real numbers. Number densities are nonnegative and initially smooth with compact phase-space support. Initial electromagnetic fields and every spatial derivative are bounded, the fields themselves are square integrable, and the two Gauss constraints hold. There is no background charge, smallness, symmetry, or neutrality hypothesis.

The conclusion is unique global classical existence, smoothness on each finite slab, compact particle phase support there, and persistence of the constraints. A uniform momentum-support bound is the continuation criterion. Constants may depend on the entire fixed species list, data, and a prescribed finite horizon. No uniform massless limit, infinite-species limit, noncompact momentum tail theorem, lower-dimensional analogue, collisions, curved spacetime, or arbitrary smooth finite-energy field class is established.

The physical equations are model assumptions. Normalization, energy, bounds and continuation are mathematical deductions from that model. The one-species signed-impulse mechanism is explicitly inherited from the pinned OpenAI manuscript. The present contribution is the finite-species transfer with the shared field and signed coefficients, particularly distinct charge-to-mass ratios. The paper does not claim an independent discovery of the underlying one-species global mechanism.

## Reconstruction of the force and energy — pages 1–4

For physical momentum `p=m_a v`, the Jacobian is `m_a^3`; defining `f_a=m_a^3 F_a(x,m_a v)` preserves number measure. The normalized velocity is the common `u=v/sqrt(1+|v|^2)`, but the acceleration coefficient is `lambda_a=e_a/m_a`. Maxwell sources retain `e_a`, not `lambda_a`. In particular, the pair coefficient is `c_ab=lambda_a e_b=e_a e_b/m_a`; the source-field derivative terms have the additional `lambda_b`. The manuscript preserves these distinctions.

Each species' phase vector field has zero divergence because `u` is a momentum gradient. Its flow preserves volume, positivity and its own density bound. The continuity equation propagates the Gauss constraints. The kinetic work from mass-weighted energy is `m_a lambda_a u·E=e_a u·E`, so the signed species work cancels the Maxwell work. Both the energy and cone-particle budgets are positive, including for opposite charges. Direct expansion confirms the field cone flux

`(|E|^2+|B|^2)/2 - n·(E×B) = (|E+n×B|^2+|n·B|^2)/2`.

Spatial cutoffs are legitimate with fields continuous into `L^2` and compact particle support on the chosen prefix. They are not being used to infer a momentum-support bound from energy alone. The aggregate `sum f_b` is used only for nonnegative Eulerian estimates; arguments involving trajectories take place on the disjoint union of the individual species label spaces. It need not solve a scalar Vlasov equation.

I checked the retarded Jacobians directly. The inverse flow derivative acquires a rank-one perturbation with determinant `1-n·u_b=d`; differentiating the source/receiver retarded equation gives `dt/ds=d/D`. Combining the two yields the stated measure conversion. Timelike curves give unique branches. The union-bound collision argument costs `O(zeta^-1)` grid points times `O(zeta^3)` phase mass at each point, so the exceptional labels have zero mass. It does not require a lower distance bound uniform in labels.

Maxwell source linearity gives each source's factor `e_b`, and applying the receiver Lorentz map adds `lambda_a`. The potential differentiation and initial-cone terms in the pinned primary source were checked rather than inferred merely from the one-species theorem. The complete signed identity contains both the acceleration kernel and transport kernel. Differentiating `k_0/(r d)` and using the retarded geometry cancels the arbitrary source acceleration; the receiver term contains the full `K_a` through `a_t=(Id-a⊗a)K_a/q_X`. No equality of species accelerations, inverse charge, or extra receiver factor is required.

The source majorants follow by resolving the Lorentz force into components normal and tangent to the cone. The electric acceleration numerator is tangent to `n`, and the receiver Lorentz map has an additional small factor after projection perpendicular to the receiver momentum. These give exactly the stated good-field and magnetic remainders. Selected cutoff derivatives are canceled only after factoring out the common physical coefficient within one pair. The positive source sum is taken afterward.

For fixed classical prefixes the cone divisors are bounded below and compact acceleration bounds justify integrations by parts and dominated limits. They do not enter the uniform estimates. A tip cutoff costs an integral proportional to its radius in three dimensions, and the initial-cone primitive is bounded using the initial momentum support and `D k_0=D u_b-eta n`. Thus the boundary terms do not conceal a momentum-dependent final constant.

## Reconstruction of the a priori estimate — pages 5–8

### Occupation and direct bounds

The bootstrap is simultaneous over all supported labels of all species, every eligible receiver dyad, and every interval staying in its energy range. `P` bounds the entire collection on the fixed compact prefix. This licenses both source and receiver stopping arguments, even for opposite force signs.

At a fixed source time, the spatial map from receiver time and cone direction is injective with Jacobian `r^2 D`. The conserved energy gives `M_hit <= C max(I,h)/p`; the retarded time change and conserved number give `M_hit <= C I phi^2/theta^2`. Velocity-shell caps give the density `Cp^3 nu^2`. All these statements transfer separately to each component and sum with fixed constants.

The stability length follows from the two bootstrap terms before a first energy exit. Each momentum increment is a small multiple of `m omega`; integrating the derivative of `u` on the segment gives a small `omega` velocity increment. In actual bins a fixed projection of relative velocity stays bounded below. Equal-time separation at hits is at most `C h(phi+omega)`, so a monotone crossing has duration at most `C h k_1`, even for a disconnected hit set. The common-cell positive energy gives mass `C/p`. Deficit bins, where actual relative separation cannot be used, are kept separate and have `ell <= CP^-2`.

The refined energy budget is shared over `p,phi` and independent of source angle and radius. The two indicator families have bounded overlap; the second has a unique retarded time. Full cells use averaging, clipped cells use their direct mass bound, and `ell<h<=I` uses the spatial map. These distinctions are needed to avoid an extra angular logarithm and are present in both the primary proof and transfer.

I reconstructed the direct near/far table using Cauchy–Schwarz with the cone `G^2` budget and the spatial `B^2` budget, after aggregating positive densities. Substitution of occupation produces the stated radial balances. In the narrow sector the transport sum reduces to `sqrt(I) R p phi`; its parameter part uses Cauchy–Schwarz over the joint budget, rather than separately spending an energy bound on every angle. The remaining-sector split at comparable angles, the large-radius magnetic bound, and the direct treatment of the deficit exception all have the required summable exponents. This yields the baseline bound and the full absolute-force bound with the extra `sqrt(w)` factor. Fixed species factors multiply constants without changing these summations.

### Direction count, improved occupation and selection

The direction-count proof first uses only baseline occupation and the projected identity. Complete direction exits have a minimum duration from the signed bootstrap. Endpoint ramps retain a fixed fraction of their signed direction change. Their bulk terms are estimated over disjoint intervals with a single total-length budget; only time-weight derivatives acquire the exit count. The moving projector is differentiated explicitly. Its coefficient and the receiver coefficient sum to `CL^2/w`, while time weights cost `CL^2` per exit. Thus the large factor `w delta` absorbs the latter, proving the direction count without using improved occupation. I found no circular use of that later estimate.

Improved occupation uses separate source and receiver direction partitions. Their common refinement costs their sum, not their product. Bad hits lie within source time `O(h)` of a receiver direction boundary, independently of the possibly large retarded time derivative. At good hits equal-time separation is `O(h phi)`, and relative velocity has a fixed `Omega(phi)` projection throughout a common direction cell. Energy controls the label mass on the larger energy-stable cell. In the specified intermediate-angle window the positive power `P^(56/3125)` absorbs `C(M,A) log(2+P)^7`. The resulting prefactor is independent of bootstrap parameters only after a threshold depending on them; the proof maintains that order.

The selection uses pure representative quantities with all density and charge constants outside them. Its weights are summable. A selected bin allegedly failing `U<=w^-1/2 W` is forced first into actual separation and then into the improved-occupation window by the energy-far, stable-cell-far and unsafe inequalities. The final contradiction can be seen without the paper's rounded constants. Writing `delta=Delta/z<4/99995`, its exact final inequalities imply

`187 H < 74 z + 974 Delta - 348 alpha - 600 min(alpha,c)`

and the earlier inequality gives

`H > z/2 + 3(alpha+c) - 4 Delta`.

Together these would require

`(39/2) z + 909 alpha + 561 c + 600 min(alpha,c) < 1722 Delta`.

All extra terms are nonnegative, whereas `39/2 - 1722*(4/99995)=555147/28570>0`. This is an independent exact separating inequality. The arithmetic alone cannot supply improved occupation: a rational negative control retained in the evidence satisfies the earlier-stage inequalities and is excluded specifically by the improved far bound.

Selected receiver coefficients therefore sum to `Cw^-1/2`, canceling the loss in the direct absolute-force estimate. The source cutoff errors transfer to unselected neighboring supports within a fixed pair. For the spatial transition, the crossing radius makes the two costs have product `I R^2 p^2 phi^2`; this is independent of source angle. The two resulting geometric angular tails converge with no extra logarithm. The time-weight estimates separate `h<=I` and `h>I`; the latter uses both selection inequalities and has positive residual exponents. The central term and exceptional deficit scales are covered by their own balances. These steps establish the weighted signed estimate with constants independent of `M,A`.

### Closure and finite-time exclusion

Restoring endpoint ramps uses signed momentum increments, not absolute-force integrals. Choose the ramp fraction, then `M`, then `A`, then the large-`P` threshold; the improvement is uniform across the finite species list. On a fixed prefix the temporary bounded force supplies only right-openness of the bootstrap set. It is absent from the final constants. Closedness follows by truncation of eligible intervals. There is therefore no assumption of the desired estimate at a maximal endpoint.

For finite-time blowup, first dyadic hits of the maximum over all species labels exist and attain their maxima by compactness. A maximizing label's last half-energy time is no earlier than the preceding joint first hit, even if the maximizing species changes. The signed increment bound forces a time gap bounded below by `c/log(2+1024*2^n)`. These gaps cannot sum to a finite time. This is conditional on the already independently checked continuation criterion, not a replacement for it.

## Continuation and regularity — pages 8–9

[Luk–Strain, arXiv v1](https://arxiv.org/pdf/1406.0165v1), Theorem 1.1 and its footnote, use compact nonnegative `H^5` particle data and `H^5` fields satisfying the constraints; they do not require a separate momentum bound for approximation iterates. Remark 1.2 explicitly permits multispecies adaptation. The source uses a `4pi` density convention, accounted for by density rescaling. I do not infer the larger field class solely from that theorem.

[Bouchut–Golse–Pallard](https://arxiv.org/pdf/math/0301175), Lemma 3.1, provides the streaming division identities with bounded coefficients when velocities stay strictly below light speed, and a zero angular residue for the last second-derivative kernel. Its Sections 4–5 give the logarithmic derivative mechanism. The literal compact-field theorem would not supply the nonneutral data class here; the paper instead uses its underlying estimates and explicit localization. This distinction is correct.

At bounded momentum radius all coefficient derivatives are controlled. Applying the division identities specieswise introduces only fixed `e_b`, `lambda_b`, and their products. The first moment-derivative inequality bounds the field. For the second, the zero-residue term is split at `min(t,(1+N(t))^-1)`: subtracting the value at the cone center controls the short part by the gradient times the splitting length, and the remaining radial integral is logarithmic. Gronwall gives the field's `W^{1,infinity}` norm bounded by `C[1+log(2+N)]`. Differentiated species transport then obeys the Osgood inequality with divergent comparison integral. The coefficients are uniform on the hypothetical finite interval of bounded momentum.

The local `H^6` iteration and tame commutator estimate retain only first derivatives in the coefficient. The current is bounded by the finite velocity-ball volume times the sum of density Sobolev norms. The same lifespan controls higher norms; restarting before an alleged loss proves persistence. Classical uniqueness uses one Maxwell difference energy and the sum of species transport difference energies. Field derivatives need not be globally square integrable for this energy argument because spatial-cutoff errors tend to zero.

For general stated fields, the signed compact charge density has Coulomb field `-grad(-Delta)^-1 rho_0` in every `H^k`: the Fourier singularity is `|xi|^-1`, square integrable near zero in three dimensions even with nonzero total charge. For a solenoidal field `G`, the potential `(integral_0^1 tG(tx)dt)×x` has curl `G` with the stated positive sign. Cutting off this potential preserves divergence. The removed divergence-free field evolves as a vacuum Maxwell solution and vanishes throughout the particle region for any fixed chosen horizon. Addition/subtraction is an exact equivalence there, so it transfers both local theory and bounded-momentum continuation. Bounded smooth derivatives supply the vacuum regularity; they are not silently replaced by an `H^k` assumption.

## Reproduction, controls and remaining scope

All three submitted checkers pass with Python assertions enabled. They certify polynomial identities, 292 supplementary exact rational kernel cases, and exponent arithmetic; they do not certify the PDE estimates. The fresh standalone checker imports no submitted module and passes **425 explicit exact conditions**. Its mechanisms include:

* The initial Maxwell trace: angular integrals of the boundary and interior velocity kernels have canceling logarithmic coefficients and sum to `-4pi u`, supplying the initial `-j` derivative. Omitting the boundary is detected. The zero-velocity case is handled by odd spherical symmetry.
* Positive cone flux with rational unit normals in varying orientations; mass, charge and common-ratio normalization, including neutral and opposite-charge cases.
* The exact separating inequality above and an earlier-stage negative witness; closure parameters for exterior constants ranging from `1/100` to `10^12`.
* The three-dimensional nonneutral Coulomb integrability boundary and cone-tip cutoff scaling.

The checks are corroborative. The main evidence for the nonlinear occupation and regularity claims is the reconstructed proof, not those finite computations. No Lean build or formal-certification claim is made. The primary dependency is pinned to commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`; [the primary repository version](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a) and file-specific URLs/hashes are recorded in `upstream_acquisition.json`.

The strongest verified claim is Theorem 1.1 in its exact stated class, with the inspected pinned analytic inputs and finite-species adaptation. No central unsupported estimate, circular bootstrap or mismatched continuation hypothesis was identified. This review does not independently certify exhaustive novelty, the older book/nearly-neutral priority comparison, all upstream formalization, or a later uninspected version. Those are limits of this review, not proof defects. The embedded historical-assessment exposure limits reviewer blindness and must not be omitted in promotion decisions.

Completion: **100% of this assigned analytic review**. No source repair, website, spreadsheet, Git, Zenodo, publication or outreach action was performed.
