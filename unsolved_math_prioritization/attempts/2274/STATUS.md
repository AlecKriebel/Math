# Status of problem 2274 / Erdos Problem 711

## Prior divergence accepted; uniform exponent-one upper question unresolved

Van Doorn's published result establishes divergence of F(n)-f(n,n).
Kominers v1 strengthens the lower scale to n log n with liminf at least 1/e.
Chen--Korsky v2 gives a still larger lower bound, implying
[F(n)-f(n,n)]/(n log n)->infinity. All are credited prior results.

The accepted uniform upper bound here has exponent 4/3 and a subpower factor.
It does not establish F(n)<=n^(1+o(1)). The prime-only upper bound has the
same 4/3 exponent with a logarithmic saving. The prime lower construction is
n times a superpolylogarithmic factor, yet remains n^(1+o(1)); it is compatible
with the unresolved exponent-one upper conjecture.

The separate fixed-start asymptotic in Erdos Problem 710 is neither settled
nor transferred to a maximum over all starts. A bound over polynomially
bounded starts does not control a full period of lcm(1,...,n).

## Acceptance qualifications

The complete authored general derivations are in AUDIT.md. Established
analytic inputs are explicitly identified and not reproved from first
principles. Kominers's auxiliary small-d common-constant choice is corrected
by c2=max(1,2b), without a failure of the main theorem. Chen--Korsky v2 is the
adopted version; v1 and the weaker appendix do not supply the accepted bounds.

This AI-assisted audit is unrefereed. Acceptance means an independent internal
AI audit, not external human peer review, journal acceptance of a preprint,
or formal proof-assistant certification. No novelty, priority, exhaustive
survey, current-best-bound certification or explicit asymptotic threshold
is claimed. Source checks were recorded on October 10, 2026; no fresh
scholarly-source inspection or mathematical computation occurred while
preparing this edition. This is not an executable replay package.
