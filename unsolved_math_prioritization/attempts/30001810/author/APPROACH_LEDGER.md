# Chronological mathematical approach ledger

Problem 30001810 / OWR-5158-010. This ledger counts mathematical approaches only. Source retrieval, inherited-attempt screening, checking, and packaging are not turns. All entries concern finite real singular chains on smooth closed connected oriented manifolds unless an entry says otherwise.

## Turn 1 — Rational reduction and geometric realization (2026-10-07 UTC)

Attempt: reduce the equality problem to a concrete integral, simplexwise-immersive realization problem, without losing the ℓ¹ budget.

Work: Fix an immersive integral triangulation cycle t. For any real immersive fundamental cycle z, choose an ordinary real (n+1)-chain w with z−t=∂w. On the finite supports of z and w this is an affine linear system with integer coefficients and integer right-hand side. Rational points are dense in its real solution set. Hence the immersive infimum is unchanged when coefficients are rational. Clearing denominators gives integral immersive cycles c representing d[M], with cost ||c||₁/d. Pairing identical oppositely signed face occurrences realizes c as a map from a finite oriented face-paired pseudomanifold; every top-simplex restriction is immersive and its normalized number of top simplices has the same infimum.

Outcome: proved exact rational and normalized pseudomanifold formulas; there is no integrality obstruction at the coefficient level. The construction allows singular links and folding across glued faces, and does not turn the pseudomanifold map into a global immersion.

Remaining gap: starting from an ordinary nearly efficient cycle, no construction here makes its top-simplex maps immersive with asymptotically zero normalized overhead. Rational approximation alone does not change their differential rank.

## Turn 2 — Finite-cover transfer and self-cover dilution (2026-10-07 UTC)

Attempt: use increasing degree to dilute the cost of an immersive fundamental cycle.

Work: Lift every simplex of an immersive cycle through a finite smooth covering. Its open-neighborhood immersion lifts after shrinking to a convex neighborhood of the domain simplex. Transfer commutes with boundary and costs at most the number of sheets. Pushforward is also immersion-preserving and cannot increase ℓ¹ cost. The two inequalities give μ(N)=d μ(M) for a d-sheeted covering N→M. Ordinary simplicial volume satisfies the same argument. Thus the defect μ−ν scales exactly under finite covers.

Outcome: proved equality μ=ν=0 for any manifold admitting a smooth self-cover of degree greater than one, and for its finite covered/covering relatives as specified in the report. Examples include tori and N×S¹. Equality for a manifold is equivalent to equality for any connected finite cover.

Remaining gap: a tower of unrelated finite covers does not by itself supply cycles of sublinear immersive cost. Pulling a fixed cycle up gives exactly the unhelpful linear upper bound.

## Turn 3 — Product chains and propagation of vanishing (2026-10-07 UTC)

Attempt: build immersive cycles on products from efficient cycles on their factors.

Work: Analyze the standard (p,q)-shuffle cross product. Every staircase simplex map Δ^(p+q)→Δ^p×Δ^q is an affine full-dimensional embedding, so composing it with the product of two open-neighborhood immersions remains immersive. Interior faces cancel by the usual shuffle identity. The number of shuffles is binomial(p+q,p).

Outcome: proved μ(M×N)≤binomial(p+q,p) μ(M)μ(N). Consequently any zero-immersive-volume factor forces μ(M×N)=ν(M×N)=0. This also propagates the self-cover examples.

Remaining gap: the combinatorial factor is not one, and the ordinary product norm is not generally multiplicative. Equality of the two norms for both factors does not follow for their product merely from this upper bound. A general sharp straightening construction remains absent.

## Turn 4 — Test relative simplex repair by an explicit fold (2026-10-07 UTC)

Attempt: keep the already paired faces of an efficient ordinary cycle fixed and replace its top simplices by immersions, using asphericity to remove extension obstructions.

Work: On D=conv{(−2,0),(1,1),(1,3)}, take f(x,y)=(x²,y), then project to R²/(10Z)². Each edge has nonzero y-velocity and therefore immerses. However, f has signed degree −1 at (1/4,3/5) and +1 at (1/4,2). Any filling with the same boundary lifts to R² with exactly the same boundary values. An immersion on connected D has constant Jacobian sign, so its two degrees cannot have opposite signs.

Outcome: proved there is no immersive filling with these fixed immersive faces, although the target is an aspherical torus and the boundary already has a smooth filling. This rigorously rejects the unqualified face-fixed repair strategy.

Remaining gap: this local obstruction is not an obstruction to an entirely different global fundamental cycle. In fact the torus has both volumes zero by Turn 2. A successful proof must allow coordinated face changes or norm-controlled changes of the cycle.

## Turn 5 — Exact duality and the missing bounded extension (2026-10-07 UTC)

Attempt: characterize the comparison by bounded cocycles rather than direct simplex repair.

Work: On the space of immersive n-cycles define L(z)=μ(M) deg(z). The definition of μ gives |L(z)|≤||z||₁. Hahn–Banach extends L with norm at most one to the span of immersive n-simplices. It annihilates the intersection with ordinary boundaries, so an algebraic extension to all singular n-chains can be chosen to annihilate all ordinary boundaries. This produces an ordinary cocycle bounded by one on immersive simplices and evaluating to μ(M) on [M]. The reverse bound is immediate by pairing.

Outcome: proved an exact dual formula, with its supremum attained, and an exact comparison criterion: μ=ν if and only if every ordinary top cocycle bounded by one on immersive simplices is cohomologous to a cocycle bounded by one on all singular simplices. The criterion includes the zero-norm case explicitly.

Remaining gap: the algebraic extension is not bounded on arbitrary simplices. Asphericity has supplied no mechanism to secure that bound. Invoking the ordinary bounded-cohomology duality without this additional step would beg the original question. Five mathematical approaches are complete; the general equality remains unresolved.
