# Fresh adversarial computational review — 2026-08-26 package

## Status and recommendation

**Computational/certificate status: PASS.**  I found no surviving theorem-facing
code or certificate mutant, no census mismatch, and no false-PASS path in the
revised canonicalizer, restoration, probe, parameter-transport, or symbolic-rank
machinery.  The defects that caused the 2026-08-25 HOLD are substantively repaired
in the inspected source and in fresh live attacks.  The controlling serial outer
mutation run exited 0 after 3,519.10 s with maximum RSS 2,635,235,328 B; all 25
aggregate mutation gates passed, with zero survivors and zero blockers.  Its
report SHA-256 is
`f2a362e9d2606b0315f9fe6e5a7659d328bd73bcf6552f0c1cc4c4f8ecdd0026`,
payload SHA-256 is
`05475591f00c75f2f0c2ee2e92c23bc869a8ed5000d28b40455ab7481870d30b`,
stdout SHA-256 is
`7dbb43e2428d3d6c74923d956c1c9741315893be328341b65a276979b14ce5e4`,
and stderr/timing SHA-256 is
`349f87ac666959d4f7bf7898f4200fdc0e707aecdd92fb54359e6a641710f0ab`.

An earlier invocation of the complete parameter-transport mutation suite ran
while a second copy of the same approximately 2.55-GB primitive regeneration was
active.  Both processes failed closed at the first production mutant with

```text
PARAMETER_TRANSPORT_MUTATIONS_FAIL:unqualified production rejection:triangle_edge_false_product_map:1:None
```

and created no success report.  This does **not** establish a semantic failure
or identify the cause: an isolated execution of that same complete, coherently
resealed mutant reached the untouched production verifier
and was rejected with the exact intended diagnostic

```text
PARAMETER_TRANSPORT_REPLAY_FAIL:rederived bytes:parameter_transport_certificate.json
```

The later low-contention serial run exercised the complete 25-gate outer
orchestration, including all ten parameter-transport mutations, and passed.  The
earlier concurrent run is preserved as a noncontrolling fail-closed diagnostic;
it is not a current computational blocker and is not treated as a semantic
failure.

One nonblocking diagnostic-quality weakness remains: on an unexpected child
rejection, the parameter mutation wrapper omits the child's captured output and
reports only `returncode` and the parsed semantic marker.  This made the concurrent
failure opaque.  It does not permit PASS and does not undermine the intended
mutants.

## Scope, copy discipline, and independence

The package reviewed was the disposable extraction at

```text
/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-26_r3/execution/r3_computational_adversary/package
```

No authoritative artifact was repaired.  Reviewer-owned reports and the one
instrumented mutant driver are outside that package under
`execution/r3_computational_adversary/`.  After notification that reviewer imports
had created unsealed `__pycache__` files in the shared isolated extraction, I did
not read, import, execute, delete, or edit anything there; all subsequent work used
the disposable copy with `-B`.

After the controlling outer run, a direct check against the original submitted
inventory returned exit 0 with 489/489 submitted paths byte-identical; its stdout
SHA-256 is
`f58c22d4d32b76efd907d6e40725c6094bb329a95c3539d9db20e75d2f5a1cc2`.
Child/reviewer execution created exactly three unsealed `.pyc` byproducts in the
disposable execution tree (`compression_common`,
`verify_final_theorem_release`, and `k2p_atlas_core`).  They are not members of
the 489-file submitted set and do not represent a submitted-source change.

The independent census program was a reviewer-owned program from the preceding
fresh review, SHA-256
`933e2dac57fd09a409288576a5473ab5d7c54070fc8c82567793f3a099a0a163`.
It imports no submission module.  It independently reconstructs the primitive
completion domains and dense raw IDs, checks every raw ID and ordered completion
word, and reconstructs restoration/probe parent and reference closure.  It counts
analytic category labels from the submitted ledgers; it is not a second
atlas-free analytic classifier and not a second symbolic algebra engine.  That
boundary is explicit in its output and is not presented as stronger independence.

## Environment

| Item | Observed value |
|---|---|
| OS | Darwin 25.5.0 |
| CPU | Apple M1 Pro |
| Physical memory | 16 GiB |
| Python | 3.14.6 |
| NetworkX | 3.5 |
| SymPy | 1.14.0 |
| Execution policy | disposable package, `-B`, no optimized mode except negative tests |
| Disk during heavy parameter attack | approximately 2.5–3.0 GiB free |

## Disposition of the prior HOLD defects

| Prior defect / required repair | Fresh result | Evidence |
|---|---|---|
| Parameter-transport mutants did not all face the full production verifier with exact diagnostics | **Fixed; fresh PASS** | Four complete attacks build coherently resealed ledgers and certificates, structurally validate them, and invoke untouched primitive regeneration. Six local attacks exercise exact semantic validators. The controlling outer run rejected all 10/10 and bound payload `93741cbeb50b2e2fde5d2c144de5d9943d1879fb61faf64115cf44ec5608b044`; the separate isolated `triangle_edge_false_product_map` production attack returned status 1 with the exact regenerated-byte diagnostic. |
| Canonicalizer mutation wrapper could convert dependency failure into apparent PASS | **Fixed; fresh PASS** | Both semantic mutants rejected exactly. An independent missing-`networkx` plus stale-PASS injection caused baseline exit 1, no success artifact, and overall wrapper failure; no false PASS was emitted. |
| Restoration/probe wrappers were not fail-closed and did not bind exact rejection mechanisms | **Fixed; fresh PASS** | Restoration rejected 13/13 and probe rejected 15/15. Every case had exit 1, the exact required diagnostic, no timeout/signal/unrelated crash, and no success artifact. Clean production baselines passed first. |
| Exact-rank sampled-evidence substitution was not tested through the production verifier | **Fixed; fresh PASS and independently reproduced** | The current complete mutant removes symbolic `fields`, inserts `sampled_point_evidence`, coherently reseals the manifest, invokes `verify_rank_upper_certificates.py`, and requires `RANK_UPPER_SYMBOLIC_FIELD_DIMENSION_FAIL:orbit=0:observed=4:required=6`. The controlling outer run rejected the seven-case rank suite, including this complete production-verifier attack, and bound payload `2fae9aab6167a060abbce5544b1ae7180a29ac3ddcbf33ae2aff1d5485b46110`. An independent in-memory attack produced the same exact assertion. |
| C05 crosswalk did not expose the executable symbolic-rank authority | **Fixed** | C05 now binds `verify_rank_upper_certificates.py` as “executable symbolic-rank replay,” `syzygy_upper.py` as its symbolic module, and the current v2 production-verifier mutation runner/report with exact hashes. |
| Supported release entry points did not all reject optimized Python | **Fixed; fresh PASS** | All four documented public entry points rejected `python -O` before work. In particular, `output/referee/build_referee_bundle.py` now has an explicit optimized-mode guard. |
| Reconstruction authority was ambiguous between article and frozen companion | **Fixed** | C11 labels `article/main.tex` the current theorem/reconstruction authority and the promotion manuscript a machine-bound companion, not current proof authority. Both inspected narratives retain all candidates through final exact semialgebraic membership. |

## Load-bearing code audit

### Primitive generation and raw enumeration — PASS

The raw4, theta2, and cycle universes are produced from explicit core vertices,
directed/undirected incidences, weak compositions, sink masks, repair tags, and
ordered subdivision words.  I found no dispatch on topology names and no hidden
rooted-tree/sunlet oracle in the current authority.  Raw source support, target
completion, and port-permutation loops use a dense arithmetic ID; the independent
decoder checked every ID for range, uniqueness, exact inverse decoding, and
ordered-child consistency before any category census.

### Canonicalization and transports — PASS

The canonicalizer retains direction, incoming/dummy roles, physical port order,
reticulation-parent order, marked triangle erasure, and boundary transport.  An
ordinary triangle is not recognized merely from an unmarked three-cycle: the
relation requires the two specified heads into the same reticulation and the
marked erased edge.  The independent canonicalizer audit reconstructs the graph
relation without accepting the atlas answer.  Both attempted false merges were
rejected under exact diagnostic contracts.

### K2P model map and parameter transport — PASS for inspected semantics

The map code explicitly sums reticulation switchings, keeps the C/T and G sectors
separate, constructs inheritance polynomials, and transports paired `(s,g)` edge
parameters.  Parent order is derived from physical mixed-edge maps.  An
inheritance complement is applied only when the certified graph transport reverses
the reticulation-parent permutation.  Root-suppressed incidences remain explicit,
and ordinary-triangle local maps are product maps rather than affine surrogates.

The current mutation runner contains four complete verifier-facing attacks:

1. false ordinary-triangle product map;
2. omitted serial factor;
3. hidden root-suppressed incidence; and
4. source/target reversal.

Each writes a full mutated certificate and content ledger, validates the mutant's
own structural contract, runs the production replay, and accepts only the named
semantic diagnostic or the exact regenerated-byte diagnostic.  The other six
attacks target missing/illicit complements, unpaired parent reversal, a false
triangle affine map, a removed restriction complement, and a broken paired
`(s,g)` map using the same exact local validators used by the producer.

The sealed 10-case parameter mutation report has file SHA-256
`16fc464cdfa339837993c70673679516c54bc4e0c9dfa3e7608471d3e1ef7b37`
and logical payload SHA-256
`93741cbeb50b2e2fde5d2c144de5d9943d1879fb61faf64115cf44ec5608b044`.
The controlling outer run freshly reproduced the 10/10 rejection result and bound
that logical payload.  The isolated complete first-mutant attack remains an
additional independent control of the production rejection path.

### Exact rank and polynomial certificates — PASS for inspected semantics

The upper-rank path is symbolic.  `syzygy_upper.py` constructs exact coefficient
systems and computes exact `DomainMatrix` ranks; the universal upper certificate
is not inferred from a sampled Jacobian.  Source lower minors use exact rational
arithmetic.  The current sampled-rank mutant destroys the required symbolic field
dimension while leaving plausible point evidence, and the production verifier's
representative check rejects it at orbit 0 with observed dimension 4 versus
required 6.

The C05 crosswalk file has SHA-256
`dbdd8fac081cbb523a3eb296f05c10c2166f56acbf128170b2ac51da5991bed8`.
It binds:

- mutation runner `16f2fd757ead0313581a493e85ccd7165b7c730368860beeb9c5316d6eb81b4c`;
- production verifier `7cc30cc31d80d999e899c4372bc0991d057fa02e847bd8167d8e33ca4a6cb0a6`;
- symbolic module `e91af12df4e82d9cd305f1f207c056fb28b083fe31a42c81a89103871fdd853e`;
- stored mutation report `685d04a045e651586904b28819ed5a1b159a44cdc62cb1f937a135911fa7b227`.

### Restoration forest — PASS

The wrapper first requires a clean semantic baseline, removes stale caller output,
then checks exact per-case diagnostics, return status 1, no timeout/signal,
absence of traceback/import failures, and absence of a success artifact.  The live
suite attacked omitted raw provenance, first and second children, wrong parents,
wrong and broken transports, cycles, reassigned quartet/T_i/quartic families,
altered Bernstein data, an invalid strict-D-plus witness, and optimized execution.
All 13 were rejected by their intended semantic checks.

### Probe machinery — PASS

The probe wrapper has the same fail-closed output contract.  Its 15 live attacks
covered omitted anchors and one-/two-port rows, parent restrictions and parents,
precedence changes, wrong parents, missing root-suppressed sites, reversed order,
invented global triangle equivalence, broken exact transport, reassigned T_i and
Bernstein data, and optimized execution.  All were rejected by the intended
diagnostic.  The independent census reconstructed complete parent and transport
reference closure rather than trusting aggregate counts.

### Release harness and output contracts — PASS

`release_common.py` binds the logical payloads of the nested reports and checks
their exact case metadata.  Freshly rerun nested wrappers use caller-owned output,
remove stale files, atomically publish only after PASS, reject aliases, and forbid
timeout/signal/unrelated crash.  The semantic-diagnostic contract test supplied 49
negative controls for nine accepted diagnostic forms and passed.

The four supported release commands all rejected optimized execution with these
markers:

| Entry point | Exact rejection |
|---|---|
| `output/referee/build_referee_bundle.py --check-only` | `optimized Python is forbidden` |
| `work/final_theorem_release/build_release_lock.py --check --require-ready` | `FINAL_RELEASE_LOCK_OPTIMIZED_MODE_FORBIDDEN` |
| `work/final_theorem_release/verify_final_theorem_release.py --quick` | `FINAL_THEOREM_RELEASE_OPTIMIZED_MODE_FORBIDDEN` |
| `work/final_theorem_release/run_release_mutations.py` | `FINAL_RELEASE_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN` |

Internal helper modules do not uniformly contain entry-point guards, but the
release README limits the supported public protocol to the guarded commands.  I
found no public path that could turn disabled assertions into a PASS.

The controlling low-contention outer command was

```text
.venv/bin/python -B work/final_theorem_release/run_release_mutations.py --timeout-seconds 7200 --output REVIEW/logs/release_mutations_control_report.json
```

It exited 0 in 3,519.10 s with maximum RSS 2,635,235,328 B.  All 25 gates were
REJECTED as intended, with zero survivors and blockers; the report, payload, and
stream hashes are recorded in the status section and execution ledger.  This
fresh run closes the outer output-contract and aggregate mutation gate.

## Independent exact census

Command (from the review root, pointed at the disposable package):

```text
.venv/bin/python -B /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/independent_checks/computation/fresh_census_audit.py --package /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-26_r3/execution/r3_computational_adversary/package --output /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-26_r3/execution/r3_computational_adversary/fresh_census_audit.json
```

Result: PASS, exit 0, 52.09 s, maximum RSS 341,934,080 bytes.  Output file
SHA-256 `602924d7481b4132bc17323c27299e1e904db15c673ce7a252d0d0e759cf51e0`;
logical payload SHA-256
`0a60795802e1e40a38590ae251cc09f3ac77331fa240f61c4162b9565ae1dd88`.

| Universe | Independently reconciled result |
|---|---|
| Primitive targets | `C(3,1)=289`, `C(3,0)=831`, total 1,120; `C(4,1)=831`, `C(4,0)=1,983`, total 2,814; `C(5,1)=1,983`, `C(5,0)=4,155`, total 6,138 |
| Primitive source supports | raw4 6, theta2 4, cycle 2 |
| Four-port raw | 405,216 = 360,408 quartet + 16,974 sign + 23,822 rank + 1,472 direct + 2,540 restoration; ledger SHA-256 `c6cd9d6b5b09371565fd3e58ff9ab3cd7266b6231b153d43f9d1e886af8eae27` |
| Four-port direct terminal classes | 934 = 839 quadratic + 36 higher degree + 4 hard + 20 isomorphism + 35 triangle; higher degree = 2 cubic + 12 quartic + 22 quintic |
| Theta2 raw | 2,946,240 = 2,942,592 quartet + 2,528 sign + 800 rank + 240 quadratic + 80 isomorphism; ledger SHA-256 `805fc7f5a3de9dad2c63a210208075cf19910cf811ffd08878f32782ce71b659` |
| Theta2 dummy forest | 56 roots, 576 six-port + 288 seven-port = 864 descendants, 832 leaves, 32 continuations |
| Cycle base | 13,440 = 5,964 restoration + 7,452 sign + 8 isomorphism + 16 triangle |
| Cycle full | 536,364 = 535,920 quartet + 132 quadratic + 300 sign + 12 isomorphism |
| Restoration | 997 canonical parents, 2,540 roots, 36,568 first children, 256 second children, 36,824 edges, 36,792 leaves, depth 2, 42 source transport classes, 4,986 target transport classes |
| Probes | 176 anchors; 2,206 source and 2,206 target sites; 29,964 one-port rows; 2,107 one-port equalities/parents; 544,571 two-port rows; 32,729 two-port equalities; 67,741 exact transports; 4,379 parent restrictions |

The audit also checked dense/raw-ID inversion, duplicates and omissions, port
permutations, ordered child IDs, all restoration row hashes/parents/root IDs, and
every referenced probe transport/restriction record.  No mismatch was found.

## Fresh execution ledger

All commands below ran from the disposable package unless otherwise noted.

| Command / attack | Exit | Wall time | Peak RSS | Output / exact result |
|---|---:|---:|---:|---|
| `.venv/bin/python -B output/referee/build_referee_bundle.py --check-only` | 0 | 0.60 s | 231,669,760 B | PASS; 406 files, 479,324,605 bytes, content root `d4385855fd9d8387080a8e789613114f047fd93aaad9a78e86924d1a29b25c3e` |
| `.venv/bin/python -B work/final_theorem_release/build_release_lock.py --check --require-ready` | 0 | 10.03 s | 518,602,752 B | PASS; 230 locked files; payload `b5eb26e953fbb76de671a4caa0db3068932af1e23b4fffdb0d118b5939f81756`; lock file `130642e235c9beaa22061c578c3c645244cdbf45a9b416d45d94492b3d2848bd` |
| `.venv/bin/python -B work/final_theorem_release/test_semantic_mutation_diagnostic_contracts.py` | 0 | 0.52 s | 64,913,408 B | PASS: nine qualified forms, 49 negative controls |
| `.venv/bin/python -B work/canonicalizer_completeness/test_canonicalizer_mutations.py --output <reviewer-output>` | 0 | 0.52 s | 50,626,560 B | PASS 2/2; output SHA-256 `48c35a2c6a2abe2327a3921dffbaecfd1ddc829d16e6478991f85dd6fb07b158` |
| canonicalizer output artifact | — | — | — | SHA-256 `48c35a2c6a2abe2327a3921dffbaecfd1ddc829d16e6478991f85dd6fb07b158`; payload `6a86dd657f3240a072df59df358fe93f475bb9a262edd52b83cd6dade7e7a73c` |
| independent missing-dependency/stale-PASS canonicalizer attack | 0 (expected catcher) | <1 s | not sampled | Baseline child exited 1 with `ModuleNotFoundError`; wrapper created no output and did not report PASS |
| `.venv/bin/python -B work/restoration_sign_reclassification/mutate_corrected_restoration_forest.py --output <reviewer-output>` | 0 | 586.20 s | 574,898,176 B | PASS 13/13; output SHA-256 `3fc427a415fa4cdb2cb31007913afdd6422a0f9833387a7f6876e0cc3a34b9b4`; payload `9f31f9688a587d79d35c24114d4a0693463486f254f0ee4892b99494d707c909` |
| `.venv/bin/python -B work/probe_coherence_corrected/run_probe_coherence_mutations.py --output <reviewer-output>` | 0 | 195.28 s | 69,386,240 B | PASS 15/15; output SHA-256 `eec59bb49db580828cdded73ca36fc01a6b0442d826c3a24fcba966e30755dd7`; payload `14f0364d516330017f0e73d904ad3d6ff5825f299d3fa2f00dcac5720a6f6e74` |
| `.venv/bin/python -B work/canonicalizer_completeness/inheritance_transport/run_parameter_transport_mutations.py --output <reviewer-output>` under duplicate 2.55-GB regeneration | 1 | 515.92 s | 2,548,809,728 B | Fail closed at first mutant: `unqualified production rejection:triangle_edge_false_product_map:1:None`; no report |
| reviewer-owned isolated complete `triangle_edge_false_product_map` production attack | 0 (expected catcher); production child 1 | 360.45 s total; 313.644 s verifier | 2,546,106,368 B | Exact intended `PARAMETER_TRANSPORT_REPLAY_FAIL:rederived bytes:parameter_transport_certificate.json`; no PASS |
| controlling low-contention `.venv/bin/python -B work/final_theorem_release/run_release_mutations.py --timeout-seconds 7200 --output REVIEW/logs/release_mutations_control_report.json` | 0 | 3,519.10 s | 2,635,235,328 B | PASS: 25/25 aggregate mutation gates, zero survivors/blockers; report `f2a362e9d2606b0315f9fe6e5a7659d328bd73bcf6552f0c1cc4c4f8ecdd0026`; payload `05475591f00c75f2f0c2ee2e92c23bc869a8ed5000d28b40455ab7481870d30b`; stdout `7dbb43e2428d3d6c74923d956c1c9741315893be328341b65a276979b14ce5e4`; stderr/time `349f87ac666959d4f7bf7898f4200fdc0e707aecdd92fb54359e6a641710f0ab` |
| post-run `shasum -a 256 -c` against original submitted inventory | 0 | not measured | not measured | 489/489 submitted paths `OK`; stdout SHA-256 `f58c22d4d32b76efd907d6e40725c6094bb329a95c3539d9db20e75d2f5a1cc2`; three unsealed reviewer/execution `.pyc` byproducts were outside the submitted set |
| independent direct sampled-rank semantic attack | 0 (expected catcher) | 0.45 s | not sampled | Exact `AssertionError:RANK_UPPER_SYMBOLIC_FIELD_DIMENSION_FAIL:orbit=0:observed=4:required=6` |
| independent finite census, command above | 0 | 52.09 s | 341,934,080 B | PASS; output/payload hashes above |
| each of four supported commands under `python -O` | 1 | <1 s each | not sampled | Exact optimized-mode marker listed above; no output artifact |

Fresh mutation reports differ bytewise from frozen reports only where their
operational timing fields differ.  The restoration and probe logical payloads are
identical to their frozen logical payloads.

## Parameter-transport concurrency diagnosis

The reviewer-owned diagnostic driver is
`execution/r3_computational_adversary/diagnose_parameter_triangle.py`, SHA-256
`16ca0b22b347143c53ba897d393b75df2ba2093191376db4c980ccb994ba72ee`.
Its result is
`execution/r3_computational_adversary/parameter_triangle_diagnostic_result.json`,
SHA-256
`ce0684e2676e381683a04f9650deb10d52f2015ee7633474eb66a71c87aa2f63`.

The isolated mutant had:

- mutated content-ledger SHA-256
  `1808af25655c548e2d35e6569a29b87fecc23d7092f86fe00ffa7ebc1b66f627`;
- mutated certificate logical payload SHA-256
  `8f233c1fd043ad8d2b16408d972f3840d99d5375d3013b94d9aa1693911d0311`;
- production mutation runner SHA-256
  `29201eae22649b75688a31b48a2b41bfd283a63f6888872ca7e3d2454a8bb554`;
- production verifier SHA-256
  `01dbe90dfd4262e2982974a2425c33435d623ebc68e2e9751f8e258f17ead160`.

This reproducer mutates the complete ledger/certificate and invokes the unchanged
production verifier; it does not call the mutation wrapper's decisive classifier.
The exact intended production rejection establishes that the first mutant and its
semantic wiring are sound.  It did not by itself substitute for all ten mutants;
the subsequent controlling serial outer run supplied that complete 10/10 and
25/25 execution evidence.  The earlier concurrent failure remains separately
recorded as a noncontrolling fail-closed diagnostic.

## Findings

### 1. No theorem-fatal or computational-completeness defect found

**Severity:** none / PASS.

No raw omission or duplication, census discrepancy, canonical collision, false
triangle symmetry, illegal inheritance complement, sampled upper-rank
substitution, restoration/probe closure break, optimized-mode bypass, or surviving
semantic mutant was found.  The revised machinery is materially stronger than
the 2026-08-25 package and fixes the identified load-bearing defects.

### 2. Full outer mutation gate passed under low contention

**Severity:** none / PASS.

The controlling command was

```text
.venv/bin/python -B work/final_theorem_release/run_release_mutations.py --timeout-seconds 7200 --output REVIEW/logs/release_mutations_control_report.json
```

It exited 0 after 3,519.10 s, rejected 25/25 with zero survivors/blockers, and
produced the exact report/payload hashes above.  The earlier concurrent attempt
exited 1 and wrote no report, so it remains diagnostic rather than controlling
evidence.  The post-run 489/489 check confirmed that no submitted byte changed.

### 3. Unexpected parameter-child failures are diagnostically opaque

**Severity:** nonblocking QA / reproducibility diagnosis.

At
`work/canonicalizer_completeness/inheritance_transport/run_parameter_transport_mutations.py:457`,
the wrapper raises

```python
require(qualified, f"unqualified production rejection:{name}:{result.returncode}:{observed}")
```

without including a sanitized tail of the already captured child output or a
classified resource/crash marker.  Under concurrent pressure this produced
`...:1:None`, which did not say whether primitive regeneration emitted a disk,
memory, or nested semantic error.

**Effect:** failure remains fail-closed, but an unexpected failure cannot be
diagnosed from the outer record alone.

**Smallest remedy:** on the unqualified branch, append a bounded, sanitized child
stdout/stderr tail and an explicit failure class while retaining the strict no-PASS
contract.  This is optional for theorem correctness.  Because the runner is frozen
and hash-bound, changing it would require regenerating its mutation report,
crosswalk bindings, release lock, portable ledger, PDFs if they print the hash, and
the outer seal.

### 4. Independence boundary remains explicit

**Severity:** nonblocking limitation, not a hidden completeness premise.

The package and this review do not supply a second all-family orbit partition
independent of both the atlas and canonicalizer, nor a separate engine that
re-expands every higher-degree polynomial.  Primitive enumeration, raw IDs,
parents/references, representative exact rank semantics, and mutation behavior
were independently attacked.  Analytic category totals outside those attacks
remain checked by authoritative producer/replayer agreement plus exact mutation
coverage.  The package states this boundary accurately.

## Computational conclusion

On the inspected code and fresh attacks, **all prior computational HOLD defects are
fixed and computational/certificate evidence is PASS**.  The finite censuses
reconcile exactly, the high-risk wrappers are fail-closed, symbolic rank authority
is explicit and attacked, supported optimized execution cannot PASS, and the
controlling official outer suite rejected all 25/25 mutations with zero survivors
or blockers.  The earlier concurrent, diagnostically unqualified run is
preserved as a noncontrolling fail-closed record.  The remaining independence boundary and
the diagnostic-quality suggestion in Finding 3 are explicitly nonblocking.
