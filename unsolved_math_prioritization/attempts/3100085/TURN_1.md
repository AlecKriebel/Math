# Turn 1: exact radical test and structural restrictions on binomial collisions

**Scoped partial; original existence question unresolved after one recovered/new substantive turn.** No previous author proof artifact was recovered. The arithmetic characterization below decides a fixed n exactly, including every real probability p in the intended domain. A modest finite control through n=80 finds no admissible collision. Neither finite checking nor the elementary restrictions prove the all-n assertion.

## 1. Tie parameters and exact arithmetic

Write B_k=binomial(n,k), q=p/(1-p)>0. The common factor (1-p)^n shows that f(p;n,a)=f(p;n,b), a<b, if and only if

 q^(b-a)=B_a/B_b.                                               (1)

Thus each pair determines one positive q. The excluded symmetric parameter p=1/2 is exactly q=1.

For each prime ell<=n, write v_ell(B_k) for its exponent in B_k. Equation (1) uniquely determines the rational exponent vector

 V(a,b)_ell=[v_ell(B_a)-v_ell(B_b)]/(b-a).                       (2)

**Proposition 1.** Two distinct pairs determine the same positive q if and only if their vectors (2) agree for every prime. The vector must be nonzero to give an allowed probability.

Indeed, if the vectors agree, both positive roots equal the real number product_ell ell^(V_ell). Conversely, if the positive roots agree, raising to the product of the two pair lengths gives equality of positive rationals; unique prime factorization gives equality of the rational exponent vectors. No floating-point root or logarithm comparison is involved.

Let r=b-a and let d be the least positive integer for which every d V_ell is integral. Then q^d is rational, and d divides r. This d is an exact rational-power denominator, not a claim about an arbitrary complex branch. If two tied pairs have lengths r,s, then d divides gcd(r,s). In particular, coprime lengths force rational odds q. This also follows directly by Bezout from q^r,q^s in Q.

## 2. The pairs must be nested

The successive ratio of the weighted sequence is

 (B_{k+1}q^(k+1))/(B_k q^k)=q(n-k)/(k+1),

which is strictly decreasing in k. Its logarithmic sequence is strictly concave, increasing up to its unique mode or adjacent two-point modal plateau, and decreasing afterward. Any equality pair has one endpoint on each side of this peak; equal values at three distinct indices are impossible. Moreover, if four indices support two equal pairs, the pairs must be nested after relabeling:

 a<c<d<b, with ties (a,b) and (c,d).                            (3)

To see the ordering directly, for a<c with equal-value partners b,d on the descending side, strict increase on the left gives F_a<F_c, so strict decrease on the right gives b>d. A modal plateau, if present, is the innermost adjacent pair and the same argument applies to lower levels.

Equal pair lengths are impossible even without the nesting observation: for fixed r, the ratio B_a/B_{a+r}=product_{j=a}^{a+r-1}(j+1)/(n-j) strictly increases with a.

## 3. Equal midpoints are excluded away from p=1/2

Suppose two nested pairs have a+b=c+d=S. Their lengths have the same parity. Set R_j=(j+1)/(n-j), so the geometric mean of R_j over j=a,...,b-1 is q for that pair.

For j and its reflected index S-1-j, put x=j+1. Then

 R_j R_{S-1-j} = x(S+1-x) / [(n+1)(n-S)+x(S+1-x)].             (4)

If S<n, the positive constant (n+1)(n-S) makes this quantity strictly increasing with x(S+1-x). Moving the reflected pair outward from the common midpoint decreases that product. Accordingly, enlarging a centered interval by its two outermost terms strictly decreases the geometric mean: those two terms have smaller geometric mean than every inner reflected pair, and also than the central singleton if one is present. Repeating this step gives q_outer<q_inner.

If S>n, the same positive-denominator expression has negative constant and reverses the inequality, giving q_outer>q_inner. All denominators in (4) are positive on the actual indices. If S=n, reflection gives R_j R_{n-1-j}=1 and every centered interval has geometric mean1, hence p=1/2.

**Proposition 2.** Two admissible equal-probability pairs cannot have the same midpoint. Consequently, for the nesting in (3), the outer length must exceed the inner length by at least3: an increase of2 would require exactly one new index on either end and hence the same midpoint. This is a necessary condition, not a full characterization.

## 4. Prime-exponent width bounds

Legendre's factorial formula gives

 v_ell(B_k)=sum_{j>=1}[floor(n/ell^j)-floor(k/ell^j)-floor((n-k)/ell^j)].

Each bracket is0 or1, and it vanishes when ell^j>n. Therefore

 0<=v_ell(B_k)<=floor(log_ell n).                               (5)

For an allowed tie let d be its rational-power denominator from Section1 and let e_ell=dV_ell. Some e_ell is a nonzero integer. If its pair length is r, then

 |v_ell(B_a)-v_ell(B_b)|=(r/d)|e_ell|.

It follows that

 r/d<=floor(log_ell n)<=floor(log_2 n).                         (6)

In particular, if q is rational, every tied pair spans at most floor(log_2 n). If two lengths are coprime, both obey this bound. Together with Proposition2, a coprime-length collision requires an outer length at least4 and thus n>=16. These conditions are not asserted sufficient.

There is a useful prime-row endpoint exclusion. If n=P is prime, v_P(B_k)=1 for every interior k and0 for k=0,P. An equality pair involving an endpoint and an interior point therefore has nonzero P-component in (2). A disjoint second pair either is entirely interior, in which case that component is zero, or uses the opposite endpoint, in which case the sign is reversed. The pair (0,P) itself has q=1. Hence an admissible two-pair collision in a prime row cannot involve an endpoint.

## 5. Finite exact control and status

The accompanying script constructs all prime-valuation rows by Legendre's formula, stores (2) as reduced integer vectors plus a common positive denominator, and checks all pairs for3<=n<=80. Exactly88,556 pairs were inspected, excluding zero vectors from the collision registry; no two disjoint pairs shared an allowed vector. Thus there is no example with n<=80 in the intended probability domain. This is a finite exact result, not an asymptotic extrapolation. Additional controls compare the vectors with direct integer powers of binomial coefficients and verify the nesting/midpoint/width restrictions in their applicable ranges.

All arguments use elementary standard facts and no historical novelty is asserted. The remaining question is whether the integer binomial-ratio exponent vectors can collide for some larger n, subject to the restrictions above, or whether a uniform obstruction excludes them. Four genuine author turns remain. Any complete resolution or final partial package requires separate independent source/proof review before a result PR.
