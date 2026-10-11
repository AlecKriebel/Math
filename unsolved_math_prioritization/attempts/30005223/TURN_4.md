# Substantive turn 4: actual irreducible fiber annihilators and a projection criterion

## Aim and outcome

This turn attacked the first missing hypothesis of turn3: can one rule out identically zero fibers after excluding the three known zero types? The answer to that blanket deterministic claim is no, already for an actual irreducible character of S11. A complete symbolic annihilator criterion and an exact fourth-moment condition for its probability are derived below. Neither provides the required bulk asymptotic without an additional estimate.

## 1. Residual characters and the exact kernel

Use the fiber notation nu,R,s of turn3. Successively applying Murnaghan–Nakayama to the fixed large cycles nu produces the virtual character of S_R

W_(lambda,nu)=sum_(eta partitions R) chi_(lambda/eta)(nu) chi_eta.

The notation chi_(lambda/eta)(nu) is the integer signed sum over the corresponding rim-hook removals, equivalently the skew character. Therefore

f_(lambda,nu)(r)=W_(lambda,nu)(2^r1^(R-2r)).                 (1)

In the ring of symmetric functions over Q, its Frobenius characteristic is p_nu^perp s_lambda, where p_t^perp=t d/dp_t. Evaluation at p_1=x,p_2=y,p_j=0 for j>=3 gives the exact polynomial

F_(lambda,nu)(x,y)
 =sum_(r=0)^s f_(lambda,nu)(r) x^(R-2r)y^r/
                         [(R-2r)!2^r r!].                (2)

Thus the entire fiber is zero if and only if this polynomial is identically zero, equivalently

p_nu^perp s_lambda belongs to the ideal (p_3,p_4,...).       (3)

This is a concrete annihilator, not merely the assertion that the residual virtual character vanishes. A nonzero residual virtual character may lie in this ideal.

There is a determinant formula for testing (3) without enumerating the whole character table. Define H_j(x,y)=0 for j<0 and, for j>=0,

H_j(x,y)=sum_(b=0)^floor(j/2) x^(j-2b)y^b/
                                      [(j-2b)!2^b b!].

If ell is the number of rows of lambda and the parts of nu are labeled nu_1,...,nu_k, then

F_(lambda,nu)=sum_(a:{1,...,k}->{1,...,ell})
 det[H_(lambda_i-i+j-sum_(t:a(t)=i)nu_t)(x,y)]_(i,j=1)^ell. (4)

Indeed Jacobi–Trudi expresses s_lambda as det(h_(lambda_i-i+j)). The operator p_t^perp changes h_m to h_(m-t). The product rule assigns each labeled derivative to one determinant row, yielding (4), including the correct multiplicities for repeated parts of nu. After specialization the complete symmetric functions are exactly H_j. This formula is finite and exact; no polynomial-time claim is made.

## 2. A genuine irreducible obstruction outside typesI–III

Take lambda=(5,2,2,2), nu=(3,3), n=11, R=5, s=2. Two rim-hook removals give

W_(lambda,nu)=2 chi_(5)+2 chi_(2,1,1,1)-2 chi_(2,2,1).

Its full Frobenius characteristic is

p_3(p_1²+p_2)=2p_3 h_2.                                   (5)

It is nonzero: its values on cycle types(3,1,1) and(3,2) of S5 are6. Yet it vanishes on every involution class. Consequently all three actual S11 values at

(3,3,1,1,1,1,1), (3,3,2,1,1,1), (3,3,2,2,1)

are zero. Direct hook statistics certify that none is typeIII; hence none is typeI orII either. Formula(4) independently gives the identically zero polynomial in x,y. This is an actual irreducible row of the source character table, unlike the deliberately reducible regular-character countercontrol in turn3.

The example does not disprove that such fibers have probability tending to zero. Its remaining size5 does not grow with n, and it is not promoted to a bulk family. Inducing (5) together with any additional character gives further virtual characters vanishing on involutions, since every restriction of an involution to a selected invariant subset is again an involution. That observation also does not manufacture new irreducible source examples. Both distinctions are essential.

## 3. Exact orthogonality gives a quantitative probability criterion

For a fixed nu let q=s+1 and form the p(n)-by-q real matrix

A_(lambda,r)=chi_lambda(mu_r)/sqrt(z_(mu_r)).

Column orthogonality gives A^T A=I_q. Thus AA^T is an orthogonal projection. Its diagonal entries

ell_lambda=sum_(r=0)^s chi_lambda(mu_r)^2/z_(mu_r)

satisfy 0<=ell_lambda<=1, sum_lambda ell_lambda=q. The entire fiber in row lambda is zero exactly when ell_lambda=0. Cauchy–Schwarz on the nonzero entries yields the deterministic bound

Pr_lambda(f identically zero)
 <=1-q²/[p(n) sum_lambda ell_lambda²].                     (6)

It follows that the sufficient uniform-relative-fourth-moment estimate

sum_lambda ell_lambda² = (1+o(1)) q²/p(n)                  (7)

on a set of fibers of probability tending to one would prove that the identically zero-fiber probability tends to zero. A size-weighted averaged version of (6) is equally valid. This addresses the exact conditional uniform-row distribution; it does not change to Plancherel measure.

The missing quantity is explicit:

sum_lambda ell_lambda²
 =sum_(r,t) [sum_lambda chi_lambda(mu_r)² chi_lambda(mu_t)²]
                                                   /[z_(mu_r)z_(mu_t)].

Ordinary two-column orthogonality does not control this diagonal fourth moment. It supplies only sum ell²<=q, hence the weak nonzero-row fraction q/p(n), which vanishes exponentially on the scales of interest. An abstract projection may concentrate on exactly q coordinates, attaining this weak bound; this is a warning about the algebraic input, not an assertion about the actual character matrix. Conversely, (7) is merely sufficient and need not be necessary for few zero fibers.

## 4. Checks and unresolved step

The checker independently constructs the row-assignment polynomial(4) by rational polynomial convolution and determinant expansion, then compares its coefficients with exact Murnaghan–Nakayama character values. It verifies the full S11 residual Schur expansion and power-sum identity(5), every member's failure of typeIII, and the explicitly virtual induction observation. Separate exact projection controls verify(6) and its normalization for small actual fibers.

The blanket nondegeneracy shortcut has been falsified. The remaining route would require a probabilistic estimate on the annihilator(3), the fourth moment in(7), or a different irreducibility-specific argument. No estimate for its bulk frequency has been established, and the original limiting vanishing probability remains unresolved after four substantive author turns.
