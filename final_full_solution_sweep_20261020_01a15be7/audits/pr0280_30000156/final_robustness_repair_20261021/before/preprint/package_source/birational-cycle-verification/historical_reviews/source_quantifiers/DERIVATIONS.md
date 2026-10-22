# Supplementary independent derivations

These are deductions from the fixed candidate map and the arithmetic inputs written in `original/PROOF.md`; they do not replace the proof or claim historical novelty.

## 1. Exact finite geometric diagnostic

Fix a prime p=3 mod 4 and N=p-1. For a divisor d of N define

`R_d = #{u in F_p : (u^2+1)^d=1}`.

Writing eta for the quadratic character, extended by eta(0)=0, a field element a has exactly `1+eta(a-1)` preimages under `u -> u^2+1`. The subgroup of dth roots of unity has exactly d elements. Consequently

`R_d = d + sum_{a^d=1} eta(a-1)`.

The fixed points of the dth iterate consist of all p points with v=0, together with p-1 nonzero-v points for every parameter counted in R_d:

`#Fix(L_p^d) = p + (p-1) R_d`.

Let `M_e=#{u:ord_p(u^2+1)=e}`. Since `R_d=sum_{e|d} M_e`, Mobius inversion gives

`M_e=sum_{d|e} mu(e/d) R_d`.

In particular `P_p=M_N`, `R_N=p`, and `R_1=M_1=1`. The last identity yields `#Fix(L_p)=2p-1`. The exact total number of cycles is

`p + (p-1) sum_{e|N} M_e/e`.

Every expression is an integer for the direct dynamical reasons above. Independent raw orbit-graph enumeration matches these formulas for the eight S-primes through 47, and exact order enumeration checks them for all 87 S-primes through 1000.

## 2. Bounded continuous witness against weak convergence

Let `mu_p=p^-2 sum_z delta_{T_p(z)/p}` and let h be the continuous clipped linear function

`h(t)=max(0,min(1,2t-1))`.

Any nonmaximal period is at most `(p-1)/2`, so h vanishes there. A maximal period is p-1, so h takes the value `1-2/p`. Exactly `(p-1)P_p` points have maximal period. Therefore

`integral h dmu_p = (p-2)(p-1)P_p/p^3`.

Set `theta_p=phi(p-1)/(p-1)`. The candidate's character estimate implies `P_p/p=theta_p+o(1)`, uniformly as p tends to infinity in S. The displayed expectation is thus `theta_p+o(1)`. CRT/Dirichlet gives a sequence with theta tending to zero, and the unconditional prime mean gives another with theta at least 1/24. Expectations of bounded continuous functions must converge under weak convergence. They do not here.

## 3. Nonconvergence cannot be repaired by density-zero deletion

All densities here are relative to the primes. The candidate proves an unconditional mean `E_X theta -> A` with `A>=7/24`, where `E_X` averages over primes p<=X. Let

`B={p=3 mod 4 : theta_p>=1/24}`,

and set `beta_X=#(B intersect [1,X])/pi(X)`. For odd primes, `theta_p<=1/2`. Outside B but inside S the ratio is below 1/24. Since both odd mod-4 classes have density 1/2,

`E_X theta <= 1/4 + 1/48 + (1/2-1/24) beta_X + o(1)`

`             = 13/48 + (11/24) beta_X + o(1)`.

Rearranging the inequality and taking the lower limit yields

`liminf beta_X >= (7/24-13/48)/(11/24) = 1/22`.

Thus B has lower density at least 1/22 among all primes, and at least 1/11 within S. This strengthens the candidate's assertion that B is infinite.

For every epsilon>0, choose a fixed finite product Q of odd primes so that

`(1/2) product_{ell|Q}(1-1/ell) < epsilon`.

The fixed reduced CRT progression `p=3 mod 4`, `p=1 mod Q` has positive prime density `1/phi(4Q)`. Every prime in it satisfies `theta_p<epsilon`. This is a whole positive-density progression for each fixed epsilon, rather than merely one chosen sequence of primes.

For a fixed x in [1/2,1), write `D_p(x)=1-theta_p+e_p`, where `e_p->0` along S. Take epsilon=1/192 above. The CRT progression eventually satisfies `D_p(x)>95/96` because `theta_p<1/192` and `|e_p|<1/192`. Meanwhile B eventually satisfies `D_p(x)<31/32` because `theta_p>=1/24` and `|e_p|<1/96`.

These two separated ranges each occur with positive lower density. For any proposed real limit, one of the ranges stays at distance at least 1/96 from it: use their midpoint `47/48`. It follows that the CDF values do not even converge in prime density, either among all reduction primes on which the statistic is completed or within S. Removing a prime-density-zero set cannot fix this.

This does not claim failure on **every** arbitrary positive-density refinement. That stronger quantifier is neither needed nor established here.

## 4. Endpoint and extension checks

The maximal normalized period is `1-1/p`; all proper periods are below 1/2. Therefore, for each p in S, the CDF is constant on `[1/2,1-1/p)` and becomes one at the right endpoint. For a fixed x<1 this plateau contains x eventually; at x=1 every point is counted for every p. At x=0 no positive period is counted. The behavior at moving thresholds is not used to infer a fixed-threshold limit.

For `q=p^n`, the polynomial `u^2+1` has no root precisely when q=3 mod 4, so for p=3 mod 4 the same everywhere-defined inverse condition holds when n is odd and fails when n is even. The original construction takes n=1 throughout. It does not mix growing extension degrees into the prime limit.
