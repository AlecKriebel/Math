# Source, scope, and prior-work verification

Checked 2026-10-04 UTC. Catalogue identity: **2306088 / AMR-022-6088**, queue rank 589, Hayman–Lingham Function Theory **Problem 6.88**.

## Exact source and scope

- The requested [catalogue URL](https://www.unsolvedmath.com/problems/2306088) was opened first. The web tool could not access it; direct retrieval returned HTTP 403. No authentication or anti-bot bypass was attempted.
- The exact statement and update were checked in [Hayman–Lingham, arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), printed p. 148, PDF leaf 149. The page was visually inspected. The catalogue's 2018 update reports no progress; it is superseded by the resolving literature below.
- The main question asks for the largest constant c in the finite-area sharpening of the second-coefficient inequality. It also states existence of an analogous positive constant c1 for boundary length. It does **not** explicitly ask for the best perimeter constant.
- The pinned dataset record and its entire prior AI report were read. The prior report contains no proof, says only that nothing was located, and calls the residual the two sharp constants. That last description is stronger than the source. We retain the actual source's area-optimality and perimeter-existence scope, while disclosing that sharp perimeter optimality is not proved.
- The exact record is from dataset `ulamai/UnsolvedMath`, immutable revision `37e53eabe540fb458758e198be61634bd02ee008`. Source-file hashes agree with the repository manifest; the corpus and prior AI report are not distributed in this packet.

## Resolving primary literature

1. **Aharonov, Shapiro and Solynin (1999)**, *A minimal area problem in conformal mapping*, J. Analyse Math. 78, 157–176. [DOI](https://doi.org/10.1007/BF02791132).
   - The publisher metadata and abstract explicitly identify a resolution of the normalized-univalent prescribed-second-coefficient area problem.
   - The publisher's HTML abstract displays denominator 7. This is numerically incompatible with the explicit attaining map. It is not used for the constant.
   - The complete 1999 proof was not obtained. The subscription page was not bypassed, and no purchase, login, account creation, or contact with any person occurred.
2. **The same authors (2006)**, *Minimal area problems for functions with integral representation*, J. Analyse Math. 98, 83–111. [DOI](https://doi.org/10.1007/BF02790271); [public author-posted text](https://www.academia.edu/31230874/Minimal_area_problems_for_functions_with_integral_representation).
   - Read the introduction's attribution and Section 4, pp. 105–109: representation (4.2), Lemma 8, Theorem 3 and (4.10)–(4.21), Lemma 9, and Theorem 4.
   - Theorem 3, p. 106, explicitly contains the factor 27π/8, the small-coefficient branch, and the inverse-Koebe extremal. Theorem 4, p. 109, transfers this exact result to the full univalent class and credits the 1999 paper.
   - This was read as public author-posted OCR, not independently authenticated page images. The constant, normalization and boundary cases were checked analytically against the explicit maps and against the project's earlier independently audited proof.
   - The 2006 proof imports its coefficient comparison lemma from 1999. That unavailable original proof is not represented as read. The earlier project proof supplies a separately audited ordinary-conformal-radius reconstruction of the needed non-strict comparison.
   - Read p. 109's separate discussion of minimal perimeter problems. It is not silently treated as solved here. Existence in Problem 6.88 follows directly from area plus isoperimetry.
3. **Aharonov and Shapiro (1974)**, *A minimal-area problem in conformal mapping (Abstract)*, Canterbury 1973 proceedings, pp. 1–5. [DOI](https://doi.org/10.1017/CBO9780511662263.002); [publisher preview](https://api.pageplace.de/preview/DT0400.9780511891809_A23680318/preview-9780511891809_A23680318.pdf).
   - Read the five-page announcement, especially Theorem 5 and its denominator 8.
   - The original announcement assumes unproved topological conditions and is historical corroboration, **not** the resolving theorem.
4. **Chuaqui, Efraimidis and Hernández (2025)**, *On Hardy spaces, univalent functions and the second coefficient*, [arXiv:2510.05395v1](https://arxiv.org/abs/2510.05395v1).
   - Checked the introduction and reference to the 1999 paper as part of the current-literature search. This paper concerns prescribed-coefficient Hardy estimates; it is not the resolving source for the sharp area constant.

## Related work and duplicate control

- The live `main` reference read during this attempt was `6a112842592930803e459f013484062787ce7772`.
- Live QUEUE.md blob `c1009ab2e12b93cffb15cb17c0ac893979ce5a44` shows row 589 as `queued`, `0/5` before this packet. No queue or repository file was changed remotely.
- Search of pull requests for numeric ID 2306088 and exact problem code found no existing PR for this item. The main attempts-directory read showed no directory for 2306088. The static related-target groups file has no group containing this ID.
- A stronger related target, **2306017 / Problem 6.17**, already has a published project verification in [PR 503](https://github.com/AlecKriebel/Math/pull/503), at checked head `54f5bfe3cde5da6778bbd20e373fc433a7ed45fe`.
- The prior proof, source gate, original non-passing audit, and repaired passing audit were all read. The first audit's biangle-source discrepancy remains an explicitly preserved historical defect. The repaired proof uses ordinary conformal radius and a negative slit, and does not claim an independent full-class equality classification.
- This packet is a corollary and catalogue-status correction using that same published mathematical result. It is not another independent discovery, and has discovery count **0**.

## Publication boundaries

Only authored proof notes, provenance metadata, logs, and reproducible controls belong to the proposed publication. Complete scholarly PDFs, source OCR/HTML, dataset corpus, private retrieval records, and internal coordination are excluded. The current packet is frozen for a fresh independent review; it does not claim that review has happened.
