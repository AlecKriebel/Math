# Complete-graph extremality under death--Birth updating

This folder contains the manuscript, paper-level audit, and entry points into
the repository-wide exact-replay package for

> **Complete-Graph Extremality under Death--Birth Updating: Fitness-Two Local
> Optimality and Strong-Selection Rigidity**.

The paper combines two complementary theorems about the same normalized
replacement-kernel gap:

1. every fixed finite directed structure is either eventually suppressing
   under strong selection or dynamically identical to the complete kernel;
2. at fitness two, the complete kernel is a strict nondegenerate local
   maximizer in the full positive loopless row-stochastic kernel polytope,
   including directed and nonreversible perturbations.

The all-fitness weighted-triangle theorem and two symmetric weighted
four-vertex families provide global low-order slices.  The paper does **not**
claim global complete-kernel maximality at fitness two or a local radius
uniform in population size.

From this folder run:

```sh
./replay.sh
./build.sh
```

`all.sh` performs both.  The deterministic manuscript PDF is written to
`output/pdf/complete_graph_extremality_db.pdf`; rendered pages for visual QA
are written to `output/rendered/`.

The development-tree replay calls exact rational/symbolic certificates tracked
elsewhere in this repository together with the paper-specific integration
audit.  The release-bundle script copies those dependencies into a standalone
archive.  No sampled floating-point calculation carries a theorem quantifier.
