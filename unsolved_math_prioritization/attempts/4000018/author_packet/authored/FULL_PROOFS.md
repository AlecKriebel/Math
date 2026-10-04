# Full proofs of scoped statements

## 0. Definitions and quantifiers

For a metric space \((X,d)\), let \(P_t(x,\cdot)\) be a Markov transition semigroup with finite first moments. Write \(P_t^*\delta_x\) for this law. All Wasserstein distances below use the stated metric. Define \(O(\kappa,C;T)\) to mean

\[
W_1(P_s^*\delta_x,P_t^*\delta_y)
\le e^{-\kappa\min(s,t)}r+\frac{C(\sqrt t-\sqrt s)^2}{2r},
\qquad r=d(x,y)>0,
\tag{O}
\]

for **every** pair of distinct points and **every** \(s,t\in[0,T]\). This is stronger in spatial scope than the annular assumption in Ollivier's Proposition 52. At zero time use \(P_0^*\delta_x=\delta_x\); with first-moment continuity it follows from a positive-time formulation by taking limits. We never evaluate the displayed quotient at \(x=y\).

For an operator \(L\) on an algebra, put

\[
\Gamma(f,g)=\tfrac12[L(fg)-fLg-gLf],\quad
\Gamma(f)=\Gamma(f,f),\quad
\Gamma_2(f)=\tfrac12L\Gamma(f)-\Gamma(f,Lf).
\]

\(BE(K,N)\) denotes \(\Gamma_2(f)\ge K\Gamma(f)+(Lf)^2/N\), on its specified domain. For \(N=\infty\) the last term is zero. In this packet “BE” is used to avoid confusing this generator condition, often also called CD, with synthetic Lott–Sturm–Villani CD. We use positive finite \(N\) or \(N=\infty\); negative-dimension extensions are outside scope.

## 1. A dimension-independent unequal-time bound for a reset process

**Theorem 1.** Let \(X\) have diameter at most \(D\in(0,\infty)\), and let \(\nu\) be a Borel probability measure. The kernels

\[
P_t^*\delta_x=a_t\delta_x+(1-a_t)\nu,\qquad a_t=e^{-2t},
\tag{1}
\]

satisfy \(O(1,16D^2;1/4)\).

**Proof.** The kernels are Markov, and \(P_sP_t=P_{s+t}\) follows by multiplying \(a_sa_t=a_{s+t}\). All moments needed here are finite because the space is bounded. By symmetry assume \(0\le s\le t\le1/4\). Couple mass \(a_t\) at \(x\) to \(y\), couple the common mass \(1-a_s\) of \(\nu\) identically, and couple the remaining mass \(a_s-a_t\) at \(x\) to \(\nu\). Thus

\[
W_1(P_s^*\delta_x,P_t^*\delta_y)
\le a_t r+(a_s-a_t)D.
\tag{2}
\]

If \(s=t\), this is \(e^{-2s}r\le e^{-s}r\), proving (O). Otherwise put

\[
q=\sqrt t-\sqrt s>0,\quad
A=e^{-s}-e^{-2t}>0,\quad B=e^{-2s}-e^{-2t}\ge0.
\]

Because \(e^u-1\ge u\) and \(e^{-2t}\ge1-2t\ge1/2\),

\[
A=e^{-2t}(e^{2t-s}-1)\ge(2t-s)/2.
\tag{3}
\]

Also \(B=\int_s^t2e^{-2u}\,du\le2(t-s)=2q(\sqrt t+\sqrt s)\). Since

\[
(\sqrt t+\sqrt s)^2\le2(t+s)\le4(2t-s),
\tag{4}
\]

we get \(BD\le4Dq\sqrt{2t-s}\). The arithmetic-geometric mean inequality and (3) give, for every \(r>0\),

\[
Ar+\frac{8D^2q^2}{r}
\ge2\sqrt{8AD^2q^2}
\ge4Dq\sqrt{2t-s}\ge BD.
\tag{5}
\]

Combining (2) and (5) proves
\(W_1\le e^{-s}r+8D^2q^2/r\), as claimed. Endpoints with \(s=0\) are included directly. \(\square\)

The invariant law is \(\nu\). Reversibility follows from

\[
\int fP_tg\,d\nu
=a_t\int fg\,d\nu+(1-a_t)\left(\int f\,d\nu\right)\left(\int g\,d\nu\right).
\]

On a compact metric space the semigroup is Feller and uniformly continuous on \(C(X)\). It is usually not strong Feller: \(P_tf\) retains the discontinuities of a bounded measurable \(f\) through the nonzero term \(a_tf\). Its jumps are genuine resets, so it is not a diffusion or a strongly local Dirichlet-form heat flow.

At equal times one actually has

\[
W_1(P_t^*\delta_x,P_t^*\delta_y)=e^{-2t}d(x,y).
\]

The upper bound uses the common-mass coupling. For the lower bound, the 1-Lipschitz function \(z\mapsto d(z,y)\) cancels the common \(\nu\)-part and gives exactly \(e^{-2t}d(x,y)\). Therefore \(\kappa=1\) in Theorem 1 is an admissible lower bound, not its optimal same-time curvature (which is 2).

## 2. Exact Bakry–Émery profile of the reset generator

**Theorem 2.** Suppose \(\nu\) is atomless, and take the bounded generator
\(Lf=2(\int f\,d\nu-f)\) on bounded measurable functions. For \(N\in(0,\infty)\), its optimal pointwise/a.e. BE curvature is

\[
K_N=1-4/N.
\tag{6}
\]

For \(N=\infty\), the optimal curvature is \(K_\infty=1\). In particular, the example in Theorem 1 with \(D=1\) has finite \(C=16\) and \(BE(1,\infty)\), but fails \(BE(1,N)\) for every finite \(N\).

**Proof.** Let \(m=\int f\,d\nu\), \(g=f-m\) and \(V=\int g^2\,d\nu\). Direct use of the definitions gives

\[
Lf=-2g,\quad \Gamma(f)=V+g^2,\quad
\int\Gamma(f)\,d\nu=2V,
\]

\[
L\Gamma(f)=2(V-g^2),\quad
\Gamma(f,Lf)=-2\Gamma(f),\quad
\Gamma_2(f)=3V+g^2.
\tag{7}
\]

Consequently

\[
\Gamma_2(f)-K\Gamma(f)-\frac{(Lf)^2}{N}
=(3-K)V+(1-K-4/N)g^2.
\tag{8}
\]

If \(K\le1-4/N\), both coefficients are nonnegative, proving sufficiency. Conversely, choose a measurable set \(E\) of mass \(p\in(0,1)\) and \(f=1_E\). On \(E\), which has positive measure,
\(g=1-p\), \(V=p(1-p)\). Dividing (8) by \((1-p)^2\) gives

\[
(3-K)\frac p{1-p}+1-K-4/N.
\tag{9}
\]

As \(p\downarrow0\), this tends to \(1-K-4/N\). Atomlessness permits arbitrarily small such sets, so any larger \(K\) fails. The same argument with \(4/N=0\) proves the infinite-dimensional assertion. \(\square\)

The failure is not an artifact of a pointwise-null set or the use of discontinuous tests. On \([0,1]\) with Lebesgue measure, take the continuous Lipschitz tent
\(f_\varepsilon(x)=\max(1-x/\varepsilon,0)\). Its mean is \(\varepsilon/2\), its variance is \(\varepsilon/3-\varepsilon^2/4\), and \(g(0)=1-\varepsilon/2\). At \(K=1\), finite BE would require

\[
N\ge \frac{2(1-\varepsilon/2)^2}{\varepsilon/3-\varepsilon^2/4},
\]

which tends to infinity. The strict failure persists on a neighborhood of zero of positive measure. These functions belong to the generator's full \(C([0,1])\) domain.

Important limitation: at any \(K<1\), a finite BE dimension does exist, namely \(N\ge4/(1-K)\). The example disproves finite-dimensional inference at the **same specified curvature** \(K=\kappa=1\); it does not disprove every possible weakened-curvature relationship.

## 3. Geometric dimension is unbounded at fixed transport data

**Corollary 3.** No finite function of the three numerical data \((\kappa,C,T)=(1,16,1/4)\) can bound Hausdorff dimension across the class of compact geodesic metric probability spaces with reversible Feller Markov semigroups satisfying (O).

**Proof.** For every integer \(n\ge1\), let
\(X_n=[0,1]^n\), \(d_n(x,y)=\|x-y\|_2/\sqrt n\), and let \(\nu_n\) be normalized Lebesgue measure. This is compact, geodesic, has full support and diameter one, and has Hausdorff dimension \(n\). Apply Theorem 1. The constants do not vary with \(n\). \(\square\)

There is also one infinite-dimensional compact example. Take

\[
X=\prod_{j=1}^{\infty}[0,2^{-j}]\subset\ell^2,
\qquad d(x,y)=\sqrt3\,\|x-y\|_2.
\]

The uniform tail bound \(\sum_{j>m}4^{-j}\to0\) and finite-dimensional compactness imply compactness in \(\ell^2\). The set is convex, so straight segments are geodesics. Its diameter is one because \(3\sum_{j\ge1}4^{-j}=1\). The product of uniform measures on the factors is a full-support atomless Borel probability measure: to obtain a neighborhood of positive probability, control finitely many coordinates and then use the uniform tail bound. The coordinate subcube obtained by fixing all coordinates after \(n\) at zero is bi-Lipschitz to an \(n\)-dimensional box. Monotonicity of Hausdorff dimension therefore gives \(\dim_H X\ge n\) for every \(n\). Apply Theorems 1 and 2.

These conclusions concern an arbitrary chosen Markov semigroup. They do not identify the reset process with the canonical heat flow of any of these metric-measure spaces.

## 4. Positive transfer from finite-dimensional heat-flow estimates

**Proposition 4.** Suppose a Markov heat flow on \((X,d)\) satisfies, for some \(K>0\) and finite \(N>0\),

\[
W_2(P_s^*\delta_x,P_t^*\delta_y)^2
\le e^{-K\tau(s,t)}r^2+
2N\frac{1-e^{-K\tau(s,t)}}{K\tau(s,t)}(\sqrt t-\sqrt s)^2,
\quad
\tau(s,t)=\frac23(t+\sqrt{st}+s).
\tag{10}
\]

Assume continuity at zero in \(W_2\) when zero times are included. Then for every \(T>0\), \(O(K,2Ne^{KT};T)\) holds.

**Proof.** Order the times so \(s\le t\). Then \(\tau(s,t)\ge2s\), while \((1-e^{-u})/u\le1\) for \(u\ge0\). Thus

\[
W_1\le W_2\le\sqrt{e^{-2Ks}r^2+2Nq^2}
\le e^{-Ks}r+\frac{Ne^{Ks}q^2}{r}
\le e^{-Ks}r+\frac{Ne^{KT}q^2}{r}.
\]

Here \(q=\sqrt t-\sqrt s\) and the middle inequality is \(\sqrt{a^2+b}\le a+b/(2a)\), valid for \(a>0,b\ge0\). This is (O) with the stated constants. \(\square\)

Erbar–Kuwada–Sturm, arXiv:1303.4382v2, Theorem 3 and Proposition 2.22, give (10) for the canonical heat flow on their \(RCD^*(K,N)\) spaces. The metric-measure, Cheeger-energy and finite-dimension assumptions are recorded separately in SOURCE_AND_ASSUMPTIONS.md. This is a use of their theorem, not a new proof of that theorem.

An alternative transfer follows directly from Kuwada's (1.4). Let
\(w(r)=\sqrt{NK/(e^{2Kr}-1)}\), \(J=\int_s^t w(r)\,dr\),
\(\alpha=J/(\int_s^t e^{Kr}w(r)\,dr)\). His estimate is
\(W_2^2\le\alpha^2r^2+J^2\). One has \(\alpha\le e^{-Ks}\) and \(J\le\sqrt{2N}(\sqrt t-\sqrt s)\), giving precisely the same upper bound and proof. On a complete smooth \(m\)-dimensional Riemannian manifold, this applies to \(L=\Delta+Z\) under his finite \(N\ge m\) tensor inequality; for \(N=m\), the convention requires \(Z=0\).

For any \(C>2N\), choosing \(T\le K^{-1}\log(C/(2N))\) yields (O). Therefore the infimum of admissible small-time coefficients, when the horizon may depend on the coefficient, is at most \(2N\). This argument does **not** prove attainability at \(C=2N\) on a positive horizon. For generator \(\tfrac12\Delta\), the time-rescaling in the next proposition gives \(\kappa=K/2\) and \(C=Ne^{KT/2}\), with small-time infimum at most \(N\).

When \(K=0\), the same argument gives \(C=2N\) without a horizon factor. No positive-curvature diameter conclusion follows from \(K=0\).

## 5. Normalization prevents a raw identification

**Proposition 5.** If \(P_t\) satisfies \(O(\kappa,C;T)\), then:

1. \(Q_t=P_{at}\), \(a>0\), satisfies \(O(a\kappa,aC;T/a)\).
2. With unchanged kernels and metric \(d'=b d\), \(b>0\), the condition is \(O(\kappa,b^2C;T)\).
3. Every \(C'\ge C\) is also admissible.

**Proof.** Substitute \(as,at\) into (O), using \((\sqrt{at}-\sqrt{as})^2=a(\sqrt t-\sqrt s)^2\). For the second assertion, \(W_1^{d'}=bW_1^d\) and \(d'=bd\). Multiplying (O) by \(b\) yields the coefficient \(b^2C\). The third follows by monotonicity of the nonnegative added term. \(\square\)

In contrast, replacing \(L\) by \(aL\) changes \(\Gamma\) to \(a\Gamma\), \(\Gamma_2\) to \(a^2\Gamma_2\), and carries \(BE(K,N)\) to \(BE(aK,N)\): the dimension parameter is unchanged. For a fixed operator, \(BE(K,N)\) also implies \(BE(K,N')\) for \(N'\ge N>0\).

Thus a raw admissible \(C\) cannot equal an intrinsic dimension without both normalization and an extremal convention. These elementary facts do not preclude useful relations once a canonical metric, generator, curvature bound and notion of optimal coefficient have been fixed.

## 6. Euclidean Brownian calibration

**Proposition 6.** For standard Brownian motion \(P_t^*\delta_x=\mathcal N(x,tI_n)\) on \(\mathbb R^n\), the infimal coefficient for (O) with \(\kappa=0\), on any positive horizon, obeys
\(n-1\le C_*\le n\). When \(n=1\), \(C_*>0\).

**Proof of the upper bound.** With \(Z\sim\mathcal N(0,I_n)\), couple \(x+\sqrt s Z\) to \(y+\sqrt t Z\). This gives

\[
W_2^2\le\mathbb E|x-y+(\sqrt s-\sqrt t)Z|^2=r^2+nq^2.
\]

In fact equality holds: in any coupling \(U,V\) of the two Gaussian variables, subtract the means and use Cauchy–Schwarz to bound their covariance trace by \(n\sqrt{st}\). Therefore \(W_2^2=r^2+nq^2\), and \(W_1\le W_2\le r+nq^2/(2r)\).

**Proof of the lower bound.** Set \(s=0\), \(x=0\), \(y=re_1\), \(r>0\). There is only one coupling with a Dirac law, so
\(W_1(\delta_0,P_t^*\delta_y)=\mathbb E|re_1+\sqrt tZ|\). The Hessian of \(|z|\) at \(re_1\) has trace \((n-1)/r\). Taylor expansion gives

\[
\mathbb E|re_1+\sqrt tZ|=r+\frac{n-1}{2r}t+o(t).
\tag{11}
\]

For completeness, choose a smooth cutoff agreeing with \(|z|\) on the ball of radius \(r/2\) around \(re_1\). Its Taylor remainder has expectation \(o(t)\) there; the complementary Gaussian tail, multiplied by the at-most-linear growth of the original norm, is also \(o(t)\). This justifies (11) despite the norm's singularity at the origin. Substituting (11) into (O) and dividing by \(t/(2r)\) gives \(C\ge n-1\).

For \(n=1\), take \(r=\sqrt t>0\). Then the same inequality forces

\[
C\ge2(\mathbb E|1+Z|-1)>0.
\tag{12}
\]

The strict inequality follows because \(1+Z\) has a strictly positive probability of being negative, and \(\mathbb E|1+Z|=1+2\mathbb E[-(1+Z)1_{Z<-1}]\). Scaling \(r=\sqrt t\) permits this test on every positive time horizon. \(\square\)

This is a calibration under \(L=\tfrac12\Delta\). It does not identify the exact optimum for general \(n\), and it does not make \(n-1\) a universally valid coefficient. In particular \(C=n-1=0\) is already false on the line. For \(L=\Delta\), the coefficients double by Proposition 5.

## 7. Infinite-dimensional BE bounds do not control unequal times

**Proposition 7.** On \(\mathbb R^n\), \(n\ge1\), let \(L=\Delta-\lambda x\cdot\nabla\) with \(\lambda>0\). Then the Ornstein–Uhlenbeck semigroup has equal-time Wasserstein contraction
\(W_1(P_t^*\delta_x,P_t^*\delta_y)=e^{-\lambda t}|x-y|\), and satisfies \(BE(\lambda,\infty)\). Nevertheless, it satisfies no \(O(\kappa,C;T)\) with finite \(C\), any real \(\kappa\), and any \(T>0\).

**Proof.** The transition law is Gaussian with mean \(e^{-\lambda t}x\) and covariance \(\lambda^{-1}(1-e^{-2\lambda t})I_n\). At equal times, translation coupling gives the upper bound, and projection onto the direction \(x-y\) gives the matching lower bound. Direct differentiation in the Gamma definitions gives
\(\Gamma(f)=|\nabla f|^2\) and
\(\Gamma_2(f)=\|\operatorname{Hess}f\|_{HS}^2+\lambda|\nabla f|^2\), proving the BE assertion.

Fix any \(0<s<t\le T\), fix \(r>0\), and set \(x=Re_1\), \(y=(R+r)e_1\). The difference of their transition means has absolute value

\[
|(e^{-\lambda s}-e^{-\lambda t})R-e^{-\lambda t}r|\longrightarrow\infty
\quad\text{as }R\to\infty.
\]

It is a lower bound for \(W_1\), by the 1-Lipschitz coordinate function. The right-hand side of (O) is independent of \(R\) and finite. This contradiction proves the claim. \(\square\)

At the same curvature \(\lambda\), no finite \(N\) is possible in BE: the test \(f(x)=x_1\) has \(\Gamma_2-\lambda\Gamma=0\) and \((Lf)^2=\lambda^2x_1^2\). If a compactly supported domain is desired, use a smooth function equal to \(x_1\) in a neighborhood of any point with \(x_1\ne0\); the local Gamma calculation is unchanged. Therefore the positive infinite-dimensional condition cannot be substituted for the finite-dimensional hypotheses of Proposition 4.

## 8. What these proofs do and do not settle

Theorem 1 and Corollary 3 refute a universal geometric-dimension upper bound from the numerical W1 data alone in the broad metric-plus-Markov-kernel framework. Theorem 2 refutes a universal same-curvature finite-BE-dimension inference. Proposition 4 supplies a rigorously quantified finite-dimensional sufficient condition in the canonical heat-flow framework.

The original Problem R asks for a relationship, without specifying a class, normalization, extremal choice of constants, or direction of implication. The results above delimit several precise interpretations. They do not establish an exact equivalence for canonical strongly local diffusions or RCD heat flows, an optimal \(C\)-versus-\(N\) formula there, or a complete classification. Those gaps are why the target is retained as unresolved in this packet.
