# Independent bounded priority audit

Audit completed: 2026-09-23 UTC (2026-09-22 America/Los_Angeles). Assigned audit completion: **100%**. This percentage describes the bounded search and source comparison, not certainty of global novelty. No individual was contacted.

**Finding:** no prior resolution of the general-convex-body equality characterization was found in the sources and searches below. The candidate targets an explicitly recorded conjecture, not a new inequality. A defensible publication claim is: *We prove the equality characterization conjectured by Fradelizi, Paouris, and Schütt; our literature search found no earlier proof.* Do not claim that novelty has been certified.

## Exact source and scope

The primary historical source is Fradelizi's contribution, joint with Paouris and Schütt, *Simplices in the Euclidean ball*, in **Oberwolfach Report 53/2009**, printed pp. 2907–2909, DOI [10.4171/OWR/2009/53](https://doi.org/10.4171/OWR/2009/53), [publisher PDF](https://ems.press/content/serial-article-files/46255). Printed p. 2908 gives the extreme-point lower bound with the centroid term, gives its simplex equality characterization for polytopes, and expressly conjectures the same characterization for arbitrary convex bodies. The following theorem concerns Löwner position; it is a different result and does not enlarge the equality conjecture in question.

The journal source is M. Fradelizi, G. Paouris and C. Schütt, *Simplices in the Euclidean Ball*, **Canadian Mathematical Bulletin 55(3) (2012), 498–508**, DOI [10.4153/CMB-2011-142-1](https://doi.org/10.4153/CMB-2011-142-1), [published PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/DE65A193C3EE743DF0EA834A8405026E/S0008439500021561a.pdf/simplices_in_the_euclidean_ball.pdf). Theorem 1.1 and the paragraph immediately after it are on p. 499. Section 3 proves the polytope case and passes to general bodies by approximation. Its Lemma 3.2 already supplies the simplex second-moment identity. The PDF records electronic publication on **2011-07-08**; Cambridge's later platform date of 2018-11-20 must not be mistaken for first publication.

For a compact full-dimensional convex set K, let g_K be its volume centroid and C_2(K) its volume-normalized integral of squared Euclidean norm. The conjecture is the equality classification in

    C_2(K) >= (r^2 + (n+1)|g_K|^2)/(n+2),

under |v| >= r for every extreme point v. The paper's prose uses “greater than r,” but its equality clause and Section 3 explicitly permit |v| = r. The non-strict formulation makes that intended boundary case unambiguous. Equality means an arbitrary nondegenerate simplex with vertices on the origin-centered sphere r S^(n-1), without an extra zero-centroid or regularity requirement. Adding g_K = 0 characterizes equality in the weaker bound C_2(K) >= r^2/(n+2).

The current [catalogue entry OWR-4136-011](https://www.unsolvedmath.com/problems/OWR-4136-011) was independently matched by the coordinating reviewer through the browser; see `source-match.md`. It restricts to n > 2 and matches the above statement. The candidate's n >= 1 result therefore covers the catalogue problem. My direct web and HTTP fetches of that catalogue page failed (HTTP 429), but the mathematical source comparison here uses the publisher originals.

## Forward-citation audit

On 2026-09-23, Crossref and Semantic Scholar returned two citing works; OpenAlex returned four. The union was inspected using primary full texts, not inferred from titles alone.

| Citing work | Exact relationship to the target | Assessment |
| --- | --- | --- |
| D. Alonso-Gutiérrez, *A remark on the isotropy constant of polytopes*, Proc. AMS 139 (2011), 2565–2569, [DOI](https://doi.org/10.1090/S0002-9939-2010-10669-X), [institutional published PDF](https://zaguan.unizar.es/record/61278/files/texto_completo.pdf) | Remark 2.2 cites FPS for estimates tied to the centroid in John position. The article estimates isotropy constants from vertex/facet counts. | Does not state or prove the general equality characterization. |
| G. Paouris and E. M. Werner, *Relative entropy of cone measures and L_p centroid bodies*, Proc. LMS 104 (2012), 253–286, [DOI](https://doi.org/10.1112/plms/pdr030), [author preprint](https://arxiv.org/abs/0909.4361) | The 2009 preprint cites FPS at its comparison of L_p centroid bodies, following equation (2.8). Its principal equalities concern affine invariants and ellipsoids. | No target resolution in the inspected preprint; its citation is to a different part/application of FPS. |
| M. Fradelizi, M. Meyer and V. Yaskin, *On the volume of sections of a convex body by cones*, Proc. AMS 145 (2017), 3153–3164, [DOI](https://doi.org/10.1090/proc/13457), [author preprint](https://arxiv.org/abs/1604.05351) | Lemma 7 cites FPS [8] for a simpler proof of directional second-moment/support-function estimates. | Does not establish the extreme-point equality conjecture. |
| H. Huang, *John Ellipsoid and the Center of Mass of a Convex Body*, Discrete Comput. Geom. 60 (2018), 809–830, [DOI](https://doi.org/10.1007/s00454-017-9924-5), [author preprint, version 4](https://arxiv.org/abs/1605.06881) | Lemma 4.2 attributes a John-position moment estimate to FPS and supplies another proof. The main result concerns displacement of the centroid from the John ellipsoid. | Does not establish the extreme-point equality conjecture. |

Citation-index endpoints inspected:

- [Crossref work record](https://api.crossref.org/works/10.4153/CMB-2011-142-1).
- [OpenAlex work record](https://api.openalex.org/works/https://doi.org/10.4153/CMB-2011-142-1) and [all four citing records](https://api.openalex.org/works?filter=cites:W2019702124&per-page=100).
- [Semantic Scholar work and citations](https://api.semanticscholar.org/graph/v1/paper/DOI:10.4153/CMB-2011-142-1?fields=title,citationCount,citations.title,citations.year,citations.externalIds).

The differing counts demonstrate why no one index should be treated as exhaustive.

## Broader search log

All following searches ran on 2026-09-23 UTC. Quotation marks shown are the actual search syntax. Search results were screened for the exact functional, hypotheses, and equality conclusion. Some broad searches returned unrelated simplex mean-width, Mahler, isotropy, triangulation, or localization results; these are not resolutions of this question.

Representative exact queries (including the principal independent search families):

1. `"OWR-4136-011"`
2. `"Simplices in the Euclidean ball" equality convex bodies`
3. `"Simplices in the Euclidean Ball" conjecture`
4. `"Simplices in the Euclidean Ball" Fradelizi citations`
5. `"10.4153/CMB-2011-142-1"`
6. `"Simplices in the Euclidean ball" 2020`; repeated with `2024` and `2026`.
7. `"Simplices in the Euclidean ball" "conjecture" -site:cambridge.org -site:citeseerx.ist.psu.edu -site:perso.math.u-pem.fr -site:ems.press -site:oa.tib.eu`
8. `"second moment" "extreme points" "simplex" "equality"`
9. `"second moment" "extreme points" convex body inequality Fradelizi`
10. `"equality case" "Fradelizi" "Paouris" "Schütt" -site:citeseerx.ist.psu.edu -site:cambridge.org -site:perso.math.u-pem.fr`
11. `"Fradelizi–Paouris–Schütt" equality`; repeated with ASCII hyphens.
12. `"Fradelizi" "Paouris" "Schutt" "equality" "moment"`
13. `"Fradelizi" "second moment" "equality" "simplex" 2025 2026`
14. `"Fradelizi" "Paouris" "Schütt" "rigidity"`
15. `"Fradelizi" "Paouris" "Schütt" "conjecture" "solved"`
16. `"convex body" "countably" "simplices" "extreme points"`
17. `"convex body" "countable" "triangulation" "extreme"`
18. `"convex body" "simplices" "extreme points" "decomposition"`
19. `"second-moment" "Fradelizi" simplex equality`
20. `"moment of inertia" "extreme points" simplex`
21. `site:arxiv.org "Fradelizi" "Paouris" "Schutt" "Simplices"`

The [Fradelizi author bibliography](https://perso.math.u-pem.fr/fradelizi.matthieu/content/articles-preprints.html) was retrieved through indexed search results, including listed 2026 publications. The [Paouris author bibliography](https://sites.google.com/tamu.edu/grigoris-paouris/researchpapers) was opened directly and includes 2026 preprints. Neither listed a discernible equality-conjecture resolution. This is title-level screening of those bibliographies, not full-text review of every author publication. The Schütt author search returned bibliographic aggregators; these were used only as discovery leads, not mathematical evidence.

## Attribution and remaining uncertainty

Credit FPS for the inequality, the complete polytope equality case, the simplex moment formula, and the conjecture itself. The candidate's relevant extension is the equality-preserving passage to arbitrary bodies using a countable decomposition into simplices with original extreme-point vertices. No separate originality claim for that decomposition lemma is warranted by this bounded search: incremental polytope triangulation is standard, and a useful elementary observation can have prior appearances outside indexed keywords.

No material contradictory lead remains unresolved within this audit. Residual uncertainty is ordinary bibliographic incompleteness: unindexed material, inaccessible books/theses, differently phrased statements, and unpublished proofs are not ruled out. Mathematical verification is a separate question addressed by the proof audits. Independent human expert review would strengthen publication confidence; no outreach has been prepared or initiated.

Local source copies and citation-index JSON records use the `priority_` prefix in `sources/`. Their hashes appear in `priority-source-inventory.json`; external full texts are reading copies, not intended for redistribution in the paper or upload package.
