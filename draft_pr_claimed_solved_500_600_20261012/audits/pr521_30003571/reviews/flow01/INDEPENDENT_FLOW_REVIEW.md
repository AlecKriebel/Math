# Independent analytic audit of frozen PR #521

**Reviewer:** flow01. **Final checkpoint:** 2026-10-13 03:19 UTC. **Completion:** 100% of the assigned analytic audit. No prior audit was used as evidence.

**Verdict:** the analytic mechanism in `public/PROOF.md` is valid for the precise probability-normalized flow it states. I found no mathematical blocker to the claimed finite-time counterexample. The exact horizontal coefficient and its sign survive an independent nonlinear-family reduction, a monomial coefficient calculation, and gauge/frame checks. This is an audit of validity, not of historical novelty or catalogue administration.

The reviewed proof has SHA-256 `4deb64c3b249dcf26a87ccdd222bad837e61f107b5304ed0e3ad2c6f1e444b36`.

## 1. Claim and possible falsifiers

The claim is that the flow

\[
\phi_t=\log\bigl(\operatorname{MA}(\phi)/\mu_\phi\bigr)
\]

on \(L=\mathcal O_E(2)=\mathcal O(2,2)\) for \(E=\mathcal O(1)\oplus\mathcal O(1)\) admits smooth, everywhere strictly positive initial curvature, while its actual finite-time solution has a negative horizontal curvature coefficient at \((s,z)=(0,0)\). Both fiber measures are probabilities. The initial metric must be the square of a positive metric on \(\mathcal O_E(1)\), and the total space must remain compact and smooth. The hypothesis is not a claim about Griffiths' conjecture, a limiting metric, or another normalization.

I specifically tried to falsify it through: an incorrect projectivization convention; a non-global fiber density; an unnoticed base/frame term in normalization; the wrong anticanonical coefficient or time scale; nonstationarity of the central fiber; first-base-derivative terms in the second variation; use of a formal linearization in place of the nonlinear solution; missing finite-time parameter regularity; and a sign error in the final evaluation.

## 2. Global geometry and the scalar equation

Write \(A=\mathcal O_{\mathbf P^1}(1)\), so \(E=A\otimes\mathbf C^2\). Under the stated convention \(f_*\mathcal O_E(1)=E\), the tautological quotient line is \(A\boxtimes\mathcal O(1)\). Consequently

\[
X=\mathbf P^1\times\mathbf P^1,\qquad
L=A^2\boxtimes\mathcal O(2),\qquad
\det E=A^2,\qquad
K_{X/S}^{-1}=L\otimes f^*A^{-2}=\mathcal O(0,2).
\]

This checks the sign of the determinant factor directly. In particular \(\mathcal O_E(1)=\mathcal O(1,1)\) is ample.

Choose a nonzero holomorphic determinant frame \(d\) on a base chart. Its corresponding \(L\)-valued fiber one-form can be written \(dz\otimes\ell\) in a compatible frame \(\ell\). Its norm density is \(e^{-\phi}dA_z\). Define

\[
I=\int e^{-\phi}dA_z,\qquad M=\int g\,dA_z,\qquad
g=\phi_{z\bar z}.
\]

With Euclidean area \(dA_z=dx\,dy\), \(M=2\pi\); another fixed area convention cancels in the ratio. The two probability densities are

\[
\mu_\phi=I^{-1}e^{-\phi}dA_z,
\qquad \operatorname{MA}(\phi)=M^{-1}g\,dA_z.
\]

Thus the literal scalar equation is

\[
\boxed{\phi_t=\log g+\phi+\log I-\log M.}\tag{A}
\]

The coefficient of the weight on \(\mathcal O_E(2)\) is one. Tensor-power rank is already present in the curvature of the weight and is not an extra factor multiplying \(\phi\).

Three global checks are decisive:

* Changing \(d\) to \(a(s)d\) multiplies its norm density and \(I\) by \(|a(s)|^2\), so \(\mu_\phi\) is unchanged. If compatible \(L\) frames are also changed, \(\phi\) and \(\log I\) acquire opposite additions. Since \(\log|a|^2\) is pluriharmonic, curvature is unchanged.
* Under \(\zeta=1/z\), \(\phi_\zeta=\phi_z-2\log|z|^2\), \(dA_\zeta=|z|^{-4}dA_z\), and \(g_\zeta=|z|^4g_z\). Both densities and the scalar right side of (A) match on overlaps.
* For any smooth real base function \(b(s)\), the right side of (A) is invariant under \(\phi\mapsto\phi+b\): \(g\) is unchanged and \(I\mapsto e^{-b}I\). A fixed base weight can therefore be retained throughout a fiberwise flow. This is an invariance, not a freely adjustable time-dependent base correction.

Using unnormalized curvature volume in the numerator changes the right side by the fixed constant \(\log M\). Adding \(t\log M\) to the solution produces that alternative convention and changes no curvature. This check does not equate the flow with a flow using an unnormalized anticanonical denominator: that would remove the nonlocal term and change horizontal evolution.

## 3. Independent check of the initial metric

Set \(u=|s|^2\), \(v=|z|^2\), \(p=u/(1+u)\), \(x=v/(1+v)\), \(\epsilon=1/96\), and \(\delta=1/4\). Split the initial weight as

\[
B(s)=2\log(1+u)+(2-\epsilon)/(1+u),\quad
F(z)=2\log(1+v),\quad
\phi_0=B+F+\delta p x^2.
\]

The additions to the usual \(\mathcal O(2,2)\) weight are global smooth functions. On inverse coordinate charts, \(p\) becomes \(1/(1+|1/s|^2)\) and \(x\) becomes \(1/(1+|1/z|^2)\), with the usual degree-two metric transition for the logarithmic terms. The square-root weight \(\phi_0/2\) has the degree-one transitions of \(\mathcal O(1,1)\), so it supplies the required positive initial metric on \(\mathcal O_E(1)\).

For an independent Hessian check, a radial function \(H(u,v)\) has

\[
H_{s\bar s}=H_u+uH_{uu},\quad
H_{z\bar z}=H_v+vH_{vv},\quad
|H_{s\bar z}|^2=uv\,H_{uv}^2.
\]

Applying these identities gives the normalized coefficients

\[
A_0=4p+(\epsilon+\delta x^2)(1-2p),\quad
B_0=2+2\delta p x(2-3x),\quad
Q_0=4\delta^2p(1-p)x^3(1-x).
\]

The following decompositions give independently checkable global bounds:

\[
\begin{aligned}
A_0-[\epsilon+(4-2\epsilon-2\delta)p]
 &=\delta[x^2+2p(1-x^2)]\geq0,\\
B_0-(2-2\delta)
 &=2\delta[(1-p)+p(1-x)(1+3x)]\geq0,\\
4\delta^2p-Q_0
 &=4\delta^2p[(1-x)(1+x+x^2)+x^4+p x^3(1-x)]\geq0.
\end{aligned}
\]

All factors are nonnegative on the closed square \([0,1]^2\), including infinity points. Therefore

\[
A_0B_0-Q_0\geq\frac1{64}+\frac{159}{32}p>0,
\qquad B_0\geq\frac32.
\]

There is no initial semipositive or boundary degeneracy.

## 4. Analytic input and a concrete normalized-solution construction

The analytic input is the standard all-time smooth normalized Kähler–Ricci flow on compact \(\mathbf P^1\), together with smooth dependence on smooth initial data over finite time intervals. Positive curvature on the *total space* is not an assumption of this input. Finite-time parameter smoothness is the only horizontal regularity needed.

This need not be hidden inside a limiting-metric assertion. Let

\[
g_F=F_{z\bar z}=2/(1+|z|^2)^2,\qquad
\mu_F=\pi^{-1}(1+|z|^2)^{-2}dA_z.
\]

For a real parameter \(|k|<1/2\), the initial fiber weight \(F+kx^2\) is positive: its normalized vertical coefficient is \(2+2k x(2-3x)\geq 2-2|k|>1\). Let \(g(t,k)\) be the standard smooth solution of

\[
g_t=(\log g)_{z\bar z}+g,\qquad
g(0,k)=g_F+k(x^2)_{z\bar z}.\tag{B}
\]

The ratio \(g/g_F\) is a global smooth function on the fiber. Define, globally on that fiber,

\[
Q(t,k)=e^t kx^2+\int_0^t e^{t-\tau}\log(g(\tau,k)/g_F)\,d\tau,
\]

\[
C(t,k)=\int_0^t\log\left(\int e^{-Q(\tau,k)}\mu_F\right)d\tau,
\qquad q=Q+C.
\]

Equation (B) and \((\log g_F)_{z\bar z}=-g_F\) imply

\[
Q_{z\bar z}=g-g_F,\qquad
q_t=\log(g/g_F)+q+\log\int e^{-q}\mu_F.\tag{C}
\]

This explicitly constructs the normalized weight from the standard curvature flow, with the correct scalar gauge. Smoothness of \(g\) in \((t,k,z)\) over every finite interval implies the same for \(Q,C,q\); integration over the compact fiber preserves it. Smooth parameter dependence follows from classical parabolic wellposedness on the positive cone, and can be checked by difference quotients or differentiated parabolic equations. The base remains a parameter; no smoothing in base directions is asserted or needed.

Uniqueness of (C), or (A), also follows directly. For two solutions with difference \(v\), \(|\log I_1-\log I_2|\leq\|v\|_\infty\). At fiber maxima/minima the log-Hessian comparison gives the upper Dini estimate \(D^+\|v\|_\infty\leq2\|v\|_\infty\). Common initial data then imply equality of the solutions by Grönwall. This supplies the uniqueness used below without requiring uniqueness of a Kähler–Einstein limit.

The cited primary sources are compatible with these finite-time inputs: [Naumann, published Theorem 5 and equations (8), (10), (13)](https://intlpress.com/api/bgcloud-front/resource/pdf/volume/1806601940286992386-1806601940286992386-fb415fcde747f9c588db3e8aababba9d.pdf) state this probability flow and smooth existence on \(X\times[0,\infty)\). [Berman, Theorem 28 and Section 2.3](https://arxiv.org/pdf/1002.3717) separate all-time smooth existence from convergence assumptions. The condition \(H^0(TX_s)=0\) belongs to a convergence assertion, not to existence; \(\mathbf P^1\)'s automorphisms create no finite-time obstruction here.

## 5. Exact nonlinear family reduction and the true second jet

Use the *actual* solutions from (C) to define

\[
\Phi(t,s,z)=B(s)+F(z)+q(t,\delta p(s),z).\tag{D}
\]

Base-gauge invariance and (C) show that (D) solves (A) on all base charts, with precisely the proposed initial data. Uniqueness makes it the nonlinear solution in the claim. No approximate family has been substituted.

At \(k=0\), \(g=g_F\), \(Q=C=q=0\). Thus the central fiber is exactly stationary. Since \(p_s(0)=0\), \(p_{s\bar s}(0)=1\), and \(B_{s\bar s}(0)=\epsilon\), the chain rule in (D) gives

\[
\Phi_s(0,z)=\Phi_{s\bar z}(0,z)=0,\qquad
w(z,t):=\Phi_{s\bar s}(0,z)=\epsilon+\delta a(z,t),
\]

where \(a=\partial_k q|_{k=0}\). This also verifies the symmetry consequences directly, without relying only on a lifted rotation argument.

Differentiating (C) at \(k=0\), justified by the finite-time parameter smoothness, yields

\[
a_t=\Delta_F a+a-\langle a\rangle_F,
\quad a(0)=x^2,
\quad\Delta_F=g_F^{-1}\partial_z\partial_{\bar z}.\tag{E}
\]

Equivalently \(w_t=\Delta_Fw+w-\langle w\rangle_F\). As a cross-check by direct base differentiation, \(I_s=0\), \(I_{s\bar s}=-I\langle w\rangle_F\), and \(g_s=0\) on the central fiber. Those identities reproduce (E), with no variance or log-Hessian-square term left over.

Equation (E) describes an exact derivative of the genuine nonlinear solution. Solving it is not a small-time approximation to that derivative. At the central fiber the Schur complement is \(c=\Phi_{s\bar s}-|\Phi_{s\bar z}|^2/g=w\), and the product-coordinate tangent vector \(\partial_s\) has curvature coefficient \(w\). Any negative \(w\) therefore supplies an actual negative tangent direction.

## 6. Independent monomial solution and finite-time sign

Radial integration gives \(\langle H(x)\rangle_F=\int_0^1 H(x)dx\), while direct radial differentiation gives

\[
\Delta_F H=\tfrac12\{x(1-x)H''+(1-2x)H'\}.
\]

For \(a=a_0+a_1x+a_2x^2\), (E) becomes the triangular coefficient system

\[
\dot a_2=-2a_2,\qquad
\dot a_1=2a_2,\qquad
\dot a_0=-a_2/3,
\quad (a_0,a_1,a_2)(0)=(0,0,1).
\]

Consequently, writing \(R=e^{-2t}\),

\[
a(x,t)=-(1-R)/6+(1-R)x+Rx^2,
\]

\[
\boxed{w(0,t)=\epsilon-\frac\delta6(1-e^{-2t}).}\tag{F}
\]

Its initial derivative is \(-\delta/3=-1/12\), consistent with direct evaluation of (E) at the fiber pole, where \(\Delta_F x^2=0\). At \(t_*=(\log2)/2\), \(R=1/2\), and

\[
w(0,t_*)=\frac1{96}-\frac1{48}=-\frac1{96}.
\]

The exact threshold is \(R<3/4\), or \(t>\tfrac12\log(4/3)\). The minimum on the central fiber is attained at \(x=0\), since \(\partial_xa=(1-R)+2Rx\geq0\) for \(t\geq0\). There is no limiting-time argument. Uniqueness of (E) follows by noting that the mean of a zero-initial-data difference is constant, then applying the heat maximum principle to the difference multiplied by \(e^{-t}\).

## 7. Source diagnostic, repairs, and exact remaining gap

An adversarial check detects a normalization inconsistency in Naumann's printed Proposition 4, equation (14): its literal \(+r c\) term disagrees with (A), which produces \(+c\). Take a product Fubini–Study fiber weight plus any base weight \(B(s)\). Probability normalization makes this family stationary, with \(c=B_{s\bar s}\), zero Kodaira–Spencer term, zero fiber Laplacian of \(c\), and \(\partial_s\partial_{\bar s}\log I=-c\). The printed formula would give \(c_t=(r-1)c\), contradicting stationarity for \(r=2\). Thus the printed formula cannot be imported literally without a change of notation or scaling. The draft correctly avoids importing it and calculates from the defining flow.

This discrepancy is **not a blocker** to the draft's theorem. A useful optional repair is to add this pure-base diagnostic so readers see why the coefficient-one calculation must take precedence over the printed evolution formula. A second minor repair is to define `u=|s|^2` consistently: the displayed definition in Section 2 currently appears as `\nu=|s|^2` while subsequent expressions use `u`.

**Strongest verified result:** conditional only on established finite-time Kähler–Ricci flow wellposedness, the stated smooth compact counterexample has the exact coefficient (F), initial strict total-space positivity, and negative horizontal curvature at the specified finite time. The imported analytic fact is a standard theorem about positive fiber metrics, not an equivalent form of the target positivity-preservation claim.

**Exact remaining analytic gap:** none found. Historical novelty, the repository's catalogue claim wording, and administrative publication status were outside this review. The attached dependency-free exact check verifies algebraic identities and signs, and expressly does not claim to establish parabolic existence by computation.

Source provenance is recorded by the parent audit in `audits/pr521_30003571/PRIMARY_SOURCE_RECEIPT.json`; no full copyrighted source is included in this review artifact.
