# Polar-alignment stability and the depth bound \(512/3755\)

## Status

This note strengthens the explicit generalized-depth bound for a
hypothetical unrestricted qutrit three-copy counterexample:
\[
\boxed{
 0<\delta<\frac{512}{3755}
 =\frac3{22}-\frac1{82610}.
}
\]
The preceding common trace-slack theorem gave
\(\delta<3/22\).  The improvement retains the polar-alignment defect
which that scalar bound discarded.

The new ingredient is an exact stability lemma.  For every
rank-at-most-two matrix \(C\), put
\[
 E(C)=(s_1(C)+s_2(C))^2-|\operatorname{Tr}C|^2.
\]
There is a phase times a positive semidefinite rank-at-most-two matrix
\(P\), with the same singular values as \(C\), such that
\[
 \|C-P\|_2^2\leq2E(C).
\]
The established positive-semidefinite three-copy theorem and the
operator-norm bound \(\|{\cal L}^{\otimes3}\|=1\) then force a
quantitative lower bound on \(E(C)\) at any negative transition.

This is an exact improvement of the localization of a counterexample,
not a proof that no counterexample exists.  The dependency-free exact
checker is
`verification/verify_n3_polar_alignment_depth_improvement.py`.

## 1. Distance to the positive cone from trace alignment

Let
\[
 C=\sum_{r=1}^2s_r|u_r\rangle\langle v_r|,
 \qquad s_1\geq s_2\geq0,
\tag{1}
\]
be a thin singular-value decomposition, with zero terms omitted.  Put
\[
 t=\operatorname{Tr}C
 =\sum_rs_r\langle v_r,u_r\rangle.
\tag{2}
\]
Choose a phase \(\zeta\) so that
\[
 \zeta\overline t=|t|;
\]
if \(t=0\), choose any phase.  Define
\[
 P=\zeta\sum_rs_r|u_r\rangle\langle u_r|.
\tag{3}
\]
Up to the scalar phase \(\zeta\), \(P\) is positive semidefinite of
rank at most two, and it has the same singular values and
Hilbert--Schmidt norm as \(C\).

Set
\[
 d_r=1-\operatorname{Re}
 \left(\zeta\langle u_r,v_r\rangle\right)\geq0.
\tag{4}
\]
Then
\[
\begin{aligned}
 \|C-P\|_2^2
 &=2\sum_rs_r^2d_r,\\
 (s_1+s_2)-|t|
 &=\sum_rs_rd_r.
\end{aligned}
\tag{5}
\]
The second identity follows from the choice of \(\zeta\).  Therefore
\[
\begin{aligned}
 \|C-P\|_2^2
 &\leq2s_1\bigl((s_1+s_2)-|t|\bigr)\\
 &=2E(C)\frac{s_1}{s_1+s_2+|t|}\\
 &\leq2E(C).
\end{aligned}
\]
We have proved:

### Lemma 1

Every rank-at-most-two \(C\) admits a phase-positive
rank-at-most-two \(P\) with the same singular values such that
\[
\boxed{\|C-P\|_2^2\leq2E(C).}
\tag{6}
\]

## 2. A negative transition needs polar defect

Write
\[
 {\cal A}={\cal L}^{\otimes3}.
\]
Its sector eigenvalues are
\[
 -\frac18,\quad\frac14,\quad-\frac12,\quad1,
\]
so
\[
 \|{\cal A}\|_{\rm op}=1.
\tag{7}
\]
Put
\[
 N=\|C\|_2^2=\|P\|_2^2,\qquad
 \Delta=(s_1-s_2)^2.
\]
The positive-semidefinite theorem gives
\[
 Q_3(P)\geq\frac18\Delta\geq0.
\tag{8}
\]
Using (6)--(8),
\[
\begin{aligned}
 Q_3(C)
 &=Q_3(P)
   +\langle C-P,{\cal A}C\rangle
   +\langle P,{\cal A}(C-P)\rangle\\
 &\geq\frac18\Delta
      -2\sqrt N\,\|C-P\|_2\\
 &\geq\frac18\Delta-2\sqrt{2NE}.
\end{aligned}
\tag{9}
\]

Normalize the Schur energy of a negative transition by
\[
 \langle z,S_Vz\rangle=1,\qquad
 \langle z,H_Vz\rangle=-\delta.
\tag{10}
\]
Since \(\langle z,H_Vz\rangle=2Q_3(C)\),
\[
 Q_3(C)=-\frac\delta2.
\tag{11}
\]
Equations (9)--(11) imply
\[
 \frac\delta2+\frac18\Delta
 \leq2\sqrt{2NE}.
\]
In particular,
\[
\boxed{
 E\geq\frac{\delta^2}{32N}.
}
\tag{12}
\]

## 3. Exact combination with the trace-slack identity

Retain the exact negative-depth simplex variables
\[
 y=(1-5\delta)L=4\sum_i g_i,\qquad
 a=\|\Pi_1C\|_2^2.
\tag{13}
\]
The common trace-slack calculation, before discarding the
polar-alignment defect, is the identity
\[
\boxed{
 1584\delta+297y+567a+18\Delta+18E=216.
}
\tag{14}
\]
The sector reconstruction also gives the exact norm formula
\[
\boxed{
 N=4\delta+\frac94a+\frac34y.
}
\tag{15}
\]
Consequently
\[
 567a+297y
 \geq252(N-4\delta),
\tag{16}
\]
because the right side is
\[
 567a+189y.
\]
Combining (12), (14), and (16), and dropping
\(18\Delta\geq0\), gives
\[
\begin{aligned}
 216
 &\geq1584\delta
   +252(N-4\delta)
   +\frac{9\delta^2}{16N}.
\end{aligned}
\tag{17}
\]
Equation (15) gives \(N\geq4\delta\).  On that half-line, the last
two terms in (17) are minimized at \(N=4\delta\), since
\[
 \frac{d}{dN}
 \left[
 252(N-4\delta)+\frac{9\delta^2}{16N}
 \right]
 =
 252-\frac{9\delta^2}{16N^2}
 \geq252-\frac9{256}>0.
\tag{18}
\]
Therefore
\[
\begin{aligned}
 216
 &\geq
 1584\delta+\frac9{64}\delta\\
 &=\frac{101385}{64}\delta.
\end{aligned}
\]
Thus
\[
 \delta\leq
 \frac{216\cdot64}{101385}
 =\frac{512}{3755}.
\tag{19}
\]

The inequality is strict for a negative physical transition.  Indeed,
equality in (16) requires \(y=0\), while
\[
 y=4\sum_i g_i>0
\]
by the fixed-left strictness theorem.  Hence
\[
\boxed{
 0<\delta<\frac{512}{3755}.
}
\tag{20}
\]
Finally,
\[
 \frac3{22}-\frac{512}{3755}
 =\frac1{82610},
\tag{21}
\]
which records the exact improvement over the previous explicit
constant.

## 4. Remaining obstruction

The gain is numerically small because the comparison (6) is a global
operator-norm estimate.  Its structural content is more useful:
every negative transition must stay quantitatively separated from
the phase-positive rank-two cone, and the required separation is paid
for by the same exact polar defect \(E\) appearing in the common
trace-slack identity.

A stronger result would require either:

1. a sharper endpoint continuity estimate than (9), using the common
   singular planes rather than only \(\|{\cal A}\|=1\); or
2. an exact coupling of \(E\) to the three local Haar defects \(g_i\).

Neither strengthening is proved here.
