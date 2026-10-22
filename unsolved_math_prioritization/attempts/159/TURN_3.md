# Turn 3: an outer-reflection criterion and a failed symmetrization

Original conjecture unresolved. This turn tests whether the known palindromic-product result can be localized and then extended to arbitrary products. The inward coefficient argument is adapted, with credit, from the classical palindromic case and the explicit presentation at TheSil/palindromic_zero_one_polynomials. The Lean project was read as mathematical source, not installed or run. No new priority claim is made.

## 1. Only a short outer reflection window is sufficient

Let C=AB be an admissible normalized factorization as in Turn 1, with degrees 1≤m=deg A≤n=deg B. Equal positive degrees are already impossible. Suppose

c_k = c_(m+n−k) for 0≤k≤floor(m/2).

Then A is a palindromic Boolean polynomial and B is Boolean. B need not be palindromic unless C is palindromic throughout.

Here is the coefficient proof, with the limited reflection hypothesis explicit. The unit corners in c_m and c_n force

a_i b_(m−i)=0 and a_i b_(n−i)=0 for 1≤i≤m−1.

Prove successively, for k≤floor(m/2), that a_k=a_(m−k), b_k=b_(n−k), and these four coefficients are Boolean. The endpoint case is Turn 1. At the next k, earlier reflected terms match in the two convolution coefficients. Their common cross-sum T is an integer. Hence the two boundary sums satisfy

a_k+b_k = a_(m−k)+b_(n−k) = t, with t∈{0,1}.

Also a_k b_(n−k)=0 and a_(m−k)b_k=0 by the corner constraints. If t=0, all four vanish. If t=1, either a_k>0, forcing b_(n−k)=0, a_(m−k)=1, b_k=0 and a_k=1, or a_k=0, which forces b_k=b_(n−k)=1 and a_(m−k)=0. This completes the inward step. The reflected halves cover A. Since A is integral and monic, division of C by A makes B integral; its [0,1] bounds make it Boolean.

The proof uses only the stated outer reflection coefficients, not symmetry of C at all indices. There is no proof-method restriction in this target; the coefficient induction here is legitimate. 

## 2. Consequences and boundary checks

If an unfair factorization exists with smaller degree m, some product coefficient c_k must differ from c_(m+n−k) at a distance 1≤k≤floor(m/2). Therefore the first asymmetry from the product's ends bounds the smaller factor degree from below: if reflection holds through distance r, any unfair factorization must have smaller degree at least 2r+2.

This is an all-degree criterion. It extends the *hypothesis used by this argument* beyond fully palindromic products; no claim of novel literature priority is made. For example, A=1+x² and B=1+x⁵+x¹¹ give a Boolean nonpalindromic product, but its first and last nonconstant coefficients both vanish, so the window criterion applies. This example also shows why the conclusion must not assert that B is palindromic.

The case m=1 needs no reflection beyond the endpoints: A=1+x is already Boolean. Degree-zero factors are handled separately as in Turn 1. For full palindromicity, after A and B are Boolean and A is palindromic, cancellation in AB=A*B* additionally makes B palindromic, recovering the credited known theorem.

## 3. Why reflection does not reduce the full problem to this case

Two natural symmetrizations fail for distinct reasons.

Multiplication: C C* is palindromic, but its middle coefficient is the sum of the squares of the coefficients of C, namely the number of nonzero coefficients. For a nonconstant normalized C that is at least 2, so this product is not Boolean.

Disjoint reflected padding: for L>deg C, D=C+x^L C* is a palindromic Boolean polynomial. However an original factor A need not divide D, so the known theorem for D cannot be applied to the original factorization. This failure already occurs for the fair example C=A=1+x+x³, B=1. Its reciprocal is 1+x²+x³. These distinct monic polynomials have the same degree, so A does not divide C*. Since A(0)=1, A is coprime to x, and therefore A does not divide C+x^L C* for any L.

Even when divisibility happens in a special example, nonnegativity of the new quotient would still have to be established. No padding or multiplication construction here preserves all necessary hypotheses for an arbitrary unfair factorization.

## 4. Remaining gap

The outer-reflection criterion covers an infinite family of products but leaves asymmetric boundaries. The general conjecture cannot be inferred from the bounded support scan in Turn 2 or by either symmetrization above. The next turn will inspect exact algebraic certificates for a residual asymmetric coefficient pattern rather than claiming that symmetry is without loss of generality.
