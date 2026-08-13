# Candidate global repair (not yet promoted)

Status: **UNRESOLVED — under adversarial review**

## Scope

The proposed theorem is restricted to binary standard semi-directed
strongly-tree-child level-2 networks with at most one triangle per blob and
open JC parameters.  It does not use the withdrawn automatic-triangle
strengthening.

## Remove the false bridge chart

The historical manuscript claims that a bridge factorization has only one
reciprocal scalar and that the observable tensor determines a separate bridge
multiplier.  This is false.  If endpoint-arm multipliers are retained, the
observable depends on their product with the bridge multiplier.  For example,

```text
(1/2, 1/2, 1/2) and (3/5, 3/5, 25/72)
```

have the same product `1/8` but are not related by the claimed
reciprocal-only action.

The repaired proof must claim only what rank-one factorization intrinsically
gives: the two endpoint slices as projective points.  It must not assign an
identifiable physical bridge multiplier or assert a free product chart.

## Candidate localization by bounded marginals

Assume the independently audited pointwise cut theorem.  A one-sided global
containment then gives the same labelled bridge tree.

Fix one blob and choose one labelled descendant taxon from every component
created by deleting that blob from the bridge tree.  Marginalizing all other
taxa turns each outside branch into a two-port stationary JC kernel.  Its one
nontrivial Fourier multiplier is a strictly positive convex combination of
products of open edge multipliers, and therefore lies in `(0,1)`.  The
resulting marginal is exactly a local completed-blob tensor with one open JC
arm multiplier per port.

At a source parameter preimage of the relative-open containment set:

1. internal parameters of the chosen blob are independent of all other blob
   parameters;
2. the ordinary edge adjacent to each incident bridge multiplies only the
   corresponding effective arm scalar and has nonzero derivative;
3. after intersecting with the local regular locus, the marginal map is a
   submersion onto a relative-open subset of the completed local source
   model; and
4. every such marginal also belongs to the corresponding completed local
   target model.

If all four points survive review, each global one-sided containment induces
a local one-sided containment at every blob.  The independently certified
root/nonroot atlases can then exclude every local change except labelled
isomorphism and ordinary triangle redirection `T`.  This proves necessity
without an exact bridge-fiber theorem and rules out cross-blob compensation
by a direct marginal argument.

## Candidate sufficiency

For labelled-isomorphic blobs use identical parameters.  For each `T`-related
blob use the exact open-domain local port-tensor common germ.  These local
common germs and identical bridge-tree contexts give a common semialgebraic
global image set.  Full dimension must be proved without the false bridge
chart, for example by showing that the common construction is the image of a
nonempty open subset of each full parameter space and intersects the regular
locus on both sides.  Symmetry of `T` and the local full-rank certificates are
load-bearing here.

## Required reviewer attacks

- Does marginalizing an outside branch ever produce more than a two-port JC
  scalar because of reticulation-choice correlations?
- Can the preimage of a relative-open source image be trapped in the critical
  locus of the selected local marginal?
- Does a root-containing blob require a distinct local completion language?
- Can weak selected target completions invalidate the finite atlas?
- Is the common multi-`T` construction full-dimensional in both global model
  images without a bridge-product rank formula?

No statement in this file is part of the final theorem until these questions
and the finite atlas gates are independently closed.
