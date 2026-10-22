# Independent arithmetic and scope audit

Audit date: 2026-10-21. Target: AIM Problem 5.1, Problem ID 20000691. This audit does not certify a new solution or an all-moment asymptotic.

## Independently verified mathematics

1. For a fixed finite set of odd primes in either sign of the full fundamental-discriminant family, the local character has probabilities P(0)=1/(p+1) and P(+1)=P(-1)=p/(2(p+1)). Squarefree progression counts and CRT give limiting independence. Positive fundamental discriminants of size at most X have odd density 2/pi² and even density 1/pi². The odd classes 1 and 5 modulo 8 split equally, so the three values at 2 each have probability 1/3. Negative discriminants have the same probabilities. These are limiting finite-dimensional distributions, not a central-point Euler-product averaging theorem.
2. For z_j=p^(-1/2-alpha_j), the expected local product is 1/(p+1)+p/(2(p+1))*[product_j(1-z_j)^(-1)+product_j(1+z_j)^(-1)]. Its degree-two terms are sum_(i<=j) z_i z_j up to the factor p/(p+1). Extraction of all K=k(k+1)/2 full-zeta factors leaves a product convergent absolutely and locally uniformly when |Re alpha_j|<=delta<1/4. This establishes the arithmetic-factor continuation only.
3. In the chi_(8d) family, d positive odd squarefree, the density in the d variable is 4/pi² and the p=2 expectation is 1. With identical full-zeta extraction and densities omitted, A_full/A_8=E_2. At zero shifts this ratio is 5/3, 13/3, 41/3 for k=1,2,3. It is not a full-moment ratio. Conductor scaling 8d, logarithms, gamma parity, and density must be transferred separately.
4. For the all-integer square diagonal, the Dirichlet series factors as zeta(s)^K A_k(s), with the latter product absolutely convergent for Re s>1/2. Its local second coefficient at s=1 is binom(k+3,4)-K(K+3)/2, giving -1,-4,-12,-30 for k=1,2,3,4. This does not evaluate the nonsquare terms in a moment. Restricting m to odd integers changes the arithmetic constant.
5. The functional equation for positive conductor 8d supplies d^(-alpha)g(alpha), where g(alpha)=(pi/8)^alpha Gamma(1/4-alpha/2)/Gamma(1/4+alpha/2). A swapped subset J therefore gives X^(1-sum_J alpha) fhat(1-sum_J alpha) product_J g(alpha) T(beta). The minus signs of the swapped shifts and the Mellin argument are essential. For k=1 and T(alpha)=C/(2alpha)+D+O(alpha), coalescence gives X{C/2[fhat(1)log X+fhat'(1)-g'(0)fhat(1)]+2D fhat(1)}. Replacing the shifted Mellin factor by fhat(1) loses XC fhat'(1)/2.
6. A nonsquare dual frequency need not vanish termwise: the ordinary quadratic Gauss sum modulo 3 at frequency 2 equals -i sqrt(3). Square-frequency pole extraction is an analytic organization, not a termwise support assertion.

## Poisson and theorem-scope restrictions

A schematic Poisson formula is not an exact identity with unspecified conventions. Conrey–Rodgers Lemma 2 explicitly requires odd modulus, the factor (2/m), the sign (-1)^r, a squarefree sieve variable c, and transform argument rD/(2c²m). In the chi_(8d) application (8/m) cancels (2/m). Its zero-frequency value is phi(m) on squares and zero otherwise. Nonzero square frequencies account for one-swap residues only after the contour shifts, Euler-product identities, and gamma-factor comparison proved in that paper.

Conrey–Rodgers Theorem 1 assumes quadratic Lindelöf and gives error O(N^(1/4)D^(1/2+epsilon)ell^(1/4+epsilon)). For fixed twist ell and N=D^eta, eta<2 permits a power saving; eta=2 does not. Their Proposition 1 suppresses j-swaps for eta<j, but does not prove that every predicted higher swap occurs for eta>=j. Their Section 5 identities do not supply missing uniform analytic estimates.

Čech v3 Corollary 1.7 is unconditional for k<=4, conditional on GLH in general, for the specified untwisted long polynomials. Remark 1.4 expressly excludes continuation sufficient for central k>=4 or two-swap detection. Corollary 1.5 treats the first three central moments with power saving, not all central moments. Its fixed-shift theorem should not silently become uniform in moving shifts.

The natural product-AFE scale D^(k/2) explains why k=3 is the first integer strictly inside 1<eta<2. Substitution of that scale is not itself a rigorous transfer from the fixed-weight long-polynomial theorem: conductor-dependent weights, gamma factors, both AFE pieces, tails, collision limits, and uniform estimates remain necessary.

Principal shifted averaging poles coalesce at w=1 and produce the X-scale polynomial. The cubic w=3/4 pole produces a distinct X^(3/4) term. Shen–Stucky's O(X(log X)^(6+epsilon)) fourth-moment remainder resolves degrees 10 through 7, not the full degree-ten polynomial with o(X) remainder. Neither local arithmetic nor zero/one-swap theorems certify the general high-moment analytic remainder or novel completion of the AIM heuristic task.

## Primary sources inspected

- Conrey–Rodgers, https://arxiv.org/html/2208.01783v2 : Theorem 1, Proposition 1, Lemma 2, Sections 4–5.
- Čech v3, https://arxiv.org/html/2402.07473v3 : principal shifted recipe, Remark 1.4, Corollaries 1.5 and 1.7.
- The fourth-moment and cubic-secondary distinctions were preserved; this audit does not independently reprove those external theorems.

## Acceptance boundary

The underlying mathematical report was independently accepted as partial/expository only. This portable edition removes coordination wording without changing mathematical sections. Its byte integrity and finite checks are tested separately by verify_package.py. Neither the original review nor the executable checks certify novelty, an all-k moment theorem, or analytic estimates beyond the stated elementary proofs.
