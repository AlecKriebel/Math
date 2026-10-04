# Why the isolated 2009 definition requires a scope correction

This is a counterexample to the bare printed conditions read literally, not a solution of the intended Julia-set or modern degenerate-Herman-ring problem.

## Source context

Oberwolfach Report 54/2009, printed page 2958, Problem 2 introduces an analytic periodic Jordan curve with an irrational circle-homeomorphism return map, excluding the closure of a Herman ring. It does not explicitly require membership in the Julia set or exclude a Siegel disk. Problem 1 immediately above explicitly discusses level curves in both kinds of rotation domains. The context strongly suggests that the authors intend to exclude these already described rotation-domain examples. The present note does not use the omitted condition as a claim to have solved their research question.

## Literal counterexample

Let alpha=(sqrt(5)-1)/2 and lambda=exp(2*pi*i*alpha). The quadratic polynomial

  P(z)=lambda*z+z^2

has a Siegel disk Delta at zero. Indeed alpha has continued fraction [0;1,1,...], so its continued-fraction denominators satisfy q_(n+2)=q_(n+1)+q_n. They grow at least geometrically every two steps and at most as 2^n. Thus sum log(q_(n+1))/q_n converges, which is the Brjuno condition. The classical Brjuno linearization theorem yields a conformal map h:D_R -> Delta, R>0, satisfying P(h(z))=h(lambda*z). This standard consequence is also stated as equations (2.3)-(2.5) in Yang, arXiv:2207.06770v2.

For each r in (0,R), C_r=h({|z|=r}) is an analytic Jordan curve, P(C_r)=C_r, and P restricted to C_r is conjugate to the irrational rotation by alpha. Distinct radii give disjoint, distinct curves. Every C_r lies strictly inside the Fatou component Delta. Any Herman ring is a different Fatou component H. An interior point of Delta has a neighborhood contained in Delta and disjoint from H, so it cannot belong to the closure of H. Hence no C_r is contained in the closure of any Herman ring.

There are uncountably many radii, already for degree two. Thus the isolated printed conditions admit no finite degree-only bound.

## What this does not establish

Every C_r is in the Fatou set, so none meets the modern definition requiring C_r subset J(P). These curves also fail the intended exclusion of level curves in rotation domains. This is a definition audit, with a standard classical example and no novelty claim. The 2009 periodic counting problem under its intended exclusions remains unresolved by this observation.

The example also warns against silently identifying three counting conventions: individually invariant curves; all periodic component curves; and periodic cycles. A bound for one convention does not automatically give the others.
