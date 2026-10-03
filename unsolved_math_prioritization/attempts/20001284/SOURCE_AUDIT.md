# Source identity, scope and literature audit

Checked 3 October 2026 UTC. This is a targeted primary-source audit, not an exhaustive bibliographic database search.

## Exact target and access limitation

- Catalogue: [20001284](https://www.unsolvedmath.com/problems/20001284), code AIM-CONVEX_GEOMETRY-0016; title “Finite-dimensional local rigidity from central-section perimeters.” The exact detail page returned HTTP 403 to retrieval and to the cloud browser. Its live detail content was not verified. Search results indexed the matching title in the site's geometry/AIM listing.
- A supplied catalogue snapshot at repository revision 37e53eabe540fb458758e198be61634bd02ee008 was reused. The complete problems-file SHA-256 was 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf, and the research-results-file SHA-256 was 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b. Both were checked. The raw files and extracted records are not included here.
- Original primary source: AIM, *Problems from the workshop “Mahler's conjecture and duality in convex geometry”*, 9–13 August 2010, notes by Jaegil Kim, [official PDF](https://aimath.org/WWN/mahlerduality/mahlerduality.pdf), Problem 20, printed p. 3. The PDF was independently read through web retrieval. The catalogue's extracted “0.” and trailing “2” are extraction artifacts; they are not the original problem number.

The source asks a **global** equality question for **origin-symmetric star bodies in ambient dimension 3**. Sections are **2-dimensional planes through the origin**. Their measured quantity is **1-dimensional boundary length**, not the section area, the 3-dimensional body volume, projection perimeter, or boundary area of a different-dimensional section. The finite-dimensional title is a catalogue partial-result title; it must not narrow the source target.

The results in this packet explicitly assume positive C² or C¹ radial functions where stated. A continuous radial function alone need not produce finite-length section boundaries. This packet does not exploit an infinity-equals-infinity convention to claim a resolution, nor silently assert regularity for all source star bodies.

## Current primary status source

R. J. Gardner, *Geometric Tomography, Second Edition: Corrections and Update*, [version 3.0](https://faculty.gardner.wwu.edu/Update%20Version%203_0.pdf), dated 14 September 2026. The author's [research page](https://faculty.gardner.wwu.edu/research.html) links this version. Printed p. 12, under Problem 7.6, continues to classify the full problem as open. The old 2.1 link in the imported record now returned 404; it was not used as the current status authority.

This update credits an affirmative C¹ body-of-revolution special case to Howard, Nazarov, Ryabogin and Zvavitch, and the convex-polytope case to Yaskin. The Howard–Nazarov–Ryabogin–Zvavitch work remains listed as a preprint in the checked source; its complete primary manuscript was not obtained, so this packet does not overstate details beyond Gardner's report. An open-status statement is evidence about the literature, not a proof that a new local result is impossible.

## Theorems actually inspected

1. V. Yaskin, [*On perimeters of sections of convex polytopes*](https://www.math.ualberta.ca/~vladyaskin/papers/Perimeters.pdf), J. Math. Anal. Appl. 371 (2010), 447–453, [DOI](https://doi.org/10.1016/j.jmaa.2010.05.050). The theorem, on preprint p. 2, assumes origin-symmetric **convex polytopes** in Rⁿ. For each k with 2≤k≤n−1 it uses the (k−1)-dimensional boundary area of all k-dimensional central sections. It is not a theorem for arbitrary star bodies. In n=3,k=2 its quantity is perimeter.
2. Anamaria Rusu, [*Determining Starlike Bodies by Their Curvature Integrals*](https://people.math.sc.edu/howard/Theses/rusu.pdf), University of South Carolina Ph.D. thesis (2008), Theorem 16, printed pp. 13–17, and Corollary 17, p. 17. Radial functions form an analytic one-parameter expansion about the unit ball, converging absolutely in C¹; every body is origin-symmetric and every relevant section has the ball's boundary area. The theorem makes the entire path constant. It does not assert arbitrary two-body C²-neighborhood injectivity. The present local theorem is proved by a different two-point operator estimate and is not obtained by simply invoking analytic-path rigidity.
3. D. Ryabogin and V. Yaskin, [*On counterexamples in questions of unique determination of convex bodies*](https://www.math.kent.edu/~ryabogin/RYversion4.pdf), Proc. Amer. Math. Soc. 141 (2013), 2869–2874, [DOI](https://doi.org/10.1090/S0002-9939-2013-11594-0), Lemma 2.1, Proposition 2.2 and Theorem 2.4. The mechanism uses antipodal switching when **origin symmetry is not required**, giving noncongruent smooth convex bodies (also polytopal examples) with equal central-section intrinsic-volume data. The authors trace the switching idea to earlier Gardner–Volčič and Goodey–Schneider–Weil work. Attempt 5 credits this mechanism; it is not a solution under the source symmetry hypothesis.
4. B. Rubin, [*The Fourier Transform Approach to Inversion of lambda-Cosine and Funk Transforms on the Unit Sphere*](https://arxiv.org/abs/2005.03607), 2020, provides primary literature context for classical Funk inversion. The packet writes out the exact spherical-harmonic multiplier and elementary binomial bounds actually used; it does not rely on an unquoted theorem for its new weighted estimate.

## Excluded near-matches

Makai and Martini, [*Unique local determination of convex bodies*](https://arxiv.org/abs/1602.00959), Acta Math. Hungar. 150 (2016), 176–193, concerns sections in supporting affine planes of an interior reference body, and cap data. Those planes are not the central planes through a fixed origin used here. Its local theorem does not directly resolve this target. Section **volumes** and projection perimeter uniqueness results likewise cannot be substituted for central-section perimeter data.

## Imported partial and present claims

The supplied earlier AI report gives finite-even-harmonic-band local injectivity by the Funk linearization, selection of independent evaluations, and the finite-dimensional inverse function theorem. It explicitly leaves cutoff-uniform local and global questions unresolved. That report is background, not a campaign author turn or a peer-reviewed source.

The present packet supplies a direct, cutoff-independent C² local two-point stability proof and explicit quantitative small-chart sampling, together with precise failed global routes. No exact prior theorem matching the new local statement was identified in the checked sources, but this does **not** establish novelty. No claim of first discovery, human peer review, formal verification or global solution is made.
