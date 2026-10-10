# Function Theory 7.4: exact scope, known bounds, and five partial approaches

Problem: 2307004 / AMR-022-7004. Investigation date: 2026-10-05.

**Disposition: the sharp universal constant remains unresolved after five substantive approaches.** The results below are scoped partials and reconstructions of known methods. No novelty, priority, or full-resolution claim is made. No external review is claimed in this author packet.

## 1. Exact target and normalization

For every positive integer n, let z_1=1 and let z_2,...,z_n be arbitrary complex numbers, with repetitions and zero values allowed. Put S_k=sum_{j=1}^n z_j^k and M_n(z)=max_{1<=k<=n}|S_k|. The target is the supremum c_* of all real c for which M_n(z)>c for every such n and tuple. Equivalently,

c_* = inf_{n>=1} inf_{z_1=1} M_n(z).

The strict endpoint needs separate care: if the infimum is attained, c_* itself is not an admissible constant in the strict inequality. Determining the infimum and, if requested, endpoint admissibility would settle the problem. The source imposes no unit-disc restriction on z_2,...,z_n and no distinctness, realness, or conjugate-symmetry assumption. The exponent window is exactly 1,...,n, not 2,...,n+1.

Define R_n as the minimum of M_n over tuples with max_j|z_j|=1. This minimum exists by continuity on a compact set. In fact

R_n = inf_{z_1=1} M_n(z),

and the latter infimum is also attained by a tuple lying in the closed unit disc. To prove this, take a tuple with z_1=1, choose z_j of largest modulus R>=1, and set w_i=z_i/z_j. After reordering, w_1=1 and max|w_i|=1, while |sum_i w_i^k|=|S_k|/R^k<=|S_k|. This proves one inequality. Conversely, rotate and reorder any normalized tuple to place a maximal-modulus entry at 1 without changing any |S_k|. This proves the other inequality and attainment.

Thus c_*=inf_n R_n. This is not automatically the same as limsup_n R_n. No monotonicity or convergence of R_n is proved here. Adding a zero changes the exponent window and need not preserve a tuple's objective: z=(1,-3/10+i/2) has both first two sums of modulus below 9/10, but its third sum is 599/500+i/100, of modulus above 1.

For n=1, R_1=1. If the fixed-root normalization is omitted, the all-zero tuple has M_n=0.

## 2. Approach 1: solve the full complex two-point problem

**Theorem 1.** R_2=sqrt(3-sqrt(5)).

Write w=1+z_2, t=|w|^2 and x=Re(w). Then S_1=w and S_2=w^2-2w+2. Direct expansion gives

|w^2-2w+2|^2 = (t-2)^2/2 + 8(x-(t+2)/4)^2.                 (1)

Let t_0=3-sqrt(5) and r=sqrt(t_0). Since (2-t_0)^2/2=t_0 and 0<t_0<2, if |w|<r then (1) implies |S_2|>r. Therefore max(|S_1|,|S_2|)>=r for every complex z_2, without any modulus restriction.

For attainment choose x=(t_0+2)/4 and y=sqrt(t_0-x^2), and set w=x+i y and z_2=w-1. The quantity under the square root is positive: 3/4<t_0<4/5, while x<7/10, so t_0-x^2>3/4-49/100>0. Equation (1) gives |S_1|=|S_2|=r. Also |z_2|^2=t_0-2x+1=t_0/2<1. Thus this is a normalized admissible minimizer. Conjugation gives another minimizer.

This exact finite case gives an upper bound on c_* but cannot settle an infimum over unbounded n. It also rules out restricting an extremal search to real z_i.

## 3. Approach 2: phase geometry of Newton recurrence

We give a self-contained proof of the classical bound M_n>1/2. The result is known from Biró's work; the presentation below is an authored reconstruction, not an improvement.

Set

Q(t)=prod_{i=2}^n(1-z_i t)=sum_{j=0}^{n-1}b_j t^j,

with b_0=1 and b_n=0. Put C_j=sum_{h=0}^j b_h and B_j=sum_{h=0}^j|b_h|. Formal logarithmic differentiation, or Newton's identities, gives for 1<=j<=n

sum_{k=1}^j S_k b_{j-k}=C_{j-1}-j b_j.                  (2)

Suppose M_n<=1/2. Equation (2) implies

|C_{j-1}-j b_j|<=B_{j-1}/2.                             (3)

We claim |C_j|>=B_j/sqrt(2) for 0<=j<=n-1. It holds at j=0. If it holds at j-1, the disc in (3), centered at C_{j-1}, has radius at most |C_{j-1}|/sqrt(2). It avoids the origin and lies within angle pi/4 of the ray through C_{j-1}. Consequently b_j is nonzero and

Re(b_j conjugate(C_{j-1})/|C_{j-1}|)>=|b_j|/sqrt(2).

Projection onto this ray gives

|C_j|>=|C_{j-1}|+Re(b_j conjugate(C_{j-1})/|C_{j-1}|)
     >=(B_{j-1}+|b_j|)/sqrt(2)=B_j/sqrt(2).

This proves the induction. But (2) at j=n, using b_n=0, gives |C_{n-1}|<=B_{n-1}/2, contradicting B_{n-1}/sqrt(2)>B_{n-1}/2. The n=1 case is immediate. Hence M_n>1/2.

**Exact obstruction to a naive improvement.** A scalar invariant |C_j|>=gamma B_j together with the same disc/projection estimate can propagate under M_n<=q only if

sqrt(1-(q/gamma)^2)>=gamma,

or q^2<=gamma^2(1-gamma^2)<=1/4. Thus this particular invariant and estimate cannot certify any q>1/2. This is a limitation of the proposed argument, not a limitation on the actual optimum. Biró's 2000 proof gets beyond 1/2 by exploiting additional summed identities and near-equality geometry.

## 4. Approach 3: coefficient majorants and modulus obstructions

Write P(t)=prod_{i=1}^n(1-z_i t)=sum_{j=0}^n a_j t^j. Formally,

P(t)=exp(-sum_{k>=1} S_k t^k/k).

If |S_k|<=M for 1<=k<=n, the coefficientwise triangle inequality for the exponential gives

|a_j| <= d_j(M)=(M)_j/j!  (0<=j<=n),                  (4)

where (M)_0=1 and (M)_j=M(M+1)...(M+j-1). One can alternatively prove (4) inductively from j a_j=-sum_{k=1}^j S_k a_{j-k}; the majorant coefficients satisfy the analogous positive recurrence.

Since P(1)=0,

1<=sum_{j=1}^n|a_j|<=sum_{j=1}^n d_j(M)
 =prod_{k=1}^n(1+M/k)-1.                               (5)

The final identity follows by induction. Let rho_n be the unique positive solution of prod_{k=1}^n(1+rho_n/k)=2. Then M_n>=rho_n. This is a rigorous degree-dependent estimate, but rho_n tends to zero. Indeed, for each fixed epsilon>0, the product tends to infinity: for all sufficiently large k, log(1+epsilon/k)>=epsilon/(2k), and the harmonic series diverges. Thus the triangle-inequality majorant loses the uniform cancellation geometry.

There is nevertheless a sharp restricted-class consequence. If every |z_i|>=1, then |a_n|=prod_i|z_i|>=1. For M<1, each factor in d_n(M)=prod_{j=1}^n(M+j-1)/j is strictly below 1, contradicting (4). Hence M_n>=1 in this exterior class. The bound is attained: take all (n+1)-st roots of unity except one, and rotate the remaining tuple so one entry is 1. For 1<=k<=n the unrotated power sum is minus the k-th power of the omitted root, so its modulus is 1. Rotation preserves the modulus.

If all z_i are real, M_n>=1 also holds: for n>=2 the second sum is 1+sum_{i=2}^n z_i^2>=1, and for n=1 the assertion is immediate. Equality is possible at (1,0,...,0).

These results identify necessary features of configurations beating 1: at least one nonreal entry and at least one entry inside the unit circle. They do not permit either restriction to be imposed on the original problem.

## 5. Approach 4: exact inverse problem and the constant-sum ansatz

For arbitrary candidate moments s_1,...,s_n define b_0=1 and

j b_j=sum_{k=1}^j(1-s_k)b_{j-k}  (1<=j<=n).             (6)

**Theorem 2.** The numbers s_1,...,s_n are the first n pure power sums of some n complex numbers with z_1=1 if and only if b_n=0.

Necessity is (2). For sufficiency, put Q(t)=sum_{j=0}^{n-1}b_j t^j and P(t)=(1-t)Q(t). Recurrence (6) says that Q agrees through degree n with exp(sum_{k=1}^n(1-s_k)t^k/k), since its degree-n coefficient vanishes. Hence P agrees through degree n with exp(-sum_{k=1}^n s_k t^k/k). The monic polynomial F(X)=X^n P(1/X) has degree n, even when P has degree below n; the latter case just supplies zero roots. By the fundamental theorem of algebra it has n complex roots with multiplicity, and F(1)=0. Newton's triangular identities show that their first n sums are exactly s_1,...,s_n. Label one of the roots 1.

Thus R_n is the minimum infinity norm of a zero of the explicit holomorphic polynomial b_n(s_1,...,s_n). This is an exact reformulation, not a solution: a sharp zero-free polydisc for this polynomial is the original extremal difficulty.

A natural equioscillation proposal takes all s_k=u. Then (6) is the coefficient recurrence for (1-t)^{u-1}, so

b_n=(1-u)_n/n!=prod_{j=1}^n(j-u)/n!.

It vanishes only at u in {1,...,n}. Thus the all-equal complex moment ansatz cannot produce a bound below 1. This is an exact failure result for that restricted proposal, not a restriction on arbitrary phases or blocks.

## 6. Approach 5: two-block construction and an exact finite certificate

This approach follows the two-block mechanism in Biró's 2000 upper-bound paper. The construction and certificate here are independently authored finite algebra, with no copied source code or source text and no claim to a new method or improved record.

Let m=floor(n/2), choose u in C, and set alpha=1-u and beta_j=(alpha)_j/j!. Require s_k=u for 1<=k<=m and allow s_{m+1},...,s_n to vary. Since 2(m+1)>n, only the linear term of the high-degree perturbation contributes to coefficient n in

(1-t)^{-alpha} exp(-sum_{k=m+1}^n(s_k-u)t^k/k).

Therefore the exact condition b_n=0 becomes

sum_{k=m+1}^n s_k v_k=W,
where v_k=beta_{n-k}/k and W=beta_n+u sum_{k=m+1}^n v_k. (7)

The image of the product of discs |s_k|<=r under the left side is the closed disc of radius r sum|v_k|. Thus suitable higher moments exist if and only if |W|<=r sum|v_k|. A witness when the sum is positive is

s_k=(W/sum|v_h|) conjugate(v_k)/|v_k|

for nonzero v_k, with s_k=0 for v_k=0. This produces the finite upper estimate

R_n <= max(|u|, |W|/sum|v_k|).                           (8)

The denominator is nonzero because v_n=1/n. No computation of polynomial roots or assumption about their moduli is needed; Theorem 2 applies to arbitrary complex roots, and Section 1 then supplies normalization if desired.

### Exact certificate

CERTIFICATE.json gives n=32, u=869/2000-(5777/10000)i for the first 16 moments, rational real and imaginary parts for the next 15 moments, and an exactly corrected final moment obtained from (7). The generator rounds only proposed phases; all accepted inequalities and polynomial identities are subsequently checked with rational arithmetic.

The exact verifier establishes simultaneously:

- |s_k|^2 < (29/40)^2 for every 1<=k<=32;
- b_32=0 in Gaussian-rational arithmetic;
- P(1)=0 for the degree-32 monic polynomial recovered by Newton identities;
- a second Newton reconstruction recovers every supplied moment.

Consequently there exists a fully specified algebraic tuple with z_1=1 and M_32<29/40, and c_*<29/40. The coefficient recurrence and the rational input list constitute an exact algebraic specification of the tuple; decimal roots are unnecessary.

This is weaker than published asymptotic upper bounds. Its purpose is a compact, wholly replayable finite control. Optional numerical searches of two real parameters for n=2,3,4,8,16,32,64,128 suggest radii decreasing from about 0.8740 to 0.7061 within this family. They are not global optimizations, interval certificates, a monotonicity proof, or evidence of a sharp limiting constant.

## 7. Literature reconciliation and exact remaining gap

The governing primary collection is Hayman and Lingham, Research Problems in Function Theory (New Edition), arXiv:1809.07200v2, printed page 161 / PDF page 162, Problem and Update 7.4. It records Atkinson's 1/3 bound and reports no received progress. This update is not a current literature survey.

Biró, An improved estimate in a power sum problem of Turán, Indagationes Mathematicae 11(3) (2000), 343-358, explicitly proves existence of an effectively computable absolute q>1/2 for every n and every tuple with z_1=1. Its printed page 344 states that no numerical value is computed. The theorem statement, hypotheses, proof structure and conclusion were inspected; this investigation does not independently certify every estimate or extract q from that proof. The weaker 1/2 result has been proved independently in Section 3 of this packet.

Biró, An upper estimate in Turán's pure power sum problem, Indagationes Mathematicae 11(4) (2000), 499-508, proves limsup R_n<1 and gives the explicit consequence limsup R_n<5/6. Its page-507 addendum reports a Harcos computation giving limsup R_n<0.69368. The latter is recorded as a primary-paper numerical report; it was not independently interval-verified here.

A public 2026 repository by S. Griego proposes the asymptotic upper certificate C_42<=0.6906538. Its README explicitly separates exact verification of a limiting numerical inequality from the analytic asymptotic reduction and supplies no finite threshold. Only its public claim/status and limits were inspected here. The proof and code were not replayed, and this proposal is not used as a theorem in this packet. It is an upper-bound proposal, not a claimed sharp determination of c_*.

The remaining task is to determine the exact infimum of R_n over every positive integer n, prove a matching global lower bound, supply a sharp construction or limiting sequence, and clarify strict endpoint attainment. None of the five approaches does this. In particular, finite certificates, a scalar-cone obstruction, reported numerical improvements, and an asymptotic limsup bound do not close the gap.

## References and access level

1. [Hayman-Lingham primary collection](https://arxiv.org/abs/1809.07200v2), [PDF](https://arxiv.org/pdf/1809.07200). Fresh PDF obtained and relevant page visually verified. The cover identifies it as a draft copy.
2. [Biró 2000 lower-bound paper, author-hosted PDF](https://users.renyi.hu/~biroand/pdfs/Turan1.pdf), [DOI](https://doi.org/10.1016/S0019-3577(00)80003-8). Full 16-page published-paper PDF obtained; theorem and proof structure inspected, not a line-by-line independent audit.
3. [Biró 2000 upper-bound paper, author-hosted PDF](https://users.renyi.hu/~biroand/pdfs/AnUpperEstimateinTuran.pdf), [DOI](https://doi.org/10.1016/S0019-3577(00)80018-X). Full 10-page published-paper PDF obtained; definitions, construction, Section 3 and addendum inspected.
4. [Cheer-Goldston 1996, publisher DOI](https://doi.org/10.1090/S0025-5718-96-00744-2). Metadata/abstract and citation inspected; attempted publisher PDF was blocked and a mirror returned 502. No full proof was read and no theorem here relies on its uninspected content.
5. [Griego proposed certificate, v1.0.0](https://github.com/sebastian-griego/turan-c42-certificate/tree/v1.0.0). Public README claim/status only; not adopted as verified mathematics.

Only authored mathematics/code and public verification metadata are included in this packet. Downloaded primary sources and extracted source text are excluded.
