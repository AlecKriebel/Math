# Regular negative-mass ZAS slices do not force the weak Bianchi identity

## Result and scope

The universal regular-zero-area-singularity (ZAS) conjecture in Annegret Burtscher's Oberwolfach report, printed pp. 2232–2233, is false under its stated geometric admissibility condition and the boundary test-field convention of Burtscher–Kiessling–Tahvildar-Zadeh (BKTZ), Definition 2.1. The counterexample below is static, spherically symmetric and asymptotically flat. Its natural spacelike slices have the standard harmonically regular negative-mass Schwarzschild ZAS. The offending integral exists absolutely and is nonzero.

This does not contradict BKTZ's sufficient-condition theorem, which includes an additional curvature-growth assumption. No claim is made about a conjecture strengthened by an energy condition, a specified electromagnetic matter model, or additional lapse/curvature hypotheses. Historical priority is not established.

Throughout, set the physical constants (c=G_{\mathrm{Newton}}=1), use signature ((-+++)), and write (G^\mu{}_{\nu}) for the mixed Einstein tensor. On the smooth interior,
\[
G_{\mu\nu}\nabla^\mu\psi^\nu=G^\mu{}_{\nu}\nabla_\mu\psi^\nu.
\]

## 1. The metric and the precise test space

Fix (a>0). Let
\[
\overline M=\mathbb R_t\times\{x\in\mathbb R^3:|x|\geq a\},\qquad
M=\operatorname{int}\overline M,\qquad \rho=|x|,\quad
\phi=1-\frac a\rho.
\]
Equip (M) with
\[
\boxed{g=-\phi^{-2}dt^2+\phi^4\bigl(d\rho^2+\rho^2d\Omega^2\bigr).} \tag{1}
\]
The metric is smooth and Lorentzian on (M), but is not asserted to extend as a nondegenerate metric to its inner boundary. Test fields are smooth sections of (T\overline M), compactly supported in the manifold-with-boundary topology. They are allowed to have a nonzero normal component at the inner boundary. This is the boundary-reaching convention used in BKTZ Definition 2.1, the footnote to Theorem 1.1, and the explicit radial boundary term in equation (2.5).

If instead one requires compact support in the punctured open manifold (M), every test stays away from the singularity and the assertion follows from the ordinary smooth Bianchi identity. Such a convention cannot express the conjecture about crossing the singularity. A different smooth structure obtained by collapsing the boundary sphere is also a different test-field problem; no unproved equivalence with it is assumed here.

## 2. Geometric admissibility

Every constant-(t) slice has metric
\[
h=\phi^4\delta,
\]
where \(\delta\) is the Euclidean metric on \(\rho\ge a\). The resolution pair \((\delta,\phi)\) is smooth at the boundary, \(\phi=0\) there, and the Euclidean unit normal pointing into the exterior satisfies
\[
\overline\nu(\phi)=\partial_\rho\phi\big|_{\rho=a}=\frac1a>0.
\]
Moreover, \(\Delta_\delta\phi=0\). These are exactly the regularity conditions in Bray–Jauregui Definition 6, and in fact the harmonic condition in Definition 7.

For any sequence of surfaces converging in \(C^1\) to the boundary sphere, their Euclidean areas stay bounded while the maximum of \(\phi^4\) on those surfaces tends to zero. Their \(h\)-areas therefore tend to zero. Thus the ZAS condition holds for the full class of approaching surfaces, not merely coordinate spheres.

The regular ZAS mass is
\[
\begin{aligned}
m_{\rm reg}
&=-\frac14\left(\frac1\pi\int_{S_a}
       (\overline\nu\phi)^{4/3}\,dA_\delta\right)^{3/2}\\
&=-\frac14\left(4a^{2/3}\right)^{3/2}=-2a<0. \tag{2}
\end{aligned}
\]
The slice is asymptotically flat and is exactly the usual negative-mass Schwarzschild spatial metric. Its area radius is
\[
r=\rho\phi^2=\frac{(\rho-a)^2}{\rho},\qquad
h=\frac{dr^2}{1+4a/r}+r^2d\Omega^2. \tag{3}
\]
Thus its cumulative mass is the constant \(-2a\). This is a statement about the spatial metric; the spacetime lapse in (1) is different from the Schwarzschild vacuum lapse.

The singularity is timelike in the limiting sense relevant to the source. Each tube \(\rho=a+\varepsilon\) has spacelike normal and Lorentzian induced metric. More explicitly, the optical radial coordinate
\[
s(\rho)=\int_a^\rho\phi(u)^3\,du
\]
is finite at \(\rho=a\), is strictly increasing in the interior, and has \(s\sim(\rho-a)^4/(4a^3)\). The radial part of (1) is \(\phi^{-2}(-dt^2+ds^2)\); hence its conformal radial boundary \(s=0\) is timelike. The angular spheres shrink to zero physical area. Section 3 shows invariant curvature blow-up, so this is a genuine singularity rather than a coordinate singularity. Also \(\phi\to1\) at infinity, so (1) is asymptotically flat.

The assertion about spacelike slices here uses the static foliation, as in BKTZ Section 1.3. It does not assert regular ZAS resolution for every arbitrary tilted hypersurface; that substantially different universal quantifier is not part of their construction.

## 3. Curvature computation, including a useful lapse family

Write
\[
N_v=\frac{\rho+a}{\rho-a},\qquad
N=A+B N_v,\qquad A,B\ge0,\quad A+B>0, \tag{4}
\]
and temporarily replace (1) by \(g_N=-N^2dt^2+h\). Formula (1) is the case \(A=B=1/2\), since \((1+N_v)/2=\phi^{-1}\).

The three-dimensional conformal Ricci formula gives
\[
\operatorname{Ric}(h)_{ij}
=-2\phi^{-1}\partial_i\partial_j\phi
+6\phi^{-2}\partial_i\phi\partial_j\phi
-2\phi^{-2}|d\phi|_\delta^2\delta_{ij}, \tag{5}
\]
where we used \(\Delta_\delta\phi=0\). Its mixed eigenvalues in the radial and two angular directions are
\[
\frac{4a}{\rho^3\phi^6},\quad
-\frac{2a}{\rho^3\phi^6},\quad
-\frac{2a}{\rho^3\phi^6}. \tag{6}
\]
In particular \(R_h=0\).

Direct differentiation gives the static-vacuum identities
\[
\operatorname{Hess}_h N_v=N_v\operatorname{Ric}(h),\qquad
\Delta_h N_v=0. \tag{7}
\]
For clarity, the radial and \(\theta\theta\) Hessian components used to check (7) are
\[
N_v''-2\frac{\phi'}\phi N_v',\qquad
\left(\rho+2\rho^2\frac{\phi'}\phi\right)N_v',
\]
and the \(\varphi\varphi\) component is the second expression times \(\sin^2\theta\). They agree with \(N_v\) times the corresponding covariant Ricci components from (6).

For a static warped product \(-N^2dt^2+h\), direct Christoffel computation yields
\[
\operatorname{Ric}(g_N)_{tt}=N\Delta_hN,\quad
\operatorname{Ric}(g_N)_{ti}=0,\quad
\operatorname{Ric}(g_N)_{ij}=\operatorname{Ric}(h)_{ij}-N^{-1}(\operatorname{Hess}_hN)_{ij}.
\]
Equations (4) and (7) imply \(\Delta_hN=0\), \(R_{g_N}=0\), and
\[
G^t{}_t=0,\qquad G^i{}_j=\frac A N\operatorname{Ric}(h)^i{}_j. \tag{8}
\]
For (1), this is
\[
\boxed{
(G^t{}_t,G^\rho{}_\rho,G^\theta{}_\theta,G^\varphi{}_\varphi)
=\left(0,\frac{2a}{\rho^3\phi^5},-\frac{a}{\rho^3\phi^5},-\frac{a}{\rho^3\phi^5}\right).
} \tag{9}
\]
All off-diagonal mixed components vanish. Consequently
\[
\operatorname{Ric}(g)_{\mu\nu}\operatorname{Ric}(g)^{\mu\nu}
=\frac{6a^2}{\rho^6\phi^{10}}\longrightarrow+\infty\quad(\rho\downarrow a). \tag{10}
\]

## 4. Absolute convergence and an explicit nonzero test

Choose \(\eta\in C_c^\infty(\mathbb R)\) with \(\int\eta(t)dt=1\), and choose \(\chi\in C_c^\infty([a,\infty))\) equal to \(1\) near \(a\). Set
\[
\psi=\eta(t)\chi(\rho)\partial_\rho. \tag{11}
\]
Because \(a>0\), \(\partial_\rho=x^i\partial_{x^i}/\rho\) is smooth up to the entire inner boundary. The components of (11) in spherical coordinates are angular-independent, including at the boundary. Thus (11) also satisfies the additional angular-independence convention used when writing BKTZ equation (2.5).

For (1),
\[
dV_g=\phi^5\rho^2\,dt\,d\rho\,d\Omega.
\]
The only connection coefficients needed in the contraction are
\[
\Gamma^\rho{}_{\rho\rho}=2\frac{\phi'}\phi,
\qquad
\Gamma^\theta{}_{\theta\rho}=\Gamma^\varphi{}_{\varphi\rho}
=\frac1\rho+2\frac{\phi'}\phi.
\]
The time contribution vanishes because \(G^t{}_t=0\). Using (9), the terms involving \(\phi'/\phi\) cancel algebraically on the smooth interior, and the full scalar density is exactly
\[
\begin{aligned}
G^\mu{}_{\nu}\nabla_\mu\psi^\nu\,dV_g
&=2a\eta(t)\left(\frac{\chi'(\rho)}\rho-\frac{\chi(\rho)}{\rho^2}\right)
 dt\,d\rho\,d\Omega\\
&=2a\eta(t)\frac d{d\rho}\left(\frac{\chi(\rho)}\rho\right)
 dt\,d\rho\,d\Omega. \tag{12}
\end{aligned}
\]
Its absolute value is integrable: \(\rho\ge a>0\), and \(\eta,\chi,\chi'\) have compact support. Therefore the integral in the proposed weak identity is an ordinary absolutely convergent integral, not a principal value. Integrating (12),
\[
\boxed{
\int_MG^\mu{}_{\nu}\nabla_\mu\psi^\nu\,dV_g
=8\pi a\left[\frac{\chi(\rho)}\rho\right]_{a}^{\infty}
=-8\pi\ne0.
} \tag{13}
\]
This proves the counterexample.

The cancellation in (12) takes place between ordinary smooth functions before integration. Separately integrating individual connection summands, each of which can have a logarithmic divergence, would be invalid. No product of distributions, singular multiplication rule or delta-curvature extension is used.

## 5. The entire family has a well-defined boundary defect

There is an even stronger integrability check. In the exterior Cartesian coordinates \(x^i\), put \(n_i=x_i/\rho\). For (4) and (8),
\[
D^i{}_j:=N\phi^6G^i{}_j
=\frac{Aa}{\rho^3}(6n_i n_j-2\delta_{ij}). \tag{14}
\]
This is smooth up to \(\rho=a>0\), symmetric in its Euclidean indices, and traceless. Since the spatial connection of \(\phi^4\delta\) is
\[
\Gamma^j{}_{ik}=2\phi^{-1}
(\delta^j_i\partial_k\phi+\delta^j_k\partial_i\phi-\delta_{ik}\partial^j\phi),
\]
symmetry and tracelessness give \(G^i{}_j\Gamma^j{}_{ik}=0\). The other mixed Einstein components vanish. Hence, for **every** smooth boundary-reaching compactly supported vector field,
\[
G^\mu{}_{\nu}\nabla_\mu\psi^\nu\,dV_{g_N}
=D^i{}_j\partial_i\psi^j\,dt\,d^3x. \tag{15}
\]
Thus the full contraction is absolutely integrable for the entire test space, not only the test (11).

The Euclidean divergence of (14) vanishes. Indeed its radial and tangential eigenvalues are \(D_r=4Aa/\rho^3\) and \(D_T=-2Aa/\rho^3\), and
\[
D_r'+\frac2\rho(D_r-D_T)=0.
\]
Euclidean integration by parts with outward normal \(-n\) at the inner sphere yields the exact defect formula
\[
\boxed{
\int_MG^\mu{}_{\nu}\nabla_\mu\psi^\nu\,dV_{g_N}
=-\frac{4A}{a^2}\int_{\mathbb R\times S_a}\langle\psi_{\rm spatial},n\rangle_\delta\,dt\,dA_\delta.
} \tag{16}
\]
For (11) this is \(-16\pi A\). Within the family (4), therefore, the homogeneous weak identity for every source-convention test holds **if and only if** \(A=0\). At \(A=0\), the metric is the negative-mass Schwarzschild vacuum metric after constant time rescaling and \(G=0\). The metrics \(A,B>0\) have the same ZAS slices and the same inverse-linear order of lapse blow-up as this vacuum example, but a nonzero defect.

## 6. Why the existing theorem and physical restrictions remain distinct

Let \(x=\rho-a\). In (1), \(\phi=O(x)\), \(\phi'=O(1)\), \(e^\gamma=N=O(x^{-1})\), and \(\gamma'=O(x^{-1})\). These match assumptions (i) and (ii) of BKTZ Theorem 1.1. However, (9) gives exactly \(G^\mu{}_{\nu}=O(x^{-5})\), with a nonzero leading coefficient. The theorem demands the strictly better bound \(O(x^{-5+\kappa})\) for some \(\kappa>0\). Thus (1) lies at the excluded boundary, and there is no contradiction with the theorem.

The same spatial metric with the standard vacuum lapse is a positive control, not a counterexample. Reissner–Weyl–Nordström is unnecessary here and would not establish the claim, because the cited source excludes its singularity from the regular-ZAS class.

If one interprets the Einstein tensor as a matter tensor \(T=G/(8\pi)\), the energy density in the static orthonormal frame is zero and the two angular pressures are negative. The null energy condition fails for a null vector with angular spatial direction. No such condition appears in the stated geometric conjecture. This example therefore does not settle a separately strengthened conjecture requiring that condition or a specified electromagnetic matter model.

## References

1. A. Burtscher, *Matter particles, naked singularities, and a weak second Bianchi identity*, in *Mathematical Aspects of General Relativity*, Oberwolfach Reports 18 (2021), report 40, printed pp. 2231–2233. [DOI](https://doi.org/10.4171/OWR/2021/40).
2. A. Burtscher, M. K.-H. Kiessling and A. S. Tahvildar-Zadeh, *Weak second Bianchi identity for static, spherically symmetric spacetimes with timelike singularities*, Classical and Quantum Gravity 38 (2021), 185001. [arXiv:1901.00813v3](https://arxiv.org/abs/1901.00813v3). Definition 2.1, Theorem 1.1, equation (2.5), and Sections 1.3–1.4.
3. H. L. Bray and J. L. Jauregui, *A geometric theory of zero area singularities in general relativity*, Asian Journal of Mathematics 17 (2013), 525–559. [arXiv:0909.0522](https://arxiv.org/abs/0909.0522). Definitions 4, 6, 7 and 10.
