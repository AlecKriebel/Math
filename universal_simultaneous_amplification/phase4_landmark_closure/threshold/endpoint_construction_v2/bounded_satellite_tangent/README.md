# Bounded satellite tangent cone

This folder asks whether replacing the dilute strong `K_2` satellites by a
richer fixed gadget can raise the proved hybrid threshold

\[
R_*=1.5028569127905696\ldots .
\]

Current exact results:

- `CLIQUE_SATELLITE_THEOREM.md`: `K_2` is the unique clique `K_s` whose
  dilute tangent can cross fitness `3/2` after balancing with hub pendants.
- `GENERAL_GADGET_SCREEN.md`: first-principles gate formulas for arbitrary
  weighted gadgets and portal loads.
- `certify_unweighted_gadgets.py`: among all 142 connected unweighted
  gadgets through six vertices with uniform portals, `K_2` is uniquely
  feasible at `r=3/2`, certified by exact subset chains and quadratic signs.

The weighted/nonuniform-portal optimizer is discovery only.  It found no
positive tangent for three- or four-vertex supports at `R_*`; boundary
degenerations approach smaller gadgets.  This does not prove an all-weight
or all-size obstruction.

Run the exact certificates with `replay.sh`.

