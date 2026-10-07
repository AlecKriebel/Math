# Approach 5: can maximization within a normal fan give a classification?

## Strategy tested

One possible global construction is to maximize the Riesz energy among area-one polygons with prescribed allowed normal directions. An interior maximizer would have the required sliding stationarity. To turn this into a classification, one would at least need to exclude collapsed-side boundary maximizers and then prove uniqueness or characterize every critical branch.

The calculation concerns the Riesz-only objective while varying the candidate Wulff shape. A vertex cut is not a fixed-normal deformation of the original triangle, and no decrease of its full crystalline energy is asserted.

The following calculation isolates a concrete obstruction to a uniform boundary-exclusion argument. It is a mathematical shape-variation calculation, not a literature or packaging step.

## 1. Birth of a side by cutting a vertex

Let \(P\) have area 1, let \(p\) be a vertex, and remove a small triangular cap \(D_t\) around \(p\), obtained by inserting a fixed new supporting direction. Write \(\delta_t=|D_t|\to0\), \(Q_t=P\setminus D_t\), and
\[
\widehat Q_t=(1-\delta_t)^{-1/2}Q_t.
\]
Then \(|\widehat Q_t|=1\). The cap shrinks to \(p\), and continuity of \(v_P\) gives
\[
\int_{D_t}v_P=\delta_t v_P(p)+o(\delta_t).
\]
The self-energy estimate \(V_\alpha(D_t)\le C\delta_t^{2-\alpha/2}=o(\delta_t)\) is valid for every \(\alpha<2\). Therefore
\[
V_\alpha(Q_t)=V_\alpha(P)-2\delta_t v_P(p)+o(\delta_t).
\]
By the homogeneity \(V_\alpha(rE)=r^{4-\alpha}V_\alpha(E)\),
\[
V_\alpha(\widehat Q_t)-V_\alpha(P)
=\delta_t\left[\frac{4-\alpha}{2}V_\alpha(P)-2v_P(p)\right]+o(\delta_t).
\tag{1}
\]
If \(P\) is sliding-critical with common side average \(A\), Euler's identity and \(\sum_i h_i\ell_i=2|P|\) imply
\[
(4-\alpha)V_\alpha(P)=2\sum_i h_i\int_{L_i}v_P=4A|P|.
\]
For area one, (1) becomes
\[
V_\alpha(\widehat Q_t)-V_\alpha(P)
=2\delta_t[A-v_P(p)]+o(\delta_t).
\tag{2}
\]
Thus the sign depends on a vertex value, not solely on equal side averages.

## 2. Positive sign: equilateral triangles

Take an equilateral triangle and one of its sides, positioned horizontally with midpoint at 0. Every horizontal slice of the triangle is a centered interval. For each fixed positive vertical distance \(y\), convolution of the strictly decreasing even function \(s\mapsto(s^2+y^2)^{-\alpha/2}\) with a centered interval is even and strictly decreasing for positive horizontal coordinates. This follows directly by differentiating its endpoint antiderivative:
\[
\frac d{dx}\int_{-a}^{a}[(x-s)^2+y^2]^{-\alpha/2}\,ds
=[(x+a)^2+y^2]^{-\alpha/2}-[(x-a)^2+y^2]^{-\alpha/2}<0
\]
for \(x>0,a>0\). Integrating over slices proves that \(v_P\) along the base is strictly decreasing from its midpoint to either endpoint. The endpoint value is therefore strictly below the side average \(A\). Rotation symmetry gives this at each vertex.

Consequently every sufficiently small fixed-direction vertex cut, followed by area renormalization, strictly **increases** \(V_\alpha\). This supplies a valid boundary-exclusion direction at an equilateral triangular boundary shape.

## 3. Negative sign: very obtuse triangles

The opposite sign also occurs, already for any fixed \(0<\alpha<1\). Let
\[
T_\varepsilon=\operatorname{conv}\{(-1,0),(1,0),(0,\varepsilon)\},
\qquad p_\varepsilon=(0,\varepsilon),\qquad |T_\varepsilon|=\varepsilon.
\]
Put \(w(x)=1-|x|\) for \(|x|\le1\). The cross section at horizontal position \(x\) is \(0<y<\varepsilon w(x)\).

By changing variables \(y=\varepsilon s\) and dominated convergence,
\[
\frac{v_{T_\varepsilon}(p_\varepsilon)}{\varepsilon}
\longrightarrow J_\alpha:=\int_{-1}^1w(x)|x|^{-\alpha}\,dx
=\frac2{(1-\alpha)(2-\alpha)}.
\tag{3}
\]
The domination is by \(w(x)|x|^{-\alpha}\), integrable for \(\alpha<1\).

Similarly,
\[
\frac{V_\alpha(T_\varepsilon)}{\varepsilon^2}
\longrightarrow I_\alpha:=\int_{-1}^1\int_{-1}^1
w(x)w(y)|x-y|^{-\alpha}\,dx\,dy.
\tag{4}
\]
Here the dominating kernel is \(w(x)w(y)|x-y|^{-\alpha}\), also integrable for \(\alpha<1\).

An exact one-dimensional convolution calculation gives
\[
I_\alpha=
\frac{2(2^{4-\alpha}-4)}
 {(1-\alpha)(2-\alpha)(3-\alpha)(4-\alpha)}.
\tag{5}
\]
For a direct verification, \(w*w\) is even and equals
\[
(w*w)(u)=
\begin{cases}
\frac23-u^2+\frac12u^3,&0\le u\le1,\\
\frac16(2-u)^3,&1\le u\le2,\\
0,&u\ge2.
\end{cases}
\]
Insert this into \(I_\alpha=2\int_0^2u^{-\alpha}(w*w)(u)\,du\), integrate the displayed polynomials, and simplify to (5).

Every triangle is sliding-critical. If \(A_\varepsilon\) is its common side average, the scaling identity above gives
\[
\frac{A_\varepsilon}{\varepsilon}
=\frac{4-\alpha}{4}\frac{V_\alpha(T_\varepsilon)}{\varepsilon^2}
\longrightarrow\frac{4-\alpha}{4}I_\alpha.
\]
Subtracting this limit from (3) yields
\[
J_\alpha-\frac{4-\alpha}{4}I_\alpha
=\frac{16-4\alpha-2^{4-\alpha}}
 {2(1-\alpha)(2-\alpha)(3-\alpha)}>0.
\tag{6}
\]
To prove the strict sign, convexity of \(\alpha\mapsto2^{4-\alpha}\) on [0,1] gives
\[
2^{4-\alpha}\le16-8\alpha<16-4\alpha\qquad(0<\alpha<1).
\]
For all sufficiently small \(\varepsilon>0\), therefore,
\[
v_{T_\varepsilon}(p_\varepsilon)>A_\varepsilon.
\]
Uniform dilation to area one multiplies both sides by the same positive factor, preserving the inequality. Formula (2) shows that a small cut at this very obtuse apex, followed by area normalization, strictly **decreases** \(V_\alpha\).

## 4. Consequence and exact gap

A boundary triangle of a larger allowed-normal class can have a favorable or unfavorable new-side direction. Equal side-average potentials do not provide a universal sign at a collapsing facet. Therefore the simple argument “every boundary polygon can be improved by turning on its missing normal” is false in general.

This does **not** prove that a whole normal class lacks an interior critical point, that the obtuse triangle is a global maximizer in that class, or that there are multiple critical points. Establishing those stronger statements would need additional global control. The sign analysis leaves the classification unresolved but pinpoints an actual obstruction, rather than merely asserting that compactness is difficult.

The thin-triangle calculation is deliberately restricted to \(0<\alpha<1\), where its one-dimensional limiting kernels are integrable. No unproved extension to \(1\le\alpha<2\) is claimed.
