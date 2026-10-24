# Literature disproof of the universal (2,2)-move conjecture

Row 1884; ID 10400211; AMR-103-0211. Disposition: already_solved; turns: 1. This means disproved by prior published work, not a newly proved result.

## Target and safe witness

The target is Ohtsuki's Conjecture 12.5, credited to Nakanishi and Harikae, printed page 533 / PDF page 161 of https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf. It asks for universal link reduction to a trivial link using (2,2)-moves. The neighboring algebraic-link special case and modified conjectures with extra moves are different statements.

Take the unoriented closure L of the three-strand braid (sigma_1 sigma_2)^6. This exact braid closure is the primary witness; no knot-table chirality identification is needed.

## Published theorem dependency and deduction

Dąbkowski–Przytycki, Unexpected connections between Burnside groups and knot theory, PNAS 101 (2004), 17357–17360, Theorem 2(i), excludes reduction of L to any unlink by rational p/q moves for prime p >= 5. Theorem 1.2 supplies rational-move invariance of B_L(p), the exponent-p quotient of the fundamental group of the double branched cover. Published source: https://pmc.ncbi.nlm.nih.gov/articles/PMC536021/ ; DOI: https://doi.org/10.1073/pnas.0406098101 . The corresponding preprint statements are Theorems 2.1(1) and 1.6 at https://arxiv.org/pdf/math/0309140 (inspected version v1).

Specialize to p=5. The author abstract https://arxiv.org/abs/0712.0985 identifies signed (2,2)-moves as rational signed 5/2-moves. Both signs belong to rational 5/q moves, since -5/2 = 5/(-2), with q any nonzero integer. Invariant preservation is symmetric under inverse replacements. Therefore a finite signed-(2,2) reduction of L to an unlink would contradict the published rational-move theorem. This refutes the universal conjecture, also under any narrower convention allowing fewer moves.

The case study https://arxiv.org/pdf/math/0501539 (inspected version v1), pages 2–3, corroborates the signed convention and disproof. Ordinary 5-move nonreducibility alone is insufficient: the case study only gives the direction that a 5-move is a composition of signed (2,2)-moves.

## Dependency and verification limits

The published proof sketch uses Sanov's associated-Lie-algebra theorem. That theorem and the published rational-move obstruction are explicit mathematical dependencies, not independently reconstructed here. No group orders, lower-central quotient values, braid-group presentation computation, or independently executed Burnside comparison are claimed. The GAP/Magnus/Magma calculations in the same article concern a separate exponent-four Whitehead-link argument and provide no computational certificate for this witness.

The acceptance is analytic/source-based. Package validation only checks bytes, inventory, and provenance. A passing validator is not an executable mathematical proof. No source PDFs, source text, dataset contents, private corpus records, or private coordination material are included. Public source inspection history is inherited from the acceptance, not newly claimed by this packaging step. No usable image inspection or local PDF hashes are claimed.
