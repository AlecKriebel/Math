# Research log — 4300001

All times are UTC on 4 October 2026. The percentages below are informal estimates
of progress toward determining the full prime-dependent order, not probabilities
of correctness. Five substantive approach families are counted conservatively;
tool calls and source lookups are not additional turns. Later proof organization
combines lemmas across families without claiming independent discovery paths.

## Readiness and source check — 11:22–11:24

The catalogue URL returned 403. The pinned record and prior report were read, and
Ward's original five-page December 2006 note was obtained. Its Problem A exactly
matches the polynomial and 3≤M<7 bound. Live repository checks found queued 0/5
and no exact-ID duplicate. The original mathematical target retains arbitrary
admissible p; selecting p=2 is a special-case result. Starting estimate: 5%.

## Approach 1 / turn 1 — geometric valuations and Frobenius

Mechanism: reconstruct the four-sided Newton-polygon lower bound and the
seven-term Frobenius obstruction. Verify the current minimum-nonmixing theorem
against Derksen–Masser rather than treating the old catalogue report as authority.

Outcome: the source's 3≤M≤6 is applicable; Derksen–Masser (2017/2018) makes the
minimum nonmixing order effectively computable in general. Its examples are not
this target. Ordinary sparse multiples alone are insufficient without controlling
the radical of the monomial group; the paper explicitly exhibits that obstruction.
Exact gap: the relevant radical and shortest relation have not yet been computed.
This family is blocked as a complete solution until that algebraic work is done.
Checkpoint about 11:25. Completion estimate: 15%.

## Approach 2 / turn 2 — function field, ramification, and reciprocal symmetry

Mechanism: regard f as a primitive quadratic in y. Factor its discriminant, handle
p=3 and p=5 explicitly, and use an Artin–Schreier pole at p=2. At odd p, simple
coordinate divisors force radical saturation. At p=2, coordinate orders 2 and 4
control odd radical factors and logarithmic differentiation controls square roots.

Outcome: f is absolutely irreducible for every prime, with constant field F_p.
The radical equals F_p^*⟨x,y⟩. Derksen–Masser now identifies M+1 with the least
support of an ordinary Laurent multiple. Reciprocal involutions exclude relations
on two x-levels or two y-levels, in particular all four-term multiples.
Exact gap at this checkpoint: five- and six-term multiples are not excluded.
Checkpoint about 11:27. Completion estimate: 30%.

## Approach 3 / turn 3 — characteristic-two boundary parity and differentiation

Mechanism: use the special coefficient field F_2. Every extreme face has even
support. For a hypothetical six-term multiple, each face has exactly two terms.
Its four face-pairs form a graph: either a forest with at most two components,
or a rectangle with at most two isolated points. Face multiplicities force
constant exponent parity on each component. Radical saturation rules out two
classes, while a derivative calculation rules out the remaining three-class case.
Frobenius descent excludes a single parity class.

Outcome: a complete characteristic-two sparse-weight exclusion, giving M_2=6.
The final proof uses the uniform five-term lemma below to simplify one proper-
subsum check; the original mechanism used a minimal-support counterexample.
Exact gap: odd-characteristic face coefficients need not all equal 1, so a face
can have three terms summing to zero. The graph proof cannot be transplanted.
Checkpoint about 11:30. Completion estimate: 60%.

## Approach 4 / turn 4 — specialization at a boundary root

Mechanism: evaluate a putative sparse multiple at y=β, β²=−1. Its extreme
x-columns vanish. The defining polynomial specializes to βx(x²+x+1).
With at most five total terms, at most one interior monomial remains, which
cannot be divisible by x²+x+1. Two-column supports were already excluded.

Outcome: all five-or-fewer-term multiples are excluded for every prime,
including p=3 where x²+x+1 has a repeated root. Thus 5≤M_p≤6 uniformly.
Exact gap: with six terms, two interior monomials can form a binomial divisible
by x²+x+1. The specialization no longer gives a contradiction.
Checkpoint about 11:32. Completion estimate: 65%.

## Approach 5 / turn 5 — odd-prime normal form and bounded exact sparse search

Mechanism: force a six-term witness to have two terms on each extreme x-column
and two interior terms. Specialization at both roots of y²+1, retaining repeated
roots at p=3, forces a multiple-of-three interior x-gap, an even interior y-gap,
and a signed coefficient constraint. Test small multiplier boxes exactly over
F_2,F_3,F_5,F_7 rather than infer a global negative result from numerical fitting.

Outcome: Proposition 6.1 gives necessary congruences, not sufficiency or an
exponent bound. The 59,561 normalized multipliers in the four stated boxes all
produce support at least seven. Exact algebra and finite graph controls pass.
No six-term witness was found, and none was ruled out globally for odd p.
The effective general algorithm was not implemented; replacing the task by its
existence theorem would not determine this polynomial's mixing order.
Final checkpoint about 11:41. Completion estimate remains 65%.

## Final budget and scope

Five substantive families have been used. Stop fresh proof search for this
original target. Recommended disposition: unsolved, 5/5, with the characteristic-
two resolution and uniform 5≤M≤6 bound retained as partial results, subject to
fresh independent review. A special case is not promoted to a full resolution.

No source PDF or full corpus is part of the public artifact. No third party was
contacted. No remote file, branch, queue, PR, or release was changed in this task.
