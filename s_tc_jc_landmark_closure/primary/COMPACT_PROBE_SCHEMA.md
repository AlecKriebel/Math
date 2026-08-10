# Compact path-bound probe certificate

Status: implementation specification; not a theorem certificate.

The three-outgoing hard cover is expected to have thousands of raw terminal
paths.  Expanding every `A+p` and conditional `A+p+q` relation into the
verbose four-stream schema would duplicate deterministic graph and transport
data many millions of times.  The compact certificate stores the same
decorated directed relation universe without that duplication.

## 1. Frozen path inventory

Base summaries are ordered by their normalized project-relative path.  Within
each summary, allowed terminal states are ordered by `state_id`, and each
state's `raw_coverage` rows are ordered by `path_binding_id`.  The resulting
ordered list is the path inventory.  Its normalized JSON commitment and exact
length are recorded in every shard summary.

Each path row stores:

- the inventory index;
- base summary, state, path, and fixed-full root IDs;
- exact source and target parent graph IDs together with normalized-body IDs
  (the historical hard-cover IDs retain their original arc order);
- the dummy-restoration order and restored role-to-label map;
- sorted admissible source and target internal blob arcs;
- the packed `A+p` relation array;
- the packed concatenation of the conditional `A+p+q` arrays.

The parent graph bodies remain in the content-addressed hard-cover graph
stream.  A child graph is defined, without a lookup table, by its parent graph,
the indexed arc, and the next physical label.  Port insertion uses the
deterministic fresh vertices `max(V)+1,max(V)+2`; exact deletion must recover
the parent.

## 2. Complete relation indexing

For source arcs `s_0,...,s_(r-1)` and target arcs
`t_0,...,t_(c-1)`, the `A+p` cell with flat index `ic+j` is the decorated
directed relation obtained by inserting `p` on `s_i` and `t_j`.  Thus no
source-to-target embedding or port correspondence is inferred from a target
hash.

Conditional `A+p+q` blocks occur in increasing `A+p` flat-index order, only
for cells classified as labelled isomorphism or ordinary `T`.  Within each
block the same row-major rule is applied to the independently regenerated
admissible arcs of the exact `A+p` source and target children.  Block lengths
are therefore derivable and are checked before decoding the next block.

Every cell is one little-endian unsigned 32-bit word.  The high three bits are
the class and the low twenty-nine bits index the appropriate local library:

| code | class | library |
|---:|---|---|
| 0 | generic polynomial separation | witness |
| 1 | strict open-cube separation | witness |
| 2 | labelled isomorphism | transport |
| 3 | ordinary triangle redirection `T` | transport |

Codes 4--7 are invalid.  The arrays are Base64-encoded in the path JSON row;
the enclosing JSONL stream is deterministically gzip-compressed.

## 3. Witness library

Every quartet descendant mask is represented by the lexicographically
smaller of the selected side and its four-bit complement.  This is exact
because all retained group-based Fourier coordinates have total character
zero, so complementary split sides induce the same JC factor.  Duplicate
rows are then zipped to one effective multiplier.  This normalization is
part of the graph-to-polynomial compiler and must be independently
regenerated; it may not be inferred from a stored polynomial.

A witness record contains the selected quartet chunk, invariant index,
directed zero/nonzero orientation, exact polynomial ID, and, for a strict
separator, the complete exact sign certificate.  The polynomial body is in a
separate content-addressed sparse-polynomial stream.  During verification the
polynomial is regenerated from the two child graphs through displayed-tree
switchings and descendant masks before its ID may be looked up.

## 4. Transport library

An allowed cell has a unique transport because every anchor and permitted
probe is pointwise rigid.  Its compact transport record stores:

- the target vertex list corresponding to the sorted source vertices in the
  labelled `T` quotient;
- the target-edge permutation corresponding to the source quotient-edge
  order;
- source and target reticulation lists and the transported reticulations
  outside a redirected triangle;
- the physical port-label transport;
- the source and target raw-to-canonical maps.

The Fourier-coordinate transport is the identity on the fixed physical port
labels and is recorded as such.  For ordinary `T`, the separate audited local
`T` germ supplies the parameter correspondence; the graph record never claims
equality of complete stochastic images.

Transport bodies may be binary packed, but their exact normalized JSON form
and SHA-256 commitment must be recoverable losslessly.  A verifier must
regenerate the unique transport from the child graph pair before comparing the
stored body.

## 5. Shards and completeness

Shards use disjoint half-open path-index ranges.  A merge manifest is valid
only if:

1. all shards have the same path-inventory commitment and input commitments;
2. their ranges are disjoint, gapless, and cover the full inventory;
3. every row index appears exactly once;
4. every packed array has the exact regenerated length;
5. the aggregate directed classification counts agree with the sum of the
   shard counts; and
6. no unresolved class occurs.

The active merger additionally reconstructs the inventory and every declared
input hash from the base summaries, decodes every packed relation word,
recomputes the aggregate class counts, checks that every witness, transport,
and polynomial body is used, and binds two semantic replay certificates for
each exact shard summary: one from the primary verifier and one from a
clean-room implementation.  A byte-consistent shard manifest without both
successful summary-bound replays is not a certificate.

The compact form is first validated against every record of the already
verified verbose theta-2 stream.  Only after record-for-record agreement may
it be used as the primary representation for the larger three-outgoing
extension.

## 6. Independent release requirement

The clean-room implementation may read the locked hard-cover graph encodings
and compact certificate as inputs, but it must independently implement graph
validation, semi-directed reduction, internal-arc recovery, insertion and
deletion, displayed-tree Fourier tensors, invariant pullbacks, strict signs,
and unique quotient transports.  It must compare a normalized relation word
for every packed cell and reject at least deletion, duplication, changed arc,
reversal, wrong polynomial, wrong transport, wrong parent, cross-root merge,
and truncated-block mutations.
