# Hostile review of exact evaluators A and B

> **Final status update, 2026-07-25 13:49 PDT:** both medium verifier-A
> findings and the later low graph6-header finding were fixed and independently
> reverified. The original audit text is retained as a chronological snapshot;
> the final addendum at the end gives the current verdict.

**Audit time:** 2026-07-25 13:34 PDT  
**Reviewer role:** independent adversarial reviewer; no evaluator source was
modified.  
**Model audited:** attacks only at unoccupied vertices; exactly one guard moves
along one edge to the attacked vertex; every configuration in the family and
every response configuration dominates.

## Bottom line

I found **no mathematical correctness defect** in either evaluator on valid
simple-graph input. In particular, I found no one-guard/all-guards confusion,
occupied-attack error, acceptance of nondominating states, fixed-point
soundness error, graph/complement swap, or unsafe coloring symmetry break.
The two eternal-domination cores are sufficiently independent to make their
agreement meaningful.

The pair is **accepted for exploratory search and exact differential checking
on canonical graph6 records through the current target order 12**, subject to
the limitations below. It is **not yet accepted as the final decisive
certificate system**, and the campaign's required first-72-hour validation
gate has not yet been completed: exhaustive connected evaluation through order
9 is still absent.

Two concrete hardening defects remain in verifier A. Neither changed a value on
any valid graph tested, but both should be fixed before verifier A is presented
as an adversarial standalone checker.

## Audited snapshot

The campaign directory was still untracked in the surrounding repository, so
file hashes, rather than the unrelated enclosing commit, identify the audited
code.

| File | SHA-256 |
|---|---|
| `src/verifier_a/core.py` | `4b10f91d91e90e9ed32f5c6df43ef3b51effb720a3e4017cf8e7a1befafe86e6` |
| `src/verifier_b/graph.py` | `8e41ef22cf3d2d0b9a5fd16d220f9526a2329d2553c3baba6fdfc633f4f43c72` |
| `src/verifier_b/invariants.py` | `6dc2ce5544bfa364a3381e06e91c15864aca6dfd693978e177f8921df432258e` |
| `src/verifier_b/eternal.py` | `cdb8b053416e74e8508d9c3b4e0a373c0b7c68ecbdac9a512b50803295c322d2` |
| `reviews/hostile_oracle.py` | `3be38241af20a020ac92c1cbc3bd8704346d18cb1278108f614b268546882388` |

Machine envelope: MacBookPro18,1, Apple M1 Pro, 10 cores, 16 GiB physical
memory, Python 3.14.6, nauty/Traces 2.9300. All review jobs were single-process
and stayed small enough to leave the machine responsive.

## Severity-ranked findings

### Gate blocker 1 — no independently checkable lower-bound certificate for θ

Both stacks correctly compute `theta` in the tested range, and both emit a
minimum clique partition, which certifies only the upper bound. Neither CLI
emits a proof that the complement is not colorable with one fewer color:
verifier A returns the result of an internal subset dynamic program, while
verifier B returns the result of a backtracking coloring search without a
checkable trace.

This does not invalidate either exact evaluator. It does mean that an eventual
counterexample cannot yet meet the campaign's stated certificate requirement
for `theta >= k+1`. Before a decisive claim, add a proof-producing coloring
encoding (DRAT/LRAT) or a compact independently checkable complete search
trace.

### Gate blocker 2 — the mandatory exhaustive order-9 regression is unfinished

At audit time:

- checked-in unit tests evaluated all labeled graphs only through order 5 in
  verifier A and used transparent parameter oracles only through order 4 in
  verifier B;
- the nauty interoperability unit test went only through connected order 7
  and tested parser/writer round trips, not all parameters;
- the checked-in unlabeled regression log covered order 5;
- this hostile review extended exact A/B comparison to all 11,117 connected
  unlabeled graphs of order 8, but did not run the 261,080 connected graphs of
  order 9.

Thus the evaluators pass a strong interim audit, but the explicit “connected
unlabeled graphs through order 9” prerequisite remains open. This is a
coverage gap, not a found counterexample or an algorithm defect.

### Medium — verifier A silently accepts overlong all-zero graph6 payloads

`BitGraph.from_graph6` checks that there are enough payload bits and rejects
nonzero bits after the required edge slots, but it never requires the exact
payload length. Consequently it silently accepts and canonicalizes malformed
records:

```text
'??'  -> A accepts order 0 and rewrites to '?';  B rejects
'@?'  -> A accepts order 1 and rewrites to '@';  B rejects
'B??' -> A accepts order 3 and rewrites to 'B?'; B rejects
'Bw?' -> A accepts K3 and rewrites to 'Bw';      B rejects
```

Relevant code: `src/verifier_a/core.py`, payload handling around lines 132–140.
The fix is to require
`len(payload) == ceil(n(n-1)/2 / 6)` before padding validation, as verifier B
already does. Add regression cases for both too-short and too-long payloads.
This matters for canonical instance manifests and hashes even though valid
graph6 calculations are unaffected.

### Medium — verifier A's certificate checker can raise instead of reject

`verify_eternal_result` shifts by the supplied response guard before checking a
numeric range. A malformed but type-correct certificate with guard `-1`
raises `ValueError: negative shift count` rather than returning `False`.
Verifier B rejects the analogous negative guard.

Reproducer on `K2`:

```python
g = BitGraph.complete(2)
bad = EternalResult(
    1, (1, 2),
    {(1, 1): (-1, 2), (2, 0): (1, 1)},
    0,
)
verify_eternal_result(g, bad)  # ValueError: negative shift count
```

Relevant code: `src/verifier_a/core.py`, lines 414–418. Validate
`isinstance(guard, int)` and `0 <= guard < graph.n` before shifting. More
generally, an externally facing checker should fail closed on every malformed
certificate rather than relying on dataclass annotations.

### Low — two checked-in “independence” tests are correlated

1. `tests/test_verifier_b.py::brute_eternal_decision` enumerates families, but
   calls verifier B's own `is_dominating` and `verify_eternal_family` to decide
   whether each family works. It therefore does not independently test the
   direct family checker.
2. `tests/test_nauty_interop.py` parses each nauty record with verifier A and
   writes it back with verifier A. A common wrong edge-bit ordering in A's
   reader and writer could pass that test.

The review-only `reviews/hostile_oracle.py` closes both blind spots for this
audit: it uses a Boolean adjacency matrix, directly enumerates nonempty
families through order 4, and obtains edge lists independently from nauty
`showg`. Promote equivalent checks into the permanent regression suite.

## Failure-mode audit

### One guard, one edge, unoccupied attacks

- Verifier A constructs each successor as
  `configuration ^ guard_bit ^ attacked_bit`, with `guard_bit` selected from
  `configuration & graph.adj[attacked]`. The attack loop uses
  `full ^ configuration`, so only unoccupied vertices are attacked.
- Verifier B skips `attack in source`, iterates one `guard in source`, requires
  adjacency, and constructs exactly `(source - {guard}) | {attack}`.
- `C5` at `k=2` rejects the one-guard strategy while the deliberately mutated
  all-guards implementation accepts it.
- `K2` at `k=1` accepts the correct occupied-attack convention while the
  deliberate occupied-attack mutant rejects it.

No variant confusion was found.

### Dominating states

Both builders enumerate only dominating `k`-sets and admit a successor only
when it belongs to that universe. `P3` at `k=1` is the useful trap: the center
singleton dominates, but moving to either attacked leaf does not, and both
stacks correctly reject eternal domination with one guard.

Generated response certificates were also checked directly against a separate
matrix implementation on every labeled graph through order 5. No
nondominating source or target was admitted.

### Greatest fixed point and deletion order

Verifier B performs simultaneous deletion. Verifier A deletes in place during
a scan, despite its prose describing repeated deletion rounds. This is not a
soundness problem: a state is removed only after every witness for some attack
has already been removed, so asynchronous iteration of this descending
monotone elimination reaches the same greatest fixed point.

The review compared both implementations with a separately written
synchronous matrix oracle on every labeled graph through order 5 and found the
identical greatest family at every `k`. A targeted cascade case was
`graph6='FCQb?'`, `n=7`, `k=3`: there are eight initial dominating
configurations, synchronous deletion removes `7` and then `1`, verifier A
reports no family after its in-place iteration (`rounds=3`, including the
terminal stability scan), and verifier B also returns no family.

### γ, i, α, and θ

- `gamma`, `i`, and `alpha` match direct subset-definition oracles on all 1,100
  labeled graphs through order 5.
- Verifier A computes a clique partition directly by subset DP.
- Verifier B colors the complement with complete DSATUR-style backtracking.
  Consecutive introduction of color names is sound because it removes only
  color-name permutations; no graph-label symmetry is imposed.
- A third oracle assigned clique-part labels directly, without constructing a
  complement. It agreed on all labeled graphs through order 5.
- Reconstructed partitions from both stacks were checked for disjointness,
  full coverage, clique validity, and claimed size throughout the hostile
  sweeps.

No complement/coloring or clique-cover/partition error was found.

### graph6 semantics

Both implementations use the same conceptual upper-triangle loop, so their
agreement alone cannot validate edge ordering. The hostile run decoded every
connected order-8 record using nauty `showg -qe`, then independently checked
both parsers and both writers against those external edge lists. All 11,117
records agreed exactly. The only graph6 defect found is verifier A's malformed
trailing-zero acceptance described above.

### Implementation independence

Verifier B imports no verifier-A module. Its graph is a tuple of frozenset
neighborhoods; configurations are frozensets; transitions are explicit
`Move` records grouped by attack; fixed-point deletion is simultaneous.
Verifier A uses integer graph/configuration masks, packed successor-index
sets, and in-place elimination. Their theta algorithms are also genuinely
different (clique-subset DP versus complement coloring).

The shared mathematical definition and ordinary subset loops are unavoidable,
not shared-core dependence. The `src/search/differential.py` driver imports
both stacks, but neither verifier imports that driver.

## Exact commands and results

### Checked-in suite

```sh
python3 -m unittest discover -s tests -v
```

Result at the audited snapshot:

```text
Ran 44 tests in 0.353s
OK
```

### Independent hostile oracle

```sh
PYTHONHASHSEED=0 python3 -u reviews/hostile_oracle.py
```

Result:

```json
{
  "connected_unlabeled_cases": 11117,
  "connected_unlabeled_order": 8,
  "explicit_family_enumeration_through": 4,
  "graph6_semantics_checked_by": "tools/nauty2_9_3/showg",
  "labeled_oracle_cases": 1100,
  "outcome": "all hostile comparisons agreed",
  "random_cases": 2000,
  "random_order_range": [5, 11],
  "seed": 270725,
  "synchronous_oracle_through": 5,
  "wall_seconds": 84.32144499999413
}
```

The same run checked greatest families at every guard count, both clique
partitions, and generated response certificates on the 1,100 labeled oracle
cases.

### Order-12 stress

Using seed `120327`, the review generated 200 labeled graphs of order 12 at
edge probabilities drawn from
`(0.08, 0.20, 0.35, 0.50, 0.65, 0.80, 0.92)` and called
`reviews.hostile_oracle.cross_check_matrix` on each.

```sh
PYTHONHASHSEED=0 python3 - <<'PY'
import random, time
from reviews.hostile_oracle import matrix_from_edges, cross_check_matrix
rng = random.Random(120327)
probabilities = (.08, .20, .35, .50, .65, .80, .92)
started = time.perf_counter()
for case in range(200):
    probability = rng.choice(probabilities)
    edges = tuple(
        (u, v)
        for u in range(12)
        for v in range(u + 1, 12)
        if rng.random() < probability
    )
    cross_check_matrix(matrix_from_edges(12, edges))
print({
    "outcome": "all agreed", "cases": 200, "order": 12,
    "seed": 120327, "wall_seconds": time.perf_counter() - started,
})
PY
```

```text
{'outcome': 'all agreed', 'cases': 200, 'order': 12,
 'seed': 120327, 'wall_seconds': 30.86721441699774}
```

This compared all five parameters, greatest eternal families at every `k`,
and both reconstructed clique partitions. It is a stress test, not exhaustive
order-12 coverage.

### Published 56-graph catalog

The full catalog had SHA-256
`801f054853d07652c795fb16217425869f857d7f5d74e427165d554faf4eae1d`.
I reran:

```sh
temp_review_dir=$(mktemp -d /tmp/gamma-theta-review.XXXXXX)
PYTHONPATH=src python3 -m search.validate_mmv2022 \
  --catalog instances/mmv2022_table9.csv \
  --parameters "$temp_review_dir/parameters.csv" \
  --log "$temp_review_dir/log.json"
```

It reproduced all 56 graphs, the 55 cases with
`alpha = gamma_infinity < theta`, and zero counterexamples, with parameter
histogram:

```text
(1,1,3,3,4): 2
(2,2,2,3,4): 1
(2,2,3,3,4): 52
(2,3,3,3,4): 1
```

The regenerated parameter CSV was byte-identical to
`results/mmv2022_parameters.csv` (SHA-256
`ef74175dfd81542a167feed5a2d7f66be723846993642fb65344d08655b594c6`).
I additionally decoded all 56 records through nauty `showg` and ran the
hostile A/B comparison on those external edge lists; all agreed.

## Recommendation

1. **Verifier B:** accept as an exact, independent small-graph evaluator for
   valid input at the current order-12 target.
2. **Verifier A core algorithms:** accept for canonical valid graph6 input and
   internally generated certificates; fix exact graph6 length checking and
   fail-closed certificate validation before calling it a standalone
   adversarial verifier.
3. **Two-stack trust architecture:** accept provisionally. The independent
   oracle, complete order-8 sweep, order-12 stress, and full published catalog
   reproduction provide strong evidence.
4. **First-72-hour validation gate:** do not mark complete until connected
   unlabeled order 9 is exhaustively evaluated with a resumable manifest and
   coverage count.
5. **Decisive counterexample certificates:** do not accept yet. Add a durable
   external certificate format/checker and a proof-producing lower-bound
   artifact for `theta`.

Nothing in this audit resolves or finitely advances the conjecture by itself;
these are validation results for the computational foundation.

---

## Fix-verification addendum — 2026-07-25 13:45 PDT

### Scope and snapshot

I re-audited only the two requested verifier-A fixes and their new tests. I did
not edit evaluator code.

| File | Re-audited SHA-256 |
|---|---|
| `src/verifier_a/core.py` | `b8abc9efee8b954e6306f3b60674944c843e22f3ff7bd112355415bd62bd63c0` |
| `tests/test_verifier_a.py` | `811ff269e12b7252242ae954cb9486f5850e5454ed0e353b65b0c59f4ea67f50` |
| `reviews/verifier_a_fix_probe.py` | `77b833233494325aca2c2b8f353a59382d75b6205c5a54e394bac96675ac2951` |

### Resolution of the two findings

**FIX VERIFIED — exact graph6 payload length and padding.** Verifier A now
computes the required number of payload characters, requires exact equality,
and separately rejects nonzero padding. This correctly distinguishes:

- missing or truncated order/edge data;
- overlong payloads ending in either zero or nonzero six-bit characters; and
- a correctly sized payload whose unused low bits are nonzero.

The permanent tests cover the original reproducers (`B`, `B??`, `Bw?`, `??`,
`@?`, and `B@`). The review probe additionally checked deterministic valid
graphs at every order 0–20 in string, bytes, and header forms; a canonical
18-bit-header graph at order 63; truncation and two forms of overlength at
each tested order; and every available padding width. Results were:

```json
{
  "valid_records_checked": 64,
  "short_payloads_rejected": 22,
  "overlong_payloads_rejected": 85,
  "nonzero_padding_rejected": 15,
  "explicit_malformed_records_rejected": 23
}
```

No requested payload-length or padding defect remains.

**FIX VERIFIED — fail-closed malformed eternal certificates.** The checker now
validates the result type, exact integer type and range of `k`, family
iterability/hashability, configuration types and ranges, response container,
response tuple shape, exact integer types and ranges of guard and successor,
move legality, target membership/domination, and exact response-key coverage
before returning `True`.

The new permanent test covers the original negative-guard exception,
out-of-range successor, and extra-response cases. The review probe extended
this to 47 malformed certificates using ordinary built-in/JSON-shaped values:

- negative, oversized, Boolean, floating, string, and null guard/count fields;
- negative, oversized, Boolean, floating, string, and null successors;
- empty, noniterable, unhashable, Boolean, negative, out-of-range, and string
  family entries;
- null, list, tuple, and string response containers;
- wrong response shapes, missing and extra keys, an unoccupied guard, an
  occupied nonadjacent guard, and a wrong in-range successor; and
- objects that are not `EternalResult` instances.

All 47 returned `False`; none raised. A valid `C5` certificate and three valid
vacuous-response certificates (orders 0, 1, and a fully occupied `K4`) returned
`True`. No requested fail-closed defect remains for normal serialized
certificate data.

### Commands and results

```sh
python3 -m unittest discover -s tests -v
```

```text
Ran 46 tests in 0.368s
OK
```

```sh
PYTHONHASHSEED=0 python3 -u reviews/verifier_a_fix_probe.py
```

```json
{
  "certificate": {
    "malformed_certificate_cases_rejected_without_exception": 47,
    "vacuous_response_certificates_accepted": 3,
    "valid_certificate_accepted": true
  },
  "graph6": {
    "explicit_malformed_records_rejected": 23,
    "noncanonical_order_headers_still_accepted": {
      "~???": "?",
      "~~??????": "?"
    },
    "nonzero_padding_rejected": 15,
    "overlong_payloads_rejected": 85,
    "short_payloads_rejected": 22,
    "valid_records_checked": 64
  },
  "outcome": "requested fixes pass; noncanonical graph6 order headers remain accepted"
}
```

### Remaining defect found during re-audit

**Low — both graph6 parsers accept noncanonical order headers.** The medium
payload-length bug is fixed, but verifier A and verifier B both accept
over-encoded order values:

```text
~???      -> accepted as order 0, canonical output "?"
~~??????  -> accepted as order 0, canonical output "?"
```

Under the graph6 size encoding, the 18-bit form is for orders 63–258,047 and
the 36-bit form is for orders at least 258,048. These two records are therefore
noncanonical. This cannot change a result on a canonical graph6 record, but it
can silently normalize malformed manifest input and is worth fixing before
freezing canonical hashes. Require decoded order `>= 63` in the 18-bit branch
and `>= 258048` in the 36-bit branch in both parsers, with regressions for the
two strings above.

### Updated recommendation

The two requested verifier-A fixes are **accepted**. Verifier A is now
fail-closed for the tested ordinary malformed certificate data, and its
payload length/padding validation is strict. The low-severity noncanonical
order-header issue does not revoke acceptance for canonical valid graph6
inputs. The earlier, separate campaign gate blockers—exhaustive connected
order-9 evaluation and a durable lower-bound certificate for `theta`—are
unchanged by this addendum.

---

## Canonical-header fix addendum — 2026-07-25 13:49 PDT

**FIX VERIFIED in both parsers.** Verifier A now rejects an 18-bit decoded
order below 63 and a 36-bit decoded order below 258,048. Verifier B enforces
the same lower bounds in its independent order decoder. The exact reproducers
now both raise `ValueError` in both stacks:

```text
~???
~~??????
```

The focused probe also rejected medium-form encodings of orders 1 and 62 and
long-form encodings of orders 1, 62, 63, and 258,047. It accepted and
round-tripped canonical boundary records at orders 0, 1, 62, and 63, including
header/bytes forms. Header-only encodings at the upper medium boundary
258,047 and lower long boundary 258,048 passed the canonical-header check and
then failed for the expected missing payload, confirming that the inequalities
are not off by one.

Re-audited hashes:

| File | SHA-256 |
|---|---|
| `src/verifier_a/core.py` | `f43860bb3048b39f6cb99aba75b60cdfe7c77e0dc1c0489c17851b061fd91af1` |
| `src/verifier_b/graph.py` | `12b77a569e16eb8d7aa94ecb0f37800944effb7e9d8b73814adc1ec9a1777237` |
| `tests/test_verifier_a.py` | `cb271be1bbe1325ca3465ab160e8183079aad577e639b2febfa34fec43848154` |
| `tests/test_verifier_b.py` | `0022048d70ab3fd2c4435c625fa4838701a10f4b0256778e5168bdd0663dfded` |
| `reviews/graph6_header_fix_probe.py` | `6a4b28ad19499e19491b2b7e32b2cba40875dd37cf5ac3ad316e5766d1e8c8a3` |

Commands and results:

```sh
PYTHONHASHSEED=0 python3 -u reviews/graph6_header_fix_probe.py
```

```json
{
  "canonical_large_headers_recognized_before_payload_check": 4,
  "noncanonical_parser_rejections": 16,
  "noncanonical_records": 8,
  "outcome": "canonical order-header fix passes in both parsers",
  "reported_reproducers_rejected_by_both": ["~???", "~~??????"],
  "valid_boundary_forms_accepted": 16
}
```

```sh
python3 -m unittest discover -s tests -v
```

```text
Ran 48 tests in 0.356s
OK
```

**Final input-hardening verdict:** accepted. I found no remaining graph6
length, padding, canonical-order-header, or ordinary malformed-certificate
defect in the re-audited scope. This does not alter the separate order-9
coverage and proof-producing `theta` certificate requirements.
