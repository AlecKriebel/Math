# Independent audit of the order seven free exterior kernel

**Theoretical-edition note.** This is the complete authored mathematical audit, with only the provenance/privacy and unavailable-artifact edits documented in PROVENANCE.md. Its computational passages describe historical supplementary checks. The scripts, fixtures, outputs, and logs are not included, and preparation of this edition did not rerun them. This is an AI mathematical audit, not human peer review or formal proof-assistant verification. Original authored-artifact hashes below identify the pre-edition documents, not any edited public copies.

Problem 10400035 / AMR-103-0035 / Stanford Question 2.13. Audit of substantive approach 3; this audit introduces no additional proof-search approach.

## Verdict and accepted scope

**ACCEPTED.** The frozen argument proves that the space of rational ordinary finite-type invariants of smooth, ordered, upward-oriented, unframed two-string links contains a nonzero invariant of exact order seven that vanishes on every string link whose actual exterior fundamental group is free of rank two. Consequently

\[
N_7(2)\ne0,\qquad N_n(2)\ne0\quad(n\ge7).
\]

The proof's two essential inputs pass independently: every such free exterior is fixed by the particular label-preserving simultaneous reversal used in the finite-type argument, and the Duzhin--Karev seven-legged diagram survives in the ordinary unframed rational diagram space. Rational integration followed by antisymmetrization then gives the asserted invariant.

No mathematical correction to the frozen proof or its geometric support lemma is required. This is a source-backed mathematical audit with independent exact computation, not a formal proof-assistant verification. The invariant is existentially constructed through a rational weight system and integration. A closed formula or a numerical value on a named nonsingular string link is not supplied or required by the stated claim.

Acceptance makes no claim about the least possible order, orders three through six for two strands, or higher-order kernels for three or more strands. It does not establish novelty. The earlier accepted results and audits remain unchanged.

## Exact input binding

The initially announced draft hash was superseded before substantive acceptance. This report binds only to the final freeze communicated and verified during this audit:

- `PROOF_KERNEL_ORDER_SEVEN.md` (before the documented edition-only redactions): 18,687 bytes; SHA256 `0f2641cee6c3ac7bc6b8590aa052c2be59473e356fb5358d3989bdacb5213eef`.
- `MARKED_FREE_REVERSAL_LEMMA.md`: SHA256 `e82a3d37dcfaf98bafd6fa9afb1e2b6da37904769d1146b553a082698e549db1`.

The independent checker verifies all 29 entries in the turn-three manifest. It additionally verifies every entry in the preceding proof and audit manifests: 24 in turn one, 7 in the turn-one audit, 36 in turn two, and 71 in the turn-two audit. Thus 138 predecessor entries and 167 entries overall match their listed lengths and hashes. The manifests themselves are hashed in the independent results. The author scripts were replayed on temporary copies, so their output-writing behavior did not alter the frozen input packet.

## The exact marked geometric statement

### Category and involution

The two basepoints are distinct points on the real diameter of the transverse disk. The fixed rigid map is

\[
r(x,y,t)=(x,-y,1-t),\qquad
(\rho\gamma)_i(s)=r(\gamma_i(1-s)).
\]

Its ambient determinant is positive. Each label is preserved, each strand's two endpoints are exchanged by the ambient map, and reversing the interval parameter restores the upward direction. The standard collars are restored as well. This operation has square equal to the identity and does not exchange the two strands. A different basepoint configuration may be identified once and for all with this one; it is not being varied separately for each link.

Both the actual operation and its diagram-level action were checked. Ambient orientation is preserved and both oriented branches at every crossing are reversed, so the ordinary crossing-change filtration is preserved. There is no use of a mirror, a label-swapping planar half-turn, an orientation reversal of only one component, or a variable boundary re-marking.

### Actual freeness gives a handlebody

For the compact exterior, the outer sphere with four disks removed is joined to two lateral annuli. Its boundary is a connected closed genus-two surface. Removing the arc cores or the interiors of regular neighborhoods gives the same fundamental group.

The irreducibility argument is valid in the smooth category. An embedded sphere in the exterior bounds a ball in the ambient ball. Every removed tube is connected, avoids the sphere, and reaches the outer boundary; it cannot lie in the interior ball. Hence that ball lies in the exterior.

If a positive-genus boundary component were incompressible, its closed surface group would inject into a free group. This is impossible because every subgroup of a free group is free, whereas a closed positive-genus orientable surface group is not. The Loop Theorem supplies a compression. Cutting along a properly embedded disk preserves irreducibility: the disk cannot enter the ball bounded by an interior sphere disjoint from it, because its boundary lies on the manifold boundary. Reconstructing a disk cut attaches one-handles, so the component groups after cutting are free factors and remain free. Compression terminates; for example, the sum of `3g-2` over positive-genus boundary components decreases. Irreducible final components with spherical boundary are balls. Reversing the cuts constructs a handlebody.

This verifies the supplied argument without assuming bottom meridians form a basis and without replacing the full group by nilpotent quotients. Nogueira's Appendix 4 also explicitly records the free-tangle group/handlebody equivalence. Hatcher's smooth Schoenflies and Loop Theorem statements support the elementary compression proof. There is no appeal to a tangle being a braid or being trivial.

### Boundary marking before extension

The crucial construction is the boundary identification from the trivial exterior to the actual exterior. On the outer four-holed sphere it is literally the identity. On each lateral annulus it is furnished by a tubular chart prescribed to be standard at both ends.

These tubular charts exist. The oriented normal bundle of an interval is trivial, and any two prescribed endpoint frames can be joined. The possible integer twists represent choices of chart rather than an additional framing requirement on the string link. Annular and outer-sphere maps agree on the seam circles and in sufficiently small standard end neighborhoods.

Conjugating the trivial exterior's half-turn by this complete boundary identification gives the desired map on the whole closed boundary. It equals the original rigid half-turn on the outer sphere and has tube-coordinate formula

\[
(z,s)\longmapsto(\bar z,1-s).
\]

It has six fixed points, two on the outer sphere and two on each annulus. Equivalently, it is explicitly conjugate to the standard genus-two hyperelliptic involution. The boundary identification is not assumed to extend over the handlebodies, so this construction does not smuggle in a trivialization of the actual tangle.

### Centrality gives the required exact extension

The hyperelliptic mapping class is central in the orientation-preserving mapping class group of the closed genus-two surface and has a standard handlebody extension. Choose any orientation-preserving diffeomorphism from the actual genus-two handlebody to the standard one. Conjugating the already prescribed boundary map by this diffeomorphism yields a boundary mapping class equal to the standard hyperelliptic class. Thus there is a handlebody diffeomorphism whose boundary restriction is isotopic to the prescribed map.

That statement alone would not yet prove the marked result. The supplied collar correction fills precisely this gap. If the extension's boundary map is `sigma` and the required map is `tau`, the diffeomorphism `tau sigma^{-1}` is isotopic to the identity. Extend a surface isotopy through a boundary collar, equal to its terminal value near the boundary and to the identity at the inner edge. Composing the original extension with this collar diffeomorphism makes its restriction exactly `tau` everywhere.

The intermediate surface isotopy need not preserve individual annuli or the outer sphere; no such property is needed because only the final corrected boundary map is glued. Standard uniqueness and straightening of smooth collars lets this extension have the compatible product germs. This remains true at the seams after compatible rounding, because the tubular charts were standard at their ends.

Bruno--Mecchia, printed page 272, directly states the two mapping-class facts used here. Its surrounding discussion concerns closed genus-two three-manifolds, but the relevant paragraph states the surface/handlebody facts in full generality. No hyperbolicity assumption is imported into this tangle argument. The downloaded primary source is sufficient; the unavailable Haas--Susskind PDF is supplementary and is not a missing dependency.

### Tube filling and boundary-fixed isotopy

Fill each annulus by its explicitly prescribed tube diffeomorphism. Complex conjugation in the disk and interval reversal have negative determinant separately and positive determinant together. The filled map preserves each tube and label, reverses its core parameter exactly, and agrees with the original rigid half-turn on the endpoint disks and standard end neighborhoods.

After gluing, the resulting ball diffeomorphism `h` satisfies

\[
h(\gamma_i(s))=\gamma_i(1-s),\qquad h|_{\partial C}=r|_{\partial C}.
\]

It can be made equal to `r` on a boundary collar. An involution property for `h` is neither obtained by the collar correction nor needed. Composing with `r` gives

\[
g=rh,\qquad g|_{\partial C}=\mathrm{id},\qquad
g(\gamma_i(s))=(\rho\gamma)_i(s).
\]

Hatcher's relative-ball theorem makes `g` isotopic to the identity relative to the boundary; the usual collar-straightening version preserves a smaller boundary collar. The induced isotopy is therefore in the requested fixed-endpoint, ordered, upward-oriented category. Extending it by the identity outside the ball gives the corresponding fixed-at-infinity isotopy.

This also identifies why arbitrary tube twists do not invalidate the conclusion. Changing a chart changes both the boundary involution and its tube filling by the same conjugation, while their endpoint restrictions and core-reversal identity stay exact. No residual pure braid or four-punctured-sphere mapping class remains, since the final ambient map is pointwise the identity on the entire outer boundary and is isotopic to the identity relative to it. The proof asserts no preservation of an independently chosen framing.

The resulting universal statement `rho L = L` holds for every actual free two-string exterior. It was not inferred from any finite collection of examples. The genus-two centrality input is essential, so this proof has no automatic higher-strand extension.

## The finite type and ordinary rational input

### The source reversal convention agrees

Duzhin--Karev v5 defines numbered long components with standard lines `(i,0,t)` and defines inversion by reversing every component orientation. Restoring the upward convention uses the orientation-preserving rigid motion `(x,y,z) -> (x,-y,-z)`. This keeps each numbered asymptotic line in its position and becomes the specified `r` after centering the longitudinal coordinate. On chord diagrams the source explicitly reverses vertical order while leaving the vertical support lines in place, as verified visually on pages 2 and 3.

Consequently the source operation is the required simultaneous label-preserving reversal. The argument does not replace it by the operation obtained by exchanging horizontal strand positions. The source's long/string equivalence supplies the same ordinary finite-type symbol algebra in the compact ball category after fixing the collars. In particular, the fixed-ball formulation does not require any extra outside braid.

### The seven-wheel is a rational nonzero odd symbol

The diagram in Proposition 2 was inspected visually. Reading its colors in the appropriate cyclic direction gives `1121222`; reading the opposite direction gives the reversed necklace. It is a connected wheel with seven trivalent and seven univalent vertices, hence degree seven. The source fixes vertex cyclic orientations by its planar convention. A possible global orientation sign does not affect nonvanishing or oddness.

Lemma 4 transports simultaneous reversal through symmetrization to the parity of the number of legs. Thus this seven-legged diagram is negated. Proposition 2 gives its nonzero Lie-weight image. The independent finite-dimensional integer calculation below confirms nonzero evaluation without invoking algebraic independence of stable necklace generators. This matters because the source's broad invariant-theory discussion does not itself supply a precise reference for every stability assertion.

The calculation initially proves nonvanishing in the framed diagram space. It is not by itself a proof of ordinary unframed survival, and the audit does not treat it as one.

### The 1T quotient is genuinely handled

Section 6 of v5 explicitly handles the one-term relations and distinguishes framed and ordinary links. Lemma 8 places the connected heptapus in the ordinary subspace because it is a connected Jacobi diagram different from the two deleted monochromatic struts. The concluding paragraph applies that statement to Proposition 2 itself. This is the controlling version and the required deframing input; the earlier retained v1 is not substituted for it.

There is also a structural consistency check. Symmetrization preserves the diagram coalgebra and sends the connected wheel to a primitive element. The framing primitives are the degree-one self-struts. Quotienting by those central primitives removes the framing directions while preserving the complementary connected primitive of degree seven. Thus the specific deframing conclusion used here is consistent with the primitive-space description in Section 6. No assertion that an arbitrary raw `gl_N` weight functional already annihilates 1T is needed.

### Rational integration and antisymmetrization

On page 2 the source permits a characteristic-zero coefficient field, explicitly including the rationals, and states symbol surjectivity onto the ordinary weight systems that annihilate isolated chords. In a fixed degree, the relevant diagram space is finite dimensional over the rationals. Since the ordinary class of the wheel is nonzero, a rational functional `W` can be chosen with value one on it.

Set `W^- = (W - W composed with tau)/2`. Its value on this odd class is one, and `W^- composed with tau = -W^-`. Integrate `W^-` to a rational ordinary invariant `f` of order at most seven. Define

\[
v=(f-f\circ\rho)/2.
\]

The symbol of the pullback is the pullback of the symbol by the diagram involution, as stated in the source's Lemma 1. Therefore the degree-seven symbol of `v` is exactly `W^-`, rather than zero or twice a wrongly normalized functional. This proves exact order seven and nonzero value somewhere on the full ordinary string-link space. It does not require `f` itself to be exactly odd before antisymmetrization.

For every free exterior, the independently established equality `rho L = L` gives `v(L)=0`. Thus the same nonzero `v` lies in every `N_n(2)` for `n >= 7`. This is the full accepted conclusion.

## Independent arithmetic and adversarial verification

The independent checker does not import the author's arithmetic functions. It constructs all terms of the product of adjoint operators recursively as operators of the form `M -> A M B`, then takes cyclic trace classes. This reproduces the four terms

\[
N(T_{1121222}-T_{1122212})+3T_2(T_{112212}-T_{112122}).
\]

A second computation explicitly forms the 16 by 16 matrices of the commutator operators on the matrix-unit basis of `gl_4`, multiplies them, and takes their trace. It is independent of the four-term reduction. For the two displayed integer matrices it obtains:

- `T_empty = 4`, `T_2 = -2`.
- `T_1121222 = 38`, `T_1122212 = 20`.
- `T_112212 = -12`, `T_112122 = -23`.
- Direct commutator trace `6`, reversed-word trace `-6`, antisymmetric difference `12`.

Twenty further deterministic integer-matrix pairs, five each in sizes 2, 3, 4, and 5, agree between the recursive expansion, the printed polynomial, and direct adjoint-operator multiplication. Every reverse has the opposite value. The observed zero values in small matrix sizes are not used to infer minimal degree or any vanishing theorem.

The normal and optimized independent runs have identical output and pass 211 explicit guards. The guards include all file bindings, source identities, polynomial and direct-matrix identities, and the additional matrix checks. No `assert` statement supplies a required check.

Eleven adversarial changes are each rejected both normally and under `python -O`, for 22 independent mutation failures:

1. Wrong frozen proof hash.
2. Substitution of the retained DK v1 for v5.
3. Failure to reverse the right factors.
4. Omission of the adjoint minus sign.
5. Replacement of the color word by `1112222`.
6. Treating the seven-legged reversal as even.
7. Corruption of one integer-matrix entry.
8. Using anticommutators in the direct matrix calculation.
9. Changing the coefficient three to two.
10. Claiming the direct value is five.
11. Erasing antisymmetry by setting the reversed value equal to the original.

The author's checker also passes its baseline on temporary copies in both execution modes. All four supplied author mutants are rejected in both modes, giving eight further rejected mutation runs. This replay supplements the independent computation rather than replacing it.

These are arithmetic and identity checks. The universal geometric theorem, one-term survival, and rational integration are separate mathematical obligations audited above; no finite test suite establishes them.

## Source identity and inspection record

All five retained PDFs were fetched afresh from their public source URLs during this audit and compared byte for byte to the retained files. Every response was HTTP 200 and every comparison passed. Only retrieval metadata was newly saved; the fetched source bodies were not copied into an authored deliverable.

- Duzhin and Karev, *Detecting the orientation of long links by finite type invariants*, arXiv:math/0507015v5, 25 July 2005. [Versioned primary PDF](https://arxiv.org/pdf/math/0507015v5). 195,094 bytes; SHA256 `f92b93fe6cfe04f1720c8ee080f19af2103ced2ab4fcc616c7c95ed3df6dfae3`. Read the relevant text on pages 1--3, 5--9; visually inspected the retained renders of pages 1--3 and 8--9. Page 9 expressly supplies ordinary deframing.
- Bruno and Mecchia, *On quotient orbifolds of hyperbolic 3-manifolds of genus two*, Rend. Istit. Mat. Univ. Trieste 46 (2014), 271--299. [Journal primary PDF](https://rendiconti.dmi.units.it/volumi/46/014.pdf). 780,746 bytes; SHA256 `b4c1c4a76c3028a54ba1223536ec7b1c1820474e6584d622161bfba743c12f0c`. Read and visually inspected printed page 272 for centrality and handlebody extension.
- Hatcher, *Notes on Basic 3-Manifold Topology*. [Author primary PDF](https://pi.math.cornell.edu/~hatcher/3M/3Mfds.pdf). 702,282 bytes; SHA256 `c8add1a8633f36cb50de313f8f340a3f2b63b5548077d6e30f9c51a073398ff6`. Independently rendered and visually inspected printed pages 1 and 56, which are PDF pages 2 and 57, for the smooth conventions, Schoenflies, and Loop Theorem.
- Hatcher, *A proof of the Smale Conjecture, Diff(S3) equivalent O(4)*, Annals of Mathematics 117 (1983), 553--607. [Author primary PDF](https://pi.math.cornell.edu/~hatcher/Papers/SmaleConjecture.pdf). 14,720,341 bytes; SHA256 `d85554b61d9315081c51e8cf0438d5674c41507e2ac634dd465e029753333344`. Visually inspected PDF page 52, printed page 604, Appendix statement (1), because the extracted text's encoding is unreliable.
- Nogueira, *Knot complements with meridional essential surfaces of arbitrarily high genus*, Coimbra preprint 14--09. [Institutional primary PDF](https://www.mat.uc.pt/preprints/ps/p1409.pdf). 305,322 bytes; SHA256 `455b0187bbf9b8214022236ac7a949ecdc5e3a13f7e92aec802ed6d9f9f6d98b`. Checked Appendix 4's retained text for the full-group free-tangle/handlebody equivalence. The accepted predecessor source was left untouched.

The supplementary Haas--Susskind source has no independently retained PDF in this packet. It is unnecessary for acceptance because the sufficient Bruno--Mecchia statement and the explicit extension construction were checked directly. This audit does not invent a hash or claim fresh inspection of the unavailable PDF.

## Scope preservation and final disposition

The exact two-strand ordinary rational conclusion is accepted. The proof does not depend on a framing, a meridian-basis identification, pure-braid reduction, or a sublink-deletion freeness assertion. It does not resolve orders three through six, a minimum-order question, any corresponding higher-strand theorem, or a classification of all kernel elements.

The accepted order-at-most-two predecessor claims retain their existing status. All predecessor files listed in their proof and audit manifests were checked unchanged. This audit made no edits to the proof-search packet, no new proof-search turn, no queue or remote changes, no publication, no copied-source sharing, and no outreach.

The original audit status and supporting manifest bound this verdict to its frozen inputs and independent checks; those computational artifacts are not included here. The present edition has its own noncircular file manifest. Subsequent changes to the proof, geometric lemma, or dependencies require renewed review of the affected claims.
