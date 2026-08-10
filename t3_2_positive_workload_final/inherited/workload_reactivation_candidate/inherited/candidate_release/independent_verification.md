# Independent verification

The universal proof is mathematical.  Computation is load bearing only for
the finite two-active workload-cone atlas.

Two implementations are supplied:

1. `src/workload_atlas.py` constructs the reduced rational atlas and its
   canonical representatives.
2. `src/exhaustive_two_active_atlas.cpp` independently enumerates all
   `3^10` assignments for each of four exact workload chambers, without
   importing the Python implementation.

The C++ replay checks every ordered two-linkage assignment with both blocks
nontrivial.  Every shielded assignment is classified as:

* admitting a common affine invariant positive on both active species;
* deficiency zero; or
* one of the two service architectures, up to species permutation and block
  exchange.

The independent Python verifier separately reconstructs the reduced 29-class
atlas and the strongly connected support counts for the service systems.
Exact rational tests also verify the deficiency-zero rank interface and the
one-active source-degree facts.
