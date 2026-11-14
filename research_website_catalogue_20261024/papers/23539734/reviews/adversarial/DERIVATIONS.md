# Independent adversarial derivations

UTC: 2026-11-14T23:37:27.505838+00:00. Completion estimate: 82% (mathematical audit and independent finite search complete; final provenance/seal pending).

## 1. Dynamics, boundaries, and point weights

Let a=u²+1. Over Q the maps (u,av) and (u,v/a) compose to the identity on a!=0. The orbit of (1,1) is (1,2^m), proving infinite order. A polynomial inverse cannot exist: over C the fibers u=±i collapse all v to zero, so the forward polynomial is noninjective. The invariant u has generic affine-line fiber, whose smooth projective model has genus zero.

For p=3 mod4, a never vanishes. On v!=0 a positive iterate fixes the point exactly when a^d=1; v=0 is always fixed. This gives periods dividing N=p-1. A proper divisor d of N has d<=N/2<p/2. If x>=1/2 and px<N, every proper-divisor period and every zero section is counted while precisely (p-1)P_p points of maximal period are excluded. Therefore D_p(x)=1-(p-1)P_p/p². At x=N/p these points enter, and the CDF equals 1. This is a genuine moving-boundary control, not a failure of the fixed-x theorem.

Smallest example p=3: multipliers are 1,2,2; periods have point histogram {1:5,2:4}. D_3(1/2)=5/9, D_3(3/4)=1, P_3=2. The primitive-exclusion expression is 5/9 and applies at 1/2; it must not be applied at 3/4 because p(1-x)>1 fails. The ramp moment is 4/27, equal to (1-2/3)(2*2/9). This falsifies an unqualified all-p/all-x identity but the published text explicitly imposes the needed cutoff.

For p=1 mod4, exactly two a's vanish; their v!=0 points enter a fixed zero section after one step and are nonperiodic themselves. Thus the full-plane map is not a permutation. Removing the two complete fibers leaves an invariant permutation domain. These are actual finite reduction facts, not a model assumption.

## 2. Primitive indicator without numerical characters

Choose a generator g, write a=g^k. For each prime l|N, the sum of order-l characters at a is l-1 if l|k and -1 otherwise. The squarefree-divisor sum in the published indicator factors over l. Its factor vanishes if l|k; otherwise multiplication by phi(N)/N cancels all factors l/(l-1). This proves the exact indicator for gcd(k,N)=1. Extending every character, including the principal one, by zero at a=0 correctly assigns zero to nonunits. The principal term is p theta in class 3 and (p-r)theta for all odd primes. No primality or sampling shortcut can replace those terms.

## 3. Independent norm proof bypassing Gauss sums

The paper uses Gauss and Jacobi sums. An independent exact double-sum proof attacks the same estimate. Let eta be quadratic and chi nonprincipal. Since the number of u with u²=a-1 is 1+eta(a-1),
S_chi=sum_{a!=0}eta(a-1)chi(a).
The constant term vanished because sum chi=0. Hence
|S_chi|²=sum_{t!=0}chi(t) C(t),
C(t)=sum_{b!=0}eta(tb-1)eta(b-1).
For t=1, C(1)=p-2. For t!=0,1, the quadratic in b has nonzero discriminant and leading coefficient t. The standard quadratic-character identity gives its complete sum -eta(t); removing b=0 subtracts 1. Thus C(t)=-eta(t)-1.

This quadratic identity has an elementary proof: after completing the square, sum_x eta(x²-c)=-1 for c!=0, because the equation y²=x²-c has exactly p-1 solutions, parametrized bijectively by (x-y)(x+y)=c (2 invertible). Therefore
|S_chi|²=(p-2)-sum_{t!=0,1}(chi eta)(t)-sum_{t!=0,1}chi(t).
The last sum is -1. If chi!=eta, the first sum is also -1, giving p; if chi=eta it is p-2, giving 1. This proves |S_chi|<=sqrt(p) for all nonprincipal chi at every odd p, and S_eta=-1 follows separately from sum_u eta(u²+1)=-1. No missed degree factor or inverse-character exception remains.

The independent verifier checks the formal group-ring Jacobi identity and all squared character magnitudes simultaneously through integer circular autocorrelations at all 53 odd primes <=251. If s_e counts u with nonzero u²+1=g^e, its autocorrelation has finite Fourier spectrum ((p-r)² at the principal character, 1 at the quadratic character, p at every other nonprincipal character). The exact coefficient prediction tested for each shift j is
sum_e s_e s_{e-j}=p*1_{j=0}+[(p-r)²-p+(1-p)(-1)^j]/(p-1).
This uses integers/rationals only and does not import a supplied checker.

Summing the indicator and applying the norm bound gives
|P_p-(p-r)theta_p|<=theta_p(2^{omega(N)}-1)sqrt(p).
Six primes below 16 cost <=64; each other prime l>=17 satisfies 2<=l^{1/4}, so 2^{omega(N)}<=64 N^{1/4}. In class 3,
|D_p(x)-(1-theta_p)|<=|P_p/p-theta_p|+P_p/p²<=64p^{-1/4}+1/p.
For all odd primes the principal correction r theta_p/p is <=2/p. These bounds are uniform in p, subject only to the explicit CDF cutoff in x.

## 4. Mean and incompatible subsequences

phi(n)/n=sum_{d|n}mu(d)/d, including n=1. Interchanging the finite sums gives the claimed prime mean identity including p=2. For K=(log X)^6 the absolute d>K contribution is <=X sum_{d>K}1/d²=O(X/K). Siegel-Walfisz at moduli d<=K gives summed error O(X log K/(log X)^4)=o(X/log X). The series sum_d1/[d phi(d)] converges because phi(d)>=sqrt(d/2), verified prime-powerwise: only 2^1 has phi(q^a)^2/q^a<1. The Euler product is therefore justified absolutely. Dividing by pi(X) gives A.

The product lower bound is literal: the odd-prime tail sum is <=sum_{n>=3,n!=4}1/[n(n-1)]=5/12, so A>=1/2*(1-5/12)=7/24>13/48. If theta<1/24 eventually on class 3, the two classes' limiting prime proportions and theta<=1/2 give global mean <=1/4+1/48=13/48, contradiction. This supplies an infinite high-theta class-3 sequence, not a positive-density assertion by itself.

For Q_j the product of the first j odd primes, r=1+2Q_j satisfies r=3 mod4 and r=1 modQ_j. It is coprime to 4Q_j. Dirichlet supplies arbitrarily large primes in each fixed class; choose them increasing with j. Then theta<=1/2 product_{l|Q_j}(1-1/l)->0. The bridge gives limsup D=1; the high-theta sequence gives liminf D<=23/24. Neither construction assumes the other sequence has positive density.

## 5. Atomless law and positive UPPER density

Let empirical measures lambda_X of b_p converge weakly to atomless nu. Suppose b_p->c on A and limsup A(X)/pi(X)=delta>0. For any epsilon>0 all but finitely many A-primes lie in I_epsilon=[c-epsilon,c+epsilon]. Atomlessness makes this a nu-continuity set, so its whole-prime frequency converges to nu(I_epsilon). Along endpoints realizing delta, the finite omitted set is negligible, giving delta<=nu(I_epsilon). As epsilon decreases to zero, continuity from above gives delta<=nu({c})=0. This defeats dense-block attempts, including sets whose lower density is zero. Compact boundedness ensures c is finite; the cited scalar is bounded in [0,1].

If A subset S has upper relative density delta, then A(X)/pi(X)=[A(X)/S(X)]*[S(X)/pi(X)], whose limsup is delta/2>0. Thus the whole-prime law suffices: a conditional class-3 law is not needed. With D=1-theta+o(1), CDF convergence would force scalar convergence.

The DH primary text, Proposition 2.1 and equation (2.1), applied to g(n)=phi(n)/n and m=2, explicitly supplies a continuous distribution on odd primes. The finite exception p=2 has zero limiting weight. AS primary formula (1.1) makes p_1(q)=phi(q-1)/(q-1); Theorem 1.3(i) asserts continuity, and Section 6 explicitly first proves it over primes and transfers to prime powers. Thus the exact atomless input needed here is supported; continuity must not be upgraded to absolute continuity. DH actually discusses singularity.

## 6. Weak convergence, deletion, and huge completions

For regular periods, h(d/p)=0 for proper d|N because d/p<1/2, while h(N/p)=1-2/p. Zero sections have d=1 and contribute zero for every odd p. Thus integral h dmu=(1-2/p)*(p-1)P_p/p² in class 3; on regular domains replace p² by p(p-r). Both equal theta+o(1). A weak limit of probabilities on [0,infinity) forces convergence of this globally bounded continuous test, hence of theta, contradicting the atomless argument. This avoids the invalid shortcut from CDF failure at a possible discontinuity to weak failure.

For R=p(p-r) and e<=rp retained exceptional points, alpha=e/(R+e)<=r/p. Whatever their finite nonnegative assigned periods, the completed measure is (1-alpha)mu_reg+alpha nu_exceptional. For 0<=f<=1 the integral change is <=alpha; for real bounded f it is <=2 alpha ||f||_infinity. The bounds hold for arbitrary mixtures, arbitrary p-dependent periods, and mass escaping to infinity. Only retained mass matters. Uniform regular-point weights and keeping every regular point are essential assumptions; the proposition explicitly imposes them.

## 7. Historical/source boundary and exact gap

The complete two-page Vivaldi primary body states the p-normalized, point-weighted CDF and a broad birational existence assertion. Genus-one curves enter the subsequent heuristic, so restricting this example to genus-zero does not evade that written assertion. It separately defines the p²-normalized prime average in Conjecture 2. The example is a polynomial forward map; the source's projective-plane convention for rational nonpolynomial forward maps does not obstruct its full affine class-3 domain. OS Section 2.1 contains the claimed older triangular family after swapping u,v. BCST Section 2 supports the primitive-indicator mechanism, and MP Lemma 2 at r=m=1 supports the mean. Roberts reference 9 establishes the disclosed unseen-preprint lead, without establishing its contents or novelty relationship.

No mathematical counterexample or unresolved proof gap was found in the stated claims. Historical firstness, novelty, or current problem status is not established by this review; the manuscript already disclaims those conclusions and retains the unresolved lead. The strongest verified result is the exact claimed theorem and supplementary conventions, conditional only on standard credited unconditional arithmetic inputs authenticated at their cited primary locations. Finite computations do not certify the infinite-prime conclusions.
