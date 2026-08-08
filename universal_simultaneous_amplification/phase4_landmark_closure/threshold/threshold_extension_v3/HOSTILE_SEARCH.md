# Hostile discovery screen

Date: 2026-08-08 (America/Los_Angeles)

These results are deliberately separated from the exact theorem.  They are
numerical discovery evidence only unless explicitly labelled otherwise.

## Invariant objective

For a fully absorbing bounded gadget, the leaf-eliminated separator depends
on its isolated chains through `A_B,A_D,K` and is optimized exactly over the
free gate scale by `search_invariant_gadgets.py`.  This objective includes
the uniform-singleton subtraction `-r`.

## Screens at `R_hyb`

* Every connected unweighted gadget through six vertices was screened with
  arbitrary nonuniform portal loads.  The isolated `K_2` attained zero; all
  other reported optima were negative.
* Weighted path, cycle, star, complete-bipartite, and complete supports of
  orders three through six were optimized over internal weights and portal
  loads.  No positive separator was found.
* Unweighted star gadgets of every order from three through 300 were solved
  by their exact two-count lumping and optimized over hub-versus-leaf portal
  load.  Every separator was negative; the best was the three-vertex path.
* Asymmetric correlated networks of two and three strong pairs were
  optimized over all pair scales, all core loads, and all pair--pair loads.
  Both searches converged to the uncoupled equality boundary
  `sigma=sigma_*` with pair--pair loads tending to zero.

These searches do **not** prove an arbitrary weighted-gadget or asymmetric
portal-network theorem.  They motivated the exact symmetric-doublet
certificate and identify the unresolved asymmetric/second-order modes.
