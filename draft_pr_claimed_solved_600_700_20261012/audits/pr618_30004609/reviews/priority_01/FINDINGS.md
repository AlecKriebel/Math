# Independent priority audit: PR #618 / problem 30004609

Audit date: 2026-10-12 (America/Los_Angeles). Audit role: primary-source priority and attribution review, independent of the two fresh mathematical-review families. No external communication, PR action, publication action, queue edit, or original-packet edit was made.

## Verdict and exact scope

**The full-source-resolution framing is defensible, subject to mandatory literature and chronology corrections. An exhaustive first-resolution claim is not defensible.** The frozen candidate addresses the full conjecture in Tohăneanu's Oberwolfach Report 5/2021, p. 284: finite central free arrangements over characteristic-zero fields, nonzero exponents only 1 and 2 with at most one 3. Products, nonessential arrangements and ranks at most two are legitimate reductions/boundaries. This audit found no pre-October-4 inspected primary theorem that supplies the unresolved all-rank cyclic case without first proving the central incidence structure. This bounded finding is not proof of historical novelty.

A materially important exact result was found during this review: Alper Ferudun's October-12-2026 unrefereed preprint gives the same full target, by an all-rank relation-dependency support count and terminal-triple modular removal. It must be acknowledged. Its existence does not justify treating the October-4 frozen candidate as a rediscovery of a pre-existing October-12 publication, or rejecting a valid proof solely for that reason. Neither independent development nor exhaustive first priority can be inferred from the records.

## Chronology that can actually be checked

The parent's authoritative read-only GitHub evidence is preserved at the audit root in `PR_PUBLIC_CHRONOLOGY.json`, `REPOSITORY_PUBLIC_VISIBILITY.json`, and `PROOF_COMMIT_CHRONOLOGY.txt`. PR #618 was created at **2026-10-04T16:19:57Z**, with unchanged head `cae273cb692bde0a0a73790c3840af8c7eb1eed7`. That head's commit time is 2026-10-04T16:18:59Z. The frozen proof SHA-256 is `73716fdb49896b2443ada06ed707dba1e0d08f304d9e563cf251c949d8752798`. The repository is currently public. Commit dates alone are mutable attribution metadata; the server's PR creation date is the stronger disclosure evidence. This audit has not reconstructed every historical repository-visibility change.

The public Zenodo record API independently supplies:

| Item | Version DOI | Server record creation (UTC) |
|---|---|---|
| Ferudun original note | 10.5281/zenodo.23307000 | 2026-10-12T00:39:41.612424Z |
| Ferudun attribution revision | 10.5281/zenodo.23313624 | 2026-10-12T09:20:42.830800Z |

The concept DOI is 10.5281/zenodo.23306999. PDFs were obtained from the public Zenodo file API, and their hashes match the author's displayed metadata. Version 1.1 corrects all-2 attribution. The candidate's dated public PR is earlier than these inspected Zenodo records. That statement is narrower and better supported than a universal first-proof claim. The mathematical result should be framed as a proof of the source conjecture, with this precise chronology in a brief priority note.

## Earlier results and the exact remaining gap

### Tohăneanu's own low-exponent program

Primary sources: [2017 v1](https://arxiv.org/abs/1707.07091v1), [2020 v3](https://arxiv.org/abs/1707.07091v3), [2022 withdrawal](https://arxiv.org/abs/1707.07091v4), and [OWR 5/2021](https://ems.press/content/serial-article-files/46883), printed pp. 283–286.

The all-1/2 theorem was already stated and proved in the July-2017 first version, pp. 2–5; v3 carries it in §3. The January-2022 withdrawal notice identifies hand-enumeration incompleteness in §§4.2.1–4.2.2 and an unjustified factor-size inference in Proposition 4.8(a). It does not identify the all-2 theorem as false. Accordingly, credit Tohăneanu for that theorem, while preserving the withdrawal warning and avoiding unsupported dependence on affected small-rank or inductively-free proofs.

The proof strategy already includes free-arrangement formality, rank-two multiplicity bounds, exponent-derived rank-two counts, and construction of a modular coatom from two hyperplanes occurring only in one dependent triple. The terminal-triple mechanism is v3 Lemma 2.2 (pp. 3–4); the one-3 count is Lemma 4.2 (p. 7). These are antecedents of the candidate's pruning and count, even though it reproves them directly. The all-rank forcing of a cyclic core is the substantive additional step.

### DiPasquale's TF2 theorem: two subcases covered, cyclic case excluded

Primary source: [arXiv:1806.05295v1](https://arxiv.org/abs/1806.05295v1), pp. 13–15 and 19–21. Publication metadata is confirmed by [the publisher](https://link.springer.com/article/10.1007/s00208-021-02357-6): Math. Ann. 385 (2023), 745–786, DOI 10.1007/s00208-021-02357-6; online version of record January 24, 2022. The theorem numbers below refer to the inspected arXiv version, since its numbering was not silently substituted for the journal's.

Corollary 4.10 establishes total formality for free multiarrangements. Section 6 defines TF2 by total formality plus vanishing of the higher free modules. Proposition 6.1 equates freeness, supersolvability and exactly r−1 multiple rank-two flats for irreducible TF2 arrangements; its proof uses rank-two connectivity and an incidence construction. This establishes a substantial published predecessor for the tree portion of the candidate.

Here is the applicability calculation, using the candidate's independently checkable counts. Write R for the global relation space, and q for the sum of the dimensions of the local rank-two relation spaces. For an irreducible all-2 arrangement, n=2r−1, there are r−1 triple flats, and q=dim R=r−1. For a one-3 arrangement with exactly one fourfold flat, u=r−2 and v=1, so q=u+2v=r=dim R. Formality makes the local-sum map onto R; equality of dimensions therefore makes it an isomorphism. The same local-relation independence persists in each localization. The recursively defined higher relation kernels vanish; Corollary 4.10 supplies total formality, so these arrangements are TF2. Proposition 6.1 then yields supersolvability.

For the remaining one-3 case, v=0 and u=r+1. The local-sum map has source dimension r+1 and image dimension r, so its kernel has dimension one. This is a genuine dependency among rank-two relations. The arrangement cannot be TF2: otherwise Proposition 6.1's rank identity would require n=r+u=2r+1 rather than 2r. The rank-three K4 arrangement is already an explicit boundary showing why a free arrangement need not be TF2. Invoking Proposition 6.1 for the cyclic case would drop an essential hypothesis. Its §7 treatment of formal rank-three non-TF2 arrangements provides homological characterizations, not an all-rank substitute for the missing forcing step.

### Earlier tree/Orlik–Terao classifications

Primary source: Denham, Garrousian and Tohăneanu, [arXiv:1211.4562](https://arxiv.org/abs/1211.4562), Ann. Comb. 18 (2014), 289–312, §5 (arXiv pp. 18–21). Theorem 5.6 relates line-closed 3-trees, supersolvable all-2 arrangements and iterated parallel connections with three-point lines. Theorem 5.11 characterizes quadratic complete-intersection Orlik–Terao algebras. The tree and parallel-connection descriptions should be credited; line-closedness or the complete-intersection assumption cannot be inferred from bare formality without an argument.

Le and Römer, [arXiv:1211.5318](https://arxiv.org/abs/1211.5318), J. Algebraic Combin. 38 (2013), 989–1016, Theorem 4.16 and Corollary 4.18 (arXiv pp. 18–20), require a complete-intersection Orlik–Terao ideal before obtaining equivalences involving freeness, formality and supersolvability. This is a restricted classification. It does not supply the full target; even the six-element K4 arrangement has four necessary quadratic generators at codimension three and is outside the quadratic complete-intersection class. The unique-fourfold-flat case is also outside that class's rank-two multiplicity condition.

Schenck and Tohăneanu, [arXiv:0901.0253](https://arxiv.org/abs/0901.0253), Math. Res. Lett. 16 (2009), 171–182, §3 (arXiv pp. 10–11), already describe the K4 triangle-relation example and higher relation kernels. The existence of a K4 relation dependency is not itself new. The candidate's distinctive proof step is forcing every minimal dependency into precisely that core through the global incidence-cycle bound, without assuming the arrangement graphic.

Le and Mohammadi, [arXiv:1502.01005](https://arxiv.org/abs/1502.01005), Adv. Appl. Math. 71 (2015), 34–51, Theorem 4.1 and examples in §5, study relation subsets and Orlik–Terao ideals. They do not eliminate the relevant extra hypotheses or classify all low-exponent free arrangements. Assuming quadraticity/complete intersection to invoke earlier equivalences merely transfers the central difficulty.

### Low-rank classification and modern formality work

Tohăneanu, [arXiv:1405.2122v2](https://arxiv.org/abs/1405.2122v2), Discrete Math. 339 (2016), 54–61, Theorem 2.4 (arXiv p. 7), classifies rank-three arrangements with a minimal quadratic derivation. The rank-three target is thus established prior work. DiPasquale, Sidman and Traves, [arXiv:2209.04929v2](https://arxiv.org/abs/2209.04929v2), Proposition 7.9 (arXiv pp. 30–31), explicitly explains that the first and third types of that classification are supersolvable/free and the second is nonformal. Its broader results concern Jacobian saturation, rigidity and formality; they do not prove the all-rank low-exponent target.

Möller, Mücksch and Röhrle, [arXiv:2202.09104v2](https://arxiv.org/abs/2202.09104v2), DCG 72 (2024), 73–90, Lemma 2.1 and Corollary 5.2, provide a standard modular-coatom criterion and preservation of formality under modular localization. This is further prior context for the candidate's direct pruning argument. It does not force the needed modular coatom from low exponents.

### Recent regular-matroid theorem

Liang and Wang, [arXiv:2608.01331v2](https://arxiv.org/abs/2608.01331v2), Theorem 1.1 (p. 1), prove free iff supersolvable for central arrangements whose underlying matroid is regular. The hypothesis is material. A four-element rank-two flat gives a U(2,4) restriction, so the unique-fourfold-flat branch is not regular. In the no-fourfold branch, graphical/regular structure follows after the candidate's core-and-attachments analysis; assuming it at the start bypasses the exact central difficulty. This route is blocked as a replacement proof until an independent mechanism establishes regularity. The result deserves contextual mention if the paper discusses graphic matroids, but cannot be advertised as already resolving the full source conjecture.

## The later exact preprint and mechanism comparison

Primary source: Ferudun, [version 1.1](https://doi.org/10.5281/zenodo.23313624), Theorems 1.1–1.2, Lemmas 4.2–4.3, Theorem 5.2 and Remark 6.1 (pp. 2, 7–11). Its full target is identical. Its stronger formal-arrangement statement assumes n=2r, rank-two multiplicities at most four and the matching rank-two defect. Relevant proofs were checked directly; no missing hypothesis was found in that all-rank argument.

Both proofs use the dimension deficiency among local triple relations, support cancellation, connectedness and modular terminal-pencil removal. The candidate chooses a minimal dependency, observes that every support element occurs at least twice, and bounds its incidence subgraph by the whole graph's cycle dimension three. This forces four triples on six elements and exhausts the cyclic core. Ferudun instead compares the numbers of leaves outside a dependency support and remaining triples, obtaining a terminal triple; induction ends at the complete quadrilateral. Its Remark 6.1 gives the same K4-with-triangle-attachments classification. These are distinct presentations with substantial mathematical overlap. The new paper should explain this comparison without claiming that the shared standard mechanisms are newly invented, or speculating about whether either author saw the other's work.

## Required edits before publication promotion

1. Update every current novelty/source-audit assertion that no full-target source was located. Preserve the dated October-4 audit as historical evidence; label the current October-12 update distinctly.
2. Cite Ferudun's exact full-target preprint in the introduction/priority note and include the checked PR-versus-Zenodo chronology. Do not use a title/abstract promising a certified first solution or a theorem still open as of October 12 without the qualification.
3. Credit Tohăneanu's 2017 all-2 theorem and the shared formality/modular-pruning/numerical-count strategy. Continue to state the 2022 withdrawal caveats precisely; do not treat every sentence of the withdrawn paper as disproved.
4. Add DiPasquale's published TF2 predecessor and make the equality-of-local-relations subcase deduction explicit, while explaining why the cyclic one-3 case escapes it. Cite theorem numbers as arXiv numbering unless the journal numbering is checked.
5. Credit the earlier DGT tree/parallel-connection structure and known rank-three classification. Make no claim to discover supersolvability of the K4 arrangement or terminal-triple modular pruning.
6. Retain characteristic zero and all source boundaries; any arbitrary-characteristic extension would require its own proof/assumption audit. Retain an explicit unrefereed, extensively AI-assisted disclosure; internal AI reviews are not independent human peer review.

## Recommended defensible wording

Suggested title: **A relation-incidence proof of Tohăneanu's low-exponent supersolvability conjecture**.

Suggested priority paragraph: “A version of the relation-incidence proof presented here was recorded in GitHub PR #618 on 4 October 2026. During the publication audit we located Ferudun's 12 October 2026 preprint, which proves the same full conjecture using a related dependency-support count. We acknowledge that result and compare the two arguments. The dated disclosure records are preserved in the verification package; we make no exhaustive claim of first priority or claim about independent development.”

The established all-2 theorem, unique-fourfold TF2 consequence, rank-three classification and modular-pruning mechanisms are prior work. Relative to the pre-October-4 sources actually inspected, the candidate's all-rank forcing of the one-3 cyclic structure was not supplied by a previously located theorem. That is the strongest defensible scoped contribution statement.

## Limits

This is an extensive bounded web/primary-source review, not a complete MathSciNet citation census or an investigation of private/unindexed manuscripts. The author's currently public research list was inspected; it identifies the low-exponent work as an OWR extended abstract and lists no later full-target followup. That absence is weak evidence. Journal theorem numbering for DiPasquale was not independently matched to the paywalled main text; arXiv numbering is explicit. No author or other individual was contacted. Raw scholarly fulltexts and rendered pages remain in the ignored `sources.private/` directory and must not be included in a publication package.
