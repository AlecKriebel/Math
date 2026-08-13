# Primitive and directed-relation certificate contract

## Primitive records

Every canonical primitive record commits to:

- the locked convention digest;
- core type and total boundary-port count;
- canonical labelled mixed graph and its content hash;
- internal directed presentation transported to canonical vertices;
- reticulation order and ordered incoming-parent edges;
- binary, acyclic, reachability, tree-child, simple-standard, level, and
  strong-arrow-tail validation traces;
- every displayed switching;
- every selected/deleted edge and descendant port mask;
- the complete exact JC coordinate compiler version;
- a displayed-parameter signature and tensor sample hash;
- every raw presentation merged into the record, with vertex, edge, port,
  reticulation, and inheritance-parent transports.

The graph hash is never inferred from a historical topology identifier.

## Decorated directed relations

A relation record is the canonical coloured disjoint union of the source and
target mixed graphs.  Source and target colours are distinct.  One explicit
`MATCH` edge joins each source port to its corresponding target port.  The
record additionally stores:

- source and target primitive hashes;
- source-to-target direction;
- the complete port bijection;
- incoming, outgoing, selected-support, restored-support, and sink roles;
- source and target raw-to-relation vertex maps;
- edge, reticulation, inheritance-parent, label, and Fourier-coordinate
  transports when applicable;
- a classification and a witness binding hash.

Thus two relations with the same target but different source embeddings or
port correspondences are different records.

## Universe commitments

Each manifest stores sorted primitive and relation record hashes, exact raw and
canonical counts, duplicate counts, a deterministic Merkle root, generator
source hashes, and a hash of every preserved failure.  The verifier regenerates
these objects from the primitive rules.

The selected-completion audit additionally commits to the contracted directed
core, every minimum repair, selected sink mask, selected ordinary segment
occupancy, corrected `selected_retains_strong_core` bucket, fixed-core graph
check, and the dummy-rule false-negative witness. Dummy presence is never used
as the core-retention predicate. A separately bound sink-omission witness
records that this predicate does not decide intrinsic selected `S_TC` after
arbitrary reduction.

## Mandatory rejected mutations

The contract tests reject at least:

1. deletion or duplication of a primitive;
2. deletion or duplication of a relation;
3. a changed mixed edge or reticulation arrowhead;
4. a changed port correspondence;
5. a changed raw-to-canonical vertex or edge map;
6. reversal of source and target without rebuilding the relation;
7. swapping witness bindings between relations;
8. changing an inheritance-parent transport;
9. retaining stale record-set or Merkle hashes.
10. marking the preserved dummy-bearing core-retention witness as nonretaining;
11. promoting the fixed-core predicate to intrinsic selected `S_TC` membership.
