# PR193 priority and source-status audit

Audit date: 2026-10-15 UTC. Target: immutable submitted HEAD `b9a399eeac816dbb8f0e50e81b498c26e5acef81` of [AlecKriebel/Math PR193](https://github.com/AlecKriebel/Math/pull/193). This audit does not repeat the three independent mathematical audits.

## Verdict

**No earlier four-or-more intersection counterexample to the pure-power, shared-focus claim was located in the primary texts and public records checked. Historical novelty and firstness remain unestablished.** No checked later correction or superseding result removes the published target. This is a bounded literature finding, not a certificate that no such work exists.

The safe mathematical description is an exact counterexample with at least five centers to the published three-center expectation in the crossing-allowed realization setting, with historical priority unconfirmed. Do not describe it as the first counterexample, as a newly introduced family of curves, as human peer-reviewed, as an exact maximum, or as a proper-embedding result.

## Target and overlap threshold

The checked target is an alpha=16 cube realization with six distinct boundary vertices, noncollinear alternating triples, a certified incoming center, and at least five distinct outgoing centers. Crossings are permitted. An earlier legitimate example with **at least four** common solutions of

`|X-B|^alpha - |X-A|^alpha = lambda`,
`|X-C|^alpha - |X-A|^alpha = mu`,

for one alpha>1 and noncollinear foci would already defeat priority for disproving the shared-focus bound. It need not use alpha=16, these data, or five points. Converting such an earlier curve example to the full cube claim would require admissible other boundary vertices and an incoming realization; those are distinct obligations.

The proposed data are A=(0,0), B=(2073/10000,0), C=(4719/10000,64/10000), lambda=27/1250, mu=1. The scalar distance-power construction, algebraic boundary completion, and incoming certificate were searched as mechanisms as well as by title/data.

## Primary target, versions, and corrections

[OWR35/2020](https://ems.press/content/serial-article-files/46871?nt=1), DOI [10.4171/OWR/2020/35](https://doi.org/10.4171/OWR/2020/35), printed p.1785, presents the maximum-three conjecture after its crossing-allowed existence theorem. Its workshop ran 15–21 November 2020. The target is therefore an explicit conjectural count, separate from existence.

The [arXiv record](https://arxiv.org/abs/2003.08941) reports v1 submitted 2020-03-19 16:28:07 UTC and v2 revised 2021-10-04 13:55:18 UTC, with no later version displayed on this audit date. Full PDFs were obtained. V1 Remark3.14 already proposes the bound; v2 Remark4.8 retains it. The v1 PDF's internal title-page date is March7,2022 despite its 2020 version strip; that internal date is not used as dissemination evidence.

The [publisher's full text](https://ems.press/content/serial-article-files/39488), DOI [10.4171/AIHPD/163](https://doi.org/10.4171/AIHPD/163), Ann. Inst. H. Poincaré D10(4),781–817(2023), retains the expectation at Remark4.8, printed p.811. The [current publisher landing page](https://ems.press/journals/aihpd/articles/9465214) lists publication 15February2023; Crossref/Numdam report 14February2023. This one-day catalog discrepancy does not affect the target or any comparison here. The landing page supplies no correction notice, and Crossref returned neither an update-to field nor a correction relation; those absences alone do not exclude an unindexed correction.

The [current HAL record and full text](https://hal.science/hal-02512557) are version2, deposited in2022 and carrying a metadata modification in July2026. The retrieved document contains the dated October2021 manuscript and the same Remark4.8. The newer repository modification date is not evidence of a new mathematical version. The author's [hosted copy](https://www.normalesup.org/~ramassamy/publications/alpha_realizations.pdf) also retains that remark.

A search-result phrase suggesting a correction was checked against the DOI registration: [10.1093/imrn/rnad282](https://doi.org/10.1093/imrn/rnad282) is an erratum to *Components in Meandric Systems and the Infinite Noodle*. It concerns another paper by Thévenin, not this target.

## Closest older overlap: identical powered-distance bisectors

[Ash–Bolker, Generalized Dirichlet tessellations](https://www.cs.umb.edu/~eb/dirichlet/generalizedDT.pdf), Geometriae Dedicata20(1986),209–243, DOI [10.1007/BF00164401](https://doi.org/10.1007/BF00164401), defines weighted comparisons `phi(|X-P|)+w(P)` in equations(1.6)–(1.8). Section5, pp.232–242, studies general increasing phi. Its closing pure-power example phi(t)=t^4 discusses individual-curve critical points and asymptotes; its infinite-component example uses the oscillatory phi(t)=t+k sin(t), k<1. These are prior curve geometry, but the inspected discussion does not exhibit four shared-focus intersections for any pure power t^alpha. Generic **valence** results count cells meeting at one vertex, not the number of vertices shared by a fixed triple. The scanned PDF was OCRed; the decisive pp.241–242 were also visually checked.

[Bourne–Peletier–Roper, Hexagonal patterns in a simplified model for block copolymers](https://arxiv.org/abs/1305.6540), SIAM J. Appl. Math.74(5)(2014),1315–1337, DOI [10.1137/130922732](https://doi.org/10.1137/130922732), Definition4.12 in the author manuscript (published definition preceding Proposition4.4, p.1330), explicitly defines p-power cells using `|X-x_i|^p-w_i`, for p in[1,infinity). Section4.2 proves the optimal-transport representation. The general p part and numerical-results discussion do not supply a four-intersection witness. Its arXiv v2 strip dates to December2013 while a internal title-page date says September2021; neither internal date is needed to establish that the published family predates2020.

[Bourne–Roper, Centroidal power diagrams, Lloyd's algorithm and applications to optimal location problems](https://arxiv.org/abs/1409.2786), SIAM J. Numer. Anal.53(6)(2015),2545–2569, DOI [10.1137/141000993](https://doi.org/10.1137/141000993), Section5, printed p.2568, repeats this general p family and discusses an algorithm extension. Its computation sections concern ordinary squared-distance power cells. The inspected full text provides no fixed-triple four-intersection example.

The exact equivalence is elementary: set p=alpha and weights w_A=0,w_B=lambda,w_C=mu. Equality of the three weighted costs is exactly the two target equations. Consequently, **introducing those bisectors, their nonlinearity, or a connection to weighted Voronoi cells cannot be claimed as new here**. Neither nonconvex cells nor arbitrary-phi pathologies imply the required pure-power count without a further argument. Such an implication would transfer the central difficulty to an unsupported claim and is not used.

## Backward and forward citation checks

The target's actual reference list was extracted from the full text; Crossref supplies no reference list. The direct geometric backward leads [Lucarelli–Saksena–Farrell–Wang2008](https://www.cs.jhu.edu/~ijwang/pub/lucarellietalEWSN.pdf), DOI [10.1007/978-3-540-77690-1_4](https://doi.org/10.1007/978-3-540-77690-1_4), Section2, and [Xu–Sahni–Rao2008](https://www.cise.ufl.edu/~sahni/papers/properties.pdf), Theorems6–7, concern ordinary distance differences, alpha=1. The former discusses up to four intersections of **full conics** before enforcing the measured branch, which leaves at most two. It is not a prior alpha>1 counterexample.

The following potentially pertinent later primary full texts were retrieved and searched, and the actual citation/definition contexts were read:

- [Melotti–Ramassamy–Thévenin2022, Points and lines configurations](https://www.normalesup.org/~ramassamy/publications/points_lines.pdf): its target citation motivates a degeneration of alpha=1 hyperbola configurations to perpendicular bisectors, not a powered-distance count.
- [Affolter2024, Möbius invariant Y-systems](https://arxiv.org/abs/2312.07367), DOI10.1093/imrn/rnae237: the target citation is in Remark10.5, p.26, about s-embedding cube flips and recurrences. No general-alpha count is supplied there.
- [Affolter2023 thesis](https://arxiv.org/abs/2305.02212), Section10.3: Lemma10.41 and nearby discussion use proper s-embeddings and Miquel moves. This is another source mentioning the target that a single forward index did not reveal.
- [Affolter–de Tilière–Melotti2023/2024 dSKP I](https://arxiv.org/abs/2208.00239) and [II](https://arxiv.org/abs/2208.00244), plus [Affolter–George–Glick–Ramassamy2026](https://arxiv.org/abs/2601.08944): inspected main-result/definition contexts concern other circle/projective systems, with no located target powered-distance count.
- [Affolter et al., Discrete Lorentz surfaces and s-embeddings I](https://arxiv.org/abs/2410.11575): full-text search/main setting concerns s-embeddings and Lorentz geometry; the search lead did not supply an alpha>1 multiplicity result.

The current [Melotti research list](https://www.imo.universite-paris-saclay.fr/~paul.melotti/recherche.html), [Ramassamy publication list](https://www.normalesup.org/~ramassamy/publications/publications.html.en), and [Thévenin publication list](https://www.normalesup.org/~thevenin/publication.html) were inspected, including listed work through2025/2026. Ramassamy's [45-slide March2021 talk](https://www.normalesup.org/~ramassamy/documents/alpha_embeddings.pdf) states existence/nonuniqueness but does not give a four-center example. No assertion about unpublished author knowledge follows.

OpenAlex current work W3012709382 exposed one forward citing paper. The independently found 2022 paper and 2023 thesis demonstrate that this is not an exhaustive citation census. Semantic Scholar's API returned429; a complete subscription-index citation audit was not available. Broad equation, generalized-hyperbola, powered-distance Voronoi, and multilateration searches were also run; materially relevant leads are above. The query matrix records bounded searches rather than treating irrelevant results or no hits as a proof of absence.

## Repositories, Zenodo, and dissemination chronology

The current public GitHub API reports [PR193](https://github.com/AlecKriebel/Math/pull/193) created_at `2026-10-01T04:37:32Z`, open, with submitted head b9a399e. Both the [first commit's candidate](https://github.com/AlecKriebel/Math/blob/e6a4a9ca2c6fe34d73142573fbf9e605b9a4c585/unsolved_math_prioritization/attempts/30004563/CANDIDATE.md) and the [submitted head's candidate](https://github.com/AlecKriebel/Math/blob/b9a399eeac816dbb8f0e50e81b498c26e5acef81/unsolved_math_prioritization/attempts/30004563/CANDIDATE.md) are currently publicly retrievable and byte-identical to the frozen original, SHA256 `293f5ad9475b4a8d045121b2eccecbcf0d4937df3077e9bb430c7f9056e12f51`.

This records author dissemination and GitHub's current chronology. Commit author/committer dates can be set by authors. Current raw retrieval is not a contemporaneous archive attestation of when every file first became publicly visible. Neither the repository nor its AI audit files establish external human review, third-party awareness, independence from unknown work, or first discovery.

Public Zenodo API exact phrase/identifier searches returned no target for alpha-realizations,30004563, or p-power diagrams; cube moves returned an unrelated Rubik's-cube record. DataCite title search recovered the original arXiv DOI; the broad alpha-realizations query also returned unrelated alpha-sigma material. GitHub repository/issue searches were bounded and noisy, with no authenticated global code search. An indexed EulerSolve papers page was searched for the target terms; no directly relevant entry was identified, and its direct HTML retrieval returned403. No absence conclusion is drawn. The parent supplied no existing PR193 DOI; none was created here.

## Open status and remaining gaps

1. **Source status:** the latest checked primary target texts still present the three-bound as an expectation/conjecture. No later resolution was located in this corpus.
2. **Mathematical status:** the separate audits supply a valid counterexample to that bound. Once that argument is accepted, the bound is false regardless of priority. Calling it simply “still open” would ignore the currently public candidate.
3. **Historical status:** novelty is unestablished; no earlier >=4 witness has been located. Unindexed papers, source repositories, talks, theses in other languages, private work, and incomplete citation databases remain possible gaps. No unsupported percentage probability of firstness is assigned.
4. **Unresolved mathematical questions:** the exact maximum and proper-embedding multiplicity are outside this result. The arbitrary-phi and alpha=1 literature does not settle them.

Completion of this **bounded priority audit**:100%. Completion of a proof of historical firstness:unestablished and not quantified. There is no evidentiary basis for unconditional novelty clearance. A further independent bibliography review could improve confidence; no outreach was prepared or initiated.

## Artifact boundary

`SOURCE_EVIDENCE_MATRIX.json` and `QUERY_SOURCE_MATRIX.json` distinguish exact claims, access, checked sections, overlap, and unresolved gaps. Download manifests and `PRIVATE_SOURCE_HASHES.json` record retrieval reproducibility. `DISSEMINATION_EVIDENCE.json` records the public-byte comparisons. Only `SAFE_INTEGRATION_ALLOWLIST.json` entries may be integrated. Source PDFs, OCR, text extractions, renders, raw HTML/API responses, and downloaded public candidate copies remain excluded in `private_sources/`. No Git/ref/index/PR/shared-file edits, publication, metadata/service writes, or external communications were performed.
