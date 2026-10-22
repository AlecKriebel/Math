# Audited clarifications

2026-10-04. This addendum supplements the preserved author checkpoint and
independent audit. The classification remains **unsolved, five approaches
used out of five**. Neither unrestricted source question has been resolved.
No new result or priority claim is introduced here.

## Claim precision in submission/RESULT.md, Section 5

Read the sentence concerning an infinite sequence of singular values with
entry times tending to infinity as replaced by the following:

“Pointwise membership of each singular value in some U_m does not by itself
establish a uniform index for the entire singular-value set; no such uniform
bound, or general component-capture theorem, has been proved here.”

In particular, this checkpoint does not claim to construct an entire function
satisfying all the source hypotheses with an infinite sequence of singular
values having unbounded entry times. The discussion identifies a missing
implication, rather than claiming that such an example has been realized.

## Polynomial boundary detail in Section 1

Use smooth Jordan curves in the argument-principle criterion for simple
connectivity. Take the tree neighbourhood G to have smooth boundary and no
critical values on that boundary. Polynomial properness and the nonvanishing
of the derivative over the boundary make P^{-1}(boundary G) a compact smooth
one-dimensional manifold, hence a finite disjoint union of circles. Each
bounded simply connected component V of P^{-1}(G) has exactly one of these
circles as boundary. Its closure is consequently a topological disc, justifying
the disc version of Riemann-Hurwitz used in the author proof.

## Contracting disc and indices in Sections 2 and 5

Let a be the attracting fixed point. Choose r>0 and q<1 such that

    |f(z)-a| <= q |z-a| for |z-a| <= r.

Such a choice follows from |f'(a)|<1 and continuity of the quotient
(f(z)-a)/(z-a), extended at a. Take B=B(a,r), and let m run over
0,1,2,... in W_m=f^{-m}(B) and in its component U_m containing a.
The contraction estimate ensures f(closure B) is contained in B. The
increasing open sets W_m cover the full basin. Compact subsets of that basin
are contained in one W_M by a finite-cover argument, and the same estimate
then yields locally uniform convergence of iterates to a.

The capture index M in the author's component-capture equivalence is allowed
to depend on the component V and on m. No assertion is made that every finite
W_m is connected. The independent audit supplies a polynomial example with
complete invariance and disconnected finite-stage pullbacks, together with
the exact arithmetic and the analytic explanation of delayed capture.

## Status of the preserved records

The author and audit directories are byte-for-byte preserved historical
artifacts. In particular, the author's machine-readable pending-audit field
records its original freeze state. The separate audit has now accepted the
work as an unresolved checkpoint with the clarifications above. The full
audit, its source checks and its independently implemented tests are included.
Finite controls remain finite controls; they do not verify either general
entire-function assertion. Literature and priority statements retain their
bounded-search qualifications.
