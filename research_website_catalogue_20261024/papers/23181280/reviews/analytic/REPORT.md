# COMPLETE analytic-family review: Zenodo 23181280

The literal original theorem is supported: aggregate root-dependent spanning-tree cost is NP-complete with costs in {0,1,2}, strongly NP-complete under the stated explicit encoding, and strongly NP-complete with costs in {1,2,3} after the uniform shift. No central reduction defect, counterexample to the stated theorem, or necessary mathematical source correction was found. This is one bounded independent scientific review with checkable proofs and computations, without human peer review, formal certification or publication clearance. The 203-paper catalogue remains ongoing.

The reviewed object is **NP-completeness of aggregate root-dependent spanning-tree cost**, declared October 6, 2026, version 1.0, Full List row 94, [DOI 10.5281/zenodo.23181280](https://doi.org/10.5281/zenodo.23181280). Fresh actual API files were authenticated and frozen before mathematical review. The complete actual four-page PDF, all four page renders and the full controlling TeX were then read before external primary bodies, historical audits, supplied programs or other review opinions. The substantial independent reduction was sealed in `EARLY_DERIVATION.md` and its receipt before those subsequent checks.

## Exact model and supported proof

There is one common undirected spanning tree. Every root induces an orientation of its entire edge set, and every arc in that orientation is charged using that root's independently supplied table. All 2N|E| nonnegative integral entries and the integer threshold are explicitly encoded. This input model is essential; a separate optimized tree for each root or a terminal-path-only objective would be different.

The reduction normalizes at-most-three-literal CNF in polynomial time, explicitly handles empty and absent clauses, and densely relabels occurring variables. It constructs two hubs, one vertex per variable and one per clause. The symmetric t-root table gives every arbitrary tree the identity

`F_t(T) = K + (1-h) + (q-m)`,

where K=n+2m, h indicates the hub edge and q counts clause-variable edges. Since h<=1, q>=m and all remaining root costs are nonnegative, any tree at or below K must contain the hub edge and make every clause a leaf. Acyclicity and connectivity then force exactly one hub attachment per variable. No large unspecified penalty is required: the coefficient two already gives a strict unit structural gap.

These forced trees encode truth assignments and one selected literal per clause. At each clause root, exactly its selected variable's hub edge has the potentially nonzero direction; all other variable hub edges point the zero-cost reverse way. The clause-root cost is therefore exactly the indicator that its selected literal is false. This proves both satisfiability directions for every formula size. It does not equate the unrestricted optimum with a maximum-satisfiability objective, and the manuscript correctly avoids that stronger claim.

The graph has N=n+m+2 and at most 1+2n+3m edges. Its full cost table has polynomial size, entries in {0,1,2}, and K<=2N. A proposed tree can be checked by traversing it from all roots and adding polynomially many binary integers. Thus the proof establishes NP membership, NP-hardness and hardness under unary numerical encoding. Adding one to every cost changes every tree's objective by precisely N(N-1), proving the positive-cost corollary with polynomially bounded threshold. Transposing every table proves equivalence to the inward orientation convention.

## Independent falsification controls

`independent_checks.py` is original review code using only the existing standard-library Python runtime. It independently reconstructs tables, enumerates trees and checks tree counts by an exact matrix-tree determinant. Its 54 formula cases cover 5,752 tree/formula cases. For every enumerated tree it checks two distinct whole-objective evaluators, the unrestricted structural identity, exclusion of unstructured trees, each structured clause-root identity, reduction answers, inward transposition and the uniform positive shift. Sparse labels, repeats, tautologies, empty/no clauses, single literals, duplicate clauses and the single-vertex objective were checked. The final receipt is `CHECK_RESULTS.json`. These are meaningful finite controls, not an NP-hardness proof.

The isolated one-literal orientation control shows why transposition matters: a false-literal structured tree has outward cost 4 at K=3, but simply reversing orientation without transposing the table gives cost 3. A corrupted base cost is also detected. An initial true-literal test was nondiscriminating and was replaced by this false-literal case; no source claim was changed.

The supplied `verify_exact.py` and `run_checks.py` were inspected completely before execution. Only selected checker functions, normalization boundaries, three representative formula cases and two negative guards were executed in an isolated identical clone under normal and optimized Python. Results agreed and the intended guards rejected corruption. No historical program, full supplied replay, build or seal script was executed. `SUPPLIED_SELECTED_REPLAY_RECEIPT.json` records the exact scope and script hash. The supplied current-manuscript binding also matches the actual controlling TeX; historical proof bytes were checked by hash without reading their argument.

Two secondary boundaries received independent derivations. Symmetric root tables reduce the objective to an ordinary edge-additive MST, so the asymmetry in the hard construction is substantive. The paper's warning about the classical joint lift is supported by an exact rational witness: the four-clause unsatisfiable eight-vertex instance has 384 trees, integer minimum 11 and threshold 10, while common fractional edge marginals and root-specific convex mixtures satisfy the joint lift at cost 10. `EXACT_JOINT_LIFT_WITNESS.json` supplies every entry. This verifies a secondary caution; it is not used as the complexity proof or promoted as a separate result.

## Primary interfaces, attribution and limits

The actual EMS report's printed pp.3014-3015 state Kaibel's Problem 1 with precisely the common-tree sum of whole induced root arborescence costs and identify Martin's formulation as motivation. Its Problem 2 instead charges root-to-vertex paths and is outside the manuscript's claim. The workshop dates are November 4-10, 2018; the publisher records December 17, 2019 publication. See [the primary report](https://ems.press/content/serial-article-files/46772?nt=1) and [publisher dates](https://ems.press/journals/owr/articles/16633).

Karp's actual chapter scan was checked visually: the Main Theorem on printed p.94 declares the listed problems complete, and item 11 on p.95 is satisfiability with at most three literals per clause. This is the exact source restriction used in the reduction. The academic-host scan is a primary-body copy; its bytes are authenticated, while publisher-byte equivalence is not asserted. The PDF has no searchable text layer, so local OCR was used for navigation and the two relevant page images were read directly. See [the chapter scan](https://www2.seas.gwu.edu/~simhaweb/champalg/tsp/papers/KarpOriginal.pdf).

The actual Conforti--Cornuéjols--Zambelli February 2010 manuscript, Section 6.1 pp.25-26, and Friesen's actual 2019 dissertation, Proposition 2 p.8, match the cited classical common-edge/root-orientation formulation. The note credits that background and does not claim it as its contribution. See [the author manuscript](https://www.andrew.cmu.edu/user/gc0v/webpub/ExtFor-Feb2010.pdf) and [the dissertation](https://d-nb.info/1219966134/34).

All four primary bodies were accessible as actual local PDFs. Some web-reader/DOI requests failed, including the Karp scan's size limit, but they were not substituted by search snippets. The exact inspected interfaces are recorded in `PRIMARY_INTERFACE_LEDGER.json`. Bounded queries did not establish an earlier resolution; this is not evidence of novelty. The author's October 6 negative-search audit was not independently reproduced. Absolute first discovery, exhaustive earlier coverage and continued open status in 2026 remain **uncertified**.

## Custody and disposition

The actual PDF is 57,772 bytes, SHA256 `f51acb267822dd082fdb28a14bc581b37fc3b3a75008647a3e04fa8a3d84fbf4`. The original support archive is 151,513 bytes, SHA256 `66f7d7e25370062e0f70b7fdce538dc90a5a264957557714f11d1ac42ebc14aa`. Both match their fresh API sizes and MD5 checksums; the full API file objects and real transport facts are preserved. Its 47 canonical unique safe members total 304,697 expanded bytes, pass CRC/member hashing, and contain no encryption or symlinks. The archived and extracted PDF equal the fresh outer PDF. The controlling TeX SHA256 is `a0e7e6158267fbf9ca4cafbd5ccb4cfa4ac79a1e0aea61282c9ee09d7e8d11d5`.

All 59 frozen source bindings and the early derivation bindings were preserved. The previous discotope review packet remains sealed. The declared edition is October 6, 2026 version 1.0; the API record was created October 6 at 06:48:28.773371 UTC and updated October 10. Current authenticated retrieval does not establish first public availability of these exact bytes or priority.

All borrowed fulltexts, extracts, OCR and renders remain wholly in ignored caches. No source repair, historical verdict normalization, configuration, shared-core, site, Sheet, UI, Git, deployment, redirect, release or outreach action occurred. No external communication was prepared or initiated. Root retains synthesis and publication authority.

Bounded analytic-family completion estimate: **100%**. This does not mark the 203-paper catalogue or any broader discovery goal complete.
