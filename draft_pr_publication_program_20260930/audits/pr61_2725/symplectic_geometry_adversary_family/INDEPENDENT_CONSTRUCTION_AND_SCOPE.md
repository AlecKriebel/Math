# Independent construction and scope audit

Recorded after the frozen initial argument and direct primary reads, before the
original historical review or any other fresh family's mathematical report.
The audited claim is an application of an existing theorem, not a new construction.

Let `lambda=e^t(dz-y dx)` on `R x R3`. Interpret the question on Legendrian
isotopy classes, so equality means Legendrian isotopy. Even if the literal wording
is read as a relation on embeddings, the counterexample below is stronger than
the trivial issue of two different representatives of one isotopy class.

The one imported existence statement needed is this: sufficiently many equal
positive and negative stabilizations of a nontrivial decomposably disc-fillable
knot and of the standard unknot admit Lagrangian concordances in both directions.
The precise primary locator is [DRG v4, Corollary 1.5 and Theorem 5.7](https://arxiv.org/html/2409.00290v4).
The named example is the mirror of `9_46`. Denote the resulting fixed ends by
`A=S_+^k S_-^k Lambda` and `B=S_+^k S_-^k U`, for one sufficiently large `k`.

## Exactness, topology and the actual order argument

An embedded cylindrical Lagrangian concordance has domain `R x S1`. The pullback
`beta=lambda|L` is closed because the submanifold is Lagrangian. A circle in a
cylindrical end generates `H_1(L;Z)`. On that circle beta vanishes: its tangent
is tangent to the Legendrian knot and has no t component. Thus its period is zero.
Every loop is homologous to an integral multiple of that circle, and Stokes'
theorem makes the period of a closed one-form invariant under that homology.
All periods therefore vanish. Integrating beta from a base point yields a
well-defined smooth function f with `df=beta`.

In each cylindrical end, lambda vanishes on both the t direction and the knot
direction, so f is constant on that end. Its two end constants can differ. This
is exactly the standard condition of being constant separately at each end;
[EHK Definition 1.1 and its footnote](https://ems.press/content/serial-article-files/32160)
distinguish it from requiring a common constant on every component of a link end.
No higher-genus exactness inference is being made. The annuli here are orientable,
proper, embedded, cylindrical outside compact sets, and have Euler characteristic
zero. They qualify as cobordisms for the original problem even though the problem
permits more complicated topology.

Consequently `A <= B` and `B <= A` for the exact-cobordism relation. Stabilization
is a local modification preserving the smooth knot type. A Legendrian isotopy is
in particular a smooth isotopy. The original nontrivial knot therefore cannot
become Legendrian isotopic to the unknot after these stabilizations. Thus `A != B`
as Legendrian isotopy classes, and antisymmetry fails. One pair of knots suffices
to disprove the proposed partial order on all links.

This argument does not use nonsymmetry as a substitute for nonantisymmetry, does
not pass to a quotient by mutual concordance, and does not identify the two
stabilized knots merely because their classical invariants agree. Quotienting
any reflexive transitive relation by mutual reachability would change the set of
objects in the question. Reflexivity and transitivity are not needed to infer
the failure of antisymmetry from this pair. For knots, the cylinder supplies
reflexivity; concatenation supplies transitivity after matching a single
primitive constant on the common connected end. That matching does not justify
unrestricted componentwise gluing of links.

## Construction dependency checks

The forward direction comes from a decomposable disc filling with a standard
minimum removed, then equal end stabilizations. These stabilizations can be
inserted along a band in a Lagrangian neighborhood; [Chantraine Proposition 5.1,
printed83](https://msp.org/agt/2010/10-1/agt-v10-n1-p03-p.pdf) gives the local
operation and its proof. A source proof also exists via the satellite construction
in [CNS Theorem 2.4, printed803](https://msp.org/agt/2016/16-2/agt-v16-n2-p06-p.pdf).
Neither route changes the smooth concordance topology.

The reverse direction has two distinct steps: a formal/totally-real deformation
of the reversed smooth annulus, then a Lagrangian approximation after stabilizing
both fixed ends. Reversing t alone does not preserve the Lagrangian condition.
Our local patch in controls.py supplies an exact counterexample to that shortcut.
The approximation's relevant hypotheses and equal end counts are stated directly
in [Dimitroglou Rizell Theorem 1.1](https://arxiv.org/html/2408.16614).
The theorem is for contact three-manifolds, so no high-dimensional loose-Legendrian
principle is substituted here. Compact support and sufficiently small approximation
keep a construction initially in R3 in that contact chart. Alternatively the
symplectization lift of a contactomorphism `phi*alpha'=e^g alpha`, given by
`(t,x)->(t-g(x),phi(x))`, preserves lambda and sends cylindrical ends to cylindrical
ends as sets. The principal DRG theorem states the required R3 ambient directly.

The two unmodified ends have `tb=-1, rot=0`. The same numbers p,q of positive
and negative stabilizations change these to `tb=-1-p-q, rot=p-q` at both ends.
Taking p=q=k gives `tb=-1-2k, rot=0`; this is compatible with the annulus identity
`tb(B)-tb(A)=-chi(L)=0` and rotation preservation. These necessary compatibility
checks are not existence proofs. The k is existential, not a claimed computed
threshold. Nothing here proves that a reverse annulus is regular or decomposable.

## Two source-proof precision controls and the import boundary

1. The concluding sentence of DRG Proposition 5.4 should not be imported as the
   assertion `pi_2(U(2)/SO(2))=0`. The space of oriented, unframed Lagrangian
   two-planes is `U(2)/SO(2)`. In the homotopy sequence, `pi_1(SO(2))=Z` maps
   trivially to `pi_1(U(2))=Z` because real rotations have complex determinant one.
   Since `pi_2(U(2))=0`, the quotient has `pi_2=Z`. The framed argument is different:
   the tangent bundle of a parametrized annulus is trivial, so a chosen oriented
   tangent frame gives a unitary frame map. After the cross-annulus winding and
   collars are matched, a relative disk comparison of those frame maps does lie
   in `U(2)`, where pi_2 vanishes. This supplies a legitimate framed interpretation
   of that step, rather than a false statement about the unframed Grassmannian.
   This review does not reprove the relative immersion and totally-real embedding
   h-principles subsequently invoked in the source.

2. The approximation argument must control time derivatives as well as C0 size.
   Two samples in [-epsilon,epsilon] interpolated over time 1/M can have derivative
   2 epsilon M. Linear interpolation alone therefore does not give a bound
   2 epsilon. To use this route, the endpoint error must be chosen relative to the
   time mesh, and the smooth reference family's derivatives and monotone loop
   areas must be controlled together. The finite rational mutant in controls.py
   detects this unsupported shortcut; it is not a counterexample to the published
   approximation theorem. I read its complete operative Section4 construction
   but do not claim an independent closure of all its analytical and smoothing
   estimates. The approximation theorem remains an explicit imported dependency.

The independently proved part is exactness for the cylindrical annuli and the
deduction from the fixed mutual pair to failure of antisymmetry, with the endpoint,
quotient, stabilization and dimension requirements checked. The geometric
existence theorem and the foundational h-principles are attributed imports.
This is an audit of a known-result application, not a formal verification or a
self-contained new proof of those imports. The narrowly framed original PR
already disclaims independent recertification of the complete h-principle.

Verdict formed before historical-review reading: no defect found in that scoped
known-result application; `already_solved` is appropriate. Preserve the source
proof/import qualifications above in any operative review. No new paper or novelty
claim follows from this activity.
