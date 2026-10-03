# Distinct postseal adversarial audit of the stronger rank route

2026-10-03 07:23 UTC. Completion estimate: 85% of the whole-package audit; actual refreshed queue/integration gate is pending. The original mathematical seal was completed before this derivation was read. This report concerns the independent diagonal family's additional audit deduction and is not a sixth author turn or a replacement theorem in PR375.

## Exact claim and verdict

The proposed deduction is `log M(exp T)=O(T/(log T)^2+(log T)^2)` a.s. as integer T tends to infinity, hence `log M(D) log log D/log D ->0` a.s. as real D tends to infinity. Under the exact independent 1/n inclusion model I find the universal proof valid, with no unproved probabilistic premise or rank assumption remaining. The proof below identifies every mechanism that a finite control cannot certify. The deduction remains a distinct postcandidate audit finding and does not determine the sharp log-log exponent, imply convergence on that scale, certify novelty, alter the frozen author packet, or justify a paper/DOI.

## Row restriction: the essential extra mechanism

For a whole equal-sum fiber of size K let its incidence columns be binary vectors in Q^K, and let its rank modulo the diagonal be R. Select R incidence columns independent modulo the diagonal. If two rows agree on these columns, their difference annihilates the diagonal and this basis, hence every incidence column; the two subsets would coincide. Therefore K<=2^R.

If R>=r, the matrix consisting of the diagonal column and any r independent incidence columns has column rank r+1. It has an invertible square submatrix on r+1 rows. Restrict to those rows. They are distinct subset representations of the same sum, and their incidence columns have quotient rank exactly r because the ambient quotient now has dimension r. This extraction is purely existential; the union event can be counted directly in dimension r+1. There is no missing factor for the original huge family or its row-subset choices. Every extracted witness already has r+1 labeled rows accounted for by its binary incidence columns.

Thus absence of any full-rank r+1-row witness bounds every fiber by 2^(r-1). Confusing absence of a particular family with absence of every extracted witness would invalidate this step; the written proof counts the entire full-rank witness event.

## Uniform event, bands, and the complete reinsertion count

Set epsilon=1/20, lambda=log(21/20), b=(21/20)log3-1, delta=1/100, r=floor((log T)^2), h_j=log(2^(j+1)-1), and `u=(b+delta)T/((21/20)h_r)`. Let the upper window be the finite integer set `[ceil(exp u),floor(exp T)]`, and let `t=10 log(T+2)/lambda`. Include all intervals of the logarithmic grid `u,1+floor u,...,T+1`, restricted to that ground set, plus the small-prefix count. There are O(T^2) intervals. The harmonic mean is at most interval log length plus an absolute constant, and `E exp(lambda N)<=exp(epsilon E N)` holds also with the forced first coordinate. Chernoff subtracts `(21/20)lambda` times the interval length, exceeding the mean coefficient epsilon, leaving at most `C exp(-lambda t)`. Hence the full event fails with probability O(T^-8), summable in integer T. Grid endpoints, truncation and the prefix split are explicitly covered; no statement uniform over an uncountable collection is needed.

Greedily retain descending independent incidence columns modulo the diagonal. A full-rank witness supplies exactly r pivots x_1>...>x_r. Set z_j=floor(log x_j); they may tie. For fixed ordered binary pivot columns and bands, every residual entry in `[exp(z_(j+1)+1),exp(z_j+1))` has its quotient type in the j-th flag space, and the bottom band `[exp u,exp(z_r+1))` has types in the last space. Residual entries above the top band have the diagonal type. This follows from the actual greedy ordering, not from a hypothesized generic flag. Allowing all classes in those enlarged bands only overcounts. Each j-th space has dimension j+1 and at most `2^(j+1)-1` diagonal quotient classes, uniformly over all rational spaces. Each class is counted, including the zero class.

For every residual assignment the equal-sum equation is a linear system in the r pivot numbers with independent quotient columns, so it determines at most one rational root tuple. A valid root must be an integer, distinct, ordered, in its specified band, and absent from the residual set; invalid solutions are discarded. The exact finite Bernoulli mass is the residual mass times `product 1/(x_j-1)`, bounded by `2^r exp(-sum z_j)`. The probabilities of distinct residual configurations sum to one. Deletion decreases every occupancy count, so the good event's interval bounds hold for each residual configuration that contributes. This completes the full root-elimination sum; no individual-root summation or assertion about a deletion distribution is inserted.

## Negative coefficients and growing parameters

The residual assignment logarithm is bounded by

`(21/20)[sum_(j<r)(z_j-z_(j+1))h_j+(z_r+1-u)h_r] + t sum_j h_j`.

Subtract the root charge `sum z_j` and add r log2. The coefficient of z_1 is b. Every later coefficient is `(21/20)log[(2^(j+1)-1)/(2^j-1)]-1<0`, because the ratio is at most 7/3 and `(21/20)log(7/3)<1`. The fresh exact atanh-series certificate checks this strict inequality; the universal ratio bound is elementary. Use z_1<=T and z_j>=0 on negative coefficients. Since `(21/20)u h_r=(b+delta)T`, the resulting exponent is at most `-delta T+O(t r^2+r)`.

There are at most `2^(r(r+1))` ordered binary pivot bases and `(T+1)^r` band tuples. Their logarithmic cost is O(r^2+r log T). For the stated r and t, the total error is O((log T)^5)=o(T). The union probability is therefore eventually at most exp(-delta T/2), summable. This is a uniform all-r argument with explicit error growth; finite rank enumerations do not establish it.

First Borel–Cantelli applied to both exceptions gives eventual good occupancy and absence of every full-rank witness. The high-window fibers are at most 2^(r-1). The deterministic convolution bound charges only `2^N([1,exp u))` to the small prefix, and good occupancy bounds that N by `(21/20)u+t`. Since h_r~r log2, this gives precisely `log M(exp T)=O(T/r+r+log T)`. Multiplication by log T/T tends to zero. For real D use the neighboring integer T in the exp grid; its two normalizers have ratio tending to one. Nonnegativity gives the claimed limit zero. The infinite assertions follow from these summable inequalities, not from a finite simulation.

## New falsifiers and boundaries

`rank_extension_controls.py` imports only this auditor's independent rational utilities, no sibling or candidate code. It checks complete equal-sum fibers of every selected subset of [2,9], extracts independent row restrictions, and enumerates the entire rank-two deletion/reinsertion kernel on [2,6], including every affine target identity. Every actual rank-two collision configuration is covered with exact probability weights; the union over ghost assignments dominates the full event probability. This is stronger than testing a chosen witness or selected pivot tuple. The coefficient certificate is exact rational arithmetic. Results and UTC are in `RANK_EXTENSION_CONTROLS.json`. No failures arose. These controls test the finite mechanisms and can falsify omissions; the preceding proof supplies universality.

The frozen PR's C_* upper statement and fixed logarithmic-moment upper statements remain valid even if a stronger bound is available. Changing the author theorem/history is outside this auditor's authority. The whole original scientific target still has an unmatched polylogarithmic lower scale and no finite identified leading exponent. Historical and other-family verdicts were read only after the original mathematical seal and serve as comparison, not premises.
