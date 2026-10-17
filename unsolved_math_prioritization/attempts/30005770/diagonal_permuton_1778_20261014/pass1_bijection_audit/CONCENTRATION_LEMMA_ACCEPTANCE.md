# Independent check of concentration support lemmas

Shared PASS 1, 14 October 2026. This is the structural/bijection reviewer's additional check of Sections 2, 3 and 5 of `pass1_concentration_audit/AUDIT.md`.

## Verdict

**All four requested support statements pass:** the exact square-spread inversion-density correction, its weak-convergence equivalence, the one-sided permuton estimate, and the uniform small-point-probability support criterion. None of these statements alone proves the universal target.

## 1. Exact pattern-density calculation

Let q(mu) be the probability that two independent mu-points are discordant. The uniform coordinate marginals are nonatomic, so coordinate ties have probability zero. For the square-spread permuton of pi, ordered pairs of distinct squares contribute `2 inv(pi)/n^2`. Choosing the same square has probability `1/n`; conditional on that event the four coordinate variables are independent uniform variables on their respective intervals, and discordance has probability1/2. Therefore

`q(mu_pi)=2 inv(pi)/n^2+1/(2n)`.

The correction is necessary even for the identity permutation. Its square-spread permuton is not literally supported on the diagonal.

For a general permuton and F(x,y)=mu([0,x]x[0,y]), conditioning on the first point gives one discordant orientation with probability `x-F(x,y)`. Symmetry of the two samples supplies the factor2. Thus

`q(mu)=2 integral (x-F(x,y)) dmu`.

Since F<=min(x,y), this gives `q>=2 integral(x-y)_+`. Equality of the coordinate means gives `2 integral(x-y)_+=integral|x-y|`, and the explicit diagonal coupling gives `d_BL<=integral|x-y|`. The entire inequality chain is valid for every permuton, with no uniform-avoider assumption.

## 2. Weak convergence and expected inversion density

If deterministic permutons mu_j converge weakly to mu, then their product measures converge weakly. The discordance-indicator discontinuity set is contained in coordinate ties, which have zero mu-times-mu mass. Portmanteau therefore proves continuity of q on the space of permutons.

For random permutations, `E inv(Pi_n)/n^2 ->0` implies `E q(mu_(Pi_n))->0` by the exact finite-n formula. Markov and `d_BL<=q` prove weak convergence in probability to mu_I.

Conversely, weak convergence in probability to deterministic mu_I and continuity of q imply q->0 in probability. Boundedness0<=q<=1 implies convergence of its expectations, hence of expected inversion density by the same exact formula. No coupling across n, almost-sure claim, or uniform-in-pattern rate is required.

## 3. One-sided strip estimate

For Z=X-Y, uniform marginals give EZ=0. If `P(Z>delta)<=delta`, then `E Z_+<=delta+P(Z>delta)<=2delta`, hence `E|Z|<=4delta`. Coupling (X,Y) to (X,X) yields the d_BL bound. Markov on |Z| gives the stated two-sided strip-mass estimate.

The anti-diagonal reflection uses Z=X+Y-1 and (X,1-X), with exactly the same zero-mean identity. The proof therefore controls a weak metric without introducing total variation or a spurious two-sided maximum-displacement bound.

## 4. Small-point probabilities imply zero limiting mass

Take U relatively open in the square, and f continuous, nonnegative, with support compactly contained in U. A positive distance separates its support from the relative complement of U, unless that complement is empty. For sufficiently large n, every grid cell meeting the support has its upper-right corner in U. Using the density-n square convention and the assumed uniform bound b_n gives

`E integral f dmu_(Pi_n) <= ||f||_infinity n b_n ->0`.

For any subsequence whose random permutons converge in distribution to M, `mu -> integral f dmu` is bounded and continuous, so its expectation under M is zero. Nonnegativity makes that integral zero almost surely. A countable collection of continuous bump functions covering U, or a standard countable compact exhaustion with such functions, then yields M(U)=0 almost surely.

The uniformity over all moving lattice corners in U and the scale b_n=o(1/n) are essential to this stated argument. A pointwise little-o assertion cannot silently replace them. The relative-topology wording above also covers neighborhoods meeting the boundary of the unit square.

## Scope

These are valid general analytic support lemmas. Their correctness supplies no missing enumeration estimate for arbitrary alpha and no positive-mass conclusion from equal exponential growth rates. The separate labeled-tree argument establishes only the two restricted target cases already accepted in `WEIGHTED_HEIGHT_ACCEPTANCE.md`.
