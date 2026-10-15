# Independent analytic and geometric reconstruction

Audit target: PR 662, head `e31701151c331a6eed9224fb37a75a374ea1043e`; problem 2306086. This derivation was written before opening the existing audit. It checks the qualitative theorem only, without a novelty or explicit sharp-bound claim.

## Claim and boundary conditions

Let \(\mathbb D=\{|z|<1\}\), and let \(S_{\mathbb R}\) consist of holomorphic injections \(f:\mathbb D\to\mathbb C\) with \(f(0)=0\), \(f'(0)=1\), and \(f(\bar z)=\overline{f(z)}\). Put

\[
A_f(z)=(1-|z|^2)\frac{f''(z)}{f'(z)}-2\bar z.
\]

The precise target is that \(M(z)=\max_{f\in S_{\mathbb R}}|A_f(z)|\) exists, equals 4 on \((-1,1)\), is strictly less than 4 on \(\mathbb D\setminus\mathbb R\), and admits a gap uniform on each compact subset of that latter set. The maximum is over functions at a fixed point, not a maximum over all nonreal points. All denominators below are inside the disk. The source expression at \(z=0\) is separately zero; it is not the normalized functional \(A_f(0)=f''(0)\).

## 1. Exterior construction, area, and exact equality

For normalized injective \(F(z)=z+a_2z^2+\cdots\), the only zero of \(F\) is 0. The function \(h(z)=F(z)/z\), extended by \(h(0)=1\), is holomorphic and zero-free on the simply connected disk, so it has a holomorphic logarithm \(L\) with \(L(0)=0\). Define

\[
H(w)=w\exp[-L(w^{-2})/2],\qquad |w|>1.
\]

This definition removes any ambiguity about the square root. It gives \(H(w)^2=1/F(w^{-2})\), an odd, nonzero holomorphic function, and
\(H(w)=w-(a_2/2)w^{-1}+O(w^{-3})\).

If \(H(w_1)=H(w_2)\), squaring and using injectivity of \(F\) gives \(w_1^{-2}=w_2^{-2}\), hence \(w_2=\pm w_1\). The minus sign, together with oddness, would force \(H(w_1)=0\). Thus \(H\) is injective on the exterior.

For any exterior injection \(H(w)=w+b_0+\sum_{n\ge1}b_nw^{-n}\), the circle \(|w|=R>1\) maps to a smooth Jordan curve. Its positive orientation is the one with the bounded component on the left: the holomorphic injection maps the exterior into the unbounded component, and its asymptotic behavior at infinity fixes that component. Green's formula and Fourier orthogonality give its enclosed area as

\[
\frac1{2i}\int_{|w|=R}\overline{H(w)}\,dH(w)
=\pi\left(R^2-\sum_{n\ge1}n|b_n|^2R^{-2n}\right)\ge0.
\]

Laurent series and their differentiated series converge uniformly on this circle. For every finite \(N\), \(\sum_{n=1}^N n|b_n|^2R^{-2n}\le R^2\); letting \(R\downarrow1\), then \(N\to\infty\), yields \(\sum n|b_n|^2\le1\) without any unproved interchange at the boundary.

For the constructed odd \(H\), \(b_1=-a_2/2\); hence \(|a_2|\le2\). Equality makes the single term \(|b_1|^2\) equal to 1, so every other negative coefficient vanishes. Its constant term already vanishes by oddness. Therefore

\[
H(w)=w-\lambda w^{-1},\quad |\lambda|=1,
\qquad F(z)=\frac{z}{(1-\lambda z)^2}=:k_\lambda(z).
\]

This argument proves the required equality case, rather than assuming that saturation of a bound merely suggests a slit image. Conversely, \(k_\lambda(z_1)=k_\lambda(z_2)\) factors as \((z_1-z_2)(1-\lambda^2 z_1z_2)=0\), so it is injective on the disk and attains the coefficient bound.

To identify its image, \((1+z)/(1-z)\) maps the disk onto \(\{\Re u>0\}\), and

\[
k_1(z)=\tfrac14\left[\left(\frac{1+z}{1-z}\right)^2-1\right].
\]

Squaring the right half-plane gives \(\mathbb C\setminus(-\infty,0]\). Thus \(k_1(\mathbb D)=\mathbb C\setminus(-\infty,-1/4]\), and rotation gives a single straight ray for every \(k_\lambda\).

## 2. Koebe transform and the equality information it actually supplies

An injective holomorphic function has nonzero derivative: if the first nonzero Taylor term at an interior point had degree \(m\ge2\), small nearby values would have \(m\) local preimages. Hence the following transform is defined:

\[
\phi_a(w)=\frac{a+w}{1+\bar a w},\qquad
F(w)=\frac{f(\phi_a(w))-f(a)}{(1-|a|^2)f'(a)}.
\]

Here \(\phi_a(0)=a\), \(\phi'_a(0)=1-|a|^2\), and \(\phi''_a(0)=-2\bar a(1-|a|^2)\). The normalization is \(F(0)=0\), \(F'(0)=1\), and

\[
F''(0)=(1-|a|^2)\frac{f''(a)}{f'(a)}-2\bar a=A_f(a).
\]

The coefficient theorem therefore yields \(|A_f(a)|\le4\), with equality forcing \(F=k_\lambda\). This conclusion concerns the transformed function. It does **not** directly imply that the original normalized \(f\) is a Koebe rotation. Solving the transform for \(f\) gives

\[
f(z)=\frac{k_\lambda(\phi_{-a}(z))-k_\lambda(-a)}{(1-|a|^2)k'_\lambda(-a)}.
\]

Such inverse transforms are normalized schlicht functions; in general they have an affine slit image with a different marked interior point and are not Koebe rotations. What transfers immediately is only that \(f(\mathbb D)\) is the complement of a straight ray, because the range differs from \(F(\mathbb D)\) by a nondegenerate complex affine map.

An exact adversarial control takes \(a=i/2\), \(\lambda=1\) in this formula. It has

\[
f(z)=z+\left(\frac65-\frac45i\right)z^2
+\left(\frac{11}{25}-\frac{48}{25}i\right)z^3+\cdots,
\qquad T_{i/2}f=k_1,\qquad A_f(i/2)=4.
\]

For any Koebe rotation, its coefficients obey \(4a_3-3a_2^2=0\); for this map that residual is \(-16/25-48i/25\). Thus it is not a Koebe rotation. Its omitted ray has endpoint \(-5/12\) and outgoing vector \(7/15-8i/5\). In particular, an endpoint can be real while the ray fails conjugation invariance. This verifies that the proof must constrain both the endpoint and the direction. The seven exact checks in `exact_adversarial_controls.py` all pass; they target this false shortcut rather than sample the claimed strict inequality.

## 3. Symmetry of the slit and conformal-radius normalization

If \(f\in S_{\mathbb R}\), its image is invariant under conjugation. Thus, under equality, its omitted ray \(R\) is conjugation invariant. A closed ray \(R=c+v[0,\infty)\), \(|v|=1\), has a unique finite endpoint \(c\). Conjugation must fix that endpoint, so \(c\) is real; equality of the remaining ray forces \(\bar v=v\), so \(v=\pm1\). Since 0 lies in the image, the ray is exactly one of

\[
(-\infty,c],\ c<0,\qquad [c,\infty),\ c>0.
\]

For the first domain the map \(g(z)=4|c|k_1(z)\) has \(g(0)=0\), derivative \(4|c|>0\), and the same image. For the second use \(g(z)=4c\,k_{-1}(z)\), again with derivative \(4c>0\). The inverse composition \(h=g^{-1}\circ f\), not the pointwise quotient of functions, is a disk automorphism fixing zero. Schwarz's lemma for it and its inverse makes \(h(z)=e^{i\theta}z\); therefore

\[
1=|h'(0)|=\frac1{4|c|}.
\]

It follows that \(|c|=1/4\), and the positive derivatives force \(h'(0)=1\), hence \(h\) is the identity. Only at this stage is the original function identified as \(k_1\) or \(k_{-1}\).

If the unnormalized real-on-real injection has negative derivative at zero, dividing \(f-f(0)\) by the real number \(f'(0)\) still gives an element of \(S_{\mathbb R}\). Neither the ratio \(f''/f'\) nor the theorem is affected. The normalized derivative is explicitly +1 throughout the comparison above.

For \(z=x+iy\), direct differentiation and cancellation give

\[
A_{k_1}(z)=\frac{4[(1-|z|^2)+iy]}{1-z^2},\qquad
A_{k_{-1}}(z)=\frac{4[-(1-|z|^2)+iy]}{1-z^2}.
\]

Since \(|1-z^2|^2=(1-|z|^2)^2+4y^2\), both satisfy

\[
|A_{k_{\pm1}}(z)|^2
=16-\frac{48y^2}{|1-z^2|^2}.
\]

The denominator is nonzero in the disk. Thus equality is excluded for every nonreal point in the real class, and \(A_{k_1}(x)=4\), \(A_{k_{-1}}(x)=-4\) for real \(x\in(-1,1)\). This is pointwise strictness; it still requires compactness for a uniform-in-function gap.

## 4. Compactness with the denominator and limit issues made explicit

The already proved universal inequality gives
\(|f''/f'|(re^{i\theta})\le(4+2r)/(1-r^2)\). Along each radius,

\[
\frac{d}{dr}\log|f'(re^{i\theta})|
=\Re\left(e^{i\theta}\frac{f''}{f'}(re^{i\theta})\right)
\le\frac{4+2r}{1-r^2}.
\]

Integration from 0 yields \(|f'(z)|\le(1+|z|)/(1-|z|)^3\); integrating \(f'\) radially then yields \(|f(z)|\le |z|/(1-|z|)^2\). Hence the normalized schlicht class is locally bounded and normal.

Suppose \(f_n\) converges locally uniformly to \(f\). Cauchy's formula preserves \(f(0)=0\) and \(f'(0)=1\), so \(f\) is not constant. For every fixed \(w\in\mathbb D\), define the holomorphic divided differences

\[
q_n(z)=\begin{cases}(f_n(z)-f_n(w))/(z-w),&z\ne w,\\f_n'(w),&z=w.\end{cases}
\]

They are zero-free and converge locally uniformly to the corresponding \(q\). Hurwitz's theorem makes \(q\) either zero-free or identically zero. The latter would make \(f\) constant; hence \(q\) is zero-free. This proves both that \(f\) is injective and that \(f'(w)\ne0\). Reflection symmetry passes to the limit. Thus \(S_{\mathbb R}\) is compact in the topology of local uniform convergence.

For fixed \(z\), derivative convergence and the nonzero limiting derivative make \(f\mapsto |A_f(z)|\) continuous. It attains its maximum. Since every value at nonreal \(z\) is strictly less than 4, the attained maximum is strictly less than 4. Mere nonattainment of 4 without this compactness would not establish the result.

For the compact-set version, if \(f_n\to f\) locally uniformly and \(z_n\to z\in\mathbb D\), Cauchy convergence on a compact neighborhood gives \(f_n^{(j)}(z_n)\to f^{(j)}(z)\), \(j=1,2\), and \(f'(z)\ne0\). Thus \((f,z)\mapsto |A_f(z)|\) is jointly continuous. On \(S_{\mathbb R}\times K\), with nonempty compact \(K\subset\mathbb D\setminus\mathbb R\), it attains a maximum \(m_K<4\); choose \(\epsilon_K=4-m_K\). For empty \(K\) the assertion is vacuous. Compactness here excludes approach both to the real axis and to the unit circle; a merely bounded or relatively closed subset of the open punctured domain is not sufficient.

For nonzero \(z\), multiplication by \(|z|/(1-|z|^2)\) transfers the bound to the displayed original expression. At real nonzero points the two Koebe examples give its sharp classical radius. At zero that expression is identically zero, as specified above.

## 5. Exact residual limitations

This argument determines neither the magnitude of \(4-M(z)\) at a general nonreal point nor its extremizer. It also does not settle priority, current literature, or the strongest intended meaning of the original problem. These are scope limitations, not defects in the stated qualitative theorem. No step of the reconstruction transfers the central qualitative strictness question to an unsupported stronger claim.

## 6. Later comparison with the existing audit

The core reconstruction in Sections 1–5 was recorded before the existing `audit/INDEPENDENT_AUDIT.md` was read; the explicit inverse-transform control in Section 2 was added afterwards. The existing audit's geometric conclusion agrees with this reconstruction. Its inverse-composition wording correction is already explicitly incorporated by `SCOPE_CLARIFICATION.md`. The existing audit is corroboration, not a premise used in the core reconstruction; its numerical/source claims were not certified in this analytic/geometric review.
