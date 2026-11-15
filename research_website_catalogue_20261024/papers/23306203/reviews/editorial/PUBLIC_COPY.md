# An exact period criterion for focal-distance products in elliptic billiards

Alec Kriebel · 11 October 2026 · Native deposit version 1.0.0 · Unrefereed preprint

## Original printed abstract

For a noncircular elliptic billiard with a strictly nested nondegenerate confocal elliptical caustic, we prove that the product of ordinary distances from all vertices to either fixed focus is independent of phase if and only if the least period is 2 modulo 4. This proves the least-period interpretation of entry k₁₁₄ in Reznik–Garcia–Koiller's list of unproved invariants and classifies every other primitive period and every repeated traversal. The proof identifies the complete divisor of the focal-distance factor in the classical Jacobi parameter. An exact doubled-triangle example shows why a condition on return length alone is insufficient. The parametrization, identities and divisor method are established tools. This AI-assisted research note is unrefereed.

<details id="native-deposit-description"><summary>Original Zenodo deposit description</summary><p>For a noncircular elliptic billiard with a strictly nested nondegenerate confocal elliptical caustic, the product of ordinary distances from all vertices to either fixed focus is independent of phase if and only if the primitive least period is congruent to 2 modulo 4. The result covers all admissible primitive star turns and both orientations. For every even least period, the two focal products are equal at each phase. Repetitions raise the positive primitive product to an integer power, so listed return length alone is insufficient. Circles are treated separately; hyperbolic and degenerate caustics are excluded.</p><p>This research note proves the primitive interpretation of the experimentally recorded invariant k114 in Reznik–Garcia–Koiller (2020/2021), establishes the exact period classification, and gives an exact doubled-triangle counterexample to the unrestricted six-event return interpretation. It applies Stachel's published parametrization, classical Jacobi identities and established meromorphic divisor methods. No new-method or exclusive historical priority claim is made. The bounded primary-source audit found no explicit earlier proof of this exact target; novelty of the specific formulation is not certified. Full text of one related 2023 Dragović–Gajić article was unavailable, and the accompanying priority note records that coverage gap.</p><p>The deposit contains the manuscript PDF and a support archive with standalone LaTeX source, exact finite arithmetic controls, independent supplementary theta-series diagnostics, recorded outputs, metadata, references and priority-search limits. Finite checks support the analytic all-period proof; floating-point computations are not validated numerical certification.</p><p>AI tools were used extensively in solving, drafting, source comparison, reproduction and independent adversarial reviews. This preprint is unrefereed and has not undergone conventional human peer review. The author is responsible for its claims.</p></details>

## What the result says

A billiard trajectory inside an ellipse bounces according to the usual reflection law. In a confocal family, every side touches the same inner ellipse, called the caustic. Moving the starting point changes the polygon’s phase while retaining that caustic.

This note asks when the product of the distances from all polygon vertices to one fixed focus stays unchanged as the phase moves. The answer depends on the least period: the number of bounces before the trajectory first returns. Counting a repeated traversal as a longer list can give the wrong answer.

## The full theorem

Fix outer and inner ellipses x²/a²+y²/b²=1 and x²/A²+y²/B²=1, with a>b>0, A>B>0, a>A, b>B and a²−b²=A²−B²=c²>0. The caustic is strictly nested, nondegenerate and confocal. The foci F±=(±c,0) are fixed, and the factors are ordinary positive Euclidean distances from the original billiard vertices, not squared distances or distances from an outer tangent polygon.

For any actual periodic elastic billiard family tangent to that caustic, let n be its primitive least period and set Dₙ±(u)=∏ⱼ₌₀ⁿ⁻¹ |Pⱼ(u)−F±|. Each focal product is independent of phase if and only if n≡2 (mod 4). Every admissible primitive coprime star winding and both orientations are included; n=1 and n=2 cannot occur in this strict elliptical-caustic setting.

For every even least period, Dₙ⁺(u)=Dₙ⁻(u) at each phase. This includes n≡0 (mod 4), when the equal products still vary with phase. Equality between the two foci is a different assertion from phase constancy.

For every integer r≥1, an r-fold traversal gives (Dₙ±)ʳ. Positivity makes this power operation injective, so repetition preserves the primitive constancy class in both directions. For a listed return length N≡2 (mod 4), constancy holds exactly when its least period is even.

## Why least period controls the product

The proof uses Stachel’s classical Jacobi parametrization P(u)=(−a sn u,b cn u), with modulus k=c/A∈(0,1), K=K(k), K′=K(√(1−k²)), cn(v)=B/b and 0<v<K. Here a=A dn(v)/cn(v), and successive vertices are separated by δ=2v=4Kτ/n, where gcd(τ,n)=1 and 0<τ<n/2. Reversing orientation gives the same cyclic subgroup.

The manuscript checks that the tangent contacts lie inside the actual chords and that the two inward rays satisfy elastic reflection across the normal. Real injectivity modulo 4K makes n the true vertex period. The geometric calculation gives the positive ordinary-distance factors g±(u)=a±c sn u; a>c prevents a hidden sign or square-root convention.

On the sn torus ℂ/(4Kℤ+2iK′ℤ), the factor g₊ has two simple poles p=iK′ and p+2K, and two distinct simple zeros p−K±v. These are complete, because zero and pole degrees agree. This torus is used for the focal factor; the full complex boundary map need not have the same imaginary period.

Writing H=⟨δ⟩ for the n-element orbit subgroup, translating the complete divisor through H gives one double zero coset, represented by z=−1/4+τ/(2n), and pole cosets H and 1/2+H. For odd n there are 2n uncancelled simple poles. For even n there are n double poles, cancelled exactly when (−n+2τ)/4 is an integer: precisely n≡2 (mod 4).

A divisor-free meromorphic function on the compact connected torus is constant. In the other classes a pole remains; the identity theorem transfers that nonconstancy to the physical real family. The half-period identity g₋(u)=g₊(u+2K) gives the second focus and the even-period pointwise equality. This is an all-period proof, rather than an extrapolation from finite checks.

For n=2m≡2 (mod 4), the positive constant can be evaluated as ∏ⱼ₌₀ᵐ⁻¹ [a²−c² sn²(2jv)]. It has units of lengthⁿ.

## Why a listed return length of six is insufficient

Take a=√15, b=√7, c=√8, A²=135/16 and B²=7/16. The triangle with vertices (a,0), (−3a/4,7/4), (−3a/4,−7/4), and its central reflection, are primitive three-bounce trajectories in the same fixed confocal family. Their side lines x=−A and x±ay=a are tangent to the caustic, their contact points lie inside the segments, and the inward unit rays satisfy the physical reflection law.

At the fixed focus F₊ their positive primitive products are 15a/2+3c and 15a/2−3c. Traversing each triangle twice produces six listed events, but the two products differ by (15a/2+3c)²−(15a/2−3c)²=90ac=180√30>0.

Thus a return length of six alone does not force phase constancy. The example distinguishes an unrestricted repeated-list interpretation from a statement explicitly about primitive least period; it does not refute that primitive statement.

## Circle and other boundaries

For a circle the two foci coincide with its center, every focal distance is the radius a, and every listed N-event product is aᴺ. This is a separate elementary case: the noncircular pole argument is not continued through c=0.

Hyperbolic or degenerate caustics, grazing or two-bounce limits and uniform lower bounds on the size of phase variation are outside the theorem. Ordinary floating-point agreement does not certify constancy, especially when real variation is below numerical resolution. No validated numerical bounds or proof-assistant formalization are claimed.

## Context and credit

Reznik, Garcia and Koiller recorded the focal product as k₁₁₄. Their final 2021 Arnold Mathematical Journal article, Fifty New Invariants of N-Periodics in the Elliptic Billiard, defines ordinary vertex-to-focus distances and lists the 2-mod-4 observation in Table 2 with an unknown proof entry. Its text does not explicitly resolve primitive least period versus a return list allowing repetitions. The earlier v11 preprint has the different title Eighty New Invariants; editions are not silently substituted.

Stachel’s published 2022 Theorem 4.3 and equation (4.9) supply the classical parametrization. Standard Jacobi periods, shifts and addition identities, and the general meromorphic Poncelet pole-removal method, retain prior credit. Schwartz, Akopyan–Schwartz–Tabachnikov and Roitman–Garcia–Reznik provide method precedents. The target-specific calculation is the focal divisor and its orbit-coset arithmetic; no new elliptic-function method is claimed.

Other products have different factors: k₁₁₅ concerns vertices of the outer tangent polygon, k₁₁₇ concerns caustic-contact lengths, and k₂₀₂ concerns perpendicular distances to sides. Ferudun’s related unrefereed note addresses k₁₁₅, rather than the original billiard-vertex product here.

The source comparison is bounded. No exclusive historical priority, influence, exhaustive literature coverage or present worldwide openness is certified. The full billiard body of the related Dragović–Gajić article remained unavailable, and the inspected author-site Ferudun body was not authenticated as the exact Zenodo-deposit bytes. These limits do not become claims that the unread material is irrelevant.

## Read the complete paper

The complete unchanged five-page searchable paper is available below, with ordinary open and download links. The original support ZIP contains its editable TeX, source and priority notes, metadata, exact finite controls, optional supplementary diagnostics and recorded outputs. The PDF is a separate native asset; the ZIP contains no embedded PDF.

Finite arithmetic controls support the manuscript’s divisor inventories and physical examples. The universal classification rests on its written geometric and analytic proof; supplementary floating-point diagnostics do not replace that proof.

[Open or download the complete PDF](focal_product_period_criterion.pdf) · [Complete original support ZIP](focal_product_support.zip) · [BibTeX](citation.bib)

## Collaboration

Independent verification of the geometric bridge or focal-divisor argument, substantive primary-source comparison, or work toward journal submission would be welcome. Any eventual authorship would reflect actual mathematical or writing contributions agreed together.

## AI assistance and review status

AI tools were used extensively in mathematical exploration and solving, source comparison, exact computation and code, drafting, editing and adversarial checking. Alec Kriebel is the named human author and is responsible for the claims. This is an unrefereed preprint, without conventional independent human peer review, journal acceptance or proof-assistant certification. Internal AI checks do not supply those certifications.

## Rights

The authored manuscript, notes, metadata, verification materials and companion diagnostic code are licensed Creative Commons Attribution 4.0 International (CC BY 4.0), under the actual deposited LICENSE.md. Cited external publications retain their own rights.

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## Related literature

- [Reznik–Garcia–Koiller: Fifty New Invariants of N-Periodics in the Elliptic Billiard](https://doi.org/10.1007/s40598-021-00174-y). Final 2021 article, definitions and Table 2 k₁₁₄; observed invariant credit.
- [Stachel: On the motion of billiards in ellipses](https://doi.org/10.1007/s40879-021-00524-2). Published 2022 Theorem 4.3 and equation (4.9): canonical parametrization.
- [NIST DLMF, Chapter 22](https://dlmf.nist.gov/22). Classical Jacobi periods, poles, shifts and addition formulas.
- [Schwartz: The pentagram integrals for Poncelet families](https://doi.org/10.1016/j.geomphys.2014.07.024). Established meromorphic Poncelet and pole-removal method.
- [Akopyan–Schwartz–Tabachnikov: Billiards in ellipses revisited](https://doi.org/10.1007/s40879-020-00426-9). Classical complexification and pole-cancellation context.
- [Roitman–Garcia–Reznik: New Invariants of Poncelet–Jacobi Bicentric Polygons](https://doi.org/10.1007/s40598-021-00188-6). Related Jacobi/Liouville methods, with different invariants.
- [Ferudun: Focal Distance Products of Outer Elliptic Billiard Polygons](https://doi.org/10.5281/zenodo.23093258). Related unrefereed k₁₁₅ note; distinct outer-tangent vertices and byte-custody limit.
- [Dragović–Gajić: Points with rotational ellipsoids of inertia, envelopes of hyperplanes which equally fit the system of points in ℝᵏ, and ellipsoidal billiards](https://doi.org/10.1016/j.physd.2023.133776). Related article whose full billiard body remains a disclosed coverage gap.

## Citation

Alec Kriebel. An exact period criterion for focal-distance products in elliptic billiards. Zenodo, 11 October 2026. Native deposit version 1.0.0; the printed paper has no version line. doi:10.5281/zenodo.23306203.
