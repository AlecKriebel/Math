# Exact K2P tree--sunlet sign certificate

Let

\[
X_h=q_{hhA},\quad Y_h=q_{hAh},\quad Z_h=q_{Ahh}
\]

for `h=s,g`, and let `V=q_{CTG}`.  Every positive three-leaf K2P tree satisfies

\[
\mathcal T_3:=V^2X_g-X_s^2Y_gZ_g=0.
\]

For the three-sunlet with the reticulation incident with leaf 3, using edge
notation `(a,b,c,d,e,f)` and inheritance probability `delta`, direct
substitution gives

\[
\boxed{
\mathcal T_3=
-a_s^2b_s^2a_gb_gc_g^2f_s^2\,
\delta(1-\delta)d_ge_g(1-f_g)^2.}
\]

Every factor outside the leading minus sign is strictly positive on the open
positive-eigenvalue stochastic K2P domain.  Thus a strict three-sunlet cannot
realize a tree distribution.  Equality forces at least one explicit boundary
collapse:

- `delta=0` or `delta=1`;
- `d_g=0` or `e_g=0`; or
- `f_g=1`.

This is the exact certificate behind the numerical optimization that drove an
inheritance weight to zero, an edge eigenvalue to zero, and a path edge to the
identity.  It also explains why equality of complex closures is irrelevant:
the three-sunlet map is dominant, but its physical image occupies a strict
semialgebraic chamber disjoint from the tree image.

The two other orientations have the corresponding leaf-permuted certificates.
At the common ordinary-triangle point all three values equal `-1/82944`, so a
single open tensor neighborhood belongs to all three orientation images while
remaining disjoint from the tree model.
