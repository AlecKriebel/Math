# Independent probability and asymptotic derivation

This derivation addresses the probability/asymptotic mechanism in the original candidate at assigned head efc3f35a72543ad9ae76fd31a860116f1ffd4a32. It was developed independently before and after a sealed first assessment. Author diagnostics are not used as proof. Write q=3/4 and r=1/4.

## 1. Scope, definitions, and falsifiable success criterion

The source starts with either digit with probability 1/2, keeps its current digit with probability q, and switches with probability r. Samples are independent strings. For a prefix w of length d, its cylinder mass is pi(w); pi(empty)=1. Every mass at depth d>=1 is at most (1/2)q^(d-1). Partitioning a unit interval by these conditional probabilities provides a monotone map h from uniform coordinates into strings, away from the countable set of endpoints. The coordinate of a sample is uniform, and coordinates preserve lexicographic order.

For a path s, let L_d(s) be its sampled prefix count and m(s)=sum_{d>=0}pi(s|d). The exact operational cost is Z_n(s)=sum_{d>=0} L_d(s) 1[L_d(s)>1]. Rank cost is Y_n(k)=Z_n(h(U_(k))). This model correspondence was independently verified in the primary manuscript, equations (2)-(3), printed page 3; the profile definitions were checked on printed page 4. It is also the stopping rule used by the independent operational implementation.

Success means proving that one fixed nonboundary t admits two deterministic cost bands, each with probability bounded away from zero, whose separation divided by sqrt(n) diverges along an integer subsequence. This yields failure of tightness after every deterministic centering. A process tightness claim alone, a changing t, a data-dependent center, or finite numerical agreement would fail this criterion.

## 2. A deterministic uniform cost lemma

Let D be the supremum discrepancy of a sample empirical CDF against the uniform CDF. If no sample lies at a cylinder endpoint, every cylinder I=[a,b) satisfies

    |L(I)-n|I|| <= 2nD.

This is a difference of two empirical-CDF discrepancies. Cylinder endpoints form a countable set, so all n uniforms avoid them simultaneously with probability one. The same statement holds with alternate endpoint assignments on that event.

Suppose no pair of strings has a common prefix of length H. Then all depth-H counts are at most one, and no descendant can contain more samples. In particular Z_n(s) has no charged terms at depths d>=H, for every path s. For every nonnegative integer L,

    L 1[L>1] - L = -1[L=1].

Thus singleton removal incurs at most H over the H retained depths. This is the exact step where summing an infinite untruncated prefix count would be invalid: the selected string belongs to its own singleton cylinder forever. The finite stopping event removes that difficulty.

The remaining deterministic mean tail satisfies

    sum_{d>=H} pi(s|d) <= (1/2) q^(H-1)/(1-q) = 2q^(H-1).

Consequently, simultaneously for all paths,

    |Z_n(s)-n m(s)| <= 2nHD + H + 2nq^(H-1).                 (A)

No relation or independence between s and the sample is needed. Taking s=h(U_(k)) is therefore justified.

## 3. Probability of the uniform lemma event

For a Bernoulli variable X of arbitrary parameter p, the centered cumulant K(lambda)=log E exp(lambda(X-p)) has K(0)=K'(0)=0 and K''(lambda)=p_lambda(1-p_lambda)<=1/4. Integration gives K(lambda)<=lambda^2/8. Applying Markov's inequality to n independent copies and choosing lambda=4 epsilon gives

    P(|n^(-1) sum X_i-p|>epsilon) <= 2 exp(-2n epsilon^2).

At the n^2+1 grid points a/n^2, choose epsilon=sqrt(2 log(n)/n). The union failure probability is at most 2(n^2+1)n^(-4)<=4n^(-2). Between successive points the empirical CDF is monotone, and subtracting x loses at most the grid mesh. Therefore

    D <= d_n := sqrt(2 log(n)/n)+n^(-2)

except with probability at most 4n^(-2). This interpolation uses both one-sided inequalities; omitting the mesh gives a false claim.

For two independent strings, their common length-H prefix probability is sum_w pi(w)^2. A useful independent strengthening for this symmetric source is

    sum_{|w|=H} pi(w)^2 = (1/2)(q^2+r^2)^(H-1)
                           = (1/2)(5/8)^(H-1).

The first symbols coincide with probability 1/2; conditional on a common symbol, two independent transitions continue to coincide with probability q^2+r^2. The candidate's looser bound (1/2)q^(H-1) is therefore valid. A pair union bound, with no assumption about independence among pairs, gives a collision probability at most n^2 q^(H-1)/4.

With H_n=ceil(5 log(n)/log(4/3))+1, q^(H_n-1)<=n^(-5). Let G_n be the endpoint-avoidance, small-CDF-discrepancy, and collision-free event. Then

    P(G_n^c) <= 4n^(-2)+(4n^3)^(-1),
    R_n := 2nH_n d_n+H_n+2n^(-4)

is a valid bound in (A) on G_n. In particular R_n=O(sqrt(n)(log(n))^(3/2)). A bound less than zero for the displayed lower probability at very small n is harmless; only its approach to one is used.

For completeness, the supremum itself can be made measurable. With probability one, the finite sample contains no duplicate infinite strings, hence some finite random H separates every pair. On that event Z_n is a finite sum of continuous cylinder functions on the compact binary path space; m is continuous by its uniformly convergent tail bound. Their absolute difference has a supremum over a fixed countable dense path set. The later proof also avoids the supremum entirely by applying (A) pointwise on a single measurable event.

## 4. Rank geometry and a genuine nonboundary continuity point

Define v's ones at positions j^2 for j>=2. Let W_j be its prefix ending at position j^2-1. Its j-2 isolated earlier ones contribute 2j-4 switches among j^2-2 transitions; the other j^2-2j+2 transitions preserve the digit. Therefore

    P_j=pi(W_j)=(1/2)r^(2j-4)q^(j^2-2j+2),
    P_2=9/32,
    P_(j+1)/P_j=r^2 q^(2j-1).                             (B)

W_j ends in zero. The left sibling mass when v next chooses one is qP_j. Its fixed coordinate t is therefore sum_{j>=2}qP_j. In particular 0<t<pi(000)=9/32<1. Infinite zeros and ones preclude eventual constant tails, so t is strictly inside every cylinder containing v and is not any cylinder endpoint.

After any shared nonempty prefix w, each mean continuation sum is in [0,3pi(w)], because subsequent masses decrease by at most q per level. Hence the difference of the two continuation sums is at most 3pi(w), not twice that value. For every finite prefix of v, sufficiently nearby coordinates share that prefix, and pi(v|d) tends to zero. This proves continuity of m composed with h at t, despite the sequence of nearby jumps.

Let tau_j be the common coordinate of W_j0 111... and W_j1 000.... Let C_j=sum_{d=0}^{j^2-1}pi(v|d). Summing the continuation geometric series gives

    A_j=m(W_j0 111...)=C_j+P_j q[1+r/(1-q)]=C_j+(3/2)P_j,
    B_j=m(W_j1 000...)=C_j+P_j r[1+r/(1-q)]=C_j+(1/2)P_j.

Thus A_j-B_j=P_j. The coordinate tau_j is sum_{i=2}^j qP_i. The path v is strictly within the cylinder W_j1 0^(2j), whose left endpoint is tau_j and whose mass is

    P_j r*r*q^(2j-1)=P_j q^(2j)/12.

It follows that 0<t-tau_j<P_j q^(2j)/12. This is a cylinder-containment bound, not a limit inferred from the first few terms of an infinite series.

## 5. A subsequence with negligible cost error and explicit rounding bounds

Set w_j=P_j q^j, K_j=floor(j/2), n_j=ceil(w_j^(-2)). Exact rounding gives

    1 <= n_j w_j^2 < 1+w_j^2,
    sqrt(n_j)P_j >= q^(-j).

Since w_j tends to zero, sqrt(n_j)w_j tends to one. Equation (B) implies w_(j+1)/w_j=q^(2j)/16; the integers n_j increase strictly and tend to infinity.

At each depth, transition probabilities are at least 1/4. The conservative lower mass bound P_j>=4^(-(j^2-1)) and q^j>=4^(-j) imply

    n_j <= 2*16^(j^2+j-1),
    log(n_j)<3(j^2+j).

Using log(4/3)>1/4, H_(n_j)<=20 log(n_j)+2<=122j^2. Also sqrt(2 log(n_j))<=4j. Since n_j>=w_j^(-2) and P_j<=1/2, termwise division of R_n by nP yields the following explicit bound:

    R_(n_j)/(n_j P_j)
       <= 976j^3 q^j + 61j^2 q^(2j)
          +(61/2)j^2 q^(4j) + q^(10j)/256.                (C)

The four terms respectively bound the CDF square-root contribution, H/(nP), the grid-mesh contribution 2H/(n^2P), and the deterministic tail 2/(n^5P). For example, 1/(sqrt(n_j)P_j)<=q^j; H/(n_jP_j)<=122j^2 P_j q^(2j)<=61j^2q^(2j).

Define e_j to be the right side of (C) plus q^K_j. Every term tends to zero. There is also an explicit all-large-index certification: the exact rational value e_80 is less than 1/8 (approximately 0.050548382289126746). For j>=10, q(1+1/j)^3<=q(11/10)^3<1, so j^3q^j decreases; the j^2q^(2j) and j^2q^(4j) terms similarly decrease for j>=4. The remaining terms are nonincreasing. Therefore e_j<1/8 for every j>=80. The rational diagnostic checks the base value; these inequalities certify all larger indices.

The adjacent cylinders W_j0 1^K_j and W_j1 0^K_j have lengths P_j q^K_j/4 and P_j q^K_j/12, ending and starting at tau_j respectively. For j>=80, 12q^(j-K_j)<1, so the coordinate windows (tau_j-w_j,tau_j) and (tau_j,tau_j+w_j) fit. Their endpoint mean errors are bounded by 3P_jq^K_j/4 and P_jq^K_j/4, hence each is at most P_jq^K_j. Finally,

    (t-tau_j)/w_j < q^j/12 -> 0,
    sqrt(n_j)(t-tau_j) -> 0.                             (D)

The latter follows by multiplying by sqrt(n_j)w_j, which tends to one; no independent choice of a drifting target rank occurs.

## 6. Triangular binomial CLT with moving endpoints

Here is a direct justification of the only asymptotic distribution step. Suppose p_n tends to t in (0,1). With sigma_n^2=p_n(1-p_n), let X_(n,i) be independent Bernoulli(p_n) variables. For fixed u, Taylor expansion and |X_(n,i)-p_n|<=1 give, uniformly for large n,

    E exp(iu(X_(n,i)-p_n)/sqrt(n sigma_n^2))
      =1-u^2/(2n)+O(n^(-3/2)).

Raising to the nth power, taking logarithms, and using sigma_n bounded away from zero show that the characteristic function of the normalized binomial sum tends to exp(-u^2/2). The characteristic-function convergence theorem supplies the standard normal limit. This establishes the triangular version directly; a CLT for fixed Bernoulli parameter alone is not being silently substituted.

Let k_n=floor(nt)+1, and let x_n=t+z_n/sqrt(n), where z_n tends to a finite z. Then x_n tends to t and stays in (0,1) eventually. The exact order-statistic identity is

    P(U_(k_n)<=x_n)=P(Bin(n,x_n)>=k_n)
                  =1-P(Bin(n,x_n)<=k_n-1).

The standardized lower-tail threshold is

    (k_n-1-nx_n)/sqrt(n x_n(1-x_n)) -> -z/sqrt(t(1-t)),

because k_n-1=floor(nt) differs from nt by less than one. Normal continuity therefore gives the limit Phi(z/sqrt(t(1-t))). This also proves the order-statistic CLT and permits moving endpoints rather than only fixed z.

Along n_j, (D) and the width rounding show that the scaled endpoints tau_j-w_j, tau_j, tau_j+w_j tend to -1,0,1 relative to t. The selected uniform has a continuous distribution, so open/closed boundary distinctions add no probability. Each one-sided window consequently has probability tending to

    rho=Phi(1/sqrt(t(1-t)))-1/2>0.

Since sqrt(t(1-t))<=1/2, rho>=Phi(2)-1/2. An orientation value is about 0.4924021556; this decimal is not evidence for the limiting assertion.

## 7. Dependence, deterministic bands, and the quantifiers of non-tightness

Define E_j^- and E_j^+ by the two coordinate windows. On E_j^- intersect G_(n_j), the cost lemma and local mean control yield

    |Y_(n_j)(k_(n_j))/n_j-A_j| <= P_j e_j < P_j/8

for j>=80. The analogous relation holds around B_j on E_j^+ intersect G_(n_j). A dependence-free union estimate gives

    P(E_j(sign) intersect G_(n_j))
       >=P(E_j(sign))-P(G_(n_j)^c)=rho-o(1).

Here sign means either plus or minus. No product estimate or conditional independence is used. Indeed E_j and G_n depend on the same uniforms, so independence would require proof and in general is false.

It follows that each deterministic interval

    J_j^-=n_j[A_j-P_j/8,A_j+P_j/8],
    J_j^+=n_j[B_j-P_j/8,B_j+P_j/8]

contains the cost with probability at least rho-o(1). The interval distance is (3/4)n_jP_j. Its quotient by sqrt(n_j) diverges at least as (3/4)q^(-j).

Fix any finite radius M>0. For all sufficiently large j, every interval of length 2M sqrt(n_j) can intersect at most one of J_j^- and J_j^+. For any center a, one complete band is disjoint from [a-M sqrt(n_j),a+M sqrt(n_j)] and has probability at least rho-o(1). The same error bound holds for every center, yielding

    limsup_j sup_{a in R} P(|Y_(n_j)(k_(n_j))-a|<=M sqrt(n_j))<=1-rho.

Now choose any deterministic sequence c_n and epsilon=rho/2. For every finite M, arbitrarily large j satisfy

    P(|(Y_(n_j)(k_(n_j))-c_(n_j))/sqrt(n_j)|>M)>epsilon.

This is exactly the negation of tightness; it rules out weak convergence to any real-valued distribution. It remains valid even when c_n is chosen after knowing the deterministic bands, including c_n equal to the expectation. A random center that depends on the sample is outside the quantified claim.

## 8. Limits of verification and surviving boundary cases

- For every fixed n the cost is integrable: it is at most n times one plus the maximum common-prefix length among finitely many pairs, whose tail is bounded by a finite multiple of (5/8)^d. Thus centering by the expectation really is a deterministic real center.
- n=1 has cost zero; all high-probability estimates are stated for n>=2 and the subsequence is much larger.
- t is fixed and interior. The normal approximation does not apply uniformly as t approaches 0 or 1, and no such claim is made.
- K_j>=1 for j>=2. Window inclusion is deliberately deferred to sufficiently large j; the explicit bound above establishes j>=80, rather than falsely requiring small-index inclusion.
- The exact ceiling and rank-floor inequalities are preserved; replacing ceil(n_j) by an approximate floating integer or dropping the rank's plus one is unnecessary and potentially wrong.
- A mean profile continuous at t can still have this obstruction: vanishing nearby jumps remain large compared with the sample's sqrt(n)-scale cost fluctuations along specially chosen indices.
- All finite diagnostics are falsification controls. The all-index conclusions come from the exponential probability bounds, explicit envelope and monotonicity, characteristic-function limit, and uniform band geometry.

Strongest verified result: the exact original fixed-rank, every-deterministic-centering non-tightness theorem survives this independent probability/asymptotic adversarial review. No unfilled mathematical gap remains in this assigned mechanism. This does not establish historical priority or classify every nonboundary rank.
