# Primary-source literature ledger

Audit date: 14 September 2026. This ledger records the sources actually used, what was inspected, and the limits of the conclusions. It is not a claim that all possible literature has been exhaustively searched.

## Exact problem and current version

**Kourovka Notebook**, 21st edition, update posted 1 September 2026.

- Website: https://kourovkanotebookorg.wordpress.com/
- Primary PDF: https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/21tkt.pdf
- Current arXiv mirror surfaced in search: https://arxiv.org/html/1401.0300v46

The website identifies the September update as current. Problem 16.63 on printed p. 102 asks the exact odd-order, nontrivial finite p-group equality question and attributes it to D. MacHale. It explicitly cross-refers to Archive 12.77. The problem page and archive p. 255 were inspected as PDF page images, as was the cover.

Archive 12.77 asks whether the order of a finite noncyclic p-group of order greater than p^2 divides its full automorphism-group order. Its printed answer is negative, citing González-Sánchez–Jaikin-Zapirain (2015). This is a DIFFERENT question. The adjacent Archive 12.78(a) records a negative result at order p^6; its underlying original proof is not a dependency of this construction.

## Existing small-automorphism construction

**Jon González-Sánchez and Andrei Jaikin-Zapirain**, “Finite p-groups with small automorphism group,” Forum of Mathematics, Sigma 3 (2015), e7.

- https://arxiv.org/abs/1406.5772
- https://arxiv.org/html/1406.5772v2

Read Theorem 1, its hypotheses, and the construction discussion. For each prime p the authors construct a family with `|Aut(G_i)| = O(|G_i|^(40/41))`, hence examples with fewer automorphisms than elements. This does not give exact equality, nor does the theorem assert that the full automorphism groups in the family have p-power order. It motivates a Lie-algebra approach, not the desired conclusion by itself. The archived divisibility result is credited to these authors.

## Restricted equality theorems

**M. Shabani-Attar**, “On Equality of Order of a Finite p-Group and Order of Its Automorphism Group,” Bulletin of the Malaysian Mathematical Sciences Society 38 (2015), 461–466.

- DOI: https://doi.org/10.1007/s40840-014-0030-z
- Accepted manuscript: https://math.usm.my/bulletin/pdf/acceptedpapers/2012-10-027-R1.pdf

The actual theorem statements and proofs were inspected, including page images. The relevant restrictions are:

- Proposition 2.2: an odd-prime equality example must be purely nonabelian.
- Proposition 2.5: the maximal-class equality possibilities are 2-groups.
- Theorem 2.6: equality with a cyclic Frattini subgroup gives only the specified 2-groups.
- Theorem 2.8: **class two AND cyclic centre**, together with equality, forces p=2.

The final theorem does NOT exclude all odd-prime groups with cyclic centre, or all class-two groups without its other hypothesis. No restricted theorem is used as a universal nonexistence proof.

## Lie-algebra template, with finite-characteristic reproof

**Bakhrom Omirov and Jie Ruan**, “On Lie Algebras with Only Inner Derivations,” arXiv:2605.04602v1, 6 May 2026.

- https://arxiv.org/abs/2605.04602
- https://arxiv.org/html/2605.04602v1

Read Theorem 4.8 and the preceding module constructions. With six radical summands of highest weights `(6,4,6,2,4,0)`, the theorem gives a 31-dimensional perfect Lie algebra with nontrivial centre and only inner derivations. The arXiv record inspected listed version 1.

This report credits that template, supplies raw transvectants with every coefficient fixed, and independently verifies integer Jacobi. Its proofs of H1 vanishing, the FULL automorphism group over F_1009, the one-dimensional centre, and the derivation dimension do not assume automatic reduction of a characteristic-zero statement. The asymmetric lattice, rigid flag and exact finite full-automorphism count are the new steps of this construction.

## Lazard: actual hypotheses and preservation of FULL automorphisms

**Serena Cicalò, Willem A. de Graaf and Michael Vaughan-Lee**, “An effective version of the Lazard correspondence,” Journal of Algebra 352 (2012), 430–450.

- DOI: https://doi.org/10.1016/j.jalgebra.2011.11.031
- Primary author-hosted PDF: https://iris.unitn.it/retrieve/e3835192-3015-72ef-e053-3705fe0ad821/lazard.pdf

Read the finite-ring discussion on pp. 433–434 and inspected both pages as images. The relevant condition is nilpotency class `c < p`, for finite p-groups and finite p-Lie rings. The operations define each other, and the authors explicitly explain preservation of the automorphism group. An exponent-p assumption is not required. This construction has `c <= 846 < 1009`, so it is within that range. The software's range of precomputed BCH coefficients is not a restriction of the theorem.

Original attribution: **Michel Lazard**, “Sur les groupes nilpotents et les anneaux de Lie,” Annales scientifiques de l'École Normale Supérieure (3) 71 (1954), 101–190.

- Metadata inspected: https://www.numdam.org/item/?id=ASENS_1954_3_71_2_101_0

The full original French paper was not downloaded; the specific finite hypotheses used here were checked in the Cicalò–de Graaf–Vaughan-Lee primary paper. The report does not pretend otherwise.

## Novelty search and rejected false positives

Searches included exact combinations of “16.63”, “MacHale”, “automorphism”, “same order”, “equality”, and 2026, plus the article titles above. The current notebook still presents 16.63 as a question. No published resolution of the exact equality question was located.

A surfaced SciNet entry dated 10 July 2026 is a reposted OPEN problem, not a resolution:
https://api.scinet.pub/p/d9791e15-22b8-42c3-bf53-22d2c932390a
Its claimed equivalence between “not equal” and “strictly greater” is false and is not relied on. The abelian inversion argument and the known small-automorphism examples already show why it cannot be used as a universal formulation.

Results about central, IA or class-preserving automorphisms were not substituted for results about the full automorphism group. Search absence alone is not a proof of bibliographic priority. The present report is new, unpublished work with exact verification, not a claim of external acceptance.
