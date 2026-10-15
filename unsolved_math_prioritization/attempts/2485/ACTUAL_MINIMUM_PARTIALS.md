# Actual-minimum partial results for Erdős Problem 1095

Authored partial results, 12 October 2026. Target: Erdős Problem 1095. This is not a full resolution or a novelty claim.

Let

\[
g(k)=\min\{n>k+1:\ p\nmid\binom nk\text{ for every prime }p\le k\},
\qquad L_k=\operatorname{lcm}(1,\ldots,k).
\]

The exclusion of both n=k and n=k+1 is retained. In particular g(1)=3 and g(2)=6. The results below concern this actual minimum, not the reciprocal-density model.

## 1. A finite constructive upper bound

For each prime p<=k, let a_p be the unique integer with p^{a_p}<=k<p^{a_p+1}, and let b_p=floor(k/p^{a_p}). Thus 1<=b_p<=p-1. For a real cutoff 0<=y<=k put

\[
P_y=\prod_{p\le y}p,\qquad
D_y=\sum_{y<p\le k}\frac{b_p}{p},\qquad
B_y=\sum_{y<p\le k}b_p.
\]

**Theorem 1.** If k>=3, D_y<1, and the positive integer T satisfies T>B_y/(1-D_y), then

\[
g(k)\le T L_kP_y-1.
\]

More precisely, at least one of t L_k P_y-1, 1<=t<=T, is admissible. All quantities in this criterion are finite integers or rational numbers; an always-valid choice is T=floor(B_y/(1-D_y))+1.

**Proof.** Put A=L_kP_y. Fix p<=k. If p<=y, then p^{a_p+1} divides A. Every digit through position a_p of tA-1 is p-1, and Lucas's criterion holds automatically.

If p>y, write A=p^{a_p}c_p with p not dividing c_p. The bottom a_p base-p digits of tA-1 are p-1. For s=t c_p mod p, its digit in position a_p is s-1 if s>=1 and p-1 if s=0. Therefore this prime rejects t if and only if

\[
tc_p\bmod p\in\{1,2,\ldots,b_p\}.
\]

These are exactly b_p nonzero residue classes of t modulo p. Among 1<=t<=T they exclude at most b_p(T/p+1) integers. A union bound over p>y excludes at most T D_y+B_y<T integers, leaving a valid t. The witness exceeds k+1: L_k is divisible by k(k-1), so L_k-1>k+1 for k>=3. Thus the witness lies in the defining domain, completing the proof. No independence assumption is used.

### A secondary-term consequence

**Corollary 2.** With the prime number theorem as an external standard input,

\[
\limsup_{k\to\infty}
\frac{\log g(k)-\log L_k}{k/\log k}\le 1.
\tag{1}
\]

Equivalently, there is a real function e(k)->0 such that

\[
g(k)\le L_k\exp\big((1+e(k))k/\log k\big)
\]

for all sufficiently large k.

**Proof.** Fix epsilon>0, and take y=(1+epsilon)k/log k. Eventually y>sqrt(k), so b_p=floor(k/p) for p>y. The prime number theorem and partial summation give

\[
\sum_{p>y}p^{-2}\sim \frac1{y\log y}.
\]

Indeed this sum is -pi(y)/y^2+2 integral_y^infinity pi(t)/t^3 dt; replacing pi(t) by t/log t has relative error o(1) uniformly for t>=y, and the integral is asymptotic to 1/(y log y). Consequently

\[
D_y\le k\sum_{p>y}p^{-2}\le\frac{1+o(1)}{1+\epsilon}.
\]

For large k, 1-D_y is bounded below by a positive constant depending only on epsilon. Since B_y<=k^2, Theorem 1 permits T=O_epsilon(k^2). Write theta(y)=sum_{p<=y}log p. Then

\[
\log g(k)\le\log L_k+\theta(y)+\log T
=\log L_k+(1+\epsilon+o(1))\frac{k}{\log k},
\]

because theta(y)~y and log T=O_epsilon(log k)=o(k/log k). Taking the limsup and then allowing the fixed epsilon to decrease to zero proves (1). We do not insert an uncontrolled k-dependent epsilon into the estimates.

**Credit and limits.** This sharpens the explicit cutoff constant in the original Ecklund–Erdős–Selfridge construction, which used the same t L_kP_y-1 family with y approximately 6k/log k and T=k^2, and expressly observed that 6 could be reduced. We make no priority claim for coefficient 1. The leading exponential scale is still exp((1+o(1))k); this does not prove g(k)<L_k, subexponential growth, the predicted exp(Theta(k/log k)) size, or either successive-ratio conjecture. The bound is generally far larger than known numerical minima.

Primary source: E. F. Ecklund Jr., P. Erdős and J. L. Selfridge, *A new function associated with the prime factors of (n choose k)*, Mathematics of Computation 28 (1974), 647–649, especially pp.648–649: https://www.renyi.hu/~p_erdos/1974-01.pdf .

## 2. Exact transport at a prime parameter

Let A_k(n) mean that n>=k and every prime <=k is coprime to C(n,k). Unlike g(k), this notation does not exclude n=k or n=k+1.

**Theorem 3.** Let q>=3 be prime and n>q+1. Then A_q(n) is equivalent to all three conditions

1. A_{q-1}(n-1);
2. gcd(n, product_{p<q}p)=1;
3. n mod q^2>=q.

In particular,

\[
g(q)\ge g(q-1)+1.
\tag{2}
\]

**Proof.** Put C=C(n,q) and B=C(n-1,q-1); both are positive integers. The exact identity B=qC/n gives, for any prime p<q,

\[
v_p(B)=v_p(C)-v_p(n).
\]

If A_q(n), the right side is -v_p(n). Its nonnegativity forces v_p(n)=0 and then v_p(B)=0, proving conditions 1 and 2. Conversely, conditions 1 and 2 give v_p(C)=v_p(B)+v_p(n)=0 for every p<q. The base-q digits of q are 10, so Lucas's criterion at the remaining prime q is exactly floor(n/q) mod q>=1, equivalent to condition 3. Finally n-1>q=(q-1)+1, so every q-admissible n yields a permissible competitor for g(q-1); applying this to n=g(q) proves (2).

Thus g(q) is exactly one plus the first m>q for which A_{q-1}(m), m+1 has no prime divisor below q, and (m+1) mod q^2>=q. This is a first-survivor characterization, not merely a density relation. It identifies the extra obstruction a ratio proof would need to control. It supplies no unbounded multiplicative jump: a lower bound of 1+1/g(q-1) for the ratio tends to one.

The prime requirement matters. At a general parameter K, the identity becomes v_p(C(n,K))=v_p(C(n-1,K-1))+v_p(n)-v_p(K). For a composite K, primes p<K can divide K, so this argument does not yield (2).

## 3. The remaining problem

The actual asymptotic scale, the eventual inequality g(k)<L_k, and

\[
\limsup g(k+1)/g(k)=\infty,
\qquad
\liminf g(k+1)/g(k)=0
\]

remain unresolved by this continuation. The existing CRT density and model-ratio theorems are not substitutes for distribution of the first admissible integer. The strongest new local analytic result above is the exact finite construction and its explicit secondary-term consequence, together with exact prime-step transport. Separate authored files give a source-lemma correction and complete independent minimality certificates for k<=46.
