# Independent audit of Function Theory Problem 5.38, four-turn candidate

2026-10-02. **Mathematical verdict: PASS for both classical sharp comparisons under the explicitly corrected nonnegative initial-derivative hypothesis.** No substantive analytic gap was found. There is one nonblocking argument-wording clarification, recorded below.

**Original-source disposition: the requested substantial proof simplification remains unverified.** The two inequalities are known results, not new discoveries. This packet gives reviewed alternative proofs with explicit algebraic simplifications, but the available historical comparison does not establish that it resolves the source's qualitative request. Do not promote correctness of the known inequalities into a full source-literal solution.

This is an independent AI mathematical audit, not a formal proof-assistant verification, a human referee report, or a historical novelty certificate. No publication is performed by this review.

## Frozen package

Repository checkpoint:

https://github.com/AlecKriebel/Math/commit/52b319cfab24b188150cabadd097f83ea876eec4

The four complete proof files read have these SHA-256 hashes:

- TURN_1.md: ae3a685bb9fc801c1eb1e91a71b047ea16a4b6ba830bcfb18af6855048f3712a
- TURN_2.md: ede8da0fd9cce2ee74ea16e4ea8c2d47ae41e363c34c0c952a7724b2e0961ea6
- TURN_3.md: 23067aab48a2b6780615471dfb46f4792fabedce5e2b34585b0d09a000abf0dc
- TURN_4.md: eb2e4f099fdd367110276d7ecc2e35213d7e34513d14236f3cdeb86047c61062

CANDIDATE_README.md: 91ea6510cdb3b43c150bd378724dab96970b631cb2e04bb2d1c41d26a2b50203

SOURCE_SCOPE.md: 033795d01ae172fde8df7b5d82b4fca3f1355622ddeab9b46855a6f1f674858c

source_manifest.json: 10b86e967385b3e715320b3e6803e2b93fa1665f3c24727d5912c1392d8805e2

## 1. Exact hypotheses and source intent

The corrected theorem is: F is normalized holomorphic univalent on the unit disk, g=F composed with a holomorphic disk self-map phi, phi(0)=0, and a=phi'(0) is real with 0<=a<=1. Then the modulus comparison holds through R=(3-sqrt(5))/2 and the derivative comparison through rho=3-sqrt(8), both sharply. Neither g nor phi must be univalent.

I independently reopened Hayman–Lingham, Problem 5.38 and its update, https://arxiv.org/pdf/1809.07200v2, PDF p.100. It asks for simpler proofs of both known sharp inequalities. Its displayed real-only hypothesis is insufficient: phi(z)=-z and the Koebe function violate both comparisons at every negative real evaluation point. The packet gives this exact counterexample and transparently adopts the classical nonnegative normalization. This diagnosis does not itself solve the intended simplification request.

Simultaneous rotation of F and phi preserves that normalization and permits evaluation at positive r. Rotating phi alone would not justify changing an arbitrary complex or negative a into the required one while retaining the same pointwise comparison; the proof does not do so.

## 2. Derivative reduction and boundary certificate

### Exact jet and two-point bound

Schwarz–Pick gives phi(z)=z(a+omega(z))/(1+a omega(z)) with omega(0)=0 and |omega(z)|<=|z|. At r, Schwarz–Pick for omega(z)/z gives the stated derivative disk, including its radius and its center c/r. The disk is attainable by disk automorphisms and their contractions; the boundary |c|=r correctly collapses to a singleton. Differentiating phi gives the center numerator a+2c+a c^2, exactly as claimed.

The Koebe transform is normalized and univalent. Direct differentiation gives the factor (1-r^2)^2/|1-rw|^2 multiplying ordinary derivative distortion at the pseudohyperbolic displacement. The conversion to the hyperbolic derivative Q times ((1+delta)/(1-delta))^2 is exact. The optional attainment discussion is also valid, but the lower-bound proof only needs the upper bound. F' never vanishes, so the final maximum-modulus step for g'/F' is legitimate.

### Small a and the boundary circle

The elementary bound Q<=(r+t)/(1+rt) follows by factoring the numerator and denominator of the Schwarz–Pick triangle estimate. The estimate for the maximum delta is valid even when a-r^2 is negative; the factored derivative-sign expression remains positive. At rho this yields the claimed small-a bound, and its gap factors as (1-a)(3a^2-14a+3), positive on [0,1/6].

On |c|=rho, the formulas for Q^2 and delta^2 have the correct constants 8/9 and 32. The logarithmic derivative of the product is nonnegative precisely when

    (4/9)a(1-a)(1-v)>=delta[D^2-(8/9)(1-a^2)].

Both sides are nonnegative in the stated range. Therefore the subsequent squaring is reversible there. The polynomial P, its strictly negative second v derivative, and both endpoint factorizations check. Convexity of the two quadratic factors in a makes their endpoint-negative values sufficient. The endpoint Q=0 at a=1/3,v=-1/3 is correctly treated by continuity, rather than by a logarithm at zero. The final positive endpoint satisfies the factorized bound with numerator (1-a)^2(a+11).

### Interior-defect monotonicity

Starting with the full complex c, the squared-modulus and denominator identities produce exactly Q=(T+b)/(D+b), with the stated definitions of k,k0,v,D,b,T. There is no omitted derivative-disk term. The displacement odds also reduce to the claimed expression.

At fixed a,v, every k between k0 and its final feasible value remains feasible because |v|<=sqrt(1-k^2). The radicand is therefore nonnegative along the path. For positive radicand, direct differentiation gives the displayed derivative. Its bracket is at most

    D/(2k0)-k<=1/sqrt(2)-2sqrt(2)/3=-sqrt(2)/6<0.

Here D+b>=T>0 and D<=4/3 justify the two inequalities. A possible zero radicand can occur only at a feasible path endpoint; continuity covers it. As k increases, b increases, so delta also decreases. Hence the product is dominated by the boundary jet with the same a,v. All limiting cases a=0, a=1, c=0, and |c|=rho are covered by the stated separate arguments or continuity.

The derivative proof is complete. Its sharpness variation is correct: for the displayed Koebe/Blaschke family, the derivative with respect to a at a=1 equals (r^2-6r+1)/(1+r)^2. It is negative for rho<r<1, so a sufficiently close to one from below gives a strict violation beyond rho.

## 3. Modulus proof: Grunsky constant, branch, and phase geometry

### Grunsky consequence

I directly inspected the saved image of printed p.105 of Duren–Schiffer's primary paper, https://msp.org/pjm/1988/131-1/pjm-v131-n1-p06-p.pdf. It confirms the precise classical quadratic inequality with weights 1/n and the displayed exterior logarithmic kernel. The local PDF SHA-256 is 698b00f1de7bbafd1f87038c2faf2ede815612a89f46435670dde110be0133cf.

For an odd normalized univalent h, G(zeta)=1/h(1/zeta) is an odd normalized exterior function. Subtracting its kernel at (u,-v) from its kernel at (u,v) cancels the one-variable inversion factors. Oddness removes coefficients with m+n odd, leaving exactly -2 times the odd-odd sum. Symmetric bilinear polarization is valid over complex vectors and gives norm bound one. The odd-index sums are half of L(t), so the final constant is exactly sqrt(L(|u|^2)L(|v|^2)), with no missing factor of two.

The logarithmic kernel has the analytic branch inherited from its convergent bidisk series. Apparent u=plus-or-minus-v singularities are removable by univalence, oddness, and nonvanishing derivatives. At the actual points used in the proof none of those degeneracies occurs. Infinite truncation is justified by convergence in the weighted sequence norms.

The square-root transform of F is holomorphic because F(z)/z has no zeros. Its injectivity follows from F's injectivity and oddness exactly as stated; thus it is an admissible h.

### Value region and phase

The Schur-value inequality expands to the stated quadratic in a. If s>r^2, its nonpositivity forces a>0 and X>0. Its discriminant gives the lower bound X0. The equivalent imaginary-part condition and the radial-segment containment follow algebraically; no unjustified sufficiency claim for the enlarged region is needed. At s=r the only permitted value is w=r.

For q=(sqrt(r)-sqrt(w))/(sqrt(r)+sqrt(w)), Re q>0 since s<r, and its angle to the imaginary axis has the stated tangent square. Replacing X by X0 preserves the correct inequality direction. Both factorized comparisons proving 2r^2(s+X0)>=s(r+s)^2 are valid on r^2<s<r<R. The positivity condition r<sqrt(2)-1 follows from R<sqrt(2)-1. Concavity of arctan then gives the lower bound on gamma.

If |F(w)|=|F(r)|, the transformed ratio Z is nonzero and purely imaginary. Therefore every logarithm of Z/q has imaginary part whose absolute value is at least gamma. The Grunsky upper bound contradicts this, because L(t)/t increases and the scalar separation atan(sqrt(5)/2)>(1/2)log 5 is rigorously established by the displayed rational bounds. No floating-point estimate is needed.

**Minor wording clarification:** TURN_4 section 4 says the minimum absolute value among the arguments of the fixed Z/q “is gamma.” Equality need not hold for its fixed imaginary sign; the minimum can instead be pi/2+|arg q|. The required and valid statement is “is at least gamma.” The preceding inequality in the same paragraph already states the needed bound, so this is not a gap in the proof. The author was asked to make this one-sentence clarification in a later public version.

Finally the inner disk is strictly controlled by ordinary growth for r<R. A violation in the outer region would create an equal-modulus point along the admissible radial segment, already ruled out. Continuity gives the closed radius R. The classical phi(z)=z^2 Koebe example proves sharpness. This proves the full modulus half with no extra univalence assumption on g.

## 4. Independent controls and preservation

All four author scripts were rerun from copies, so the frozen proof directory was not modified by scripts that write their own receipts. Results: 44,182 turn-1 exact assertions, 17 turn-2 symbolic checks, 9 turn-3 checks, and 14 turn-4 checks. The saved turn-2/3/4 receipts reproduce byte-for-byte.

The separate `independent_controls.py` imports no author code. It independently verifies 22 exact symbolic or rational identities, including direct differentiation of the radical defect expression, the angular log-derivative sign conversion, the odd Grunsky kernel on an explicit univalent odd test function, both geometric factorizations, and the sharpness variation. It also performs 3,409 separately labeled 90-digit numerical falsification checks on raw complex jets and phase geometry. Those diagnostics are not proof of the universal inequalities. The analytic audit above addresses the full domains and boundary cases.

Run the portable script with

    python3 independent_controls.py --proof-dir PATH_TO_FROZEN_PROOF_DIRECTORY

The receipt binds all four proof hashes. Python requires SymPy and mpmath, both already present in the audited environment.

## 5. Historical comparison and source-goal verdict

Duren's 1977 *Subordination* survey, pp.25-27, was inspected in its indexed reproduction, with the displayed-formula OCR limitation retained. The official chapter identity is https://doi.org/10.1007/BFb0096821. Its description of Shah's modulus proof already uses the Rogosinski value region, Koebe growth on the inner disk, an equal-modulus contradiction outside, the odd square-root transform, and Lebedev's two-point inequality. Thus the candidate's principal modulus architecture is classical. Its two explicit positive factorizations make the missing phase estimate checkable, but do not alone establish a historically new mechanism or a substantial simplification relative to the unrecovered original calculation.

Barnard–Pearce's author manuscript, https://kjpearce100.github.io/mathwebsite/papers/bp1.pdf, pp.2-4, was read directly. It records Campbell's Schur/two-point setup, small/large-a split, and the threshold 1/6 for the alpha=2 range. The candidate specializes that setup and adds a clean interior-defect monotonicity calculation plus a concise concavity certificate. This is a concrete presentation improvement over the multiregion framework shown there; it is not evidence of a new sharp inequality.

The complete Shah originals and Campbell III were not retrieved. The four-turn package is also a research development, not a typeset side-by-side final proof comparison. Consequently neither a substantial reduction in the original proof's complexity nor superiority to every existing short proof is established. Nor did this audit verify that the candidate merely reproduces an already-published short proof verbatim or in full detail. It would therefore be premature both to label a new source-goal solution and to declare the simplification request already solved by a specifically identified identical proof.

The appropriate split disposition is:

- Both corrected classical inequality proofs and both sharpness claims: mathematically verified on this audit
- Literal real-only source statement: false, with the packet's counterexample correct
- New inequality or historical priority claim: not made and not justified
- Exact qualitative request for substantially simpler proofs of both known inequalities: still unverified at this four-turn checkpoint

No substantive mathematical repair is required beyond the nonessential argument-wording clarification. A final turn may address the source-level simplification objective, but correctness alone must not substitute for that objective.
