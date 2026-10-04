# Source and status audit

Checked 2026-10-04 UTC. This is a bounded literature check, not proof that no solution exists.

## Target provenance

- Requested catalogue: https://www.unsolvedmath.com/problems/3341 . The web reader could not access it; a direct HTTP read returned 403.
- Original question: https://www.openproblemgarden.org/op/mso_alternation_hierarchy_over_pictures . The maintained mirror's direct problem route failed in this session. The original node is readable at https://openproblemgarden.org/comment/reply/37448 . The readable page attributes the question to Étienne Grandjean and dates its posting May 18, 2012. No newer solution was displayed there.
- The imported pinned numeric record is 3341, code OPG-37448, title “MSO alternation hierarchy over pictures.” Its background preserves the question, discussion and a dated 2026-08-17 triage. That generated triage is background evidence, not a proof certificate. There is no matching OPG-37448 key in the pinned separate research-results map; no exact-title match was found in that map.

The question asks for strictness under polynomial or linear balance. Its discussion distinguishes the unrestricted-grid result from the balanced problem, records non-complement-closure of EMSO on squares, and mentions a possible Boolean-EMSO collapse. None of those statements is a full resolution. The uniform balance and exact-shape conventions are kept separate in PARTIAL_RESULTS.md.

## Primary mathematical sources

1. O. Matz, N. Schweikardt, W. Thomas, *The Monadic Quantifier Alternation Hierarchy over Grids and Graphs*, Information and Computation 179(2), 356–383 (2002), DOI https://doi.org/10.1006/inco.2002.2955 . Publisher record: https://www.sciencedirect.com/science/article/pii/S089054010292955X . The publisher abstract was available in search; direct article opening failed. The abstract establishes unrestricted-grid/graph strictness and identifies iterated-exponential format witnesses. The complete paper was not downloaded or reverified here. Our superpolynomial-intersection proposition is independently proved and does not depend on a guessed indexing of that construction.

2. P. Gardy, *MSO hierarchy on picture language and the need for a notion of balance*, primary slides, https://lsv.ens-paris-saclay.fr/~gardy/Talk/balancedMSOpicturelangages.pdf . The web tool exposed the complete text, but direct download returned 403 and screenshot rendering failed. Its printed slides 8, 10–15, and 21–23 discuss complexity encodings, tiling recognition, mirror non-complement-closure, and balance. No date was verified; search crawl/publication estimates are not used as the talk's date. Its mirror example informs the known-result attribution; our square reflection formula and counting argument are supplied in full. Its folding remark is context only, not an invoked unproved equivalence in our argument.

3. É. Grandjean, F. Olive, G. Richard, *Descriptive complexity for pictures languages (extended abstract)*, arXiv:1201.5853v1 (January 27, 2012), https://arxiv.org/abs/1201.5853 and https://arxiv.org/pdf/1201.5853 . The PDF was downloaded privately and locally text-extracted. Theorem 2.5 credits Giammarresi–Restivo–Seibert–Thomas for EMSO=recognizable picture languages; Theorem 2.6 generalizes the characterization. This is the one substantive external theorem used by the square tiling proof. Sections on coordinate representation and cellular automata are not mistaken for a balanced pixel-MSO alternation resolution. The preprint's generalized hierarchy discussion is not a substitute for the exact OPG question.

4. É. Grandjean and F. Olive, *Descriptive complexity for pictures languages*, CSL 2012, https://doi.org/10.4230/LIPIcs.CSL.2012.274 . Official publication record verified. A longer author-hosted version dated April 27, 2012 is available at https://pageperso.lis-lab.fr/~frederic.olive/Materiel/Publis/GrandjeanO12.pdf ; its text was readable in the web tool. It explicitly distinguishes pixel and coordinate representations and presents the recognizability characterization. This related source is not evidence of a later solution of the balanced hierarchy question.

The original recognizability theorem is D. Giammarresi, A. Restivo, S. Seibert, W. Thomas, *Monadic second-order logic over rectangular pictures and recognizability by tiling systems*, Information and Computation 125(1), 32–45 (1996). We verified its statement through Source 3, not by claiming to have independently checked its original full proof.

## Current search and repository duplicate gate

Exact-title and balanced/square MSO hierarchy searches, including recent-year terms, found no verified complete resolution. The accessible OPG text remains old, so this negative finding has the usual indexing and coverage limits.

Read-only repository checks used AlecKriebel/Math main commit 25aaa7146e257ef5276e80aae60429cf3f4765f9. The queue row was rank 599, queued, 0/5. No selected state entry or attempts/3341 directory existed. All-state PR searches for 3341 and for MSO/pictures returned no matches. No selected ID occurs in the checked related-target groups. Two recursive-tree calls failed with a transport error, so the repository check is not advertised as a complete full-tree search. The repository root listing and the full attempts listing were nevertheless read successfully.

## Provenance hashes and redistribution limits

Pinned source corpus SHA-256 values:

- problems.json: 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf
- research_results.json: 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b

Only the original mathematical write-up, source notes, controls, and results are included in the proposed publication package. Downloaded source PDFs, full corpus bytes, repository snapshots and private coordination are excluded.

## Result classification

- Full resolution: no.
- Verified already-solved status: no.
- Strongest unconditional result in this attempt: reconstructed first-level square separation and explicit route barriers.
- Conditional result: PH strictness would imply balanced MSO strictness, via a detailed tableau reduction.
- Proposed visible status/turns: unsolved, 5/5.
- Findings-field changes: not requested or authorized by this package.
