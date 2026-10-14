# Independent review of the conditional squared-kernel criterion

Same PASS2 continuation, 14 October 2026. Reviewed artifact: `pass2_staircase_bias/SQUARED_KERNEL_NEXT_TARGET.md`, 8757 bytes, SHA-256 `f5dfd42ac902e46190f4ca5887752693efa00fb5f95a5af3e5d2646ad63a0dd9`.

## Verdict

**Accepted as a conditional theorem.** For the exact canonical kernel already accepted in `KERNEL_CROSS_REVIEW_RECEIPT.json`, the strict inequality

`beta = limsup (sum_{|A|+|C|=n} K(A,C)^2)^(1/n) < lambda`

would imply exponential largest-cell tails and hence the anti-diagonal weak limit for uniform 1324 avoiders. The proof correctly derives the subcritical resolvent condition from the Hilbert–Schmidt margin; it does not leave that condition as a second independent hypothesis.

The displayed strict growth inequality has not been established. This acceptance proves neither an unconditional largest-cell estimate nor the 1324 limit, and does not close the universal target. Finite squared-kernel data are diagnostic only.

## 1. Size normalization and margin

For the nonempty state space C = Av(213) minus the empty permutation, set `e_A=z^(|A|/2)` and `B_AC=z^((|A|+|C|)/2)K(A,C)`. Then

`e_(A_0) B_(A_0,A_1) ... B_(A_(q-1),A_q) e_(A_q)`

is exactly `z^(sum_i |A_i|) product_i K(A_i,A_(i+1))`. Consequently the scalar path series counts the actual canonical state paths, without missing endpoint factors or changing the uniform counting law. The matrix is directed and is not assumed self-adjoint.

Its squared Hilbert–Schmidt norm is exactly the ordinary square sum defining S_n, not a two-cycle sum. The known exact entries `K(I_k,J_m)=binom(k+m-1,k-1)-1`, with balanced positive k,m, imply beta >= 4 by the central binomial exponential rate. Thus beta < lambda permits `rho < R < min(1/beta,1/4)` and a single `1 < u < R/rho`. The series at R converges by its root-test radius. All boundary vectors needed below belong to ell^2 because the state enumeration is Catalan and R < 1/4.

## 2. Positive spectral comparison

For nonnegative bounded matrices on ell^2, coordinatewise domination gives domination of all powers. Moreover `|Tx| <= T|x|`, so the operator norm can be computed on nonnegative vectors and is monotone under that domination. The spectral-radius formula therefore implies `r(T) >= c r(U)` whenever `T >= cU >= 0`.

Since both cell sizes are at least one, for `0 < z < z' < rho` one has `B(z') >= (z'/z)B(z)`. This exponent and strict scaling factor are correct. In particular, a hypothetical `r(B(z)) >= 1` yields `r(B(z')) > 1`.

## 3. Compact approximation and the scalar contradiction

At z', the Hilbert–Schmidt margin makes B(z') compact. Finite principal truncations converge in Hilbert–Schmidt norm, hence operator norm, by the tail of the convergent squared-entry sum.

The proof uses only persistence of a nonzero isolated compact eigenvalue, not an unsupported general continuity claim for spectral radius. An eigenvalue of modulus greater than one has an isolating contour wholly outside the unit disk. Norm convergence of the operators and a Neumann-series resolvent estimate give uniform resolvent convergence on this contour. The resulting Riesz projections converge to the nonzero limiting projection, so eventually the finite truncation has an eigenvalue inside that contour.

For such a finite nonnegative truncation T_N, every coordinate of e_N is positive. If d is their minimum, then for every q,

`e_N^T T_N^q e_N >= d^2 sum_ij (T_N^q)_ij >= d^2 ||T_N^q||_(ell^2 to ell^2)`.

The last inequality follows by inserting the Frobenius norm. If its spectral radius exceeds one, the scalar series diverges. But its exact size-normalized interpretation counts only canonical paths whose states belong to the truncation, so its sum is at most `F(z')-1`, which is finite. This contradiction proves `r(B(z)) < 1` throughout the subcritical interval. No irreducibility, infinite-dimensional Perron theorem, or eigenvector at rho is needed.

## 4. Weighted domains and coefficient extraction

The subcritical Neumann series now converge in operator norm. Their applications to e are ell^2 vectors f and g with the exact nonnegative path coordinates claimed in the transfer note; the transpose has the same spectral radius.

For the diagonal multiplier `D_u(A,A)=u^(|A|/2)`, both matrices `D_u B` and `D_u B^T` are Hilbert–Schmidt: each squared entry is bounded by its corresponding summand at uz, and uz < R. Also `D_u e` belongs to ell^2.

There is no need to assume D_u bounded. Interpret `f=e+Bf` coordinatewise and form the ell^2 vector `D_u e + (D_u B)f`. Its coordinates are exactly `u^(|A|/2) f_A`; hence f lies in the domain of D_u. The same argument applies to g. This justifies the stated smoothing step without applying an unbounded operator outside its domain. Cauchy–Schwarz then gives `H(z,u) < infinity` for the same fixed u > 1 and every z < rho.

Finally, for fixed epsilon > 0, choose `z=rho*u^(-epsilon/2)`. Nonnegative coefficient extraction and `log a_n = n log lambda + o(n)` give the exponential upper rate `-(epsilon/2)log u`. Constants at this fixed z may depend on epsilon; uniform boundedness as z increases to rho is unnecessary. The previously accepted deterministic bound `d_BL(mu_pi,anti) <= 3 max_cell_size/n` transfers the result to the weak limit, conditional on the unproved margin.

## Source and dependency check

I independently opened both primary spectral sources and inspected the retained pages. Nonnenmacher's Theorem 5.1.9 describes the nonzero compact spectrum; Demkowicz's Theorem 1.4 and Lemma 1.12 supply the Riesz decomposition and finite algebraic multiplicity facts. The cited page numbers and retained PDF hashes match `SPECTRAL_SOURCE_PINS.json`. These supply standard spectral background, not the new conditional combinatorial implication.

- [Nonnenmacher, Introduction to Spectral Theory, Fall 2022, printed pp. 67–68](https://www.imo.universite-paris-saclay.fr/~stephane.nonnenmacher/enseign/Spectral%20Theory%202022%20chap1-6.pdf#page=68)
- [Demkowicz, Lecture Notes on Non-Self Adjoint Operators and Related Topics, Theorem 1.4 and Lemma 1.12](https://oden.utexas.edu/media/pending_reports/book.pdf#page=12)

The accepted encoding is pinned at `dfbab3a20d05861a7c4aba868b89a225f2ac5db201a467358f015f6efabe2b03`; its independent geometry audit is pinned at `a7b8cbfc9809ea36aafa324fac985c826e6f93457ea36d0f24a245bd6e676161`. The staircase geometry report is pinned at `b2a215ce3c6b6b3f711b9976489d8cd0ff5be19cc8d097f3a367e15fced82303`. All earlier acceptance files and receipts remain unchanged.
