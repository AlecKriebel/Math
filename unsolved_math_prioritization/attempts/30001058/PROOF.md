# Exact dimension-two dilation thresholds

## Scope and quantifiers

This is an elementary dimension-two calculation. It does not settle the optimization problem in other dimensions, establish novelty, or certify the current status of the general problem.

Fix the ambient degree parameter $d=2$, even when the input has smaller degree. Let

\[
\mathcal H=\{a+bt+ct^2:a\in\mathbb Z_{\ge1},\ b,c\in\mathbb Z_{\ge0}\}.
\]

For $h\in\mathcal H$, define $g$ and $U_n$, for every positive integer $n$, by

\[
\frac{h(t)}{(1-t)^3}=\sum_{k\ge0}g(k)t^k,
\qquad
\frac{U_nh(t)}{(1-t)^3}=\sum_{k\ge0}g(nk)t^k.
\]

Write $U_nh(t)=a+B_n t+C_n t^2$. The symbols $m,N$ below are positive integers; $n$ is an integer dilation parameter, not a real variable in the quantified claims.

Three packages must be distinguished:

1. **Unconditional package:** for every $h\in\mathcal H$ and every $n\ge N$, $U_nh$ has degree two, distinct negative real roots, positive strictly log-concave coefficients, and $a,B_n,C_n<mC_n$. For each fixed $h$, its ordered roots converge to $-1,0$ as $n\to\infty$.
2. **Full original-theorem package:** the unconditional package, with the additional requirement that every $h\in\mathcal H$ satisfying $a+b>c$ obeys $a<C_n<B_n<mC_n$ for every $n\ge N$. A single threshold $N$ is used for both parts.
3. **Polygon package:** for every two-dimensional lattice polygon $P$ and every $n\ge N$, the same root and coefficient assertions hold for $\delta_{nP}$, together with $1<C_n<B_n<mC_n$.

The exact feasible sets are

\[
\begin{array}{ll}
\text{Unconditional:}&N\ge3,\quad m>\dfrac{N+4}{N-2};\\[3pt]
\text{Full original theorem and polygons:}&N\ge4,\quad m>\dfrac{N+4}{N-2}.
\end{array}
\]

For integer $m$, the strict inequality means

\[
m\ge \left\lfloor\frac{N+4}{N-2}\right\rfloor+1.
\]

## 1. Recovering the operator exactly

The generating function gives, as a polynomial in $k$,

\[
g(k)=a\binom{k+2}{2}+b\binom{k+1}{2}+c\binom{k}{2}
=\frac{(a+b+c)k^2+(3a+b-c)k+2a}{2}.
\]

Multiplication of the series for $g(nk)$ by $(1-t)^3$ gives the numerator coefficients

\[
h_0(n)=g(0)=a,\quad B_n=g(n)-3g(0),\quad
C_n=g(2n)-3g(n)+3g(0).
\]

Every coefficient of degree at least three vanishes, since it is a third finite difference of the quadratic polynomial $g(nk)$. Thus

\[
 B_n=\frac{(n^2+3n-4)a+n(n+1)b+n(n-1)c}{2},
\]
\[
 C_n=\frac{(n-1)(n-2)a+n(n-1)b+n(n+1)c}{2}.
\]

These are integers, either from coefficient extraction or because each displayed multiplier is integral for integer $n$. At $n=1$ they return $B_1=b,C_1=c$.

## 2. Degree, positivity, roots, and log-concavity

Put

\[
A=\frac{(n-1)(n+4)}2,\quad D=\frac{(n-1)(n-2)}2,
\quad E=\frac{n(n+1)}2,\quad F=\frac{n(n-1)}2.
\]

Then $B_n=Aa+Eb+Fc$, $C_n=Da+Fb+Ec$. For $n\ge3$, all four multipliers are positive, so $a,B_n,C_n>0$, and the degree is exactly two. The discriminant expands as

\[
 B_n^2-4aC_n=(A^2-4D)a^2+(2AE-4F)ab+(2AF-4E)ac
 +E^2b^2+2EFbc+F^2c^2.
\]

Direct factorization gives

\[
A^2-4D=\frac{n^2(n-1)(n+7)}4,
\quad 2AE-4F=\frac{n^2(n-1)(n+5)}2,
\]
\[
2AF-4E=\frac{n^2(n^2+2n-11)}2.
\]

All three are positive for $n\ge3$: the last quadratic is $4$ at $n=3$ and strictly increasing thereafter. Since $a\ge1$, the discriminant is strictly positive. With positive $B_n,C_n,a$, the two real roots have negative sum and positive product; hence both are strictly negative. Also $B_n^2>4aC_n>aC_n$, the strict log-concavity inequality for three coefficients.

For a fixed input set $S=a+b+c>0$. Then $B_n/n^2\to S/2$, $C_n/n^2\to S/2$, and $a/n^2\to0$. More explicitly, the ordered roots are

\[
\beta_1(n)=\frac{-B_n-\sqrt{B_n^2-4aC_n}}{2C_n},
\qquad
\beta_2(n)=\frac{-B_n+\sqrt{B_n^2-4aC_n}}{2C_n}.
\]

Dividing numerator and denominator by $n^2$ yields $\beta_1(n)\to-1$, $\beta_2(n)\to0$. The original Eulerian convention counts permutations of two elements by one plus their number of descents, so $A_2(t)=t+t^2$; these are precisely its roots. The convergence statement fixes $h$ first; no uniform-in-$h$ convergence claim is needed.

## 3. Exact coefficient extremum and the strict bound

For $n\ge3$,

\[
\frac{B_n}{C_n}=
\frac{(Da)(A/D)+(Fb)(E/F)+(Ec)(F/E)}{Da+Fb+Ec}.
\]

This is a weighted average, with positive first weight and nonnegative remaining weights. Its column ratios are

\[
R(n)=\frac{n+4}{n-2},\qquad \frac{n+1}{n-1},\qquad\frac{n-1}{n+1}.
\]

They are strictly decreasing in that order: the first difference has numerator $4n-2>0$ over $(n-2)(n-1)$, and the second has numerator $4n>0$ over $n^2-1$. Consequently

\[
\frac{B_n}{C_n}\le R(n),
\]

with equality exactly when $b=c=0$. Such an input is admissible for every integer $a\ge1$. Meanwhile

\[
\frac a{C_n}\le\frac1D\le1<R(n),\qquad \frac{C_n}{C_n}=1<R(n).
\]

Thus the maximum of all three coefficient ratios, over all inputs, is exactly $R(n)$, attained in the middle coefficient. Since

\[
R(n)=1+\frac6{n-2}
\]

is strictly decreasing, $a,B_n,C_n<mC_n$ for every input and every $n\ge N\ge3$ is equivalent to $m>R(N)$. Equality $m=R(N)$ fails, rather than being allowed, because the extremum is attained. This proves sufficiency and sharpness of the ratio condition.

The input $h=1$, at $n=2$, has $U_2h=1+3t$, with $C_2=0$. Every proposed threshold $N\le2$ includes this dilation and fails degree, coefficient positivity, and the strict coefficient bound. This proves the unconditional feasible set.

## 4. The conditional clause in the original theorem

In dimension two the source's index range $0\le i\le\lfloor d/2\rfloor-1$ contains only $i=0$. Its additional hypothesis, including the requirement that at least one inequality be strict, is exactly $a+b>c$. Its conclusion becomes $a<C_n<B_n<mC_n$.

If $n\ge4$, then $D\ge3$ and hence $C_n\ge Da\ge3a>a$. Independently,

\[
B_n-C_n=3(n-1)a+n(b-c).
\]

Under $a+b>c$, $b-c>-a$, so

\[
B_n-C_n>(2n-3)a>0.
\]

Together with the unconditional package, this proves sufficiency for $N\ge4,m>R(N)$. The input $h=1$ satisfies the additional hypothesis, but $U_3h=1+7t+t^2$ has $C_3=a=1$; thus any $N\le3$ fails strict alternation at $n=3$. The same input attains $R(N)$, so the coefficient bound cannot improve when restricted to inputs satisfying the additional hypothesis. This proves the full original-theorem feasible set.

## 5. Lattice polygons and the extremizing polygon

For a lattice polygon, write $I$ for its number of interior lattice points and $q\ge3$ for its number of boundary lattice points, in its affine lattice. The polygon Ehrhart formula (equivalently, Pick's theorem) gives

\[
\delta_P(t)=1+(I+q-3)t+It^2.
\]

Thus $a=1,b=I+q-3,c=I$, so $b-c=q-3\ge0$. In particular $a+b>c$, and the preceding result proves all assertions for $N\ge4,m>R(N)$. Alternatively, $B_n-C_n=3(n-1)+n(q-3)>0$ and $C_n>1$ directly establish alternation for $n\ge4$. The coefficient inequality $b\ge c$ is also the dimension-two instance of Proposition 4.2 in Jochemko's paper; no classification of possible polygon $\delta$-vectors is needed.

The unimodular triangle $T=\operatorname{conv}\{(0,0),(1,0),(0,1)\}$ is an actual two-dimensional lattice polygon with $\delta_T(t)=1$. Indeed, $L_T(k)=(k+1)(k+2)/2$, so its generating numerator is $1$. It supplies the equality witness at $n=3$ and attains $R(n)$ for every $n\ge3$. The bounds are therefore necessary within actual polygons, not merely within an algebraic superset of their coefficient vectors.

## 6. Integer optimization and boundary checks

For the unconditional package, smallest $N$ is $3$, and at $N=3$, $R(3)=7$, so smallest compatible $m$ is $8$. For the full original theorem and polygon package, smallest $N$ is $4$, and $R(4)=4$, so smallest compatible $m$ is $5$.

For all three packages, $m=1$ is impossible because $C_n<mC_n$ fails. For $m=2$, the strict inequality $R(N)<2$ is equivalent to $N>8$; thus the smallest compatible $N$ is $9$. At $N=8$, $h=1$ gives equality $B_8=2C_8$, not a valid strict bound.

The coordinatewise nondominated pairs $(N,m)$ are

- Unconditional: $(3,8),(4,5),(5,4),(6,3),(9,2)$.
- Full original theorem and polygons: $(4,5),(5,4),(6,3),(9,2)$.

Equivalently, for a specified integer $m\ge2$, the least admissible unconditional $N$ is $3+\lfloor6/(m-1)\rfloor$; for either full package it is the maximum of this number and $4$. There is no single feasible pair that minimizes both coordinates simultaneously.

## Sources and boundaries of the claim

- Matthias Beck, joint work with Alan Stapledon, *Asymptotics of Ehrhart series of lattice polytopes*, in *Discrete Geometry*, Oberwolfach Report 44/2008, printed pp. 2498–2500. The definition and Eulerian convention are on p. 2498; Theorem 2, Corollary 3 and the optimization question are on p. 2499. [Official report](https://ems.press/content/serial-article-files/46191).
- Beck–Stapledon, *On the Log-Concavity of Hilbert Series of Veronese Subrings and Ehrhart Series*, arXiv:0804.3639v3, pp. 1–3. This related manuscript uses $h_0=1$ in the inspected PDF theorem and has a differently worded conditional hypothesis. The OWR report controls the present target. [Version record](https://arxiv.org/abs/0804.3639v3).
- Katharina Jochemko, *On the real-rootedness of the Veronese construction for rational formal power series*, arXiv:1602.09139v2, Theorem 1.1 on pp. 2–3 and Proposition 4.2/Corollary 4.4 on p. 9. Her denominator exponent is a parameter called $d$, so the current operator is $U^{3}_{n,0}$ in that notation. The real-rootedness results do not by themselves impose the full-degree, coefficient-ratio, and strict-alternation package here. [Version record](https://arxiv.org/abs/1602.09139v2).

The proof of the thresholds above is the explicit elementary calculation, not a claim that the cited later result leaves every aspect of the original problem unsolved. No current all-dimensional status or novelty assertion is made.
