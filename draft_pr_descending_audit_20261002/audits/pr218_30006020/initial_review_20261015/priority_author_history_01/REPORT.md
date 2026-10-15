# PR218 / 30006020: independent author-history priority audit

Audit date: 2026-10-15 UTC. Lane: author publication/preprint history, public followups, and selected citing papers. This report was written without reading root or sibling priority conclusions or inherited reviews. It is a priority audit, not a repetition of the separately passed mathematical/source gate.

## Finding

**The searched public primary material does not supply a verified prior theorem with the candidate's full total-variation model or its every-mesoscopic-scale conclusion. Priority remains unresolved.** In particular, the named Delecroix–Liu small-components project is a concrete undischarged lead. Missing search results or author-list entries cannot show that its methods or unposted manuscript do not already include the candidate's conclusions.

There is substantial positive prior coverage that must be credited: the macroscopic law and stable-graph/composition machinery are old; the microscopic Poisson intensity and generalized Ewens weights were publicly displayed in Liu's 2022 thesis; and OWR states a microscopic result while posing the intermediate-area problem. The candidate must not present the microscopic mechanism, the weights, or the Poisson intuition as newly discovered.

## Exact target used for comparison

The frozen candidate concerns the principal holomorphic quadratic stratum Q(1^(4g−4)), first N→∞ at fixed g, then g→∞, unbounded heights, maximal horizontal cylinders each counted once, and areas divided by total surface area. Its proposed additions are:

- A whole-multiset TV approximation by positive compositions of n=3g−3 with weights a_j=ζ(2j)/(2j), followed by Dirichlet parameters (2j_i).
- For **every** s_g→0 with g s_g→∞, the rescaled area point process tends to PPP(dx/(2x)), with all fixed joint count moments.
- For [g^(−1/2),2g^(−1/2)], Poisson mean (log 2)/2, including expectation and variance limits.

A fixed microscopic window, a density's large-x asymptotic, weak macroscopic convergence, or a PPP in a different ensemble does not by itself match those assertions. The necessary missing ingredient in such a comparison is control that is uniform when the window grows in microscopic coordinates, together with the claimed moment transfer.

## Chronology and editions

| Primary record | Verified chronology and relevance |
|---|---|
| [DL arXiv record](https://arxiv.org/abs/2202.10255) | Only v1 is listed: 21 February 2022, 14:20:52 UTC. The full v1 was freshly retrieved, not inferred from its abstract. |
| [DL publisher record](https://ems.press/journals/jems/articles/14297869) | Submitted 4 March 2022; accepted 26 February 2024; published 7 June 2024. Final citation: JEMS 27(12) (2025), 5093–5131, DOI 10.4171/JEMS/1469. Online-first and final PDFs are distinct files; both were read for the introduction's announcement. |
| [DGZZ arXiv record](https://arxiv.org/abs/2007.04740) | v1: 9 July 2020; v2: 5 July 2022. Publisher-version PDF and DOI 10.1007/s00222-022-01123-y agree on the identity. Online publication: 20 June 2022. |
| [Liu thesis](https://www.imj-prg.fr/theses/pdf/mingkun_liu.pdf) | Title page: defense 27 September 2022. Official IMJ host; retrieved HTTP Last-Modified 14 November 2022. That header is a file-history clue, not proof of first public availability. |
| [OWR report](https://doi.org/10.4171/owr/2024/41) | Workshop: 8–13 September 2024. Report number 41/2024. DOI registry publication date: 14 February 2025. Report year, workshop date, and publication date must be distinguished. |
| [Durham seminar](https://www.mmagee.net/seminar.html) | Liu talk dated 26 February 2025; the linked [author slides](https://www.math.univ-paris13.fr/~mingkun.liu/talks/Durham.pdf) carry that date and mention joint work with Delecroix. |

The DL final PDF hash matches the frozen manifest: `03b84a6c19a8a9b25ad4c8991157f55247fe75e3297bad310aac7bcc85013a8b`. Its numbering is used below; v1 numbering differs. Crossref records were checked only for bibliographic integrity, not for theorem coverage.

## Evidence matrix from full primary texts

| Source and inspected location | Actual positive coverage | Exact comparison gap |
|---|---|---|
| DL final: Theorems 1.2, 1.4, 3.2, 4.1; §6 and Lemma 6.4 proof; introduction p.5098 | Macroscopic PD(1/2), square-tiled correspondence, explicit graph mixture, reduction to a bounded-loop one-vertex model, and uniform coefficients/monomial machinery. The introduction announces ongoing microscopic Poisson work and absence below g^(−1−ε). | The inspected statements do not assert the candidate's TV comparison to the ideal composition/Dirichlet model or its quantifier over every mesoscopic sequence. They are substantial credited inputs; a new formulation or consequence needs a separate priority judgment. |
| Liu thesis: Remark 1.5.9, equations (1.4)–(1.5), printed/PDF p.22; Chapter 6 main theorem | Announces ongoing Delecroix work with microscopic intensity ρ(x)=e^(−x)/x ∑_(r≥1)(cosh(x/r)−1)=e^(−x)/x ∑_(j≥1)ζ(2j)x^(2j)/(2j)!, and fixed [a/(6g−6),b/(6g−6)] Poisson counts. It explicitly compares generalized Ewens weights ζ(2j)/2, hence cycle masses ζ(2j)/(2j). Chapter 6's main asymptotic theorem is PD(1/2). | The remark is an announcement rather than a supplied microscopic proof. It does not quantify growing a,b or arbitrary s_g. The displayed weights are already prior material. |
| OWR: Theorem 2, Problem 2, reference [5], printed p.2387 / PDF p.19 | States microscopic PPP and macroscopic PD for the principal quadratic law, and explicitly poses the requested √g window. Names *Small components of random multicurves on large genus hyperbolic surfaces* as “in preparation”. | No full proof or mesoscopic theorem is supplied in this short contribution. The named project remains a direct priority lead. |
| Durham slides: PDF pp.26, 193–195 | Primitive multigeodesics are the introductory setting. A slide labelled “Conjecture” gives microscopic [a/(6g),b/(6g)] counts with density e^(−x)(cosh x−1)/x, annotated ≈1/(2x). | The displayed n=1 density should not be silently substituted for the all-multiplicity thesis density. A tail annotation does not establish a growing-window theorem. No TV statement is displayed. |
| [Barazer–Giacchetto–Liu, final 2025 paper](https://doi.org/10.1017/fms.2025.31): Theorems A–B, pp.2–3; §2.4 | Fixed number n of faces; random metric ribbon graphs; total face length ∼12g−12+6n. Cycle lengths converge to PPP with density (cosh ℓ−1)/ℓ, with fixed disjoint interval count laws. Faces are excluded from cycles in the final formulation. This paper cites DL and DGZZ. | Different sampled object, observable, and normalization. It does not identify these cycle lengths with normalized areas of all cylinders in the target ensemble. Its mention of a mesoscopic sparse-map limit is also a different model. |
| [Liu–Rafi–Souto–Trin, arXiv:2605.03833v1](https://arxiv.org/abs/2605.03833): introduction, Theorems 8.3, 8.5, 7.15; reference [7] | Frequencies of curve types with fixed self-intersection number, including separating/nonseparating asymptotics. It cites final DL. Both arXiv and author-hosted full PDFs were obtained; their hashes differ. | Not an area/component-length point-process theorem. The version difference is preserved rather than treating the author's PDF as identical to arXiv. |
| [Delecroix–Legrand-Duchesne, arXiv:2501.15978](https://arxiv.org/abs/2501.15978): Theorem 1.6 | Cylinder-shear connectivity in specified hyperelliptic square-tiled components. | The result addresses reconfiguration, with no target mesoscopic distribution statement in the inspected full text. |
| [Delecroix et al., arXiv:2608.24497](https://arxiv.org/abs/2608.24497): Theorems 1–3 | Algorithms for nets, pseudo-nets, and length spectra on a supplied hyperbolic surface. | Deterministic algorithmic setting, not the target random area law. |
| [Baroni–Fisac–Liu, arXiv:2609.01382](https://arxiv.org/abs/2609.01382): Theorem 1.1 | Exact word-length curve counts in a fixed once-punctured-torus mapping-class orbit. | Fixed genus-one setting; no large-genus cylinder-area statement. |

The OWR microscopic multiplier is printed **4g−4**. The thesis uses **6g−6**, consistent with the candidate's stated exact-formula convention. This audit preserves the discrepancy. It neither silently repairs OWR nor infers failure of the mesoscopic claim from it. Both versions describe a microscopic regime; neither alone supplies the required uniform mesoscopic result.

## Current public author lists and followups

The freshly retrieved [Delecroix research page](https://www.labri.fr/perso/vdelecro/research.html) and correct-name [arXiv author inventory](https://arxiv.org/search/math?query=Delecroix%2C+Vincent&searchtype=author&abstracts=show&order=-announced_date_first&size=200) were compared. The arXiv page returns 37 math results, including August 2026 work. [Liu's page](https://www.math.univ-paris13.fr/~mingkun.liu/research.html), [current CV](https://www.math.univ-paris13.fr/~mingkun.liu/CV/CV_en.pdf), and correct-name [arXiv inventory](https://arxiv.org/search/math?query=Liu%2C+Mingkun&searchtype=author&abstracts=show&order=-announced_date_first&size=200) return eight mathematical papers, including September 2026 work. Neither inventory contains the named small-components title. These are bounded discovery results, not exhaustive claims about all public or private work.

A retrieval pitfall matters: DL's inverted displayed author names lead its automatic arXiv author links to `Vincent, D` and `Mingkun, L`. Those incomplete two-result/one-result searches were discarded. The corrected inventories are pinned separately in SOURCE_PINS.json and summarized in AUTHOR_INVENTORY.tsv.

Selected 2025–26 announcements were opened at their primary hosts. Durham's abstract calls the Delecroix collaboration partly ongoing. [Dublin, October 2025](https://www.maths.tcd.ie/~dmc/), [Lille, June 2025](https://math.univ-lille.fr/detail-event/default-0defe9346d), [Tours, February 2025](https://www.idpoisson.fr/agenda-de-lidp/?id=13768), [Luxembourg, May 2026](https://math.uni.lu/geometry/gt_seminar/), and [Montpellier, June 2026](https://imag.umontpellier.fr/?idseance=5706&page_id=526) describe the Barazer–Giacchetto–Liu metric-map direction. [IHP, 9 September 2026](https://indico.math.cnrs.fr/event/17206/?print=1) describes the exact torus-count paper. The [ENS event page](https://www.math.ens.psl.eu/evenement/mingkun-liu-raconte-moi-les-surfaces-hyperboliques-aleatoires/) is about random hyperbolic surfaces and systoles, and dates the talk 25 March 2026; the current CV lists an April entry. This mismatch is retained. Abstracts only establish announced subject matter, not absence of unadvertised results.

## Undischarged lead and release implication

**Lead AH-1:** the full small-components project named by OWR reference [5], supported by the thesis's detailed formula and the DL introduction's ongoing-work announcement. A manuscript or later full statement might contain uniform asymptotics or a stronger coupling even if its title emphasizes microscopic components. Searches using the exact title, author combinations, cylinder areas, microscopic/mesoscopic/intermediate scales, and total variation did not locate such a text. This is insufficient to clear priority.

**Lead AH-2:** not every talk in the current CV has a public full text; for example, the September 2026 Rennes entry was not resolved to a primary full statement. No theorem-coverage conclusion is drawn from that gap.

The warranted outcome of this lane is **no verified anticipation found in the inspected public primary texts, with a named unresolved followup**, rather than a novelty certificate. Before any preprint claims, retain explicit credit for the published machinery and the public microscopic announcements. The candidate's exact new scope, if any, must be judged against the other independent priority lanes and adversarial synthesis. Outside clarification could help resolve AH-1; under the project's independent-research policy, only the human may communicate externally. No outreach was prepared or initiated.

## Reproducibility and containment

Fresh retrievals, full PDFs/HTML/text, rendered pages, response headers, and raw search payloads reside only in ignored `private_reading/` and `private_transport/`. SOURCE_PINS.json records URLs, retrieval timestamps, sizes and SHA-256 hashes; SEARCH_LEDGER.md records queries and limitations. Visual checks: OWR p.19, DL final p.6, thesis p.22, Durham pp.26 and 195, and metric-map final p.3. Entire relevant theorem pages were read, rather than treating search snippets as evidence.

No individual was contacted. No Git/index/ref, provider state, paper, deposit, tracker, or sibling file was changed. The safe authored manifest is limited to this lane's reports and compact metadata. Completion estimate: **100% of this bounded lane audit; no estimate of mathematical novelty is implied**.
