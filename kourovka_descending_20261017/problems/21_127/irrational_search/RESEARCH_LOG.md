# 21.127 irrationality route research log

## 2026-10-24T20:40:03.231304+00:00 — exact target and independent mechanism selection

Goal: exhibit a finite graph Gamma and explicit g in [A(Gamma),A(Gamma)] with rigorously irrational scl, or record exact barriers after substantial independent effort. Estimated completion toward a complete negative solution: 2%. No solution or originality claim.

The original Notebook statement was checked in the source contract at ../priority/SOURCE_CONTRACT.md. This route starts independently of the finite LP and graph-decomposition families. Primary initial sources: Zhuang arXiv:0710.0026v1; Fournier-Facio--Lodha arXiv:2110.06286v2; Servatius, Automorphisms of graph groups, J. Algebra 126 (1989), 34--60, DOI 10.1016/0021-8693(89)90319-0.

Approach families selected: (1) transplant known irrational rotation-scl examples through special/RAAG embeddings or retractions; (2) quotient/Rips constructions with a genuine scl-transfer theorem; (3) irrational circle dynamics or a self-similar word/surface mechanism directly inside a RAAG. Subgroup inclusion alone gives only an upper bound for ambient scl. Quotients give only a lower bound for lifts. Neither one-sided inequality is an irrationality certificate.

## 2026-10-24T20:42:25.315099+00:00 — two transplant obstructions and a direct dynamics diagnostic

Estimated completion toward a complete negative solution: 4%. The centralizer projection separates every nontrivial central element from the rational commutator subgroup of its centralizer; this excludes the full golden-ratio Thompson lift and every finite-index subgroup. Infinite roots similarly exclude the full Zhuang lifts and all their finite-index subgroups. An independent adversary is checking both proofs and primary sources. A general finite-index lemma initially omitted the infinite-order hypothesis on the central element; this has been repaired, and both intended applications had infinite-order translations from the outset.

A separate explicit construction on F_2 gives [f,g] equal to rigid translation sqrt(2)/100 while the abstract word [a,b] has scl=1/2. Thus irrational dynamics on a RAAG word cannot itself solve the problem. The missing ingredient is an extremal quasimorphism with a matching exact surface upper bound. Written in DYNAMICAL_IRRATIONALITY_FILTER.md.

## 2026-10-24T20:49:04.843248+00:00 — route barriers reproduced and source provenance frozen

Estimated completion toward a complete negative solution: 3% (revised downward because the transplant mechanisms are excluded and no eligible irrational-scl candidate remains). The original negative research goal is unchanged. Primary PDFs and SHA-256 values were cached for Zhuang, Fournier-Facio--Lodha, Servatius' centralizer theorem as stated precisely by Charney, the 2026 Fournier-Facio Rips-limit construction, and Calegari--Walker's scl-distorting free-group inclusions. Raw source texts/PDFs are source material, not research conclusions. The 2026 Rips paper's main theorem has a nontrivial perfect normal subgroup with vanishing scl; no special or RAAG embedding of the limit is asserted, and an actual nontrivial zero-scl commutator would preclude one.

CENTRALIZER_OBSTRUCTION.md passed an independent adversarial review after explicitly requiring infinite order and m!=0 in its general finite-index persistence lemma. DYNAMICAL_IRRATIONALITY_FILTER.md passed after declaring the commutator/function-composition convention. The exact finite covering sanity script checked 100 odd degrees n=1,...,199 and 10,000 permutation points, with no failures; this bounded computation supplements the all-odd algebraic covering proof and is not evidence for general RAAG rationality. The actual rotation defect is only bounded alpha<=d<=1, and no extremality or irrational scl ratio is claimed.

A further concrete finite-index inclusion H<=F(a,b), index3, has a genus-two boundary word whose realization fails the deck-invariant symplectic intersection condition. A prior Calegari--Walker theorem then forces strict scl decrease under this inclusion. This supplies an explicit illustration that passing through a special finite-index subgroup does not silently preserve each element's scl. A fresh delta review is checking this deduction and the transfer/limit scope notes.

Unsuccessful remaining mechanism: directly realize a fixed finite RAAG word by surfaces whose efficiency converges to an irrational number and certify a matching extremal quasimorphism. Merely an irrational circle rotation, a substitution eigenvalue, an irrational coefficient on a real chain, a limit of different rational words, or an irrational quotient value does not establish such equality. No mechanism overcoming these gaps was found.

## 2026-10-24T20:52:22.634739+00:00 — final negative-route checkpoint

Independent adversarial final delta review passed all four current proof/scope artifacts, with no substantive objection outstanding. Parent readback matched all eight target/review-artifact hashes in the final delta manifest. The explicit finite-index example also passed an independent boundary-count obstruction; the supporting matrix JSON's row/column label was corrected without changing its exact arithmetic. No exact smaller ambient scl value is claimed. Review completion: 100% of these partial artifacts. Estimated completion toward a complete negative solution: 3%.

Family outcome remains unsolved, complete_solution=false, apparently_original_solution=false, publication_gate_open=false. No outreach, version-control change, Zenodo action, spreadsheet mutation, or publication preparation was performed. Authored work and reproducibility/review metadata are ready for the root research checkpoint. Full-solution effort can only resume upon a materially new equality/extremality mechanism; no existing audited barrier is represented as resolving 21.127.
