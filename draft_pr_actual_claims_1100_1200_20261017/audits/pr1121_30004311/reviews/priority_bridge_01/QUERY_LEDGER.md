# Focused query and inspection ledger

Recorded UTC: 2026-10-17T20:18:38.949104+00:00. The session began 2026-10-17T20:13:58Z. The web tool does not expose a reliable per-query execution timestamp, so no invented exact timestamps are assigned below. These queries were executed during this session before this ledger was written (batch 10 was added afterward at 2026-10-17T20:20:08.246070+00:00); individual network fetches have exact actual UTC timestamps in FETCH_RECEIPTS.json.

Search results were discovery leads only. Unless a body inspection is recorded, a title/abstract does not count as evidence that a theorem is present or absent.

| Batch | Exact search queries | Outcome |
|---|---|---|
| 1 | `"simple left brace" "center" "abelian" "Sylow"`; `"asymmetric" "nontrivial" "metabelian" brace`; `"simple left braces" "radical ring"` | Located primary families and survey leads; no theorem inferred from snippets. |
| 2 | `brace "simple" "matched product" "radical"`; `brace "simple" "metabelian" "nontrivial" "asymmetric"`; `"simple left braces" "central" multiplicative group`; `"Constructing simple left braces" Cedo Jespers Okninski` | Followed matched-product references 1610.00477 and 1511.08477; both bodies inspected. |
| 3 | `"simple left braces" "ring" "matched" nilpotent`; `"brace" "center" "metabelian" simple`; `"simple braces" "Sylow" "non-trivial" "2025"` | Identified recent cyclic-Sylow source and older survey. |
| 4 | `"simple left brace" "abelian Sylow" -site:researchgate.net -site:academia.edu`; `"simple left braces" "asymmetric product" 2025 2026`; `"brace" "metabelian" "centre"`; `"brace" "metabelian" "center" "simple"` | Found exact OWR question and 2025 journal publication of 2401; current arXiv body checked. |
| 5 | `"An abundance of simple left braces" -site:researchgate.net -site:academia.edu -site:arxiv.org`; `"Every finite abelian group is a subgroup" "2026"`; `"Every finite abelian group is a subgroup" "2025"`; `"New simple solutions" "permutation groups" "2026"` | Metadata/citation leads. OpenAlex records and current citing lists retrieved privately. |
| 6 | `"simple left braces" construction ring 2024 2025 2026`; `"simple braces" "nilpotency" "construction"`; `"matched products" "simplicity" braces "2025"`; `"left brace" "nontrivial center" simple` | Located 2609.24640. Main construction statements and seed body inspected, not rejected by title alone. |
| 7 | `"simple brace" "non-trivial centre"`; `"simple brace" "nontrivial center"`; `"simple left brace" "centre"`; `"simple left brace" "center" group` | No full-target primary bridge established; search absence is not used as novelty evidence. |
| 8 | `"Asymmetric product of left braces and simplicity" "doi"`; `"More on skew braces and their ideals" arxiv`; `"simple" "left braces" "nilpotency class" "Sylow"`; `"simple left braces" "truncated"` | DOI for 1705 resolved; More on skew braces is a lead, but its body was not separately fetched/inspected in this bounded audit. |
| 9 | `"brace" "simple" "truncated polynomial"`; `"simple left braces" "logarithm"`; `"simple brace" "nilpotent ring"`; `"simple braces" "commutative" "matched"` | Did not establish a published higher-nilpotency simplicity theorem. No conclusion drawn from absence. |

| 10 | `"every finite left brace" "simple" "embeds"`; `"brace" "subbrace of a finite simple"`; `"finite brace" "simple left brace" "embedding"`; `"radical ring" "simple left brace" "subbrace"` | Located 2609.20401; current v1 record and full §3 group construction inspected, plus simplicity-permanence statement/proof. Own support-based elimination completed. |

## Direct records and bodies

The four requested arXiv abstract/version records were opened directly. The PDFs were freshly fetched at versioned URLs, extracted privately and inspected at the scopes in SOURCE_VERSIONS.json. Reference chasing added 1610.00477v1 and 1511.08477v3. Later-body checks added 2112.07271v1, 2311.07112v3, 2609.24640v1, 2607.17125v2, and 2609.20401v1.

The 2025 publisher DOI and ScienceDirect body were requested directly; no final body was obtained. The direct official PDF returned HTTP 403. Hence final-version identity is unverified.

OpenAlex requests used the journal/merged records for 1705 (W2619595180), 1807 (W2884510882), 2001 (W3037527354), and 2401/2025 (W4411149198), retrieving all returned citing entries in one page per record (counts 29,12,8,0). Raw response bodies remain ignored. Citing bodies actually inspected include 2112.07271 and the survey 2311.07112. Other metadata leads, including Soluble skew left braces, More on skew braces, On two-sided skew braces, Semi-affine structures, Cabling, and various radical/cohomology papers were not all read; none is certified irrelevant merely from its metadata. The 2026 deformation/cyclic-Sylow sources were independently found by search, not represented as complete OpenAlex coverage.

No person was contacted. No repository index, refs, branch, commit, push, PR, or release was changed by this subagent.
