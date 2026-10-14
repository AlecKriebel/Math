# Exact descendant-weighted bottleneck for inversion concentration

This note records an unproved sufficient bridge left after the accepted frontier theorem. It is not a proof of that bridge or of the diagonal limit.

Assume throughout that |alpha| >= 2; the excluded case alpha=1 has only increasing permutations and is already solved. Use C_j, a_j, L and D_t from ACTIVE_FRONTIER_PROOF.md. For pi in C_n, let sigma_j(pi) be the standardized restriction to its j largest values, with sigma_0 empty. If child_k(sigma) means insertion of a new minimum at allowed gap k, then the successive minimum insertion gaps sum exactly to inv(pi). Hence, under the exact uniform law on C_n,

E inv(Pi_n)
 = (1/a_n) sum_(j=0)^(n-1) sum_(sigma in C_j)
      sum_(k=0)^(L(sigma)-1) k D_(n-j-1)(child_k(sigma)).

There is no unspecified independence in this identity. Each full permutation traverses one insertion edge at every level, and a fixed edge has exactly the displayed number of completions.

The ancestor marginal is

P(sigma_j(Pi_n) = sigma) = D_(n-j)(sigma)/a_n.

Because the gap used at level j is at most L(sigma_j)-1 <= n, the following condition would suffice for inversion density to vanish: for every epsilon > 0,

(1/n) sum_(j=0)^(n-1)
  [ (1/a_n) sum_(sigma in C_j, L(sigma)>=epsilon n) D_(n-j)(sigma) ] -> 0.

Indeed, after division by n^2, the contribution of labels below epsilon n is at most epsilon, and the remaining contribution is bounded by the displayed average. Taking limsup and then epsilon down to zero proves E inv(Pi_n)/n^2 -> 0.

The frontier theorem controls the same exceptional set under weight 1/a_j, not under D_(n-j)(sigma)/a_n. These laws agree only when the completion count is constant, which is not generally true. The exact completion bounds established in the proof are

B(L(sigma),t) <= D_t(sigma)
 <= binomial(L(sigma)+t-1,t) a_t
 <= binomial(j+t,t) a_t.

They suffice when t=o(n), equivalently at ancestor levels j=n-o(n), to control those near-final insertion levels. For t proportional to n they permit an exponential tilt. No estimate in this packet removes that tilt across a positive fraction of the insertion levels. That is the remaining bulk-concentration obstacle for this route.

For completeness, vanishing inversion density does give the required weak-permuton conclusion. The standard footrule/Kendall inequality sum_i |pi(i)-i| <= 2 inv(pi) can be proved by sorting adjacent descents: each swap removes one inversion and changes the footrule by at most two. Coupling a uniform point in each permutation square to its same-x point on the diagonal gives

d_BL(mu_pi,mu_I) <= integral |x-y| dmu_pi
 <= (1/n^2) sum_i |pi(i)-i| + 1/n
 <= 2 inv(pi)/n^2 + 1/n.

The middle inequality uses |x-y| <= |i-pi(i)|/n + 1/n within square i. Thus the missing weighted estimate would complete the target, but it has not been proved here. The inversion criterion itself is credited background already recorded in the original Oberwolfach report, not a new solution.
