# Precision addendum for short coefficient detection

This separately authored addendum leaves the frozen author packet unchanged. It clarifies one harmless endpoint convention and supplies details useful for checking the accepted partial arguments. It does not solve the all-forms problem.

## Zero dimensional spaces

**Operative correction:** interpret Section 1 of the frozen proof with the two replacements in GRAM_ZERO_DIMENSION.patch. CORRECTION.json binds the exact original proof, corrected proof, patch, author archive, and author manifest. The patch is applied only to a separate copy, resealed, and actually replayed under normal and optimized Python and the author's relocation/mutation suite; the resulting evidence is in AUDIT_RESULTS.json. The unchanged author freeze is retained alongside this correction.

In the Gram formulation, discuss the least eigenvalue only when d=dim S_k(N)>0. When d=0, the desired inequality is vacuous, and the equivalent statement is the quadratic-form inequality A_X* A_X >= K^(-1) Id on the zero vector space. That statement remains meaningful. This also covers even weights and small levels whose cusp space vanishes, besides the odd weights already mentioned. A zero form satisfies every displayed detection inequality without division by its norm.

## Why the oldform result needs no Deligne bound

The product expansion of Delta has real integer coefficients. Since S_12(1) is one dimensional and Hecke operators preserve it, Delta is a normalized Hecke eigenform. Comparing the coefficient of q in T_n Delta gives its eigenvalue tau(n). The relation T_p^2=T_(p^2)+p^11 therefore gives tau(p^2)=tau(p)^2-p^11. Dividing by p^11 gives lambda(p^2)=lambda(p)^2-1 with real lambda(p).

For t=lambda(p)^2, the polynomial t+(t-1)^2 has minimum 3/4 at t=1/2. No upper bound on t enters. Neither Deligne's theorem, a Rankin--Selberg asymptotic, nor a nonvanishing assertion for individual tau(p) is required for this partial result. This observation does not remove the separately cited analytic input in the horostrip argument.

For real x>=2, put L=floor(log_2 x). The prime 2 together with one prime in each interval (2^j,2^(j+1)), 1<=j<L, gives at least L distinct primes <=x. For x=2 N^(epsilon/2), L=floor(1+epsilon log N/(2 log 2)) is at least epsilon log N/(2 log 2). This is an all-N argument, including N=1. It proves the stated logarithmic slope without an unmentioned asymptotic exception.

## Uniform coefficient and tail constants

Write b_f(n)=n^((k-1)/2)a_f(n), H=H_N(f), and I=I_N. The cited coefficient estimate with its auxiliary parameter delta=1/2 yields

    |a_f(n)|^2 <= C_k d N^2 n H/I.

Using I>=N, d<=C'_k N log log(3N), and log log(3N)<=C'' N gives the author's coarse bound A_k N^3 n H uniformly for N>=1. All constants depend only on k. Alternatively the valence bound gives d<=floor(kI/12), yielding an even stronger coarse N^2 bound; the proof does not need that improvement.

Let m=k-1>=1. With the convention 0^0=1, define

    B_k = (m-1)!/(4 pi)^m * sum_{j=0}^{m-1} (2j/e)^j/j!.

The integer incomplete-gamma expansion and max_(t>=0) t^j exp(-2 pi t)=(j/(2 pi e))^j imply W_k(t)<=B_k exp(-2 pi t). Also

    sum_{n>=1} n exp(-pi nY)
      = 1/[4 sinh^2(pi Y/2)] <= 1/(pi^2 Y^2).

Thus the author's tail estimate holds with E_k=A_k B_k/pi^2. Given the horostrip constants D,c at eta=epsilon/2, first replace D by min(D,1). Choose q>=6 with E_k 2^(-q)<=c/2 and set A=q/pi. The quantity X=A Y^(-1) log(2N/Y), Y=D N^(-1-eta), is >=1. Its tail factor satisfies

    E_k N^3 Y^(-2) exp(-pi XY)
      = E_k 2^(-q) N^(3-q) Y^(q-2) <= c/2.

The last inequality holds for every N>=1 and 0<Y<=1, without a finite-exception argument. Since log N<=N^eta/(e eta),

    X <= [A/D * (log(2/D)+(2+eta)/(e eta))] N^(1+epsilon).

After subtracting the tail, cH/2<=W_k(0)S_f(X). This proves the reverse implication with K=2W_k(0)/c and the displayed cutoff constant. The constants D,c already depend only on k,eta. The conclusion is the equivalence of two families of assertions, each quantified over every positive exponent. It does not assert that a horostrip bound at one fixed eta gives detection at that identical exponent without logarithmic loss.

## Geometry and attribution

For p=101 the matrices 1 and ST^j, 0<=j<p, represent distinct left cosets of Gamma_0(p) in SL_2(Z): the lower-left entry of ST^j(ST^l)^(-1) is l-j. There are p+1 representatives, exactly the index. The rectangles used by the author have disjoint interiors inside their tiles. Hyperbolic invariance gives area 1/2 for each of the 24 rectangles after applying S. This proves the stated countermodel for that domain.

It does not establish that every possible fundamental domain has the same low-height area. In particular, this audit makes no claim that the published exponent-2 theorem is refuted, and no claim that an improved prime-level theorem follows merely by deleting the infinity-cusp term from an arithmetic sum.

The Hecke facts above can be checked in [William Stein's level-one chapter](https://wstein.org/books/modform/modform/level_one.html), Propositions 2.29 and 2.31 and Example 2.35. The independent analytic input is [Assing--Li--Wang--Xia](https://arxiv.org/pdf/2503.05685v1), equation (3.2). All derivations and additional constants in this addendum are authored calculations.
