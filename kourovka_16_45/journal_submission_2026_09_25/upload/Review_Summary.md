# Review of the Kourovka 16.45 submission

Prepared 25 September 2026, San Francisco.
Target: Bulletin of the Australian Mathematical Society.

## Mathematical conclusion

The audited claim is the explicit counterexample

`G = F_29^2 ⋊ <[[0,28],[1,0]], [[2,7],[12,28]]>`

with `|G| = 100920` and `b_f(G) = b(G) = 3 < 4 = mu′(G)`.
The maximum `b` includes all permutation representations, with bases taken
for the permutation image. The proof makes no smallest-order claim.

No substantive mathematical defect was found. The main manuscript contains
the complete structural argument; computations corroborate its explicit
finite inputs and witnesses. Novelty was checked by a bounded primary-source
search, which found no earlier resolution. That search is not an exhaustive
certification of historical priority.

The final pre-submission check found the author's own version 1.0.1 in the
official Kourovka Notebook online repository, labelled as a solution of
Problem 16.45. Its PDF matches the Zenodo preprint. The manuscript now records
this hosting and avoids relying on the printed notebook's lack of a solution
comment as a description of current online status. Repository hosting is not
external journal peer review or proof certification. No proof change was
needed for this contextual correction.

## Independent review paths

| Review | Evidence and result |
|---|---|
| Structural | Re-derived the subgroup/base correspondences, restrictions, complement invariants, line bounds, Sylow splitting, all action kernels, normal subgroups and explicit witnesses. No gap found. |
| Exact computation | A new implementation reconstructed the mathematical specification before reading supplied code. It agreed with supplied Python/C++ implementations on all 76 actual complement subgroups. All 100920 affine elements agreed across the two Python reconstructions. |
| Exhaustive small checks | Tested 1215450 four-families and 67525 triples; no irredundant four-family or faithful minimal triple exists in the complement. Also checked all 62 subgroups of the scalar line group and the characteristic-11 boundary example. |
| Primary literature | Confirmed the September 2026 Notebook statement/update, Cameron 2014 and 2024 conventions, and recent related literature. No earlier equivalent counterexample found in the documented searches. |
| Fresh final referee | Reviewed the compressed journal manuscript before earlier audit verdicts, independently re-derived the full proof and recomputed the displayed witnesses. No proof revision requested. |

These were independent AI-agent work paths within the project, not external
human peer review or full proof-assistant formalization. All mathematical
arithmetic in the verification programs is exact.

## Changes made for submission

- Reorganized the paper around its explicit theorem and the normality obstruction.
- Preserved all essential proof steps while moving verification details and the characteristic-11 example into a three-page reproduction note.
- Simplified the complement lower bound using the pulled-back natural action of A5.
- Distinguished recent faithful-only notation from the all-actions invariant.
- Corrected the earlier review's section reference to Cameron 2024 Section 6 and retained only cited references.
- Added MSC2020, confirmed author details, accurate funding/conflict statements, detailed AI disclosure and an immutable reproduction link.
- Used the Bulletin's official unchanged class, with seven-page main manuscript, three-page reproduction note, and no invented publication DOI or received date.

## Journal decision

Archiv der Mathematik's live author agreement prohibits articles largely
written by AI. It is therefore not the target for this manuscript as prepared.
The Bulletin's journal-specific instructions expressly address disclosed
AI-generated text. The substantive assistance remains disclosed, and human
author approval and accountability are required. The ordinary Green Open
Access route is listed as having no publication charge.

## Author responsibilities before upload

Read and approve the final paper, own its mathematical claims, and confirm
the paper is not under consideration elsewhere. Verify the disclosure against
your records, adding any reliably known historical tool/model build details.
Those identifiers were not consistently recorded and have not been invented.
Enter any additional postal information directly in the portal. No submission,
external communication, account acceptance or publishing agreement has been
made on your behalf.

Detailed reports and reproducible checks are preserved in the project. The
package is prepared for author review and journal submission; it does not
guarantee an editor will send it for review or accept it.
