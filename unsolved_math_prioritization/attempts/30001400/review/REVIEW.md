# Independent review: fixed-dimensional closure of multiple-copy majorization

**Problem:** 30001400.  
**Verdict:** **PASS_COMPLETE_CREDITED_FIXED_DIMENSION_CLOSURE**.  
**Recommended status:** `already_solved`, `1/5` validation/reduction family.  
**Mandatory mathematical corrections:** none.

Reviewed `KNOWN_CONSEQUENCE.md`, SHA-256 `e796e4e473d4744e20c5a12b9f5b14d87efd4de35fbe510686cd91e2e840599b`. This is an independent AI source and proof audit. The conclusion is credited to the published eventual-majorization theorem and the stated smoothing reduction; no historical priority or human peer-review claim is accepted.

## 1. The original target is exactly a fixed-dimensional closure

I inspected the complete Aubrun contribution, printed pp. 2999–3001 of [OWR 56/2009](https://ems.press/content/serial-article-files/46257), including the rendered theorem page and final question. Its Theorem 1 takes two positive vectors `x,y` of a fixed dimension `d`, and characterizes approximation to `x` by vectors in that **same** probability simplex, with `y` fixed. The final question asks whether the multiple-copy relation can replace the catalytic relation in that theorem. The adjacent theorems allowing an extra coordinate or unbounded dimension are expressly different statements.

The candidate's theorem preserves every one of these quantifiers. Its approximating vector changes only `x`; every approximation remains positive and in dimension `d`; the comparison target remains exactly `y`; and the required tensor exponent may vary with the approximation. No fixed exponent or uniform copy threshold is requested. The original theorem assumes nonzero coordinates, so a claim about arbitrary zero-containing limiting target vectors is unnecessary and is not made.

The orientation also matches: `x≺y` means that `y` majorizes the more mixed vector `x`, or equivalently `x=By` for a bistochastic matrix. The three power-sum families in the candidate are exactly the source conditions.

## 2. Published Proposition 8 supplies the right theorem

I checked the recovered published 2021 main article and the actual typeset online supplement of Mu–Pomatto–Strack–Tamuz, *From Blackwell Dominance in Large Samples to Rényi Divergences and Back Again*, [DOI 10.3982/ECTA17548](https://doi.org/10.3982/ECTA17548). In particular I visually inspected supplement pp. 18–19, Proposition 8 and its proof, and checked the supporting main Theorem 1 and definition of a generic pair.

The proposition has equal finite support sizes, **different maxima and different minima**, and requires all of:

- strict lower entropy for the majorizing distribution at every positive order, including order one and positive infinity;
- strict higher entropy at every negative order, including negative infinity;
- strict lower derivative at order zero.

It gives ordinary majorization for **every sufficiently large common tensor power**. This is stronger than the existence of one power needed at each approximation point. Neither the negative orders nor the derivative condition can be omitted. The candidate uses the proposition with `μ=y`, `ν=x_ε`, in the correct direction.

Positive finite vectors give bounded log-likelihood ratios in the associated experiments. The candidate's eventual strict extreme-coordinate comparisons therefore supply exactly the genericity assumptions of the main theorem. It does not apply that theorem directly to an equal-extrema boundary pair.

The supplement's prose describes `H(0)` as a support size, while its displayed definition actually gives the logarithm of that size. The candidate consistently uses `H(0)=log d`. The slip does not affect equality of support sizes or the derivative formula being used. The audit relies on the displayed mathematical definitions and proposition, not that prose shortcut.

This is a source/application audit of the published theorem, not an independent reconstruction of its entire large-deviation proof. The published theorem's difficulty and attribution remain with its authors.

## 3. Necessity and boundary support

If `a^⊗n≺y^⊗n`, convexity of `s^p` for `p<0` and `p>1`, and concavity for `0<p<1`, give the corresponding tensor power-sum inequalities. Tensor multiplicativity is exact: `N_p(a^⊗n)=N_p(a)^n`. Taking positive `n`th roots gives all required inequalities for `a`; normalization and equal dimension handle orders one and zero.

For a sequence tending to a strictly positive `x`, each fixed real power sum is continuous near `x`. The limit may therefore be passed separately for each real order, yielding the full family of necessary inequalities. No uniform convergence in the order parameter is needed.

Even if one allowed zero coordinates in approximants as a notational convention, they cannot appear in this particular comparison. In dimension `d^n`, the next-to-last majorization inequality and equal total mass give `min(a^⊗n)≥min(y^⊗n)>0`. Since these minima are `min(a)^n` and `min(y)^n`, the approximant must be positive. This correctly rules out a hidden support-size change.

## 4. Smoothing gives every strict hypothesis

Assume the three weak power-sum families. After taking logarithms and dividing by `1−p` with its proper sign, they imply

`H_x(p)≥H_y(p)` for `p>0`, and `H_x(p)≤H_y(p)` for `p<0`.

At order one, use continuity; at the infinite orders, use the maximum/minimum asymptotics of the power sums. This yields `max x≤max y` and `min x≥min y`.

Since the entropy functions are analytic near zero for positive vectors, the difference `H_x−H_y` has value zero there. Its nonnegative values immediately to the right imply `(H_x−H_y)'(0)≥0`. This is the missing weak derivative comparison; it does not follow merely by setting the order to zero in a power-sum inequality.

For nonuniform `x`, set `z=(1−ε)x+εu_d`, with `0<ε<1`. Strict Jensen inequalities show that the uniform vector has strictly smaller power sums for `p<0` or `p>1`, and strictly larger ones for `0<p<1`. Applying convexity/concavity to the segment from `x` to `u_d` then gives the strict entropy improvements claimed in the candidate. Order one is handled separately by strict concavity of Shannon entropy; strictness cannot simply be inferred from a limit of strict inequalities at other orders.

For the derivative at zero, `H'_a(0)=log d+d^(-1)Σ log a_i`. The strictly larger logarithmic product of `z` therefore gives `H'_z(0)>H'_x(0)`. As an independent check, its derivative along the segment is

`d/dε Σ log z_i = ((1/d)Σ 1/z_i − d)/(1−ε)>0`.

The final strict inequality is the harmonic-mean inequality, because `Σz_i=1` and `z` remains nonuniform for `ε<1`. This confirms the direction and shows directly that no equality at the derivative boundary survives smoothing.

For the extremes, the affine coordinate transformation is increasing, so

`max z=(1−ε)max x+ε/d < max x ≤ max y`,

`min z=(1−ε)min x+ε/d > min x ≥ min y`.

Nonuniformity is exactly what guarantees `max x>1/d>min x`. Thus both infinite-order strict inequalities and both unequal-extrema assumptions hold. All arguments are analytic for the entire order ranges; finite sampling is not substituted for them.

If `x` is uniform, the constant sequence already works because `u_d≺y`. This includes `d=1`. If `y` were uniform while `x` were nonuniform, the weak extreme comparison would already be impossible, so there is no omitted exceptional branch.

Applying Proposition 8 separately for each `ε` gives `z^⊗n≺y^⊗n` for all sufficiently large `n`. Taking `ε_k=1/(k+1)` yields the required fixed-dimensional approximating sequence, with exact distance `||z−x||₁=ε||u_d−x||₁`. The theorem is not claimed to hold for the unperturbed boundary pair itself.

## 5. Experiment translation and orientation

For the binary experiment `(a,u_d)`, direct substitution into Rényi divergence gives the three formulas in the candidate. I independently checked the signs in the negative-order formula: the coefficient `(1−p)/p` is negative when `p<0`, which reverses the relevant entropy comparison exactly as required. At order one in the reversed experiment, the divergence is `−H'_a(0)`.

On `n` copies the two uniform reference distributions both have cardinality `d^n`. A stochastic channel sending the more informative experiment to the less informative one must preserve this uniform distribution. In equal finite dimensions, this makes its matrix bistochastic. Hence its signal distribution equation is exactly ordinary majorization, not a relation with padding, dimension changes, or a catalyst. The role of equal support sizes is substantive.

## 6. Independent controls

The submitted checker passes **10,598 assertions** and reproduces its receipt byte for byte. The frozen mathematical artifact and submitted code hashes match.

A separate standard-library checker passes **26,754 exact assertions**. It uses 637 positive nonuniform rational vectors and checks the independent logarithmic-product derivative identity, strict proper-prefix smoothing gaps, extrema, fixed dimension and exact approximation distance. It also checks the Rényi translation as equality of formal coefficients of `log N_p` and `log d`, tensor products of explicit uniform-preserving channels, the zero-coordinate exclusion, uniform cases, and a positive pair with two-copy but not one-copy majorization.

These computations diagnose algebra and orientation. They do not certify the continuum of entropy inequalities by a grid or replace the published eventual-majorization theorem. The complete sufficiency argument is the analytic smoothing proof together with that credited input.

## 7. Final conclusion

Every original fixed-dimensional positive-vector quantifier is covered, including the boundary cases handled by approximation rather than a nongeneric direct application. The requested closure characterization is a complete consequence of the published 2021 theorem. Preserve `already_solved 1/5`, credit Mu–Pomatto–Strack–Tamuz and the earlier Turgut/Aubrun–Nechita results, and retain the lack of a novelty claim or effective copy bound. No mandatory correction to the frozen artifact is needed.
