# Parallel-theta and root-created 2-sub-blob audit

After one-step root suppression, an adjacent pair of root children produces two parallel pole copies. If the context contains another pole-to-pole route of length `L`, the raw multigraph has theta path lengths `(1,1,L)`.

## `(1,1,2)`

No binary LSA-valid rooting exists. With root children `p,q` and, say, `p->q`, vertex `q` is reticulate. Binary degree constraints force the sole internal vertex of the length-two route to receive both branches, making it a proper stable ancestor of every leaf. This contradicts the LSA condition. Both independent enumerators return zero valid presentations.

## `(1,1,3)`

Binary LSA-valid rootings exist, but none is tree-child. In one orientation the root-child reticulation has a reticulation child; in the reflected orientation the upper tree vertex has two reticulation children. The two independent enumerators find four valid rootings and zero tree-child rootings.

## `L >= 4`

Tree-child presentations occur. Cleanup identifies the two parallel pole copies and suppresses the two pole vertices, yielding the ordinary simple cycle obtained by shortening the third route by two edges. The exact zipper map proves complete open-JC image equality with the cleaned cycle, even when the remaining route reconnects the two terminals.

For `L=4,...,9` the independent enumerators agree on `2(L-3)` tree-child rootings. This finite frontier checks the all-size structural proof but is not its premise.

## Isolated zipper

If no alternate pole-to-pole route exists, the artifact is a root-created 2-blob and cleanup yields an ordinary edge. Englander's rooted inputs exclude such a 2-blob; Brits' broader rooted inputs allow it. The same exact zipper tensor proves equality with the edge model. It introduces no new semi-directed topology or observational move.

## No other active cleanup core

For a tree-child cleanup rooting, the parent-side root child is a tree vertex and the child-side root child is a reticulation; the two external terminals are nonreticulate. Hence the parallel pair has one common arrowhead, cleanup stops after the zipper, and no reticulation arrowhead outside the zipper disappears. Oppositely headed, doubly headed, loop, or propagating cases require a non-tree-child or non-LSA rooting and do not occur in the landmark class.
