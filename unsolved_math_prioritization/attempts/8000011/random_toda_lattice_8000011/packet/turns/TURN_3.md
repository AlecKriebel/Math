# Author turn 3: second-order mean constant

2026-10-03 06:22 UTC. Partial theorem. Original general request unresolved. Completion estimate: 80% toward fixed-n asymptotic packet, 15% toward full target.

## Two-term fixed-n asymptotic

With probability one, the smallest adjacent eigenvalue gap d is attained at a unique index r, 1<=r<n. Indeed the ordered GOE density is absolutely continuous and equality of two distinct adjacent gaps is a proper linear hypersurface. The corresponding slow coupling is k_*=n−r.

For each fixed sample, the tau sums from Turn 1 imply

 b_k(t)=c_k exp(−d_k t)(1+o(1)),
 b'_k(t)/b_k(t)=−d_k+o(1), t→infinity.

The second statement follows by differentiating the finite exponential sums after factoring their unique dominant terms. It is not obtained by differentiating an unspecified little-o. Since all d_k>0, every coupling is eventually strictly decreasing. Uniqueness of d makes b_(k_*) eventually strictly larger than every other coupling.

Moreover T_all(epsilon)→infinity as epsilon→0: on every compact time interval, max_k b_k(t) is continuous and strictly positive, so has positive minimum. Thus for sufficiently small epsilon the first simultaneous crossing occurs in the eventual regime where the slow coupling is the maximum and decreases strictly. Solving its scalar crossing equation gives

 T_all(epsilon)−log(1/epsilon)/d → log(c_(k_*))/d.          (7)

Turn 2 already bounds the left-hand side in absolute value by the integrable variable (4K+n log2)/d; the limit is bounded by the same variable. Dominated convergence therefore proves

 E[T_all(n,epsilon)] = C_n log(1/epsilon)+B_n+o_n(1),       (8)

where C_n=E[1/d] and B_n=E[log(c_(k_*))/d]. The little-o is only for fixed n; no uniformity in n is claimed. No reciprocal of the difference between the smallest and second-smallest gaps is needed for domination, so nearly tied gaps do not create an unexamined expectation singularity.

## Norming constants cancel from the mean correction

Expanding the dominant Vandermonde products at a gap index r gives

 c_(n−r) = (lambda_(r+1)−lambda_r) sqrt(w_r/w_(r+1))
            prod_(j=r+2)^n [(lambda_j−lambda_r)/(lambda_j−lambda_(r+1))].   (9)

For the minimum-gap index r, independence and exchangeability of the Dirichlet weights give conditional mean log(w_r/w_(r+1))=0. The logarithms are integrable by Turn 2, so conditioning and cancellation are legitimate. Hence the second constant is an eigenvalue-only integral:

 B_n=E_lambda{ [log d + sum_(j=r+2)^n log((lambda_j−lambda_r)/(lambda_j−lambda_(r+1)))]/d }.                  (10)

The sum is empty for r=n−1. Selection of r depends only on lambda. This formula is asymmetric because the Lax clock sorts descending and the weights refer to the first endpoint; it nevertheless defines the required mean. Reflection symmetry can give an alternative symmetrized expression, but is unnecessary.

## n=2 normalization check

For n=2, d has density (d/4)exp(−d²/8), d>0. This follows from d=sqrt((a_1−a_2)²+4b_1²): a_1−a_2 is N(0,4), and 2b_1 is twice an independent chi_1 variable. Thus

 C_2=sqrt(pi/8),
 B_2=(sqrt(pi/8)/2)(log2−EulerGamma).

The calculation uses integral_0^infinity exp(−d²/8) dd and its Mellin derivative. It checks the factors of two in the Lax clock. This is not a general-n exact mean formula.

## Remaining gap

We now have a justified two-term small-tolerance expansion for each fixed n, with finite explicit spectral integrals for both coefficients. Finite positive tolerance, growing dimension, and general average-complexity behavior remain outside the theorem. The expansion and the cancellation require independent review before being promoted.
