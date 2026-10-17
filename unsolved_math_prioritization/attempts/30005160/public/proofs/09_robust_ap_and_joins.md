# Proof 09  Arithmetic progressions with radial noise and joins

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Proof dependencies included in this package: [Circuit obstructions and positive uncentered blocks](01_circuit_obstructions.md); [Radial test functions and affine joins](04_radial_joins.md); [Arithmetic progression triples and a failed multiradius extension](05_arithmetic_progressions.md).

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

## 1. Main result

**Theorem.** Every affine join of blocks of the following types has the strict real majorant property for every finite exponent `p>=2`:

- singletons;
- three-point arithmetic progressions;
- two-layer simplices `{a_i,a_i+v}`, where `v` and the differences `a_i-a_1` are independent;
- center-free cross-polytopes `{c+u_i,c-u_i}`, where the directions `u_i` are independent.

The blocks may be replaced by integer-frequency configurations with the same labelled affine relation lattices. All subsets also have the property. “Affine join” means that the full augmented integer relation lattice is the direct sum of the labelled block relation lattices.

The new analytic assertion is stronger than an isolated AP `L^p` inequality: the AP sign comparison remains valid after adding **arbitrary independent bounded rotationally invariant complex noise**. Consequently, all other signed blocks may be held as noise during one-block-at-a-time sign replacement. The AP-free blocks admit the same robust comparison through the radial bisubharmonic cone.

This does not settle centered cross-polytopes containing their center and at least two endpoint pairs for `2<p<3`. Such a block is not an affine join of its AP triples: the triples share their center and also create cross-pair relations.

## 2. A monotone arcsine moment, including the nonsmooth exponent range

**Lemma 1.** For every real `alpha>0`,

`F_alpha(x) = E_theta |x+cos(theta)|^alpha`

is even, continuous, and strictly increasing as a function of `x>=0`. More precisely, for `|x|<1`,

`F_alpha(x) = F_alpha(0) sum_{n>=0} [(-alpha/2)_n^2 / ((1/2)_n n!)] x^(2n)`.

Every coefficient is nonnegative, and the `x^2` coefficient is `alpha^2 F_alpha(0)/2>0`. The series may terminate when alpha is a positive even integer. No differentiation of a nonintegrable pointwise derivative is used.

### Distributional ODE proof

Set `g(u)=|u|^alpha`, regarded as a locally integrable distribution. Its homogeneity gives, as distributions,

`u g'(u)=alpha g(u)`,

`u g''(u)=(alpha-1)g'(u)`,

`u^2 g''(u)=alpha(alpha-1)g(u)`.

The first identity follows directly by distributional integration by parts, and the next two follow by differentiation and multiplication by `u`. All are valid for every `alpha>0`.

For a smooth function, periodic integration of the derivative of `sin(theta) g'(x+cos(theta))` gives

`E_theta cos(theta) g'(x+cos(theta)) = E_theta sin^2(theta) g''(x+cos(theta))`.       (2.1)

The same equality holds as distributions in `x`: test against a compactly supported smooth function of `x`, perform the `x` convolution first, and the resulting angular integrand is smooth and periodic. Thus (2.1) is valid without assuming that `g''` is represented by a locally integrable function.

Write `t=cos(theta)` and `u=x+t`. The left side of (2.1) is

`alpha F_alpha(x)-x F_alpha'(x)`.

Using the homogeneity identities, the right side is

`(1-x^2) F_alpha''(x) + 2x(alpha-1) F_alpha'(x) - alpha(alpha-1) F_alpha(x)`.

Consequently

`(1-x^2) F_alpha'' + (2alpha-1)x F_alpha' - alpha^2 F_alpha = 0`                 (2.2)

as a distribution, in particular on `(-1,1)`.

The integral defining `F_alpha` is continuous everywhere by uniform continuity of `|u|^alpha` on compact intervals. Equation (2.2) upgrades it to a classical smooth solution on `(-1,1)`. For completeness, on any compact subinterval divide by `1-x^2` and write `V=F_alpha'` as a distribution. The equation has the form `V'+bV=cF_alpha`. Multiplication by the smooth integrating factor turns its left side into a distributional derivative equal to a continuous function. Hence `V` is a continuously differentiable function up to an additive smooth homogeneous solution, and `F_alpha` is `C^2`. Repeated differentiation bootstraps to smoothness. Evenness now implies `F_alpha'(0)=0`.

A power-series solution `F_alpha(0) sum a_n x^(2n)`, with `a_0=1`, satisfies (2.2) exactly when

`a_(n+1) = (2n-alpha)^2 / ((2n+1)(2n+2)) * a_n`.

Thus

`a_n = (-alpha/2)_n^2 / ((1/2)_n n!) >= 0`.

Unless it terminates, the ratio tends to one, so this series and its derivatives converge on every compact subset of `|x|<1`. It solves (2.2) and has the same value and derivative at zero as `F_alpha`. Uniqueness for a regular second-order linear ODE gives the asserted identity throughout `(-1,1)`. Its positive `x^2` coefficient proves strict increase on `[0,1)`.

For `x>=1`, every `x+cos(theta)` is nonnegative and increases with `x`; hence the integral is strictly increasing pointwise in `x`. Continuity of `F_alpha` at `x=1` joins the two intervals. No derivative or hypergeometric evaluation at the singular endpoint is required. Evenness follows by shifting theta by pi. This proves Lemma 1.

## 3. Radial noise preserves the weaker scalar AP condition

Call a `C^2` function `h:R->R` **AP-admissible** if `h` is even and `h''` is even and nondecreasing on `[0,infinity)`. Convexity of `h''` is not required.

**Lemma 2.** Let `p>2` and let `Y` be any bounded rotationally invariant complex random variable. Then

`h(x)=E |x+Re(Y)|^p`

is AP-admissible.

Indeed, `|x|^p` is `C^2` for `p>2`, and bounded noise permits differentiation under the expectation on every compact interval. With `alpha=p-2>0`,

`h''(x)=p(p-1) E |x+Re(Y)|^alpha`.

Radiality implies symmetry of `Re(Y)`, so `h` and `h''` are even. Also `Y` has the same law as `R exp(iTheta)`, where `R=|Y|` and `Theta` is an independent uniform angle; this statement includes a possible atom at `R=0`. Conditional on `R=r>0`,

`E_Theta |x+r cos(Theta)|^alpha = r^alpha F_alpha(x/r)`.

Lemma 1 makes this nondecreasing in `x>=0`. The `r=0` value is `x^alpha`, also nondecreasing. Averaging over `R` proves the claim. This covers arbitrary radial probability laws and does not assume a density.

**Lemma 3.** If `h` is AP-admissible, then

`H_h(u,v)=E_theta h(sqrt(u)+sqrt(v)cos(theta))`

is supermodular on `[0,infinity)^2`.

On the positive quadrant, differentiation under the integral gives

`(H_h)_(uv)(u,v) = 1/(4sqrt(uv)) E_theta [cos(theta) h''(sqrt(u)+sqrt(v)cos(theta))]`.

Pairing a cosine with its negative and writing `a=sqrt(u)`, `b=sqrt(v)`, `T=|cos(theta)|`, the final expectation equals

`(1/2) E [ T (h''(a+bT)-h''(a-bT)) ] >=0`.

This follows from evenness of `h''`, monotonicity on the positive half-line, and `a+bT>=|a-bT|`. Rectangle integration proves supermodularity in the open quadrant, and continuity extends it to the boundary. This proof needs neither fourth derivatives nor convexity of `h''`.

## 4. Robust AP comparison under arbitrary radial noise

For an even continuous scalar function `h`, write its angular radialization as

`Phi_h(z)=E_phi h(Re(exp(-i phi)z))`.

Let `h` be AP-admissible. For nonnegative `a,b,c`, set `A=a+b`, `B=|a-b|`, and `D=A^2-B^2>=0`. The two essential real-sign patterns on the AP triple become the same parametrically uniform ellipse shifted along its major and minor axes:

`Z_major=c+A cos(theta)+i B sin(theta)`,

`Z_minor=A cos(theta)+i(B sin(theta)+c)`.

The elementary reduction is the same as in the earlier circuit and block results: overall sign and the change `theta -> theta+pi` remove common signs; changing exactly one endpoint sign interchanges the semiaxes, up to rotation/reflection. The even radial test is invariant under these harmless changes.

After projecting in direction phi, the random sinusoid from the centered ellipse has squared scalar amplitude

`v(X)=B^2+D X`, where `X=cos^2(phi)`.

The squared deterministic shift is `c^2 X` for the major-axis shift and `c^2(1-X)` for the minor-axis shift. Its sign is irrelevant because `h` is even and the cosine variable is symmetric. Thus

`E Phi_h(Z_major)=E_X H_h(c^2 X,v(X))`,

`E Phi_h(Z_minor)=E_X H_h(c^2(1-X),v(X))`.

Since `X` and `1-X` have the same law, twice the difference is the expectation of

`H_h(c^2 X,v(X)) + H_h(c^2(1-X),v(1-X))`

`- H_h(c^2(1-X),v(X)) - H_h(c^2 X,v(1-X))`.

Both coordinate orderings agree, whether `X>=1/2` or `X<=1/2`. Lemma 3 therefore makes this a nonnegative supermodularity rectangle. The AP sign comparison holds for every test `Phi_h` with `h` AP-admissible.

Now fix arbitrary bounded radial noise `Y`, independent of the AP variable. Let `g(x)=|x|^p` and `h(x)=E_Y g(x+Re(Y))`, with `p>2`. By Lemma 2, `h` is AP-admissible. Fubini and rotational invariance of `Y` give the exact identity

`E_Y Phi_g(z+Y) = Phi_h(z)`.

Moreover `Phi_g(z)=m_p |z|^p`, where `m_p=E|cos(phi)|^p>0`. Applying the preceding AP comparison to `Phi_h` and canceling `m_p` proves

`E |Z_major+Y|^p >= E |Z_minor+Y|^p`.                       (4.1)

At `p=2`, direct orthogonality gives sign equality, also with independent radial noise (which has mean zero). Therefore (4.1) holds for every `p>=2`.

Importantly, this proves the property needed for arbitrary joins. We do not claim that convolution by radial noise preserves the entire AP-admissible scalar class. We prove directly that every radial convolution of the particular power test yields an AP-admissible scalar function; the aggregate of all other signed blocks is itself admissible noise at every replacement step.

## 5. Robust comparison for the AP-free blocks

For completeness, the two-layer-simplex proof in [Proof 01](01_circuit_obstructions.md) works for every continuous radial planar function `Phi` such that `Delta^2 Phi` is a nonnegative distribution. Smooth radial positive mollification preserves these properties and converges uniformly on compact sets.

For smooth `Phi`, define circle and disk averaging operators `M_s,D_s` at radius `sqrt(s)`. The circle/disk identity is

`partial_s M_s Phi=(1/4)D_s Delta Phi`.

It follows by the divergence theorem. All these convolution operators commute, so for `i!=j` the mixed derivative of the independent circular-sum mean is

`partial_(s_i)partial_(s_j) [product_k M_(s_k) Phi](0)`

`= (1/16)[D_(s_i)D_(s_j) product_(k!=i,j) M_(s_k) Delta^2 Phi](0) >=0`.

Thus the multiradius mean is lattice-supermodular. Conditional on the common layer angle of a two-layer simplex, its squared circle radii are `a_j^2+b_j^2+2 sigma_j a_jb_j cos(t)`. Pairing `cos(t)` and its negative, and applying the join/meet inequality, aligns every `sigma_j` positively. This proves sign comparison for every radial bisubharmonic test, and mollification handles the continuous distributional case.

The center-free-cross identity in [Proof 01](01_circuit_obstructions.md) transfers this entire radial-test comparison, because averaging an extra common rotation makes its radial expectation identical to the two-layer-simplex expectation for the same real coefficient arrays. No power-specific step is used.

For any `p>2`, the power test has

`Delta^2 |z|^p=p^2(p-2)^2 |z|^(p-4)>=0`

as a locally integrable planar distribution. Both boundary fluxes at zero vanish, so no delta contribution is omitted. If `Y` is arbitrary bounded independent radial noise, the function

`Psi(z)=E|z+Y|^p`

is continuous and radial, and `Delta^2 Psi` is the convolution of a nonnegative distribution with the reflected probability law of `Y`, hence is nonnegative. Consequently the prism and center-free-cross sign comparisons remain valid after adding `Y`. At `p=2` they give equality. A singleton likewise has sign equality after adding radial noise.

## 6. Affine-join replacement and full real majorants

For an integer-frequency configuration partitioned into blocks, insert an independent uniform common phase. Its augmented joint character law is Haar measure on the compact subgroup of the phase torus whose annihilator is

`L=ker_Z[(1,n): n in Gamma]`.

By the affine-join hypothesis, `L` is the direct sum of the labelled component relation lattices. The product of the corresponding block Haar laws has exactly the same Fourier coefficients as the full joint law: one on `L`, zero off `L`. The measures are therefore equal. This proves that the block polynomial values are independent.

Every block law is rotationally invariant, because every augmented relation in that block has coordinate sum zero, so its phase subgroup contains the diagonal circle. The independent global phase inserted initially changes no radial moment. Configurations with identical labelled affine relation lattices have identical augmented phase laws, proving the stated transfer without an unjustified unimodular coordinate-change assumption.

Fix coefficient magnitudes and an arbitrary real sign pattern. During replacement of one block's signs by positive signs, the sum of every other signed block is bounded independent radial noise. Sections 4 and 5 show that this replacement cannot decrease the `p`th absolute moment. Repeating through the finite blocks proves the full sign comparison for all `p>=2`.

Finally, for `p>=1` the `p`th absolute moment is convex in the real coefficient vector. Every vector with `|a_n|<=A_n` lies in the convex hull of the sign vertices of this coefficient box. All vertices are bounded by the all-positive vector, so Jensen's inequality proves the arbitrary-majorant statement. Coefficients equal to zero and removal of frequencies cause no problem.

## 7. Scope and provenance

This proof extends the accepted low-exponent sufficient class to all affine joins of AP triples and the AP-free blocks. It does not supply a complete classification in `2<p<3`: the remaining mass-two blocks are centered crosses with at least two endpoint pairs, and mixtures containing those blocks.

The circle/disk averaging mechanism is credited to Baernstein–Culverhouse, *Majorization of sequences, sharp vector Khinchin inequalities, and bisubharmonic functions*, Studia Math. 152 (2002), especially Lemma 1 / equation (3.2), DOI https://doi.org/10.4064/sm152-3-3. The present proof of Lemma 1 and the weaker AP-admissible closure argument are self-contained. No external hypergeometric identity or unverified source is required for their validity.
