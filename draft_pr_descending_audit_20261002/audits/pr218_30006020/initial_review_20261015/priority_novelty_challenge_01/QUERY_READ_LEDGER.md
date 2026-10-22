# Query and reading ledger

All retrievals and searches were performed on 2026-10-15 UTC. Complete external payloads are retained only in ignored `private/`; the public pins report identifiers and hashes. No outside individual was contacted.

## Inputs and independence

- Read frozen `submitted/unsolved_math_prioritization/attempts/30006020/CANDIDATE.md`, `TARGET.json`, and `source_manifest.json` only. Repository filename inventory was used to locate those three files; no root or sibling review content was opened.
- Read the PDF tool skill as operational guidance. No manuscript, previous review, tracker, or depositor content was consulted.

## Fresh primary reading

| Source | Extent actually read | Key locators |
|---|---|---|
| OWR 41/2024 complete report | Complete Delecroix contribution, printed 2384-2387; report opening date; visual printed 2387 | PDF pp. 16-19, Problem 2; theorem 2; references [3]-[5] |
| DL final publisher PDF, DOI 10.4171/JEMS/1469 | Complete 39 page paper including proofs and references; visual p. 5116 | §§1-6, Theorems 1.2/1.4/2.7/3.2/4.1/6.3, (6.1)-(6.8), Lemma 6.4 proof, Lemma 6.7 |
| DL arXiv v1 | Front matter and introduction screened for edition/date comparison; final paper controls theorem numbering | arXiv 2202.10255 v1, 2022-02-21 |
| DGZZ final author hosted publisher version | Abstract/TOC; all main theorem statements and ensemble definitions in introduction; §3.1 coefficient estimates and §3.2 permutation model; §5.1 statements and proofs relevant to 5.2; §5.2 proof of 1.12 and Corollary 5.3; §6.2 and references screened | Theorems 1.7/1.8/1.12/1.14/3.4/3.7/5.1/5.2, Lemmas 3.5/3.6; visual PDF p. 83 |
| DGZZ/DL publisher metadata and arXiv abstract pages | Metadata and version histories | DGZZ 2022-06-20 online; DL 2024-06-07 online, 2025 issue |
| Current Liu and Delecroix research pages | Full publication lists and linked later talk inventory | Liu list includes 2026 papers through arXiv:2609.01382; neither list supplies a downloadable Small components paper |
| Barazer-Giacchetto-Liu final metric maps PDF | Complete introduction, definitions of spectrum and random map, all Theorems A-D and §1.2 comparison | DOI 10.1017/fms.2025.31, fixed n faces, total perimeter ~12g, short cycles |
| Liu 2026 non-simple curves preprint | Abstract and metadata only; excluded at screening, no theorem coverage asserted | arXiv:2605.03833 |
| Liu Durham February 2025 talk | Text extraction searched throughout; small component slides read; visual slide 195 | PDF has many repeated handwritten overlays; conjecture concerns [a/(6g),b/(6g)] |
| Liu CIRM November 2024 talk | Title and topic screen; text searched throughout | Metric map length spectrum, distinct ensemble |
| Nikeghbali-Storm-Zeindler arXiv:1302.5938 | Definitions 3.2, Theorem 3.3, Corollary 3.4; relevant proof setup; §5.1 Theorem 5.1 and corollaries | Actual moving set condition (3.7), not an inferred all o(n) theorem |
| Nikeghbali-Zeindler arXiv:1105.2315 | Introduction, actual Theorem 3.1 and Corollary 3.1.1, proof setup | Fixed b cycle counts |
| ABT 2003 EMS book | Complete accessible preface plus publisher contents/metadata; full book unavailable through publisher download | General all sublinear component approximation is an unresolved exact theorem lead, not certified coverage |
| Stark 1997 CPC article | Publisher abstract and metadata only; full PDF unavailable in checked publisher page | DOI 10.1017/S0963548396002775; all b=o(n) assembly TV result is a lead requiring theorem/assumption verification |

## Web search batches

Provider result payloads `q1_web_raw.json` through `q11_web_raw.json` are private. Search results were used to discover primary sources; unrelated results and secondary summaries were not promoted to evidence.

| Batch | Exact queries / direct operations | Outcome |
|---|---|---|
| q1 | `"Delecroix" "Liu" "mesoscopic"`; `"cylinder areas" "Poisson" Delecroix Liu`; `"2202.10255" "Poisson"`; `"square-tiled" "mesoscopic"` | No same target result; discovered 2025 metric map paper |
| q2 | `"Length partition of random multicurves" Delecroix Liu`; `"Delecroix" "Liu" "Poisson" multicurves`; `"random multicurves" "microscopic"`; `"Delecroix" "cylinder" "areas" 2025 2026` | DL publisher, current author pages, older fixed type length results |
| q3 | `"Small components of random multicurves"`; `"cylinders of intermediate area"`; `"Delecroix" "Liu" "total variation"`; `"cylinder areas" "large genus"` | OWR report returned; no accessible Small components paper identified |
| q4 | Direct author pages, arXiv:2312.10517, DL publisher page; arXiv domain queries `"Small components" multicurves Delecroix Liu`, `"random multicurves" "mesoscopic"`, `"cylinder areas" Poisson` | Current primary metadata and article lists; many irrelevant query results |
| q5 | `Delecroix Liu small components random multicurves large genus`; `Delecroix Liu cylinder intermediate area mesoscopic Poisson genus`; `"multicurves" "mesoscopic"`; `"cylinder-area" Poisson genus` | Reconfirmed DL/DGZZ; found arXiv:2605.03833, unrelated non-simple frequency result |
| q6 | `weighted random permutations mesoscopic cycle lengths Poisson process Nikeghbali Zeindler`; `logarithmic combinatorial structures scale invariant Poisson process mesoscopic cycles`; `"Delecroix" "intermediate" cylinders`; exact Small components title | Found primary generalized weighted permutation papers; no geometric target theorem |
| q7 | Direct arXiv:1302.5938 and 1105.2315; `"generalized weighted" "total variation" "cycles"`; `"logarithmic combinatorial structures" "b=o(n)"`; `"weighted random permutations" "b(n)" "Poisson"` | Actual older theorem read; broader assembly approximation leads |
| q8 | EMS domain queries for logarithmic structures Theorem 6.1 / Small components; exact Stark Explicit Limits title | Accessible primary preface; Stark publisher abstract, no complete theorem read |
| q9 | Find PDF links on Stark publisher page; search exact Stark title with PDF and primary EMS book title | Full Stark unavailable; EMS book located |
| q10 | Open verified EMS book `/books/emm/18` | Metadata; subscription stated |
| q11 | Click book contents and full PDF links | Contents readable; full PDF redirects to subscription page |

Additional direct opens: OWR and DGZZ DOI resolver calls in the web tool returned internal errors, but fresh direct complete PDFs succeeded through public institution/author URLs; metadata retrieval through publisher URLs then succeeded. One guessed EMS book URL `/books/em/1531` failed and was abandoned; the verified correct book URL was discovered by search. All such read failures leave no evidence of theorem coverage.

Search limitations: exact absence is not established by indexed search or author list omission. An in-preparation article or unindexed talk may contain stronger conclusions. No public source located here gives a proved moving mesoscopic statement for this principal quadratic area ensemble.
