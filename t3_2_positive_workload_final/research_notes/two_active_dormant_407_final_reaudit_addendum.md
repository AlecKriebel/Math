# Final re-audit addendum: the arbitrary-paid-interruption tail is not closed

Audit timestamp: 2026-08-10 PDT.

Frozen snapshot:

    theorem note  1f715c98b5c77919eb3de9b5bbd9c15c6e7ff800ab4eb5849c7ace494852c0b6
    certificate   0de5883c41ea039bfd3178511d2d4a697e6a276f592a5fe0479c155b1388dc19
    focused tests 3baf477a8c924097edacf428337a255fcc1a1a437a81d3f2cdeb6141c663a75f

## Verdict

**FAIL as written at descriptor-local scope.**  The logarithmic actual-service
endpoint repair in Section 7.2 survives this audit, including the exact
`{2U,V+I}/{0,I,2I,U+I}` orientation whose service endpoint is `u+2`.
The finite killed-`Q` correction, fourth-power algebra, and exact 951-to-317
physical-state telescope also survive.  The unresolved load-bearing gap is
the arbitrary-paid-interruption endpoint and duration assertion (7.17).

This is a proof-completeness failure, not an exhibited counterexample to the
claimed recurrence statement.  It does not authorize any incidence, pair, or
global count promotion.  All analytic and recurrence flags must remain false.

## Surviving service-endpoint repair

Let `Q` retain service-free contracted continuations and let `S` retain the
actual terminal spectator endpoint.  For

    h_C(u) = B_ell(u) + C log(u+e),

the maximal-source alternatives in (7.13) are exhaustive.  If a maximal-order
service mark is present, its bounded spectator jump costs at most
`j_* log(u+e)+O(1)`, while deleting the `C log(u+e)` boundary term pays
`-C log(u+e)`.  If no maximal-order service mark is present, the strong cut
supplies a maximal-order descending continuation; every positive clock is one
source order lower.  Choosing `C>j_*` therefore handles the previously fatal
`u -> u+2` endpoint and every bounded zero-order service endpoint.

The positive residual has finite support.  Lemma 7.1's killed transience then
makes its compact `Q`-Green correction bounded.  Retaining `S B_ell`, rather
than replacing service by a cemetery value, gives the stated
`O(log(u+e))` actual-endpoint loss.  No new rate or strong-orientation
counterexample to this argument was found.

## Load-bearing gap at (7.17)

The text controls the first paid interruption and says to expand again at the
next one.  It then invokes a *finite nested hierarchy* of polynomial weights.
The physical paid count `J`, however, is unbounded.  For any fixed truncation
order `K`, the exact nonnegative ordered expansion has an endpoint-weighted
remainder of the form

    K_0 K_1 ... K_(K-1) P^[K] f_r,

where `f_r` is the unbounded endpoint weight.  Total continuation mass at most
one controls an unweighted remainder, as in Section 6, but does not control
this weighted remainder.  The snapshot supplies none of the following:

- a weighted contraction for the full paid kernel;
- a joint factorial/Foster tail for the unbounded cofactor and paid count;
- a paid-count cutoff with an endpoint-weighted boundary estimate; or
- a uniform bound on the displayed remainder as `K` tends to infinity.

Consequently neither line of (7.17) follows from the written finite iteration.
The same missing closure is used again for the all-paid sum in (7.18), all
fixed physical-duration moments, the all-reaction promotion estimate (8.2),
exhaustion `P(D)=1-o(1)`, and the Taylor moments (8.6a).  Thus the negative
fourth-power conclusion (8.6b) is not yet established by the snapshot even
though its algebra is correct conditional on those moment estimates.

## Concrete repair target

Before the promotion cutoff `U < n^(1/3)`, lower reactions which increase
`I` have total clock at most

    C{(1+U)^2 + (1+U)I},

whereas the fast clock is comparable to `n I` for `I>0`; a source containing
`2I` cannot increase `I` because every target has cofactor count at most two.
This gives a small upward ratio, at worst `O(n^(-1/3))`, until the cofactor is
large.  Degree-two paid neutral cycles at a fixed cofactor level must then be
controlled jointly with their competing fast service clock.  A stated joint
factorial Lyapunov estimate for `(I,J,R)`, followed by summation of the ordered
series in polynomial endpoint weights, would close the required remainder.
The repair must explicitly derive both lines of (7.17) and the corresponding
duration bound; citing a finite hierarchy alone is insufficient.

## Section 6 bookkeeping

The exact-physical-state regeneration convention and cumulative exceptional
mark `A` are coherent.  Equation (6.3) must be read as the raw
`I/J^raw/C^raw` boundary event only: `A` can enter a new exact-regeneration
block already near its cutoff, so a literal per-block estimate including the
`A` branch is false.  The following paragraph does split off `A` and controls
it by the Section 5.3 macro trichotomy, so the final `-1/8` boundary arithmetic
survives.  This is a notation-scope blemish, not the load-bearing failure.

## Reproduction checks

The canonical suite and the two prior adversarial suites all pass (18 tests in
total).  Direct certificate replay reproduces the frozen selector hashes,
407 incidences, 333 pairs, 951 generalized rows, 317 handoff targets, and all
false certification flags.  Independent Pandoc HTML and LaTeX conversions of
the theorem note complete without warnings.  These finite and render checks do
not supply the missing analytic paid-tail estimate.
