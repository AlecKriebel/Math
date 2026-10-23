# A verified five-dimensional counterexample to the centroid-section question

## Result and attribution

The universal assertion that every convex body in every dimension \(n\geq3\) has at least \(n+1\) distinct centroid-preserving hyperplane sections is **false**. The construction of Sergii Myroshnychenko, Kateryna Tatarko, and Vladyslav Yaskin (MTY) gives a counterexample in dimension five, with exactly one such **unoriented** hyperplane.

This is a verification and explanatory reconstruction of their prior work, not a new counterexample or a novelty claim. Their paper is *Answers to questions of Grünbaum and Loewner*, Advances in Mathematics **461** (2025), article 110081, DOI [10.1016/j.aim.2024.110081](https://doi.org/10.1016/j.aim.2024.110081). The directly inspected proof is the ten-page author manuscript [arXiv:2404.15188v2](https://arxiv.org/abs/2404.15188v2), dated 7 November 2024, Theorem 3 on p.4 and its proof on pp.5–8. The publisher PDF was not recovered; no identity of manuscript and publisher bytes, or statement about the publisher's handling of the manuscript issue below, is asserted.

The reconstruction below checks the actual construction. It replaces a misstated Fourier identity in the inspected manuscript by a valid, proved spherical-Radon identity, and replaces the Taylor-remainder step by continuity of an exact integral. These repairs leave MTY's counterexample and credit intact.

## 1. Target and measure conventions

For a compact convex body \(K\subset\mathbb R^5\) with nonempty interior, write

\[
c(K)=\frac{1}{\operatorname{vol}_5(K)}\int_Kx\,dx.
\]

If \(H\) is a hyperplane through \(c(K)\), the centroid of \(K\cap H\) uses ordinary induced four-dimensional Euclidean measure on \(H\). We construct \(c(K)=0\) and prove

\[
c(K\cap u^\perp)=0\quad\Longleftrightarrow\quad u=\pm e_5.
\]

The two normals designate the same hyperplane, so the count is one, rather than two; the proposed lower bound in dimension five is six. This is the centroid specialization, not the question of finding some other suitable interior point, and not a statement about maximum Tukey depth or volume-bisecting sections.

Let \(S^4\subset\mathbb R^5\), \(t(v)=v_5\), and \(\omega=|S^3|=2\pi^2\). All sphere integrals below use unnormalized Euclidean surface measure. Define the spherical Radon transform by

\[
(Rf)(u)=\int_{S^4\cap u^\perp}f(v)\,d\sigma_3(v).
\tag{1}
\]

## 2. Analytic facts used, with normalization checks

### 2.1 Self-adjointness

For continuous functions \(f,h\) on \(S^4\),

\[
\int_{S^4}(Rf)h\,d\sigma_4
=\int_{S^4}f(Rh)\,d\sigma_4.
\tag{2}
\]

Indeed, the incidence measure on ordered perpendicular pairs \((u,v)\) is invariant under exchanging its coordinates. More explicitly, the equatorial integral in (1) is the limit of integrals against an even approximate delta function of \(u\cdot v\); the gradient of \(v\mapsto u\cdot v\) within the sphere has length one on its zero set. The resulting double-integral kernel is symmetric, and Fubini followed by the coarea limit gives (2). Thus no unspecified normalization factor occurs.

### 2.2 A smooth inverse on even functions

The map \(R\) is a bijection from even \(C^\infty(S^4)\) to itself. Here is a spectral verification, including the needed regularity.

On spherical harmonics of degree \(\ell\), its eigenvalue is

\[
\mu_\ell=\omega\frac{C_\ell^{3/2}(0)}{C_\ell^{3/2}(1)},
\tag{3}
\]

where \(C_\ell^{3/2}\) is the Gegenbauer polynomial. To obtain (3), average a harmonic over the rotations fixing a chosen pole. The resulting zonal harmonic is its value at that pole times \(C_\ell^{3/2}(t)/C_\ell^{3/2}(1)\). Its average on the pole's equator is therefore the right side of (3) times that value. Rotation covariance gives the formula at every pole.

Odd eigenvalues are zero, while for \(\ell=2k\),

\[
\mu_{2k}=\omega(-1)^k\frac{\mathrm{Cat}_k}{4^k},
\qquad
\mathrm{Cat}_k=\frac{1}{k+1}\binom{2k}{k}>0.
\tag{4}
\]

For example, \(\mu_0=\omega\) and \(\mu_2=-\omega/4\), consistent with direct integration of constants and quadratic harmonics. The central binomial coefficient is the largest among the \(2k+1\) coefficients whose sum is \(4^k\); hence

\[
|\mu_{2k}|^{-1}\leq\frac{(k+1)(2k+1)}{\omega}.
\tag{5}
\]

Smooth functions have spherical-harmonic coefficients decreasing faster than any polynomial. This follows by repeated integration by parts with the spherical Laplacian, whose degree-\(\ell\) eigenvalue is \(-\ell(\ell+3)\); the standard finite-dimensional harmonic derivative bounds then give convergence in every derivative. Dividing the even coefficients by (4) preserves this rapid decrease by (5). It defines a unique even smooth inverse \(R^{-1}\). This proof also shows continuity of the inverse in smooth seminorms and that it commutes with rotations. Only the inverse of two fixed smooth functions and their linear combinations will be needed.

Self-adjointness also holds for this inverse on even smooth functions: substitute \(f=R^{-1}a\), \(h=R^{-1}b\) into (2).

### 2.3 The ellipsoid integral

For a positive definite \(5\times5\) matrix \(A\), define \(f_A(v)=(v^TAv)^{-2}\) on the sphere. Then

\[
(Rf_A)(u)
=\omega(\det A)^{-1/2}(u^TA^{-1}u)^{-1/2}.
\tag{6}
\]

To prove this, intersect \(\{x:x^TAx\leq1\}\) with \(u^\perp\). Its four-volume is the volume of the four-ball divided by the square root of the determinant of the restriction of \(A\) to \(u^\perp\). The determinant of that restriction is \(\det A\,(u^TA^{-1}u)\), by the block determinant/Schur complement identity in an orthonormal basis ending in \(u\). Polar integration in the four-dimensional hyperplane identifies four times the same volume with \(Rf_A\). Since four times the four-ball volume is \(2\pi^2=\omega\), (6) follows.

These facts suffice for the construction without appealing to an intersection-body characterization or an uninspected Fourier-analysis textbook lemma.

## 3. A quantitatively convex MTY seed

Fix

\[
a=\frac1{100},\qquad b=a^{-2}-1,
\qquad r(t)=1-2a^3(1+bt^2)^{-1/2}.
\tag{7}
\]

Let \(M\) be the radial body with radius \(r(t(v))\). This is MTY's seed on p.5, specialized to dimension five. It is smooth, invariant under rotations of the first four coordinates, and origin-symmetric. Its radius is at least \(1-2a^3>0\), so it is compact and contains a ball about zero.

For completeness, its convexity follows from an explicit estimate. Write \(q(t)=2a^3(1+bt^2)^{-1/2}\), so \(r=1-q\). Direct differentiation gives

\[
|q|\leq2a^3,\quad |q'|\leq2a^2,\quad |q''|\leq8a.
\tag{8}
\]

For the last two bounds, set \(y=\sqrt b\,t\), use \(\sqrt b\leq a^{-1}\) and \(b\leq a^{-2}\), and bound the resulting functions \(|y|(1+y^2)^{-3/2}\), \((1+y^2)^{-3/2}\), and \(y^2(1+y^2)^{-5/2}\) by one. On \(S^4\), \(|\nabla t|\leq1\) and \(\nabla^2t=-tI\), so

\[
\|\nabla^2r\|\leq8a+2a^2,
\qquad
\min r-\|\nabla^2r\|\geq
1-2a^3-8a-2a^2=\frac{459899}{500000}>0.
\tag{9}
\]

Here and below the Hessian norm is the operator norm, and a uniform upper bound can replace its pointwise value.

To connect this estimate to global convexity, set \(f=1/r\) on the sphere and \(F(x)=|x|f(x/|x|)\) for \(x\ne0\), with \(F(0)=0\). The tangential block of the Euclidean Hessian of this homogeneous gauge is a positive scalar multiple of

\[
\nabla^2f+fI
=r^{-2}(rI-\nabla^2r)+2r^{-3}\nabla r\otimes\nabla r,
\tag{10}
\]

which is positive definite by (9). Homogeneity makes the radial direction a null direction of the Hessian. Thus the restriction of \(F\) to every line not crossing zero is convex. On a line crossing zero, its left slope is \(-F(-v)<0\) and its right slope is \(F(v)>0\); the slope jump is also convex. Consequently \(F\) is globally convex and \(M=\{F\leq1\}\) is a convex body, with a strict positive curvature margin. The same argument works for sufficiently small \(C^2\) perturbations of \(r\), including non-even perturbations.

By (6), an explicit inverse-Radon image of \(r\) is

\[
w_M(t)=\frac1\omega\left[1-2a^4\bigl(1-(1-a^2)t^2\bigr)^{-2}\right],
\qquad Rw_M=r.
\tag{11}
\]

In particular \(w_M(\pm1)=-1/\omega<0\). This is the sign-changing-transform feature of MTY's non-intersection-body seed; it has been checked directly here rather than inferred from that terminology.

## 4. The sign-changing volume-moment parameter

Put

\[
\delta=\frac{a^2}{4(1-a^2)}=\frac1{39996},\qquad z_0=1-\delta,
\]

and define the even axial smooth bump

\[
G(t)=
\begin{cases}
(1-t^2)\exp\!\left(-\dfrac{\delta}{t^2-z_0}\right),&t^2>z_0,\\
0,&t^2\leq z_0.
\end{cases}
\tag{12}
\]

It is smooth across the cap boundaries because the exponential is flat there. It is smooth at the poles because it is a smooth function of \(t\) near each pole. It vanishes at the poles and outside the caps, and is positive in each punctured cap. On its support,

\[
1-(1-a^2)t^2\leq\frac54a^2,
\qquad w_M(t)\leq-\frac7{25\omega}<0.
\]

The support has positive spherical measure. Therefore

\[
\int_{S^4}w_MG\,d\sigma_4<0.
\tag{13}
\]

Use precisely MTY's positive companion function,

\[
H(t)=1-(4-3t^2)^{-1/2}.
\tag{14}
\]

It is positive away from the poles and zero at the poles. Equation (6), now with \(A=\operatorname{diag}(1,1,1,1,4)\), gives

\[
w_H(t)=\frac1\omega[1-(1+3t^2)^{-2}],
\qquad Rw_H=H.
\tag{15}
\]

The function \(w_H\) is nonnegative and positive when \(t\ne0\). Using (2), (11), and (15),

\[
\int_{S^4}w_MH\,d\sigma_4
=\int_{S^4}(Rw_M)w_H\,d\sigma_4
=\int_{S^4}r\,w_H\,d\sigma_4>0.
\tag{16}
\]

For \(0\leq\lambda\leq1\), set

\[
g_\lambda=(1-\lambda)G+\lambda H,
\qquad Q_\lambda=R^{-1}g_\lambda.
\tag{17}
\]

For every \(0<\lambda\leq1\), \(g_\lambda\) is positive at every nonpolar direction and zero precisely at the two poles. The function \(Q_\lambda\) is even, smooth, axial, and linear in \(\lambda\).

## 5. The equatorial division is smooth

Axial invariance makes \(Q_\lambda\) constant on the equator. Evaluate \(RQ_\lambda=g_\lambda\) at \(e_5\):

\[
\omega Q_\lambda(t=0)=g_\lambda(e_5)=0.
\tag{18}
\]

Near the equator, write \(Q_\lambda(v)=\psi_\lambda(t(v))\). This is a smooth one-variable representation because rotations of the first four coordinates act transitively on every latitude. Antipodal evenness together with axial invariance gives \(\psi_\lambda(-t)=\psi_\lambda(t)\). Thus both \(\psi_\lambda(0)\) and \(\psi_\lambda'(0)\) vanish. Taylor's integral formula gives

\[
\psi_\lambda(t)=t^2\int_0^1(1-s)\psi_\lambda''(st)\,ds.
\]

Consequently

\[
\phi_\lambda(v)=
\begin{cases}Q_\lambda(v)/t(v),&t(v)\ne0,\\0,&t(v)=0\end{cases}
\tag{19}
\]

is smooth and odd, including at the equator. It is axial, and all its derivatives are uniformly bounded for \(\lambda\in[0,1]\), because \(\phi_\lambda=(1-\lambda)\phi_0+\lambda\phi_1\). The order-two vanishing uses axial invariance as well as antipodal evenness. Merely being even and vanishing on a hyperplane would not by itself justify setting this quotient equal to zero there.

## 6. The perturbed bodies really are convex bodies

Define, for sufficiently small \(\varepsilon\geq0\),

\[
\rho_{\lambda,\varepsilon}(v)
=\bigl(r(t(v))^5+\varepsilon\phi_\lambda(v)\bigr)^{1/5},
\quad
K_{\lambda,\varepsilon}
=\{sv:v\in S^4,\ 0\leq s\leq\rho_{\lambda,\varepsilon}(v)\}.
\tag{20}
\]

Since \(r\geq1-2a^3>0\) and \(\phi_\lambda\) is uniformly bounded, there is an \(\alpha>0\) for which the expression inside the fifth root is bounded below by a positive constant for all \(\lambda\in[0,1]\), \(\varepsilon\in[0,\alpha]\). Reduce \(\alpha\) if needed. The radii then converge to \(r\) in \(C^2\), uniformly in \(\lambda\), as \(\varepsilon\to0\). The strict margin (9), or equivalently the positive definite matrix (10), persists uniformly. Thus (20) defines compact convex bodies with nonempty interior throughout this parameter rectangle. In fact they are smooth and strictly convex, although neither additional property is required by the target.

Each body is invariant under every orthogonal transformation of its first four coordinates. Its volume centroid therefore has zero first four coordinates; only the fifth first moment remains to be set to zero.

## 7. Exact section moments control every direction

Fix any \(u\in S^4\). Polar integration within the four-dimensional Euclidean hyperplane \(u^\perp\) gives

\[
\begin{aligned}
\int_{K_{\lambda,\varepsilon}\cap u^\perp}x_5\,d\operatorname{vol}_4(x)
&=\frac15\int_{S^4\cap u^\perp}t(v)\rho_{\lambda,\varepsilon}(v)^5\,d\sigma_3(v)\\
&=\frac\varepsilon5\int_{S^4\cap u^\perp}Q_\lambda(v)\,d\sigma_3(v)\\
&=\frac\varepsilon5 g_\lambda(u).
\end{aligned}
\tag{21}
\]

The seed term disappears because \(t\,r^5\) is odd on an antipodally symmetric equator. The identity \(t\phi_\lambda=Q_\lambda\) holds on the entire sphere, including the equator by (18). Thus the calculation has no excluded directions, singular integrands, limiting directions, or finite direction-sampling step.

For \(\varepsilon>0\) and \(0<\lambda<1\), (21) is strictly positive unless \(u=\pm e_5\). Every section contains a four-dimensional ball about zero since the body contains a five-dimensional ball. Its four-volume is positive and finite. Dividing (21) by that positive volume proves that every nonpolar section centroid has strictly positive fifth coordinate, and in particular cannot be the origin.

For the remaining hyperplane \(e_5^\perp\), equation (19) gives \(\phi_\lambda=0\), while \(r(0)=1-2a^3\) is constant. Its section is exactly the four-ball of radius \(1-2a^3\) centered at zero. All five coordinates of its centroid therefore vanish. This explicitly verifies the tangential coordinates, rather than inferring an entire centroid from a single zero coordinate.

## 8. The ordinary volume centroid is exactly zero

Let

\[
J(\lambda,\varepsilon)
=\int_{K_{\lambda,\varepsilon}}x_5\,dx
=\frac16\int_{S^4}t(v)\bigl(r^5+\varepsilon\phi_\lambda\bigr)^{6/5}\,d\sigma_4(v).
\tag{22}
\]

At \(\varepsilon=0\), \(J=0\) by symmetry. The fundamental theorem of calculus, with all fifth-root arguments bounded uniformly away from zero, gives the exact identity

\[
J(\lambda,\varepsilon)=\frac\varepsilon5 F(\lambda,\varepsilon),
\quad
F(\lambda,\varepsilon)
=\int_{S^4}Q_\lambda(v)
\int_0^1\bigl(r^5+s\varepsilon\phi_\lambda\bigr)^{1/5}\,ds\,d\sigma_4(v).
\tag{23}
\]

The formula for \(F\) is also defined at \(\varepsilon=0\), and is jointly continuous on \([0,1]\times[0,\alpha]\). There is no division by \(\phi_\lambda\), and no transformed remainder whose parameter continuity must be established. At zero,

\[
F(\lambda,0)=\int_{S^4}rQ_\lambda\,d\sigma_4
=\int_{S^4}w_Mg_\lambda\,d\sigma_4,
\tag{24}
\]

where the last equality is (2) and (11). Equations (13) and (16) give

\[
F(0,0)<0<F(1,0).
\]

Continuity preserves these strict endpoint inequalities for every sufficiently small positive \(\varepsilon\). Fix any one such \(\varepsilon_0\leq\alpha\). The intermediate value theorem in \(\lambda\) supplies a \(\lambda_0\in(0,1)\) with \(F(\lambda_0,\varepsilon_0)=0\). Equations (22)–(23) then give zero fifth volume first moment. The other four moments vanish by the rotational symmetry already proved. The body has positive finite volume, so

\[
c(K_{\lambda_0,\varepsilon_0})=0.
\tag{25}
\]

Together, (21), the polar four-ball check, and (25) establish exactly one distinct unoriented centroid-preserving hyperplane. This completes the dimension-five counterexample and negates the universal target.

## 9. Relation to the inspected MTY proof and the repaired statement

The construction uses the same seed, the same positive companion \(H\), the same two-endpoint moment argument, and the same odd perturbation of the fifth power of the radial function as MTY. The bump in (12) is simply one explicit choice satisfying their p.5 conditions. The inverse-Radon normalization replaces their homogeneous Fourier normalization by a positive constant, which is absorbed into the small parameter \(\varepsilon\).

With MTY's convention \(\widehat f(y)=\int f(x)e^{-ix\cdot y}\,dx\), define

\[
Tf=\left.\widehat{\,|x|^{-1}f(x/|x|)\,}\right|_{S^4}
\]

for even smooth \(f\). The correct minimal Fourier identity used by their proof is

\[
\int_{S^4}(Tf)h\,d\sigma_4=\int_{S^4}f(Th)\,d\sigma_4
\quad\text{for even smooth } f,h,
\tag{26}
\]

where **both homogeneous extensions have degree \(-1\)**. Indeed their valid Fourier/Radon formula on p.3, equation (1), and Fourier inversion yield \(RT=((2\pi)^5/\pi)I=32\pi^4I\), so \(T=32\pi^4R^{-1}\); (26) follows from the proved self-adjointness of \(R^{-1}\). The inverse-Radon construction above does not require Fourier inversion to establish the counterexample; this observation identifies the normalizations and the valid replacement lemma in the original presentation.

**Author-manuscript issue, verified against the rendered p.3.** The hypotheses printed immediately before MTY equation (5) give complementary homogeneous degrees \(-k\) and \(-5+k\), yet the displayed equality is not true under those hypotheses. Set \(f(x)=|x|^{-1}\) and \(h(x)=|x|^{-4}\). Their transforms restrict on \(S^4\) to \(16\pi^2\) and \(2\pi^3\), respectively. Thus the two asserted integrals would be \(16\pi^2|S^4|\) and \(2\pi^3|S^4|\), which are unequal. The constants also follow directly from the radial Fourier formula in Yaskin's cited precursor, author PDF p.3.

The actual applications on MTY pp.6 and 8 use same-degree \(-1\) extensions, and are valid under (26). Therefore this is a repairable formulation/citation mismatch in the inspected author manuscript, not an obstruction to Theorem 3. Nothing here asserts whether the journal version repeats or corrects it.

Two further clarifications close compressed steps in the manuscript:

- Its p.6 quotient needs the axial symmetry and evenness argument of Section 5, including order-two vanishing; all those hypotheses are present in the construction.
- Its p.5 strict comparison of the two inverse quadratic radii has equality on the equator. The needed positivity follows instead from \(r\geq1-2a^3>0\), so this harmless strictness overstatement has no effect on the construction.

## 10. Source and dependency pins

1. **MTY, arXiv:2404.15188v2, 7 November 2024:** [versioned PDF](https://arxiv.org/pdf/2404.15188v2). Entire ten-page text inspected; key mathematical pages 3 and 5–8 also inspected as rendered images. Page 1: centroid definition and exact problem. Pages 2–3: transform conventions. Page 4: Theorem 3. Page 5: seed, convexity lemma, negative transform, bump. Page 6: companion function, parameter and quotient. Page 7: exact section moment and volume moment. Page 8: endpoint choice. Pages 9–10: references. PDF length 167,961 bytes; SHA-256 `970f4af59ffb9cd4d24530b8614c57b4391a269efa966100665dfe9e2fda9b46`.
2. **Vladyslav Yaskin, *On strict inclusions in hierarchies of convex bodies*.** [Author-hosted PDF](https://www.math.ualberta.ca/~vladyaskin/papers/inclusions.pdf); published citation Proc. Amer. Math. Soc. **136** (2008), 3281–3291, DOI [10.1090/S0002-9939-08-09424-0](https://doi.org/10.1090/S0002-9939-08-09424-0). The recovered author PDF is ten pages; pp.2–4 were inspected for Theorem 2.2 and Lemmas 2.3–2.5. With \(k=1\), \(m=4\), ambient dimension five, its construction is exactly the dimension-five seed in (7), with its small parameter renamed \(a\). Page 3 gives the general radial Fourier constants used to check the manuscript issue. This seed's convexity and transform calculations were nevertheless re-proved above, rather than relying on the precursor's perturbation assertion. PDF length 201,198 bytes; SHA-256 `76537d725c0ecdc407f0aa6a2c60a2e9621cd174aa7c301efef11780ec4a4291`. This is an author-hosted version, not a claimed byte-identical publisher PDF.
3. **Publication identity:** MTY's publication is listed among the 2025 published papers on [Yaskin's institutional author page](https://www.math.ualberta.ca/~vladyaskin/). The primary [arXiv version page](https://arxiv.org/abs/2404.15188v2) verifies the v2 date and authorship. These metadata were rechecked on 14 October 2026.

The self-adjointness, inverse-Radon regularity needed here, ellipsoid integral, convexity estimate, smooth quotient, exact section moments, and centroid adjustment were justified in this report. No uninspected result concerning the classification of intersection bodies is necessary to this dimension-five certificate.

## 11. Scope and verdict

**Verified:** the MTY construction supplies a smooth convex body in \(\mathbb R^5\) with nonempty interior, ordinary volume centroid zero, exactly one unoriented hyperplane through zero whose induced-measure section centroid is zero, and a strict positive fifth section moment for every other direction. The universal \(n\geq3\) claim is therefore false, already by credited prior work.

**Not claimed:** an explicit closed-form value of the small perturbation parameter or the intermediate-value root; a sampled numerical proof of all directions; a new mathematical result; certification of dimensions three or four from this construction; inspection of the MTY version-of-record PDF; or byte equivalence of any author and publisher versions. The existential parameter choice is rigorous and sufficient for the target. The manuscript's stated extension to every \(n\geq5\) is consistent with the same proof structure; this report's fully worked certificate is dimension five, which alone suffices.

The author-manuscript equation-(5) formulation requires the correction stated in Section 9. With that explicit repair, no remaining mathematical gap in the sufficient dimension-five counterexample was found.
