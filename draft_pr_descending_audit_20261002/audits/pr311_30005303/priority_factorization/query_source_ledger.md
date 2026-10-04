# Query/source ledger

## Source-first stage

- 2026-10-04T16:30:50.966846+00:00 — Opened publisher PDF URL https://ems.press/content/serial-article-files/46992 with web tool, and fetched it directly. DOI 10.4171/OWR/2022/55 checked in PDF header; source passage printed pp. 3125–3126; references p. 3127. Exact bytes/hash and source read scope are in source_only_checkpoint.json. No search of candidate/root/sibling contents.

## Query register and native evidence

All raw web results are private `private_sources/web_query_NN.txt`. The following is the exact search text register; related opens/finds are summarized separately. Search-result text is discovery evidence only unless a primary statement is separately identified and body-read. The web calls 01–11 did not have their own separately measured clock timestamps; the ordered sequence and surrounding timestamped source/checkpoint/command observations are preserved. No reconstructed precise query times are asserted. Their private result files' measured filesystem times are included in the final manifest but are not claimed to be query-call times. Native command captures beginning at 16:32:47.974153 UTC preserve exact argv, actual start/end UTC, exit status, stdout and stderr. Earlier initial fetch/render/criteria creation calls exist in the session tool transcript but were not captured by that wrapper; this is an explicit capture limit.

| Result file | Stage | Exact search text / primary opens |
|---|---|---|
| 01 | Source-first, before 16:32:47 GMS fetch | `"On the toric algebra of graphical models" Geiger Meek Sturmfels pdf`; `"Lauritzen" "factorization" "lattice" "MTP2"`; `"totally positive" "Markov" "factorize" conjecture`. Discovered GMS primary PDF/arXiv record. |
| 02 | Source-first | `"MTP2" "factorization" "counterexample"`; `"Markov" "lattice support" factorization`; `"Total positivity in exponential families with application to binary variables"`. Opened GMS author PDF; found Kahle–Sullivant primary. |
| 03 | Source-first | Opened `https://arxiv.org/abs/2411.03139` and its PDF, and searched the PDF for relevant Example/Conjecture passages. Body statement actually checked. |
| 04 | Source-first, before first conclusion freeze 16:35:56 UTC | Opened v1 PDF and arXiv submission history. Queries `"Lattice supported distributions and graphical models" "Example 6.5"`; title/journal search. Publisher status leads were metadata only; no journal body inferred. |
| 05 | Source-first | `"Gibbs and Markov random systems with constraints" pdf`; `"Conditional independences among four variables" "1995" pdf`; `"Total positivity in Markov structures" pdf`. Citation-chain leads. |
| 06 | Source-first | `Moussouris Gibbs Markov constraints 1974 BF01011714`; `"Conditional independences among four random variables I" pdf`; `"MTP2" "Kahle" "Sullivant"`. Moussouris publisher metadata/abstract; no original full body. |
| 07 | Source-first | Opened Studený author page, Springer Moussouris page and a purported DML link. Queries `"MTP2" "factorization" zeros lattice counterexample four cycle`; `"lattice supported distributions" counterexample MTP2`. DML was another title and rejected. An unrelated repository STATUS snippet appeared incidentally; not opened or used, no candidate/root/sibling file body read from it. |
| 08 | Source-first | Looked for publisher fulltext of Moussouris; opened `https://arxiv.org/pdf/1603.01481`, which is Onural, not Gandolfi–Lenarda. The temporary incorrect local filename was corrected transparently by captured rename; no identity inference from that filename. |
| 09 | Source-first; older primary fetched 16:38:10 UTC, conclusion before candidate read | `"A note on Gibbs and Markov Random Fields with constraints and their moments" pdf`; `"Moussouris" "pdf" "1974" Markov`; `"lattice supported" "Proc" AMS Kahle Sullivant`. Discovered actual Gandolfi–Lenarda publisher primary, read Lemma5.2. |
| 10 | Post-release | `"MTP2" "closed" "Ising" factorization`; `"ferromagnetic" "Ising" "closure" probability`; `"log-supermodular" "pairwise" "zeros" factorization`. No prior equivalent finite-factor closure statement established. |
| 11 | Post-release | `"MTP2" "C6" factorization`; `"MTP2" "six-cycle"`; `"Markov" "factorization" "a,a,b,b,c,c"`; `"Markov" "lattice" "Gandolfi"`. No C6-specific primary table established. Negative discovery output is not novelty evidence. |
| 12 | Post-release; saved at actual 16:48:22.739183 UTC | `"binary" "MTP2" "factorization" "closed"`; `"ferromagnetic" "graphical models" "closure"`; `"Kolmogorov" "Rother" "Minimizing nonsubmodular functions" 2007`. Secondary snippets were discovery only. |
| 13 | Post-release; primary fetch at actual 16:48:40.984348 UTC | Opened exact author-hosted `https://www.microsoft.com/en-us/research/wp-content/uploads/2007/01/PAMI07-QPBO.pdf`; actual body and §§2.1–2.2 checked. |
| 14 | Post-release; UTC clock captured in request JSON, results saved at actual 16:50:28.254816 UTC | `"Gandolfi" "Lenarda" "MTP2"`; `"lattice supported distributions" "closed"`; `"MTP2" "factorization" "six"`; `"Markov" "Gibbs" "2/9" "1/9"`. Publisher alternate PDF independently returned exact GL law. Secondary generalization snippet omitting the natural-rank hypothesis was not used. Conference abstract was corroborating metadata, not an additional theorem body. |

## Primary-source and citation-chain register

| Source, identifier and exact location | Body-read status | Claim comparison |
|---|---|---|
| Lauritzen, DOI10.4171/OWR/2022/55, publisher `https://ems.press/content/serial-article-files/46992`, printed3125–3127 | PDF passage read/text extracted; pages3125–3126 visually read before freeze | Exact target definition. 600619 bytes and expected SHA authenticated. |
| Geiger–Meek–Sturmfels2006, DOI10.1214/009053606000000263, `https://math.berkeley.edu/~bernd/AOS0092.pdf`, Theorems3.1/3.2, Proposition1/(4.10), Examples7/8 | Primary body read; command captures `read_gms_general_theorems`, `read_gms_prop1`, `read_gms_invariants_refs` | Known quartics and toric/feasible-support distinction. Actual examples independently checked and all coordinate-flip MTP2 recodings rejected. |
| Kahle–Sullivant2024, arXiv2411.03139v1, Example6.5p13, Definition2.4p3, Theorem6.1p10 | Primary body read; Example6.5 visually read; private result03/04 plus `read_prior_statements`, `read_ks_attribution` | Explicit lattice/global/nonfactorization family; exact MTP2 specialization. Primary arXiv history5Nov2024 14:31:16UTC verified; PDF6Nov date noted. Later acceptance metadata not a body/date claim. |
| Gandolfi–Lenarda, DOI10.2140/memocs.2016.4.407, `https://msp.org/memocs/2016/4-3/memocs-v4-n3-p13-p.pdf`, Lemma5.2printed415–417, Example6.3p418, introductory definitions/refs | Primary law/proof body read before candidate; relevant pages visually checked; actual publisher HTML fetched and date read | Exact old qualifying law and exact candidate rotation. Publisher Published13April2017 authenticated. Volume2016 not treated as publication date. |
| Fallat etal2017, DOI10.1214/16-AOS1478, UCL primary deposit PDF, Example5.4/Theorem6.1/§7 | Primary body read; command captures `read_fallat_examples`, `read_fallat_factors` | Zeros can break intersection; graphoid/decomposable/strict positivity assumptions block unrestricted specialization. |
| Lauritzen–Uhler–Zwiernik2021, DOI10.1214/20-AOS2007, `https://web.math.ku.dk/~lauritzen/papers/AOS2007.pdf`, §4.4/Example4.7/Lemma4.9/Cor4.10 | Primary body read; `read_luz_extended`, `read_luz_support`, `read_luz_lattice` | Extended-family compactness and positive-margin support do not prove finite-factor boundary identity. |
| Kolmogorov–Rother2007, DOI10.1109/TPAMI.2007.1031, author-hosted manuscript §§2.1–2.2 | Primary body read, fetched245472bytes SHA447685d9ff5acf753829bfd0db4c3654e70be12d59841f3bf9d3864fccb18096 | Classical cut/flow reparameterization; no assertion of source closure theorem. |
| Moussouris1974, DOI10.1007/BF01011714, Springer page | Metadata/abstract read; original full body unavailable; alleged DML fulltext was another title | Cannot promote an unread original example to qualifying priority. GMS's reproduced example checked separately. |
| Matúš–Studený1995, DOI10.1017/S0963548300001644, author page `https://staff.utia.cas.cz/studeny/a12.html`, primary PDF `/FTP/matus-ci4-i.pdf` | Author page and body example catalogue inspected; not every historical consequence proved | No fully derived binary MTP2/global/nonfactorization specialization established. Not an exclusion theorem for all content. |
| Onural2016, arXiv1603.01481, actual primary PDF | Body inspected; captured rename corrects initial download's mistaken local label | Constraint scope/fixed graph differs; no exact target equivalent specialized theorem established. |

## Comparison execution checkpoints

- 16:34:33.004994–16:34:33.037663 UTC: initial exact primary-example check; results frozen in first-priority manifest.
- 16:38:50.840394 UTC: source-only older-law check; no candidate material read; exact products1vs2 and MTP2/global checks captured.
- 16:40:13.953096 UTC: first released-candidate body reads; per-file actual read times in input manifest.
- 16:41:30.028010 UTC: publisher date HTML fetch; subsequent date read establishes13April2017.
- 16:44:20.082951–16:44:20.204658 UTC: independent C4/C6/old-law exact verifier.
- 16:50:28.369591–16:50:28.496153 UTC: fresh rerun; 16:50:28.560043–16:50:28.594209 UTC: identical output bytes confirmed.

Every timing above except separately labelled early observations comes from actual captured UTC clocks; inspect the native captures for exact measured end times rather than inferring them from this prose. The final `native_command_index.json` is a content-hashed index of the private raw captures and is not a replacement for them. No search result, abstract, acceptance metadata or failure to locate a theorem is counted as a primary proof of an already-solved claim.
