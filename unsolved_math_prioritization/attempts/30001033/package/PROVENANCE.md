# Source and status checks

Checked 2026-10-04 UTC. The exact target is 30001033 / OWR-2053-013, originally queued at rank 610, 0/5.

## Source chain

1. The requested catalogue URL https://www.unsolvedmath.com/problems/30001033 was attempted first. Its direct request returned HTTP 403; the web-tool open also failed. The pinned imported record was inspected rather than pretending the live catalogue had been read.
2. The primary source is the contribution “Two new families of Cayley graph expanders” by Norbert Peyerimhoff, joint work with Alina Vdovina, in Oberwolfach Report 42/2008, printed pp. 2389–2391. The exact conjecture is Conjecture 3 on p. 2391. Landing page: https://ems.press/journals/owr/articles/2053 . Official PDF: https://publications.mfo.de/bitstream/handle/mfo/3086/OWR_2008_42.pdf?isAllowed=y&sequence=1 . The report concerns the September 2008 workshop; EMS records publication on 30 June 2009. The catalogue's mixed year conventions should not be mistaken for different reports.
3. The primary detailed paper is https://arxiv.org/abs/0809.1560 (v1, 9 September 2008). Its two-generator presentation in §2 matches the target after x0↦x and x1↦y. Its 9×9 matrices on p. 5 and the leading-diagonal scheme in §2 underpin the reconstructed certificate here. The three relators were separately checked by exact polynomial multiplication, so a wrong transcription would be detected. Its Conjecture 1 explicitly distinguishes the proven visible filtration quotients from the conjectured equality with lower-central quotients. The published paper is N. Peyerimhoff and A. Vdovina, J. Pure Appl. Algebra 215 (2011), 2780–2788, DOI https://doi.org/10.1016/j.jpaa.2011.03.018 . The detailed source inspected was the arXiv version, not an assertion that every typo survived into print.
4. The follow-up https://arxiv.org/abs/1304.4480 (2013), by Barker, Boston, Peyerimhoff and Vdovina, Remark 3.2, still states a finite-width conjecture and reports Magma checks through index 100. It appeared in IMRN 2015, 3598–3618. Its notation changes: the earlier two-generator group is denoted H in that article, while G denotes the ambient seven-generator triangle group. Thus the follow-up is used as supporting status/context evidence, not as an independently certified universal computation for every formulation. The source reports its computations; they were not reproduced to depth 100 here.

## Statement-quality cautions

The report's p. 2391 was visually inspected. It really prints γ(i+1)=[γ(i),γ(i)] while naming the lower central series. We use γ0=G and γ(i+1)=[γ(i),G], consistent with the intended lower-central problem. The 2008 preprint's lower exponent-2 recurrence has a similar printed issue; the later follow-up uses the conventional [λ(i),G]λ(i)^2 recurrence. Some other preprint indices and letters are visibly inconsistent. Our proof therefore spells out conventions and verifies the concrete matrices instead of relying on an unexamined transcription.

The catalogue's finite-width shorthand does not justify replacing the exact 2,3,3 periodic formula by an arbitrary uniform bound of 3. This package retains the full exact formula.

## Current-literature search and limits

Searches included exact title, author names with “finite width” and “conjecture,” resolution/proof terms, and recent-year variants. The authors' Durham publication page and later citing records were checked. Relevant further primary leads included “Trivalent expanders and hyperbolic surfaces,” “Parameterized Counting and Cayley Graph Expanders” (2023), and the 2015 Beauville work. Search results did not identify a later theorem resolving this exact all-index lower-central formula. Some Durham repository opens returned access errors; no conclusion is based on inaccessible full text.

This is a bounded search, not proof that no resolution exists. Accordingly we recommend **unsolved**, not a categorical historical claim that the problem is certainly open as of this date. Neither a search miss nor the age of a conjecture supplies novelty certification.

## Repository checks

Read the current repository and queue instructions, queue, state, related-target groups, and pinned selected statement. The observed main head was 09c599e87ba4aae8c7fd16924b607545c1d82a0a. The queue blob was c1009ab2e12b93cffb15cb17c0ac893979ce5a44; the state blob was 5d61841df2ecf0363dfba1858e568fc79734819f.

The live row was rank 610, queued, 0/5. There was no target entry in state, no matching related-target group, no exact-ID code result or PR result, no “finite width” PR result, no exact-ID branch, and no existing target attempt README at the checked path. The pinned research-results dictionary had no OWR-2053-013 entry. These checks found no duplicate but cannot exclude differently named or unindexed work.

No shared queue or remote state was changed. The proposed update is only this target's Status=unsolved and Turns=5/5; no Findings update is proposed without separate approval.

## Scope of the artifacts

The polynomial relations, rank cycle, Smith factors, bounded finite-group images, and Magnus leading terms are exact calculations with replayable controls. The main unresolved mathematical issue is separately stated in PROOF.md, equation (12). The computations and source-derived material are not advertised as a novel resolution. The package intentionally omits downloaded scholarly PDFs and imported corpus files.
