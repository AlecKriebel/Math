# Fusing the triple-Hodge face deficit with the explicit high-AAA theorem

## Status

This note closes the filter-invariance gap between the common
triple-Hodge face tradeoff and the proved explicit high-AAA
neighborhood.  It gives a rigorous, explicit improvement of the
hypothetical negative-depth ceiling:
\[
 \boxed{\qquad
 0<\delta<
 \frac{648+2187\varepsilon_0}
      {5112+21141\varepsilon_0}
 <\frac9{71},
 \qquad \varepsilon_0=10^{-120}.
 \qquad}                                                   \tag{1}
\]
Equivalently, the improvement below \(9/71\) is exactly
\[
 \boxed{\qquad
 \frac9{71}-
 \frac{648+2187\varepsilon_0}
      {5112+21141\varepsilon_0}
 =
 \frac{34992\varepsilon_0}
 {71(5112+21141\varepsilon_0)}>0.
 \qquad}                                                   \tag{2}
\]

The numerical size is intentionally tiny because the available
high-AAA radius \(10^{-120}\) is deliberately crude.  The structural
point is stronger: no condition-number estimate for the logical
filters is needed.  The normalized filtered triple-Hodge expectation
is itself a lower bound on the homogeneous concurrence of the
*unfiltered* pair of code planes, because determinant-one filters
leave that concurrence invariant.

This still does not prove unrestricted three-copy positivity.  It
turns the previously qualitative incompatibility between the formal
\(9/71\) endpoint and the classified stable-rank orbit into an exact
uniform exclusion neighborhood.

The dependency-free checker is
`verification/verify_n3_high_aaa_face_fusion.py`.

## 1. A filter-invariant deficit bridge

Let \(C\) have rank two, let
\[
 p=s_1(C)s_2(C)>0,
\]
and let \(U,V\) be its two orthonormal singular-plane frames.  Put
\[
 e={\cal J}_3(C)+\frac p3\geq0,                          \tag{3}
\]
where
\[
 {\cal J}_3(C)
 =\frac18\left(
 \|C\|_2^2-\sum_i\|\operatorname{Tr}_iC\|_2^2
 +\sum_{i<j}\|\operatorname{Tr}_{ij}C\|_2^2
 -|\operatorname{Tr}C|^2\right).
 \tag{4}
\]
The nonnegativity in (3) is the proved triple-skew exterior
tradeoff.

Factor \(C/\sqrt p=(UA)(VB)^\dagger\) with
\(A,B\in SL(2,\mathbb C)\), as in the proof of that tradeoff.
For the unfiltered logical triple-skew feature
\(Q_{(3)}(U,V)\), the filtered-swap formula gives
\[
\begin{aligned}
 {\cal C}(Q_{(3)}(U,V))
 &={\cal C}\!\left(
 (A\otimes B)Q_{(3)}(U,V)(A\otimes B)^\dagger
 \right)\\
 &\geq
 -\operatorname{Tr}\!\left[
 F_{\rm L}(A\otimes B)Q_{(3)}(U,V)
 (A\otimes B)^\dagger\right]\\
 &=-\frac89\,\frac{{\cal J}_3(C)}p\\
 &=\boxed{\frac8{27}-\frac{8e}{9p}.}                    \tag{5}
\end{aligned}
\]
The first equality is exact determinant-one covariance of
homogeneous concurrence.  Thus even arbitrarily ill-conditioned
filters cause no loss in (5).

The explicit high-AAA theorem says
\[
 {\cal C}(Q_{(3)})>\frac8{27}-\varepsilon_0
 \quad\Longrightarrow\quad
 {\cal C}(Q_{(2)}+Q_{(3)})<\frac49.                     \tag{6}
\]
Combining (5)--(6) gives the dichotomy
\[
\boxed{
\begin{aligned}
 e&<\frac98\varepsilon_0p
 &&\Longrightarrow\quad\text{the sharp shifted degree-two
 inequality holds strictly on the two planes},\\
 \text{or}\qquad
 e&\geq\frac98\varepsilon_0p .
\end{aligned}}                                           \tag{7}
\]

## 2. Face coordinates

Normalize a hypothetical negative direction by
\[
 \langle S_V\rangle=1,\qquad
 \langle H_V\rangle=-\delta,\qquad \delta>0,
\]
and put
\[
 u=(1-5\delta)L>0.
\]
The exact face-simplex identities are
\[
\begin{aligned}
 c&=\frac{1+\delta}{3},\\
 R&=\frac32(1-5\delta-u),\\
 S&=\frac34u.
\end{aligned}                                             \tag{8}
\]
Let \(a\) be the total one-traceless mass and
\(\Delta=(s_1-s_2)^2\).  The triple-Hodge face tradeoff is
\[
 \boxed{\qquad
 2556\delta+459u+405a+144\Delta\leq324.
 \qquad}                                                   \tag{9}
\]
Its exact slack is
\[
 \boxed{\qquad
 864e=
 324-2556\delta-459u-405a-144\Delta .
 \qquad}                                                   \tag{10}
\]

The norm and exterior mass are also exact:
\[
\begin{aligned}
 N=\|C\|_2^2
 &=4\delta+\frac34u+\frac94a,\\
 p=\frac{N-\Delta}{2}
 &=2\delta+\frac38u+\frac98a-\frac12\Delta.
\end{aligned}                                             \tag{11}
\]

## 3. The high-AAA branch

Suppose the first branch of (7) holds.  By (6), the coupled feature
bound is strict.  Its lossless exterior reformulation gives
\[
 c<\frac49(N+p).
\]
Using (8) and (11), this is exactly
\[
 \boxed{\qquad
 42\delta+9u+27a>6+4\Delta.
 \qquad}                                                   \tag{12}
\]

Multiply (12) by \(15\).  Equivalently,
\[
 405a>90+60\Delta-630\delta-135u.
\]
Substitute this strict lower bound for \(405a\) into (9).  This
eliminates \(a\) and leaves
\[
 1926\delta+324u+204\Delta<234.
\]
Consequently
\[
 \boxed{\qquad
 \delta<\frac{234}{1926}=\frac{13}{107}.
 \qquad}                                                   \tag{13}
\]

## 4. The complementary branch

Now suppose
\[
 e\geq\frac98\varepsilon_0p.                             \tag{14}
\]
Equation (10) gives
\[
 K:=324-2556\delta-459u-405a-144\Delta
 =864e\geq972\varepsilon_0p.                            \tag{15}
\]

The nonnegativity \(K\geq0\), substituted into the second line of
(11), gives the useful lower bound
\[
\begin{aligned}
 p
 &\geq
 \frac{87\delta-9}{8}
 +\frac{63}{32}u+\frac{81}{32}a\\
 &\geq\frac{87\delta-9}{8}.                             \tag{16}
\end{aligned}
\]
For completeness, (16) is obtained by replacing
\[
 \Delta\leq
 \frac{324-2556\delta-459u-405a}{144}
\]
in (11).

If \(\delta\leq13/107\), the final bound (1) already holds.  Otherwise
\(\delta>13/107>3/29\), so the last member of (16) is positive.
Dropping the positive \(u,a,\Delta\) terms from the left side of
(15), and then using (16), yields
\[
 324-2556\delta
 >K
 \geq\frac{243}{2}\varepsilon_0(87\delta-9).             \tag{17}
\]
The first inequality is strict because \(u>0\).
Solving (17) gives
\[
 \delta<
 \frac{648+2187\varepsilon_0}
      {5112+21141\varepsilon_0}.                         \tag{18}
\]

Finally,
\[
 \frac{648+2187\varepsilon_0}
      {5112+21141\varepsilon_0}
 >\frac{13}{107}
\]
for \(\varepsilon_0=10^{-120}\), while direct cross multiplication
gives (2).  Therefore the two branches (13) and (18) combine to prove
(1).

## 5. Remaining quantitative target

The proof used the existing high-AAA radius only through (6).  If an
improved exact radius \(\varepsilon_*\) is proved, the same argument
immediately replaces \(\varepsilon_0\) by \(\varepsilon_*\) in
(1)--(2).  A substantial depth improvement therefore reduces to
either:

1. enlarging the stable-rank neighborhood on which the coupled
   Takagi feature is controlled; or
2. proving a direct lower bound on \(e/p\) away from the
   common-factor equality orbit.

The second option is the invariant stability inequality suggested by
the exact deficit decomposition of the sharp triple-skew theorem.
