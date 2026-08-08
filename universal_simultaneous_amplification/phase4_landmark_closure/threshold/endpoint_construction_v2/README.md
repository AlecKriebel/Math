# Endpoint construction branch, version 2

This directory is a discovery branch for the unresolved endpoint question at
fitness `r=3/2`.  It deliberately optimizes

\[
 M(G)=\min\{\rho_{\rm Bd}(G)/\rho_{\rm Bd}(K_n),
             \rho_{\rm dB}(G)/\rho_{\rm dB}(K_n)\}
\]

rather than the already-refuted product or balanced-mean inequalities.

The first search class consists of weighted complete multipartite blow-ups
with arbitrary within-class weights.  Class sizes may be bounded, sublinear,
or proportional to the population, so the code can probe vanishing
exceptional sets and singular weight scales that are outside the already
closed fixed-positive-proportion regime.  The count process is strongly
lumped because every vertex in a class has the same weighted adjacency to
each class; `equitable_search.py` constructs its transition rates directly
from the Bd and dB definitions.

The initial floating-point searches remain reconnaissance only.  The later
dilute pair--pendant hybrid has been promoted to a proved growing family:
see `HYBRID_CONSTRUCTION_AUDIT.md`, `verify_hybrid_lumping.py`, and
`verify_hybrid_coefficients.py`.  It proves

\[
 R_{\rm sim}\ge1.5028569127905696\ldots>3/2.
\]

The exact global threshold remains open.
