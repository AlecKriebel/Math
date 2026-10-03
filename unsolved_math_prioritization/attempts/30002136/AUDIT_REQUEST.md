# Independent audit request: 30002136

Audit this frozen five-turn WIP packet as a partial-result/unsolved report. Do not extend the mathematical search or create a sixth author turn. No full-target solution or novelty claim is submitted.

The original problem asks for fixed nonconjugate u,v∈F2 with equal traces for every rho:F2→SL3(C), or a proof of impossibility. Check that every note and status keeps this exact quantifier and field. Original source: Kapovich, Question0.1, OWR35/2012 p2195, https://ems.press/content/serial-article-files/46404 . Check current-source credit, including Lawton–Louder–McReynolds §§4.2–4.3 and the 2025 Aougab et al. status statement linked in README.

Main audit targets:
- The universal trace→inverse trace→characteristic-polynomial argument uses contragredient representations, not inversion as an antihomomorphism. The source's separate wording is retained, with equivalence proved specifically for the universal SL3 setting.
- The low-occurrence theorem quantifies over arbitrary companions in allF2. Abelianization alone is insufficient. Scrutinize LOW_MINORITY_PROOF.md §2: the unique maximal Laurent term, all nonzero C^p entries for p≠0, cyclic reduction, pure-power cases, and recovery of all four signed counts.
- Turn2 zero/repeated/negative gap exponents; three-cycle common shifts; four-gap directed-deck classification; all assertions of density and GL3 scalar extension.
- Turn3 generic determinant/adjugate coefficient formula and separation of swapped nonzero gaps, including opposite exponents.
- Turn4 the complete length5 equality-pattern classification; whether b11^2 b12 b23 b31 really has only five index paths; the exceptional-word cyclic rewrite; the signs in Cayley–Hamilton and the alternant; nonvanishing on the relevant invertible dense set. Distinguish a deck collision from full trace equivalence.
- Turn5 canonical format with one negative b, p,r≠0 and q allowed0; both adjugate coefficients; extraction of q independently of the other powers; unordered-to-ordered reconstruction; all repeated/negative edge cases.
- The automorphic formulation must be justified by composition of representations and preservation of conjugacy. Do not assume all words enter the excluded families.

Reproduce all five checkers from independent commands and compare saved outputs. Review the arguments, not just PASS labels. The checkers are finite exact sanity tests; the proof of arbitrary exponent parameters is in the notes. Current files bind to FINAL_MANIFEST.json; earlier turn manifests belong to their historical commits for files that later changed.

Return an explicit scope-qualified verdict, corrections or counterexamples, strongest supported theorem, exact remaining gap, and whether exhausted/unsolved5/5 is accurately represented. Any result PR requires a fresh independent audit; this packet itself is only WIP.
