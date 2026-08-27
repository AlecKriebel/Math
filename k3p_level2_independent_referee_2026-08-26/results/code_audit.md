# Adversarial code and certificate audit

Checkpoint: 2026-08-26 18:02 PDT (2026-08-27 01:02 UTC). Assigned code-audit work is 100% complete. This report concerns only the isolated copy at `package_copy`; I did not alter the original release package, use the network, or contact anyone.

## Bottom line

The active exact algebra is substantially stronger than a checksum-only package: the four-port representative maps, separator pullbacks, directed-rank upper bounds, restoration rows, literal tree--sunlet separator, cut minors, and Krawczyk boxes are generally recomputed with integer or rational arithmetic. I found no source/target reversal in those computations, and the interval routines I traced use exact rational endpoints rather than floating-point pseudo-intervals.

I nevertheless found two load-bearing reproducibility defects.

1. No active bundled command regenerates or independently classifies the complete four-port relation universe. The active checks prove the algebra on the already frozen 14-orbit/40-survivor lock, but they do not prove that this lock exhausts the 405,216 source/target/permutation cases or the 27,834 cases surviving the frozen topology filter.
2. The advertised independent probe replay does not semantically reconstruct its graph transports, marginal restrictions, quartet witnesses, or K3P tree--sunlet pullbacks. It checks their self-hashes, row order, reference membership, and stored metadata. The hour-scale producer is therefore still load-bearing for the mathematical meaning of 574,535 probe rows.

Both defects affect the central classification implication. They do not exhibit a false theorem or a false stored separator, but they prevent an unconditional conclusion from the active computer-assisted proof as packaged. The result is presently certified only conditional on (i) the correctness and completeness of the frozen four-port universe/lock and (ii) the correctness of the probe producer's semantic graph and algebra calculations.

## Severity-ranked findings

### 1. HIGH — full four-port exhaustiveness is frozen, not regenerated

The bundled metadata reports six sources, 2,814 targets, and 27,834 post-topology raw relations in `input_frozen/k3p_cloud_artifacts/descriptor_report_4(1).json:2-18`. The underlying search space is

`6 * 2814 * 24 = 405,216`

source/target/port-permutation cases. The 142,589,253-byte object named by that report's byte count and SHA-256 is not bundled as such. The active lock instead stores the result: 14 canonical orbits, an unmaterialized `frozen_universe_sha256`, and 40 raw survivors at `input_frozen/k3p_cloud_artifacts/K3P_14_ORBIT_LOCK.json:69-71,928-929`.

A compressed frozen companion ledger *is* bundled. A read-only streaming count found exactly 405,216 rows with this partition:

- `topology_excluded`: 377,382
- `rank_excluded`: 23,822
- `retained_terminal`: 1,472
- `restoration_obligation`: 2,540

Thus the last three categories total 27,834. This ledger is provenance, not a fresh K3P enumeration. The companion lock explicitly limits it to graph evidence and says every algebraic edge needs K3P rebinding (`COMPANION_DEPENDENCY_LOCK.md:3-17`); in particular, the 23,822 `rank_excluded` assignments are not graph-only facts.

The active computations never independently reproduce those categories:

- The primary verifier loads `K3P_14_ORBIT_LOCK.json`, asserts its stored 14/40/38/2 census, and iterates only the lock records (`reproducibility/exact_four_port.py:830-843`).
- The clean-room implementation independently reconstructs maps for the selected records, but its primitive universe starts from five handwritten core templates (`clean_room/verify_h21_transport_and_fourteen_orbits.py:83-120`). It constructs six sources and 2,814 targets (`:328-407`, with census assertions at `:1683-1688`) and then iterates only `RECORDS.items()`, where `RECORDS` came from the frozen lock (`:71-72,1695-1698`). Its additional exhaustive step partitions only the 24 port permutations of the single H21 base relation into seven double cosets (`:1700-1719`); it does not cross all sources and targets.
- The primary's representative double-coset replay is likewise limited to 14 lock records and 38 stored raw members (`reproducibility/exact_four_port.py:560-626`).
- The integrated gate checks the stored 14/38/2 census and the 9+5 separator partition (`reproducibility/verify_k3p_same_classification.py:182-250`).
- The complete 44-command mathematical regeneration list contains no four-port universe or lock producer. It reaches `primary_rebind`, which runs the same lock-consuming primary verifier (`reproducibility/run_release_suite.py:116-240`). The portable plan simply imports that list (`referee_tools/run_active_verifiers.py:220-263`).
- The probe producer is the only active mathematical consumer of `raw_directional_ledger.jsonl.gz`. It streams the ledger only to extract the `raw_id` values already named by the frozen 176-anchor contract and checks that those requested IDs were found (`probes/regenerate_k3p_probes.py:1672-1684`). The probe verifier merely checks the ledger's file hash (`probes/verify_k3p_probes.py:280-292`).

Theorem dependency: this is the finite exhaustiveness step behind the claim that the 14 named nontrivial orbits (plus two sink swaps) are all four-port obstructions. Exact certificates for those named orbits cannot exclude an omitted source/target relation.

Repair: add an active, independently implemented driver which derives the primitive input universe, iterates all 405,216 cases, recomputes the topology and K3P rank filters, and deterministically obtains the 40 surviving raw records and their 14-orbit/2-sink-swap quotient. It should bind every output row to reconstructed literal graphs/maps and include coherent omission/reclassification mutations. If the 142 MB K3P descriptor universe is intended as the certificate, bundle it and verify every row rather than only its report hash.

### 2. HIGH — the “independent” probe verifier does not verify probe semantics

The verifier's docstring says it “validates every exact-map and marginal reference” and “independently recomputes every stored tensor Bernstein certificate” (`probes/verify_k3p_probes.py:2-8`). Its implementation does not do those things.

- `validate_transport` checks a self-hash, the relation enum, injectivity of the two stored lists, and a few triangle list properties (`:96-125`). It never reconstructs either graph and never checks that the vertex map preserves labels/vertices, that the edge map is induced by the vertex map, or that incidence and arrowheads are preserved.
- `validate_restriction` checks a self-hash, a stored relation string, an integer label, and that three strings have length 64 (`:127-135`). It reconstructs neither the child restriction nor its parent.
- Exact Bernstein machinery is present as `sparse_from_payload` and `bernstein_replay` (`:154-222`) but neither function has a call site. An AST call count confirmed zero direct calls to both.
- Quartet certificates are accepted when their two *stored* split lists differ (`:302-305`); no graph generates those splits.
- K3P tree--sunlet records are accepted from stored circuit hashes and a nonzero-count field (`:307-344`). The active literal separator theorem itself is separately and convincingly replayed, but this verifier does not compile the particular probe triple graphs or recompute their six circuit pullbacks.
- The one- and two-port loops comprehensively check Cartesian row order, counts, reference membership, and parent identifiers (`:357-494`), but all mathematical statuses ultimately refer back to the semantically unchecked registries above.
- The integrated fresh gate invokes this same verifier and compares its payload to the stored report (`reproducibility/verify_k3p_same_classification.py:932-943`); it does not invoke another graph-semantic verifier.

I performed a non-mutating unit demonstration by importing the verifier and passing `validate_transport` a coherently self-hashed “isomorphism” whose sole vertices were the strings `not-a-source-vertex` and `not-a-target-vertex` and whose sole edge endpoints were nonexistent. It accepted the record and printed:

`ACCEPTED_SEMANTICALLY_UNBOUND_TRANSPORT e9838dd8b71d8a4dab4c7cca6e91835435fa20d64a37afe4e3febafe291ed7aa`

The mutation suite does not close this gap. Its broken-transport mutation alters a target vertex name but leaves the inner `transport_sha256` stale (`probes/test_k3p_probe_mutations.py:323-332`), so rejection proves self-hash sensitivity rather than graph semantics. The altered tree-circuit mutation similarly changes a stored hash (`:343-349`) without coherently rebuilding the record. The helper does recompute outer ledger hashes and reseal the release certificate (`:82-167`), which makes the missing inner/semantic reseal particularly clear.

Theorem dependency: complete one-/two-port coherence and hence the promotion from bounded primitives/restoration to arbitrary attachment words. The producer contains real graph and algebra reconstruction, but producer/verifier independence is absent at this boundary.

Repair: the independent verifier must rebuild each referenced source and target graph from independently reconstructed anchors and insertion sites, recompute exact labelled mixed-graph relations, validate transport incidence/arrowheads/labels, perform the actual parent restriction, compile the three-sector Fourier maps, recompute quartet splits and all six circuit pullbacks, and invoke the existing Bernstein routine on any sign certificates. Add coherently resealed semantic mutations, not only stale-hash corruptions.

### 3. MEDIUM — cut-transfer algebra is independent only conditional on frozen topology masks

The 204-direction cut computation is exact and strongly replayed, but every implementation starts from the same frozen JC topology artifact. The active gate declares `cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json` load-bearing (`reproducibility/strong_cut_transfer_gate.py:70-78`). The global-transfer producer iterates the frozen 72 records and their stored switching signatures, rechecks displayed-by-all flags, and derives 216/12/204 (`cut_recovery/strong_crossbridge/global_transfer/build_global_transfer.py:72-132`). The final verifier independently expands switching algebra, but its `FROZEN` input is the same artifact and its direction universe is reconstructed from those masks (`cut_recovery/strong_crossbridge/final_certificate/verify_final_certificate.py:28,174-214`).

This is not algebraic circularity: the minor and Bernstein re-expansions are meaningful. It is a topology-enumeration boundary. Neither path derives the five primitive templates, 72 active-labelled records, or the stored signatures from the graph axioms. The handwritten primitive-topology proof is therefore load-bearing. An independent graph generator would resolve this computationally; alternatively, the paper and final report should state this conditional boundary explicitly.

### 4. MEDIUM — the active clean-room path does not rerun the advertised 25-mutation hardened audit

`ACTIVE_MANIFEST.json:123-125` describes `clean_room/verify_clean_room.sh` as having passed “10 gate mutations and 25 adversarial mutations.” The wrapper runs the historical failure replay, the main verifier, one regression, the 10-mutation suite, and an optimized-mode rejection (`clean_room/verify_clean_room.sh:12-29`). It never invokes `clean_room/adversarial/hardened_cleanroom_reaudit.py`.

The integrated gate invokes only that wrapper (`reproducibility/verify_k3p_same_classification.py:895-898`). The primary verifier reads the stored hardened report and checks its prose/accounting fields while freshly running only the main clean-room verifier (`reproducibility/verify_primary.py:215-264`). The 44-command regeneration list also has no hardened-re-audit command (`reproducibility/run_release_suite.py:116-240`).

The main clean-room algebra is strong, so this is a fresh-reproducibility and active-boundary defect rather than evidence that an orbit certificate is wrong. Repair by adding the hardened audit and sentinel to the wrapper/regeneration plan, or change the manifest/integrated gate to say that the 25-mutation report is stored evidence only.

### 5. MEDIUM — several global theorem transitions are validated as prose, not proved by code

This is partly an honest limitation: `START_HERE.md:120-123` warns the referee to assess handwritten topology, analytic, semialgebraic, genericity, reconstruction, and gluing transitions.

- The primary bridge/marginal routine emits formula strings and booleans for incidence-tree no-holonomy, analytic normalization, physical factorization, and all positive path lengths; its only general executable assertion is the finite stored anchor-rank check (`reproducibility/exact_primary.py:791-830`).
- H14 map pullbacks, rank 14, the exact common point, and smoothness are genuinely computed, but contextual contraction and the rank sandwich are checked as stored fields/string fragments (`global_infrastructure/verify_global_infrastructure.py:560-567`).
- Genericity, Nash-stratification, target-section, real-to-complex dimension, and exact-reconstruction conclusions are predominantly exact string comparisons (`global_infrastructure/verify_global_infrastructure.py:843-887`).

These steps must stand or fall with the handwritten proof, not the integrated gate's `CERTIFIED` status. In particular, a passing run should not be reported as independent computational validation of these arguments.

### 6. LOW — the H14 primitive-exponent check is vacuous, though the fixed coefficient is primitive

The verifier intends to check that the coefficient binomial's exponent-difference vector has gcd one, but evaluates

`math.gcd(*[1 for _ in supports[0] + supports[1]])`

which is identically one (`global_infrastructure/verify_global_infrastructure.py:526-554`, especially `:542`). It does not compute exponents. The fixed coefficient recorded by the producer,

`-qCGT*qG0G*qTT0 + qCTG*qGG0*qT0T`,

has disjoint square-free supports and therefore really does have primitive exponent difference (`global_infrastructure/generate_global_infrastructure.py:766-776`). This is a verifier-hardening defect, not a counterexample to the delivered H14 irreducibility argument. Repair by constructing the exponent-difference vector and taking the gcd of its nonzero entries; add an `x^3-y^3` mutation.

### 7. LOW — standalone primary checks rely on optimizable `assert`, and rank labels are not dimension-bound there

`reproducibility/exact_primary.py`, `exact_four_port.py`, and `verify_primary.py` contain many load-bearing `assert` statements and no optimized-Python refusal. For example, the four-port lock/map/pullback checks are assertions at `exact_four_port.py:830-1043`. Direct `python -O reproducibility/verify_primary.py` is therefore not a sound certification entrypoint.

The official integrated path mitigates this: it rejects optimized Python (`reproducibility/verify_k3p_same_classification.py:1007-1010`), and the clean-room verifier uses non-optimizable `require` checks. The issue should nevertheless be fixed or the standalone primary command should explicitly refuse `-O`.

The primary four-port rank replay also reports the certificate's `rank` after taking a determinant without requiring `rank == len(rows) == len(columns)` (`reproducibility/exact_four_port.py:895-909,953-988`). The clean-room directed-rank verifier supplies exactly that missing check (`clean_room/verify_h21_transport_and_fourteen_orbits.py:1436-1475`). A read-only check found that every delivered source and directed-rank record currently has matching rank/row/column sizes, so the fixed artifacts are not invalidated.

### 8. LOW — standalone final cut verifier exits successfully for a blocked certificate

The final cut verifier accepts either `PASS` or coherently `BLOCKED`, emits `PASS_BLOCKED` for the latter (`cut_recovery/strong_crossbridge/final_certificate/verify_final_certificate.py:571-588`), and unconditionally returns zero after verification (`:631-664`). The regeneration command has no sentinel for this step (`reproducibility/run_release_suite.py:156-161`). Later global-transfer construction explicitly requires final `PASS`, so the full chain eventually fails closed. The standalone step and transcript can still misleadingly register a successful command for an incomplete certificate. Return nonzero for `PASS_BLOCKED`, or give the runner a `"status": "PASS"` sentinel.

## Positive checks

- Package integrity passed independently: 574 outer payload files / 153,326,366 bytes and 548 proof-core members / 152,714,245 bytes were hash- and size-consistent.
- The clean-room four-port verifier independently constructs the selected literal graphs, root-suppressed mixed automorphism groups, displayed-frame conjugation, double cosets, Fourier coordinate transport, polynomial pullbacks, and five target dimension upper bounds. The defect is universe selection, not the representative algebra.
- Restoration is materially more independent than the probe verifier. Its verifier imports neither producer nor producer support, reconstructs 36,824 source/target rows, rechecks parent restrictions and graph hashes, recompiles exact K3P descriptors, checks target pullback zero/source pullback nonzero in the correct direction, and evaluates strict rational witnesses (`restoration/verify_k3p_restoration.py:1170-1217,1231-1406`).
- The sharpness interval code uses `Fraction` endpoints. Its interval operations and Krawczyk/rank calculations are exact rational enclosures (`sharpness/independent_krawczyk_replay.py:61-114,478-617`); the differently structured adversarial `Ball` implementation is also rational (`sharpness/adversarial/adversarial_audit.py:69-130`). I found no missing outward rounding, because there is no binary floating-point rounding in the decisions.
- The cut-transfer verifiers re-expand switching polynomials, minors, and Bernstein coefficients with exact integer/fraction arithmetic. Direction normalization and old/new port maps are explicitly checked within the frozen direction universe.
- The literal tree--sunlet v2 verifier reconstructs the printed map and exact six-circuit pullbacks. I found no sector collapse or source/target reversal there.

## Commands and toolchain

No active mathematical verifier, complete regeneration, restoration producer, or hour-scale probe producer was started by this audit. The parent referee owns those executions.

Executable/read-only checks actually run by this audit were:

1. `/usr/bin/python3 package_copy/referee_tools/verify_package_integrity.py --package-root package_copy` — PASS.
2. `python3 --version`, `/usr/bin/python3 --version`, and the package venv import/version probe. Results: venv Python 3.14.6; `/usr/bin/python3` 3.9.6; `mpmath 1.3.0`, `networkx 3.5`, `numpy 2.5.2`, `sympy 1.14.0`.
3. `gzip -cd .../raw_directional_ledger.jsonl.gz | wc -l` plus a standard-library streaming `Counter` over its `category` field — 405,216 rows and the category census stated above.
4. A standard-library AST call-site count for `sparse_from_payload` and `bernstein_replay` — both defined, both zero direct calls.
5. The isolated direct `validate_transport` demonstration described in Finding 2 — accepted the semantically unbound record.
6. A standard-library JSON check of every source/directed rank record's claimed rank and minor dimensions — all delivered records matched.
7. `./RUN_REVIEW.sh plan` — **not completed**. Its integrity preflight raced a concurrently active parent-owned verify workspace and saw a verifier temporary path disappear. It did not reach plan reconstruction and did not start a mathematical command. No further top-level runner command was attempted.
8. Two direct `/usr/bin/mktemp -t k3p-cleanroom-optimized.XXXXXX` probes, followed by removal of the two audit-created empty files. They showed that macOS BSD `mktemp -t` ignores the runner's intended workspace `TMPDIR` and uses `/var/folders/...`; this is an operational portability wrinkle, not theorem evidence.

Static inspection used `rg`, `rg --files`, `find`, `wc -l`, and repeated exact `nl -ba FILE | sed -n 'A,Bp'` reads. The inspected active boundary included the top-level wrappers and manifests; primary/clean-room four-port code; literal separator; probe producer/verifier/mutations/sealer; restoration producer/support/verifier/mutations; exact and adversarial sharpness; signed-pair/cyclic/final/global cut-transfer producer/verifier/release paths; global infrastructure producer/verifier/mutations; and the integrated gate/mutations. One early read-only JSON introspection one-liner raised `KeyError` because I guessed a field name incorrectly; it was corrected and no conclusion depends on it.

## Unexecuted and unresolved checks

- The parent agent, not this audit, is running the mandated fresh integrated replay and one complete regeneration. I make no claim about their final exit statuses.
- I did not rerun the 25-case hardened clean-room adversarial audit, the excluded Git-bound release-engineering mutation suite, historical verifiers, PDF builds, or any network-dependent operation.
- I did not independently prove the five-core primitive topology theorem, all-n cherry argument, bridge-fibre/no-holonomy theorem, contextual H14 gluing, Nash/genericity transition, real-to-complex dimension step, or reconstruction algorithm. Those are handwritten-proof obligations and should be assessed with the proof audit.
- Because Finding 1 identifies the missing active universe regeneration, four-port exhaustiveness cannot be resolved by a successful run of the present 44-command plan.
- Because Finding 2 identifies dead/missing semantic replay, probe correctness cannot be upgraded to producer-independent evidence by a successful run of `verify_k3p_probes.py`; the fresh producer run is useful but not independent verification.
