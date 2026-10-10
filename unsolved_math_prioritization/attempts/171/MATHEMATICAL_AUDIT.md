# Independent audit: rotation-only pyjama lower bounds

## Decision

**ACCEPT as a correct, self-contained partial quantitative result. No mathematical correction is required.** The accepted result concerns closed periodic strips, rotations about the origin only, and coverage of every point of the entire plane. It does not determine the asymptotic order of the covering number. Novelty is not certified.

The distributed [mathematical report](MATHEMATICAL_REPORT.md) has 9,809 bytes and SHA-256 `0e4d77d843d3b9d6396a12b2ec0e2e6a20b0d7a0088d314b281bcc4f76946173`. Audit date: 2026-10-10 UTC. This edition preserves the complete accepted mathematical reasoning, with the two optional editorial clarifications described in section 7. This AI-assisted, unrefereed audit is not external human peer review, journal acceptance or formal proof-assistant certification.

The accepted conclusions are, for every `0 < epsilon < 1/2`,

\[
N(\varepsilon)\geq
\left\lceil\max\left\{
\frac{\pi}{2\arcsin(\varepsilon/(1-\varepsilon))},
1+\frac1{2\varepsilon}\right\}\right\rceil,
\qquad
\liminf_{\varepsilon\downarrow0}\varepsilon N(\varepsilon)\geq\frac\pi2.
\]

Also accepted: the exact central-disk angular-gap criterion; the credited equality `N(epsilon)=3` for `1/3 <= epsilon < 1/2`; `N(epsilon)=1` for `epsilon >= 1/2`; and `N(epsilon)>=4` for `0 < epsilon < 1/3`.

## 1. Problem identity and model

The audited formulation is

\[
P_u(\varepsilon)=\{x\in\mathbb R^2:\operatorname{dist}(u\cdot x,\mathbb Z)\leq\varepsilon\},\qquad |u|=1.
\]

If `R` is a rotation and `u=R e_1`, then `R P_{e_1}=P_u`. Thus these are exactly the allowed rotations; no translation, rescaling, or phase shift is present. Negating `u` leaves the set unchanged because the integer lattice is invariant under negation. Parallel and antiparallel normals must therefore be identified when a proof requires invertible pairs.

Target 171 has corpus identifier `GREEN-083`; the original source is Green's **Problem 41**, not Problem 83. The original statement on printed p. 21 specifies rotation about the origin, the inequality `dist(x,Z) <= epsilon`, and coverage of `R^2`. These details were visually verified in the rendered primary PDF. The original source is [Ben Green, 100 Open Problems, Problem 41](https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf).

The lower-bound arguments are conditional on an arbitrary finite cover and do not need an existence theorem. Calling the minimum `N(epsilon)` is consistent with the known finite-existence result of [Freddie Manners, A solution to the Pyjama Problem](https://arxiv.org/abs/1305.1514). The author's core lower-bound proof does not rely on the proof of that theorem.

## 2. Theorem 1: first-circle obstruction

### 2.1 Excluding all noncentral strips

For `epsilon < r < 1-epsilon` and `|x|=r`, Cauchy–Schwarz gives `|u dot x|<=r`. If `k` is a nonzero integer, then

\[
|u\cdot x-k|\geq |k|-|u\cdot x|\geq1-r>\varepsilon.
\]

Consequently the intersection with this circle is exactly that of the central strip `|u dot x|<=epsilon`. This works for every orientation simultaneously. The interval of permitted radii is nonempty precisely under the stated assumption `epsilon<1/2`. There is no assertion that the same simplification holds on larger circles.

### 2.2 Angular measure and all-point coverage

Writing `u=(cos theta,sin theta)` gives `|cos(t-theta)|<=epsilon/r`. There are two antipodal closed arcs, each with angular length `2 arcsin(epsilon/r)`. Because `0<epsilon/r<1`, no arc is the full circle and the total measure is exactly `4 arcsin(epsilon/r)`. A whole-plane cover covers every point of the test circle, so finite subadditivity yields

\[
2\pi\leq4n\arcsin(\varepsilon/r).
\]

Disjointness is not assumed. Repeated directions only make this necessary inequality weaker, which is harmless.

### 2.3 Limiting radius, ceiling, and asymptotic constant

The inequality holds for every radius in the open interval. Its continuous limit as `r` increases to `1-epsilon` yields the weak real bound in (1). One need not exhibit a maximum radius where no noncentral strip touches. Since `n` is an integer, `n>=A` implies `n>=ceil(A)`. If `A` happens to be an integer, the proof gives that integer, not the next one; the manuscript correctly keeps weak inequalities.

Put `q=epsilon/(1-epsilon)`. Then

\[
\varepsilon\frac\pi{2\arcsin q}
=\frac\pi2(1-\varepsilon)\frac q{\arcsin q}
\longrightarrow\frac\pi2.
\]

This proves the stated liminf. Multiplication by the ceiling changes this expression by less than `epsilon`, so there is no integrality issue in the limiting constant. It does not prove a limit for the actual covering number.

For positive integer `n>=2`, the arguments of the inverse sine and the comparison angle lie in its increasing branch. Solving `arcsin(q)>=pi/(2n)` gives exactly

\[
\varepsilon\geq\frac{\sin(\pi/(2n))}{1+\sin(\pi/(2n))}.
\]

This is equivalent to the displayed lower-bound inequality, not a sufficient condition for a whole-plane cover. The source wording describes it correctly as a necessary condition.

### 2.4 Tangency endpoint

At radius `1-epsilon`, only `k=1` and `k=-1` can contribute noncentral points; equality in the projection bound forces `x=+(1-epsilon)u` or `x=-(1-epsilon)u`. These are at most two isolated points for each strip. Their angular measure is zero. The optional direct endpoint argument is valid, and the proof as written already avoids depending on it.

### 2.5 Comparison with the volume lower bound

The ratio to `1/(2epsilon)` is

\[
\frac{\pi\varepsilon}{\arcsin(\varepsilon/(1-\varepsilon))}\longrightarrow\pi.
\]

Thus the improvement is an asymptotic multiplicative constant in a lower bound of order `epsilon^{-1}`. The qualifications in the report's volume-bound comparison and remaining-gap section are essential and correct. No conclusion that `epsilon N(epsilon)` diverges follows.

## 3. Proposition 2: exact central-disk criterion

Here an axis is the line down the middle of a strip, perpendicular to its normal. Its angle differs from the normal angle by `pi/2`; all cyclic gaps are unaffected by that common shift. Angles are considered modulo `pi`, which also removes antiparallel duplication.

At radius `r>epsilon`, membership in a central strip means that the directional distance to its axis is at most `a_r=arcsin(epsilon/r)` on a circle of circumference `pi`. For a finite set of axis points, the greatest distance from any direction to the nearest axis is one half of the largest successive cyclic gap `g`. A midpoint of a largest gap attains this distance. Hence coverage is equivalent to `g<=2a_r`, including equality because the intervals are closed.

The criterion handles `m=1`: its unique gap is `pi`, whereas `2a_r<pi` for `r>epsilon`, so one central strip cannot cover that circle. No empty set of axes occurs in a plane cover. Tied gaps and gaps crossing angle zero are handled by the cyclic endpoint definition.

For a fixed axis, reducing the radius decreases `|u dot x|` along each ray. Thus coverage of the radius-`1-epsilon` boundary by central strips is equivalent to coverage of the entire closed disk. Points of radius at most `epsilon` are in every central strip. This proves the necessity and sufficiency claim for the **central** strips. To derive necessity for the original periodic whole-plane cover, use the strictly smaller circles from Theorem 1 and continuity. No claim that the periodic sets have no noncentral tangencies on the outer boundary is needed.

Since the gaps add to `pi`, `g>=pi/m`, with equality for equally spaced axes. Consequently `m` equally spaced central strips cover the disk exactly when `m>=pi/[2 arcsin(epsilon/(1-epsilon))]`. This proves optimality of this specific local-disk obstruction. It is not an upper bound on the original plane-covering number.

## 4. Proposition 3: pairwise densities and the second moment

### 4.1 Distinct unoriented directions

After discarding duplicates modulo sign, a plane cover still covers and contains `m<=n` strips. If `m=1`, any solution of `u dot x=1/2` is uncovered when `epsilon<1/2`. Thus it is legitimate to assume `m>=2`. For two distinct remaining directions the row vectors are nonparallel, so the map

\[
A_{ij}x=(u_i\cdot x,u_j\cdot x)
\]

is invertible. This would fail for antiparallel duplicates; their explicit removal in the manuscript is indispensable and sufficient.

### 4.2 One- and two-strip mean densities

The one-dimensional periodic set `Z+[-epsilon,epsilon]` occupies a fraction `p=2epsilon` of each unit interval; boundaries have measure zero. Extending it freely in a perpendicular direction gives a bounded measurable indicator periodic under a full-rank lattice and mean `p`.

For a pair, in `A_{ij}` coordinates the product indicator is the product of two copies of that one-dimensional periodic indicator. The mean on `[0,1)^2` is exactly `p^2`. Pulling the square back gives a fundamental parallelogram of `A_{ij}^{-1} Z^2`. Its area and the integral are both multiplied by the same constant Jacobian `1/|det(A_{ij})|`; their ratio remains `p^2`. It is irrelevant whether the normal coordinates or the angle are rational.

### 4.3 Disk averages for a fixed lattice

Choose half-open fundamental parallelograms of a fixed finite diameter `D`. Every cell meeting the boundary of `B_R` lies within the annulus `R-D <= |x| <= R+D`, after replacing a negative inner radius by zero. This annulus has area `O(R)` as `R` tends to infinity. Tiling cells have disjoint interiors. Complete interior cells contribute their exact mean, while all boundary-cell contributions and the matching mean-area correction differ by at most a constant times that annulus area. Dividing by `pi R^2` proves convergence.

The implicit constant may depend on the pair of directions, especially for nearly parallel pairs. No uniformity in orientation is needed: the finite cover is fixed before taking `R` to infinity. There are finitely many first and second moments, so their limits may be added. No common lattice or independence of three or more indicators is used. The report explicitly states “any bounded measurable function”; every application is to a measurable periodic indicator.

### 4.4 Polynomial inequality and algebra

For a cover, `1<=M(x)<=m` holds everywhere, including strip boundaries, where `M=sum I_j`. Thus `(M-1)(M-m)<=0` pointwise. Its disk-average limit is

\[
mp+m(m-1)p^2-(m+1)mp+m
=m\big((m-1)p^2-mp+1\big)
=m(1-p)(1-(m-1)p).
\]

The factor `m(1-p)` is strictly positive under the exact assumptions. Therefore `(m-1)p>=1`, and `n>=m>=1+1/(2epsilon)`. The signs, coefficients, multiplicities of unordered pairs, and final passage from `m` to `n` are correct.

Combining the independent real lower bounds under one ceiling is valid. Near `epsilon=1/2` from below the second-moment bound is strictly greater than 2 and hence forces at least three strips. At `epsilon=1/2` the positive factor `1-p` vanishes; the proposition correctly excludes this endpoint, where one strip already covers the plane.

## 5. Boundary examples and the credited three-strip range

For `epsilon>=1/2`, every real number is within `1/2` of an integer. One unrotated set covers the plane, and zero sets do not, so the stated equality is exact.

Take the three unit normals separated by angles `2pi/3`. Their sum is zero. A point outside all three **closed** strips at `epsilon=1/3` would have all three fractional parts strictly between `1/3` and `2/3`. Their sum would then be strictly between 1 and 2. But the sum of fractional parts is an integer because the sum of the original three dot products is zero. This is impossible. The strict fractional-part inequalities are exactly the complement of closed-strip membership, and they correctly include the endpoint width `1/3` in the coverage result.

Two nonparallel normals cannot cover for any `epsilon<1/2`: solve their two independent linear equations with right sides `1/2`. If they are parallel, discard duplication and use the one-strip obstruction. Hence the equilateral upper bound is minimal on `1/3<=epsilon<1/2`.

For `epsilon<1/3`, `epsilon/(1-epsilon)<1/2`, so `arcsin(epsilon/(1-epsilon))<pi/6`; the first-circle bound is strictly greater than 3, and integrality gives at least 4. At equality `epsilon=1/3`, the bound equals 3, in agreement with the explicit cover.

The equilateral construction is expressly present on printed p. 2 of [Malikiosis–Matolcsi–Ruzsa, A note on the pyjama problem](https://arxiv.org/abs/1211.6138), with the closed-strip definition on p. 1. The source was submitted in 2012 and published in European Journal of Combinatorics in 2013. Its attribution in the report is correct. No exact classification of arbitrary three-direction configurations was supplied or audited.

## 6. Source scope and literature qualifications

### 6.1 Equally spaced axes really do fail below one third

[Malikiosis, Rotations by roots of unity and Diophantine approximation](https://arxiv.org/abs/1510.03645), Theorem 1.1 on printed p. 1, gives a point whose root-of-unity projections all have fractional parts in `(epsilon,1-epsilon)` whenever `epsilon<(p-1)/(2p)`, where `p` is the smallest odd prime divisor of the root order; for powers of two the threshold is `1/2`. Each odd prime satisfies `(p-1)/(2p)>=1/3`.

For `m` equally spaced unoriented axes, the corresponding normals, together with their negatives, form a globally rotated set of `2m`-th roots of unity. The common rotation can be absorbed into the test point, and negating a normal does not change its strip. Apply the source theorem with root order `2m`. It supplies an uncovered point for every `epsilon<1/3`. Thus the report's equally-spaced-direction obstruction follows from the actual stated theorem, without an endpoint mismatch. This is a credited result, not part of the manuscript's original proof.

### 6.2 Prior upper bound and open-versus-closed transfer

[Kravitz–Leng, Quantitative pyjama](https://arxiv.org/abs/2510.17744), Theorem 1.1 on printed p. 1, states a triple-exponential upper bound for `0<epsilon<1/10`. Although its abstract uses closed-set language, its main definition uses the open periodic interval `(-epsilon,epsilon)`. Enlarging each open strip to its closure preserves any whole-plane cover at the same width. The source's p. 2 records the explicit volume lower bound `1/(2epsilon)`. These statements and conventions were visually verified; the lengthy upper-bound proof was not independently audited here.

The paper's pp. 28–29 also discuss a rotation-plus-dilation variant whose lower bound cannot be improved by more than a factor of two. This creates no contradiction: the manuscript needs all normal lengths to equal one to obtain its common circle free of noncentral strips. Allowing arbitrary dilations removes that geometry. This is an additional scope check, not an extension of the theorem.

### 6.3 Novelty and status

The source inspections support the statement that the manuscript improves the *explicit cited volume bound* by an asymptotic factor of pi. They do not support a claim of globally best known or first discovered. An additional bounded search on 2026-10-10 used the phrases `"pyjama" "lower bound" arcsin`, `"pyjama" "lower bound" "circle"`, and `"pyjama" "second moment"`. It did not identify the same proof or formula. Search absence is not a novelty proof, and no claim depends on it.

The outcome remains **partial progress**. Neither this lower bound nor the credited upper bound identifies the order of `N(epsilon)`. No polynomial upper bound, superlinear lower-bound order, exact small-epsilon formula, or solution of a lonely-runner variant is established.

## 7. Corrections and limits of acceptance

- Required mathematical corrections: none.
- Required source-scope corrections: none.
- Optional editorial clarifications applied in this edition: explicitly repeat `0<epsilon<1/2` in Proposition 2 and insert “measurable” in the periodic averaging lemma in the proof of Proposition 3. Both were already clear from the governing context and applications; neither changes the mathematical argument or affects acceptance.
- All mathematical statements, proof steps, boundary examples and source qualifications are preserved.
- Scoped acceptance applies to the distributed report identified above. Any mathematical additions need their own review.

The mathematical justification is the complete reasoning above and in the distributed report. [SOURCE_METADATA.json](SOURCE_METADATA.json) records the public scholarly citations, PDF identities and the limits of recorded retrieval and inspection. No historical novelty, priority or current-openness certification is claimed.
