# Postrun hostile review: order-12, k=4 v3 case 1111, attempt 1

Review status: **CERTIFICATE_REPLAY_PASSED_ONE_LEAF_ONLY**

Aggregate status: **INCOMPLETE_NONCLAIM**

This review is scoped to exactly one leaf:

- run: `results/order12_k4_production_v3_seed0`;
- case: `1111`;
- attempt: `000001`;
- cube units: `4`, `14`, `23`, `31`.

No CaDiCaL process was launched during this review. The production run, its
runtime sources, the frozen v2 run, and all provisional artifacts were treated
read-only.

## Verdict

The retained LRAT certificate freshly verifies the exact independently
reconstructed case-1111 leaf CNF with the pinned `lrat-check` executable.
The replay was performed on private temporary copies under the campaign-global
heavy-child lock and the retained production resource bounds.

This supports the recorded `UNSAT_LRAT_VERIFIED` status for this one leaf only.
It does not establish the other fifteen leaves, does not establish Boolean
partition coverage by itself, and does not support an order-12 aggregate
theorem.

## Independent leaf-CNF reconstruction

The reconstruction did not import runner transition, partition, or proof
logic. It read the retained parent bytes, parsed the DIMACS header, derived the
all-positive case-1111 units from cube variables `4, 14, 23, 31`, increased
the clause count by four, preserved the parent body byte-for-byte, and appended:

```text
4 0
14 0
23 0
31 0
```

Parent census:

- variables: 18381;
- clauses: 114742;
- literals: 1180016;
- size: 3992947 bytes;
- SHA-256:
  `adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac`.

Reconstructed leaf census:

- variables: 18381;
- clauses: 114746;
- literals: 1180020;
- size: 3992966 bytes;
- SHA-256:
  `aafc85341993ed030fe72ba222a4efaa5a02f6ea6fa95519a9dd2ed755b94d1f`.

The reconstructed bytes are exactly equal to the retained
`attempt-000001/instance.cnf` bytes. The partition case, attempt
configuration, certificate, and independently derived units all agree.

## Outcome and certificate inspection

The retained decisive records are:

- attempt configuration SHA-256:
  `ee962c55d3a5250cf81d2b520ea1f135f83f902025ef07c3e21ce17acd8a242e`;
- outcome SHA-256:
  `00e3c1916026077009431a0dd15af9c4ffbc9fdb477c182bf046e33c76ed4d6e`;
- certificate SHA-256:
  `7c9705f584ccedddf1b8096d4912878c303898d089c24ff38c122e4bd328ded1`.

The outcome has v3 pipeline status `UNSAT_LRAT_VERIFIED`, leaf claim
`LEAF_UNSAT_AFTER_LRAT_REPLAY`, and aggregate claim `NONE`. The certificate
has leaf status `UNSAT_LRAT_VERIFIED` and aggregate status
`NO_AGGREGATE_CLAIM_PENDING_INDEPENDENT_COVERAGE_AUDIT`.

The outcome inventory is the exact set of retained attempt artifacts. Every
inventory path, size, and SHA-256 matches the current single-link regular file.
Every certificate binding to the CNF, solver result, raw proof, normalized
proof, normalization report, LRAT, six resource reports, and twelve child logs
also matches exactly. The outcome's six child records equal the certificate's
six child records. The retained solver result is exactly
`s UNSATISFIABLE`.

Key proof artifacts:

- raw binary DRAT:
  `a50b814d857e29b5b5556308911c6d1ea119356beb9213ab1a062d1da3caa5ba`,
  215475 bytes;
- normalized addition-only proof:
  `f3401ad850f65db8808cd0949e6899ba6b6718902f83a289225c7f5b6390302d`,
  106318 bytes;
- converted LRAT:
  `90787a09742237e3c38c8b4f36916b2d0ccbd37be3920feb16ddb3306ec228d0`,
  692139 bytes.

## Independent binary-proof scan

An independent canonical unsigned-varint parser scanned both binary streams.

Raw proof:

- total records: 16646;
- additions: 9690;
- deletions: 6956;
- literals: 145507;
- post-empty deletions: 3;
- empty addition record: 16643;
- maximum variable observed: 18352.

Normalized proof:

- total records and additions: 9690;
- deletions: 0;
- literals: 68033;
- empty addition record: 9690;
- maximum variable observed: 18352.

The exact raw addition stream has size 106318 and SHA-256
`f3401ad850f65db8808cd0949e6899ba6b6718902f83a289225c7f5b6390302d`;
it is therefore byte-for-byte the retained normalized proof.

## Fresh private LRAT replay

The retained CNF and LRAT were copied to a resolved private temporary
directory. The originals were hashed and metadata-snapshotted before and after
the replay and were unchanged.

Pinned checker:

- binary:
  `tools/drat_trim_2023_05_22/lrat-check`;
- SHA-256:
  `5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2`;
- source archive SHA-256:
  `2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108`.

Bounds and measurements:

- wall limit: 1800 seconds;
- memory limit: 2048 MiB;
- file limit: 768 MiB;
- exit code: 0;
- timed out: false;
- memory limit exceeded: false;
- termination signal: none;
- measured wall time: 0.09322391601745039 seconds;
- user CPU: 0.072534 seconds;
- system CPU: 0.007064 seconds;
- maximum RSS: 47.8125 MiB;
- peak-polled RSS: 46.5 MiB;
- available memory before launch: 4806983680 bytes.

The checker emitted exactly one clean `c VERIFIED` status, no warning or error,
and empty stderr:

- fresh stdout SHA-256:
  `9651ddfc442f9c7e1659778be8a0e984030b09ac86de757b60bb815425ef2380`;
- fresh stderr SHA-256:
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Secondary read-only runner audit

The committed runner's read-only audit passed with:

- status: `PASS_READ_ONLY_AUDIT_NO_MATHEMATICAL_CLAIM`;
- aggregate status: `INCOMPLETE_NONCLAIM`;
- histogram: one recorded `UNSAT_LRAT_VERIFIED`, fifteen `PENDING`;
- latest checkpoint:
  `3dbb5c8336528603c73a04066be85ee317978603d8a56c3103853aa126625202`;
- runtime sources verified: true;
- proofs freshly replayed by `audit_run`: false.

That secondary audit is provenance confirmation only. The fresh private replay
above supplies the independent semantic check for case 1111.

## Mandatory aggregate boundary

The aggregate order-12 result remains open. Fifteen leaves are pending. A
separate aggregate verifier must freshly replay every completed leaf LRAT
against its bound leaf CNF and independently check the full Boolean partition
coverage before any aggregate mathematical claim is made.
