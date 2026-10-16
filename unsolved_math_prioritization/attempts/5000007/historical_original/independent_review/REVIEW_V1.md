# Independent adversarial review of 5000007

Review begun 2026-10-01. This report reviews the frozen candidate, not a proof silently changed during review. A separately named revision will receive its own verdict. The review is AI-assisted and is not human peer review or certification of novelty.

## Frozen inputs

- CANDIDATE_PROOF.md: e12f714910e410332c0e028fa410f7157dbf17913a571bb462109e4d8b93a8c1
- EXTERNAL_CERTIFICATE_AUDIT.md: 79a51a6b4813d7221ec4dc88c3a5f60e9234ae4b45652a919daafbb6d4b172c6
- check_certificate.py: a92cb4143ddc8952203290628d7de6a5a462b283c78d48acfda79a54a790da7c
- check_half_turn.py: 3cbb9b90004f0f7e56acfbd8d03ae1ff3fc3d7aed089b49320c79ad226e69e43

All four hashes matched before and after review. The author-generated output JSON files reproduced byte-for-byte. This was only a supplementary check; the independent reconstruction and geometric reasoning below do not depend on importing either author program.

## V1 verdict

The mathematical proof passes for the parity-selected type defined explicitly in the candidate: an interior trajectory has an even number N of face occurrences and beta-alpha=2pi/5, with ordinary edge trajectories also assigned type A0. Its proof covers arbitrarily long and self-intersecting trajectories, without a length bound or global simplicity assumption.

The unqualified upstream extraction, which defines A0 by the numerical difference alone, is false. Do not describe this review as establishing that literal sentence. The original source provides strong evidence for the parity-selected reading, but its shorthand and bare numerical cases overlap in exceptional directions. A scope-corrected final manuscript must put the distinction and the explicit diagonal exceptions up front.

Completion estimate for this V1 review: 100%. Final review of any revised proof and final publication/budget decisions are separate.

## 1. Source interpretation and exceptional directions

I inspected the actual pixels of Fuchs Figure 8, printed p.502, and the odd-polygon table, printed p.505, as well as the surrounding definition, diagonal calibration, p.506 shorthand, and Conjecture 3.2. Figure 8 marks the terminal interior angle as pi-beta, not beta. It uses the outgoing boundary ray of the oriented billiard polygon. Developing the billiard reflects its labels at every crossing; a consistently outward-oriented physical dodecahedron face is not that labeled polygon after an odd number of reflections.

The sentence preceding Definition 2.1 assigns the difference relation to even N and the sum relation to odd N. The definition presents n-2 distinct types and Figure 9 fixes both ordinary diagonals as non-A0. Those facts justify interpreting the formulas with their parity-selected sign. This is an explicit contextual interpretation of a source whose isolated shorthand is not literally sufficient, not a new unmentioned assumption in the proof.

Here is a complete control for the extraction issue. Normalize p0=0, p1=1, and p(j+1)-pj=r^j with r=exp(2pi i/5). The one-face diagonal p0 to p2 has alpha=36 degrees. Its outgoing terminal billiard ray has angle 144 degrees, while its reversed tangent has angle 216 degrees. Thus the terminal interior angle is 72 degrees, beta=108 degrees, and beta-alpha=72 degrees. Nevertheless N=1 and beta+alpha=144 degrees, giving A2 in this orientation. The reflected diagonal p0 to p3 has alpha=72 degrees and beta=144 degrees, and is A1. Both have graph-distance-two endpoints.

These are exactly the interior exceptions added by the difference-only definition. For odd N, beta+alpha is an integral multiple of72 degrees. Combining this with beta-alpha=72 degrees and 0<alpha<108 degrees leaves alpha=36 or72 degrees. Both initial directions hit an initial-face vertex immediately, so there is no longer first-vertex trajectory in either direction. Boundary directions alpha=0 or108 degrees are edges, with graph-distance-one endpoints.

## 2. Double-pentagon germ identification

The candidate's P and Q=conjugate(P) have the correct five parallel side identifications. The map h(z)=1-z interchanges the pentagons and descends to their half-turn involution. Explicitly, h(pj)=q(1-j), with indices modulo 5. It maps the initial p0 corner to the q1 corner. On each glued edge the induced map reverses the edge parameter, so its five regular fixed points are precisely the edge midpoints; polygon interiors are exchanged. The common vertex is the remaining fixed point.

For an even number of developed faces the final occurrence is a translate of Q. If theta is its outgoing clockwise boundary-ray direction, the terminal sector gives theta=alpha-beta modulo 2pi. The A0 relation therefore selects theta=-72 degrees, which is the unique outgoing Q ray at q1. The reversed terminal germ transformed by h has the same corner, direction, and unit-speed parametrization as the initial germ. Uniqueness of continuation on the flat surface until the first singularity proves h(sigma(L-t))=sigma(t). Self-intersections do not compromise this parameterized argument.

There is no hidden appeal to a conjectural Veech orbit classification. The first-vertex condition is preserved by the translation covering: polygon interiors and open sides project to the same kinds of points, and only polygon vertices map to the double-pentagon singularity. The regular midpoint therefore lies on a glued side at its midpoint. Its lift to the original dodecahedron is a physical edge midpoint, regardless of the sheet of the unfolding.

Conversely, for an interior germ a reverse-invariant saddle connection must end in h(p0)'s Q corner, hence must have even N and the same 72-degree relation. Boundary-edge cases are handled separately. Thus the claimed virtual-Weierstrass identification is valid for the explicitly parity-defined class.

## 3. Physical endpoint exchange

The edge-midpoint axis of a regular dodecahedron has a 180-degree rotational symmetry. At its regular intrinsic fixed point its developed differential is-I. Applying that rotation to the reversed parameterized geodesic produces the same midpoint germ. Uniqueness up to the first vertex in either direction forces endpoint exchange, even for a self-intersecting image. No assumption that the whole hyperelliptic involution descends from the cover is required.

The frozen finite check of edge-axis rotations is correct on inspection and reproduces. Independently, the dodecahedral graph G(10,2) gives the same endpoint-distance histogram 4,8,4,4 for distances 1,3,4,5 under its corresponding fixed-point-free edge-swapping involution.

## 4. Independent exact witness reconstruction

The separate program reviewer_exact_check.py was authored for this review and represents the cyclotomic field as rational four-tuples modulo Phi_5. It imports no author or external checker. Billiard labels are transported combinatorially using alternating cyclic orientation, independently of the coordinate reconstruction.

It verifies all 15 printed crossing parameters by exact substitution, their strict ordering and open-edge location, strict interior points for every convex face subsegment, and the absence of intermediate collinear developed vertices. It independently confirms squared length (307+137sqrt5)/2 and endpoint graph distance 2.

The final physical endpoint 2 has billiard label1; the next billiard label2 is physical vertex 16. The source outgoing ray is therefore2->16, with developed vector r^3 and direction216 degrees. The initial direction satisfies0 < alpha < 36 degrees by exact signs. Consequently pi-beta=36 degrees - alpha, and beta-alpha=144 degrees. The witness is source type A1.

The physical outward ray 2->10 instead has direction108 degrees. The external identity involving that ray is true, but its77.041...-degree interior angle is neither the selected terminal source interior angle nor beta. The external source-type identification therefore fails even though its geometric trajectory is valid.

The pinned external proof was independently fetched through the GitHub read connector and matches the saved text exactly: Git blob 29d80113dc2c8fe54568e59e8ce7262a3f24a565; content SHA256 84baf6ab43b2c33c7a1b11e50e47fe2b48d891da981f44da9da18f4a5ba60513. No external software was executed.

## 5. Suggestion, expressly separate from the frozen proof

The author sent a post-freeze simplification of Lemma 3. It is valid on independent examination: a graph-distance-two pair has a unique common neighbor because the dodecahedral graph has no 4-cycle. An automorphism swapping the pair fixes that neighbor. A nonidentity rotation of order2 cannot fix a dodecahedral vertex, whose rotational stabilizer has order 3. Thus an edge-axis half-turn cannot swap a distance-two pair. The reviewer checker independently verifies the no 4-cycle property from the face incidence data. This is not silently substituted into V1; use it only in a separately reviewed revision.

## 6. Attribution, search, and limits

Classical inputs must be credited. Athreya-Aulicino-Hooper Section 5 already defines virtual-Weierstrass saddle connections and proves their midpoint characterization; Proposition 5.1 uses the physical midpoint involution for coincident endpoints, and Theorem 5.2 rules out closed such connections on the dodecahedron. Section 4 supplies the translation-cover framework. The candidate adds its explicit source-angle identification and the distance-two exclusion; it must not present the general virtual-Weierstrass construction as new.

Primary-source checks and targeted web searches on 2026-10-01 did not locate an authoritative later resolution of this precise source-type distance-two statement. That limited search is not evidence of worldwide priority. The conflicting public certificate is an unrefereed claim and has the specific type error above. No outreach is authorized or needed.

The lost historical attempt count remains a separate provenance issue. This review does not reset the count, grant a new proof budget, certify that a prior candidate was found within that budget, or authorize queue promotion. It validates the supplied complete proof at its stated scope.

## Sources

- Fuchs (2021), official journal PDF: https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf, pp. 501-506 and 514-515; local PDF SHA256 9550009b3a903727a89abba863c520def9bf900b6bec779b63ef6cc82d43f01d
- Athreya-Aulicino-Hooper, arXiv 1811.04131v2, Sections 4-5: https://arxiv.org/html/1811.04131v2
- External literal proof at fixed commit: https://github.com/DannyExperiments/dodecahedron-short-geodesic-counterexample/blob/7b403decdc9317f6ba3dc2c4a91243a0bf0c9ff9/proof/PROBLEM_AND_PROOF.md
