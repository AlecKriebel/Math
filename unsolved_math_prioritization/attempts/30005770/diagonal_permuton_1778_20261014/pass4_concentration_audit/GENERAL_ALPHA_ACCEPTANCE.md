# Independent acceptance of general-alpha growth, packing and spatial obstruction

Shared PASS4, 14 October 2026.

## Verdict and exact pin

**Accepted in full within its stated partial scope.** Reviewed artifact:

`pass4_general_alpha/GROWTH_PACKING_AND_SPATIAL_BARRIER.md`, 13032 bytes, SHA-256 `c0e18d22fbda449f7303cf9688a66f10269d417e2687e2766ae7cd72e5632465`.

The strict growth gap, exact deletion count, exponential lower-tail bounds for deletion distance and disjoint packing, deterministic perfect-packing constructions, crossing metric bound and crossing-subpattern observation all check. No mathematical correction is required. No uniform-probability counterexample or universal diagonal theorem is proved.

## 1. Growth limits and the strict gap

A pattern ending in its minimum is direct-sum indecomposable, so its avoidance class is direct-sum closed. Its counts are supermultiplicative and bounded exponentially; hence a_n<=lambda^n with a genuine finite growth limit.

A permutation cannot have both a proper direct-sum cut and a proper skew-sum cut. If one cut comes first, choose an entry before that cut and one after the other cut: the two decompositions require opposite value orders for the same pair. Thus alpha is indecomposable under at least one of the operations, and Av(alpha) is closed under that operation. This correctly proves existence of mu and b_n<=mu^n, rather than assuming a growth limit for an arbitrary non-closed class. For length at least two, at least one monotone permutation avoids alpha at every size, so mu>=1.

Every alpha-free member has frontier label n+1. Applying the accepted frontier tail at scales approaching one, or equivalently its uniform absolute coefficient form, gives log(mu/lambda)<=-gamma, with gamma=log C(1/lambda)>0. No ratio-limit theorem is used. This is a special consequence for alpha versus alpha skew-sum1, not a blanket strict-growth assertion for all proper permutation subclasses.

## 2. Exact deletion encoding and entropy

For a fixed deletion size h, the two subsets record both positions and values. The deleted subpattern remains in the target class by heredity, and the retained subpattern is alpha-free. These four records reconstruct the original permutation uniquely. A canonical successful deletion choice is enough to make the map a function; the ambient tuple count is an upper bound, not an asserted sampling law.

The factor binom(n,h)^2 a_h b_(n-h) is therefore correct. Substituting the two exponential coefficient bounds gives

    |E_(n,h)| <= lambda^n exp{n[2H(h/n)-(1-h/n)g]},
    g=log(lambda/mu)>=gamma.

For0<delta<1/2 the exponent function increases throughout0<=h/n<=delta, including its continuous endpoint. Thus summing all h<=floor(delta n) incurs only a polynomial factor. Division by the actual a_n retains the subexponential defect lambda^n/a_n; it is not replaced by a bounded constant. The displayed limiting rate and eventual exponential probability bound follow.

The inequalities P_alpha<=D_alpha<=mP_alpha have the correct directions. Every deletion must hit each disjoint occurrence; conversely, deleting the union of a maximum packing leaves no further occurrence, since that would enlarge the packing. Hence the small-packing event is contained in the small-deletion-distance event with the stated factor m. This supplies exactly the same exponential rate bound.

## 3. Perfect packing for non-increasing alpha

When alpha is not the identity, its increasing-block inflation Q_k has exactly the descents of alpha. Every descent of a selected subpattern requires a descent in the corresponding intervening segment, and these segments are disjoint. Therefore a contained pattern cannot have more descents than its host. Since alpha skew-sum1 adds one descent, Q_k avoids it.

The prefix consisting of k direct-sum copies of alpha also avoids the target, and target sum-closure preserves avoidance after adjoining Q_k. The transversal choices in Q_k are disjoint alpha occurrences, partitioning all its entries; together with the prefix copies they form a perfect packing.

The first m entries form alpha, so the frontier is exactly m. The smallest s=o(n) values eventually lie in the direct-sum prefix, and their positions are at most m ceil(s/m)<=s+m-1. These are the asserted deterministic low-value properties.

A nonidentity permutation has a nonzero diagonal crossing at some prefix cut ell: otherwise all its initial sets would be the corresponding smallest values and it would be the identity. At the displayed lattice cut, exactly k c_alpha(ell) points cross. The square-spread permuton mass is exactly this count divided by2mk, giving at least1/(2m) at a fixed normalized cut.

## 4. Perfect packing for increasing alpha

For pi=I_((m-1)k) direct-sum J_k, an increasing m-subsequence must use a point from the lower-valued increasing prefix. Every later point exceeds that prefix point, so it cannot supply the terminal minimum of the forbidden pattern. Thus avoidance is valid, including m=2 and k=1.

Each group of m-1 prefix entries plus a distinct tail entry is increasing, and these groups partition all entries. The frontier is m, and the smallest o(n) values occupy their identity positions. At the midpoint of the decreasing tail the crossing count is floor(k/2), giving normalized mass tending to1/(2m).

## 5. Crossing mass really gives a fixed weak deviation

Under the contract's Euclidean bounded-Lipschitz metric, the function |x-y|/sqrt2 has supremum at most one and Lipschitz constant at most one. For a permuton, equality of opposite crossings gives

    integral |x-y| dmu = 2 integral_0^1 c_mu(t)dt.

The crossing function is1-Lipschitz with zero endpoint values. If its maximum is M, the full triangular lower envelope of area M^2 fits inside[0,1], so the last integral is at least M^2. Consequently d_BL(mu,mu_I)>=sqrt2 M^2.

Substituting the crossing lower limit1/(2m) gives exactly1/(2sqrt2 m^2), as claimed. The inversion-density calculations also agree when density means inv(pi)/n^2: respectively inv(alpha)/(4m^2) and1/(2m^2). No total-variation or maximum-displacement conclusion is being substituted for weak distance.

## 6. Spatial limitation

At a diagonal grid cut, the upper-left and lower-right crossing sets have equal size. If the former contained alpha, any point from the latter would occur later and have smaller value, completing alpha skew-sum1. Thus every crossing rectangle induces an alpha-free pattern. This is an exact actual-class observation.

It does not contradict the global perfect packing: occurrences covering crossing vertices can finish outside the rectangle. Nor does the deletion theorem control a crossing subset whose complement still has a substantial fraction of all entries. The explicit constructions prove the failure of that deterministic inference while preserving the accepted frontier and small-value properties. Their probabilities under the exact uniform law remain unestimated.

All constants may depend on the fixed alpha. No growing-pattern or uniform-in-alpha theorem is asserted. The alpha=1 case is appropriately separated as the already trivial increasing-permutation class.
