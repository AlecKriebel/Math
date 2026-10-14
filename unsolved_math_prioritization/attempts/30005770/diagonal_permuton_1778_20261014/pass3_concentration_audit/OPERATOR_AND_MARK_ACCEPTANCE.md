# Independent acceptance of the weighted-operator boundary and one-sided mark

Shared PASS3, 14 October 2026.

## Verdict and exact version

**Accepted in full within the stated scope.** Reviewed file:

`pass3_kernel_bounds/WEIGHTED_OPERATOR_BOUNDARY.md`, 8398 bytes, SHA-256 `b4b2057622a189442bcff813648db124642862ce65f3805bc843bc25550d9597`.

The earlier submitted SHA `a74b47f5cc5979dbc73ee302146a670544271a4f14bb97a73d6313651bf3eb1b` differs only by the cited reciprocal-certificate hash. I verified that replacing the final citation hash by its earlier value reproduces the earlier whole-file hash. There is no mathematical change between those versions.

The final reciprocal input is `pass3_kernel_feasibility/SQUARED_KERNEL_GAP_IMPOSSIBLE.md`, 11091 bytes, SHA-256 `99e3262041ff09e1ce308fbc5a13704d286602e0eb5af7d814d99915848c314f`. Its actual-permutation two-collapse encoding and symmetric four-point guard give a_n<=T_(n+4), with T counting ordered reciprocal kernel products. That exact combinatorial input is independently accepted in the complementary structural audit; it is also consistent with my direct inspection of the construction.

No correction is required. The statements do not prove the missing two-sided mark, largest-cell sublinearity, or a weak permuton theorem.

## 1. Positive diagonal Hilbert–Schmidt obstruction

The matrix is correctly defined entrywise as

    B_q(z)_(A,C)=z^((|A|+|C|)/2) K(A,C) q_C/q_A,

with each q_A finite and strictly positive. The family may depend on z. The proof does not assume an unbounded diagonal matrix defines an everywhere-defined similarity on ell^2.

On a finite symmetric index square E x E, AM–GM applied to the two reciprocal entries gives

    sum_(A,C in E) |B_q(z)_(A,C)|^2
      >= sum_(A,C in E) z^(|A|+|C|) K(A,C)K(C,A).

The diagonal factors cancel exactly. Increasing E by bounded state size and using nonnegativity proves the inequality for the full sums in the extended reals. The accepted coefficient inequality a_n<=T_(n+4) then gives the lower bound z^4 F(z).

For every positive z>rho, F(z) diverges by its exact radius, so no such entrywise reweighting is Hilbert–Schmidt there. This requires neither compactness nor irreducibility nor a spectral-radius argument. It does not establish divergence at rho unless F(rho) itself diverges. It does not exclude bounded non-Hilbert–Schmidt operators, other spaces, or exclusively subcritical estimates.

## 2. Uniform absolute frontier coefficients

For every fixed alpha of length at least two, the accepted Catalan amplification gives

    N_n(m) [s^t]C(s)^m <= a_(n+t) <= lambda^(n+t).

Distinct level-n parents have disjoint descendant sets, and labels at least m dominate the Catalan label-m continuation. Thus the count inequality has the right normalization before summing.

For fixed 0<s<1/lambda, multiply the coefficient inequality by s^t and sum all t>=0. Both sides are nonnegative, and the right geometric series converges. This proves exactly

    N_n(m) <= lambda^n / [(1-lambda s) C(s)^m].

The statement includes zero counts when m>n+1 and the n=0 sentinel convention. Continuity of C up to1/4 permits choosing log C(s)>eta for every eta<log C(1/lambda), including lambda=4. The resulting constant is independent of both n and m.

The use of a_j<=lambda^j is valid because the class is sum-closed and its finite exponential growth is the Fekete supremum. The result is an absolute count bound. It does not assert a_n is comparable to lambda^n by fixed multiplicative constants.

## 3. Exact first-cell translation and a common exponential mark

The bijection pi -> reverse(pi inverse) sends1324 avoidance to4231 avoidance and the top-value213-free interval to the longest312-free prefix. The exact identity T=L-1 is correct, including alpha-absent permutations. Therefore the uniform absolute frontier bound applies simultaneously at every first-cell threshold.

For 1<u<C(1/lambda), choose eta with log u<eta<log C(1/lambda). The elementary tail-sum formula

    u^T=1+(u-1)sum_(m=1)^T u^(m-1)

and the absolute count bound give a constant times lambda^n for the total first-cell exponential weight at size n. The geometric series in m converges because u exp(-eta)<1. The size generating series consequently converges at every0<z<rho, with this same fixed u.

The exact first-state path decomposition identifies that series with sum_A u^|A| z^|A| h_A(z). The factor ell_A is absent because the marked cell is first. This is a genuine strengthened one-sided estimate, but there is no inference to the arbitrary-cell weight z^|A| ell_A h_A.

## 4. The weighted-sup contractions are well defined

For0<z<z'<rho, every coordinate h_A(z') is finite and at least one. The space with norm sup_A |f_A|/h_A(z') is a weighted copy of ell-infinity. For any vector in this space, the transition sum is absolutely convergent, since it is dominated by its norm times

    sum_C K(A,C)z^|C|h_C(z')
      <= (z/z')[h_A(z')-1].

The nonempty-state condition gives the factor z/z'. Dividing by h_A(z') proves operator norm at most z/z'<1. Its Neumann resolvent is bounded on that explicitly specified space. The reversed transition and ell(z') satisfy the same argument with the orientation reversed.

These spaces and weights depend on z'. A pair of separate weighted-sup bounds does not supply an exponential mark for the product ell_A(z)h_A(z), an ell^2 compactness property, or a common two-sided smoothing margin. The final note preserves this limitation correctly.

## Conclusion

Theorem A rules out a broad proposed repair of the impossible strict squared-kernel gap. Theorems B–C strengthen the available first-cell control, and Section D supplies valid subcritical weighted operators. All are accepted exact statements. The arbitrary-cell two-sided completion problem remains open.
