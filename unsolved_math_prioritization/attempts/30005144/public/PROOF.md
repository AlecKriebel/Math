# A literature-based proof, with the asymptotic convention made explicit

## 1. Exact target and conventions

Let \((M^3,g)\) be a smooth connected complete Riemannian manifold without boundary. Outside a compact set, suppose there is one end identified with \(\mathbb R^3\setminus\overline B_R\), and write \(g_{ij}=\delta_{ij}+h_{ij}\). We use the convention printed in Mazurowski's 2022 preprint, Definition 26:

\[
h_{ij}=O(r^{-1}),\qquad \partial_kh_{ij}=O(r^{-2}),
\]

and \(h\to0\) smoothly at infinity. In particular, every ordinary coordinate derivative of \(h\), through order three, tends uniformly to zero outside large compact sets. We do **not** infer weighted second- or third-derivative decay from these conditions. Assume \(R_g\ge0\) and \((M,g)\not\cong(\mathbb R^3,\delta)\).

Let \(\mathcal C(M)\) be the compactly supported Caccioppoli sets. For \(c>0\), put

\[
\mathcal A_c(\Omega)=P_g(\Omega)-cV_g(\Omega),\qquad
\omega_c(M)=\inf_{\{\Omega_s\}}\max_{s\in[0,1]}\mathcal A_c(\Omega_s),
\]

where the paths are continuous in the flat-plus-varifold \(\mathbf F\) topology, start at the empty set, and end with negative \(\mathcal A_c\). This is Definitions 5–6 of the cited 2022 preprint. The OWR report describes smoothly varying open-set families; the path constructed below has smooth embedded boundaries for every positive parameter and collapses continuously to the empty set at zero.

**Candidate conclusion.** For every \(c>0\),
\[
\omega_c(M)<16\pi/(3c^2).
\]

This note is a reduction to known geometric-analysis results, not an independent reproving of them or a novelty claim.

## 2. Precisely imported results

Use the following results of Mazurowski–Zhu, arXiv:2502.18455v1, abbreviated [MZ]. Their end assumption is

\[
\sum_{k=0}^3 |x|^k|\partial^k(\widehat g-\delta)|=o(1).
\tag{2.1}
\]

1. **Smooth-flow theorem:** [MZ, Theorem 1.5, pp. 4–5; proof p. 30]. For an end satisfying (2.1), inverse mean curvature flow emerging from a sufficiently far-out point \(q\) at time \(-\infty\) is smooth through any fixed finite time \(T\). Its leaves are embedded two-spheres. The normalization is \(\min_{\partial D_1(q)}u=0\).
2. **Uniform spatial bounds:** [MZ, Lemmas 2.4–2.5 and Corollary 2.6 / equation (2.11), pp. 14–16]. If \(\widehat C^{-1}\delta\le\widehat g\le\widehat C\delta\), there is \(C>1\), depending only on \(\widehat C\), such that, for \(q\) sufficiently far out and all \(t\le T\),
\[
D_{C^{-1}e^{t/2}}(q)\setminus\{q\}
\subset\Omega_t\setminus\{q\}
\subset D_{Ce^{t/2}}(q)\setminus\{q\}.
\tag{2.2}
\]
3. **Initial Hawking mass:** [MZ, Lemma 2.3, pp. 13–14]. Along the point-emerging weak flow, the Hawking-mass limit as \(t\to-\infty\) exists and is nonnegative.

Crucially, these three inputs do **not** assume nonnegative scalar curvature on the ambient manifold: [MZ, §2.1] extends the original end to an arbitrary complete metric on \(\mathbb R^3\), and Lemma 2.3 explicitly estimates a possibly negative scalar-curvature error. Nonnegative scalar curvature is used below only where our smooth flow lies.

We also use zero-mass rigidity in the three-dimensional Riemannian positive mass theorem, and the smooth Geroch monotonicity formula. The former excludes a non-Euclidean, complete, boundary-free, nonnegative-scalar-curvature manifold that is flat outside a compact set. An asymptotically Euclidean flat exterior has a Euclidean exterior after changing its asymptotic coordinates and zero ADM mass. Equivalently, apply zero-mass rigidity to this geometrically Euclidean end. A primary modern reference stating the requisite rigidity is Agostiniani–Mazzieri–Oronzio, *A Green's Function Proof of the Positive Mass Theorem*, Theorem 2.1, DOI 10.1007/s00220-024-04941-8. No mass theorem is being applied to the auxiliary metric constructed next.

## 3. Transplantation removes the derivative-convention mismatch

There are points of nonzero Riemann curvature arbitrarily far out in the original end. Otherwise the end is eventually flat, and the preceding zero-mass rigidity contradicts the assumed non-Euclidean geometry.

Choose points \(q_j=10^j e_1\in\mathbb R^3\), radii \(L_j=j\), and a fixed smooth cutoff \(0\le\chi\le1\), equal to one on \(D_1\) and supported in \(D_2\). The balls \(D_{2L_j}(q_j)\) are pairwise disjoint. Smooth convergence of the original metric allows us to choose non-flat points \(p_j\) arbitrarily far out so that the original coordinate ball \(D_{2L_j}(p_j)\) lies in the end and

\[
\sup_{D_{2L_j}(p_j)}\sum_{k=0}^3|\partial^k h|
\le\varepsilon_j,
\qquad \varepsilon_j\le j^{-1}|q_j|^{-5}.
\tag{3.1}
\]

Shrink these bounds by a fixed constant if necessary to ensure every metric below lies between \(\tfrac12\delta\) and \(2\delta\). Define a metric on all of \(\mathbb R^3\) by

\[
\widehat g(x)=\delta+
\sum_{j=1}^{\infty}\chi\!\left(\frac{x-q_j}{L_j}\right)
 h(p_j+x-q_j).
\tag{3.2}
\]

Each summand is understood to be zero outside its support. The sum is locally finite and its supports are disjoint, so it is smooth. It is positive definite and complete by uniform equivalence to the Euclidean metric. On \(D_{L_j}(q_j)\), translation to \(D_{L_j}(p_j)\) is an isometry with the original metric. Thus \(R_{\widehat g}\ge0\) there and \(\operatorname{Rm}_{\widehat g}(q_j)\ne0\). Scalar curvature is allowed to have either sign in the cutoff annuli.

For \(k\le3\), the product rule and \(L_j\ge1\) give

\[
\sup_{D_{2L_j}(q_j)}|\partial^k(\widehat g-\delta)|
\le C_\chi\varepsilon_j.
\]

Because \(|x|\asymp|q_j|\) on these balls, multiplication by \(|x|^k\) gives a quantity tending to zero as \(j\to\infty\). Outside the balls the metric is Euclidean. Hence (2.1) holds for this **single fixed** auxiliary metric. It is important to use one fixed metric before invoking the far-out threshold; applying a different cutoff metric at each point would not control that threshold.

Fix a desired volume \(v>0\). The constant \(C\) in (2.2) is fixed for \(\widehat g\). Choose a finite \(T\) such that

\[
2^{-3/2}\frac{4\pi}{3}C^{-3}e^{3T/2}>v.
\tag{3.3}
\]

Now take \(j\) so large that \(q_j\) is beyond every threshold in the three imported results for this \(T\), and \(L_j>Ce^{T/2}\). The resulting smooth point-emerging flow and every enclosed set for \(t\le T\) lie inside \(D_{L_j}(q_j)\). The lower inclusion in (2.2) and uniform metric equivalence imply \(V_{\widehat g}(\Omega_T)>v\). Every flow region can therefore be translated isometrically into the original manifold, and the whole relevant flow has nonnegative ambient scalar curvature. There is no appeal to nonnegative scalar curvature in a cutoff annulus and no assumption that weak flows are globally local under changes of metric.

## 4. Strict sub-Euclidean isoperimetry along the trapped flow

Write \(A(t)=|\Sigma_t|\), \(V(t)=|\Omega_t|\), and

\[
m(t)=\frac{A(t)^{1/2}}{(16\pi)^{3/2}}
\left(16\pi-\int_{\Sigma_t}H^2\,d\mu\right).
\]

The flow is smooth, \(H>0\), and its leaves are spheres. Geroch's formula becomes

\[
m'(t)=\frac{A(t)^{1/2}}{(16\pi)^{3/2}}
\int_{\Sigma_t}\left(2|\nabla\log H|^2+R_{\widehat g}+|\mathring A|^2\right)d\mu\ge0.
\tag{4.1}
\]

The imported initial-mass result gives \(m(t)\ge0\). In fact \(m(t)>0\) for every finite \(t\le T\). To check strictness, suppose \(m(t_0)=0\). Monotonicity and the nonnegative limit force \(m\equiv0\) on \(( -\infty,t_0]\). Every nonnegative term in (4.1) then vanishes. Thus every leaf has constant \(H\), is umbilic, and has zero ambient scalar curvature. Also \(H^2A=16\pi\) on each leaf.

In flow coordinates, \(\partial_t\gamma_t=2A_t/H=\gamma_t\), while the normal metric is \(H^{-2}dt^2\). Set \(r=\sqrt{A/(4\pi)}\). Since \(A'=A\), we have \(dt=2dr/r\) and \(H=2/r\); consequently the swept metric is \(dr^2+r^2\gamma\), with \(\gamma\) independent of \(r\). Its scalar curvature is \(r^{-2}(R_\gamma-2)\), so \(R_\gamma=2\). In dimension two this means Gaussian curvature one; hence this cone metric is flat. The annulus bounds show that the swept regions exhaust a punctured neighborhood of \(q_j\); smoothness at that point forces \(\operatorname{Rm}(q_j)=0\), a contradiction.

It follows that

\[
\int_{\Sigma_t}H^2<16\pi.
\]

The area and volume variations are \(A'=A\) and \(V'=\int H^{-1}\). Hölder gives

\[
A\le\left(\int H^2\right)^{1/3}\left(\int H^{-1}\right)^{2/3},
\qquad
(A^{3/2})'=\tfrac32A^{3/2}<6\sqrt\pi\,V'.
\]

Both area and volume tend to zero at the point endpoint by (2.2). Integrating yields

\[
A(t)<K V(t)^{2/3},\qquad K=(36\pi)^{1/3},\quad -\infty<t\le T.
\tag{4.2}
\]

This is the same geometric mechanism as [MZ, Lemma 2.21]; the calculation spells out why it is valid on the trapped flow even if the auxiliary metric has negative scalar curvature elsewhere.

## 5. The strict mountain-pass estimate

Fix \(c>0\) and take \(v>\max\{1,(K/c)^3\}\). By Section 3 and strict volume increase, truncate the smooth flow when its volume first equals \(v\). Reparameterize the time interval \(( -\infty,t_v]\) by \(s=e^{t-t_v}\in(0,1]\), and set \(\Omega_0=\varnothing\). The area is \(A(t_v)s\), so both mass and volume tend to zero at \(s=0\). The path is \(\mathbf F\)-continuous, including that endpoint, and smooth for \(s>0\).

For \(s>0\), (4.2) gives

\[
\mathcal A_c(\Omega_s)<K V_s^{2/3}-cV_s.
\]

The function \(f(V)=KV^{2/3}-cV\) has its maximum at

\[
V_*=(2K/(3c))^3=32\pi/(3c^3),\qquad
f(V_*)=16\pi/(3c^2)=:W.
\]

At \(s=0\), the functional equals \(0<W\). At \(s=1\), it is negative since \(v>(K/c)^3\). The functional is continuous on a compact parameter interval, so its maximum is attained; every value is strictly below \(W\). Therefore

\[
\omega_c(M)\le\max_s\mathcal A_c(\Omega_s)<W,
\]

as claimed. The compactness step is essential: pointwise strict inequalities on an arbitrary noncompact parameter set would not by themselves imply a strict supremum bound.

## 6. Euclidean normalization and limits of verification

In Euclidean space a ball of radius \(r\) has energy \(4\pi r^2-(4\pi c/3)r^3\), with maximum \(W\) at \(r=2/c\). Conversely, Euclidean isoperimetry implies every continuous mountain-pass path must pass through volume \(V_*\) and have energy at least \(W\). Indeed a negative endpoint has volume greater than \((K/c)^3>V_*\). Thus \(\omega_c(\mathbb R^3)=W\), and the non-Euclidean exclusion is necessary.

`verify_algebra.py` checks the one-variable identities and equality-cone scalar formula algebraically. It cannot verify [MZ], positive mass rigidity, Geroch monotonicity, the transplantation estimates, or the topological and analytical continuity arguments. Those are theorem dependencies and proof obligations for the independent auditor.

## References

- [OWR] Liam Mazurowski, *Prescribed Mean Curvature Min-Max Theory in Some Non-compact Manifolds*, in *Geometrie*, Oberwolfach Report 28/2022, pp. 1574–1576; the conjecture is on p. 1576 and equation (1) and path definition on p. 1575. https://doi.org/10.4171/OWR/2022/28
- [M22] Liam Mazurowski, *Prescribed Mean Curvature Min-Max Theory in Some Non-Compact Manifolds*, arXiv:2204.07493v1, Definitions 5–6 and 26. https://arxiv.org/abs/2204.07493v1 . The later journal article is *Advances in Mathematics* 464 (2025), 110133, https://doi.org/10.1016/j.aim.2025.110133 . Its final full text was not verified here.
- [MZ] Liam Mazurowski and Jintian Zhu, *Existence of Constant Mean Curvature Surfaces in Asymptotically Flat and Asymptotically Hyperbolic Manifolds*, arXiv:2502.18455v1 (25 February 2025), especially Theorem 1.5, §2, Lemmas 2.3–2.5 and 2.21, Corollary 2.6, Proposition 2.1, and proof of Theorem 4.3. https://arxiv.org/abs/2502.18455v1
- Virginia Agostiniani, Lorenzo Mazzieri, Francesca Oronzio, *A Green's Function Proof of the Positive Mass Theorem*, *Communications in Mathematical Physics* 405, 54 (2024), Theorem 2.1. https://doi.org/10.1007/s00220-024-04941-8
- Gerhard Huisken and Tom Ilmanen, *The Inverse Mean Curvature Flow and the Riemannian Penrose Inequality*, *Journal of Differential Geometry* 59 (2001), 353–437. https://www2.math.ethz.ch/EMIS/journals/NYJM/jdg/p/2001/59-3-1.pdf
