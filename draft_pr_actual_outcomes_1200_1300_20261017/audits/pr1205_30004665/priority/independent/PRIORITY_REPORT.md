# Independent priority audit of PR #1205 / problem 30004665

Audit date: 2026-10-17, America/Los_Angeles. This is a bounded, independent literature and provenance audit, not a proof of novelty. No individuals were contacted, no author programs were executed, and no publication or PR mutation was performed.

## Decision

The original OWR2021 canonical-W converse is false, assuming the independently checked canonical-potential reconstruction and separation certificates in the mathematical gate. The literature audit found no earlier **explicit statement** of this refutation. It did, however, find a substantial and previously missing priority fact: **the exact reduced word and its complete 22-term string-coordinate support already occur in primary-author public computational data committed on 6 March 2020**. Those data, transported through the established chamber map, give exactly the canonical support used in this PR, including both squared monomials.

Consequently a paper must not claim discovery of this reduced word, this support, or the first counterexample without qualification. A concise **corrective and independently verified note** is defensible if it attributes the old data, explicitly identifies the historical 2021 formulation, gives the canonical calculation and exact nonredundancy certificates, and states that no priority or current-openness claim is established. The evidence does not justify the categorical disposition “an explicit refutation was already published”; neither does it justify “we newly solve a problem that remained open in October 2026.”

The mathematical negative answer and the originality of recognizing that answer are separate questions. This audit clears the former only through the parent mathematical gate. It does not clear an unconditional novel-resolution narrative.

## Exact earlier data: a positive priority finding

The repository cited by Koshevoy–Mironov's subsequent computational work is [mironovd/crystal](https://github.com/mironovd/crystal). Its [file history](https://api.github.com/repos/mironovd/crystal/commits?path=crystal_D_4.out.xz&per_page=100) attributes `crystal_D_4.out.xz` to commit [`0d6e564cf5e69d79c1074d5d1e3e72ac700904d6`](https://github.com/mironovd/crystal/commit/0d6e564cf5e69d79c1074d5d1e3e72ac700904d6), Git committer date 2020-03-06T15:08:29Z. The [pinned compressed data](https://raw.githubusercontent.com/mironovd/crystal/0d6e564cf5e69d79c1074d5d1e3e72ac700904d6/crystal_D_4.out.xz) are byte-identical to the current file at repository commit `1fc6481a835fdfdf65763c15a46be9403cb9a961`. Git dates are provenance evidence, not an independently timestamped proof of the exact date a server made a commit public. The later 2022–2023 primary publications explicitly point to this repository, which establishes an independent public citation trail before this PR.

Case 267 uses exactly

`(1,2,3,2,4,2,1,2,3,2,4,2)`.

It lists 14, 1, 5, and 2 monomials for simple roots 1, 2, 3, and 4. `compare_prior_data.py` parses that historical output as inert syntax, constructs the reciprocal chamber matrix directly from the word, and solves its triangular integer system. The resulting canonical supports include

`y_2 y_3 y_4 y_5 y_6^2 y_7 y_8 y_10`

and that monomial multiplied by `y_1`. The entire 22-term transformed support agrees with the parent's independently checked support. See `PRIOR_DATA_COMPARISON.json` for all rows and `RETRIEVALS.json` for bytes and SHA256 digests.

The old output records **support**, not coefficient multiplicities, facet certificates, or an explicit contradiction of the later OWR conjecture. Those are limits on what can be credited to the data alone. Nevertheless the construction is present, and claiming it as newly discovered would omit material prior art.

## Historical formulations and the inferential boundary

1. [OWR20/2021](https://ems.press/content/serial-article-files/46898), Schumann's report, printed pp.1123–1125, ends with an equivalence formulated using W in its designated dual cluster torus. Printed p.1125 was visually checked. This is a genuine canonical-coordinate assertion; the PR addresses its necessary direction. The same page already announces nonredundancy for minuscule summands.

2. [OWR52/2021](https://ems.press/content/serial-article-files/46930), printed pp.2882–2883, retains the canonical-W sufficient criterion. Its final conjecture concerns coefficients instead of repeating the canonical-W exponent converse. The literal printed coefficient inequality on p.2883 is “less or equal to 1”; this conflicts with the later published convention and is not silently corrected here. The report does **not** explicitly say that the earlier canonical-W converse has been disproved. Omission or changed wording alone is not a published refutation, withdrawal, or evidence of the authors' private knowledge.

3. [Koshevoy–Schumann 2022](https://doi.org/10.1007/s10801-022-01144-z), published pp.1031–1053, Definition4/Conjecture3 concern the chamber pullback varsigma, while Definition10 concerns canonical W. The p.1046 proof of Theorem2 asserts equivalence of the two exponent bounds by a monomial torus map. The current example contradicts that asserted equivalence, but its varsigma satisfies the exponent bound. Theorem6 already supplies minuscule nonredundancy; the source's D4 central example on p.1050 uses a different word and has a redundant term. The candidate is not that published redundancy example. The old arXiv word discrepancy is already corrected in the publisher PDF and supplies no new correction claim. The arXiv abstract currently lists only v1 (29 September 2021); the current publisher PDF has the same digest as the submitted provenance copy. Crossref returns no correction relation, and targeted searches found no separate erratum. These are bounded checks, not proof that no correction exists.

Combining the historical support with the announced minuscule theorem and the one-monomial central summand makes an earlier deduction of nonredundancy available. In particular, the canonical-W failure cannot be promoted as independent of prior minuscule work. One must also avoid circularly using the false exponent-equivalence assertion to prove the canonical exponent bound. The current integer certificates are useful precisely because they independently establish nonredundancy for the specific example.

The elementary fact that arbitrary monomial coordinate changes alter coordinatewise exponent bounds is insufficient by itself: such a change need not be another designated reduced-word cluster chart. The verified candidate uses the actual canonical reduced-word seed. The prior-data comparison likewise uses the established chamber map, not an arbitrary reparameterization invented to create a square.

## Later work and citation trails checked

- [Labardini-Fragoso–Schumann, arXiv2208.00028v2](https://arxiv.org/abs/2208.00028v2), revised 10 October2022, Sections7.3–7.5: identifies potentials with projective-representation F-polynomials, gives the chamber map and a Newton-vertex description, and cites the known canonical sufficient criterion. No explicit refutation of the original exponent converse was found in the inspected passages or global text searches. Its [2024 publisher record](https://ems.press/journals/jca/articles/14298117) was inspected; the final paper requires a subscription and its full text was **not** obtained. The arXiv v2 is not represented as a complete audit of the later final version.
- [Koshevoy–Mironov, EasyChair8975](https://easychair.org/publications/preprint/z55N/open), dated 3 October2022, targeted printed pp.1–3 and6–7 of its seven-page mathematical text: gives computational methods and a different empty-interior Newton-polytope conjecture. [2023 slides](https://pca-pdmi.ru/2023/files/51/F-poly-Newton%283%29.pdf), especially pp.17–19 and29–30, report D4 computations and cite the public repository. Such computations make the overlap with old data important; an absence of interior lattice points is not the statement that every support point is a vertex.
- [Koshevoy–Mironov 2024 slides](https://pca-pdmi.ru/2024/files/30/coefficients-pre2.pdf), especially pp.17–24, discuss coefficient computation and its relation to redundant inequalities. They supply neither this explicit canonical-W refutation nor a license to identify the original converse with a coefficient criterion.
- [Kanakubo–Koshevoy–Nakashima, arXiv2109.01997](https://arxiv.org/abs/2109.01997), Example5.4, and [arXiv2207.08065](https://arxiv.org/abs/2207.08065), Example4.6: distinct D4 words and algorithms. The exact candidate does occur in the linked earlier data, as above.
- The direct citation lists differ: Springer/Dimensions displays2, Semantic Scholar returns4, and the OpenAlex DOI record returns1. All four Semantic Scholar leads were followed. Besides the two computational/representation papers above, [Special Kirillov–Reshetikhin crystals, arXiv2608.27949](https://arxiv.org/abs/2608.27949), §3.3, cites KS22 for background; [Lifting holomorphic disks..., arXiv2608.15571](https://arxiv.org/abs/2608.15571) has a background citation. Targeted text inspection found no converse refutation in either. Citation-database counts are incomplete indexes, not an exhaustive forward citation search.

## Remaining gap and publication conditions

The strongest priority conclusion is: **an independently certified explicit counterexample to the historical canonical-W converse, using a reduced word and support already present in prior primary-author computational data; no earlier explicit refutation located within the audited sources.**

The remaining gap is whether another publication, an inaccessible final revision, an unindexed source, or the original authors' other work already explicitly made this deduction or corrected the exponent equivalence. Negative keyword searches cannot close that gap. The de Laporte author page was available through the web index but its direct retrieval returned404, and Zenodo's record API rejected unauthenticated searches (400/403); neither is counted as a completed exhaustive author-publication search. Exact-author/topic web searches did not find an earlier AlecKriebel preprint of this result.

Before publication, globally add the old dataset and minuscule attribution to the manuscript, abstract, README, source provenance, metadata description, and verification narrative. Describe the result as a correction to a specified historical formulation, avoid firstness/current-openness claims, and distinguish the later varsigma and coefficient conjectures. Do not label an internal AI audit as external peer review. The old data, fetched PDFs, and source screenshots in `sources/` are local audit inputs, not proposed attachments to the preprint; the public source repository declares no license, so link and attribute it instead of redistributing its files.

Completion estimate for this bounded audit: **100%**. Completion estimate for an unconditional novelty/first-resolution claim: **not established**.
