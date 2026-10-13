# Supplemental algebra and boundary adversary

UTC: 2026-10-13T04:09:56.216257+00:00
Own completion: 90%. Overall PR177: 65% unchanged.

The universal proof does not need a theorem describing all of V or extending a character from C[g]. Hypothetical arbitrary h in g^N=f h is itself finite-order, so it acquires P_h from the written singular-braid lemma. The resulting polynomial identity t^(2N)=t^2(4t^2-1)P_h(t) is impossible at t=1/2 for every N>=1. This remains true when h vanishes or changes arbitrarily away from the test family; no injectivity of the restriction is used.

A tempting counterargument is the pointwise solution h_N(L)=g(L)^(N-1)/(4g(L)-1) for g(L)>0 and h_N(L)=0 for g(L)=0. It satisfies f h_N=g^N as a function on links. This does not supply membership in V. If it were finite-order, its restriction would be a polynomial P. Infinitely many positive integers would force (4t^2-1)P(t)=t^(2N-2), and evaluation at 1/2 makes that impossible. Thus even a bounded pointwise inverse fails the required polynomial restriction; the proof has not assumed every function on actual links is finite type.

In the labelled theory let B=(ell_ij). Then g=sum ell_ij*ell_ij belongs to B, so f also belongs to B and fV is contained in B. However g is outside rad(fV), hence outside fV. Thus fV is strictly smaller than B although their actual zero sets coincide. The counterexample cannot decide whether every finite-type invariant vanishing on algebraically split labelled links belongs to B, the source's separate example. The same strictness argument also explains why equality of actual zero sets never licenses replacing the selected ideal by a different ideal.

Forgetting labels or orientations simply passes to an invariant subalgebra after pullback to oriented labelled links. The restriction-character construction restricts to that subalgebra, which contains g and f. It does not rely on character extension, label choices made globally on unordered links, or orientation at an intercomponent singularity being canonical. The vanishing-order condition is unaffected by changing local crossing-sign conventions, which only multiply the alternating cube value by a sign.

The all-component version does not assert a uniform crossing-growth constant for all invariants or an order bound common to V. A component-count function has order zero and restricts to a constant on the fixed family. The degree bound for g uses finitely many pairwise affine forms on each resolution cube and remains two for every finite component count. Empty links, if included, and knots have g=0 and enlarge the nonempty actual zero set without changing the character obstruction on two components.

All use of nonnegative integer values refers to ordinary integer linking numbers before embedding into a coefficient field. Over any characteristic-zero field the embedding of integers is injective; 1/4 is available and nonzero powers remain nonzero. The integer-valued companion statement only uses a ring map into Q, not into Z. Formal series in a completion cannot be evaluated at 1/2 without additional structure and can admit an inverse of 4g-1. The manuscript explicitly excludes that domain, positive characteristic, and homogeneous-ideal variants.

No added defect found by these boundary attempts. These are original algebraic checks, not sampled evidence or new claims of historical novelty.
