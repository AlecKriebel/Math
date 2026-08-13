# Adversarial review: compact path-bound probe format

## Verdict

**UNRESOLVED for release-scale promotion.**

The result divides cleanly:

- **VERIFIED:** the current one-path compact shard is a lossless encoding of
  the corresponding already-audited verbose relations.
- **VERIFIED AFTER CORRECTION:** the regenerated summary now binds the exact
  schema bytes through `schema_specification_sha256`; the earlier missing
  field was an implementation-version transition, not a semantic failure.
- **FALSE:** the current standalone shard merger is not a semantic
  completeness verifier, although it emits `EXACTLY_COMPUTED`.
- **UNRESOLVED:** class codes 1 (strict sign) and 3 (ordinary `T`) are not
  exercised by this triangle-free smoke, and no full n4/n3 sharded compact
  output has yet passed this clean-room review.

This review concerns only the evidence format.  It makes no claim about the
global JC theorem.

## Exact smoke result

The clean-room implementation imports no primary or prior-review module.  It
independently reconstructs the frozen path inventory, narrow root
suppression needed for blob-arc recovery, admissible internal arcs,
deterministic port insertion and deletion, graph content addresses, packed
word decoding, and the complete source-to-target relation ordering.

For path index 0 it obtains:

| item | exact count |
|---|---:|
| `A+p` directed relations | 121 |
| conditional `A+p+q` directed relations | 1,584 |
| all decoded relations | 1,705 |
| generic polynomial separations | 1,562 |
| labelled isomorphisms | 143 |
| used witness bodies | 64 |
| used transport bodies | 110 |
| used polynomial bodies | 22 |

Every decoded relation agrees with one and only one verbose binding.  The
comparison includes:

1. source and target direction;
2. base state, path, and fixed-full root provenance;
3. source and target parent graph bodies and normalized IDs;
4. row-major `p` arc-pair indexing;
5. conditional `q` block order and shape for every allowed `p` cell;
6. exact inserted vertices, labels, and subdivided arcs;
7. exact deletion to the stated parent;
8. source and target child graph IDs and bodies;
9. verbose binding and state content addresses;
10. classification and complete witness or transport body;
11. parent-transport coherence for `q`;
12. absence of missing, duplicate, trailing, or orphan records.

The normalized 1,705-record comparison digest is

`0f55c0c74946409ece9d98dbccb3e0ab7c7e4ba33b0440926f2ae4bfcbd26e89`.

The current compact shard therefore does not lose a source embedding, port
matching, direction, witness, or transport relative to the verbose stream.

## Mutation sensitivity

All eleven semantic mutations are rejected after recomputing the mutated
path-record content address, so rejection does not merely come from the outer
file hash:

- relation deletion;
- relation duplication;
- truncated `q` block;
- changed admissible-arc order;
- source/target reversal;
- wrong witness index;
- wrong transport index;
- wrong parent;
- wrong fixed-full root;
- cross-path provenance merge;
- duplicate path row.

The first rejection category for every mutation is preserved in
`certificates/compact_smoke_mutations.json`.

## Schema and collision review

The row key `(path_index, stage, p_flat[, q_local])` is a bijection onto the
raw Cartesian arc-pair universe for this smoke.  Conditional `q` blocks are
delimited by independently regenerated child-arc counts, not by trusting the
stored block list.  Numeric witness and transport indexes are shard-local,
contiguous, and checked against complete normalized bodies.  Every stored
library body is used, every referenced polynomial is present, and every
compact polynomial equals the verbose body with the same content address.

SHA-256 is used only as an integrity/content-address layer in the artifact.
The clean-room semantic comparison also compares the normalized bodies
directly, so the smoke verdict does not rest merely on equal hashes.

Two branches remain unexercised.  The smoke has no strict-sign separator and
no ordinary-`T` terminal.  Code paths 1 and 3 are structurally analogous to
the verified witness and transport branches, but analogy is not a replay
certificate.  Before promotion, add at least one graph-derived fixture for
each and apply the same relation-by-relation and mutation checks.

## Preserved merge-layer failure

The black-box test executes `primary/merge_compact_probe_shards.py` without
importing it.  The genuine one-path shard is correctly rejected as incomplete
(1 of 132 paths).  However, after changing only summary declarations and
letting the merger hash the modified summary, it accepts all of the following
and writes an `EXACTLY_COMPUTED` manifest:

- `path_inventory_count = 1` while retaining the 132-path inventory
  commitment;
- a forged aggregate classification count;
- a nonempty unresolved-classification list paired with producer status
  `EXACTLY_COMPUTED`;
- an incorrect `schema_specification_sha256`;
- an incorrect path-inventory commitment.

It now checks the existence and byte/logical hashes of all four shard
streams, so the older missing-library defect is already corrected.  The
remaining problem is semantic: the merger compares declarations across
shards but neither reconstructs them nor binds successful primary and
clean-room replay certificates.

This does not invalidate the verified one-path row codec.  It does prevent a
merged manifest, by itself, from certifying gapless semantic coverage.

## Required correction before n4/n3 promotion

The release-scale gate should require all of the following:

1. The merger recomputes the schema-file hash, bit-cache hash, input hashes,
   path inventory count, and path-inventory commitment from the committed
   sources.
2. Each shard is accompanied by a primary semantic replay and an independent
   replay whose certificates bind the exact shard-summary SHA-256.
3. The merger binds those replay certificates and rejects any shard lacking
   both successful statuses.
4. Either the merger or the bound replays decode all cells, recompute class
   counts, reject unresolved classes, validate library indexes and content
   bodies, and reject orphan witnesses/transports/polynomials.
5. A compact fixture exercises strict-sign code 1 and ordinary-`T` code 3.
6. The full n4 compact stream is compared relation by relation with all
   168,582 audited verbose bindings before the representation is used for n3.
7. Full multi-shard mutations include a deleted range, duplicated range,
   cross-shard path merge, altered shard summary, and a replay certificate
   bound to the wrong summary.

After those changes, this clean-room decoder is suitable for rerunning on a
full n4 shard set and on n3 shards.  Until then the correct status is
`UNRESOLVED`, not `VERIFIED`.

## Reproduction

Run:

```bash
bash reviews/compact_probe_format/verify_all.sh
```

The wrapper runs the semantic comparison twice and requires byte-identical
certificates.  It then reproduces the expected merge-layer failure and checks
the exact malformed cases that are currently accepted.

Key hashes at review time:

| artifact | SHA-256 |
|---|---|
| `primary/COMPACT_PROBE_SCHEMA.md` | `af4de0d81a6597e627b5c5bd3ee92c86b8c5bd85bfd4caf4e0315fec5107d7a4` |
| compact smoke summary | `0c8469402313746a151b85679a99f741ac19d35fe9bfa6fa28faa8e93ce2e0d2` |
| verbose theta2 summary | `e9f68bfb7333e25d0cb9dd2851fba4c88e032052c0a3664f46f3c640640a870b` |
| clean-room implementation | `d7b2a5fb093431ca7b5bd2e68586db92c5ac828e6ac09a91277e6d6ee8cc1ccb` |
| clean-room smoke certificate | `9fe537bb2d75a2a28fd1aa9e88545e2271682150c7adee6ea9414c35835c539d` |
| mutation certificate | `2478d200acf408e3a35d3c6d1fa2c173751db9576317d5872ab5689eb4999b3c` |
| merger under review | `f6cbc81d12811f2cf58b2540d8b9553e7ed673f52affe46ae58560d4db599d35` |
| merge adversarial certificate | `b1daee3579a71f3921e3344583f9bc95635550b76a23efd926727e9c5c754ca9` |

No primary file was changed by this review.
