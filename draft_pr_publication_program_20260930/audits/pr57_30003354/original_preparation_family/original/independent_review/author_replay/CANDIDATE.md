# Failure of the conformal parametrization at every finite integer endpoint

**Target:** 30003354 / OWR-15208-008.  
**Status:** complete candidate counterexample construction, pending separate adversarial review. Priority is unconfirmed; no published-new-result claim is made.  
**Scope:** every finite integer r≥0, on both the plane and the sphere, with all metrics smooth, complete and of strictly positive Gaussian curvature.

## 1. Exact formulation

Let $M_0=\mathbb C$ with $g_0=|dz|^2$, and let $M_1=S^2$ with the unit round metric

$$g_1=\frac{4|dz|^2}{(1+|z|^2)^2}$$

in stereographic coordinates. Let $\mathcal D(M_0)$ be the smooth orientation-preserving diffeomorphisms fixing 0 and 1, and let $\mathcal D(M_1)$ fix 0, 1 and infinity. Let $\mathcal O_\kappa$ consist of smooth real functions for which $e^{-2u}g_\kappa$ is complete with nonnegative curvature.

The source's continuous bijection is

$$P_\kappa:\mathcal O_\kappa^{,r}\times\mathcal D^{,r+1}(M_\kappa)
\longrightarrow\mathcal R_{\ge0}^{,r}(M_\kappa),
\qquad P_\kappa(u,\phi)=\phi^*(e^{-2u}g_\kappa).$$

The superscripts specify compact-open $C^r$ and $C^{r+1}$ topologies **on smooth objects**, not finite-regularity classes. The extra derivative on the diffeomorphism is essential. The exact interpretation is explicit in [Belegradek–Hu's 2016 erratum](https://doi.org/10.1007/s00208-015-1354-1) and [Banakh–Belegradek, Sections 2, 8–9](https://arxiv.org/abs/1510.07269). The [original workshop report](https://ems.press/doi/pdf/10.4171/OWR/2017/3), printed p. 149, asks about the integer endpoint; its abbreviated use of the pullback symbol must not be read as assigning only r derivatives to $\phi$ itself.

**Candidate theorem.** For every finite integer $r\ge0$ and each $\kappa\in\{0,1\}$, $P_\kappa^{-1}$ is not continuous. This remains true after restricting to strictly positive-curvature metrics. The conclusion concerns this parametrization, not an assertion that the underlying spaces admit no other homeomorphism.

We construct $g_n\to g_*$ in $C^r$ whose unique normalized diffeomorphisms $\phi_n$ do not approach the identity in $C^{r+1}$. No assertion is made against the known $C^\infty$ or noninteger Hölder results.

## 2. Fixed positive-curvature backgrounds

Use the following radial background, depending on the surface:

$$g_*=e^{-2b(z)}|dz|^2,\qquad
b(z)=\begin{cases}
\tfrac12\log(1+|z|^2),&M_0,\\
\log(1+|z|^2)-\log2,&M_1.
\end{cases}$$

On the plane this is the complete cigar metric, with curvature $2/(1+|z|^2)>0$; completeness follows from the divergent radial integral $\int_0^\infty(1+s^2)^{-1/2}ds$. On the sphere it is $g_1$, with curvature 1. On every fixed coordinate disk, $\Delta b$ has a positive lower bound.

All perturbations below equal $g_*$ outside $|z|<1/4$. Diffeomorphisms fix 0 and are the identity outside this disk, so all required normalization points are fixed, including infinity. The inverse image of $g_*$ under $P_\kappa$ is $(b,\mathrm{id})$ on the plane and $(0,\mathrm{id})$ on the sphere.

## 3. The endpoint r=0: a slow radial twist

Choose a smooth function $\eta:\mathbb R\to[0,1]$ equal to 0 on $(-\infty,0]$ and 1 on $[1,\infty)$, with bounded derivative. Set $R=1/4$, choose $\theta_0\notin2\pi\mathbb Z$, and, for $s>0$, set

$$\theta_n(s)=\theta_0\eta\!\left(\frac{\log(R/s)}n\right),\qquad
\phi_n(z)=e^{i\theta_n(|z|)}z.$$

Define $\phi_n(0)=0$. This is a smooth diffeomorphism: it is a constant rotation on $|z|\le Re^{-n}$, the identity for $|z|\ge R$, and its inverse subtracts the same angle at each radius. It preserves orientation. Moreover

$$q_n(s):=s\theta_n'(s),\qquad \|q_n\|_\infty\le\frac{|\theta_0|\|\eta'\|_\infty}{n}.$$

In orthonormal polar frames in the source and target, the differential is a rotation followed by the shear with matrix $\left(\begin{smallmatrix}1&0\\q_n&1\end{smallmatrix}\right)$. Since $b$ is radial, the matrix of $\phi_n^*g_*$ relative to $g_*$ is

$$\begin{pmatrix}1+q_n^2&q_n\\q_n&1\end{pmatrix}.$$

Thus $g_n=\phi_n^*g_*\to g_*$ uniformly, even globally in the background tensor norm. Each $g_n$ is complete with positive curvature because it is isometric to $g_*$. Its normalized conformal factor is the fixed one for $g_*$, and its normalized diffeomorphism is $\phi_n$. But

$$D\phi_n(0)=\operatorname{Rot}(\theta_0)\ne I$$

for every n. This proves failure at r=0 on both surfaces.

## 4. Logarithmic coordinate perturbations for r≥1

Fix an integer $r\ge1$. Choose $\chi\in C_c^\infty(\mathbb C)$ radial, equal to 1 for $|z|\le1/8$ and 0 for $|z|\ge1/4$. For integers $n\to\infty$, put

$$\rho_n=e^{-n},\quad \varepsilon_n=1/n,\quad
s_n(z)=(|z|^2+\rho_n^2)^{1/2},\quad L_n(z)=\log s_n(z),$$

$$f_n(z)=z+w_n(z),\qquad
w_n(z)=\varepsilon_n\chi(z)z^{r+1}L_n(z).\tag{4.1}$$

All functions are smooth for each n. Constants in the estimates below may depend on r and the fixed cutoff, but not on n. We discard finitely many initial n whenever necessary.

### 4.1 Uniform estimates

For real derivatives of order $j\ge1$,

$$|D^jL_n(z)|\le C_j s_n(z)^{-j}.\tag{4.2}$$

This follows either by repeated differentiation of $\frac12\log(|z|^2+\rho_n^2)$ or by rescaling $(z,\rho_n)$; the resulting rational functions are bounded on the unit half-sphere. By Leibniz's rule, on the inner disk,

$$|D^k(z^{r+1}L_n)|\le C_{r,k}s_n^{r+1-k}(1+|\log s_n|),\qquad0\le k\le r+1.\tag{4.3}$$

On the cutoff annulus all derivatives of fixed order are uniformly bounded, since $|z|\ge1/8$. In particular,

$$\|Df_n-I\|_{C^0}\le C_r\varepsilon_n\to0,
\qquad \|(f_n)_z\|_{C^r}\le C_r.\tag{4.4}$$

For the second bound, the largest possible logarithm is $n+O(1)$, canceled by $\varepsilon_n=1/n$. Consequently $f_n$ is globally injective and onto: its displacement has Lipschitz constant less than 1, so the inverse equation is a contraction on $\mathbb R^2$. Its positive Jacobian and the smooth inverse function theorem make it a smooth orientation-preserving diffeomorphism. It is the identity outside the fixed disk and fixes 0.

With Wirtinger derivatives $\partial_z=(\partial_x-i\partial_y)/2$, define

$$\mu_n=\frac{(f_n)_{\bar z}}{(f_n)_z}.$$

On the inner disk,

$$(f_n)_{\bar z}=\frac{\varepsilon_n z^{r+2}}{2(|z|^2+\rho_n^2)}.\tag{4.5}$$

Its derivatives of order k≤r have magnitude at most $C_r\varepsilon_n s_n^{r-k}$. The cutoff contribution is also $O(\varepsilon_n)$ in $C^r$. Thus

$$\|(f_n)_{\bar z}\|_{C^r}\le C_r\varepsilon_n.$$

By (4.4), $(f_n)_z$ stays uniformly away from zero and has uniformly bounded $C^r$ norm. Differentiating its reciprocal finitely many times therefore gives

$$\boxed{\|\mu_n\|_{C^r}\le C_r\varepsilon_n\longrightarrow0.}\tag{4.6}$$

In contrast, because $\chi=1$ near 0 and $L_n(0)=\log\rho_n=-n$,

$$\boxed{\partial_x^{r+1}(f_n-\mathrm{id})(0)=-(r+1)!}\tag{4.7}$$

as a complex-valued derivative. Terms in which a derivative hits $L_n$ leave an undifferentiated factor of $z^{r+1}$ of positive degree at 0 and vanish. Hence $f_n$ cannot converge to the identity in $C^{r+1}$.

### 4.2 Metrics realizing these normalized diffeomorphisms

For a smooth real correction $a_n$ supported in the same disk, define

$$g_n=e^{-2b(z)-2a_n(z)}|dz+\mu_n(z)d\bar z|^2.\tag{4.8}$$

For a complex coefficient $\mu$, the notation denotes the real quadratic form obtained from the squared complex modulus. Its eigenvalues relative to $|dz|^2$ are $(1\pm|\mu|)^2$, so this is a smooth positive metric for large n. Outside the disk it equals $g_*$; on the plane it is therefore complete (also uniformly comparable to the complete background).

Let $h_n=\log|(f_n)_z|$ and

$$U_n=(b+a_n+h_n)\circ f_n^{-1}.$$

Since $df_n=(f_n)_z(dz+\mu_n d\bar z)$, identity (4.8) is exactly

$$g_n=f_n^*(e^{-2U_n(w)}|dw|^2).\tag{4.9}$$

On the plane take $u_n=U_n$. On the sphere put $u_n=U_n-b(w)$; this is zero outside the disk and extends smoothly across infinity. Then (4.9) is $g_n=P_\kappa(u_n,f_n)$. Once positivity is proved below, $u_n\in\mathcal O_\kappa$ by isometry and completeness. Normalized uniqueness from the source, or simply uniqueness of normalized plane/sphere conformal automorphisms, identifies $f_n$ as the diffeomorphism component of $P_\kappa^{-1}(g_n)$.

## 5. Integer endpoints r≥2

For r≥2, set $a_n=0$. By (4.6), $g_n\to g_*$ in $C^r$, hence in $C^2$ on the fixed compact support. Gaussian curvature is a continuous function of the positive metric's two-jet. The background curvature has a positive minimum on that disk, so $g_n$ has positive curvature there for all sufficiently large n. Outside, it is the background metric. The metrics are complete, their normalized inverse images have diffeomorphism component $f_n$, and (4.7) proves inverse discontinuity.

## 6. The endpoint r=1: a curvature-preserving correction

C^1 convergence alone does not preserve a lower curvature bound, so the preceding argument cannot simply be reused. We give a correction that is small in C^1 and prove its sign directly.

In this section r=1. On $|z|\le1/8$ write $s=s_n$, $\varepsilon=\varepsilon_n$, and $\ell=1+|\log s|$. The estimates from (4.1)–(4.3), with one further derivative, give

$$|Df_n-I|\le C\varepsilon,\quad
|D^2f_n|\le C\varepsilon\ell,\quad
|D^3f_n|\le C\varepsilon/s.\tag{6.1}$$

In the third estimate the degree-two polynomial has no third derivative, so every surviving Leibniz term differentiates the logarithm at least once. These estimates imply

$$|\nabla h_n|\le C\varepsilon\ell,\qquad
|D^2h_n|\le C(\varepsilon/s+\varepsilon^2\ell^2)
\le C'\varepsilon/s,\tag{6.2}$$

because $s\ell^2$ is uniformly bounded for $0<s<1$.

Define the pulled-back Euclidean Laplacian on a real function v by

$$\mathcal L_n v=\big[\Delta_w(v\circ f_n^{-1})\big]\circ f_n.
$$

The ordinary chain rule writes it as

$$\mathcal L_n v=A_n^{ij}\partial_{ij}v+B_n^i\partial_i v,
\quad A_n=(Df_n)^{-1}(Df_n)^{-T}.$$

The inverse-map second-derivative formula and (6.1) give

$$\|A_n-I\|\le C\varepsilon,\quad A_n\ge\tfrac12 I,
\quad |B_n|\le C\varepsilon\ell.\tag{6.3}$$

All matrices and norms here are in real coordinates. Since b and its first two derivatives are bounded on this disk, (6.2)–(6.3), $s\ell\le C$ and $s\ell^2\le C$ imply, for a constant $C_0$ independent of n,

$$\mathcal L_n(b+h_n)\ge\Delta b-C_0\varepsilon/s
\ge-C_0\varepsilon/s.\tag{6.4}$$

The regularized radius is convex and satisfies

$$\nabla s=z/s,\quad D^2s=I/s-zz^T/s^3\ge0,
\quad \Delta s=\frac{|z|^2+2\rho_n^2}{s^3}\ge1/s.$$ 

Therefore (6.3) gives

$$\mathcal L_n s\ge\frac1{2s}-C\varepsilon\ell\ge\frac1{4s}\tag{6.5}$$

for all sufficiently large n, uniformly in z: multiply the error by s and use the boundedness of $s\ell$.

Choose a fixed constant $K>4C_0$, and set

$$a_n(z)=K\varepsilon_n\chi(z)s_n(z).\tag{6.6}$$

This function is smooth, supported in the fixed disk, and tends to zero in C^1 because $|\nabla s_n|\le1$ and $s_n$ is uniformly bounded on the support. On the inner disk, (6.4)–(6.5) give

$$\mathcal L_n(b+h_n+a_n)\ge(K/4-C_0)\varepsilon_n/s_n>0.\tag{6.7}$$

On the closed cutoff annulus $1/8\le|z|\le1/4$, all derivatives of fixed order of $f_n-\mathrm{id}$, $h_n$ and $a_n$ are $O_K(\varepsilon_n)$. Thus $\mathcal L_n(b+h_n+a_n)\to\Delta b$ uniformly there. The latter has a strictly positive minimum, so the same positivity holds throughout that annulus for sufficiently large n. Outside the support, the metric is $g_*$.

Finally, the curvature of $e^{-2U_n}|dw|^2$ is $e^{2U_n}\Delta_w U_n$, and

$$\Delta_w U_n(f_n(z))=\mathcal L_n(b+h_n+a_n)(z).$$

This proves positive curvature everywhere, not just positivity of an approximate linearized curvature. Equations (4.6), (4.8) and $a_n\to0$ in C^1 imply $g_n\to g_*$ in C^1. But (4.7) gives $\partial_x^2(f_n-\mathrm{id})(0)=-2$ for all n. The r=1 case is established on both surfaces.

## 7. Conclusion and limits

Each integer r has its own sequence of smooth complete positive-curvature metrics. In each case the metrics converge in the exact source topology and the uniquely normalized diffeomorphisms fail to converge in the required one-higher-derivative topology. This proves the candidate theorem for all finite integer endpoints, while leaving the known Hölder and C^infinity homeomorphism results intact.

The construction uses familiar endpoint mechanisms (slow twists and regularized logarithms). A bounded literature search found the original expectation of failure and the 2016 erratum, but did not establish priority for the construction or its full curvature-preserving version. Independent review and a broader novelty assessment remain necessary before describing this as a new result.
