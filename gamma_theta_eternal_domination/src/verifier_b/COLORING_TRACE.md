# Exhaustive complement-coloring trace

`coloring_trace_generator.py` produces a finite certificate for
\(\theta(G)>k\), equivalently for the non-\(k\)-colorability of
\(\overline G\).  `coloring_trace_checker.py` independently replays it using
only verifier B's ordinary set-based `Graph`.

## Proof format

The format name is `gamma-theta-complement-coloring-unsat-v1`.  It is
newline-delimited JSON:

1. one header binding the canonical graph6 syntax for a fixed vertex
   labeling, \(k\), a domain-separated graph6 SHA-256, and a
   domain-separated SHA-256 of the pair `(graph6, k)`;
2. preorder tree records of the form
   `{"legal_colors":[...],"type":"node","vertex":v}`; and
3. one footer binding the number and SHA-256 of the canonical node records.

Every record ends in an LF byte.  The footer is followed immediately by EOF.
The SHA-256 of the whole certificate is reported separately by both generator
and checker.

For a canonical ASCII graph6 string `g` and decimal ASCII color count `k`, the
two header digests are exactly

```text
graph6_sha256 = SHA256(b"graph6\0" + g)
claim_sha256  = SHA256(b"gamma-theta-complement-coloring-unsat-v1\0"
                       + g + b"\0" + k)
```

The footer's `trace_sha256` hashes the concatenation of every node serialized
with sorted keys, no JSON whitespace, ASCII escaping, and one final LF per
node.  Header and footer are not in that digest.

At depth \(v\), vertices \(0,\ldots,v-1\) have colors and \(v\) is the
least uncolored vertex.  `legal_colors` must be exactly the increasing list of
all colors in \(0,\ldots,k-1\) absent from already colored neighbors of \(v\)
in \(\overline G\).  There is one immediately following subtree for every
listed color, in that order.  An empty list is a conflict leaf.

There is deliberately **no color-name symmetry breaking**: even at the root,
all \(k\) legal color names and all \(k\) children occur.  There is also no
DSATUR ordering, forward pruning, clique shortcut, or solver assertion hidden
in the proof.

## Why replay proves the claim

For a trace node with current partial coloring \(a\), the checker recomputes
the complete legal-color set \(L\).  If \(L\) is empty, \(a\) cannot extend.
Otherwise, every proper extension must assign the next vertex one color
\(c\in L\), and the trace contains and verifies the child for every such
\(c\).  Induction up the finite tree proves that no root assignment extends
to a proper \(k\)-coloring.  If any branch reaches depth \(|V(G)|\), the
checker rejects the trace because that branch is a complete coloring.

The checker rejects a wrong graph or \(k\), hash mismatch, noncanonical or
malformed graph6, duplicate/unknown/missing JSON fields, wrong vertex order,
an omitted/duplicated/reordered/illegal color, a truncated tree, a bad footer,
and every byte after the footer.  It does not import the generator or either
search coloring routine.

Here “canonical graph6” means the unique shortest graph6 encoding of the
supplied labeling. Establishing that the labeling is also the canonical
representative of its isomorphism class is a separate nauty check.

Every true trace has \(n>0\) and \(0\leq k<n\), because the empty graph is
zero-colorable and any order-\(n\) graph is \(n\)-colorable by assigning
distinct colors. The generator and checker enforce this semantic bound before
constructing a color list, which caps hostile-input work at the graph order.

## Commands

From the campaign root:

```text
PYTHONPATH=src python3 -m verifier_b.coloring_trace_cli generate GRAPH6 K proof.ndjson
PYTHONPATH=src python3 -m verifier_b.coloring_trace_cli verify proof.ndjson --graph6 GRAPH6 --k K
```

Generation writes to a temporary sibling file, flushes and fsyncs it, and
renames it atomically only after a full contradiction tree is complete.  If
the complement is \(k\)-colorable, generation reports a coloring and removes
the partial file.  Existing certificates are preserved unless `--overwrite`
is explicit.
