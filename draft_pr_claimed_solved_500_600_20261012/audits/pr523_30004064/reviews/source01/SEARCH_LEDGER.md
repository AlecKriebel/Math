# Source and priority search ledger

All operations were read only. No author was contacted. Searches ran 2026-10-13, approximately04:20–04:32UTC. This is an extensive bounded audit, not a guarantee that every earlier paper was discovered.

## Targeted web query batches

The following exact queries were submitted in batches. Results were pooled by the web tool, so this ledger does not attribute every hit to a single query when the response did not do so.

| Batch | Queries | Material outcome |
|---|---|---|
| 1 | `Kadu OWR 4 2019 dual binary tomography conjecture 1 258`; `10.1109/TCI.2019.2898333`; `arxiv 1807.09196 dual binary tomography` | Primary OWR and author-paper locations. General DOI query also returned irrelevant imaging hits, ignored. |
| 2 | `"A Convex Formulation for Binary Tomography" "correction"`; same title plus `"conjecture"`; same title plus `"zero"`; `"binary tomography" "Kadu" "counterexample"` | Positive direct prior hit: Ferudun2026 paper page and PDF; Utrecht version of record; CWI manuscript. |
| 3 | `"23110494" tomography`; `"Kadu" "Leeuwen" "tomography" "erratum"`; authors/tomography plus `"correction"`; `"dual" "binary tomography" "conjecture" -site:researchgate.net -site:eulersolve.org` | OWR and author sources; no separate erratum identified. Excluding prior preprint tested for alternative later sources, not evidence of absence. |
| 4 | `"Fishburn" "Schwander" "Shepp" "Vanderbei" 1997 tomography`; `"dual" "binary tomography" "zero optimum"`; `"OWR-16766-003"`; `"Kadu–van Leeuwen" conjecture` | Old primary theory located by co-author publication page; source-target duplicate linked by Ferudun paper. |
| 5 | `Fishburn Schwander Shepp Vanderbei discrete Radon transform pdf site:princeton.edu`; `"binary tomography" "conjecture" "Kadu" -site:researchgate.net -site:eulersolve.org`; `"1807.09196" "correction"`; `"2898333" "erratum"` | Author-hosted1997 PDF located; source paper/seminar references found; no separately identified correction. |

## Primary retrieval and clause inspection

Successful retrieval records with full URLs, byte counts, SHA-256, and exact times are retained in `sources/retrieval.json`. Local reading copies are ignored from version control/publication by `.gitignore`.

| Source | Retrieved and inspected evidence |
|---|---|
| EMS OWR4/2019 complete PDF | SHA `8d9d44137ed3246a1e5819e6518d4c4033c35188df351a0963fa0c3e8951ec2f`; complete Kadu contribution printed256–259; Theorem1/Conjecture1 at258; full contribution rendered and visually checked. |
| arXiv1807.09196 v1 | SHA `21d94c86fb2f67496f3bf431d0e802350632ea0f30b0726c38ceec07d680a159`; source history24July2018; §§IIA–C, scalar equations10–11 and strict zero-sign convention checked. |
| arXiv v2 | SHA `523f3040011cb49048dddbac8f0acebf17bd8a4e9875a9c08231cfb2379eb23d`; source history13December2018; sign convention, scalar formula, approximate iteration/smoothing and numerical enumeration checked. |
| arXiv v3/CWI | SHA `e65aa0919a97a9e1634b2a14c8dfe56d8c92d009e853321b02d6a1bc5feea4ac`; source history15December2020; CWI exact byte match; §§II, III, IV and auxiliary-variable Algorithm2 inspected; relevant pages rendered. |
| IEEE version of record, Utrecht repository | SHA `6d9ae82c92c0c06a396a1297be6ed744250f0fa2fd12037864ad015d1d5a4915`; printed §II/scalar on3, numerical §III on5; only Algorithm1, no v3 Algorithm2; relevant pages rendered. |
| IEEE DOI Crossref metadata | Registration record created9February2019; journal volume6, pages1–11, year2020; no `update-to` erratum field, empty relationship object at retrieval. Metadata is a navigation/chronology aid, not a theorem source. |
| Author BinaryTomo manuscript | SHA `92b5dedea78da7bb351fafc4b9d5a8a2e70db6a015eec8463144187b581fd8c8`; confirms author manuscript matching old scalar/approximate discussion rather than a universal recovery proof. |
| Author code | Pinned commit `db4965de499981be13ddf7a979f1cd0e9e1fd51f`; `test_tomo_cvx.m` and `bin/getA.m` inspected; full25-commit history retrieved, latest18January2023; all-state issue list empty. No code executed. |
| Ferudun primary paper, source ZIP, metadata, verification report | PDF SHA `b374bbc76792418e60fa96a329a5ae6b6f5e596b12b5572b69466d6467bab43b`; ZIP SHA `a1649a1c96877ba7ef9cee94817509cbc6e2a7c9c3762a2d9bd1f06e05e32310`; verification SHA `d21284beda94c727ec1c72e5610446bd09ab9b91000e2be1247ac7bb7ccd3362`; metadata hashes match downloads. Lemma2.1, Proposition2.2, Theorems4.1/4.2/4.6 inspected; independent exact checks of5×5 and explicit4×4 witnesses. Broader solver/central-path claims not independently adopted. |
| Ferudun DOI DataCite metadata | SHA `caf292e9df24b0e5187a7f5c2572765293622a2fd58993cfc2da533545e95d04`; DOI10.5281/zenodo.23110494 `findable`, registered/created/updated2October2026 at20:09:16Z; version1.0. Positive chronological evidence of pre-existing explicit theorem. |
| Fishburn–Schwander–Shepp–Vanderbei1997 | Author-hosted PDF SHA `b19ec9544ae0ce9e80e0b8a3ada6e2d90717eda90dc0c73c911c6ad45c586cd9`; Theorems2–4 at printed47/PDF9 visually checked; old binary-vs-fuzzy uniqueness and nonadditivity theory distinguished from later conjecture. |

## Frozen catalogue retrieval

Full catalogue revision `372682f27c1b0d3d39e75fa63ad7932c7a2e1bde` independently downloaded:69,291,427bytes, SHA `37067f43734b76ee886b032469836767c34d892de14397ce6aa71da01500e252`. Exact target record was isolated; adjacent duplicate records002/004 are retained separately in the extraction. The target clean/current statement inserts an exact-minimizer formulation, while its original statement only asks about the proposed dual approach. Catalogue openness/verification labels are metadata, not mathematical evidence.

## Citation-neighborhood screening

OpenAlex work `W2905465750` and all13 indexed citing works were retrieved. Titles/metadata/abstracts were screened for corrections, recovery theorems, or discussion of this conjecture. OpenAlex is discovery metadata only. No indexed citation is accepted as mathematical evidence without its primary text; none was needed for the positive priority duplication.

- Binary photoacoustic tomography for improved vasculature imaging (2021), DOI10.1117/1.jbo.26.8.086004.
- Compressed sensing-based image reconstruction for discrete tomography with sparse view and limited angle geometries (2025), DOI10.1371/journal.pone.0327666.
- Level-Set Method for Limited-Data Reconstruction in CT using Dictionary-Based Compressed Sensing (2023), DOI10.1109/ICCAE56788.2023.10111292.
- Binary Tomography Reconstruction with Limited-Data by a Convex Level-Set Method (2022), DOI10.32604/cmc.2022.029394.
- New Level-Set-Based Shape Recovery Method and its application to sparse-view shape tomography (2021), DOI10.1145/3506651.3506655.
- Novel regularization method for diffuse optical tomography inverse problem (2022), DOI10.1016/j.ijleo.2022.169095.
- Proximal Algorithms for a Class of Abstract Convex Functions (2025), DOI10.1007/s11228-025-00743-9.
- Properties of SAT Formulas Characterizing Convex Sets with Given Projections (2022), DOI10.1007/978-3-031-19897-7_13.
- A novel dual-based ADMM to the Chan-Vese model (2023), DOI10.1007/s11042-023-14707-4.
- CoShaRP: a convex program for single-shot tomographic shape sensing (2021), DOI10.1088/1361-6420/ac1776.
- Supervised Reconstruction for Silhouette Tomography (2024), DOI10.2352/EI.2024.36.5.MLSI-298.
- A level-set structural approach for multi-physics joint inversion using full-waveform and gravity data (2025), DOI10.1088/1361-6420/ae16cf.
- Some Strategies Addressing Non-Convex Variational Problems in Image Processing (2024), DOI10.70675/c691699ez1b0fz4434zb6fcze27db8bf447c.

## Access limits and caution

The web reader failed on DOI redirects, some PDF screenshots, the old author PDF, and the Utrecht PDF. Direct HTTP succeeded for the relevant PDF and metadata reading copies. Zenodo HTML/API were403 and were not bypassed; independently available DataCite metadata establishes DOI registration. Kadu's thesis PDF returned403 and was not read. The author-hosted paper/source ZIP and metadata are public but are not peer-review certification. The exact prior lemma and checked constructions, not the author's verdict or numerical run totals, ground this audit.

A bounded negative erratum search cannot establish novelty. The strong conclusion is a positive theorem match with a dated public DOI and independently verified mathematics. No Russian/Hungarian literature or paywalled whole-citation corpus was exhaustively audited.
