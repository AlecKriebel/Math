# Quadratic Dirichlet moments: five-route mathematical audit

Date: 2026-10-21. Problem ID 20000691. Status: **partial/expository; no new solution or novelty accepted**. This report studies the original AIM heuristic question, not an artificially strengthened all-k asymptotic theorem. It compares elementary calculations with the cited primary sources. The original question imposes no particular sign, family, cutoff, shifts or error bound.

## Executive finding

The elementary local laws, full-zeta arithmetic factor and prime-2 ratio are correct under their stated finite-prime/zero-swap interpretation. They do not solve the high-moment problem. Length substitution alone is not a rigorous reduction to Conrey–Rodgers and does not prove the threshold. We give exact square-diagonal results and a smoothing counterexample below; neither is a novel full-moment theorem.

The mechanism supported in the long-polynomial range is: zero Poisson frequency gives the square diagonal, and residues from nonzero square frequencies furnish one-swaps. The product-AFE scale D^(k/2) first enters the open interval (D,D²) at k=3. This is a structural explanation, not an all-k proof or a proof of two-swaps. The cubic X^(3/4) residue is a different, smaller scale.

## 1. Finite-prime density and arithmetic route

**Question attempted:** Can independent local laws determine the required moment, and is prime 2 correct?

### Proved finite-prime statement

For either sign of fundamental discriminants Δ with |Δ|≤X, each fixed finite collection (χ_Δ(p)) converges in distribution to independent Y_p with

P(Y_p=0)=1/(p+1),  P(Y_p=+1)=P(Y_p=-1)=p/[2(p+1)].

Here p=2 is included. For χ_(8d), d positive odd squarefree, the same odd-prime law holds but Y_2=0 identically.

**Proof details.** At an odd prime, among the p²−1 residues modulo p² not divisible by p², there are p−1 residues divisible by p and p(p−1)/2 residues of each nonzero quadratic-symbol sign. The ratios are exactly those displayed. For any fixed modulus, insertion of μ²(n)=Σ_(c²|n)μ(c), counting progressions for c≤√X, and estimating the omitted density tail gives the squarefree local densities with O_q(√X) discrepancy. CRT multiplies the finitely many local densities. The conductor restrictions defining fundamental discriminants are imposed modulo a power of 2 and are independent of these fixed odd-prime congruences.

For positive discriminants, odd Δ arise from positive squarefree n≡1 mod4. They have density 2/π² among positive integers. Even Δ=4m arise from squarefree m≡2,3 mod4 with m≤X/4, and have combined density 1/π² in conductor. The odd classes 1 and 5 mod8 have equal density 1/π², hence χ_Δ(2)=+1 and −1 each have density 1/π²; even Δ give zero with that same density. Negative discriminants give the same answer, with the underlying squarefree residue classes permuted. CRT with the odd-prime restrictions proves independence including 2. Omitting the exceptional trivial conductor changes no limit.

Consequently, for a fixed finite set S and |z_(j,p)|<1, the mean of Π_(p∈S,j)(1−χ_Δ(p)z_(j,p))^−1 tends to Π_(p∈S)E_p, where

E_p(z)=1/(p+1)+p/[2(p+1)]{Π_j(1−z_j)^−1+Π_j(1+z_j)^−1}.

No passage S→all primes depending on X is claimed.

### Proved factorization, not a central Euler-product average

Put z_j=p^(−1/2−α_j), K=k(k+1)/2. Initially Re α_j>0,

Π_p E_p = A_full(α) Π_(i≤j) ζ(1+α_i+α_j).

After multiplying each E_p by Π_(i≤j)(1−p^(−1−α_i−α_j)), the local remainder is 1+O_(k,δ)(p^(−2+4δ)), uniformly on compact sets |Re α_j|≤δ<1/4. The even-degree expansion proves this: the degree-two terms are Σ_(i≤j)z_i z_j; their coefficient differs from 1 by O(1/p); every remaining term has degree at least four. Thus A_full is an absolutely locally uniformly convergent product in that strip. This is a meromorphic continuation of a Dirichlet-series Euler product, not permission to average an infinite Euler product for central L-values.

The chi8 arithmetic function A8 uses the same odd-prime factors and the p=2 factor Π_(i≤j)(1−2^(−1−α_i−α_j)) when extracting full zeta functions. Therefore the identity of meromorphic arithmetic factors is

A_full(α)=E_2(α) A8(α).

At α=0,

E_2=1/3+[(1−1/√2)^−k+(1+1/√2)^−k]/3.

For k=1,2,3,4 its values are 5/3,13/3,41/3,137/3. This is the ratio A_full/A8, NOT its reciprocal. If ζ_2 rather than ζ is extracted, change the convention first.

**Failed extension.** Finite-prime independence gives no uniform truncation, no approximate functional equation, no off-diagonal control, and no all-k moment. Arithmetic-factor transfer alone does not transfer density, parity, conductor normalization, or a moment polynomial. Even at k=0, conductor counts distinguish full positive density 3/π² from the chi8 subfamily density 1/(2π²), a factor 6 invisible in a local Euler expectation.

## 2. Square-diagonal Dirichlet-series route

**Question attempted:** Can one rigorously extract the degree without proving a central moment?

Fix an integer k≥1. Define b_k(m)=d_k(m²)Π_(p|m)p/(p+1), and, for Re s>1,

Z_k(s)=Σ_m b_k(m)m^−s = ζ(s)^K B_k(s),

B_k(s)=Π_p (1−p^−s)^K [1+p/(p+1) Σ_(a≥1) binom(2a+k−1,k−1)p^(−as)].

The bracket's first coefficient is Kp/(p+1). After extraction the local factor is 1+O_k(p^(−2σ)+p^(−1−σ)) on compact subsets σ=Re s>1/2. Hence the Dirichlet-series coefficients β(n) of B_k satisfy Σ|β(n)|n^−σ<∞ for every σ>1/2. Also B_k(1)>0: every local factor is positive and the sum of their deviations from 1 converges. Thus Z_k has an exact pole of order K at 1.

### Elementary rigorous partial result

As M→∞,

Σ_(m≤M) b_k(m)/m = B_k(1)(log M)^K/K! + O_k((1+log M)^(K−1)).

**Proof.** The identity Z_k=ζ^K B_k implies b_k=d_K*β by absolute convergence. Elementary harmonic-sum induction gives

H_K(y):=Σ_(n≤y)d_K(n)/n = (log y)^K/K!+O_K((1+log y)^(K−1)), y≥1.

Indeed H_1(y)=log y+O(1), and H_(K+1)(y)=Σ_(a≤y)H_K(y/a)/a; comparison with the integral of (log(y/t))^K/t yields the next term and O((1+log y)^K) error. Consequently the target sum is Σ_(r≤M)β(r)H_K(M/r)/r. Absolute convergence at σ<1 controls Σ|β(r)|(1+log r)^K/r. Expanding (log M−log r)^K gives the leading term B_k(1)(log M)^K; every other term is O((1+log M)^(K−1)). The tail r>M is O(M^(−(1−σ))) in the weighted β sum, so does not alter that estimate. This proves the claim, including K=1.

For chi8, restrict m to odd integers and replace B_k by

B8_k(s)=(1−2^−s)^K Π_(p odd) (1−p^−s)^K [1+p/(p+1)Σ_(a≥1)binom(2a+k−1,k−1)p^(−as)].

The same proof applies. B_full(1)/B8(1)=E_2. The local p^−2 coefficient at s=1 is binom(k+3,4)−K(K+3)/2, giving −1,−4,−12,−30 for k≤4, independently verified by expansion.

**Failed extension.** This exact diagonal harmonic sum has no discriminant averaging and does not account for conductor-dependent AFE weights or nonzero Poisson frequencies. Its degree K is consistent with symplectic moments but cannot certify their leading coefficient. In particular substituting M≈D^(k/4) into this identity is not an evaluation of the k-th moment.

## 3. Quadratic Poisson and long-polynomial route

**Question attempted:** Do nonzero frequencies rigorously supply the missing principal terms, and where does k=3 arise?

To make the Poisson normalization explicit, fix odd m>0, smooth Ψ of compact support in (0,∞), D>0 and finite Y. With the normalized real Gauss factors G_r(m) of Conrey–Rodgers Lemma 2, and Ψ~(v)=∫Ψ(u)[cos(2πvu)+sin(2πvu)]du, the exact truncated-sieve identity is

Σ_(d odd) Σ_(c²|d,c≤Y) μ(c) Ψ(d/D) (d/m)
= D(2/m)/(2m) Σ_(c≤Y,(c,2m)=1) μ(c)/c² Σ_(r∈Z)(−1)^r G_r(m) Ψ~(rD/(2c²m)).

The left d-sum is over positive odd d (equivalently all odd integers after extending Ψ by zero). Crucially: this is not the full squarefree restriction until the sieve tail is justified. In chi8 averages multiplication by (8/m) cancels (2/m), since m is odd. For a twist m=nℓ one must retain ℓ throughout, and only odd nℓ survive.

G_0(m)=φ(m) for square m and zero otherwise. At an odd prime p not dividing r, G_r(p)=(r/p)√p. Thus **G_2(3)=−√3**, an exact nonsquare-frequency counterexample to termwise vanishing. The ordinary complex Gauss sum at the same parameters is −i√3; these are different normalizations, both nonzero. Our code verifies the latter independently.

For c=1, rapid transform decay suggests effective |r|≲m/D; in the actual sieved expression it is |r|≲c²m/D. Smoothness gives decay, not compact Fourier support or exact absence of all r≠0. Discarding c² in an asserted proof is unjustified. Nonzero square r can produce auxiliary principal-character poles, but identifying their complete residue with one-swaps needs the Euler-product and gamma identities and justified contour shifts in CR Section 5. A nonprincipal auxiliary character's absence of an individual zeta pole does not itself bound the aggregated nonsquare contribution.

**Established external theorem.** CR Theorem 1, under quadratic Lindelöf, gives the zero/one-swap formula for its smooth polynomial average with error

O(N^(1/4)D^(1/2+ε)ℓ^(1/4+ε)).

For fixed odd ℓ and N=D^η this saves a power only for η<2. CR Proposition 1 suppresses recipe j-swap integrals when η<j; it does not prove those terms become nonzero at η≥j. Čech v3 Corollary 1.7 obtains the untwisted counterpart unconditionally for k≤4, or under GLH for general k. These are polynomial averages, not arbitrary central moments.

**Threshold heuristic and failed reduction.** A product AFE has natural length D^(k/2), so k=3 is the first integer strictly inside 1<η<2. However, the product AFE has conductor-dependent gamma weights, two dual pieces and shifted prefactors. Reducing it to the fixed-cutoff polynomial theorem requires Mellin separation, uniform estimates in auxiliary Mellin variables, tails and shift coalescence; none is proved by writing N=D^(k/2). On that formal scale the error exponent is 1/2+k/8: 7/8 at k=3, 1 at k=4, 9/8 at k=5. Thus even granting the missing weight reduction does not give o(D) at k=4 or above. A rigorous reduction based on length alone is rejected. Boundary η=1 or 2 needs the actual weights. Higher swaps remain predicted, not demonstrated here.

## 4. Shifted recipe, smoothing and normalization route

**Question attempted:** Can we give an exact convention-safe prediction and test simplifications?

Choose d>0 odd squarefree, f∈C_c^∞((0,∞)), k fixed, and define fhat(z)=∫f(t)t^(z−1)dt. Write

T(β)=(4/π²)Σ_(n_1,...,n_k odd, Πn_j square) [Π_(p|Πn_j)p/(p+1)] Π_j n_j^(−1/2−β_j),

g(α)=(π/8)^α Γ(1/4−α/2)/Γ(1/4+α/2).

The series for T initially converges absolutely when Re β_j>0; its Euler factorization then continues it meromorphically. For J⊆{1,...,k}, put A_J=Σ_(j∈J)α_j and β_j=−α_j on J and α_j otherwise. The **principal conjectural** answer is

Σ_J X^(1−A_J) fhat(1−A_J) [Π_(j∈J)g(α_j)] T(β).

This is Čech v3 Conjecture 1.1 in alpha coordinates. It is a conjecture for general k, not a theorem derived in this report. The factors may have shift poles; combine the summands before α→0. Coalescence gives the predicted degree K polynomial. The actual error term remains a conjectural analytic input, not a consequence of the finite local law.

### Exact counterexample to dropping the shifted Mellin factor

Already for k=1, write the Laurent expansion T(α)=C/(2α)+D_0+O(α), with C=(4/π²)A8(0)>0. Put f_0=fhat(1), f_1=fhat'(1), g_1=g'(0). Straight Taylor expansion, with no asymptotic-number-theory assumption, gives

lim_(α→0){ f_0 T(α)+X^−α g(α)fhat(1−α)T(−α) }
= (C/2)[f_0 log X+f_1−f_0 g_1]+2D_0 f_0.

Replacing fhat(1−α) by f_0 removes C f_1/2 from this exact expression. For any nonzero nonnegative smooth bump supported in (2,3), f_1=∫f(t)log t dt>0. Restoring the exterior factor X, the lost term is **XC f_1/2**, not o(X). Thus the smoothing simplification fails even after poles cancel. This is an exact algebraic counterexample about the recipe, not a new asymptotic for a moment.

### Conductor and sign audit

For primitive real χ_Δ, root number is +1 for either sign. The gamma parity is a=0 for Δ>0 and a=1 for Δ<0. The functional-equation multiplier at 1/2+α is

(|Δ|/π)^−α Γ((1/2+a−α)/2)/Γ((1/2+a+α)/2).

Hence negative-discriminant formulas need 3/4 in place of 1/4; the even gamma factor cannot simply be reused. In conductor scale the full positive or negative family has density 3/π². The positive chi8 family has density 1/(2π²) in |Δ|, but 4/π² in d. Exactly,

Σ_(d odd squarefree) f(8d/Y)L(1/2,χ_(8d))^k = M_(k,8)(Y/8;f).

If M_(k,8)(X;f) has principal expression X P(log X), the conductor expression is (Y/8)P(log Y−log 8), not YP(log Y). This exact change of variables shifts every lower logarithmic coefficient. Combining signs similarly requires adding the two parity-dependent expressions, not doubling every coefficient. Sharp cutoffs require independent error control: approximating them by smooth weights is not automatically uniform in derivatives or interval width.

**Failed extension.** The exact shifted arithmetic identity A_full(β)=E_2(β)A8(β) applies separately to arithmetic factors. Multiplying an entire coalesced polynomial by the single unshifted constant E_2(0) need not transfer its lower coefficients: derivatives of E_2(β), gamma parity, density and conductor shifts also matter.

## 5. Multiple-Dirichlet-series and secondary-pole route

**Question attempted:** Can analytic continuation finish the all-k heuristic or resolve the higher-swap boundary?

The principal swap hyperplanes in averaging coordinate w are w=1−Σ_(j∈J)α_j. Their Mellin residues explain exactly the factors X^(1−A_J)fhat(1−A_J). The coalescing hyperplanes account for the principal logarithms. This pole dictionary is an explanation conditional on having suitable continuation and growth bounds, not itself a proof of those inputs.

For a simple isolated secondary pole at w=ρ with residue R, Mellin inversion gives R X^ρ fhat(ρ). A pole of order r gives X^ρ times a polynomial of degree at most r−1 in log X, with coefficients involving derivatives of fhat. This is an exact contour-residue calculation when the required contour shift and growth bounds hold. Therefore the cubic w=3/4 pole has a different scale from any principal swap with vanishing shifts; it cannot supply a missing X(log X)^j coefficient. No conflict exists between such an X^(3/4) term and an o(X) principal-polynomial conjecture.

Čech v3 Remark 1.4 explicitly identifies continuation past central w=1 only for k≤3 and an obstruction to central k≥4 and two-swap detection. Functional equations alone do not authorize continuation outside the proved domain. Baluyot–Čech's general matching of MDS residues and recipes is a heuristic with continuation inputs. Diaconu–Whitehead's cubic secondary asymptotic is a proved external result in its specified smoothed family, not a universal statement for every f or every subfamily; its residual coefficient may depend on the weight and must be checked in a transfer. The newer conditional first-moment analysis also prevents treating “secondary powers begin at k=3” as a universal law.

Shen–Stucky's unconditional fourth-moment result has error O(X(log X)^(6+ε)) and resolves the four highest orders 10,9,8,7 of its degree-ten recipe polynomial. It does not resolve all coefficients through the constant with o(X) remainder. In their AFE organization diagonal and nonzero-square pieces partly cancel. Thus the slogan that every off-diagonal piece is an additional main term is not decomposition invariant.

**Failed extension.** No new continuation domain, two-swap analytic estimate, secondary residue, or all-k central asymptotic has been obtained. The next genuinely new step would have to establish such an analytic input, rather than repackage the local law or invoke the functional equations formally.

## Acceptance limits and source map

Acceptable partials here are elementary identities, diagonal asymptotics, normalization corrections and falsification of overstrong simplifications. No new scholarly novelty is claimed. The complete AIM Conrey–Keating high-moment mechanism remains unresolved by this work; possessing the CFKRS recipe does not establish that mechanism at all swap levels.

Primary sources:
- AIM Problem 5.1: http://aimpl.org/zetamoments/5/
- Conrey–Rodgers, Theorem 1, Proposition 1, Lemma 2, Section 5: https://arxiv.org/html/2208.01783v2 . Published in Mathematische Zeitschrift 311, article 59 (2025): https://doi.org/10.1007/s00209-025-03848-x .
- Čech v3, Conjecture 1.1, Remark 1.4, Corollaries 1.5 and 1.7: https://arxiv.org/html/2402.07473v3
- Shen–Stucky, Theorem 1.1, Corollary 1.2 and discussion of cancellations: https://arxiv.org/html/2402.01497v1
- Baluyot–Čech, MDS heuristic: https://arxiv.org/html/2501.12529v1
- Diaconu–Whitehead cubic result (external theorem status): https://arxiv.org/abs/1804.00690
- Čech conditional secondary first moment (external theorem status): https://arxiv.org/abs/2509.03197

Computation: checks.py and EXACT_CHECKS.json use exact rational local arithmetic and finite fundamental-discriminant enumeration. The latter is only a sanity check; proofs are above. No L-value moment numerical experiment was performed. An arithmetic and scope review is included separately; acceptance is restricted to these partial statements, not a solution or novelty claim.
