# Local complete-graph optimality under death--Birth updating

This folder contains the manuscript, paper-level audit, and entry points into
the repository-wide exact-replay package for

> **Local Complete-Graph Optimality at Fitness Two and Strong-Selection
> Rigidity under Death--Birth Updating**.

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

## Certified replay

The sole certified end-to-end command is run from the root of the enclosing
frozen reproducibility package:

```sh
./run_all_referee_checks.sh
```

It verifies the exact package tree and hashes, safely extracts the verified
source archive into a fresh directory, rejects links, special nodes,
unmanifested files/directories, and bytecode caches, creates a pinned private
runtime, invokes the bootstrap and verifier runner internally, rebuilds the
PDF, and compares it byte-for-byte with the delivered manuscript.

## Development helpers

In a development checkout, the corresponding component run is:

```sh
./submission/bootstrap_replay.sh --development
./build.sh
```

`all.sh` performs both development operations. Direct execution of
`bootstrap_replay.sh` or `replay.sh` is not a package-integrity certificate;
`replay.sh` is an internal stage and rejects standalone invocation. The
deterministic manuscript PDF is written to
`output/pdf/complete_graph_extremality_db.pdf`; rendered pages for visual QA
are written to `output/rendered/`.

The development-tree replay calls exact rational/symbolic certificates tracked
elsewhere in this repository together with the paper-specific integration
audit.  The release-bundle script copies those dependencies into a standalone
source archive, while the enclosing referee/reproducibility package supplies
the certified launcher and exact package verifier. No sampled floating-point
calculation carries a theorem quantifier.
