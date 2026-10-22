# Source, prior-work, and novelty gate

Checked 3 October 2026 UTC. Problem 20001353 / AIM-DYNAMICAL_SYSTEMS-0011, queue rank 512.

## Original target

Recovered title: **Maximal subgroups in Thompson groups**.

Recovered statement: **Find new maximal subgroups of infinite index in Thompson groups**.

Provenance: the catalogue's original_statement and clean_statement agree, as does the separately cached prior research record. Their recorded canonical provenance is AIM workshop *Groups of dynamical origin*, section 3, item 3.2, canonical extraction item 10. The source URL is [AIMPL section 3](http://aimpl.org/groupdynamorigin/3/).

The exact [catalogue page](https://www.unsolvedmath.com/problems/20001353) returned HTTP 403 via the local HTTP read and was inaccessible through web retrieval. The AIMPL page returned HTTP 502 in the local read and was inaccessible through web retrieval. Therefore the wording above is recovered from the pinned catalogue extraction, **not independently reverified against a fresh copy of the original AIMPL page**. Its consistency across two cached records is not two independent primary witnesses.

The accessible [official AIM workshop report](https://aimath.org/pastworkshops/groupdynamoriginrep.pdf), page 1, lists Rachel Skipper's talk on maximal subgroups of Thompson groups. It supports the workshop context but does not reproduce this particular problem. It must not be cited as the direct source of the exact sentence.

The catalogue/queue title “A maximal dyadic-pair stabilizer in Thompson's group T” names an earlier partial result. It must not replace the original question. The source does not explicitly enumerate F,T,V, does not ask for classification, and does not assert that no examples are known. Working in classical T is within the ordinary interpretation of “Thompson groups”; the scope is declared rather than inserted into the quotation.

## Pinned-cache integrity

The privately retained source records were extracted from these read-only inputs:

- problems.json: SHA256 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf
- research_results.json: SHA256 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b

No source corpus, raw record, source PDF, or full-text source extraction belongs to the public packet.

## Genuine prior attempts

The existing cached attempt proves the k=2 case, including maximality, countable index, F wr C_2 structure, and conjugacy. It explicitly does not establish the case k≥3 and has low novelty confidence. We do not claim the pair case as new work.

Read-only searches of AlecKriebel/Math pull requests for the exact ID, exact AIM code, “dyadic”, and “maximal subgroups” found no same-question PR. A wider Thompson search found [PR 409](https://github.com/AlecKriebel/Math/pull/409), concerning conjugacy in braided Thompson groups; that is mathematically distinct and is not a duplicate of this problem. This is a bounded search, not a guarantee that no unindexed branch, inaccessible conversation, or differently titled attempt exists. The inspected queue row still had queued, 0/5 before this work.

## Directly matching later literature

[Alper Ferudun, *Maximal Finite-Set Stabilizers in Thompson's Group T*](https://eulersolve.org/papers/aim-dynamical-systems-0011/), manuscript 4 September 2026, released online 5 September 2026, DOI [10.5281/zenodo.22324898](https://doi.org/10.5281/zenodo.22324898), announces exactly the all-k theorem proved in PROOF.md. Its landing page was retrieved and explicitly describes it as an AI-assisted, unrefereed preprint. Its linked PDF and verification report could not be retrieved, including through the DOI route.

This is decisive against claiming novelty for the theorem here. It is not evidence that the inaccessible proof has passed independent review. We instead reconstruct and check the theorem from elementary definitions, with a fresh independent audit requested on this packet.

## Other current primary literature

- Gili Golan Polak, [*On maximal subgroups of Thompson's group F*](https://ems.press/journals/ggd/articles/14297830), Groups Geom. Dyn. 19 (2025), 797–860, DOI 10.4171/GGD/795; published online 23 May 2024. The [arXiv full text](https://arxiv.org/html/2209.03244) proves that all infinite-index maximal subgroups of F are closed in the core-automaton sense and constructs infinitely many pairwise nonisomorphic examples. It is not a complete classification.
- James Belk, Collin Bleak, Martyn Quick, Rachel Skipper, [*Type systems and maximal subgroups of Thompson's group V*](https://eprints.gla.ac.uk/328840/2/328840.pdf), Trans. Amer. Math. Soc. Ser. B 12 (2025), 417–469. Corollary 2.3 treats same-tail finite-set stabilizers in V, and Theorem 7.5 supplies an uncountable family of pairwise nonisomorphic maximal subgroups not stabilizing finite point sets. These are Cantor-space V results, not a proof for T's circular-order action.
- The same four authors, [*The maximality of T in Thompson's group V*](https://eprints.gla.ac.uk/354070/3/354070.pdf), Arch. Math. 125 (2025), 1–7, DOI 10.1007/s00013-025-02136-8, prove T maximal in V. Maximality in one ambient group must not be confused with maximality of a subgroup inside T.
- Gili Golan, [*Higman–Thompson groups F_n all the way down*](https://arxiv.org/abs/2607.04038), July 2026 preprint; [full text](https://arxiv.org/html/2607.04038v1), Theorem 1.1, gives nested infinite-index maximal copies of F_n with controlled overgroups and trivial intersection. Problem 1.4 still asks about classifying minimally acting maximal subgroups. It is a distinct broad classification problem.

These sources show why “there are no known examples” and “all maximal subgroups have been classified” would both be wrong. The requested example-producing direction has established and recent contributions. The direct all-k T theorem is already announced elsewhere and is independently proved here; no global firstness, full classification, or definitive end to this open-ended programme is claimed.
