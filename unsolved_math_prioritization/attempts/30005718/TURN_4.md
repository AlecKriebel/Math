# Turn 4 Uniform endpoint estimates give eventual full row ultra log concavity

**Target:** 30005718 / OWR-14298007-013. **Substantive author count:** 4/5.

**Result:** There exists an integer N such that every original polynomial V_n is ultra-log-concave for n at least N, using its actual degree and retaining its initial zero coefficients. The proof supplies no numerical value of N. The source asks for every n, so the original problem remains unresolved. A finite check through n=500 cannot fill an unspecified finite exceptional range.

The new step is uniform control of the two shrinking edge regions left by TURN_3. The lower edge needs the second correction to its logarithmic adjacent ratio; its positive monomial shift is relevant. At the upper edge an exact parity identity reduces the problem to ordinary analytic powers with a small saddle, avoiding a nonuniform comparison of two coalescing spectral branches.

## 1 An analytic small saddle lemma

Let Lambda(z) and A(z) be holomorphic in a disk about zero, real on its real diameter, with

Lambda(0)=1, Lambda'(0)=a>0, A(0)>0.

Take a sufficiently small positive radius so Lambda is nonzero there and its real logarithm f=log Lambda is holomorphic. Put D=z d/dz,

alpha=D f, s=D alpha, nu=s/alpha.

Near zero, alpha=a z+O(z^2), s=a z+O(z^2), and nu=1+O(z). Thus alpha has a real-analytic local inverse rho=rho(alpha), positive for small positive alpha, and nu remains positive. If integers m,j satisfy j→infinity and 0<j/m≤alpha_0 for a sufficiently small fixed alpha_0, then, uniformly in that full range,

[z^j] A(z)Lambda(z)^m
 = A(rho)Lambda(rho)^m rho^(-j) / sqrt(2 pi m s(rho))
   times [1+B_1(alpha)/j+B_2(alpha)/j^2+O(j^(-5/2))].                 (1)

Here rho is chosen by alpha(rho)=j/m. Both B_1 and B_2 extend real-analytically to alpha=0. In particular all displayed coefficients and their fixed-order derivatives are bounded on a sufficiently small closed interval. The coefficients on the left are eventually positive in this range, even though this lemma does not assume that every Taylor coefficient of Lambda or A is nonnegative.

### Uniform angular bound

Write f(z)=a z+sum_(l≥2) b_l z^l. For real theta,

1−cos(l theta) ≤ l^2(1−cos theta).

Absolute convergence permits choosing rho_0 so

sum_(l≥2) l^2 |b_l| rho^l ≤ a rho/2  for 0<rho≤rho_0.

Consequently

Re[f(rho exp(i theta))−f(rho)] ≤ −(a rho/2)(1−cos theta).            (2)

Since alpha is comparable to rho, multiplication by m gives uniform suppression in the large parameter j=m alpha, including angles away from zero. The amplitude is uniformly bounded on these circles and A(rho) is bounded away from zero.

### Uniform local expansion

Set kappa_l=D^l f. Every kappa_l/alpha extends analytically to rho=0 with value 1. Likewise (D^l A)/A is analytic near zero. In the Cauchy integral set y=sqrt(j) theta. The quadratic exponent is −nu y^2/2; its cubic through sextic corrections have orders j^(-1/2), j^(-1), j^(-3/2), j^(-2), with uniformly analytic bounded coefficients. Expand the amplitude through fourth order and the exponential through total order j^(-2). The odd polynomials of y integrate to zero. The remaining Gaussian moments give B_1 and B_2, as analytic expressions in these coefficients and positive powers of 1/nu.

For a remainder bound, split at |theta|=j^(-2/5). Outside this interval, (2) bounds the integral by an exponential in −c j^(1/5), or better. Inside it, the phase Taylor remainder after order six is bounded by C j |theta|^7 = C j^(-5/2)|y|^7, and the amplitude remainder by C j^(-5/2)|y|^5. The omitted products from the exponential expansion satisfy the same order times a fixed polynomial in |y| and a Gaussian majorant. The cubic perturbation is uniformly small on this interval. Its Gaussian majorant can be chosen independently of rho because nu stays bounded away from zero. Integration and replacement of the truncated Gaussian interval by the real line give the relative O(j^(-5/2)) in (1). This also proves analyticity of the correction coefficients, rather than assuming smoothness of an unspecified error.

For example, writing h_l=(D^l A)/A and c_l=kappa_l/alpha,

B_1=−h_2/(2nu)+h_1 c_3/(2nu^2)+c_4/(8nu^2)−5c_3^2/(24nu^3).

An explicit long expression for B_2 is unnecessary: the finite Taylor/Gaussian-moment prescription above defines it and proves its analyticity. The independent-checkable moment code in this turn implements that prescription. The method is the classical large-powers saddle expansion, with its small-saddle uniformity supplied here; TURN_2 records the Flajolet–Sedgewick reference.

### Consequence for adjacent coefficients

Let c_m,j denote the coefficient in (1), let q be a fixed positive integer, and let S(alpha)=f(rho)−alpha log rho. Taking a real logarithm of (1) gives

log c_m,j = m S(alpha)−(1/2)log j+b(alpha)
            +b_1(alpha)/j+b_2(alpha)/j^2+O(j^(-5/2)),              (3)

where b,b_1,b_2 are real-analytic at zero. In fact b=log[A(rho)/sqrt(2 pi nu)], b_1=B_1 and b_2=B_2−B_1^2/2. Also S''=−1/s and S''''=O(alpha^(-3)), because S=−alpha log alpha plus an analytic function at zero.

Apply (3) at j−q,j,j+q. Work on a slightly smaller alpha interval so these neighboring saddles are covered. The Legendre term contributes q^2/(m s)+O(j^(-3)); the logarithmic prefactor contributes −q^2/(2j^2)+O(j^(-4)); b contributes O(m^(-2)). The central differences of b_1(j/m)/j and b_2(j/m)/j^2 are O(j^(-3)) and O(j^(-4)), respectively. These follow by differentiating those explicit smooth functions, using j≤alpha_0 m. The three undifferentiated final errors together are O(j^(-5/2)). Therefore

log[c_m,j^2/(c_m,j−q c_m,j+q)]
 = q^2/(m s(rho))−q^2/(2j^2)+O(j^(-5/2)+m^(-2)).                (4)

No derivative bound on the final O term is used. All constants are uniform in the full small-saddle range.

The lemma remains valid if an additional coefficient-integral contribution is bounded relative to its displayed leading term by C sqrt(j) exp(−c j). Such a contribution is smaller than the required error uniformly for large j.

## 2 The lower edge

Retain m=n−4, F_m=z^(-3)V_(m+4), and j=k−3. From TURN_2, exactly near zero,

F_m(z)=H(z)lambda(z)^m+H_-(z)lambda_-(z)^m,

lambda=1+(3/2)z+(z/2)sqrt(5+4z),
H=2(1+z)+(z^2+6z+6)/sqrt(5+4z),

and the minus functions change the square-root contribution's sign. These are analytic at zero despite the transfer eigenvalues meeting there. Here lambda'(0)=a=(3+sqrt5)/2>0 and H(0)=2+6/sqrt5>0.

The secondary eigenvalue has derivative a_-=(3−sqrt5)/2<a. On the entire circle |z|=rho, for rho sufficiently small,

|lambda_-(z)| ≤ 1+a_- rho+C rho^2,
lambda(rho) ≥ 1+a rho−C rho^2.

Their ratio is at most exp(−c rho). The secondary amplitude is bounded. Since m rho is comparable to j, its whole Cauchy integral relative to the main saddle term is at most C sqrt(j) exp(−c' j). Thus the small-saddle lemma applies to the actual coefficients of F_m, not just to a formal dominant term.

Use (4) with q=1. Let beta=3/2 and define the exact inverse-variance gap

D_0(rho)=1/s(rho)−1/alpha(rho)−1/(beta−alpha(rho)).                 (5)

TURN_2 proves this is positive for all rho>0. At the lower endpoint it has a strictly positive limit. Indeed, lambda=1+a rho+b rho^2+O(rho^3), where b=1/sqrt5, so

lim_(rho→0) D_0(rho)=1/3−2/(sqrt5 a^2)
                    =(3+7sqrt5)/(45+21sqrt5)>0.                 (6)

Consequently D_0≥d_0>0 on a fixed sufficiently small saddle interval.

The original degree is d=floor[3(m+1)/2]+3. Thus d=beta m+c_m, where c_m is 4 or 9/2. The original coefficient at k is c_m,j with k=j+3. Uniformly in the small lower band,

log[(k+1)(d−k+1)/(k(d−k))]
 = (1/m)[1/alpha+1/(beta−alpha)]−(7/2)/j^2
   +O(j^(-3)+m^(-2)).                                          (7)

The 7/2 is important: log(1+1/(j+3))=1/j−(7/2)/j^2+O(j^(-3)). The other edge is of order m and has only an O(m^(-2)) correction.

Subtracting (7) from (4) gives the original normalized ULC logarithmic margin

D_0(rho)/m+3/j^2+O(j^(-5/2)+m^(-2)).                            (8)

Choose J large so the first error is at most (3/2)/j^2, and then m large so the second is at most d_0/(2m). This proves strict ULC simultaneously for all j≥J with j/m in a fixed sufficiently small positive band. The finitely many remaining fixed indices 1≤j<J are eventually strict by TURN_3, so one maximum of their thresholds completes the lower edge. Index j=0 has a zero preceding coefficient and is immediate.

Thus there are epsilon_lower>0 and M_lower such that, for every m≥M_lower, every original inequality with 0≤j≤epsilon_lower m holds, and is strict when its central coefficient and the factor d−k are positive. This is uniform edge coverage; it is stronger than a separate theorem for each fixed j.

## 3 Exact upper parity reduction

Let a_(r,h) be the coefficient of w^h in the reversal of the original V_n. Equivalently, it is the coefficient at original degree d−h. Write m=2r for the even case and m=2r+1 for the odd case. The degrees of F_m are 3r+1 and 3r+3, respectively.

Set x=sqrt(w) formally and define analytic functions near zero

L(x)=sqrt(1+5x^2/4)+(3/2)x+x^3,
Kappa(x)=L(x)^2,
E(x)=2x+2x^3+(1+6x^2+6x^4)/(2sqrt(1+5x^2/4)).                    (9)

They satisfy Kappa(0)=1, Kappa'(0)=3, and E(0)=1/2. Define A_1=E and A_0=E L. Then the exact coefficient identities are

a_(r,h)=2[x^(2h+1)] A_1(x)Kappa(x)^r       when m=2r,
a_(r,h)=2[x^(2h)]   A_0(x)Kappa(x)^r       when m=2r+1.            (10)

To derive them rather than infer them numerically, put

H_e(x)=x^2 H(1/x^2)=E(x)/x.

Also lambda(1/x^2)=x^(-3)L(x), while the minus eigenvalue is −x^(-3)L(−x). Hence the even reversal is

x^(-1)E(x)Kappa(x)^r+(−x)^(-1)E(−x)Kappa(−x)^r,

and the odd reversal is

E(x)L(x)Kappa(x)^r+E(−x)L(−x)Kappa(−x)^r.

The sums are even series; in the even case their possible simple poles cancel. Taking the coefficient of x^(2h) proves (10), including r=0. This also reproduces the fixed-tail leading coefficients of TURN_3. The square-root notation introduces no competing complex saddle, because (10) is now an ordinary coefficient extraction in the variable x.

## 4 Uniform upper edge inequalities

Apply the small-saddle lemma to Lambda=Kappa, amplitude A_delta, power r, and coefficient index ell=2h+delta, where delta=1 or 0 according to (10). Both amplitudes are analytic and equal 1/2 at zero. Put alpha=x d/dx log Kappa and s=x d/dx alpha. Then s/alpha→1 as x→0.

Adjacent h values correspond to a step q=2 in ell. The factor 2 in (10) cancels in the ratio, and (4) yields, uniformly for large h in a sufficiently small h/r band,

log[a_(r,h)^2/(a_(r,h−1)a_(r,h+1))]
 =4/(r s)−2/ell^2+O(ell^(-5/2)+r^(-2)).                         (11)

Choose the saddle interval small enough that s/alpha≤6/5. Choose eta>0 with eta≤1/4 so that 0≤h≤eta r implies this saddle condition and the lemma's slightly enlarged neighboring-index condition for all sufficiently large r. For h≥5,

4/(r s) ≥ 4/[(6/5)(2h+delta)] ≥ (3/2)/h.                        (12)

The total absolute size of the remaining terms in (11) is at most 1/(10h) for all sufficiently large h, uniformly in this band; here r^(-2)≤1/(16h^2) because h≤r/4. Thus the coefficient curvature is at least (7/5)/h.

The original degrees are d=3r+4 and d=3r+6. At the original index k=d−h, the required binomial curvature obeys

log[(k+1)(h+1)/(kh)]
 ≤1/h+1/(d−h)
 ≤(12/11)/h,                                                    (13)

since h/r≤1/4 and d≥3r. Because 7/5>12/11, this proves strict original ULC for all sufficiently large h uniformly throughout 0<h≤eta r. The remaining finitely many fixed h≥1 are eventually strict by TURN_3. The top coefficient h=0 is an endpoint, and its missing-next-coefficient inequality is automatic if included by the zero-extension convention.

Therefore a common large-r threshold covers the entire upper edge h≤eta r. Both parity rows are included.

## 5 Joining the bands

Take the two uniform edge regions just established. Outside them, j≥epsilon_lower m and h=D_m−j≥eta r, where D_m=deg F_m and r=floor(m/2). Since D_m=(3/2)m+O(1) and r=m/2+O(1), the remaining indices lie, for all sufficiently large m, in one fixed proportional interior band

epsilon m≤j≤(3/2−epsilon)m

for a sufficiently small epsilon>0. TURN_2 proves eventual strict ULC there with one threshold. Taking the maximum of the two edge thresholds and this one gives an N for every row and every index. The fixed leading zero coefficients do not violate ULC, and there are no internal zeros by TURN_1.

**Theorem.** There exists N such that the original degree-normalized coefficient sequence of V_n is ultra-log-concave for every n≥N. For those sufficiently large n, every interior inequality with a positive central coefficient is strict.

The proof is existential. None of the unspecified analytic thresholds is replaced by a bounded numerical sample. In particular, the fact that the exact earlier checker verifies n≤500 does not prove that its range overlaps this eventual theorem.

## 6 Checks and remaining work

The checker `checks/verify_turn4.py` verifies the exact parity coefficient reduction, its low-order analytic identities, the endpoint inverse-variance limit, the Gaussian correction prescription and the binomial shift coefficients. Separate numerical diagnostics, if supplied, are labelled non-interval evidence. Neither type of computation proves the uniform analytic remainder or supplies an effective N; those are distinct issues.

**Sharp remaining gap after four turns:** prove the original assertion for the finite but presently unbounded set n<N, or obtain an explicit rigorously certified threshold and verify every row below it. A new all-size structural induction could also close that gap. The general question about tools for polynomial matrix recursions has acquired a sufficient bulk/endpoint method, not a necessary-and-sufficient classification.

**Original status:** unresolved, 4/5 substantive author turns. Subjective planning completion estimate 70 percent; not a correctness or novelty probability. Classical saddle-point methods are not claimed as new, and historical priority of this scoped eventual consequence has not been certified.
