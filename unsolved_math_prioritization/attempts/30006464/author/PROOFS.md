# Authored partial results and precise gap

## 0. Target and conventions

Fix an integer weight k >= 2, with trivial nebentypus on Gamma_0(N). Odd k has the zero space. Write

    f(z) = sum_{n>=1} a_f(n) n^((k-1)/2) exp(2 pi i n z),
    H_N(f) = integral_{Gamma_0(N)\H} |f(z)|^2 y^(k-2) dx dy,
    S_f(X) = sum_{1<=n<=X} |a_f(n)|^2.

The target asks, for each epsilon > 0, for C,K depending only on k,epsilon, such that H_N(f) <= K S_f(C N^(1+epsilon)) simultaneously for all N and every f in the entire cusp space. No Hecke, newform, or Atkin-Lehner eigencondition is allowed. Let I_N=[SL_2(Z):Gamma_0(N)]=N product_{p|N}(1+1/p).

The OWR source is printed p. 2756; it announces a squarefree Atkin-Lehner-eigenfunction case. Assing--Li--Wang--Xia Theorem 3.5 proves the general exponent 2+epsilon. Their norm is H_N/I_N and their Fourier coefficient is b_f(n)=n^((k-1)/2)a_f(n); multiplying their theorem by I_N produces the bound in these conventions. These are prior results, not results of this report.

## 1. The exact finite-frame formulation

Choose any H_N-orthonormal basis e_1,...,e_d and let A_X have entry (n,j)=a_{e_j}(n), for 1<=n<=floor(X). If f=sum c_j e_j, then

    H_N(f)=c* c,    S_f(X)=c* (A_X* A_X)c.

Thus a uniform detection inequality is equivalent to a uniform positive lower bound for the least eigenvalue of the Hermitian Gram matrix A_X* A_X. If floor(X)<d, rank-nullity gives a nonzero form with all sampled coefficients zero.

The classical Sturm/valence bound makes A_B injective at B=floor(k I_N/12). For fixed N this implies a positive least eigenvalue, hence some level-dependent constant. It supplies no quantitative uniform lower bound. For example, the injective abstract maps diag(1,t) have lower Gram eigenvalue t^2 tending to zero. This is a linear-algebra warning, not a modular-form counterexample. The full problem remains the smallest-eigenvalue estimate, not mere detection of nonzero forms.

## 2. Exact oldform scaling and a genuine obstruction to epsilon=0

Let g=Delta be the level-one weight-12 cusp form with raw coefficients tau(m), tau(1)=1. Put lambda(m)=tau(m)/m^(11/2), and f_N(z)=g(Nz). These are genuine trivial-character oldforms in S_12(N).

For A=diag(N,1), use the determinant-normalized slash operator: g|_12 A=N^6 g(Nz). Conjugation gives A Gamma_0(N) A^(-1)=Gamma^0(N). Changing variables in the Petersson integral, and then using its index I_N in SL_2(Z), proves

    H_N(f_N)=N^(-12) I_N H_1(g).

Its normalized Fourier coefficients vanish unless N divides n, and

    a_{f_N}(Nm)=N^(-11/2) lambda(m),
    S_{f_N}(X)=N^(-11) sum_{m<=X/N}|lambda(m)|^2.                 (2.1)

Consequently, whenever the denominator is nonzero,

    H_N(f_N)/S_{f_N}(X)
      = product_{p|N}(1+1/p) H_1(g) / sum_{m<=X/N}|lambda(m)|^2. (2.2)

For every fixed C>=1, setting X=CN freezes the denominator at a finite positive number. Take N to be the product of all primes <=r. Then P(N)=product_{p<=r}(1+1/p) is unbounded. Here is an elementary proof, requiring no prime number theorem:

    P(N)= product_{p<=r}(1-1/p^2) product_{p<=r}(1-1/p)^(-1)
         >= (1/2) sum_{m<=floor(r)} 1/m.

The first product is at least product_{n=2}^{floor(r)}(1-1/n^2)>1/2. The second Euler product contains every positive integer <=r among its nonnegative reciprocal terms. The harmonic sums diverge.

Thus there are no constants C,K valid for all N with H_N(f)<=K S_f(CN), even at k=12. If C<1, (2.1) already gives a zero sum. Cutoffs below N also fail for f_N. This is a counterexample only to the stronger epsilon=0 or sublinear variant, never to the requested positive-epsilon statement.

## 3. Positive-epsilon detection holds uniformly on all extreme Delta dilates

We now prove, without a Rankin--Selberg asymptotic or Deligne bound, that for every epsilon>0 and all N>=1,

    H_N(c Delta(Nz)) <= H_1(Delta) max(1,8 log(2)/(3 epsilon))
                         S_{c Delta(Nz)}(4 N^(1+epsilon)).      (3.1)

The c=0 case is trivial, and a nonzero scalar cancels. The classical Hecke relation gives real lambda(p) and

    lambda(p^2)=lambda(p)^2-1.

For t=lambda(p)^2>=0,

    |lambda(p)|^2+|lambda(p^2)|^2
      = t+(t-1)^2 = (t-1/2)^2+3/4 >=3/4.                   (3.2)

All indices p,p^2 are distinct as p ranges over primes. Therefore for T>=1,

    sum_{m<=T}|lambda(m)|^2 >= 1+(3/4) pi(sqrt(T)).           (3.3)

Bertrand's theorem, one prime per successive dyadic interval, gives pi(x)>=floor(log_2 x) for x>=2. With T=4 N^epsilon this implies

    sum_{m<=T}|lambda(m)|^2 >= 1+(3 epsilon/(8 log 2))log N. (3.4)

On the other hand,

    P(N)=sum_{d|rad(N)}1/d <= sum_{d<=N}1/d <=1+log N.      (3.5)

Insert (3.4)--(3.5) in (2.2). The inequality
(1+u)/(1+a u)<=max(1,1/a), for u>=0,a>0, proves (3.1).

This controls a separately specified one-dimensional family for every level, not its entire oldspace, not arbitrary mixtures of dilates, and not the entire cusp space. The constant H_1(Delta) is a fixed positive number. No claim of novelty is made.

## 4. Two invalid shortcuts, with exact countermodels

### 4a. Orthogonal source blocks do not prevent coefficient cancellation

On C^2 with its standard norm take the orthogonal involution W=diag(1,-1). The sampling map T(x,y)=x+y has norm one on each W-eigenline but annihilates (1,-1). Accordingly, summing lower estimates for separate Atkin-Lehner eigenspaces does not bound S_f(X) below for their sum. The truncated coefficient Gram matrix must control cross terms. This toy map is not asserted to arise from a modular form.

### 4b. A low-height cusp-tail bound cannot be extrapolated to 1/N

The arithmetic cusp sum that occurs in the cited proof is

    sum_{v|N} [N v^2/gcd(v^2,N)] phi(gcd(v,N/v)) = N I_N.

Removing v=N leaves R(N)=N I_N-N^2; R(p)=p for a prime. These identities do not by themselves yield a uniform geometric bound Vol(F_N intersect {y<Y})<=2YR(N) throughout Y~1/N.

Here is an exact domain test at p=101. Let F be the usual SL_2(Z) domain and form the standard Gamma_0(p) domain from the distinct left-coset representatives 1 and S T^j (0<=j<p). For j=26,...,49, consider the rectangles

    z'=x'+iy',  j-1/2 <= x' <= j+1/2,  1<=y'<=2

inside T^j F. Their S-images belong to distinct tiles of F_p, up to null boundaries, and

    Im(S z')=y'/((x')^2+(y')^2) <= 2/(51/2)^2=8/2601<1/101.

Their total hyperbolic area is 24 integral_1^2 y'^(-2)dy'=12. Thus

    Vol(F_p intersect {y<1/p}) >=12>2=2(1/p)R(p).

Translate tiles by integers if a strip representative is desired; heights and areas are unchanged. This disproves the proposed unrestricted extrapolation for this legitimate domain. It neither disproves the cited theorem at its much smaller heights nor rules out a more carefully chosen domain or a mass estimate using f. Obtaining a uniformly valid bound in the needed height range is an additional proof obligation. No prime-level theorem is claimed from this calculation.

## 5. An equivalent analytic remaining target: uniform horostrip observability

For 0<Y<=1 let

    J_f(Y)=integral_0^1 integral_Y^infinity |f(x+iy)|^2 y^(k-2)dy dx.

Parseval and Tonelli, applied first to finite sums and then by the usual convergence of cusp expansions at positive height, give

    J_f(Y)=sum_{n>=1}|a_f(n)|^2 W_k(nY),
    W_k(t)=Gamma(k-1,4 pi t)/(4 pi)^(k-1).                 (5.1)

The whole positive-epsilon question is equivalent to the following family of estimates: for every eta>0 there exist D,c>0, depending only on k,eta, such that

    J_f(D N^(-1-eta)) >= c H_N(f)                           (5.2)

for every N and f. One may shrink D to ensure D<=1, since J is decreasing.

**Detection implies (5.2).** Take Y=(C N^(1+eta))^(-1), enlarging C>=1. For n<=1/Y, W_k(nY)>=W_k(1)>0, hence (5.1) bounds J below by W_k(1) S_f(1/Y).

**(5.2) implies detection.** A deliberately coarse consequence of the general coefficient estimate in Assing--Li--Wang--Xia (3.2), after norm conversion and use of d<<_k N log log(3N), is

    |a_f(n)|^2 <= A_k N^3 n H_N(f).                        (5.3)

Indeed use its parameter 1/2 and I_N>=N; enlarge constants for small N. The incomplete gamma expression for integer k>=2 gives W_k(t)<=B_k exp(-2 pi t). Consequently, for X>=1 and 0<Y<=1,

    sum_{n>X}|a_f(n)|^2 W_k(nY)
      <= E_k N^3 Y^(-2) exp(-pi X Y) H_N(f).               (5.4)

To check this, split exp(-2pi nY) into two factors, bound one by exp(-pi XY), and sum n exp(-pi nY)<=constant Y^(-2).

Given epsilon, apply (5.2) with eta=epsilon/2. Put Y=D N^(-1-eta) and X=A Y^(-1)log(2N/Y). By taking A sufficiently large depending on k,c,D, the factor in (5.4) is <=c/2 for all N: for pi A>=6 it is at most E_k 2^(-pi A) N^(3-pi A)Y^(pi A-2). The tail is then absorbed in (5.2), and W_k(t)<=W_k(0) bounds the remaining sum above. Finally log(2N/Y)<<_{D,epsilon} N^(epsilon/2), so X<=C_{k,epsilon}N^(1+epsilon). This proves the equivalence.

J_f(Y) integrates a horizontal strip, which may cover portions of the quotient more than once. It is not asserted to be bounded above by H_N(f). Only the specified lower estimate is needed.

## Final gap

No uniform least-Gram-eigenvalue bound from section 1, or equivalent horostrip lower bound (5.2), is proved for all forms and all levels. The oldform theorem controls only c Delta(Nz); the geometric and cancellation examples reject shortcuts. Thus the original target is **unresolved after five approaches**. The known exponent-2 result and the announced restricted squarefree result retain their original attribution.
