# Root reconstruction of a potential earlier covering combination

Saved 2026-10-15 during the distinct priority phase, after root mathematical
clearance. This is a checkable provisional coverage argument, not a final
historical verdict. The historical family independently found a rank-count
route; the Schur family independently found the 2004 ascending-process source.
This note records my own reconstruction of their exact connection.

## Authenticated earlier statements

The Aldous–Diaconis 1993 notes, printed 36–37, define precisely the finite
positive drift-jump system and state its limiting simultaneous law as
`(Gamma(B(1)),...,Gamma(B(k)))`, equation (42), where Gamma is an independent
unit-rate Poisson arrival sequence and B is the compatible limiting top-card
rank sequence. Compatibility of the first finite labels is stated just before
(41). The printed spatial scaling and quantitative mean-coupling bound are
unsafe, but this simultaneous representation is independently consistent with
the validated construction. It is credited earlier material, not a new claim.

Aldous–Diaconis 1999, printed 418, identifies the full top row of the RSK
insertion tableau with all patience-sorting pile tops. RSK is a bijection between
permutations and pairs of standard tableaux of the same shape. Thus a fixed
tableau T of size n has probability `f^shape(T)/n!` under a uniform permutation.
Restricting the small labels gives the coherent infinite Plancherel tableau law;
the same conclusion follows from RSK symmetry and restriction to prefixes of a
uniform permutation. No unspecified distribution remains in this description.

Borodin–Olshanski, arXiv math-ph/0402064v2, 29 September 2004 (published 2006),
defines at printed 3 the up transition
`p_up(mu,nu)=f^nu/((|mu|+1)f^mu)` when one box is added.
Printed 5, equation (1.9), sets birth rate `u'(t)v(t)` and death rate
`-n v'(t)/v(t)`. Remark 1.5 at printed 6 explicitly includes horizontal
ascending curves. Definitions 2.1–2.2 and Theorem 2.3, printed 6–7, identify
this process with RSK of the unit Poisson field in nested rectangles.
These are rigorous statements, not the separate conjectural 2013 dynamics.

## All-law equivalence, with the correct parameter rather than a hyperbola

Choose the horizontal curve `C(x)=(x,1)`, x>0. It is admissible: `u'=1`,
`v'=0`; hence its births have rate one and there are no deaths. The diagram
at x has poissonized Plancherel parameter x. It can equivalently be constructed
by taking an infinite coherent standard Plancherel tableau T, an independent
unit-rate Poisson process N(x), and revealing the labels at most N(x).

Let B_r be the r-th entry of the first row of T. Then the independently
Poisson-marked first-row entries are `Gamma(B_r)`. For every positive r,x,

`Gamma(B_r)>x  <=>  B_r>N(x)  <=>  lambda_1(x)<=r-1`.

All these equivalences hold jointly for arbitrary finite lists, not just for
one marginal. This converts the already stated stationary rank representation
into an explicitly specified first-row hitting-level functional of the exact
ascending process of the 2004 theorem. The source's *stationary hyperbolic
diagram process* is a different use of the same paper and is not the argument
here. Likewise, diagram process x is a simultaneous spatial threshold, not
physical drift time s.

## Derive the candidate's exact chain weights from earlier transitions

For `mu subset nu`, write n=|mu|, d=|nu|-|mu|. Conditional on d births between
x and x+Delta, each length-d Young-lattice path has probability

`(f^nu/f^mu) n!/(n+d)!`.

There are exactly `f^(nu/mu)` such paths. Independent rate-one Poisson births
therefore give the transition

`P_Delta(mu,nu)=exp(-Delta) Delta^d/d! * f^(nu/mu) * f^nu/f^mu * n!/(n+d)!`.

From the empty diagram at threshold zero, multiply these transitions at
`0=x_0<x_1<...<x_m`. All dimension ratios and intermediate factorials
telescope, leaving

`exp(-x_m) [f^(lambda^m)/|lambda^m|!] * product_j [Delta_j^d_j f^(lambda^j/lambda^(j-1))/d_j!]`.

Using the classical exponential specialization/skew Jacobi–Trudi determinant
converts this exactly to the submitted weight. Summing over
`lambda^j_1<=r_j-1` gives every submitted simultaneous event, including
nonmonotone index sequences. No limit theorem, unknown correlation, or
additional invariant-measure equation is needed to pass from the earlier
transition theorem to these weights. The source theorem's own jump rates
already specify all the finite-dimensional shape laws.

The original size cutoff follows from the same independent Poisson process:
the unconstrained raw size-n mass is `x_m^n/n!`. The geometric bound and
shared-normalizer rational enclosure are elementary explicit consequences.
This does not establish that an earlier source wrote the identical enclosure,
the same software, or the same threshold determinant presentation.

## Separate closer 2013 lead and its limitation

Borodin–Olshanski arXiv1303.2795v1, 12 March 2013, printed 8–9, projects a
generalized-tableau process to the first row and describes a Plancherel
degeneration with velocity y and equal rate-one backward Poisson fields.
For a fixed finite row prefix, the generator then matches the candidate: the
independent per-particle Poisson clocks apply on disjoint current gaps.

However, the introduction explicitly says that this note contains no proofs,
and its general nonexplosion and Gibbs-preservation claims have conjectural
qualifications. Claim 5.4 plus a formal limit is not by itself a rigorous
covering theorem. The earlier 1993/1999/2004 argument above does not rely on
that conjecture or an unproved process-limit passage.

## Exact remaining priority question

The argument gives a strong complete *automatic consequence* of earlier
explicit statements, rather than just a list of old ingredients. Whether this
warrants an `already_solved` credit correction must be adversarially tested:
coherent P-tableau restriction, the exact interpretation of B, independent
Poisson marking, and the descriptive explicitness standard must all survive.
No authenticated earlier source examined so far announces that it has answered
the February 2018 question by name. No proposer endorsement or worldwide
historical closure is inferred. It is possible for a useful explicit exposition
or verification implementation to add value while not supporting the claimed
novel resolution of an open problem.

Primary PDF bytes and retrieval times are separately pinned in this folder.
Whole third-party reading objects are excluded from the public authored record.
