# R5 computational and certificate-semantics adversarial review

Date: 2026-08-28 (America/Los_Angeles)

Package audited:

`/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-28_r5/isolated/k2p_principal_d_plus_submission_referee`

## Scoped conclusion

**Computational evidence: PASS for the assigned layer.** I found no surviving
defect in primitive enumeration, raw-coordinate uniqueness, canonicalization,
symbolic rank-upper semantics, restoration/probe joins, parameter transports,
or fail-closed behavior. In particular, both round-4 blockers are genuinely
repaired:

1. a coherently layer-resealed compressed JSONL row containing either a
   same-valued or conflicting duplicate name is now rejected for the duplicate
   name itself; and
2. every submitted portable entry point rejects both `python -O` and inherited
   `PYTHONOPTIMIZE=1` before leaving output, while the atlas's formerly
   assertion-dependent certificate checks now fail identically in normal and
   optimized modes.

This is a scoped computational conclusion, not a substitute for the root
referee's fresh quick/full/release runs or the separate mathematical proof
audit. I deliberately did not invoke those global harnesses because they were
assigned to the root referee.

No file under `isolated/` was edited. Reviewer-owned programs and results are
confined to `independent_checks/computation/`.

## Environment

- macOS 26.5.2 (build 25F84), Darwin 25.5.0, arm64.
- Apple M1 Pro, 10 logical CPUs, 17,179,869,184 bytes RAM.
- System Python: CPython 3.14.6, Clang 21.0.0.
- Dependency-bearing interpreter used for NetworkX/SymPy attacks:
  `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-27_r4/execution/k2p_principal_d_plus_submission_referee/.venv/bin/python`,
  also CPython 3.14.6, with NetworkX 3.5 and SymPy 1.14.0.

The dependency interpreter came from the immediately preceding isolated R4
review because the R5 environment had not yet been populated when these
focused attacks began. It executed only R5 source and R5 evidence. Its package
versions equal the declared R5 versions. Stdlib-only scans used system Python.

Peak RSS was not collected: the commands below used macOS `/usr/bin/time -p`,
which reports wall/user/system time but not peak memory.

## 1. Primitive generation, raw uniqueness, and canonicalization

### Code semantics inspected

The finite graph universe is generated from explicit primitive encodings, not
topology-name answers or a hidden rooted classifier. In
`package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py`, `CORES`
at line 19 contains the arc/reticulation/sink/repair grammar;
`weak_compositions` at line 53 and `target_completions` at line 161 enumerate
sink masks, ordered subdivision words, dummy leaves, and permitted repair
segments. `source_supports` constructs the source family from the same graph
grammar. Raw generation then crosses source index, target index, and every
physical port permutation explicitly:

- four-port `generate_raw_ledger.py`: permutations at line 67 and raw-ID
  arithmetic at lines 320-331;
- theta2 `generate_theta2_ledger.py`: permutations at line 80 and raw-ID
  arithmetic at lines 502-508; and
- cycle `generate_cycle_closure.py`: base IDs at lines 130-213, completion IDs
  at lines 313-421, and permutations at line 435.

The verifier independently reconstructs the coordinate represented by each
ordinal and requires `row.raw_id == ordinal`; see four-port
`verify_raw_ledger.py` lines 283-344 and theta2 `verify_theta2_ledger.py`
lines 862-913. A category is attached only after this complete raw-coordinate
enumeration. The current corrected-composite route rejects the revoked
tree/sunlet and rooted-oracle reasons; neither raw ledger contains such a row.

The atlas canonicalizer enumerates the exact signed reticulation action
`B_r = S_r semidirect (Z/2)^r`: every reticulation order and every independent
incoming-parent flip are present, while physical port labels are transported
and are not quotiented. A flip is paired with inheritance complement. The
separate canonicalizer auditor implements its own graph restriction/root
suppression, ordinary-triangle predicate, marked incidence expansion, and
labelled graph-isomorphism comparison rather than calling the atlas relation
answer.

### Independent checks and reconciled counts

The reviewer-owned broad scan, freshly run against R5, found:

- 10,084 primitive graph records and 10,084 distinct primitive encodings:
  six raw4 sources, 2,814 raw4 targets, four theta2 sources, 6,138 theta2
  targets, two cycle sources, and 1,120 cycle targets;
- all 10,084 pass independently implemented DAG, degree, integer-label,
  dummy-label, and strong-tree-child predicates;
- the four-port raw IDs are exactly `0..405215`, with the partition
  `360408 + 16974 + 23822 + 1472 + 2540 = 405216`;
- the theta2 raw IDs are exactly `0..2946239`, with the partition
  `2942592 + 2528 + 800 + 240 + 80 = 2946240`;
- all 23,822 four-port and 800 theta2 rank-exclusion rows name the symbolic
  upper-certificate mechanism and contain no sampled-rank field; and
- cycle has 13,440 base rows, 5,964 restoration roots, and 536,364 completion
  rows, with zero wrong base/parent links and zero roots without children.

The same scan reconstructed raw IDs directly from source, target, and
permutation coordinates and checked every row once, so omission, duplication,
or permutation-coordinate aliasing would change either the ordinal equation,
row count, or ordered roots.

The stored canonicalizer-completeness certificate was also audited against its
producer/verifier semantics. It records 10,084 slow-versus-fast descriptor
comparisons and 4,012 rank/topology-eligible relation presentations, partitioned
as 3,932 `none`, 54 ordinary triangle, and 26 labelled isomorphism, with zero
disagreements. Its two semantic mutations reject a nonordinary three-cycle and
an erased-but-unmarked selected triangle. The reviewer scan directly compared
17 disclosed slow/fast representatives spanning all primitive families; sample
root `6c82701b4d1a55a37698b286ec505777b5af741e5d509c2d15572b859ddfd4be`.

**Independence boundary.** The broad reviewer scan uses stdlib parsing,
hashing, raw-coordinate reconstruction, and separately written graph
predicates, and never calls the submitted classifier or release verifier. It
does call the submitted primitive grammar constructor to instantiate the
10,084 graphs and calls the two atlas descriptor routines on the disclosed
17-record comparison sample. Thus the all-row coordinate/graph/join audit is
independent of classification, but it is not a second independently authored
primitive generator or a full second algebraic classification of all
3,351,456 raw directions. The submitted all-primitive slow/fast audit remains
load-bearing and is a gate in the root referee's fresh full run.

## 2. Polynomial and symbolic-rank certificate semantics

I inspected the atlas's switching-sum Fourier-map construction, exact sparse
polynomial pullbacks, all six separator engines, rank-lower minor bindings, and
the rank-upper verifier. The critical upper-bound mechanism is symbolic:
`work/rank_upper_certificates/syzygy_upper.py` forms the integer coefficient
system obtained by expanding `J_f V = 0` for polynomial vector fields. Exact
evaluation is used only to establish independence of already-symbolic kernel
fields; it is not a sampled Jacobian upper bound. This is stated in the code at
lines 10-20 and implemented by `coefficient_system` from line 53. The verifier
then compares the resulting global upper bound to the exact nonzero source
minor.

The stored replay closes 4,379 descriptors: 3,515 base-ansatz descriptors plus
864 exceptional descriptors transported from 75 representatives, with zero
unresolved rows. Its seven semantically resealed attacks cover omitted and
duplicated coverage, altered syzygy coefficients, reassigned representatives,
broken port transport, a false upper claim, and substitution of sampled rank
for symbolic upper rank; all have zero survivors.

My independent fail-closed program monkeypatched the kernel routines to inject
a false unit kernel into each of six engines: reference quadratic, fast
quadratic, cubic, degree-4 homogeneous, subset degree-3, and positive-target.
Every engine raised its explicit source/target-pullback invariant in all three
modes: normal, `-O`, and inherited optimization. This directly verifies that
the 22 former `assert` statements were replaced by operative
`AtlasInvariantError` checks rather than merely hidden behind an entry-point
guard. AST inspection found zero `assert` nodes in the atlas.

I found no path by which sampled evidence can be relabelled as a symbolic rank
upper certificate, nor a separator engine that can accept a known nonzero
target pullback under optimization.

## 3. Restoration, probes, restrictions, and parameter transports

### Restoration

The reviewer scan independently parsed and joined the complete forest:

- 997 canonical parents and 2,540 physical roots;
- 36,568 first children, 32 continuation parents, and 256 second children;
- 36,824 edges and 36,792 terminal leaves;
- zero duplicate rows, wrong/missing parents, cycles, or unresolved leaves.

It also reconciled the first-child proof split:
35,758 quartet, 606 full-map `T_i`, 148 exact multihomogeneous quadratic,
24 inherited `F_{2,112}` quartic, and 32 continuation rows. The separately
stored replay reports all 36,568 first exact relations as `none`, all 256 second
children, and 78 exact physical witness checks. The 13 stored mutations target
omitted raw/child rows, wrong source or target transports, reassigned quartet,
`T_i`, and quartic evidence, altered Bernstein data, invalid `D_plus` witness,
wrong second parent, a cycle attempt, and optimized mode; all reject.

The 297 restoration archetypes are descriptive PC-PARTIAL compression only.
The inspected analyzer/verifier does not promote equal polynomial bodies to
graph-orbit equivalence; the full 36,824-edge forest and graph/transport
ledgers remain authoritative.

### Probe and transport closure

The reviewer scan independently reconstructed the required joins and found:

- 176 anchors and all 2,206 source plus 2,206 target sites;
- 29,964 one-port rows and 2,107 equality parents;
- 544,571 two-port rows and 32,729 reverse-order equality rows;
- 67,741 exact transport rows and 4,379 parent restrictions;
- zero missing parent/transport links and zero invented triangle witnesses.

The separately implemented submitted probe graph audit does not import the
corrected-probe producer or verifier. It rebuilds children from the frozen
primitive input reconstructor, applies classifier precedence itself, and
reconstructs graph transports, restrictions, reverse parents, and the global
ordinary-triangle condition. Its exact partition is:

- one-port: 27,758 quartet, 1,915 isomorphism, 192 triangle, 99 `T_i`;
- two-port: 511,266 quartet, 30,969 isomorphism, 1,760 triangle, 576 `T_i`;
- 638 applied quartet certificates, 156 applied `T_i` relation certificates,
  118 Bernstein polynomial replays, zero new triangles, zero incoherent rows,
  and zero unresolved rows.

Its 12 local semantic mutations reject omitted raw rows, wrong parents/sites,
wrong reverse transport, broken global triangle, reassigned quartet/`T_i`,
wrong restriction, broken transport, an old rooted-oracle field, classifier
reassignment, and child-graph mutation.

The parameter-transport builder/verifier was inspected row by row at the rule
level. It transports paired `(s,g)` serial products, obtains ordered parent
permutations from the graphs, applies inheritance complement exactly for a
certified parent-order reversal, never assigns an affine flip to a local
triangle section, handles root-suppressed paired factors, and requires every
reticulation incidence to be accounted for. Its ledgers contain 67,741 probe
relations, 71,022 probe-restriction occurrences, and 5,540 restoration-
restriction occurrences. Its ten attacks include removed or illicit
complements, unpaired parent reversal, false triangle maps, omitted serial
factor, broken paired `(s,g)` action, hidden root-suppressed incidence, and
source-target reversal without inverse transport; all reject with zero
survivors.

No illicit inheritance complement, direction reversal, parent-order loss,
missing site, or fabricated triangle survived either the stored mutation
contracts or the independent joins.

## 4. Round-4 fail-closed repairs

### Duplicate and malformed JSON

`work/final_theorem_release/strict_json.py` now enforces, recursively:

- unique object names at every nesting depth;
- rejection of `NaN`, `Infinity`, and non-finite parsed floats;
- strict UTF-8 and top-level object type;
- canonical decompressed JSON/JSONL bytes;
- no blank or unterminated JSONL rows; and
- compressed, expanded-stream, document, row, and nesting limits.

Sixty Python files import this shared reader. The outer bundle checker does not
trust that implementation: `proof_compression_submission/crosswalk/check_revised_referee_bundle.py`
contains a separate duplicate-aware, bounded parser and invokes its
`verify_json_member` for frozen and submission members.

The submitted strict-reader suite passed 17 mutations and two clean documents.
My independent clean-data scanner then parsed every shipped compressed JSON
family without importing `strict_json`: 26 files (17 JSONL and nine JSON),
8,601,558 rows/documents, and 7,633,642,325 decompressed bytes. Every object had
unique names; every row/document was valid UTF-8, finite, and byte-for-byte
canonical. There were zero duplicate names and zero noncanonical payloads.

Finally, I recreated the former R4 exploit in a disposable hardlinked clone.
For the first `one_port_ledger.jsonl.gz` row I inserted a duplicate
`parent_anchor_id`, once with the same value and once with a conflicting
earlier value. In both cases the ordinary Python decoder retained the later
value, so the mutation preserved the old verifier's effective semantics. I
then updated the mutated ledger hash and coherently resealed the local probe
certificate. The production verifier rejected both before semantics with:

`CORRECTED_PROBE_REPLAY_FAIL:STRICT_JSON_DUPLICATE_NAME:one_port_ledger.jsonl.gz:line=1:name='parent_anchor_id'`

Both exits were 1 and neither left a success artifact. Mutant ledger hashes:

- same-valued: `8a8e570ce091d56aea020329e4007f95f2ae4b7883fa6550644332b6ed90fce5`;
- conflicting: `bfe9cf3dc1673f80267b7fbea14b751e7ddbfbe62e81dd570ad5d4a1551f0b52`.

This is a semantic rejection, not an unrelated outer checksum failure.

### Optimized Python

The submitted matrix exercised 18 portable entry points under both direct
`-O` and inherited `PYTHONOPTIMIZE=1`, for 36 entry-point attacks, plus the
false-fast-separator test under three modes. It passed with no residual output.

My smaller independent matrix targeted all seven entry points exposed by the
R4 finding (`verify_package`, `guarded_run`, resumable driver,
`merge_manifests`, semantic comparator, direct residual replay, and
`run_all_sources`) in both optimized modes. All 14 exited 1 with exactly
`K2P_PORTABLE_OPTIMIZED_MODE_FORBIDDEN` and left no output. The portable source
fingerprint remained
`d5b18d845c040f96a04a8a573bb5fc9feece81c1923f8ba7d221a8091ce8c074`
before and after.

The proof-specific scripts that still contain assertions have their own early
optimization guards; the load-bearing atlas contains no assertions and its
semantic checks were independently attacked as described above. I found no
documented production path on which optimization can erase a validation or
turn failure into PASS.

## 5. Cross-version semantic invariance

A reviewer-owned stdlib comparator read all six R4 and R5 residual manifests
with duplicate-name rejection, required the exact per-source counts
`(536,747,276,276,64,32)`, and compared all 1,931 summaries after removing only
the two row byte/provenance fields `record_sha256` and
`semantic_record_sha256`. The projections are identical. Independently
recomputed combined root for each version:

`6b6659a67a2a02d20c9865c891e84bf02cb1d4a2a9a198ba14e630bf907ad9ee`

At the manifest top level, only `compiler_sha256`, `input_lock_sha256`, and
`semantic_manifest_sha256` differ in each source, as expected after the source
and evidence reseal. The submitted 19-field comparator also reports exact
equality for all 36 stored complete direct records, combined root
`201a616ee636d075f12d276585a66d88bebbeb73ad03018b11e61b18c6dc697d`.

Thus the R4 repairs change validation and provenance boundaries, not the
stored mathematical classification.

## 6. Findings and residual limits

### Blocking findings

None in the assigned computational layer.

### Non-defect execution note

Running `test_optimized_entrypoints.py` first with bare system Python failed
inside its normal-mode semantic probe because NetworkX was not installed in
that interpreter. The same target passed using the dependency-bearing
interpreter above. This is an investigator-environment miss, not a package
failure; the package's documented `setup_environment.sh` is the relevant
fresh-environment gate and is being run by the root referee.

### Evidence limits

- Stored PASS certificates are not treated as mathematical proof. Their
  producer/verifier semantics were inspected, and focused independent attacks
  and complete independent joins were performed. The root referee's fresh
  full harness remains required to turn stored replay assertions into fresh
  execution evidence.
- The reviewer raw scan independently checks every coordinate, graph invariant,
  ledger join, and partition count, but does not recompute every polynomial
  separator or exact rank determinant through a second CAS implementation.
  Those algebraic spot checks and the proof-level interpretation belong to the
  separate mathematical audit.
- Hash agreement is used only for provenance and for detecting mutation/source
  drift; it is never the basis for accepting a graph or algebraic claim.

## 7. Execution ledger

All commands below were run with the stated package as input. Peak memory is
unavailable.

1. Submitted strict-JSON mutation suite

   Command (cwd: isolated project):

   ```sh
   /usr/bin/time -p python3 -B proof_compression_submission/crosswalk/test_strict_json.py
   ```

   Exit 0; real 0.04 s. Output:
   `{"clean_documents": 2, "mutations_rejected": 17, "status": "PASS"}`.
   Stdout SHA-256:
   `5efaf2b222f7ecaed14101d4a552a2320591b9faf89eeccf4ac424b3d60ec344`.

2. Submitted optimized-entry-point matrix, bare system Python

   ```sh
   /usr/bin/time -p python3 -B package/referee/k2p_offline_sweep_portable/test_optimized_entrypoints.py
   ```

   Exit 1; real 1.86 s; normal-mode semantic probe raised
   `ModuleNotFoundError: No module named 'networkx'`. No package conclusion was
   drawn from this environment-only run.

3. Submitted optimized-entry-point matrix, dependency environment

   ```sh
   /usr/bin/time -p /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-27_r4/execution/k2p_principal_d_plus_submission_referee/.venv/bin/python -B package/referee/k2p_offline_sweep_portable/test_optimized_entrypoints.py
   ```

   Exit 0; real 2.57 s. Output
   `K2P_PORTABLE_OPTIMIZED_ENTRYPOINT_MATRIX_PASS`. Stdout SHA-256:
   `4b25654b34ece9abe5f14dfca1da1a45bde74507d37c88b21e8a59c6a9593e46`.

4. Reviewer duplicate-name, optimized-entry-point, and atlas-invariant attacks

   ```sh
   /usr/bin/time -p /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-27_r4/execution/k2p_principal_d_plus_submission_referee/.venv/bin/python -B independent_checks/computation/r5_fail_closed_attacks.py --project isolated/k2p_principal_d_plus_submission_referee --python /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-27_r4/execution/k2p_principal_d_plus_submission_referee/.venv/bin/python --output independent_checks/computation/r5_fail_closed_attacks_result.json
   ```

   Exit 0; real 25.45 s; internal measured runtime 24.951625916874036 s.
   Stdout SHA-256:
   `2d036d0241a944b0939e21ec9e2f0a5e2438245641abc3216ac209e745625404`.
   Result file SHA-256:
   `3dbaa595b7a2e1c711f98821f5c187f57f2ac385bf64f0166fca9a5e0da3e50d`;
   payload SHA-256:
   `b7403bf7b5076a8645fa1777d8ab0e80eec0a31a705bfa996c38e739be7e2559`.

   A non-controlling authoring attempt of this reviewer script exited 1 because
   it called `Path.resolve()` on the venv interpreter and thereby selected the
   base Python without NetworkX. The reviewer script was corrected to retain
   the lexical venv path before the controlling run above; no package file was
   involved and no result artifact from the failed attempt was used.

5. Reviewer broad semantic/graph/join scan

   ```sh
   /usr/bin/time -p /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-27_r4/execution/k2p_principal_d_plus_submission_referee/.venv/bin/python -B /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-27_r4/independent_checks/computation/r4_independent_semantic_attack.py --project /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-28_r5/isolated/k2p_principal_d_plus_submission_referee --output /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-28_r5/independent_checks/computation/r5_independent_semantic_scan_result.json
   ```

   Exit 0; real 221.73 s, user 208.32 s, sys 5.85 s. Stdout SHA-256:
   `84ef04d16f75743a1a77a0c852d59e11e3aa450d2bb7fa04994abec4c7925b9d`.
   Result file SHA-256:
   `22ef5fcd2197d791fc5a4c6cff61672978f50cfd93e11ca405cbda7e46214cd3`;
   payload SHA-256:
   `ce04ed741461d9f193be7df96fee9ca0b5c160217c1c6b57e59f859a1836431d`.
   The retained schema name says `r4` because this unchanged reviewer-owned
   method was first written in R4; the command and recorded source project show
   that this was a fresh execution on R5.

6. Reviewer all-compressed-JSON scan

   ```sh
   /usr/bin/time -p python3 -B independent_checks/computation/r5_compressed_json_audit.py --project isolated/k2p_principal_d_plus_submission_referee --output independent_checks/computation/r5_compressed_json_audit_result.json
   ```

   Exit 0; real 157.39 s, user 152.31 s, sys 0.96 s. Stdout SHA-256:
   `fe913b41f29bc0650cfa0d816ebde36f30069192f048ec82142cebbbaab78817`.
   Result file SHA-256:
   `dda6fd9c283a53e9a08fe8ca961051ef89bf927f571554e6c82f8d0a1507c37e`;
   payload SHA-256:
   `0ae7ebaf67ab86923fe8d522a0b1ccd2d2b261a273772b84bed776d91d61e42c`.

7. Reviewer full 1,931-summary semantic projection comparison

   ```sh
   /usr/bin/time -p python3 -B independent_checks/computation/r5_manifest_projection_compare.py --baseline /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-27_r4/execution/k2p_principal_d_plus_submission_referee/package/referee/k2p_offline_sweep_portable/results/four_port_release_v4 --candidate isolated/k2p_principal_d_plus_submission_referee/package/referee/k2p_offline_sweep_portable/results/four_port_release_v4 --output independent_checks/computation/r5_manifest_projection_compare_result.json
   ```

   Exit 0; real 0.28 s, user 0.22 s, sys 0.03 s. Stdout SHA-256:
   `b48e6043d2663db20e11e8a7c7b44984a85022e780885c40097e39ba93cf8baf`.
   Result file SHA-256:
   `d04ffce1d5597e75fce7616780aa6fbd0cf8515992fdebca47a9fd1cbf51c4cc`;
   payload SHA-256:
   `a57ce847db833cd8df3902211152da5135dd2fe0864ef4639f126c45df6d4594`.

8. Submitted 19-field comparator on the 36 shipped complete direct records

   The first invocation without `--allow-partial` exited 1 with the intended
   diagnostic that 36 records are not the complete 1,931-record sweep. The
   explicit partial comparison was run from the isolated project root:

   ```sh
   python3 -B package/referee/k2p_offline_sweep_portable/compare_semantic_runs.py --allow-partial /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-27_r4/execution/k2p_principal_d_plus_submission_referee/package/referee/k2p_offline_sweep_portable/results/four_port_release_v4 package/referee/k2p_offline_sweep_portable/results/four_port_release_v4
   ```

   Exit 0. Output root
   `201a616ee636d075f12d276585a66d88bebbeb73ad03018b11e61b18c6dc697d`;
   stdout SHA-256:
   `f02c2695f246df709e464d8e4aa03586164c2961b6c0322f27e8d16b2a94f445`.

## 8. Principal evidence hashes

### R4 repair surface

| Artifact | SHA-256 |
|---|---|
| `work/final_theorem_release/strict_json.py` | `16328479a779a335080d5a828ef3b0f25e9e87286d2161f0c1e55f0730e0d46c` |
| outer independent bundle checker | `41bbd578dcd43cd9607aa335385eb8f58d6f5e5be94003960b51c4b3200eb7ce` |
| submitted strict-reader test | `297d6cea1fce1ef8e3c383b81e8fb4eac41235201472a35065fb5b251094d5a6` |
| submitted optimized-entry-point test | `edf00610156de30065331b4137b1b3bd4917717541796b3fa9c7d5576bcf4c7b` |
| portable atlas core | `afafe6c4289870a02226516e2b7ff207c57b844f4c45fc6864cedf826e9ec742` |
| `verify_package.py` | `28e7bc2db7afa55d5e5a77af6ba1b6f32c105fe419f3742ee591151a12b86d83` |
| resumable driver | `914897efd77c75ce0ac66462b35e86d65c2b48b8868ace11f08ea4a4edf64be6` |
| manifest merger | `8fb186acf5b8905f8a123e027b7af6fb42f6f49880b36a881f967aec24c200cf` |
| semantic comparator | `46f45478d26a62e05dfa493cfd7209428328d65c8e65c0baa59a0907f7534485` |
| guarded runner | `5ce353fc4f5b42123bb1b3f6a1ad315ea80438fc41e840026a79c5372e7952eb` |
| `run_all_sources.sh` | `bb063b508b17d022b4ac46f9f92bf174cc1fd7bb8a1a9a63aa1decd9c082d0d9` |

### Enumeration, canonicalization, and algebra

| Artifact | SHA-256 / payload |
|---|---|
| four-port raw generator | `91e58a4a9b9328448ae5e028e12b9550a16f1a6f1b4246afb156c1e1d7cb6d44` |
| four-port raw verifier | `615ae57fac469f9e6243c3295ef5121c0927873444e346696a05b12eb34e3d15` |
| canonicalizer auditor | `0e4f2315d836053d1f50742af163668d243b086afda84515d197a2da09756bda` |
| canonicalizer verifier | `d6f6d7e05b700675055409229f0115e568bda1fcdeafc463e7d417ffdbe3706d` |
| canonicalizer certificate file | `5522164471b06895f0388c8c2baad716e9e87344c3cf595c7d3075ac70e6e655` |
| canonicalizer certificate payload | `3decee5310c9108d4a43a9fc5b3d1eabe53484276c00c84d58d7fa1346250e2b` |
| rank-upper verifier | `f5a72dcdf390252c1d5003e56a9fb097fc2624a18ce34b05e79abc9c1e50f86a` |
| symbolic syzygy engine | `e91af12df4e82d9cd305f1f207c056fb28b083fe31a42c81a89103871fdd853e` |
| rank replay file | `c967917601f64803c96c1ba11cabc5fd3ea8d6021f9e55441c4210d9b886793d` |
| rank mutation report file / payload | `a591d0e910d2fae3ee11664a591b485c474327f74b05711143e5c11d4a77f524` / `7e6c4b2c83181aa73317064178c02a10fc18e3f6d6b7cad5a78544178308775a` |

### Restoration, probes, and transports

| Artifact | SHA-256 / payload |
|---|---|
| restoration forest | `396d1970af17b5e90c3f1b00ceab1b810816e93ec68a566bd0479f05c722793f` |
| restoration verifier | `99f8a373d1bbb924cc312777733a38d663cfc7e58f14d47b431357b222171f3b` |
| restoration replay file / payload | `d74cc01341f405732c6ff62558ca3afff705c15cdf9a6f16dcc6ccd7636749c4` / `2e190fa1ea877545ace1706c3ae3a423f44cfecc4bc2bba32033c46d109657b0` |
| corrected-probe verifier | `a101909cc492594d635752882a476ac4694314fa3b0be306857fb5a5dfd76053` |
| corrected-probe certificate file / payload | `6edd4097d0ce6cc0938e1a7eaee8d01c7e9daac814e72422250f1dbdea04bdd3` / `7799adda95bbc89dff01257e76f811cf6a30061d97265a75f4e42e8d618da8b4` |
| independent probe graph auditor | `ed6dccf6273fa1ba60a34c201d9ea4b0774eed2548055ddee5f90fd4282621c5` |
| independent probe audit file / payload | `025fb011c5bf736bbcdf4bbef9f045d389f9a3ccb87597f5068a9a0972aa76f6` / `de15d876ec9f8b5e0cb88cb12d3df481af985aded388e111bae029f0f03ade6a` |
| independent probe mutation file / payload | `7224b26a0eead1aa39ccb0092b14b24990cdf5c455e15d040bd8d9181fd6463b` / `cee41ecd404a1b854a2867a0b3e7b56fd810836ab8e5e6c990977adcba0e0c20` |
| parameter-transport builder | `9058470d4e6f95106dc6d13de5399d88003aa90734dadb489e63f104e32788a8` |
| parameter-transport verifier | `fe065ed7e54a5a969e8578c3f72d347ac2248b47d9a2283a6f42d130932d26da` |
| parameter-transport certificate file / payload | `a706ebea37b9fbf338f1d8ae439e9d1a14cd14589f8b78699b657f039cd09a68` / `d05f4563b7c6a1cda2930d26b7cfa8172f8c9e0fce53d61bd42f97f3f672cb77` |
| parameter-transport mutation runner/report payload | `df5fc31ac588bc76032527fbb396de40eb2275b980b867079b101951927b5bea` / `00e791f01cdab4ee7413fd38f75176cbec1dd7eabd86a4de2632a559dfec7445` |

### Reviewer-owned evidence

| Artifact | SHA-256 / payload |
|---|---|
| `r5_fail_closed_attacks.py` | `c9dd8cdf445a4c3a9807302907ac255d16c3b3747000059228f165fbeca9ba86` |
| fail-closed result | `3dbaa595b7a2e1c711f98821f5c187f57f2ac385bf64f0166fca9a5e0da3e50d` / `b7403bf7b5076a8645fa1777d8ab0e80eec0a31a705bfa996c38e739be7e2559` |
| `r5_compressed_json_audit.py` | `46fa12e7a18914186d5456c244297a601a8bcc94bb8c9e5393660ad3f99a0536` |
| compressed-JSON result | `dda6fd9c283a53e9a08fe8ca961051ef89bf927f571554e6c82f8d0a1507c37e` / `0ae7ebaf67ab86923fe8d522a0b1ccd2d2b261a273772b84bed776d91d61e42c` |
| broad R5 semantic result | `22ef5fcd2197d791fc5a4c6cff61672978f50cfd93e11ca405cbda7e46214cd3` / `ce04ed741461d9f193be7df96fee9ca0b5c160217c1c6b57e59f859a1836431d` |
| `r5_manifest_projection_compare.py` | `7c2538505d11a8a92b76442a61458f9a49d805b94d3ef2dba1d97010abd37724` |
| 1,931-summary comparison result | `d04ffce1d5597e75fce7616780aa6fbd0cf8515992fdebca47a9fd1cbf51c4cc` / `a57ce847db833cd8df3902211152da5135dd2fe0864ef4639f126c45df6d4594` |

## Recommendation to the root referee

Carry this assigned layer as **PASS**, subject only to the already-planned
fresh global quick/full/release execution. R4 duplicate-name parsing and
optimized-Python behavior need no further repair based on this audit. If the
root harness also passes, I have no computational-completeness or
reproducibility action to request from the authors for these issues.
