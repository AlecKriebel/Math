# Acceptance: the universal (2,2)-move conjecture was disproved

**Verdict:** ACCEPT as `already_solved`, specifically **disproved in prior literature**, for row 1884, ID 10400211 / AMR-103-0211. This is a literature-based mathematical acceptance, not a new counterexample or an independently reconstructed proof of the cited theorem.

## Target

Ohtsuki's Conjecture 12.5 concerns reduction of every link to some trivial link by (2,2)-moves. It is on printed page 533, PDF page 161, and credited there to Nakanishi and Harikae. The nearby algebraic-link statement is a special case, not the universal assertion. [Original problem collection](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf)

## Exact witness and theorem dependency

Use the unoriented link L obtained by closing the three-strand braid (sigma_1 sigma_2)^6. Dąbkowski–Przytycki's Theorem 2(i) in *Unexpected connections between Burnside groups and knot theory*, PNAS 101 (2004), 17357–17360, rules out its reduction to any unlink by rational p/q moves for prime p >= 5. Its exponent-five specialization therefore supplies the needed obstruction. Theorem 1.2 supplies rational-move invariance of B_L(5), the exponent-five quotient of the fundamental group of the double branched cover. The published proof sketch invokes Sanov's associated-Lie-algebra theorem. The explicit GAP/Magnus/Magma calculations elsewhere in that article concern the separate exponent-four Whitehead-link argument; they must not be attributed to this witness. [Published article](https://pmc.ncbi.nlm.nih.gov/articles/PMC536021/), [DOI](https://doi.org/10.1073/pnas.0406098101)

The preprint independently makes the braid word legible: Theorem 2.1(1), page 5; invariance is Theorem 1.6 on that page. It states the rational-move question with arbitrary nonzero integer denominator q. Its proof remains a sketch, not a complete explicit exponent-five group comparison. [Preprint, retrieved version v1](https://arxiv.org/pdf/math/0309140)

## Convention bridge and logical deduction

The authors explicitly identify signed (2,2)-moves with rational signed 5/2-moves. [Dąbkowski–Ishiwata–Przytycki, abstract](https://arxiv.org/abs/0712.0985)

Thus both signs lie in the rational 5/q family: -5/2 = 5/(-2). A proposed finite signed-(2,2) reduction would be a prohibited rational-move reduction. Inverse replacements cause no problem: preservation of an isomorphism invariant is symmetric. No link orientation is needed. Reflection exchanges the two signs and preserves unlinks, so the signed equivalence relation also takes a counterexample to its mirror counterexample. If the original diagram is interpreted as allowing fewer moves, impossibility for the larger signed family still suffices.

The 2005 case-study preprint explicitly defines equivalence using both signs (page 2), identifies 9_49 as a counterexample there, and states that the mirror of 9_49 is equivalent to the above braid closure (page 3). The safe primary witness remains the exact braid closure, avoiding knot-table chirality ambiguity. Ordinary 5-move nonreducibility alone is insufficient: that paper explains that a 5-move is a composition of the signed (2,2)-moves, not the converse. [Case study, retrieved version v1](https://arxiv.org/pdf/math/0501539)

## Verification boundary

This review independently checked the cited source text, theorem numbering, sign quantifiers, and logical implication. It did not reproduce Sanov's theorem, derive a complete braid-group presentation, compute lower-central quotients, run a group-algebra package, or verify every diagrammatic equivalence to 9_49. No group orders or independently calculated invariant values are asserted. PDF screenshots were requested, but no usable image inspection is claimed. No local source-file hashes are claimed. The source theorem is an explicit dependency, not an unexplained computational certificate. No publication or queue edits were made.
