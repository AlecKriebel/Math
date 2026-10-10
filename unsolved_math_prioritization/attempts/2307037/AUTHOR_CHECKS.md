# Author checks and adversarial review

This is the author self-review preceding the separately tasked independent mathematical audit in AUDIT.md. The original proof and source-hypothesis files were frozen before these supplementary controls. These controls supplement the analytic reasoning and are not hidden computational dependencies of the standalone proof.

## Analytic checks

1. **Exact area:** prescribe quadrature masses pi*lambda_j. The resulting disks have radius sqrt(lambda_j), and the quadrature set has area pi. Its null boundary permits closure without increasing area.
2. **Repeated poles:** coalesce equal locations. All combined weights stay positive and the normalized rational function is unchanged.
3. **Faraway poles:** the quadrature set need not fit inside any fixed disk. Splitting its indicator at sqrt(2)*R controls its far part without using a support-radius-dependent constant.
4. **One set for all radii:** construct S as the closure of the quadrature set once. Only the decomposition used to estimate its field changes with R.
5. **Sign and pi:** harmonic quadrature gives integral_Omega (w-z)^(-2) dA = pi*g(z), while T carries -1/pi. Thus T chi_Omega = -g.
6. **All complementary components:** for any z outside the closed S, the kernel is harmonic on a neighborhood of S. It is not necessary that z belong to the unbounded component.
7. **Lebesgue integral:** the target is bounded using the ordinary kernel representation off the closed S. Principal values occur only in the statement of the established transform theorem and introduce no cancellation into the target nonnegative integral.
8. **No pointwise triangle-sum entropy defect:** the sharp near-field transform estimate is applied to one indicator, not to the uncancelled sum of point-pole magnitudes.
9. **Source hypotheses:** boundedness, almost-everywhere continuity, density gap, and null boundary are checked for the disk construction and iteration. No disjointness or connectedness hypothesis is invented.
10. **Small/large R and mass endpoints:** a=0 is interpreted by continuity; a=pi gives the exact near coefficient. R>1 ensures log R is positive. The final inequality is uniform as R decreases to 1.
11. **Sharp leading coefficient:** PROOF.md proves that g(z)=z^(-2) forces the coefficient at least 2*pi for every exceptional set of area pi.
12. **Attribution:** the sharp indicator estimate and positive-mass quadrature existence are credited to prior literature. Neither is presented as an authored discovery.

## Supplementary finite controls

The historical normal and Python -O runs produced byte-identical mathematical results. The standard-library test program used explicit exceptions, not removable assertions. Programs and raw result files are not part of this edition. It executed:

- 29 integrity predicates covering the source identities and frozen proof documents
- 187 exact rational predicates for homogeneous-kernel scaling and repeated-pole coalescence
- 8,016 high-precision Decimal diagnostic predicates for the entropy bound and localization inequality, including a=0, a=pi and radii approaching 1
- 43 floating diagnostic predicates for independent angular integration and direct disk quadrature, including translated disks far from the origin
- 7 deliberately incorrect alternatives rejected

The angular relative error was below 4.3e-16, and the direct disk-quadrature scaled absolute error below 5.6e-13 in the tested cases. These numbers are ordinary floating-point diagnostics, not certified interval enclosures. Decimal evaluations likewise do not prove a continuum of inequalities. The analytic argument supplies the all-parameter reasoning.

The seven negative alternatives were: using the ordinary union of overlapping half-mass disks as a full-area replacement; forgetting the pi mass factor; reversing the Beurling sign; treating a first-order kernel as scale-invariant; using no separation in the far-field split; dropping the positive entropy loss; and losing the fixed total-mass normalization.

The eight relevant Levine–Peres page-text comparisons also match after removing whitespace. That comparison is supporting source-identification evidence; the original pages were inspected separately.

## Subsequent acceptance and limitations

The author identified no unresolved mathematical step in the deduction, given the two established inputs. The subsequent independent internal AI-assisted audit checked the complete proof and those inputs’ hypotheses and accepted the complete affirmative deduction without required mathematical correction. The manuscript and audit are unrefereed. No historical-priority claim, optimal-additive-constant claim, formal-proof certification, or external human-peer-review claim is made.
