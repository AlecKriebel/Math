# PR734 / problem 2515 priority audit

**Verdict: PRIOR FULL RESULT FOUND.** The frozen candidate is a rediscovery of the full counterexample published by **JonLuca De Caro on 24 July 2026**, not a new solution of Kourovka Notebook Problem 21.6. The earlier preprint proves the same infinite conclusion with the same finite local group, the same restricted binary wreath limit, and the same argument covering every transitive subgroup. Its primary record is [A counterexample on cyclic blocks in finitary permutation groups](https://zenodo.org/records/21538908), DOI [10.5281/zenodo.21538908](https://doi.org/10.5281/zenodo.21538908).

This priority finding does not contradict the mathematical clearance supplied by the root audit. It establishes a prior full result and a required attribution. It does not establish plagiarism, dependence of one derivation on another, editorial acceptance, or the earliest possible historical predecessor.

## Scope and controlling problem

The audited input is the frozen PROOFS.md at head `7a00d71fdf01ffb785863c859d75e88f943d38cf`; its exact bytes and the two prior source-audit files are hashed in `input_metadata.json`. No candidate proof, other audit shard, Git state, PR, publication, or release was changed.

The current editor-hosted [October 2026 update-2 Notebook](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-1.pdf), printed p.177, Problem 21.6, asks a universal containment question for transitive Sylow p-subgroups of an arbitrary transitive finitary group G. The required individual cycle supports are blocks for the sought subgroup H. Printed p.89, Problem 15.23, defines total imprimitivity through finite point sets contained in finite blocks. Both complete pages were inspected visually. The candidate treats the intended infinite setting, with p=2 and S=G, and excludes even the weaker cycle-support condition without total imprimitivity.

The [current editor update post](https://kourovkanotebookorg.wordpress.com/2026/10/06/october-2026-update-2-for-the-21st-edition/), integrated Notebook, updates-only file, and [repository listing](https://kourovkanotebookorg.wordpress.com/repository/) contain no solution annotation or repository entry for 21.6 at this inspection. That current editorial display does not erase an earlier public preprint. The old `21tkt.pdf` URL in the frozen metadata now returns HTTP 404; the current editor link points to `21tkt-1.pdf`. This is source replacement drift, not a mismatch of problem identity. The new complete PDF has 1,872,313 bytes and SHA-256 `c6056609ce6e48bacc28db5acc61b835f8095104e47d5c9e95b84abdfd6de692`.

## Primary evidence for the full predecessor

An ordinary read of the official [Zenodo record API](https://zenodo.org/api/records/21538908) returned creator JonLuca De Caro, publication date 2026-07-24, creation time 2026-07-24T22:47:55.506462Z, and update time 2026-07-24T22:47:55.864922Z. The five-page PDF independently displays 24 July 2026 on p.1. The record discloses GPT 5.6 Sol assistance and identifies source problem OP-0695 / Kourovka 21.6. It is an open preprint, not an editor-confirmed solution.

The complete PDF and its source archive were retrieved from official public file endpoints. Their downloaded MD5 values match the checksums declared in the record:

| Item | Bytes | SHA-256 | Declared and verified MD5 |
|---|---:|---|---|
| main.pdf | 85,435 | `07ccf31fe5695eaa845750a4daabc16b6fb572fb9e119f2d053eecc8c934d466` | `167c35898355b47e8074b94553935d50` |
| submission.tar.gz | 6,464 | `4208942e4c5431b1ee880f8aeef4f2451d0c4fb0b19b7c7770b5867e9df84ea6` | `0cd920f674278732a3633234deca37af` |

The archive contains `main.tex`. All five PDF pages and the relevant source were inspected; pp.1, 3, 4, and 5 were rendered and checked visually. Full source bodies and PDF/image intermediates were kept private and removed from this audit before closure. The audit retains authored contrasts, bibliographic facts, hashes, and a reproducible finite identification.

## Exact mathematical comparison

| Candidate component | Prior preprint location | Comparison |
|---|---|---|
| Order-32 minimally transitive P on eight points | §4, pp.3–4 | De Caro uses the known group 8T21 in different labels. Full generated groups agree under the relabelling below. |
| Crossing cycle support | §4, p.4 | The prior proof gives a two-point cycle whose translate meets it in one point. The candidate uses a different witness in the same action. |
| First-factor recursion G_(n+1)=G_n wr C2 | §5, p.4 | The same imprimitive binary recursion and identity extension on the other factor occur. |
| Exact bottom stabilizer image P | §5, pp.4–5 | The earlier proof preserves the bottom fibres and proves that their induced local action is exactly its finite Q. |
| Every transitive H is excluded | §3.2, pp.2–3; §5, p.5 | The earlier reduction forces H_B^B to be transitive in Q and uses minimal transitivity, then lifts a crossing cycle. It does not assume H contains the initial Q. |
| Sylow requirement S=G | §3.1, p.2; conclusion p.5 | The same reduction takes the ambient transitive finitary 2-group as its own Sylow subgroup. |

Here is a checkable comparison independent of the source's library labels. Let Q be the earlier action on {1,...,8}, and map its labels by

`rho = [1, 3, 5, 7, 2, 4, 6, 8]`.

Conjugating the complete 32-element Q by rho gives precisely the candidate's parity-defined P. The authored standard-library calculation in `verify_finite_attribution.py` exhausts these finite generated groups, checks this equality, and verifies the prior source's GAP-convention word witness. It also checks the candidate's own crossing witness. Results are recorded in `finite_attribution_certificate.json`.

The infinite equivalence is explicit: a finitely supported binary tail (t_0,t_1,...) in the earlier domain maps to the integer sum t_j*2^j, and the bottom coordinate maps by rho. This maps its stage X_n to D×{0,...,2^n−1}, respects each first-factor embedding, and respects each coordinatewise binary top swap. Induction therefore identifies the entire earlier permutation group with the candidate's G. The equality of bottom actions and the universal H obstruction consequently agree. This domain identification is an audit deduction, not a quotation from the prior paper.

There is no essential gap in this material-equivalence check. In particular, the earlier argument is not merely a finite-domain objection, does not replace individual cycle support by whole-element support, and does not cover only subgroups containing the base copy. It states and proves the full intended infinite negative answer. These are the same possible hidden distinctions that the candidate's mathematical audit already controlled.

## Earlier finite and construction attribution

The finite ingredient predates both 2026 proofs. [Conway, Hulpke, and McKay (1998)](https://doi.org/10.1112/S1461157000000115), §3.1, pp.5–6, explicitly give the 21st degree-eight transitive group, its order 32, its minimal transitivity, and its base/top factor gluing. Replacing their point 0 with point 8 gives the generators in [Hulpke's 2002 author-hosted supplement](https://www.math.colostate.edu/~hulpke/paper/ctglist.pdf), printed p.2, Degree 8, Nr.21. The finite parity twist is the same established gluing mechanism. Hulpke's supplement asks readers to cite [Constructing transitive permutation groups (2005)](https://doi.org/10.1016/j.jsc.2004.08.002). Its author-version §12.3 provides the classification context; that version's Table 2 omits the degree-eight row, so the exact identification rests on the 1998 discussion and 2002 supplement.

The Frattini-contained core-free point-stabilizer mechanism is established in [Dalla Volta and Siemons (2007)](https://arxiv.org/abs/math/0702194), Theorem 3.1(ii), arXiv p.5. A later explicit family in [Xia and Zheng, arXiv:2608.25792v1](https://arxiv.org/abs/2608.25792), Notation 4.1 and Lemma 4.2, pp.6–7, specializes to precisely P: p=2, m=2, b=(1,0), kernel ideal (X1,X2). The construction in the proof of Theorem 1.5, pp.11–12, then has kernel dimension 3 and group order 32. Its first generator is the inverse of the candidate a, and its second is b. This August 2026 preprint is later than the July full counterexample; it is family context, not earliest credit.

The infinite ordered wreath method is explicit in [Pinnock's author-hosted notes](https://chrispinnock.com/assets/2015/01/fpg.pdf), §1.2, Lemma 1.2, p.3, and the exact fixed-first-component direct limit appears in [Altınkaya's June 2025 primary conference slides](https://www.advgrouptheory.com/agta2025/Talks/Altinkaya.pdf), PDF pp.21–23. These constructions and block-chain arguments must not be described as new. De Caro's full preprint already combines this method with the finite obstruction and hereditary restriction.

## Central literature and access limits

Primary metadata and abstracts were screened for Asar's 2011 cyclic-block paper, 2017 Turkish Journal paper, 2017 Communications in Algebra paper, 2006 finitary paper, and 2008 subgroup paper. The accessible records concern examples already having the property, minimal non-FC questions, stabilizers, or block normalizers. These abstracts do not announce the target answer. That is an abstract-level contrast, not an exclusion of their unseen theorems.

The original 2011 paper was not obtained: the canonical publisher PDF endpoint returned HTTP 202 with zero bytes, and direct reader routes failed. The 2017 Communications in Algebra PDF returned HTTP 403. Ordinary Turkish journal requests returned 403; its web download failed, and the separate legacy publisher archive hostname did not resolve. No traffic-filter workaround, account login, purchase, or outreach was used. The older audit's Scribd reproduction does not supply a primary full-text check here. Exact Proposition 2.1 / Lemma 3.1 contrasts from that reproduction are therefore not promoted to independently verified original-paper evidence.

A newly located [Asar 2026 Sylow paper](https://link.springer.com/article/10.1007/s11587-026-01079-8), published 7 March 2026, has a primary accessible abstract about unique-versus-continuum numbers of Sylow subgroups. Its full text is subscription content. [Bier, Leshchenko, and Sushchanskyy (2016)](https://doi.org/10.1016/j.jalgebra.2015.12.019) has a primary abstract about Sylow subgroups of the full finitary symmetric group; that ambient scope differs from Sylow subgroups of arbitrary G in 21.6. The 1999 Leinen–Puglisi manuscript is explicitly closed access in its author-institution repository. No unseen classification or containment theorem from these papers was assumed.

These access limits prevent a claim that July 2026 is the earliest historical answer. They do **not** weaken the documented existence of a complete, earlier, materially identical public proof. Complete original Asar texts would help extend historical attribution; no outreach was prepared or initiated.

## Search controls and disposition

The deduplicated ledger records 76 indexed search queries across exact problem answers, finite minimal transitivity, Frattini stabilizers, parity, hereditary block restriction, wreath/direct-limit transfers, and finitary Sylow subgroups, plus two ordinary direct Zenodo catalogue queries. The indexed searches failed to reveal the exact prior preprint. Both direct Zenodo queries returned record 21538908. This is concrete evidence that a bounded search miss cannot serve as a novelty certificate.

The appropriate disposition is **retain the independently checked mathematics as a verification or rediscovery, credit De Caro's full prior result, and do not promote PR734 as a novel solution**. A different elementary presentation or a different crossing witness in the same finite action does not change the full theorem's priority. Necessary finite attribution is Conway–Hulpke–McKay plus Hulpke's supplement/classification work; the exact full-result attribution is De Caro. No proof repair or paper drafting was performed in this audit.
