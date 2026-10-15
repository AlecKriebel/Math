# A sharp barrier for a two-point relaxation of the one-exceptional-sum problem

12 October 2026. Authored analytic diagnostic for row 1741, problem 2350 / Erdős 864.

## Scope and conclusion

The original problem concerns an integer set (A\subseteq\{1,\ldots,N\}) for which at most one integer has more than one representation (a+b), where representations are unordered and equal summands are allowed. Its proposed upper leading constant is (2/\sqrt3). The reflected-Sidon lower construction does not establish that upper bound.

This note does **not** improve the absolute upper bound or produce an integer counterexample. It proves an exact obstruction to one particular analytic approach. The natural macroscopic convolution relaxation of the symmetric case has optimal leading constant (\sqrt2), strictly above the proposed (2/\sqrt3). Its unique maximizing measure is uniform. Thus that relaxation, even with the disjointness of positive-radius sums and differences retained as a packing inequality, cannot establish the conjectured constant.

All arguments below are supplied here. No novelty claim or claim about exhaustion of other proof approaches is made.

## 1. Exact finite packing

Let (B\subseteq\{1,\ldots,L\}), (k=|B|), and let (C=B\cup(-B)). For positive integers (j), define

\[
d_B(j)=\#\{(b,c)\in B^2:b-c=j\},\qquad
s_B(j)=\#\{(b,c)\in B^2:b\le c,\ b+c=j\}.
\]

Then (C) has at most one repeated unordered sum, with zero as the only possible repeated sum, if and only if

\[
d_B(j)+s_B(j)\le 1\quad(j>0). \tag{1}
\]

Indeed, a representation of a positive integer by two elements of (C) has either two positive summands, counted by (s_B), or one positive and one negative summand, counted by (d_B). Two negative summands cannot yield a positive sum. Reflection gives the identical assertion for negative sums; zero has exactly the (k) pairs \(\{-b,b\}\). This also handles (k=0,1).

In particular (B) is Sidon, all its positive differences are distinct, and its positive-difference set is disjoint from its unordered-sum set. The disjointness is precisely the absence of an equation (b_1+b_2+b_3=b_4) in (B), allowing repetitions. Conversely, these three conditions imply (1). For an ordinary integer Sidon set, unique unordered sums and unique positive differences are equivalent: an equality (a-b=c-d>0) yields (a+d=c+b), and a repeated unordered sum yields a repeated positive difference after sorting its summands.

For every nonnegative function \(\phi\) on \((0,2]\), (1) gives the exact finite weighted inequality

\[
\frac1L\sum_{j=1}^{2L}\phi(j/L)\{d_B(j)+s_B(j)\}
\le \frac1L\sum_{j=1}^{2L}\phi(j/L). \tag{2}
\]

This assertion includes arbitrary nonnegative weights, not just interval indicators or triangular weights.

## 2. Necessary continuum inequalities

Consider any sequence of such sets with (L\to\infty), and normalize their counting measures by

\[
\nu_L=L^{-1/2}\sum_{b\in B}\delta_{b/L}.
\]

The difference count yields (k(k-1)/2\le L-1), so the masses of \(\nu_L\) are uniformly bounded. Pass to any weakly convergent subsequence \(\nu_L\to\nu\), supported on \([0,1]\). Write \(\widetilde\nu(E)=\nu(-E)\), and let \(\lambda\) denote Lebesgue measure on \(\mathbb R\).

The following are necessary conditions:

\[
\nu*\widetilde\nu\le\lambda, \tag{D}
\]

\[
\left.(\nu*\widetilde\nu)\right|_{(0,\infty)}
+\tfrac12\left.(\nu*\nu)\right|_{(0,\infty)}
\le\left.\lambda\right|_{(0,\infty)}. \tag{P}
\]

Here inequalities mean domination of nonnegative measures, equivalently inequalities against all nonnegative continuous compactly supported test functions.

To prove (D), the exact autocorrelation is

\[
\nu_L*\widetilde\nu_L
=\frac{k}{L}\delta_0+
\frac1L\sum_{j=1}^{L-1}d_B(j)(\delta_{j/L}+\delta_{-j/L}).
\]

Since (d_B(j)\le1), its non-diagonal part is bounded by the lattice Riemann-sum measure on \([-1,1]\). The diagonal mass (k/L) tends to zero. Weak convergence of the convolutions follows from weak convergence of the measures on the common compact support. Passing to the limit proves (D).

For (P), take a continuous test function compactly supported in \((0,\infty)\). The exact sum identity is

\[
\frac1L\sum_j s_B(j)\delta_{j/L}
=\tfrac12\nu_L*\nu_L+
\frac1{2L}\sum_{b\in B}\delta_{2b/L}. \tag{3}
\]

The last measure has mass (k/(2L)\to0). Substituting (3) and the positive part of the autocorrelation into (2), then passing to the Riemann-sum limit, proves (P). There is no assertion of convergence of individual lattice occupancies.

## 3. The relaxation is solved exactly

Let \(\mathcal R\) be the set of all nonnegative measures \(\nu\) supported on \([0,1]\) satisfying (D) and (P). Then

\[
\max_{\nu\in\mathcal R}\nu([0,1])=1, \tag{4}
\]

and the unique maximizing measure is \(\nu=\lambda|_{[0,1]}\).

First, (D) forces \(\nu=f\,dx\) with (f\in L^2(\mathbb R)), (f\ge0), supported on \([0,1]\), and

\[
\int_0^1 f(x)^2\,dx\le1. \tag{5}
\]

For a direct proof, put \(\eta_\varepsilon=\varepsilon^{-1}1_{[-\varepsilon/2,\varepsilon/2]}\). Tonelli's theorem gives

\[
\|\nu*\eta_\varepsilon\|_2^2
=\int (\eta_\varepsilon*\widetilde\eta_\varepsilon)(t)
\,d(\nu*\widetilde\nu)(t)
\le\int (\eta_\varepsilon*\widetilde\eta_\varepsilon)(t)\,dt=1.
\]

Weak compactness of the unit ball of (L^2), together with convergence of this approximate identity against continuous compactly supported tests, identifies \(\nu=f\,dx\). Weak lower semicontinuity gives (5). Cauchy–Schwarz now yields \(\int_0^1f\le1\). Equality forces (f=1) almost everywhere on \([0,1]\).

It remains to check that this equality case satisfies the extra packing constraint. For \(f=1_{[0,1]}\),

\[
(f*\widetilde f)(t)=(1-|t|)_+,
\]

and

\[
(f*f)(t)=
\begin{cases}
t,&0\le t\le1,\\
2-t,&1\le t\le2,\\
0,&\text{otherwise}.
\end{cases}
\]

Thus (D) holds, and the left-hand density in (P) is exactly

\[
(f*\widetilde f)(t)+\tfrac12(f*f)(t)
=1-\tfrac t2\quad(0<t<2), \tag{6}
\]

and is zero for (t>2). This is everywhere at most one. It proves attainability and completes (4).

## 4. Consequence for the proposed proof route

Translating (C=\pm B) by (L+1) gives an admissible set in \(\{1,\ldots,2L+1\}\) of size (2k). In this symmetric subclass, the proposed (2/\sqrt3) bound would imply

\[
\limsup\frac{k}{\sqrt L}\le\sqrt{\frac23}.
\]

But (D) and (P), which retain all of the macroscopic nonnegative weighted inequalities (2), allow mass one. Their exact relaxed optimum corresponds to the original leading constant (\sqrt2).

The uniform measure in Section 3 is a counterexample to the proposed *analytic implication* “(D) and (P) force mass at most \(\sqrt{2/3}\).” It is **not** an integer set and is not a counterexample to Erdős 864. No sequence of admissible integer sets approaching this uniform relaxed maximizer has been constructed here. A proof of the proposed sharper bound must use additional information beyond these two limiting measure dominations, for example information about correlations between the microscopic occupied sum and difference sites that is lost when (1) is weakly averaged.

In particular, one must not replace (1) by a claim that the limiting sum and difference densities have disjoint supports. Such disjointness is generally not preserved by weak limits of mutually singular measures. Equation (6) demonstrates exactly the overlap allowed by the correct necessary condition. The realizability of the particular overlapping pair of convolution densities is not asserted.

## 5. Rigidity and a conditional sharp bound

If \(\nu\in\mathcal R\) has mass (c), its density satisfies the explicit stability inequality

\[
\int_0^1(f(x)-c)^2\,dx
=\int_0^1f(x)^2\,dx-c^2
\le1-c^2. \tag{7}
\]

Consequently any actual sequence in the symmetric subclass with (k/\sqrt L\to1), if one exists, has the unique weak profile \(\lambda|_{[0,1]}\). Every subsequential limit has mass one and is the unique maximizer established above. This is a necessary structural condition, not an existence assertion.

More generally, if a limiting profile is supported on a measurable set of length at most (a), then Cauchy–Schwarz and (5) give (c\le\sqrt a\). In particular a macroscopic central gap removing the bottom third of the positive radii forces (c\le\sqrt{2/3}\), which is the proposed constant in the symmetric case. There is no proof here that arbitrary extremal sets have such a gap. Indeed a hypothetical sequence approaching the relaxed constant one would instead be uniform, by (7).

## Verification and provenance

The exact original formulation and normalization were checked against the retained row-1741 statement and the prior screen's mathematical statement. The source problem is [Erdős problem 864](https://www.erdosproblems.com/864); the original historical discussion is Erdős, *Some of my Forgotten Problems in Number Theory*, printed pages 39–40. No assertion about a current website status label is used.

The independently authored finite diagnostic, not distributed in this prose edition, exhausts all (B\subseteq\{1,\ldots,L\}\) for (0\le L\le16). It verifies the exact characterization (1), equivalence with Sidon plus the triple-sum exclusion, identity (3), and the autocorrelation identity. It separately checks the piecewise-linear identity (6) using exact rational arithmetic. These finite checks are diagnostics; the proofs above do not depend on an asymptotic extrapolation from them.
