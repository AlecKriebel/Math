# Gradient lower bounds for shrinking Ricci solitons

Problem 30002086 / OWR-11789-007. Research date: 3 October 2026.

## Disposition

**Unsolved in this investigation after five substantive approaches.** No general proof or complete shrinking-soliton counterexample is supplied. The results below are conditional estimates, exact reformulations, and rigorous checks of limitations of attempted arguments. They are not claimed to be new theorems of independent research significance.

The question asks whether every smooth, connected, complete gradient shrinking Ricci soliton, normalized by

\[
\operatorname{Ric}+\nabla^2 f=\tfrac12 g,
\]

has a constant \(C>0\) such that

\[
|\nabla f|(x)\ge C^{-1}\quad\text{when }d_g(p,x)\ge C,
\tag{Q}
\]

where \(p\) minimizes \(f\). The constant may depend on the individual soliton. It is not asserted to depend only on dimension or entropy.

Haslhofer's contribution in the 2012 *Geometrie* report displays (Q) on printed p. 1669, equation (5), and poses its universal validity on p. 1670. The surrounding application is four-dimensional. The catalogue asks the dimension-free version; neither that version nor the unrestricted four-dimensional case is resolved here. The report's bibliographic year is 2012; online publication was 20 February 2013. [Official report](https://ems.press/content/serial-article-files/46397), [publication record](https://ems.press/journals/owr/articles/11789).

## 1. Normalization and exact logical target

Adding a constant to \(f\) changes neither its gradient nor its minimizing points. Hamilton's identity permits the normalization

\[
F=R+|\nabla F|^2,
\qquad F=f+c.
\tag{1}
\]

If instead \(\int_M(4\pi)^{-n/2}e^{-f}=1\), then \(c=-\mu(g)\), so \(F=f-\mu(g)\). These two conventions must not be silently identified.

Write \(r=d_g(p,\cdot)\), \(q=|\nabla F|^2\), and \(\Delta_F=\Delta-\langle\nabla F,\nabla\cdot\rangle\). The standard identities are

\[
R\ge0,\quad q=F-R,\quad \Delta F=n/2-R,
\quad \Delta_FF=n/2-F,
\quad \nabla R=2\operatorname{Ric}(\nabla F,\cdot).
\tag{2}
\]

Haslhofer–Müller, Lemma 2.1, gives

\[
\tfrac14(r-5n)_+^2\le F\le\tfrac14(r+\sqrt{2n})^2.
\tag{3}
\]

In particular \(F\) is proper and has a minimum. These facts require no global pointwise curvature bound. [2011 paper, Section 2](https://arxiv.org/abs/1005.3255).

If \(M\) is compact, choose \(C>\operatorname{diam}M\); the conclusion is vacuous. Hence a compact Einstein example with constant potential does not disprove (Q). If the shrinker equation is given with constant \(\lambda>0\), scale the metric to \(\bar g=2\lambda g\) before using the displayed constants. Distances multiply by \(\sqrt{2\lambda}\), gradient norms divide by that factor, and the existence assertion is unchanged.

For a noncompact soliton, the following are equivalent:

1. (Q).
2. Some \(c_0>0,r_0<\infty\) satisfy \(q\ge c_0\) on \(\{r\ge r_0\}\).
3. Some \(c_0>0,A<\infty\) satisfy \(F-R\ge c_0\) on \(\{F\ge A\}\).

For (2) to (1), take \(C\ge\max(r_0,c_0^{-1/2})\). The equivalence with (3) follows from (3) and properness. Thus a full proof needs an **absolute positive gap** between scalar curvature and the normalized potential at infinity.

Failure is equivalent to an escaping sequence \(x_j\) with \(q(x_j)\to0\). Such a sequence necessarily satisfies

\[
F(x_j)\longrightarrow\infty,\quad
\frac{F(x_j)}{r(x_j)^2}\longrightarrow\tfrac14,\quad
\frac{R(x_j)}{r(x_j)^2}\longrightarrow\tfrac14,\quad
\frac{R(x_j)}{F(x_j)}\longrightarrow1,
\tag{4}
\]

and, more strongly, \(F(x_j)-R(x_j)\to0\). Ratio saturation alone does not imply failure: an absolute gap of one would still prove (Q).

## 2. Approach one: scalar-gap estimates and model tests

**Proposition.** Suppose that, outside a compact set,

\[
R\le\alpha r^2+B,\qquad \alpha<1/4.
\tag{5}
\]

Then (Q) holds, and \(|\nabla f|\) in fact grows at least linearly at infinity.

**Proof.** Put \(\delta=1/4-\alpha>0\). For \(r\ge5n\), (1) and (3) imply

\[
q\ge\delta r^2-\frac{5n}{2}r+\frac{25n^2}{4}-B.
\]

For \(r\ge10n/\delta\), the linear loss is at most \(\delta r^2/4\). If also \(r^2\ge4\max(B,0)/\delta\), the constant loss is at most \(\delta r^2/4\). Consequently \(q\ge\delta r^2/2\). This proves the proposition. The sufficient condition itself is already recorded in Haslhofer–Müller's 2011 paper, Remark following Theorem 1.2; it is not a new resolution.

A bounded scalar curvature \(R\le A\) is a special case, directly giving

\[
q\ge\tfrac14(r-5n)_+^2-A.
\tag{6}
\]

More generally, \(R\le(1-\varepsilon)F\) outside a compact set yields \(q\ge\varepsilon F\). Neither curvature condition is part of the unrestricted problem.

For the Gaussian \(\mathbb R^n\), \(F=|x|^2/4\) and \(|\nabla F|=r/2\). For \(N^k\times\mathbb R^m\), \(m\ge1\), with compact \(N\) satisfying \(\operatorname{Ric}_N=g_N/2\),

\[
F=k/2+|z|^2/4,\quad R=k/2,\quad q=|z|^2/4.
\]

If \(D=\operatorname{diam}N\), then \(r^2=d_N(p_N,y)^2+|z|^2\) and \(q\ge(r^2-D^2)_+/4\). Thus the noncompact product models pass the test, even though the minimum set can have positive dimension.

**Remaining obstruction.** The known universal estimate is only \(R\le F\), with quadratic leading coefficient \(1/4\). It does not supply either (5) or the weaker absolute gap in Section 1.

## 3. Approach two: minimizing geodesics and the endpoint curvature term

Let \(\gamma:[0,r]\to M\) be a unit-speed minimizing geodesic from \(p\) to \(x\). The soliton equation gives the exact identity

\[
\langle\nabla F(x),\dot\gamma(r)\rangle
= r/2-\int_0^r\operatorname{Ric}(\dot\gamma,\dot\gamma)\,ds,
\tag{7}
\]

because \(\nabla F(p)=0\). In particular, a uniform upper bound on the geodesic integral would prove linear growth.

For \(r\ge2\), choose the usual cutoff \(\phi=s\) on \([0,1]\), \(\phi=1\) on \([1,r-1]\), and \(\phi=r-s\) on \([r-1,r]\). The summed index form gives

\[
\int_0^r\phi^2\operatorname{Ric}(\dot\gamma,\dot\gamma)\,ds
\le(n-1)\int_0^r|\phi'|^2ds=2(n-1).
\]

If Ricci curvature on the two endpoint segments is bounded above in the relevant direction by \(K_p,K_x\ge0\), respectively, then

\[
\int_0^r\operatorname{Ric}(\dot\gamma,\dot\gamma)ds
\le2(n-1)+\tfrac23(K_p+K_x).
\tag{8}
\]

The coefficient follows from \(\int_0^1(1-s^2)ds=2/3\). Under a global bound \(\operatorname{Ric}\le Kg\), (7)–(8) imply

\[
|\nabla F|(x)\ge r/2-2(n-1)-4K/3.
\tag{9}
\]

This is a version of the mechanism used by Fang–Man–Zhang in their finite-topological-type theorem. Their title alone must not be read as an unconditional theorem: the Ricci/Bakry–Émery results have additional assumptions, and their shrinking-soliton corollary assumes bounded scalar curvature. [2008 paper, Theorems 1–2 and Section 2](https://arxiv.org/abs/0801.0103).

**Remaining obstruction.** Smoothness bounds \(K_p\), but not \(K_x\) uniformly as \(x\) escapes. Scalar nonnegativity does not give an upper bound on a directional Ricci eigenvalue. Replacing the unknown endpoint term by a constant would assume the missing geometric information.

## 4. Approach three: Bochner and maximum principles

Weighted Bochner applied to \(F\), using \(\operatorname{Ric}_F=g/2\), gives

\[
\tfrac12\Delta_Fq
=|\nabla^2F|^2+\langle\nabla F,\nabla\Delta_FF\rangle
+\operatorname{Ric}_F(\nabla F,\nabla F)
=|\nabla^2F|^2-q/2.
\]

Hence

\[
\Delta_Fq=2|\nabla^2F|^2-q
\ge\frac2n(n/2-F+q)^2-q.
\tag{10}
\]

At a hypothetical small-gradient point with large \(F\), the right side is strongly positive. This has the **wrong sign for excluding a minimum** of \(q\): a local minimum satisfies \(\Delta_Fq\ge0\), consistently with (10).

At an actual critical point of \(F\), differentiation yields

\[
\nabla^2q=2(\nabla^2F)^2,
\tag{11}
\]

a positive-semidefinite tensor. Also, \(\Delta F=n/2-F\) there. Thus any critical point with \(F>n/2\) cannot be a local minimum of \(F\), but can be a saddle or maximum; its gradient-square is nevertheless at a minimum. This eliminates a tempting mistaken inference from the existence of a minimizing basepoint.

The scalar equation is

\[
\Delta_FR=R-2|\operatorname{Ric}|^2\le R-2R^2/n.
\tag{12}
\]

A high positive scalar maximum is also consistent with the sign of (12). These formulas alone do not rule out arbitrarily thin high-curvature, low-gradient regions. In fact (10) forces large Hessian norm along a bad sequence:

\[
|\nabla^2F|(x_j)\ge|n/2-F(x_j)+q(x_j)|/\sqrt n.
\]

**Remaining obstruction.** No applicable minimum principle with the opposite inequality or uniform local derivative control was obtained. Formal use of an Omori–Yau minimum sequence would retain the compatible sign, rather than produce a contradiction.

## 5. Approach four: topology, properness, and a rigorous false-inference test

If the critical points of \(F\) are confined to a compact set, choose a regular level \(a\) above that set. On \(\{F\ge a\}\), the vector field

\[
X=\nabla F/q
\]

satisfies \(X(F)=1\). Integral curves exist across every bounded interval of \(F\)-values because the corresponding slab is compact and contains no zero of \(q\). Thus the end is a product of the compact level set with a half-line, and \(M\) has finite topological type. A positive uniform lower gradient bound implies this conclusion. The converse has not been established for shrinkers, and even absence of critical points at infinity is logically weaker than (Q).

Here is a precise check showing that proper quadratic growth, \(|\nabla\sqrt F|\le1/2\), and absence of critical points on the ends do not by themselves imply (Q).

Choose a smooth bump \(\psi\), supported in \([-1,1]\), with \(0\le\psi\le1\), \(\psi(0)=1\), and \(\psi'(0)=0\). For integers \(k\ge2\), let

\[
\varepsilon_k=2^{-k-3},\qquad a_k=1-k^{-3},\qquad
b(r)=\frac{r}{\sqrt{1+r^2}}
\sum_{k=2}^{\infty}a_k\psi((r-k)/\varepsilon_k),\quad r\ge0.
\]

The supports are disjoint and locally finite. Set

\[
H(r)=\sqrt{1+r^2}-\int_0^r b(s)ds,
\qquad F_0(x)=\tfrac14H(|x|)^2\quad(x\in\mathbb R).
\tag{13}
\]

Because the sum vanishes near zero, \(F_0\) is smooth on all of \(\mathbb R\). Moreover,

\[
0\le\int_0^r b(s)ds\le2\sum_{k=2}^{\infty}\varepsilon_k=1/8,
\]

so \(H>0\), \(H=r+O(1)\), and \(F_0\) is proper with \(F_0=r^2/4+O(r)\). For \(r>0\),

\[
0<H'(r)=\frac r{\sqrt{1+r^2}}
\left(1-\sum_{k=2}^{\infty}a_k\psi((r-k)/\varepsilon_k)\right)\le1.
\]

Consequently zero is the unique critical point of \(F_0\), and

\[
0<F_0'(k)=\frac{H(k)}2\frac{k}{\sqrt{1+k^2}}k^{-3}
\le\frac1{2k^2}\longrightarrow0.
\tag{14}
\]

The auxiliary function \(S_0=F_0-|F_0'|^2=H^2(1-H'^2)/4\) is nonnegative. The bounds in (3), with \(n=1\), even hold for this profile with \(p=0\): \(H>0\) together with \(H\ge r-1/8\) implies \(H\ge(r-5)_+\), while \(H\le\sqrt{1+r^2}\le r+\sqrt2\).

**This is not a Ricci-soliton counterexample.** On the Euclidean line scalar curvature is zero, whereas \(S_0\) is merely an auxiliary function. Also \(F_0''=1/2\), required by the one-dimensional shrinking equation, fails at the bump centers: using \(\psi'(0)=0\),

\[
F_0''(k)\le\tfrac12\left(k^{-6}+\frac1{k^3(1+k^2)}\right)<1/2\qquad(k\ge2).
\]

This construction isolates precisely which deductions cannot replace the full soliton equation.

Recent literature continues to distinguish these issues. Bertellotti–Buzano's *Ends of (singular) Ricci shrinkers*, published online in 2025 and in volume 32 (2026), imposes absence of far-out critical points where needed. Fei He's May 2026 preprint discusses general finite topology as a question beyond the Kähler case, and proves topology theorems under stated curvature conditions. Neither supplies the absolute scalar-potential gap required here. [Bertellotti–Buzano](https://doi.org/10.1007/s00029-025-01104-y), [He](https://arxiv.org/abs/2605.04476).

## 6. Approach five: blow-up of a hypothetical bad sequence

Suppose (Q) fails. Put \(a_j=F(x_j)\to\infty\), \(g_j=a_jg\), and \(u_j=F-a_j\). Constant metric scaling gives

\[
\operatorname{Ric}_{g_j}+\nabla^2_{g_j}u_j=\frac1{2a_j}g_j,
\quad R_{g_j}+|\nabla u_j|_{g_j}^2=1+u_j/a_j.
\tag{15}
\]

At the basepoint,

\[
u_j(x_j)=0,\quad |\nabla u_j|_{g_j}^2(x_j)=q(x_j)/a_j\to0,
\quad R_{g_j}(x_j)\to1.
\]

**Conditional limit statement.** If these pointed manifolds and potentials converge smoothly on compact sets to a complete smooth limit, its equations are

\[
\operatorname{Ric}+\nabla^2u=0,\qquad R+|\nabla u|^2=1,
\quad \nabla u(o)=0,\quad R(o)=1.
\tag{16}
\]

These are steady, not shrinking, soliton equations. They are not contradictory. An explicit complete example satisfying (16) in dimension two is the scaled cigar

\[
g_{\rm cig}=\frac4{1+x^2+y^2}(dx^2+dy^2),\qquad
u=-\log(1+x^2+y^2).
\]

A direct computation yields

\[
R=\frac1{1+x^2+y^2},\quad |\nabla u|^2=\frac{x^2+y^2}{1+x^2+y^2},
\quad\operatorname{Ric}+\nabla^2u=0.
\tag{17}
\]

The origin has \(u=0,\nabla u=0,R=1\). Completeness follows from divergence of \(\int_0^\infty2(1+r^2)^{-1/2}dr\). Taking a product with Euclidean space gives examples of (16) in every dimension \(n\ge2\), including four.

This does not assert that cigar products occur as these blow-up limits. Additional inherited geometric conditions could exclude them. It proves only that the limiting equations and basepoint values alone do not yield the desired contradiction. Smooth compactness around escaping points also remains unproved in this argument.

The 2015 Haslhofer–Müller note does not fill that gap: its four-dimensional local energy and noncollapsing constants are formulated on balls about minimizing basepoints and depend on radius. It removes the gradient hypothesis from a compactness theorem using a different curvature argument; it does not deduce that hypothesis for each shrinker. [2015 note, Theorem 1.1 and Section 2](https://arxiv.org/abs/1407.1683).

## 7. What is established and what remains

Established here: exact normalization and failure sequence; conditional linear estimates under a strict quadratic scalar bound; geodesic endpoint calculation; correct Bochner signs; the finite-topology implication; an explicit non-soliton false-inference test; and the exact rescaled steady-limit equations and complete steady comparison example.

Not established: a curvature-free positive lower bound for \(|\nabla f|\) outside a compact set, boundedness of the far-out critical set for arbitrary shrinkers, or any actual shrinking-soliton counterexample. The exact remaining target is to prove or disprove

\[
\liminf_{r(x)\to\infty}(F(x)-R(x))>0
\]

for every complete noncompact gradient shrinker. No claim of exhaustive literature coverage or priority is made. The accompanying symbolic checks verify displayed algebra and comparison examples; they do not certify a universal geometric theorem.
