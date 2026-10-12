# Digit-cylinder compression for the Erdős–Selfridge minimum

Authored mathematical continuation, 12 October 2026. All logarithms are natural. This is a proof submission, not a claim of novelty or external acceptance.

Define

\[
g(k)=\min\{n>k+1:p\nmid\tbinom nk\text{ for every prime }p\le k\},
\qquad L_k=\operatorname{lcm}(1,\ldots,k).
\]

**Principal theorem.** Using the prime number theorem,

\[
\boxed{\displaystyle\limsup_{k\to\infty}\frac{\log g(k)}k\le\frac67.}
\tag{1}
\]

In particular, \(g(k)<\exp(0.86k)<L_k\) for every sufficiently large integer \(k\). No effective numerical onset is asserted.

The mechanism is a reduction of the joint CRT endpoint budget, not merely a change of sieve parameters. For an omitted prime \(p>k/2\), the full forbidden set can require order \(p^2\) residues, but its disjoint description using congruences of different moduli has exactly \(p\) classes. The proof retains both digit conditions and their exact combined density. It never treats the two same-prime conditions as independent events.

A separate theorem below shows a remaining positive exponential cost for this particular absolute-error Bonferroni method, even after the compression. This is a barrier for that certificate, not a lower bound for the actual minimum or actual discrepancy.

## 1. A mixed-modulus finite sieve lemma

For each prime in a finite set \(P\), let an event \(B_p\subseteq\mathbb Z\) be a disjoint union

\[
B_p=\bigsqcup_{a\in A_p} C_{p,a},
\]

where \(C_{p,a}\) is a union of \(c_{p,a}\) distinct residue classes modulo a power \(p^{d_{p,a}}\), with \(d_{p,a}\ge1\). Disjointness is as subsets of integers, including when the component moduli differ. Put

\[
w_p=\sum_{a\in A_p}\frac{c_{p,a}}{p^{d_{p,a}}}<1,
\qquad h_p=\sum_{a\in A_p}c_{p,a},
\qquad \rho=\prod_{p\in P}(1-w_p).
\tag{2}
\]

All cardinalities are nonnegative integers. Components with zero classes may be omitted. Let \(e_j\) denote an elementary symmetric polynomial, with \(e_0=1\) and \(e_j=0\) above the list length. For even \(r\ge2\), define

\[
Q_{r-1}=\sum_{j=0}^{r-1}(-1)^j e_j(w),\qquad
E_{r-1}=\sum_{j=1}^{r-1}e_j(h),\qquad
R_r(z)=z^{-r}\prod_{p\in P}(1+zw_p),\quad z>0.
\tag{3}
\]

If \(N(T)\) counts integers \(1\le t\le T\) avoiding all events, then, for integer \(T\ge1\),

\[
N(T)\ge TQ_{r-1}-E_{r-1}
\ge T(\rho-R_r(z))-E_{r-1}.
\tag{4}
\]

**Proof.** Fix a nonempty subset \(J\subseteq P\). Expand \(\bigcap_{p\in J}B_p\) by choosing one component for each prime in \(J\). These choices give disjoint sets because the components at any one prime are disjoint. For each choice, CRT applies to its pairwise coprime prime-power moduli. It gives \(\prod_{p\in J}c_{p,a_p}\) residue classes modulo \(\prod_{p\in J}p^{d_{p,a_p}}\). Each class has count differing from its expected count in \([1,T]\) by at most one. Summing over component choices therefore proves

\[
\left|\#\bigl([1,T]\cap\bigcap_{p\in J}B_p\bigr)
 -T\prod_{p\in J}w_p\right|
\le\prod_{p\in J}h_p.
\tag{5}
\]

Indeed, the sum of the component densities factors as the product of the sums in (2), and the sum of their error budgets factors as the product of the \(h_p\). Thus the main density is unchanged by the compression.

Odd Bonferroni truncation at degree \(r-1\) gives the first inequality in (4): at an integer lying in \(\nu\ge1\) events its truncated contribution is \(-\binom{\nu-1}{r-1}\le0\), whereas a survivor contributes one. The empty intersection has exact count \(T\) and no error. Applied to independent events of probabilities \(w_p\), consecutive Bonferroni inequalities give

\[
0\le\rho-Q_{r-1}\le e_r(w)\le R_r(z).
\tag{6}
\]

The final inequality follows by expanding the nonnegative coefficients of \(\prod_p(1+zw_p)\). This proves (4). Consequently, whenever \(R_r(z)\le\rho/2\), the choice

\[
T=\left\lfloor\frac{2E_{r-1}}\rho\right\rfloor+1
\tag{7}
\]

gives an actual survivor. ∎

The Bonferroni part is classical Brun pure sieve machinery. The extra input here is the more economical exact representation used in (5).

## 2. The digit decomposition and its exact local cost

Let \(\sqrt{k}<p\le k\), and write

\[
k=bp+a,\qquad 1\le b<p,\quad0\le a<p.
\]

If \(p\nmid M\), the affine map \(t\mapsto tM-1\) is a bijection modulo \(p^2\) and modulo \(p\). Write the first two base-\(p\) digits of \(tM-1\) as \((n_0,n_1)\). Lucas's criterion says that the prime fails exactly when \(n_0<a\) or \(n_1<b\). Split this into the two disjoint events

\[
U_p=\{n_0<a\},\qquad
H_p=\{n_0\ge a,\ n_1<b\}.
\tag{8}
\]

The event \(U_p\) has \(a\) residue classes modulo \(p\), so its density is \(a/p\). The event \(H_p\) has \(b(p-a)\) residue classes modulo \(p^2\), so its density is \(b(p-a)/p^2\). Their disjoint union therefore has exact density and compressed endpoint weight

\[
w_p=\frac ap+\frac{b(p-a)}{p^2}
 =1-\frac{(p-a)(p-b)}{p^2},
\qquad
h_p=a+b(p-a)=bp-(b-1)a\le k.
\tag{9}
\]

By contrast, representing the entire failure set only modulo \(p^2\) uses

\[
\beta_p=ap+b(p-a)
\tag{10}
\]

classes. Both counts describe the same set; only their error budgets differ. When \(p>k/2\), one has \(b=1\), \(a=k-p\), and therefore

\[
\boxed{h_p=p},\qquad
\beta_p=p(k-p)+2p-k,
\qquad
w_p=\frac{k}{p}-1+\frac{2p-k}{p^2}.
\tag{11}
\]

The endpoint \(p=k\) is included: \(a=0\), the units event is empty, and \(H_p\) still has \(p\) classes modulo \(p^2\). The leading digit has not disappeared.

**Minimality within the cylinder-cover model.** A cylinder here is one residue class modulo \(p\) or \(p^2\), viewed inside \(\mathbb Z/p^2\mathbb Z\). In the original \(n\)-coordinate, there are exactly \(a\) full modulo-\(p\) fibers contained in the bad set, namely those with units digit below \(a\). In each remaining fiber, exactly \(b\) of its \(p\) points are bad; because \(b<p\), that fiber itself is not contained in the bad set. Hence these remaining bad points must each be covered by a singleton cylinder. Any cover of the bad set by cylinders contained in it uses at least \(a+b(p-a)\) cylinders, and (8) achieves this number disjointly. The affine bijection preserves fibers and singletons. Thus \(h_p\) is the smallest such cylinder count, including for the multiplier variable. This does not assert optimality among signed representations or estimates exploiting cancellation between classes.

## 3. A lattice with all local conditions retained

For \(k\ge9\), let \(a_p\) satisfy \(p^{a_p}\le k<p^{a_p+1}\). Set

\[
O_k=\{p:3k/4<p\le k\},\qquad
M_k=\frac{L_k}{\prod_{p\in O_k}p}\prod_{p\le\sqrt{k}}p.
\tag{12}
\]

All products are over primes. Since every omitted prime exceeds \(\sqrt{k}\), it has exponent one in \(L_k\). Thus \(M_k\) is integral and has valuations \(a_p+1\) for \(p\le\sqrt{k}\), one for \(\sqrt{k}<p\le3k/4\), and zero for \(p\in O_k\).

Consider \(n=tM_k-1\), \(t\ge1\). The elementary identity

\[
(1+X)^n\equiv\prod_j(1+X^{p^j})^{n_j}\pmod p
\]

gives Lucas's criterion

\[
p\nmid\tbinom nk\quad\Longleftrightarrow\quad n_j\ge k_j
\text{ at every base-}p\text{ digit}.
\tag{13}
\]

- If \(p\le\sqrt{k}\), all relevant digits of \(n\) are \(p-1\), so the condition is automatic.
- If \(\sqrt{k}<p\le3k/4\), write \(M_k=pc_p\) with \(p\nmid c_p\), and put \(b_p=\lfloor k/p\rfloor\). The units digit is \(p-1\); the next digit fails exactly when \(tc_p\bmod p\in\{1,\ldots,b_p\}\). This event consists of \(b_p\) classes modulo \(p\), with \(w_p=b_p/p\), \(h_p=b_p\).
- If \(p\in O_k\), use the two disjoint components (8), with weights (11).

These cover every prime \(p\le k\), every relevant digit, and only the required failures. The lemma applies to the events indexed by primes, not to separate allegedly independent digit events.

Both \(2^{a_2+1}>k\) and \(3^{a_3+1}>k\) divide \(M_k\), and they are coprime. Hence \(M_k>k^2\). Every \(tM_k-1\) lies in the strict domain \(n>k+1\).

## 4. Fixed parameters proving the principal theorem

Write \(\theta(x)=\sum_{p\le x}\log p\) and \(\psi(k)=\log L_k\). Exactly,

\[
\log M_k=\psi(k)-\theta(k)+\theta(3k/4)+\theta(\sqrt{k}).
\]

The identity \(\psi(k)=\sum_{j\ge1}\theta(k^{1/j})\) and the elementary bound \(\theta(x)\le x\log x\) imply \(\psi(k)-\theta(k)=O(\sqrt{k}(\log k)^2)=o(k)\). The prime number theorem therefore gives

\[
\log M_k=(3/4+o(1))k.
\tag{14}
\]

Choose the fixed parameters

\[
z=6,\qquad A=3/28,\qquad
r=2\left\lceil\frac{Ak}{2\log k}\right\rceil.
\tag{15}
\]

For retained primes, \(w_p\le k/p^2\) and \(1-w_p\ge1/p\). On \((\sqrt{k},2\sqrt{k}]\), the sum of \(-\log(1-w_p)+\log(1+6w_p)\) is \(O(\sqrt{k}\log k)\), even when summed over all integers. Above \(2\sqrt{k}\), \(w_p\le1/4\), and the summand is at most \((4/3+6)w_p\). The integer square tail then gives

\[
\sum_{\sqrt{k}<p\le3k/4}
\log\frac{1+6w_p}{1-w_p}
=O(\sqrt{k}\log k)=o(k/\log k).
\tag{16}
\]

For omitted primes, put \(u=p/k\in(3/4,1]\). Uniformly,

\[
w_p=u^{-1}-1+O(1/k),\qquad0\le u^{-1}-1\le1/3.
\]

The function \(\log((1+6w)/(1-w))\) has bounded derivative on a fixed neighborhood of \([0,1/3]\). Replacing \(w_p\) by its limiting value causes total error \(O(1)\), even using the bound \(\#O_k\le k\). PNT on this fixed compact interval yields

\[
\sum_{p\in O_k}\log\frac{1+6w_p}{1-w_p}
=(K+o(1))\frac{k}{\log k},
\tag{17}
\]

where

\[
K=\int_{3/4}^1\log\frac{6-5u}{2u-1}\,du
=\frac9{20}\log\frac94+\frac14\log\frac12.
\tag{18}
\]

For clarity, the weighted PNT in (17) follows by uniformly approximating its continuous integrand with upper and lower step functions, applying \(\pi(vk)-\pi(uk)=(v-u+o(1))k/\log k\) on each fixed step, and then refining the partition. No shrinking-interval prime estimate is used.

The required strict margin has a simple integer certificate:

\[
A\log6-K=\frac{176\log2-111\log3}{140}>0,
\tag{19}
\]

because

\[
2^{176}=95780971304118053647396689196894323976171195136475136
\]

is greater than

\[
3^{111}=91297581665113611259115979754590511595360241199911147.
\]

Thus (16)–(19) give

\[
\log\frac{R_r(6)}\rho
=\left(K-A\log6+o(1)\right)\frac{k}{\log k}\longrightarrow-\infty.
\tag{20}
\]

In particular, \(R_r(6)\le\rho/2\) eventually. The same retained-prime estimates, and bounded omitted-prime logarithms with \(\pi(k)=O(k/\log k)\), show

\[
-\log\rho=O(k/\log k)=o(k).
\tag{21}
\]

Every compressed local weight satisfies \(h_p\le k\), including retained primes. There are at most \(k\) active primes, so \(\sum_p h_p\le k^2=:U\). Put \(m=r-1=(A+o(1))k/\log k\). For all sufficiently large \(k\), \(U\ge m\), and

\[
E_{r-1}\le\sum_{j=1}^{m}\frac{U^j}{j!}
\le m\frac{U^m}{m!}
\le m\left(\frac{eU}{m}\right)^m=:V.
\tag{22}
\]

Since \(\log m=\log k-\log\log k+O(1)\),

\[
\log V\le\log m+m(1+2\log k-\log m)
=(A+o(1))k.
\tag{23}
\]

The factor is now \(A\), rather than the \(2A\) incurred by the full prime-square residue count. For \(T\) in (7), equations (21)–(23) imply \(\log T\le(A+o(1))k\). The finite lemma gives an actual survivor \(t\le T\). Section 3 proves that \(tM_k-1\) is admissible and in the strict domain. Therefore

\[
\log g(k)\le\log(TM_k)
\le(3/4+3/28+o(1))k=(6/7+o(1))k.
\]

This proves (1). Since \(6/7<0.86<1\) and \(\log L_k\sim k\), the two eventual strict inequalities stated after (1) follow. ∎

## 5. A sharp homogeneous Bonferroni threshold

The following statement isolates a limitation that persists even if the generating-function bound \(R_r(z)\) is replaced by exact evaluation of \(Q_{r-1}\).

Let \(0\le w_i<1\), \(1\le i\le s\), let \(\rho=\prod_i(1-w_i)\), and let \(r\) be even with \(2\le r\le s\). Then

\[
\boxed{\frac rs e_r(w)\le\rho-Q_{r-1}\le e_r(w).}
\tag{24}
\]

**Proof of the new lower bound.** Apply Taylor's integral remainder at 1 to \(F(x)=\prod_{i=1}^s(1-w_i x)\). Because \(r\) is even,

\[
\rho-Q_{r-1}
=r\sum_{|J|=r}\left(\prod_{i\in J}w_i\right)
\int_0^1(1-t)^{r-1}\prod_{i\notin J}(1-w_i t)\,dt.
\tag{25}
\]

For \(0\le t\le1\), every remaining factor is at least \(1-t\). The integral is thus at least \(\int_0^1(1-t)^{s-1}\,dt=1/s\). This proves the lower bound. Dropping the remaining factors bounds the integral by \(1/r\) and reproves the upper bound. ∎

Let

\[
H(x)=-x\log x-(1-x)\log(1-x),
\]

with the continuous values at 0 and 1, and let \(\kappa\in(1/4,1)\) be the unique root

\[
H(\kappa)-\kappa\log3+\log(3/2)=0.
\tag{26}
\]

The function on the left has derivative \(\log((1-x)/(3x))\), increases up to \(1/4\), then decreases strictly, is positive at 0 and negative at 1. Thus the root is unique. Exact comparisons give

\[
\frac45<\kappa<\frac56,
\tag{27}
\]

because five times its value at \(4/5\) is \(\log(9375/8192)>0\), and six times its value at \(5/6\) is \(\log(2187/3125)<0\). Numerically only, \(\kappa\approx0.8107103751\).

Suppose, along integer \(k\to\infty\), there are \(s\le k\) weights, of which a distinguished \(N\) satisfy \(w_i\ge1/3\), with \(N/\log k\to\infty\). If even \(r\ge2\) gives \(Q_{r-1}>0\), then

\[
r\ge(\kappa-o(1))N.
\tag{28}
\]

To prove this, first suppose \(r>s\). Then \(Q_{r-1}=\rho\), the budget includes \(e_N\), and the conclusion on \(r\) is immediate because \(s\ge N\). The case \(N<r\le s\) likewise already satisfies the conclusion on \(r\), without any claim that \(Q_{r-1}=\rho\) in that case. Otherwise \(2\le r\le N\le s\), so (24), \(\rho\le(2/3)^N\), and the distinguished terms of \(e_r\) give

\[
\frac{\rho-Q_{r-1}}\rho
\ge\frac rs\binom Nr3^{-r}(3/2)^N.
\tag{29}
\]

For \(x=r/N\), the elementary entropy bound

\[
\binom Nr\ge\frac{\exp(NH(x))}{N+1}
\tag{30}
\]

holds. One proof uses the binomial distribution with success probability \(x=r/N\): the term at \(r\) is a mode, hence has mass at least \(1/(N+1)\). Fix \(\epsilon>0\). On \([0,\kappa-\epsilon]\), the continuous function in (26) is bounded below by a positive constant, provided the interval is nonempty. If \(r/N\) belonged to that interval, the right side of (29) would be at least \(2\exp(cN)/(k(k+1))\to\infty\), contradicting \(Q_{r-1}>0\). This proves (28).

**Sharpness of the threshold used in this comparison.** If all \(N=s\) weights are exactly \(1/3\), then for every fixed \(\epsilon>0\), an even \(r\) with \(r/N\ge\kappa+\epsilon\) and \(r\le N\) satisfies \(e_r(w)/\rho\le\exp(-c_\epsilon N)\), using \(\binom Nr\le\exp(NH(r/N))\). The upper bound in (24) then gives \(Q_{r-1}>0\) eventually. If \(r>N\), the polynomial is already exact. Conversely (28) excludes \(r/N\le\kappa-\epsilon\). Thus \(\kappa\) is the sharp asymptotic threshold for the homogeneous \(1/3\) comparison, not necessarily the optimal threshold for the varying weights of the full Lucas problem.

## 6. The residual exponential budget barrier

Consider any omission sets \(O_k\subseteq\{p:\sqrt{k}<p\le k\}\) and the same type of single lattice

\[
M_k=L_k\left(\prod_{p\in O_k}p\right)^{-1}
\prod_{p\le\sqrt{k}}p.
\tag{31}
\]

Use all its true local prime-failure events and their exact weights, as in Sections 2–3. The following omission hypothesis concerns this separate family; it is not satisfied by, or imposed on, the fixed \(3/4\)-cutoff construction proving (1). Suppose that all but \(o(k/\log k)\) primes in

\[
I_k=(3k/5,3k/4]
\]

are omitted. PNT gives a distinguished omitted subset of size

\[
N=(3/20+o(1))k/\log k.
\tag{32}
\]

Every such prime has \(b=1\), and (11) gives

\[
w_p\ge1/3,\qquad h_p=p>3k/5,
\qquad\beta_p\ge p(k-p)\ge3k^2/16.
\tag{33}
\]

The last inequality follows since \(u(1-u)\ge3/16\) on \([3/5,3/4]\). There are at most \(k\) active prime events. Therefore any even truncation with \(Q_{r-1}>0\) satisfies (28).

For \(E^{\mathrm{split}}_{r-1}=\sum_{j=1}^{r-1}e_j(h)\), choose any fixed \(\epsilon>0\) smaller than \(\kappa\), and then \(j=\lfloor(\kappa-\epsilon)N\rfloor\). By (28), this \(j\) is at most \(r-1\) for all sufficiently large \(k\) (apply (28) first with a smaller error, for example \(\epsilon/2\)). The distinguished terms give

\[
E^{\mathrm{split}}_{r-1}\ge\binom Nj(3k/5)^j.
\]

After taking logarithms, dividing by \(k\), using (32), and letting \(\epsilon\downarrow0\), we obtain

\[
\boxed{\displaystyle\liminf_{k\to\infty}
\frac{\log E^{\mathrm{split}}_{r-1}}k
\ge\frac{3\kappa}{20}>\frac3{25}.}
\tag{34}
\]

For the uncompressed prime-square budget \(E^{\mathrm{full}}_{r-1}=\sum_{j=1}^{r-1}e_j(\beta)\), the same argument yields

\[
\boxed{\displaystyle\liminf_{k\to\infty}
\frac{\log E^{\mathrm{full}}_{r-1}}k
\ge\frac{3\kappa}{10}>\frac6{25}.}
\tag{35}
\]

The \(o(1)\) statements in (28), (32), (34), and (35) refer to any sequence of omission sets and even truncations satisfying the displayed hypotheses.

Any proof of survival based solely on the positive lower certificate \(TQ_{r-1}-E_{r-1}>0\) needs \(Q_{r-1}>0\), and then \(T>E_{r-1}/Q_{r-1}\ge E_{r-1}\), because \(Q_{r-1}\le\rho\le1\). Thus (34) forces positive exponential multiplier cost even with the compressed budget. In particular, if \(\log M_k=o(k)\), the omission hypothesis automatically holds: the retained primes in \(I_k\) all divide \(M_k\), so their number is at most \(\log M_k/\log(3k/5)=o(k/\log k)\). Such a subexponential lattice cannot, through this absolute-error Bonferroni certificate, prove an \(\exp(o(k))\) witness.

This is not an impossibility theorem for more refined sieves, cancellations among endpoint errors, averaging over multiple digit patterns, or the true first survivor. The quantities \(E\) are explicit upper budgets used by this method; proving that these budgets are large does not prove that the actual discrepancies are large. The cylinder-count minimality in Section 2 identifies why merely subdividing or recombining the same unsigned prime-power cylinders cannot remove this remaining budget cost.

## 7. Verification of the earlier generating-function observation

For completeness, the weaker proposed obstruction can be verified directly without the Taylor argument. Under (32)–(33), if \(0<z\le1\), then \(R_r(z)/\rho>1\). If \(z>1\), each distinguished prime contributes

\[
\frac{1+zw_p}{1-w_p}\ge\frac{z+3}{2}\ge\sqrt{3z}.
\]

All other factors are at least one. Consequently, if \(r\le N/2\), then

\[
R_r(z)/\rho\ge3^{N/2}z^{N/2-r}>1.
\]

Thus the condition \(R_r(z)\le\rho/2\) requires \(r>N/2\). Taking \(j=\lfloor N/2\rfloor\le r-1\) in the uncompressed budget proves \(\log E^{\mathrm{full}}_{r-1}\ge(3/20+o(1))k\). That observation is correct. Equations (34)–(35) strengthen it and avoid making the barrier depend on use of a generating-function estimate.

## 8. Scope and sources

The original lcm-lattice construction is due to Ecklund, Erdős and Selfridge, *A New Function Associated with the Prime Factors of (n choose k)*, Mathematics of Computation 28 (1974), 647–649: https://www.renyi.hu/~p_erdos/1974-01.pdf . Its printed pages 648–649 were freshly consulted. The previously accepted reduced-lattice proof established coefficient \(813/875\) using the full prime-square budget. The present proof preserves that construction's valid digit conditions while replacing its endpoint estimate by (5), (9).

The standard sieve input is the classical Brun/Bonferroni truncation. Kevin Ford, *Sieve Methods Lecture Notes, Spring 2023*, Theorem 1.5 and Lemma 1.6, https://ford126.web.illinois.edu/sieve2023.pdf , were freshly inspected. The finite proof is reproduced here so that the different-modulus accounting and initial-interval conclusion can be checked directly. No new general sieve principle is claimed.

The 2021 v3 document by Sorenson, Sorenson and Webster is an addendum, https://arxiv.org/html/1907.08559v3 . Its inspection supplies background only; no asserted uniform first-residue heuristic is used as a proof premise.

The main bound remains exponential. Neither subexponential growth nor either successive-ratio conjecture is proved. No all-\(k\) strict lcm comparison, effective onset, novelty, priority, or exhaustive literature claim is made. The independent exact checker is supplementary regression evidence, not a substitute for the asymptotic proof.
