# Five-avenue audit of the PF-infinity proof-simplification problem

## Verdict and scope

**Not solved.** The requested object is a genuinely more straightforward proof of the infinite Toeplitz classification. Below are rigorous elementary pieces and a reconstruction of a known representation-theoretic route. They are useful for identifying the exact bottleneck, but do not establish a new simplification. In particular, the 2022 source explicitly asks about Okounkov's existing proof, so repackaging that route cannot be counted as resolving the problem.

Write h_n=0 for n<0 and T(h)=(h_{j-i})_{i,j>=0}. PF-infinity means every finite minor is nonnegative. For h_0=1 the classification is

H(z)=exp(gamma z) product_i(1+alpha_i z)/product_i(1-beta_i z),

with gamma, alpha_i, beta_i nonnegative and sum_i(alpha_i+beta_i)<infinity. General nonzero sequences additionally have a positive scalar and an initial z^m factor. The zero sequence is separate. These conventions avoid the ambiguity of a quotient whose numerator and denominator both vanish at zero.

## Avenue 1. Direct sufficiency: complete elementary proof

1. The upper bidiagonal Toeplitz matrix of 1+alpha z is totally nonnegative. In each minor, the only potentially nonzero matching is order-preserving: a crossing would require an earlier row to use its superdiagonal while a later row uses a column strictly to its left, which is impossible with distinct columns. Thus each minor is either zero or a nonnegative monomial.
2. For beta>0, the Toeplitz matrix of (1-beta z)^(-1) is diagonally equivalent to U_ij=1_{j>=i}. Every minor of U is zero or one. Indeed rows restricted to selected columns are nested suffix indicator vectors; successive row subtraction gives disjoint intervals, and a nonzero square determinant then requires one pivot in each interval, in increasing order. For beta=0 the matrix is the identity.
3. T(H_1 H_2)=T(H_1)T(H_2). Each relevant Cauchy–Binet sum is finite, because intermediate indices lie between the smallest selected row and largest selected column. Products preserve total nonnegativity.
4. exp(gamma z)=lim_N(1+gamma z/N)^N coefficientwise. A fixed minor is a polynomial in finitely many coefficients, so coefficientwise limits preserve total nonnegativity.
5. Summability of alpha_i and beta_i gives locally uniform convergence of numerator products everywhere, and of reciprocal denominator products on a sufficiently small disk about zero. The finite products converge coefficientwise. Another application of step4 finishes the infinite product.

Nothing in this direction supplies necessity. A planar-network drawing is an alternative proof of steps1–3, not a proof of the hard direction.

## Avenue 2. Factor peeling and rational necessity

Here are the precise useful reductions. These are classical mechanisms, not claimed as novel.

### A. Elementary reciprocal closure

If H(0)=1 and T(H) is totally nonnegative, then T(1/H(-z)) is too. On a finite leading principal block T_N, the inverse is the corresponding block of T(1/H). Jacobi's complementary-minor identity, together with det(T_N)=1, gives its inverse minors signs (-1)^(sum rows+sum columns). Conjugating by diag(1,-1,1,-1,...) cancels these signs. Any desired finite minor fits in some T_N. This is an exact closure property, not a classification import.

### B. Ratio and peeling lemma

If h_n has infinite support, all h_n>0. To see the no-gap assertion, the minor on rows0,k and columns k,k+1 is h_k h_1-h_{k+1}; a first zero therefore forces the next zero, and induction applies. The adjacent minors give h_n^2>=h_{n-1}h_{n+1}. Consequently h_{n+1}/h_n decreases to b>=0, and the radius of H is 1/b (infinity if b=0).

**Peeling claim:** (1-bz)H(z) is PF-infinity. A convenient proof uses two standard finite symmetric-function identities, not Edrei:
- Jacobi–Trudi: s_lambda(h)=det(h_{lambda_i-i+j});
- each skew Schur function is a nonnegative integer combination of ordinary Schur functions (Littlewood–Richardson).

Every Toeplitz minor is a skew Schur specialization or is forced to vanish; conversely every ordinary Schur determinant is a Toeplitz minor: use rows i-lambda_i+M and columns j+M, with M large enough to make all indices nonnegative. Thus PF-infinity is equivalent to nonnegativity of all s_lambda(h).

For N>=lambda_1, expand s_(N,lambda)(h)/h_N using Jacobi–Trudi. Its first row converges to (1,b,b^2,...). Subtract b times each previous column, from right to left, and expand along that first row. The limit is s_lambda(h'), where h'_n=h_n-bh_{n-1}. Thus every s_lambda(h')>=0. The skew-Schur expansion yields all Toeplitz minors of h' nonnegative. The first coefficient drops from h_1 to h_1-b.

This explicitly records the external algebraic ingredient: a proof claiming to be purely elementary must also prove or deliberately admit the skew-Schur positivity implication. Stating only that coefficient differences are nonnegative is insufficient.

### C. Iteration and rational case

Iterate while the ratio limit b is positive. The extracted b_i are nonincreasing because h'_n<=h_n gives a nondecreasing convergence radius; their sum is bounded by the original h_1. At a finite stopping point the residual is entire. At an infinite stopping point b_i tends to zero, and the coefficientwise residual is also entire. Here is a direct justification: the residual coefficients decrease at every step and remain nonnegative. Their limits are coefficientwise bounded by each H_N, whose radius is 1/b_(N+1). These radii tend to infinity, so the limit is entire. It is PF-infinity by coefficientwise closedness. Summability ensures the product identity H_infinity=H product_i(1-b_i z) near zero.

For rational H, positivity of coefficients and Pringsheim's theorem place a singularity at its finite positive convergence radius. It is a pole; multiplication by 1-bz removes one order. Only finitely many poles can be removed, leaving a PF-infinity polynomial. Apply reciprocal closure and the same rational argument to 1/H_entire(-z). Its poles must all be positive, so all zeros of the polynomial are negative. Thus rational necessity follows from peeling, finite symmetric-function positivity, and Pringsheim, without the full Edrei classification.

This is a complete rational subcase, conditional only on the named standard identities/theorem, not on an equivalent infinite classification. It cannot decide the general zero-free entire remainder.

## Avenue 3. Approximation proposals and exact failures

### Taylor truncation fails

The geometric sequence h_n=1 is PF-infinity. Truncating at degree2 gives (1,1,1,0,...). Its minor on rows(0,1,2), columns(1,2,3) is

[[1,1,0],[1,1,1],[0,1,1]], determinant -1.

Thus the finite real-rooted-polynomial theorem does not apply to Taylor truncations of a general PF-infinity function.

### Arbitrary PF-polynomial approximation also fails for pole-bearing targets

A normalized polynomial with nonpositive real zeros has h_1=sum alpha_i and h_2=sum_(i<j)alpha_i alpha_j<=h_1^2/2. This inequality persists under coefficientwise convergence. But 1/(1-z) has h_1=h_2=1. Therefore it cannot even be approximated coefficientwise by normalized PF-infinity polynomials. This stronger obstruction rules out repairing Taylor truncation by choosing unspecified real-rooted approximants.

### Rational approximants require a genuine density theorem

Finite truncations of the *canonical product*, once available, do approximate H. However using this to prove existence of the canonical product is circular. Finite-dimensional total-nonnegative matrix factorizations do not automatically give rational Toeplitz approximants: their elementary factors generally do not remain Toeplitz. A valid proof would need to establish this extra structured approximation step independently.

### Coefficientwise closure has only one direction

Limits of PF-infinity sequences are PF-infinity. It does not follow that every PF-infinity sequence is a limit of the desired smaller subclass. The preceding h_2 inequality gives an explicit failure for the polynomial subclass.

## Avenue 4. Known symmetric-function / moment / canonical-product route

This avenue can finish the mathematical classification, but it reconstructs known reasoning, especially Okounkov1998 section2.4. It is not a new answer to the 2022 request. The useful distinction is that it need not import Edrei or Thoma as a black box.

After first peeling, call the entire PF-infinity residual A. Apply reciprocal closure to B(z)=1/A(-z), then peel B to an entire PF-infinity residual R, with Q(z)=product_j(1-beta_j z) and R=BQ near zero. The entire identity A(-z)R(z)=Q(z) follows by analytic continuation. If R(w)=0 then Q(w)=0, so w=1/beta_j is positive. But R has nonnegative coefficients and R(0)=1, making R(w)>0 for every positive real w. This contradiction proves R zero-free. Consequently A(z)=product_j(1+beta_j z)/R(-z). The sum of first-stage and second-stage parameters is bounded by the original h_1: the first stage subtracts its parameter sum from h_1, reciprocal closure preserves that residual first coefficient, and the second stage subtracts its own sum. Only the assertion R(z)=exp(gamma z) remains. This identity argument does not require Pringsheim for the infinite reduction; Pringsheim was only an optional convenience in the rational discussion.

One can expose the non-classification ingredients behind this last assertion as follows. If R'(0)=c>0, replace z by z/c, so h_1=1. Define p_k formally by

log R(z)=sum_(k>=1) p_k z^k/k.

Finite symmetric-group character theory gives a central positive-definite function on S_n:

chi_n(sigma)=product_(cycles C of sigma) p_|C|.

Indeed the Frobenius character formula expands it as sum_(lambda partitions n) s_lambda(h) chi^lambda(sigma). All coefficients are nonnegative, and chi_n(identity)=p_1^n=1. Equivalently, it is a convex combination of normalized irreducible characters with weights dim(lambda)s_lambda(h), whose sum is1. Compatibility under adjoining fixed points follows from p_1=1. This uses finite-group character theory and Frobenius' identity, not the classification of characters of S_infinity.

Here is a finite-dimensional derivation of the moment measure. In the group algebra of S_(n+1), put X_n=(1/n)sum_(i=1)^n(i,n+1). In any unitary representation X_n is self-adjoint of norm at most1. The normalized positive-definite character state therefore gives a probability spectral measure mu_n on [-1,1]. For each fixed k>=1, the fraction of ordered k-tuples of distinct indices in the expansion of X_n^k tends to1. Their transposition product is a (k+1)-cycle, hence their character value is p_(k+1). Repeated-index terms have character absolute value at most1 and total relative weight tending to0. More precisely the moment error is at most 2[1-(n)_k/n^k]<=k(k-1)/n for n>=k, where (n)_k is the falling factorial. Consequently

integral t^k dmu_n(t) -> p_(k+1).

By compactness of probability measures on [-1,1], some weak limit mu satisfies p_(k+1)=integral t^k dmu(t), including k=0 because p_1=1.

Since R is entire and zero-free, R'/R=sum_(k>=1)p_k z^(k-1) is entire. If mu has positive mass delta outside [-epsilon,epsilon], then

p_(2k+1)=integral t^(2k)dmu(t)>=delta epsilon^(2k),

contradicting infinite radius of that series. Therefore mu is the mass at0, p_k=0 for k>=2, and R=exp(z). Undo normalization to get exp(cz). If c=0, log-concavity already gives R=1.

This is a transparent proof architecture with no equivalent-classification black box, but its imports are substantial: finite character/Frobenius identities, Littlewood–Richardson positivity, finite spectral theorem, measure compactness, and elementary complex analysis (with Pringsheim additionally used in the rational subcase as presented). Establishing those prerequisites is not the same as discovering a new elementary replacement. The spectral/moment core is already exactly the kind of method discussed by the source's Okounkov comparison.

## Avenue 5. Additional exact shortcut counterexamples

- Nonnegative coefficients alone do not eliminate a nonlinear zero-free exponential: exp(z^2) is entire, zero-free, and coefficientwise nonnegative, but its Toeplitz minor on rows(0,1), columns(1,2) is [[0,1],[1,0]], determinant -1.
- Log-concavity alone is too weak: (1,1,1,0,...) is nonnegative, has interval support, and satisfies every adjacent log-concavity inequality, yet the displayed 3x3 minor is negative. Therefore using only coefficient ratios cannot complete the proof.
- The numerator/denominator summability is not cosmetic. Without it, finite-factor approximations need not converge to an analytic function around zero. In normalized form the extracted parameter sum is controlled by h_1; that bound must be proved before using an infinite product.
- Replacing the final zero-free step by the assertion that a zero-free entire function with nonnegative coefficients is exponential-linear is false, as exp(z^2) shows. The missing condition is precisely the full PF-infinity structure, used through the positive moment representation above.

## Imported facts versus deductions in this report

Imported known identities/results: finite Jacobi–Trudi and Littlewood–Richardson positivity; finite Frobenius character formula; finite spectral theorem; compactness of probability measures on a compact interval; Pringsheim; classical factor-peeling/Okounkov architecture. Explicit derivations here: Cauchy–Binet sufficiency, complementary-minor reciprocal closure, bordered-Schur peeling calculation, analytic limit justification, elementary finite-star-transposition moment extraction, the independent auditor’s entire-identity zero-free argument, and exact counterexamples. These derivations are explanatory reconstructions and are not asserted to be historically new.

Unproved research goal: an independently justified simplification of the infinite necessity direction that improves on the comparison proofs already identified by the 2022 source. No such improvement is established.

## Sources and provenance boundaries

1. Dyachenko–Sokal, Oberwolfach Report13/2022, pp661–662, DOI10.4171/OWR/2022/13. Original question and explicit Okounkov comparison. Official PDF: https://ems.press/content/serial-article-files/46952?nt=1 . Retrieval hashes are recorded in SOURCE_METADATA.json.
2. A. Okounkov, On the representations of the infinite symmetric group, arXiv:math/9803037, especially section2.4 pp28–31: https://arxiv.org/abs/math/9803037 . Directly inspected locally, not merely inferred from search snippets.
3. A. Edrei, Proof of a conjecture of Schoenberg on the generating function of a totally positive sequence, Canadian J.Math.5 (1953),86–94, https://doi.org/10.4153/CJM-1953-010-3 . Original classification source; not used as a proof black box here.
4. K. Rietsch, Totally positive Toeplitz matrices: classical and modern, https://arxiv.org/abs/2509.25163 . Contemporary context only. Any formulation proved using Edrei is circular as a replacement proof and is not imported here.

No third-party source text, dataset contents, or private coordination is needed in a public mathematical attempt record. This report's mathematical exposition is authored reconstruction, not a copied source document.
