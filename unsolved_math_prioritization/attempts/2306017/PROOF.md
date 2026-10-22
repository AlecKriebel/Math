# Minimum image area with a prescribed second coefficient

## Disposition and attribution

Hayman–Lingham Problem 6.17 (catalogue ID 2306017, AMR-022-6017) has a published solution by Dov Aharonov, Harold S. Shapiro and Alexander Yu. Solynin. This is an attribution and mathematical verification note, not a claim of a new solution.

Let S consist of holomorphic injective functions

\[
f(z)=z+\sum_{n\ge2}a_nz^n\qquad (|z|<1).
\]

Write \(a=|a_2|\). The minimum of \(A(f)=\operatorname{area}f(\mathbb D)\) is

\[
M(a)=
\begin{cases}
\pi(1+2a^2),&0\le a\le\tfrac12,\\[2mm]
\dfrac{27\pi}{8(2-a)^2},&\tfrac12<a<2.
\end{cases}
\tag{1}
\]

At \(a=2\), only a rotation of the Koebe function is possible and its area is infinite. For \(a>2\), the class is empty. These endpoint assertions use the classical second-coefficient theorem and its equality case.

The resolving paper is [Aharonov–Shapiro–Solynin (1999)](https://doi.org/10.1007/BF02791132), J. Analyse Math. 78, 157–176. A later proof and the explicit extremal occur in Theorems 3–4, pp. 106–109, of [their 2006 paper](https://doi.org/10.1007/BF02790271); its [author-posted full text](https://www.academia.edu/31230874/Minimal_area_problems_for_functions_with_integral_representation) is available. The 1999 full text was not obtained, and this note does not claim to have checked that original proof.

## 1. Explicit extremal and independent normalization check

Rotations \(f(z)\mapsto e^{-i\theta}f(e^{i\theta}z)\) preserve area and multiply the second coefficient by \(e^{i\theta}\), so consider \(a_2=a\ge0\).

For \(a\le1/2\), the polynomial \(z+az^2\) is injective: equality of its values at distinct \(z,w\in\mathbb D\) would require \(1+a(z+w)=0\), impossible because \(|a(z+w)|<1\). The coefficient area formula proves both (1) and uniqueness in this range.

For \(1/2<a<2\), set

\[
\tau=\frac23(2-a),\quad k(z)=\frac{z}{(1-z)^2},\quad
p_\tau(z)=k^{-1}(\tau k(z)),\quad
F_\tau(z)=\frac{p_\tau(z)+p_\tau(z)^2/2}{\tau}.
\tag{2}
\]

Here \(0<\tau<1\) and the inverse branch satisfies \(p_\tau(0)=0\). Since \(k\) maps the disk conformally onto \(\mathbb C\setminus(-\infty,-1/4]\), the function \(p_\tau\) maps the disk conformally onto a disk with a segment of its negative radius removed. Thus \(F_\tau\) is injective, being the composition of \(p_\tau\) and the injective polynomial \(q(w)=w+w^2/2\), followed by a dilation.

Expansion of \(k(p_\tau)=\tau k(z)\) gives

\[
p_\tau(z)=\tau z+2\tau(1-\tau)z^2+O(z^3),\qquad
F_\tau(z)=z+(2-3\tau/2)z^2+O(z^3).
\]

Consequently \(F_\tau\in S\) has exactly the prescribed coefficient. The removed segment and its image under \(q\) have zero planar area. Since \(A(q)=\pi(1+2/4)=3\pi/2\),

\[
A(F_\tau)=\frac{3\pi}{2\tau^2}
=\frac{27\pi}{8(2-a)^2}.
\tag{3}
\]

This proves attainment of the stated value as an **upper bound**; the lower bound is separate.

## 2. Verification of the typically-real lower bound

A normalized analytic function is typically real if
\(\operatorname{Im}f(z)\operatorname{Im}z\ge0\). Use the classical Robertson representation, equivalently the Herglotz representation applied to \((1-z^2)f(z)/z\):

\[
f(z)=\int_0^\pi\frac{z}{1-2z\cos t+z^2}\,d\rho(t),\qquad
\rho([0,\pi])=1,\quad \int\cos t\,d\rho(t)=a/2.
\tag{4}
\]

This standard representation is an external theorem input, also used in the 2006 paper, equation (4.2). For an analytic function that need not be univalent, write
\[
E(f)=\int_{\mathbb D}|f'(z)|^2\,dA
    =\pi\sum_{n\ge1}n|a_n|^2.
\]
This is area counted with multiplicity. It equals the ordinary image area \(A(f)\) for univalent functions. The bound in this section concerns \(E\), not ordinary image area for a possibly noninjective typically-real function.

For the Dirichlet inner product \(\langle g,f\rangle=\int_{\mathbb D}g'\overline{f'}\,dA\), the representation and the real Taylor coefficients of \(F_\tau\) give

\[
\operatorname{Re}\langle F_\tau,f\rangle
=\int_0^\pi H_\tau(t)\,d\rho(t),\qquad
H_\tau(t)=\pi\frac{\operatorname{Im}(e^{it}F_\tau'(e^{it}))}{\sin t}.
\tag{5}
\]

For completeness, the coefficient of \(z^n\) in the integrand of (4) is
\(\sin(nt)/\sin t\). Integrating on \(|z|<r\) first gives (5) with
\(\pi r^2\operatorname{Im}(e^{it}F_\tau'(r^2e^{it}))/\sin t\).
These kernels converge uniformly, including the removable endpoints: \(F_\tau'\) is continuous on the closed disk and analytic near \(1\) and \(-1\). Away from those endpoints \(\sin t\) is bounded away from zero. Near them analyticity and reflection make the difference quotients uniform. For finite Dirichlet energy, the inner products converge by Cauchy–Schwarz. Infinite energy needs no argument.

The continuity assertion follows directly by differentiating (2):

\[
F_\tau'(z)=\tau^{-3/2}(1+z)
                 \left(\frac{p_\tau(z)}z\right)^{3/2}.
\tag{6}
\]

The analytic power is fixed by its positive value at zero. The two square-root singularities of \(p_\tau'\) cancel against \(1+p_\tau\); \(p_\tau/z\) is nonzero and continuous on the closed disk.

Put \(y=\sin(t/2)\) and \(t_0=2\arcsin\sqrt\tau\). On \(0<t<t_0\), write \(p_\tau(e^{it})=e^{i\phi}\), so \(\sin(\phi/2)=y/\sqrt\tau\). The triple-angle identity and (6) give

\[
H_\tau(t)=\pi\tau^{-3}(3\tau-4y^2)
          =\pi\tau^{-3}(3\tau-2+2\cos t).
\tag{7}
\]

On \(t_0<t<\pi\), put \(s=\sqrt{y^2-\tau}\). The upper boundary value of the Pick function is
\(p_\tau(e^{it})=-(y-s)^2/\tau\), and (6) yields

\[
H_\tau(t)=-\pi\tau^{-3}\frac{(y-s)^3}{y}.
\]

Subtracting the affine expression on the right of (7) gives the nonnegative exact remainder

\[
\pi\tau^{-3}\left(4y^2-3\tau-\frac{(y-s)^3}{y}\right)
=\pi\tau^{-3}\frac{s(4y^2-\tau)}{y}\ge0.
\tag{8}
\]

Integration against (4) now gives

\[
\operatorname{Re}\langle F_\tau,f\rangle
\ge\pi\tau^{-3}(3\tau-2+a)
=\frac{3\pi}{2\tau^2}=A(F_\tau).
\]

Finally,

\[
E(f)=E(F_\tau)+2\operatorname{Re}\langle F_\tau,f-F_\tau\rangle
                         +\|f'-F_\tau'\|_{L^2}^2
\ge E(F_\tau)=A(F_\tau).
\tag{9}
\]

Equality in (9) forces \(f=F_\tau\). This calculation checks the lower-bound mechanism in the 2006 paper with a probability measure on \([0,\pi]\); its kernel therefore has half the factor used with that paper's half-mass measure.

## 3. Passage to arbitrary univalent functions by ordinary conformal radius

The geometric theorem input is the classical circular-symmetrization inequality
\[
R(V,0)\le R(V^*,0),
\tag{10}
\]
where \(R\) is ordinary conformal radius and \(V^*\) is the circular symmetrization of a simply connected domain containing zero. Its precise source is [Dubinin (1994)](https://www.mathnet.ru/eng/rm1153), pp. 19–20, equation (1.17), together with equation (1.8), p. 13, relating the interior reduced modulus to \((2\pi)^{-1}\log R\). These displays and definitions were checked as page images. This is the interior invariant at zero, not the reduced modulus of a biangle with zero on its boundary.

We give the coefficient comparison explicitly. First suppose \(f\in S\) extends univalently to a neighborhood of the closed disk. Put \(\Omega=f(\mathbb D)\), and let \(C=\Omega^*\), symmetrized about the positive real axis. On each circle, circular symmetrization replaces a proper intersection by a centered **open** arc of the same angular length. A whole circle is retained only when the original domain contains that whole circle. In particular a punctured circle of angular measure \(2\pi\) remains punctured at the negative axis. This distinction is essential for the slit argument below.

For clarity, the domains used here remain simply connected. The complement of a bounded simply connected domain containing zero is connected and meets every circle of radius at least the distance from zero to its boundary. After circular symmetrization, every complementary arc attaches to the negative ray. The rearranged domain is connected because each of its circular arcs meets the positive axis, and the radial range of the original connected domain is an interval. Its complement is connected as well. Deleting a further terminal negative radial segment retains these properties. Area is preserved by circular symmetrization, by integration of angular lengths.

Let \(\delta=\operatorname{dist}(0,\partial\Omega)>0\). Then \(C\) contains the disk of radius \(\delta\), and its negative real intersection is \((-\delta,0)\). For \(0<t\le\delta\), set
\[
C_t=C\setminus(-\infty,-t].
\]
At \(t=\delta\), \(C_t=C\), so (10) gives \(R(C_\delta,0)\ge1\). As \(t\downarrow0\), Koebe's quarter theorem gives \(R(C_t,0)\le4t\to0\). The domains vary continuously in the Carathéodory kernel sense for \(t>0\); hence their conformal radii vary continuously. Choose \(t\) with \(R(C_t,0)=1\), and let \(G:\mathbb D\to C_t\) satisfy \(G(0)=0\), \(G'(0)=1\).

For \(0<x<1\), put
\[
U_x=\mathbb D\setminus[-1,-x],\qquad
c_x=|f(-x)|,\qquad T_x=-G(-x)>0.
\]
Reflection symmetry and uniqueness of the normalized Riemann map imply that \(G\) is real on \((-1,1)\). Its derivative there is positive, since it is real, nonzero, and positive at zero. The inverse map is real-symmetric too, so this real interval maps onto the real component of \(C_t\) containing zero. Its negative real endpoint is \(-t\). Consequently
\[
B_x=G(U_x)=C\setminus(-\infty,-T_x].
\tag{11}
\]

Let \(E_x=f(U_x)\). Its complement contains the curve \(f([-1,-x])\), joined at \(f(-1)\) to the unbounded complement of \(\Omega\). Thus it meets every circle of radius \(s\ge c_x\). The definition of circular symmetrization implies that \(E_x^*\) excludes every negative point \(-s\) with \(s\ge c_x\), even if the original circle was missing only one point. Also \(E_x\subset\Omega\) implies \(E_x^*\subset C\). Therefore
\[
E_x^*\subset C\setminus(-\infty,-c_x].
\tag{12}
\]

If \(c_x<T_x\), (11)–(12) give \(E_x^*\subsetneq B_x\): every point \(-s\) with \(c_x<s<T_x\) belongs to \(B_x\) and is excluded from \(E_x^*\). Both are simply connected domains containing zero. Strict monotonicity of conformal radius now gives
\[
R(U_x,0)=R(E_x,0)\le R(E_x^*,0)<R(B_x,0)=R(U_x,0),
\]
a contradiction. The equalities use conformal covariance and \(f'(0)=G'(0)=1\). Strict monotonicity also follows directly from Schwarz's lemma applied to the normalized Riemann maps of the two nested domains. We have proved
\[
-G(-x)\le |f(-x)|\qquad(0<x<1).
\tag{13}
\]

Rotate the initial map so that \(a_2(f)=a\ge0\), and write \(G(z)=z+bz^2+\cdots\), with \(b\) real. At zero, (13) reads
\[
x-bx^2+O(x^3)\le x-ax^2+O(x^3),
\]
so \(b\ge a\). A normalized real-symmetric univalent map is typically real: a nonreal point cannot map to a real point, since its conjugate would have the same image, and the sign in the upper half disk is fixed near zero. Since \(G\) is bounded, the second-coefficient theorem gives \(b<2\). For \(a>1/2\), Section 2 therefore yields
\[
A(f)=A(G)\ge M(b)\ge M(a).
\tag{14}
\]
Area equality uses circular symmetrization and the zero area of the deleted radial segment. Both branches of \(M\) are increasing and agree at \(a=1/2\). The smaller coefficient range was proved directly in Section 1.

For arbitrary \(f\in S\), apply this conclusion to \(f_\rho(z)=f(\rho z)/\rho\), \(0<\rho<1\), which extends univalently past the closed disk and has second coefficient \(\rho a_2\). The coefficient formula gives
\[
A(f_\rho)=\pi\sum_{n\ge1}n|a_n|^2\rho^{2n-2}\uparrow A(f),
\]
so continuity of \(M\) proves the lower bound as \(\rho\uparrow1\). Together with (3), this gives (1) for the exact original problem, using the explicitly identified classical theorem inputs.

## 4. Status and verification limits

The 2018 arXiv version of Hayman–Lingham still says no progress had been reported on 6.17. That sentence is not current mathematical evidence against the published solution.

The 1999 publisher's HTML abstract displays a denominator 7. The explicit construction (3) disproves that stronger numerical bound. The correct denominator 8 is printed in the 1974 primary announcement and in the 2006 Theorem 3. The earlier announcement was conditional on topological assumptions and is not used as the resolving proof.

Section 3 avoids the biangle comparison in the 2001 paper. Its author-posted OCR gives a strict decrease of the biangle reduced modulus under the stated symmetrization, whereas the cited Solynin (1993), Lemma 1.3, printed p. 120, gives the opposite non-strict direction for its specialized transformation. This source discrepancy remains unresolved. Neither that inequality nor the unavailable 1999 coefficient lemma is used above.

The proof retains the classical Robertson–Herglotz representation, Riemann mapping and kernel convergence theorems, ordinary conformal-radius symmetrization, and the second-coefficient theorem as external inputs. It is not a formal proof assistant certificate or a reconstruction of every foundational proof. The ordinary symmetrization source was inspected as page images; the 2001 and 2006 papers were read as public author-posted OCR. The historical 1999 full proof remains unread.

The argument proves the minimum value and gives attaining maps. It independently proves uniqueness only in the polynomial range and in the typically-real Dirichlet-energy problem. Classification of all equality cases in the full univalent class for \(1/2<a<2\) is not proved here and remains attributed to the published 2006 Theorem 4. No new theorem or priority is claimed.
