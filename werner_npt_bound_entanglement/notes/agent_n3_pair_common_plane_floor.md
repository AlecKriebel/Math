# A conjugation-correct common-plane floor for the three-copy pair problem

## Status

This note records an exact reduction and one exact positive chart.  It
does **not** prove the unrestricted three-copy theorem.

Let
\[
 S_{(2)}=\frac49\sum_{i<j}{\mathsf A}_i{\mathsf A}_j,
 \qquad
 S_{(3)}=\frac89{\mathsf A}_1{\mathsf A}_2{\mathsf A}_3,
 \qquad
 {\mathsf A}_i=\frac{I-F_i}{2},
\]
and let \(Q_{(2)},Q_{(3)}\) be their positive logical two-qubit
compressions to the left and right singular planes.  The following
matrix inequality is sufficient for the sharp shifted pair theorem:
\[
 \boxed{\quad
 Q_{(2)}^\Gamma+
 \left(\frac29-\frac12\operatorname{Tr}Q_{(3)}\right)I_4
 \succeq0.
 \quad}                                                   \tag{1}
\]
After keeping track of all conjugations, (1) is exactly equivalent to
a single common-plane compression inequality, equation (11) below.
That is the surviving global target.

Equation (1) is proved here when the two singular planes have a common
logical two-dimensional factor on one physical site.  This chart
contains both the standard sharp zero code and the exact code for
which the three-exterior concurrence is \(8/27\).

The dependency-free exact checker is
`verification/verify_n3_pair_common_plane_floor.py`.

## 1. A universal partial-transpose floor

For every positive two-qubit operator \(R\),
\[
 \boxed{\qquad
 R^\Gamma+\frac12\operatorname{Tr}(R)I_4\succeq0.
 \qquad}                                                  \tag{2}
\]
Indeed, decompose \(R=\sum_a|z_a\rangle\langle z_a|\).  If the two
Schmidt coefficients of \(z_a\) are \(\sigma_1,\sigma_2\), the
eigenvalues of
\((|z_a\rangle\langle z_a|)^\Gamma\) are
\[
 \sigma_1^2,\quad \sigma_2^2,\quad
 \sigma_1\sigma_2,\quad-\sigma_1\sigma_2.
\]
Since
\[
 \sigma_1\sigma_2\leq
 \frac12(\sigma_1^2+\sigma_2^2)
 =\frac12\|z_a\|^2,
\]
the asserted floor holds for every pure summand and hence for their
sum.

Applying (2) to \(Q_{(3)}\), equation (1) implies
\[
 \frac29I_4+(Q_{(2)}+Q_{(3)})^\Gamma\succeq0.             \tag{3}
\]
This is precisely the positive-part matrix inequality needed in the
shifted pair reduction.  Thus (1) bypasses a separate evaluation of
the concurrence of \(Q_{(2)}+Q_{(3)}\).

## 2. The conjugation-correct common-plane inequality

Let \(U=(u_0,u_1)\) and \(V=(v_0,v_1)\) be the two orthonormal
singular frames.  The logical partial transpose in (1) is a
compression on the common four-plane
\[
 {\cal L}=\overline{\operatorname{ran}U}\otimes
          \overline{\operatorname{ran}V}.                \tag{4}
\]
This point is essential: replacing this plane by the un-conjugated
feature plane gives a false identity for complex frames.

Let \(P_i\) be the normalized maximally-entangled projector between
the two replicas at physical site \(i\).  For
\(k=0,1,2,3\), let \(P_k\) project onto the joint sector in which
exactly \(k\) of the three projectors \(P_i\) occur.  Put
\[
 r_k=\operatorname{Tr}(P_{\cal L}P_k),\qquad
 \sum_{k=0}^3r_k=4.                                      \tag{5}
\]
Partial transpose on the second physical replica sends
\[
 {\mathsf A}_i\longmapsto
 Y_i=\frac{I-3P_i}{2}.                                   \tag{6}
\]
On a sector with exactly \(k\) maximally-entangled factors, direct
evaluation gives
\[
\begin{array}{c|rrrr}
k&0&1&2&3\\ \hline
S_{(2)}^\Gamma&1/3&-1/3&0&4/3\\
S_{(3)}^\Gamma&1/9&-2/9&4/9&-8/9 .
\end{array}                                               \tag{7}
\]
Consequently
\[
 3Q_{(2)}^\Gamma
 =P_{\cal L}(P_0-P_1+4P_3)P_{\cal L},                    \tag{8}
\]
and
\[
 \operatorname{Tr}Q_{(3)}
 =\frac19(r_0-2r_1+4r_2-8r_3).                           \tag{9}
\]
Using \(r_0=4-r_1-r_2-r_3\),
\[
 3\left(\frac29-\frac12\operatorname{Tr}Q_{(3)}\right)
 =\frac12(r_1-r_2+3r_3).                                \tag{10}
\]
Therefore (1) is exactly equivalent to
\[
\boxed{
 P_{\cal L}(P_0-P_1+4P_3)P_{\cal L}
 +\frac12(r_1-r_2+3r_3)I_{\cal L}\succeq0.
}                                                        \tag{11}
\]
The operator and its scalar trace correction arise from the same
product four-plane \({\cal L}\); separating their sector bounds loses
the required nonlinear geometry.  Equivalently, for every unit
\(\psi\in{\cal L}\), with
\(p_k(\psi)=\|P_k\psi\|^2\), the remaining assertion is
\[
 p_0(\psi)-p_1(\psi)+4p_3(\psi)
 +\frac12(r_1-r_2+3r_3)\geq0.                            \tag{12}
\]

## 3. Exact common-factor theorem

Suppose that, after choosing bases in the two singular planes, there
are unit vectors \(x,y\) on the first two physical sites and a common
orthonormal pair \(e_0,e_1\) on the third such that
\[
 u_a=x\otimes e_a,\qquad v_a=y\otimes e_a,
 \qquad a=0,1.                                           \tag{13}
\]
Changing logical bases allows the same conclusion whenever the third
physical support is common and the first two-site factor is fixed in
each plane.

Put
\[
 \xi=\overline{x}\otimes y
\]
on the two replicas of the first two physical sites and define
\[
 \eta_i=\langle\xi|{\mathsf A}_i|\xi\rangle
 \quad(i=1,2),\qquad
 \eta_{12}=\langle\xi|{\mathsf A}_1{\mathsf A}_2|\xi\rangle.
                                                               \tag{14}
\]
If
\[
 \tau_i=\operatorname{Tr}
 \left(\rho_i^{\overline{x}}\rho_i^y\right),
\]
then
\[
 \eta_i=\frac12(1-\tau_i),\qquad
 0\leq\eta_i\leq\frac12.                                \tag{15}
\]
Let \(A_{\rm L}=(I-F_{\rm L})/2\) be the logical singlet
projector.  Factorization of the three local swaps gives the exact
logical matrices
\[
\boxed{
\begin{aligned}
 Q_{(3)}&=\frac89\eta_{12}A_{\rm L},\\
 Q_{(2)}&=\frac49\left[
       \eta_{12}I_4+(\eta_1+\eta_2)A_{\rm L}\right].
\end{aligned}}                                           \tag{16}
\]
The smallest eigenvalue of \(A_{\rm L}^\Gamma\) is \(-1/2\).
Since \(\operatorname{Tr}A_{\rm L}=1\), equations (15)--(16)
therefore yield
\[
\boxed{
\lambda_{\min}\left(
 Q_{(2)}^\Gamma+
 \left(\frac29-\frac12\operatorname{Tr}Q_{(3)}\right)I_4
\right)
=\frac29(1-\eta_1-\eta_2)\geq0.
}                                                        \tag{17}
\]
This proves (1), hence the shifted pair inequality, throughout the
common-factor chart.  Equality in (17) occurs exactly when
\(\eta_1=\eta_2=1/2\), equivalently \(\tau_1=\tau_2=0\).

For completeness, the same chart also proves the stronger
concurrence-split target.  The two matrices in (16) are invariant
under logical spin flip, so
\[
\begin{aligned}
 {\cal C}(Q_{(3)})&=\frac89\eta_{12},\\
 {\cal C}(Q_{(2)})&=\frac49
 \max\{0,\eta_1+\eta_2-2\eta_{12}\}.                     \tag{18}
\end{aligned}
\]
Moreover,
\[
 4\eta_{12}
 =1-\tau_1-\tau_2+|\langle\overline{x},y\rangle|^2
 \leq2,                                                  \tag{19}
\]
and \(\eta_1+\eta_2\leq1\).  Hence
\[
 {\cal C}(Q_{(2)})+{\cal C}(Q_{(3)})
 =\frac49\max\{\eta_1+\eta_2,2\eta_{12}\}
 \leq\frac49.                                            \tag{20}
\]

## 4. Three exact landmarks

For
\[
 U=(|000\rangle,|001\rangle),\qquad
 V=(|110\rangle,|111\rangle),
\]
one has
\[
 \eta_1=\eta_2=\frac12,\qquad \eta_{12}=\frac14.
\]
The floor (17) is zero.  Explicitly,
\[
 \operatorname{spec}(Q_{(2)}^\Gamma)
 =(-1/9,1/3,1/3,1/3),\qquad
 \operatorname{Tr}Q_{(3)}=2/9.                          \tag{21}
\]

For the exact three-exterior countercode based on
\[
 |\Phi\rangle=(|00\rangle+|11\rangle+|22\rangle)/\sqrt3
\]
and a common third-site logical frame, one has
\[
 \eta_1=\eta_2=\eta_{12}=\frac13.
\]
Here
\[
 \operatorname{spec}(Q_{(2)}^\Gamma)
 =(0,8/27,8/27,8/27),\qquad
 \operatorname{Tr}Q_{(3)}=8/27,                         \tag{22}
\]
so the floor has strict margin \(2/27\).

Finally, the computational code
\[
 U=(|000\rangle,|001\rangle),\qquad
 V=(|112\rangle,|212\rangle)
\]
has
\[
 Q_{(2)}=\frac13I_4,\qquad Q_{(3)}=\frac19I_4.           \tag{23}
\]
Thus \(\operatorname{Tr}Q_{(3)}=4/9\) is sharp even though the
matrix floor equals \(I_4/3\).

## 5. Remaining problem

The unrestricted target is the common-plane inequality (11) for
\[
 {\cal L}=\overline{\operatorname{ran}U}\otimes
          \overline{\operatorname{ran}V},
\]
with arbitrary complex two-planes \(U,V\subset(\mathbb C^3)^{\otimes3}\).
This is a product four-plane satisfying two coupled sets of Pluecker
relations.  The sector weights \(r_k\) alone do not characterize it.
A global proof must couple the principal angles of \({\cal L}\) to
the four sectors with those Pluecker relations, exactly as (11)
does.

Unrestricted complex numerical searches have approached equality in
(1) and have not produced a violation.  This is discovery evidence
only and is not used in any theorem above.
