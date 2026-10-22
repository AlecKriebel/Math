# Five-turn outcome: adaptive hybrid finite elements, 30003216

**Original source target: unsolved, 5/5 substantive author turns. Independent review pending. No novelty claim.**

The exact OWR42/2016, printed p2422 target is adaptive convergence for the Ku–Lee–Sheen coarse-primary/fine-H(div)-flux method. The source announces a mixed-type flux estimator with additional higher-order terms, but prints neither that local estimator nor its adaptive marking, two-mesh coupling or delta-update rule. The displayed right-hand side also omits div(tau_h); the full cited2017 paper supplies the corrected equation. These source limitations are explicit in SOURCE_SCOPE.md.

The five turns prove scoped results for the recovered equations and fully specified reconstructed algorithms. They do not establish that a historical unprinted procedure is equivalent to either reconstruction, and do not cover all dimensions, coefficients or spaces in the source's general method.

## Retained mathematical results

1. The hybrid flux solve is exactly a mixed reaction-diffusion solve with conservation defect delta(P_h u_H-q_h). Fixed-delta nested two-stage sequences are Cauchy, but can have the wrong limit if their coarse input stagnates. A smooth square eigenmode gives a fine-only bias and a vanishing unaugmented residual. This is a calibration example, not a counterexample to the source's augmented estimator. (`turns/TURN_1.md`)
2. The exact distance to the conservative mixed flux is the minimum-norm divergence lift of that defect. In a simply connected planar RT0 model a negative-norm defect augmentation is reliable and efficient up to data oscillation. A computable L2 substitution is reliable, with no claimed uniform efficiency. Quantitative bulk-marking transfer is proved, initially with a zero-indicator termination gap explicitly retained. (`turns/TURN_2.md`)
3. An explicit variable-delta algorithm on a star-shaped polygon terminates and converges in H(div): absolute defect tolerance, tangential edge marking and data-oscillation refinement. A nested mixed-flux Cauchy lemma handles arbitrary changing coarse inputs. Zero indicators are covered. This is a specified variant, with no rate or complexity claim. (`turns/TURN_3.md`)
4. An explicit fixed-delta P1/RT0 two-mesh algorithm on a simply connected polygon converges in H1 for the primary variable and H(div) for the flux. It uses separate primary residual/fine tangential marking and a fine-over-coarse overlay. The limit error satisfies -Delta e+delta P_infinity e=0, whose positivity identifies the exact solution without assuming full density of the limiting adaptive spaces. (`turns/TURN_4.md`)
5. On convex polygons, an explicit flux upper estimator consists of mixed tangential terms, fine data oscillation and a sqrt(delta)-weighted higher-order coarse residual. It is reliable for every delta>0 and tends to zero under the specified fixed-delta algorithm. Only the tangential part is claimed efficient relative to flux error alone. (`turns/TURN_5.md`)

The last four algorithm/estimator statements are planar A=I, homogeneous-Dirichlet, exact-solve results with the further hypotheses stated in each turn. No source-general theorem is silently substituted by these restrictions.

## Exact remaining gap

The original augmented estimator and intended adaptive rule have not been recovered or identified. Their equivalence to the explicit reconstructions has not been proved. General coefficients, three dimensions, higher-order RT/BDM, nonhomogeneous data, inexact solvers, parameter-policy equivalence, and the claimed computational advantage of a coarse/fine scale relation are not resolved here. Existing2024 Uzawa/reduced-mixed results are credited; a directly related2026 publisher preview is an access-limited literature lead, not a theorem imported without inspection.

No sixth proof-search turn is taken. The collection is submitted for separate adversarial review as scoped partial mathematics, with the original question left unresolved.

## Checks and publication boundary

The five independently authored finite checkers report82,268,245,467,296 exact controls respectively (1,358 total). They check algebra, normal-flux interpolation, matrix projections, residual signs and refinement weights. They do not establish infinite-dimensional convergence or source equivalence; the written proofs carry those claims.

FROZEN_MANIFEST.json binds the portable author collection. Full source PDFs, extracted texts, images and imported records remain local reading copies. Source retrieval, publication work and reviews of other problems were excluded from the substantive-turn count. Only a later independent review and publication gate may promote this partial packet to a draft PR; the final original-target queue status should remain unsolved5/5.
