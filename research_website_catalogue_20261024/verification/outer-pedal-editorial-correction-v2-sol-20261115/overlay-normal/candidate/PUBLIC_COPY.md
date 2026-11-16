Geometry · Elliptic billiards · Research note


# The outer-pedal area centroid in even-period elliptic billiards


Alec Kriebel · Independent researcher · ORCID


13 October 2026 · Version 1.0 · Unrefereed preprint


As an even-period billiard orbit moves around an ellipse, the perpendicular feet of a fixed point on the orbit's boundary tangent lines form a changing polygon. Its signed-area centroid stays fixed wherever that centroid is defined. This note proves the observation of Reznik, Garcia and Koiller, gives the centroid explicitly, and identifies the exact circle on which it can fail to exist for star orbits.





## Read the paper


Open the searchable PDF · Download PDF · Download source and verification ZIP · BibTeX



The reader displays the original deposited PDF. Open it directly to use your PDF viewer's search and navigation. The ZIP contains the LaTeX source and authored verification materials.


Persistent record: doi:10.5281/zenodo.23331331.





## Abstract


Reznik, Garcia and Koiller observed that the area centroid of the outer-side pedal polygon of an even-period elliptic billiard is independent of the orbit phase (invariant k307). We prove this observation on the natural domain of the signed-area centroid and give its explicit value. The proof uses antipodal pairing, support coordinates and telescoping edge moments. For simple even orbits the centroid exists for every fixed pedal point. For even star orbits it can be undefined on a fixed circle, which we determine exactly and realize in a noncircular eight-period example. The note includes a reproducible verification package; the written identities give the all-period proof.





## The polygon and the centroid


Let the billiard boundary be the noncircular ellipse x²/a² + y²/b² = 1, with a > b > 0, and fix the confocal elliptic caustic x²/(a² − λ) + y²/(b² − λ) = 1, where 0 < λ < b². Assume a Poncelet family whose least period N ≥ 4 is even. Primitive self-intersecting star trajectories are allowed; their vertices keep their trajectory order.


For any fixed real point M = (Mₓ, Mᵧ), let Qᵢ(M) be its perpendicular foot on the full tangent line to the boundary ellipse at the billiard vertex Pᵢ. These tangent lines are the sides of the outer polygon. The feet are not restricted to tangent segments.


For complex plane points, write [p,q] = Im(conj(p)q), with conj denoting complex conjugation. With cyclic indices, the signed shoelace area, cubic edge moment and centroid are


S(Q) = ½ Σᵢ [Qᵢ,Qᵢ₊₁]
T(Q) = Σᵢ [Qᵢ,Qᵢ₊₁](Qᵢ + Qᵢ₊₁)
C(Q) = T(Q)/(6S(Q)),  only when S(Q) ≠ 0.


For a star, this is the signed-area centroid with multiplicity. It is not the centroid of the unsigned regions cut out by the star and is not the arithmetic mean of the pedal vertices.





## The full formula and its domain


Set z = Mₓ + iMᵧ and introduce the real quantities


H = (a² + b²)/2,       e = (a² − b²)/2
d = 1 − λ(a⁻² + b⁻²), F = Hd + 2λ
v = −4eλd/(F² − e²d²), G = 2F + d|z|².


For the branch oriented counterclockwise around the caustic, F > 0, F² − e²d² > 0 and the outer-pedal area at the origin satisfies S(0) > 0. For every fixed M,


S(M) = S(0)(2F + d|z|²)/(2F).

C(Q(M)) = z/2
  − { z(F + 2Hd + evd)
      + conj(z)[2Fv + 3ed + (vd/2)|z|²] }
    / {3(2F + d|z|²)},       provided G ≠ 0.


The explicit centroid depends on the ellipse, caustic and fixed pedal point, but not on the orbit phase wherever G ≠ 0. The unnormalized origin area S(0) is not asserted to be phase invariant; it cancels in the centroid quotient.



- If d ≥ 0, the centroid exists for every fixed point M.


- If d < 0, its exact undefined locus is the fixed circle |M|² = −2F/d. The signed area is zero there, so the signed-area centroid is undefined by its definition.


- The least period is four if and only if d = 0. The four-period rectangle case gives C(Q(M)) = M/3 for every M, and is handled before any division by d.


- Every simple winding-one even family has d ≥ 0, so every M is allowed. For a simple family of least period at least six, d > 0.






## Why the phase disappears


The proof begins with the antipodal symmetry of an even least-period elliptic billiard. The forward Poncelet map commutes with central inversion; the finite orientation-preserving circle action identifies inversion with a half-period shift. This applies to primitive stars as well as simple trajectories.


Support coordinates for the boundary ellipse turn the consecutive tangent geometry into an identity for doubled unit normals. A cyclic edge-moment identity telescopes on this auxiliary ordered polygon without assuming that it is simple. Antipodal pairing cancels the odd terms in the pedal construction. Reducing the remaining cubic moments, then applying the translation law for signed first moments, gives both the area factor and the complete centroid formula above. The four-period rectangle branch is established separately.


The contribution is the all-even-least-period signed-centroid formula together with its exact natural domain and the simple/star boundary analysis. The all-period conclusion rests on written identities. The accompanying exact and numerical materials provide reproducible supporting evidence; finite samples alone do not establish arbitrary periods, uniform stability near degeneracies, or a formally certified proof.





## An exact eight-period star


The exceptional circle occurs in a noncircular example with


a² = 221/96,  b² = 27625/20736,  λ = 125/96.


Multiply the following normalized vertices coordinatewise by (a,b), retaining this order:


(0,1), (−12/13,−5/13), (1,0), (−12/13,5/13),
(0,−1), (12/13,5/13), (−1,0), (12/13,−5/13).


This is a primitive physical eight-period star of winding number three. Its caustic has semiaxes 1 and 25/144. The star had already been used in repository problem 5100065; the note uses it as an exact diagnostic rather than claiming a new star construction.


d = −120/221,  F = 2795/1728,  v = 7/13
undefined circle: |M|² = 123539/20736.


Writing M = (X,Y) and R² = X² + Y², the exact signed moments are


S = −√30(20736R² − 123539)/134784
Tₓ = −√30 X(41472R² − 272935)/109512
Tᵧ = −√30 Y(52992R² − 347633)/97344.


At M = (13√731/144, 0), the area vanishes while T = (221√21930/10368, 0) ≠ 0. Thus a genuine nonremovable singularity occurs at this diagnostic point. The centroid is undefined on the entire zero-area circle; a nonremovable pole at every point of that circle is not claimed.





## Conventions and limits


Reversing the trajectory changes the signs of both S and T, leaving their centroid quotient unchanged. Repeating an even least-period trajectory scales the two moments by the same factor. Merely repeating an odd primitive orbit to obtain an even list does not supply the required antipodal pairing and is outside this theorem.


The hypotheses exclude a circular boundary, hyperbolic or degenerate caustics, and zero-signed-area pedal polygons. Conclusions about unsigned region centroids, arithmetic vertex means, or uniform numerical stability at excluded limits do not follow. In the star case the doubled-normal polygon can have negative signed area; the simple-orbit positivity argument is not extended to stars.





## Earlier work and attribution


Reznik, Garcia and Koiller formulated the outer-side pedal area-centroid observation as invariant k307, in Table 4 and the associated discussion of their work. Their published Fifty new invariants of N-periodics in the elliptic billiard (2021) and the separately identified arXiv version 11, Eighty new invariants, are distinct editions.


Bialy and Tabachnikov's Dan Reznik's identities and more supplies neighboring vertex-centroid identities, including k306, and classical even-orbit symmetry. The vertex mean and the signed-area centroid require different moment arguments. Schwartz and Tabachnikov's work on Poncelet centers of mass supplies signed/multiplicity centroid context and general centroid-locus theorems. Applying a fixed-conic Poncelet theorem directly to arbitrary-point outer pedals would require a separate fixed-conic realization, which is not assumed here.


The note credits the original observation and classical methods. Its contribution is the explicit formula, the all-period support and cubic-moment proof, and the exact domain analysis. Historical priority and exclusive firstness are not established.



- D. Reznik, R. Garcia and J. Koiller, Fifty new invariants of N-periodics in the elliptic billiard, Arnold Mathematical Journal 7 (2021), 341–355. Published article. Separate edition: Eighty new invariants, arXiv version 11.


- M. Bialy and S. Tabachnikov, Dan Reznik's identities and more, European Journal of Mathematics 8 (2022), 1341–1354. Published article.


- R. E. Schwartz and S. Tabachnikov, Centers of mass of Poncelet polygons, 200 years after, The Mathematical Intelligencer 38 (2016), no.2, 29–34. Identified arXiv version 1.






## Research status and collaboration


AI tools were used extensively in solving, verification, literature research, writing and adversarial review. This is an unrefereed preprint; it has not received external human peer review or proof-assistant formalization.


Mathematicians working on billiards, Poncelet geometry, signed polygon moments or exact geometric computation are welcome to develop professional collaborations around these contributions. Useful contributions include independent proofs, precise corrections and further applications with explicit hypotheses.


The note and its authored verification materials, including authored code, are available under Creative Commons Attribution 4.0 International. Referenced third-party works retain their own rights.





## Citation


Alec Kriebel (2026). The outer-pedal area centroid in even-period elliptic billiards. Version 1.0. Zenodo. https://doi.org/10.5281/zenodo.23331331. Download BibTeX.




Original Zenodo deposit description


This deposit description differs from the printed abstract above and is reproduced separately.


We prove the k307 outer-side pedal area-centroid observation of Reznik, Garcia and Koiller for billiards in a noncircular ellipse with a strict confocal elliptic caustic and least even period. The ordered perpendicular feet of any fixed point on the boundary tangent lines have an explicit phase-independent signed area centroid wherever their signed area is nonzero. We classify the entire zero-area locus: none when d is nonnegative, and a fixed circle when d is negative. Simple winding-one even families have a centroid for every fixed point; the four-period value is M/3. An exact primitive eight-period star shows that the exceptional undefined locus is real. The note supplies an all-period support-coordinate and cubic-moment proof. The verification archive contains the LaTeX source, exact symbolic and rational certificates, independent high-precision orbit controls, audit reports and reproducibility instructions. The original observation and classical methods are credited. Bounded primary-source audits found no earlier covering proof, without certifying historical firstness. AI tools were used extensively in solving, verifying, literature research, writing and adversarial review. This is an unrefereed preprint and has not received external human peer review or proof-assistant formalization.
