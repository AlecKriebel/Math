# Independent adversarial audit: involutive bounded deformation mechanism

Checkpoint: 2026-10-07 14:03:15 UTC (2026-10-07 07:03:15 America/Los_Angeles).

Local audit completion estimate: **100%** for verifying or falsifying the proposed qualitative deformation lemma. This percentage concerns this lemma only; it does not estimate completion of the all-von-Neumann-algebra cohomology input, the Banach–Mazur arguments, priority work, or the publication package.

## Verdict and scope

**The proposed mechanism is valid**, provided the finite constants used for selecting representatives and primitives are explicitly enlarged beyond the bounds on the relevant quotient inverse maps. This resolves the possible nonattainment of quotient norms. With that convention, the proposed defect estimate, constant

\[
D=8K+8L+16L^2,
\]

ordered product convergence, and near-identity bound all check. No substantive counterexample or remaining proof gap was found in this fixed-algebra lemma.

The cochain symmetry map is **conjugate-linear in the cochain**, but takes complex multilinear cochains to complex multilinear cochains. The averaging projection is consequently real-linear; this is sufficient for every use in the proof. The final conjugacy is complex-linear and preserves the given involution. If the perturbed product has the original unit, the final conjugacy fixes that unit automatically, even though the intermediate correction maps need not fix it.

This audit read `research/PROJECT_BRIEF.txt` and the applicable `/Users/alec/Documents/Math/AGENTS.md`. It checks the proposed proof directly rather than relying on Johnson, Raeburn–Taylor, or Roydor as a black-box deformation theorem. Roydor's PDF was not needed for this standalone calculation. Ordinary actual-image vanishing of the stated cohomology groups is an **assumption** of the audited lemma, not a result certified here. An independent internal sign-audit subagent also derived the reversal identity; its conclusion was checked against the calculations below. No external people were contacted, and no Git, manuscript, or publication operations were performed.

## Exact claim being checked

Let \(A\) be a fixed complex \(C^*\)-algebra, possibly nonunital, with multiplication \(m(a,b)=ab\) and its original involution and norm. Let \(C^n\) be the Banach space of all bounded complex \(n\)-linear maps \(A^n\to A\), with operator multilinear norm. Use the ordinary Hochschild differential with self-coefficients:

\[
\begin{aligned}
(\delta^n f)(a_1,\ldots,a_{n+1})
={}&a_1 f(a_2,\ldots,a_{n+1})\\
&+\sum_{j=1}^{n}(-1)^j
 f(a_1,\ldots,a_ja_{j+1},\ldots,a_{n+1})\\
&+(-1)^{n+1}f(a_1,\ldots,a_n)a_{n+1}.
\end{aligned}
\]

Assume

\[
H^2(A,A)=\ker\delta^2/\operatorname{ran}\delta^1=0,
\qquad
H^3(A,A)=\ker\delta^3/\operatorname{ran}\delta^2=0,
\]

where the denominators are the **actual** images, not their closures. Then there are constants \(\eta_A>0\) and \(L_A<\infty\) such that every bounded complex bilinear, associative multiplication \(\mu\) with

\[
\mu(a,b)^*=\mu(b^*,a^*),\qquad
\|\mu-m\|<\eta_A
\]

admits a bounded invertible complex-linear map \(\Phi:A\to A\), preserving the original involution, with

\[
\Phi\mu(a,b)=m(\Phi a,\Phi b)
\quad\text{and}\quad
\|\Phi-I\|\le e^{4L\|\mu-m\|}-1.
\]

Here \(L\) is a fixed enlarged primitive-selection constant constructed below. In particular, after further decreasing \(\eta_A\), one has \(\|\Phi-I\|<1/2\). No constant is claimed uniform in \(A\). No complete boundedness, normality, weak-star continuity, or isometry of \(\Phi\) is asserted.

## 1. Cochain involution: signs, field, and averaging

For \(n\ge1\), set

\[
(R_nf)(a_1,\ldots,a_n)=f(a_n^*,\ldots,a_1^*)^*,
\qquad
s_n=(-1)^{(n-1)(n-2)/2},
\qquad S_n=s_nR_n.
\]

The two conjugations in each argument cancel: inserting \(\lambda a_j\) into \(R_nf\) inserts \(\overline\lambda a_j^*\) into \(f\), and the final adjoint changes \(\overline\lambda\) back to \(\lambda\). Thus \(R_nf\in C^n\). By contrast, multiplying the entire cochain by \(\lambda\) introduces just one final conjugation, so

\[
R_n(\lambda f)=\overline\lambda R_nf.
\]

Since adjoint is isometric and the reversed tuple of adjoints ranges over the same product of unit balls, \(\|R_nf\|=\|f\|\). Reversing and taking adjoints twice gives \(R_n^2f=f\). The signs \(s_n\) are real, so \(S_n\) is also a conjugate-linear isometric involution.

Directly reverse the arguments in \(\delta^nf\) and take adjoints. The first and last terms exchange places. For an interior term with index \(j\), the corresponding index after reversal is \(k=n+1-j\), and

\[
(-1)^j=(-1)^{n+1}(-1)^k.
\]

The result is

\[
R_{n+1}\delta^n=(-1)^{n+1}\delta^nR_n.
\]

Since

\[
\frac{s_{n+1}}{s_n}=(-1)^{n-1}=(-1)^{n+1},
\]

the proposed signed operators satisfy

\[
\boxed{\delta^nS_n=S_{n+1}\delta^n}.
\]

For low degrees, \(S_1=R_1\), \(S_2=R_2\), \(S_3=-R_3\), and \(S_4=-R_4\). In particular, \(\delta^1R_1=R_2\delta^1\), while \(\delta^2R_2=-R_3\delta^2\). These checks rule out the usual unsiged degree-two reversal error.

The map

\[
P_n=(I+S_n)/2
\]

is a real-linear norm-contracting projection onto the fixed cochains, and the displayed commutation identity makes it a cochain projection. In the degrees needed here,

\[
S_2\Delta=\Delta
\iff \Delta(a,b)^*=\Delta(b^*,a^*),
\]

\[
S_1h=h
\iff h(a^*)=h(a)^*.
\]

Hence averaging produces the required involution compatibility without losing complex multilinearity or increasing norms. It does not by itself provide a primitive; the actual-image cohomology hypothesis supplies that separately.

## 2. Closed range and selection constants

Write \(Z^n=\ker\delta^n\) and \(B^n=\operatorname{ran}\delta^{n-1}\). Each \(C^n\) is Banach. Since \(\|m\|\le1\), the differential is bounded, with \(\|\delta^n\|\le n+2\), and \(Z^n\) is closed. The associative Hochschild identity \(\delta^{n+1}\delta^n=0\) follows by cancellation of adjacent multiplication terms.

Actual \(H^3=0\) gives \(B^3=Z^3\), so \(\operatorname{ran}\delta^2\) is closed. The induced map

\[
\overline\delta^2:C^2/Z^2\longrightarrow B^3
\]

is a bounded linear bijection between Banach spaces. Its bounded inverse gives a finite \(K_0\) with

\[
\operatorname{dist}(f,Z^2)\le K_0\|\delta^2f\|.
\]

Choose once and for all \(K>K_0\), with \(K>0\). For \(\delta^2f\ne0\), the strict slack permits selecting an actual \(z_0\in Z^2\) with

\[
\|f-z_0\|\le K\|\delta^2f\|.
\]

For \(\delta^2f=0\), take \(z_0=f\). This handles the nonattainment issue explicitly; the estimate on a distance alone does not justify selecting a best approximant at its exact infimum.

Similarly, actual \(H^2=0\) makes

\[
\overline\delta^1:C^1/\ker\delta^1\longrightarrow Z^2
\]

a bounded linear Banach-space bijection. If its inverse norm is bounded by \(L_0\), choose \(L>L_0\), \(L>0\). For every \(z\in Z^2\), there is an actual \(h_0\in C^1\) such that

\[
\delta^1h_0=z,\qquad \|h_0\|\le L\|z\|.
\]

For \(z=0\), take \(h_0=0\). These are existence selections; no bounded linear right inverse or complemented kernel is required or inferred.

## 3. Associativity gives a quadratic coboundary defect

Let \(\Delta=\mu-m\) and \(\delta=\|\Delta\|\). Expanding associativity of \(m+\Delta\) and using associativity of \(m\) gives exactly

\[
\delta^2\Delta(a,b,c)
=\Delta(\Delta(a,b),c)-\Delta(a,\Delta(b,c)).
\]

For example, the linear part of the associator
\(\mu(\mu(a,b),c)-\mu(a,\mu(b,c))\)
is \(-\delta^2\Delta(a,b,c)\), which verifies the sign. Consequently,

\[
\|\delta^2\Delta\|\le2\delta^2.
\]

Choose \(z_0\in Z^2\) as above and put \(z=P_2z_0\). Because \(S_2\Delta=\Delta\), averaging preserves the approximation estimate:

\[
\|\Delta-z\|\le2K\delta^2,
\qquad
\|z\|\le\delta+2K\delta^2,
\qquad S_2z=z.
\]

Choose a primitive \(h_0\) of \(z\), and put \(h=P_1h_0\). Commutation of \(P\) with \(\delta\) gives

\[
\delta^1h=z,\qquad S_1h=h,
\qquad
\|h\|\le L(\delta+2K\delta^2).
\]

If \(\delta\le1/(2K)\), then \(\|h\|\le2L\delta\). If also \(\delta\le1/(4L)\), then \(\|h\|\le1/2\).

## 4. Exact correction identity and its bound

Set \(g=I+h\), \(b=g^{-1}\), and

\[
\nu(a,b')=g\mu(ba,bb').
\]

The use of \(b'\) as an argument here is only to distinguish it from the inverse map \(b\). The Neumann series gives \(\|b\|\le2\). Both \(g\) and \(b\) are complex-linear and preserve adjoints. The transported product \(\nu\) is associative by conjugation, and is involution-compatible because all three of \(\mu,g,b\) are.

For arbitrary \(x,y\in A\), a direct expansion, without discarding higher-order terms, gives

\[
\begin{aligned}
g\mu(x,y)-m(gx,gy)
&=\Delta(x,y)-\delta^1h(x,y)
  +h\Delta(x,y)-m(hx,hy).
\end{aligned}
\]

Indeed, the terms linear in \(h\) are
\(h(xy)-h(x)y-xh(y)=-\delta^1h(x,y)\).
Substituting \(x=ba\), \(y=bb'\) proves the proposed exact identity

\[
\nu-m=
\big[(\Delta-\delta^1h)+h\Delta-m(h\cdot,h\cdot)\big](b\cdot,b\cdot).
\]

Therefore

\[
\begin{aligned}
\|\nu-m\|
&\le\|b\|^2
\big(2K\delta^2+\|h\|\delta+\|h\|^2\big)\\
&\le4(2K+2L+4L^2)\delta^2\\
&=D\delta^2,
\qquad D=8K+8L+16L^2.
\end{aligned}
\]

There is no missing \(\|\mu\|\) factor: the quadratic term in this exact identity uses the original \(m\), whose norm is at most one. The \(h\Delta\) term accounts for the other product contribution.

## 5. Iteration, ordered products, and exact limiting conjugacy

Assume

\[
\delta_0=\|\mu_0-m\|
\le\min\left\{\frac1{2K},\frac1{4L},\frac1{2D}\right\}.
\]

Repeat the construction with \(\mu_n\), and set

\[
\mu_{n+1}=g_n\mu_n(b_n\cdot,b_n\cdot),
\quad g_n=I+h_n,
\quad b_n=g_n^{-1},
\quad \delta_n=\|\mu_n-m\|.
\]

Associativity and involution compatibility persist at every step. Since

\[
\delta_{n+1}\le D\delta_n^2\le\tfrac12\delta_n,
\]

all smallness assumptions persist, and

\[
\delta_n\le2^{-n}\delta_0,
\qquad t_n:=\|h_n\|\le2L\delta_n\le\tfrac12,
\qquad \sum_{n\ge0}t_n\le4L\delta_0=:s.
\]

Define the correctly ordered products

\[
\Phi_n=g_{n-1}\cdots g_0,
\qquad
\Psi_n=b_0\cdots b_{n-1}=\Phi_n^{-1},
\qquad \Phi_0=\Psi_0=I.
\]

The norm bounds

\[
\|\Phi_n\|\le\prod_{j<n}(1+t_j)\le e^s,
\]

\[
\|\Phi_{n+1}-\Phi_n\|
=\|h_n\Phi_n\|\le e^s t_n
\]

make \(\Phi_n\) Cauchy in operator norm. For the inverses,

\[
\|b_n\|\le(1-t_n)^{-1}\le e^{2t_n},
\quad
\|b_n-I\|\le2t_n,
\quad
\|\Psi_n\|\le e^{2s},
\]

so

\[
\|\Psi_{n+1}-\Psi_n\|
=\|\Psi_n(b_n-I)\|\le2e^{2s}t_n.
\]

Thus \(\Phi_n\to\Phi\) and \(\Psi_n\to\Psi\) in operator norm. Passing to the limit in both inverse identities gives \(\Phi\Psi=\Psi\Phi=I\). Complex linearity and adjoint preservation are closed under operator-norm limits.

An inductive product identity gives

\[
\Phi_n\mu_0(x,y)=\mu_n(\Phi_nx,\Phi_ny).
\]

Since \(\mu_n\to m\) in bilinear operator norm and \(\Phi_n\) is uniformly bounded and converges in operator norm, the limit is

\[
\boxed{\Phi\mu_0(x,y)=m(\Phi x,\Phi y)}.
\]

The standard finite-product expansion, or a telescoping estimate against the product of the scalar factors \(1+t_j\), yields

\[
\|\Phi_n-I\|\le\prod_{j<n}(1+t_j)-1.
\]

Taking the limit proves

\[
\|\Phi-I\|\le e^s-1\le e^{4L\delta_0}-1.
\]

For example, choosing

\[
\eta_A=\min\left\{
\frac1{2K},\frac1{4L},\frac1{2D},
\frac{\log(3/2)}{8L}\right\}
\]

and requiring \(\|\mu-m\|<\eta_A\) ensures \(\|\Phi-I\|<1/2\). The extra factor of two in the last threshold avoids endpoint ambiguity. The case \(\mu=m\) may simply take \(\Phi=I\).

## 6. Unit and boundary cases

If \(A\) has unit \(1\) and \(\mu\) has that same unit, the final map is unital. For any \(y=\Phi x\), surjectivity and the conjugacy identity give

\[
m(\Phi1,y)=\Phi\mu(1,x)=\Phi x=y,
\qquad
m(y,\Phi1)=\Phi\mu(x,1)=y.
\]

Thus \(\Phi1\) is the two-sided unit for \(m\), so \(\Phi1=1\). No normalized-cochain hypothesis is needed for this final conclusion. One should not assert from the given selection argument that every intermediate \(h_n(1)=0\) or \(g_n(1)=1\): that stronger statement has not been established and is unnecessary.

If \(A\) is unital but no unit of \(\mu\) was assumed, the established isomorphism itself supplies the unit \(\Phi^{-1}(1)\) for \(\mu\). In the nonunital case, the proof does not introduce or use a unit. The zero algebra causes no difficulty: all cochains are zero and one may take arbitrary positive finite \(K,L\) and \(\Phi=I\).

The only algebraic input beyond the original associative multiplication is exact associativity of \(\mu\). An approximately associative perturbation would add a residual term to the coboundary defect and is not covered. Likewise, reduced cohomology vanishing would not justify the primitive selection or the closed-range step here.

## Remaining gap relative to the larger research program

The strongest verified statement of this audit is the precise fixed-\(A\) conditional lemma above. It does **not** establish ordinary \(H^2=H^3=0\) for arbitrary von Neumann algebras, uniform control over central summands, the geometric near-isometry-to-near-multiplication bridge, the predual bridge, novelty, or publication readiness. Those are separate inputs to the core project. Within the audited involutive deformation mechanism, the exact remaining gap is **none**, once the enlarged-selection-constant convention is included explicitly.
