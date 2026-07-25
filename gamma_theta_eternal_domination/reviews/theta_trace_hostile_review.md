# Hostile review of the complement-coloring trace certificate

**Audit time:** 2026-07-25 14:00 PDT  
**Reviewer role:** independent adversarial reviewer; no generator, checker, CLI,
graph, or test implementation was modified.  The only code added by this
review is `reviews/theta_trace_hostile_probe.py`.

## Verdict

I found **no soundness defect** in the proof format, generator, or replay
checker on bounded valid inputs.  If
`check_uncolorability_trace` accepts a certificate, its reconstructed tree
really exhausts every assignment of colors `0,...,k-1` to
\(\overline G\), and no branch is a complete proper coloring.  It therefore
certifies

\[
  \chi(\overline G)>k,\qquad\text{equivalently}\qquad \theta(G)>k.
\]

There is no hidden color-name symmetry break: the root has all \(k\) named
colors, and every internal node has exactly all colors legal under the
reconstructed partial assignment.  The checker binds both the graph6 record
and \(k\), can additionally require an externally supplied graph and \(k\),
and rejects structurally incomplete or overcomplete trees.

The format is **accepted as a mathematically valid independently checkable
theta lower-bound certificate for the campaign's bounded targets** (currently
orders at most 12 and small \(k\)).  A decisive verification command should
always pass both `--graph6` and `--k`, and the returned whole-certificate
SHA-256 should be placed in the artifact manifest.

It is **not yet accepted as a fully hardened parser for arbitrary untrusted
files** because of the two availability/error-normalization findings below.
Neither finding permits a false proof to be accepted.  The CLI catches the
second issue and exits nonzero; the first can consume unbounded resources
before a verdict.

## Audited snapshot

| File | SHA-256 |
|---|---|
| `src/verifier_b/coloring_trace_generator.py` | `c071540e8afd9bfeb361792678a1bdb7a8c263d880c080b6b1a5d5adc3b058e6` |
| `src/verifier_b/coloring_trace_checker.py` | `006ef73ab5ae5ae5e122fdafc08988a4b6229d966a479c2415528c2ed23b6342` |
| `src/verifier_b/coloring_trace_cli.py` | `67b61fa7ad600408bc70d1d7bb07afcb43556a6949bf270b98e25bcdb4974c82` |
| `src/verifier_b/graph.py` | `12b77a569e16eb8d7aa94ecb0f37800944effb7e9d8b73814adc1ec9a1777237` |
| `src/verifier_b/COLORING_TRACE.md` | `4d194d8818a0ad805aeeb0b29d7f10674bb044fd4954df6a1e898783e7584a28` |
| `tests/test_coloring_trace.py` | `f0941ba2589b104f593d7808fe6352d3641a77620159f51e01c377e0d8f85612` |
| `reviews/theta_trace_hostile_probe.py` | `cef014f3b1f7297a8b680071513df35f8908ed1d66e3fedbe27ba79d82146bb8` |

The implementation hashes above were rechecked after all probes.  The
review-only probe hash identifies the exact script that produced the results
below.

## Severity-ranked findings

### Medium — a tiny certificate can request an unbounded color loop

The checker accepts any nonnegative integer in the header as \(k\), then
materializes the full list of colors by iterating `range(color_count)` at
`coloring_trace_checker.py:139-148`.  The generator does the same at
`coloring_trace_generator.py:127-135`.  A few-kilobyte JSON header can encode
a roughly 4,000-digit integer that Python will parse, after which either
program can run until memory exhaustion while building the root's
`legal_colors`.

This is only an availability defect; it cannot make a false claim verify.  It
matters on the campaign's 16 GiB laptop, where all computations are required
to stay responsive.

There is a complete semantic guard available.  For a graph of order \(n\),
the complement is \(k\)-colorable whenever \(n=0\) or \(k\ge n\) (give every
vertex a distinct color).  Hence every true noncolorability certificate has
\(n>0\) and \(0\le k<n\).  The checker should reject all other headers before
entering the color loop; the generator can report the explicit distinct-color
coloring immediately.  This both proves the early exit and caps the loop by
the graph order.

### Medium — the documented Boolean wrapper can raise on malformed JSON

`verify_uncolorability_trace` is documented as a fail-closed Boolean wrapper,
but its exception list at `coloring_trace_checker.py:212-219` omits plain
`ValueError`.  Python's JSON decoder raises a plain `ValueError`, rather than
`JSONDecodeError`, when an integer token exceeds the interpreter's digit
limit.  A header containing a 5,000-digit `k` therefore makes
`verify_uncolorability_trace(path)` raise instead of returning `False`.
`_LineReader.read_object` at lines 251-256 also fails to normalize this case
to `TraceVerificationError`.

The command-line verifier already catches `ValueError` and exits with status
1, so the standalone CLI does fail closed.  The programmatic Boolean API does
not.  Catching JSON's plain `ValueError` in `read_object` and wrapping it as
`TraceVerificationError` is the narrow fix; also catching `TypeError` and
`ValueError` in the Boolean wrapper would harden invalid API arguments.

Minimal reproducer:

```python
path.write_bytes(
    b'{"claim_sha256":"x","format":'
    b'"gamma-theta-complement-coloring-unsat-v1","graph6":"@",'
    b'"graph6_sha256":"x","k":' + b"9" * 5000
    + b',"type":"header","vertex_order":"least-uncolored"}\n'
)
verify_uncolorability_trace(path)  # raises ValueError, rather than False
```

### Low — “canonical graph6” means canonical encoding, not canonical labeling

The check `Graph.from_graph6(g).to_graph6() == g` establishes the unique
shortest graph6 syntax for that **particular vertex labeling**, including
payload length and zero padding.  It does not establish that the labeling is
the canonical representative of the graph's isomorphism class.  This has no
bearing on the theta proof, which is label invariant, but the campaign's final
graph-data requirement separately asks for a canonical Graph6 string in the
isomorphism sense.  That stronger property must still be supplied by the
nauty canonicalization pipeline; the trace checker should not be cited as
proving it.

## Proof-format soundness audit

At recursion depth \(v\), the checker has reconstructed colors for exactly
vertices \(0,\ldots,v-1\).  It recomputes

\[
L(a,v)=\{c\in\{0,\ldots,k-1\}:
          c\ne a(u)\text{ for every already-colored }
          u\in N_{\overline G}(v)\}.
\]

It requires the node's `legal_colors` field to equal the increasing list
\(L(a,v)\), not merely a subset.  It then consumes one child subtree for
every \(c\in L(a,v)\), in order, after extending the reconstructed assignment
by \(a(v)=c\).  Consequently no legal color can be omitted, duplicated, or
reordered without rejection.  This uses no color permutation or graph
automorphism assumption.

Induct on the number of uncolored vertices.  A node with \(L(a,v)=\varnothing\)
has no extension.  Otherwise every proper extension chooses exactly one
\(c\in L(a,v)\), and the checker successfully verifies that child's
nonextendibility.  If a branch ever reaches \(v=n\), the checker rejects,
because the reconstructed assignment is then a complete proper coloring.
Acceptance at the root therefore proves that no proper \(k\)-coloring exists.

The preorder stream is unambiguous even though a node does not repeat the
branch color: the checker itself loops over the exact ordered legal-color
list, sets that color, and consumes precisely one recursively delimited
subtree.  A premature footer is read where a node is required; a missing
subtree reaches EOF or the wrong record; an extra subtree remains after the
expected tree and prevents the expected footer/EOF.

The header's graph6 and \(k\) are used directly in replay, while the
domain-separated hashes detect ordinary corruption.  The optional
`expected_graph` and `expected_k` comparisons prevent a valid proof for a
different claim from being substituted.  SHA-256 is not needed for the
logical induction: even a party able to rewrite the header hashes must still
supply a complete replay-valid tree for the rewritten graph and \(k\).

## Generator audit

The generator uses the same fixed least-uncolored vertex order stated by the
format, but it does not share a transition routine with the checker.  It
writes the exact legal colors, recursively explores every listed color, and
raises `ColorableGraphError` as soon as any branch reaches depth \(n\).  The
temporary output is then deleted, so a colorable graph cannot leave a newly
published certificate.  For a genuinely uncolorable graph every branch ends
at an empty legal-color node and the footer is written only after the whole
tree.

Output publication is atomic: the generated sibling temporary file is
flushed, `fsync`ed, and renamed only after completion.  With
`overwrite=False`, a target created during generation is not overwritten.
An existing target also survives a failed `--overwrite` generation, which is
the safe behavior provided callers respect the nonzero result.

The full unsymmetrized format is exponentially large in the worst case and
generation is not resumable within a single tree.  This is an operational
limitation rather than a logical flaw.  It was small in the current targets:
the 56 published \(k=3\) traces together used only 6,098 nodes.  Before using
the format at materially larger \(n\) or \(k\), jobs should be time-boxed and,
if needed, the root search should be partitioned into independently checkable
subclaims rather than allowing a nonresumable multi-gigabyte trace.

## Independence audit

The generator and checker do not import verifier A, `src/search`, verifier B's
DSATUR solver, or verifier B's invariant routines.  Each imports only the
ordinary set-based `verifier_b.graph.Graph` representation from campaign
code.  The checker does not import the generator; format constants, hash
construction, legal-color computation, and recursion are separately written.
Sharing the graph parser is transparent and does not share the claim-solving
core.

The hostile probe's truth oracle is independent of complement construction:
it works directly in \(G\), recursively assigning clique-part labels and
requiring two equally labeled vertices to be adjacent in \(G\).  Its second
trace replayer likewise checks that direct clique condition and does not call
the campaign checker, verifier A, the search stack, or the DSATUR routine.
For the order-at-most-11 MMV records it also independently decodes the
one-byte graph6 format and compares the resulting edge set with verifier B's
parser.

## Exact adversarial evidence

Command:

```text
PYTHONHASHSEED=0 python3 -u reviews/theta_trace_hostile_probe.py
```

Result:

```json
{
  "claims_checked_through_order_5": 6505,
  "cli_checks": 12,
  "false_claims_rejected": 3572,
  "independent_oracle": "direct clique-partition recursion",
  "independent_replayed_nodes": 12521,
  "labeled_graphs_through_order_5": 1100,
  "mmv_records": 56,
  "mmv_trace_nodes": 6098,
  "mutated_or_truncated_proofs_rejected": 1027,
  "outcome": "all soundness comparisons agreed; one wrapper robustness bug reproduced",
  "true_certificates_checked": 2933,
  "wall_seconds": 3.1771572080033366
}
```

The 6,505 exhaustive claims cover every \(k=0,\ldots,n\) on every labeled
graph through order 5.  The oracle classified 2,933 as true theta lower-bound
claims; generator, campaign checker, and independent replayer all accepted
exactly those.  It classified 3,572 as false; the generator found an explicit
coloring, raised, and left no output for every one.

The 56 records in `instances/mmv2022_table9.csv` were independently decoded
and independently shown not to admit a three-clique partition.  All 56
generated \(k=3\) traces passed both replayers.  C5 at \(k=2\) was checked
separately.

The malformed-stream test rejected all 1,005 proper byte prefixes of the C5
proof plus 22 structural, header, color-list, footer, JSON, and trailing-byte
mutations.  These included an internally rehashed changed \(k\), an
internally rehashed changed graph, omitted/duplicated/reordered colors,
omitted/duplicated nodes, an early footer, wrong node count, wrong trace hash,
unknown fields, duplicate JSON keys, non-ASCII, missing LF, and bytes after
the footer.

Boundary probes confirmed:

- the empty graph is colorable for \(k=0,1,3\), so no proof is published;
- every nonempty graph tested has a valid \(k=0\) proof, including the
  singleton;
- \(k=n\) colorable claims are rejected throughout the exhaustive sweep;
- negative and Boolean \(k\) arguments are rejected;
- a 63-vertex graph at the graph6 one-byte/18-bit order boundary verifies at
  \(k=0\); and
- twelve independent CLI probes gave the documented success/nonzero exit
  codes for valid, false, mismatched, malformed, missing, and boundary inputs.

The full checked-in suite was also rerun:

```text
python3 -m unittest discover -s tests -v
Ran 58 tests in 2.546s
OK
```

## Required follow-up

1. Add the mathematically sound \(n>0\) and \(k<n\) guard to generator and
   checker before accepting arbitrary external trace files.
2. Normalize every JSON parsing `ValueError` to `TraceVerificationError`, and
   make the documented Boolean wrapper return `False` for all malformed
   content/API inputs.
3. Add permanent regressions for the 5,000-digit integer and a parseable but
   enormous \(k\).
4. In final artifact instructions, invoke verification with external
   `--graph6` and `--k`, record the full certificate hash, and use nauty—not
   this checker—to establish canonical isomorphism labeling.

## Fix-verification addendum — 2026-07-25 14:08 PDT

Both medium findings above are **fixed and independently reverified**.  The
low graph6 terminology issue is also clarified in the format documentation.
This addendum supersedes the conditional language in the original verdict:
the current implementation is **unconditionally accepted for the campaign's
theta lower-bound certificates**.  No soundness, fail-closedness, or
resource-bound defect remains within the stated small-order campaign scope.

### Updated audited snapshot

| File | SHA-256 |
|---|---|
| `src/verifier_b/coloring_trace_generator.py` | `07b3b434744051003f7e66057cf0dcafe5eaed39d70b48c8d5fb6e94d737b56f` |
| `src/verifier_b/coloring_trace_checker.py` | `00d8c03a6aadc62045dca540a52b2cfade712fb26d6304c0b4e328882730f1d5` |
| `src/verifier_b/coloring_trace_cli.py` | `26fe36eeb3bb69fc3439fbe26bd0d5e270adcebfb59ab640ca4735d1e78c2935` |
| `src/verifier_b/graph.py` | `12b77a569e16eb8d7aa94ecb0f37800944effb7e9d8b73814adc1ec9a1777237` |
| `src/verifier_b/COLORING_TRACE.md` | `214447f75b592f501f56543008074689e17bd0f1a319db019379b8e5fec0ac2b` |
| `tests/test_coloring_trace.py` | `3176ab2c942fb8e11bae8d9fdb6b395e5912f1ba11360b40b799603ab9ff90e1` |
| `reviews/theta_trace_hostile_probe.py` | `741260a8ba907282ee1d5985ee349813eb38630fe307cbdfc1de9c54de9b2bf1` |

### M1 closure — semantic bound is sound and precedes color iteration

The generator now handles `n == 0` and `k >= n` immediately after validating
the argument types, before constructing a target file, complement, hash, or
legal-color list.  It returns the explicit coloring `()` for the empty graph
and `tuple(range(n))` for `k >= n`.  The latter is always a proper coloring of
any order-\(n\) graph because all vertices have distinct colors.  Its
`ColorableGraphError` message no longer converts an enormous \(k\) to decimal.

The checker enforces the same theorem immediately after parsing \(G\) and
\(k\), before `range(k)` or claim-hash decimal conversion.  Therefore every
trace that reaches replay satisfies \(n>0\) and \(0\le k<n\); work per
legal-color computation is bounded by the graph order.  The review directly
tested:

- generator input `k = 1 << 100000`, which promptly raised
  `ColorableGraphError`, returned coloring `(0,)`, and created no output;
- a parseable 3,001-digit header \(k\), which raised
  `TraceVerificationError` with the false-lower-bound diagnostic before
  replay; and
- the same parseable huge \(k\) through the CLI, which promptly exited 2.

The guard does not exclude any true certificate: the empty graph is
0-colorable, and every graph on \(n\) vertices is \(n\)-colorable.

### M2 closure — malformed content and API arguments now fail closed

`_LineReader.read_object` now normalizes every JSON `ValueError`, including
Python's integer-digit-limit error, to `TraceVerificationError`.
`verify_uncolorability_trace` now also catches `TypeError`, `ValueError`, and
`OverflowError` in addition to its previous fail-closed exception set.

The original 5,000-digit reproducer now makes
`verify_uncolorability_trace` return `False`; the detailed checker raises
`TraceVerificationError` carrying an `invalid JSON` diagnostic.  Invalid
programmatic arguments (`None` path, Boolean expected \(k\), and negative
expected \(k\)) likewise return `False`.  The CLI rejects the 5,000-digit
certificate with exit status 1 and no traceback.

### Documentation closure

`COLORING_TRACE.md` now says explicitly that canonical graph6 means the
shortest graph6 syntax for a fixed labeling, and that nauty must separately
establish a canonical isomorphism representative.  It also documents and
proves the \(n>0,\ 0\le k<n\) bound.  The earlier low finding is therefore
closed; nauty canonicalization remains an intentional separate artifact
obligation, not a trace-checker defect.

### Full rerun

The updated independent probe:

```text
PYTHONHASHSEED=0 python3 -u reviews/theta_trace_hostile_probe.py
```

reported:

```json
{
  "claims_checked_through_order_5": 6505,
  "cli_checks": 13,
  "false_claims_rejected": 3572,
  "independent_oracle": "direct clique-partition recursion",
  "independent_replayed_nodes": 12521,
  "labeled_graphs_through_order_5": 1100,
  "mmv_records": 56,
  "mmv_trace_nodes": 6098,
  "mutated_or_truncated_proofs_rejected": 1027,
  "outcome": "all soundness comparisons agreed; hardening fixes verified",
  "true_certificates_checked": 2933,
  "wall_seconds": 2.9384762500121724
}
```

Thus the fixes did not perturb any of the original 6,505 truth comparisons,
2,933 independently replayed true certificates, 3,572 rejected false claims,
56 MMV traces, C5 trace, or 1,027 structural/malformed mutations.  The
additional CLI probe is the parseable enormous-\(k\) generation case.

The complete repository test suite was then rerun:

```text
python3 -m unittest discover -s tests -v
Ran 59 tests in 2.496s
OK
```

### Remaining limitations

There are no remaining severity-ranked implementation findings for the
campaign target.  The full tree is still exponential and a single generated
tree is not resumable; Python recursion also limits use on very deep,
large-order certificates.  These are previously documented scalability
limitations outside the current order-12/small-\(k\) target, not certificate
soundness defects.  Continue to time-box larger jobs, retain whole-file
hashes, pass external `--graph6` and `--k` during decisive verification, and
use nauty separately for isomorphism-canonical labeling.
