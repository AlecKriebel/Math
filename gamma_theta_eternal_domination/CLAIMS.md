# Claim Registry

Every mathematical or computational assertion must use exactly one status:
`PROVED`, `CERTIFIED-FINITE`, `OBSERVED`, `CONJECTURED`, or `REFUTED`.

| ID | Status | Claim | Evidence |
|---|---|---|---|
| C-000 | OBSERVED | Campaign scaffolding and resource limits were recorded on 2026-07-25. | `STATE.md`, local system queries |
| C-001 | PROVED | For every nonempty finite simple graph, \(\gamma\leq i\leq\alpha\leq\gamma^\infty\leq\theta\) in the one-guard model. | `math/reductions.md`, Theorem 2; accepted by `reviews/reductions_hostile_review.md` |
| C-002 | PROVED | If \(\gamma=\gamma^\infty\), then \(\gamma=i=\alpha=\gamma^\infty\), and the graph is well-covered; well-coveredness alone is insufficient. | `math/reductions.md`, Corollaries 3–4 and \(K_{3,3}\) warning; hostile review accepted |
| C-003 | PROVED | \(\gamma\), \(\gamma^\infty\), and \(\theta\) are additive over components; hence any counterexample has a connected counterexample component. | `math/reductions.md`, Proposition 5 and Corollary 6; hostile review accepted |
| C-004 | PROVED | Relative to the Strong Perfect Graph Theorem, every counterexample contains an induced odd hole or odd antihole. | `math/reductions.md`, Proposition 7; hostile review accepted |
| C-005 | PROVED | One-guard eternal domination is monotone on induced subgraphs: \(H\leq_{\rm ind}G\Rightarrow\gamma^\infty(H)\leq\gamma^\infty(G)\). | `math/reductions.md`, Lemma 8; hostile review plus 32,767 induced-pair tests per evaluator |
| C-006 | PROVED | Relative to the Strong Perfect Graph Theorem, \(\alpha=\gamma^\infty=2\Rightarrow\theta=2\); therefore every counterexample has common parameter \(k\geq3\). | `math/reductions.md`, Lemma 9, Theorem 10, Corollary 11; hostile review accepted |
| C-007 | CERTIFIED-FINITE | Both independent evaluators reproduce all 56 MMV (2022) Table 9 graphs: 56 have \(\gamma^\infty<\theta\), 55 have \(\alpha=\gamma^\infty<\theta\), and none has \(\gamma=\gamma^\infty<\theta\). | `instances/mmv2022_table9.csv`, `results/mmv2022_parameters.csv`, `results/logs/mmv2022-validation.json`, manifest ART-001–003 and ART-016–017 |
| C-008 | CERTIFIED-FINITE | Evaluators A and B agree on all parameters and the greatest eternal family at every \(k\) for 1,100 labeled graphs through order 5 and 1,000 deterministic random graphs of orders 6–10. | `results/logs/differential-day1.json`, manifest ART-004 |
| C-009 | CERTIFIED-FINITE | On all 21 connected unlabeled graphs of order 5, the evaluators reproduce the MMV Table 7 counts and find no graph with \(\gamma^\infty<\theta\). | `results/logs/unlabeled-n05-r00-of-01.json`, manifest ART-005 |
| C-010 | PROVED | If an eternal \(k\)-family exists, every independent \(k\)-set belongs to every such family. Consequently, if \(\alpha=\gamma^\infty\), every maximum independent set is secure; failure at one maximum independent state gives a checkable proof that \(\gamma^\infty\geq\alpha+1\). | `math/lemmas/maximum_independent_states.md`; accepted by `reviews/private_lemma_hostile_review.md`, manifest ART-014 |
| C-011 | CERTIFIED-FINITE | On all 12,113 connected unlabeled graphs of orders 1 through 8, evaluators A and B agree on all five parameters and the greatest eternal family at every \(k\), and none has \(\gamma^\infty<\theta\). | `results/logs/unlabeled-n01-r00-of-01.json` through `unlabeled-n08-r00-of-01.json`, manifest ART-005 and ART-007–013 |
| C-012 | CERTIFIED-FINITE | Every one of the 56 MMV (2022) Table 9 graphs has \(\theta=4\), witnessed by a direct four-coloring of its complement and an independently replayed exhaustive trace proving that its complement is not three-colorable. | `certificates/mmv2022_theta_k3/`, `results/mmv2022_theta_certificates.csv`; hostile review accepted, manifest ART-016–018 |
| C-013 | PROVED | For \(H=\overline G\) with \(\omega(H)=3\), \(\gamma(G)=3\) exactly when every vertex pair of \(H\) has a common neighbor, and the entire one-guard game translates to externally uncontained triples closed under nonedge moves. This gives an exact complement-side \(k=3\) synthesis target. | `math/lemmas/complement_k3_dictionary.md`; accepted by `reviews/complement_k3_hostile_review.md`, manifest ART-019 |

No claim above resolves the \(\gamma\)–\(\theta\) conjecture. Claims C-007–C-009
and C-011–C-012
are finite validation results, not universal proofs.
