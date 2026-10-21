# Ohtsuki Problem 12.6: five-route existence-proof audit

Private working audit, 2026-10-21. No publication, repository changes, or queue edits. No new universal invariant is constructed here. This audit identifies exact dependencies and a conditional residual criterion, not a solution or a claim of novelty.

## Target and conventions

The source is Ohtsuki, Problems on invariants of knots and 3-manifolds, §12.4, pp.533–534, Problem 12.6. The target is a new proof of existence of a universal Vassiliev knot invariant using KTG presentations and operations. The preceding paragraph already knows an extension of the Kontsevich invariant and reconstruction from generator values. Therefore reconstruction from previously known values does not, by itself, answer the request.

The source permits nonorientable ribbon neighborhoods and half-integer framing, with tetrahedron and positive/negative half-twisted Möbius generators. Its operations are connected sum, unzip, bubbling, and unknot creation. By contrast, Bar-Natan–Dancso defines oriented edges with cyclically oriented trivalent vertices and oriented thickenings; its original operation package is orientation reversal, edge deletion, unzip, and connected sum. Its dotted repair replaces this package with orientation reversal, tree connected sum, and adjacent dot/anti-dot cancellation. These are not literally identical theories.

A half-framing cannot simply be called an ordinary integer framing after renormalization. An orientation double cover is not a proof of equivalence: it changes the skeleton, and descent and the Möbius generator still require a construction. Restricting to the orientable subcategory may suffice for the knot conclusion only if a complete construction of every required knot and all presentation changes is proved there. That restricted result is different from an extension to every original object.

## Route 1: strict homomorphic expansion on ordinary KTGs

Attempt: choose generator values, assign ordinary induced chord-diagram operations, and demand strict commutation.

This route encounters a published degree-two obstruction. In Bar-Natan–Dancso, Theorem 3.1 and Appendix Lemmas 6.2–6.4/Corollaries 6.5–6.6, connected sum of two trivial unknots followed by unzip forces the unknot value v to obey v²=v. Since an expansion has v=1+positive degrees, it is invertible, hence v=1. The dumbbell value is consequently 1. Tetrahedron and crossing values produce an associator, whose crossing normalization has linear term t12/2. Its degree-two constraints force a nonzero degree-two value after orientation reversal and an unzip turning the tetrahedron into the dumbbell, a contradiction.

Importantly, the appendix argument explicitly relies on orientation reversal, unzip, and connected sum; omission of edge deletion alone is not a demonstrated escape. We have verified the source's logical chain, not independently reimplemented its omitted degree-two diagram calculation. This is a literature barrier, not a newly proved impossibility theorem. It does not refute the broad original request, which does not require this exact strict target operation package. Any transfer to the original half-framed theory needs an exact restriction/operation dictionary first.

## Route 2: dotted KTGs and anomaly absorption

Attempt: add dots and anti-dots, correct by powers of the unknot value, and use the resulting homomorphic expansion as the existence proof.

Bar-Natan–Dancso Theorem 3.3 defines its new expansion from Z_old by inserting nu^(1/2) at each dot and nu^(-1/2) at each anti-dot. The formula is meaningful in the completed rational/characteristic-zero algebra because nu has constant term 1. Adjacent inverse factors cancel, and the tree connected-sum correction compensates for the known unzip anomaly.

The proof of universality explicitly uses that Z_old is already an expansion. Thus this repairs homomorphicity but does not establish the existence premise independently. It would be logically circular to define nu as the value of an as-yet-unconstructed invariant and use Theorem 3.3 as the construction of that invariant. It is not circular to use a previously independently constructed Z_old; that merely produces an existing dependent proof. To obtain a new proof, one must independently specify dot factors and tetrahedron values, verify the relations, and verify the symbol map. No such independent specification was found in this attempt.

## Route 3: elementary configuration integrals and renormalization

Attempt: start from the naive KTG integral and prove convergence, invariance, and universality by local corrections rather than importing an associator.

Dancso 2010 supplies substantial published progress on exactly this analytic route. Sections 4–6 regularize vertex divergence and repair isotopy defects through counterterms and syzygies. Proposition 6.7 yields a universal invariant commuting with orientation switch, edge delete, and connected sum. Section 6.5 then changes the target unzip, rather than proving strict commutation with the unmodified induced map. This distinction reconciles the introduction's broad commuting language with the later no-go theorem.

The route does not require explicitly assuming an associator. Calling it logically circular merely because it uses Kontsevich integrals would be incorrect: a direct construction can be an independent proof of existence without assuming the result to be proved. However, reproducing this 2010 construction is not new mathematics, and its dependency on the knot-integral framework plus its framing/operation conventions requires an exact audit before identifying it with the presentation-driven request. Bar-Natan–Dancso Remark 4.3 explains that its associator produced from this input is implicitly derived from KZ and normalization. We therefore certify an existing analytic construction, not a newly independent presentation-based solution.

## Route 4: associator/tetrahedron generator assignments

Attempt: choose a normalized solution (Phi,R), with R starting 1+t12/2, transport it to tetrahedron and twist values, and descend along the KTG relations.

This is a legitimate conditional route. It is not a new proof merely to set Phi=Z_old(tetrahedron), prove Phi obeys associator identities, and feed Phi back to construct Z_old. Bar-Natan–Dancso Theorem 4.2 and Remark 4.3 explicitly expose this dependency: starting from the Murakami–Ohtsuki construction already imports an associator, while starting from Dancso imports the implicit KZ input.

An independently proved associator existence theorem could break that logical cycle, but then the source and depth of that theorem must be acknowledged. In addition, pentagon and hexagon cannot silently substitute for the entire original presentation: one must state and verify symmetry, normalization, framing/half-twist, bubbling, and unknot relations, as applicable to the selected presentation. A Möbius assignment has to obey the relevant orientation/framing compatibility, not merely a formal square-root equation. We have not supplied this full dictionary or verification. Thus this route remains conditional, rather than a proof that the original problem is either solved or impossible.

## Route 5: degree-by-degree relation lifting

Attempt: replace an imported invariant by solving the presentation relations recursively in the completed diagram spaces.

Here is a precise residual lemma, valid for a specified finite many-sorted presentation with degree-compatible filtered polynomial operations in separated, complete diagram spaces. Each multilinear operation is required to send inputs of degrees i_1,...,i_k to degree at least i_1+...+i_k. Let a tuple x satisfy all relations modulo F^(n+1). Choose arbitrary lifts to the next quotient, and let e be the relation defects in degree n+1. Let L be the linearization mapping degree-(n+1) corrections to degree-(n+1) changes of those defects. Then corrected lifts exist exactly when -e belongs to im L.

Proof: write each lifted generator as x_i+h_i, with h_i of degree n+1. Expand every polynomial relation. Terms with two corrections have degree at least 2n+2 and vanish modulo F^(n+2), for n>=0. The remaining expression is exactly e+Lh. This proves both directions. For operations involving inverses of constant-one series, the same statement follows by expansion of the inverse in the complete filtered algebra. With a compatible sequence of successful lifts, completeness gives a full relation-satisfying assignment; continuity makes all relation defects zero in the limit.

Syzygies can imply M e=0 with ML=0. This proves only that the error is a cycle. It does not imply it is removable unless its class in ker M/im L vanishes. Neither finite generation nor finite presentation proves that vanishing. Nor do solutions through a fixed degree, or even unrelated solutions at every finite degree, automatically supply the necessary compatible inverse-limit sequence. In the ordinary strict package Route 1 shows the process cannot succeed with the prescribed universality normalization. In a repaired/original package the actual complexes and all-degree vanishing or explicit compatible lift algorithm are still missing here.

This formal lemma is elementary obstruction theory, not a novel theorem about KTGs. It isolates what an independent proof would have to establish instead of hiding it behind 'solve the finite relations'.

## Universality and descent: two separate obligations

Relation satisfaction gives an invariant only after proving that the stated relations generate all equivalences between admissible presentations. It does not by itself prove universality. An identically trivial positive-degree assignment illustrates this logical gap whenever it respects the chosen operations: relation-respecting maps need not have the required derivative normalization.

A sharper circularity check comes from Bar-Natan–Dancso §2, printed p.5: chord diagrams modulo 4T/VI map surjectively to the associated graded, but the proof that there are no further relations uses an existing universal invariant. Equality of two topological filtrations does not establish injectivity of this diagram map. Write q:D_n→gr_n V for that surjection. A genuinely new construction must establish gr_n(E)∘q=id on D_n by direct singular evaluation; this then proves q is injective, rather than presupposing it. In particular, replacing the target diagram algebra by the abstract associated graded and choosing a vector-space splitting does not establish the full diagram-valued universality theorem.

For an actual construction, one must show that an n-singular knot is evaluated as its degree-n chord diagram plus higher degrees. A standard local sufficient mechanism is to present each crossing in compatible local KTG expressions, prove that the over-minus-under expression begins with the single corresponding chord, and show that all surrounding operations preserve filtration and induce the expected symbol operation. Multilinearity then expands the n-fold crossing difference into the product/composition of n degree-one differences, yielding the desired leading chord diagram. One still must prove that the chosen presentation handles arbitrary singular knots without introducing lower-degree terms or changing the local symbol. The 2013 appendix's spanning-tree construction is relevant existing work, but using its graph-generation result requires checking the chosen operation package.

## Outcome and dependency ledger

- Strict ordinary operations: published no-go applies; no new no-go theorem claimed.
- Dotted repair: valid existing construction, explicitly dependent on an existing expansion.
- Elementary integral construction: valid existing analytic route, not an independently new construction in this audit.
- Associator-to-generators: conditional until independent input and complete operation/framing dictionary are supplied.
- Recursive lifting: exact obstruction condition identified; no all-degree KTG vanishing or compatible lift construction proved.

No complete independent proof was obtained. No primary statement inspected certifies that the literal original Problem 12.6 is fully settled. Conversely, this audit does not establish that it remains open in all interpretations. Appropriate status is literature-sensitive partial progress / exact-formulation unresolved, with no new full-closure claim.

## Primary sources

- Ohtsuki (ed.), 2002, §12.4, pp.533–534: https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf
- Dancso, 2010, introduction, Proposition 6.7, §§6.5–6.6: https://msp.org/agt/2010/10-3/agt-v10-n3-p04-p.pdf
- Bar-Natan–Dancso, 2013, §§2–4 and Appendix: https://www.math.toronto.edu/drorbn/papers/ktgs/ktgs.pdf
- Additional historical context independently checked: Bar-Natan–Thurston, Algebraic Structures on Knotted Objects and Universal Finite Type Invariants, 2001, §§1.2–1.3, describes the generators/relations/syzygies lifting program and its relation-error obstruction spaces. https://www.math.toronto.edu/drorbn/papers/AlgebraicStructures/LongAlgebraicStructures.html

## Independent adversarial review

A separate reviewer independently checked the primary text and agreed with the operation/framing mismatch, the narrow scope of the no-go theorem, and the explicit old-expansion dependency. It additionally identified the associated-graded circularity above, which was then checked directly against §2, p.5. The reviewer also noted that BND does not pursue finite presentation (p.6 footnote), so its finite-generation result must not be cited as a complete presentation certificate. No objection was resolved by claiming closure.
