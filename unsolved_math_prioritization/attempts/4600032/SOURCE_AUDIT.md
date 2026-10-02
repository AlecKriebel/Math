# Formulation audit: 4600032 / AMR-045-0032

2026-10-02. **Formulation hold.** The exact imported sentence has an elementary periodic-point obstruction. The primary PDF prints the opposite embedding direction. No determinate source correction incorporating the missing periodic condition was located. No substantive resolution of an intended repaired one-sided embedding theorem is claimed.

## Source comparison

The requested https://www.unsolvedmath.com/problems/4600032 was attempted and failed. The complete pinned record and prior report were read from dataset revision 37e53eabe540fb458758e198be61634bd02ee008. Both complete cached JSON files were checked against the repository's byte sizes and SHA256 hashes. The record asks whether a one-sided subshift S of entropy less than log N, with at most N one-step shift preimages per point, embeds into the one-sided full N-shift T. Its report asserts that the statement is faithful to Boyle Question 20.2. That assertion is inaccurate about the direction.

The primary author PDF was retrieved completely and its definitions on p.3 and all of Section 20 on p.21 were read. Page 21 was rendered and visually inspected, not merely extracted. The file's cover is dated March 19, 2008. URL: https://www.math.umd.edu/~mboyle/papers/openfinalsub3nov2007.pdf . It is the author-posted version of *Open problems in symbolic dynamics*, Contemporary Mathematics 469 (2008), 69–118, DOI https://doi.org/10.1090/conm/469/09161 . The DOI endpoint was unavailable during this audit; no publisher-version line-by-line comparison is claimed.

There are three distinct formulations:

1. **Printed Question 20.2:** with h(S)<h(T)=log N and the preimage upper bound on S, the conclusion asks for T to embed into S. That conclusion is incompatible with entropy monotonicity
2. **Imported record:** the direction is changed to S embedding into T, but there is no periodic-orbit capacity hypothesis. The fixed-point example in HOLD_RESULT.md rejects this sentence
3. **A possible repaired research question:** the forward direction plus suitable periodic-orbit or preimage-tree compatibility conditions. The sufficiency of any such repair is not established here, and its status as the intended question is not assumed

Immediately above Question 20.2, the same source states the two-sided Krieger embedding theorem with both entropy and periodic-orbit capacity conditions. The source does not impose mixing or irreducibility on S in Question 20.2; only T is full. The definitions section likewise supplies no blanket mixing assumption. The paragraph after the question explicitly discusses compatibility of preimage trees with periodic-point embeddings. Its sentence about comparing the numbers of preimages has the reversed inequality relative to its own tree-embedding description. The correct necessary inequality follows directly by injecting the source preimages into the target preimages; no intended repair is inferred from this inconsistency.

## Expanded/current primary-source check

- The author's current publication page, https://math.umd.edu/~mboyle/papers/ , links the same checked PDF for this article
- The author's open-problem update page, https://www.math.umd.edu/~mboyle/open/ , is marked last revised March 20, 2016. Its complete list of reported solutions contains no Question 20.2 entry or correction
- Other indexed author-hosted drafts, ppost3nov2007.pdf and ppost10sept.pdf, retain the same printed direction and do not supply a verified correction
- Christophe Reutenauer's *Open Problems Session 2*, dated July 13, 2013, records Boyle's problem in §6, p.2: https://mathtube.org/sites/default/files/lecture-notes/Open2.pdf . This PDF was fully retrieved, and p.2 was rendered and visually inspected. The notation interchanges the letters S,T relative to the imported record, but the special-case question has the forward embedding direction into the binary full shift. The preceding text explicitly notes necessary compatibility with periodic orbits; the special-case sentence itself still supplies no formal periodic-capacity hypothesis. It supports the direction correction, not an unambiguous complete repaired target
- Boyle's earlier *Symbolic Dynamics and Matrices*, §9, discusses necessary entropy, periodic and preimage-tree constraints in the one-sided setting: https://math.umd.edu/~mboyle/papers/ima1992.pdf . Its indexed primary text was read. This is credited background for the elementary obstruction, not a new solution

Targeted searches for the exact question, an erratum, the preimage bound, and one-sided full-shift embeddings did not locate an explicit complete correction. This bounded failure to locate one is not evidence that none exists. No outside person was contacted.

## Prior-attempt and related-target gate

Live all-state exact-ID PR, exact-ID/46000 branch, and target-path history searches were empty. Default-branch code search found only review assignment metadata. Related one-sided/embedding and symbolic-dynamics PR searches did not identify this target. In the available recovered all-ref repository (335 remote refs, 2,953 reachable commits), there is no target-path, matching title or exact-ID proof history. Main state and related-target groups contain no matching entry. Live QUEUE gives rank 343, queued 0/5. The complete catalog record gives eligible, no holds, review hash 09f6570c6618950d0a4f0b40a54cae876eeeb8b7575d0791d60086942865d300, and already flags the missing periodic capacity as a potential obstruction.

Adjacent records 4600030–4600034 were read. In particular 4600031 asks for general necessary and sufficient conditions for one-sided embeddings, and 4600033–4600034 concern conjugacy/classification. None is answered by this audit. No proof artifact from another attempt is reused.

## Count and disposition

One substantive author response records the explicit finite-SFT obstruction and proof in HOLD_RESULT.md. Source retrieval and correction searching are not extra turns. Count 1/5; this is not an exhausted five-turn attempt. Further proof work is held until a determinate corrected source statement is established. Four turns remain if the same target is legitimately clarified; the count must not be reset.

Recommended disposition is a formulation/readiness hold, not claimed_solved or a novelty claim. Primary PDFs, rendered pages and raw imported records remain local-only. Independent source/proof review is requested before any final campaign disposition. Completion of an intended research theorem is unassessed because its corrected hypotheses are not fixed.
