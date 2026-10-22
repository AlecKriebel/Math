# Sources, status, and provenance

Checked 2026-10-04 UTC. The exact universal problem has not been resolved in this investigation. A bounded search found no complete later resolution; this is not a proof of literature-wide absence.

## Exact statement

The requested catalogue URL, https://www.unsolvedmath.com/problems/30000203 , returned HTTP 403 in direct retrieval and could not be opened by the research tool. The precise upstream record was therefore recovered from the pinned UnsolvedMath corpus and verified against the official primary PDF:

- Groups and Geometries, Oberwolfach Reports 12/2005, DOI https://doi.org/10.4171/owr/2005/12 .
- C. E. Praeger and A. Seress's contribution, pp. 690--693.
- Theorem 3 and Question 4 on printed p. 692, PDF page 46. This page was visually inspected after rendering.
- The question is strictness of the upper bound for **every** finite primitive twisted-wreath group and its specified component. The corpus wording agrees; no smaller substitute target is used.

## Primary mathematical study

Giudici, Li, Praeger, Seress and Trofimov, 2006, DOI https://doi.org/10.1515/9783110199741.75 . The publisher's bibliographic record confirms the chapter and pp. 75--94. The accessible author-upload rendering is at https://www.researchgate.net/publication/228677624_On_minimal_subdegrees_of_finite_primitive_permutation_groups .

The full target appears as Question 1.6. The established subgroup construction is in Construction 4.1 and Lemmas 4.2--4.3; the general double-coset assignment is Construction 4.12. Those mechanisms are independently re-proved in the partial-results artifact. They do not resolve the strict inequality merely by restatement.

Example 4.15 in that accessible rendering contains an all-n component-class assertion inconsistent with the exact A8 count. The printed publisher PDF was not retrieved, and the author-upload PDF also returned 403; therefore the discrepancy is explicitly confined to the inspected author-upload text. The underlying A8 count is independently proved.

## Later related sources checked

- Chua, Giudici and Morgan, Coprime subdegrees of twisted wreath permutation groups, Proc. Edinburgh Math. Soc. 62 (2019), 1137--1162; https://doi.org/10.1017/S0013091519000130 ; author preprint https://arxiv.org/abs/1801.02456 . The preprint PDF was read, particularly the introduction and Section 2. Its main subject is existence/classification of coprime subdegrees for specified families, a different question. Theorem 2.3 supplies the primitivity criterion used for the alternating examples here. No inference from the word “settle” in its abstract to settlement of this problem is made.
- Burness and Shalev, Permutation groups with restricted stabilizers, J. Algebra 607 (2022), 160--185; https://doi.org/10.1016/j.jalgebra.2021.08.012 . Inspected author PDF dated July 23, 2021: https://seis.bristol.ac.uk/~tb13602/docs/BSh_final.pdf . Remark 3.9, p. 15, was visually inspected. Its stated minimum 12 for the referenced A5/A6 example is inconsistent with the self-contained minimum-15 proof. The surrounding two-point-stabilizer conclusion is not invalidated by this correction. The version of record was not independently compared.
- Cheryl Praeger's public publication list confirms the 2006 bibliographic entry: https://cherylpraeger.github.io/research.html .

Search strings included: “Minimal Subdegrees” “Twisted”; “OWR793” “006”; “On minimal subdegrees” pdf; “MinSubDeg” “Question” twisted wreath; “twisted wreath” “minimal” “strict”; “Question 1.6” “subdegrees”; “minimal subdegrees” “strict inequality”; “On minimal subdegrees” correction OR erratum; “Giudici” “subdegrees” “105”; and the named 2019/2021 papers. Search-result crawl dates were not treated as publication dates. No author or third party was contacted.

## Pinned corpus and repository checks

Dataset revision: 37e53eabe540fb458758e198be61634bd02ee008. The entire problems.json and research_results.json files were hashed and agree with the repository's manifest; hashes are in SOURCE_PROVENANCE.json. Exactly one matching numeric record was selected. No prior report matching the numeric ID, problem code, or exact title was located in research_results.json.

Live main was verified as 03c3cc4ee2502f6937185fb55d17e1143fe5b6ea at the repository gate. The queue had rank 601, queued, 0/5. State had no entry for this ID; the exact attempt directory was absent. Exact-ID repository search, PR search, branch search, and “subdegrees” PR search returned no matches. The related-target-groups file contained no ID match; the pinned corpus had no additional title/statement matching the subdegree/twisted-wreath terms. This does not rule out differently named or unindexed duplicates.

The current assessment file's full Git blob SHA was independently matched against the live file metadata. Its selected review_hash is 6fa59e0ea044936e4e25f8dd332365b9a47b7ed61067608e72a192dff32d93b1. The original individual review was also fetched at the pinned repository commit. It suggests a one-coordinate point. Proposition 2 shows exactly why that mechanism cannot yield strictness.

## Attribution and scope

The source corpus is credited to UnsolvedMath contributors (CC BY 4.0); source publications retain their own terms. This package publishes original proofs, derived finite data and citations only. It excludes source PDFs, corpus dumps, source-page images and private research coordination. Neither the value 15, the A8 class count, nor the source discrepancies are claimed to be previously unknown.
