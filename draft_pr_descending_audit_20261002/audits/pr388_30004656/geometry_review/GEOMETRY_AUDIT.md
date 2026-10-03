# Independent adversarial geometric review of PR 388

Reviewed 2026-10-02, America/Los_Angeles. Scope: frozen candidate `snapshot/problems/30004656_robustness`, SOURCE_GATE, Turns 1–3, and the corresponding summary statements in RESULT. Independent AI-assisted audit; not human peer review, a historical novelty certificate, or a certification of the full BLN conjecture.

**Disposition: PASS for the three stated mathematical partials. No mathematical repair is required.** The original unrestricted conjecture remains unresolved. One optional public-summary clarification is recorded below: explicitly retain `n >= 8d` in the comparison between Turn 3 and the `sqrt(n/k)` order. Other turns and package-level reproducibility are outside this review's scope.

## 1. Primary target and review independence

SOURCE_GATE was read first, then the published [BLN COLT paper](https://proceedings.mlr.press/v134/bubeck21a/bubeck21a.pdf), pp. 2–3 and Theorem 6. The conjecture concerns random spherical or covariance-normalized Gaussian inputs, independent signs, a fixed Lipschitz activation, and arbitrary real network parameters. Its spherical-domain lower order is `sqrt(n/k)`. The separate matching-construction question is not this target. The paper's global-norm projection theorem does not by itself prove its spherical-domain conjecture.

Each candidate mechanism was independently reconstructed before the existing review or candidate checker code was read. The standard-library control script in this folder imports no candidate code. Only after deriving the arguments and executing those controls was `review/ADVERSARIAL_REVIEW.md` read. Its geometric assessments agree with this review. The [Shmalo v1 preprint](https://arxiv.org/pdf/2607.07778v1), appendix A.7, does contain the credited fiber-transport observation; its larger theorem is not an input to this audit.

The independent claim under review is that the candidate's *restricted* geometric results follow from their expressly stated assumptions. A proof for all functions is allowed to imply a neural lower bound. A width-dependent conjecture is not solved merely because some fixed-dimensional data are intrinsically difficult to interpolate smoothly.

## 2. Turn 1: exact circle interpolation law

### Deterministic optimum and shortest marked gap

For finite distinct data in a metric space, any interpolant has Lipschitz constant at least

`L_data = max_{i != j} |y_i-y_j| / distance(x_i,x_j)`.

For signs, this is zero if all signs agree and otherwise equals `2 / D`, with `D` the shortest opposite-sign chord. Define `F(x)=min_i(y_i+L_data distance(x,x_i))`. Each term is `L_data`-Lipschitz; taking a finite minimum preserves this constant. At a datum `x_j`, each term is at least `y_j` by the finite-data Lipschitz inequality, and the `j`th term equals `y_j`. Hence the minimum attains the claimed optimum on the circle and also extends globally. Clipping is a contraction and does not change values of ±1. This construction makes no two-layer attainment claim.

Write the normalized cyclic gaps `s_i` and mark a gap exactly when its endpoint signs differ. The number `J` is even, since returning to the starting label requires an even number of flips. With both signs present, `J >= 2`, and `T=min_marked s_i` satisfies `T <= 1/J <= 1/2`.

Every shorter arc connecting opposite signs crosses a marked edge: along that arc the endpoint sign change requires an odd number of flips. Its length is at least `T`. The marked edge attaining `T` itself provides an opposite-sign pair and is a shorter arc because `T <= 1/2`. Thus the minimum shorter-arc length is exactly `T`. Chord distance `2 sin(pi T)` is increasing on `[0,1/2]`, giving

`L_* = 1/sin(pi T)`.

This proof includes `n=2`, ties at `T=1/2`, multiple minimizing edges, unequal gap sizes, and wraparound edges. It would fail if one replaced chord distance by unnormalized angular distance without the sine; the candidate does not do that.

### Random law and conditioning

Rotate the sample by the angle of the indexed datum `x_1`. Conditional on that angle, all remaining angles are independent uniform variables, and their shifted law does not depend on the conditioned angle. Ordered spacings starting at this *sample point* therefore have uniform density on the `(n-1)`-simplex. They are Dirichlet with all parameters one.

This rooting is substantive. Ordering around a deterministic origin gives a size-biased wraparound gap: its mean is `2/(n+1)`, while the other gaps have mean `1/(n+1)`. Rooting at a sample point gives mean `1/n` for each gap. The independent numerical control explicitly distinguishes these cases.

Permuting iid independent signs using an order determined only by inputs leaves an iid sign sequence independent of spacings. For any even flip subset there are exactly two consistent cyclic sign assignments. Therefore

`P(J=j)=2 binom(n,j)/2^n` for even `j`, and zero for odd `j`.

In particular `P(J=0)=2^(1-n)`, the probability of all-equal signs. Given `J=j`, the chosen marked coordinates are independent of spacings, and exchangeability allows any fixed subset of `j` coordinates. For `t >= 0`, translating each marked coordinate by `t` maps the survival region to a simplex with mass `1-jt`. Its `(n-1)`-dimensional volume rescales by `(1-jt)^(n-1)`. Thus

`P(T>t | J=j) = max(1-jt,0)^(n-1)`.

At `jt=1` the survival probability is zero. There is no hidden independence assumption about simplex coordinates. Conditional distributions for `j>0` are continuous, so `>` versus `>=` at the CDF conversion causes no atom error. Since `T in (0,1/2]`, for `u >= 1` the event `L_* <= u` is `T >= arcsin(1/u)/pi`. This gives exactly Turn 1 equation (5), with the all-equal atom at zero. For `0 <= u < 1`, only that atom contributes. At `u=1`, there is no extra atom: attaining `T=1/2` has zero probability.

An independent explicit edge control is `n=2`: for `u >= 1`, the candidate CDF reduces to `1-arcsin(1/u)/pi`; its value at one is `1/2`, and its limit at infinity is one.

### High-probability constants and quantifiers

`J` has the Binomial `(n,1/2)` law conditioned on even parity, whose conditioning probability is exactly `1/2`. The standard multiplicative Chernoff lower-tail estimate at half the mean therefore gives `P(J<n/4) <= 2 exp(-n/16)`.

On `J >= n/4`, simplex survival is at most `exp(-(n-1)nt/4)`; if `Jt >= 1` it is zero and the bound still holds. At `t=8(A+1)log(n)/n^2`, this exponent is at most `-(A+1)log(n)` because `2(n-1)/n >= 1` for `n >= 2`. The all-equal event is included in the bad-`J` event, so `T` need not be defined there. For sufficiently large `n`, `t <= 1/2`. On the good event, `sin(pi T) <= pi t`, producing the exact stated floor and failure bound.

The event uses only the labeled data, so it holds simultaneously for every interpolant, width, and even a data-chosen activation. This is stronger than needed for a fixed activation. With fixed `A` and `k >= 1`, `n^2/log(n)` eventually dominates `sqrt(n/k)`. This is a correct fixed-`d=2` spherical implication. It provides no claim about growing dimension, Gaussian sphere norms, minimal neural width, or attaining the unrestricted optimum with a network.

**Turn 1 status: PASS.**

## 3. Turn 2: positive-density charts and birthday collisions

### Patch assumptions and deterministic floor

For an injective Lipschitz chart on the compact coordinate cube, images of measurable coordinate cells are measurable; the chart is a homeomorphism onto its image. Density absolute continuity gives zero probability to coordinate boundaries. Outside-patch mass is permitted and is retained in Poisson splitting.

A cell has coordinate volume `(2r)^s/M`, so its mass is between `A_0/M` and `B_0/M`. Its diameter is at most `2r C sqrt(s)/m`. If opposite labels occur in that cell, their required value difference is two, giving the floor `m/(r C sqrt(s))`. The domain must contain those actual sample points. Injectivity and the density assumption ensure distinctness almost surely; if inconsistent data did coincide, no interpolant would exist and the lower-bound assertion would be vacuous.

### Poisson and fixed-sample probabilities

With independent `N ~ Poisson(n/2)`, splitting by cell and sign gives independent Poisson counts of mean `x_j=np_j/4`. The probability of two signs in a cell is `(1-exp(-x_j))^2`. For `x in [0,1]`, `exp(x)>=1+x` implies `1-exp(-x)>=x/(1+x)>=x/2`. Consequently the cell collision probability is at least `n^2 p_j^2/64`. Cell independence and `1-z<=exp(-z)` give

`P(A_N) <= exp(-n^2 sum_j p_j^2/64) <= exp(-A_0^2 n^2/(64M))`,

where `A_q` means no opposite-sign cell among the first `q` observations. The condition `M>=B_0 n/4` makes every `x_j<=1`.

The coupling direction is correct: `A_n and N<=n` implies `A_N`. Therefore `P(A_n)<=P(A_N)+P(N>n)`. Since `E 2^N=exp(n/2)`, Markov gives `P(N>n)<=exp(-(log(2)-1/2)n)`. Independence of `N` from the infinite sample sequence is sufficient; the proof does not condition on `N=n`. An independent exact dynamic program with nonuniform cell masses and outside-patch mass tests this same inequality.

### Rounding, asymptotics, and model applications

For `q=(n^2/(B log(n)))^(1/s)>=1`, `q<=ceil(q)<=2q`, so

`n^2/(B log(n)) <= M <= 2^s n^2/(B log(n))`.

The stated `B=64*2^s*(A+1)/A_0^2` turns the collision exponent into at least `(A+1)log(n)`. Also `M>=B_0 n/4` eventually because all chart constants and `s` are fixed and `n/log(n)` diverges. The sufficiently-large-`n` dependence is necessary and is explicitly retained. No claim for `n=1`, where `log(n)=0`, is present.

For the sphere graph `Phi(z)=(z,sqrt(1-||z||^2))`, the chosen cube gives `||z||<=1/4`. The derivative has operator norm `1/sqrt(1-||z||^2)<=4/sqrt(15)<2`; the same expression is the surface Jacobian. Division by the fixed total sphere area gives positive finite lower and upper densities. Convexity of the coordinate cube permits integrating the derivative bound into a global chart Lipschitz bound. Both colliding points lie on the sphere, so this is the actual spherical Lipschitz norm.

The floor is `c n^(2/s)/(log(n))^(1/s)`. Comparing its square with `n/k` gives exactly

`k >= C n^(1-4/s)(log(n))^(2/s)`.

For fixed spherical `d=2,3,4`, `s=d-1<4`, and the floor eventually dominates `sqrt(n)`; for `d=5`, the comparison requires `k >= C sqrt(log(n))`. The normalized Gaussian model has a positive bounded density on any fixed finite cube and `s=d`, giving the stated global-norm implication in fixed `d<=3`. Gaussian samples are off the sphere almost surely; this proof cannot be read as a sphere-restricted Gaussian theorem.

The exact equal-cell formula is also correct. A cell's exponential generating function is `2 exp(z/(2M))-1`: all-positive sequences or all-negative sequences, subtracting the doubly counted empty sequence. Taking the `M`th power, expanding, and extracting `n!` times the `z^n` coefficient gives equation (6). The independent dynamic program uses explicit cell sign states and agrees exactly.

**Turn 2 status: PASS.** Constants depend on the fixed chart and dimension. It supplies no uniform growing-dimensional neural width penalty.

## 4. Turn 3: simultaneous adaptive-rank sphere floor

### Sphere-domain bridge

For rank `r<d`, fix a unit kernel vector `z`. The lifts `x(u)=u+sqrt(1-||u||^2)z` lie on the sphere and satisfy `Px(u)=u`. If `||u||,||v||<=1/2`, rationalizing the height difference gives

`|sqrt(1-||u||^2)-sqrt(1-||v||^2)|`

`<= (||u||+||v||)||u-v|| / (sqrt(1-||u||^2)+sqrt(1-||v||^2))`

`<= ||u-v||/sqrt(3)`.

Orthogonality then improves the triangle bound to the stated lift distance `<=2||u-v||/sqrt(3)`. Thus the restriction of `g` to the projected half-ball is `(2/sqrt(3))L`-Lipschitz. This uses only two points on the sphere, not a straight segment through the ball. No differentiability, global Lipschitzness, continuity outside the projected ball, or network parameter bound is assumed. If `r=d`, no kernel exists, but the candidate never invokes the lift in that case.

### Common covariance and label event

Rotational invariance and Gaussian radial decomposition yield

`E(d<u,x>^2)^m = d^m(2m-1)!! / product_{j=0}^{m-1}(d+2j) <= (2m-1)!!`.

The `m=0` value is one. Every moment-series term is nonnegative, so monotone convergence justifies exchanging expectation and series. The dominating Gaussian-square series gives `E exp(d<u,x>^2/4)<=sqrt(2)`. Markov with independent inputs gives a fixed-direction upper-tail probability `<=exp(-n+(n/2)log(2))` at `4n/d`.

A fixed `1/4`-net can have at most `9^d` elements. For a symmetric matrix, approximating a maximizing unit vector changes its quadratic form by at most `2*(1/4)||A||`; positive semidefiniteness then bounds the norm by twice the net maximum. Hence covariance failure is at most

`exp(d log(9)-n+(n/2)log(2)) <= exp(-n/4)` for `n>=8d`.

At the boundary `n=8d`, the exact exponent coefficient is approximately `-0.378773`, comfortably below `-1/4`. Independent sign counts fail the required interval `[3n/8,5n/8]` with probability at most `2 exp(-n/32)` by Hoeffding. A union bound gives the candidate probability; small parameters can make this displayed bound uninformative, but still valid.

Let `S=sum_i x_i x_i^T`. On the common event, for *every* rank-`r` projection,

`sum_i ||Px_i||^2 = trace(PS) <= r ||S|| <= 8nr/d`.

This is a deterministic consequence of the already chosen data event, valid even when `P` is selected using both labels and inputs. There is no uncountable projection union bound and no independence claim about the chosen projection.

### Accuracy, pair counting, and all ranks

Empirical mean square error `<=1/256` allows at most `n/16` points with error `>1/4`. If `1<=r<=d/512`, projection energy allows at most `32nr/d<=n/16` points with norm `>1/2`. There are at least `3n/8` disjoint opposite-sign pairs. Deleting every pair with any bad endpoint loses at most `n/8` pairs, leaving at least `n/4`. The two bad sets may overlap; bounding their union by their total size is conservative and valid.

Each retained pair has value difference at least `3/2`. The sphere lift therefore forces projected distance at least `3sqrt(3)/(4L)>=1/L`. Finite `L=0` cannot occur with this value difference, so the division is justified; `L=infinity` satisfies the conclusion directly. Disjointness of pairs gives

`sum_pairs ||P(x_i-x_j)||^2 <= 2 sum_i ||Px_i||^2 <= 16nr/d`.

Thus `n/(4L^2)<=16nr/d`, or `L^2>=d/(64r)`.

For `r=0`, the function is constant on the sphere. Minimizing constant empirical square error gives the empirical label variance `4p(1-p)>=15/16` for `p in [3/8,5/8]`, excluding the accuracy threshold. For `r>d/512`, both signs have at least one accurate point, whose chord distance is at most two. Thus `L>=3/4`; with `d/r<512` this implies

`L >= (3/(32sqrt(8))) sqrt(d/r)`.

The same constant is smaller than the small-rank constant: its square is `9/8192<1/64`. At the branch boundary its square times `512` is exactly `9/16`, matching `(3/4)^2`. This verifies the stated unified constant, including integer rank thresholds, `r=d`, and every `d>=2`.

### Neural implication and exact remaining gap

A width-`k` network depends only on the orthogonal projection onto the span of its hidden slopes, of rank at most `min(k,d)`. Biases and output weights do not enlarge that span. An affine skip adds at most one slope. All choices may depend on the data, since the event controls every projection and every factorized function. Passing from `r<=k` to the weaker `sqrt(d/k)` lower bound is correct. Rank-zero networks cannot fit at the stated accuracy.

The exact comparison with the original order is: for fixed `C_0>=8` and

`8d <= n <= C_0 d`,

`L >= (3/(32sqrt(8 C_0))) sqrt(n/k)`.

This is an optional wording clarification to Turn 3's phrase “when n is comparable to d”; the theorem already declares `n>=8d`. The derivation does not establish `d<=n<8d` with its displayed constants. For `n/d` unbounded, it misses the essential multiplicative `sqrt(n/d)` factor. No algebraic reformulation can remove that gap.

**Turn 3 status: PASS.** The sphere-domain projection mechanism is credited rather than presented as a new general resolution.

## 5. Independent artifacts and limitations

`independent_geometry_controls.py` produced `INDEPENDENT_GEOMETRY_CONTROLS.json` without importing candidate code. Controls passed:

- 59,600 exact rational circle shortest-arc/marked-edge configurations; exhaustive flip-pattern counts through `n=7`; 1,190 simplex-lattice tail counts; explicit `n=2` CDF identity.
- 18 seeded CDF comparisons, each based on 35,000 independent draws for its dimension, plus the rooted versus deterministic-origin gap control.
- 72 exact uniform-cell dynamic-program/inclusion-exclusion comparisons; 48 nonuniform, outside-patch Poisson/coupling checks; 2,520 exact rounding comparisons.
- 32,000 numerical sphere-lift boundary/interior checks; 1,700 exact moment comparisons; exact rank, error-count, and branch constants.

These are independent falsification and reproducibility controls, not proofs of infinite probability laws. The written derivations above justify those laws and uniformity. Numeric comparisons use fixed seeds and explicit tolerances. No assertion count or simulation is evidence for historical novelty.

The three families have distinct precise gaps: circle geometry cannot cover growing `d`; fixed-chart collisions have dimension-dependent constants and weaken as intrinsic dimension grows; adaptive rank controls `d` rather than `n`. Combining them does not resolve BLN Conjecture 1. No source theorem is used to transfer a global norm to a sphere norm, and no sphere theorem is claimed for off-sphere Gaussian observations.

The previous geometric review agrees with this independent outcome. No frozen candidate files, Git state, or external services were modified. The scope permits acceptance of these partial findings under an **unsolved** disposition, subject to the parent's separate audit of Turns 4–5 and the complete PR.
