# Hostile parser and certificate-input review

Review checkpoint: 2026-10-24T22:51:16Z. Completion estimate: **100% of the assigned finite-input audit**. Decision: **PASS for the deposited pinned checker and certificate, with the API/schema limits below**. No tested corruption produced false mathematical certification. This percentage is not a probability of mathematical correctness or progress on the broader research claim.

The reviewer inspected only the deposited checker and certificate, the source manifest, the published current-result file, and relevant README lines. No prior review artifacts were consulted. Source files were not edited. All new files and temporary experiments were confined to this review folder. No network, Git, or external communication was used.

## Inputs and exact claim

The checker is `verify_currents.py`, SHA256 `f329371d046d69e94130a2326320f050d740d281ba1387bccbf050d800468ed1`. The certificate is `square_flow_certificate.json.gz`, SHA256 `6573c55f2998f4576a050a0757ca74f1cae9cadfa96ec61c69b181c530f79c4f`, 165,241 compressed bytes and 4,460,799 decompressed bytes. These values agree with the deposited manifest. The unchanged copies here match the source before and after the tests.

The falsifiable audit hypothesis was that the normal entry point rejects modified certificate bytes and that direct checking rejects corrupted graph declarations, source assignments, currents, or energies. The test scope distinguishes three entry points:

1. `main()` reads a sibling file and checks its compressed-byte SHA256 before decompression or parsing (checker lines 156–160).
2. `check(data)` accepts an already parsed object, regenerates the graph, and validates the finite witness (lines 94–154). It does not enforce the certificate hash.
3. `inspect_flow(...)` is an internal helper supplied with trusted graph edges, source, and denominator by `check` (lines 72–85, 119). Calling it with arbitrary helper arguments is a different contract.

Assumptions are an unchanged checker/interpreter, normal standard-library integer and JSON semantics, and integrity of the pinned SHA256 identification. Runtime tampering, SHA256 collision construction, arbitrary hostile Python objects, and denial-of-service resilience are outside this audit.

## Reproducible evidence

Run from this folder:

```sh
python3 -I -S -B test_hostile_parser.py
```

The suite uses the entire genuine 40-by-19,931-current certificate and the unchanged checker. It does not mock graph generation, replace the real flows with small examples, or execute the release build program. It writes `test_results.json`, which records every case, expected result, actual result, exception/rejection reason, and timing. Python 3.14.6 completed the run from 22:50:20.311488Z to 22:50:37.618431Z in 17.307 seconds.

**161/161 expected outcomes passed: 145 rejections and 16 acceptances**, including genuine baselines and explicitly predicted permissive cases. The latter are reported below, not hidden as blanket malformed-input rejections.

| Entry point | Accepted | Rejected |
| --- | ---: | ---: |
| `main()` genuine baseline | 1 | 0 |
| Unchanged checker subprocess | 1 | 19 |
| Unchanged checker subprocess with `-O` | 1 | 1 |
| Direct `check(data)` | 4 | 113 |
| `json.loads` followed by `check(data)` | 6 | 6 |
| Direct internal helper | 3 | 6 |

The genuine JSON was separately parsed with duplicate-key and nonstandard-number detection: **no duplicate keys, no NaN/Infinity tokens, and actual integer types for all declared integer scalar fields**. Evidence is in `genuine_json_structure.json`.

## Adversarial findings

**Pinned entry point: PASS.** All 20 altered-file subprocess tests stopped at `exact certificate SHA256`, including equivalent JSON recompression, changed gzip contents, truncation, appended junk, appended empty gzip member, duplicate keys, alternate numeral syntax, missing JSON delimiters, and a run under Python optimization. The genuine certificate passed both ordinary and `-O` execution. The explicit `require` guards do not depend on Python `assert` execution.

**Current/source/graph corruption: PASS.** Direct checks rejected a changed first or last current; Boolean, floating-point, null, and string currents; missing or extra entries; missing or extra rows; exchanged or duplicated source rows; reversed signs; and zero flows. Edges with deletion, addition, duplication, reversed orientation, exchanged order, loops, out-of-range endpoints, Boolean/float endpoints, or extra endpoints failed. Coordinating an edge-order swap with all corresponding current columns still failed, because the certificate requires the exact independently generated edge order. Terminal deletion, addition, reordering, duplication, and invalid types failed. Explicit helper tests rejected wrong, zero, out-of-range, negative, Boolean, and float sources.

**Energy/denominator corruption: PASS.** Altered energy totals or per-row energies, nonintegral energy types, omitted/extra energy entries, and wrong scalar denominators failed. Changing a current and honestly recomputing energies still failed divergence. Adding an integer circulation around the real triangle `(0,1,2)` preserved divergence, but recomputing its energies failed the fixed total-energy check. Thus the direct checker is deliberately specific to this certificate's total; it is not a general acceptance test for every feasible flow below a threshold.

**Duplicate-key parsing: permissive, bounded.** Python's default JSON loader keeps the last occurrence of a duplicate object key. A wrong `q`, empty `flows`, or wrong total energy placed before the genuine same-named field was accepted by `json.loads + check`. Putting the wrong value last was rejected. The resolved accepted object still had the genuine checked mathematical data. This is a strict-schema/document-ambiguity issue, not a demonstrated false-math acceptance, and every modified serialization failed the pinned `main`. The deposited certificate itself has no duplicate keys. Do not claim that the direct parser rejects all duplicate-key JSON.

**Types and unused metadata: permissive, bounded.** `vertices=3070.0` and the JSON exponent spelling `3.07e3` pass because line 99 checks numerical equality but not `type(vertices) is int`. The graph size is independently computed as the integer 3,070, so this changes no mathematical constraint. `construction` may be absent, arbitrary unknown fields are ignored, and Python accepts a NaN token in ignored metadata. None is returned as a checked fact. Mathematical parameters, edge endpoints, sources, currents, energy entries, and denominator fields have the strict integer guards relevant to this witness. A claim of universal strict-JSON/schema validation would require qualification or further hardening.

**Helper denominator misuse: out of contract.** Direct calls to `inspect_flow` accept an equal-valued float denominator, or a zero flow with denominator `0`/`False`, because the helper does not validate that argument's type or positivity. `check` rejects these certificate denominators and always invokes the helper with its fixed integer default `D=10^9`. This does not bypass either supported whole-certificate entry point. A future public generic flow API should validate its denominator and graph arguments itself.

Missing required keys and certain malformed containers raise `KeyError` or `TypeError`, rather than a uniform validation error. They nevertheless stop validation and never return `PASS`. This is error-reporting robustness, not a false certification path.

## Strongest verified result and exact limit

The deposited pinned checker passed the genuine full certificate and rejected every altered-file test before parsing. With the pin intentionally bypassed through its direct API, the checker rejected the tested substantive mathematical corruptions. Static inspection explains why accepted JSON data must match the fixed graph/terminal order and satisfy all exact integer divergence and energy constraints: current types and all divergences are checked, per-row energies are recomputed, and both the exact total and denominators are fixed. The permissive cases above preserve those constraints.

This audit does **not** independently prove that the indexed graph is the intended mathematical graph, establish the infinite free-FUSF transfer, check novelty/priority, or constitute exhaustive formal verification of Python or the checker. Those are separate evidence obligations. No finding here blocks promotion of the finite certificate on parser-integrity grounds; promotion of the overall theorem remains dependent on the independent mathematical reviews.
