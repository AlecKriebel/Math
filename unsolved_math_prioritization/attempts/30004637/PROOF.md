# Branching Brownian RUOT: provable computational components and remaining gap

**Problem 30004637 / OWR-4990379-007; rank 560. Status: partial, unresolved.**

This note does not give a general fast solver for the question posed by Aymeric
Baradat, joint work with Hugo Lavenant, in Oberwolfach Report 10/2021, §3.2,
printed p. 555. It supplies five explicitly bounded approaches, complete proofs
of the claims below, and small reproducible checks. None is presented as a new
resolution, an impossibility theorem for fast algorithms, or a novelty claim.

## 1. Exact target and conventions

The source asks: “Is it nevertheless possible to design a fast algorithm doing
the job?” The job is the minimization, for prescribed finite nonnegative measures
on the torus, of

\[
 \int_0^1\!\int_{\mathbb T^d}
       \bigl(\tfrac12|v|^2+\Psi(r)\bigr)\,d\rho_t\,dt,
 \qquad
 \partial_t\rho+\operatorname{div}(\rho v)
       =\tfrac\nu2\Delta\rho+r\rho,
 \quad \rho(0)=\rho_0,\quad\rho(1)=\rho_1,
\]

where \(\nu,\lambda>0\), \(p_k\ge0\), \(\sum p_k=1\), and

\[
 H(s):=\Psi^*(s)=\nu\lambda\sum_{k\ge0}p_k
             (e^{(k-1)s/\nu}-1).
\]

The source does not prescribe an input representation, accuracy criterion,
complexity bound, or a uniform regime in \(\nu,\lambda,p\). It includes general
endpoint measures and offspring laws, not merely a positive finite grid.
Fixing such a grid or replacing \(\Psi\) by a quadratic is a restriction or a
change of model. In particular, the static entropy-penalized unbalanced
transport problem solved by generalized Sinkhorn is not automatically this
problem.

Except in Approach I, the explicit scalar calculations use **critical binary
branching** \(p_0=p_2=1/2\), for which

\[
 H(s)=\nu\lambda(\cosh(s/\nu)-1),\qquad
 \Psi(r)=\nu\{r\operatorname{arsinh}(r/\lambda)
             -\sqrt{\lambda^2+r^2}+\lambda\}.                 \tag{1}
\]

These parameters use the OWR variance-rate convention \(\nu\), not a diffusion
standard deviation. Formula (1) follows by the unique maximizer
\(s=\nu\operatorname{arsinh}(r/\lambda)\) in the Legendre transform. In
particular

\[
 \Psi'(r)=\nu\operatorname{arsinh}(r/\lambda),\qquad
 \Psi''(r)=\nu/\sqrt{\lambda^2+r^2}>0.                        \tag{2}
\]

## 2. Approach I: direct endpoint scaling fails even in a scalar model

Take the allowed pure-birth mechanism \(p_2=1\), and ignore spatial location by
using a constant terminal test function. Starting from one particle, let
\(N_t\) be its number of descendants and \(G_t(s)=\mathbb E[s^{N_t}]\).
For \(0<s<1\), conditioning on the first infinitesimal branching event and
using independence of the two descendant families gives

\[
 \partial_tG_t=\lambda(G_t^2-G_t),\quad G_0=s,
 \qquad G_t(s)=\frac{e^{-\lambda t}s}
 {1-(1-e^{-\lambda t})s}.                                  \tag{3}
\]

The displayed expression solves the ODE and initial condition, and uniqueness
holds on this bounded range. Writing \(q=e^{-\lambda t}\), direct differentiation
yields, for \(t>0\),

\[
 G_t''(s)=\frac{2q(1-q)}{(1-(1-q)s)^3}>0.                    \tag{4}
\]

A fixed linear integral operator applied to constant input \(s\) is linear in
\(s\); (4) rules out that representation for this branching propagation. Thus
the unchanged Brownian heat-kernel multiplication step cannot evaluate the
branching endpoint transform. This proves only a failure of that particular
transfer of Sinkhorn. Nonlinear updates, a different representation, or other
fast algorithms are not ruled out.

**Gap.** A useful nonlinear endpoint update still needs evaluation of the
branching semigroup, quantitative convergence, and a controlled approximation
scheme. Giving the update the exact semigroup as an oracle relocates the hard
part rather than solves it.

## 3. Approach II: a fully justified binary local proximal operation

For \(\rho>0\), \(m\in\mathbb R^d\), \(z\in\mathbb R\), set

\[
 f(\rho,m,z)=\frac{|m|^2}{2\rho}+\rho\Psi(z/\rho).
\]

Extend by \(f(0,0,0)=0\), and by \(+\infty\) at all other points with
\(\rho\le0\). This is the closed convex perspective, since \(\Psi\) is convex
and superlinear. Equivalently, the following direct support-function argument
also verifies the closure at vacuum. Define

\[
 K=\{(a,b,c):a+|b|^2/2+H(c)\le0\}.
\]

For \(\rho>0\), first maximizing \(a\rho+b\cdot m+cz\) over \(a\), then
\(b,c\), gives \(f\). At \(\rho=0\), \(b\) and \(c\) can be arbitrary
by making \(a\) negative enough, so the supremum is zero precisely when
\(m=z=0\). At \(\rho<0\) the supremum is infinite by \(a\to-\infty\).
Consequently \(f\) is the support function of \(K\). Directly computing its
conjugate gives \(\sup_{\rho>0}\rho(a+|b|^2/2+H(c))\), together with zero
from the origin; thus \(f^*=\iota_K\) as claimed.

### Proposition 1 (projection reduced to monotone scalar equations)

Given \(x=(a,b,c)\), if \(x\in K\) its Euclidean projection is \(x\). Otherwise
put \(h_0=a+|b|^2/2+H(c)>0\). For \(\tau\ge0\), let \(c_\tau\) be the
unique solution of

\[
 c_\tau+\tau H'(c_\tau)=c,
 \qquad H'(u)=\lambda\sinh(u/\nu).                          \tag{5}
\]

There is a unique \(\tau_*\in(0,h_0]\) for which

\[
 h(\tau):=a-\tau+\frac{|b|^2}{2(1+\tau)^2}+H(c_\tau)=0.     \tag{6}
\]

The projection is

\[
 P_Kx=(a-\tau_*,\ b/(1+\tau_*),\ c_{\tau_*}).               \tag{7}
\]

**Proof.** The left side of (5) is continuous, strictly increasing with derivative
\(1+\tau H''\ge1\), and has limits of opposite signs at infinity. Its root is
between \(0\) and \(c\), with the interval reversed for negative \(c\).
Implicit differentiation gives

\[
 c_\tau'=-\frac{H'(c_\tau)}{1+\tau H''(c_\tau)},\qquad
 \frac{d}{d\tau}H(c_\tau)
       =-\frac{H'(c_\tau)^2}{1+\tau H''(c_\tau)}.            \tag{8}
\]

Thus

\[
 h'(\tau)=-1-\frac{|b|^2}{(1+\tau)^3}
               -\frac{H'(c_\tau)^2}{1+\tau H''(c_\tau)}
          \le-1.                                          \tag{9}
\]

We have \(h(0)=h_0>0\) and \(h(h_0)\le0\), proving existence and uniqueness.
Let \(\bar x\) be (7) and \(g(a,b,c)=a+|b|^2/2+H(c)\). Then \(g(\bar x)=0\)
and \(x-\bar x=\tau_*\nabla g(\bar x)\). Convexity of \(g\) implies
\(\nabla g(\bar x)\cdot(y-\bar x)\le0\) for every \(y\in K\).
Hence \((x-\bar x)\cdot(y-\bar x)\le0\), the sufficient and necessary
Euclidean projection condition, which proves (7). ∎

This independently supplies the details behind the local projection mechanism
in Baradat–Lavenant, arXiv:2111.01666v2, Lemma 6.17. Its printed p. 122 has a
monotonicity-word typo and a missing square in the subsequent derivative;
(8)–(9) are the directly derived formulas used here. This observation concerns
the inspected preprint, not an assertion about corrections in the 2025 book.

Moreau's identity here can be proved without an external theorem. If
\(p=P_K(x/\gamma)\) and \(u=x-\gamma p\), the projection inequality makes
\(p\) attain the support function at \(u\), so \(p\in\partial f(u)\).
Thus \(0\in u-x+\gamma\partial f(u)\), exactly the strictly convex proximal
minimization condition. It follows that

\[
 \operatorname{prox}_{\gamma f}(x)=x-\gamma P_K(x/\gamma).    \tag{10}
\]

In exact real arithmetic, bisection of (6) needs at most
\(\max\{0,\lceil\log_2(h_0/\eta)\rceil\}\) steps to enclose \(\tau_*\) in an interval
of length \(\eta\); each inner equation (5) has the explicit bracket just
proved. The outer count assumes exact inner evaluations. A fully validated nested
implementation needs error bounds for the inner evaluations and sign tests.
These are scalar-operation counts, not bit-complexity estimates.
A pointwise error bound is available: the vector in (7), as a function of
\(\tau\), is Lipschitz with constant at most

\[
 B=\sqrt{1+|b|^2+\lambda^2\sinh^2(|c|/\nu)}.
\]

This follows from (8), \(|c_\tau|\le|c|\), and differentiation of the other
two coordinates. An inner residual \(e\) in (5) bounds its root error by
\(|e|\), since the derivative in (5) is at least one. In particular, small
\(\nu\) and large \(|c|/\nu\) can cause severe conditioning; the bounds are
not uniform. The supplied floating-point tests are regressions, not directed-
rounding interval certificates.

**Gap.** Cheap local proximal evaluations do not bound the number of global
iterations or continuum discretization error. Arbitrary offspring distributions
also require separate domain and evaluation assumptions.

## 4. Approach III: FFT/tridiagonal affine projection on a periodic grid

This section concerns a specified **backward-Euler linear constraint**, not the
centered scheme in the source and not an asserted convergent discretization.
Let \(T\ge1\) be the number of time steps, \(N\ge1\) periodic spatial cells,
\(t=T\), and define

\[
 (Du)_j=N(u_j-u_{j-1}),\quad S=DD^*,\quad E=tI+(\nu/2)S.
\]

Use the Euclidean norm on all arrays. Unknowns are the interior densities
\(\rho_1,\ldots,\rho_{T-1}\), and \(m_n,z_n\in\mathbb R^N\) for
\(1\le n\le T\). End densities \(\rho_0,\rho_T\) are fixed. The constraint is

\[
 E\rho_n-t\rho_{n-1}+Dm_n-z_n=0,\quad 1\le n\le T.         \tag{11}
\]

Move endpoint contributions to a right side \(b\), and call the remaining
matrix \(A\). For \(T>1\), \(b_1=t\rho_0\), \(b_T=-E\rho_T\), with other
rows zero; for \(T=1\), \(b=t\rho_0-E\rho_T\). The \(-I\) block on \(z\)
shows that \(A\) is surjective, regardless of the endpoints.

### Proposition 2 (near-linear affine projection)

For any input array \(x\), its projection onto \(Ax=b\) is

\[
 x-A^*(AA^*)^{-1}(Ax-b).                                    \tag{12}
\]

In the real-arithmetic model, (12) costs \(O(TN\log N+TN)\) operations and
\(O(TN)\) storage, using spatial FFTs and \(N\) positive-definite tridiagonal
systems of size \(T\).

**Proof.** If \(y=(AA^*)^{-1}(Ax-b)\), then (12) is feasible. Its difference
from \(x\) lies in \(\operatorname{range}A^*=(\ker A)^\perp\), proving
orthogonal minimality. Moreover \(AA^*\succeq I\) from the \(z\) block.
The spatial Fourier symbol of \(S\) is
\(\ell_k=4N^2\sin^2(\pi k/N)\). Write \(e_k=t+\nu\ell_k/2\).
After a spatial Fourier transform the matrix \(AA^*\) at frequency \(k\)
is tridiagonal. For \(T>1\) its diagonal entries are

\[
 d_n=1+\ell_k+\mathbf1_{n<T}e_k^2+
                         \mathbf1_{n>1}t^2,
\]

and its neighboring entries are \(-te_k\). For \(T=1\) the matrix is the
scalar \(1+\ell_k\). To verify these formulas, each interior density column
has coefficient \(E\) in row \(n\) and \(-tI\) in row \(n+1\); the momentum
and source columns contribute \(S+I\) on each diagonal block. All other blocks
vanish. Tridiagonal elimination has nonzero positive pivots because these
matrices are positive definite. It takes \(O(T)\) operations per frequency.
The FFT and its inverse cost \(O(TN\log N)\), and applying \(A,A^*\) is
local, of cost \(O(TN)\). This also establishes the storage bound. ∎

The proof includes \(T=1\), \(N=1\), and \(\nu=0\). No matrix inverse needs to
be stored. Positivity of densities is **not** imposed by this affine projection.
Floating-point stability is a different question from the operation count;
for example the elementary bound

\[
 \lambda_{\max}(AA^*)\le(2T+2\nu N^2)^2+4N^2+1
\]

follows from \(\|S\|\le4N^2\). Thus the condition number need not be mesh
independent despite \(\lambda_{\min}\ge1\).

**Gap.** This accelerates one linear operation. A global optimization method,
positivity handling, certified stopping, and approximation of the original
measure problem remain necessary. No claim is made that (11) is the optimal
choice of discretization.

## 5. Approach IV: finite-grid rate and a posteriori certificates

Two precise finite-dimensional facts clarify what a successful full solver
would still need.

### Proposition 3 (restricted positive-domain projected gradient)

Consider \(F(u)=\sum_i w_i f(\rho_i,m_i,z_i)\), with \(w_i>0\), on any nonempty
compact convex set \(C\) contained in

\[
 \delta\le\rho_i\le R,\qquad |m_i|\le M,\qquad |z_i|\le Z,
 \quad \delta>0.
\]

The set may impose affine discretized PDE and boundary constraints. With the
Euclidean norm, a valid gradient Lipschitz constant on \(C\) is

\[
 L=\frac{\max_i w_i}{\delta}
       \left[1+(M/\delta)^2+
                    (\nu/\lambda)(1+(Z/\delta)^2)\right].    \tag{13}
\]

Assume exact projection onto \(C\) is available. Then the iterations
\(u_{n+1}=P_C(u_n-L^{-1}\nabla F(u_n))\), starting at \(u_0\in C\), satisfy

\[
 F(u_n)-\min_C F\le\frac{L\operatorname{diam}(C)^2}{2n},
 \qquad n\ge1.                                             \tag{14}
\]

**Proof.** Write \(v=m/\rho\), \(r=z/\rho\). For a perturbation
\((a,b,c)\), direct differentiation gives

\[
 D^2f[(a,b,c)]^2=
       \rho^{-1}|b-va|^2+
       \rho^{-1}\Psi''(r)(c-ra)^2.                          \tag{15}
\]

By Cauchy–Schwarz and (2), this is between zero and the coefficient in (13)
without \(\max w_i\), times \(a^2+|b|^2+c^2\). The stated Hessian bound follows
by summing the disjoint coordinate blocks, and integrating along a segment in
\(C\) proves the Lipschitz gradient and descent inequalities. The projection
optimality condition, for any \(v\in C\), is

\[
 \langle\nabla F(u_n)+L(u_{n+1}-u_n),v-u_{n+1}\rangle\ge0.
\]

Combine this with convexity at \(u_n\) and the descent inequality to obtain

\[
 F(u_{n+1})-F(v)\le\frac L2
             (\|u_n-v\|^2-\|u_{n+1}-v\|^2).
\]

Taking \(v=u_n\) also proves monotonicity of objective values (indeed with a
nonnegative squared-step decrease). A minimizer \(u_*\) exists by compactness.
Sum the displayed inequality with \(v=u_*\) from 0 to \(n-1\), then use
monotonicity to bound the final gap by the average gap. This proves (14). ∎

The projection in Proposition 2 is onto an affine set, **not** onto the boxed
set \(C\). Proposition 3 is therefore an oracle iteration bound, not a
near-linear overall algorithm. Letting \(\delta\downarrow0\) makes (13)
degenerate. It does not cover vacuum or singular endpoint measures uniformly.

### Proposition 4 (a finite-grid primal/dual gap)

For an all-variable perspective discretization, let
\(F(u)=\sum_iw_if(u_i)\) and impose \(Bu=b\). If \(u\) is primal feasible and
\(y\) obeys \((B^*y)_i/w_i\in K\) for every cell, then

\[
 0\le F(u)-\inf_{Bv=b}F(v)\le F(u)-\langle b,y\rangle.      \tag{16}
\]

**Proof.** The support-function representation gives
\(w_if(v_i)\ge (B^*y)_i\cdot v_i\). Summing for any feasible \(v\) gives
\(F(v)\ge\langle y,Bv\rangle=\langle y,b\rangle\).
Taking the infimum and evaluating at \(u\) yields (16). ∎

This requires genuinely feasible \(u,y\), or validated residual corrections.
A small successive-iterate difference by itself proves neither feasibility nor
a small objective gap. Strong duality or existence of a dual maximizer is not
needed for the bound, but would matter for obtaining tight certificates.

**Gap.** Removing positivity boxes, computing their projections, bounding
inexact numerical errors, and linking the finite-grid value to continuum RUOT
remain unproved here. No source convergence assertion is imported without its
existence and qualification assumptions.

## 6. Approach V: quantify rather than equate the quadratic surrogate

Set \(Q(r)=\nu r^2/(2\lambda)\). For critical binary branching,

\[
 0\le Q(r)-\Psi(r)\le\frac{\nu r^4}{24\lambda^3}
 \quad\hbox{for every real }r,                              \tag{17}
\]

and the left inequality is strict for \(r\ne0\).

**Proof.** Both functions are even and vanish to first order at zero. For
\(r\ge0\), their second-derivative difference is

\[
 \frac\nu\lambda
       \left[1-\frac1{\sqrt{1+(r/\lambda)^2}}\right].
\]

For \(x\ge0\), \(0\le1-(1+x)^{-1/2}\le x/2\), since its derivative is
\(\tfrac12(1+x)^{-3/2}\le1/2\). Integrate this bound twice with
\(x=(r/\lambda)^2\) to get (17), using
\(\int_0^r(r-s)s^2ds=r^4/12\). Strict positivity follows from strict positivity
of the second-derivative difference for \(r>0\). Evenness covers negative \(r\).
∎

Consequently, on any **same** admissible class of curves with \(|r|\le R_g\)
and \(\int_0^1\rho_t(\mathbb T^d)dt\le M_g\), replacing only \(\Psi\) by
\(Q\) changes each objective by a number in
\([0,\nu M_gR_g^4/(24\lambda^3)]\), hence changes the infimum by at most
that number. The conclusion uses the same diffusion constraint and admissible
set. It does **not** assert equivalence to ordinary diffusion-free WFR, or
closeness of optimizers without further stability assumptions.

There is no uniform relative equivalence of the penalties at large growth.
From (1), \(\Psi(r)=\nu |r|\log(2|r|/\lambda)+O(|r|)\); hence
\(\Psi(r)/Q(r)\to0\) as \(|r|\to\infty\). Even at fixed parameters this rules
out treating the quadratic replacement as an identity.

This matters for a recent claimed practical route. Ying et al.,
arXiv:2605.00545v2 (10 June 2026), §4.6, §7 and Appendix B.3, explicitly use a
WFR approximation for the unavailable RUOT semi-coupling. Appendix C.11 adds
small numerical comparisons; it does not prove a uniform error bound or an
exact solver for the original OWR target. We use the newer version rather than
carry forward the differing parameter conventions of v1.

**Gap.** Bounds on growth and integrated mass for actual minimizers, a
quantitative continuum approximation, and an error-controlled scalable solver
are still needed. The proxy's empirical performance cannot fill those gaps.

## 7. Precisely what remains unresolved

Baradat–Lavenant already supplied a numerical dynamical convex-optimization
method; its existence should not be called a new solution. The question is
broader and less formal than a single complexity conjecture. This packet gives
neither a general fast algorithm with controlled accuracy for the source
measure-level model nor a proof that one cannot exist. The five approaches
produce local and finite-dimensional tools, with explicit gaps at exactly that
boundary.

The strongest computed results below are regression tests of the formulas:
local KKT residuals, symbolically checked derivatives, and equality of an
FFT/tridiagonal projection with a dense small-matrix reference. They are not
numerical evidence of a new full solver, empirical runtime claims, or a proof
of continuum convergence. All general assertions in this note are established
by the analytic arguments above.

## References

1. A. Baradat (joint with H. Lavenant), OWR 10/2021, pp. 552–555,
   https://doi.org/10.4171/OWR/2021/10 .
2. A. Baradat and H. Lavenant, *Regularized unbalanced optimal transport as
   entropy minimization with respect to branching Brownian motion*,
   https://arxiv.org/abs/2111.01666v2 , especially §6.3 and Appendix A.
   Published monograph metadata: https://doi.org/10.24033/ast.1247 .
3. J. Ying et al., *Beyond Continuity: Simulation-free Reconstruction of
   Discrete Branching Dynamics from Single-cell Snapshots*,
   https://arxiv.org/abs/2605.00545v2 .

AI-assisted and unrefereed. No novelty or priority claim.
