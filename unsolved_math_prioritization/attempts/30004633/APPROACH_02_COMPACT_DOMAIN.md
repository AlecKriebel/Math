# Approach 2: compact-domain Barenblatt convergence by a signed-pressure cutoff

**Problem:** 30004633 / OWR-4990379-003. **Author continuation:** 2 of the required 5 approaches. **Status:** independently derived candidate proof, awaiting independent review. This is new work, not a recovery, reproduction, or acceptance of the historical first-approach packet.

## 1. Scope and primary-source check

The exact OWR question concerns convergence of the Moreau–Yosida Lagrangian particle scheme for less regular porous-medium solutions, particularly a moving Barenblatt free boundary. The report fixes a compact physical domain and freezes a proximal map on each time interval. Its open question is on printed p. 522. [OWR 10/2021](https://ems.press/content/serial-article-files/46885), DOI [10.4171/OWR/2021/10](https://doi.org/10.4171/OWR/2021/10).

The corresponding primary paper is Gallouët–Mérigot–Natale, [arXiv:2105.12605v2](https://arxiv.org/abs/2105.12605v2), DOI [10.1137/21M1422756](https://doi.org/10.1137/21M1422756). Its equations (1.17), (1.21) define the frozen scheme, Theorem 1.2 uses smooth velocity, and §6 explicitly places its Barenblatt experiment outside its theorem. The arXiv identifier 2106.08084 in the supplied corpus is unrelated to this scheme.

Natale's later [arXiv:2304.05069v2](https://arxiv.org/abs/2304.05069v2), §4.2.1, likewise excludes its Barenblatt example from its convergence theorem. It is a different interacting-cell discretization and is not substituted for the original scheme below.

The result here concerns the **original compact-domain frozen scheme**, in every dimension and for every exponent m>1, for positive-time Barenblatt data with its support separated from the physical wall. It does not treat arbitrary irregular weak solutions, initial Dirac data at time zero, a support striking the wall, or Euler dynamics. It therefore resolves a concrete free-boundary subclass, not every reading of the general open problem.

## 2. Statement

Let d≥1, m>1, 0<t0<T. Set

\[
\beta=(d(m-1)+2)^{-1},\qquad \lambda=d\beta(m-1)=1-2\beta.
\]

Choose A>0 so that

\[
q_0(t,x)=A t^{-\lambda}-{\beta\over2t}|x|^2,\qquad
\rho(t,x)=\left({m-1\over m}(q_0(t,x))_+\right)^{1/(m-1)}
\tag{2.1}
\]

has mass one. Its support radius R(t) is determined by R(t)^2=2A t^{2\beta}/\beta. Translation of its center is allowed.

As in GMN §1 and the opening paragraph of §4, the particle positions take values in Rᵈ and are not required to remain in M. Only finite-energy reconstructed densities are constrained to M. GMN explicitly discusses particles outside M. No convexity assumption is imposed here or used below.

Let Ω be a bounded open Lipschitz domain with

\[
\overline{B_{R_*}(0)}\subset\Omega,\qquad R_*>R(T).
\tag{2.2}
\]

Write M=closure(Ω). Put ρ0=ρ(t0), H=L²(ρ0;Rᵈ), and partition the initial support into measurable sets P_i of positive ρ0-mass. Let H_N be the functions constant on these sets and Π_N the orthogonal projection. Define

\[
X_N(t_0)=\Pi_N\mathrm{Id},\qquad
\delta_N^2=\|\Pi_N\mathrm{Id}-\mathrm{Id}\|_H^2,
\]

\[
\mathcal F(Y)=\begin{cases}\displaystyle{1\over m-1}\int_\Omega r^m,&Y_\#\rho_0=r\,dx\text{ supported in }M,\\+\infty,&\text{otherwise},\end{cases}
\quad
\mathcal F_\varepsilon(X)=\inf_Y\left\{{\|X-Y\|_H^2\over2\varepsilon}+\mathcal F(Y)\right\}.
\]

At nodes t_n, of successive spacings at most τ, choose **any** minimizer Y_n of the expression defining F_ε(X_N(t_n)). On each interval solve exactly

\[
\dot X_N(t)={\Pi_NY_n-X_N(t)\over\varepsilon}.
\tag{2.3}
\]

This is the original frozen-proximal time discretization, not JKO and not an implicit particle minimization. In particular

\[
X_N(t)=e^{-(t-t_n)/\varepsilon}X_N(t_n)
 +(1-e^{-(t-t_n)/\varepsilon})\Pi_NY_n.
\]

There is a C depending on d,m,t0,T,A and the chosen physical-wall clearance, but not on N, ε, τ or the proximal selections, such that, for 0<ε≤1 and 0<τ≤ε,

\[
\sup_{t_0\le t\le T}\|X_N(t)-X(t)\|_H^2
 +\int_{t_0}^T\|\dot X_N(t)-\dot X(t)\|_H^2\,dt
 \le C\left({\delta_N^2\over\varepsilon}+\varepsilon+{\tau\over\varepsilon}\right),
\tag{2.4}
\]

where X(t,a)=(t/t0)^β a is the exact material flow. Consequently convergence holds if ε→0, δ_N²/ε→0 and τ/ε→0.

The reconstructed densities r_n=(Y_n)#ρ0 also converge uniformly in time in W₂ to ρ(t) when r_n is used on [t_n,t_{n+1}). Their signed relative energies tend uniformly to zero. The estimate compares material velocities. It does **not** assert the same error bound for evaluating the discontinuous zero-extended physical velocity at the particle positions.

## 3. Proximal existence and the exact admissible variation

Existence does not require differentiability or uniqueness of the Lagrangian minimizer. If X=∑x_i 1_{P_i} and w_i=ρ0(P_i), minimize instead over nonnegative subdensities r_i of mass w_i:

\[
\sum_i\int_\Omega {|x_i-y|^2\over2\varepsilon}r_i(y)\,dy
 +{1\over m-1}\int_\Omega\Big(\sum_i r_i\Big)^m\,dy.
\tag{3.1}
\]

A finite competitor exists, for example r_i=w_i/|Ω|. A bounded minimizing sequence is weakly bounded in the finite product of Lᵐ(Ω), since 0≤r_i≤∑r_j. Positivity and mass constraints are weakly closed, the cost is weakly continuous on bounded Ω, and the integral is weakly lower semicontinuous. Thus a minimizer exists. Each atomless source measure ρ0 restricted to P_i can be mapped measurably to r_i dy of the same mass. Combining those maps realizes (3.1) in H. Conversely every admissible map decomposes this way. This proves equality with the Lagrangian problem and attainment. The standard atomless transport fact can also be obtained by the existence of a transport map from an absolutely continuous finite measure to another such measure.

Let Y_n be any minimizer and r_n=(Y_n)#ρ0. For a smooth vector field v supported compactly inside Ω, the maps Id+s v are diffeomorphisms preserving Ω for both signs of sufficiently small s. Varying Y_n by (Id+s v)∘Y_n gives

\[
{1\over\varepsilon}\langle Y_n-X_N(t_n),v(Y_n)\rangle_H
 =\int_\Omega r_n^m\operatorname{div}v\,dx.
\tag{3.2}
\]

Indeed the transport-cost derivative is the scalar product on the left, whereas the energy derivative under this change of variables is −∫r_nᵐ div v. These derivatives are justified by dominated convergence, since r_n∈Lᵐ and the diffeomorphisms have bounded Jacobians. Formula (3.2) neither assumes zero reconstructed pressure on the physical wall nor discards a boundary term. Compact support of v makes the variation admissible.

## 4. Constructing the smooth signed pressure

Choose R(T)<R1<R2<R*. Let χ∈C_c^∞(B_{R2}) be radial, 0≤χ≤1, and χ=1 on B_{R1}. For any κ>0 set

\[
q(t,x)=\chi(x)q_0(t,x)-(1-\chi(x))\kappa,
\qquad u(t,x)=-\nabla q(t,x).
\tag{4.1}
\]

This defines globally smooth functions on [t0,T]×Rᵈ. All spatial derivatives used below, together with ∂_t q and its spatial gradient, are uniformly bounded. The field u is compactly supported inside Ω. Also q_+=q_{0,+}, hence ρ in (2.1) equals ((m−1)q_+/m)^{1/(m−1)}.

Inside B_{R1}, direct differentiation using λ=dβ(m−1) and λ+2β=1 gives

\[
\partial_tq_0-|\nabla q_0|^2+(m-1)q_0\operatorname{div}(-\nabla q_0)=0.
\tag{4.2}
\]

Define the residual

\[
\mathcal R=\partial_tq-|u|^2+(m-1)q\operatorname{div}u.
\tag{4.3}
\]

It vanishes inside B_{R1} and outside B_{R2}. On the remaining compact annulus, q0 is uniformly negative over [t0,T], because R1>R(T). Thus there is η>0 such that q≤−η on the entire annulus. In particular

\[
|\mathcal R|\le C_R(-q)\mathbf1_{\{q<0\}}.
\tag{4.4}
\]

The actual density satisfies ∂_tρ+div(ρu)=0 distributionally, with flow X(t,a)=(t/t0)^βa on its mass-carrying support. This follows either directly from (2.1) or by change of variables under X. Its flux has compact support inside Ω, so it is a no-flux compact-domain solution. Its physical pressure is q_+, whose spatial gradient jumps at the moving free boundary; no global differentiability of that physical pressure is assumed.

Put P(t)=∫Ωρ(t)^m. Two identities needed below are

\[
P'(t)=\int_\Omega\rho\,\partial_tq\,dx
 =-(m-1)\int_\Omega\rho^m\operatorname{div}u\,dx.
\tag{4.5}
\]

The first follows from differentiating the C¹ function c(q_+)^{m/(m−1)}; its derivative is ρ. For the second, the explicit scaling gives P(t)=P(t0)(t/t0)^{-λ}, while div u=dβ/t on the support. These identities are valid for every m>1.

## 5. Signed relative energy and stepwise dissipation

For r≥0 define

\[
e(t,x,r)={r^m\over m-1}-q(t,x)r+\rho(t,x)^m.
\tag{5.1}
\]

Fenchel's inequality, or direct minimization in r, gives e≥0. Where q<0, ρ=0 and e≥(−q)r. Thus (4.4) implies

\[
\left|\int r\mathcal R\right|\le C_R\int e(t,x,r).
\tag{5.2}
\]

Write X=X_N(t), V=dot X_N(t), Y=Y_n, and r=r_n on a time interval. Define

\[
A_n(t)={\|X-Y\|_H^2\over2\varepsilon},\qquad
E_n(t)=\int_\Omega e(t,x,r_n(x))\,dx,
\]

\[
Z_n(t)=A_n(t)+\mathcal F(Y_n)-\int q(t,X)\,d\rho_0+P(t).
\tag{5.3}
\]

If Q=sup|∇q|, the identity

\[
Z_n=A_n+E_n+\int[q(t,Y_n)-q(t,X)]\,d\rho_0
\]

and Q||X−Y||≤||X−Y||²/(4ε)+εQ² give

\[
Z_n\ge\tfrac12 A_n+E_n-\varepsilon Q^2.
\tag{5.4}
\]

Thus W_n=Z_n+(Q²+1)ε is nonnegative and A_n+E_n≤2W_n.

Let f_n=F_ε(X_N(t_n)). The frozen energy satisfies

\[
{d\over dt}[A_n+\mathcal F(Y_n)]=-\|V\|_H^2,
\quad f_{n+1}\le A_n(t_{n+1})+\mathcal F(Y_n)\le f_n.
\tag{5.5}
\]

Consequently Δ_n=f_n−f_{n+1}≥0, ∫_{t_n}^{t_{n+1}}||V||²≤Δ_n, and ∑Δ_n≤f_0. At every node Z, and therefore W, jumps downward or remains unchanged, because the cross term and P are continuous while the new proximal minimization can only decrease the frozen energy.

## 6. Exact differential calculation, including the frozen-step defect

Set D_n(t)=||V−u(t,X)||²_H. Differentiating (5.3) gives the exact identity

\[
Z_n'+D_n=-\langle V,u(t,X)\rangle_H
 +\int[|u(t,X)|^2-\partial_tq(t,X)]\,d\rho_0+P'(t).
\tag{6.1}
\]

Since u(t,X) is constant on every P_i and V=(Π_NY−X)/ε,

\[
-\langle V,u(X)\rangle
 ={\langle X-Y,u(X)\rangle\over\varepsilon}
 =-\int r^m\operatorname{div}u
 +F_n^{\rm freeze}+C_n^{\rm space},
\tag{6.2}
\]

where (3.2) has been applied to v=u(t,·), and

\[
F_n^{\rm freeze}={\langle X-X_N(t_n),u(t,Y)\rangle\over\varepsilon},
\qquad
C_n^{\rm space}={\langle X-Y,u(t,X)-u(t,Y)\rangle\over\varepsilon}.
\tag{6.3}
\]

With L=sup Lip(u), one has C_n^{space}≤2LA_n. Put g=|u|²−∂_tq and G=sup Lip(g). Moving its evaluation from X to Y costs at most

\[
\left|\int[g(t,X)-g(t,Y)]\,d\rho_0\right|
 \le G\|X-Y\|_H\le A_n+\tfrac12\varepsilon G^2.
\tag{6.4}
\]

Using (4.3), (4.5), and rᵐ=(m−1)U(r), all the remaining terms combine **exactly** as

\[
-\int r^m\operatorname{div}u+\int r(|u|^2-\partial_tq)+P'
 =-(m-1)\int e(t,x,r)\operatorname{div}u-\int r\mathcal R.
\tag{6.5}
\]

This algebra is the vacuum cancellation. Replacing q by q_+ at this point would destroy the smoothness used in (6.4).

Finally, writing X(t)−X(t_n)=∫_{t_n}^tV(s)ds and U∞=sup|u|, Young's inequality gives

\[
|F_n^{\rm freeze}(t)|
 \le {1\over2\varepsilon}\int_{t_n}^t[\|V(s)\|_H^2+U_\infty^2]\,ds
 \le {\Delta_n+\tau U_\infty^2\over2\varepsilon}.
\tag{6.6}
\]

Combining (5.2), (5.4), and (6.1)–(6.6), with constants uniform over the finite interval,

\[
W_n'+D_n\le C W_n+C\varepsilon
 +{\Delta_n+\tau U_\infty^2\over2\varepsilon}.
\tag{6.7}
\]

At nodes W jumps downward. Piecewise Grönwall and summing (6.6) over intervals of length at most τ therefore yield

\[
\sup_tW(t)+\int_{t_0}^TD(t)dt
 \le C\left(W(t_0)+\varepsilon+{\tau\over\varepsilon}(1+f_0)\right).
\tag{6.8}
\]

One obtains the bound for the unweighted integral of D either by the integrating factor or by integrating (6.7) after the uniform W bound. For a final partial interval the same argument uses its actual length; no equal-mesh assumption is required.

## 7. Initialization and material-flow error

Using Id as a proximal competitor,

\[
f_0\le {\delta_N^2\over2\varepsilon}+\mathcal F(\mathrm{Id}).
\tag{7.1}
\]

Since U(ρ0)−q(t0)ρ0+ρ0ᵐ=0 pointwise,

\[
Z(t_0)\le {\delta_N^2\over2\varepsilon}
 +\int[q(t_0,a)-q(t_0,\Pi_Na)]\rho_0(a)\,da.
\]

Taylor expansion around each cell barycenter makes the linear term integrate to zero. A bounded global Hessian of q gives

\[
W(t_0)\le {\delta_N^2\over2\varepsilon}+C\delta_N^2+C\varepsilon.
\tag{7.2}
\]

Thus (6.8) yields, without a coupling assumption on δ_N,

\[
\sup_tW(t)+\int D\le C\left[(1+\tau/\varepsilon){\delta_N^2\over\varepsilon}
 +\delta_N^2+\varepsilon+\tau/\varepsilon\right].
\tag{7.3}
\]

For ε≤1 and τ≤ε this is bounded by the right side of (2.4).

Let B=X_N−X_exact. Because dot X_exact=u(t,X_exact) for ρ0-almost every label and u is globally Lipschitz,

\[
{d\over dt}\|B\|_H^2
 \le D(t)+(1+2L)\|B\|_H^2,\qquad \|B(t_0)\|_H^2=\delta_N^2.
\]

Grönwall proves the flow part of (2.4). Furthermore

\[
\|\dot X_N-\dot X_{exact}\|_H^2
 \le 2D(t)+2L^2\|B(t)\|_H^2,
\]

which proves its material-velocity part.

For the reconstructed density, use the common-label coupling:

\[
W_2(r_n,\rho(t))\le\|Y_n-X_N(t)\|_H+\|X_N(t)-X_{exact}(t)\|_H.
\]

The first squared term is 2εA_n≤4εW_n, and the second is already controlled. Also E_n≤2W_n, proving the stated relative-energy convergence. No assumption has been made that Y_n, its density, or the particles avoid the physical wall.

## 8. Limitations and review targets

1. This result requires positive starting time and fixed positive clearance of the target support from the physical wall. Constants may diverge as either is lost.
2. It is a conditional convergence estimate for the exactly minimized, exactly integrated frozen scheme. Numerical solver errors require additional estimates.
3. The smooth velocity u in vacuum is an auxiliary extension. Material-flow and material-velocity convergence are asserted; an identical quantitative estimate for the discontinuous physical-velocity evaluation at particles is not asserted.
4. No sharpness claim is made for the rate or the scale conditions.
5. No claim is made that the historically missing first-approach files have been recovered, matched, or audited.
6. The independent review should check the sign in (3.2), the pressure identity (4.5), the cancellation (6.5), the frozen defect (6.6), the node jumps, and the compatibility of the cutoff with the actual compact-domain minimization.

The constructive proof is new author work. Source descriptions above establish which problem and scheme are being addressed; they do not certify this theorem.
