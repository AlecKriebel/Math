# Five outgoing centers in a 16-realization cube move

Alec Kriebel · 15 October 2026 · Unrefereed research note

## Original abstract

We specify six algebraic boundary points, an incoming center, and at least five distinct outgoing centers for a cube move of 16-realizations. Existence follows from strict rational sign bounds for two continuous one-variable residuals. The boundary parameters are uniquely defined real roots of monotone polynomials. This contradicts the at-most-three expectation for construction curves sharing a focus in Remark 4.8 of Melotti–Ramassamy–Thévenin, in the realization setting allowing crossings. The fixed boundary is crossed, so the example concerns no proper embedding. Neither the exact number of centers for this boundary nor a universal maximum is determined.

## Plain language

A local cube move replaces one central point by another while keeping six boundary points fixed. The quadrilateral rule equates the sums of opposite side lengths raised to a chosen power.

At power 16, this note gives one fixed algebraic boundary with an incoming center and at least five outgoing choices. The same boundary works for all of them; its segments cross, so this is a realization allowing crossings.

## Result

Six fixed distinct algebraic points A₁,…,A₆, with both alternating triples noncollinear, admit an incoming center Z and at least five distinct outgoing centers X at α = 16. Every selected center differs from every boundary point.

A quadrilateral PQRS is an α-quad when |P−Q|^α + |R−S|^α = |P−S|^α + |Q−R|^α. The three incoming ordered faces are A₁A₂A₃Z, A₃A₄A₅Z and A₅A₆A₁Z; the three outgoing ordered faces are A₂A₃A₄X, A₄A₅A₆X and A₆A₁A₂X. All six identities hold for the same boundary.

The outgoing centers are at least five intersections of two distinct smooth construction curves sharing the focus A₂. This exceeds the at-most-three expectation for α > 1 in Melotti–Ramassamy–Thévenin, Remark 4.8, p. 811, and the maximum-three conjecture in the crossing-permitted workshop setting, p. 1785. The cited existence theorem is a separate statement.

## Why it works

Set A = (0,0), B = (2073/10000,0), C = (4719/10000,64/10000) and λ = 27/1250. The outgoing equations are |X−B|¹⁶ − |X−A|¹⁶ = λ and |X−C|¹⁶ − |X−A|¹⁶ = 1.

With s = |X−A|¹⁶, nonnegative real eighth roots give the three squared distances. An invertible linear system recovers X; one continuous residual G(s) then characterizes the original equations in both directions, retaining all real-branch constraints.

Strict rational signs at 9/10000, 11/10000, 13/10000, 1/2, 1 and 10¹⁶ alternate. The intermediate value theorem supplies a zero in each of five disjoint finite intervals. Different s give different centers; uniqueness within an interval is unnecessary. A concavity estimate controls the remote endpoint without subtracting nearly equal large radicals.

Three uniquely defined real roots of monotone rational polynomials fix the other boundary vertices. Their exact edge-power identities telescope. For this same fixed boundary, a second continuous residual has opposite strict endpoint signs and produces an actual incoming center. The written algebra verifies every incoming and outgoing ordered face, including the dependent third incoming identity.

Exact rational enclosures separate the selected centers from boundary vertices and every line through a boundary pair. A strict orientation pattern proves an interior crossing of [A₁,A₂] and [A₃,A₄].

Each common-focus curve is individually smooth because its powered-distance difference has a nonzero gradient. The boundary point A₃ lies on one curve and has a strictly positive residual for the other, proving that the two curves are distinct sets. This individual regularity does not assert joint transversality of their intersections.

The original standard-library verifier and rational certificate accompany the proof. Its default command recomputes and compares the complete certificate without writing; integer and Fraction arithmetic decide the signs. The existence argument uses the written distance equivalence, monotone boundary definitions, strict signs and exact face identities.

## Limitations

The fixed boundary crosses. It cannot yield a proper embedding for any choice of central point, and the construction concerns the realization and immersion conventions that permit crossings.

At least five is a lower bound. The exact total for this boundary and a universal maximum are undetermined here. No result for α < 1, root uniqueness within the brackets or joint intersection transversality is asserted.

The note does not establish historical firstness, independence from unknown work or the present worldwide status of stronger questions.

## Background

Melotti–Ramassamy–Thévenin define the α-quad and cube-move realization setting, including crossed faces. Their Remark 4.8 states the common-focus intersection-count expectation addressed by this construction. The Oberwolfach contribution states the corresponding maximum-three conjecture for crossing-permitted α-immersions.

Weighted-distance and pure-power families predate this note. Ash–Bolker study costs φ(|x−P|)+w(P), including a fourth-power example. Their separate oscillatory cost t+k sin(t) is a different example and does not itself settle this pure-power shared-focus count.

Bourne–Peletier–Roper define p-power costs |x−xᵢ|^p−wᵢ in the author manuscript, Definition 4.12; Bourne–Roper also discuss this established family. At p = 16 with weights (0,λ,1), equality of the three costs is exactly the displayed outgoing system. The contribution here is the explicit fixed-boundary count construction, with its incoming witness and face identities.

Read the complete unchanged six-page paper below, open or download the original PDF, or download the complete original verification ZIP. The original standalone TeX is also available separately. The ZIP includes the authored proof and exact verification materials.

Independent verification, a substantive primary-source comparison or work toward a journal submission would be welcome. Collaboration and authorship would reflect actual contributions.

AI systems were used extensively in proof exploration, drafting, code generation and adversarial mathematical checks. This is an unrefereed preprint and has not received conventional human peer review. No formal proof-assistant certification is claimed.

The note and its original supporting artifacts, including the authored code, are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). Cited third-party publications retain their own rights; their full texts are not included.

Alec Kriebel. Five outgoing centers in a 16-realization cube move. Zenodo, 15 October 2026. doi:10.5281/zenodo.23392409.
