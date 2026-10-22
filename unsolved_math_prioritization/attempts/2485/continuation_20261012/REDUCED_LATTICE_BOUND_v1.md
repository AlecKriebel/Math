# A reduced-lattice exponential bound for the actual Erdős–Selfridge minimum

Authored mathematical continuation, 12 October 2026. All logarithms are natural. This document presents a proof, not a claim of novelty or external acceptance.

Let

\[
g(k)=\min\{n>k+1:\ p\nmid {n\choose k}\text{ for every prime }p\le k\},
\qquad L_k=\operatorname{lcm}(1,\ldots,k).
\]

**Theorem.** With the prime number theorem as a standard input,

\[
\boxed{\displaystyle
\limsup_{k\to\infty}\frac{\log g(k)}{k}
\le\frac{813}{875}<\frac{93}{100}<1.}
\tag{1}
\]

Consequently, for every sufficiently large integer \(k\),

\[
g(k)<\exp(93k/100)<L_k.
\tag{2}
\]

The proof deletes a short upper interval of primes from the classical lcm lattice and explicitly sieves the resulting two-digit restrictions. It establishes survival in a bounded initial interval of multipliers by the classical Brun pure sieve. No heuristic uniformity of the least admissible residue is assumed. This still gives an exponential bound; it does not prove subexponential growth or either successive-ratio conjecture.

## 1. The finite sieve fact being used

Let \(q_i\ge2\) be pairwise coprime integers, and let \(B_i\) be a set of \(\beta_i\) residue classes modulo \(q_i\), where \(0\le\beta_i<q_i\). Put \(w_i=\beta_i/q_i\), \(\rho=\prod_i(1-w_i)\). For even \(r\ge2\), let

\[
Q_{r-1}=\sum_{j=0}^{r-1}(-1)^j e_j(w),\qquad
E_{r-1}=\sum_{j=1}^{r-1}e_j(\beta),\qquad
R_r(z)=z^{-r}\prod_i(1+z w_i)\quad(z>0).
\]

Here \(e_j\) is the elementary symmetric polynomial, with \(e_0=1\) and \(e_j=0\) above the length of the list. If \(N(T)\) counts integers \(1\le t\le T\) avoiding all \(B_i\), then

\[
N(T)\ge TQ_{r-1}-E_{r-1}
\ge T\big(\rho-R_r(z)\big)-E_{r-1}.
\tag{3}
\]

In particular, \(R_r(z)\le\rho/2\) and the integer choice

\[
T=\left\lfloor\frac{2E_{r-1}}{\rho}\right\rfloor+1
\tag{4}
\]

ensure \(N(T)>0\).

**Proof of the finite fact.** For a nonempty set of indices \(J\), the simultaneous forbidden classes form \(\prod_{i\in J}\beta_i\) distinct classes modulo \(\prod_{i\in J}q_i\), by CRT. Their count in \([1,T]\) differs from \(T\prod_{i\in J}w_i\) in absolute value by at most \(\prod_{i\in J}\beta_i\). The empty intersection count is exactly \(T\).

If a particular integer lies in \(\nu>0\) forbidden events, its odd Bonferroni sum through degree \(r-1\) is \(-{\nu-1\choose r-1}\le0\); if \(\nu=0\), it is 1. Thus the odd sum lower-bounds the survival indicator. Summing all endpoint errors gives \(E_{r-1}\) and the first bound in (3). On one full CRT period, odd/even Bonferroni gives
\(Q_{r-1}\le\rho\le Q_{r-1}+e_r(w)\).
The nonnegative coefficient expansion gives \(e_r(w)\le z^{-r}\prod_i(1+z w_i)\), proving (3). Equation (4) makes its right side strictly positive. This retains the endpoint errors; positivity of the period density alone would not prove survival in the initial interval. ∎

This fact is classical Brun/Bonferroni sieve machinery, not a new general sieve principle. The argument above is included to specify precisely the constants and the use of prime-square moduli.

## 2. The reduced lattice and all of its local conditions

Fix an integer \(k\ge9\). For each prime \(p\le k\), let \(a_p\) be the integer with \(p^{a_p}\le k<p^{a_p+1}\). Define

\[
O_k=\{p:6k/7<p\le k\},\qquad
M_k=\frac{L_k}{\prod_{p\in O_k}p}\prod_{p\le\sqrt{k}}p.
\tag{5}
\]

All products here and below are over primes. Since \(6k/7>\sqrt{k}\) for \(k\ge9\), each omitted prime has exponent exactly one in \(L_k\), and the two products in (5) have disjoint prime supports. Thus \(M_k\) is a positive integer.

We consider the integers

\[
n=tM_k-1,\qquad t\ge1.
\tag{6}
\]

We use the elementary digit criterion

\[
p\nmid{n\choose k}\quad\Longleftrightarrow\quad n_j\ge k_j\text{ in every base-}p\text{ digit}.
\tag{7}
\]

For completeness, \((1+X)^n\equiv\prod_j(1+X^{p^j})^{n_j}\pmod p\), so comparison of the coefficient of \(X^k\) gives \({n\choose k}\equiv\prod_j{n_j\choose k_j}\pmod p\), establishing (7).

There are three disjoint prime ranges.

**Small primes, \(p\le\sqrt{k}\).** Here \(v_p(M_k)=a_p+1\). Every relevant digit of \(n\) is \(p-1\); these primes impose no sieve restriction.

**Retained primes, \(\sqrt{k}<p\le6k/7\).** Here \(v_p(M_k)=1\), and \(k\) has exactly two base-\(p\) digits. Write \(M_k=pc_p\) with \(p\nmid c_p\), and \(b_p=\lfloor k/p\rfloor\). The units digit of \(n\) is \(p-1\). Its next digit fails (7) exactly when

\[
tc_p\bmod p\in\{1,\ldots,b_p\}.
\]

Thus the forbidden set of multipliers has modulus and cardinality

\[
q_p=p,\qquad \beta_p=b_p,\qquad w_p=b_p/p.
\tag{8}
\]

**Omitted primes, \(6k/7<p\le k\).** Now \(p\nmid M_k\), so \(t\mapsto tM_k-1\) is a bijection modulo \(p^2\). The two digits of \(k\) are \((1,k-p)\): its high digit is 1 because \(p>k/2\), and its units digit is \(k-p\). By (7), an allowed residue of \(n\pmod{p^2}\) has high digit in \(\{1,\ldots,p-1\}\) and units digit in \(\{k-p,\ldots,p-1\}\). These choices are independent digit choices, so there are exactly

\[
(p-1)(2p-k)
\]

allowed residues. Therefore the forbidden multiplier set has

\[
\begin{split}
q_p&=p^2,\\
\beta_p&=p^2-(p-1)(2p-k)=p(k-p)+2p-k,\\
w_p&=\frac{k}{p}-1+\frac{2p-k}{p^2}.
\end{split}
\tag{9}
\]

In particular, \(0<\beta_p<p^2\). The full two-digit condition has been kept; a modulus-p units test alone would be insufficient.

The moduli in (8) and (9) are pairwise coprime, since each underlying prime occurs just once. The finite fact in Section 1 therefore applies to this combined family of forbidden multiplier sets.

**The strict domain.** Both 2 and 3 are at most \(\sqrt{k}\) when \(k\ge9\), and neither is omitted. Hence the relatively prime integers \(2^{a_2+1}>k\) and \(3^{a_3+1}>k\) both divide \(M_k\). Thus \(M_k>k^2\), and every integer in (6) satisfies \(n>k+1\). Any survivor is an actual admissible competitor for \(g(k)\).

## 3. The cost of the lattice

Write \(\theta(x)=\sum_{p\le x}\log p\) and \(\psi(k)=\log L_k\). Equation (5) gives

\[
\log M_k=\psi(k)-\theta(k)+\theta(6k/7)+\theta(\sqrt{k}).
\tag{10}
\]

The elementary identity \(\psi(k)=\sum_{m\ge1}\theta(k^{1/m})\) and the bound \(\theta(v)\le v\log v\) show
\(\psi(k)-\theta(k)=O(\sqrt{k}(\log k)^2)=o(k)\).
The PNT gives \(\theta(6k/7)=(6/7+o(1))k\). Therefore

\[
\log M_k=(6/7+o(1))k.
\tag{11}
\]

## 4. Controlling the growing sieve remainder

Let the list \((w_p)\) include exactly the retained and omitted primes from (8)–(9), and set \(\rho=\prod(1-w_p)\). We use \(z=4\).

First, the retained primes contribute only

\[
\sum_{\sqrt{k}<p\le6k/7}
\left[-\log(1-w_p)+\log(1+4w_p)\right]
=O(\sqrt{k}\log k)=o(k/\log k).
\tag{12}
\]

To check this without discarding any leading digit, note that \(w_p\le k/p^2\) and \(1-w_p\ge1/p\). On \(\sqrt{k}<p\le2\sqrt{k}\), this bounds the first logarithm by \(\log p\), and the second by 4; summing even over all integers costs \(O(\sqrt{k}\log k)\). On \(p>2\sqrt{k}\), we have \(w_p\le1/4\), so their sum is at most \((4/3+4)w_p\). Its sum is bounded by a constant times \(k\sum_{m>2\sqrt{k}}m^{-2}=O(\sqrt{k})\). This proves (12).

On the omitted interval, write \(u=p/k\in(6/7,1]\). Equation (9) gives uniformly

\[
w_p=u^{-1}-1+O(1/k),\qquad 0\le u^{-1}-1\le1/6.
\]

The function \(\ell(w)=\log((1+4w)/(1-w))\) has bounded derivative on a fixed neighborhood of \([0,1/6]\). Thus replacing \(w_p\) by \(u^{-1}-1\) incurs a total \(O(1)\) error even if we bound the number of primes by \(k\). The PNT on the fixed compact interval \([6/7,1]\) then gives

\[
\sum_{p\in O_k}\ell(w_p)
=\left(K+o(1)\right)\frac{k}{\log k},
\tag{13}
\]

where

\[
\begin{split}
K&=\int_{6/7}^1\log\frac{4-3u}{2u-1}\,du\\
&=\frac{10}{21}\log\frac{10}{7}+\frac{5}{14}\log\frac57.
\end{split}
\tag{14}
\]

To justify the weighted use of the PNT, approximate the continuous integrand on this fixed interval uniformly by upper and lower step functions. For every fixed subdivision, \(\pi(vk)-\pi(uk)=(v-u+o(1))k/\log k\). Taking the limit for the subdivision and then refining it gives (13). No shrinking prime interval or unproved uniform version of the PNT is being used. The integral in (14) is evaluated by integrating \(\log(4-3u)\) and \(\log(2u-1)\) separately.

The same estimates, or simply the bounded omitted-prime logarithms and \(\pi(k)=O(k/\log k)\), give

\[
-\log\rho=O(k/\log k).
\tag{15}
\]

Fix

\[
A=9/250,\qquad
r=2\left\lceil\frac{A k}{2\log k}\right\rceil.
\tag{16}
\]

Then \(r\) is even and \(r=(A+o(1))k/\log k\). By (12)–(14),

\[
\log\frac{R_r(4)}{\rho}
=-r\log4+\sum_p\ell(w_p)
=\left(K-A\log4+o(1)\right)\frac{k}{\log k}.
\tag{17}
\]

Section 6 below provides a self-contained rational certificate that

\[
A\log4-K>1/5000>0.
\tag{18}
\]

It follows that \(R_r(4)\le\rho/2\) for every sufficiently large \(k\).

## 5. The endpoint errors and the actual first multiplier

Let \(B=\sum_p\beta_p\). Every local modulus in (8)–(9) is at most \(k^2\), and there are at most \(k\) primes. Hence

\[
B\le k^3=:U.
\tag{19}
\]

This includes the full forbidden-residue cardinality modulo \(p^2\), not just the number of omitted primes or a modulus-p surrogate.

For \(m=r-1\), the elementary bound \(e_j(\beta)\le B^j/j!\) gives, since \(U\ge r\) eventually,

\[
E_{r-1}\le\sum_{j=1}^m\frac{U^j}{j!}
\le m\frac{U^m}{m!}
\le m\left(\frac{eU}{m}\right)^m=:V.
\tag{20}
\]

Using \(m=(A+o(1))k/\log k\), we have

\[
\begin{split}
\log V
&\le\log m+m(1+3\log k-\log m)\\
&=(2A+o(1))k.
\end{split}
\tag{21}
\]

Here \(\log m=\log k-\log\log k+O(1)\). In particular the cost is \(2Ak\), not \(Ak\); retaining the prime-square endpoint errors is essential.

Choose the integer \(T\) in (4). Equations (15), (20) and (21) show

\[
T\le2V/\rho+1\le3V/\rho,
\qquad \log T\le(2A+o(1))k.
\tag{22}
\]

For sufficiently large \(k\), equation (17) allows the finite sieve fact to be applied, so there exists an actual integer \(1\le t\le T\) avoiding every forbidden residue set. Sections 1–2 prove that \(tM_k-1\) is admissible and exceeds \(k+1\). Therefore

\[
g(k)\le TM_k-1,
\qquad
\log g(k)\le\left(\frac67+2A+o(1)\right)k
=\left(\frac{813}{875}+o(1)\right)k.
\]

This proves (1). Since \(813/875<93/100<1\), the first inequality in (2) holds eventually. The PNT also gives \(\log L_k\sim k\), so the second inequality in (2) holds eventually. ∎

## 6. Self-contained rational certificate for the positive margin

For a positive rational \(q\), put \(v=(q-1)/(q+1)\) and

\[
L_{40}(q)=2\sum_{j=0}^{39}\frac{v^{2j+1}}{2j+1}.
\]

Define the explicitly rational number

\[
D_{40}=\frac9{250}L_{40}(4)
-\frac{10}{21}L_{40}(10/7)
-\frac5{14}L_{40}(5/7).
\]

Direct finite rational arithmetic gives

\[
\frac{23004153}{10^{11}}<D_{40}<\frac{23004154}{10^{11}}.
\tag{23}
\]

These are comparisons of explicitly displayed finite rational sums; multiplying through by positive common denominators reduces them to integer inequalities. The accompanying exact-arithmetic check reproduces both comparisons, but the certificate is fully specified here without an executable.

The logarithm power series and a geometric tail bound give

\[
|\log q-L_{40}(q)|\le\frac{2|v|^{81}}{81(1-v^2)}.
\]

The three values of \(v\) above are \(3/5,3/17,-1/6\), all of absolute value at most \(3/5\). Hence for \(\Delta=A\log4-K\),

\[
|\Delta-D_{40}|\le
\left(\frac9{250}+\frac{10}{21}+\frac5{14}\right)
\frac{2(3/5)^{81}}{81(1-(3/5)^2)}
<10^{-18}.
\tag{24}
\]

The last comparison is rational. Equations (23)–(24) imply \(\Delta>1/5000\), establishing the strict margin required in (18). For orientation only, \(K\) is approximately 0.04967655546 and \(\Delta\) approximately 0.000230041537. No floating-point approximation is a proof premise.

## 7. Scope, credit and unresolved questions

The lattice idea originates with Ecklund, Erdős and Selfridge, *A New Function Associated with the Prime Factors of (n choose k)*, Mathematics of Computation 28 (1974), 647–649: https://www.renyi.hu/~p_erdos/1974-01.pdf . Their construction keeps all of \(L_k\); the current argument instead removes a top prime interval and pays explicitly for its two-digit congruences. Their p.649 discusses the desired inequality \(g(k)<L_k\); (2) establishes that inequality only for sufficiently large \(k\), without an effective numerical threshold and without claiming it for every \(k\).

The finite sieve lemma is the classical Brun pure sieve. Useful primary expositions are Kevin Ford, *Sieve Methods Lecture Notes, Spring 2023*, Theorem 1.5 and Lemma 1.6, https://ford126.web.illinois.edu/sieve2023.pdf ; and Terence Tao, *254A, Notes 4: Some sieve theory* (2015), equation (5), Exercise 9 and equation (13), https://terrytao.wordpress.com/2015/01/21/254a-notes-4-some-sieve-theory/ . No new general sieve principle is claimed.

Sorenson, Sorenson and Webster's 2020 paper and 2021 addendum carefully separate the reciprocal-density approximant from heuristic assertions about \(g(k)\): https://doi.org/10.2140/obs.2020.4.371 and https://arxiv.org/html/1907.08559v3 . The present proof uses the density solely inside a finite lower bound with all endpoint errors included. It does not infer a first-residue bound from periodic density alone.

The principal bound in (1) is still exponential in \(k\). This document proves neither \(g(k)=\exp(o(k))\), the anticipated \(\exp(\Theta(k/\log k))\) scale, nor either conjecture about successive ratios. It supplies no effective onset for (2). Bounded source checks do not establish novelty, priority or the absence of a stronger result elsewhere.
