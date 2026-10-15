# Independent analytic curvature and boundary-flux review

## Conclusion and exact scope

**PASS for the mathematical curvature, contraction, convergence, and boundary-flux claims in the frozen proof.** I found **zero mandatory mathematical corrections**, **zero unresolved analytical gaps**, and **two optional presentation additions** described below.

The conclusion is conditional on exactly the test space specified in the frozen proof: smooth compactly supported **vector fields on the exterior manifold with its boundary sphere retained**, whose spatial normal component need not vanish at that boundary. For that test space, the displayed counterexample has a well-defined ordinary absolutely convergent contraction integral and its value is \(-8\pi\) for the displayed radial test. More generally, the family has the asserted defect \(-16\pi A\). This report does not independently establish that the external open-problem statement uses precisely this test space, and it does not establish historical priority. Those are separate source and priority questions, not analytic consequences of the calculations below.

I recorded the area-radius/static-warp mechanism in `INITIAL_HYPOTHESIS.md` before reading the frozen author `PROOF.md`. I read no historical audit, peer verdict, or root synthesis. The independently generated checker imports no author code. Exact finite checks support, but do not replace, the universal derivations in this report.

## 1. Assumptions and an independent coordinate reduction

Let \(a>0\), \(\rho>a\), \(\phi=1-a/\rho\), and
\[
h=\phi^4(d\rho^2+\rho^2d\Omega^2),\qquad
q=\frac{\rho+a}{\rho-a},\qquad N=A+Bq,
\]
where \(A,B\ge0\) and \(A+B>0\). Thus \(N>0\) throughout the smooth interior. Consider \(g=-N^2dt^2+h\), with signature \((-+++)\) and the usual Ricci convention matching the coordinate formula below.

Use the area radius
\[
r=\rho\phi^2=\frac{(\rho-a)^2}{\rho},\qquad
\frac{dr}{d\rho}=1-\frac{a^2}{\rho^2}>0.
\]
One directly obtains
\[
f(r)=1+\frac{4a}{r}=q^2,
\qquad h=f^{-1}dr^2+r^2d\Omega^2,
\qquad g=-N(r)^2dt^2+f^{-1}dr^2+r^2d\Omega^2.
\]
This is a smooth interior change of variables; its degeneracy at \(\rho=a\) is not used to change the specified boundary smooth structure. The analytic curvature derivation below uses \(r\), while the distributional test space and integrability proof retain \(\rho\) and exterior Cartesian coordinates.

The spatial admissibility arithmetic can also be checked independently. The resolution metric is the smooth Euclidean metric; \(\phi(a)=0\), \(\partial_\rho\phi(a)=1/a>0\) for the normal into the exterior, and \(\Delta_\delta\phi=\phi''+2\phi'/\rho=0\). For any surfaces converging in \(C^1\) to \(S_a\), the Euclidean areas stay bounded and the maximum of \(\phi^4\) tends to zero, so \(\operatorname{Area}_h=\int\phi^4dA_\delta\to0\). Using the regular-ZAS mass formula stated in the frozen proof gives \(-\tfrac14(4a^{2/3})^{3/2}=-2a\). These checks concern the static slices and do not introduce a quantifier over arbitrary tilted hypersurfaces. External parity of the supplied definition and conjecture is still a separate source question.

## 2. Spatial curvature and the vacuum lapse

For \(h=f^{-1}dr^2+r^2d\Omega^2\), its non-angular Christoffel symbols include
\[
\Gamma^r_{rr}=-\frac{f'}{2f},\quad
\Gamma^r_{\theta\theta}=-fr,\quad
\Gamma^r_{\varphi\varphi}=-fr\sin^2\theta,\quad
\Gamma^\theta_{r\theta}=\Gamma^\varphi_{r\varphi}=\frac1r.
\]
Together with \(\Gamma^\theta_{\varphi\varphi}=-\sin\theta\cos\theta\) and \(\Gamma^\varphi_{\theta\varphi}=\cot\theta\), direct substitution in the Ricci formula gives
\[
\operatorname{Ric}(h)_{rr}=-\frac{f'}{rf},\qquad
\operatorname{Ric}(h)_{\theta\theta}=1-f-\frac{rf'}2,
\]
with the \(\varphi\varphi\) component equal to the second expression times \(\sin^2\theta\). Since \(f'=-4a/r^2\), the mixed spatial eigenvalues are
\[
\lambda_r=\frac{4a}{r^3},\qquad
\lambda_\theta=\lambda_\varphi=-\frac{2a}{r^3}.
\]
Their sum is zero. Because \(r^3=\rho^3\phi^6\), these agree with the frozen proof's formula (6), without using its conformal-Ricci calculation.

For any radial scalar \(u(r)\), the mixed Hessian eigenvalues are
\[
(\operatorname{Hess}_h u)^r{}_r=fu''+\frac{f'}2u',\qquad
(\operatorname{Hess}_h u)^\theta{}_\theta
=(\operatorname{Hess}_h u)^\varphi{}_\varphi=\frac{fu'}r.
\]
For \(q=\sqrt f\),
\[
q'=-\frac{2a}{qr^2},\qquad
q''=\frac{4a}{qr^3}-\frac{4a^2}{q^3r^4}.
\]
Consequently the Hessian eigenvalues are \(4aq/r^3,-2aq/r^3,-2aq/r^3\). Hence, identically on the whole interior,
\[
\operatorname{Hess}_h q=q\operatorname{Ric}(h),\qquad
\Delta_hq=0.
\]
This independently establishes the Schwarzschild static-vacuum identity rather than assuming it because the spatial metric is Schwarzschild.

## 3. Full spacetime curvature and invariant singularity

The additional time Christoffel symbols are
\[
\Gamma^t_{tr}=\frac{N'}N,\qquad
\Gamma^r_{tt}=fNN'.
\]
Using
\[
R_{\mu\nu}=\partial_\lambda\Gamma^\lambda_{\mu\nu}
-\partial_\nu\Gamma^\lambda_{\mu\lambda}
+\Gamma^\lambda_{\mu\nu}\Gamma^\kappa_{\lambda\kappa}
-\Gamma^\kappa_{\mu\lambda}\Gamma^\lambda_{\nu\kappa},
\]
one obtains
\[
R_{tt}=N\Delta_hN,\quad R_{ti}=0,\quad
R_{ij}=\operatorname{Ric}(h)_{ij}-N^{-1}(\operatorname{Hess}_hN)_{ij}.
\]
The preceding calculation and \(N=A+Bq\) show that \(\Delta_hN=0\) and \(\operatorname{Hess}_hN=Bq\operatorname{Ric}(h)\). Thus the **scalar curvature is identically zero**, while the mixed Einstein tensor is
\[
G^t{}_t=0,\qquad
(G^r{}_r,G^\theta{}_\theta,G^\varphi{}_\varphi)
=\frac A N\left(\frac{4a}{r^3},-\frac{2a}{r^3},-\frac{2a}{r^3}\right).
\]
All off-diagonal components vanish. For \(A=B=1/2\), \(N=\phi^{-1}\), and this becomes exactly
\[
\left(0,\frac{2a}{\rho^3\phi^5},-\frac{a}{\rho^3\phi^5},-\frac{a}{\rho^3\phi^5}\right).
\]
There is no omitted time pressure or time-energy component.

Put \(\mu=A/N\) and \(\beta=Bq/N=1-\mu\). Squaring the diagonal Ricci tensor yields
\[
R_{\alpha\beta}R^{\alpha\beta}=\frac{24a^2\mu^2}{r^6}.
\]
For the main lapse this is \(6a^2/(\rho^6\phi^{10})\), exactly the claimed formula (10), and it diverges at the inner end. The proof correctly uses a scalar **curvature invariant** for blow-up; it does not claim that the scalar curvature \(R\), which is zero, diverges.

There is also an independent invariant check for every parameter boundary. The spatial orthonormal sectional curvatures are
\[
K_{r\theta}=K_{r\varphi}=\frac{2a}{r^3},\qquad
K_{\theta\varphi}=-\frac{4a}{r^3}.
\]
The squared time-spatial Riemann components are determined by the mixed Hessian eigenvalues of \(N\) divided by \(N\), namely \((4,-2,-2)a\beta/r^3\). Therefore
\[
R_{\alpha\beta\gamma\delta}R^{\alpha\beta\gamma\delta}
=\frac{96a^2}{r^6}(1+\beta^2).
\]
This diverges for **all** allowed family members. In particular, the vacuum case \(A=0\) has vanishing Ricci tensor but Kretschmann invariant \(192a^2/r^6\), so it remains genuinely singular. The ultrastatic case \(B=0\) has Kretschmann invariant \(96a^2/r^6\).

## 4. Index pairing and arbitrary-field contraction

The test object in the proof is a vector field \(\psi^\nu\). On the smooth interior, raising the derivative index means
\[
G_{\mu\nu}\nabla^\mu\psi^\nu
=G_{\mu\nu}g^{\mu\alpha}\nabla_\alpha\psi^\nu
=G^\alpha{}_{\nu}\nabla_\alpha\psi^\nu.
\]
This is a correct tensor contraction, and it is also the contraction in
\[
\nabla_\alpha(G^\alpha{}_{\nu}\psi^\nu)
=(\nabla_\alpha G^\alpha{}_{\nu})\psi^\nu
+G^\alpha{}_{\nu}\nabla_\alpha\psi^\nu.
\]
There is no mistaken transposition of one vector and one covector index.

Lowering \(\psi\) using this singular metric is **not** an operation that preserves smoothness at the retained boundary. Accordingly, this calculation does not silently identify this vector-field test space with a different space of independently smooth covector fields. The frozen proof expressly fixes the vector-field convention, which is the exact analytical assumption being verified here.

Use exterior Cartesian coordinates \(x^i\), set \(n_i=x_i/\rho\), and regard spatial index symmetry below as symmetry with respect to the Euclidean background. Since the radial and angular mixed eigenvalues are as above,
\[
D^i{}_j:=N\phi^6G^i{}_j
=\frac{Aa}{\rho^3}(6n_i n_j-2\delta_{ij}).
\]
This tensor density is independent of \(B\), Euclidean symmetric, trace zero, and smooth up to \(\rho=a>0\). The spacetime density is \(dV_g=N\phi^6\,dt\,d^3x\).

For the conformally Euclidean spatial metric, writing \(p_i=\partial_i\phi\),
\[
\Gamma^j_{ik}=\frac2\phi(\delta^j_i p_k+\delta^j_k p_i-\delta_{ik}p^j).
\]
Then, for each \(k\),
\[
D^i{}_j\Gamma^j_{ik}
=\frac2\phi\bigl((\operatorname{tr}D)p_k+D^i{}_k p_i-D^k{}_j p_j\bigr)=0.
\]
The first term vanishes by trace zero; the second and third cancel by Euclidean symmetry. Also \(\Gamma^j_{it}=0\) and all mixed Einstein components containing a time index vanish. Thus for **every** smooth test vector field, including arbitrary time dependence and angular dependence,
\[
G^\mu{}_{\nu}\nabla_\mu\psi^\nu\,dV_g
=D^i{}_j\partial_i\psi^j\,dt\,d^3x.
\]
The equality is established pointwise for \(\rho>a\) before any integration. It does not multiply distributions or assign values to the degenerate metric on the boundary.

## 5. Absolute convergence, coordinate poles, and separated divergences

A smooth compactly supported vector field on the closed exterior has bounded Cartesian components and bounded first derivatives on a compact set. Because \(a>0\), \(D\) is bounded on that set as well. The displayed contraction density is therefore bounded and compactly supported with respect to the finite Euclidean measure \(dt\,d^3x\). In particular,
\[
\int_M\left|G^\mu{}_{\nu}\nabla_\mu\psi^\nu\right|\,dV_g
=\int_M|D^i{}_j\partial_i\psi^j|\,dt\,d^3x<\infty.
\]
This is the full scalar absolute integrability required in the proof. It is stronger than convergence for one specially chosen radial test.

The Cartesian proof removes all potential spherical-coordinate pole issues. Smooth Cartesian fields can have spherical components whose displayed coordinate derivatives behave badly at poles; that is not a defect in their intrinsic smoothness or in the scalar integral. No boundedness of each spherical component over one global spherical chart is assumed.

Some separated spherical connection contributions are not individually integrable at \(\rho=a\). For the main radial test, the weighted \(\phi'/\phi\) radial term and two angular terms each behave like constants times \(1/(\rho-a)\), but their sum cancels. One must combine the ordinary smooth terms on the interior first. The remaining scalar density is absolutely integrable. The proof follows precisely this valid order and does not invoke a principal value.

## 6. Divergence and flux, with both normal calculations

For a radial/tangential Euclidean tensor density with eigenvalues
\[
D_r=\frac{4Aa}{\rho^3},\qquad D_T=-\frac{2Aa}{\rho^3},
\]
its Cartesian divergence is
\[
\partial_iD^i{}_j=
\left(D_r'+\frac2\rho(D_r-D_T)\right)n_j=0.
\]
One can also check directly from
\[
D^i{}_j=Aa(6x_i x_j\rho^{-5}-2\delta_{ij}\rho^{-3}):
\]
the divergence of the first term is \(-6Aa x_j\rho^{-5}\), and that of the second is \(+6Aa x_j\rho^{-5}\).

Integrate over \(a+\varepsilon<\rho<R\), with time and outer-radius cutoffs outside the support. The outward Euclidean normal on its inner sphere is \(-n\), not \(+n\). Therefore the interior integral equals
\[
-\frac{4Aa}{(a+\varepsilon)^3}
\int_{\mathbb R\times S_{a+\varepsilon}}
\psi_{\rm spatial}\cdot n\,dt\,dA_\delta.
\]
Smoothness at the boundary and the already-proved absolute convergence permit passage to \(\varepsilon\downarrow0\). The result is
\[
\int_MG^\mu{}_{\nu}\nabla_\mu\psi^\nu\,dV_g
=-\frac{4A}{a^2}
\int_{\mathbb R\times S_a}\psi_{\rm spatial}\cdot n\,dt\,dA_\delta.
\]
This verifies the exact sign and all area/Jacobian factors in the proof's formula (16).

For an independent physical-metric normal check, on a tube \(\rho=b\) the outward unit spacelike normal of the truncated exterior has covector component \(\nu_\rho=-\phi^2\), and the induced volume density is \(N\phi^4 b^2\,dt\,d\Omega\). For \(J^\mu=G^\mu{}_{\nu}\psi^\nu\), their product is
\[
J^\rho\nu_\rho\,dS_g
=-N\phi^6 b^2G^\rho{}_\rho\psi^\rho\,dt\,d\Omega
=-\frac{4Aa}{b}\psi^\rho\,dt\,d\Omega.
\]
At \(b\downarrow a\), this again gives \(-4A\int\psi^\rho\,dt\,d\Omega\). Thus neither a lapse factor nor a conformal normal factor is missing.

For \(\psi=\eta(t)\chi(\rho)\partial_\rho\), with \(\int\eta=1\) and \(\chi(a)=1\), the field has boundary normal component \(\eta\), and \(dA_\delta=a^2d\Omega\). Hence the flux is \(-16\pi A\); \(A=1/2\) gives \(-8\pi\). Equivalently, direct spherical contraction gives
\[
G^\mu{}_{\nu}\nabla_\mu\psi^\nu\,dV_g
=4Aa\eta(t)\left(\frac{\chi'}\rho-\frac\chi{\rho^2}\right)
\,dt\,d\rho\,d\Omega,
\]
which is an ordinary derivative of \(4Aa\eta\chi/\rho\) and has exactly the same endpoint value.

## 7. Boundary cases, limits, energy condition, and asymptotics

- **Vacuum boundary \(A=0,B>0\):** \(N=Bq\), \(G=0\), and the defect is zero for all tests. Rescaling time by \(B\) gives the negative-mass Schwarzschild vacuum spacetime. Its Kretschmann scalar still diverges. Thus the claimed vacuum positive control is correct.
- **Ultrastatic boundary \(B=0,A>0\):** \(N=A\), \(G_{\rm spatial}=\operatorname{Ric}(h)\), and the defect is \(-16\pi A\) for the normalized-coordinate-time radial test. There is no lapse blow-up here. The frozen proof restricts its assertion about matching the vacuum's inverse-linear lapse order to \(A,B>0\), so it does not overstate this boundary case.
- **Excluded \(A=B=0\):** The metric would be degenerate on the whole interior, and is expressly excluded. Parameters of opposite sign can cause lapse zeros and are outside the claim.
- **Limit \(A\downarrow0\) at fixed \(B>0\):** The mixed curvature correction tends pointwise to zero away from the singularity, and the full densitized contraction and defect tend to zero exactly linearly in \(A\). Curvature singularity remains in the vacuum Weyl tensor.
- **Limit \(B\downarrow0\) at fixed \(A>0\):** On any compact interior set the metric and curvature converge to the ultrastatic member. The tensor density and flux are unchanged by \(B\). However the inner-end power law is not uniform in this limit: for \(A,B>0\), the Ricci eigenvalues have order \((\rho-a)^{-5}\); at \(B=0\) their order is \((\rho-a)^{-6}\). The proof does not interchange these limits.
- **Null energy condition:** In a static orthonormal frame the energy density is zero. The angular pressure is \(-2a(A/N)/(8\pi r^3)\). For the null vector with time and angular frame components \((1,1)\), \(T(k,k)<0\) whenever \(A>0\). Thus the counterexample violates NEC; within this allowed family NEC holds only at the vacuum boundary \(A=0\). This is consistent with the stated exclusion of an NEC-strengthened conjecture.
- **Asymptotic flatness:** \(q=1+2a/\rho+O(\rho^{-2})\), \(N=A+B+2aB/\rho+O(\rho^{-2})\), and \(\phi^4=1-4a/\rho+O(\rho^{-2})\). After constant time normalization \(\tau=(A+B)t\), the spacetime tends to Minkowski space with \(O(\rho^{-1})\) metric corrections and \(O(\rho^{-2})\) first derivatives. The main lapse already has \(A+B=1\). Nonvacuum Einstein stresses have long-range order \(\rho^{-3}\); no compactly supported matter or integrability at spatial infinity is asserted or required for compact test fields.
- **Timelike inner end:** The general optical derivative is \(ds/d\rho=\phi^2/N\). For \(B>0\) this is asymptotic to \((\rho-a)^3/(2Ba^3)\); for \(B=0\) it is asymptotic to \((\rho-a)^2/(Aa^2)\). Its integral is finite and strictly increasing at the interior end in either case. The radial metric is \(N^2(-dt^2+ds^2)\), so the limiting radial boundary is timelike in precisely the stated conformal sense. The main case gives \(s\sim(\rho-a)^4/(4a^3)\), as claimed.
- **Flat-radius limit \(a\downarrow0\):** This is not part of the fixed-\(a\) theorem, but it does not create a paradox. The chosen radial field \(x/|x|\) is smooth on each retained sphere \(S_a\) and is not uniformly smooth at the collapsed origin as \(a\to0\). For a fixed Cartesian field smooth through the origin, the integral of its constant term against \(n\) vanishes, and the defect is \(O(a)\). More directly, the bulk bound near the shrinking sphere is \(O(a\log(1/a))\). Thus the defect tends to zero for fixed smooth Cartesian tests, consistently with the flat metric limit.

Because a radial boundary-reaching test exists and gives nonzero defect when \(A>0\), whereas \(G=0\) when \(A=0\), the homogeneous identity for every test is indeed equivalent to \(A=0\) within the stated family. Tests supported strictly inside the open exterior or tests with vanishing boundary normal component have zero flux. The counterexample does not purport to apply to those smaller spaces.

## 8. Independent exact computation and its limits

`check_curvature.py` builds the diagonal four-metric and all first and second derivatives at an equatorial coordinate point, including the essential second angular derivative of \(\sin^2\theta\). It then constructs all Christoffel symbols and their derivatives from the metric, contracts Ricci and the full four-dimensional Riemann tensor, and checks the displayed mixed Einstein, scalar-curvature, Ricci-square, Kretschmann, and densitized eigenvalue formulas. It separately constructs the Cartesian density and checks its trace, the contracted connection, its divergence, and the inner-normal sign.

There are **60 exact rational metric cases** including vacuum, ultrastatic, main, and other positive mixed lapses, and **27 exact rational Cartesian cases**, totalling **1,557 explicit exact equalities**. The normal and `-O` runs both pass and produce identical result bytes. Checks use explicit exceptions, so optimization does not remove them. The code imports no frozen author checker or peer code.

These finite tests detect transcription, sign, missing angular derivative, and index-contraction mistakes. They do not certify all parameters, all positions, or all fields. The analytic derivations in sections 1–7 establish those quantified claims.

## 9. Issues and promotion limits

**Mandatory mathematical issues: none. Unresolved analytical gaps: none.**

Optional additions to a future research note:

1. Display the Kretschmann expression \(96a^2r^{-6}(1+(Bq/N)^2)\) if discussing singularity of the entire lapse family, so readers do not mistake vanishing vacuum Ricci curvature for regularity. The current proof needs only the main example's Ricci-square blow-up, which it already proves correctly.
2. State explicitly that covector lowering by the singular metric does not preserve the chosen boundary smoothness, if contrasting different distributional conventions. The current proof consistently uses vector tests and its interior index identity is correct.

These are clarity improvements, not repairs needed for the claimed calculations. Neither source parity nor priority is inferred from this review. Before promoting the result as resolving the specific open problem, the separate source review must verify the precise vector-field test space and the admissibility quantifiers; the priority audit must establish the appropriate historical classification. No foreign full-text sources, invalid fixtures, credentials, or unrelated working files were created or selected in this review.
