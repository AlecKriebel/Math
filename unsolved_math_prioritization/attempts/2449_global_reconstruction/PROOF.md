# EP1038 / database 2449: reconstruction of the finite-polynomial extrema

Public edition dated 2026-10-12. This retains the complete substantive mathematical report, with transparent editorial changes to private references and review-status wording. Independently authored executable checkers, raw interval certificates, full numerical records, detailed diagnostic outputs, and source copies are not included. Hashes identify omitted evidence but do not provide executable public reproducibility. The work is AI-assisted and unrefereed, with no external human peer review or formal proof-assistant certification. In Section 10.2, the original description of all three positive series as entire is corrected: C_0 and S_0 are entire, whereas T_0 is analytic for |w|<1. The certified domain 0<=w<0.03, all formulas, computations and conclusions are unchanged.

**Draft date:** 2026-10-12 (UTC). **Status:** authored local proof draft with completed end-to-end numerical and analytic review, including a separate adversarial analytic challenge. The combined evidence is accepted for the finite-polynomial scope stated below. This is not an external peer-review or problem-site acceptance, and this drafting task has not published the document. The earlier fixed-candidate packet remains unchanged.

## 0. Scope, attribution, and exact accepted theorem

Let \(\mathcal P\) consist of the nonconstant monic real polynomials with every root, counted with multiplicity, in \([-1,1]\). The original question is to determine the extreme possible lengths of
\[
 E_f=\{x\in\mathbb R:|f(x)|<1\},\qquad f\in\mathcal P.
\]
This is Problem 1 on printed page 131 of Erdős–Herzog–Piranian, *Metric properties of polynomials* [EHP]. We reconstruct the lower argument in Wang's proposed manuscript [W], using the one-cut family credited there to Tao [T]. The reconstruction and independent arithmetic checks make no novelty claim. The public result page was rechecked on 2026-10-12 and still describes the manuscript as **Proposed**. The scoped acceptance reported here does not establish a change in that public status or community consensus.

Define
\[
 H(q)=\frac{2q}{(1+q)^2},\quad s(q)=\frac{1-q}{1+q},\quad
 A(q)=\frac{\log H(q)}{\log q}.
\]
There is a unique \(q_s\in(0,3-2\sqrt2)\) satisfying \(A(q_s)=s(q_s)\). For \(0<q<q_s\), define \(u_+(q)\in(1,1/q)\) to be the nontrivial root and \(u_-(q)\in(1/q,\infty)\) the root of
\[
 F(q,u)=A(q)\log\frac{u-q}{|1-qu|}-\log u=0.
\]
At \(q_s\), set \(u_+(q_s)=1\) by continuation. Set
\[
 \Lambda(q)=H(q)\bigl(u_-+u_-^{-1}-u_+-u_+^{-1}\bigr).
\]
The two explicit numerical obligations developed below have passed complete independently authored checks and a separate full numerical recomputation. Together with the analytic reductions reviewed independently, they imply:

1. \(\Lambda\) has a unique minimizer \(q_*\) on \((0,q_s]\).
2. With the exact real number \(L=\Lambda(q_*)\),
   \[
   \inf_{f\in\mathcal P}|E_f|=L,\qquad |E_f|>L\quad(f\in\mathcal P).
   \]
   Hence the infimum is not attained.
3. The certified enclosures are
   \[
   0.025715536866527<q_*<0.025715536866528,
   \quad 1.834430475762661<L<1.834430475762662.
   \]
4. With Tao's Theorem 2.1 as an explicitly external mathematical input,
   \[
   \sup_{f\in\mathcal P}|E_f|=2\sqrt2,
   \]
   with equality exactly for \(f=(x^2-1)^m\), \(m\ge1\).

The uniqueness in item 1 is **only uniqueness of the parameter in this one-cut family**. We do not prove uniqueness of minimizing general measures, classify all relaxed minimizers, or claim a lower theorem for arbitrary non-empirical probabilities. We will not need the existence of a relaxed minimizer at all.

This is an independently worded proof exposition and a complete map of its analytic and numerical dependencies. The finite slab records and independently authored programs remain local. Their integrity metadata are not substitutes for the mathematical inequalities, and this document is **not a self-contained executable reproduction package**. It does specify the formulas, algorithms, domains, remainder bounds, coverage requirements, and actual available evidence. The evidence and remaining publication/reproducibility boundaries are described in Section 16.

## 1. Exact passage to finitely supported potentials

For \(f(x)=\prod_{j=1}^n(x-r_j)\), put
\[
 \mu=\frac1n\sum_{j=1}^n\delta_{r_j},\qquad
 V_\mu(x)=\int\log|x-t|\,d\mu(t).
\]
Then \(V_\mu=n^{-1}\log|f|\), including value \(-\infty\) at the roots, so \(E_f=\{V_\mu<0\}\). Since \(|x-t|\ge1\) for \(|x|\ge2\) and \(t\in[-1,1]\), every negative set under consideration lies in \((-2,2)\). For an empirical measure its boundary is finite: every boundary point is a zero of the nonzero polynomial \(f^2-1\). Thus strict versus non-strict inequalities do not change its length. This observation is deliberately not applied to a continuous measure having a zero-potential interval.

### 1.1 Simultaneous component collapse

Every component \((a,b)\) of \(\{V_\mu<0\}\) contains a root. Otherwise \(V_\mu\) is strictly concave there, is continuous with value zero at both endpoints, and is nonnegative between them, a contradiction.

In each component replace all its root mass by a single atom at its mass-weighted mean. The mass remains rational and the new location remains in the original component and in \([-1,1]\). Call the resulting empirical probability \(\widetilde\mu\). For \(x\notin E_\mu\), the function \(t\mapsto\log|x-t|\) is concave on each old component. Jensen's inequality therefore raises every component's contribution under this replacement. All root mass was in those components, so
\[
 V_{\widetilde\mu}(x)\ge V_\mu(x)\ge0,
 \qquad E_{\widetilde\mu}\subset E_\mu.                 \tag{1.1}
\]
Inside any old component there is now one pole. On either side of that pole, strict concavity and the nonnegative old endpoint imply that the negative portion is the interval adjoining the pole. Hence there is exactly one new component in each old component, containing exactly one distinct root cluster. Old nonnegative separating points remain nonnegative, including a single zero shared by the closures of two old components.

It suffices to bound this atomized finite measure from below. In what follows we replace \(\mu\) by \(\widetilde\mu\); inequality (1.1) will transfer the conclusion back to the original polynomial.

### 1.2 An endpoint atom with at least half the mass

Reflect so that the mean \(m=\int t\,d\mu(t)\) is nonpositive. For \(-1<x<0\),
\[
 |x-t|\le1-xt\quad(-1\le t\le1),
\]
because the difference of their squares is \((1-x^2)(1-t^2)\). Consequently
\[
 V_\mu(x)\le\int\log(1-xt)\,d\mu(t)
 \le\log(1-xm)\le0.
\]
Equality throughout would force a point mass by strict concavity, then force its location to be zero by the last equality. At that point mass the first inequality is strict. Thus \((-1,0)\subset E_\mu\).

Let \(c\) be the one cluster in this component. It is the leftmost cluster: another root to its left, necessarily in \([-1,0]\), would be in the same component. Thus \(c\le m\le0\). Translate the measure and variable by \(-c-1\). Its support becomes a subset of \([-1,-c]\subset[-1,1]\), its mean remains nonpositive, and its main atom is at \(-1\).

To check the boundary geometry, let \(r_0\ge0\) be the old right endpoint of the main component. If \(r_0-c<1\), its distance from the main atom is less than one and its distances from every residual root to its right are at most one. Their weighted geometric mean cannot be one, contrary to \(V_\mu(r_0)=0\). Therefore the translated boundary \(\beta=r_0-c-1\) is nonnegative. Residual roots lie in \([\beta,1]\).

Let \(A\) be the mass at \(-1\). At \(\beta\), weighted arithmetic–geometric mean gives
\[
 1\le A(1+\beta)+(1-A)(1-\beta)=1+(2A-1)\beta.
\]
If \(\beta>0\), then \(A\ge1/2\). If \(\beta=0\), equality forces every residual root to be 1; the nonpositive mean gives the same conclusion. The case \(A=1\) has length 2 and is already strictly above the claimed \(L\).

Otherwise put \(k=A/(1-A)\ge1\). Translate by one and divide the potential by \(1-A\). Neither operation changes length or sign, and the resulting problem is
\[
 W(x)=k\log|x|+\sum_{i=1}^N p_i\log|x-d_i|,
 \quad1\le d_1<\cdots<d_N\le2,\quad p_i>0,\quad\sum_i p_i=1.       \tag{1.2}
\]
The \(p_i\) are rational. The component containing zero and all residual components are distinct; single-point contact is allowed. This last property is essential later.

## 2. A lower bound on every residual component

Let \(M_k\) be the main width and define positive numbers
\[
 R_i=\exp\left[-\frac{k\log d_i+\sum_{j\ne i}p_j\log|d_i-d_j|}{p_i}\right].  \tag{2.1}
\]
For \(0<x<1\),
\[
 W(x)\le k\log x+\log(2-x)\le\log(x(2-x))<0.
\]
Every residual component is therefore to the right of 1. On its component around \(d_i\), remove the self-pole. The remaining background is strictly concave. If the left and right endpoint distances are \(s,u>0\), concavity at \(d_i\) and the two zero endpoint equations give
\[
 R_i\le s^{u/(s+u)}u^{s/(s+u)}\le\frac{s+u}{2}.
\]
The first inequality follows after division by \(-p_i\), which reverses the inequality. The second follows by differentiating
\((1-w)\log w+w\log(1-w)\): its maximum is \(-\log2\) at \(w=1/2\). Summing disjoint component lengths yields
\[
 |E_\mu|\ge J_k:=M_k+2\sum_iR_i.                     \tag{2.2}
\]

Let \(b_k\in(0,1)\) solve \(b_k^k(2+b_k)=1\). Monotonicity gives one such solution. The estimates just used and
\(W(-r)\le k\log r+\log(2+r)\) show that \((-b_k,1)\) is in the main component. Also \(b_k\ge b_1=\sqrt2-1\). Thus
\[
 M_k\ge\sqrt2.                                      \tag{2.3}
\]

## 3. The elementary range \(1\le k\le29/20\)

Set \(K=29/20\), \(y_i=2-d_i\), and \(\bar y=\sum p_i y_i\). Distinctness of the first two components provides \(b\in(0,d_1)\) with \(W(b)\ge0\), also in the contact case. Jensen gives
\[
 0\le k\log b+\log(2-\bar y-b).
\]
In particular \(b\ge1\), since \(b^k(2-b)<1\) for \(0<b<1\). Maximizing \(2-b-b^{-K}\) gives
\[
 \bar y\le\varepsilon:=2-(K+1)K^{-K/(K+1)}<1/25.        \tag{3.1}
\]
Here the last strict inequality requires no numerical oracle. The inequalities
\(e^{3/8}>1+3/8+(3/8)^2/2+(3/8)^3/6>K\), and, with \(z=87/392\),
\[
 \frac{49}{20}(1-z+z^2/2-z^3/6)-\frac{49}{25}
 =\frac{522631}{245862400}>0
\]
prove it by the lower Taylor bound for \(e^{-z}\).

Write \(Q=\sum_i p_i^2\), \(t=1-Q\), and \(S=\sum_iR_i\). Since
\(|d_i-d_j|\le y_i+y_j\), logarithmic concavity gives
\[
 2\sum_{i<j}p_ip_j\log|d_i-d_j|\le t\log(2\varepsilon/t).
\]
When \(t=0\), both sides use the value zero by continuity. Combining this with (2.1), \(d_i\le2\), and weighted arithmetic–geometric mean with weights \(p_i^2/Q\), gives
\[
 Q\log(3S)\ge\log3-k\log2-t\log(6\varepsilon/t).
\]
For \(t>0\), \(t\log(c/t)\le c/e\). Since \(\varepsilon<1/25\) and \(e>8/3\), the last term is less than \(9/100\). Positive atanh-series estimates give
\[
 \log3>263/240,\qquad \log2<1123/1620,
\]
and
\[
 \frac{263}{240}-\frac{29}{20}\frac{1123}{1620}-\frac9{100}
 =\frac{11}{16200}>0.
\]
Thus \(S>1/3\), and (2.2)–(2.3) imply
\[
 J_k>\sqrt2+2/3>2.                                  \tag{3.2}
\]
This argument already belonged to the accepted fixed-candidate audit and is repeated to close the small-\(k\) part of the global proof.

## 4. Reference probabilities with constant conductor potential

For \(1\le a<2\), put
\[
 c=(a+2)/2,\quad r=(2-a)/2,\quad H=r/2,
 \quad de(d)=\frac{dd}{\pi\sqrt{(d-a)(2-d)}}.
\]
The measure \(e\) is a probability on \([a,2]\). The measure
\(d\omega(d)=\sqrt{2a}\,de(d)/d\) also has mass one. Define
\[
 d\eta(d)=\left(k+1-\frac{k\sqrt{2a}}d\right)de(d)
 =\mathcal A(d)\,de(d).                              \tag{4.1}
\]
Its mass is one and it is nonnegative exactly when
\[
 a\ge2\left(\frac{k}{k+1}\right)^2.                   \tag{4.2}
\]
All reference choices used by the numerical gate satisfy strict positivity.

The substitution \(d=c-r\cos\theta\), \(0\le\theta\le\pi\), makes \(de=d\theta/\pi\). The Poisson expansion, or the elementary arcsine Cauchy transform, gives on the conductor
\[
 \int\log|d-e|\,de(e)=\log H,
\]
\[
 \int\log|d-e|\,d\omega(e)
 =\log d+\log H-\log D_0,
 \quad D_0=(a+2+2\sqrt{2a})/4.
\]
Thus the weighted reference potential
\[
 W_0(x)=k\log|x|+\int\log|x-d|\,d\eta(d)
\]
is equal to the constant
\[
 C=\log H+k\log D_0                              \tag{4.3}
\]
on \([a,2]\). These are explicit identities, not an invocation of an unproved minimization property of equilibrium measures.

We require simple main crossings
\[
 x_-<0<x_+<a,\qquad W_0'(x_-)<0<W_0'(x_+).              \tag{4.4}
\]
Their width is \(M_0=x_+-x_-\). Section 12 gives explicit formulas and shows how the numerical gate proves (4.2) and (4.4) uniformly. Positivity of the reference ensures that its negative-side crossing is unique and that a positive-slope zero is the first positive zero: \(W_0'<0\) on the negative axis and \(W_0''<0\) on \((0,a)\). In particular (4.4) gives a positive point immediately after \(x_+\), so the main component is strictly separated from the conductor.

## 5. Convex support for the exact main width, including contact

For a residual quantile \(T:[0,1]\to[1,2]\), let
\[
 \Psi_T(y)=y\exp\left(\frac1k\int_0^1\log(1-y/T(u))\,du\right),
 \quad R(T)=\exp\left(-\frac1k\int_0^1\log T(u)\,du\right).
\]
For \(y<\mathop{\rm ess\,inf}T\),
\[
 W_T(y)/k=\log(|\Psi_T(y)|/R(T)).                       \tag{5.1}
\]
For the atomic target,
\[
 \frac{\Psi_T'(y)}{\Psi_T(y)}=\frac1y-\frac1k\sum_i\frac{p_i}{d_i-y}.
\]
On \((0,d_1)\) the right side decreases strictly from \(+\infty\) to \(-\infty\). Hence there is one maximum at \(y_c\). Component separation from Section 1 gives
\(R(T)\le\Psi_T(y_c)\). Strict inequality describes an actual nonnegative gap; equality describes a common zero contact point. On the negative axis \(\Psi_T\) increases from \(-\infty\) to zero.

Let \(\Phi_T\) denote the inverse branch at zero. The main endpoints are
\(\Phi_T(-R(T))\) and \(\Phi_T(R(T))\), taking the increasing real limit at contact. Lagrange inversion gives
\[
 \Phi_T(z)=\sum_{n\ge1}a_n(T)z^n,\quad
 a_n=\frac1n[y^{n-1}]\prod_i(1-y/d_i)^{-np_i/k}.
\]
All coefficients are nonnegative. More explicitly,
\[
 a_nR^n=\frac1n\sum_{j_1+\cdots+j_N=n-1}
 \prod_i\frac{(np_i/k)_{j_i}}{j_i!}\,d_i^{-(np_i/k+j_i)}.             \tag{5.2}
\]
Here \((z)_j\) is the rising factorial. A positive monomial \(m=\prod_i d_i^{-\gamma_i}\) with \(\gamma_i>0\) has
\[
 \frac{v^T(\nabla^2m)v}{m}
 =\left(\sum_i\frac{\gamma_i v_i}{d_i}\right)^2
  +\sum_i\frac{\gamma_i v_i^2}{d_i^2}\ge0.
\]
Every finite odd truncation of \(2\sum_{m\ge0}a_{2m+1}R^{2m+1}\) is therefore convex in the root coordinates.

Let \(T_0\) be the continuous reference quantile and \(v=T-T_0\). Since the target weights are rational, take increasingly fine common equal-mass partitions refining its blocks; approximate \(T_0\) on the same cells. For fixed \(n\), \(a_n\) is a polynomial in the finitely many inverse moments \(\int T^{-j}\), \(1\le j<n\), because its coefficient-generating function is
\[
 \exp\left(\frac nk\sum_{j\ge1}\frac{y^j}{j}\int T^{-j}\right).
\]
These moments, \(R(T)\), and their first variations converge under common-partition approximation. For example,
\[
 D\!\int T^{-j}[v]=-j\int vT^{-j-1},\qquad
 DR(T)[v]=-\frac{R(T)}k\int v/T.
\]
The bounds \(T\ge1\) and \(|v|\le1\) justify dominated convergence. Passing each finite-dimensional support inequality to this limit is valid.

There are two remaining convergence issues. First, nonnegative inverse coefficients and **Pringsheim's theorem** imply that no complex singularity can reduce the inverse-series radius below a positive real level where the inverse is still regular. At a strictly separated reference, the simple positive crossing occurs before any positive real singularity, so \(R(T_0)\) lies strictly inside the convergence disk. Choose a slightly larger closed disk whose inverse values have modulus less than \(a\); this follows from nonnegative coefficients and the real inverse. The defining logarithmic integral is analytic under sufficiently small bounded perturbations \(T_0+sv\) there. The analytic implicit-function theorem and Cauchy estimates yield locally uniform convergence of the inverse series and of its material derivative. This justifies passage from finite truncations to the reference width and derivative.

Second, at a contact target evaluate the odd series with \(R\) replaced by \(\lambda R\), \(0<\lambda<1\). The monomials in (5.2) acquire only positive factors, so the support argument is unchanged. Letting \(\lambda\uparrow1\), the nonnegative target series increases to the exact contact width, while the separated reference value and derivative converge absolutely. Thus for both separated and contact finite targets,
\[
 M_k(T)\ge M_0+DM_k(T_0)[v].                           \tag{5.3}
\]
No assumption that every interpolating quantile remains separated was made.

## 6. The adjoint has an endpoint correction

Set
\[
 \sigma_-=-1/W_0'(x_-),\quad \sigma_+=1/W_0'(x_+),
 \quad K_j=\sqrt{(a-x_j)(2-x_j)},
\]
\[
 D=\sum_{j\in\{-,+\}}\frac{\sigma_jK_j}{a-x_j},\qquad
 d\xi(d)=\left(D-\sum_j\frac{\sigma_jK_j}{d-x_j}\right)de(d).       \tag{6.1}
\]
Both \(\sigma_j\) are positive. The numerator vanishes at \(a\) and has derivative
\(\sum_j\sigma_jK_j/(d-x_j)^2>0\). Thus \(\xi\) is finite, atomless, and positive on every nonempty subinterval; write \(R_0=\xi([a,2])>0\).

Use the spatial velocity \(v(d)=T(u)-T_0(u)\), \(d=T_0(u)\), and put \(F(d)=\mathcal A(d)v(d)\). The first variation of the weighted potential at a moving material point is
\[
 g(d)=\frac{kv(d)}d+\operatorname{pv}\int\frac{v(d)-v(e)}{d-e}\,d\eta(e).
\]
The spatial derivative of the constant-platform identity cancels the terms containing \(v(d)\). Therefore
\[
 g(d)=\operatorname{pv}\int\frac{F(e)}{e-d}\,de(e),
 \quad DM_k(T_0)[v]=-\sum_j\sigma_j\int\frac{F(d)}{d-x_j}\,de(d).    \tag{6.2}
\]
The exact identity needed is
\[
 DM_k(T_0)[v]-\int g\,d\xi
 =-\mathcal A(2)v(2)\left(\frac{\sigma_-}{K_-}+\frac{\sigma_+}{K_+}\right). \tag{6.3}
\]

Here is a direct verification. Define \(0<\rho_j<1\) by
\(x_j=c-r(\rho_j+\rho_j^{-1})/2\). Then
\[
 K_j=\frac{r(1-\rho_j^2)}{2\rho_j},\quad
 \frac{K_j}{d-x_j}=P_{\rho_j}(\theta),\quad
 P_\rho=1+2\sum_{n\ge1}\rho^n\cos n\theta.
\]
The angular density of \(\xi\) is
\(\mathcal B(\theta)=D-\sum_j\sigma_jP_{\rho_j}(\theta)\), with
\(D=\sum_j\sigma_jP_{\rho_j}(0)\). For a finite cosine expansion
\(F(c-r\cos\theta)=f_0+2\sum_{n\ge1}f_n\cos n\theta\), use
\[
 \frac1\pi\operatorname{pv}\int_0^\pi
 \frac{\cos n\phi}{\cos\theta-\cos\phi}\,d\phi=-U_{n-1}(\cos\theta).
\]
This follows from the constant, \(n=1\), and cosine-recurrence cases. The Poisson integrals of \(U_{n-1}\) are
\[
 S_n(\rho)=
 \begin{cases}(1+\rho^2-2\rho^{n+1})/(1-\rho^2),&n\text{ odd},\\
 2\rho(1-\rho^n)/(1-\rho^2),&n\text{ even}.
 \end{cases}
\]
Indeed, expand \(U_{2m}=1+2\sum_{\ell=1}^m\cos2\ell\theta\) and
\(U_{2m-1}=2\sum_{\ell=1}^m\cos(2\ell-1)\theta\). Writing
\(\Gamma=\sum_j\sigma_j/K_j\), substitution in (6.2) gives the coefficients in
\(DM_k-\int g\,d\xi\): \(-\Gamma\) for \(f_0\), \(-2\Gamma\) for even indices and \(+2\Gamma\) for odd indices. They are exactly those of
\(-\Gamma F(2)=-\Gamma(f_0+2\sum(-1)^nf_n)\), proving (6.3) for these expansions.

The actual velocity has finitely many jumps. To pass to it, use Poisson–Abel factors \(\lambda^n\). Subtract its jump steps in the angular coordinate; the remaining continuous piece is piecewise analytic and has cosine coefficients \(O(n^{-2})\). Its regularized transform is bounded by a constant times
\(1+|\log\min(\theta,\pi-\theta)|\). A jump \(\Delta\) at \(\theta_0\) contributes precisely
\[
 \frac{\Delta}{\pi r\sin\theta}
 \left[\log|1-\lambda e^{i(\theta+\theta_0)}|
 -\log|1-\lambda e^{i(\theta-\theta_0)}|\right].
\]
At the interior jump the logarithmic singularity is uniformly integrable:
its integral over an interval of length \(2\delta\) is \(O(\delta(1+|\log\delta|))\), uniformly in \(\lambda\). At either angular endpoint the numerator is \(O(\sin\theta)\), uniformly in \(\lambda\). Since \(\mathcal B\) is bounded and is \(O(\theta^2)\) at zero, these estimates give convergence of the interior pairing. Exterior integrals converge by domination, and the endpoint term converges because the even periodic extension of \(F\) is continuous at \(\pi\). Identity (6.3) therefore applies to the block velocities used here.

For the target, \(v(2)=d_N-2\le0\). The correction is nonnegative. Combining (5.3) and (6.3), we obtain the one-sided estimate
\[
 M_k(T)\ge M_0+\int g\,d\xi.                          \tag{6.4}
\]
Replacing (6.3) by an uncorrected equality would be unjustified.

## 7. Reduction to a mixed energy inequality for each block

The target quantile is constant, equal to \(d_i\), on an interval \(I_i\subset(0,1)\) of length \(p_i\). Transfer \(\xi\) to quantile space by the reference distribution function, writing \(\widehat\xi\). Put
\[
 r_i=\widehat\xi(I_i)>0,\qquad
 E(I_i)=\int_{I_i}\int_{I_i}
       \log|T_0(u)-T_0(v)|\,dv\,d\widehat\xi(u).
\]
All these integrals are absolutely convergent. In angular coordinates the logarithm is the sum of two log-sine kernels and a constant, while both density factors are bounded. The log-sine singularities are integrable on the square. In particular Fubini applies, including at shared block endpoints.

For \(u\in I_i\), off-block target differences and reference differences have the same sign because both quantiles are ordered. Apply
\[
 (y-x)/x\ge\log y-\log x\qquad(x,y>0)
\]
to their absolute values. On the same block the corresponding quotient of differences is exactly \(-1\). Applying the same inequality to \(d_i/T_0(u)\), then using the platform identity (4.3) and the definition of \(R_i\), gives
\[
 g(T_0(u))\ge-p_i\log R_i-C-p_i
              +\int_{I_i}\log|T_0(u)-T_0(v)|\,dv.
\]
Together with (2.2) and (6.4), this yields
\[
 J_k\ge M_0+\sum_i\{E(I_i)-p_ir_i\log R_i-Cr_i-p_ir_i+2R_i\}.
\]
For fixed \(p_i,r_i>0\), the expression depending on \(R_i\) has its unique minimum at \(R_i=p_ir_i/2\). Therefore
\[
 J_k\ge M_0+\sum_i\left\{E(I_i)-p_ir_i\log(p_ir_i/2)-Cr_i\right\}.  \tag{7.1}
\]

For any proposed lower target \(L\), define
\[
 C_{\mathrm{eff}}=C+(L-M_0)/R_0.
\]
If every nonempty quantile interval \(I\), of ordinary mass \(p=|I|\) and adjoint mass \(r'=\widehat\xi(I)\), satisfies
\[
 \frac{E(I)}{pr'}-\log(pr'/2)-\frac{C_{\mathrm{eff}}}{p}>0,         \tag{7.2}
\]
then each excess in (7.1) is strictly larger than
\((C_{\mathrm{eff}}-C)r_i\). Since \(\sum_i r_i=R_0\), a finite sum gives \(J_k>L\). Positivity of both masses is indispensable. No classification of equality in an earlier inequality is necessary once (7.2) is strict.

## 8. The named external circle theorem and the exact scalar formula

Write \(\mathcal A(\theta)=\mathcal A(c-r\cos\theta)\) and use
\(d\eta=\mathcal A(\theta)d\theta/\pi\),
\(d\xi=\mathcal B(\theta)d\theta/\pi\).
Both factors are nonnegative and increasing on \([0,\pi]\). Put
\[
 a_\pi=\mathcal A(\pi),\quad b_\pi=\mathcal B(\pi),\quad
 Q=\int_J\frac{\mathcal A(\theta)}{a_\pi}\,d\theta,\quad
 R=\int_J\frac{\mathcal B(\theta)}{b_\pi}\,d\theta
\]
for the angular interval corresponding to a block. Its physical masses are
\(p=a_\pi Q/\pi\) and \(r'=b_\pi R/\pi\).

### 8.1 Exact external input

We use **Michael Christ and Marina Iliopoulou, *Inequalities of Riesz-Sobolev type for compact connected Abelian groups*, Theorem 1.1 and its nonnegative-function extension (1.3)** [CI]. With normalized Haar measure, the theorem bounds a convolution pairing by the same pairing of symmetric decreasing rearrangements. It applies on the circle to arbitrary nonnegative measurable functions. No equality, stability, or strict-admissibility theorem from that paper is used.

This is an explicit replacement for relying on an unqualified citation to Baernstein's 1989 paper: that work has a 1995 correction, and [CI] cites both. The inspected primary [CI] PDF was edited March 12, 2021. We do not purport to reconstruct its proof. Its Theorem 1.5 also gives a direct alternative by applying its \([0,1]\)-valued version at each layer of the kernel, but Theorem 1.1/(1.3) is sufficient here.

### 8.2 Applying the theorem, with normalization

Let the circle have length \(2\pi\), and set
\[
 K(t)=\log|e^{it}-1|,\qquad \ell(t)=\log2-K(t).
\]
On \([-\pi,\pi]\), \(\ell\) is nonnegative, integrable, even, and decreasing in \(|t|\). Define the even extensions
\[
 f(\theta)=1_J(|\theta|)\mathcal A(|\theta|)/a_\pi,\qquad
 g(\theta)=1_J(|\theta|)\mathcal B(|\theta|)/b_\pi .
\]
They lie between zero and one, and have ordinary Lebesgue masses \(2Q\) and \(2R\). Rescaling to Haar probability introduces equal factors on both sides of the external theorem, so we may retain ordinary Lebesgue measure.

The theorem, applied to \(\min(\ell,N)\) and then by monotone convergence, increases the \(\ell\)-energy under symmetric decreasing rearrangement. For a symmetric decreasing nonnegative \(h\) and \(0\le p\le1\) of mass \(2Q\),
\[
 \int(1_{[-Q,Q]}-p)(h-h(Q))\ge0.
\]
The two factors have the same sign inside and outside the centered arc, and the constant term cancels by equality of masses. This is the fixed-mass comparison allowing \(p\) to be replaced by its centered arc. Convolutions of symmetric decreasing nonnegative circle functions are symmetric decreasing: layer-cake reduces this to the elementary circular overlap of two centered arcs. Two such comparisons replace \(f^*,g^*\) by the centered arcs of half-lengths \(Q,R\). Thus the \(K\)-energy is bounded below by that of those arcs.

The identity
\[
 \frac{|d(\theta)-d(\phi)|}{H}
 =|e^{i\theta}-e^{i\phi}|\,|e^{i\theta}-e^{-i\phi}|
\]
is responsible for the factor two. Splitting the even-extended double integral into four quadrants gives
\[
 \frac{E(I)}{pr'}-\log H
 =\frac1{2QR}\int_{\mathbb T}\int_{\mathbb T}
    f(\theta)g(\phi)K(\theta-\phi)\,d\theta\,d\phi.
\]
The normalized centered-arc energy is
\[
 \mathscr A(Q,R)=\frac1{4QR}\int_{-Q}^Q\int_{-R}^R K(\theta-\phi)\,d\phi\,d\theta
 =-\sum_{n\ge1}\frac{\sin(nQ)\sin(nR)}{n^3QR}.
\]
The series follows by first using the Abel-regularized Fourier expansion of \(K\), then passing to the integrable kernel. Its integrated series is absolutely convergent for fixed positive \(Q,R\). We obtain \(E(I)/(pr')\ge\log H+2\mathscr A(Q,R)\).

Write \(\operatorname{sinc}X=\sin X/X\) and
\[
 h(X)=\mathscr A(X,X)-\log(X/\pi)
 =\log(2\pi)-\frac32+2\int_0^1(1-t)\log\frac{\sin Xt}{Xt}\,dt.
\]
The function \(\sin u/u\) decreases on \((0,\pi)\), because
\(\sin u-u\cos u\) has derivative \(u\sin u>0\). Hence \(h\) decreases on \((0,\pi]\). Its series gives \(h(\pi)=0\), so \(h\ge0\).
Finally,
\[
 2\mathscr A(Q,R)-\mathscr A(Q,Q)-\mathscr A(R,R)
 =\sum_{n\ge1}\frac{(\operatorname{sinc}(nQ)-\operatorname{sinc}(nR))^2}{n}.
\]
Substitution and cancellation of the physical masses yield
\[
\begin{split}
 \frac{E(I)}{pr'}-\log(pr'/2)-\frac{C_{\mathrm{eff}}}{p}
 \ \ge\ &\log\frac{2H}{a_\pi b_\pi}+h(Q)+h(R)\\
 &+\sum_{n\ge1}\frac{(\operatorname{sinc}(nQ)-\operatorname{sinc}(nR))^2}{n}
 -\frac{\pi C_{\mathrm{eff}}}{a_\pi Q}.                 \tag{8.1}
\end{split}
\]
This expression, with all factors of two and \(\pi\) included, is the sole block scalar submitted to the numerical calibration.

## 9. The one-cut family and its actual exterior branches

For \(q\) in the admissible interval set
\[
 s=\frac{1-q}{1+q},\quad a_{\mathrm{sh}}=2s^2,\quad
 H=\frac{2q}{(1+q)^2},\quad D_0=\frac{2}{(1+q)^2}=\frac Hq.
\]
The platform is zero when
\[
 k=-\frac{\log H}{\log(H/q)},\qquad A=\frac{k}{k+1}=\frac{\log H}{\log q}.
\]
After undoing the shift and multiplying the residual probability by \(1-A\), the corresponding probability on \([-1,1]\) is
\[
 d\mu_q=A\delta_{-1}
 +\frac{1-2As/(t+1)}{\pi\sqrt{(t-(2s^2-1))(1-t)}}\,1_{(2s^2-1,1)}(t)\,dt. \tag{9.1}
\]
It is nonnegative exactly when \(A\le s\). Define
\[
 d(q)=\log2-2\log(1+q),\qquad
 \chi(q)=(1+q)d(q)+2q\log q.
\]
Algebra gives \(A\le s\) if and only if \(\chi\ge0\), while
\[
 \chi'(q)=\log\frac{2q^2}{(1+q)^2}<0,\qquad\chi(0+)=\log2.
\]
Opposite endpoint signs in the numerical isolation of \(q_s\), together with this monotonicity, identify its unique zero. Its isolated interval is below \(0.124<3-2\sqrt2\); the last inequality can be checked from \(0.124^2-6(0.124)+1>0\).

For \(u>1\), set
\[
 x_{\mathrm{sh}}=1+s^2-H(u+u^{-1}).
\]
Here \(K_x=H(u-u^{-1})\), the exterior Poisson parameter is \(1/u\), and
\[
 x_{\mathrm{sh}}=D_0(u-q)(1-qu)/u.
\]
The reference potential reduces exactly to
\[
 W_0(x_{\mathrm{sh}})=-(k+1)F(q,u).
\]
The derivative of \(F\) on \(1<u<1/q\) is
\[
 F_u=\frac{qu^2-Bu+q}{u(u-q)(1-qu)},\quad
 B=1+q^2-A(1-q^2).
\]
When \(q<q_s\), \(B>2q\). The numerator has reciprocal positive roots, with exactly one in \((1,1/q)\). Thus \(F\) first decreases from \(F(q,1)=0\), then increases to \(+\infty\). There is exactly one nontrivial plus root, and it is simple. For \(u>1/q\),
\[
 F_u=-\frac{A(1-q^2)}{(u-q)(qu-1)}-\frac1u<0,
\]
with limits \(+\infty,-\infty\), so the minus root is unique and simple. At \(q_s\) the plus derivative numerator is \(q(u-1)^2\), and the nontrivial branch reaches \(u=1\). The regular soft chart below justifies its continuation.

The two physical endpoints, after undoing the shift, are
\[
 \alpha=s^2-H(u_-+u_-^{-1}),\qquad
 \beta=s^2-H(u_++u_+^{-1}).
\]
Their distance is precisely \(\Lambda(q)\). These branch classifications identify the roots of the interval equations; a root box near a floating approximation would not suffice.

## 10. Numerical obligation A: global minimization in the one-cut family

The independent Certificate 6.1 replacement has a scale \(S=2^{240}\). Its fixed record is replayed without floating proposals. The obligation is to verify all interval signs, root brackets, chart joins, and final rational comparisons specified here, not just a sampled approximation to the minimum.

### 10.1 Bulk and complete singular tail

Use \(\tau=-1/\log q\), \(q=e^{-1/\tau}\), and \(z_\pm=qu_\pm\). Then \(A=1-\tau d(q)\), and the regularized equations are
\[
 G_\pm(\tau,z)=A\log\frac{z-q^2}{|1-z|}-\log z-d(q)=0,               \tag{10.1}
\]
\[
 \Lambda=\frac{2(z_--z_+)}{(1+q)^2}
 +\frac{2q^2}{(1+q)^2}(z_-^{-1}-z_+^{-1}).                       \tag{10.2}
\]
For each closed parameter slab, rational root boxes must have uniformly opposite endpoint signs and a strictly positive plus derivative or strictly negative minus derivative throughout. The boxes must satisfy \(q<z_+<1<z_-\). Their existence and correct branch identity then precede any Newton contraction.

If \(m\) is a dyadic midpoint and \(Z\) already contains the roots for every parameter in \(P\), the mean-value theorem gives
\[
 z\in m-G(P,m)/G_z(P,Z).
\]
Intersection with this interval preserves every previously established root; it is not used as an existence criterion.

Ordinary implicit differentiation supplies
\[
 z_\tau=-G_\tau/G_z,\qquad
 z_{\tau\tau}=-(G_{\tau\tau}+2G_{\tau z}z_\tau+G_{zz}z_\tau^2)/G_z.
\]
For completeness,
\[
 q_\tau=q/\tau^2,\quad q_{\tau\tau}=q(1-2\tau)/\tau^4,\quad
 d_\tau=-2q_\tau/(1+q),\quad
 d_{\tau\tau}=-2\{q_{\tau\tau}/(1+q)-q_\tau^2/(1+q)^2\}.
\]
Also \(A_\tau=-d-\tau d_\tau\) and
\(A_{\tau\tau}=-2d_\tau-\tau d_{\tau\tau}\). For
\(U=\log(z-q^2)-\log|1-z|\),
\[
 U_z=(z-q^2)^{-1}+(1-z)^{-1},\quad
 U_{zz}=-(z-q^2)^{-2}+(1-z)^{-2},
\]
\[
 U_\tau=-2qq_\tau/(z-q^2),\quad
 U_{\tau z}=2qq_\tau/(z-q^2)^2,
\]
\[
 U_{\tau\tau}
 =-2(q_\tau^2+qq_{\tau\tau})/(z-q^2)
  -(2qq_\tau)^2/(z-q^2)^2.
\]
Product rules for \(G=AU-\log z-d\) and (10.2) complete all derivative formulas.

Extend \(q(0)=0\). On the complete tail \(0\le\tau\le1/50\),
\[
 0\le q\le e^{-50},\qquad0\le q_\tau\le2500e^{-50}.
\]
The fixed boxes
\(499/1000\le z_+\le501/1000\) and
\(149/100\le z_-\le15001/10000\)
pass uniform endpoint and derivative signs. At zero, (10.1) reduces to
\(-\log(2|1-z|)=0\), whose simple roots are \(1/2,3/2\).
The same regularized first-derivative calculation encloses
\(-0.788<\Lambda_\tau<-0.737\) throughout the closed tail. No unexamined positive cutoff replaces this limiting argument.

### 10.2 Soft edge

Set \(y=(\log u_+)^2\), and define positive series (the first two are entire; the third is analytic for \(|w|<1\))
\[
 C_0(y)=\sum_{m\ge0}\frac{y^m}{(2m)!},\quad
 S_0(y)=\sum_{m\ge0}\frac{y^m}{(2m+1)!},\quad
 T_0(w)=\sum_{m\ge0}\frac{w^m}{2m+1}.
\]
Here \(T_0(w)\) is a scalar series, unrelated to the earlier reference quantile. Put
\(b=qS_0/(1-qC_0)\), \(w=yb^2\). After deflating the identically present root \(u=1\), the plus equation is
\[
 D(q,y)=A-1+2AbT_0(w)=0.                             \tag{10.3}
\]
The conditions \(y\ge0\), \(1-qC_0(y)>0\), \(0\le w<0.03\) imply
\(qe^{\sqrt y}<1\), so the hyperbolic/atanh identity leading to (10.3) is on the correct real branch. Also
\(D(q,0)=A(1+q)/(1-q)-1=(A-s)/s\).

Each regular soft slab verifies strict opposing signs and \(D_y>0\). The final slab extends numerically beyond the upper isolation of \(q_s\), but its application is restricted to \(q\le q_s\). On that admissible subdomain \(D(q,0)\le0\) analytically. The positive upper sign and \(D_y>0\) therefore supply the root, including \(y=0\) at the endpoint. No root for inadmissible parameters is asserted.

The length is evaluated in the nonsingular form
\[
 \Lambda=\frac{2z_-}{(1+q)^2}+\frac{2q^2}{(1+q)^2z_-}-2HC_0(y).
\]
Using \(y_q=-D_q/D_y\) and \((z_-)_q=-(G_-)_q/(G_-)_z\), its total derivative is strictly positive in each soft slab.

Each series is summed through index 32. With \(K=33\), upper argument \(Y\), and shift \(\sigma=0,1\), the \(C_0,S_0\) tails and their first derivatives are bounded above by
\[
 \frac{Y^K}{(2K+\sigma)!(1-\rho)},\qquad
 \frac{KY^{K-1}}{(2K+\sigma)!(1-(K+1)\rho/K)},
 \quad \rho=\frac{Y}{(2K+\sigma+2)(2K+\sigma+1)}.
\]
For \(T_0\), replace \((2K+\sigma)!\) by \(2K+1\) and \(\rho\) by \(Y\). For \(C_0\) and \(S_0\), successive value-term ratios decrease and are bounded by \(\rho\), while derivative-term ratios are bounded by \((K+1)\rho/K\). For \(T_0\), value-term ratios are bounded above by \(Y\) and derivative-term ratios by \((K+1)Y/K\) for indices at least \(K\). These bounds justify the displayed geometric tails; all denominators are checked positive. Value and derivative remainders are bounded separately before chain-rule propagation.

### 10.3 Exhaustive coverage and one stationary point

The independent cover differs from the source author's subdivision. It checks:

| Chart | Full domain | Finite slabs | Required result |
|---|---|---:|---|
| Closed tail | \(0\le\tau\le1/50\) | 1 | \(\Lambda_\tau<0\) |
| Left bulk | \(1/50\le\tau\le27/100\) | 38 | \(\Lambda_\tau<0\) |
| Convex tube | \(27/100\le\tau\le28/100\) | 2 | \(\Lambda_{\tau\tau}>0\) |
| Right bulk | \(28/100\le\tau\le87/200\) | 75 | \(\Lambda_\tau>0\) |
| Regular soft | \(1/10\le q\le6181/50000\) | 51 | \(\Lambda_q>0\) |
| Endpoint soft | \(6181/50000\le q\le q_s\) | 1 | \(\Lambda_q>0\) |

The record verifies first and last endpoints and every adjacent overlap, using exact rational subdivision and outward dyadic conversion. The cross-chart inequality
\(1/10<e^{-200/87}<q_s\) supplies a genuine overlap, not just a rounded equality. Since \(dq/d\tau>0\), the derivative orientations agree.

With the exact rational proposal
\[
 q_c=0.02571553686652745032257637166391965344,\quad \tau_c=-1/\log q_c,
\]
two dyadic points enclosing \(\tau_c\pm10^{-30}\) lie strictly in the convex tube and have strictly negative and strictly positive first derivatives respectively. Continuity gives a stationary point; strict convexity gives uniqueness within the tube; all remaining derivative signs exclude others and establish a unique global minimum on the whole admissible family.

Uniform substitution over this narrow stationary box gives outward decimal displays
\[
\begin{split}
 q_*&\in[
 0.02571553686652745032257637166357505416085527329520287597773595470,\\
 &\hspace{22mm}
 0.02571553686652745032257637166426425271914472670479712402226614016],\\
 L&\in[
 1.834430475762661711090753635120553436511864256655884976379752017,\\
 &\hspace{22mm}
 1.834430475762661711090753635129018849529897507462271417764406996].
\end{split}
\]
The raw endpoints are dyadic integers, not parsed versions of these displays. The replay checks the shorter theorem decimals directly against those endpoints, including
\(0.123630684649383<q_s<0.123630684649384\).

## 11. The already accepted fixed upper bound and exact target linkage

The existing accepted fixed-candidate argument establishes, at the exact \(q_c\) above,
\[
 \inf_{f\in\mathcal P}|E_f|\le\Lambda(q_c)
 <T:=1.83443047576266171109075363512901884952989750747.              \tag{11.1}
\]
That result was published in draft PR 1310 [U], with positive-platform recovery and rational witnesses. It did not establish global minimality, the matching lower bound, or nonattainment.

For clarity, its exact rational root boxes are the following centers with radius \(10^{-45}\):
\[
 p_c=
 \frac{17861896208523519533866067426369570685214609183110155278092269729}
 {10^{63}},
\]
\[
 m_c=
 \frac{11085120457314950695388194505227588799135079864873862940404965203}
 {2\cdot10^{62}}.
\]
At \(q=q_c\), exact rational logarithm intervals using 90 atanh terms prove negative/positive signs at \(p_c\mp10^{-45}\), and positive/negative signs at \(m_c\mp10^{-45}\). The branch proof in Section 9 identifies the roots. Monotonicity of \(u+u^{-1}\) for \(u>1\) then bounds the width from above by
\[
 H\{m_h+m_h^{-1}-p_l-p_l^{-1}\}<T.
\]
The previously accepted outward upper display is
\(1.8344304757626617110907536351247861430208808821566781865818401394\), strictly below the exact rational \(T\). Section 14 supplies the recovery argument uniformly at any strictly admissible one-cut parameter, so the same argument specializes to this accepted candidate.

Once numerical obligation A gives family minimality, \(L\le\Lambda(q_c)<T\). Independently, its new raw dyadic enclosure itself has upper endpoint strictly below \(T\); the exact rational positive difference was checked by the end-to-end interface audit. Either bridge is sufficient. Replacing \(T\) by the shortened \(1.834430475762662\) would not justify the finite-reference signs in the next section.

## 12. Numerical obligation B: a strictly positive block calibration for every finite \(k\ge29/20\)

This is a sufficient independent replacement for Wang's Certificate 7.1. It is not a reproduction of the source author's slab counts or stronger reported margin digits. Every smaller positive margin below is sufficient for (7.2).

### 12.1 Finite references and explicitly evaluated quantities

For a reference \((k,a)\), let
\[
 \rho_0=\frac{\sqrt2-\sqrt a}{\sqrt2+\sqrt a},\quad
 K_x=\sqrt{(a-x)(2-x)},\quad \rho_x=\frac r{c-x+K_x}.
\]
For the physical exterior chart \(x<a,\ x\ne0\), Poisson expansion gives
\[
 W_0(x)=k\log|x|+\log\frac{c-x+K_x}{2}
                   -2k\log(1-\rho_0\rho_x),                         \tag{12.1}
\]
\[
 W_0'(x)=\frac kx-\frac1{K_x}
         +\frac{2k\rho_0\rho_x}{K_x(1-\rho_0\rho_x)}.                \tag{12.2}
\]
The interval code checks the chart before using these formulas. Uniform opposite endpoint signs and slopes throughout the root boxes prove (4.4), rather than merely locating some algebraic zero. Three Newton intersections preserve these roots.

At the crossings, with \(\rho_\pm=\rho_{x_\pm}\), the required constants are
\[
 a_\pi=1+\frac{2k\rho_0}{1+\rho_0},\quad
 b_\pi=4\sum_j\frac{\sigma_j\rho_j}{1-\rho_j^2},\quad
 R_0=2\sum_j\frac{\sigma_j\rho_j}{1-\rho_j},
\]
\[
 Q_{\max}=\pi/a_\pi,\qquad R_{\max}=\pi R_0/b_\pi,\qquad
 C_{\mathrm{eff}}(T)=C+(T-M_0)/R_0.                              \tag{12.3}
\]
The bounds on block masses follow by integrating over the entire reference interval. All denominator signs, Poisson ranges, density positivity, root slope signs, and positive adjoint mass are tested.

The finite references are
\[
 a=1153/500-k/4\quad(36/25\le k\le21/10),\qquad
 a=9/5\quad(21/10\le k\le21/5).                                \tag{12.4}
\]
Their initial rational mesh has width \(1/400\); an unresolved slab is bisected and never accepted from a sampled sign. The completed covers contain 395 and 840 slabs respectively.

On each slab the checks give \(C_{\mathrm{eff}}(T)<0\) and
\(0<R_{\max}<Q_{\max}<\pi\). Put
\[
 B=\log(2H/(a_\pi b_\pi))+h(Q_{\max})+h(R_{\max}),\qquad
 P=-\pi C_{\mathrm{eff}}(T)/a_\pi>0.
\]
For \(a=9/5\), dropping all nonnegative squares in (8.1) gives the lower bound \(B+P/Q_{\max}\), which is positive.

For the affine reference, if \(Q\le R_{\max}\), use \(B+P/R_{\max}\). If \(R_{\max}\le Q\le Q_{\max}\), retain the \(n=1\) square and use decreasing sinc to obtain
\[
 f(Q)=B+P/Q+(\operatorname{sinc}Q-\operatorname{sinc}R_{\max})^2.
\]
The code covers \(Q=R_{\max}+u(Q_{\max}-R_{\max})\) by 32 closed rational \(u\)-intervals and proves
\[
 f'(Q)=-P/Q^2+
 2(\operatorname{sinc}Q-\operatorname{sinc}R_{\max})\operatorname{sinc}'Q<0.
\]
It then suffices to test \(f(Q_{\max})>0\), together with \(B+P/R_{\max}>0\). These bounds include every positive block mass, however small; there is no hidden minimum-mass cutoff.

For every \(X>0\) used in these checks,
\[
 h(X)=-\sum_{n=1}^{80}\frac{\sin(nX)^2}{n^3X^2}
      -\log(X/\pi)+\epsilon_X,\quad
 -\frac1{2\cdot80^2X^2}\le\epsilon_X\le0.                       \tag{12.5}
\]
This follows from \(\sum_{n>80}n^{-3}\le1/(2\cdot80^2)\).
Monotonicity of \(h\) allows outward upper caps in lower bounds. No special-function or trilogarithm oracle is used.

Increasing the target \(L\) to \(T\) increases \(C_{\mathrm{eff}}\) and decreases (8.1). Thus the exact bridge \(L<T\) in Section 11 makes every finite check at \(T\) a valid lower bound for the desired check at \(L\).

### 12.2 Terminal zero-platform references, without an omitted infinite tail

Let \(q>0\), \(\tau=-1/\log q\), \(t=\tau d(q)=1-A\), and
\[
 k=(1-t)/t,\qquad a=2\left(\frac{1-q}{1+q}\right)^2.
\]
Then \(C=0\) exactly. The two exterior equations are (10.1). Their boxes satisfy \(q<z_+<1<z_-\); uniform signs, slopes, and four Newton intersections identify the physical branches.

Define
\[
 P_0=t+\frac{2q(1-t)}{1+q},\quad
 \operatorname{raw}(z)=1-\frac{A(1-q^2)z}{(1-z)(z-q^2)},
\]
\[
 w_+=-1/\operatorname{raw}(z_+),\qquad
 w_-=1/\operatorname{raw}(z_-),\qquad
 D_*=2P_0(w_++w_-).                                          \tag{12.6}
\]
The signs \(\operatorname{raw}(z_+)<0<\operatorname{raw}(z_-)\) are checked. The exact cancellations are
\[
 D_*=\frac{a_\pi b_\pi}{2H},\quad
 Q_{\max}=\frac{\pi t}{P_0},\quad
 R_{\max}=
 \frac{\pi[(1+q/z_+)w_++(1+q/z_-)w_-]}{2(w_++w_-)}.             \tag{12.7}
\]
To verify rather than assume the cancellation, differentiate the one-cut exterior relation:
\(\operatorname{raw}=-uF_u\),
\(dx/du=-H(1-u^{-2})\), and \(W_0=-(k+1)F\).
Hence each positive inverse-slope magnitude is \(\sigma=tK w\). Therefore
\[
 a_\pi=P_0/t,\quad b_\pi=4tH(w_++w_-),\quad
 R_0=2tH[(1+q/z_+)w_++(1+q/z_-)w_-],
\]
which proves (12.7). These are identities at every finite positive \(\tau\), not substitutions at a singular limit.

Obligation A gives \(M_0=\Lambda(q)\ge L\) for all admissible terminal references. Since \(C=0\),
\[
 C_{\mathrm{eff}}=(L-M_0)/R_0\le0.
\]
Its contribution in (8.1) is consequently nonnegative. This is precisely where the **global family minimum**, rather than only a fixed upper bound, is needed. We may drop that contribution and the nonnegative square series. On the simple terminal boxes it suffices to prove \(-\log D_*>0\); on the refined boxes retain \(h(Q_{\max})+h(R_{\max})\).

For the complete tail \(0<\tau\le1/50\), use \(q<2^{-72}\).
For example \(\log2<25/36\) implies \(72\log2<50\).
Evaluate the closed independent box
\[
 0\le\tau\le1/50,\quad0\le q\le2^{-72},\quad
 z_+\in[499/1000,501/1000],\quad z_-\in[149/100,15001/10000].
\]
The same endpoint and slope tests prove containment. Reference positivity requires
\(\mathcal A(a)=1-2kq/(1-q)>0\). Since \(q(\tau)/\tau\) increases on \((0,1)\),
\[
 kq\le q/(\tau d)\le50\cdot2^{-72}/d_{\mathrm{lower}},
\]
which certifies positivity without inverting an interval containing zero.
The cancelled expression \(D_*\) is well-defined throughout the closed box and is at most \(0.038237980791\). At every actual \(\tau>0\), it is positive. Therefore
\(-\log D_*\ge1-D_*>0.961762019209\).
No finite reference at \(\tau=0\) is asserted.

The remaining terminal boxes cover from \(1/50\) to
\(\tau(q_{\mathrm{cap}})\), with
\(q_{\mathrm{split}}=26631/10^6\) and
\(q_{\mathrm{cap}}=41542/10^6\).
There are 256 simple slabs and 39 refined slabs.
The transformation from exact rational \(q\) to a \(\tau\)-interval is outward: the simple cover reaches the split's upper endpoint, the refined cover begins at the split's lower endpoint, and the refined cover reaches the cap's upper endpoint. Thus conversion cannot leave a gap.

The exact endpoint checks give
\[
 \chi(q_{\mathrm{cap}})>0.372861191115,\qquad
 4.199981974345<k(q_{\mathrm{cap}})<4.199981974346<21/5.
\]
Furthermore
\[
 k'(q)=-\frac{\chi(q)}{q(1+q)d(q)^2}<0,\qquad k(q)\longrightarrow\infty
 \quad(q\downarrow0).
\]
Since \(\chi\) is decreasing, the cap check proves admissibility throughout this terminal interval. It also proves that the terminal family covers every \(k\ge21/5\), with strict overlap. In the simple terminal range, \(Q_{\max}<\pi\) follows from \(a_\pi>1\), and \(R_{\max}/\pi\) is a positive weighted mean of two numbers \((1+q/z_\pm)/2<1\). In the refined range both strict cap inequalities are additionally interval-checked before use of (12.5).

### 12.3 The actual independent lower margins

The proved normalized-surplus lower bounds, rounded downward for display, are:

| Reference | Cover | Strict lower bound |
|---|---:|---:|
| Affine \(a=1153/500-k/4\), \(36/25\le k\le21/10\) | 395 slabs | \(0.028229353338717\) |
| Constant \(a=9/5\), \(21/10\le k\le21/5\) | 840 slabs | \(0.036361685512222\) |
| Closed tail, \(0<\tau\le1/50\) | one box | \(0.961762019209\) |
| Simple terminal to \(\tau(q_{\mathrm{split}})\) | 256 slabs | \(0.000564594536104\) |
| Refined terminal to \(\tau(q_{\mathrm{cap}})\) | 39 slabs | \(0.065630278169259\) |

The 1,530 finite slabs plus the singular-tail box cover all required parameters. The elementary range overlaps the affine range because \(36/25<29/20\). The two finite reference ranges share \(21/10\), and the terminal range overlaps \(21/5\) strictly. These conclusions depend on exact endpoint comparisons in the records, not decimal inspection of this table.

## 13. What constitutes a rigorous computation here

Both independent kernels represent \([l/S,u/S]\) by integers \(l\le u\), with \(S=2^{240}\) for obligation A and \(S=2^{160}\) for obligation B. Rational and terminating-decimal inputs are enclosed by exact integer division. Lower endpoints round toward minus infinity, upper endpoints toward plus infinity. Products use all four corners, and reciprocal is permitted only when zero is excluded. A square crossing zero includes zero as its minimum. Thus each primitive preserves real inclusion. The Python integer implementation and execution hardware remain ordinary trust assumptions.

For \(\log x\), reduce an exact positive endpoint by an exact power of two to \(y\in[1,2]\) and set \(v=(y-1)/(y+1)\). Use
\[
 \log y=2\sum_{j=0}^{N-1}\frac{v^{2j+1}}{2j+1}+\epsilon,\quad
 0\le\epsilon\le\frac{2v^{2N+1}}{(2N+1)(1-v^2)}.
\]
The same formula bounds \(\log2\), after which the signed integer multiple of \(\log2\) restores the scale. Obligation A uses \(N=96\), B uses \(N=56\). Endpoint monotonicity gives a log enclosure for an interval.

For the exponential, reduce a nonnegative argument by repeated halving. Obligation A uses \(v\le1/8\), sums through degree 60, and bounds the omitted tail by
\((v^{61}/61!)/(1-v/62)\). Obligation B uses \(v\le1\), sums to the same degree, and bounds the tail by \(2/61!\). Repeated interval squaring restores the scale, and negative inputs use reciprocal. Every truncation and rounding error remains inside the final interval.

Obligation B's square root uses integer square root of \(lS,uS\), with a one-unit upward correction unless the upper radicand is a perfect square. It encloses \(\pi\) with
\(16\arctan(1/5)-4\arctan(1/239)\), using 120 alternating terms and next-term remainder bounds. Trigonometric range reduction is accepted only after proving that the reduced interval lies in \([-4,4]\). The sine polynomial through degree 73 has error at most \(4^{75}/75!\), and cosine through degree 72 has error at most \(4^{74}/74!\). For nonpoint intervals, all possible sine/cosine critical points are enumerated; the search window's extreme critical points are checked to lie beyond the input endpoints. This prevents an endpoint-only enclosure from omitting an interior extremum.

First- and second-order derivative records obey ordinary chain/product rules. A second derivative product contains the term \(2f'g'\); reciprocal has second derivative \(2(f')^2/f^3-f''/f^2\). The soft-series remainders in Section 10 bound derivatives separately.

Floating computations may propose roots, subdivisions, or trigonometric integers. Every accepted proposal must pass the exact domain, sign, slope, and interval containment tests. Obligation A's saved-record replay is float-free; the full obligation B regeneration still uses validated floating proposals. Correctness does not depend on their accuracy, but termination or choice of accepted subdivisions can. Neither implementation should be presented as a formally verified or general-purpose hostile-input interval library.

All proof gates use explicit exception checks, rather than Python assertions removable by optimization. The frozen kernel audit independently checked the arithmetic, series remainders, derivative propagation, and root contraction and ran 2,454 exact tests, including 29 rejection controls, in normal, -O, and -OO modes with identical receipts. The complete certificate builders separately ran their full checks in these modes. Obligation B's coverage checker rejected nine corruption/domain controls. These tests corroborate the inclusion proofs; finite tests alone never certify a continuum.

## 14. Strict finite lower bound and sharp recovery

### 14.1 Strictness for every individual finite polynomial

Using numerical obligations A and B with the analytic chain above, consider an atomized finite target. The single-atom case has length 2, and Section 3 gives \(J_k>2\) for the elementary range. Every other finite \(k\) has a reference for which (8.1) is strictly positive for every positive block mass. Each block has \(p_i>0\) and \(r_i>0\), and there are finitely many blocks. Equations (7.1)–(7.2) give \(J_k>L\). By (2.2), and finally the inclusion (1.1),
\[
 |E_f|>L\qquad\text{for every }f\in\mathcal P.                    \tag{14.1}
\]
There is no claim of a uniform positive excess over all degrees or all parameters.

### 14.2 A positive platform before discretizing

At \(q=q_*\), fix \(s=s(q_*)\), \(a=2s^2-1\), and \(A_*=A(q_*)<s\).
For \(A_*<A<s\) sufficiently close to \(A_*\), put
\[
 d\mu_A=A\delta_{-1}
       +\left(1-\frac{2As}{t+1}\right)
         \frac{1_{(a,1)}(t)\,dt}{\pi\sqrt{(t-a)(1-t)}}.            \tag{14.2}
\]
The density is positive because its minimum factor is \(1-A/s>0\).
The arcsine mass and reciprocal moment are \(1\) and \(1/(2s)\), respectively; hence its continuous mass is \(1-A\) and \(\mu_A\) is a probability supported in \([-1,1]\).

The conductor value of its potential is
\[
 C(A)=\log((1-a)/4)-A\log q_*=\log H(q_*)-A\log q_*>0,            \tag{14.3}
\]
since it vanishes at \(A_*\) and \(\log q_*<0\). Let
\(S(z)=\sqrt{(z-a)(z-1)}\) be the branch asymptotic to \(z\) at infinity. The arcsine transform and partial fractions give, off the support,
\[
 V_A'(z)=\frac{1-2As/(z+1)}{S(z)}.                              \tag{14.4}
\]
For real \(x<a\), \(S(x)<0\). On \((-\infty,-1)\), the potential decreases from \(+\infty\) to \(-\infty\), giving one simple zero. On \((-1,a)\), it increases until \(2As-1<a\), then decreases to the positive conductor value, giving one simple zero on the increasing branch. On \((1,\infty)\), the derivative is positive and the starting value is positive, so there is no further zero. Its negative set is exactly one interval and its zero set has two points.

At \(A=A_*\), the conductor value is zero, but the two exterior crossings remain simple by Section 9; they are separated from the conductor. The implicit-function theorem applied near them gives
\[
 |E_{\mu_A}|\longrightarrow\Lambda(q_*)=L
 \quad\text{as }A\downarrow A_* .                               \tag{14.5}
\]

### 14.3 Actual equal-weight empirical measures and monic polynomials

Fix \(A>A_*\). Choose quantile midpoint empirical approximations
\(\nu_n=n^{-1}\sum_{j=1}^n\delta_{t_{j,n}}\Rightarrow\mu_A\).
Their roots lie in \([-1,1]\), and repeated roots accommodate arbitrary atom masses.

Weak convergence of such probabilities implies convergence of their logarithmic potentials in \(L^1(-2,2)\). A direct proof avoids continuity at the logarithmic singularity. Truncate below:
\(K_M(x,t)=\max(\log|x-t|,-M)\).
For each fixed \(x\), this is bounded continuous in \(t\). Weak convergence and bounded convergence in \(x\) give convergence of the truncated potentials in \(L^1\). Uniformly in \(t\),
\[
 \int_{-2}^2\{K_M(x,t)-\log|x-t|\}\,dx\le2e^{-M}.
\]
This is the integral of \(-M-\log|y|\) over \(|y|<e^{-M}\).
After integrating against any probability, the same error bound applies; let \(n\to\infty\), then \(M\to\infty\).

If \(v_n\to v\) in measure and the zero set of \(v\) has measure zero, then
\[
 \{1_{\{v_n<0\}}\ne1_{\{v<0\}}\}
 \subset\{|v|\le\delta\}\cup\{|v_n-v|\ge\delta\}
\]
up to null sets. First let \(n\to\infty\), then \(\delta\downarrow0\).
Thus the negative-set indicators converge in \(L^1\). Apply this to \(V_{\mu_A}\), whose zero set consists of two points. Since all negative sets are contained in \((-2,2)\),
\[
 |E_{\nu_n}|\longrightarrow|E_{\mu_A}|.
\]
The polynomial \(f_n(x)=\prod_{j=1}^n(x-t_{j,n})\) belongs to \(\mathcal P\), and \(E_{f_n}=E_{\nu_n}\).

Choose \(A_m\downarrow A_*\), and for each \(m\) select one empirical approximation whose length error is below \(1/m\). Equations (14.5) and the last convergence produce a sequence of finite monic polynomials with lengths tending to \(L\). Combined with (14.1), this proves the exact infimum and its nonattainment, using the verified numerical obligations and stated external mathematical inputs.

The positive-platform step is essential. At \(\mu_{A_*}\), a positive-length interval has potential zero. Direct empirical approximation at that measure does not itself control the lengths of negative sets from above. This proof neither assumes such continuity nor changes the strict inequality at the zero platform.

## 15. The supremum, with its separate attribution boundary

Tao's Theorem 2.1 in [T] states the upper extremal result and equality classification for probabilities supported in an interval of length two. Apply it to \(U_\mu=-V_\mu\). It gives \(|E_f|\le2\sqrt2\), with equality measure
\((\delta_{-1}+\delta_1)/2\). An empirical measure equals this probability precisely when its degree is \(2m\) and each endpoint occurs \(m\) times. The corresponding monic polynomial is \((x^2-1)^m\).

Conversely,
\[
 \{|x^2-1|<1\}=(-\sqrt2,0)\cup(0,\sqrt2)
\]
has length \(2\sqrt2\). The omitted point zero matters for the exact set notation but not its length.

This upper theorem is an attributed external input. Neither the present lower reconstruction nor the independently reconstructed lower certificates reproduce Tao's full upper proof or any optional source upper-scalar computation.

## 16. Evidence, review scope, and limits of the deliverable

The mathematical implication chain is:
\[
\begin{gathered}
 \text{finite atomization and normalization}
 \ \Longrightarrow\ \text{small-}k\text{ proof or block calibration},\\
 \text{convex support}+\text{corrected adjoint}+\text{circle theorem}
 \ \Longrightarrow\ (8.1),\\
 \text{obligation A}\ \Longrightarrow\ \text{unique family minimum }L
 \text{ and terminal }C_{\mathrm{eff}}\le0,\\
 \text{accepted fixed upper bound (or raw A enclosure)}
 \ \Longrightarrow\ L<T,\\
 \text{obligation B with exact covers}
 \ \Longrightarrow\ |E_f|>L,\\
 \text{positive-platform empirical recovery}
 \ \Longrightarrow\ \inf|E_f|\le L .
\end{gathered}
\]
Tao's upper-extremum theorem is a separate branch.

Available local evidence now includes the frozen obligation A integer certificate and float-free normal/-O/-OO replay receipts; the obligation B full finite and terminal result records and matching normal/-O/-OO reruns; the independent kernel audit; and an end-to-end review that independently recomputed obligation A and **all** obligation B finite/terminal slabs, obtaining byte-identical results. That end-to-end review accepted its scoped finite-polynomial conclusion. A separate adversarial analytic challenge subsequently completed with no blocking defect found. It accepted the implication from the explicitly stated certificate/reference assumptions to the finite strict lower bound and recovery; it did not itself execute or reaccept the numerical certificates. The full end-to-end recomputations discharge those numerical assumptions. The combined evidence has therefore been accepted for the finite-polynomial theorem, with the external inputs and scope restrictions retained. This local draft is not a claim of journal, community, or problem-site acceptance.

The independently authored code and complete certificates have not been supplied as part of this exposition or publicly released by this task. A third party can implement the algorithms specified above, but cannot replay the omitted exact local records from a file hash alone. Before advertising a public executable replay, the permitted public inventory, actual program/record availability, usage instructions, and fresh reproduction must be checked separately. The earlier public fixed-candidate report already contains its rational witnesses; the new complete global record does not thereby become public.

No author numerical verifier or linked Lean development was executed. No source PDF, copied source text, dataset content, private coordination material, Git change, PR action, or queue mutation was produced by this drafting task. The mathematical method is conventional mathematical reasoning with AI-assisted review; it is unrefereed, with no external human peer review or formal proof-assistant certification.

Neither completed mathematical review identifies a remaining blocking gap for the original finite-polynomial theorem. The separate challenge explicitly tested contact, coalescing roots, discontinuous quantile velocities, endpoint corrections, tiny positive block masses, the full circle normalization, and zero-platform recovery. Its six floating diagnostics were corroborative only and are not numerical certificates. No pending mathematical gate is identified within this accepted scope; public release and executable-reproduction claims still require their own correctly scoped preparation. The source remains a public proposal, and the stronger original Certificate 7.1 margin figures and source slab counts are not accepted claims of this reconstruction.

## References and publicly identifiable source versions

- **[EHP]** P. Erdős, F. Herzog, and G. Piranian, *Metric properties of polynomials* (1958), original Problem 1, printed page 131. [Primary PDF](https://users.renyi.hu/~p_erdos/1958-05.pdf). Retained PDF: 4,304,732 bytes; SHA-256 5d20ad770563e425ac3343e31581859a24facabf744f10489b8f8d201b0ec12a.
- **[W]** Shouqiao Wang, *A Proposed Complete Solution to Erdős Problem 1038*. [Manuscript](https://multiscalar.ai/results/erdos-1038/paper.pdf); [public result page](https://multiscalar.ai/results/erdos-1038/). Retained PDF: 488,289 bytes; SHA-256 3a7e857b12e59f24af17f36a30030b0ad6368c2d59955ef58e643400917565ad. The public page still stated “Proposed” when checked on 2026-10-12. The construction and reductions are attributed to this manuscript and its Tao/EHP antecedents.
- **[T]** Terence Tao, *Superlevel sets of logarithmic potentials*, December 27, 2025. [Primary PDF](https://terrytao.wordpress.com/wp-content/uploads/2025/12/erdos-1038-2.pdf). Retained PDF: 359,077 bytes; SHA-256 7ef1d231d1689873bafba3bbe5e70710bc605eee245d71614f3abd0917824d41. Theorem 2.1 is the external supremum input; Section 4 develops the underlying one-cut construction.
- **[CI]** Michael Christ and Marina Iliopoulou, *Inequalities of Riesz-Sobolev type for compact connected Abelian groups*, Theorem 1.1 and equation (1.3), with Theorem 1.5 as an alternative formulation. [Primary author/publisher-hosted PDF](https://preprint.press.jhu.edu/ajm/sites/default/files/AJM-christ-iliop.pdf), edited March 12, 2021. Retrieved PDF: 548,600 bytes; SHA-256 40bd076e6f40ce4b907520f095ffc853ba117e0ddb2999c50e4199bcaf1aeab3.
- **[U]** Independently authored accepted fixed-candidate upper-bound report, [draft PR 1310](https://github.com/AlecKriebel/Math/pull/1310), frozen publication commit 845701107993994ce9d56a93164535bcb9b33874. Its scope is the one-sided fixed-candidate bound and recovery; it is not a prior global acceptance.
- Standard external tools additionally used are Lagrange inversion, Pringsheim's positive-coefficient singularity theorem, real and analytic implicit-function theorems, Cauchy estimates, elementary Fourier/Poisson identities, and the usual Fubini, Tonelli, dominated-convergence, and monotone-convergence theorems. Their application hypotheses are specified at the points of use.
