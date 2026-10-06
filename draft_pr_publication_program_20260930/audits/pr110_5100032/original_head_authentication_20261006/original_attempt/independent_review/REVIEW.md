# Independent review: focal antipedal invariant k603

**Verdict: PASS_COMPLETE_PROOF.** The per-edge identity is correct for the source's strictly nested confocal ellipses, with ordinary nonnegative focal distances. It telescopes to the requested equality for every closed admissible orbit, including star orbits and repeated traversals. No mandatory mathematical correction is required.

Recommended campaign status: **claimed_solved, 2/5**. This is a separate adversarial AI review using gpt-6-astra at xhigh reasoning, completed on 2026-09-30. Historical priority remains unconfirmed, and this is not human peer review.

## Frozen artifact and reproduction

- PROOF.md: 8478d2a792944c5fb9e8a53324e0c6bce8eba317de29c31a6fcbd6ca0205709d
- Submitted verify.py: 0d05777d1c794b78dc2cae69bbaed52c2dcc6b33c79a8fe016e8079a03d957e4
- Submitted verification.json: d5bfd8ef0fddd6d1c81c2c66f1e8ff9d6d949ff0656f776f5bf11914fbdcb67b
- All **17,364 submitted exact assertions on 1,447 rational chords** passed; running in an isolated working directory reproduced the written receipt byte-for-byte
- **1,993 independent exact diagnostics on 90 unit-normal chords** passed

The author's checker writes its receipt in the current directory. Its correct replay is therefore from author_replay itself, as shown below. No author mathematical file was edited.

## 1. Exact source and exclusions

I checked [Reznik–Garcia–Koiller, arXiv:2004.12497v11](https://arxiv.org/abs/2004.12497v11), its introduction, Sections 3.5 and 3.7, and Table 7. I independently retrieved the complete [published 2021 article](https://amj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), checked the same definitions, and visually inspected its introduction and Table 7 on printed p. 349.

Both introductions define the elliptic billiard in this work using a pair of **confocal ellipses**. Table 7 labels k603 as the ratio of the two sums of focal **antipedal** distances, with value one for all $N$. Section 3.7 defines those distances by ordinary Euclidean norms. The quantities are not pedal feet, side lengths, areas, or signed distances. Consecutive endpoint-line intersections give the antipedal vertices; a cyclic shift in their indexing does not affect either sum.

The candidate's domain $a>b>0$ and $0<\lambda<b^2$ is exactly a strictly nested, nondegenerate confocal elliptical caustic. It does not claim a hyperbolic-caustic or degenerate two-bounce extension. Those exclusions do not discard part of the confocal-ellipse pair stipulated by this source. A circle has coincident foci, so the separately mentioned circle limit has immediate equality wherever the construction is defined.

A bounded primary-source search did not locate a later general-$N$ proof of this exact ratio. This does not certify novelty. The distinction between the source's still-unproved table entry and a new historical discovery remains explicit.

## 2. Antipedal distances and the absolute-value issue

With a focus translated to the origin, the line through $A$ perpendicular to $A-f$ is characterized by
$Q\cdot(A-f)=|A-f|^2$, and likewise for $B$. Solving those two equations gives the displayed squared-distance formula. The triangle-area identity then gives
\[
q_f=\frac{|A-f|\,|B-f|}{\operatorname{dist}(f,AB)}.
\]
Both numerator factors and the denominator are positive in the situation used later. Thus this is an equality of ordinary positive distances; no signed square root has been substituted.

For an elliptical caustic the two foci lie strictly inside it. Hence a tangent chord cannot pass through either focus. In the author's coordinates this is proved quantitatively by
\[
(U-eC)(U+eC)=(b^2-\lambda)D^2>0,
\qquad (U-eC)+(U+eC)=2U>0.
\]
Both factors are therefore positive. The two heights really are $(U\mp eC)/D$, without absolute-value sign changes from one edge to another. This is the essential sign check.

The endpoint focal distances are $a\mp c\cos t$, not their possibly negative signed variants; they are strictly positive because $a>c$. Nonzero focal height also makes the endpoint vectors linearly independent, so the antipedal vertex is finite and uniquely defined. The final denominator sum is positive.

## 3. Consistent edge orientation

An orientation with the caustic on the left is available for every orbit considered. At a point outside the caustic, reversing the incoming tangent direction makes the caustic lie on the right of that tangent. The other outgoing tangent is the unique one that leaves the caustic on the left. The nondegenerate billiard/Poncelet continuation uses this other tangent. Thus the choice is consistent throughout the orbit, not made separately with incompatible signs on different edges.

Since the origin is strictly inside the caustic, it also lies to the left of each edge. Consequently $\det(A,B)>0$. The affine scaling from the ellipse to the unit circle preserves that sign, so the forward central-angle difference has its representative in $(0,\pi)$. This justifies $0<\delta<\pi/2$, hence $U>0$ and $V>0$ on every edge.

This reasoning also applies to star polygons: their successive forward increments may wind more than once in total, but each individual increment has the same local range. Reversing the entire orbit handles the other orientation, and it does not change the unordered endpoint-line intersection or either focal distance. No use of convexity of the whole orbit polygon is hidden here.

## 4. Algebra and an independent derivation of the coefficient

The focal-product expansion
$R_\sigma=a^2H_\sigma^2+b^2V^2$ is correct. Tangency gives $V^2=\lambda D^2$, and the positive height-product identity rationalizes $D^2/H_\sigma$ using the opposite height. This yields the author's formula (7) and, after subtraction, formula (8).

The displacement is $y_B-y_A=2bCV=2b\sqrt\lambda\,DC$. Substituting this into (8) gives exactly
\[
\Gamma=\frac{c}{ab\sqrt\lambda}
\left[-a^2+\frac{b^2\lambda}{b^2-\lambda}\right].
\]
It is independent of the edge. The proof never divides by $C$ or by $y_B-y_A$, so horizontal edges are included. The coefficient can be positive, negative, or zero; none of those cases changes the positivity of the individual distances.

I also recovered the identity in different coordinates. Let a tangent chord have outward unit normal $(u,v)$, support value $h>0$, and positive tangent direction $(-v,u)$. Put
\[
K=a^2u^2+b^2v^2,\qquad h^2=K-\lambda.
\]
The chord length and focal-height product are
\[
\ell=\frac{2ab\sqrt\lambda}{K},\qquad
(h-cu)(h+cu)=b^2-\lambda>0.
\]
The endpoint $x$-coordinate sum and product obtained from the quadratic ellipse intersection are
\[
x_A+x_B=\frac{2a^2hu}{K},\qquad
x_Ax_B=\frac{a^2(h^2-b^2v^2)}K.
\]
Using these in the two focal products and dividing by the respective positive heights gives
\[
q_+-q_-=
\frac{2cu\bigl((a^2+b^2)\lambda-a^2b^2\bigr)}
     {K(b^2-\lambda)}.
\]
Since $y_B-y_A=u\ell$, this is the same $\Gamma(y_B-y_A)$. This derivation independently checks the coefficient and its sign without relying on the author's half-angle expansion.

## 5. Closure and all-$N$ scope

For a closed sequence the vertical increments telescope exactly:
\[
\sum_i(y_{i+1}-y_i)=0.
\]
All edges use the same caustic parameter, so the same coefficient multiplies this sum. Therefore the two sums of positive focal distances are equal, and their ratio is one. This argument has no dependence on the parity of $N$, low-period symmetry, or a special family member. It does not require either sum separately to be constant.

An orbit traversed repeatedly simply repeats every summand. The assumptions already exclude zero-length or focal chords and caustic degeneracy; no limiting argument is needed to make an undefined antipedal intersection meaningful.

The exact checks are supportive algebraic evidence, not the proof of existence or closure of sampled orbits. The independent checker uses unit-normal/support coordinates, exact quadratic-field coefficients for ellipse endpoints, and rational antipedal intersections obtained by adding and subtracting the two endpoint equations. It tests both signs of the coefficient and of vertical displacement, including zero displacement. The all-real identity and the final telescoping argument are mathematical, not inferred from a finite list.

## Reproduction and disposition

From this review directory, the independent controls are:

    python3 independent_checks.py

For the submitted controls, run in the isolated subdirectory:

    cd author_replay
    python3 verify.py

The regenerated verification.json must match the submitted receipt hash listed above. The independent checker uses SymPy; the submitted checker uses standard-library Python.

**Final disposition: claimed_solved, 2/5, for k603 in the source's confocal-ellipse setting.** No mandatory correction remains. Retain the positive-distance definitions, elliptic/nondegenerate scope, and the absence of a novelty or human peer-review claim.
