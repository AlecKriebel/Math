# Finite-cutoff Nyman–Beurling distances: partial results and exact gaps

## Status and scope

**Status: unsolved.** Neither right-continuity at every cutoff nor strict decrease between arbitrary positive cutoffs is proved here. The results below are partial statements with proofs, not a resolution of the two-part question. No novelty is asserted for the partial lemmas.

The problem is the second and third question in M. Balazard's section 8 of the problem session in *Dirichlet Series and Function Theory in Polydiscs*, Oberwolfach Reports 06/2014, printed p. 390, DOI [10.4171/OWR/2014/06](https://doi.org/10.4171/OWR/2014/06). We work in

\[
 H=L^2((0,\infty),dt/t^2),\qquad
 \chi=\mathbf1_{(1,\infty)},\qquad e_a(t)=\{t/a\},
\]
\[
 E_\lambda=\overline{\operatorname{span}}\{e_a:1\leq a\leq\lambda\},
 \qquad D(\lambda)=\|\chi-P_{E_\lambda}\chi\|\quad(\lambda>1).
\]

Taking the closed span does not change the infimum distance. We also use the natural endpoint definition at \(\lambda=1\), explicitly as an extension. Values at individual breakpoints are irrelevant in this Hilbert space. Inner products are linear in their first argument; all displayed witnesses are real.

## 1. Strong parameter continuity and what it proves

### Proposition 1

The map \(a\mapsto e_a\) is continuous from \((0,\infty)\) into \(H\). The function \(D\) is nonincreasing and left-continuous at every \(\lambda>1\).

**Proof.** If \(a\) ranges over a compact interval with lower endpoint \(a_0>0\), then

\[
 |e_a(t)|\leq\min(t/a_0,1).
\]

The square of this majorant is integrable against \(dt/t^2\). As \(a\to a_*\), pointwise convergence holds except at the countable set \(t/a_*\in\mathbb N\). Dominated convergence proves the assertion.

The spaces \(E_\lambda\) are nested, proving monotonicity. Also

\[
 E_\lambda=\overline{\bigcup_{1<r<\lambda}E_r}.
\]

Indeed all generators with parameter below \(\lambda\) belong to the union, and \(e_\lambda\) is the norm limit of generators whose parameters increase to \(\lambda\). Given \(\eta>0\), choose a finite linear combination approximating the distance at \(\lambda\), replace any endpoint generators by slightly smaller ones, and obtain a vector in some \(E_r\) with approximation error at most \(D(\lambda)+\eta\). Monotonicity gives the opposite inequality. Thus \(D(r)\to D(\lambda)\) as \(r\uparrow\lambda\). ∎

In particular, \(D\) has at most countably many discontinuities; any discontinuity is a downward right jump. This does not prove that there are none.

### Exact right-limit obstruction

Put

\[
 E_{\lambda+}=\bigcap_{\varepsilon>0}E_{\lambda+\varepsilon}.
\]

For a decreasing sequence of closed subspaces, their orthogonal projections converge strongly to the projection onto their intersection. Here is the short proof. If \(V_{n+1}\subseteq V_n\) and \(p_n=P_{V_n}x\), then for \(m\geq n\),

\[
 \|p_n-p_m\|^2=\|p_n\|^2-\|p_m\|^2.
\]

The right side tends to zero because the norms decrease. The limit belongs to every \(V_n\), and the residual is perpendicular to their intersection. Applying this to \(E_{\lambda+1/n}\),

\[
 D(\lambda+)^2
 =D(\lambda)^2-
 \|P_{E_{\lambda+}\cap E_\lambda^\perp}\chi\|^2. \tag{1}
\]

Consequently right-continuity of this particular distance is equivalent to the vanishing of the last projection. Proving \(E_{\lambda+}=E_\lambda\) would suffice but is stronger than necessary. Neither assertion is established below.

## 2. A finite-range Möbius obstruction

This section gives an elementary obstruction to exact approximation at finite cutoff, as well as strict inclusion of the spaces. The distinction between strict inclusion and strict improvement of a specified projection is essential.

Let \(z(t)=t\mathbf1_{(0,1)}(t)\), so \(\|z\|=1\), and define

\[
 C(f)=\langle f,z\rangle=\int_0^1 f(t)\,\frac{dt}{t}.
\]

For a finite sum \(f=\sum_j c_j e_{a_j}\) with \(a_j\geq1\),

\[
 C(f)=\sum_j c_j/a_j,\qquad f(t)=C(f)t\quad(0<t<1).
\]

The latter property persists under norm limits, since restriction to \((0,1)\) is continuous and the span of \(z\) is closed.

Let \(\mu\) be the ordinary Möbius function. For \(t\geq1\) put

\[
 (Tf)(t)=\sum_{n\leq t}\mu(n)
       \left(C(f)\frac{t}{n}-f(t/n)\right). \tag{2}
\]

This definition makes sense almost everywhere for every \(f\in H\). On each finite interval \([1,R]\) it is a bounded linear map into \(L^2([1,R],dt/t^2)\). In fact, the sum has finitely many terms and

\[
 \|\mathbf1_{[n,R]}(t)f(t/n)\|_{L^2(dt/t^2)}
 \leq n^{-1/2}\|f\|_H,
\]

while \(C\) is bounded and \(t\) is square integrable on a finite interval in that measure.

### Proposition 2

For a finite sum as above,

\[
 (Tf)(t)=\sum_j c_j\mathbf1_{[a_j,\infty)}(t)
 \quad\text{almost everywhere}. \tag{3}
\]

Every \(f\in E_\lambda\) has \(Tf\) equal to a constant almost everywhere on \((\lambda,\infty)\). As a result,

1. \(E_\lambda\subsetneq E_\nu\) whenever \(1\leq\lambda<\nu\);
2. \(D(\lambda)>0\) for every finite \(\lambda\geq1\).

**Proof.** For one generator the summand in (2) is \(\mu(n)\lfloor t/(na)\rfloor\). The divisor identity

\[
 \sum_{n\geq1}\mu(n)\lfloor x/n\rfloor
 =\sum_{k\leq x}\sum_{n\mid k}\mu(n)
 =\mathbf1_{[1,\infty)}(x)
\]

proves (3); the sum is finite. For finite sums with all \(a_j\leq\lambda\), (3) is constant after \(\lambda\). On each \((\lambda,R)\) the constant functions form a closed one-dimensional subspace, so local boundedness of \(T\) passes this property to all of \(E_\lambda\). Constants agree on overlapping intervals, giving a single constant on the whole tail.

For \(\lambda<b\leq\nu\), \(Te_b=\mathbf1_{[b,\infty)}\) is not constant on \((\lambda,\infty)\). Thus \(e_b\notin E_\lambda\), whereas \(e_b\in E_\nu\). This proves strict inclusion.

Finally \(C(\chi)=0\), and (2) gives

\[
 T\chi(t)=-\sum_{n\leq t}\mu(n)\quad\text{almost everywhere}. \tag{4}
\]

This step function is not eventually constant: at every prime \(p\), its jump is \(-\mu(p)=1\), and primes are unbounded. Therefore \(\chi\notin E_\lambda\). Since \(E_\lambda\) is closed, its distance from \(\chi\) is strictly positive. ∎

### Quantitative dual certificate

Let \(q>1\), choose \(0<\varepsilon<\min(1,q-1)\), and set

\[
 \psi(t)=\varepsilon^{-1}\mathbf1_{(q,q+\varepsilon)}(t)
       -\varepsilon^{-1}\mathbf1_{(q-\varepsilon,q)}(t).
\]

For \(\lambda\leq q-\varepsilon\), the bounded functional

\[
 L(f)=\int_1^\infty \psi(t)(Tf)(t)\,dt
\]

annihilates \(E_\lambda\). Its representing vector is

\[
 h(u)=A u\mathbf1_{(0,1)}(u)
      -u^2\mathbf1_{[1,\infty)}(u)
        \sum_{n\leq q+\varepsilon}\mu(n)n\psi(nu), \tag{5}
\]
\[
 A=\sum_{n\leq q+\varepsilon}\frac{\mu(n)}{n}
        \int_n^\infty t\psi(t)\,dt. \tag{6}
\]

These expressions follow by substituting \(t=nu\) in the finite sum. In particular \(L(f)=\langle f,h\rangle\). The vector belongs to \(H\): below 1 it is linear, and above 1 it is a compactly supported piecewise quadratic function.

If \(q=p\) is prime, (4) has exactly one integer jump in the support of \(\psi\), giving \(\langle\chi,h\rangle=1\). Therefore

\[
 D(\lambda)^2\geq\frac{1}{\|h\|^2}>0
 \qquad(\lambda\leq p-\varepsilon). \tag{7}
\]

For rational \(q,\varepsilon\), the norm in (7) is exactly rational. The included program integrates the piecewise polynomial (5), with no floating-point arithmetic. For example, \(p=2,\varepsilon=1/4\) gives

\[
 \|h\|^2=\frac{32155}{768},\qquad
 D(\lambda)^2\geq\frac{768}{32155}
 \quad(1\leq\lambda\leq7/4).
\]

These weak finite-cutoff lower bounds are not proposed as improvements on known asymptotic lower bounds.

### Where this route stops

Define the closed space

\[
 N_\lambda=\{f\in H:f=C(f)t\text{ on }(0,1),\quad
 Tf\text{ is constant on }(\lambda,\infty)\}.
\]

The argument proves \(E_\lambda\subseteq N_\lambda\). It also proves

\[
 \bigcap_{\varepsilon>0}N_{\lambda+\varepsilon}=N_\lambda.
\]

Indeed, the constants agree on overlapping tails, and their union covers \((\lambda,\infty)\). Thus \(E_{\lambda+}\subseteq N_\lambda\). A proof that \(E_\lambda=N_\lambda\) would settle right-continuity, but no density proof for that equality is supplied. Local Möbius inversion alone gives no control of the global \(H\)-norm when approximating the recovered coefficients by finite step functions.

## 3. Plateau test and an exact dilation variation

Write \(p=P_{E_\lambda}\chi\), \(r=\chi-p\), and \(\lambda<\nu\). Nested orthogonal projections give

\[
 D(\lambda)^2-D(\nu)^2
   =\|P_{E_\nu\cap E_\lambda^\perp}\chi\|^2. \tag{8}
\]

Thus a plateau occurs exactly when \(r\perp E_\nu\). Equivalently,

\[
 \langle r,e_a\rangle=0\quad\text{for all }a\in(\lambda,\nu]. \tag{9}
\]

For any one new generator put \(v=(I-P_{E_\lambda})e_a\). Proposition 2 makes \(v\ne0\) for \(a>\lambda\), and

\[
 D(\lambda)^2-
 \operatorname{dist}(\chi,E_\lambda+\mathbb C e_a)^2
 =\frac{|\langle r,e_a\rangle|^2}{\|v\|^2}. \tag{10}
\]

Strict inclusion establishes the denominator is positive, not that the numerator is positive. As a simple falsification of the converse inference, in \(\mathbb R^3\) the vector \((0,0,1)\) has distance 1 both from \(\operatorname{span}(1,0,0)\) and from \(\operatorname{span}\{(1,0,0),(0,1,0)\}\).

There is also a useful exact variation, which does not settle (9). For \(a\geq1\) let

\[
 (U_a f)(t)=a^{1/2}f(t/a).
\]

This operator is unitary, and \(U_a E_\lambda\) is the closed span of parameters in \([a,a\lambda]\). Put \(q_0=P_{E_\lambda}z\), \(Q=\|p\|^2\), \(B=C(p)\), and \(Z=\|q_0\|^2\). These quantities are real because the subspace and target are preserved by complex conjugation. Since

\[
 U_a^{-1}\chi=a^{-1/2}
   (\chi+\mathbf1_{(1/a,1)}),
\]

and every vector of \(E_\lambda\) is \(C(f)t\) below 1,

\[
 P_{E_\lambda}\mathbf1_{(1/a,1)}=(\log a)q_0.
\]

Consequently, for \(s=\log a\),

\[
 \|P_{U_a E_\lambda}\chi\|^2
   =e^{-s}(Q+2Bs+Zs^2). \tag{11}
\]

Whenever \(a\lambda\leq\nu\), this is a lower bound on \(\|P_{E_\nu}\chi\|^2\). In particular, \(2B>Q\) would guarantee strict improvement for all sufficiently small positive \(s\). But there is no proof of that inequality, and it cannot be a general strategy: on \((0,1)\), \(r=-Bt\), so \(|B|\leq D(\lambda)\), while \(Q=1-D(\lambda)^2\). If \(D(\lambda)<\sqrt2-1\), the first derivative of (11) at zero is strictly negative. This variation therefore does not force the desired gain in the small-distance regime.

## 4. Fixed finite tuples versus an unbounded number of terms

A genuine related result must not be mistaken for the question above. Nicolas Jousse proves continuity of the projection for each fixed finite tuple of fractional-part dilates, including colliding parameters (Theorem 7 and the definitions preceding it), and strict improvement of the optimal error when the unrestricted number of terms increases (Corollary 1, pp. 1404–1405). [Primary paper](https://aif.centre-mersenne.org/item/10.5802/aif.2127.pdf).

For a fixed positive integer \(n\), define

\[
 d_n(\lambda)=\min_{a_1,\ldots,a_n\in[1,\lambda]}
 \operatorname{dist}(\chi,\operatorname{span}\{e_{a_1},\ldots,e_{a_n}\}).
\]

Under the isometry \(f(t)\mapsto f(1/x)\) from \(H\) to \(L^2(0,\infty;dx)\), the parameters in Jousse's notation are \(\theta_i=1/a_i\). His fixed-tuple continuity, combined with the parametrization \(a_i=1+(\lambda-1)x_i\), \(x_i\in[0,1]\), and compactness of that cube, yields continuity of each \(d_n\). The elementary minimum-continuity step follows from uniform continuity of the objective on a compact neighborhood of any fixed \(\lambda\).

However,

\[
 D(\lambda)=\inf_{n\geq1}d_n(\lambda), \tag{12}
\]

and a decreasing infimum of continuous nonincreasing functions need not be right-continuous. The explicit scalar example

\[
 b_n(x)=\max\{0,1-n\max(0,x-2)\}
\]

has infimum 1 for \(x\leq2\) and 0 for \(x>2\). It is a logical negative control, not a counterexample involving the Nyman–Beurling generators.

Two precise necessary features of any hypothetical right jump follow:

* The number of terms in near-minimizers approaching the jump from the right must be unbounded. Otherwise a subsequence with at most \(N\) terms would contradict continuity of \(d_N\).
* Their coefficient total variation must be unbounded. Indeed, replacing every \(a_j>\lambda\) by \(\lambda\) changes a finite sum by at most

\[
 \left(\sum_j|c_j|\right)
 \sup_{\lambda\leq a\leq\lambda+\varepsilon}\|e_a-e_\lambda\|.
\]

The second factor tends to zero. A uniform bound on the first for near-minimizers would rule out a jump. Bounded Hilbert norms give no such coefficient bound: the unit vectors

\[
 \frac{e_{1+h}-e_1}{\|e_{1+h}-e_1\|}\qquad(h\downarrow0)
\]

are represented by two coefficients whose total variation tends to infinity.

These are substantive restrictions on a possible discontinuity, but do not exclude it. Jousse's strict inequality for an integer term-count parameter also does not imply strict decrease when the allowed parameter interval expands.

## 5. Mellin-space reduction and boundary synthesis gap

For \(s=1/2+i\tau\), Mellin–Plancherel uses the transform

\[
 \mathcal Mf(s)=\int_0^\infty f(t)t^{-s-1}\,dt.
\]

For the generators and target, the usual integral identities in the strip \(0<\Re s<1\) are

\[
 \mathcal M\chi(s)=1/s,\qquad
 \mathcal Me_a(s)=-a^{-s}\zeta(s)/s.
\]

The integral for the generator follows, for example, by splitting into unit intervals and continuing the identity obtained from the partial sums of \(\sum n^{-s}\); the same identity is recorded in Jousse's paper, p. 1402, in reciprocal-variable notation. Thus the exact minimization is

\[
 D(\lambda)^2=
 \inf_P\frac1{2\pi}\int_{\mathbb R}
 \frac{|1+\zeta(1/2+i\tau)P(1/2+i\tau)|^2}
 {1/4+\tau^2}\,d\tau, \tag{13}
\]

where \(P(s)=\sum_jc_ja_j^{-s}\) and \(1\leq a_j\leq\lambda\).

Equivalently, it is a weighted Fourier-exponential approximation problem on the frequency interval \([0,\log\lambda]\), with weight

\[
 w(\tau)=\frac{|\zeta(1/2+i\tau)|^2}{2\pi(1/4+\tau^2)}
\]

and target \(-1/\zeta(1/2+i\tau)\), defined arbitrarily at its discrete zero set. The target belongs to \(L^2(w\,d\tau)\) because multiplication cancels the zeta factor almost everywhere.

This representation does not by itself show that intersections of decreasing weighted exponential spans have no extra boundary vectors. Nor does it provide the nonvanishing correlation in (9). Dividing a bounded weighted-norm approximating sequence by its zeta factor supplies no uniform pointwise bounds near zeros. Treating the spans as ordinary unweighted Paley–Wiener spaces would discard the essential weight. A justified weighted spectral-synthesis or density statement is still required.

### Independent finite-cutoff sanity checks

For one generator, put \(c=1-\gamma\), where \(\gamma\) is Euler's constant. Direct integration and Stirling's formula give

\[
 \langle\chi,e_a\rangle=\frac{\log a+c}{a},\qquad
 \|e_a\|^2=\frac{\log(2\pi)-\gamma}{a}\quad(a\geq1).
\]

For the first identity, summing \(\int_n^{n+1}(t-n)t^{-2}dt\) yields \(\int_1^\infty\{t\}t^{-2}dt=1-\gamma\). For the second, including the interval \((0,1)\), the partial integral to \(N+1\) equals

\[
 2N+2-H_{N+1}-2N\log(N+1)+2\log(N!),
\]

whose limit is \(\log(2\pi)-\gamma\). Scaling gives the displayed formulas.

It follows that

\[
 D(1)^2=1-\frac{(1-\gamma)^2}{\log(2\pi)-\gamma},
\]

and, with \(a=\min\{\lambda,e^{1+\gamma}\}\),

\[
 D(\lambda)^2\leq
 1-\frac{(\log a+1-\gamma)^2}{a(\log(2\pi)-\gamma)}.
\]

Indeed \((s+c)^2e^{-s}\) is strictly increasing for \(0\leq s<2-c=1+\gamma\). Therefore \(D(\lambda)<D(1)\) for every \(\lambda>1\). This establishes strict improvement from the endpoint extension only, not between arbitrary \(1<\lambda<\nu\).

## Conclusion

The proved statements are left-continuity, exact formulas for the right-jump and plateau obstructions, positivity at every finite cutoff, strict increase of the approximation spaces, explicit rational dual certificates, and strict improvement from the endpoint \(\lambda=1\). The two requested global properties still require, respectively, control of the right-limit defect and a nonzero residual correlation with a new generator on every nonempty parameter interval. Neither follows from the finite-dimensional literature result or the controls provided here.
