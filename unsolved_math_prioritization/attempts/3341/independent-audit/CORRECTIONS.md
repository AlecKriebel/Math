# Corrections and source clarifications

The frozen release is unchanged. These recommendations do not change the unsolved 5/5 classification or invalidate its partial mathematical results.

## C1: actual binary-block separation (small factual correction)

Location: PARTIAL_RESULTS.md, “Binary coding detail.”

Replace:

> Payload bits are isolated, blocks have zero margins, and no other 3×3 ring exists.

With:

> Payload bits are isolated. The zero strips between neighboring blocks separate their nonzero regions, and no other 3×3 ring exists.

Reason: the ring occupies rows and columns 1,2,3, so it touches each block's top and left edges. Those edges are not zero margins. The existing coordinate layout, decoder, and marker proof need no change.

## C2: spell out Gardy's exact-format convention (recommended source precision)

Location: PARTIAL_RESULTS.md, §1, after the distinction between exact w=P(h) and B(C,d); and/or SOURCE_STATUS.md, source 2.

Suggested addition:

> The original OPG question states linear/polynomial relatedness informally. Gardy's slide 22 explicitly gives exact-format language conditions w=c h and w=P(h), with one fixed c or P for the language. Those are separate from the uniform upper-bound domains B(C,d) used here. Slide 23 states a folding/unfolding equivalence in the linear setting; this write-up does not invoke that claim as a proved transfer theorem.

Reason: the release is already cautious and does not make the invalid transfer, but saying only that “the source” leaves the distinction unspecified can obscure Gardy's explicit definitions. Squares are not a subdomain of every fixed exact format w=c h with c>1.

## C3: connect successor signatures (optional proof-explication)

Location: PARTIAL_RESULTS.md, §4.2, at the recognizability citation.

Suggested addition:

> The cited preprint uses cyclic successors with boundary predicates. For the direction used here, replace H(x,y) by succ_h(x)=y ∧ ¬Right(x), and similarly for V. This turns any EMSO sentence in our nonwrapping adjacency signature into an EMSO sentence in that source's signature, with the same set prefix. Its recognizability theorem therefore supplies the needed tiling presentation; no converse FO definition of wraparound is required.

Reason: the source's stronger signature does not break the argument, but explicitly giving the needed one-way translation closes an avoidable presentation gap.

## No requested mathematical or status changes

Do not upgrade to solved, change the five-turn exhaustion, assert a PH equivalence, claim novelty for the square separation, or advertise bounded controls as an unbounded proof. The authoring lookup's historical access failures need not be erased merely because the www OPG route became readable during this audit.
