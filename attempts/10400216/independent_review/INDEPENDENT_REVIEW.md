# Independent full scoped-partial review: 10400216 / Ohtsuki12.11

## Verdict and exact freeze

**PASS_SCOPED_PARTIALS. The original general-shadow problem remains unsolved after five substantive author turns.** No mandatory mathematical correction was identified in the frozen packet.

This verdict binds the author manifest `c3668164cd8707b6ae59f0a1973bda87970501d6882b88e6dfa506ebff1c09c2`, containing43 files, including:

- `RESULT.md`: `95c21ea31454a0b93c1d41c69effa4fbc554541eedffd2cfed3eaa27747760a7`
- `PROOF_COLLECTION.md`: `b0c1c295738d33b1e0e1d74304f76553dccef0e631ed8ffbf3c23c5412a8f35d`
- all five full `TURN_n.md` proofs and their preserved historical manifests

All43 author hashes, all ten primary PDF hashes, and every historical manifest were verified. All five author receipts replay byte-for-byte, totaling771,420 exact controls. The separately written reviewer checker passes **99,870 exact controls**, including a direct four-port medial construction, direct two-edge-cut tests and independent Euler/cusp calculations. None of these finite checks is treated as a topology oracle or a substitute for the all-size proofs.

The reviewer did not contribute to the author derivation or edit its frozen files. No complete source solution, historical novelty or new geometric theorem is certified. The conservative `unsolved 5/5` disposition is appropriate for what this packet establishes.

## 1. Source target and interpretation

The complete Ohtsuki Section12.4 and printed Problem12.11 concern Turaev shadow diagrams, with the boundary/framing reconstruction indicated in Figure22. The question asks for a shadow condition covering the alternating examples and producing a hyperbolic-volume lower bound. Its immediately preceding motivation already credits the planar alternating-diagram bound and points to the greater efficiency of general shadow diagrams.

The packet therefore rightly distinguishes an exact canonical planar reformulation from a condition on general or moved shadows. The source does not demand a purely local test, an optimal coefficient, or an impossibility theorem. The author's obstructions do not establish any such universal impossibility. Nonhyperbolic alternating knots are not silently assigned a hyperbolic volume; every geometric claim retains its manifold/hyperbolicity hypotheses.

The ten reading copies include separately hashed screen and print versions of Ohtsuki. Their locators match their bytes. Ishikawa–Koda is explicitly the inspected arXivv1 Section5, with the unavailable final-typeset comparison disclosed. The Miyamoto inequality is read in the complete Agol–Storm–Thurston primary source, which explicitly states it; the packet does not claim independent access to Miyamoto's original paper.

## 2. Turn1: canonical small-face obstruction

The Euler calculation is valid for every connected nonempty four-valent planar projection with at least one crossing, allowing loops, multiple edges and repeated facial incidences. It gives E=2n, F=n+2 and total facial deficit8. Every face has positive boundary-walk length. Consequently at least three faces have valence at most3, or at least four when monogons are absent. Any outside-face choice leaves the asserted bounded face.

I visually checked Thurston's printed351 corner rule: opposite corners have the same sign and adjacent corners opposite signs, with magnitude1/2. Thus the canonical sum obeys |2g|<=v with multiplicity counted, and the formal squared slope for a v<=3 face is at most18. This is strictly below4pi². The proof does not identify a relative-shadow formal expression with an actual cusp length without the additional closed special-shadow hypotheses.

The conclusion is properly restricted to an unchanged canonical region or a conversion explicitly preserving its incidence and gleam. It does not exclude moves changing those data. It also does not reverse the Costantino–Thurston shadow-complexity inequality: presentation size supplies an upper bound for volume, not the requested lower bound.

## 3. Turn2: actual partial filling and simultaneous cusp scale

This is a valid conditional relative criterion. A closed special-shadow completion is part of the certificate, rather than assumed for every relative polyhedron.

Costantino–Thurston's neighborhood-of-singular-set construction gives the drilled block manifold with volume2v_oct V. Its cusp for a disk region is filled by the corresponding region attachment. Ishikawa–Koda's detailed Lemma5.3 reconstructs these attachments as primitive solid-torus fillings and gives one simultaneous disjoint horocusp system with squared slope length4g²+k². This is the actual Euclidean length at the specified cusp scale, not normalized length.

The partial-region construction in the author proof is topologically consistent with those sources. Puncturing a disk region and making its new boundary external leaves a collar of the original attaching circle instead of the disk handle. Its external-boundary reconstruction drills that circle; the other disk handles remain attached. Thus it leaves exactly that cusp unfilled in the block manifold. A framing choice on the annulus does not add a missing filled slope. The gleams required by the relative reconstruction are retained on the unpunctured regions; regions meeting external boundary do not require the removed numerical gleam. This argument depends on the specified completion/block description and does not cover arbitrary relative shadows by fiat.

In the cusp lattice with generators(2,0) and(epsilon,k), the region slope has coefficients((2g-epsilon)/2,1). The parity condition on2g makes these integral, the second coefficient makes the slope primitive, and its Euclidean vector is(2g,k). This checks both the half-integral case and the factor of two.

Since4g²+k² is an integer and39<4pi²<40, the strict long-slope condition is exactly Q>=40. The inspected Futer–Kalfagianni–Purcell Theorem1.1 expressly allows filling a subset of cusps with disjoint horoball neighborhoods. Its geometrization qualification is satisfied here. It gives the claimed lower bound for M_I itself. The rational factor3/245 is computed correctly from pi<22/7. The empty filled subset is separately handled by the unfilled block volume.

The conditional incidence obstruction also passes. A connected four-valent singular graph with V true vertices has Euler characteristic−V. Disk attachments add f; annuli with one external boundary component add zero. Under the explicit collapsibility hypothesis f=V+1. There are6V region-corner incidences. Connectedness with a nonempty vertex set and no vertex-free singular component forces each such annulus to meet at least one vertex. If the *extra retained corner bound* holds, Q>=40 forces each filled disk to have at least five incidences. Hence6V>=5(V+1)+u and V>=5+u. None of these hypotheses is silently transported through arbitrary shadow moves.

The coverage gap is real and correctly stated. A lower bound for the newly drilled manifold is not a lower bound for an omitted short filling. Dehn filling has the opposite volume-monotonicity direction. Merely having the expected number of boundary tori also does not identify the original knot exterior.

## 4. Turn3: Tait signs, saturation and the actual knot control

The sign used is the checkerboard/Tait sign, not the oriented crossing writhe. I compared the canonical corner picture with Moffatt's signed Tait/medial reconstruction. The same convention at all crossings makes a medial arc connect a following to a preceding port, so alternation is equivalent to agreement of neighboring Tait signs. Connectedness propagates it through the projection.

Equality |2g_B|=v_B says all incidences at that black vertex have the same sign. A connected Tait graph then has one common edge sign; loops contribute twice but create no exception. Summing v_B=2n proves equivalence with total absolute black gleam n. The defect formula is integral and has the correct factor: n−sum|g_B|=sum min(p_B,m_B).

The marked canonical subcase recovers exactly the credited Lackenby lower bound, with primeness and hyperbolicity retained. It does not establish an intrinsic condition after the planar marking is lost.

I independently rebuilt the wheel as a four-port medial graph. It has one unoriented component, the claimed16-visit word, and the stated strict black/white aggregate signs after changing only edge a. The common-sign over/under pattern alternates; the changed sign does not. Its defect is2. This is a valid nonalternating-diagram countercontrol. The proof appropriately makes no assertion that the knot lacks some other alternating diagram, and its formal outside-face value is unnecessary to the bounded-face countercontrol.

## 5. Turn4: hyperbolic all-k family and exterior-preserving collapse

The stated rotations of the three-vertex multigraph are planar and determine an actual signed medial diagram. The all-k traversal argument passes: the parallel bundle is crossed successively, and its parity determines the two middle visits in the word. Every crossing appears twice on the same component, with opposite branch parity. Thus the family consists of knots for every k>=2.

The primeness argument is valid for this family. A separating two-intersection curve would produce a cut vertex in the black Tait graph, apart from the loop-only alternative; the graph has neither cut vertices nor loops. Its lack of bridges also excludes nugatory crossings. As an additional control, the reviewer tested direct two-edge deletions in the medial projection, independently of the author's Tait cut-vertex test. The graph is neither a two-vertex bond nor a simple cycle for k>=2, so its reduced prime alternating diagram is not the standard two-braid exception. The exact Menasco statement recorded in Lackenby's introduction therefore yields hyperbolicity.

The bigon accounting gives exactly two twist chains: the parallel p bundle and the a,b pair adjoining the degree-two black vertex. Lackenby's upper bound is consequently16v_3, independent of k. The absolute gleam and omitted-outside-face estimates have the stated growth. Therefore a scalar lower bound coercive in any one of those raw quantities fails on this family. This conclusion neither rules out combined/normalized data nor claims a lower-bound impossibility for the original problem.

The collapse is genuinely a move for the same reconstructed exterior. I read Costantino–Thurston's full boundary-color definitions and the canonical construction immediately preceding Example3.15, and visually checked its collapse figure. Coloring the free link boundary external gives the exterior; the outside disk boundary is false and may be collapsed in that construction. The selected A face meets precisely a,p_1,...,p_k once each and misses b. Deleting its single local sector removes one K4-link edge at each affected vertex; suppression of the two bivalent link vertices yields a theta link, not a new true vertex. No affected crossing is visited twice by that face. The remaining b neighborhood is untouched.

Thus the construction supplies a shadow with at most one true vertex, indeed the displayed surviving vertex. Costantino–Thurston Theorem3.37 explicitly covers manifolds with torus boundary. Hyperbolicity gives positive Gromov norm, so ordinary shadow complexity cannot be zero. Its value is exactly one, and volume<=2v_oct follows in the correct direction. No claim that planar gleams survive this collapse unchanged is used.

## 6. Turn5: complete characteristic correction and checkerboard normalization

The geometric input is used with the correct object and hypotheses: a finite-volume hyperbolic interior, an actual essential two-sided surface, its natural parabolic cut, and the actual characteristic decomposition. Agol–Storm–Thurston Theorem9.1 supplies the finite-volume double/Gromov-norm estimate; doubling the hyperbolic guts doubles its volume while graph-manifold pieces contribute no norm. The Miyamoto inequality stated in their Section2 then gives v_oct(−chi(G)). Empty guts cause no exception.

The Euler calculation is correct. A compact orientable torus-boundary manifold has chi(M)=0, and cutting along S gives chi(N)=chi(S). Annular/toroidal frontier has zero Euler characteristic. An I-bundle has the Euler characteristic of its base, including nonorientable bases; the relevant Seifert pieces have Euler characteristic zero. Thus

    −chi(G)=−chi(S)−beta(S).

The product term must be an upper bound on the entire characteristic contribution for a safe lower volume bound. The general nonzero-frontier formula has the correct additional minus-chi(frontier) term. Partial product discovery, unverified normal surfaces and nonannular cell patches do not certify this criterion; the proof says so explicitly.

The parallel-fiber example is legitimate. In the infinite cyclic cover F times the real line, the fiber group injects. A purported boundary-compressing disk projects to a homotopy of its essential fiber arc into the boundary, a contradiction. Cutting along m parallel fibers yields exactly m copies of F times I, all characteristic product pieces, so the raw negative Euler characteristic grows while guts stay empty and the ambient volume fixed. The argument does not purport to defeat a condition excluding such padding.

For prime alternating twist-reduced diagrams, the inspected Lackenby Theorem5 gives precisely the two stated non-bigon-region guts formulas. Its Section3 explicitly explains use of the frontier when a checkerboard surface is one-sided: the additional neighborhood is an I-bundle, leaving the same guts. It contributes no extra factor of two. Applying the modern bound separately to both cuts gives a maximum, and averaging those two bounds gives v_oct/2 times(t−2), not v_oct times(t−2). The packet retains that required half-factor.

This is a valid conditional general-shadow route only when the full surface/decomposition certificates are supplied. The packet does not prove their construction from an arbitrary efficient decorated shadow or their universal alternating coverage. It therefore remains a partial reduction rather than a completed source answer.

## 7. Evidence, turn budget and publication scope

Each turn contains a substantive deduction: a universal canonical short-slope obstruction; a repaired subset-filling criterion and incidence obstruction; a cancellation-sensitive canonical criterion and knot control; an all-size exterior-preserving compression family; and a full product-sensitive lower-bound reduction. Source retrieval and replay are not counted as further turns.

The author's finite checks and the reviewer's99,870 controls have deliberately limited roles. The latter use a separately written four-port model, direct medial edge connectivity, all six local collapse sectors, primitive cusp coordinates and actual orientable/nonorientable base Euler values. Full theorem/source checks, not enumeration, establish the topological conclusions.

An unresolved draft may retain these scoped results with all cited credit and the exact gaps. It must not promote the raw-count controls to a universal obstruction, the canonical criterion to a general moved-shadow theorem, or an incomplete product list to certified guts. The parent retains publication authority. No author-file change is requested.
