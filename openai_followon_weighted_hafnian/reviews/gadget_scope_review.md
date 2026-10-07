# Scope-limited independent gadget review

Saved from the final messages of the independently spawned internal adversarial
agent `/root/gadget/attack`, at 2026-10-07 05:21 UTC (2026-10-06 22:21
America/Los_Angeles). This is an automated research check, not conventional
human peer review. The report below preserves the original verdict and its
subsequent confirmation of the corrected proof. Its additional computational
procedure is saved separately in `reviews/gadget_scope_checks.py`.

The older proof hash in the initial report identifies the version reviewed
before a single editorial correction. The subsequent confirmation identifies
the final corrected proof. Implementation and test hashes did not change.
The preservation step did not modify the proof, implementation, test data,
or manuscript and did not rerun tests.

## Original final report

Scope-limited pass: no substantive defect found in the exact gadget, global
reduction, rational scaling, projection, or implementation. This review does
**not** validate the upstream FPRAS, an efficient approximate sampler, novelty,
or a publication package.

I independently reconstructed these points:

- The binary DAG has exactly `W` paths: each step doubles the previous path
  count and adds precisely the optional direct path.
- Split-vertex matchings comprise one source–sink path plus identity edges.
  Other selected components would require directed cycles. Removing both
  terminals leaves only identity edges; removing one leaves odd order.
- In a glued perfect matching, each gadget covers an even number of vertices.
  Its internal order is even, so it uses zero or both original endpoints.
  Active gadgets therefore form an original perfect matching.
- Different gadgets cannot introduce parallel edges: internal vertices are
  private, and direct terminal edges belong to distinct original pairs.
- `D = product(q_e)` has polynomial binary length; `W_e=p_eD/q_e` is integral;
  every original matching has exactly `m` edges. Fiber multiplicity is
  `D^m product(A_e)`.
- The graph-size and arithmetic bounds are polynomial in explicit binary
  input length. Encoding vertex labels adds logarithmic factors and preserves
  polynomial bit complexity.
- The empty instance, zero count, disconnected support, omitted zero edges,
  irrelevant diagonals, and small rational values are covered correctly.
- The conditional TV pushforward argument is valid for a sampler supported
  on perfect matchings. Its existence remains a separate dependency.

One editorial correction: Section 6 describes `2^512` as a “512-bit
denominator.” Its binary length is **513**. Use “denominator `2^512`” or
“513-bit denominator.”

Reviewed SHA-256 values:

```text
proofs/GADGET_PROOF.md
29fa0beb837c255a099d3b1e3301f98d01d6f43d4315ccbed1588048e7cd484e

code/gadget.py
fb5bda83d3474d2c123c58c6213879928bdb27bb25ef6cff43e7a1b447444225

code/test_gadget.py
6372ed3b61ac1e9946b7c57a263206d2f6467f8bfe47be61fdf3107e5bbe57cc
```

Computational checks passed under Python 3.14.6:

- Existing suite, run in memory without overwriting its report: 64 signatures,
  729 integer K4 assignments, 40 seeded K6 instances, 12 boundaries, three
  full fibers, and eight rejected invalid domains. Final reproduction took
  0.511 seconds.
- Independent list-based enumeration agreed with both reference counters on
  **all 32,835 simple graphs** of orders 0, 2, 4, and 6.
- Independent enumeration confirmed all four signature states for
  `W=1,...,64`.
- **80 additional rational instances** passed complete projection-fiber
  comparison, using seed 17012027 and at most two fractional edges per
  four-vertex instance.
- Construction, DAG path count, graph simplicity, and size bounds passed for
  **1000-, 2048-, and 4096-bit weights**. These tests did not attempt
  exponentially expensive perfect-matching enumeration at those sizes.
- Projection rejected empty, truncated, repeated-edge, and outside-edge
  certificates; reversed edge orientations were accepted correctly.

The independent enumerator does not use the asserted signature, gadget
ownership, or scaled-hafnian identity to count expanded matchings. Expected
fiber sizes are computed directly from original rational edge weights. The
existing suite is therefore not circular in the relevant sense.

No reviewed files or reports were modified. Imports disabled bytecode writes.
The complete successful additional-check procedure is preserved in
`reviews/gadget_scope_checks.py`; run it from the dedicated project directory.
Its reference enumeration is finite evidence and does not replace the proof.

## Corrected-hash confirmation

Verified Section 6 now says “the denominator `2^512` (513 bits).” The previous
inaccurate phrase is absent.

Latest reviewed proof SHA-256:

```text
11d1300ce0a8e750b35a7b18e70dd24d683a9374eb92fbeabf4c8c1cb10b0a21
```

The correction resolves the sole editorial finding. The scope-limited pass
remains valid; no files were altered during verification.
