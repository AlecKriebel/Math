# Independent review of KP-2.17 / 2765

**Verdict: PASS for the explicitly scoped partial results and source-scope hold. The general closed-surface problem remains unresolved.**

Reviewed on 2026-09-30 by a separate GPT-6 Astra agent at xhigh reasoning. This is an adversarial AI review, not external peer review, and it establishes no historical priority.

The frozen artifact is RESULTS.md, SHA-256:

45784cd0addcd047c60dd9f6dc6b7f7a031fdef595c5293ac1c91c7937a35d59

Both initially supplied copies had this hash. The reviewer did not edit the author artifact. The review also examined SOURCE_AUDIT.md, the source manifest, the exact checker and its recorded output.

## 1. Exact source and scope

The author-hosted K3 book was inspected at Chapter 2's conventions, printed p. 84; the opening of §2.4, p. 96; and Problem 2.17 with its remarks, pp. 98–99. The last two pages were checked visually. The pinned record agrees with the actual numbered problem. The linked AIM workshop report is not the numbered problem list.

K3 uses oriented finite-type surfaces by default, allowing punctures and boundary. Section 2.4 discusses complete hyperbolic metrics; it does **not explicitly add finite area** there. Problem 2.17 neither restricts its reference geodesic to be simple nor expressly fixes a noncompact current convention. Its conclusion concerns a convex combination of closed curves. The length-twin example illustrates an allowed phenomenon, without asserting that every possible summand must itself be a length twin.

Accordingly, Proposition 4 is a correct counterexample to the **separately stated complete finite-area, cusped, Radon-current interpretation**. It is not a convention-free answer to the source question. The package already makes this distinction and appropriately retains its unresolved status.

Source: [K3, author-hosted preliminary book](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).

## 2. All metrics imply lamination data, but the converse is unavailable

For a closed oriented surface of genus at least two, Bonahon's realization of the Thurston boundary in projective current space permits a sequence of positive rescalings of Liouville currents to converge to any nonzero measured lamination. Applying the continuous intersection pairing to the fixed current difference proves Proposition 1. This does not require defining a trace function for an arbitrary current.

Leininger's Theorem 1.4 explicitly distinguishes hyperbolic equivalence from simple-intersection equivalence, with filling-curve counterexamples to the reverse implication. Theorems 5.1–5.2 give the current and compactification facts used here. Equality against simple curves extends to measured laminations by density and continuity, so those counterexamples also obstruct reversing the package's lamination-data implication. Jyothis's Theorem 1.3 and Remark 1.4 add equal-self-intersection examples; they do not repair the reverse implication.

No step in the package substitutes equality against measured laminations for equality against all Liouville currents. The latter is retained in the definition of the fiber and in the final unresolved target.

Sources: [Leininger, *Equivalent curves in surfaces*](https://arxiv.org/abs/math/0302280), [Jyothis, v3](https://arxiv.org/abs/2309.14532v3).

## 3. Simple-reference rigidity

Proposition 2 is valid for every positive integral multiple of an essential simple closed curve on the specified closed surface.

The relevant topology has no hidden pair-of-pants exception. Cutting along a separating essential simple curve gives components of positive genus with one boundary component each. Cutting along a nonseparating curve gives genus \(g-1\geq1\) and two boundary components. On each such component, a pants decomposition together with simple dual curves gives a finite relative filling system disjoint from the original curve. Interior cuffs are crossed by their duals; the duals are themselves crossed by cuffs. The system can be chosen so that its complementary regions are disks and collars of the original boundary components.

The support argument needs positivity, which is part of the stated current convention. If a support geodesic crossed a chosen test curve, the crossing would persist in an open neighborhood in geodesic space. A small crossing box, projected to a fundamental segment of the test curve, would contribute strictly positive intersection. Thus zero intersection excludes every such support geodesic, not merely almost every chosen representative.

After realizing the finite system geodesically:

- A different complete geodesic cannot touch an edge and then turn along it. Tangency of hyperbolic geodesics forces coincidence.
- A geodesic avoiding the arrangement lies in a single complementary lift. A disk lift is bounded, so contains no complete hyperbolic geodesic.
- A lift of a compact boundary collar lies at bounded distance from the associated boundary axis. A complete geodesic contained there must have that axis's two ideal endpoints and must equal the axis.
- The chosen interior axes are excluded because another selected curve crosses them.

Consequently, the support consists only of lifts of the reference simple curve. This is a discrete orbit in geodesic space; Radon local finiteness and invariance give a common finite atomic weight. Equality at one metric determines that weight. In particular, a diffuse current, or a positive measure on spiraling geodesics, cannot evade the support argument.

This reasoning fundamentally uses the simple reference's zero-intersection tests. A filling self-intersecting reference has no analogous disjoint simple filling system. The proposition does not address that case.

## 4. Compact fiber

Proposition 3 is correct under the closed-surface hypotheses.

Burger–Iozzi–Parreau–Pozzetti, Proposition 2.6(1), gives compactness of a fixed positive Liouville-length slice when the carrier lies in a fixed compact set. Here that compact set is the entire closed surface. Their Theorem 2.4 supplies the needed continuity. A nonconstant closed geodesic has positive length, so rescaling reduces the asserted slice to the normalized one. Intersecting with all the closed affine equations defining the fiber preserves compactness and convexity; the reference current ensures nonemptiness.

Equivalently, the current/flow correspondence identifies the fixed length with a fixed mass, up to a universal convention factor, on the compact unit tangent bundle. This alternative agrees with the directly cited compactness theorem.

No extreme-point classification follows. Compactness permits limits with new support, and Krein–Milman does not identify extreme points with closed curves. Even a prospective finite-support theorem would still need to address the exact convex conclusion. The package correctly preserves both limitations.

Source: [Burger–Iozzi–Parreau–Pozzetti, §2](https://people.math.ethz.ch/~burger/pub/2021_Currents_systoles.pdf).

## 5. The thrice-punctured example

Under the explicit conventions in Proposition 4, all parts of the example are correct.

### The metric family really is a singleton

Three distinct marked punctures on the Riemann sphere can be moved to \(0,1,\infty\) by a unique Möbius transformation; uniformization gives the unique complete finite-area hyperbolic metric. The pure mapping class group introduces no additional marked parameter, and cusp permutations are realized by isometries. Thus scaling the Liouville current to match one nonperipheral geodesic does match the entire stated metric-length function.

This is stronger than checking finitely many points in a positive-dimensional Teichmüller space. The zero-dimensional parameter count alone would not establish uniqueness; the uniformization argument does.

### The current and its length are admissible

The Liouville density on pairs of distinct ideal endpoints is smooth and positive. It is locally finite on the geodesic space, since compact sets stay away from the diagonal. It is therefore a nonzero, nonatomic invariant Radon current.

The passage from finite Liouville flow volume to finite current length is legitimate, without assuming continuity of the full intersection form in the cusped current space. A direct verification uses the intersection point and the two unoriented tangent directions as coordinates for a transverse pair of geodesics. The product Liouville measure in these coordinates is a fixed positive multiple of

\[
 |\sin(\theta-\phi)|\,d\operatorname{Area}\,d\theta\,d\phi .
\]

The angular integral over \([0,\pi)^2\) equals \(2\pi\). Tonelli's theorem therefore makes the self-intersection a finite positive multiple of hyperbolic area. This is also the local Crofton/current-flow identification underlying the length normalization. The precise universal factor is immaterial to the ratio in equation (5.1).

Trin's published §3.1 records total oriented Liouville flow volume \(4\pi^2|\chi(S)|\), which is \(4\pi^2\) here. No assertion that this whole oriented volume equals the author's normalized current length is required.

### The concrete geodesic and nonatomic obstruction

In the principal level-two subgroup, the matrices in the package give

\[
 AB=\begin{pmatrix}5&2\\2&1\end{pmatrix},
 \qquad \operatorname{tr}(AB)=6,\qquad
 \lambda_{\pm}=3\pm2\sqrt2 .
\]

The element is hyperbolic, with translation length \(2\operatorname{arcosh}(3)>0\). It supplies a nonperipheral closed geodesic on the thrice-punctured sphere.

Any finite positive combination of closed counting currents is supported on a countable union of lift orbits and is atomic. A nonzero scalar multiple of the Liouville current assigns zero mass to every such countable set, so cannot equal that combination. This excludes finite convex combinations in particular.

### Convention controls

The three cusp lengths are fixed at zero in this construction. Allowing positive geodesic-boundary lengths produces a three-parameter pair-of-pants family. Attaching funnels to the geodesic boundaries gives a complete infinite-area surface homeomorphic to the thrice-punctured sphere, so “complete” alone does not imply the finite-area singleton convention.

Trin's Proposition 2.2 concerns currents on a compact surface with geodesic boundary. It rules out representing all cusped metric lengths by one current in that different compact-core space. Her example of discontinuous intersection on cusped currents also prevents importing closed-surface continuity indiscriminately. The package uses neither identification; its closed arguments and its cusped example are properly separated.

Source: [Trin, published 2024 version, §§2–3.1](https://aif.centre-mersenne.org/item/10.5802/aif.3625.pdf).

## 6. Independent exact controls

The author's checker was rerun with SymPy 1.14.0. Its 30-assertion JSON receipt reproduced byte for byte.

The separate independent_checks.py passes **72 exact assertions**. It independently:

1. Constructs the full six-element \(\mathrm{SL}_2(\mathbb F_2)\) quotient and its regular coset permutations. The elliptic generators have no fixed cosets; the parabolic has three cycles of width two. The usual modular-surface signature calculation gives genus zero and three cusps.
2. Checks the level-two matrices, three distinct cusp fixed points, the hyperbolic word, reciprocal eigenvalues, and the exact trace recurrence for its powers.
3. Verifies the two word classes are distinct even up to unoriented cyclic conjugacy and are not proper powers.
4. Expands the trace-reversal identity in eight independent matrix-entry variables, rather than adopting the author's diagonal determinant-one parametrization. A different-word negative control does not satisfy the polynomial identity.
5. Checks the finite angular factor, Gauss–Bonnet area, and oriented tangent-volume normalization.

These controls do not certify a theorem about an infinite-dimensional current space or a continuum of metrics. The topological support and analytic compactness arguments were audited separately above.

Reproduce from this review directory:

    python independent_checks.py > independent_results.json

All six local source PDFs match the author's frozen provenance hashes. The relevant published Trin theorem and Burger–Iozzi–Parreau–Pozzetti compactness statement were also checked through their public primary sources. A bounded current literature check identified no basis to promote this package to a full closed-surface solution; no exhaustive priority claim is made.

## 7. Publication disposition

The reviewed mathematical claims may be published as **partial results with an unresolved/source-scope-hold status**, accompanied by this review and the precise conventions. No source-artifact correction is required for this verdict.

The remaining full target is to control the positive current fiber of an arbitrary, potentially self-intersecting closed reference geodesic on a closed surface of genus at least two, including the finite convex-combination conclusion. Neither the simple-reference theorem, compactness, equality against measured laminations, nor the conditional \(S_{0,3}\) example resolves it.

## Final artifact hash coverage

On 2026-09-30, the final repository copy of RESULTS.md was checked against the original reviewed bytes. Its only change replaces the pending-review sentence with a statement that the scoped review passed and a link to this report. Exact byte replacement reproduces the complete final file; all mathematical statements and scope qualifications are unchanged. The PASS_PARTIAL_SOURCE_SCOPE verdict therefore also covers final SHA-256:

d3c44c82d2ffb2d20080288821381c8fe4e4e79b6d632bfe5c93b94c71716115
