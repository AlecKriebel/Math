# Source gate: row 1880, 30001558 / OWR-4425-014

Disposition: ELIGIBLE ONLY FOR THE FRAGILE SUBPROBLEM. No matching completed draft was found. Do not spend a new proof campaign on robustness or describe the combined entry as wholly unsolved. No proof attempt or queue edit is made here.

## Original source and exact target

The source is Jeffrey Shallit's contribution to *Mini-Workshop: Combinatorics on Words*, Oberwolfach Reports 7 (2010), printed pp. 2232–2233, Problems 39 and 40. Workshop year 2010 and publication year 2011 are different dates, not different reports. DOI: https://doi.org/10.4171/OWR/2010/37 . Primary PDF: https://ems.press/content/serial-article-files/46296 .

Problem 39 asks for an infinite ternary squarefree word such that every nontrivial finite change creates a square. In ternary words, a change means replacement by either other symbol, not a specified cyclic flip. The author suggests a Thue–Morse gap construction with its first symbol removed but does not prove it.

Problem 40 is answered in the same report: Pascal Ochem gives a Brinkhuis substitution construction permitting aligned block alternatives, and James Currie independently supplies a solution. This is credited prior work, not a new result.

## Later primary literature and quantifier guard

Benjamin Przybocki, *Lengths of Irreducible and Delicate Words*, https://arxiv.org/abs/2108.06646v3 , subsequently published as EJC 29(3) (2022), P3.7, https://doi.org/10.37236/10669 , distinguishes single-letter delicacy from arbitrary finite changes. Theorem 1.3 of the preprint classifies finite delicate ternary squarefree lengths as 5 and every length at least 7. Section 3's block construction also yields an infinite single-letter-delicate word, but this does not establish arbitrary finite-change fragility. Section 5, Question 21 of the published version, asks about finite k-delicate words for all k. The adjacent known all-k infinite result concerns binary overlap-freeness, not ternary squarefreeness.

Consequently none of those results settles the remaining target. Search on 2026-10-21 found no later primary resolution; that bounded negative search is not proof of global current openness.

## Exact mathematical handoff

Seek w in {0,1,2}^N that is squarefree and has the following property: every squarefree v in {0,1,2}^N with v_n=w_n for all sufficiently large n must equal w. Equivalently its finite-change equivalence class contains no other squarefree word. All replacements at finitely many chosen coordinates must be covered, including coordinated changes that remove squares created by individual changes. A singleton-change theorem is insufficient. Any candidate built from binary gaps must control index shifts after a change in gap sum; binary finite-flip fragility alone is not a valid immediate transfer.

## Duplicate and provenance checks

The full local problems corpus contains one exact-ID record; research_results has no OWR-4425-014 key. GitHub PR searches across all states for exact ID, source key, fragile, squarefree, and square-free found no matching target draft. Broad searches returned unrelated number-theoretic uses. These checks do not guarantee absence of unindexed unpublished work.

Fresh corpus and PDF byte hashes, source identities, and inspection limits are in the two metadata files. Copied dataset record, PDFs, and extracted source text are retained privately and are excluded from any public packet. No publication, commit, branch mutation, or QUEUE change occurred.
