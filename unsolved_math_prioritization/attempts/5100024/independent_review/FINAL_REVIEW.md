# Independent full review: k406,a / 5100024

**Verdict: PASS for the complete domain-qualified statement and the analytic zero-area existence result.** No mathematical revision is required. The vertex centroid is always the center; the ordinary signed-area centroid is the center wherever its signed-area denominator is nonzero. Zero-area configurations really exist. A constant extension is explicitly distinguished from a defined quotient. This is a classical-symmetry consequence with a checked domain analysis, not a certified historical discovery.

## Exact inputs and independence

Reviewed unchanged `PROOF.md`, SHA-256 `6569729e6152ae1711f12ad88483af5e6346aa8d7b99dad234e49010e5c934d2`, bound by `MANIFEST.json`, SHA-256 `fb8d7dc044588c2116163146a317b8977fb6754e521a21f8d8d025abdffd72b2`. All nine manifest entries and three complete primary PDFs match their recorded hashes. The full original record and prior report were read. This review was performed after the candidate froze, without authoring or supplying its proof. The reviewer previously worked on other elliptic-billiard pedal invariants and read related canonical parametrizations; that background is disclosed, but there was no contribution to this antipedal candidate. The independent checker imports no author functions.

The author has one substantive research turn. This review is validation, not an additional author attempt. Publication and queue disposition remain with the campaign coordinator. The review is adversarial AI validation, not human peer review.

## 1. Independent source verdict

Both complete editions were inspected, including visually rendered Table 5: [arXiv v11](https://arxiv.org/pdf/2004.12497v11), p.7, and [published article](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), p.348. The row is stable: k406,a concerns the **outer polygon's antipedal**, both vertex and signed-area centroids, even period, and M=O. Section 3.5 and its self-intersection footnote support the signed convention. The neighboring k405 concerns the original polygon and is distinct; [PR140](https://github.com/AlecKriebel/Math/pull/140) also has that distinct scope. No focal claim from it is imported.

A minor edition-location clarification is recorded here without changing the frozen proof: the centroid quotient is in **v11 §2**, whereas the **published edition puts it in §3.4, p.346**; published §2 gives the signed area. The candidate's unqualified reference to “Section 2” is correct for v11 and should not be read as the published location. The formulas themselves agree exactly. The source's perpendicular “rays” describe the usual supporting-line antipedal construction used in its polygon diagrams and in the restored record.

[Stachel, *On the motion of billiards in ellipses*](https://doi.org/10.1007/s40879-021-00524-2), Theorem 4.3 and (4.9), p.1614, were read in the complete published PDF and visually checked. They give the step 2v, v=2τK/N, and the displayed axes for a nested confocal elliptical caustic. The least-period convention is implemented by gcd(N,τ)=1, not by merely listing an odd orbit twice. Reversal permits 0<τ<N/2; primitive stars remain covered. Hyperbolic/collapsed caustics and two-bounce degeneracies are not within the restored scope. The circle serves as a comparison limit; actual zero-area examples obtained below are noncircular.

The real half-period identities and derivatives also agree with [DLMF §22.4](https://dlmf.nist.gov/22.4) and [§22.13](https://dlmf.nist.gov/22.13). The question marks in old source tables and the prior report's literature search do not establish novelty or current unresolved status.

## 2. Finiteness, primitive pairing, and moments

The axes formula indeed yields a strictly nested confocal pair: a²−α²=b²−β²=β² sn²(v)/cn²(v)>0 for 0<v<K. The real pair (sn u,cn u) has least joint period 4K and is injective over one traversal, so a reduced τ/N produces N distinct vertices and exactly that least period.

For even N, τ is odd, and adding N/2 steps adds 2τK. Hence the opposite vertex is its negative. This is the relevant symmetry; there is no invalid cancellation of a factor of two in a modular equation.

The eccentric-angle lift t(u)=am(u)+π/2 satisfies t'>0 and t(u+2K)=t(u)+π. Every forward increment of size δ<2K is therefore strictly between zero and π, including stars. Its midpoint-angle tangent formula has denominator cos(d)>0. Moreover the difference of successive midpoint angles is half the sum of two such increments, strictly between zero and π. Thus det(R_i,R_{i+1})>0, and both successive original tangents and successive antipedal lines have unique finite intersections. This reasoning does not assume that the derived polygon is convex or has positive area, nor does it overlook a singular phase.

Negation commutes with both line-intersection operations, so Q_{i+N/2}=−Q_i. Vertex sums cancel. Opposite edges have equal signed cross products and opposite endpoint sums; their first-moment terms cancel exactly. Division is used only after imposing A(Q)≠0. Reversal changes the signs of area and numerator together, preserving a defined centroid. Repetitions of an already even primitive polygon do not affect the identity, but repetitions cannot create the primitive parity hypothesis.

## 3. Independent check of the smooth signed-area formula

I recovered the limiting envelope in eccentric angle, rather than repeating the candidate's polar substitution. Put R=(A cos t,B sin t), D=A²−B². Solving

    R·q=R·R,       R'·q=2R·R'

gives

    q_x=A cos t+(D/A)cos t sin²t,
    q_y=B sin t−(D/B)sin t cos²t.

Consequently the first/third harmonic coefficients are

    q_x=(A+D/(4A))cos t−D/(4A)cos(3t),
    q_y=(B−D/(4B))sin t−D/(4B)sin(3t).

Orthogonality in (1/2)∫det(q,q')dt gives

    area/π=(A+D/(4A))(B−D/(4B))+3D²/(16AB)
          =AB−D²/(8AB).

This independently confirms the candidate's integral, sign, and factor eight. The separate checker verifies the two envelope equations modulo cos²t+sin²t=1 and the symbolic harmonic identity. The area is π for (A,B)=(1,1), −97π/32 for (4,1), and −97π/512 for (1,1/4). The result is signed parametrized area; a negative value is not an assertion about ordinary unsigned region area. Cusps or crossings of the envelope do not invalidate the integral.

## 4. Actual finite-period zero-area existence

The analytic existence argument passes independently of every numerical diagnostic.

Fix a nondegenerate caustic and use τ=1 with even N tending to infinity. Regard δ=4K/N as a real parameter near zero and substitute v=δ/2 into the axes formula. This gives a smooth family of outer ellipses tending to the caustic. The midpoint-angle formula for R_δ(u) extends smoothly to δ=0, with denominator tending to one.

In the divided-difference system, each quotient is an integral of the corresponding derivative over u+sδ, 0≤s≤1. It therefore extends smoothly in both variables. At δ=0 the determinant is det(R,R')=αβ dn u, uniformly bounded below by αβ sqrt(1−k²)>0 on the compact period. Matrix inversion consequently gives a smooth periodic Q_δ near zero, with uniform first and second derivative bounds. The limit is exactly the envelope audited above. This also justifies differentiating the parametrized family; a pointwise limit alone would not have sufficed.

Write det(Q_δ(u),Q_δ(u+δ))=δ det(Q_δ,Q'_δ)+O(δ²), uniformly in u. Since Nδ=4K, summing contributes O(δ), and the remaining Riemann sum converges to (1/2)∫det(q,q')du. This proves the claimed area limit, rather than assuming polygonal area is continuous under only pointwise convergence.

At k₀=sqrt(15)/4 with α=1, the limiting area is strictly negative. Hence every sufficiently large even N has negative area at that endpoint, for a fixed phase (for example u=0). At k=0 the same fixed N, τ=1 family is a regular polygon with positive area. For this fixed N, K, the axes, and all intersections vary continuously on 0≤k≤k₀; their determinants do not vanish. The intermediate value theorem therefore supplies a k_* strictly between the endpoints with exactly zero signed area. The resulting pair remains strictly nested, confocal, nondegenerate and noncircular, and gcd(1,N)=1 ensures primitive even period. The proof changes the ellipse pair when varying k, which is entirely legitimate for the asserted existence of admissible zero-area configurations. It does not claim a zero in every fixed Poncelet family.

The absence of an explicit numerical N or a certified numerical root is not a gap in this existential proof. The numerical sequence in the independent receipt is only a diagnostic.

## 5. Optional extension and exact scope

At each fixed reduced even (N,τ), the area is real analytic on the connected full parameter space of 0<k<1 and normalized phase. All line denominators are nonzero. Its circular limit is positive: with α=1 the antipedal circumradius is sec³(v), so its signed area is N sin(2v)/(2 cos⁶(v))>0. Therefore the analytic area is not identically zero and its zero set has empty interior. The nonzero-area domain is dense in this **full parameter space**, making the constant extension uniquely continuous there. This is not a claim that the nonzero-area subset must be dense in each separately fixed ellipse family; none is needed.

The extension does not make the source's quotient defined at a zero denominator. Thus the packet proves the entire natural-domain invariant and separately diagnoses why a literal all-configurations-defined reading would be false. Preserve both qualifications in any publication. No stronger unsigned-area centroid claim, focal statement, hyperbolic-caustic extension, or priority claim is approved.

## 6. Reproduction and final disposition

The author script was read and executed in an isolated replay directory. Its output matches `verification.json` byte for byte: **23,800 exact assertions** and **9,976 separately labeled 80-digit diagnostics**.

The separately authored `independent_check.py` passes **16,506 exact assertions** over 124 rational centrally symmetric ellipse polygons, including star orderings, reversal, repetitions, translation covariance, negative signed areas, a general zero-area symmetry control, and a symbolic envelope calculation. It also passes **16,298 numerical diagnostic assertions** at 65 digits over 88 actual Jacobi-billiard families and nine additional limit/circle cases. These numerical tests do not certify a zero or substitute for the analytic proof. No author functions are imported; the numeric construction uses midpoint tangent intersections and a line-through-point parameterization instead of the author's Cramer-rule implementation.

All nine frozen author files and three primary source hashes pass. No author files were changed. `REVIEW_MANIFEST.json` binds the portable top-level review files; omit local `reading/` and `author_replay/` directories from publication. Run `python3 independent_check.py` with installed SymPy/mpmath to reproduce its JSON output.

**Final recommendation:** accept this as the complete classical consequence on the restored natural domain after one author turn, with the genuine zero-area qualification and explicit optional-extension distinction retained. The minor edition-specific citation location is corrected in this review. No mathematical correction or further author search is required for this target.
