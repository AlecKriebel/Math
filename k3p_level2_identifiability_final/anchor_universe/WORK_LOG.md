# Work log

## 2026-08-27T22:28:14Z — source audit and first active producer checkpoint

Completion estimate: **70%** toward the C2 repair.

- Located the complete legacy theta2 and cycle producer sources and checked
  their exact finite censuses.
- Defined the active boundary as graph construction, physical incoming-port
  metadata, exact mixed relations, and fixed-full restoration only.  K2P
  algebra is forbidden.
- Implemented the graph-only producer and completed its first exhaustive run
  in 174.600 seconds.
- Derived 133 non-four anchors: 117 isomorphisms and 16 ordinary triangles.
- The run exposed 44 abstract theta2 mixed-graph isomorphisms per source that
  arise only after deleting a marginalized target incoming role.  The active
  producer now records these as incoming-boundary mismatches rather than
  silently relying on the historical rank filter.
- A terminal structural-locator audit matched all 133 legacy non-four rows.
  Twelve restored-cycle source hashes differed only because the new insertion
  helper had added a redundant `dummy_name=None` attribute.  The helper was
  corrected to reproduce the public graph serialization exactly.
- Remaining work: fresh deterministic producer run, separate no-import
  verifier, coherent mutation suite, complete 43+133 crosswalk, and final
  focused replay.

## 2026-08-27T22:56:09Z — complete C2 gate checkpoint

Completion estimate: **100%** toward the scoped C2 anchor-universe gate in
this directory; global manifest and theorem-gate integration remain with the
parent effort.

- Replayed the final graph-only producer in 172.088 seconds.  It derives 133
  non-four seed rows with ordered semantic-key root
  `6c2eaccd894aaf2dc4dd8bde2f1590fc753e5e6ee53b18102b6fa8ede865df7a`:
  one tree, 36 cycle rows, and 96 theta2 rows.
- Replayed the separate clean-room verifier in 25.343 seconds.  It imports no
  producer or atlas and compares all 133 row bodies, keys, source/target graph
  hashes, censuses, and exhaustive raw/restoration cardinalities.
- Explicitly enumerated the 176 marginalized-incoming theta parents and their
  424 fully physical graph-isomorphic restoration paths: 56/176/192 at
  restoration depths one/two/three.  All 984 nonempty prefixes are exact.
- Certified a canonical restriction/root-movement transport for all 424
  paths into 15 theta seed graph-pair classes, including the transported
  source and target one-port attachment edges.  Mapping digest:
  `29afb6d8ab4adc9e3fb588063d19ac7f7caed40ae0364034d8fc9b9951d2bff2`;
  unmatched paths: zero.
- Reconciled those transports in 18.39 seconds with 66 distinct existing
  `isomorphic` one-port ledger rows and 66 canonical one-port relation classes.
  This terminal crosswalk uses the frozen contract only to resolve legacy
  graph-hash identities and site indices after the clean-room set is fixed.
- Crosswalked the 133 derived rows with the separately active 43 four-port
  rows to the complete 176-row contract.  Final relation census: 143 exact
  isomorphisms and 33 ordinary triangles.
- Rejected 11 coherently resealed artifact mutations plus optimized execution
  in 309.190 seconds; the clean control passed.
- K2P polynomial, rank, sign, Fourier, and separator evidence remain forbidden
  and unused throughout the active derivation and verification.

## 2026-08-28T00:28:51Z — exhaustive four-port descendant closure

Completion estimate: **100%** toward C2, including the raw four-port and
downstream fixed-full completeness boundary.

- Replaced rowwise reliance on the 43 designated four-port serialization rows
  by a graph-only replay of all 144 raw equality parents.  They comprise 30
  isomorphic and 114 triangle presentations in nine ordered graph-pair
  classes, all represented by the 26 direct serialization rows.
- Exhausted all 1,260 first-restoration requests and all 96 second-restoration
  requests.  They map to 161 existing one-port rows and 64 existing two-port
  rows, respectively, with exact relation agreement and zero unmatched
  requests.  The 17 restored serialization rows account for 11 terminal pair
  classes; the eight remaining terminal presentations are already reached by
  four existing triangle descendants.
- Bound the raw ledger and graph core, both port manifests, both port ledgers,
  and the two-port parent inventory into the crosswalk and integrated gate.
  The crosswalk payload is
  `3466b1341cc8d9fd22c96dc51ca89cddd67a69b01936394d76eef7b99eda0d62`.
- Expanded the mutation evidence to 16/16 rejected attacks.  Four new
  coherently rebound attacks reach the raw-parent count, used P1 equality
  status, used P2 separation status, and extra-terminal identity checks.
  The report payload is
  `90344a9dc622e129d8e03a04ac1334796b46663bfab2fdd154ca1fb458e879e3`.

## 2026-08-28T01:55:16Z — portable mutation-certificate v3

Completion estimate: **100%** toward the scoped anchor-universe gate; final
release replay remains with the parent effort.

- Removed runtime, traceback, absolute-path, and temporary compressed-byte
  data from the logical mutation payload.  Every subprocess result is still
  checked before sealing for its stable pass sentinel or exact failure code.
- Temporary mutation ledgers are written as canonical JSONL inside gzip streams
  with `mtime=0` and no embedded filename.  The report binds decompressed
  bytes/content plus exact logical row censuses and ordered row roots, so its
  theorem payload is independent of gzip implementation details.
- The standalone suite rejects all 16 attacks.  Report SHA-256:
  `3a6358848df8f677358b16a42bb96e913de35c57f78c5870a491e37dfcf24ae4`;
  logical payload:
  `1ce5f3f9a5947ed4814c1d99b6b21ca85541931dcef36234e3889bb8730d43c5`.
- The integrated gate now checks the v3 portability policy, exact diagnostic
  codes, logical commitments, and the absence of forbidden ephemeral fields.
