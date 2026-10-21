# A Hardy-only result for lower clamped traces

## Scope and status

This is an authored calculation, not a novelty claim or a classification of admissible boundary conditions. It establishes the origin Hardy equality for one local space that is not nested in the Navier space. It does **not** establish the critical Sobolev equality for this space, and therefore does not by itself answer the simultaneous-constants question.

Let (n>6), let (B_R\subset\mathbb R^n) be the ball centered at the origin, and put

\[
X_R=\{u\in H^3(B_R):\gamma_0u=0,\ \partial_\nu u=0\}.
\]

Then

\[
\inf_{u\in X_R\setminus\{0\}}
\frac{\int_{B_R}|\nabla\Delta u|^2\,dx}
     {\int_{B_R}|x|^{-6}|u|^2\,dx}
= H_{3,2}
=\left(\frac{(n-6)(n-2)(n+2)}{8}\right)^2.
\tag{1}
\]

The constant on the right is the sharp whole-space constant for precisely this energy. The proof below also verifies that identification without relying on an explicit-constant citation.

The space is genuinely outside the elementary Navier sandwich: (u(x)=(1-|x|^2/R^2)^2) belongs to (X_R), whereas its Laplacian has nonzero boundary trace. Thus (X_R\not\subset\{u\in H^3(B_R):u=\Delta u=0\text{ on }\partial B_R\}).

## Proof

Scaling reduces to (R=1). Initially take a smooth function on the closed ball that vanishes in a neighborhood of the origin and has the stated boundary traces. Expand it into orthonormal spherical harmonics. For a coefficient of degree (\ell), write

\[
u_\ell(r)=r^{-a}v(t),\qquad t=-\log r,
\qquad a=\frac{n-6}{2},\quad c=\frac{n-2}{2}=a+2,
\]

and set

\[
\lambda=\ell(\ell+n-2),\qquad C=c^2+\lambda,\qquad d=C-4.
\]

The two boundary traces say (v(0)=v'(0)=0). The vanishing near the origin makes (v) compactly supported for large (t). A direct polar-coordinate calculation gives

\[
\Delta(u_\ell Y_\ell)=r^{-c}w(t)Y_\ell,
\qquad w=v''-4v'-dv.
\]

Since (n-2c-2=0), the energy and weighted denominator for this mode are respectively

\[
E_\ell=\int_0^\infty\bigl((w'+cw)^2+\lambda w^2\bigr)\,dt,
\qquad D_\ell=\int_0^\infty v^2\,dt.
\tag{2}
\]

Integrating the cross terms and using (v(0)=v'(0)=0) gives the exact identity

\[
\begin{split}
E_\ell={}&\int_0^\infty\bigl[
(v''')^2+(3C+8)(v'')^2
 +(d^2+C(16+2d))(v')^2+Cd^2v^2
\bigr]dt\\
&+(4-c)|v''(0)|^2.
\end{split}
\tag{3}
\]

For clarity, the boundary term has two contributions. The cross term in
(\int(w'+cw)^2) is (-c|w(0)|^2=-c|v''(0)|^2); the expansion of
(\int|v'''-4v''-dv'|^2) contributes (4|v''(0)|^2).

For any (A>0) and a smooth (f) vanishing at infinity,

\[
0\le\int_0^\infty(f'+\sqrt A f)^2dt
=\int_0^\infty((f')^2+Af^2)dt-\sqrt A|f(0)|^2.
\tag{4}
\]

Apply (4) with (f=v'') and (A=3C+8). The remaining boundary coefficient is
(\sqrt{3C+8}+4-c>0): this is immediate for (c\le4), while for (c>4),
(3C+8-(c-4)^2\ge 2c^2+8c-8>0).
Moreover (c>2), hence (C>4), (d>0), and all the remaining derivative coefficients in (3) are nonnegative. Consequently

\[
E_\ell\ge C(C-4)^2D_\ell
\ge c^2(c^2-4)^2D_\ell.
\tag{5}
\]

The last inequality follows because (s(s-4)^2) is increasing on (s>4) and (C\ge c^2>4). Since

\[
c^2(c^2-4)^2
=\left(\frac{(n-6)(n-2)(n+2)}8\right)^2,
\]

orthogonality and Parseval's identity sum (5) over the modes and prove the lower bound for the initial smooth class. One can equivalently first take finite spherical-harmonic sums and then pass to the limit; away from the origin the angular expansion converges in the relevant Sobolev and weighted norms.

### Density and the origin

The smooth closed-ball functions with the two vanishing lower traces are dense in (X_1) in (H^3). This is the usual smooth density theorem in the kernel of a subset of the Sobolev trace map on a smooth domain, obtainable from smooth approximation and a continuous right inverse for the traces.

The origin can then be removed by a diagonal cutoff argument. For each smooth approximant (u), multiply by a smooth cutoff (\chi_\varepsilon) that is zero on (B_\varepsilon), one outside (B_{2\varepsilon}), and obeys (D^j\chi_\varepsilon=O(\varepsilon^{-j})). For (0\le j\le3), the (L^2)-norms of the error terms are bounded by constants times (\varepsilon^{n/2-j}), or higher powers; they tend to zero because (n>6). This operation leaves the boundary traces unchanged. Thus the initial class is dense in (X_1) in (H^3).

Apply the established inequality to the resulting approximants. Their energies converge, and a subsequence converges pointwise almost everywhere. Fatou's lemma yields the weighted inequality for every (u\in X_1), including finiteness of the weighted denominator. Alternatively, applying the inequality to differences shows convergence in the weighted (L^2) norm.

### Sharpness and the whole-space constant

Choose a nonzero (\psi\in C_c^\infty((1,2))), and take the radial mode

\[
v_T(t)=\psi(t/T),\qquad
u_T(r)=r^{-a}\psi((-\log r)/T),\qquad T\longrightarrow\infty.
\]

Every (u_T) is smooth and compactly supported in the annulus
(e^{-2T}<r<e^{-T}), hence in (X_1) and indeed in (C_c^\infty(B_1)).
In (3), the boundary term vanishes, the denominator is of order (T), and the integrals of the squared first, second and third derivatives are of orders (T^{-1},T^{-3},T^{-5}). Therefore the quotient tends to (c^2(c^2-4)^2). This proves sharpness in (X_1).

For the whole-space inequality, the identical spherical-harmonic change of variables uses (t\in\mathbb R) instead of the half-line. For compactly supported smooth functions avoiding the origin, there are no boundary terms at all in (3), so (5) proves the same lower bound. The cutoff argument above extends it to arbitrary compactly supported smooth functions, and the defining completion extends it to the homogeneous Sobolev space (D^{3,2}(\mathbb R^n)). The same annular radial functions show sharpness there. This verifies the whole-space identification in (1).

## Limitation

No critical Sobolev lower bound
(S_{3,2}\|u\|_{L^{2n/(n-6)}(B_R)}^2\le\int_{B_R}|\nabla\Delta u|^2)
has been established here for all (u\in X_R). The spherical-harmonic proof works cleanly for the quadratic radial Hardy denominator, not the nonlinear critical Sobolev denominator. Do not report this proposition as preservation of both constants, as a result for arbitrary domains, or as a resolution of the original classification question.
