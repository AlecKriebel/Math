# Static code/certificate audit of the revised K3P package

Date: 2026-08-27
Audited package: `/Users/alec/Documents/Math/k3p_level2_identifiability_final/release/dist/K3P_Level2_Independent_Referee_Package`
Method: static source and sealed-artifact inspection only. I did **not** execute any package Python, producer, verifier, or mutation runner.

## Executive disposition

The two categorical code findings from the earlier draft are no longer true of the current package.

| Draft finding tested adversarially | Current disposition | Reason |
|---|---|---|
| No active path re-enumerates all 405,216 four-port presentations and independently derives (40=38+2) and fourteen orbits. | **Withdraw.** | The current producer constructs the full primitive Cartesian universe, and a separately imported core/verifier reconstructs every graph, map, exact obstruction, raw row, and quotient. |
| No separate active verifier semantically reconstructs all 574,535 probe rows. | **Withdraw as a categorical finding; retain a boundary qualification.** | `verify_k3p_probes_semantic.py` reconstructs and checks every one-/two-port row, including transports, restrictions, quartet decks, and K3P circuit pullbacks. Its independent boundary starts at the 176 public candidate profiles; upstream locator reconstruction is producer-side, not independently repeated inside this verifier. |

I found no artifact-only omission/reclassification attack that can pass the ordinary full four-port verifier or the full semantic probe verifier with the audited code fixed. The remaining observations below concern independence strength, cross-package boundary wording, and defense-in-depth, not a basis for retaining either obsolete categorical finding.

## 1. Full 405,216-case four-port path is real and active

### 1.1 Raw inputs and producer trace

`proof_package/four_port_atlas/full_universe_replay/generate_full_four_port_replay.py` has one producing input, the bundled pure-Python atlas compiler (`:34-37`, loaded at `:144-150`). The atlas itself contains no file reads or imports of a frozen ledger. The producer then:

1. Constructs six sources, 831 incoming-selected targets, 1,983 incoming-marginalized targets, and all 24 permutations, with hard census checks (`generate_full_four_port_replay.py:324-335`). This is exactly (6(831+1983)24=405216).
2. Traverses every target/permutation in every source lane and independently assigns a topology result (`:338-367`).
3. Compiles every compatible relabelled target map and all source maps (`:370-406`).
4. Regenerates an exact rational nonzero Jacobian minor for every distinct descriptor (`:183-197`, `:409-433`).
5. Builds coefficientwise polynomial vector-field syzygies for targeted generic rank uppers (`:204-321`). The equations encode (J_fV=0) coefficient by coefficient (`:236-275`), and the upper is computed as parameter count minus `rank([A;E])-rank(A)` (`:277-321`). A sampled Jacobian rank is therefore used as a lower bound only.
6. Searches exact target-vanishing/source-nonvanishing quadratic pullbacks and exact transported (H_{14}) quartics (`:474-605`, `:608-772`).
7. Reconstructs labelled isomorphism, ordinary-triangle, restoration, and residue categories member by member (`:693-750`).
8. Derives the residue from those classifications, demands 40 raw records, builds double cosets, and derives fourteen orbits plus two sink swaps (`:815-956`). No fourteen-orbit artifact is read in this route.
9. Streams a dense raw ledger for every raw ID from 0 through 405,215 (`:959-1019`) and seals all registries and the quotient (`:1118-1173`).

The stored result is consistent with that trace: `full_universe_replay/artifacts/FULL_FOUR_PORT_REPLAY.json` records 405,216 raw rows, 27,834 post-topology rows, 2,540 restoration obligations, 40 residue rows, and fourteen orbits. The stored independent report records the same result at `full_universe_replay/INDEPENDENT_FULL_FOUR_PORT_VERIFICATION.json:35-48`.

### 1.2 Separate semantic verifier

`proof_package/four_port_atlas/full_universe_replay/verify_full_four_port_replay.py` imports only `independent_replay_core` (`:22`), not the producer or atlas. Its active full path:

- verifies compressed/uncompressed artifact envelopes and exact schemas (`:68-140`);
- reconstructs all primitive graphs and all 405,216 topology decisions (`:172-201`);
- recompiles the 13,686 compatible keys and 4,379 distinct descriptors (`:204-232`);
- recomputes every rational rank minor and every targeted syzygy upper, including a nonzero evaluation-image minor (`:235-291`);
- reconstructs every eligible map class, quadratic/H14 certificate, labelled graph relation, and raw binding (`:330-431`);
- reconstructs and compares every raw ledger row, with explicit early-EOF and trailing-row failures (`:434-488`);
- derives the forty-row quotient and all double cosets from the reconstructed residue (`:496-590`); and
- compares the derived quotient exactly to the sealed quotient (`:858-876`).

The independent core supplies its own five-core grammar (`independent_replay_core.py:32-51`), completions (`:107-224`), restrictions/topology (`:237-379`), switching Fourier compiler (`:382-507`), exact quadratic algebra (`:510-651`), exact Jacobian minors (`:654-768`), coefficientwise syzygy upper (`:775-888`), mixed-graph relations (`:891-972`), and (H_{14}) pullbacks (`:979-1040`). Thus this is not a hash-only or census-only replay.

### 1.3 Exact-rank and polynomial boundary

The rank argument is sound for the way it is consumed. A source point minor supplies a generic lower bound; a target vector-field span supplies a generic upper bound. A rank exclusion is made only when the independently reconstructed target upper is strictly below the source lower (`verify_full_four_port_replay.py:343-351`). The verifier also reconstructs a nonzero minor of the evaluated syzygy image (`:270-286`).

Terminology should remain precise: `rank_certificate` computes the exact rank of one exact rational Jacobian evaluation, which by itself is a **generic lower bound**, not a generic-rank equality. The upper registry is generated only for target descriptors encountered with a smaller point rank (`generate_full_four_port_replay.py:635-643`), not universally for all 4,379 maps. This does not invalidate any rank exclusion, and the package's own proof-boundary text correctly says so (`full_universe_replay/PROOF_BOUNDARY.md:25-49`). It would be an overstatement to call every number in `exact_rank_minor_registry` a separately proved exact generic rank.

The polynomial tests are genuinely coefficientwise:

- quadratic target kernel and source nonzero pullback: `independent_replay_core.py:631-650`;
- transported (H_{14}) target zero and source nonzero pullback: `:1017-1039`;
- producer strict rational physical evaluations: `generate_full_four_port_replay.py:444-482`, `:582-604`.

## 2. The all-574,535-row semantic probe replay is real

### 2.1 Coverage and row semantics

`proof_package/probes/verify_k3p_probes_semantic.py` expressly imports neither the producer nor atlas (`:1-13`); its only nonstandard import is NetworkX (`:37`). It reconstructs:

- rooted graphs from the public site profiles (`:146-205`);
- every mixed-edge insertion and exact marginal restriction (`:208-269`, `:581-614`, `:1203-1219`);
- labelled mixed-graph transports, incidence, labels, and arrowheads (`:421-509`);
- complete displayed-switching quartet decks (`:616-696`);
- literal three-sector K3P switching descriptors and sparse coordinate maps (`:699-925`);
- row-specific tree/sunlet circuit decks (`:928-1005`); and
- canonical equality relation classes and reversed marginals (`:1076-1134`, `:1884-1941`).

It first rebuilds and checks all 176 anchors and all candidate sites (`:1544-1632`). It then consumes exactly one stored row for every source-site/target-site pair in the 29,964-row one-port Cartesian product (`:1634-1764`), reconstructs all 2,107 retained parent profiles (`:1766-1812`), and consumes exactly one stored row for every pair in the 544,571-row two-port universe (`:1814-1976`). Both streams fail on early EOF or trailing rows (`:1659-1662`, `:1751`; `:1839-1842`, `:1962`). It also requires every transport, restriction, quartet proof, and tree-sunlet proof registry item to have a semantic consumer (`:1978-1985`).

The stored report confirms 29,964 + 544,571 = 574,535 rows and lists 67,741 transports, 4,379 restrictions, 638 quartet certificates, 675 tree-sunlet certificates, and 32,729 reverse marginals (`probes/K3P_PROBE_SEMANTIC_VERIFICATION.json:3-8`, `:33-42`). These are not merely read from a summary: the counters are accumulated in the nested reconstruction loops and compared to the certificate (`verify_k3p_probes_semantic.py:1752-1763`, `:1963-1976`).

### 2.2 Classifier and exact evidence

The semantic verifier enforces the declared classifier order at the evidence level:

- equality rows must occur on transported sites and carry a transport that is revalidated against the reconstructed child graphs (`:1673-1707`, `:1859-1878`);
- quartet rows must occur on incompatible sites and reproduce the first complete switching-deck mismatch (`:1721-1731`, `:1942-1946`);
- tree-sunlet rows must occur only after quartet equality and must recompile the literal K3P three-sector maps and six circuit pullbacks (`:1732-1745`, `:1947-1954`).

The exact tree-sunlet strict-positivity theorem is a separate dependency. The row replay proves tree-circuit coefficientwise zero and sunlet-circuit polynomial nonzero (`:946-1005`) and binds the independently verified v2 separator artifact (`:1524-1531`). The v2 verifier independently re-expands the standard literal map and proves that the six circuits cannot vanish simultaneously (`three_port/literal_separator_v2/verify_literal_separator_v2.py:206-262`, `:265-342`). Therefore the row verifier is semantic, but its pointwise positivity conclusion properly depends on that global theorem and labelled-port transport; it is not reproved from scratch 675 times.

### 2.3 Mutations and fail-closed behavior

The semantic verifier rejects seven coherently resealed or semantic mutations: nonincidence transport, wrong restriction label, false quartet, false six-circuit deck, incomplete site profile, altered transport-scope claim, and mixed-sign Bernstein data (`verify_k3p_probes_semantic.py:1319-1451`). The older streaming mutation suite separately exercises omissions, wrong parents, missing root sites, reverse order, transport corruption, registry omissions, optimized mode, and hash-seed stability (`probes/test_k3p_probe_mutations.py:217-363`, `:365-425`).

All principal paths refuse optimized Python before relying on any assertion behavior:

- four-port producer: `generate_full_four_port_replay.py:1022-1025`;
- four-port verifier: `verify_full_four_port_replay.py:823-825`;
- semantic probe verifier: `verify_k3p_probes_semantic.py:1454-1456`;
- integrated theorem gate: `reproducibility/verify_k3p_same_classification.py:1446-1449`.

Unknown probe statuses are fatal (`verify_k3p_probes_semantic.py:1746-1747`, `:1955-1956`), and the main exception boundary exits nonzero (`:2043-2050`).

## 3. Active-plan integration

The current plan is **not a 44-command plan**. `referee_tools/ACTIVE_VERIFIER_PLAN.json:46-55` declares 54 original regeneration commands, one nonmathematical exclusion, and 53 mathematical commands. The phrase at `:111` is explicitly a historical “reference prior 44-command runtime.” Any present-tense report that calls the current active plan “the 44-command plan” should be corrected.

The 53-command order includes the literal separator build/verify/mutations, full four-port producer, restoration producer/verifier/mutations, four-port structure comparison/mutations, hour-scale probe producer, fast probe verifier, full semantic probe verifier, and probe mutations (`ACTIVE_VERIFIER_PLAN.json:83-109`). The concrete commands appear at `proof_package/reproducibility/run_release_suite.py:212-258`.

One apparent trap is not a gap: the immediate post-producer four-port command is only `--structure-only` (`run_release_suite.py:233-241`). The same regeneration sequence ends with `integrated_fresh_independent_replay` (`:278-281`), and that integrated gate freshly invokes the **full** four-port verifier (`verify_k3p_same_classification.py:1303-1320`) and the **full** semantic probe verifier (`:1357-1380`). The ordinary portable verify phase also invokes the integrated fresh replay (`ACTIVE_VERIFIER_PLAN.json:25-34`).

The integrated report requires fourteen fresh child checks to pass and binds their payloads (`referee_tools/run_active_verifiers.py:336-363`). The copied-workspace runner runs package integrity first (`:445-477`) and rejects any non-ephemeral workspace drift (`:366-422`). Thus the active theorem consumer is not relying only on stored PASS JSON.

## 4. Residual red-team findings and hardening opportunities

### 4.1 Independence is implementation separation, not algorithmic diversity — assurance qualification

The four-port verifier truly does not import the producer or atlas. However, `independent_replay_core.py` is a close, readable reimplementation of the same construction: compare its core table (`:32-51`) with `input_frozen/k3p_cloud_artifacts/k3p_atlas_core.py:11-42`, completion grammar (`independent_replay_core.py:182-224` versus atlas `:141-182`), topology reduction (`:237-379` versus atlas `:355-472`), and map compiler (`:432-507` versus atlas `:474-535`). This is enough to defeat stale artifacts and producer-only bugs, but a shared conceptual or transcription error can survive both implementations.

Recommendation: describe the result as a “separate no-import exact replay” rather than an algorithmically independent derivation, or add a genuinely different compiler/canonicalizer for selected exhaustive cross-checks. This qualification does **not** restore the obsolete “no active replay” finding.

### 4.2 The standalone semantic probe boundary begins at public profiles — scope qualification

The semantic verifier validates the frozen contract and stored input-replay payload/status (`verify_k3p_probes_semantic.py:1495-1508`) and then reconstructs graphs from the contract's public candidate profiles. It does not itself replay every anchor locator from the raw four-port, theta2, and cycle inputs.

That upstream reconstruction exists in the active producer: `regenerate_k3p_probes.py:1672-1784` reconstructs each origin from raw inputs, and `:1786-1812` checks graph hashes, exact relations, transports, and complete site profiles. The new four-port verifier also cross-checks 43 four-port anchor locators against its derived raw rows (`verify_full_four_port_replay.py:661-684`). But the semantic verifier's own independence claim should remain conditional on the 176 public profiles, exactly as its stored report says (`K3P_PROBE_SEMANTIC_VERIFICATION.json:10-14`).

Recommendation: add an active no-producer anchor-origin verifier for all 176 locators, or state this conditional boundary wherever “all-row independent replay” is summarized. The 574,535 child rows themselves are semantically replayed.

### 4.3 Standalone four-port handoff wording is stronger than its local checks — low/medium hardening

The full four-port verifier does substantial semantic crosswork: it derives 2,540 restoration presentations, matches their presentations bijectively to forest roots, checks 36,568 first-layer rows and proof-kind counts (`verify_full_four_port_replay.py:593-653`), and matches 43 probe raw locators/categories (`:661-684`). But its final checks of the stored restoration and semantic-probe reports are only status/count-field checks (`:654-659`, `:685-692`); it does not verify those reports' payload seals or bind their file hashes in its own report.

The integrated fresh gate closes this in the active theorem path by freshly running both verifiers and comparing fresh/stored payloads (`verify_k3p_same_classification.py:1303-1394`). Therefore this is not a final-gate bypass, but the standalone report sentence that “every restoration/probe handoff is actively bound” (`INDEPENDENT_FULL_FOUR_PORT_VERIFICATION.json:35`) should be read as integrated, not self-contained.

Recommendation: verify the dependent reports' payload seals and source hashes locally, or include their hashes in the four-port report bindings.

### 4.4 Transport bijectivity is implicit in current graph cardinalities — defense in depth

`validate_transport_on_graphs` requires complete source and target vertex/edge coverage and a function on source rows (`verify_k3p_probes_semantic.py:455-475`), then checks incidence and arrowheads (`:482-509`). It does not explicitly require unique target images or equal source/target cardinalities. With the audited rows, paired graphs arise from equal-size related parents and symmetric insertions, so coverage plus cardinality makes the map bijective; I found no current row exploiting this. A coherently forged profile with unequal cardinalities could, in principle, attempt a many-to-one labelled graph morphism.

Recommendation: add explicit equal-cardinality and injective-image checks for vertex and edge maps, and add a coherently resealed folding mutation.

### 4.5 Mutation suites are useful but not exhaustive — no correctness downgrade

The full four-port mutation suite uses a structure-only clean baseline (`test_full_four_port_mutations.py:194-203`) and five focused coherent mutations plus optimized mode (`:204-229`). It does not directly mutate a quadratic coefficient, an (H_{14}) term, a graph grammar primitive, or an entire syzygy equation. The semantic probe mutations similarly use one selected witness of each semantic kind. This limits what can be inferred from “mutation PASS,” but it is not a verifier gap: the ordinary full paths reconstruct and compare every relevant class/row/pullback.

Recommended additions are coherent quadratic/H14 coefficient mutations, a deleted syzygy equation with all outer seals updated, a folded transport as above, and a swapped tree-sunlet orientation/port transport.

## 5. Final recommendation to the main report

1. Delete/withdraw the statement that the package lacks an active full 405,216-case enumeration and derivation of (40/14/2).
2. Delete/withdraw the statement that the package lacks a separate semantic replay of all 574,535 probe rows.
3. Replace them, if desired, with the narrower assurance notes in Sections 4.1–4.4: close code lineage, the public-profile start boundary, integrated rather than standalone cross-report closure, and an implicit transport-bijection assumption.
4. Update every reference to the current “44-command plan” to “53 mathematical regeneration commands”; 44 is retained only as a historical runtime reference.

Static-audit conclusion: **both major earlier code findings are falsified by the current revision and should be withdrawn, while the stated independence/cross-bound scope should be narrowed as above.**
