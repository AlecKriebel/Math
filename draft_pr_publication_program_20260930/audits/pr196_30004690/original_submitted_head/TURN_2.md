# Recovered substantive turn 2: anisotropic ellipse-flow obstruction

Problem 30004690. Historical substantive-turn count remains unknown. This is documented recovered turn 2. The full interior non-C² construction is still unresolved.

## New mechanism and exact question

Turn 1 treated dilations inside one fixed slit-domain Riemann map. Here the domains are allowed to change conformal shape: we test arbitrary nested ellipses with independently varying major and minor axes, collapsing to a segment. This is a simple genuinely anisotropic candidate for the source's inverse Hele–Shaw construction. The desired improvement would be a smooth density that is positive on regular points of the terminal slit and allowed to vanish at its singular endpoints.

The calculation below shows that this entire ellipse ansatz cannot provide even a continuous bounded density positive at any interior point of the slit. The obstruction is independent of the time reparametrization.

## Geometry and inverse density

Work in a coordinate w=x+iy on P¹, with injection at infinity. A Möbius change of coordinate moves the injection to zero if desired. For 0<b<b0 let

    E_b = {x²/a(b)² + y²/b² <= 1},
    Ω_b = P¹ \ E_b,

where a is C¹, a(b)>0, a'(b)>0, and a(b) tends to a0>0 as b decreases to zero. Then Ω_b increases as b decreases, and its complement collapses to the segment [−a0,a0]. We allow an arbitrary increasing area-time parameter t as b decreases.

The exterior conformal parametrization is

    w(ζ) = (a+b)/(2ζ) + (a−b)ζ/2,    |ζ|<1,

with w(0)=infinity. On |ζ|=1 this gives an ellipse parametrization, up to reversing the sign of its angular parameter. Harmonic measure at the source is therefore dθ/(2π). Parametrize the same ellipse by

    w_b(θ) = a(b) cosθ + i b sinθ.

For a decreasing b, its inward normal displacement times boundary arclength is

    −db [ b a'(b) cos²θ + a(b) sin²θ ] dθ.

Write D_b(θ)=b a'(b) cos²θ+a(b) sin²θ. It is positive. Darcy's law, or equivalently equality of weighted normal flux with harmonic measure, implies that the prescribed area density ρ must obey

    ρ(w_b(θ)) = k(b)/D_b(θ),                        (1)

where k(b)=−t'(b)/(2π)>0. This scalar k incorporates every possible time reparametrization. Normalization of dd^c changes only the harmless common positive scalar. Crucially, k does not depend on θ.

## Obstruction theorem

**Claim.** If a nonnegative ρ satisfying (1) extends continuously to a neighborhood of the terminal segment, then ρ vanishes on the entire segment.

**Proof.** Suppose for a contradiction that ρ(x0,0)>0 at some |x0|<a0. For small b choose θ_b by cosθ_b=x0/a(b). Then w_b(θ_b) tends to (x0,0), and continuity gives a fixed m>0 such that

    ρ(w_b(θ_b)) >= m.

The tip w_b(0)=(a(b),0) tends to (a0,0). Continuity there gives an upper bound M>0 for ρ(w_b(0)). Formula (1) at the tip yields

    k(b) <= M b a'(b).

At θ_b it gives

    m [b a'(b) cos²θ_b + a(b) sin²θ_b] <= k(b).

Combining these inequalities and discarding the first nonnegative term on the left gives

    m a(b) sin²θ_b <= M b a'(b).

Since |x0|<a0, a(b) sin²θ_b is bounded below by a positive constant. Consequently b a'(b)>=c>0 for every sufficiently small b. But then

    a(b1)−a(b) = integral_b^b1 a'(s) ds
                >= c log(b1/b),

contradicting a(b)→a0<infinity. Thus ρ(x0,0)=0 for every interior point of the segment. Continuity also forces zero at its endpoints. This proves the claim.

Only boundedness at a tip and positive continuity at a regular slit point were used. Smoothness is therefore more than sufficient for the obstruction. If a' vanishes at a positive b, the corresponding stationary tip already makes (1) incompatible with finite positive k, so that case does not rescue a regular strong flow.

## Scope and remaining gap

This does not prove that every smooth-density slit flow has zero density on its entire slit. It applies to axis-aligned nested ellipses with the stated parametrization; it is not a theorem about arbitrary nonelliptic domains. It also does not prove C² regularity of every ellipse-associated HCMA solution with zero slit density.

What it rules out is the intended simple repair of turn 1 by varying the ellipse aspect ratio and changing the time scale. Such a repair cannot keep positive density on regular slit points while merely flattening the endpoints. The endpoint approach must be geometrically more localized than an ellipse can supply, or a different HCMA mechanism is needed.

A possible next direction is a nonelliptic family with position-dependent collapse speed along the slit and separately controlled endpoint caps. To settle the original problem, that route must still establish a single globally smooth nonnegative prescribed density, the precise HCMA solution, and actual failure of second differentiability. None of those missing claims is inferred from numerical evidence or from loss of maximal rank alone.

## Source relation

The inverse-density mechanism comes from Ross–Witt Nyström's [2019 duality paper, Theorem 3.1 and its proof](https://www.numdam.org/item/10.5802/aif.3237.pdf) and the [2021 Oberwolfach contribution, p. 1324](https://ems.press/content/serial-article-files/46904). The published inverse theorem uses standard behavior at the terminal point; it does not automatically certify a collapsing slit endpoint. The calculation above directly tests the missing endpoint condition for a particular nonradial family.

Outcome: a rigorously identified obstruction for a second construction family. No full resolution or novelty claim. Work on the original target remains active; this checkpoint is preserved before a separate requested review task.
