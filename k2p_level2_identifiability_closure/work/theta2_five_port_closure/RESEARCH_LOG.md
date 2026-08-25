# Research log: theta2 five-port closure

## 2026-08-21 08:20 PDT — primitive gate reopened

- No retained exact theta2 artifact was found; the earlier statement that the
  five-port gate was “closed provisionally” was treated as unproved.
- Exact target census: 1,983 selected-incoming plus 4,155 marginalized-
  incoming completions, with 120 port permutations and four source repairs.
- Goal completion estimate: 15%.

## 2026-08-21 08:48 PDT — topology and descriptor census

- Enumerated all 2,946,240 raw directions under the 1.5 GB cap.
- Per repair: 735,648 displayed-quartet exclusions, 632 tree--sunlet
  exclusions, and 280 survivors.
- Compiled 120 unique descriptors with exact lower-rank histogram
  `14:8, 16:80, 18:32`.
- Goal completion estimate: 45%.

## 2026-08-21 08:57 PDT — corrected selected-graph relation

- Located the cause of five apparent nonquadratic/nonisomorphic cases: the
  exploratory check had passed the full completion graph, including dummies,
  into the mixed canonicalizer.
- Replaying against `selected_graph_from_completion` gives per repair exactly
  88 rank-excluded, 24 quadratic-separated, and 8 isomorphic classes, with no
  unresolved class.
- Goal completion estimate: 70%.

## 2026-08-21 09:00 PDT — symbolic rank upper closure

- The coefficientwise polynomial-vector-field ansatz proves upper=lower for
  all 120 descriptors in 26.9 seconds.  No exception transport is needed.
- Goal completion estimate: 82%.

## 2026-08-21 09:21 PDT — complete raw ledger generated

- Generated the deterministic 2,946,240-row ledger in 423.6 seconds with
  maximum resident size 591,314,944 bytes.
- Exposed 32 explicit canonical isomorphism mappings and all 80 raw member
  transports.
- An adversarial review correctly rejected treating all 80 as physical
  terminals: 56 retain target dummy roles.
- Goal completion estimate revised downward to 72%.

## 2026-08-21 09:40 PDT — fixed-full restoration closure

- Dummy multiplicity: 24 no-dummy, 40 one-dummy, 16 two-dummy raw anchors.
- Six-port layer: 576 children = 504 quartet-separated +72 isomorphic; 32
  isomorphisms retain one role.
- Seven-port layer: 288 children =256 quartet-separated +32 exact full
  isomorphisms.
- Independent in-memory replay passed with 78 exact source mixed-graph
  classes, 12 target classes, 102 directed relation classes, and one status
  per class.
- No higher-leaf algebra and no target marginal openness were used.
- Goal completion estimate: 94%; remaining work is byte-identical full replay,
  mutation suite, and integration of the four-port raw rank-upper bundle.

## 2026-08-21 10:20 PDT — promotion replay complete

- The first full fresh-process replay found a proof-serialization defect:
  auxiliary incidence-edge nodes were named by traversal indices and therefore
  differed across Python hash seeds.  No mathematical census changed.
- Replaced those auxiliary IDs by the lexicographically minimal induced map on
  actual mixed-graph vertices, obtained from the full exact incidence
  isomorphisms.  All 32 base maps have the same aggregate SHA-256 under hash
  seeds 1 and 777:
  `01ab6664cc7aec41396cedf34c8d52b9083313398887f0e2e00e7cb698ae013c`.
- Structural replay passed; all 16 adversarial mutations were rejected with
  zero survivors.
- Full isolated regeneration passed byte-identically in 468.07 seconds with
  maximum resident size 606,601,216 bytes.
- Best-guess completion: **100%** for the primitive theta2 five-port gate and
  its fixed-full six/seven-port restoration closure.

## 2026-08-24 21:20 PDT — fail-closed compiler provenance rebind

- Preserved the frozen theta2 artifacts and required their exact legacy
  compiler, canonicalizer, and input-lock bindings.
- The full replay now reconstructs the current rank and restoration gzip bytes
  by replacing only the enumerated provenance fields, then derives the two
  summary metadata rows and summary seal.  All other artifacts remain subject
  to literal byte identity.
- Structural replay passed all 2,946,240 rows.  The producer mutation suite
  rejected 18/18 cases, including wrong legacy compiler and canonicalizer
  bindings, with zero survivors.  The full 2.9-million-record generation was
  intentionally not rerun at this checkpoint.
- Best-guess completion remains **100%** for the primitive theta2 gate; final
  end-to-end release replay remains an outer package qualification step.
