# Independent adversarial audit: gradient lower bounds for Ricci shrinkers

- Problem: 30002086 / OWR-11789-007, rank 502
- Audit date: 3 October 2026
- Verdict: **PASS_PARTIAL_UNSOLVED**
- Recommended mathematical disposition: **unsolved after five approaches**
- Blocking findings: **none**
- Full proof or shrinking-soliton counterexample: **neither supplied nor certified**
- Novelty and exhaustive literature coverage: **not established**

The packet correctly identifies the original estimate, proves the stated conditional and auxiliary results, and explicitly retains the unrestricted gap. Its examples are not misclassified as shrinking-soliton counterexamples. This pass certifies a bounded partial-result research packet, not a resolution of the problem or publication authorization.

## 1. Frozen input and verification method

The seven payload files and their byte counts match the author manifest. The manifest SHA-256 is `1ea588919fe8349438901131ff2b091552798f7f9c34f544ec5eeaa7794780b7`; RESULT.md has SHA-256 `e2ccde8f4042a0ba2b240593df580ab6cee90941f01f3d2622d1533c7e755116`.

The author's script was copied to an isolated temporary directory and executed there. All **41** controls passed, and the generated receipt was byte-identical to the frozen receipt. The independent `audit_controls.py` passes **50** exact controls. In particular, it checks the cigar by a different route, using intrinsic radial arclength and warped-product curvature rather than Cartesian Christoffel symbols. It also adds exact negative controls for scalar-ratio saturation, directional Ricci curvature, the critical-point sign issue, and the distinction between steady and shrinking equations.

Neither script decides the general problem. The geometric arguments, infinite construction, source hypotheses, and quantifiers were reviewed separately below. The release was not edited. `FROZEN_INPUTS.json` records the checked payload identities; `author_rerun.json` records the isolated replay.

## 2. Original-source and dimension gate

The original report's printed pages **1669 and 1670** were rendered and inspected visually, including the sentence after the page break. The shrinking normalization is Ric + Hess f = g/2. The basepoint minimizes the potential. Equation (5) requires one positive constant that supplies both an exterior radius and the reciprocal gradient lower bound. The next page presents universal validity of that condition as a problem.

The displayed condition belongs to Theorem 2's four-dimensional application. The catalogue formulation does not specify dimension. The packet appropriately separates the all-dimensional question from the original four-dimensional setting and solves neither. It does not add scalar bounds, Ricci bounds, Kähler structure, a prescribed end, noncollapsing at arbitrary scales, or noncompactness to the original quantifiers. Its per-soliton constant is not a claimed uniform constant on a moduli space.

The report is bibliographically 2012, with online publication on 20 February 2013. The separate author extract corroborates the condition. A local file with the extract's PDF filename is actually HTML; the packet discloses that failed download and bases its page-level claims on the valid official PDF instead. The auditor independently accessed the official report and the author extract through public web retrieval. Sources: [official OWR report](https://ems.press/content/serial-article-files/46397), [publisher record](https://ems.press/journals/owr/articles/11789), [author extract](https://www.math.utoronto.ca/roberth/papers/Haslhofer_owr_singularities.pdf).

## 3. Normalization, geometry, and exact target

Write C1 = R + |grad f|² - f. Hamilton's identity makes C1 constant on a connected shrinker. Thus F = f + C1 gives

\[
F=R+|\nabla F|^2.
\]

With the mass-one normalization used in the sources, C1 = -mu, so F = f - mu. The packet gets this sign right. Adding a constant leaves gradients, Hessians, and minimizers unchanged. The trace, drift-Laplacian, and differentiated scalar identities in RESULT.md follow with the displayed conventions.

The growth envelope is correctly transferred to F:

\[
\frac{(r-5n)_+^2}{4}\le F\le\frac{(r+\sqrt{2n})^2}{4}.
\]

The cited growth lemma applies without a global pointwise curvature hypothesis. Completeness makes closed metric balls compact, so the lower bound proves properness; the minimum exists. Scalar nonnegativity and the Hamilton identity give q = |grad F|² = F - R, with 0 <= R <= F. The relevant source locations are Lemma 2.1 and equations (2.4), (2.5), and (2.16) in the [2011 Haslhofer–Müller paper](https://arxiv.org/abs/1005.3255).

The compact case is vacuous: C greater than the diameter leaves no point with r >= C. A constant-potential compact Einstein shrinker therefore does not refute the question. Starting instead with Ric + Hess f = lambda g, lambda > 0, the scaling gbar = 2 lambda g gives coefficient 1/2; distances and gradient norms transform reciprocally as stated.

The equivalences among the single-C condition, a positive lower bound for q outside a ball, and a positive lower bound for F - R above a potential level are correct. For the latter equivalence, use the two-sided envelope to convert exterior balls and high potential levels. For failure, choose points with r >= j and |grad F| < 1/j. Conversely, any escaping sequence with q tending to zero contradicts every fixed positive exterior bound.

Dividing the growth envelope by r² proves F/r² -> 1/4 at infinity. Along a bad sequence, R = F - q then gives R/r² -> 1/4 and R/F -> 1. The stronger absolute statement q -> 0 is essential. The algebraic comparison F = r²/4, R = F - 1 has the same ratio limit but a gap of one. It is used only as a logical control, not as soliton data. This distinguishes the actual unresolved target from a weaker scalar-ratio statement.

## 4. Approach one: conditional scalar-gap estimate and models

For R <= alpha r² + B, with delta = 1/4 - alpha > 0, the lower potential bound gives

\[
q\ge\delta r^2-\frac{5n}{2}r+\frac{25n^2}{4}-B
\]

once r >= 5n and the curvature hypothesis applies. The two further thresholds in the packet make each negative term at most delta r²/4. The nonnegative constant 25n²/4 may be discarded, leaving q >= delta r²/2. Hence the claimed linear gradient bound is valid. If alpha is negative, the separate r >= 5n requirement must still be retained; the proof does retain it. Bounded scalar curvature and R <= (1-epsilon)F are correctly identified as stronger sufficient assumptions, not universal conclusions.

The Gaussian formulas are exact. On the Einstein–Euclidean product, the compact Einstein factor has scalar curvature k/2, and the normalized potential adds precisely this constant to |z|²/4. Product distance gives r² = dN² + |z|², so the diameter estimate for q is correct. A positive-dimensional minimum set causes no defect in the exterior bound.

The strict-quadratic sufficient condition is already in the Remark after Theorem 1.2 of the [2011 paper](https://arxiv.org/abs/1005.3255). The packet identifies that provenance and makes no novelty claim. Its residual obstruction is real: R <= F, by itself, permits the leading coefficient 1/4 and does not establish an absolute positive deficit.

## 5. Approach two: geodesic integral and endpoint control

For a unit-speed minimizing geodesic from a minimizer, the potential derivative starts at zero. Integrating Hess F(gamma', gamma') = 1/2 - Ric(gamma', gamma') gives equation (7) with the correct sign and coefficient.

The summed second-variation inequality is valid for the Lipschitz, piecewise-linear cutoff; it can equivalently be obtained by smooth approximation. For endpoint cutoff length ell, the cutoff energy is 2/ell and the missing weight integral at each endpoint is 2 ell/3. Setting ell = 1 gives exactly 2(n-1) and 2/3 in the packet. Under a global directional upper bound Ric <= K g, the two endpoint losses total 4K/3. Taking the gradient norm above its component along gamma' proves equation (9), whether or not the right side is already positive.

The starting endpoint has uniform bounded geometry because it lies in a fixed compact ball. The ending endpoint does not. Nonnegative scalar curvature does not bound a Ricci eigenvalue: the algebraic eigenvalues (T, -T, 0, 0) have zero trace and arbitrarily large positive first eigenvalue. This is a tensor-level control of the inference, not an asserted shrinker realization.

Fang–Man–Zhang's Theorem 1 contains Ricci upper bounds or a Ricci lower bound together with injectivity-radius control; its Theorem 2 assumes bounded scalar curvature. The paper's title cannot erase those assumptions. The packet accurately describes both the argument and the missing exterior endpoint estimate. Source: [Fang–Man–Zhang, arXiv:0801.0103](https://arxiv.org/abs/0801.0103).

## 6. Approach three: Bochner signs and critical points

The weighted Bochner identity uses Ric_F = g/2 and grad Delta_F F = -grad F. Consequently

\[
\Delta_F q=2|\nabla^2F|^2-q
\ge\frac2n(n/2-F+q)^2-q.
\]

The trace-Hessian inequality is applied in the correct direction. At a local minimum of q, the gradient drift vanishes and Delta_F q >= 0; a strongly positive lower bound on this Laplacian does not contradict the minimum. At an actual critical point of F, differentiating q twice gives Hess q = 2(Hess F)², a positive-semidefinite tensor. Its positivity is compatible with a negative trace of Hess F. In particular, F > n/2 excludes a local minimum of F but does not exclude a maximum or saddle. The scalar inequality has the corresponding compatible sign at a high scalar maximum.

The Hessian lower bound along a bad sequence follows directly from |Hess F| >= |Delta F|/sqrt(n). It indicates a severe local curvature/Hessian regime but does not rule it out. No global minimum principle with a contradictory sign, quantitative derivative estimate, or justified compactness theorem is smuggled into the conclusion. This approach ends at a genuine gap.

## 7. Approach four: finite topology and infinite smooth profile

If all critical points lie in a compact set, their F-values are bounded. Choose a larger regular value a. The field X = grad F/q has X(F) = 1. On every finite slab a <= F <= b, compactness and q > 0 give a smooth bounded vector field with the required continuation. This proves the product description of the exterior through all finite level intervals, even without a single lower bound on q valid on the entire end. The compact sublevel and its collar give finite topological type. The proof thus does not assume its desired stronger gradient bound.

The auxiliary profile is valid. The bump supports are disjoint: adjacent half-widths have sum 3 times 2^(-k-4), less than one for k >= 2. They are locally finite. Each standard smooth compactly supported bump has matching zero derivatives at its support boundary, so the sum is smooth. It vanishes near zero; the even extension of F0 is therefore exactly (1+x²)/4 near zero and is smooth there.

The total possible integral loss is at most 1/8. Therefore H >= sqrt(1+r²)-1/8 > 0, H = r + O(1), and H' is strictly positive for r > 0. At a point in the kth support, 1-a_k psi >= k^(-3) > 0; outside the supports it equals one. This proves the unique-critical-point claim and properness. The upper bound H' <= 1 gives |grad sqrt(F0)| <= 1/2 and nonnegativity of the auxiliary S0.

At r = k, the exact derivatives are

\[
H'(k)=\frac{k}{\sqrt{1+k^2}}k^{-3},\qquad
H''(k)=\frac{k^{-3}}{(1+k^2)^{3/2}}.
\]

Together with H(k) <= sqrt(1+k²), these imply F0'(k) <= 1/(2k²). The asserted Hessian bound follows from F0'' = (H'² + HH'')/2. It holds for every k >= 2, not just the six centers sampled by the author's script: each term in the loose bound decreases with k, and its value at k = 2 is 13/640 < 1/2. The growth envelope with n = 1 follows from H >= (r-5)_+ and H <= r+sqrt(2).

This is decisively not a one-dimensional shrinker: actual Euclidean scalar curvature is zero, S0 is only an auxiliary function, and the required equation F0'' = 1/2 fails at every bump center. It refutes only the proposed deduction from growth and absence of exterior critical points.

## 8. Approach five: rescaling and the complete steady comparison

Under constant scaling g_j = a_j g, the Levi-Civita connection, Hessian as a covariant two-tensor, and Ricci as a covariant two-tensor are unchanged. Scalar curvature and squared gradient norms divide by a_j. For a_j = F(x_j) and u_j = F-a_j this gives precisely equation (15). Smooth pointed convergence of both metrics and potentials, if available, lets a_j^(-1) tend to zero in those equations and yields the steady system in (16), with u(o) = 0 as well.

Completeness and smooth convergence of a limit are hypotheses here. The author does not claim that the original bad sequence automatically has such a subsequence. The basepoint scalar tends to one and the scaled basepoint gradient tends to zero exactly as written.

For an independent check of the cigar, set s = 2 asinh(r). Its metric becomes

\[
ds^2+h(s)^2d\theta^2,\qquad h(s)=2\tanh(s/2),
\quad u(s)=-2\log\cosh(s/2).
\]

The Gaussian curvature is -h''/h = (1/2)sech²(s/2). Both orthonormal Hessian entries, u'' and u'h'/h, equal its negative. Thus Ric + Hess u = 0, while R = sech²(s/2) and |grad u|² = tanh²(s/2) sum to one. The origin is a smooth pole because h(s) = s + O(s³), and the Cartesian expression independently makes smoothness transparent. Radial arclength extends to infinity; every escaping curve has length at least its radial variation. This proves completeness. Euclidean products preserve the displayed equations in every dimension at least two, including four.

The steady equation is not the shrinking equation, so this example only prevents a contradiction based on those limiting equations and basepoint values alone. Whether additional inherited properties exclude this model is a separate question, correctly left open.

The [2015 Haslhofer–Müller note](https://arxiv.org/abs/1407.1683) removes the gradient and Euler-characteristic hypotheses from its compactness theorem through a different local curvature estimate. It does not establish those removed hypotheses. Its estimates (2.1) and (2.4) concern balls controlled relative to a minimizing basepoint, with radius-dependent constants. Moreover, the theorem concerns shrinkers with the fixed shrinking normalization, not the rescaled almost-steady sequence here. It cannot simply be invoked to supply the missing smooth complete limit at escaping basepoints.

## 9. Literature and current-status boundary

The source audit's recent-status statements were checked against the primary sources. Bertellotti–Buzano's Theorems 1.2 and 1.3 explicitly retain the absence of far-out critical points where needed. The introduction lists bounded scalar curvature and strict sub-quarter quadratic scalar growth as sufficient conditions. Proposition 3.6 supplies the appropriate level-flow mechanism. The article was published online in November 2025 and appears in Selecta Mathematica volume 32 (2026). Source: [Ends of (singular) Ricci shrinkers](https://link.springer.com/article/10.1007/s00029-025-01104-y).

Fei He's May 2026 preprint distinguishes Kähler finite topology from the general situation and places explicit curvature assumptions on the results cited by the packet. It is not an unrestricted gradient theorem. Source: [Topology of gradient Ricci shrinkers via weighted L2 cohomology](https://arxiv.org/html/2605.04476v1). The August 2026 Xu–Zhang abstract is explicitly Kähler-specific, consistent with the packet's limited use of it: [arXiv:2608.10953](https://arxiv.org/abs/2608.10953).

Targeted additional searches for the gradient estimate and exterior critical-point problem did not identify an unrestricted resolution. This is a bounded literature check, not proof that no relevant paper exists. In particular, the audit verdict should not be converted into a claim of complete priority research or of a newly established global status theorem. The catalogue/repository-history observations are author-reported bounded searches; this mathematical audit does not certify an exhaustive historical search.

## 10. Final disposition and release boundary

All five approaches have substantial, checkable content. None closes the common missing step: an absolute positive lower bound for F-R at infinity without additional curvature or geometric hypotheses. No change to the frozen mathematical payload is required for its stated partial-result disposition.

The correct final label remains **unsolved, five approaches completed**, with the conditional estimates and false-inference tests retained. The frozen `independent_review: pending` entry is provenance of the author candidate, not a failed audit; the independent verdict is this separate report. Do not label the problem solved, the bump profile a Ricci shrinker, the cigar an actual blow-up, or the compactness improvement a proof of the gradient condition.

The audit directory is limited to original review prose, verification code, hashes, and short receipts. It contains no source PDFs, source screenshots, full extracted source texts, raw catalogue records, or private coordination. No remote mutation was performed. Publication or repository changes require the separate authorized workflow; this audit grants no such authority.
