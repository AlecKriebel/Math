# Variational state accuracy does not alone control adjoint accuracy

**Status: unresolved original target; one scoped obstruction; independent review pending.** This note separates a known cotangent-lift criterion from the extra regularity needed to transfer approximation order. It gives an explicit regular, translation-invariant discrete-Lagrangian family whose state map has uniform second-order accuracy but whose adjoints have a nonvanishing error. The family is smooth for each positive step size and deliberately lacks a uniform smooth expansion through zero step size. It is therefore **not asserted to refute the intended question for conventional smooth families of variational integrators**. No novelty claim is made.

## 1. Exact source and established scope

Sina Ober-Blöbaum's contribution to [OWR12/2015](https://publications.mfo.de/bitstream/handle/mfo/3459/OWR_2015_12.pdf?isAllowed=y&sequence=1), printed pp.631–633, considers forced Euler–Lagrange dynamics, their discrete Lagrange–d'Alembert formulation, and a running-plus-terminal optimal-control objective. On p.632 it asks about commutation of discretization and optimization for general classes of variational integrators. The preceding result concerns particular symplectic schemes, their discrete adjoints, and preservation of approximation order. The paragraph does not specify a complete universal scheme class or a complete list of step-size and optimal-control regularity assumptions.

[Campos–Ober-Blöbaum–Trélat (2015)](https://www.ljll.fr/~trelat/fichiers/CamposOberBlobaumTrelat_DCDS2015.pdf), Theorem5.2, proves commutation for a specified convergent symplectic Galerkin discretization, with positive quadrature weights, regularity/coercivity/uniqueness assumptions, and a positive control Hamiltonian Hessian. Its conclusion retains the general-method question and separately discusses nonsmooth constrained controls and abnormal minimizers. It also explicitly leaves a convergence proof for the adjoint variables to future work; the formal matching of schemes must not silently be promoted to an unconditional boundary-value convergence theorem.

A newer relevant theorem is [Tran–Southworth–Leok (2024)](https://doi.org/10.1007/s00332-024-10071-1), Theorem3.3: the discrete adjoint of a one-step state map is its cotangent lift. That theorem characterizes exact commutation with this selected adjoint discretization. Proposition3.3 transfers the state order under variational equivariance and regularity of sensitivities and terminal cost. **Being derived from a discrete mechanical action is not the definition of variational equivariance.** The latter says that taking the tangent variation commutes with applying the numerical method.

The [2026 control-Lagrangian paper](https://doi.org/10.1007/s11044-025-10138-1), Theorem3.7 and Proposition3.8, identifies matching state equations and orders for a specified low-order family. These known results do not identify every preselected variational discretization of an optimal-control problem with the needed adjoint scheme.

In particular, three different assertions must be distinguished:

1. the mechanical state map is symplectic;
2. a chosen state-costate scheme is the cotangent lift, and hence gives exact discrete gradients;
3. those discrete gradients approximate continuous gradients with the same order as the states.

The following calculations concern the missing implication from state accuracy to the third assertion. They do not replace the original classification problem by the second assertion.

## 2. The exact discrete adjoint and a sufficient regularity hypothesis

Let a discrete state equation be

\[
x_{k+1}=\Psi_h(x_k),\qquad x_k\in\mathbb R^m,
\]

and let the objective be a terminal function \(\Phi(x_N)\). Varying the constrained objective, or simply applying the chain rule, gives

\[
\lambda_N=D\Phi(x_N),\qquad
\lambda_k=D\Psi_h(x_k)^T\lambda_{k+1}.\tag{1}
\]

For an invertible derivative this is equivalently the forward cotangent lift
\((x_k,\lambda_k)\mapsto(\Psi_h(x_k),D\Psi_h(x_k)^{-T}\lambda_k)\).
The identity

\[
\lambda_{k+1}^T\delta x_{k+1}=\lambda_k^T\delta x_k
\]

holds for every tangent variation, and conversely determines the adjoint update. This is the finite-dimensional formula in the cited 2024 theorem. Symplecticity of \(\Psi_h\) on a mechanical phase space does not, by itself, bound the error in \(D\Psi_h\).

Here is a standard sufficient estimate, stated to expose precisely what is needed. Let \(\varphi_h\) be the exact time-h state flow. Work on a fixed finite time interval and a compact neighborhood containing the exact and discrete trajectories. Assume, uniformly there,

\[
\|\Psi_h-\varphi_h\|\le Ch^{r+1},\qquad
\|D\Psi_h-D\varphi_h\|\le Ch^{r+1},\tag{2}
\]

\[
\|D\varphi_h\|\le1+Lh,\qquad
\|D\varphi_h(x)-D\varphi_h(y)\|\le Lh\|x-y\|,\tag{3}
\]

for \(r\ge1\), and assume \(D\Phi\) is bounded and Lipschitz on the neighborhood of terminal states. Then the states and the discrete adjoints (1) both have global error \(O(h^r)\), uniformly at mesh points.

**Proof.** The first inequality in (2), together with the derivative bounds, gives the usual recursion
\(e_{k+1}\le(1+L_1h)e_k+Ch^{r+1}\), hence \(e_k=O(h^r)\). Put
\(A_k=D\Psi_h(x_k)\), \(B_k=D\varphi_h(x(t_k))\). Their norms are bounded by \(1+L_1h\), and (2)–(3) imply

\[
\|A_k-B_k\|\le Ch^{r+1}+Lh\,e_k=O(h^{r+1}).
\]

A telescoping expansion of any product from k to N−1 has at most \(N=O(h^{-1})\) terms; the other matrix factors have uniformly bounded products. Thus the discrete and exact solution-sensitivity matrices differ by \(O(h^r)\). Applying their transposes to terminal gradients and using the Lipschitz bound on \(D\Phi\) proves the assertion. ∎

This is a conditional sensitivity estimate, not a new general commutation theorem. Running costs can be included by augmenting the state with the accumulated cost, provided the same derivative estimates hold for the augmented discretization. To transfer a residual estimate to convergence of an optimal control, additional control-derivative estimates and stability of the optimality system are needed. They are not consequences of a state-only estimate (2) without its derivative inequality.

## 3. A regular variational family with second-order states and inconsistent adjoints

Consider the free particle on \(Q=\mathbb R\), with

\[
L(q,v)=\frac12v^2,\qquad H(q,p)=\frac12p^2.
\]

Its exact state flow is \(\varphi_h(q,p)=(q+hp,p)\).
For every \(h>0\), define

\[
F(z)=z\arctan z-\frac12\log(1+z^2),\qquad
K_h(p)=\frac h2p^2+h^5F(p/h^2).\tag{4}
\]

Since \(F'(z)=\arctan z\),

\[
K_h'(p)=hp+h^3\arctan(p/h^2),\qquad
K_h''(p)=h+\frac{h}{1+p^2/h^4}.\tag{5}
\]

In particular, \(h\le K_h''(p)\le2h\), so \(K_h'\) is a smooth increasing bijection of \(\mathbb R\). Let \(P_h(s)\) be its inverse and define the type-I discrete Lagrangian

\[
L_d(q,Q;h)=P_h(Q-q)(Q-q)-K_h(P_h(Q-q)).\tag{6}
\]

This is a global smooth function of \((q,Q)\) for each positive h. Its discrete Legendre relations are

\[
p=-D_1L_d=P_h(Q-q),\qquad P=D_2L_d=P_h(Q-q).
\]

Also
\(D_{12}L_d=-1/K_h''(P_h(Q-q))\ne0\), so the discrete Lagrangian is regular. Its phase-space integrator is exactly

\[
\Psi_h(q,p)=\bigl(q+hp+h^3\arctan(p/h^2),p\bigr).\tag{7}
\]

It is translation invariant in q, preserves momentum p exactly, and is symplectic: its derivative is a shear matrix of determinant one, equivalently \(dQ\wedge dP=dq\wedge dp\). Thus the example is not merely a nonsymplectic state discretization.

### Action consistency and state order

The exact discrete free-particle action is \(L_d^E(q,Q;h)=(Q-q)^2/(2h)\). Put \(Q-q=hv\) and \(p=P_h(hv)\). Equation (5) gives

\[
|p-v|\le\frac\pi2h^2.
\]

The function F is even and satisfies \(0\le F(z)\le(\pi/2)|z|\). Hence

\[
L_d(q,q+hv;h)-\frac h2v^2
=-\frac h2(p-v)^2-h^5F(p/h^2)=O(h^3),\tag{8}
\]

uniformly for bounded velocities. This is a value estimate for the discrete action, with no derivative estimate inferred from it.

For a fixed horizon \(T=Nh\), iteration of (7) is explicit:

\[
p_N=p_0,\qquad
q_N=q_0+Tp_0+Th^2\arctan(p_0/h^2).\tag{9}
\]

Thus the global state error is at most \((\pi/2)Th^2\), uniformly in the initial state. The same bound with \(t_k\) in place of T applies at every mesh point. For fixed \(p_0\ne0\), division of the error by \(h^2\) tends to \((\pi/2)T\operatorname{sgn}(p_0)\), so the order is genuinely two.

### An adjoint error that does not tend to zero

Differentiate (9):

\[
D\Psi_h^N(q_0,p_0)=
\begin{pmatrix}
1&T+\dfrac{T}{1+p_0^2/h^4}\\
0&1
\end{pmatrix}.
\tag{10}
\]

The exact sensitivity is \(\bigl(\begin{smallmatrix}1&T\\0&1\end{smallmatrix}\bigr)\). At \(p_0=0\), their upper-right entries are 2T and T for every h. Therefore the state maps converge uniformly with order two while their derivatives do not converge at this initial momentum.

Take the smooth bounded-below terminal objective

\[
\Phi(q,p)=q+\frac12(q^2+p^2).
\]

Starting at \((q_0,p_0)=(0,0)\), both exact and discrete states remain zero, and the common terminal covector is \(D\Phi(0,0)=(1,0)\). Formula (1) and (10) give initial discrete covector \((1,2T)\), whereas the exact adjoint gives \((1,T)\). More generally, at time \(t_k\) the two costates are

\[
\lambda_k=(1,2(T-t_k)),\qquad
\lambda(t_k)=(1,T-t_k).\tag{11}
\]

The discrepancy at time zero is exactly T in the second component and never decreases with refinement. This is an exact analytic obstruction, not a numerical slope estimate.

It can be embedded in a minimal optimal-control problem with fixed initial state, force \(f(q,v,u)\equiv0\), control \(u\in\mathbb R\), running cost \(u^2/2\), and the preceding terminal objective. The unique optimum is \(u\equiv0\); the states are fixed by the initial condition. Use zero discrete forces and the cost \(\sum_k h u_k^2/2+\Phi(x_N)\). The unique discrete optimum also has all controls zero, the state-constraint Jacobian has full row rank, and its KKT costates are (11). The example is deliberately unactuated: it isolates costate consistency, and makes no claim that the primal optimal control fails to converge.

## 4. Why this is a scoped obstruction rather than a full source resolution

The failure is concentrated in step-size-dependent momentum scales. If
\(R_h(p)=h^3\arctan(p/h^2)\), then

\[
\partial_pR_h(p)=\frac{h}{1+p^2/h^4},\qquad
\partial_p^2R_h(p)=\frac{-2p/h^3}{(1+p^2/h^4)^2}.
\]

Along \(p=h^2\), the second derivative is \(-1/(2h)\). There is no jointly smooth extension through \((h,p)=(0,0)\) and no uniform smooth error expansion that can be differentiated without losing the stated order. In particular the derivative part of (2) fails: the local derivative discrepancy at zero momentum is h, despite a uniform local state discrepancy bounded by \((\pi/2)h^3\).

This qualification matters. Standard variational error analyses use regularity of a desingularized family and its variations; see [Patrick–Cuell (2009)](https://arxiv.org/abs/0807.1516), especially the treatment of the zero-step singularity and the smooth discrete variational data. The present family is not offered as a counterexample to those theorems, to the 2015 spRK/sG result, or to the 2024 variational-equivariance theorem.

The remaining target is to prove a same-order comparison for a precisely specified conventional class, including consistent cost and force/control discretization and stable optimality conditions, or find a counterexample **within that class**. A proof still needs to establish the necessary derivative estimates or identify a suitable variationally equivariant lifted scheme; calling the mechanical state map symplectic is insufficient. Smooth constrained or nonsmooth optimal controls introduce additional separate issues already identified by the primary sources.

Accordingly the original record remains **unsolved, 1/5 attempts**. The established partial result is the explicit failure of the weaker implication “positive-step smooth regular variational family + second-order state accuracy implies same-order adjoint accuracy.” The supplied verifier checks exact rational sensitivity, symplectic and KKT identities at bounded sample parameters. These controls supplement the complete formulas above; they do not establish a general scheme classification.
