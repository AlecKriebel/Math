# Independent audit of the Korevaar–Schoen companion theorem

Problem 30006419. Review date: 7 October 2026.

## Verdict and object

**PASS, independently of the Reshetnyak counterexample.** The complete companion argument proves that a neighborhoodwise KS-energy-minimizing Sobolev map from the round sphere into a complete metric space is infinitesimally `(4 + sqrt(17))`-quasiconformal. The bound is explicitly nonsharp. The proof uses the standard metric-Sobolev approximate differential and its chain rule for smooth biLipschitz domain changes, within the framework used in the [source paper](https://arxiv.org/pdf/2503.08553v1).

Audited object: `KOREVAAR_SCHOEN.md`, 6,702 bytes, SHA-256 `4bac91a7e34b266391051d48ae2ef10adc60d10b6ed0d57d1c5cb8395e2a6abe`. No correction is required. The appendix is not a dependency of the negative general-energy result.

## 1. The change of angular variables is correct

For an orientation-preserving invertible matrix `A`, the angular map `v -> Av/|Av|` has angular Jacobian `det(A)/|Av|^2`. Combining that Jacobian with the degree-two homogeneity of the seminorm and the area change of variables gives

`F_s(A) = [pi (det A)^2]^{-1} integral s(w)^2 |A^{-1}w|^{-4} dw`.

Both powers are essential and are correct. This formula depends smoothly on `A` near the identity even when the seminorm is nonsmooth or degenerate. Its derivatives are bounded by a constant times the square of the maximum directional value of the seminorm. The latter is integrable for the maps under consideration.

Differentiating the determinant factor contributes `-2 tr(B)`, and differentiating the inverse-length factor contributes `4 w^T B w`. This gives exactly the manuscript's symmetric tracefree stress tensor. No differentiability of `s` with respect to its vector argument has been assumed.

## 2. The neighborhoodwise definition gives the needed weak equation

A smooth vector field compactly supported in a minimizing coordinate neighborhood generates, for either sign of a sufficiently small parameter, a diffeomorphism equal to the identity near the boundary of a smaller smooth domain. Precomposition is therefore an admissible same-trace competitor on that domain. After changing variables, the seminorm is held at the fixed new coordinate point; only the matrix in `F_s` varies. Its first derivative is the gradient of the vector field at zero parameter. Dominated differentiation yields the weak divergence-free stress equation.

This argument needs no assertion that the original map minimizes under arbitrary whole-sphere changes. Local test fields are enough because the KS density has the differentiability just established. A partition of unity or distributional locality extends the weak equation through any chosen conformal chart.

## 3. The holomorphic object is global, including the poles

Writing the tracefree tensor as entries `a,b,b,-a`, its weak divergence equations are `a_x+b_y=0` and `b_x-a_y=0`. These are precisely the distributional Cauchy–Riemann equations for `a-i b`. The coefficients are locally integrable; the distributional Weyl lemma applies.

The tensor scales quadratically when the seminorm is multiplied by a positive scalar. Under an oriented rotation `R`, it transforms by `R^T T R`. For a holomorphic coordinate derivative `lambda R`, the coefficient `a-i b` therefore multiplies by the **square of that complex derivative**, not its conjugate. The local coefficients give a global holomorphic quadratic differential.

The proof obtains a weak equation in actual source neighborhoods of both poles, so it does not assume removable singularities without an integrability argument. In a plane coordinate, a global holomorphic quadratic differential on the sphere has an entire coefficient with decay `O(|z|^{-4})` at infinity. Liouville's theorem gives zero stress everywhere, hence almost everywhere for the original measurable tensor.

## 4. Zero stress forces quantitative nondegeneracy

Normalize a nonzero seminorm to have maximum directional value one. Choose a unit vector `e_2` where the minimum `m` occurs and a perpendicular vector `e_1`, and write `L=s(e_1)`. The triangle inequality gives `1 <= sqrt(L^2+m^2)`, so `L^2 >= 1-m^2`.

Comparison with the rank-one seminorm `r(v)=L|v_1|` gives `|s(v)-r(v)| <= m` on the unit circle. Both values are at most one, hence their squares differ by at most `2m`. The operator norm of the stress kernel is two and the circumference is `2 pi`; this gives the correct bound `||T(s)-T(r)|| <= 8m` with the stated normalization.

The fourth angular moments yield `T(r)=L^2 diag(1,-1)`. Consequently zero stress implies `1-m^2 <= 8m`, hence `m >= sqrt(17)-4`. Undoing normalization gives the reciprocal bound `4+sqrt(17)`. The zero seminorm satisfies the quasiconformality inequality trivially. A nonzero rank-one seminorm has nonzero stress and is excluded.

The proof handles all planar seminorms, not only inner-product seminorms. In the inner-product case the stress reduces to `2G-tr(G)I`, recovering conformality. Balanced non-Euclidean fourfold-symmetric norms show why the general conclusion is bounded distortion rather than a round infinitesimal norm.

## 5. Independent controls and limits

The companion controls independently test the angular change of variables, centered first variations, and rotation covariance for an anisotropic inner-product norm, the nonsmooth `l^1` and `l^infinity` norms, and a degenerate rank-one seminorm. The largest angular-integration discrepancy in these checks is below `5 x 10^{-9}`; derivative discrepancies are below `2 x 10^{-10}`. Rank-one and inner-product stress formulas and the reciprocal constant were also checked symbolically or at numerical precision.

These controls do not prove the Sobolev chain rule or distributional Weyl lemma. The preceding review checks how those standard ingredients are used. No compactness, isoperimetric assumption, or small-sphere null-homotopy assumption on the target enters this theorem. The unrestricted complete-target formulation is supported by the actual proof.

The argument should not be transferred to the maximum-square energy. Its nonsmooth domain-variation density does not supply the unique differentiable stress used here. The separate Reshetnyak construction is an explicit negative control against that transfer. This verdict makes no claim about first priority or optimal constants.
