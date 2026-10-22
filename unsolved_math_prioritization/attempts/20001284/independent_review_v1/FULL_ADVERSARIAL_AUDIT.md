# Fresh independent adversarial audit: 20001284

Date: 2026-10-03 UTC. Independent AI mathematical review.

Publication copy: nonmathematical identifying and coordination metadata omitted. All mathematical findings, source qualifications and nonblocking clarifications are retained.

## Verdict

**PASS for the stated partial results and UNSOLVED 5/5 disposition.** No mathematical repair is needed for the principal cutoff-independent C² local theorem. There are two low-priority wording clarifications below. **HOLD any promotion to a global solution, unrestricted-regularity theorem, or historical-novelty claim.** This is an independent AI mathematical audit, not human peer review or formal verification.

The reviewer was separate from the contributing calculation and independently derived the decisive analytic estimate and the other four calculations. The contributing file was read as part of adversarial review; its verdict was not used as a substitute for checking the proof. The frozen author packet was not modified.

## Audited artifact and checks

- Frozen directory: `deliverable/`, 14 physical files.
- `AUTHOR_MANIFEST.json` SHA-256: `936f36854d5782e7815ddea50158a4404a23dcbf4c410d80af9513ce7593b357`.
- Independently matched byte counts, SHA-256 hashes, and Git blob hashes of all 13 manifest-listed payload files. The manifest is the fourteenth file.
- Replayed `python3 verify_exact.py`: PASS, 228 exact assertions, SymPy 1.14.0. The groups and counts exactly match `EXACT_CHECKS.json`.
- Independently checked the three supplied source PDF hashes against `SOURCE_MANIFEST.json`; all match.
- The local WIP receipt names commit `ca4bbc2728da3198ca999e709be96f84d52eac28` and the correct manifest. There is no Git working tree here. This review did not independently read the remote commit, remote queue, branch history, or PR state; those require a separate final publication check.
- The full imported corpus files are absent from this review directory; only extracted target records are present. I checked their content against the actual source problem, but did not independently certify the stated full-corpus hashes or historical prior-attempt search.

## 1. Critical local theorem: PASS

### Exact geometry and derivative

On a unit-speed section great circle, set a=ρ, b=ρ_s, c=ρ_ss and q=(a²+b²)^(1/2). The radial boundary curve has speed q. Differentiating its length in direction h gives the integral of (a h+b h_s)/q. Since ρ is positive C², b/q is C¹ on the circle and periodic integration by parts is legitimate for C¹ h. Direct differentiation gives

(b/q)_s=(a²c−ab²)/(a²+b²)^(3/2),

hence the exact zeroth-order weight is

w=a(a²+2b²−ac)/(a²+b²)^(3/2).

There is no missing geodesic term: along the incidence circle t=θ×u is unit speed and its spherical covariant acceleration is zero, so ρ_ss=Hess_{S²}ρ[t,t]. The proposed off-incidence extension is therefore correct. It is unnecessary to interpret its off-incidence values geometrically.

### Independent separated-variable estimate

Write L_l=l(l+1). For a real L²-orthonormal spherical-harmonic basis, the unnormalized Funk transform has multipliers λ_l=2πP_l(0). For l=2j, |λ_l|=2π binom(2j,j)/4^j; odd degrees vanish. Since the norm of H^(1/2) squares Fourier coefficients with weight (1+L_l)^(1/2), the relevant singular value is (1+L_l)^(1/4)|λ_l|. It is bounded above and below on even degrees. The packet's elementary binomial bounds yield its conservative constants c_F=π and C_F=2√2π. I checked the induction inequalities and the j=0 case. In particular, no L²-to-L² bounded inverse of F is being used.

For b(θ,u), put M= sup |(1−Δ_θ)²b| and expand only in θ. Twice moving 1−Δ_θ onto the harmonic gives

||a_lk||∞ ≤ √(4π) M (1+L_l)^(−2).

No derivative in u appears. The addition theorem gives sup bounds on Y_lk and its gradient. The product rule in the exact H¹ norm, followed by Hilbert-scale interpolation between L² and H¹, gives

||M_{Y_lk}||_{H^(1/2)→H^(1/2)} ≤ A_l,
A_l=√((2l+1)/(4π)) (1+√L_l).

Thus every term Y_lk F(a_lk h) has H^(1/2) norm at most C_F A_l ||a_lk||∞ ||h||₂. Summing the 2l+1 values of k costs O(l), the multiplier costs O(l^(3/2)), and coefficient decay supplies O(l^(−4)). The resulting degree summand is O(l^(−3/2)), which is summable. This proves the required bounded operator by an absolutely convergent operator-norm series. The packet's explicit majorant C_F[1+9√3(1+√2)] follows from the three stated elementary inequalities and Σ l^(−3/2)≤3.

The corresponding scalar series has degree bound O(l^(−5/2)) and converges uniformly for the continuous weights used in the theorem. For continuous h one may therefore interchange it with the finite great-circle integral. The sum also converges in H^(1/2); uniqueness of the L² limit identifies the two. Density of smooth even functions extends the operator to L²_even. This is a legitimate treatment of the lack of classical traces of arbitrary L² functions on individual circles.

### Why C² is enough

After scaling ρ=Rr, the extended weight depends only on r(u), ∇r(u), Hess r(u), and θ×u, through a smooth finite-dimensional formula with denominator bounded away from zero. Differentiation in θ changes θ×u and never differentiates any of these fields in u. At the constant ball, w=1 on the full product sphere. The finite-dimensional mean-value estimate therefore controls four θ derivatives of w−1 by C||r−1||C². The use of C⁴ in the normal variable is not a disguised requirement of C⁴ or C⁶ spatial regularity. This remains valid for C² radial functions with merely continuous Hessian.

The extension is separately even in θ and u when ρ is even, so both the data and the perturbation operator preserve the required even spaces. Dependence on R cancels exactly. All constants are independent of harmonic cutoff.

### Two-body averaging and function spaces

For h=ρ₁−ρ₀ and ρ_t=ρ₀+t h, the segment stays in the stipulated C² ball and remains positive. Pointwise differentiation under the circle integral and the fundamental theorem of calculus give

P(ρ₁)−P(ρ₀)=Fh+T_{bbar}h,
bbar=∫₀¹(w_{ρ_t}−1)dt.

The averaged weight has M(bbar)≤C_*ε. The preceding lemma identifies this equality in H^(1/2), with no approximation that demands higher spatial derivatives. Alternatively, the formula's continuous dependence on the C² parameters supplies the required Bochner continuity. Consequently

||P(ρ₁)−P(ρ₀)||H^(1/2) ≥ (π−K C_*ε)||h||₂.

For ε<min(1/2,π/(2KC_*)), the claimed inverse stability follows with C=2/π. This is a two-point estimate on a C² neighborhood, not an inverse-function theorem applied to a nonexistent open L² domain for P. The derivative's bounded L²→H^(1/2) extension is also an isomorphism by a Neumann-series argument after composing with F^(−1).

The positive claim is exactly for arbitrary positive even C² radial functions in one common normalized neighborhood of a radius-R ball, in R³, with all plane normals and H^(1/2) data norm. No uniform L²-data stability, C¹ neighborhood, global injectivity, or non-even injectivity follows. Small C² neighborhoods are themselves strictly convex, even though convexity is not a separately used hypothesis.

### Adversarial control on rough weights

The support file's warning about L∞ alone is correct. For even N, b_N=Re(u₁+i u₂)^N has sup norm 1, L² norm of order N^(−1/4), and Funk inverse multiplier of order N^(1/2). Applying the weight E_N=εb_N to the constant input gives an inverse-composed output/input ratio of order εN^(1/4). Thus positivity and pointwise smallness do not provide the asserted operator perturbation bound. The actual proof uses precisely the missing normal-variable regularity.

## 2. Midpoint defect: PASS

Independently rationalizing |X|+|Y|−|X+Y| gives

2 det(X,Y)² / [(|X|+|Y|+|X+Y|)(|X||Y|+X·Y)].

Positive first coordinates ensure the denominator is nonzero. Under the stated r,Q bounds, it is at most 8Q³, and det(X,Y)=ρ₀ρ₁∂s log(ρ₁/ρ₀). This yields the stated circle lower bound r⁴/(4Q³). Incidence disintegration has no extra factor: at fixed u the integral of the squared directional derivative over unit tangent directions is π|∇g(u)|². The mean-defect coefficient πr⁴/(4Q³) and homothety equality case are correct.

Equal endpoint data do not force midpoint equality. Strict convexity of the mean functional therefore does not solve the global problem. The packet correctly identifies this missing implication.

## 3. Six-plane quadratic model: PASS

I recomputed F(uᵀAu)(θ)=π(tr A−θᵀAθ) and solved the six equations; both the diagonal and off-diagonal inverse formulas are correct. The entrywise bounds imply ||A||F≤√123/(2π)||p||∞, using all six off-diagonal Frobenius contributions.

On the radius-r chart, |q_H|≤||H||F, |q_H'|≤2||H||F, a≥R−r and |b|≤2r. The two first-variation errors integrate to 4πx² and 8πx respectively. At r=R/100, C₀L(r)<4776/9801<1/2, yielding the stated stability constant √123/π. Averaging the derivative error is valid on the entire closed convex chart ball; there is no unjustified replacement of an integral's norm by the integral of lower bounds. The Hessian and strict-convexity bounds also check. The six-measurement minimum follows correctly from invariance of domain for continuous injectivity on an open six-dimensional chart.

## 4. Finite-plane invisibility: PASS

The product of squared linear forms is nonzero, even, analytic, and vanishes identically with its circle-tangential derivative on every measured plane. The resulting sections equal those of the ball exactly. Treating it as a product of d=2N unit linear forms gives extrinsic gradient ≤d and Hessian ≤d(d−1); Euler's identity then gives the spherical Hessian bound d²=4N².

The radial convexity form satisfies Qρ≥ρ(ρ−4εN²)I. The amplitude ε<R/(4N²) is sufficient, and ε<R/(8N²) supplies the claimed R²/2 margin. For s=1/ρ, Hess s+sI=ρ^(−3)Qρ. Its homogeneous extension has positive tangent Hessian and a radial zero direction, hence is convex off zero; lines through zero have compatible left/right slopes because s>0. Its unit sublevel set is Kρ. Thus the strict convexity certificate is valid, not merely local boundary convexity.

Some unmeasured circle has larger perimeter: choose a point with h>0 and a circle through it. Continuity makes h positive on a circle arc, and directly sqrt(ρ²+ρ_s²)≥ρ≥R, strictly on that arc. This is also an independent proof avoiding the invoked planar perimeter-monotonicity theorem. Equality on finitely many normals is not equality on all normals.

## 5. Antipodal switching and symmetry barrier: PASS

The cap profile is smooth through its boundary, analytic in the cap, and strictly maximized at its center. The numerical separation bound ensures disjoint supports. The perimeter integrand splits into the base R and single-bump increments; replacing one center by its antipode preserves each great-circle integral exactly. Small positive δ gives strictly convex smooth bodies.

The noncongruence proof also survives the translation challenge. An isometry carries an open radius-R sphere patch to a radius-R sphere patch. A cap-interior patch cannot lie on such a sphere: analyticity extends the sphere identity over that cap, and the bump's vanishing boundary derivatives force the purported sphere center to be parallel to every cap-boundary point, hence zero, which contradicts the positive bump. An exterior patch has center zero. Thus the isometry has zero translation. The distinct bump heights then force the orthogonal part to fix e₁,e₂,e₃, making it the identity, which cannot switch v to −v.

The bodies are not origin symmetric. Their radial evenizations coincide exactly, and switching antipodal profiles of an already even radial function changes nothing. This is a valid obstruction for this construction family, not a theorem that every possible symmetric collision construction fails. The literature credit is appropriate.

## Source scope independently checked

I opened the named primary sources directly; I performed no new literature-search campaign.

- [AIM workshop problem list](https://aimath.org/WWN/mahlerduality/mahlerduality.pdf), printed p. 3, Problem 20: matches the all-central-plane perimeter question for origin-symmetric star bodies in R³. The catalogue's finite-dimensional title does not narrow it.
- [Gardner update version 3.0](https://faculty.gardner.wwu.edu/Update%20Version%203_0.pdf), dated September 14, 2026, printed p. 12: continues to list the general problem as open, while distinguishing revolution and polytope special cases and nonsymmetric collisions.
- [Rusu thesis](https://people.math.sc.edu/howard/Theses/rusu.pdf), Theorem 16 and Corollary 17: an analytic one-parameter expansion about the ball, absolutely convergent in C¹, with every body's data equal to the ball's. It does not supply the packet's arbitrary two-body local theorem.
- [Yaskin paper](https://www.math.ualberta.ca/~vladyaskin/papers/Perimeters.pdf), theorem on preprint p. 2: origin-symmetric convex polytopes, all central k-sections, 2≤k≤n−1; no arbitrary-star-body theorem.
- [Ryabogin–Yaskin paper](https://www.math.kent.edu/~ryabogin/RYversion4.pdf), Theorem 2.4: nonsymmetric noncongruent convex examples with equal section intrinsic volumes, including smooth positive-curvature examples. This supports the credited mechanism, not an origin-symmetric counterexample.

The exact live catalogue detail page remains explicitly unverified in the packet; I did not retry it. Historical novelty remains unestablished. No inconsistency with the official source's global open status was found.

## Nonblocking clarifications

1. The contributing calculation allows E to be merely measurable in x and uses an essential supremum in x, but then says its series is uniformly convergent in (x,u) and identifies every circle integral. In this generality write "essentially uniformly outside a fixed x-null set" and identify the original integral for almost every normal. Incidence Fubini gives the a.e. statement; L²/H^(1/2) spaces use a.e. classes. Alternatively restrict this lemma to jointly continuous E, as Attempt 1 already does. The actual geometric weights are jointly continuous, so this is not a defect in the main theorem.
2. In Attempt 2's final discussion, "smaller perimeter data" can be made unambiguous as "no larger for every normal, strictly smaller for some normals, and strictly smaller in mean" for unequal equal-data endpoints. Strict decrease for every normal is neither proved nor required.

## Publication and queue conclusion

The original global problem remains **UNSOLVED**, with **five substantive attempts completed (5/5)**. The strongest audited partial result is the stated scale-uniform, cutoff-independent C²-near-ball two-body uniqueness and L²/H^(1/2) stability theorem. The other four attempts are correctly scoped partial results or diagnosed failed global routes. Keep the no-novelty and no-formal-verification caveats. The 228 finite controls supplement but do not replace the analytic proof. A separate remote identity/diff and authorization check is still needed for any publication action.
