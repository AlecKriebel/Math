# R6 computational and certificate-semantics review

Date: 2026-08-29

Package reviewed:
`/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/isolated/k2p_principal_d_plus_submission_referee`

Reviewer work area:
`/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/independent_checks/computation`

## Status

**Computational evidence: PASS for the layers assigned to this audit.**

I found no load-bearing defect in the primitive graph grammar, raw-ID scheme,
canonicalization/model-map interface, symbolic rank-upper certificates, direct
certificate registry, restoration forest, probe and parameter-transport joins,
strict JSON handling, optimized-mode guards, corrected-composite mutation
machinery, or the R5 printed semantic-anchor repair.

In particular, the revised raw-four and theta2 composite mutation suites really
do construct complete mutant ledgers and invoke the production independent
verifier. The frozen v2 reports bind distinct nonempty mutant hashes, record the
full input/output byte and row changes, preserve the source tree, and reject
every semantic mutation for its intended diagnostic. The R5 role confusion is
also repaired: the 934-row terminal registry and the 16,974-row overlay have
different typed schemas, and a coherent printed-hash-plus-binding swap is
rejected for schema drift.

This conclusion is about the computational/certificate layers delegated here.
By instruction I did **not** run `run_all_verifiers.py --quick`,
`run_all_verifiers.py --full`, or the outer handoff mutation suite. Those remain
separate gates in the parent referee run; no PASS in this note substitutes for
them. I treated stored reports as assertions and inspected their producers,
verifiers, source bindings, mutation provenance, and internal row-level
commitments. No authoritative package file was modified.

## Independent artifacts

The two scripts below are reviewer-authored. They do not import or call the
authoritative raw-four/theta2 classifier when reconstructing the primitive
universe, raw IDs, graph joins, physical inequalities, or stored-mutation
forensics.

1. `independent_checks/computation/r6_semantic_scan.py`
   - SHA-256:
     `9318c2927934aa3c944ed36f2d2e17dc1895ac72ec807440191219d5b31c6a84`
2. `independent_checks/computation/r6_semantic_scan_result.json`
   - SHA-256:
     `3f9bd18cfa7d800a16e41280a4470a9bdf4c9cbee96c689bc06b344eca36f732`
   - canonical payload SHA-256:
     `10fbde1a110235ef39f8739e4948fa77466470318624409f1561d11f18de011f`
   - schema: `r6-independent-k2p-computational-semantic-audit-v1`
   - status: `PASS`; unresolved: `0`
3. `independent_checks/computation/r6_bounded_fail_closed_attacks.py`
   - SHA-256:
     `74255679840615ebc5dd752239ccb2939162373b89d7b001d801a547fee92815`
4. `independent_checks/computation/r6_bounded_fail_closed_attacks_result.json`
   - SHA-256:
     `e7c9a475a8da4f6b6f4462eda1356d20910d63be3e6b475217d83743e1542a8e`
   - canonical payload SHA-256:
     `554b513fc17e9a0c7e4f1762618e997df57a9e41de263962881a156b4c2172d3`
   - schema: `r6-reviewer-bounded-fail-closed-attacks-v1`
   - status: `PASS`; unresolved: `0`

The package did not yet have an R6 execution virtual environment when these
bounded checks ran. I used the immediately preceding clean R5 environment only
as a Python/dependency runtime; every inspected input and every source binding
was resolved under the isolated R6 package above. Runtime versions were Python
3.14.6, NetworkX 3.5, and SymPy 1.14.0 on macOS 26.5.2 arm64. This does not
import or reuse any R5 evidence artifact.

Commands:

```text
python3 -B independent_checks/computation/r6_semantic_scan.py \
  --project isolated/k2p_principal_d_plus_submission_referee \
  --runtime-python /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-28_r5/execution/k2p_principal_d_plus_submission_referee/.venv/bin/python \
  --output independent_checks/computation/r6_semantic_scan_result.json
```

Exit status `0`; measured internal runtime `98.596991 s`; result hash as above.

```text
python3 -B independent_checks/computation/r6_bounded_fail_closed_attacks.py \
  --project isolated/k2p_principal_d_plus_submission_referee \
  --python /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-28_r5/execution/k2p_principal_d_plus_submission_referee/.venv/bin/python \
  --output independent_checks/computation/r6_bounded_fail_closed_attacks_result.json
```

Exit status `0`; observed wall time approximately `6.3 s`; result hash as above.

## Load-bearing source audit

### Primitive graph and K2P map core

Inspected:

- `package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py`
  - SHA-256:
    `afafe6c4289870a02226516e2b7ff207c57b844f4c45fc6864cedf826e9ec742`
  - primitive graph construction: lines 74--203
  - model descriptors and canonicalization: lines 289--548
  - exact Jacobian/rank routines: lines 551--650
  - sparse polynomial operations: from line 653
  - labelled mixed-graph isomorphism and triangle handling: lines 868--1019
- `work/raw_ledger_audit/generate_raw_ledger.py`
  - SHA-256:
    `91e58a4a9b9328448ae5e028e12b9550a16f1a6f1b4246afb156c1e1d7cb6d44`
- `work/raw_ledger_audit/verify_raw_ledger.py`
  - SHA-256:
    `615ae57fac469f9e6243c3295ef5121c0927873444e346696a05b12eb34e3d15`
- `work/canonicalizer_completeness/canonicalizer_audit.py`
  - SHA-256:
    `0e4f2315d836053d1f50742af163668d243b086afda84515d197a2da09756bda`

The generator starts from directed primitive encodings and repair/subdivision
data, not topology names or a hidden rooted-tree oracle. Direction, sink masks,
port permutations, repair tags, dummy/physical roles, and parent order survive
into record descriptors. Canonicalization uses labelled mixed-graph
isomorphism with role/color data and separately checks completeness by a
certificate partition. I found no name-based shortcut or unchecked map from a
claimed class label to an outcome.

The printed Fourier/K2P coordinate construction and polynomial pullbacks are
implemented with exact sparse integer/rational arithmetic. Exact rank routines
do not promote a sampled numerical rank to a global upper bound. The atlas
contains zero Python `assert` statements; certificate rejection remains active
under optimized Python in direct negative tests.

### Symbolic rank upper bounds

Inspected:

- `work/rank_upper_certificates/syzygy_upper.py`
  - SHA-256:
    `e91af12df4e82d9cd305f1f207c056fb28b083fe31a42c81a89103871fdd853e`
- `work/rank_upper_certificates/verify_rank_upper_certificates.py`
  - SHA-256:
    `f5a72dcdf390252c1d5003e56a9fb097fc2624a18ce34b05e79abc9c1e50f86a`

All 4,379 stored rank descriptors were accounted for. Of these, 3,515 use
multilinear exact polynomial vector fields and 864 use base fields plus an
exact transported primitive logarithmic field. A complete-mutant attack that
replaced a symbolic field family with sampled-rank-style data was rejected by
the production verifier with:

```text
K2P_RANK_UPPER_REPLAY_FAIL:RANK_UPPER_SYMBOLIC_FIELD_DIMENSION_FAIL:orbit=0:observed=4:required=6
```

The relevant mutation report has SHA-256
`a591d0e910d2fae3ee11664a591b485c474327f74b05711143e5c11d4a77f524`
and payload SHA-256
`7e6c4b2c83181aa73317064178c02a10fc18e3f6d6b7cad5a78544178308775a`.
This is symbolic evidence of a global rank upper bound, not sampled-point
evidence.

### Direct terminal certificates

The 934-row terminal registry has SHA-256
`8d821c2000da5cf2647913cbdb42f8a42dfeb6826b8b76be49d91d78ebaf9998`
and canonical payload SHA-256
`8f41e576ac8551ead8fd75d87c4b8d4aee85f5ba1007c0dcf8aaeb62fbfb1439`.
The direct-certificate body has SHA-256
`8f0760543d0b69937c24785288ee26f58db86f34bb3446d686e0422eb2fa7af7`.

Independent recount:

- 839 exact multihomogeneous quadratic classes
- 36 exact direct polynomial separators
- 35 ordinary-triangle quotient classes
- 20 exact labelled mixed-graph isomorphisms
- 4 hard bindings
- among the 36 higher-degree direct separators: 22 quintics, 12 quartics,
  and 2 cubics

I parsed every rational witness for those 36 direct separators and checked 432
edge-pair inequalities exactly. Every required inequality was strict; no
floating-point comparison was used.

I also attacked six false-certificate families (`reference`, `fast`, `cubic`,
`homogeneous`, `subset`, and `positive_target`) in ordinary mode, with `-O`,
and with `PYTHONOPTIMIZE=1`. All 18 attacks were rejected for their intended
certificate semantics.

### Restoration

Inspected:

- `work/restoration_sign_reclassification/verify_corrected_restoration_forest.py`
  - SHA-256:
    `99f8a373d1bbb924cc312777733a38d663cfc7e58f14d47b431357b222171f3b`

The frozen forest has SHA-256
`396d1970af17b5e90c3f1b00ceab1b810816e93ec68a566bd0479f05c722793f`
and payload SHA-256
`c4e5502d6bb774b426477ef3b289140e81dc16bf061261ccf3562d5de02cb2e3`.

Independent graph joins recovered exactly:

- 997 canonical parents
- 2,540 physical roots
- 36,568 first children
- 256 second children
- 36,824 edges
- 32 continuation parents
- depth two
- zero cycles and zero unresolved roots/children

For every corrected raw-four restoration member, I joined its primitive source
and target graph encoding to the forest rather than trusting the stored class
name. I recomputed child-row and transport commitments for every archetype.
Wrong-parent, missing-child, duplicate-child, cycle, and broken-terminal
mutations in the v2 report were all rejected; report SHA-256
`10e74ca5dd50da8b9597b0640181615012816f96eeb9c64153f3eadc1b395a3b`,
payload SHA-256
`bc301a61ff21c06f154a51c7caf299136cbb7bd924cb5a324eab0a38522a17eb`,
13 attempted and 13 rejected.

### Probes and parameter transport

Inspected:

- `work/probe_coherence_corrected/verify_probe_coherence_corrected.py`
  - SHA-256:
    `a101909cc492594d635752882a476ac4694314fa3b0be306857fb5a5dfd76053`
- `work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit.py`
  - SHA-256:
    `ed6dccf6273fa1ba60a34c201d9ea4b0774eed2548055ddee5f90fd4282621c5`
- `work/canonicalizer_completeness/inheritance_transport/build_parameter_transport_certificate.py`
  - SHA-256:
    `9058470d4e6f95106dc6d13de5399d88003aa90734dadb489e63f104e32788a8`
- `work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py`
  - SHA-256:
    `fe065ed7e54a5a969e8578c3f72d347ac2248b47d9a2283a6f42d130932d26da`

Independent joins recovered:

- 29,964 one-port rows and 2,107 equality survivors
  - 27,758 quartet mismatch
  - 99 full-map `T_i` strict sign
  - 1,915 isomorphic
  - 192 triangle
- 544,571 two-port rows and 32,729 equality survivors
  - 511,266 quartet mismatch
  - 576 full-map `T_i` strict sign
  - 30,969 isomorphic
  - 1,760 triangle
- 67,741 exact transport IDs
- 4,379 parent restriction IDs

Every equality record joined to an exact transport or restriction and to a
reverse marginal/inventory witness. I found no equality survivor supported
only by a class label.

Across the parameter-transport material I reconstructed 67,741 relation
occurrences, 71,022 probe-restriction occurrences, and 5,540 restoration
restriction occurrence classes. There are 277,389 affine actions: 230,232
identity and 47,157 inheritance complements, plus 3,745 triangle local
sections. Reconstructing parent order from graph encodings gave exactly the
rule used by the certificate: complement `lambda -> 1-lambda` only when a
licensed graph transport reverses reticulation-parent order. I found zero
illicit complements. Paired `(s,g)` marginal products are preserved; triangle
sections are not silently represented as affine parent flips.

Relevant mutation reports all have zero survivors:

- parameter transport: SHA-256
  `b17711eda26cb31839dab842123529159f72ed2ddd755a04facfbbb9a17ffb66`,
  payload
  `00e791f01cdab4ee7413fd38f75176cbec1dd7eabd86a4de2632a559dfec7445`;
  four complete-mutant production-verifier attacks
- probe coherence: SHA-256
  `6a0c037a5dbdd4f36713ea77202625beff11f70d60222af84f15648c30980455`,
  payload
  `b1e8b2b023f4be9418a1acbe71fd148acfadad2f5237b6de8dea611f9a7adbd9`
- independent probe replay: SHA-256
  `7224b26a0eead1aa39ccb0092b14b24990cdf5c455e15d040bd8d9181fd6463b`,
  payload
  `cee41ecd404a1b854a2867a0b3e7b56fd810836ab8e5e6c990977adcba0e0c20`

## Independent primitive and census reconstruction

The reviewer script locally reimplements weak compositions, repair insertion,
sink masks, ordered subdivision words, graph degree and DAG checks, port
permutations, and raw-ID inversion. It does not call the production decisive
classifier.

Recovered primitive counts:

- raw-four: 6 source encodings and 2,814 target encodings
- theta2: 4 source encodings and 6,138 target encodings
- all archetypes including the cycle families: 10,084, matching the package's
  declared universe

Recovered raw-ID formulae:

```text
raw4   = ((source_index * 2814) + target_index) * 24  + permutation_index
theta2 = ((source_index * 6138) + target_index) * 120 + permutation_index
```

I inverted and rebuilt twelve representative raw IDs spanning first, interior,
repair, sink-mask, port-order, and final records. For each, I regenerated the
source and target graph encoding and checked labels, degrees, acyclicity,
repair tag, sink role, and port permutation.

### Raw-four corrected composite

- 405,216 records
- 360,408 displayed-quartet exclusions
- 16,974 full-map strict-sign exclusions
- 23,822 exact-rank exclusions
- 1,472 direct-terminal presentations
- 2,540 restoration-member presentations
- 67,536 records for each of six source indices
- uncompressed ledger bytes: 391,559,514
- ledger SHA-256:
  `7cf3f953fca695d612387143818843650498f84f55cf0a776f90c9afdd95eef6`
- ordered row-hash root:
  `392285a46068797d25b342eb7b4e4b3f7570d10d7da032eebe548352b7d5766a`

### Theta2 corrected composite

- 2,946,240 records
- 2,942,592 displayed-quartet exclusions
- 2,528 full-map strict-sign exclusions
- 800 exact-rank exclusions
- 240 direct quadratic separators
- 80 labelled isomorphisms
- 736,560 records for each of four source indices
- uncompressed ledger bytes: 2,766,984,898
- ledger SHA-256:
  `805fc7f5a3de9dad2c63a210208075cf19910cf811ffd08878f32782ce71b659`
- ordered row-hash root:
  `7dbeb383b4b6b558dad35e56b81e4d900e990c6e3af1195fdc7df9a51be6d4ca`

The counts, row roots, and gzip-stream ledger hashes agree with the corrected
summaries. This is an independent grammar/ID/row scan, not acceptance of a
stored PASS flag.

## Corrected-composite v2 mutation forensics

Inspected:

- `work/corrected_composite_ledgers/generate_corrected_composites.py`
  - SHA-256:
    `41f9f15f83fc860b15994c4369ca3b8b7c6b424bdc76e5377bf11d45c76c88e3`
- `work/corrected_composite_ledgers/verify_corrected_composites_independent.py`
  - SHA-256:
    `0c9bf77a1af47d2eedf424c825703b23c6753f2ed26defb5107db7f50da6666d`
  - full replay begins at line 427; command entry point at line 514
- `work/corrected_composite_ledgers/run_composite_mutations.py`
  - SHA-256:
    `f15c3d49ed94c626943c9a568b48d29c1cedde8d2904b2aa3d9a28da19c7d7f3`
  - complete-ledger rewrite at line 239
  - semantic mutation specifications at line 311
  - per-case production-verifier execution at line 551
  - entry point at line 655

AST and data-flow inspection confirmed the call path:

```text
main -> run_semantic_case -> rewrite_complete_mutant + invoke_verifier
```

`rewrite_complete_mutant` streams the entire original gzip ledger, applies the
specified semantic mutation while preserving all other rows, writes a complete
new ledger, recomputes byte count/hash/row commitments, emits the matched
summary mutant, and then calls the production independent verifier. It does
not pass a single-row fragment to a toy checker. The source tree is hashed
before and after each test and must be unchanged. The runner also deletes any
caller-selected stale report before invoking the verifier, so an early failure
cannot leave a false PASS report in place.

Raw-four report (`k2p-raw4-corrected-composite-mutations-v2`):

- 14 tests total
- 12 semantic complete-ledger attacks
- 12 distinct nonempty mutant ledger hashes
- 12 intended diagnostics observed
- zero source-tree drift
- zero survivors
- payload SHA-256:
  `94b2f2f90ab77eee454bdbf1c5f81b3be8fd0f89d24b45a15bfed6e92f59a04c`

Theta2 report (`k2p-theta2-corrected-composite-mutations-v2`):

- 12 tests total
- 10 semantic complete-ledger attacks
- 10 distinct nonempty mutant ledger hashes
- 10 intended diagnostics observed
- zero source-tree drift
- zero survivors
- payload SHA-256:
  `6395c6a79540fb05fe10fc54b55bf446d09023e2c6107148926a9c8f6848ac80`

The remaining two tests in each family are optimized-mode and output-contract
attacks, hence the semantic complete-ledger count is two below the total.

I inspected the outer release gate as well:

- `work/final_theorem_release/run_release_mutations.py`
  - SHA-256:
    `becef7af22196affe559b253099b8e6aa68afe24cdcf9f6b122286e181b45275`
  - `corrected_composite_mutation_gate` at line 532
- `work/final_theorem_release/release_common.py`
  - SHA-256:
    `6eb62345f69505bfdb2f0600e3bba9e6539dd8c89f3c49650649b4ce5496dbc3`
  - primitive-summary validation at line 1338
- `work/final_theorem_release/verify_final_theorem_release.py`
  - SHA-256:
    `6c2a6142e5a7c4fc092f16d5c3e52d0a4a00215f445d9facb199d557f7502ba0`

The outer gate reruns all 14 raw-four and all 12 theta2 cases and requires the
new reports to be byte-identical to the frozen reports. Thus changing only a
frozen mutation report cannot satisfy the release mutation gate.

## R5 semantic-anchor repair

Inspected:

- `proof_compression_submission/adversarial_review/audit_article_sources.py`
  - SHA-256:
    `08770614791fb06159f3ace78edb504935538258e36beada50d74bb7b5117d96`
  - typed anchor table at line 82
  - printed hash/schema/count audit at line 207
  - current narrative-role audit at line 377
- `proof_compression_submission/adversarial_review/test_printed_authority_hash_gate.py`
  - SHA-256:
    `72c7866016887bbaee746a8aaa53cf6e404c48fc8331ad4ba2b4172288a4110f`

The supplement source has SHA-256
`d5f79a95a7ec0aff2ce4e8e3f818dcf930435dcde2265ed23dc6bacede1fea33`.
It labels the terminal registry with its actual SHA and role. The distinct
corrected-terminal overlay has SHA-256
`5810ffb1d023e503eaa62d9705c28a85e9c724a6ad8357f49ebe61b2dde675dc`,
schema `k2p-raw4-corrected-terminal-overlay-v2`, and 16,974 rows; it is no
longer described as the 934-class terminal registry.

I performed the stronger coherent mutation: replace both the printed digest
and its manifest binding with the overlay's digest. A hash-only gate would
accept this. The typed gate rejected it exactly as:

```text
PRINTED_FROZEN_ANCHOR_SCHEMA_DRIFT:raw-four 934-class terminal certificate registry:expected=k2p-raw4-terminal-certificate-registry-v1:actual=k2p-raw4-corrected-terminal-overlay-v2
```

The registry is independently required to have schema
`k2p-raw4-terminal-certificate-registry-v1` and count 934. I also checked all
26 baseline printed-anchor rows and the three current narrative ledgers; each
narrative is explicitly typed as a reader snapshot subordinate to the
generated release lock. This repairs the semantic-role defect rather than
merely changing a digest.

## Strict JSON, output contracts, and optimized mode

Inspected:

- `work/final_theorem_release/strict_json.py`
  - SHA-256:
    `16328479a779a335080d5a828ef3b0f25e9e87286d2161f0c1e55f0730e0d46c`

Independent strict-JSON attacks and observed rejection mechanisms:

- duplicate name with equal values -> `STRICT_JSON_DUPLICATE_NAME`
- duplicate name with conflicting values -> `STRICT_JSON_DUPLICATE_NAME`
- valid JSON with noncanonical key/whitespace bytes ->
  `STRICT_JSON_NONCANONICAL_BYTES`
- `NaN` -> `STRICT_JSON_NONFINITE_NUMBER`

No last-key-wins parsing path survived.

I invoked twelve load-bearing entry points under both command-line `-O` and an
ambient `PYTHONOPTIMIZE=1`: composite verifier, composite mutation runner,
static article audit, printed-anchor mutation suite, raw-four generator and
verifier, theta2 generator and verifier, canonicalizer audit, parameter
transport verifier, symbolic-rank verifier, and final release verifier. All 24
invocations exited nonzero with their specific optimized-mode diagnostic.

Output-contract inspection confirms that verifiers unlink or refuse stale
caller-selected reports before a dependency, schema, optimization, or semantic
failure. Malformed or missing reports cannot be interpreted as a PASS. The
release harness requires canonical JSON and explicit status/schema/payload
bindings rather than using process exit alone.

## Other frozen mutation evidence inspected

The following reports were parsed with strict JSON, their canonical payloads
recomputed, and their expected rejection fields inspected. All have zero
survivors:

- canonicalizer completeness v2:
  - file SHA-256
    `d18b54d319d5fae95a193f9597339dca4e7f648b929f088d492207bce24ae674`
  - payload SHA-256
    `eb57b8edae21e0f9cc4f90a30fea520196ab964e0878d36e31d90f9b80c570b2`
- direct closure v2:
  - file SHA-256
    `26face7a232348830b6afaaff571e3fdc7e82bd611baf7be910241e1d9961e58`
  - payload SHA-256
    `8020b1af1c84fd3cffc1c2054645dd010ef0bc1a77a6b4b55488226f476919ba`
- restoration v2:
  - file SHA-256
    `10e74ca5dd50da8b9597b0640181615012816f96eeb9c64153f3eadc1b395a3b`
  - payload SHA-256
    `bc301a61ff21c06f154a51c7caf299136cbb7bd924cb5a324eab0a38522a17eb`
- probe coherence v2:
  - file SHA-256
    `6a0c037a5dbdd4f36713ea77202625beff11f70d60222af84f15648c30980455`
  - payload SHA-256
    `b1e8b2b023f4be9418a1acbe71fd148acfadad2f5237b6de8dea611f9a7adbd9`
- independent probe v2:
  - file SHA-256
    `7224b26a0eead1aa39ccb0092b14b24990cdf5c455e15d040bd8d9181fd6463b`
  - payload SHA-256
    `cee41ecd404a1b854a2867a0b3e7b56fd810836ab8e5e6c990977adcba0e0c20`
- parameter transport v2:
  - file SHA-256
    `b17711eda26cb31839dab842123529159f72ed2ddd755a04facfbbb9a17ffb66`
  - payload SHA-256
    `00e791f01cdab4ee7413fd38f75176cbec1dd7eabd86a4de2632a559dfec7445`

The stored mutation reports are corroborative, not self-validating. The main
independent evidence here is the source/data-flow audit, local primitive/raw-ID
reconstruction, exact graph joins, exact physical-domain checks, strict-JSON
attacks, optimized invocations, false-certificate attacks, and the composite
complete-mutant provenance reconstruction.

## Findings

No theorem-fatal, proof-blocking, computational-completeness-blocking, or
reproducibility-blocking defect was found in the assigned computational scope.

No package remedy or resealing is required on the basis of this audit.

## Remaining external gates

The following are deliberately **not adjudicated by this subreview**:

- outer `verify_handoff.py` and handoff mutation suite
- clean environment setup
- global quick and full release replays
- PDF rebuild/omission tests
- archive reproducibility
- the mathematical proof and literature/attribution review

These are assigned elsewhere in the complete fresh referee run. If any of
those fails, the overall recommendation must reflect that failure despite the
computational PASS recorded here.
