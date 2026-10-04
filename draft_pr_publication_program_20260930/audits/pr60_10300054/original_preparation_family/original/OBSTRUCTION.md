# Monotone wobble: gauge reduction and the unresolved attainment problem

**Target:** 10300054 / AMR-102-0054, Calegari Question 13.1.  
**Disposition:** unresolved; recommended `unsolved`, 1/5 substantive attempts.  
**Result here:** an elementary smooth-category gauge reduction, fixed-gauge criteria, and explicit diagnostics showing why two tempting shortcuts fail. None is a counterexample to Calegari's question, and no novelty is claimed for these standard mechanisms. Separate review is pending.

## 1. The actual question and its essential hypotheses

The full [2002 primary problem list](https://arxiv.org/abs/math/0209081), printed p. 29, asks whether a minimal taut C² foliation of an atoroidal 3-manifold with nonzero Godbillon–Vey number admits defining and auxiliary forms

$$T\mathscr F=\ker\alpha,\qquad d\alpha=\alpha\wedge\omega$$

such that $\omega\wedge d\omega$ is everywhere nonnegative or everywhere nonpositive. Zeroes are explicitly allowed. The intended global-form formulation is transversely orientable; the fundamental-class evaluation uses a closed oriented manifold. We do not try to obtain a spurious negative answer by dropping these implicit conventions.

The source itself explains that separated torus leaves and nonminimal foliations can obstruct the desired conclusion. It also records that the stronger requirement $\omega\wedge d\omega>0$ forces the Euler class of the tangent plane bundle to vanish. That stronger contact condition is not the question asked.

The auxiliary form $\omega$ is not uniquely determined by $\alpha$. A pointwise-sign question must retain that freedom, not just the cohomology class. [Hurder–Langevin, Section 3](https://homepages.math.uic.edu/~hurder/papers/59manuscript-rev2016.pdf) explicitly discusses this nonuniqueness and proves independence of the class. Their nonzero-GV dynamical conclusion concerns resilient leaves and entropy, not a sign-definite representative.

The differential-form and flow arguments below are proved for smooth defining data on a closed manifold. They are an obstruction analysis inside the smooth subclass, not a regularity theorem upgrading arbitrary C² foliations. The original C² target remains unresolved as well.

## 2. Exact freedom in choosing the forms

Fix smooth $\alpha,\omega$ with $\alpha$ nowhere zero and $d\alpha=\alpha\wedge\omega$. Differentiating gives

$$\alpha\wedge d\omega=0.\tag{2.1}$$

Every defining form with the same coorientation is $\alpha_f=e^f\alpha$. Set $\omega_f=\omega-df$, so that $d\alpha_f=\alpha_f\wedge\omega_f$. Every auxiliary form for this new defining form is

$$\beta=\omega_f+h\alpha_f\tag{2.2}$$

for some smooth h, since its difference from $\omega_f$ wedges to zero with the nowhere-zero $\alpha_f$. Reversing the coorientation only adds an overall constant sign to the defining form and does not remove this parametrization of the auxiliary freedom.

The full pointwise change of density is

$$\boxed{\beta\wedge d\beta
=\omega\wedge d\omega-df\wedge d\omega+dh\wedge d\alpha_f
=\omega\wedge d\omega+d(-f\,d\omega+h\,d\alpha_f).}\tag{2.3}$$

To verify it, first replace $\omega$ by $\omega_f$; its exterior derivative remains $d\omega$. Expanding $(\omega_f+h\alpha_f)\wedge d(\omega_f+h\alpha_f)$ leaves only $\omega_f\wedge d\omega_f+dh\wedge d\alpha_f$: the terms involving h without dh vanish by (2.1) and $d\alpha_f=\alpha_f\wedge\omega_f$. Substituting $\omega_f=\omega-df$ proves (2.3).

This is much more restrictive than adding an arbitrary exact 3-form. Although any nonzero top-degree cohomology class on a closed connected oriented manifold has a strictly one-signed volume-form representative, that elementary de Rham fact does not say the representative arises through (2.2).

## 3. A fixed-gauge flow equation

Choose a smooth positive volume form $\nu$ and write

$$\omega\wedge d\omega=v\nu,\qquad
\iota_Y\nu=d\omega,\qquad\iota_{X_f}\nu=d\alpha_f.$$

Both Y and $X_f$ preserve $\nu$, since their contracted 2-forms are closed. Both are tangent to the foliation: for example $\alpha_f(X_f)\nu=\alpha_f\wedge d\alpha_f=0$. Formula (2.3) becomes

$$\boxed{\beta\wedge d\beta=(g_f+X_fh)\nu,\qquad g_f=v-Yf.}\tag{3.1}$$

For a **fixed f**, every $X_f$-invariant probability measure $\mu$ supplies the necessary condition

$$g_f+X_fh\ge0\quad\Longrightarrow\quad\int g_f\,d\mu\ge0.\tag{3.2}$$

Indeed, invariance implies $\int X_fh\,d\mu=0$, by differentiating the invariance identity. The total Godbillon–Vey number only controls the particular invariant measure proportional to $\nu$; it does not control all these measures.

For example, on the two-torus with angular coordinates x,y, let $X=\partial_x$ and $g=1+2\cos y$. Its area average is positive, but the invariant probability supported on the circle y=π has average −1. Hence no smooth h can make $g+Xh\ge0$. This is solely a transport-equation diagnostic. It is not asserted to arise as $(X_f,g_f)$ for a foliation satisfying Calegari's hypotheses.

## 4. What invariant measures do, and do not, imply

Here is a standard averaging argument, included to make the obstruction precise. Let X be any smooth vector field on a closed manifold, with flow $\Phi_t$, and let g be smooth.

**Strict criterion.** A smooth h with $g+Xh>0$ exists if and only if $\int g\,d\mu>0$ for every X-invariant probability measure.

Necessity follows from integration and compactness. For sufficiency, the invariant probability measures form a nonempty compact set, so their g-integrals have a positive minimum. There is then T>0 with

$$A_Tg(x):=\frac1T\int_0^Tg(\Phi_t x)\,dt>0\quad\text{for every }x.$$

Otherwise a sequence of increasingly long empirical measures with nonpositive g-average has a weak limit that is invariant and contradicts the positive minimum. Invariance follows directly because shifting an empirical integral by any fixed time changes it by a boundary term of size O(1/T).

Define the smooth function

$$h_T(x)=\frac1T\int_0^T(T-t)g(\Phi_t x)\,dt.$$

Integration by parts yields $Xh_T=-g+A_Tg$, proving sufficiency.

The same argument shows the **approximate nonnegative criterion**:

$$\int g\,d\mu\ge0\ \text{for all invariant probabilities}
\quad\Longleftrightarrow\quad
\forall\delta>0\ \exists h_\delta\in C^\infty:\ g+Xh_\delta\ge-\delta.\tag{4.1}$$

One can apply the strict criterion to $g+\delta$. But replacing approximate nonnegativity by an attained smooth nonnegative representative is not justified. The next explicit example shows the distinction is real for smooth transport equations.

### A nonattainment diagnostic

On $\mathbb T^2=(\mathbb R/2\pi\mathbb Z)^2$, let

$$a=\sum_{j=1}^{\infty}10^{-j!},\qquad X=\partial_x+a\partial_y.$$

For n≥2, put $q_n=10^{n!}$, $p_n=q_n\sum_{j=1}^n10^{-j!}\in\mathbb Z$, $k_n=(-p_n,q_n)$, and $c_n=q_n^{-n/2}$. The positive tail obeys

$$0<q_na-p_n\le2q_n^{-n}.\tag{4.2}$$

The number a is irrational: were it A/B, the nonzero rational difference from $p_n/q_n$ would be at least $1/(Bq_n)$, contradicting (4.2) for large n. Define

$$g(x,y)=\sum_{n=2}^{\infty}c_n\cos(k_n\cdot(x,y)).$$

This is C^infinity. Indeed, $|k_n|\le Cq_n$, and for every fixed derivative order m the series of derivative bounds is at most $C_m\sum_n q_n^{m-n/2}<\infty$. Its Haar average is zero. The irrational linear flow has Haar measure as its unique invariant probability: invariance forces every nonconstant Fourier coefficient of a measure to vanish because $k\cdot(1,a)\ne0$ for every nonzero integer k.

Thus every invariant probability integrates g to zero, and (4.1) holds. Nevertheless there is no smooth h with $g+Xh\ge0$. If such h existed, integration against the full-support Haar measure would force the continuous nonnegative function $g+Xh$ to vanish identically. The Fourier equation $Xh=-g$ would then give

$$|\widehat h(k_n)|=\frac{c_n}{2|q_na-p_n|}
\ge\tfrac14q_n^{n/2}\longrightarrow\infty,$$

which is impossible even for a continuous h. The frequencies are distinct because their second coordinates strictly increase.

Again, this two-dimensional flow is not a counterexample to the foliation problem. It only invalidates an attempted proof that substitutes closure of the smooth coboundary cone for actual attainment.

## 5. Why the strict contact shortcut does not settle the target

At a zero of $X_f$, $d\alpha_f=0$, so $\omega_f$ is proportional to $\alpha_f$ at that point. Equation (2.1) then gives $g_f=0$ there. Since $X_fh=0$ as well, every auxiliary representative for this fixed f has zero Godbillon–Vey density there. Strict positivity is therefore possible only if the tangent vector field $X_f$ is nowhere zero.

Consequently strict positivity forces $e(T\mathscr F)=0$, in agreement with Calegari's already stated observation. A nonzero Euler class would obstruct this stronger condition but would not obstruct a semidefinite representative whose zero locus is nonempty. No counterexample to the actual weak-sign question follows from the Euler-class observation.

## 6. Exact remaining gap

After choosing orientation so that the total Godbillon–Vey number is positive, the smooth version of the target asks for f,h satisfying the exact inequality

$$v-Yf+X_fh\ge0\quad\text{everywhere}.$$

This attempt does not prove that minimality, tautness and atoroidality supply a gauge f for which all invariant-measure inequalities hold. Even if they did, the equality-boundary case still requires smooth attainment, not merely (4.1). Nor does this attempt construct an actual minimal taut atoroidal foliation for which all choices of f fail. The original C² regularity introduces an additional issue that the smooth analysis here does not claim to remove.

The route is therefore stopped as unresolved. The gauge equations, source distinctions and explicit transport diagnostics are the deliverable; they are not a full proof or counterexample to Question 13.1.
