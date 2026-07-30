# An exponent-optimized quantitative high-AAA exclusion

## Status

This note strengthens the established quantitative high-\(AAA\)
theorem by ninety-two orders of magnitude:
\[
 \boxed{\qquad
 {\cal C}(Q_{(3)})>\frac8{27}-10^{-28}
 \quad\Longrightarrow\quad
 {\cal C}(Q_{(2)}+Q_{(3)})<\frac49 .
 \qquad}                                                   \tag{1}
\]
All constants are deliberately conservative and are checked using
exact rational arithmetic in
`verification/verify_n3_quantitative_high_aaa_optimized.py`.

The improvement comes from removing two unnecessary square-root
losses in the previous proof:

1. closeness of a qutrit marginal to \(I_3/3\) controls the
   Schmidt-aligned vector distance *linearly*, not through a
   Hellinger square root;
2. the top singular planes of two nearby matrices are linearly close
   in the perturbation, by applying the singular-vector equation
   across the fixed spectral gap.  A one-sided energy estimate loses
   an extra square root.

This is still a local theorem around the maximal triple-skew orbit,
not the unrestricted three-copy theorem.

## 1. Exact deficit data

Let
\[
 \varepsilon=\frac8{27}-{\cal C}(Q_{(3)}),\qquad
 \varepsilon_* =10^{-28},
\]
and assume \(0\leq\varepsilon<\varepsilon_*\).  Use the notation of
the sharp stable-rank proof and the earlier quantitative theorem:
\[
\begin{aligned}
 h&=\frac16-\|D\|_{\rm op}^2,\\
 d&=\|D\|_{\rm op}^2-|\det(U^{\mathsf T}DV)|,\\
 p_i&=\|X_{0,i}\|_2^2,\qquad
 a_i=p_i-\frac13,\\
 H_i&=\sum_{a=1}^3\|X_{a,i}\|_2^2,\qquad
 {\mathsf G}=\sum_iH_i,\\
 R&=\frac29+\frac23\sum_i p_i .
\end{aligned}                                             \tag{2}
\]
The exact Takagi deficit decomposition gives
\[
 0\leq h,d<\varepsilon.                                  \tag{3}
\]
The stable frame-gap decomposition gives
\[
\begin{aligned}
 {\mathsf G}
 &=\frac43+\sum_i a_i-8h,\\
 \sum_iH_i g_i&\leq8Rh,\\
 \sum_{i,a}\|X_{a,i}\|_2^2\ell_{a,i}&\leq8Rh,
\end{aligned}                                             \tag{4}
\]
where
\[
 g_i=\frac23\sum_{j\ne i}a_j,\qquad
 \frac89\leq R\leq\frac{20}{9}.                          \tag{5}
\]

The alternatives in the concentration argument are already excluded
when \(h<1/1446\), and all its subsequent estimates hold in the much
smaller range (3).  It gives a unique high-purity site \(C\), with
the other sites denoted \(A,B\), and
\[
\begin{aligned}
 H_A+H_B&\leq640h,\\
 a_A+a_B&\leq\frac{80}{3}h,\\
 h_{a,C}:=\|X_{a,C}\|_2^2
 &\geq\frac49-656h>\frac25
 \quad(a=1,2,3).
\end{aligned}                                             \tag{6}
\]
The last strict inequality follows already for
\(h<\varepsilon_*\).

Since \(R\leq20/9\), (4) and (6) improve the local gap estimate to
\[
 \ell_{a,C}
 \leq\frac{(160/9)h}{2/5}
 =\frac{400}{9}h<45h.                                   \tag{7}
\]
Let \(q\) be the middle diagonal weight in the local sign-frame
lemma.  Its exact local gap formula implies
\[
 q^2\leq\ell_{a,C},\qquad
 0\leq
 p_C-q^2-\frac{(1-q)^2}{2}
 \leq\frac32\ell_{a,C}.
\]
Consequently
\[
 \boxed{\qquad
 \frac12-7\sqrt h<p_C<\frac12+135h .
 \qquad}                                                   \tag{8}
\]

## 2. Linear Schmidt alignment

Because
\[
 {\mathsf G}
 =1+p_C+a_A+a_B-8h,
\]
equations (6) and (8) give
\[
\begin{aligned}
 \operatorname{Tr}(\rho_{KC}^{\Psi})^2
 &=\frac12(p_C+H_C)\\
 &>1-7\sqrt h-324h\\
 &>1-8\sqrt h.                                          \tag{9}
\end{aligned}
\]
The largest Schmidt weight across \(KC:AB\) is at least this purity.
Hence there are unit vectors \(\phi_{KC},\chi_{AB}\) such that
\[
 \|\Psi-\phi_{KC}\otimes\chi_{AB}\|<4h^{1/4}.            \tag{10}
\]

The \(K\)-marginal of \(\Psi\) is \(I_2/2\).  Trace-norm
contractivity and (10) show that the Schmidt weights of \(\phi\)
are within \(8h^{1/4}\) in \(\ell^1\) of \((1/2,1/2)\).  Aligning
the Schmidt bases with a Bell state \(\beta_{KC}\) gives
\[
 \|\phi_{KC}-\beta_{KC}\|<8h^{1/4}.                      \tag{11}
\]
For clarity, if \(\lambda_j\) and \(1/k\) are two probability
vectors, then
\[
\begin{aligned}
 \sum_{j=1}^k\left(\sqrt{\lambda_j}-\frac1{\sqrt k}\right)^2
 &=
 \sum_j
 \frac{(\lambda_j-1/k)^2}
      {(\sqrt{\lambda_j}+1/\sqrt k)^2}\\
 &\leq
 k\left(\sum_j|\lambda_j-1/k|\right)^2.                 \tag{12}
\end{aligned}
\]
For \(k=2\), the two deviations are opposite and (11) follows
with the displayed constant.

Moreover,
\[
 \|\rho_A^\Psi-I_3/3\|_1<9\sqrt h.
\]
Equations (10) and trace-norm contractivity therefore give
\[
 \|\rho_A^\chi-I_3/3\|_1<17h^{1/4}.                     \tag{13}
\]
Apply (12) with \(k=3\) and align Schmidt bases.  Since
\(\sqrt3<2\), there is a maximally entangled qutrit state
\(\Phi_{AB}\) satisfying
\[
 \|\chi_{AB}-\Phi_{AB}\|<34h^{1/4}.                     \tag{14}
\]
Combining (10), (11), and (14),
\[
 \boxed{\qquad
 \|\Psi-\beta_{KC}\otimes\Phi_{AB}\|<46h^{1/4}.
 \qquad}                                                   \tag{15}
\]

Write the Bell pair in the fixed logical basis and compare the two
logical columns.  Since \(\sqrt2<3/2\), (15) implies
\[
 \|t-\Phi_{AB}\otimes c_0\|<69h^{1/4}<70h^{1/4}.         \tag{16}
\]
The coefficient-to-Hodge map is a Hilbert--Schmidt isometry.  If
\(D_0=D_{\Phi_{AB}\otimes c_0}\), then
\[
 \boxed{\qquad
 \eta:=\|D-D_0\|_{\rm op}<70\varepsilon^{1/4}.
 \qquad}                                                   \tag{17}
\]

## 3. Linear control of the two top singular planes

Put \(r=1/\sqrt6\).  The singular values of \(D_0\) are
\[
 r,r,\quad r/2\ \text{(sixteen times)},\quad0\ \text{otherwise}.
                                                               \tag{18}
\]
Let \(P_R\) be its top two-dimensional right singular projection,
and let \(\widehat P_R\) be the top right singular projection of
\(D\).  Set
\[
 H_0=D_0^\dagger D_0,\qquad H=D^\dagger D.
\]
Since \(\|D\|_{\rm op},\|D_0\|_{\rm op}\leq r\) and \(2r<1\),
\[
 \|H-H_0\|_{\rm op}<\eta.                                \tag{19}
\]
The top/third spectral gap of \(H_0\) is
\[
 r^2-\frac{r^2}{4}=\frac18.
\]
For either of the two top eigenvectors \(y\) of \(H\), apply
\(I-P_R\) to its eigenvector equation.  The relevant inverse on
\(\operatorname{ran}(I-P_R)\) has norm at most \(16\), because
\(\eta<1/16\).  Thus
\[
 \|(I-P_R)y\|<16\eta.
\]
Taking the Hilbert--Schmidt norm over the two top eigenvectors and
using \(\sqrt2<3/2\) gives
\[
 \boxed{\qquad
 \|(I-P_R)\widehat P_R\|_{\rm op}<24\eta.
 \qquad}                                                   \tag{20}
\]
This is the linear spectral-projection estimate that replaces the
previous square-root energy bound.

It remains to compare the physical compression plane \(P_V\) with
\(\widehat P_R\).  From (3),
\[
 |\det(U^{\mathsf T}DV)|>r^2-2\varepsilon.
\]
Both singular values of the compression are at most \(r\), so its
smaller singular value is greater than \(r-2\varepsilon/r\).
Also the third singular value of \(D\) is at most
\(r/2+\eta<3r/4\).  Therefore, for every unit
\(v\in\operatorname{ran}P_V\),
\[
\begin{aligned}
 r^2-4\varepsilon
 &<\|Dv\|^2\\
 &\leq
 r^2-\frac{7r^2}{16}
 \|(I-\widehat P_R)v\|^2.
\end{aligned}
\]
Since \(r^2=1/6\),
\[
 \|(I-\widehat P_R)P_V\|_{\rm op}^2
 <\frac{384}{7}\varepsilon<55\varepsilon.               \tag{21}
\]
Equations (17), (20), and (21) now give
\[
\begin{aligned}
 \|(I-P_R)P_V\|_{\rm op}
 &<24\eta+8\sqrt\varepsilon\\
 &<1688\varepsilon^{1/4}.                               \tag{22}
\end{aligned}
\]
The identical argument for \(D^\dagger\) treats the left compression
plane (with the harmless conjugation dictated by the Hodge
convention).

## 4. Completion of the explicit neighborhood

Let
\[
 s=1688\varepsilon^{1/4}.
\]
Principal-angle alignment supplies logical bases in which each
compression isometry differs from its equality-orbit isometry by at
most \(\sqrt2\,s\).  The tensor-product compression isometry
therefore differs by at most \(2\sqrt2\,s\).

The physical two-skew feature operator has norm \(4/3\), so
\[
\begin{aligned}
 q
 &:=
 \|Q_{(2)}-Q_{(2),0}\|_{\rm op}\\
 &<\frac{16\sqrt2}{3}s
 <8s
 <13504\varepsilon^{1/4}.                               \tag{23}
\end{aligned}
\]
For \(\varepsilon<10^{-28}\), this gives
\[
 q<\frac{13504}{10^7}<\frac2{27}.                       \tag{24}
\]

The elementary local concurrence estimate from the previous theorem
therefore applies:
\[
 {\cal C}(Q_{(2)})\leq18\sqrt3\,q<36q
 <\frac{486144}{10^7}<\frac4{27}.                       \tag{25}
\]
Finally, concurrence is subadditive and the sharp triple-skew theorem
gives \({\cal C}(Q_{(3)})\leq8/27\).  Hence
\[
 {\cal C}(Q_{(2)}+Q_{(3)})
 \leq{\cal C}(Q_{(2)})+{\cal C}(Q_{(3)})
 <\frac4{27}+\frac8{27}
 =\frac49.
\]
This proves (1). \(\square\)

## 5. Consequence for the negative-depth face

The filter-invariant bridge in
`agent_n3_high_aaa_face_fusion.md` may therefore use
\(\varepsilon_*=10^{-28}\) in place of \(10^{-120}\).  Every
hypothetical negative direction obeys
\[
 \boxed{\qquad
 \delta<
 \frac{648+2187\cdot10^{-28}}
      {5112+21141\cdot10^{-28}}
 <\frac9{71}.
 \qquad}                                                   \tag{26}
\]
The exact improvement below \(9/71\) is
\[
 \frac{34992\cdot10^{-28}}
 {71(5112+21141\cdot10^{-28})}.                          \tag{27}
\]

The radius is now limited mainly by the deliberately simple local
Lipschitz estimate
\({\cal C}(Q_{(2)})\leq18\sqrt3\,q\), not by the geometry of the
stable-rank equality orbit.  A global theorem still requires a
tradeoff away from that orbit rather than further local constant
optimization.
