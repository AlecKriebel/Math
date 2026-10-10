# Exponential small-value counts at rational parameters

Problem 30003114 (OWR-14603-013). Status: **NO RESOLUTION of the intended uniform counting question.** Five approaches below retain complete elementary partial results and identify their precise gaps. They carry no novelty claim.

## 1. Governing formulation and source controls

Let a=9/10, b=19/20, and let P_d consist of every polynomial of degree at most d with coefficients in {-1,0,1}, including the zero polynomial. Put

N_d(lambda,t) = #{P in P_d : |P(lambda)| < t}.

The substantive question is whether there exists one C>0 such that, for every reduced rational lambda=p/q in [a,b], there exists c_lambda>0 for which

N_d(lambda,c_lambda exp(-C d)) < exp(d/100)

for every integer d>=1. C must be independent of p and q; c_lambda may depend on them but not on d. No coefficient normalization is used. In the authored arguments, log and exp use the natural base.

The ID-matched public dataset row supplies absolute-value bars. The original OWR 21/2016, printed pp.1125–1126, Questions 3–4, uses {-1,0,1}, not the conventional all-±1 Littlewood family. Printed Question 4 omits the bars; its surrounding minimum problem and the corrected dataset identify the small-modulus interpretation above. The author's 2016 survey, Question 4.13, explicitly requires c_{p,q}>0 but repeats the missing bars. These source defects are not claimed as solutions of the corrected target.

Three conventions matter. First, allowing d=0 and counting zero makes the strict inequality 1<1 false; we use the substantive positive-degree interpretation. Second, allowing c_lambda<=0 makes the count empty, so positivity is essential. Third, zero is one counted polynomial, not an excluded event. Nonzero rational evaluation is established below. This concerns deterministic counts at a real rational point, not a unit-circle minimum, interval measure, random-sign small-ball estimate, or flat-polynomial construction.

For comparison only: without absolute-value bars and with c_lambda>0, sign symmetry gives at least (3^(d+1)-1)/2 counted negative-valued polynomials. Already d=1 gives four, exceeding exp(1/100). This refutes only the literal uncorrected display.

## 2. Approach I: arithmetic separation and lattice counting

**Proposition 1.** For reduced p/q in [a,b], evaluation on P_d is injective. Every nonzero value has magnitude at least q^(-d), and for every t>0,

N_d(p/q,t) <= 2 ceil(t q^d)-1 <= 2t q^d+1.

**Proof.** Here q>=10. If a nonzero integer polynomial R of degree r has a rational root p/q in lowest terms, multiplying R(p/q)=0 by q^r and reducing modulo q gives q | leading_coefficient(R), since gcd(p,q)=1. For P-Q with P,Q in P_d, a nonzero leading coefficient has absolute value at most 2, impossible when q>=10. Thus P(p/q)=Q(p/q) implies P=Q. Also q^d P(p/q) is an integer, so nonzero values have magnitude at least q^(-d). Injectivity embeds the counted set into the integers j with |j|<t q^d. For s>0 that interval contains exactly 2 ceil(s)-1 integers. The final inequality follows from ceil(s)<=s+1. QED.

**Corollary 1.** On the restricted set of denominators q<=Q, the target holds with C=log Q and c_lambda=1: only zero has |P(lambda)|<Q^(-d), so N_d=1<exp(d/100).

**Exact gap.** This proves the target for every bounded denominator set, not all rationals at once. The displayed estimate contains exp((log q-C)d). A parameter-dependent prefactor cannot remove this exponential dependence from the estimate when q is unbounded. That observation is a limitation of this proof, not a disproof of the question.

## 3. Approach II: lacunary conditioning and anti-concentration

This route seeks a denominator-free upper bound. Define L=22 and

gamma=(1-3b^L)/(1-b^L)>0.

The positivity follows from the exact integer inequality 3*19^22<20^22.

**Proposition 2.** If d>=1 and 0<t<=gamma a^d/2, then, uniformly for every real lambda in [a,b],

N_d(lambda,t) <= 3^(d+1-m), where m=floor(d/L)+1.

**Proof.** Fix the coefficients outside J={0,L,...,(m-1)L}. Consider two different assignments of the m remaining coefficients. At their first differing index i, the difference has coefficient of magnitude at least 1. All later differing coefficients have magnitude at most 2. Hence the difference of the evaluations has magnitude at least

lambda^i [1-2lambda^L/(1-lambda^L)]
 = lambda^i (1-3lambda^L)/(1-lambda^L)
 >= a^d gamma.

The last inequality uses i<=d and monotonic decrease of (1-3r)/(1-r) in r, together with lambda^L<=b^L. Two values in (-t,t) have distance strictly less than 2t<=a^d gamma. Thus at most one assignment of J is counted for each fixed assignment outside J. There are 3^(d+1-m) outside assignments. QED.

**Exact gap.** This gives an exponentially small probability <=3^(-m) for independent *uniform ternary* coefficients. The deterministic count, however, has exponential rate (21/22)log 3, much larger than 1/100. Shrinking t further does not improve this one-block counting argument. Uniform ternary coefficients are not independent fair ±1 signs, and even a strong probability bound cannot be presented as the required count without its factor 3^(d+1).

## 4. Approach III: pigeonhole collisions and a necessary exponent

This route looks for a counterexample by manufacturing many small polynomials rather than one.

**Proposition 3.** For every 0<lambda<1, d>=1 and t>0, let T=1/(1-lambda). Then

N_d(lambda,t) >= 2^(d+2) t/(T+t)-1.

The inequality is real-valued; no rounding claim is needed.

**Proof.** Set n=d+1 and consider all M=2^n binary words u=(u_0,...,u_d), with value S(u)=sum u_i lambda^i. Every value lies in [0,T). Partition that interval into K=ceil(T/t) half-open intervals of width at most t, placing boundary points consistently. If their occupancy counts are m_j, Cauchy–Schwarz gives sum m_j^2>=M^2/K. Thus at least M^2/K-M ordered pairs of distinct words occupy a common interval and have |S(u)-S(v)|<t.

The coefficient difference u-v is a nonzero member of P_d. If it has z zero coefficients, exactly 2^z ordered pairs realize it: nonzero coordinates force both bits and zero coordinates allow (0,0) or (1,1). Since the polynomial is nonzero, z<=n-1. Therefore the number of distinct nonzero counted polynomials is at least

(M^2/K-M)/2^(n-1)=2^(n+1)/K-2.

Add the zero polynomial and use K<=T/t+1 to obtain the claim. This proof does not require evaluation injectivity, although it holds for the rational target. QED.

**Corollary 3.** Any C in a positive answer to the target must satisfy C>=log 2-1/100.

**Proof.** Fix lambda=9/10 and any c>0; take t_d=c exp(-Cd). If 0<C<log 2-1/100, then t_d<=T eventually and Proposition 3 gives N_d>=2^(d+1)t_d/T-1. Its exponential rate log 2-C is strictly greater than 1/100, contradicting the required upper bound for all sufficiently large d. QED.

**Exact gap.** The question permits arbitrarily large absolute C. This necessary condition rules out a range of proposed constants but supplies no obstruction for every C. A finite example with many values below one chosen threshold cannot refute the quantified statement.

## 5. Approach IV: complex analysis localizes small values near zeros

This route asks whether only boundedly many nearby roots can cause small values. We give an explicit degree-independent zero count, followed by a quantitative localization. Classical Jensen's formula, the maximum principle and Harnack's inequality are the only analytic inputs.

Use r=99/100, R=97/100, M=100, H=(R+b)/(R-b)=96,

K=ceil(log(M)/log(r/R)), A=r/(r^2+Rb), and c0=M^(1-H).

These are absolute constants, with 0<A<1 and K>=1.

**Proposition 4.** Let 0!=P in P_d. Remove its zero at the origin: P(z)=z^k f(z), where |f(0)|=1. There are at most K zeros of f in |z|<=R, counted with multiplicity. Let delta be the minimum of 1 and the distances from a real x in [a,b] to those zeros; if there are none, set delta=1. Then

|P(x)| >= a^d c0 (A delta)^K.

**Proof.** On |z|<=r the coefficient bound gives |f(z)|<=sum_{j>=0}r^j=M. Jensen's formula at radius r yields sum_{|alpha|<r} log(r/|alpha|)<=log M because |f(0)|=1. The possible presence of zeros on the radius is handled by radii tending to r; their zero contribution does not change the inequality. Every zero with |alpha|<=R contributes at least log(r/R). Hence their number N is at most K.

For these N roots with multiplicities, take the finite radius-r Blaschke product B(z)=product r(z-alpha)/(r^2-conjugate(alpha)z), with arbitrary unimodular factors. The quotient g=f/B is analytic on the disk |z|<=r after filling the removable zeros. On its boundary |B|=1, so |g|<=M by the maximum principle. Moreover |g(0)|=|f(0)|/|B(0)|>=1. The function h=log M-log|g| is nonnegative and harmonic on |z|<R, because all zeros there have been removed. Harnack's inequality at |x|<=b gives h(x)<=H h(0)<=H log M, and therefore |g(x)|>=c0.

Each factor of B at x has magnitude at least r|x-alpha|/(r^2+Rb)>=A delta. Since 0<A delta<=1 and N<=K, |B(x)|>=(A delta)^K. Finally x^k>=a^d, giving the claim. If P(x)=0 then delta=0 and the inequality remains valid. QED.

**Consequence.** If C> -log a and |P(x)|<c0 exp(-Cd), then

delta < A^(-1) exp(-(C+log a)d/K).

For sufficiently large d the right side is below 1, so there must be a root within that distance.

**Exact gap.** No uniform lower bound for the distance from a fixed rational p/q to the roots of *all varying-degree* polynomials has been established here. Boundedly many nearby roots per polynomial does not bound how many different polynomials have nearby roots or share a root. Rationality excludes exact roots, but alone gives only the denominator-dependent arithmetic scale. The cited Breuillard–Varjú common-root theorem (Proposition 20) requires r<n^(-3n), a superexponential scale. Replacing it by exp(-Cn), or claiming its conclusion at that larger scale, is unjustified.

## 6. Approach V: high multiplicity and separated product constructions

This is an explicit counterexample search within structured coefficient families. Let positive integers m_0,...,m_(s-1) satisfy m_j>sum_{i<j}m_i, and set

F(x)=product_{j=0}^{s-1}(1-x^(m_j)).

**Proposition 5.** F has coefficients in {-1,0,1}, has a zero of multiplicity exactly s at 1, and for every x in [a,b],

F(x) >= exp(-380).

Consequently x^k F(x), when it has degree at most d, has magnitude at least exp(-380) a^d on this interval.

**Proof.** The superincreasing condition makes all subset sums of the exponents distinct: at the greatest index where two subsets differ, that exponent exceeds the sum of all previous exponents. Expansion therefore has one term, of sign ±1, for each subset sum, and zeros at all other coefficients. Each factor has a simple zero at 1, proving exact multiplicity s. The same condition inductively gives m_j>=2^j>=j+1.

For 0<=u<1, integration of 1/(1-v) from 0 to u proves -log(1-u)<=u/(1-u). Thus, for x<=b,

-log F(x) <= sum_j x^(m_j)/(1-x^(m_j))
 <= (1/(1-b)) sum_{j>=0} b^(j+1)
 = b/(1-b)^2 = 380.

All factors are positive. Exponentiating proves the bound; multiplication by x^k costs at most a^d. QED.

The choice m_j=2^j gives the standard Thue–Morse ±1 polynomial of degree 2^s-1, with unbounded multiplicity at 1. It nevertheless stays uniformly away from zero on [a,b].

**Exact gap.** This rules out this large, familiar high-multiplicity construction as a counterexample. Arbitrary ternary polynomials need not factor this way. Counting or minimum behavior of this subclass cannot establish the general result.

## 7. Literature boundary and conclusion

The primary 2016 problem and survey were directly inspected. Breuillard–Varjú, *On the dimension of Bernoulli convolutions*, arXiv:1610.09154v3, Proposition 20 and Theorem 21, give common-root and root-separation tools at n^(-O(n)) scales; their stated hypotheses do not resolve this exponential-scale count. Kittle–Kogler, *On absolute continuity of inhomogeneous and contracting on average self-similar measures*, arXiv:2409.18936v4 (17 October 2025), Corollary 1.15, improves sufficient absolute-continuity conditions in terms of Mahler measure. For a reduced rational p/q in (0,1), that measure is q. The condition still depends on q and does not prove the target. Nor is absolute continuity, by itself, the same assertion as this finite polynomial count.

These were targeted literature checks, not an exhaustive proof of worldwide openness. No complete proof, counterexample to the intended statement, verified earlier resolution, or novelty claim results. The exact remaining requirement is an upper count below exp(d/100) at one denominator-independent exponential scale for every rational in [9/10,19/20], with only a parameter-dependent prefactor allowed.
