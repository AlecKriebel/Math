# Adversarial audit of weak-class sharpness

## Claim and audit standard

The audited claim is that, for every (n\geq3), two distinct binary level-2
semi-directed networks which are weakly but not strongly tree-child and are not
ordinary-triangle equivalent have strict continuous-time K2P images containing
a common analytic germ of dimension (4n-3).

The audit treats this as a hypothesis.  Success requires independent literal
graph encodings, complete edge-rooting enumeration, exact mixed-graph relation
testing, exact rational Fourier expansion and rank minors, interior
continuous-time witnesses, and an induction whose rank and graph-class steps
both have local inverses.  A numerical rank, a sampled rooting list, or an
appeal to the four-port atlas would not pass.

## Independent graph reconstruction

The first rooted representative has internal arcs

\[
 rS,rL_0,SU,SV,UX,VZ,ZX,UV,ZL_1,XL_2,
\]

with reticulations (V,X).  Thus (Z) is the subdivision vertex on the
(V\mathord{-}X) segment.  The second has arcs

\[
 rS,rL_0,SU,SX_0,VX_0,UX_1,VX_1,UV,X_0L_1,X_1L_2,
\]

with reticulations (X_0,X_1).  Both encodings satisfy the binary degree
conditions and are acyclic.  Suppressing (r) and retaining only arrowheads at
reticulations produces the semi-directed graphs used below.  No primary
builder is imported.

For every one of the nine underlying edges, the audit inserts a root, directs
the two subdivided halves away from it, retains every other reticulation
arrowhead, enumerates every orientation of the remaining ordinary edges, and
checks acyclicity and every binary indegree/outdegree condition.  This includes
all four reticulation edges in each graph.  The exact censuses are

\[
 (\#\mathrm{admissible},\#\mathrm{TC},\#\mathrm{nonTC})
   =(5,2,3),\qquad(7,2,5).
\]

Hence each graph has a tree-child rooting and a non-tree-child rooting.  This
proves weak tree-childness and disproves strong tree-childness under the
standard all-admissible-rootings convention.

The mixed-graph comparison expands each edge into an incidence vertex and
records its two endpoint head flags.  Exact labelled graph isomorphism fails.
Each graph has exactly one underlying triangle.  Forgetting the three head
flags on the chosen triangle on each side still yields zero isomorphisms.
Thus the pair is neither isomorphic nor ordinary-triangle equivalent.

## Independent K2P expansion

The audit derives the ten normalized three-leaf K2P orbit coordinates directly
from the group (ℤ_2\timesmathbb Z_2).  For every choice of one incoming edge at
each reticulation it computes descendant leaf masks, assigns the (s)-sector
to characters (C,T) and the (g)-sector to (G), multiplies the visible edge
factors, and expands the inheritance weight.  The four switch terms and all
derivatives are evaluated over (mathbb Q).  The canonical reticulation
permutation/complement action is rebuilt independently.

For the first graph the independently expanded normalized tensor is

\[
\left(1,
\frac{64009}{457492},\frac{64009}{457492},
\frac{6400}{39229939},\frac1{1372},
\frac{4048}{39229939},\frac{4048}{39229939},
\frac{6400}{39229939},\frac{4048}{39229939},\frac1{1372}\right).
\]

For the second it is

\[
\left(1,
\frac{15}{1024},\frac{15}{1024},
\frac5{512},\frac{27}{512},
\frac9{4096},\frac9{4096},
\frac5{512},\frac9{4096},\frac{27}{512}\right).
\]

After the stated pendant factors with (δ=2^{-30}), both become exactly

\[
q_{000}=1,qquad q_h=\delta^2\text{ for the six pair-sector orbits},
\qquad q_h=\frac45\delta^3\text{ for the three all-nonzero orbits}.
\]

The independent elimination returns rank nine for each normalized map.  It
also reproduces the two primary minor determinants exactly:

\[
\frac{10368019213741323}
{563981315074464023964442388464888915634290688},
\qquad
\frac{1435825}{85002596691653613846528}.
\]

All internal and pendant pairs satisfy (0<s<1) and (s^2<g<1), and both
inheritance parameters lie in ((0,1)).  The witness is therefore an interior
strict continuous-time point.  Fixing the nonzero pendant factors multiplies
the nine nonconstant output rows by an invertible diagonal matrix, so both
full maps remain rank-nine submersions at the same tensor.  As the normalized
three-leaf K2P ambient space has dimension nine, the two images contain a
common open nine-dimensional germ.

## Cherry rank and common-germ induction

Replace the retained leaf by two children with edge eigenvalues
((u_s,u_g)) and ((v_s,v_g)).  For any outside leaf (j), positivity of the
base witness makes the following Fourier coordinates nonzero and gives local
observables

\[
R_s=\frac{Q_{j=C,a=C,b=0}}{Q_{j=C,a=0,b=C}}=\frac{u_s}{v_s},
\quad P_s=Q_{\mathrm{others}=0,a=C,b=C}=u_sv_s,
\]

with the analogous formulas using (G) for (R_g,P_g).  In the positive
chart,

\[
u_s=\sqrt{R_sP_s},\quad v_s=\sqrt{P_s/R_s},
\]

and likewise in the (g)-sector.  The four new parameters therefore have an
analytic local inverse.  Their Jacobian determinant is

\[
\det\frac{\partial(R_s,P_s,R_g,P_g)}
{\partial(u_s,v_s,u_g,v_g)}
=\frac{4u_su_g}{v_sv_g}\ne0.
\]

At the certificate witness the actual physical edge pairs—not artificial
same-sector pairs—are

\[
(u_s,u_g)=(2/5,4/9),\qquad(v_s,v_g)=(3/7,5/11).
\]

Both obey (s^2<g<1), and the determinant is (2464/675).

After solving for the four new factors, every old tensor coordinate is
recovered by dividing, for example,
(Q_{\mathbf h,a,0}=q_{\mathbf h,a}u_{\sigma(a)}), by its nonzero factor.
Thus the full extension map has a local inverse onto the old nine coordinates
plus these four observables.  More generally each iteration increases rank by
exactly four.  Since both base images contain the same open set (U), both
extended images contain the image of the identical analytic map
(U\times(\text{four-edge chart})).  Induction gives

\[
9+4(n-3)=4n-3.
\]

## Graph-class induction and boundary cases

The audit attaches a labelled cherry to every admissible rooting of both base
graphs.  In all twelve cases tree-child status is unchanged, and pruning the
new leaf and suppressing its parent recovers the directed base graph exactly.
The new edges are bridges, so no new triangle is created; direct four-leaf
comparison also remains neither isomorphic nor triangle equivalent.

This local statement iterates.  A labelled isomorphism must carry the newest
labelled cherry and its common degree-three parent to their counterparts, so
pruning would induce a base isomorphism.  Every ordinary triangle remains in
the original level-2 blob because the entire attached tree is separated by
bridges; triangle redirection therefore commutes with pruning.  A TC and a
non-TC base rooting each lift, with their status unchanged.  Binary degrees and
the level-2 blob are preserved.  These facts cover the minimum case (n=3)
and every induction step.

All relevant Fourier coordinates are positive at the witness.  Hence the
ratio chart never divides by zero, and the construction does not rely on a
boundary or limiting point.

## Adversarial finding and conclusion

The primary verifier's cherry-domain loop checks four pairs of the form
((x,x)), whereas its Jacobian variables describe the two actual pairs
((u_s,u_g)) and ((v_s,v_g)).  This is a validation gap in that loop.  It is
not a counterexample: the audit checks the actual pairs and both are strict
continuous-time.  The mutation suite includes a cross-sector pair which fails
(g>s^2), ensuring that this error class is now detected.

Subject to the stated standard definitions of strong tree-childness and the
ordinary-triangle quotient, the weak-class (4n-3) sharpness theorem passes
this independent audit with no unresolved mathematical blocker.
