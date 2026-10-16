# Search provenance — PR 468 / problem 30000689

Search period: 2026-10-12 04:21–04:42 UTC. Scope: an independent bounded priority/lineage audit, not an exhaustive novelty certificate. No fresh sibling review was read; initial verdict saved at 04:26 UTC. Search results were discovery aids. Mathematical judgments used primary paper texts and fixed archive/publisher records.

## Starting material and reproducibility

Read the frozen `source_snapshot/unsolved_math_prioritization/attempts/30000689/release/PROOF.md`, `release/SOURCE_GATE.md`, and `EXPLANATORY_ADDENDUM.md`; checked original Nevo–Wagner and OWR texts held in the audit's ignored parent source folder. Downloaded selected primary PDFs in this folder's ignored `private_sources/`, extracted text, and searched theorem/conjecture/embedding passages. `SOURCE_MANIFEST.json` records source URLs, byte counts, and SHA-256 hashes for the eighteen valid PDFs downloaded here. Source metadata and failed access responses are also private. The mutable author copies are identified as such rather than dated by their current body text.

## Citation discovery

- Semantic Scholar: `https://api.semanticscholar.org/graph/v1/paper/DOI:10.1007/s11856-009-0119-5/citations?fields=title,year,url,openAccessPdf,externalIds&limit=1000` — six titles returned.
- OpenAlex: identified the DOI work as `W2016722080`; read `https://api.openalex.org/works?filter=cites:W2016722080&per-page=200` — six titles returned, partly different. Union: seven distinct titles, classified in the report.
- Crossref DOI metadata for Nevo–Wagner and Wagner's chapter: publication dates and source links checked. These are bibliographic sources, not substitutes for inspecting the theorem.
- Nevo's primary publication list and current institutional pages; Wagner's institutional publication list through 2026; Adiprasito's primary institutional homepage and author blog. Lists are not assumed complete or fully current.
- HAL's primary API for `hal-05575100` with title, author, version, submitted/produced/modified/publication dates and URI. It identified v2 deposited 27 April 2026. A filtered v1 query returned no record; no first-version date was inferred.

## Query families actually used

The following records the main literal query families and selected follow-ups, rather than copying search-provider responses or claiming every irrelevant result was read.

Exact statement and numbering:

```text
"Nevo" "Wagner" "Conjecture 1.3" sphere
"Nevo" "Conjecture 3.7" embeddability
"Nevo" "Wagner" "Conjecture 3.7" sphere
"Nevo-Wagner conjecture" sphere
"Nevo–Wagner" "sphere" conjecture
"Nevo-Wagner" conjecture embedding sphere solved
"Nevo-Wagner" proof
"Nevo Wagner" "Conjecture" "2026" sphere
"missing d-face" "sphere" embedding
"missing d-face" "Lefschetz"
"missing d-face" "embeddability" "proved"
"missing middle" "face" "sphere" embedding
"missing-face" "Nevo" "sphere" conjecture
"missing-face" "Wagner" "sphere" conjecture
"triangulated 2d-sphere" "Lefschetz"
"skeleta of spheres" "Conjecture"
"skeleta of spheres" "2019"
```

Low-dimensional and original-author follow-ups:

```text
"skeleta of spheres" "exotic"
"missing triangle" "4-sphere" "embed"
"missing triangle" "bistellar" "embedding"
"bistellar" "missing" "Nevo" "Wagner"
"Nevo" "Stellar theory" "skeleta"
"Nevo" "Bipartite rigidity" "missing"
"van Kampen" "flag" "Nevo" sphere
site:arxiv.org "Nevo" "Embeddability of simplicial complexes in manifolds"
site:eran-nevo.huji.ac.il/publications embedding sphere
"Connectivity and embeddability of buildings and manifolds" pdf
"Minors, embeddability, and extremal problems" Wagner pdf
"Minors, Embeddability, and Extremal Problems for Hypergraphs" filetype:pdf
site:pub.ista.ac.at Wagner "Minors" "Embeddability"
site:research-explorer.ista.ac.at "Minors, embeddability"
```

Broader theorem and modern mechanism checks:

```text
"Nevo" "Wagner" "g-conjecture" "proved"
"Nevo Wagner" "missing" "Lefschetz"
"Nevo" "Wagner" "Corollary" "Lefschetz"
"missing" "simplex" "sphere" "Adiprasito" embedding
"missing face" "Weber" "sphere" embedding
"Kalai-Sarkaria" "topological" "2026"
"Kalai Sarkaria" embedding sphere missing simplex
"Kalai–Sarkaria" "Nevo"
"Sarkaria" "missing simplex"
site:gilkalai.wordpress.com "Wagner" "g-conjecture"
site:gilkalai.wordpress.com "Sarkaria" "Adiprasito"
"A higher dimensional version of Fáry" arxiv
"Multigraded strong Lefschetz property for balanced simplicial complexes"
"Oba" "Grünbaum" "2026"
"Oba" "embeddable" simplicial complexes 2026
```

Several queries also excluded secondary reposts to prioritize original papers. Secondary indices and catalogues were used only to discover links; their open/solved labels were not treated as independently verified status.

## Full-text and date controls

The fixed arXiv histories were checked for `math/0602531`, `0709.0988`, `1812.10454`, `1812.08447`, `1312.0209`, `0810.5487`, `1302.5197`, `2101.10596`, `2304.08043`, `2410.17523`, `2307.14195`, and `2310.13495`. The main final report distinguishes initial submission, inspected revision, thesis body date, print issue, and electronic publication.

Important corrections: Nevo's 2006 and 2009 fixed preprints display later body dates after recompilation; Gundert's 2018 upload is a 2009 thesis; Kishimoto–Matsushita's skeleton PDF has a later body date than fixed v2. None was used as a fresh current-status assertion. The current streamlining's author-upload URL failed, but the author-linked HAL v2 document succeeded and its repository date was checked.

## Explicit coverage limits

Wagner's chapter is not certified as fully read: the Springer download returned an HTML page, renamed `wagner_survey_failed_response.html`; OpenAlex reported no open PDF. The live Math. Scand. endpoints tried for Nevo's published paper returned 404, although publisher-indexed p. 168 and fixed arXiv versions were readable. A newer Nevo institutional publication collection endpoint timed out/returned a short error; the checked primary older list openly says last updated March 2025. No subscription review service, private correspondence, unpublished specialist knowledge, or exhaustive all-language literature search was available. No external communication or outreach preparation occurred.
