# Immutable source-first baseline

Sealed UTC: 2026-10-03T13:40:40.241646+00:00
Completion estimate for assigned review: 12%.

## Access chronology
1. Received task-routing metadata and three primary-source URLs, expected lengths and SHA-256 values. No candidate narrative, program, generated output, status, history, prior review, or sibling mathematical conclusion was read.
2. Created this review folder and opened the three original PDFs through the web tool at 2026-10-03 13:38:12 UTC.
3. Independently downloaded original URLs, verified bytes/lengths/SHA-256 against routing metadata (SOURCE_ACQUISITION.json), and extracted text.
4. Read Wajnryb Chapter 8 section 3, printed pp.124–127 (PDF pp.130–133); Auroux’s Hurwitz convention near printed p.131; Baykur–Monden–Van Horn-Morris introduction/Theorem A and section 4.2 in both arXiv v2 and published version. Opened a rendered PDF image of the exact Wajnryb question on PDF p.132 to resolve the squared a1 typography.
5. Created this baseline before first access to any candidate mathematical material.

## Exact original claim, restated
Let G be the Artin group of type A5, hence B6, on a1,...,a5, with commuting relations for |i-j|>1 and ai aj ai = aj ai aj for |i-j|=1, quotiented by
    (a1 a2 a3 a4)^5 = a5 a4 a3 a2 a1^2 a2 a3 a4 a5.
Write A=a1 a2 a3 a4, h=a5 a4 a3 a2 a1^2 a2 a3 a4 a5, and C=A^10.
The question asks whether every positive literal word in these fixed generators representing C has length 40, 30, or 20 and is Hurwitz equivalent to the corresponding tuple A^10, (a1 a2 a3 a4 a5)^6, or h^2. The presentation, distinguished generators, positive-word domain, target element, and tuple-level Hurwitz operation are indispensable hypotheses.
Hurwitz moves preserve tuple length and product and replace adjacent (x,y) by (x y x^-1,x); the inverse operation is (x,y)->(y,y^-1 x y). Such moves can exit the literal generator alphabet. Equality in G and Hurwitz equivalence in G are distinct assertions.

## Independent success criteria and falsifiers
- Verify any claimed homomorphism on *all* Artin defining relations and the extra 20-to-10 relation, using explicit image conventions. A map failing any relation is not evidence about G.
- Derive abelianization and identify whether a length congruence is only necessary. Find a word satisfying all finite quotient tests but whose equality is undetermined to prevent promotion of filters to certificates.
- Separate fixed generator words from products of arbitrary positive conjugates. A mapping-class bound applies after a well-defined geometric map but cannot by itself classify Hurwitz orbits or lift equivalence from a quotient.
- Prove that all three displayed targets are equal in G if any claim uses their equality; show precisely which relation supplies it.
- Falsify rank generalizations at small rank, verify definitions at rank1, and distinguish Artin type A5 from alternating group Alt(5).
- Require complete finite enumerations and falsifying perturbations where computations claim completeness, with multiplication order checked independently.
- Classification success requires both all possible lengths and an actual Hurwitz classification in G. A strict upper bound and congruence establish at most the length menu unless lower cases and nontriviality are independently proved.

## Primary-source limits
The 2017 positive-factorizations Theorem A supplies L(boundary twist)=40 for genus2 nonseparating Dehn-twist factorizations. Its definition uses arbitrary nonseparating curves, not a fixed Artin alphabet. Theorem A does not state a three-orbit classification. The arXiv and published sources are treated as independently identified versions; corrections/version differences must be assessed before transferring a proof dependency. This baseline records only the sources’ statements and the original question; no candidate conclusion is endorsed.

Source files and acquisition timestamps are identified in receipts/SOURCE_ACQUISITION.json. Current-open status of the historical exact algebraic/Hurwitz question and novelty are not established by these sources alone.
