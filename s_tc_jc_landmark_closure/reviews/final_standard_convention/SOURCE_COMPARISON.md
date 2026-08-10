# Exact convention comparison

Status: **VERIFIED AFTER CORRECTION**

This is a narrow source audit, not a literature survey.  The exact versions
and file hashes are in `source_metadata.json` and
`convention_certificate.json`.

## 1. The sources do not use one literal reduction map

### Englander et al., bioRxiv v4

Definition 2.1 requires a binary rooted DAG with root bidegree `(0,2)`, no
parallel edges, and the root as the lowest stable ancestor.  Definition 2.2
forms a semi-directed network by undirecting non-reticulation edges and
"suppressing the former root".  It then separately requires the result to
have no parallel edges.  It does **not** put exhaustive post-root cleanup into
Definition 2.2.  Definition 2.3 calls a semi-directed network strongly
tree-child when every directed network giving it by Definition 2.2 is
tree-child, and cites the intrinsic criterion that each vertex with an
outgoing retained edge has two incident undirected edges.

The remark following Definition 2.3 assumes away 2-blobs and parallel edges;
the later induced-subnetwork Definition 2.4, not Definition 2.2, uses
exhaustive degree-two/parallel/2-blob cleanup.

**Mapping.**  The repository's `sd_0` is a literal explicit implementation of
Definitions 2.1-2.3 once one says that a rooted presentation is admitted only
when root suppression already produces the required simple mixed graph.

### Holtgrefe et al., arXiv:2507.18772v2

Section 2.2 defines semi-deorientation by undirecting arcs into nonreticulate
vertices and suppressing degree-two **roots**.  The target is required to be a
mixed graph, and mixed graphs exclude parallel arcs, parallel edges, and
edge/arc pairs.  The paper expressly declines to treat semi-deorientations
that create parallel arcs.  Its rootings are obtained by subdividing edges or
arcs and orienting the undirected part; no new reticulation may be created.

Its rooted framework is more general than Outcome P: roots may have degree
one or two, roots may be existing mixed-graph vertices, and no LSA trimming
condition is imposed.  On the binary LSA-valid phylogenetic networks used by
Outcome P, `sd_0` is the corresponding specialization.  Theorem 5 proves
strong tree-childness iff the mixed graph has no omnian.  In a simple binary
mixed graph this is exactly the repository's arrow-tail/two-undirected-arm
criterion.

### Brits et al., arXiv:2607.12919v2

Definition 2.1 agrees on binary bidegrees, no parallel directed edges, and
the LSA condition.  The following paragraph uses a broader reduction:
undirect non-reticulation edges, suppress the root, and **exhaustively**
suppress resulting parallel edges and degree-two vertices.  This is not the
same map as `sd_0`.

Section 5.1 separately defines a 2-sub-blob by two *boundary vertices*, not by
two external incident edges.  The ordinary degree-two suppression argument
therefore cannot be imported as though every literal 2-sub-blob were a
two-edge, two-terminal factor.  The exact four-sunlet regression in
`convention_certificate.json` has two boundary vertices but four external
edges.

## 2. Reconciliation

There is no single literal "current standard reduction" shared by all three
sources.  The positive level-2 theorem extends Englander et al., and its
strong tree-child terminology is the Holtgrefe et al. no-omnian notion.
Accordingly, the release-safe convention is:

1. `sd_0` is the reticulation-preserving, already-simple
   semi-deorientation used to define admissible rootings and `S_TC`;
2. every `sd_0` rooting is binary, LSA-valid, and recovers the mixed graph
   exactly;
3. `red_*` is a separate cleanup used only for restrictions, displayed
   networks, and explicitly stated quotients;
4. no preimage that loses a reticulation or arrowhead during `red_*` is an
   admissible rooting for `S_TC`.

With these corrections, the topology class is the simple standard class of
Englander v4 and the binary LSA-valid specialization of Holtgrefe v2.  It is
not the class obtained by quantifying over every rooted DAG preimage of the
Brits cleanup map.

## 3. Frozen weak theorem

The frozen weak manuscript uses the same explicit `sd_0` map.  The exact
four-leaf pair is convention-robust at its displayed rooting: no loop,
parallel edge, additional degree-two vertex, or lost arrowhead is created, so
the narrow and broad reductions agree on that presentation.  Independent
rooting enumeration gives five `sd_0` rootings, exactly two tree-child, on
each side.  Hence the pair remains in `W_TC \ S_TC` under the corrected lock.

## 4. Consequence if the broader reading is insisted upon

The broader reading cannot be silently substituted into the theorem.  The
exact LSA-valid binary level-2 rooted network

```text
rho->a, rho->r1,
a->r1, a->b,
r1->r2, b->r2,
b->L1, r2->t,
t->L2, t->L3
```

is not tree-child because `r1` has reticulation child `r2`.  Narrow `sd_0`
rejects it because suppressing `rho` creates a parallel retained edge.  The
broader cleanup collapses it to the ordinary three-leaf tree.  Thus "every
broad-cleanup preimage is tree-child" would exclude even that ordinary tree.
That is not the Holtgrefe/Englander strongly tree-child class.

## Official source links

- Englander et al., [bioRxiv v4](https://www.biorxiv.org/content/10.1101/2025.04.18.649493v4)
- Holtgrefe et al., [arXiv:2507.18772](https://arxiv.org/abs/2507.18772)
- Brits et al., [arXiv:2607.12919v2](https://arxiv.org/abs/2607.12919v2)
