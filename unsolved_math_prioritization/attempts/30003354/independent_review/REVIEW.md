# Independent adversarial review: 30003354 / OWR-15208-008

**Verdict: PASS for the complete candidate counterexample, for every finite integer $r\geq0$, on both the plane and the sphere. No mandatory mathematical correction was found.** The constructed metrics meet the smoothness, completeness and strictly positive-curvature requirements. This is an independent AI review, not human peer review or a historical-priority certificate.

Reviewed on 2026-09-30 using gpt-6-astra with xhigh reasoning. The reviewed CANDIDATE.md has SHA-256

7f358fb1aaa73dc3cfd06c798c10f6afed65ee430b622b84b90f0554dd440e62.

The snapshot and the submitted checker are preserved in [author_replay/](author_replay/). No author mathematical file was edited.

## 1. Exact source question

I read Belegradek's complete contribution in [OWR 3/2017](https://ems.press/doi/pdf/10.4171/OWR/2017/3), pp.148–151, and visually inspected p.149. The normalization fixes 0 and 1 on the plane, and 0, 1 and infinity on the sphere. The question concerns the specified conformal parametrization of smooth complete nonnegatively curved metrics.

The full [2016 Belegradek–Hu erratum](https://doi.org/10.1007/s00208-015-1354-1) explicitly corrects the regularity indices: metrics and conformal factors carry $C^{k+\alpha}$ topology, while diffeomorphisms carry $C^{k+1+\alpha}$ topology. Its unresolved endpoint is $\alpha=0$ at finite integer $k$. [Banakh–Belegradek, Sections 2, 8–9](https://arxiv.org/abs/1510.07269v2), independently specifies the compact-open topologies on smooth objects and the same derivative shift.

The workshop's abbreviated action notation does not change this target. Pullback by a diffeomorphism and pushforward by its inverse give equivalent parametrizations because inversion is a homeomorphism of the relevant diffeomorphism groups. The candidate's pullback convention is explicit and consistent throughout.

The conclusion does not assert that the metric spaces have no other homeomorphism to a product, nor does it contradict the known noninteger Hölder or $C^\infty$ statements.

## 2. Uniform logarithmic estimates for all fixed $r\geq1$

The all-$r$ estimates are valid, rather than being inferred from the finite symbolic tests.

For $s=(|z|^2+\rho^2)^{1/2}$, every positive-order derivative of $\log s$ is homogeneous of degree equal to minus its order in $(x,y,\rho)$. On the unit upper half-sphere its rational expression has a nonzero denominator and is bounded. This proves the uniform derivative bound used in (4.2), including the limit toward $\rho=0$ away from the spatial origin.

Leibniz's rule then yields the stated bounds for $z^{r+1}\log s$. The term with no derivative on the logarithm is the only one retaining a logarithm. On the inner disk, for every fixed $r\geq1$, the expression $s^r(1+|\log s|)$ is uniformly bounded. This gives $Df_n-I=O(1/n)$. The derivatives through order $r$ of $(f_n)_z$ are uniformly bounded because the largest remaining logarithm is at most $n+O(1)$, canceled by $1/n$.

The direct formula for $(f_n)_{\bar z}$ has no logarithm. Its order-$k$ derivatives, for $k\leq r$, are bounded by $C_r n^{-1}s^{r-k}$. On the fixed cutoff annulus, all relevant derivatives are uniformly $O(1/n)$. Since $(f_n)_z$ stays away from zero and has a bounded $C^r$ norm, the finite reciprocal/product rules prove $\|\mu_n\|_{C^r}=O(1/n)$.

The bad top jet is exact. At zero, differentiating the degree-$r+1$ monomial fewer than $r+1$ times leaves a zero factor. Hence only its full derivative times $\log\rho_n$ contributes, and
$$
\partial_x^{r+1}(f_n-\mathrm{id})(0)
=(r+1)!\,\varepsilon_n\log\rho_n=-(r+1)!.
$$
There is no asymptotic error or cutoff contribution at this point.

The global diffeomorphism argument also holds: for large $n$ the displacement has global Lipschitz constant below one, so the inverse equation is a contraction for every target point. The Jacobian is positive by uniform closeness to the identity. The inverse is smooth, and the map fixes 0 and is the identity outside the prescribed disk.

## 3. Exact metric realization and normalized uniqueness

The metric identity is correct:
$$
df_n=(f_n)_z(dz+\mu_n\,d\bar z),\qquad
U_n\circ f_n=b+a_n+\log|(f_n)_z|.
$$
Substitution gives exactly
$$
f_n^*(e^{-2U_n}|dw|^2)
=e^{-2b-2a_n}|dz+\mu_n\,d\bar z|^2.
$$
In particular the sign of the logarithmic Jacobian term is correct.

The real quadratic form is positive once $|\mu_n|<1$. Its two eigenvalues relative to the Euclidean metric are $(1\pm|\mu_n|)^2$. The metrics are uniformly comparable to the background and agree with it off a fixed disk.

Because a global bijection equal to the identity outside the disk sends that disk to itself, $U_n=b$ outside the disk. On the sphere, $u_n=U_n-b$ is therefore identically zero near infinity and extends smoothly across it. The maps extend there as the identity. On the plane, the complete cigar background is preserved outside a compact set; completeness follows also from uniform metric comparability. The conformal target metrics are complete by the exact isometry identity.

The stipulated normalization is satisfied without any postcomposition. Any two normalized conformal representations differ by a conformal automorphism: an affine complex map on the plane or a Möbius map on the sphere. Fixing the required two or three points makes it the identity. Thus the constructed $f_n$ really is the inverse parametrization's diffeomorphism component. It cannot be replaced by a different convergent normalized choice.

## 4. The critical $r=1$ curvature correction

This is the principal analytical risk in the argument. I checked its uniformity, the inverse-map drift, the sign of the curvature formula, and the order in which constants are chosen.

Write $\ell=1+|\log s|$. After omitting finitely many terms, $0<s<1$ throughout the inner disk. The elementary bounds
$$
s\ell\leq1,\qquad s\ell^2\leq4/e
$$
follow by setting $t=-\log s\geq0$ and differentiating $e^{-t}(1+t)$ and $e^{-t}(1+t)^2$. These bounds are uniform in both the point and $n$.

The third derivative of $z^2\log s$ has no undifferentiated-logarithm term because the polynomial has degree two. Hence
$$
|D^2f_n|\leq C\varepsilon_n\ell,\qquad
|D^3f_n|\leq C\varepsilon_n/s.
$$
Differentiating $h_n=\log|(f_n)_z|$ gives
$$
|\nabla h_n|\leq C\varepsilon_n\ell,\qquad
|D^2h_n|\leq C(\varepsilon_n/s+\varepsilon_n^2\ell^2)
\leq C'\varepsilon_n/s.
$$
The quadratic derivative term is absorbed using $s\ell^2\leq4/e$ and $\varepsilon_n\leq1$.

For a real Jacobian $J=Df_n$, the principal coefficient of the pulled-back Laplacian is indeed
$$
A=J^{-1}J^{-T},
$$
not its transposed-order alternative. The drift satisfies the exact formula
$$
B=-J^{-1}\big(A:D^2 f_n^1,\ A:D^2 f_n^2\big)^T.
$$
Thus $A-I=O(\varepsilon_n)$, $A\geq\frac12I$ for large $n$, and $|B|\leq C\varepsilon_n\ell$. The candidate retains this drift; it does not confuse the operator with just its principal part.

For $b+h_n$, all possible errors are bounded by a fixed multiple of
$$
\varepsilon_n+\varepsilon_n\ell+\varepsilon_n/s
+\varepsilon_n^2\ell^2\leq C\varepsilon_n/s.
$$
The bounded derivatives of either background $b$ are sufficient here. The resulting constant $C_0$ is independent of $n$ and of the later correction coefficient $K$.

The regularized radius has positive semidefinite Hessian, with tangential eigenvalue $1/s$ and radial eigenvalue $\rho_n^2/s^3$. Therefore
$$
\mathcal L_n s
\geq\frac{1}{2s}-C\varepsilon_n\ell
\geq\frac{1}{4s}
$$
uniformly for large $n$. Choosing a fixed $K>4C_0$ makes the inner-disk lower bound strictly positive. This is an exact operator estimate, not a first-order approximation.

The cutoff correction $K\varepsilon_n\chi s_n$ tends to zero in $C^1$: $s_n$ is bounded on the support and $|\nabla s_n|\leq1$. On the cutoff annulus, its derivatives through the needed order and those of $f_n-\mathrm{id}$ are $O_K(\varepsilon_n)$, because that annulus stays away from zero. The pulled-back Laplacian there consequently converges uniformly to $\Delta b$, which has a positive minimum. Choosing $n$ large after $K$ handles the annulus without changing $K$. Outside the support nothing changes.

Finally, $K_{e^{-2U_n}|dw|^2}=e^{2U_n}\Delta U_n$. The exponent is positive, and the exact pullback of $\Delta U_n$ is the quantity just estimated. This proves strictly positive curvature everywhere on both surfaces. Together with $\mu_n\to0$ and $a_n\to0$ in $C^1$, it proves the required $C^1$ metric convergence. No step assumes that $C^1$ convergence alone controls curvature.

## 5. The remaining endpoints

For $r\geq2$, $a_n=0$ gives convergence of metric coefficients in $C^r$ and hence in $C^2$ on the fixed compact support. Gaussian curvature depends smoothly on the positive metric two-jet. The background has a positive curvature minimum on this support; no positive global lower bound on the cigar's curvature is needed because the metrics agree with it elsewhere. The fixed top derivative of $f_n-\mathrm{id}$ proves failure of convergence in $C^{r+1}$.

For $r=0$, the radial twist is smooth at zero because it is a constant rotation on a whole neighborhood there. It is a global orientation-preserving diffeomorphism with the explicitly stated inverse. Radiality of the background removes the rotation from the pullback metric. The shear parameter is uniformly $O(1/n)$, so the metrics converge uniformly while the derivative at zero remains a fixed nonidentity rotation. Pullback preserves both completeness and positive curvature. The maps fix all the normalization points.

Each fixed integer has its own sequence and sufficiently large starting index. The proof does not require a uniform choice across all integers.

## 6. Reproducibility and independent challenges

The submitted checker has SHA-256

dad7fc79034bb61fb869a81582cae21ebade0a49474f9c590cc145586dd8a04c.

All **90 submitted symbolic checks reproduce byte for byte** in the separate replay directory. The three source PDF hashes match the author's provenance record. The original candidate hash remains unchanged.

The independent [checker](independent_checks.py) passes **136 exact assertions**, with [receipt](independent_results.json). It imports none of the author's code. Its controls include:

- Uniform logarithmic-bound certificates used above
- A nonlinear chart made of two successive shears, checking both the inverse-Jacobian order and the nonzero Laplacian drift; dropping either is detected
- The actual critical map's jets at zero and the corrected Laplacian there
- The critical linearized curvature profile, which changes sign and has scale $\varepsilon_n/s_n$, confirming that the critical endpoint needs genuine curvature control

For the last diagnostic, putting $Q=x^2+y^2$ gives the exact identity
$$
\Delta\operatorname{Re}\partial_z(z^2\log s)
=\frac{4x(Q^2+3Q\rho^2+3\rho^4)}{(Q+\rho^2)^3}.
$$
The finite profile tests are not used to infer nonlinear positivity; the all-point estimate in Section 4 supplies that proof.

The controls use SymPy 1.14.0 and exact symbolic/rational arithmetic. They do not certify completeness or uniqueness computationally; those were checked geometrically above.

## 7. Final disposition

The candidate supplies a complete negative answer for every finite integer endpoint in the exact source parametrization, including both specified surfaces and the stronger strict-positive-curvature restriction. No unresolved mathematical step was identified, and no mandatory correction is required.

A bounded independent current-source search recovered the erratum and the corrected primary work, but no verified later resolution. That does not establish historical priority. Preserve the candidate/AI-reviewed/unrefereed description and the explicit lack of a new-discovery or priority claim when publishing a draft PR.
