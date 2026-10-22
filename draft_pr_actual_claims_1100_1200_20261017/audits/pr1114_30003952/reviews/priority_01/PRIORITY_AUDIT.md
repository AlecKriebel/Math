# Priority audit: PR 1114 / problem 30003952

Frozen head: `e1a11feef98ed0fde22375c983e30b72b268d265`.
Audit started 2026-10-17 17:54:59 UTC. Independent historical/direct-consequence review only. No external contact, PR mutation, commits, pushes, publication, or subagents.

**Verdict: SKIP_ALREADY_SOLVED / PRIOR_FULL_CONSEQUENCE. A preprint framed as a NEW full resolution is not justified.** The exact pinned theorem is a direct consequence of an earlier smooth realization construction and classical covering geometry. This is a positive mathematical implication, not an inference from an unsuccessful literature search or the manuscript's generic novelty disclaimer.

The complete checkable chain is in DIRECT_IMPLICATION_PROOF.md. There is no remaining mathematical gap in that implication within the pinned oriented-surface interpretation.

## Exact claim and success criterion

The target is a prescribed pair of essential curves meeting once on any oriented smooth surface, including negative Euler characteristic: actual C-infinity maps A,B and their inverses, prescribed right-twist classes, exact ABA=BAB, compact support in any sufficiently small compact regular neighborhood, and identity on its boundary collar.

For priority failure it suffices to derive all these features from public work preceding the current claim. It is not necessary to find a later paper explicitly saying that A'Campo's printed question has been answered. Conversely, a bare B3 action, a torus homology representation, or a high-strand obstruction does not suffice.

## Strongest verified finding

The prior input and its dates are itemized in the implication proof and SOURCE_LEDGER.json. The mathematical deductions establish all of the following.

| Issue tested | Verified mechanism |
| --- | --- |
| Odd three-point cover | Mod-two meridian character; connected boundary; chi=-1; genus one, one boundary |
| Existence and uniqueness of actual lifts | All meridians have the same mod-two monodromy; exactly one lift fixes the lifted external collar |
| Exact group relation | Normalized lifting is a homomorphism on the actual maps |
| Smooth branch points | In w^2 charts, a translated base germ lifts to w or -w |
| Smooth inverses | The inverse has the same local linear form |
| Prescribed twists | Local two-point annulus quotient, plus lifted relative-boundary isotopy |
| Correct handedness | Choose the same sign of half twists, or simultaneously invert |
| No unknown center term | Generator classes identified before capping; full-twist square, not full twist, is the boundary twist |
| Arbitrary prescribed surface | Oriented neighborhood identification and extension by identity on an open collar |
| Small support and original boundary/marks | Compact interior support transports into any chosen sufficiently small neighborhood disjoint from those features |
| Ambient relations | Only the stated B3 homomorphism is realized; no unproved descent through extra ambient relations |

These are the strongest verified results relevant to the user's selection criterion. Mathematical validity of the manuscript's different construction is compatible with this priority failure.

## Sources and version comparison

The original OWR Problem 9 is at printed p.2527, physical PDF p.53; its workshop dates are 2–8 September 2018. It asks for the two prescribed right-twist representatives satisfying the braid relation at homeomorphism, C1, and Cr levels. The exact target matches the pinned theorem on the accepted oriented-surface interpretation.

The [arXiv history](https://arxiv.org/abs/1802.00490) records the first posting at 2018-02-01 21:20:30 UTC. Both the [original v1 body](https://arxiv.org/pdf/1802.00490v1) and the [Mann author body](https://pi.math.cornell.edu/~mann/papers/RealizationProblems.pdf) were freshly inspected. The [coauthor's publication record](https://bena-tshishiku.github.io/publication/nielsen-survey) identifies the chapter as Proc. Sympos. Pure Math. 102 (2019), 131–156. Its linked proceedings-formatted author PDF was inspected at the corresponding theorem and proof. Crossref's DOI metadata gives the print publication date 2019-06-27.

The relevant theorem and local construction are present in all three inspected bodies. Page numbering differs: 18–19 in the two 23-page versions, 19–20 in the 25-page proceedings-formatted author version. No relevant change was found. The latter PDF metadata says 2018-08-31, but PDF creation metadata is not treated as proof of a public dissemination date.

Direct AMS publisher/DOI body retrieval was attempted repeatedly and returned HTTP403/tool access errors. Thus this audit does not assert publisher-byte inspection or exact final-publication textual identity. That retrieval limitation does not affect the priority certificate, which is already established from the dated arXiv v1.

Farb–Margalit's pre-2018 chapter explicitly includes the odd branch count and the three-branch/one-boundary example. Its annulus and center correspondence was inspected, not inferred from Theorem 4.2's even branch count. The implication proof includes the necessary local calculation directly.

## Earlier and later trails checked

The published [Salter–Tshishiku author paper](https://nsalter.science.nd.edu/research/braidsdiffeo.pdf), Remark1.3 and bibliography, credits Thurston's 2011 observation and points to his [15–16 February 2011 MathOverflow comments](https://mathoverflow.net/questions/55555/realizing-braid-group-by-homeomorphisms). Those comments were inspected as primary author commentary. They support an earlier homeomorphism lineage; they are not needed to certify the smooth result.

The [2010 OWR report](https://ems.press/content/serial-article-files/46312), printed p.3151, Problem8, contains an older related question about small subgroups generated by a twist pair. It was inspected and kept distinct from the exact 2018 map-relation wording.

The published [Chen 2019 paper](https://msp.org/gt/2019/23-7/gt-v23-n7-p11-p.pdf) concerns n>=6 obstructions and cites the prior smooth-realization survey. Its theorem/intro, reference trail, and publication information were inspected. It neither supplies a contrary obstruction for B3 nor a missing novelty condition. The 2021 Birman–Hilden survey's primary publisher text was also inspected for the standard lift correspondence.

Exact-name, problem-number, equation, prescribed-twist, low-genus, smooth-section, and citation-trail queries are recorded separately. No primary source explicitly framed as a later solution to the identical 2018 question was located in this bounded audit. That negative search finding is not an openness claim and plays no role in the proven priority verdict.

## Novelty and disposition

No strictly stronger new mathematical claim remains in the pinned theorem. Smoothness, smooth inverse, arbitrary prescribed pair, arbitrarily small regular-neighborhood support, collar identity, and marked/punctured cases are all consequences of the older input.

The pinned proof uses a direct torus/cutoff route rather than the smooth branched lift described here. It may be a distinct exposition or proof. This audit has not established that the method itself is historically new, nor that it offers a research contribution independently suitable for a preprint. Explicit radii, a self-contained implementation of known mechanisms, or a clearer central-offset check do not convert an already implied theorem into a new resolution.

Under the user's strict instruction to skip already solved outcomes, remove this candidate from the new-open-problem-preprint stream. Preserve the proof and audit as attributed research notes if desired. Recommended status wording: “Complete independent construction; full stated conclusion follows from prior work; excluded from novel-resolution selection.” If a future expository manuscript is separately authorized, attribute the smooth input to Mann–Tshishiku and the covering correspondence to Birman–Hilden/Farb–Margalit; state that it is an exposition/new proof of a consequence, and do not claim a new resolution of an open problem.

No unsupported stronger problem should be introduced to rescue eligibility. Requiring a section of a particular ambient image or a new analytic/symplectic constraint would be a different task with its own known obstructions and would need a new exact claim and validation.

## Limits and operational record

This is an independent mathematical priority audit, not an exhaustive worldwide bibliography certification. It uses only public primary source bodies and directly checked calculations for the decisive result. No person was contacted. No external action or publication was performed. Disk exhaustion temporarily rejected a small ledger rewrite; the original valid source ledger survived, and complete artifact text was retained in tool memory for fallback delivery.

