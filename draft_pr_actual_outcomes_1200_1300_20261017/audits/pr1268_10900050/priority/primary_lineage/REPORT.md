# PR1268 / problem 10900050: independent primary-lineage priority audit

Initial independent report, 17 October 2026 UTC. This family did not read another current priority-family folder or root priority findings before its initial seal. Mathematical validity is an accepted input from MATH_GATE.json; this report addresses attribution and priority, with a checkable reconstruction of the old ingredients.

## Finding

The inspected primary lineage does not supply an explicit prior statement of the exact negative answer to printed Long Question 7.2, or a source explicitly giving the exact pair of clique numbers for Q(sqrt(10)). **Priority remains unestablished.** A bounded search cannot establish either firstness or present openness.

Two access gaps in the historical literature check have been materially closed. The full 42-page Lopez thesis was retrieved and its extracted text read, with relevant mathematical pages visually checked. The author's current publication list also led to a third, 14-page PDF containing the journal-layout Long–Thistlethwaite article. Relevant journal pages were read and visually checked. These are new audit evidence, not newly published mathematical results.

There is strong positive evidence that the principal ingredients are old. Lenstra's 1977 Proposition 2.2 already uses injection of a unit clique into residue classes of a proper ideal. Evan Dummit's 2021 course notes explicitly use P=(2,sqrt(10)) and exactly the obstruction to norms +2 and -2 modulo 5. The prime-element extension of the coloring argument follows from maximality of nonzero prime ideals. The separate CLASSICAL_IMPLICATION.md makes the composition explicit and distinguishes a present reconstruction from an established historical publication of that composition.

The suitable description is an elementary counterexample using classical arithmetic and residue classes. The present evidence does not justify describing it as a new theorem, a first solution, an independently discovered result with certified lineage, or the resolution of a currently open problem.

## Exact target and classification rules

The target is the equality question on PDF p. 6 of [arXiv:1512.04620v1](https://arxiv.org/pdf/1512.04620v1), with context on p. 5 and reference [19] on p. 7. Its setting is a totally real number field and its full ring of integers; it does not assume PID. The prime graph permits unit differences or elements generating prime ideals. The proposed equality involves the minimum over nonzero prime ideals. The accepted example has O=Z[sqrt(10)], both clique numbers 2, and minimum prime-ideal norm 2, hence strict inequality 2<4.

An explicit anticipation would state this example and clique conclusion, or another negative answer to the same universal equality with the same assumptions and graph convention. A stronger old theorem would count if its stated hypotheses and conclusion, together with separately identified arithmetic, actually imply the target. An isolated norm computation, unit-clique bound, prime-power graph result, irreducible-difference result, or PID-only equality statement does not by itself count as such an explicit anticipation.

## Primary lineage and version control

The [arXiv record](https://arxiv.org/abs/1512.04620) displays one submission, v1 on 15 December 2015. This is a verified record observation, not a claim that the question remains open. The original problem's reference points to the [16-page author manuscript](https://web.math.ucsb.edu/~long/pubpdf/LenstraHurwitz.pdf). The [separate 17-page manuscript](https://web.math.ucsb.edu/~long/pubpdf/LenstraHurwitz2.pdf) is a distinct file. Both were redownloaded, hashed, and read at the relevant definitions and Section 3.

The [author bibliography](https://web.math.ucsb.edu/~long/publications6.html), entry 83, supplies the journal citation and links [LongThistlethwaite.pdf](https://web.math.ucsb.edu/~long/pubpdf/LongThistlethwaite.pdf). This file carries JNT volume 162, pages 564–577, and DOI 10.1016/j.jnt.2015.11.002. Its first page records receipt on 15 January 2015, revision and acceptance on 5 November 2015, and online availability on 4 January 2016. The [publisher record](https://www.sciencedirect.com/science/article/pii/S0022314X15003686) was available through indexed metadata; direct GET remained 403. The usable journal full text came from the author's linked PDF.

The relevant convention is unchanged across these three PDFs. Theorem 3.1 is printed using a principal-ideal minimum, while the problem-list display uses a prime-ideal minimum. Those wordings are not silently identified here. No claim that Theorem 3.1 is false is needed or made. Source versions are separately fingerprinted; their observed internal PDF and HTTP dates do not certify first public availability or a complete revision history.

## Lopez thesis: actual full-text follow-up

[Daniel S. Lopez's institutional record](https://scholarworks.sjsu.edu/etd_theses/4974/) identifies the Fall 2018 MS thesis, DOI 10.31979/etd.3bc5-77v2. The [actual PDF link](https://scholarworks.sjsu.edu/cgi/viewcontent.cgi?article=8521&context=etd_theses) initially returned 403 to the web reader and a basic GET. Ordinary public browser navigation displayed a 42-page PDF. A normal browser User-Agent and institutional Referer then retrieved the complete PDF, 308970 bytes, SHA-256 8311f703974fdcf95b6bae4d938d78ac4b5ed5cfe928cfc386ac3f2721b3fd62. This was not an abstract-only inspection.

The extracted text of all pages was read. Visual checks covered PDF pp. 22, 29–31, and 35–39. Chapter 2 discusses unit and Lenstra–Hurwitz graphs. Definition 52, PDF p. 35, introduces graphs allowing principal ideals that are prime-ideal powers; the Lenstra–Hurwitz variant imposes additional prime-element and unit-surjectivity conditions. Theorem 55 gives upper bounds 8 or 4 for first prime graphs in real quadratic fields. Example 56 uses Q(sqrt(173)); the conclusion discusses extending prime-power results. The appendix's Sage code was read, not executed or certified.

The thesis is substantial adjacent work and merits citation. Its prime-power graphs must not be substituted for the target graph. Its upper bound 4 in the ramified case does not establish the exact value 2 in the target. No exact Q(sqrt(10)) counterexample or Question 7.2 conclusion was identified in its full extracted text. That observation cannot establish the absence of other prior work or undocumented knowledge.

## Old mechanism and citation follow-up

[Lenstra's primary 1977 paper](https://pub.math.leidenuniv.nl/~lenstrahw/PUBLICATIONS/1977b/art.pdf), pp. 238 and 242–243 (PDF pp. 2, 6–7), defines the unit-difference clique quantity and proves its bound by the smallest proper ideal quotient. The proof is exactly the residue-class injection mechanism for unit edges. Its prime-element extension requires a further algebraic step, supplied explicitly in CLASSICAL_IMPLICATION.md; the source is not represented as already stating that extension.

[Dummit's 2021 v1.90 notes](https://dummit.cos.northeastern.edu/teaching_sp21_4527/numthy_9_geometry_of_numbers_v1.90.pdf), PDF pp. 13–14, contain the exact nonprincipal norm-two ideal and the modulo-five norm obstruction. The [2022 v2.00 notes](https://dummit.cos.northeastern.edu/teaching_fa22_4527/numthy_9_geometry_of_numbers_v2.00.pdf) retain this calculation. Dates and authorship are printed in the documents, while PDF metadata supports their version descriptions. These are primary author teaching notes documenting old arithmetic, not an identified graph-priority publication. The 2021 document postdates the 2015 question, so it is not used to prove that this particular source was available when the question was asked.

[Lorenzini's author-hosted Torsion and exceptional units version](https://dinolorenzini.franklinresearch.uga.edu/sites/default/files/Lorenzini2024August1.pdf), p. 31 and reference [37] on p. 38, cites Long–Thistlethwaite concerning a sextic unit-clique size 18. This is a real citation trail but an adjacent result, not a negative answer to the target at the inspected locus. Other portions were not read. Search-only ResearchGate, MaRDI, and Math.StackExchange leads are not promoted to primary mathematical authority.

## Reproducibility and limits

QUERY_LEDGER.json records 36 fresh literal queries executed in nine four-query web-search calls, their UTC timestamps, provider, filters, aggregate result scopes, and raw-capture hashes. The nine historical queries from the submitted literature check are not counted again. The provider combines results across each call, so this audit does not invent per-query hit counts or claim that every exact phrase was honored by the engine. Broader queries returned substantial irrelevant Hurwitz-space, Paley-graph, and topology material. Only the specified primary sources were promoted to evidence.

SOURCE_LEDGER.json records actual URLs, retrieval dates, bytes, hashes, access failures, read pages, visual pages, and unread scopes. All source PDFs, HTML, text extractions, rendered pages, browser notes, and raw query captures are confined to ignored_local. The manifest enumerates authored audit outputs only; external input paths appear solely as receipts.

No individual was contacted, no outreach was prepared, and no Git, branch, index, PR, publication, or external-service mutation was performed. Historical firstness, exhaustive citation coverage, inaccessible/private/unindexed work, and the exact origin of the candidate's discovery are outside what these artifacts establish. These limits remain even though the two historical source-access gaps were closed.

## Recommended publication wording

“We give an elementary counterexample to the equality as printed in Long's Question 7.2, under the prime-element convention of Long and Thistlethwaite. The argument uses the classical nonprincipal ideal (2,sqrt(10)) and a residue-class coloring argument. We make no claim of novelty or priority.”

Credit Lenstra for the unit-clique/residue argument, Long–Thistlethwaite for the graph framework and source inequality, Lopez for the subsequent prime-power extension, and a standard arithmetic source such as Dummit's notes for the exact ideal calculation. Do not collapse the principal-ideal/prime-ideal wording distinction, and do not convert this bounded audit into a firstness, novelty, present-openness, journal-acceptance, or independent-discovery certificate.

Initial seal awaits root reverse cross-review. The sealed initial report is not to be overwritten by later review.
