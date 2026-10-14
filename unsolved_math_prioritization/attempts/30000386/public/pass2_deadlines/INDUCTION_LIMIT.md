# Why the mass/peak three-deadline proof is not a general induction

This is a limitation of the sufficient certificate in THREE_DEADLINES.md, not a losing-game result.

Use three successive later gaps of length two. Each gap has four-child scale a=1, endpoint set E_0 of size nine, wait w=1, and no block traversal. The boundary and wait reserve is therefore two updates. If the current dominating profile has mass beta and peak beta/9, its average on nine endpoints is beta/9, and the next denominator is

D=9-2 beta.

The newly farthest kernel has upper-bound profile

(beta',alpha')=(9 beta/(9-2 beta), beta/(9-2 beta)).

Starting with the point-bomb update and applying the full family recurrence gives successive farthest profiles and denominators:

- First smoothing: D=7; (beta,alpha)=(9/7,1/7).
- Second smoothing: D=45/7; (beta,alpha)=(9/5,1/5).
- Third smoothing: D=27/5; (beta,alpha)=(3,1/3).

At every step in this example the farthest profile dominates the other retained profiles on each relevant endpoint-set size. If the first lethal time is seven, its initial phase has scale a=4, no wait, and two block traversals: two moves with nine terminal candidates, then four moves with thirty-six terminal candidates (the temporal order is the reverse, but the additive estimate is the same).

The sufficient first-phase hazard bound is

2*(1/3)+4*(3/36)=1.

Thus this mass/peak certificate does not establish the strict final inequality for the allowed times {7,9,11,13}. It does not prove any actual play reaches that upper bound, and it does not show that the three-times construction is mathematically incorrect. It shows exactly where the proposed induction to a fourth time ceases to produce a certificate.

The PASS1 full-game finite-horizon result already covers horizon seventeen, so this failed certificate occurs inside an independently certified winning horizon. In particular, the example must not be described as a Devil strategy or a counterexample to the Time-Bomb conjecture.

A sharper certificate can retain the full spatial concentration profile of every convolution instead of only its mass and peak. The separate concentration-profile lane investigates that refinement. No general finite-known-set induction follows from the two-number proof supplied here.
