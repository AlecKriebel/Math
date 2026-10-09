# Independent audit of the order two free exterior kernel

**Theoretical-edition note.** This is the complete authored mathematical audit, with only the provenance/privacy and unavailable-artifact edits documented in PROVENANCE.md. Its computational passages describe historical supplementary checks. The scripts, fixtures, outputs, and logs are not included, and preparation of this edition did not rerun them. This is an AI mathematical audit, not human peer review or formal proof-assistant verification. Original authored-artifact hashes below identify the pre-edition documents, not any edited public copies.

**Disposition: ACCEPTED in the exact scope stated below.**

The supplied second approach proves

\[
N_2(k)=0\qquad\text{for every integer }k\geq2,
\]

where the invariants are rational, ordinary unframed Vassiliev invariants of order at most two on smooth ordered upward-oriented string links with fixed matching endpoints, and the vanishing set consists of **all actual three-dimensional exteriors with abstract group \(F_k\)**. No specified meridian basis is required. Consequently \(N_n(k)=0\) also holds for \(k\geq2\) and \(0\leq n\leq2\).

This is a source-dependent mathematical acceptance with independent exact algebra. It is not a machine certification of the tangle embeddings or of the cited geometric theorems. It does not settle any \(k\geq2,n\geq3\) case, assert an all-degree vanishing result, or claim novelty. The familiar one-strand exception remains separate. The first accepted approach and its audit are unchanged.

## 1 Audited version and frozen inputs

The final audited `PROOF_KERNEL_ORDER_TWO.md` (before the documented edition-only redactions) has 18,400 bytes and SHA256

`01185b1eafcce7b6a1ef55ebf5bc5f4a4bed784b82f75b1e232aa5a30a09a58f`.

The initial intake had SHA256 `580b97c7bb20290333f0a3ec0b1e8093720fbb69cf8f3d4b4921f63c4ae4309c`. The author then froze the final version, which makes the convention \(\Phi_{AB}=\Phi_A\circ\Phi_B\) explicit and adds the immediate lower-order inclusion corollary. Both changes were read and checked. The mathematical witnesses and coefficient argument did not change.

The original supporting packet had 36 records, all independently matched to the actual files. Its private artifact inventory and identity are not reproduced. The six primary source catalogue records and all 13 rational-source/inspection records also match. The rational witness lemma has SHA256 `c5bf2c4c4799af29dc9d3d74ee12c30a36467a2710eb14056fdc37eae30356b0` and was read in full.

All 24 files named by the first accepted approach's manifest remain byte-identical. In particular its report is still SHA256 `1ffa1273c4d09427d7ff85164a214ddd2c20090ae36ad71a7a9f876c5a8e0d4a`, and its accepted audit is still SHA256 `0d2e7b88e82f0553d9309c3a59483a6d1bc3453b360be7e92e0af99d6ad3aa70`. Identity checks establish the reviewed version; they are not evidence of mathematical truth by themselves.

## 2 The complete invariant space

[Meilhan, *On Vassiliev invariants of order two for string links*, arXiv:math/0402036v2](https://arxiv.org/pdf/math/0402036v2), Definitions 1.1–1.3 and Theorem 2.4, was independently read. The full printed page 5 formula was also rendered and visually inspected. It includes component Conway coefficients, the plat-minus-components invariant, pairwise linking numbers, squares, all three products for each three-label set, all three disjoint-pair products for each four-label set, and one distinct-index triple Milnor invariant per ordered increasing triple. This is exactly the spanning family in the report. Its category is smooth, fixed-endpoint, ordered and upward-oriented; the source explicitly imposes the ordinary 1T relation.

Thus writing the linking contribution as an arbitrary polynomial \(Q\) of total degree at most two loses no coordinate. Every product of two pairwise-linking variables is either a square, a product on three labels, or a product on four labels. The proof needs spanning, not an unproved uniqueness assumption. Rational coefficients are important for the later determinant and polynomial arguments.

Meilhan's plat joins the two bottom endpoints and the two top endpoints; its orientation follows the first strand and traverses the second in reverse. This agrees with the report's \(w_{ij}\). Individual orientation reversal does not change the Conway coefficient used here. No framed self-linking coordinate, link-homotopy quotient, or height-monotonicity requirement is inserted.

## 3 Pure braid tests and triple isolation

### Actual free exteriors and zero component and plat values

The complement of a geometric braid is trivialized by a height-dependent disk isotopy. Its exterior has the actual fundamental group of a disk with \(k\) punctures, namely \(F_k\). This is also stated in [Bar-Natan, *Vassiliev homotopy string link invariants*, section 4.1](https://www.math.toronto.edu/drorbn/papers/homotopy/homotopy.pdf). Only this forward implication is used; an arbitrary free tangle is not assumed to be a braid.

Deleting all but one strand leaves an unknotted long arc. Deleting all but two leaves a two-strand pure braid. A two-strand braid with its top and bottom endpoints joined in pairs is a one-bridge plat, hence an unknot; equivalently, its successive twists can be moved into a cap and removed. Therefore all \(a_i\) and \(w_{ij}\) vanish on every pure braid, including braids with nonzero pairwise linking.

### The exact commutator and longitude normalization

For \(\beta=[\sigma_1^2,\sigma_2^2]\), each two-strand deletion is the identity: in each deletion at least one of the two full twists becomes trivial, and the other cancels its inverse. This is a geometric braid-deletion statement, not merely a claim that its linking number is zero.

Under the report's explicitly fixed Artin action and composition order, independent free-word substitution reproduces the three displayed normalized conjugators. If two words conjugate \(x_j\) to the same free-group element, they differ on the right by a power of \(x_j\), since the centralizer of a free generator is its cyclic subgroup. Setting that generator's exponent sum to zero therefore gives the preferred zero-self-linking representative. The resulting degree-two Magnus terms are

\[
[X_2,X_3],\qquad -[X_1,X_3],\qquad [X_1,X_2],
\]

respectively, with no degree-one terms. All full words and signs in the submitted display pass independent reproduction.

Bar-Natan section 5.2 identifies the relevant conjugating element with a strand parallel and its Magnus coefficients with the nonrepeating Milnor coefficients. The source uses the opposite conjugation direction and an exponential Magnus convention, both explicitly distinguished in the submitted report. The audit uses the standard integral expansion \(x_i\mapsto1+X_i\). Inversion can reverse the selected coefficient's sign, but cannot erase its magnitude one. With every pairwise linking number zero, the lower-linking changes between order and basing conventions vanish. This is sufficient to detect the coefficient of the Meilhan triple invariant.

### Nonadjacent labels and basing

A supporting subdisk containing exactly any chosen three endpoints exists even when other marked points lie between them in a planar drawing: take a thin disk neighborhood of an embedded tree joining the selected points while avoiding the remaining finite set. The disk need not be convex. Performing the three-strand commutator inside this disk and fixing its complement gives a legitimate pure \(k\)-braid.

The leading longitude term is independent of the auxiliary paths used to compare local and ambient meridians. Each conjugated meridian has Magnus expansion \(1+X_i+O(2)\), so substitution into a word whose first nonconstant term has degree two preserves that term. Conjugating the longitude preserves it as well. More fully, a change of top and bottom whiskers may introduce a term of the form \(\Phi(q)q^{-1}\). Here \(c_j\in\Gamma_2 F_k\), so \(\Phi(x_j)=x_j\pmod{\Gamma_3 F_k}\), hence \(\Phi(q)q^{-1}\in\Gamma_3 F_k\). This extra term is also invisible in degree two. The text's basing conclusion is therefore valid even with this fuller change-of-path formula.

Every triple other than the chosen one contains at most two active strands. Deleting the missing active strand trivializes the local commutator by an isotopy within the supporting disk, relative to its boundary. The inactive strands lie outside it and remain stationary. Thus the whole retained triple is trivial. Milnor invariants are natural under deletion, which algebraically sets deleted variables to zero. All unwanted distinct-index triple values vanish. This establishes an isolating test for every triple, not only for consecutive labels.

### Linking polynomials

For each pair of labels, a full twist in a disk neighborhood of an arc joining that pair has linking vector equal to the corresponding standard basis vector, up to an overall sign chosen by twist direction. Its other pair deletions have zero linking. Products of these pure braids realize the entire integer lattice because linking numbers add. This multiplication takes place only among braids whose exteriors have already been certified free.

After testing the identity and the isolating commutators, the constant and triple terms are eliminated. The remaining linking polynomial vanishes on the full integer lattice and is therefore zero over \(\mathbb Q\), by the one-variable root theorem iterated over the variables. The proof does not assume that triple invariants vanish on arbitrary-linking braid products; their coefficients have already been eliminated before those evaluations.

## 4 The two free two-string witnesses

### Rational tangle with its specified cap system

The complete diagram and adjoining assertion on page 30, Figure 20, of [Kauffman–Lambropoulou, *From Tangle Fractions to DNA*](https://homepages.math.uic.edu/~kauffman/Dresden.pdf) were independently inspected. The specified tangle is \([1]+1/[2]\), of fraction \(3/2\), and its numerator closure is a trefoil. The source's numerator and elementary tangle conventions, the definition of rationality, and Theorem 6 on connectivity were checked on pages 6–9 and 39–41 of [*On the Classification of Rational Knots*, arXiv:math/0212011v2](https://arxiv.org/pdf/math/0212011v2). The relevant full page images, not only extracted text, were opened.

The diagram's endpoint trace gives NW–SW and NE–SE. This also agrees with odd/even fraction parity. Therefore assigning its southwest and southeast endpoints to the bottom, and its northwest and northeast endpoints to the matching top positions, yields two through strings. It does not impose height monotonicity.

The proof correctly marks **both numerator cap arcs**, in addition to the endpoints. Two disjoint sphere arcs have disjoint disk neighborhoods; the desired orientation-preserving identifications of those neighborhoods extend over the complementary annulus and then over the ball. Straightening endpoint collars can be performed without changing the cap system. Thus the prescribed numerator becomes the standard top-and-bottom plat. An arbitrary four-endpoint re-marking would not justify that conclusion, but the report does not use one.

The separate homeomorphism witnessing rationality identifies the actual tangle exterior with the exterior of two simultaneous boundary-parallel arcs, a genus-two handlebody. It need not preserve the chosen plat caps. Individually, each arc remains boundary-parallel under that homeomorphism. After forgetting the other arc, boundary closing paths with the same two endpoints are isotopic on the sphere; there are no other punctures to retain. The component closures are therefore unknots. These two different marking arguments are compatible and establish

\[
(a_1,a_2,w)(R)=(0,0,1).
\]

The trefoil has Conway coefficient one for either chirality. No linking value is needed. The construction uses a finite smooth endpoint-twist diagram; it introduces neither wild arcs nor a framing variable.

### Nogueira's two component types and the exchange operation

The entire appendix text and complete Figures 9–10 of [Nogueira's Coimbra preprint 14–09](https://www.mat.uc.pt/preprints/ps/p1409.pdf), printed pages 14–15, were independently examined. The source explicitly identifies the capped first strand as a trefoil, the capped second strand as \(T(3,-4)\), and the displayed tunnel construction's exterior as a handlebody. The figure artwork and over/under interruptions are present. The second identification is an additional input beyond the first accepted approach and has been checked as such; it is not inferred from the first-strand result.

This audit accepts that geometric identification as a cited primary construction. It does not claim an independently machine-recognized knot type from a marked crossing list. The PL-to-smooth and endpoint-marking conversion in the frozen first geometric lemma applies to both individually capped strands: smooth in disjoint small neighborhoods and collars, and forget the other strand before comparing sphere caps. These operations preserve the exterior and both capped knot types. A two-string handlebody exterior has genus two and hence actual group \(F_2\).

[Willerton, *On the first two Vassiliev invariants*, arXiv:math/0104061v1](https://arxiv.org/pdf/math/0104061v1), page 1, identifies \(v_2\) with the Conway \(z^2\) coefficient. Its page 5 torus formula was read and visually inspected. It gives

\[
c(T(3,-4))=\frac{(3^2-1)((-4)^2-1)}{24}=5.
\]

Independently, the normalized Alexander polynomial reconstructs the Conway polynomial \(1+5z^2+5z^4+z^6\). Mirror image and orientation reversal do not alter its even coefficient. The witness values are therefore \((a_1,a_2)=(1,5)\).

An orientation-preserving disk diffeomorphism supported away from its boundary can interchange the two basepoints. Its product with the interval transports the strands to the exchanged endpoint positions; relabeling the transported strands gives a **new** ordered string link with values \((5,1)\), retaining the free exterior. This construction does not quotient out label exchange. Its linking and plat values can safely remain unknown because their coefficients are eliminated first.

## 5 Split inclusions and every required plat value

For an arbitrary pair \(\{i,j\}\), the separating base-disk arc in the report exists: a thin regular neighborhood of a tree connecting those two points to one small boundary interval cuts out a disk containing just that pair. The complementary region is also a disk. Product collars permit insertion of either two-string witness on one side and all remaining vertical strands on the other.

The separator \(\delta\times I\) is a properly embedded disk disjoint from the strings and their chosen regular neighborhoods. The two exterior pieces intersect in a disk after harmless thickening. Seifert–van Kampen yields exactly

\[
\pi_1 E(J_{ij}(S))\cong\pi_1 E(S)*F_{k-2}.
\]

Thus each inserted witness is in \(\mathcal F_k\). For \(k=2\), the other factor is trivial. This is a proof for this particular boundary-connected-sum construction; it does not assume free exteriors survive arbitrary stacking or deletion.

All coordinates used subsequently have been accounted for:

1. The two active component closures retain their knot types. Every inactive component is an unknot.
2. For the active pair, the product subdisk identification preserves the witness's top and bottom caps. After deleting the other strands, arcs joining the two endpoints in each endpoint disk are isotopic to the standard caps. Hence its original \(w\)-value is preserved.
3. For a mixed pair, the separator keeps the retained arcs on opposite sides. The top and bottom caps can be chosen to cross the separator once each; no forgotten punctures constrain these choices. Completing the disk through the outside closure ball produces a sphere meeting the plat knot in exactly two points. The two resulting summands are the individual capped knots, possibly with one orientation reversed. Conway multiplicativity under connected sum implies additivity of the \(z^2\) coefficient, so the plat coefficient is the sum of the two component coefficients. Thus every mixed \(w\) is zero, even when the active component is knotted.
4. Two inactive strands form the trivial two-string link, whose component and plat coefficients all vanish.

These conclusions apply to every pair of labels, adjacent or not. In evaluating sublink invariants, component deletion is used only to compute closures, never to assert freeness of the deleted-component exterior.

## 6 Elimination and quantifiers

For \(v\in N_2(k)\), the pure-braid tests leave only

\[
v=\sum_i b_i a_i+\sum_{i<j}e_{ij}w_{ij}.
\]

For every pair \(i<j\), the free example \(J_{ij}(R)\) has no component coefficient and exactly one nonzero plat-difference coordinate, equal to one. It forces \(e_{ij}=0\). Evaluating the remaining component sum on the two orderings of Nogueira's example gives

\[
b_i+5b_j=0,\qquad 5b_i+b_j=0.
\]

Their determinant is \(-24\), so both coefficients vanish over \(\mathbb Q\). The pairs \((1,j)\), \(2\leq j\leq k\), cover every component whenever \(k\geq2\). There is no untested component, pair, or triple coordinate. This finishes the universal argument.

At \(k=2\), independent symbolic calculation of the six-row matrix with all five unspecified linking/plat entries gives determinant \(-48\). In the more general symbolic matrix, replacing the rational plat value by \(w\) and the second Nogueira coefficient by \(q\) gives \(2w(1-q^2)\). This explains exactly why the two geometric inputs suffice and why their linking values do not matter.

The universal proof does not derive its all-\(k\) conclusion from a finite range of computer tests. Its all-\(k\) ingredients are the arbitrary-label constructions, the integer-lattice polynomial argument, and the covering family of pairs. Computation checks finite instances and the stated algebraic identities.

## 7 The one strand boundary and higher orders

The report correctly excludes \(k=1\). To check that boundary against a primary source, this audit independently retrieved [Papakyriakopoulos, *On Dehn's Lemma and the Asphericity of Knots*, PNAS 43 (1957), 169–172](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/papa.pdf). Theorem 3(i), printed page 170 / PDF page 3, explicitly states the free-cyclic-group characterization of the unknot; the complete page was visually inspected.

Closing a single proper arc by a trivial arc in the complementary ball preserves its fundamental group. In van Kampen, the new trivial-arc exterior is a solid torus and its intersection annulus maps isomorphically on fundamental groups into that solid torus. Thus a free rank-one arc exterior gives a closed knot with cyclic group. The cited theorem makes it an unknot, so its Conway coefficient vanishes. The trefoil coefficient is one and is an ordinary order-two invariant. This confirms the familiar nonzero one-strand example. It is background, not an extension of the multi-strand elimination.

For each fixed \(k\geq2\), the inclusions \(V_n(k)\subseteq V_2(k)\) for \(0\leq n\leq2\) justify the stated lower-order corollary. There is no corresponding deduction for \(n\geq3\). In particular, neither the finite basis used here nor the first approach's filtered Milnor lemma may be silently promoted to an all-order statement. The nontriviality question in that higher-order range remains open within this work.

## 8 Independent computation and mutation controls

The submitted scripts were read and replayed in an isolated temporary directory, with original predecessor trees exposed read-only by symlinks. No frozen output was rewritten. Both normal Python and `python -O` reproduced the author's braid and kernel-result JSON byte for byte. Each of the four supplied negative controls failed with nonzero status under `python -O`.

The audit also contains an independently written algebra checker, rather than accepting the author's recorded PASS strings. It calculates full Artin images first and extracts conjugators by cyclic word peeling; this differs from the author's conjugator-tracking implementation. It checks the displayed words, truncated Magnus coefficients using two arithmetic methods, two independent deletion implementations, all 35 selected triples on three through six strands, degree-two basing invariance including the whisker term, symbolic determinant, all linking monomial evaluations through eight strands, component elimination through twelve strands, and the torus Alexander/Conway identity.

Both normal Python and `python -O` pass **825 exact algebra guards**, with equivalent results. Ten independent mutations are rejected at their intended guard in both modes, giving **20 successful rejection runs**: wrong frozen report hash, erased commutator, reversed commutator, bad inverse-Artin letter, bad displayed conjugator, wrong Magnus sign, erased rational plat value, collapsed component-coefficient gap, omitted four-distinct-label linking product, and wrong torus coefficient. The runner checks the actual expected error, not merely a nonzero process status. The original full results and logs are not included in this theoretical edition. The separate authored algebra audit is retained as AUDIT_ORDER_TWO_ALGEBRA.md.

The separate source checker has **167 optimization-safe guards**, checking byte counts and hashes for the frozen version, manifests, their listed source/inspection files, and the supplemental classical source. Normal and optimized runs produce identical output. Independently mutating the Nogueira digest or the rational PDF's expected byte count is rejected with nonzero exit status under `python -O`. None of these tests relies on Python `assert`.

These tests detect relevant algebraic and identity corruptions. They cannot detect a false geometric theorem in a cited source, prove a cap isotopy from raw pixels, or replace the all-\(k\) mathematical argument. Those obligations were reviewed separately above.

## 9 Source fingerprints and handling boundary

The six primary PDF fingerprints match the author's catalogue exactly:

- Meilhan 2004 v2: 315,045 bytes; SHA256 `8b88fa5ea5df29a3b4a16934e5ade6bab37269462ace0d43bd15bff265f9a3b7`.
- Bar-Natan author edition dated 17 February 2015: 182,750 bytes; SHA256 `56a3ecaae2d3196f008b5c52316cbe7c39cfd85a1ad8c8f1c60101b54d347cad`.
- Nogueira Coimbra 14–09: 305,322 bytes; SHA256 `455b0187bbf9b8214022236ac7a949ecdc5e3a13f7e92aec802ed6d9f9f6d98b`.
- Willerton 2001 v1: 402,625 bytes; SHA256 `7a86e5bdfdc024ff9938eb5e294b807cdb85efe40088d132c1372d4f136f29f7`.
- Kauffman–Lambropoulou Dresden author copy: 1,388,506 bytes; SHA256 `53cd49ea0448fe796c3baa07e2246f89d16352398293cb0e2b1d9019dbfa5fd1`.
- Kauffman–Lambropoulou classification v2: 459,279 bytes; SHA256 `de77c7cf69cd5464ed7b9044dc4842004c23c5c2820f334c30b5ecbd8cf4fc10`.

The supplemental Papakyriakopoulos PDF has 233,503 bytes and SHA256 `7bdcfa9f01c8f628d8dcff0c1e103b23ba3c656e979993bf76b2f1d3e35fe323`. Its five pages include a JSTOR cover and the four-page PNAS note. It was retrieved by HTTPS from the verified Edinburgh-hosted copy after the original university URL redirected to `webhomes.maths.ed.ac.uk`. A different repository presented a CAPTCHA and was not used. The retrieval record distinguishes this university-hosted scan from a publisher download.

The Willerton publisher request in the supplied packet produced HTML, not a PDF. The report properly relies on the pinned arXiv PDF and makes no publisher-byte claim. Complete PDFs, extracted source text, and source-page images remain private supporting evidence. This authored audit and its public citation/hash metadata do not authorize redistributing those bodies.

No first-approach edits, new substantive proof-search approach, publication, queue change, remote change, or outreach was performed in this audit.

**Final acceptance:** the second approach validly proves \(N_2(k)=0\) for every \(k\geq2\) in the stated ordinary rational category. Its scope includes \(n\leq2\) by inclusion and excludes the unresolved higher-order range.
