# Modern-mechanism priority audit — PR152 / problem 5000006

Audit performed 2026-10-11 America/Los_Angeles (2026-10-12 UTC). Scope: modern 2021–audit-date mechanisms and public author releases that could already establish Fuchs Conjecture 2.7. This is one independent priority family, not a whole-package R1/R2 or a publication decision.

**Bounded finding: documented exact public target coverage exists as of this audit. Historical priority and independence remain unresolved.** Alper Ferudun's October 9, 2026 unrefereed preprint contains an explicit all-`n≥4` labelled theorem and a target-specific proof. The project's original September 30 PR predates that release; today's chart-sign repair follows it. DOI chronology alone therefore does not decide originality. No claim of copying, derivation or independent discovery follows from this audit.

## Target and success criterion

The comparison target is the repaired CANDIDATE.md: for regular `n≥3`, a short trajectory ends at the first subsequent vertex and has the parity-sensitive Fuchs type `A_k`, `k mod(n−2)`. The sine weight uses `k=0,…,n−3`. Parallelism is the source's dihedral direction relation, not merely a common unfolded slope. Full coverage requires the actual `A_k`-to-length correspondence for every parallel family, including double **even** polygons and boundary sides. A common unlabelled sine spectrum, a theorem about closed cylinder circumferences, or only `n=5` fails this criterion.

Read before searches: repaired candidate and original SOURCE_AUDIT.md. Did not read sibling priority conclusions. Later read the frozen original candidate solely for the requested chart comparison. Parent supplied the original PR timestamps and head; these are identified as parent-verified evidence below.

## Exact modern coverage: Ferudun 2026

Primary sources: [author release](https://eulersolve.org/papers/amr-049/), [canonical PDF](https://eulersolve.org/papers/amr-049/paper.pdf?v=ff6b9ba5f9ba), [metadata](https://eulersolve.org/papers/amr-049/metadata.json?v=0973f794ce32), [DataCite DOI record](https://api.datacite.org/dois/10.5281/zenodo.23267641). PDF: 41 pages; SHA-256 `ff6b9ba5f9bac0027a39d6e06319f04ff08bf24776a47cf7070213924d454707`, matching the author's metadata.

Theorem C (printed p.5) states the exact sine ratio for Fuchs-labelled parallel short trajectories for every `n≥4`. Its proof is on printed p.17. Definitions retain segment parity, first-vertex stopping, sides, canonical representatives and the broader source parallelism. The n=3 case is outside that theorem's stated range and is the elementary one-type triangular-lattice case; no nontrivial general-n range is omitted.

The target chain in §§2–3, printed pp.9–17, was inspected rather than inferred from the abstract. It constructs the double n-gon for even as well as odd n, a reduced angular coordinate B, and K from the two endpoint germs. Explicit uniform twists and polygon symmetries preserve K; shortening descent reaches a polygon chord. The same derivative scales every connection in a fixed direction. Chord lengths and labels then yield the theorem. It does not need the candidate's imported cusp theorem or hyperelliptic uniqueness route.

**Focused validity assessment:** no central unsupported claim in this target chain was identified. The actual label equation, twist construction, finiteness/descent mechanism and common-factor argument were checked at the level needed to discriminate exact coverage from an unsupported abstract. This is not a full independent adversarial validation of every theorem or computational artifact in the seven-conjecture package.

## Independent comparison with the repaired index

The repaired candidate defines the intrinsic index as `K=2m+1` for odd n and `K=2m+1−e` for even n. It distinguishes intrinsic K from the physical folding-chart label `k=σK`; their sine weights coincide. The frozen original candidate instead overstates chart-independent physical label invariance.

Here is the direct mathematical identification, using the two constructions:

1. For a same-endpoint connection, the two outgoing endpoint germs differ by `π+2πm`. Dividing the reduced B-difference by π gives `1+2m` modulo n−2.
2. For different endpoints on an even double polygon, transport the backward germ by the polygon-exchanging half-turn. Its angular separation is `2πm`; B is unchanged by that half-turn. Thus the B-difference gives `2m=2m+1−e`.
3. At a physical P start, both correspondences give the source k. Reflecting the initial folding chart changes the source label by a sign, while intrinsic K is retained by the half-turn. Because the canonical sine weight is invariant under k↦−k, this does not alter the ratio theorem.

Consequently the two intrinsic mechanisms agree. The published source's P0-start label lemma does **not** assert that every Q-start physical fold has label K. Its argument normalizes saddle connections intrinsically, then evaluates the common length factor; it need not identify each intermediate affine image with a physical trajectory carrying the same k. This avoids the original candidate's chart conflation. The repair is a precise correction of that project's wording, but a separate claim that the repaired target is absent from the October 9 literature would be false.

Mechanism overlap is strong: double polygon; endpoint-germ angular index; invariant weights; reduction of one entire direction to chords; common affine scaling; dihedral alignment. A material distinction is the reduction mechanism: explicit uniform twists plus finite shortening descent in the external source, versus classical lattice/cusp input and all-affine hyperelliptic commutation in the candidate. No priority or derivation conclusion is inferred from shared mathematics.

## Chronology and provenance

| Event | Evidence and interpretation |
| --- | --- |
| Original project PR152: 2026-09-30T12:11:38Z; updated 12:19:32Z; head 99ef28d28bf380658400886d1f8c2120a5096d97 | Parent verified GitHub PR.response.json; frozen original candidate states the all-n ratio and cone/hyperelliptic/cusp route. This precedes the external DOI. |
| External manuscript/release: 2026-10-09, version 1.0 | Author landing page and metadata specify this date and first public online release. Current PDF matches the metadata's named hash. |
| DOI created: 2026-10-09T17:25:40Z; registered 17:25:41Z; Issued date 2026-10-09 | Independently retrieved primary DataCite record for 10.5281/zenodo.23267641 matches title and author. |
| Project chart-sign repair: 2026-10-12 UTC | Parent's active repaired snapshot and instruction; later than the external source. This audit does not backdate today's correction to September 30. |
| This audit's live retrieval: beginning 2026-10-12T00:04:30Z | Retrievable author PDF and metadata plus registry data establish current public availability. |

Zenodo's landing page could not be read through the web tool and its API returned HTTP 403. The **DOI-archived PDF bytes have therefore not been compared** with the live author PDF. The metadata's hash and matching live PDF, coupled to DataCite's date, provide substantial but bounded release evidence. Earlier drafts, author release history, the project's complete pre-repair public record, and discovery independence were not established here. The parent owns the definitive cross-family priority synthesis. This audit supports neither an unconditional originality certificate nor automatic rejection of the earlier project claim.

## Other materially relevant modern sources

All following full PDFs were accessible and cached. Specific portions were inspected; availability of a full text is not a claim that every proof was read.

| Primary source and inspected material | Exact overlap and remaining target gap |
| --- | --- |
| [McMullen, Billiards in regular polygons](https://ems.press/journals/lem/articles/14299155), published PDF §§2,4,5,7 and Appendix A; author PDF also inspected | Theorem 4.1/Corollary 4.3 simultaneously reduce Weierstrass/midpoint geodesics and give a common direction factor. Prime-only vertex-connection length remark compares a midpoint vertex connection to an adjacent closed trajectory. These are not all Fuchs endpoint-angle labels; even n uses the smaller opposite-side surface. No complete A_k correspondence found in the inspected target-relevant material. Publisher and Crossref say online September 24, 2025, although the volume is 72 (2026). |
| [Lee, 2609.24587](https://arxiv.org/abs/2609.24587), September 21, 2026; Theorem 1.1, §1.2, §§2,5 | Classification of algebraically primitive hyperelliptic two-zero curves, with cusp circumference/height and sine relations. It does not identify Fuchs labels of parallel first-vertex trajectories; it is restricted to algebraically primitive curve classes. |
| [Lee, 2609.26903](https://arxiv.org/abs/2609.26903), September 22, 2026; Theorem 1.1, cusp setup, §§4–5 | Classifies minimal-stratum primitive curve families including prime odd double polygons and selected 4g-gons. No full target-label map or double-even-cover all-n conclusion. Broad classification is not target coverage. |
| [Boulanger, 2309.17165](https://arxiv.org/abs/2309.17165), September 29, 2023; §§1,2.2,4.1–4.2 | Staircase saddle lengths are trigonometric and affine intersection ratios are invariant. The goal is KVol/intersection bounds on even regular quotient surfaces, not Fuchs-labelled same-direction length ratios. |
| [Boulanger, 2509.05210v2](https://arxiv.org/abs/2509.05210), first September 5, 2025, revised January 27, 2026; §§1–2,3.1–3.2 | Multiple-singularity length estimates use four classes: sides, a specified dihedral family, connections in a large cylinder, and the remainder. These classes differ from A_k; bounds depend on segment subdivisions rather than the target sine ratio. |
| [Berman et al., 2109.04495v2](https://arxiv.org/abs/2109.04495), 2021 preprint, 2022 revision, DCDS 2023; §§1–3 and full keyword inspection | Computes slope-gap statistics via shortest cusp vectors and return times. Direction/cusp and holonomy descriptions are relevant background; no Fuchs A_k endpoint-germ correspondence is supplied in the inspected material. |
| [Boulanger, Connection points on double regular polygons](https://arxiv.org/abs/2501.14657), January 24, 2025; §§1–2 and §5 theorem context | Studies which nonsingular points lie on extendible separatrices for odd n≥7. Arithmetic cusp obstructions concern whether a direction is periodic, not labels or relative lengths within a parallel family. |
| [Apisa–Saavedra–Zhang, 2011.02668](https://arxiv.org/abs/2011.02668), November 2020 preprint, Geom. Dedicata 2022; theorem, §2 and Corollary 2.8 | Periodic-point classification and centrality of the hyperelliptic involution are close background. Family is even regular quotient/odd double; no Fuchs label-to-weight correspondence. Publication after 2021 does not erase its pre-2021 provenance. |
| [Davis–Lelièvre, 1810.11310v2](https://arxiv.org/abs/1810.11310), July 23, 2024 revision; §§1,2.2–2.3 and relevant §3 statements | Two saddle-connection lengths in golden ratio and explicit pentagon renormalization. This is n=5 only and uses other path/cylinder labels. It cannot establish the full all-n target. |

Pre-2021 cutting-sequence sources were recovered by modern queries but are outside this family's main remit. Their bi-infinite coding or sandwiched-letter derivation statements cannot be promoted to the finite endpoint-type theorem without an additional label-preservation proof. These leads were not counted as modern exact target coverage.

## Access and inference limits

Searches covered alternate target mechanisms and terminology, arXiv windows, recent publisher releases and author releases. Exact-name broad search and classical history belong to other independent families. No absence certificate is claimed for unindexed sites, languages, unpublished manuscripts or later revisions.

Strongest verified finding: the publicly retrievable October 9 preprint contains the exact all-n≥4 target, actual parity-sensitive labels and a checkable distinct proof mechanism; registry chronology places its DOI after the frozen original project claim and before today's repaired snapshot. Exact remaining gap: comparative priority/provenance of the two mathematical snapshots, including immutable source-byte confirmation and discovery independence. No external contact, outreach draft, Git write, global edit or publication was performed.

Artifacts: RESULT.json; RESEARCH_LOG.md with audit-completion percentages; SEARCH_INVENTORY.md; SOURCE_INVENTORY.json with retrieval timestamps/hashes/errors; private_pdf_cache for verification only.

