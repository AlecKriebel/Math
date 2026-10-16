# Independent review: analytic closure criterion for ellipsoid null chains

**Verdict: PASS_COMPLETE_ANALYTIC_CRITERION.** The global coordinates, null-arc return map, period identity, parameter classification, and pole correction check out. No mandatory mathematical correction is requested. The result gives an explicit necessary-and-sufficient condition for the source's literal chain-existence question. It does **not** give a polynomial Cayley determinant or an algebraic torsion criterion.

Recommended campaign status: **claimed_solved, 1/5**, qualified as an analytic integral criterion for the literal parameter-condition request. A specifically algebraic Cayley-formula problem remains unclaimed. Historical priority is unconfirmed, and this separate adversarial AI review is not human peer review.

## 1. Exact requested output and its limits

I read and visually inspected Section 7, printed p. 62, of [Tabachnikov, *A Baker's Dozen of Problems*](https://armj.math.stonybrook.edu/pdf-Springer-final/014-0001-3.pdf). The exact problem sentence is:

> “Find conditions on the numbers a,b,c ensuring the existence of (n,r)-chains.”

The surrounding text specifies $a,b,c>0$, the ellipsoid $x^2/a+y^2/b+z^2/c=1$, the ambient metric $dx^2+dy^2-dz^2$, and alternating null arcs running between the two tropics. The section's heading invokes Cayley's theorem, and the following sentence points to Cayley's classical Poncelet formula. Neither the problem sentence nor the adjoining mathematical hypotheses explicitly requires a determinant, polynomial, or algebraic expression.

This matters for disposition. The candidate's equation
\[
\frac1{2\pi}\int_0^{2\pi}
\sqrt{\frac{a\sin^2t+b\cos^2t}{c+a\sin^2t+b\cos^2t}}\,dt
=\frac{n}{n+2r}
\tag{R1}
\]
together with **even $n$ for literal full tropic-to-tropic arcs**, is an explicit parameter-only necessary-and-sufficient condition. Its integration bounds are fixed and its integrand is nonsingular. It contains no unknown orbit, endpoint, or unspecified translation constant. Thus it answers the literal parameter-condition request; it is more than the tautological condition that an unknown rotation number be rational.

It would nevertheless be inaccurate to advertise the result as an algebraic Cayley formula. The source's motivating comparison makes that a natural stronger goal, and the candidate explicitly leaves it unresolved. The recommended status above is tied to the exact sentence quoted here, not to a claim that an algebraic characterization has been produced or that the historical intended output format has been conclusively established.

I also read [Genin–Khesin–Tabachnikov (GKT)](https://arxiv.org/abs/0705.0188), Sections 1–5, and visually checked the equator-map definition and Problem 5.2 on manuscript pp. 17–18. GKT counts iterates of a folded equator map. The later literal full-arc convention has a parity condition absent from that folded map. The artifact gives both conventions explicitly and correctly.

## 2. Frozen snapshot and controls

- ANALYTIC_CRITERION.md: 608217a2ffc120a965b165f5b6065edd83f8cf94c5e77f0f95a0326640db2dae
- Submitted verify.py: 4c3c7d42bff5772827044916fd7b62cfa3fa8e2be2a08b9788ec8bcd91be2040
- Submitted receipt: 25285a5225810bf4be4b716b6f5f505605087eb742021b236a3f1616d79b410f
- **2,087 submitted exact controls** reproduced with byte-identical output
- **752 independent exact diagnostics** passed

The review used gpt-6-astra at xhigh reasoning on 2026-09-30. No author mathematical file was edited. Finite algebra does not prove global coordinate coverage or contour deformation; those arguments are audited below.

## 3. Global belt coordinates and endpoint gluing

Write $f^2=b+(a-b)\sin^2t$ and $D=(a+c)(b+c)$. The parametrization (6) lies on the ellipsoid by direct substitution. The root equation (7) has strictly negative derivative in $v$ wherever $x,y$ are not both zero. On the closed Lorentz belt they cannot both vanish. Its values at the endpoints satisfy
\[
F(0)-1=c\left(\frac{x^2}{a^2}+\frac{y^2}{b^2}-\frac{z^2}{c^2}\right),
\qquad
F(c)-1=-\frac{z^2}{c}.
\]
Thus it has a unique root in $[0,c]$ exactly on the belt, and signed sine and cosine recover $t$ modulo $2\pi$. This is a global coverage argument; no choice of signs in local pseudo-confocal square roots is left unresolved.

Independently differentiating the three Cartesian coordinate functions gives
\[
g_{tt}=(v+f^2)\frac{f^2}{c+f^2},\qquad
g_{tv}=0,\qquad
g_{vv}=-\frac{(v+f^2)v}{4(a+v)(b+v)(c-v)}.
\]
For $0<v<c$ these coefficients have Lorentz signature and are nondegenerate. The formulas are regular in $a,b>0$ and do not exclude $a=b$. The meridians where a sine or cosine vanishes are covered by the original smooth Cartesian expressions; divisions introduced in a squared-coordinate calculation do not remove them.

The signed equator gluing is valid. With $\varepsilon=c-v$,
\[
H-\tau(v)=\sqrt{\frac cD}\,\sqrt{\varepsilon}\,
( \sqrt{\varepsilon})\,O(\varepsilon),
\qquad
z=\sqrt{\frac{c(c+f^2)}D}\,\sqrt{\varepsilon}
\]
on the north side. The first factor multiplying $\sqrt\varepsilon$ is analytic in $\varepsilon$ and nonzero. Therefore the signed $Y$ is smooth across $z=0$, with leading ratio
$Y/z=1/\sqrt{c+f^2}$. Using the signed square-root coordinate instead of $v$ also verifies that the equator is a regular chart, rather than a second copy or a coordinate singularity of the surface.

At a tropic,
\[
\tau(v)=\frac{v^{3/2}}{3\sqrt{abc}}+O(v^{5/2}).
\]
It remains continuous and strictly increasing up to the endpoint. This gives a homeomorphism of the closed belt with the closed cylinder, while the smooth conformal metric statement is only made on its interior. The degeneracy and cusp behavior at the tropic are retained. No nonsingular Lorentz metric on the polar caps is being assumed.

## 4. Null trajectories, winding, and the factor of two

On the interior cylinder the metric is a positive scalar multiple of $dS^2-dY^2$. Hence its two null line fields are exactly $dS/dY=\pm1$. For a nonzero null tangent on a Lorentz surface, its acceleration is orthogonal to that tangent and therefore collinear with it; the corresponding integral curve is a geodesic after reparametrization. This establishes the required unparameterized null arcs.

An arc reaches each cylinder boundary in finite $S$ advance. At a tropic, switching null families and retaining the chosen positive angular direction reflects the straight line; retracing the same incoming family would instead reverse that direction. This supplies the alternating chains of the source.

The equator is $Y=0$ and the two tropics are $Y=\pm H$. The equator-to-north-to-equator map advances $S$ by $H+H=2H$. A full north-to-south or south-to-north arc also advances $S$ by $2H$. Therefore the normalized lifted advance is
\[
\rho=\frac{2H}{L}.
\]
No additional factor of two is missing.

The coordinate $t$ has the ordinary winding number. Indeed the $xy$ projection is
$(A(v)\cos t,B(v)\sin t)$ with $A(v),B(v)>0$. Homotoping these positive scale factors to one keeps the projection away from the origin, so its degree equals that of $e^{it}$. Since $S(t+2\pi)=S(t)+L$, a closed path with total $S$ advance $rL$ winds exactly $r$ times.

For GKT's folded equator map, $n$ iterations close with winding $r$ precisely when $n(2H)=rL$. For literal full arcs, every step changes which tropic contains the endpoint, so closure additionally requires even $n$. Conversely, the same advance equation and even parity return to the same point and the same outgoing alternating-arc state.

The least folded-map period is the denominator $q$ of $\rho=p/q$ in lowest terms. The least full-arc period is $\operatorname{lcm}(2,q)$. In particular a folded-map period of one can correspond to a two-arc chain, and applying the coprimality rule for the folded map to a literal chain would be wrong. The candidate explicitly avoids that error. Positive advance excludes zero winding for a nontrivial closed chain; reversing the direction reverses its sign.

An independent axisymmetric derivation confirms the normalization. For $a=b=A$, ordinary latitude coordinates give the equator-to-tropic angular advance
\[
\int_0^{\sqrt{c/A}}\frac{\sqrt{c/A-u^2}}{1+u^2}\,du
=\frac{\pi}{2}\left(\sqrt{1+c/A}-1\right).
\]
One folded step doubles this quantity, so $\rho=(\sqrt{1+c/A}-1)/2$, exactly the candidate formula. For example $c=3A$ gives a two-full-arc, one-winding closure; $c=8A$ gives folded period one but least full-arc period two, with winding two.

## 5. Contour identity and the parameter classification

For $a>b$, the substitution $u=-f(t)^2$ on a quadrant gives $I_u=L/2$: the Jacobian supplies a factor of two on a quadrant, while $L$ is four times its quadrant integral.

The branch
\[
R(z)=\sqrt{z(z+a)(z+b)(z-c)},\qquad R(z)\sim z^2,
\]
is single-valued on the plane cut along $[-a,-b]\cup[0,c]$. Each cut pairs two branch points. Its branch signs in the proof are correct. On the upper bank of $[0,c]$, $R$ is positive imaginary; on the upper bank of $[-a,-b]$, it is negative imaginary. Multiplying by the numerator $z$ therefore makes $z/R(z)$ equal to $-i$ times the respective positive real integrand on **both** upper banks.

A counterclockwise loop around a slit traverses the upper bank from right to left, so its integral is $2iI_u$ or $2iI_v$. The differential behaves as $dz/z$ at infinity. All finite endpoint singularities are integrable; at zero the numerator further softens the branch singularity. Deforming a large counterclockwise contour onto the two slits gives
\[
I_u+I_v=\pi.
\]
With $I_v=2H$ this proves $\rho=\pi/L-1/2$, and therefore the stated mean formula and (R1).

At $a=b$, the mean and the second integral vary continuously. In a compact positive parameter neighborhood their endpoint singularities have a common integrable bound, so the limiting argument is legitimate; the direct axisymmetric calculation supplies a separate verification. Interchanging the two spatial axes corresponds to shifting $t$ by $\pi/2$, covering $a<b$.

Differentiating the strictly positive integrand in $c$ gives the negative derivative claimed. Its limits are one at $c\downarrow0$ and zero at $c\to\infty$. Thus each positive target ratio determines exactly one positive $c$ for fixed $a,b$. This classification is for the mean equation; the full-arc existence statement still retains even $n$. Analytic dependence follows from local analyticity of the integrand on the positive parameter domain and the nonzero derivative. Scaling all three parameters by the same positive constant leaves the equation unchanged.

The strict bounds obtained by comparing $f^2$ with $b$ and $a$ are correct when $a>b$. No claim at an excluded zero axis or at $c=0$ is used.

## 6. Imported elliptic-torsion inference

The candidate correctly identifies a specific error in the preserved prior report. For $a>b>0$, the quartic in (15) has four distinct branch points, so its compactification is an elliptic curve with two points over infinity. At either such point, using $\zeta=1/w$ and $y\sim\pm iqw^2$ gives
\[
dS=\left(\frac{\pm i}{2}\frac1\zeta+O(1)\right)d\zeta.
\]
The residues are nonzero and opposite. The differential is consequently of the third kind; it is neither the claimed second-kind differential nor the holomorphic differential defining the ordinary Abel–Jacobi coordinate.

It therefore does not follow from a real invariant-density translation that the return map is ordinary elliptic-group translation by an algebraic point with a division-polynomial test. The artifact rejects precisely that unsupported inference. It does not prove the nonexistence of some different algebraic formulation, generalized-Jacobian interpretation, or Cayley-type condition.

The [Wüstholz 2017 slides](https://viasm.edu.vn/Cms_Data/Contents/viasm/Media/file/billards_halong2017.pdf) were read in their period context and final null-geodesic section. They announce an arithmetic result for ellipsoids defined over a number field and mention additional Jacobian conditions. They do not provide a full proof of the present real-parameter classification or justify the prior report's ordinary-torsion shortcut. The candidate accurately preserves those access and scope limits. This review certifies no first-discovery claim.

## 7. Reproduction and final disposition

From this review directory:

    python3 independent_checks.py
    python3 author_replay/verify.py > author_replay/replayed_verification.json
    cmp author_replay/verification.json author_replay/replayed_verification.json

Both scripts use SymPy. The independent checker differentiates the metric through a separate formula, checks coordinate endpoints and gluing coefficients, derives the axisymmetric factor, explicitly iterates the boundary state, and independently verifies the slit signs and Laurent residues. These are diagnostics supporting the mathematical audit above.

**Final recommendation: claimed_solved, 1/5, for an explicit analytic necessary-and-sufficient criterion answering the literal Section 7 parameter question.** Preserve the even-arc convention, exact positive-parameter domain, classical GKT credit, and unconfirmed priority. Do not say that an algebraic Cayley determinant, ordinary elliptic torsion condition, or the stronger algebraic-output interpretation has been solved. No mandatory correction to the frozen mathematical artifact is required.
