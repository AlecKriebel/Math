# Lower-to-two response program

This package consolidates the exact dilute-module response vectors and
derives the functional cone problem for one fitness-independent family.

The principal new theorem is
`SECOND_ORDER_CLONE_OBSTRUCTION.md`: for an arbitrary fixed-order integrated
gadget perturbing the portal-clone equality manifold, the Bd response has no
quadratic term and the dB quadratic is negative definite.  This eliminates
the full fixed-order second-order clone escape, including asymmetric portals
and arbitrary positive internal matrices.

The Taylor remainder is compact-uniform only at fixed gadget order with
uniformly positive local denominators and bounded parameter jets.  Growing
rank, singular vanishing portals, higher-order interactions between module
densities, and nonseparated dynamics remain outside the theorem.

`SEPARATED_CONE_NORMAL_FORM.md` gives the complete invariant response for
every fixed gadget in the separated dilute architecture, its scalar
quadratic gate test, the semi-infinite interval cone, the positive-measure
dual, and the growing-menu diagonal lemma.

`response_library.py` is the canonical machine-readable SymPy library.
`response_library.json` is regenerated deterministically during replay.

Run:

```text
./replay.sh
```

The exact global threshold remains open.  This package proves no family up
to fitness two and no universal graph obstruction; it sharply identifies
why the most persistent fixed-order zero tangent cannot provide either.
