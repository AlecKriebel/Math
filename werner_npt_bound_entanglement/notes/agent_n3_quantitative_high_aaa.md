# An explicit quantitative high-AAA exclusion

## Status

This note makes the qualitative high-AAA neighborhood from
`agent_n3_triple_skew_reduction.md` completely explicit.  It proves
the following exact theorem.

### Theorem

For every pair of qutrit three-copy two-planes,
\[
 {\cal C}(Q_{(3)})>\frac8{27}-10^{-120}
 \quad\Longrightarrow\quad
 \boxed{
 {\cal C}(Q_{(2)}+Q_{(3)})<\frac49 .
 }                                                        \tag{1}
\]

The constant \(10^{-120}\) is intentionally crude.  Its value is not
the point: (1) is the first explicit uniform neighborhood of the
maximal triple-skew orbit on which the coupled feature inequality is
proved without assuming common-factor form.

The proof uses only the exact deficit identities, equality spectrum,
and feature formulas already established in
`agent_n3_triple_skew_reduction.md`.  All numerical comparisons are
audited with exact integer arithmetic by
`verification/verify_n3_quantitative_high_aaa.py`.

## 1. From logical deficit to a stable Hodge pair

Put
\[
 \varepsilon=\frac8{27}-{\cal C}(Q_{(3)}),\qquad
 \varepsilon_0=10^{-120},
\]
and assume \(0\leq\varepsilon<\varepsilon_0\).  Choose the coherent
unit triple-skew coefficient \(t\) attaining the leading Takagi value,
and write
\[
 D=D_t,\qquad
 M=U^{\mathsf T}DV .
\]
The exact logical deficit identity (S5) gives
\[
\begin{aligned}
 h&:=\frac16-\|D\|_{\rm op}^2<\varepsilon_0,\\
 d&:=\|D\|_{\rm op}^2-|\det M|<\varepsilon_0.
\end{aligned}                                             \tag{2}
\]
Choose a unit top right singular vector \(x\) of \(D\).  Since
\(D_tt=0\), one has \(x\perp t\).

Use the four-party purification, encoded Pauli reductions, and
notation of the stable-rank proof:
\[
 |\Psi\rangle
 =\frac{|0\rangle_K|t\rangle+|1\rangle_K|x\rangle}{\sqrt2},
\quad
 p_i=\|X_{0,i}\|_2^2,
\quad
 h_{a,i}=\|X_{a,i}\|_2^2.
\]
Set
\[
 a_i=p_i-\frac13,\quad
 H_i=\sum_{a=1}^3h_{a,i},\quad
 P_1=\sum_ip_i,\quad
 {\mathsf G}=\sum_iH_i,\quad
 R=\frac29+\frac23P_1.
\]
Every \(a_i\geq0\), \(R\leq20/9\), and the exact stable deficit says
\[
 {\mathsf G}=P_1+\frac13-8h
 =\frac43+\sum_i a_i-8h.                                 \tag{3}
\]

For a Pauli permutation \(\pi\), multiply the nonnegative frame-gap
decomposition (S2) by \(s_\pi\), and then sum over all six
permutations.  Since \(s_\pi\leq R\), each site-axis pair occurs
twice, and \(z_i^2=2h_{\pi(i),i}\), one obtains the two estimates
\[
\boxed{
\begin{aligned}
 \sum_iH_i\,g_i&\leq8Rh,\\
 \sum_{i,a}h_{a,i}\,\ell_{a,i}&\leq8Rh,
\end{aligned}}                                           \tag{4}
\]
where
\[
 g_i=R-\frac23(1+p_i)
 =\frac23\sum_{j\ne i}a_j                                \tag{5}
\]
and \(\ell_{a,i}\) is the nonnegative local gap (S4).

## 2. Quantitative concentration on one physical site

Call a site low-purity when \(p_i\leq3/8\).  In the local eigenframe
used for (S4), let \(q\) be the middle diagonal weight.  The purity
floor
\[
 p_i\geq q^2+\frac{(1-q)^2}{2}
\]
implies \(1/6\leq q\leq1/2\) at a low-purity site.  Hence
\(\ell_{a,i}\geq q^2\geq1/36\) whenever \(h_{a,i}>0\).
The second inequality in (4) therefore gives
\[
 \sum_{i:\,p_i\leq3/8}H_i
 \leq288Rh\leq640h.                                      \tag{6}
\]

There is exactly one site with \(p_i>3/8\).  Indeed, if there were
none, (6) would give \({\mathsf G}\leq640h\), contrary to (3).
If there were at least two, then every high-purity site \(i\) would
have \(g_i\geq1/36\).  The first inequality in (4) would bound each
of their \(H_i\)'s by \(288Rh\leq640h\), while (6) controls the
remaining sites.  Thus \({\mathsf G}\leq1920h\), again contrary to
(3).  Here it is more than enough that \(h<10^{-120}\).

Label the unique high-purity site \(C\), and the other sites \(A,B\).
Equations (3), (5), and (6) give
\[
\begin{aligned}
 H_A+H_B&\leq640h,\\
 H_C&\geq\frac43-648h>1,\\
 a_A+a_B&\leq\frac{80}{3}h.                              \tag{7}
\end{aligned}
\]
For any Pauli axis \(a\), choose a permutation assigning it to \(C\).
Since every frame deficit is at most \(32h\),
\[
 h_{a,C}
 \geq\frac12(R-32h)-(H_A+H_B)
 \geq\frac49-656h>\frac1{10}.                            \tag{8}
\]
Combining (4) and (8), every local gap on \(C\) obeys
\[
 \ell_{a,C}<178h.                                        \tag{9}
\]

Formula (S4) now supplies the missing quantitative equality
conditions.  Its second term gives
\[
 q_{a,C}^2\leq\ell_{a,C}<178h,
\]
while its first term gives
\[
 0\leq
 p_C-q_{a,C}^2-\frac{(1-q_{a,C})^2}{2}
 \leq\frac32\ell_{a,C}.
\]
Using \(\sqrt{178}<14\), we obtain
\[
 \boxed{
 \frac12-14\sqrt h
 <p_C<
 \frac12+534h.
 }                                                        \tag{10}
\]

## 3. An explicit distance to the equality orbit

The purity of the \(KC\) reduction is
\[
 \operatorname{Tr}(\rho_{KC}^{\Psi})^2
 =\frac12(p_C+H_C).
\]
Using (3), (6), (7), and (10),
\[
 \operatorname{Tr}(\rho_{KC}^{\Psi})^2
 >1-14\sqrt h-324h
 >1-15\sqrt h.                                           \tag{11}
\]
The largest eigenvalue of a density matrix is at least its purity.
Schmidt decomposition across \(KC:AB\) therefore produces unit
vectors \(\phi_{KC},\chi_{AB}\) with
\[
 \left\|
 \Psi-\phi_{KC}\otimes\chi_{AB}
 \right\|
 <6h^{1/4}.                                              \tag{12}
\]
Indeed the squared distance is at most \(30\sqrt h\), and
\(\sqrt{30}<6\).

The \(K\)-marginal of \(\Psi\) is exactly \(I_2/2\).  Contractivity of
trace distance in (12) shows that the two Schmidt weights of
\(\phi_{KC}\) differ from \(1/2\) by at most \(6h^{1/4}\).
There is consequently a maximally entangled state
\(\beta_{KC}\), on a two-dimensional subspace of \(C\), such that
\[
 \|\phi_{KC}-\beta_{KC}\|<12h^{1/4}.                     \tag{13}
\]

Similarly, (7) gives
\[
 \|\rho_A^\Psi-I_3/3\|_1<9\sqrt h.
\]
Together with (12), this implies
\[
 \|\rho_A^\chi-I_3/3\|_1
 <12h^{1/4}+9\sqrt h<21h^{1/4}.
\]
The elementary Hellinger/total-variation inequality for the Schmidt
weights of \(\chi\) then gives a maximally entangled qutrit state
\(\Phi_{AB}\) such that
\[
 \|\chi_{AB}-\Phi_{AB}\|<5h^{1/8}.                       \tag{14}
\]
Explicitly, for Schmidt weights \(\lambda_j\),
\[
 1-\sum_j\sqrt{\lambda_j/3}
 =\frac12\sum_j
 \left(\sqrt{\lambda_j}-\frac1{\sqrt3}\right)^2
 \leq\frac12\sum_j\left|\lambda_j-\frac13\right|.
\]

Combining (12)--(14),
\[
 \boxed{
 \|\Psi-\beta_{KC}\otimes\Phi_{AB}\|
 <23h^{1/8}.
 }                                                        \tag{15}
\]
Use the fixed computational basis on \(K\) to write
\[
 \beta_{KC}
 =\frac{|0\rangle|c_0\rangle+|1\rangle|c_1\rangle}{\sqrt2}
\]
for orthonormal \(c_0,c_1\in\mathbb C^3\).  No logical rotation is
needed: a unitary on the maximally entangled \(K\)-half can always be
transferred to its \(C\)-half.  Comparing the two \(K\)-columns in
(15) yields, in particular,
\[
 \|t-\Phi_{AB}\otimes c_0\|
 <46h^{1/8}.                                              \tag{16}
\]

The coefficient-to-Hodge map \(t\mapsto D_t\) is a Hilbert--Schmidt
isometry.  Hence, with
\[
 D_0=D_{\Phi_{AB}\otimes c_0},
\]
\[
 \|D-D_0\|_{\rm op}<46h^{1/8}.                           \tag{17}
\]

## 4. The two compression planes are explicitly close

Put \(r=1/\sqrt6\).  The exact singular spectrum of \(D_0\) is
\[
 r,r,\quad
 \underbrace{r/2,\ldots,r/2}_{16\ {\rm times}},
 \quad 0,\ldots,0.                                       \tag{18}
\]
Let \(P_R,P_L\) be its two-dimensional top right and left singular
projections.  From (2),
\[
 |\det M|>r^2-2\varepsilon_0.
\]
Both singular values of \(M\) are at most \(r\), so its smaller
singular value is greater than
\[
 r-\frac{2\varepsilon_0}{r}.                             \tag{19}
\]

For a unit vector \(v\) in the right compression plane, (17)--(19)
give
\[
 \|D_0v\|
 >r-\kappa,\qquad
 \kappa=\frac{2\varepsilon_0}{r}+46\varepsilon_0^{1/8}.
\]
Using (18),
\[
 \|(I-P_R)v\|^2
 <\frac{8\kappa}{3r}.
\]
The identical argument for \(D^\dagger\) treats the left plane.
Since \(r>2/5\) and \(\varepsilon_0<1\),
\[
 \boxed{
 \|(I-P_R)P_V\|_{\rm op}^2,\qquad
 \|(I-P_L)P_{\bar U}\|_{\rm op}^2
 <340\varepsilon_0^{1/8}.
 }                                                        \tag{20}
\]
The harmless conjugation on \(U\) is the one already present in the
Hodge compression convention.

## 5. The two-skew concurrence is below the available margin

Let
\[
 \ell=340\varepsilon_0^{1/8}.
\]
Principal-angle alignment supplies logical bases in which the two
compression isometries differ from their equality-orbit values by at
most \(\sqrt{2\ell}\) in operator norm.  Their tensor-product
isometry \(W\) therefore obeys
\[
 \|W-W_0\|_{\rm op}\leq2\sqrt{2\ell}.
\]
The physical two-skew feature operator has norm \(4/3\).  Hence
\[
 q:=\|Q_{(2)}-Q_{(2),0}\|_{\rm op}
 <\frac{16\sqrt2}{3}\sqrt\ell
 <210\varepsilon_0^{1/16}.                               \tag{21}
\]

At the equality orbit,
\[
 \operatorname{spec}Q_{(2),0}
 =\left(\frac49,\frac4{27},\frac4{27},\frac4{27}\right),
\qquad
 {\cal C}(Q_{(2),0})=0.                                  \tag{22}
\]
For completeness, the following local concurrence estimate is
elementary.  If \(Q\succeq0\), \(Q_0\) is the matrix in (22), and
\(\|Q-Q_0\|_{\rm op}=q<2/27\), then
\[
 \boxed{
 {\cal C}(Q)\leq18\sqrt3\,q.
 }                                                        \tag{23}
\]
To prove it, realize the four Takagi values as the singular values of
\[
 R_Q=Q^{1/2}J\overline Q^{\,1/2},
 \qquad J=\epsilon\otimes\epsilon.
\]
The Sylvester integral for the square root gives
\[
 \|Q^{1/2}-Q_0^{1/2}\|_{\rm op}
 \leq\frac{3\sqrt3}{2}q,
\]
because \(Q_0\succeq(4/27)I\) and
\(Q\succeq(2/27)I\).  Also
\(\|Q^{1/2}\|_{\rm op}+\|Q_0^{1/2}\|_{\rm op}<2\).
Thus
\[
 \|R_Q-R_{Q_0}\|_{\rm op}\leq3\sqrt3\,q.
\]
For clarity, the square-root estimate is also self-contained.  If
\(A=Q^{1/2}\), \(B=Q_0^{1/2}\), and \(X=A-B\), then
\[
 AX+XB=Q-Q_0,
\]
and
\[
 X=\int_0^\infty e^{-tA}(Q-Q_0)e^{-tB}\,dt.
\]
Taking norms gives the displayed bound.

Finally, if \(t_1(R)\) is the largest singular value, homogeneous
concurrence is
\[
 {\cal C}(Q)=\max\{0,2t_1(R_Q)-\|R_Q\|_1\}.
\]
The operator norm variational formula and the trace-norm triangle
inequality give
\[
\begin{aligned}
 {\cal C}(Q)
 &\leq
 2\|R_Q-R_{Q_0}\|_{\rm op}
 +\|R_Q-R_{Q_0}\|_1\\
 &\leq6\|R_Q-R_{Q_0}\|_{\rm op}
 \leq18\sqrt3\,q,
\end{aligned}
\]
because \(2t_1(R_{Q_0})-\|R_{Q_0}\|_1=0\).  This proves
(23).

Now
\[
 \varepsilon_0^{1/16}=10^{-7.5}<10^{-7}.
\]
Equations (21)--(23), using \(\sqrt3<2\), give
\[
 {\cal C}(Q_{(2)})
 <36\cdot210\cdot10^{-7}
 <\frac4{27}.                                            \tag{24}
\]
Finally, homogeneous concurrence is subadditive, and the sharp
triple-skew theorem gives
\({\cal C}(Q_{(3)})\leq8/27\).  Therefore
\[
\begin{aligned}
 {\cal C}(Q_{(2)}+Q_{(3)})
 &\leq{\cal C}(Q_{(2)})+{\cal C}(Q_{(3)})\\
 &<\frac4{27}+\frac8{27}
 =\frac49.
\end{aligned}
\]
This proves (1). \(\square\)

## 6. Relation to the balanced Lorentz reduction

Theorem (1) is stated before nonunitary logical filtering, on the
compact product of isometric code-plane frames.  It therefore gives
an explicit high-AAA region for the feature/concurrence route.

It does not by itself give a uniform neighborhood in the balanced
Lorentz coordinates.  The filters that make both logical marginals
scalar can have arbitrarily large condition number near the boundary,
and (20) is not invariant under such filters.  A transfer to the
fixed Minkowski scalar
\[
 T_{00}-T_{11}-T_{22}-T_{33}
\]
requires either a condition-number bound or a directly
filter-invariant version of the deficit.  This is the precise
remaining bridge between the quantitative high-AAA theorem and the
balanced Lorentz frontier.
