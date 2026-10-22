# 30004679 / OWR-7155442-013: exact source and eligibility

## Assigned question

Manlio Valenti's open-problem contribution in *Computability Theory*, OWR21/2021, DOI10.4171/OWR/2021/21, printed p.1183/PDF p.35, asks two **ordinary Weihrauch** reductions:

    C_{N^N} <=_W Sigma^0_1-RT ?
    C_{N^N} <=_W wFindHS_{Pi^0_1} ?

[Official report](https://ems.press/content/serial-article-files/46899). The full contribution was read, and the question page visually checked. It says trees of finite strings N^{<N}; the imported phrase “subtree of N^N” is a notation error, not a changed problem. The following KL-versus-DS question and the Gamma-coded hierarchy on the next page are explicitly separate. The imported DS literature update does not answer the two assigned questions.

C_{N^N} chooses a path through an ill-founded tree on N, given its characteristic function, equivalently a point of a nonempty negatively described closed set in Baire space. Let [N]^N mean strictly increasing sequences, and let [f]^N be the infinite subsequences of f. A homogeneous f either has all its subsequences inside an open P or has all of them outside. Sigma^0_1-RT accepts every open P and returns either type of homogeneous solution. wFindHS_{Pi^0_1} has the promise that **no** homogeneous solution lands inside P; its outputs consequently avoid P. An open-set name enumerates basic cylinders. Ordinary postprocessing receives the original input name as well as the oracle output; the reduction must work for every allowed output/realizer.

## Existing primary analysis and exact distinctions

[Marcone–Valenti, arXiv2003.04245v3](https://arxiv.org/abs/2003.04245v3), published in JSL86(2021),316–351, DOI10.1017/jsl.2021.10, explicitly retains these as Questions6.1–6.2 (preprint p.32, visually checked). Its definitions and relevant proofs were read: §§2.1–2.2, Definition4.1, Solovay construction Definition3.9/Lemma3.10, Propositions4.8–4.10 and4.29, Corollary4.16, and the conclusions. Known facts include UC_{N^N} <_W wFindHS_{Pi^0_1} <=_W C_{N^N}, C_{N^N} equivalent_W C_{2^N} star wFindHS_{Pi^0_1}, and wFindHS_{Pi^0_1} <_W Sigma^0_1-RT. The missing compact-choice call is not computable decoding. Strong nonreductions and arithmetic reductions do not settle ordinary reductions.

[Marcone–Osso, arXiv2410.06928v1](https://arxiv.org/abs/2410.06928), *The Galvin–Prikry Theorem in the Weihrauch lattice* (2024), was checked at Proposition2.29, Lemma5.11, Remark5.12 and Proposition5.13 with their relevant arguments. It retains the ordinary upper bound for wFindHS and gives an **arithmetic** equivalence with Baire choice. The superscript “a” is essential; its loss in extracted PDF text could falsely suggest a solution. Proposition2.29 on PDF p.15 was visually checked. No ordinary equivalence is inferred.

[Goh–Pauly–Valenti, arXiv2401.11807v5](https://arxiv.org/abs/2401.11807v5) (2025 revision), introduction and §4 scope, resolves the separate KL/descending-sequence issue. No proof in this attempt imports its separation theorem for the Ramsey targets. A bounded current search found no authoritative full answer to the two assigned questions. This is not exhaustive literature coverage or novelty certification.

## Prior and related-attempt gate

ID, OWR alias, wFindHS and open-Ramsey PR/commit searches, both target paths, 373 live branches and 425 mirrored refs found no matching attempt. See PRIOR_GATE.json. Neighboring records 30003692 (list choice and other questions) and30004680 (DS hierarchy and determinacy) are distinct.

[PR308](https://github.com/AlecKriebel/Math/pull/308), target30003661, asks whether WKL/compact choice strongly reduces to planar path-connected choice. Its frozen source and result were read. It neither attempts the present ordinary reductions from Baire choice nor resolves them. Merely sharing Weihrauch terminology or a path output is not a duplicate.

Direct UnsolvedMath retrieval failed; pinned imports at revision37e53eabe540fb458758e198be61634bd02ee008 were checked against the primary source. Raw records/PDFs remain separate reading inputs, not public files.

## Gate disposition

Eligible for a five-turn author attempt. **Substantive author turns: 0/5.** Known reductions and reformulations used as background must remain credited. A full positive answer must give computable name transformations with the exact domain promise and arbitrary-output correctness; a full negative answer must rule out all ordinary reductions, not just a coding template or strong reduction.
