# Prior-proof dependency audit and unresolved calculation

This is a report on the published argument, not an independent full-proof PASS. The relevant main arguments and technical appendix were read. Classical background inputs remain credited rather than foundationally rederived.

## Dependency route

Chen–Möller Theorems1.1 and1.2 are proved in Sections6 and7. The genus3 invariant is developed via a canonical plane quartic and an associated cubic, with trivial versus nontrivial3-torsion on that cubic. Propositions6.3/6.4 control the auxiliary curve and the parity; Proposition6.5 constructs irreducible parameter spaces of the expected dimensions; Lemmas6.6/6.7 address exceptional loci. The associated local calculations appear in Appendix B.1.

For genus4, the canonical curve is a(3,3)-curve on a smooth quadric away from the hyperelliptic and Gieseker–Petri loci. The quadratic differential cuts out a(2,2) parity curve. Proposition7.4 relates h⁰(D) to trivial versus nontrivial3-torsion there, and Proposition7.5 constructs the two expected components. Lemmas7.6 and7.7 are used to discard exceptional loci. Lemma7.7 in turn invokes Appendix B.4 and B.5. This last branch is where the present audit stops short of verification.

The original target Q(12) is included in E₄ and therefore uses this genus4 route. The genus3 statements do not depend on B.5. Nevertheless this report does not certify the full four-stratum result by deleting the problematic fourth case.

## Exact displayed calculation in B.5

Published p.363, in the proof of Lemma B.5, works on F₂ with negative section e, fiber f, e²=−2, e·f=1, f²=0. These conventions are expressly given in Section5, p.327. It takes R of class2e+4f and X of class3e+6f, and displays

    0 → O(e+2f) → O(3e+6f) → O_R(3e+6f) → 0.

It then states that the space of X over a fixed(R,D) has dimension h⁰(F₂,e+2f)=2. Combining its base count8+n with that2 and subtracting dim Aut(F₂)=7 gives n+3, strictly less than the stratum's n+5. This supports the assertion that no entire component is contained in the Gieseker–Petri locus. The proof of Theorem7.1 explicitly uses Lemma7.7 to remove that locus before its component construction.

The PDF was rendered and visually checked: the number2 is in the published text, not an extraction artifact.

## Arithmetic check and convention check

For the negative-section convention, projection to P¹ gives

    pi_* O(ae+bf) = direct_sum_{i=0}^a O_P¹(b−2i),  a>=0.

In the case at issue this is O_P¹(2) direct_sum O_P¹, so

    h⁰(F₂,O(e+2f))=3+1=4.

The nearby paragraph does not specify a smaller subspace of this cohomology group. The displayed exact sequence concerns the full sheaf, and the automorphism quotient is subtracted separately afterward. Replacing only2 by4 in the stated count produces8+n+4−7=n+5. This no longer supplies the strict inequality being invoked. An additional restriction might restore the intended conclusion, but none has been proved in this report; the calculation must not be silently changed and presented as a complete repair.

There are further signs of a local notation/copying issue in the same paragraph: by adjunction the class2e+4f has arithmetic genus1, and for X of class3e+6f the bicanonical restriction has degree12 (class4f on X, since e is disjoint), whereas the printed paragraph describes a rational curve and uses6f. These observations reinforce the need for clarification; they are not asserted to disprove the main classification theorem.

## Impact and limits

The published theorem remains a precisely attributable result, and Chen–Yu's2026 survey explicitly uses it. That later attribution is evidence about literature status, not a replacement proof for the unresolved local calculation. This packet must therefore be labeled **credited theorem reporting with an unresolved verification issue**, not “fully independently verified prior proof.” No formal erratum or completed alternative proof was found in the focused primary-source search. No allegation about the authors and no claim that the theorem is false is made.

Inputs not independently recertified include general torsion specialization, period-coordinate smoothness, irreducibility of the indicated pointed elliptic covers, and the complete classical background for canonical/bicanonical degenerations. The finite checker verifies signature alignment, divisor arithmetic and the displayed section/dimension calculations only. It cannot establish constancy of h⁰ on the four strata or replace their component classification.
