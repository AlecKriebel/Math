# Independent adversarial audit: rank 575 / 2305046

## Decision

**PASS as an unsolved, five-of-five investigation with eight valid partial propositions, subject to its explicitly imported results.** No solution, novelty, or exhaustive-current-literature certificate is warranted. No mathematical correction is required for the frozen package. Two nonblocking release/tooling notes and one optional wording clarification are recorded in CORRECTIONS.md.

Audited on 2026-10-04 UTC by a fresh reviewer who did not author the package. No helpers, remote writes, or edits to the frozen public package were used. The reviewed public manifest has SHA-256:

`ea9f5520cee6dbc749de5eceff5522140f37829a4b30859093823137a693e7f8`

This report concerns exactly those bytes. The public package is not a proof of Function Theory Problem 5.46. Its proper terminal disposition is **unsolved, 5/5, no novelty claim**.

## 1. Scope, definitions, and sources

The selected identifier and statement agree with the retained selected dataset record and Hayman–Lingham, printed p. 103, Problem 5.46. The derivative requirement is pointwise nonvanishing, not merely that the derivative is not identically zero. The collection's terse progress update is not an adequate summary of specialist work. [Hayman–Lingham, 2018 v2](https://arxiv.org/pdf/1809.07200v2).

I independently opened the cited scholarly sources through the web tool, read the relevant locations, checked the supplied three PDF byte hashes, and inspected rendered pages of the 2017 definitions/theorems and 2025 boundary discussion. The 2004/2005 result was read in the author-uploaded full text; no original-file hash or independently reconstructed proof is claimed for it. The original Hornblower and 2002 proofs were not reconstructed. The latter's official abstract was checked, and its criterion was checked in the 2017 paper. These are declared dependencies, not newly established results.

The definitions are consistent. Class A requires asymptotic values on paths ending at individual boundary points, densely in the circle. A general boundary path only needs modulus tending to one. An inverse tract uses nested components, with end given by the intersection of their **closures**. A full-circle end alone does not supply the additional arc-approximation property in the paper's definition of a global tract. The frozen text does not confuse these notions. [Barth–Rippon–Sixsmith, pp. 859–860](https://www.acadsci.fi/mathematica/Vol42/vol42pp0859-0873.pdf).

The Koebe-arc formulation really uses Hausdorff convergence of compact arcs. Theorem A supplies both directions of the equivalence needed here under membership in A, and the no-finite-point-asymptotic-value consequence in the interior of an arc-tract end. In the reverse direction the tract end need only **contain** the limiting arc, which is sufficient for the existence target. [Barth–Rippon, Theorem A, p. 406](https://www.researchgate.net/publication/42790512_On_a_Problem_of_MacLane_Concerning_Arc_Tracts).

The imported statements D1–D4 match Theorem B, equation (4.1), Theorem 1(a), and Theorem 6 of the 2017 source. Empty critical-value set meets the boundedness premise. Monotone accessibility is a property of the image curve, not simply escape to infinity; D4 is not applied without it. The nonlinear qualification in D1 correctly removes the affine/constant-derivative convention issue. [2017 paper](https://www.acadsci.fi/mathematica/Vol42/vol42pp0859-0873.pdf).

The 2025 source defines the same Abel-universal class used in Proposition 8; its p. 873 explicitly excludes that class from A while allowing general asymptotic paths. Its Theorem 3.2 corroborates the imported growth criterion. It is not a resolution of the selected problem. [Charpentier–Manolaki–Maronikolakis](https://ems.press/content/serial-article-files/50390).

A fresh targeted search for “MacLane arc tract 2026”, “MacLane arc tracts locally univalent”, and “MacLane arc tract solved” did not locate a later resolution. The visible recent crawl/index dates led to older sources, not new theorems. This is a bounded corroborating search, not exhaustive status verification through 2026.

## 2. Proposition-by-proposition mathematical audit

### Proposition 1: primitive parametrization — PASS

On the simply connected disk a zero-free derivative has a holomorphic logarithm. Its exponential primitive agrees with f up to the stated additive constant. Conversely its derivative is exactly the prescribed exponential. For a nonlinear primitive the derivative is nonconstant, so the constant-function convention for A does not interfere. Given F in A, negating D1 correctly converts existence of an arc tract into F' outside A. Neither side of the unknown membership pair is asserted without proof.

The residual target's phrase “nonlinear g” is stronger than necessary for the immediate parametrization; “holomorphic g with nonlinear primitive F” is clearer. It is harmless: every affine g is entire, and its primitive is entire, bounded on the closed disk, hence cannot solve the target anyway.

### Proposition 2: entire locally univalent approximants — PASS

Taylor approximations p_n to g converge uniformly on each compact disk. Exponentiation preserves that convergence, and straight-line integration gives the stated factor-r estimate. Each primitive is entire, has derivative exp(p_n), extends across the full circle, and is bounded on the closed disk. Thus each belongs to A and cannot have an escaping minimum on any sequence of disk arcs. The warning against exchanging compact convergence with boundary-uniform control is correct. The auxiliary z^n example is expressly not offered as a locally univalent sequence or candidate.

### Proposition 3 and Corollary 3.1: growth transfer — PASS

For a point of modulus r, the closed Cauchy circle of radius (1-r)/2 lies in the closed disk of radius s=(1+r)/2, strictly inside the unit disk. Maximum modulus gives the stated bound using M(s,f), despite M being defined on the circle. The case r=0 affects no integral and is valid by the same argument.

For nonnegative a and b, 1+a+b <= (1+a)(1+b). Here b=log(2/(1-r)) is positive, so log-positive conventions cause no sign reversal. Change of variables s=(1+r)/2 gives the factor 2 and integration interval [1/2,1). The auxiliary integral is at most log 2+1. These operations are valid for extended nonnegative integrals as well as finite ones. The estimate therefore really proves J(f') <= 2J(f)+1+log 2.

For x>=0, the difference between log(1+log^+ x) and log^+log^+ x lies between zero and log 2. Thus the two integrability criteria are equivalent. A target function cannot be affine, and its derivative is then nonconstant. D1 and the contrapositive of D2 force J(f') infinite; the proved inequality forces J(f) infinite. For the displayed double-exponential bound, the integrable exponent threshold is alpha<1. No converse is inferred from divergence at alpha>=1.

Affine f(z)=az+b, a!=0, must be handled directly because its derivative is a nonzero constant excluded from the package's definition of A. The frozen text does so in all uses of the criterion. Constants and zero functions are included only in the elementary inequality, where the conventions are consistent.

### Proposition 4: singular values — PASS

A nowhere-zero derivative makes the critical-value set empty. Applying D3 with bounded finite asymptotic values would rule out the requested tract, so the necessary finite-asymptotic-value set is unbounded. The source's asymptotic values are over general boundary paths; replacing them with point-asymptotic values only would be unjustified, and the package explicitly avoids that replacement. The warning that local univalence does not alone imply a covering over the full image is essential and correct.

### Proposition 5: exponential Cayley example — PASS

The Cayley transform is biholomorphic onto the right half-plane, and the derivative formula has no zero. Analytic continuation across every boundary point except 1 supplies the required dense point-asymptotic values.

The classification of finite asymptotic values works even for a general boundary path. A finite limit has modulus at least one and is nonzero; a fixed logarithm in a small disk around that limit leaves an integer-valued continuous difference on a connected tail. That difference is constant, so the Cayley transform converges finitely. The inverse transform then forces its limiting real part to be zero. Conversely every point of the unit circle is attained as such a boundary value. No hidden global logarithm on the exponential image is assumed.

The algebraic high-modulus region is exactly the disk centered at l/(l+1) with radius 1/(l+1), where l=log R>0. Its center approaches 1 and its diameter approaches zero. Therefore every Hausdorff limit of arcs with minimum modulus diverging is the singleton {1}. The infinite-valence calculation is valid because all logarithmic lifts have the same positive real part.

### Proposition 6: compact closed barriers — PASS

This is the principal topological checkpoint. Fix R>|f(z0)| and choose one barrier Omega_n whose boundary lies above R in modulus. The component V_R of the open sublevel set containing z0 cannot leave Omega_n: open connected subsets of the plane are path connected, and any exiting path must meet its Jordan boundary. Thus the closure of V_R is compactly contained in D. Continuity gives |f|<=R on that closure. At any boundary point with |f|<R, a sufficiently small disk lies in the sublevel set and meets V_R, making it part of that component and contradicting boundary status. Consequently |f|=R on the boundary.

For compact Q inside the target disk, its inverse image in V_R cannot accumulate on the boundary, because the compact set Q is separated from the target circle. It is therefore compact. This establishes properness rather than assuming it from f'!=0. Properness and the open mapping theorem make the image both relatively closed and open in the target disk; it is nonempty and hence surjective.

For each target value, properness plus isolated zeros gives a finite fiber. Local inverses exist at all fiber points. If a shrinking target neighborhood had additional preimages outside these local sheets, properness would provide a subsequence converging to an additional fiber point or one of the existing points, contradicting the chosen inverse neighborhoods. This proves the covering assertion. A connected covering of the simply connected disk has one sheet; no unproved simple-connectedness of V_R is being smuggled into this step.

The same construction works for every R>|f(z0)|. These particular components are nested by inclusion of sublevel sets. Every point z can be joined to z0 by a compact path in D; its f-image is bounded, so the entire path belongs to a sufficiently large V_R. Hence the V_R exhaust D. Any two points eventually lie in one injectivity domain, and every target value lies in a target disk on which the corresponding restriction is onto. Thus f would be biholomorphic D->C. The inverse is bounded entire and cannot be nonconstant, a contradiction.

No nestedness of the original Omega_n is needed. No compactness of arbitrary components is claimed. The final warning is decisive: target open arcs give neither closed contours surrounding a fixed point nor bounds on added closing segments. Proposition 6 does not establish the missing implication for the original problem.

### Proposition 7: derivative bounded variation — PASS

For a locally C^1 path, h=f' composed with gamma is locally C^1. Integration by parts on each compact parameter interval is legitimate and yields exactly the displayed identity. Finite total variation of the complex-valued h implies a finite endpoint limit in C. Its variation measure has finite total mass, and |gamma|<=1, so the improper Stieltjes integral converges, with tail bounded by the tail variation. The other product tends to zeta times the limiting derivative value. The stated quantitative bound follows by the triangle inequality.

This argument never needs finite length of gamma; it does not estimate the integral by path length. It remains valid when the limiting derivative value is zero. The geometric corollaries use D5 and D4 only in their proper directions. No conclusion about arbitrary asymptotic paths having derivative-BV is made, and local univalence alone would not give that conclusion.

### Proposition 8: Abel-universal crossing argument — PASS

The **frozen proof uses radial arc crossings, not expanding high-modulus Jordan barriers**. For each integer n, universality for the constant n+2 supplies arbitrarily late radii with error below 1; choosing them inductively gives increasing radii and minimum modulus exceeding n+1. Hausdorff convergence of r_n K to K is immediate.

For a continuous path ending at zeta, choose one fixed proper arc K with zeta in its relative interior. There is a fixed tail on which the path stays in its open angular sector and is nonzero. For every sufficiently large chosen radius s_n, continuity of the radial coordinate and its limit 1 give a crossing in that tail. No monotonicity of the radial coordinate is assumed or needed. Every initial compact parameter interval stays a positive distance from the unit circle, so **any** selected crossing times for s_n tending to 1 must tend to the endpoint.

Uniform approximation to the prescribed constant a on s_n K then gives an image subsequence tending to a. Repeating with two different finite constants rules out every finite point-asymptotic limit; a subsequence tending to zero rules out infinity. The approximating radii may depend on a, which is entirely sufficient. The result does not rule out asymptotic paths with nonsingleton boundary end, and no nonvanishing-derivative claim is made. There is no closure-of-open-arcs fallacy.

## 3. Controls and verification limits

On Python 3.12.14:

- `verify.py`: passed; output is byte-identical to frozen CHECKS.json.
- `verify_manifest.py`: passed, nine tracked payload files.
- `verify.py --source-dir ../private`: all three declared sizes and SHA-256 values passed.
- Both Python scripts compiled successfully with the bytecode prefix redirected outside the frozen tree.
- Independent strict inventory and SHA-256 verification passed before and after testing.
- Isolated-copy adversarial integrity tests rejected a proof-file edit and a normal extra file. They exposed the nested-manifest exclusion described in CORRECTIONS.md.

The exact finite controls cover 99 formal-series coefficient checks, 1,681 nonnegative-product cases, 3,102 horodisk-algebra cases, and the integration-by-parts value 57/64. The 128 exponential-map samples are floating-point diagnostics. The threshold controls evaluate a few exact truncated integrals. None tests membership in A, an infinite limiting arc, properness for all radii, a covering theorem, or the imported results. The package labels these limitations correctly.

## 4. Release disposition

There are no blocking mathematical findings. The five approaches remain unsuccessful routes to the full target; a count of eight partial propositions does not change that. Publish, if separately authorized, only as the frozen unsolved investigation with this independent audit, without changing a global “Findings” field or upgrading the theorem status. A release edit creates new bytes and must be rehashed and rechecked; the present approval is tied to the stated manifest.

The frozen STATUS.json says the audit is pending, consistently with its pre-audit creation time. This report and AUDIT.json record the subsequent result without altering the freeze. If release metadata is changed to mark the audit complete, verify.py's hardcoded pending-state assertion must be addressed in that new release or left explicitly as a frozen-snapshot verifier. Neither change is required to recognize the current mathematical audit result.

Source PDFs, rendered scholarly pages, and source extracts remain private and are not included in this audit deliverable. The original frozen public inventory is unchanged.
