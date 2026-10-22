# A three-point counterexample to the random generalized-lattice discrepancy comparison

## Result and scope

Let \(z,\Delta\) be independent continuous uniform random variables on \([0,1)\), and set
\[
 t_j=\{jz+\Delta\},\qquad j=0,1,2.
\]
For three independent uniform points \(U_0,U_1,U_2\), define the same normalized anchored discrepancy by
\[
 \operatorname{disc}_4(t_0,t_1,t_2)^4
 =\int_0^1\left|\frac13\sum_{j=0}^2\mathbf 1_{[0,x)}(t_j)-x\right|^4\,dx.
\]
Then
\[
 \boxed{\quad
 \mathbb E_{z,\Delta}\operatorname{disc}_4(t_0,t_1,t_2)^4
 =\frac{19}{1620}
 >\frac{4}{405}
 =\mathbb E\operatorname{disc}_4(U_0,U_1,U_2)^4.
 \quad}
\]
The difference is \(1/540\), and the ratio is \(19/16\). Thus the proposed universal inequality is false at \(n=3,d=1,p=4\), with exactly the continuous generator, independent continuous shift, anchored boxes, and normalization in the question. Using \([0,1]\) in place of \([0,1)\) has no effect on any expectation.

The question is recorded by Erich Novak, reporting joint work with Aicke Hinrichs, in *New bounds for the star discrepancy*, in *Discrepancy Theory and Its Applications*, Oberwolfach Report 13/2004, pp. 696–699, especially the discrepancy definition on p. 697 and the displayed comparison on p. 698: [DOI 10.4171/OWR/2004/13](https://doi.org/10.4171/OWR/2004/13). The argument below is self-contained. Its correctness does not depend on any novelty assertion or computation.

## 1. Uniform pairs and a triple-inclusion probability

Write \(u=t_0=\Delta\) and \(v=t_1=\{z+\Delta\}\). The variables \(u,v\) are independent uniforms: conditional on any \(\Delta\), addition modulo one preserves the uniform law of \(z\). Moreover,
\[
 t_2=\{2v-u\}.
\]
All three pairs of points are independent uniform pairs. For \((t_0,t_2)\), conditional on \(\Delta\), the variable \(\{2z+\Delta\}\) is uniform, because multiplication by the integer two preserves uniform measure on the circle. For \((t_1,t_2)\), first condition on \(z\): \(t_1\) is uniform and independent of \(z\), and \(t_2=\{t_1+z\}\).

Fix \(0\le x\le 1/2\), and put
\[
 q(x)=\mathbb P(t_0<x,\ t_1<x,\ t_2<x).
\]
On the event \(u,v\in[0,x)\), we have \(-x<2v-u<2x\). If \(2v-u<0\), its fractional part is at least \(1-x\ge x\); if \(2v-u\ge0\), there is no wrap at one except on irrelevant boundary sets. Consequently the third inclusion is equivalent, up to a null set, to
\[
 0\le 2v-u<x.
\]
For each \(u\in[0,x]\), the admissible interval for \(v\) is
\([u/2,(u+x)/2]\), of length \(x/2\), and this lies inside \([0,x]\). Therefore
\[
 \boxed{q(x)=x^2/2\qquad(0\le x\le1/2).}
\]

## 2. The exact lattice fourth moment

Let \(N_x=\sum_{j=0}^2\mathbf1_{[0,x)}(t_j)\), and write \(P_k(x)=\mathbb P(N_x=k)\). Uniform marginals and pairwise independence give
\[
 \mathbb EN_x=3x,\qquad
 \mathbb E\binom{N_x}{2}=3x^2,\qquad P_3=q.
\]
Solving these identities yields
\[
 \begin{aligned}
 P_3&=q,&P_2&=3x^2-3q,\\
 P_1&=3x-6x^2+3q,&P_0&=1-3x+3x^2-q.
 \end{aligned}
\]
For \(0\le x\le1/2\), insertion of \(q=x^2/2\) gives
\[
 (P_0,P_1,P_2,P_3)
 =\left(1-3x+\frac52x^2,\quad3x-\frac92x^2,
 \quad\frac32x^2,\quad\frac12x^2\right).
\]
The integrand's expected value is thus the following explicit polynomial:
\[
 \begin{aligned}
 F(x)&=\mathbb E(N_x/3-x)^4
       =\sum_{k=0}^3P_k(x)(k/3-x)^4\\
 &=x^4-\frac{10}{9}x^3+\frac{8}{27}x^2+\frac{x}{27},
 \qquad0\le x\le1/2.
 \end{aligned}
\]
The joint point distribution is invariant under reflection of every point modulo one, since replacing \((z,\Delta)\) by \((-z,-\Delta)\) modulo one preserves its distribution. Reflection sends \(N_x/3-x\) to the negative of \(N_{1-x}/3-(1-x)\), in distribution and off null boundary events. Hence \(F(1-x)=F(x)\). Fubini's theorem applies directly to this bounded nonnegative integrand, so
\[
 \begin{aligned}
 \mathbb E\operatorname{disc}_4(t_0,t_1,t_2)^4
 &=2\int_0^{1/2}F(x)\,dx\\
 &=2\left(\frac1{160}-\frac5{288}
                +\frac1{81}+\frac1{216}\right)
 =\frac{19}{1620}.
 \end{aligned}
\]

## 3. The iid fourth moment

For any \(n\ge1\), let \(B_1,\ldots,B_n\) be independent Bernoulli variables with success probability \(x\). With \(Y_i=B_i-x\),
\[
 \mathbb EY_i^2=x(1-x),\qquad
 \mathbb EY_i^4=x(1-x)\bigl(1-3x(1-x)\bigr).
\]
Expanding the fourth power and using independence and zero means gives
\[
 \mathbb E\left(\frac1n\sum_iY_i\right)^4
 =\frac{n\mathbb EY_1^4+3n(n-1)(\mathbb EY_1^2)^2}{n^4}.
\]
Since
\[
 \int_0^1x(1-x)\,dx=\frac16,\qquad
 \int_0^1x^2(1-x)^2\,dx=\frac1{30},
\]
the iid normalized anchored fourth moment in dimension one is
\[
 \boxed{\mathbb E\operatorname{disc}_4(U_1,\ldots,U_n)^4
 =\frac{3n-1}{30n^3}.}
\]
At \(n=3\) this is \(4/405=16/1620\), proving the strict comparison above.

## 4. A second proof of failure, using only large empty tails

There is also a counterexample at \(n=4,d=1,p=4\) that needs no calculation of the whole lattice moment.

More generally, let \(n\ge3\). On the triangle
\[
 T_+=\{(z,\Delta):0\le z\le1/(n-1),\quad
                         0\le\Delta\le1-(n-1)z\},
\]
there is no wraparound, and all points lie between \(\Delta\) and \(\Delta+(n-1)z\). For \(x<\Delta\), the empirical count is zero; for \(x>\Delta+(n-1)z\), it is \(n\). The two tail intervals alone therefore contribute at least
\[
 \frac{\Delta^5+(1-\Delta-(n-1)z)^5}{5}
\]
to \(\operatorname{disc}_4^4\). Integrating over \(T_+\) gives
\[
 \begin{aligned}
 &\int_0^{1/(n-1)}\!\int_0^{1-(n-1)z}
 \frac{\Delta^5+(1-\Delta-(n-1)z)^5}{5}\,d\Delta\,dz\\
 &\hspace{20mm}=\int_0^{1/(n-1)}
                    \frac{(1-(n-1)z)^6}{15}\,dz
 =\frac1{105(n-1)}.
 \end{aligned}
\]
A disjoint triangle with \(z\) near one gives the same amount: write \(z=1-w\), where \(0\le w\le1/(n-1)\), and take \((n-1)w\le\Delta\le1\). The points then descend from \(\Delta\) to \(\Delta-(n-1)w\). These two triangles have disjoint interiors when \(n\ge3\). Nonnegativity on the rest of the parameter square proves
\[
 \mathbb E\operatorname{disc}_4(M_n^{z,\Delta})^4
 \ge\frac2{105(n-1)}.
\]
For \(n=4\), comparison with Section 3 yields the second strict counterexample:
\[
 \mathbb E\operatorname{disc}_4(M_4^{z,\Delta})^4
 \ge\frac2{315}
 >\frac{11}{1920}
 =\mathbb E\operatorname{disc}_4(U_1,U_2,U_3,U_4)^4,
\]
where the lower-bound margin is exactly \(5/8064>0\). This proof also explains why continuous random generators cause a problem: a positive-measure set of nearly stationary rotations produces large discrepancies.

## 5. Boundary checks and limits of the conclusion

- For \(n=1\), the lone point is uniform. For \(n=2\), \((\Delta,\{z+\Delta\})\) is an iid uniform pair, coordinate by coordinate. Thus both ensembles have identical laws for all dimensions and every exponent for which the discrepancy is defined. The counterexample uses the smallest possible point count.
- For every \(n,d\), any two distinct indexed points are independent uniform points. Indeed, \(t_j\) is independent of \(z\), and \(t_k=\{t_j+(k-j)z\}\); multiplication by a nonzero integer preserves uniform measure on each circle. Consequently
  \[
   \mathbb E\operatorname{disc}_2(M_n^{z,\Delta})^2
   =\frac{2^{-d}-3^{-d}}{n}
   =\mathbb E\operatorname{disc}_2(M_n^{\mathrm{iid}})^2.
  \]
  This equality does not extend to the fourth moment, as proved above.
- Points are counted by their indices with the coefficient \(1/n\). Parameter values causing collisions or points on box boundaries form null sets and are not deleted or conditioned away.
- The negative answer concerns the displayed expected-moment comparison. It does not negate the existence of well-chosen lattice generators or other discrepancy estimates, nor does it claim an exhaustive literature-based novelty result.
