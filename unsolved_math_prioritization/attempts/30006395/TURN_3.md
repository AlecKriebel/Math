# Turn 3: the exact critical second-moment window

**Partial result; this is an L² transition, not an information-theoretic detection transition.** Author turn 3, 2026-10-01. Same unknown labelled-tree mixture as Turns 1–2. No novelty claim or final independent review yet.

## 1. Exact finite recurrence

Retain the notation of Turn 1:

    t=k²/n, rho=(1−c/n)/c,
    R(v)=[(k)_v/k^v]² n^v/(n)_v.

Define nonnegative coefficients b_v by the formal power series

    exp(sum_(s=2)^k a_s z^s)=sum_(v≥0) b_v z^v,
    a_s=t rho^(s−1) s^s/s! .                       (1)

Then the exact forest formula is

    E_P L²=sum_(v=0)^k R(v)b_v,                    (2)

where b_0=1, b_1=0. Differentiating (1) as a formal identity gives

    v b_v=sum_(s=2)^v s a_s b_(v−s).               (3)

Thus the full moment, including all component interactions through R(v), can be evaluated by a finite coefficient recurrence. Equations (1)–(3) are equalities, not independent-component approximations. The partition sum and this recurrence are compared exactly in the checker.

## 2. Two-parameter critical limit

Let k→infinity and n→infinity with

    lambda_n=k^(9/4)/n → lambda∈[0,infinity),
    theta_n=sqrt(k) log(c_n/e) → theta∈R.          (4)

Use p_n=c_n/n; then c_n→e and k/n→0, so the model and 2k≤n are valid eventually. For this unknown-tree mixture,

    E_P L² → M(lambda,theta),                       (5)

where

    M(lambda,theta)=1+
      sum_(r≥1) (lambda e/sqrt(2))^r/[r! Gamma(r/2)]
        integral_0^infinity u^(r/2−1) exp(−u²−theta u) du. (6)

This positive series is finite for every finite lambda≥0 and theta∈R. At theta=0 it becomes

    M(lambda,0)=1+
      sum_(r≥1) (lambda e/sqrt(2))^r Gamma(r/4)
                    /[2 r! Gamma(r/2)].           (7)

For lambda>0, M(lambda,theta)>1. Nevertheless (5)–(7) alone do not prove that total variation has a positive limit. They do imply a uniform second-moment bound and hence the impossibility of strong detection in every compact portion of this window.

## 3. Proof of the limit, including domination

First assume lambda>0. In the r-component summand of Turn 1 equation (6), set

    x_j=s_j/sqrt(k), u=sum_j x_j, v=sum_j s_j.

On a compact subset of (0,infinity)^r, v=O(sqrt(k)). Taylor expansion with a uniform remainder gives

    log R(v)=−v(v−1)/k + O(v³/k²+v²/n) → −u².     (8)

The first error tends to zero because v=O(sqrt(k)); the second does so because k/n→0. Also

    rho_n^(s−1) s^s/s!
      ~ [e/sqrt(2π)] s^(−1/2) exp(−theta x),       (9)

uniformly for x=s/sqrt(k) in positive compact intervals. To see this, use Stirling and

    c_n^(1−s)e^s=c_n exp(−theta_n s/sqrt(k)),

while (1−c_n/n)^(s−1) tends uniformly to one in that range.

Since t=lambda_n k^(−1/4), each discrete component weight becomes

    [lambda e/sqrt(2π)] k^(−1/2)
           x^(−1/2) exp(−theta x).

The mesh in x is k^(−1/2). Therefore, for fixed r, the exact r-component summand tends to

    (lambda e/sqrt(2π))^r/r!
      integral_(0,infinity)^r exp(−(sum x_j)²−theta sum x_j)
                                product_j x_j^(−1/2) dx_j. (10)

The constraint sum s_j≤k becomes sum x_j≤sqrt(k) and disappears on every compact set. It cannot simply be dropped without control, so we now supply domination.

Take a fixed M bounding |theta_n| and a fixed bound on lambda_n. Turn 1's finite-population inequality gives

    R(v)≤exp(−v(v−1)/(2k))
         ≤product_j exp(−s_j(s_j−1)/(2k)).         (11)

Using s(s−1)≥s²/2 and the lower Stirling bound, the component majorant in the scaled variable is a constant times

    k^(−1/2) x^(−1/2) exp(Mx−x²/4).               (12)

This is integrable. The scaled sums over x<epsilon are bounded uniformly by a constant times sqrt(epsilon), since

    k^(−1/2) sum_(2≤s≤epsilon sqrt(k)) (s/sqrt(k))^(−1/2)
       ≤2 sqrt(epsilon).

The tails x>R tend uniformly to zero by the Gaussian factor in (12). On the remaining compact interval ordinary Riemann-sum convergence applies. This proves (10), including its integrable singularities at zero and its unbounded tails.

The component-majorant sums are uniformly bounded, so the r-th summand is at most B^r/r! for a fixed B. The tail sum over r is therefore uniformly negligible. This justifies interchanging the n-limit with the r-series, without assuming a fixed number of actual overlap components.

Finally the Dirichlet integral identity

    integral_(0,infinity)^r F(sum x_j) product_j x_j^(−1/2) dx_j
       =π^(r/2)/Gamma(r/2) integral_0^infinity u^(r/2−1) F(u) du

reduces (10) to (6). Substituting t=u² at theta=0 gives (7). The same domination proves finiteness of (6).

If lambda=0, the uniform near-e bound in Turn 1 gives E_P L²≤exp(C_M lambda_n)→1, which matches M(0,theta)=1. Thus the zero endpoint does not need a separate singular Riemann-sum argument.

## 4. Exact series checks and one-sided matching

Write M(lambda,0)=sum_(r≥0) A_r lambda^r, with A_0=1. Its coefficients satisfy

    A_(r+4)/A_r = e^4/[4(r+1)(r+2)²(r+3)(r+4)],  r≥0. (13)

For r≥1 this follows from the Gamma recurrence. At r=0 it follows directly from A_4=e^4/192. The first coefficients are

    A_1=e Gamma(1/4)/(2sqrt(2π)),
    A_2=e²sqrt(π)/8,
    A_3=e³Gamma(3/4)/(12sqrt(2π)).                 (14)

The four-step ratio proves absolute convergence for every lambda and supplies a simple tail majorant along the four residue classes. It is also checked independently against the Gamma expression.

For theta>0, discard exp(−u²) in (6) and integrate the remaining Gamma integral to obtain

    1≤M(lambda,theta)≤exp(lambda e/sqrt(2theta)).   (15)

This agrees with the one-sided shrinking upper bound as the mean degree moves above e. It is not a matching total-variation statement.

## 5. Sharpness as an L² scale at c=e

Turn 1 already gives E_P L²→1 when k=o(n^(4/9)). Equations (5)–(7) show a finite nontrivial second moment when k^(9/4)/n tends to a positive constant. The remaining assertion is

    E_P L²→infinity if k^(9/4)/n→infinity,
    c=e, k→infinity, 2k≤n.                        (16)

Keep just the one-component terms in the exact positive forest sum, with ceil(sqrt(k))≤s≤floor(2sqrt(k)). For all sufficiently large k,

    R(s)≥exp(−8).

Indeed n^s/(n)_s≥1, and log(1−x)≥−2x for 0≤x≤1/2 bounds the other product. Also (1−e/n)^(s−1)≥1/2 uniformly in this range because 2k≤n. The upper Stirling bound then gives

    rho^(s−1) s^s/s! ≥ C s^(−1/2)

for a universal constant C>0. Summing over at least a fixed positive multiple of sqrt(k) such integers proves

    E_P L²−1 ≥ C' (k²/n) k^(1/4)
             = C' k^(9/4)/n,                     (17)

and hence (16).

Therefore n^(4/9) is the **exact threshold scale for L² convergence of this likelihood to 1 at c=e**. This is deliberately not called the detection threshold. Above this scale the second moment may be dominated by rare observations; an appropriate higher-moment or truncated-likelihood argument is still absent.

## 6. What is and is not implied for testing

When (4) has finite limits, E_P L² is bounded, so strong detection is impossible. More quantitatively, if R_* is the optimal sum of type-I and type-II errors, then

    R_*=E_P min(1,L) ≥1/[1+E_P L²].               (18)

For a direct proof, apply Cauchy–Schwarz to L as the product of sqrt(min(1,L)) and L/sqrt(min(1,L)); the second factor's squared expectation is at most E_P(L+L²)=1+E_P L². The value at L=0 is interpreted by continuity.

For lambda=0, the stronger conclusion TV→0 follows from Turn 1. For lambda>0, a finite limit M>1 does **not** by itself imply nonvanishing TV. Second moments need not be uniformly integrable merely because they are bounded. Nor does divergence in (16) establish a successful test. The original c_h-to-e gap and the actual critical information window remain open.

A concrete next route is to seek higher-moment uniform integrability or to truncate atypical observations in the likelihood. Another is a richer constructive statistic than the first boundary count along a path. Both require new proof work and are not consequences of the present limit.
