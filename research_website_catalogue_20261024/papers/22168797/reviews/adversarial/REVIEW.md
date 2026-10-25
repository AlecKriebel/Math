# Independent adversarial review — Zenodo 22168797

**Verdict: DEFER — a demonstrated false rank-exclusion certificate in the load-bearing finite classification.** No repair was attempted. This is a counterexample to a claimed certificate and to the associated exhaustive exclusion census, not a counterexample to the ultimate classification statement.

## Exact scope and inputs

Reviewed the entire published 26-page article, *Generic Identifiability and Directed Containment for Strongly Tree-Child Level-2 Networks under the Kimura Two-Parameter Model: The Principal Positive Domain and Strict Continuous Time*, and the entire 24-page reader supplement, plus the source definitions and relevant graph, rank, and replay programs. Record version is `1.0.5-r1`.

| Public input | SHA-256 |
|---|---|
| `K2P_SAME_Principal_Domain_Article.pdf` | `e49e72c09183679f04362afe37917e410f0b8b6fe5dc98f423a0b642dce78cf4` |
| `K2P_SAME_Reader_Supplement.pdf` | `0448cfc078f91d0bb5f08097e3055d302e1ef5308664dc3a7443e728f38ffd9d` |
| `K2P_SAME_bioRxiv_Source_20260829.zip` | `66527a3e3018b054f9e6b618a6c9e81a4ddbc6e2d0cced81542a0a7fe3eb3cd3` |
| `K2P_SAME_Reproducibility_Package_v1.0.5-r1.zip` | `477c160057f7a729215dfd37960063d283ddbedcf95396a8239a9fd22e94ac62` |

Fresh public acquisition: <https://zenodo.org/records/22168797>. Reproducibility archive: <https://zenodo.org/records/22168797/files/K2P_SAME_Reproducibility_Package_v1.0.5-r1.zip?download=1>. All seven public files were rehashed against the final acquisition receipt; all match (`inputs-final.json`). Sources were not changed. Execution used a separate ignored copy in this review's `cache/replay/`.

The claim being tested is the paper's classification of regular analytic physical containment on the principal positive Fourier domain, and its strict continuous-time restriction, for binary standard semi-directed strongly tree-child level-2 networks. It is not a claim of pointwise topology recovery at every parameter, complete-image equality after triangle redirection, or mixed-sign K2P identifiability.

## Demonstrated defect

The corrected four-port ledger contains this exact row:

```text
raw_id                  137124
source_index            2
target_index            85
port_permutation        [2, 0, 1, 3]
permutation_index       12
corrected_category      exact_rank_exclusion
exact_reason            target_exact_generic_rank_below_source
source_exact_rank       14
target_exact_rank       13
source_descriptor_sha256 8a795f76a04840e74315dc94c7e02b0f34e7a9a2dcf4b228d9c002f8994c09d9
target_descriptor_sha256 3f004717bc11a6dd75c778d0d1be0a9e2ac3577f8df865ec0175b6181651089d
```

Archive-relative path:
`k2p_same_reproducibility_v1.0.5-r1/work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_ledger.jsonl.gz`.
Its SHA-256 is `7cf3f953fca695d612387143818843650498f84f55cf0a776f90c9afdd95eef6`, the same hash printed in reader §11, p21. The complete extracted row and its exact lower/upper-certificate bindings are retained in `suspect-rank-row.json` and `rank-exclusion-counterexample.json`.

**This row is not a valid exclusion. Its source and target are labelled mixed-graph isomorphic.**

### Explicit graphs and transport

The source is the article's `theta1` core with minimum repair `{2,3}`. Write `P2` and `P3` for its port-bearing subdivision vertices. Its rooted arcs are

```text
r→S, r→L0, S→U, S→X,
V→P2, P2→X, P2→L1,
U→P3, P3→V, P3→L2,
U→V, X→L3.
```

The target is `theta0` with minimum repair `{2,3}`. Before the row's port permutation its rooted arcs are

```text
r→S, r→L0, S→U, S→V,
U→P2, P2→X, P2→L1,
V→P3, P3→X, P3→L2,
U→V, X→L3.
```

In both, `V,X` are the reticulations. Apply the target port permutation `0→2, 1→0, 2→1, 3→3`, suppress `r` once, and retain precisely the heads entering `V,X`. The following target-to-source map is a labelled mixed-graph isomorphism:

| Target vertex | Source vertex |
|---|---|
| `S` | `P3` |
| `U` | `U` |
| `V` | `V` |
| `X` | `X` |
| `P2` | `S` |
| `P3` | `P2` |
| each already-permuted `Li` | the same `Li` |

For complete checkability, these are all eleven target mixed edges and their images (`--` denotes ordinary, `→` a retained head):

| Target after port permutation | Source image |
|---|---|
| `S--L2` | `P3--L2` |
| `S--U` | `P3--U` |
| `S→V` | `P3→V` |
| `U--P2` | `U--S` |
| `P2→X` | `S→X` |
| `P2--L0` | `S--L0` |
| `V--P3` | `V--P2` |
| `P3→X` | `P2→X` |
| `P3--L1` | `P2--L1` |
| `U→V` | `U→V` |
| `X--L3` | `X--L3` |

The independent reproduction verifies every edge and head, injectivity and surjectivity, and the labels. It then compares the independently built rooted edge lists with the published compiler's source 2 and target 85, so this is not a mistaken association of the raw indices.

Both are admissible members of the theorem's class. They are simple and binary, each has one theta blob with two reticulations, and their chosen repairs occur in the printed minimum-repair table. Each retained-arrow tail has two ordinary incidences. An independent enumeration of every edge-root position and ordinary-edge orientation finds **seven admissible rootings, all seven tree-child**, for each graph. Root degree, all vertex bidegrees, acyclicity, and the lowest-stable-ancestor condition are explicitly checked.

### Why this contradicts an open-germ exclusion

This is stronger than an isolated coincidence of tensors. The map is an isomorphism of the same standard semi-directed network, with only the admissible root location changed. The source's suppressed root lies on its `S--L0` edge; the target's suppressed root maps to the source's `P3--L2` edge. Both are ordinary pendant edges.

For any strict interior source parameters, multiply its two root-arm spectra to get the effective mixed-edge spectrum, transport every effective mixed edge and reticulation-parent probability by the displayed isomorphism, and split the new root edge strictly. A fixed split factor sufficiently near `(1,1)` makes the residual factor physical throughout a neighborhood, as in the article's Lemma3.1. Multiplication and division give an analytic target section. Reversibility of each displayed-tree K2P kernel gives equality term by term in the switching sum. The same construction works in strict continuous time. The reverse transport is identical in principle.

The polynomial source map has regular points in its open physical parameter domain. Choose one and shrink around a nonzero maximal minor. The transport above remains physical and analytic there. Therefore the required regular source-relative containment exists; passing to the article's incidence quotient preserves it. There is no assumption that one particular numerical collision is generic.

As a supplementary exact control, `rank_exclusion_counterexample.py` assigns distinct rational strict-CT pairs to every mixed edge, splits the two different root edges, matches reticulation weights by the edge map, and checks equality of **all 64 conservation-supported four-leaf Fourier coordinates**. All 38 counterexample checks pass. This finite check corroborates, rather than replaces, the analytic transport argument.

## Mechanism: an arm-fixed rank was used for an incidence-quotient relation

Main p9 defines the local relation for complete factors using a slice of the action of one positive paired-sector and one positive singleton-sector scale at every port. Main pp8–9, Theorem4.2/Lemma4.3, also explains the physical role of these incidence scales. This quotient is not obtained by simply deleting all pendant parameters from a rooted presentation.

The compiler's `model_descriptor_fast2` in
`package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py`
sets `arms=selected_arm_edges(G)` at line495, omits them from `esec` at line506, and skips them again at line523. Its Jacobian is therefore for the map with selected pendant factors fixed to one, before taking the required quotient. The fixed-arm images of two different rootings need not have the same dimension.

The checker `work/corrected_composite_ledgers/verify_corrected_composites_independent.py`, lines294–312, compares those descriptor ranks and returns `exact_rank_exclusion` immediately when target rank is lower, before an isomorphism can terminate the row. The producer has the same comparison at `work/raw_ledger_audit/generate_raw_ledger.py`, lines232–245. Their file hashes are recorded in the verdict.

Fresh symbolic differentiation of the full switching formula from the printed graphs, without importing the published compiler, gives:

| Presentation | Evaluated internal-only Jacobian rank | Evaluated Jacobian rank with all pendant parameters | Rank after removing the eight-dimensional port-scale tangent space at this point |
|---|---:|---:|---:|
| source2, `theta1 {2,3}` | 14 | 17 | 9 |
| target85, `theta0 {2,3}` | 13 | 17 | 9 |

These are exact rational **pointwise** ranks, not a claim that sampled ranks by themselves prove global rank upper bounds. The invariant conclusion that the full physical generic ranks agree follows from the analytic graph transport. The numerical rank comparison's interpretation is the error, not a failure of rational matrix arithmetic.

The first program used distinct rational interior edge and inheritance values and retained all root/pendant factors for the full Jacobian. The results for all six four-port printed source supports and their mixed-graph transports are in `rank-gauge-controls.json`. No finite count is used as proof of an infinite-family theorem.

## Exactly what is affected

1. **Main §6.2, p14:** termination type(ii), the directed rank exclusion, is applied to a map whose rank does not certify the declared projective physical relation.
2. **Main Theorem6.3, pp15–16:** the claim that every finite obstruction is valid and the stated exact partition including 23,822 directed rank exclusions are false as certified; row137124 is an explicit counterexample. This also prevents accepting the claimed exhaustive support/equality-anchor coverage without further work.
3. **Reader §4 p5 and §§5–6 pp6–8:** the advertised rank implication and consequent finite classification/equality-anchor censuses do not resolve this counterexample.
4. **Main Theorem7.3 p18, Theorem8.1 pp19–20, Theorem9.1 pp20–21, and Corollary10.1 p21:** their proofs depend on the finite classification, so these broad conclusions are not cleared by this review.

The example is an isomorphic pair, so it is fully compatible with the *statement* of Theorem6.3/7.3. It invalidates the submitted proof object rather than furnishing two inequivalent strong networks with a common germ. The main theorem's truth is unresolved here. No replacement rank mechanism, repaired ledger, or repaired theorem was developed.

## Strongest positively verified material

Before inspecting published mathematical code, `independent_controls.py` ran 28 exact checks derived from the manuscript:

- inverse Fourier probabilities and the distinct principal/strict-CT domains; an interior principal-domain point demonstrates why naive square-root subdivision is invalid;
- the pair-anchor exponent determinant for degrees3–10, together with the hand argument extending the construction to arbitrary degree;
- the whole-map tree/sunlet polynomial identity;
- the ordinary triangle's common strict-CT tensor and an independently differentiated rank-nine Jacobian;
- both weak-class graphs' complete rooting censuses `(5,2,3)` and `(7,2,5)`, their exact common tensor, and both printed nonzero 9×9 determinants;
- strict-CT inequalities for the weak witness and the independently calculated primitive completion counts and raw-direction totals.

The weak-pair computation correctly finds tree-child rootings distinct from the displayed rooted representatives. The manuscript does not incorrectly assert that those particular displayed representatives are tree-child. The cherry extension's analytic inverse recovers its four new edge parameters and the old tensor; the written argument supports the `4n−3` weak-class family independently of the broken finite atlas. Likewise the rank-nine triangle germ and its contextual constant-rank argument are not refuted by the identified defect.

The general physical-domain, subdivision, bridge-fibre, and finite-semialgebraic-cover arguments were read and tested for the obvious boundary and gauge pitfalls. No additional demonstrated defect was found before the stop rule. This is not a blanket certification of every other statement in the paper.

## Replays, references, independence, and limits

The published quick suite was started in this review's isolated archive copy with Python3.12.14, NetworkX3.5, and SymPy1.14.0 (the package permits Python3.10 or newer; the archived qualified run used3.14.6). Initial execution failed only because NetworkX was absent; a dedicated local environment with the declared versions resolved that setup issue. Thirteen layers reported fresh passes before deliberate termination after the independent false-certificate finding. `quick-replay.log` and `quick-replay-stop.json` preserve the exact scope. **No whole-suite or full primitive replay pass is claimed.** In particular, the remaining direct-polynomial, complete rank, restoration, and probe layers were not cleared. The defect is established by the exact published row and graph transport regardless of whether those programs reproduce their recorded outputs.

Primary-reference interfaces checked: Englander etal. version4, Definitions2.1–2.2, the strong-tree-child convention, Propositions2.9–2.10, Theorem2.11, and Corollary2.12; Huber etal., Lemma4.2 and its generator context. These cover the displayed-quartet signs/tree-of-blobs and the two underlying level-2 generator types actually cited. The K2P character renaming is consistent with the present equal sector. Brits etal. version3/date/scope was checked against the primary arXiv record but is background, not a necessary step in this counterexample. The BCR textbook body was not obtained; its standard semialgebraic facts were provisionally accepted rather than independently re-proved. Primary raw-file hashes, URLs and access limits are in `primary-reference-bindings.json`.

No current sibling-review or archived reviewer-report body was read before or after the independent conclusion. The record, article, supplement, and mathematical support necessarily contain historical replay/status claims and historical warnings; these were incidental exposure and were never adopted as verification. Published programs with names containing “audit” or “adversarial” ran as part of the quick suite; their fresh numerical/status outputs are not independent human review. Raw primary-source PDFs supplied by the acquisition agent were used only as publications, not as that agent's opinions. No strict human-blind or formal proof-assistant claim is made.

Only this review directory was written. Original PDFs, ZIPs, extraction, website, renderer, spreadsheet, Git history, Zenodo, and external communications were not modified. Compiled/cache artifacts are ignored. Review completion is100% for the requested stop-on-demonstrated-defect route; the mathematical main claim remains deferred.

## Reproduction

From this review directory, using Python with SymPy1.14.0 and NetworkX3.5:

```text
cache/venv/bin/python independent_controls.py
cache/venv/bin/python rank_gauge_controls.py
cache/venv/bin/python rank_exclusion_counterexample.py
```

The last command expects the unmodified published reproducibility tree at `cache/replay`, copied from the receipt-bound extraction. It generates the exact graph/edge transport, 64-coordinate physical equality control, source/target compiler binding, and false ledger row, without changing a published artifact.
