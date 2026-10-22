# Eternal Gaussian solutions of the full compressible Euler system

## Verdict and exact scope

For the full, non-isentropic ideal-gas Euler equations, the existence question has an explicit affirmative example in every dimension, including three. The three-dimensional monatomic example below is already in Fellner and Schmeiser (2007), Section 5. This is a reconstruction and scope correction, not a new discovery.

The example is \(C^\infty\) at every point of \(\mathbb R_t\times\mathbb R^d_x\), has strictly positive density, and has finite, positive, conserved total mass and energy. Its specific entropy is unbounded as \(|x|\to\infty\). Its velocity is affine in space and unbounded when \(t\ne0\). It is neither an isentropic solution nor a solution with compactly supported density, bounded specific entropy, or a Sobolev perturbation of constant entropy.

This distinction is part of the result, not a removable technicality. The unrestricted non-isentropic formulation is answered; an isentropic or bounded-entropy interpretation remains unanswered by this packet. No unqualified resolution of all possible interpretations of Serre's question is claimed.

## 1. Equations and interpretation

Fix \(d\ge1\) and \(\gamma>1\). The full Euler equations on all of \(\mathbb R^d\), with no external force, are
\[
 \partial_t\rho+\operatorname{div}(\rho u)=0, \tag{1}
\]
\[
 \partial_t(\rho u)+\operatorname{Div}(\rho u\otimes u)+\nabla p=0, \tag{2}
\]
\[
 \partial_t\mathcal E+\operatorname{div}((\mathcal E+p)u)=0,\qquad
 \mathcal E=\rho\left(e+\tfrac12|u|^2\right),\quad
 p=(\gamma-1)\rho e. \tag{3}
\]
Here \(e\) is specific internal energy. For positive smooth density these are equivalent to (1) and
\[
 D_tu=-\rho^{-1}\nabla p,\qquad
 D_te+(\gamma-1)e\,\operatorname{div}u=0,\quad
 D_t=\partial_t+u\cdot\nabla.
 \tag{4}
\]
Indeed, the product rule and (1) convert (2) to the first equation in (4). Multiplying it by \(\rho u\), adding \(\rho\) times the second equation, and using
\(\operatorname{div}(pu)=u\cdot\nabla p+p\operatorname{div}u\)
gives (3). Thus checking the internal-energy equation does not omit the conservative total-energy law.

The 2012 author version of Serre's Problem 4, pp.9–10, and the journal version, pp.204–205, explicitly discuss both \(p=\rho^\gamma\) and \(p=(\gamma-1)\rho e\). The latter equation of state does not impose spatially constant specific entropy.

## 2. Explicit monatomic theorem

**Theorem.** Let \(C>0\), \(d\ge1\), \(\gamma=1+2/d\), and
\[
 \alpha(t)=1+t^2.
\]
Then
\[
 \rho(t,x)=C\alpha^{-d/2}\exp\!\left(-\frac{|x|^2}{2\alpha}\right),\qquad
 u(t,x)=\frac{t}{\alpha}x,\qquad
 e(t,x)=\frac{d}{2\alpha},\qquad
 p(t,x)=\frac{\rho(t,x)}{\alpha} \tag{5}
\]
solve (1)–(3) smoothly for every real \(t\). Their mass and energy are
\[
 M=C(2\pi)^{d/2},\qquad E=\frac d2M. \tag{6}
\]

**Proof.** Since \(\alpha\ge1\), every expression is smooth and \(\rho,p,e\) are strictly positive. Put \(h=t/\alpha\). We have
\[
 \operatorname{div}u=dh,\quad
 \nabla\log\rho=-\frac{x}{\alpha},\quad
 D_t\log\rho=-\frac{dt}{\alpha}.
\]
The last equality follows either by differentiating (5), or by observing that
\(D_t(|x|^2/\alpha)=0\). Hence \(D_t\rho+\rho\operatorname{div}u=0\).

Also
\[
 D_tu=(h'+h^2)x=\frac{x}{\alpha^2},
 \qquad -\rho^{-1}\nabla p=\frac{x}{\alpha^2},
\]
because \(h'+h^2=\alpha^{-2}\). This proves momentum conservation.

Finally,
\[
 D_te=-\frac{dt}{\alpha^2},\qquad
 (\gamma-1)e\,\operatorname{div}u
 =\frac{1}{\alpha}\frac{dt}{\alpha}
 =\frac{dt}{\alpha^2}.
\]
Thus (4), and therefore (3), hold.

At a fixed time change variables \(x=\sqrt{\alpha}\,y\). The elementary Gaussian integrals give
\[
 \int_{\mathbb R^d}\rho\,dx=M,\qquad
 \int_{\mathbb R^d}|x|^2\rho\,dx=d\alpha M.
\]
Consequently,
\[
 K(t)=\frac12\int\rho|u|^2dx=\frac{dMt^2}{2\alpha},\qquad
 U(t)=\int\rho e\,dx=\frac{dM}{2\alpha}.
\]
Their sum is \(dM/2\). All integrals are finite at every real time; there are no unverified flux-at-infinity limits in this computation. In fact, the conserved densities and fluxes are Gaussian times polynomials at each time.

The solution is nontrivial: its mass and internal energy at \(t=0\) are positive, and its density changes in time. The case \(d=3,\gamma=5/3\) has the required odd dimension. \(\square\)

## 3. Entropy, flow, and regularity checks

Use the dimensionless specific entropy
\[
 S=\log(p/\rho^\gamma).
\]
Multiplication by a positive constant and addition of a constant would give the usual physical normalization without affecting the conclusions. For (5),
\[
 S=(1-\gamma)\log C+\frac{\gamma-1}{2\alpha}|x|^2. \tag{7}
\]
There is no missing time-only term: the power of \(\alpha\) cancels because
\(d(\gamma-1)=2\). Since \(D_t(|x|^2/\alpha)=0\), \(D_tS=0\), as required.

For every fixed \(t\), \(S\) is smooth but grows quadratically in \(|x|\). Thus this construction cannot be presented as having bounded entropy or entropy close to a constant in an unweighted Sobolev space. Nevertheless \(\int\rho|S|dx<\infty\); with \(C=1\) it equals \(M\).

The Lagrangian map is explicitly
\[
 \Phi_{t,s}(x)=\sqrt{\alpha(t)/\alpha(s)}\,x. \tag{8}
\]
Its Jacobian determinant is \((\alpha(t)/\alpha(s))^{d/2}>0\), and direct differentiation proves
\(\partial_t\Phi_{t,s}=u(t,\Phi_{t,s})\).
It remains a global orientation-preserving diffeomorphism at every pair of finite times. There is no vacuum interface and no boundary on which to apply a free-front parity argument.

The ratio \(p/\rho^\gamma\) depends on \(x\) by (7). In particular, it is not a solution of the isentropic law \(p=A\rho^\gamma\) with constant \(A>0\). It does not contradict a one-dimensional isentropic nonexistence theorem, even though (5) works for \(d=1\).

## 4. Independent kinetic derivation

The same formula follows without guessing the fluid equations. Set
\[
 f(t,x,v)=C(2\pi)^{-d/2}
   \exp\!\left[-\tfrac12\bigl(|x-tv|^2+|v|^2\bigr)\right].
\]
For fixed \(v\), its dependence on \(t,x\) is through \(x-tv\), so
\(\partial_tf+v\cdot\nabla_xf=0\).
Completing the square gives
\[
 |x-tv|^2+|v|^2
 =\alpha\left|v-\frac{tx}{\alpha}\right|^2+\frac{|x|^2}{\alpha}. \tag{9}
\]
Thus \(f\), as a function of \(v\), is a Maxwellian with mass \(\rho\), mean \(u\), and scalar temperature \(\theta=1/\alpha\). Its centered second and third moments are
\[
 \int(v-u)\otimes(v-u)f\,dv=\rho\theta I,\qquad
 \int(v-u)|v-u|^2f\,dv=0.
\]
Integrating the free-transport equation against \(1,v,|v|^2/2\), respectively, gives (1)–(3), with \(p=\rho\theta\) and \(e=d\theta/2\). These integrations and differentiations are justified locally uniformly in \((t,x)\) by Gaussian decay in \(v\). This is a second complete verification of the full, rather than isentropic, equation of state.

## 5. Arbitrary adiabatic exponent

The phenomenon does not depend on choosing the monatomic exponent. Let \(q=d(\gamma-1)>0\), choose \(\theta_0>0\), and solve
\[
 a''=\theta_0a^{-q-1},\qquad a(0)=1,\quad a'(0)=0. \tag{10}
\]
The right-hand side is smooth on \(a>0\). Multiplication by \(a'\) gives the conserved scalar energy
\[
 \frac12(a')^2+\frac{\theta_0}{q}a^{-q}
 =\frac{\theta_0}{q}. \tag{11}
\]
Therefore \(a\ge1\) and \(|a'|\le\sqrt{2\theta_0/q}\) throughout the maximal interval. On every finite time interval these estimates keep \((a,a')\) in a compact subset of the ODE domain. The usual local ODE continuation theorem then extends the solution to all real time. Uniqueness also gives \(a(-t)=a(t)\).

Define
\[
 \rho=C a^{-d}e^{-|x|^2/(2a^2)},\quad
 u=\frac{a'}a x,\quad
 p=\theta_0a^{-q}\rho,\quad
 e=\frac{\theta_0}{\gamma-1}a^{-q}. \tag{12}
\]
The identities
\[
 D_t(|x|^2/a^2)=0,\quad
 D_t\log\rho=-d\,a'/a,\quad
 D_tu=(a''/a)x,\quad
 -\rho^{-1}\nabla p=\theta_0a^{-q-2}x
\]
prove continuity and momentum by (10). Since
\(D_te=-q(a'/a)e\) and \(\operatorname{div}u=d\,a'/a\), they prove the internal-energy equation as well.

The Gaussian mass is again \(M=C(2\pi)^{d/2}\), while
\[
 E=\frac{dM}{2}(a')^2+
       \frac{M\theta_0}{\gamma-1}a^{-q}
   =\frac{M\theta_0}{\gamma-1}>0 \tag{13}
\]
by (11). The entropy is
\[
 S=\log\theta_0+(1-\gamma)\log C+
           \frac{\gamma-1}{2a^2}|x|^2.
\]
It has exactly the same unbounded-entropy qualification. For \(q=2,\theta_0=1\), (10) is solved by \(a=\sqrt{1+t^2}\), recovering (5). No novelty is asserted for this elementary affine extension.

## 6. Attribution and remaining gap

The source of the explicit three-dimensional family is K. Fellner and C. Schmeiser, *Classification of Equilibrium Solutions of the Cometary Flow Equation and Explicit Solutions of the Euler Equations for Monatomic Ideal Gases*, Journal of Statistical Physics 129 (2007), 493–507, [DOI 10.1007/s10955-007-9396-8](https://doi.org/10.1007/s10955-007-9396-8). Its [author manuscript](https://homepage.univie.ac.at/christian.schmeiser/Euler.pdf), Section 5, pp.11–12, has \(\alpha=1+t^2\), the finite mass/energy formulas, and the exponential profile. Setting its rotation parameter \(\lambda=0\) and \(\varphi(g)=Ce^{-g}\) gives (5). Section 1, pp.2–4, supplies the kinetic mechanism reconstructed above. This is direct prior art, not a deduction based only on an abstract.

Serre's later [*Expansion of a compressible gas in vacuum*](https://arxiv.org/abs/1504.01580), Theorem 2.5, concerns isentropic flows smooth up to a compact vacuum boundary, with an additional exponent restriction in the inspected version. None of those boundary hypotheses hold for the Gaussian gas.

The original statement's broad classical full-Euler reading therefore admits a previously published example. If the intended target requires spatially bounded entropy, Sobolev control of entropy relative to a constant, compact support, or the isentropic system, this example is excluded. This packet provides no new proof or counterexample for those narrower targets and does not certify their current open/closed status.

