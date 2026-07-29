# An exact large-slack obstruction to the local stability chain

## Status

This note does **not** construct a negative rank-two coefficient
matrix.  It constructs an exact abstract critical-data model satisfying
all of the currently recorded scalar, one-site stationary, quantitative
isotropy, block-Gram, marginal-floor, and common-pencil-minor
inequalities, while its assigned endpoint value is negative.

The point is to identify a logical gap in the present proof strategy.
The local stability chain is decisive when the Haar brackets are small,
but its stated consequences cannot exclude the large-slack regime.  A
new inequality must couple the block Grams and the factor-pencil minors
as data of the **same** rank-two coefficient matrix.  Treating those
two exact consequences separately, even while realizing the latter by
a genuine two-dimensional qutrit code, is insufficient.

For every
\[
 0<\delta<\frac18
 \tag{1}
\]
the model below has
\[
 q=-\delta,\qquad
 g_1=g_2=g_3=\frac{1-8\delta}{9}>0.
 \tag{2}
\]
As \(\delta\downarrow0\), the Haar brackets tend to \(1/9\), the
one-site Hessian excess tends to \(5/48\), all six marginals remain
exactly balanced, and the two common-factor minor masses stay bounded
away from zero.  Thus the obstruction persists precisely in the
large-Haar-slack regime.

The dependency-free exact checker is
`verification/verify_n3_large_slack_critical_data_obstruction.py`.

## 1. Sector and marginal data

Put
\[
 g=\frac{1-8\delta}{9},\qquad
 w_0=w_1=0,\qquad
 w_2=\frac{2(1+\delta)}3,\qquad
 w_3=\frac{1-2\delta}{3}.
 \tag{3}
\]
All these numbers are nonnegative and
\[
 w_0+w_1+w_2+w_3=1.
 \tag{4}
\]
The endpoint and Haar identities hold exactly:
\[
\begin{aligned}
 -\frac18w_0+\frac14w_1-\frac12w_2+w_3
 &=-\delta,\\
 \sum_{i=1}^3g_i
 &=3g
 =\frac13-\frac34w_1-\frac83\delta.
\end{aligned}
 \tag{5}
\]
At the level of exact subsets, split \(w_2\) equally among the three
two-traceless sectors and assign \(w_3\) to the fully traceless
sector.  Then
\[
 g_i=-\frac12\left(\frac{w_2}{3}+\frac{w_2}{3}\right)+w_3
 =g.
 \tag{6}
\]
This choice also obeys two elementary rank-two restrictions that the
much simpler scalar/traceless toy distribution would violate:
\[
 w_0=0\leq\frac{2}{27},\qquad
 w_2<\frac34<\frac{24}{31}.
 \tag{7}
\]
The first is the rank-two trace bound and the second is the established
one-site-compression pair-sector bound.

Assign all six critical one-site densities the balanced value
\[
 \rho_i^L=\rho_i^R=\frac13I_3.
 \tag{8}
\]
For
\[
 m=\frac{\delta}{1+2\delta},
 \tag{9}
\]
one has \(m<1/3\), so every marginal-floor inequality
\[
 \rho_i^{L,R}\succeq mI_3
 \tag{10}
\]
holds.  The stationary marginal tent is zero because
\(\lambda_{\max}(\rho_i^{L,R})=1/3\), and the quantitative anisotropy
bound is also zero because the marginals are exactly \(I_3/3\).
The global refinement
\[
 \delta\leq\frac1{8+(16/5)S}
 \tag{11}
\]
reduces to the assumed \(\delta<1/8\), since \(S=0\).

## 2. Exact one-site stationary form

Let
\[
 {\cal L}(A)=A-\frac12\operatorname{Tr}(A)I_3,\qquad
 {\cal P}_0(A)=A-\frac13\operatorname{Tr}(A)I_3,
 \tag{12}
\]
and set
\[
 \gamma=\frac{2\delta}{3},\qquad
 t=\frac{15g}{16}.
 \tag{13}
\]
At every left and right site use the same abstract local form
\[
\boxed{
 h(A,B)=
 \gamma\langle A,{\cal L}(B)\rangle_{\rm HS}
+t\langle A,{\cal P}_0(B)\rangle_{\rm HS}.
 }
 \tag{14}
\]
It has the exact critical normalization
\[
 h(A,I)=q\,\operatorname{Tr}(A^\dagger\rho)
 =-\frac{\delta}{3}\overline{\operatorname{Tr}A},
 \qquad \rho=I_3/3.
 \tag{15}
\]
Moreover \(h(A,A)\geq0\) whenever \(\operatorname{rank}A\leq2\).
Indeed,
\[
 \langle A,{\cal L}(A)\rangle
 =\|A\|_2^2-\frac12|\operatorname{Tr}A|^2\geq0
 \tag{16}
\]
on rank at most two, while the second term in (12) is
\(t\|{\cal P}_0(A)\|_2^2\).

The critical Hessian is
\[
 G(A,B)=h(A,B)-q\operatorname{Tr}(A^\dagger B\rho)
 =h(A,B)+\frac{\delta}{3}\langle A,B\rangle.
 \tag{15}
\]
It vanishes on the scalar line and has the constant eigenvalue
\(\delta+t\) on the eight-dimensional traceless subspace.  Hence
\[
 G\succeq0,\qquad\ker G=\mathbb CI_3.
 \tag{16}
\]
Its trace gives precisely the established Haar trace-excess identity:
\[
\boxed{
 \operatorname{Tr}_{\rm HS}G+8q
 =8t=\frac{15}{2}g.
 }
 \tag{17}
\]

The quantitative-isotropy defect is not merely bounded; it is
explicit:
\[
 {\mathscr H}+\frac{2q}{3}{\cal L}
 =t{\cal P}_0.
 \tag{18}
\]
Consequently
\[
 \left\|{\mathscr H}+\frac{2q}{3}{\cal L}\right\|_{\rm op}
 =t
 \leq360\sqrt{15}\sqrt g.
 \tag{19}
\]

## 3. Exact block-Gram data

Invert the established local-form/block-Gram coefficient map.  In
matrix-unit indices its result is
\[
\boxed{
 \beta_{ar,bt}
 =
 \left(\gamma+\frac{2t}{3}\right)
 \delta_{ar}\delta_{bt}
 +\frac{2t}{15}\delta_{rt}\delta_{ab}.
 }
 \tag{20}
\]
Equivalently,
\[
 \beta=
 \left(\gamma+\frac{2t}{3}\right)
 |\operatorname{vec}I\rangle\langle\operatorname{vec}I|
 +\frac{2t}{15}I_9.
 \tag{21}
\]
Thus \(\beta\) is positive definite.  Substitution into
\[
 K_{ra,tb}
 =
 \delta_{rt}\sum_p\beta_{ap,bp}
 -\frac12\beta_{ar,bt}
 \tag{22}
\]
recovers (12) coefficient by coefficient.

The exact distance from the Haar-collapse block Gram is
\[
\boxed{
 \left\|
 \beta-\gamma
 |\operatorname{vec}I\rangle\langle\operatorname{vec}I|
 \right\|_F^2
 =\frac{352}{75}t^2.
 }
 \tag{23}
\]
It obeys the recorded quantitative estimate
\[
 \left\|\beta-\gamma
 |\operatorname{vec}I\rangle\langle\operatorname{vec}I|
 \right\|_F
 \leq4752\sqrt{15}\sqrt g.
 \tag{24}
\]
The essential feature is that the left side does not tend to zero as
\(\delta\downarrow0\): it tends to
\((5/48)\sqrt{352/75}\).  Therefore the small-block-defect
hypothesis needed to enter the slice-to-factor theorem is unavailable
in this regime.

## 4. Genuine common-origin factor-pencil data

The nonlinear minor constraints are not represented by arbitrary
unrelated nonnegative numbers.  Take the genuine qutrit code plane
with orthonormal frame
\[
\begin{aligned}
 u_0&=\frac1{\sqrt3}
 (|000\rangle+|111\rangle+|222\rangle),\\
 u_1&=\frac1{\sqrt3}
 (|012\rangle+|120\rangle+|201\rangle).
\end{aligned}
 \tag{25}
\]
Its one-site plane marginals are all
\[
 \sigma_i=\frac23I_3.
 \tag{26}
\]
Contract the first site by a Haar-unit vector \(z\).  Let \(a(z)\)
be the sum of squared \(2\times2\) minors across the second-site
flattening and \(b(z)\) the analogous sum across the third-site
flattening.  Direct exact Haar integration gives
\[
\boxed{
 {\mathbb E}a={\mathbb E}b=\frac5{36},\qquad
 {\mathbb E}(ab)=\frac{47}{2430}.
 }
 \tag{27}
\]
In particular,
\[
 \frac{{\mathbb E}(ab)}
 {{\mathbb E}a\,{\mathbb E}b}
 =\frac{376}{375}>\frac25,
 \tag{28}
\]
so the sharp common-origin correlation inequality holds strictly.
The marginal minor floors also hold:
\[
\begin{aligned}
 {\mathbb E}a,\ {\mathbb E}b
 &\geq\frac{m^8(1-m)^4}{79\,350},\\
 {\mathbb E}(ab)
 &\geq
 \frac{m^{16}(1-m)^8}{15\,741\,056\,250}.
\end{aligned}
 \tag{29}
\]
The same plane can be used for every left and right singular-plane
minor datum.

## 5. Consequence for the proof architecture

Equations (3)--(29) form an exact negative critical-data model for
every \(0<\delta<1/8\).  It satisfies:

1. nonnegative sector masses, the endpoint identity, and all three
   strict Haar brackets;
2. the marginal floor, stationary tent, anisotropy estimate, and
   stationary-value refinement;
3. the full local critical equations, rank-two-filter positivity,
   Hessian positivity, and trace-excess identity;
4. the quantitative local-isotropy and block-Gram bounds;
5. positive block-Gram principal compressions;
6. genuine, common-quadratic-origin factor-pencil minors from a
   balanced qutrit code, including their sharp correlation and
   determinant floors.

The model is deliberately not asserted to arise from one coefficient
matrix \(C\).  If it did, it would already be a negative three-copy
witness.  What it proves is the following exact limitation:

\[
\boxed{\begin{minipage}{0.88\linewidth}
No argument using only the currently recorded local stationary,
quantitative-isotropy, block-distance, marginal-floor, and separately
derived common-pencil-minor inequalities can force
\(\delta=0\).  A successful large-slack argument must impose a new
same-\(C\) compatibility relation between the block Gram in (20) and
the factor-pencil tensor in (25), or use a different global
rank-two invariant.
\end{minipage}}
\tag{30}
\]

This explains why completing the local quartic distance modulus, while
important for the near-Haar-equality branch, cannot by itself settle
unrestricted three-copy positivity.  In the large-slack branch the
antecedent of that stability theorem is absent, and the remaining
known exact consequences are jointly feasible at every negative
depth tending to zero.
