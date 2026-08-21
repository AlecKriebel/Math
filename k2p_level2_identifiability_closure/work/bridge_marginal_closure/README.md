# K2P bridge, marginal, and gluing closure

This folder reconstructs the global analytic layer needed by the principal
positive-domain theorem.  It is independent of the frozen four-port atlas.

The scope is the principal K2P domain

\[
\mathcal D_+=\{(s,g):0<s<1,\ 0<g<1,\ g>2s-1\}.
\]

`PROOF.md` gives the general proof.  `verify_bridge_marginal.py` is a
standalone exact regression for the finite linear-algebra and inequality
claims used by that proof; it is evidence for, not a replacement for, the
general argument.
