# A square-root overhead bound for the actual Erdős–Selfridge minimum

Authored mathematical continuation, 12 October 2026. This is a partial result, not a solution of Erdős Problem 1095 or a claim of priority. All logarithms are natural.

Define

\[
g(k)=\min\{n>k+1:\ p\nmid {n\choose k}\text{ for every prime }p\le k\},
\qquad L_k=\operatorname{lcm}(1,\ldots,k).
\]

We prove an exact finite lower bound on the number of admissible multipliers in a specified initial interval. Applying it with a selective extra prime product gives

\[
\boxed{\displaystyle
\limsup_{k\to\infty}\frac{\log g(k)-\log L_k}{\sqrt{k}}\le\frac{13}{5}.}
\tag{1}
\]

This improves the previously established overhead of order \(k/\log k\) to order \(\sqrt{k}\). The principal scale remains \(\exp((1+o(1))k)\); neither subexponential growth nor any successive-ratio conjecture follows. The proof uses the prime number theorem (PNT), elementary congruences, exact Chinese remainder counting and the finite Bonferroni inequalities. It makes no distributional assumption about the first admissible integer.

## 1. A finite sieve theorem, including the endpoint error

Fix an integer \(k\ge3\). For every prime \(p\le k\), let

\[
a_p=\max\{a:p^a\le k\},\qquad b_p=\lfloor k/p^{a_p}\rfloor.
\]

Thus \(1\le b_p\le p-1\). Choose an arbitrary subset \(S\) of the primes at most \(k\), and put

\[
M=L_k\prod_{p\in S}p,\quad F=\{p\le k:p\text{ prime},\ p\notin S\},
\quad w_p=b_p/p\ (p\in F).
\]

Write \(e_j(v)\) for the elementary symmetric polynomial of degree \(j\) in the finite list \(v\), with \(e_0=1\) and \(e_j=0\) for \(j\) exceeding its length. For an even integer \(r\ge2\), define

\[
Q_{r-1}=\sum_{j=0}^{r-1}(-1)^j e_j((w_p)_{p\in F}),\qquad
E_{r-1}=\sum_{j=1}^{r-1}e_j((b_p)_{p\in F}),\qquad
\rho=\prod_{p\in F}(1-w_p).
\]

Let \(N(T)\) be the number of integers \(t\) with \(1\le t\le T\) for which \(tM-1\) is admissible for \(g(k)\).

**Theorem 1 (exact finite criterion).** For every positive integer \(T\),

\[
N(T)\ge TQ_{r-1}-E_{r-1}
\ge T\big(\rho-e_r(w)\big)-E_{r-1}.
\tag{2}
\]

In particular, if \(Q_{r-1}>0\) and \(T>E_{r-1}/Q_{r-1}\), then

\[
g(k)\le TM-1.
\tag{3}
\]

A convenient sufficient criterion is: for any real \(z>0\), put

\[
R_r(z)=z^{-r}\prod_{p\in F}(1+z w_p).
\]

If \(R_r(z)<\rho\) and \(T>E_{r-1}/(\rho-R_r(z))\), then (3) holds. For rational \(z\), every quantity in this sufficient test is rational and exactly computable.

**Proof.** The coefficient identity

\[
(1+X)^n\equiv\prod_{i\ge0}(1+X^{p^i})^{n_i}\pmod p
\]

for the base-\(p\) digits \(n_i\) gives
\({n\choose k}\equiv\prod_i{n_i\choose k_i}\pmod p\). Because digits lie between 0 and \(p-1\), this is nonzero exactly when \(n_i\ge k_i\) for every \(i\). This proves the required digit criterion directly.

If \(p\in S\), then \(p^{a_p+1}\mid M\); all relevant digits of \(tM-1\) are \(p-1\), so this prime always passes. If \(p\in F\), write \(M=p^{a_p}c_p\), where \(p\nmid c_p\). The lowest \(a_p\) digits of \(tM-1\) are \(p-1\). Its digit in position \(a_p\) equals \((tc_p-1)\bmod p\). It fails precisely when

\[
tc_p\bmod p\in\{1,\ldots,b_p\}.
\tag{4}
\]

Thus prime \(p\) excludes exactly \(b_p\) residue classes of \(t\pmod p\). The residues depend on \(M\); their cardinalities do not.

For a subset \(J\subseteq F\), let \(A_J(T)\) count the integers in \([1,T]\) excluded by every prime in \(J\). For nonempty \(J\), CRT shows that these integers occupy precisely \(\prod_{p\in J}b_p\) distinct classes modulo \(\prod_{p\in J}p\). The count of each individual class differs from \(T/\prod_{p\in J}p\) in absolute value by less than 1. Consequently

\[
\left|A_J(T)-T\prod_{p\in J}w_p\right|
\le\prod_{p\in J}b_p.
\tag{5}
\]

For \(J=\varnothing\), the count is exactly \(T\), and there is no endpoint error.

If an integer is excluded by \(\nu\) primes, its contribution to the odd Bonferroni truncation is
\(\sum_{j=0}^{r-1}(-1)^j {\nu\choose j}\). This is 1 when \(\nu=0\), and when \(\nu\ge1\) equals \(-{\nu-1\choose r-1}\le0\), using \(r-1\) odd. Therefore this truncation is a pointwise lower bound on the indicator of survival. Summing it and using (5) proves the first inequality in (2).

The same odd/even Bonferroni inequalities on one full CRT period give

\[
Q_{r-1}\le\rho\le Q_{r-1}+e_r(w).
\tag{6}
\]

Here \(\rho\) is the exact proportion on that finite period, used only to bound the polynomial \(Q_{r-1}\). We do not replace the initial-interval count by its density. Equation (5) retains and bounds its discrepancy explicitly.

The coefficient expansion of \(\prod_{p\in F}(1+z w_p)\), whose coefficients are nonnegative, gives \(e_r(w)\le R_r(z)\). This proves both sufficient criteria. Under either strict criterion, the integer \(N(T)\) is positive.

Finally, every witness belongs to the required domain. Since \(k\) and \(k-1\) are coprime, \(k(k-1)\mid L_k\); hence for \(k\ge3\),
\(tM-1\ge L_k-1\ge k(k-1)-1>k+1\).
This also checks the smallest case \(k=3\). ∎

## 2. A reusable asymptotic form

For fixed real constants \(c>1\) and \(z>1\), define

\[
I(c)=\int_c^\infty-\log(1-u^{-2})\,du
=c\log(1-c^{-2})+\log\frac{c+1}{c-1},
\]

\[
J(c,z)=\int_c^\infty\log(1+zu^{-2})\,du
=-c\log(1+z/c^2)+2\sqrt z\arctan(\sqrt z/c).
\]

The evaluations follow by integration by parts. Both integrals are finite and positive.

**Theorem 2.** With the PNT as input,

\[
\limsup_{k\to\infty}
\frac{\log g(k)-\log L_k}{\sqrt{k}}
\le c-1+\frac{I(c)+J(c,z)}{\log z}
\qquad(c>1,\ z>1).
\tag{7}
\]

**Proof.** Throughout the proof, \(c,z\) are fixed constants, not functions of \(k\). Put \(x=\sqrt{k}\), and for all sufficiently large \(k\) choose the forced set

\[
S=\{p:p\le k^{1/3}\}\ \cup\ \{p:x<p\le cx\}.
\tag{8}
\]

Only primes at most \(k\) are included, which is automatic once \(cx<k\). These two intervals are disjoint. Write \(M, F, w,\rho\) as in Theorem 1. We establish the following estimates, with every error referring to \(k\to\infty\) and fixed \(c,z\):

\[
\log(M/L_k)=(c-1+o(1))x,
\tag{9}
\]

\[
-\log\rho=(2I(c)+o(1))\frac{x}{\log k},
\quad
\log\prod_{p\in F}(1+z w_p)
=(2J(c,z)+o(1))\frac{x}{\log k}.
\tag{10}
\]

Equation (9) follows from \(\theta(v)\sim v\), since its left side is
\(\theta(k^{1/3})+\theta(cx)-\theta(x)\).

To justify (10), split the unforced primes into

\[
F_2=\{p:k^{1/3}<p\le x\},\qquad F_1=\{p:cx<p\le k\}.
\]

This accounts for every unforced prime and every relevant prime-power digit. On \(F_2\), \(a_p=2\), so \(w_p\le k/p^3<1\). Since \(b_p\le p-1\), also \(-\log(1-w_p)\le\log p\). For \(k^{1/3}<p\le2k^{1/3}\), summing this last bound even over all integers costs \(O(k^{1/3}\log k)\). For \(p>2k^{1/3}\), we have \(w_p\le1/8\) and

\[
-\log(1-w_p)\le\frac87w_p,\qquad
\sum_{p>2k^{1/3}}\frac{k}{p^3}
\le k\sum_{m>2k^{1/3}}m^{-3}=O(k^{1/3}).
\]

Likewise \(\log(1+z w_p)\le z w_p\), whose sum on \(F_2\) is \(O_{z}(k^{1/3})\), splitting at the same point. Thus the entire \(F_2\) contribution to either expression in (10) is
\(O_{z}(k^{1/3}\log k)=o(x/\log k)\). No leading-digit requirement below \(\sqrt{k}\) has been discarded.

On \(F_1\), \(a_p=1\) and

\[
0\le k/p^2-w_p<1/p,\qquad 0\le w_p\le c^{-2}<1.
\]

Both logarithms in (10), viewed as functions of \(w_p\), have bounded derivative on \([0,c^{-2}]\). Replacing \(w_p\) by \(k/p^2\) therefore costs at most
\(O_{c,z}(\sum_{p\le k}1/p)=O_{c,z}(\log k)=o(x/\log k)\).

For either function
\(f(u)=-\log(1-u^{-2})\) or \(f(u)=\log(1+zu^{-2})\), the PNT yields

\[
\sum_{cx<p\le x^2} f(p/x)
=\left(\int_c^\infty f(u)\,du+o(1)\right)\frac{x}{\log x}.
\tag{11}
\]

Here is an explicit uniform-tail justification of this familiar consequence. On each fixed compact interval \([c,R]\), the PNT gives weak convergence of the scaled prime-counting measure to Lebesgue measure after normalization by \(x/\log x\); equivalently one can sandwich a Riemann sum between prime counts at the subdivision endpoints. Both functions are continuous there. On \([R,\infty)\), they are \(O_{c,z}(u^{-2})\). Partial summation of \(\pi(v)\ll v/\log v\), which itself follows from the PNT, gives \(\sum_{p>Rx}p^{-2}\ll1/(Rx\log(Rx))\). The normalized tail is consequently \(O_{c,z}(1/R)\), uniformly for sufficiently large \(x\). First take \(x\to\infty\), then \(R\to\infty\). This proves (11), including the growing upper endpoint \(x^2\). Since \(\log x=\tfrac12\log k\), equation (10) follows.

Now fix a further constant

\[
A>\frac{2(I(c)+J(c,z))}{\log z},
\tag{12}
\]

and take the even integer

\[
r=2\left\lceil\frac{A x}{2\log k}\right\rceil.
\tag{13}
\]

Equations (10) imply

\[
\log\frac{R_r(z)}{\rho}
=\left(2I(c)+2J(c,z)-A\log z+o(1)\right)\frac{x}{\log k}.
\tag{14}
\]

The coefficient has fixed negative margin by (12), so \(R_r(z)\le\rho/2\) for every sufficiently large \(k\). This controls the entire omitted Bonferroni term uniformly, rather than assuming its smallness.

It remains essential to bound the total endpoint error, whose number of terms grows with \(k\). Set \(B=\sum_{p\in F}b_p\). Since \(a_p\ge1\),

\[
B\le k\sum_{p\le k}1/p\le k(1+\log k)=:U.
\tag{15}
\]

For every \(j\), the expansion of \(B^j\) gives \(e_j(b)\le B^j/j!\). Eventually \(U\ge r\). With \(m=r-1\), the sequence \(U^j/j!\) is then increasing for \(0\le j\le m\), whence

\[
E_{r-1}\le\sum_{j=1}^{m}\frac{U^j}{j!}
\le m\frac{U^m}{m!}
\le m\left(\frac{eU}{m}\right)^m=:V.
\tag{16}
\]

The final factorial inequality follows from \(m!\ge(m/e)^m\). Since
\(m=(A+o(1))x/\log k\),

\[
\log V
\le\log m+m(1+\log U-\log m)
=\left(\frac A2+o(1)\right)x.
\tag{17}
\]

Indeed \(\log U=\log k+O(\log\log k)\) and
\(\log m=\frac12\log k-\log\log k+O_A(1)\). This bounds the full symmetric-term sum, not merely a single intersection error.

Choose the exactly defined positive integer

\[
T=\left\lfloor\frac{2E_{r-1}}{\rho}\right\rfloor+1.
\tag{18}
\]

Because \(\rho-R_r(z)\ge\rho/2\), Theorem 1 applies. Moreover \(\rho\le1\), \(V\ge1\), and (18) gives
\(T\le2V/\rho+1\le3V/\rho\). Thus (10) and (17) prove

\[
\log T\le\left(\frac A2+o(1)\right)x.
\tag{19}
\]

This is a bound on an actual first surviving multiplier: (2) proves that at least one survivor occurs in \([1,T]\). Combining (3), (9) and (19) yields

\[
\limsup_{k\to\infty}\frac{\log g(k)-\log L_k}{\sqrt{k}}
\le c-1+\frac A2.
\]

This holds for every fixed \(A\) satisfying (12). Letting \(A\) decrease to that threshold, only after taking the limsup, proves (7). ∎

## 3. A rigorously checked numerical choice

Take \(c=8/5\), \(z=4\), and \(A=4\). Formula (12) reduces to

\[
\Delta:=4\log4-2I(8/5)-2J(8/5,4)>0.
\tag{20}
\]

At these rational parameters,

\[
I(8/5)=\frac85\log\frac{39}{64}+\log\frac{13}{3},
\]

\[
J(8/5,4)=-\frac85\log\frac{41}{16}
+4\arctan\frac54
=-\frac85\log\frac{41}{16}+\pi+4\arctan\frac19.
\]

The accompanying exact-rational constant checker proves

\[
0.0402355<\Delta<0.0402356.
\]

It uses the convergent series
\(\log q=2\sum_{j\ge0}v^{2j+1}/(2j+1)\), with \(v=(q-1)/(q+1)\), and a geometric bound for its omitted tail; the alternating arctangent series; and Machin's identity \(\pi=16\arctan(1/5)-4\arctan(1/239)\). The latter follows from the tangent addition formula and the angles' ranges. All interval endpoints are rational; floating-point output is descriptive only.

Hence the strict condition (12) holds and the preceding proof with this fixed \(A\) gives coefficient
\(c-1+A/2=3/5+2=13/5\), proving (1). Formula (7) in fact gives approximately 2.585488 at these same \(c,z\), but the simpler constant in (1) avoids presenting an optimized numerical value as a conceptual improvement. No claim that \(13/5\), or any numerical minimization of (7), is best possible is made.

## 4. What changed, and the precise obstruction left

The one-term union bound needs the total local failure weight below 1 and therefore forces all primes up to order \(k/\log k\). Here the odd truncation is allowed to grow, with \(r\asymp\sqrt{k}/\log k\). Its negative remainder is controlled by the nonnegative generating function, while every initial-interval CRT error is retained in \(E_{r-1}\). The selective forcing in (8) pays only for the relevant dangerous interval above \(\sqrt{k}\); primes with higher leading positions are handled separately at negligible asymptotic cost.

This method still constructs only numbers on a lattice with spacing at least \(L_k\). For the displayed selective choice, \(M/L_k\) itself grows exponentially in \(\sqrt{k}\). Thus the theorem supplies no upper bound below \(L_k\), no \(\exp(o(k))\) construction, and no control of the actual minimum's successive ratios. Those would require an additional argument controlling admissible integers outside this lattice or substantially different constructive structure. The fact that the exact period has a computable positive density does not supply that argument.

## 5. Credit and source scope

E. F. Ecklund Jr., P. Erdős and J. L. Selfridge, *A New Function Associated with the Prime Factors of (n choose k)*, Mathematics of Computation 28 (1974), 647–649, uses the lattice \(tL_kP_y-1\), with \(y\) about \(6k/\log k\), to prove the principal exponential upper bound. That primary paper was freshly retrieved and its pp.648–649 checked: https://www.renyi.hu/~p_erdos/1974-01.pdf . The current proof keeps its lattice idea, replaces the initial union bound by an explicitly controlled finite sieve, and changes the forced prime set. It is not represented as an entirely new construction.

B. Sorenson, J. P. Sorenson and J. Webster, *An Algorithm and Estimates for the Erdős–Selfridge Function*, published in Open Book Series 4 (2020), 371–385; updated author manuscript https://arxiv.org/abs/1907.08559v3 , distinguishes its reciprocal-density approximant from statements about the first admissible integer. The updated abstract was freshly checked. The published PDF endpoint did not yield inspectable text on this retrieval; the source-status statement here therefore does not claim a fresh full-paper inspection or comprehensive priority search.

The PNT is the sole non-elementary theorem used in the proof of (1) and (7). The finite criterion (2)–(3) does not require it. Literature checks made here do not establish that this square-root secondary overhead is new. No manuscript acceptance, external verification, or resolution of Problem 1095 is asserted.
