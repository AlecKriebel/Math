# Independent mathematical audit of the planar crystalline Wulff partial results

Problem 30005209 · 7 October 2026

## Decision

**Accept the five stated planar partial results, subject to the cited published existence, rigidity, and quantitative Wulff theorems. No substantive mathematical correction is required. The requested geometric classification remains unresolved.**

This is an independent AI-assisted mathematical audit of the exact original bytes identified below, not a human referee report, formal verification, or certification of novelty. The review checks the argument and the hypotheses of its external dependencies. It does not reprove those published dependencies or establish an exhaustive literature search.

The central accepted statement is the following: for a fixed exponent \(0<\alpha<2\) and a nondegenerate planar convex polygon \(P\) of area one, equal side-average Riesz potentials are equivalent to global minimality of \(P\) for at least one positive coefficient, and equivalent to unique global minimality for every sufficiently small positive coefficient when the anisotropy is \(h_P\). Uniqueness is understood up to translations and null sets. The origin is in the interior of the chosen representative of \(P\). The threshold depends on the polygon and exponent.

This is an implicit analytic criterion. It is not an explicit geometric classification, does not classify arbitrary normal fans or remote branches of critical shapes, and does not settle the higher-dimensional problem.

The originals contain malformed inline mathematics delimiters. These do not create mathematical ambiguity in the checked arguments, but they should be repaired for presentation. A separate insertion-only patch and corrected reading copies are supplied; the originals are unchanged.

## Exact acceptance boundary

The complete original `AUTHORED_MANIFEST.json` has SHA-256

`fa8b800b4df4a938a72256b6b97a106cf9555a4ccd323003255e30b9320a1516`.

Every one of its 11 entries was checked against the actual file bytes and matched. The five mathematical manuscripts are pinned as follows:

1. `01_triangle_rigidity.md`: 3,699 bytes; SHA-256 `b29b19ae8ac0eb4916fcffbe2cb2fc95b7218c5589f0432edab9f3f2f8a1ca06`.
2. `02_stationarity_and_global_minimality.md`: 8,350 bytes; SHA-256 `91460e2373b9d539e6e75fd1caa6d5ed7b22a1aadfcbddf154c91b941bd1d140`.
3. `03_parallelogram_classification.md`: 3,166 bytes; SHA-256 `ff5aaf80230e6aae4026e0e7fe3c7196b52e45e9e5d995bc64cd14cd36073aea`.
4. `04_near_square_continuation.md`: 5,543 bytes; SHA-256 `46d2f507daf63782a95fe1f4ed5993ae8b182af848deaa0e69040bf99279662c`.
5. `05_vertex_truncation_obstruction.md`: 6,376 bytes; SHA-256 `dc8f07f66755d7af12de13ad30c5114bd0bf4e68deee2a3ce2c4ada57b3df133`.

The exact pins of all supporting files are repeated in `ACCEPTANCE.json`. The mathematical acceptance also covers the separately pinned corrected reading copies because a byte-level comparison established that their only changes are inserted backslashes in inline delimiters. No word, formula operand, sign, constant, hypothesis, citation, or conclusion was replaced or deleted.

## Sources and hypotheses independently checked

The retained seven source PDFs match all byte counts and SHA-256 values in `SOURCE_MANIFEST.json`. Fresh text extraction from each PDF reproduces the corresponding supplied extraction byte-for-byte. The relevant statements were inspected in those extractions. The public records for the 2021 and 2022 papers were additionally checked online.

The primary 2021 paper is by **Marco Bonacini, Riccardo Cristoferi, and Ihsan Topaloglu**, not Fusco–Julin–Morini. Its [arXiv record](https://arxiv.org/abs/2004.03628) confirms the authors, title, DOI, and 2021 journal reference. The [2022 CVGMT record](https://cvgmt.sns.it/paper/5058/) confirms the same authors for the triangle and quadrilateral paper.

The following distinctions are essential and correctly maintained in the packet:

- BCT's surface tension is convex, positively one-homogeneous, and positive away from zero; evenness is not required. A polygon translated to contain zero is an admissible Wulff shape for its support function. Consequently triangles and non-centrally-symmetric quadrilaterals are not excluded.
- The original classification passage in the [Oberwolfach report](https://ems.press/content/serial-article-files/46973), printed page 2172, concerns fixed-normal side translations in the planar discussion. It is not a requirement of criticality under tilting or arbitrary deformations.
- Theorem 2.5 of [BCT 2021](https://iris.unitn.it/retrieve/e3835198-3dd2-72ef-e053-3705fe0ad821/Bonacini%20-%20Cristoferi%20-%20Topaloglu%2C%20Minimality%20of%20polytopes%20in%20a%20nonlocal%20anisotropic%20isoperimetric%20problem.pdf) supplies a symmetric sufficient class. Its initial existence, quasiminimality, and fixed-normal reduction do not use that symmetry. Remark 2.6 supplies necessary equal-average conditions, not the missing classification.
- Remark 4.1 of [BCT 2022](https://cvgmt.sns.it/media/doc/paper/5058/BonCriTop22.pdf) already establishes automatic sliding stationarity for triangles. The triangle rigidity theorem there uses tilting, and the quadrilateral theorem uses sliding together with tilting. Neither contradicts the partial results here.
- Theorem 3.1(i) of [Choksi–Neumayer–Topaloglu](https://ihsantopaloglu.github.io/papers/ChNeTo.pdf) proves small-mass existence for every \(0<\alpha<d\) and positive convex one-homogeneous surface tension. Rescaling gives the needed small-coefficient, unit-volume existence. No evenness or smooth ellipticity is imposed for this existence result.
- The quantitative Wulff inequality used is BCT equation (2.6), attributed there to Figalli–Maggi–Pratelli. It applies to general finite-perimeter equal-volume competitors, rather than only to polygons.
- The relevant result in the [Figalli–Maggi author manuscript](https://people.math.ethz.ch/~afigalli/papers-pdf/On-the-shape-of-liquid-drops-and-crystals-in-the-small-mass-regime.pdf) is Theorem 3.7. It is stated for sufficiently small volume-constrained \((\varepsilon,3)\)-perimeter minimizers and concludes convex polygonality with normals drawn from the Wulff normal set. It is not restricted to minimizers of the paper's external-potential model. BCT cites the journal numbering as Theorem 7.

The scaling in `SOURCES_AND_SCOPE.md` is correct: at volume \(m\), dividing out the perimeter scale gives effective coefficient \(\gamma m^{(d+1-\alpha)/d}\). The bounded negative literature conclusion is appropriately qualified. The audit does not turn that search result into a novelty assertion.

## Approach 1 Triangle rigidity

**Accepted.** The support-space argument is exact. With three oriented normals, \(N\) has rank two, the positive side-length vector satisfies \(N^T\ell=0\), and \(\ell\cdot h=2\). These facts make the three columns of \([N\ h]\) independent. Thus every support vector has the unique representation \(Na+ch\).

The positivity of \(c\), implicit in the manuscript's geometric statement, can also be seen directly: for an interior point \(x\) of the new triangle, all \(h'_i-\nu_i\cdot x\) are positive, so their \(\ell_i\)-weighted sum is \(2c>0\). The new triangle is therefore \(a+cP\), and equal area forces \(c=1\).

The small-coefficient existence and crystalline rigidity steps consequently leave only translates of the original triangle. The independent first-variation check is also valid: translation invariance gives \(\sum_iB_i\nu_i=0\), and the one-dimensional nullspace gives \(B_i=A\ell_i\). The result applies to all nondegenerate triangles, including scalene ones, under the actual non-even source hypotheses.

The manuscript correctly credits the existing triangle stationarity observation. Its global conclusion is presented as a consequence of published reduction results, not as an unqualified new theorem of the literature.

## Approach 2 Planar analytic equivalence

**Accepted.** This is the most consequential argument in the packet. Each link in its local-to-global chain checks out.

### Smooth interaction under a single global transport

With the normal fan fixed and all sides present, each vertex is affine in the support increments. The fan triangulation from an interior origin remains nondegenerate in a sufficiently small neighborhood. The piecewise-affine maps agree on shared radial edges and form one continuous map of the whole polygon.

Because the reference domain is convex, a uniform bound on its finitely many piecewise gradients gives a global Lipschitz bound by integration along line segments. This applies to every parameter derivative of the map as well. In particular, the difference of a parameter derivative evaluated at \(x\) and \(y\) is bounded by a constant times \(|x-y|\), even when the two points lie in different triangles.

The maps are uniformly bi-Lipschitz for sufficiently small increments. Kernel differentiation twice therefore has the dominating bound \(C|x-y|^{-\alpha}\). Jacobians are bounded piecewise polynomials, so their derivatives preserve that bound. The diagonal singularity is integrable in the two-dimensional bulk precisely for the stated range \(\alpha<2\). Dominated differentiation gives a continuous bounded Hessian. The same argument applies to smoothly moving vertices when the normal directions vary.

There is no invalid appeal to an absolutely integrable same-side boundary Hessian for \(\alpha\ge1\). The spatial-difference cancellation supplied by the single global transport is exactly what is needed.

### First variation and the exact area constraint

Continuity and boundedness of the potential follow by separating a small ball from its complement. For a signed indicator difference supported on a set of measure \(\delta\), the quadratic remainder has absolute value at most \(C\delta^{2-\alpha/2}\). Since \(\alpha<2\), this is \(o(\delta)\), and hence \(o(|s|)\) when \(\delta=O(|s|)\).

The signed strip calculation yields

\[
DV_\alpha(P)[s]=2\sum_i B_i s_i,
\qquad D|P_s|[s]=\sum_i\ell_i s_i.
\]

Corner pieces have second-order area and a bounded potential, so they do not affect the first derivative. The area gradient is nonzero. Thus every tangent vector in \(\ell^\perp\) is realized by a genuine two-sided path on the exact area level set.

The crystalline perimeter is smooth on this fixed-normal chart despite the nonsmoothness of the anisotropy in other directions. Its first derivative vanishes on the constrained tangent space because the Wulff shape minimizes perimeter. Consequently total-energy minimality for any fixed positive coefficient forces \(B=A\ell\). If that condition fails, reversing a nonzero interaction derivative gives a strict descent for every fixed positive coefficient.

Under stationarity the first-order interaction term is a multiple of the area derivative. Exact area preservation makes that linear term second order. The bounded Hessian therefore gives an \(O(|s|^2)\) interaction difference.

The conversion to symmetric difference is valid: fixed middle subsegments of the nonzero sides have disjoint neighborhoods, and the other inequalities have positive slack there. The associated strips contribute at least \(c\sum_i|s_i|\). Therefore \(|s|\le C|P_s\triangle P|\), giving the required quadratic estimate in symmetric difference.

### Global competitors and precise rigidity normalization

For unit-area sets, the uniform potential bound gives an interaction Lipschitz constant \(L_\alpha\) independent of the competitors. A global minimizer satisfies

\[
P_\psi(E)\le P_\psi(F)+\gamma L_\alpha|E\triangle F|
\]

for every equal-area finite-perimeter competitor. This is stronger than the neighborhood-restricted competitor condition in Figalli–Maggi. Their scale-invariant penalty coefficient is
\(\varepsilon |K|^{1/2}|E|^{-1/2}\); both areas equal one here. Thus \(\varepsilon=\gamma L_\alpha\) is the exact appropriate normalization, and the \((\varepsilon,3)\) hypothesis follows.

Existence supplies a minimizer. Quantitative Wulff stability and comparison with \(P\) first give \(\delta(E)=O(\gamma)\), where \(\delta\) minimizes symmetric difference over translations. Small-quasiminimizer rigidity then gives a convex polygon with permitted oriented normals and uniform proximity. This is precisely the pre-symmetry reduction already used in BCT's proof.

The passage from a subset of permitted normals to the full nearby normal fan is justified. For convex bodies converging to \(P\), support values converge; all sides of \(P\) have positive length and its adjacent lines are transverse. Sufficiently close support values therefore preserve every side. A purported sequence omitting a fixed normal would contradict that persistence. This is a local statement at a fixed nondegenerate polygon, not a uniform assertion through facet collapse.

Translation alignment introduces no loss. A best-aligned translate exists, and a best alignment is itself close whenever some alignment is close: the triangle inequality controls the symmetric difference between the two translates of \(P\). A nonzero translation separated from zero cannot have vanishing symmetric difference with the fixed bounded polygon. Consequently the same local support estimate applies in the minimizing alignment, giving \(|V_\alpha(E)-V_\alpha(P)|\le C\delta(E)^2\).

Finally,

\[
0\ge\mathcal E_\gamma(E)-\mathcal E_\gamma(P)
\ge(c_P-\gamma C)\delta(E)^2.
\]

Choosing a positive coefficient below all existence, rigidity, chart, and coercivity thresholds forces \(\delta(E)=0\). All constants may depend on the fixed polygon and exponent. No uniformity across degenerate shapes, exponents, or side counts is needed or claimed.

The statement is a genuine global-minimizer result among arbitrary finite-perimeter competitors, rather than merely fixed-normal local minimality.

## Approach 3 Parallelogram classification

**Accepted.** Direct side and bulk parametrization gives the stated averages. Central symmetry identifies opposite-side averages, leaving exactly two values. Splitting the convolution variable into positive and negative parts gives

\[
M_b-M_a=\frac D2\int_0^1\int_0^1(s-t)
\bigl[H(s,t)-H(t,s)\bigr]\,ds\,dt.
\]

Both signs of the cross term have the same denominator difference
\((|a|^2-|b|^2)(s^2-t^2)\). This remains true at every nondegenerate angle, including obtuse angles. Strict monotonicity of a negative power gives the manuscript's strict sign whenever the edge lengths differ. Invertibility of the two linear parametrizations provides integrability for every \(\alpha<2\).

Thus equal side averages occur exactly for equal edge lengths, that is, rhombi. Applying Approach 2 is legitimate. Rhombi's positive conclusion is also already included in BCT's symmetric sufficient class. The rectangle path has derivative \(2(M_b-M_a)\) at unit area; the factor two and its strict nonzero value away from a square are correct.

## Approach 4 Stationary quadrilaterals near the square

**Accepted.** Recomputing the rectangle derivative and differentiating the integral gives

\[
\left.\frac{d^2}{d\tau^2}V_\alpha(R_\tau)\right|_{0}
=-4\alpha\int_0^1\int_0^1
\frac{(s-t)^2(s+t)}{(s^2+t^2)^{1+\alpha/2}}\,ds\,dt<0.
\]

The sign and factor are correct. The numerator has degree three, so the integrand has degree \(1-\alpha\) and the polar-area integral near zero is finite throughout the stated range. It is positive off a measure-zero diagonal on a set of positive measure, proving strict nondegeneracy without numerical evidence.

The support chart removes all and only translations by setting the first two independent supports to one half. The area equation solves for the fourth support because its derivative is the positive fourth-side length. The third support is therefore a complete one-dimensional constrained shape coordinate. At square normals it parametrizes rectangles with width \(1+z\), and \(\tau=\log(1+z)\). Since the first derivative vanishes at the square, this coordinate change preserves the displayed Hessian at the basepoint.

The vertex-transport estimate gives joint \(C^2\) dependence on normals and support coordinate, so the implicit function theorem applies to the scalar constrained derivative. Completeness of the quotient chart is crucial: its zero is stationarity under every fixed-normal area-preserving direction, not merely a selected test path. Local uniqueness is correctly restricted to a neighborhood of the square and the fixed nearby normal configuration.

The chosen perturbed normal configuration has only one antipodal pair and therefore cannot be a parallelogram. A side-transitive convex quadrilateral has equal side lengths and is a rhombus. The constructed exact stationary shapes therefore lie outside that class. Their defining supports are supplied by the implicit theorem; no floating-point root is being treated as an exact solution.

## Approach 5 Vertex truncation and the boundary strategy

**Accepted with its explicitly stated exponent restriction for the negative example.** Removing a shrinking cap has interaction variation \(-2\delta v_P(p)+o(\delta)\). The cap's self-energy is \(o(\delta)\). Area renormalization contributes \((4-\alpha)V_\alpha(P)\delta/2\). At sliding-stationary shapes, the dilation identity gives \((4-\alpha)V_\alpha(P)=4A|P|\), yielding the stated coefficient \(2[A-v_P(p)]\) at area one.

For an equilateral triangle, the slice integral along a base is strictly decreasing away from its midpoint. The endpoint derivative comparison is valid on each slice at positive height; alternatively the same monotonicity can be integrated directly without differentiating under a singular slice integral. Thus the vertex potential is strictly below the side average for every \(0<\alpha<2\), and sufficiently small cuts increase the area-normalized Riesz energy.

For the thin obtuse triangle, the proposed dominations by the one-dimensional kernels hold exactly when \(0<\alpha<1\). The triangular density has the stated piecewise cubic self-convolution. Termwise integration gives

\[
I_\alpha=\frac{2(2^{4-\alpha}-4)}{(1-\alpha)(2-\alpha)(3-\alpha)(4-\alpha)},
\qquad J_\alpha=\frac{2}{(1-\alpha)(2-\alpha)}.
\]

Subtraction gives the manuscript's numerator \(16-4\alpha-2^{4-\alpha}\). Convexity bounds the exponential by its chord on \([0,1]\), proving strict positivity in the open interval. The apex potential is therefore strictly greater than the side average for sufficiently thin triangles at each fixed exponent in that interval. Dilation preserves the comparison, and the corresponding normalized cut decreases the Riesz energy.

This disproves the universal boundary-improvement claim for an allowed-normal family with the new normal at that apex. It does not assert a global maximizer, absence of interior critical points, or multiplicity. The packet correctly separates a new-facet test of the Riesz-only strategy from fixed-normal variations for the original triangle's full crystalline energy. The negative example is not extended without proof to \(1\le\alpha<2\).

## Computational checks and typography

A separate copy of the supplied verification script was run without modifying the authored files. It passed 12 parallelogram sign and symmetry cases, four square-Hessian consistency cases, and three thin-triangle convolution cases. Its output agrees byte-for-byte with the retained `verification_results.json`.

These checks are floating-point sanity checks, not interval-certified inequalities or proof certificates. The accepted strict signs, Hessian, and convolution identity are supported by the analytical arguments reviewed above.

`TYPOGRAPHY_ONLY.patch` inserts 171 backslashes across the eight Markdown files. Of these, 169 repair missing opening delimiters; two repair the fully unescaped initial exponent interval in the README. A programmatic diff confirms insertion-only changes consisting solely of backslashes. The corrected files have paired inline and display delimiters. `TYPOGRAPHY_MANIFEST.json` records exact original and corrected hashes, byte counts, and insertion counts. The patch itself is 44,012 bytes with SHA-256 `46b92198186437ead57ebdff5f6bd536078bcb41d617d75823d8ca47ec1a5f0d`.

The corrected reading copies intentionally do not reuse the old authored manifest. Applying the patch to a publication copy requires regenerating that copy's authored-file manifest. The audit's original-file pins remain the record of what was received and reviewed.

## Final disposition

The five substantive approaches are supported at the scope stated in the manuscripts. No source document, dataset content, private source, or coordination material is included in this report or in the typography patch. Existing source attribution and the unresolved classification status must remain visible.

**Accepted as planar partial results. Classification status: unresolved after five approaches. No novelty, human-review, or formal-proof claim.**
