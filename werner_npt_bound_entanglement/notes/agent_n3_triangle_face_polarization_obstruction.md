# Polarization of the strict triangle, and an exact face-feature obstruction

## Status

This note polarizes the exact two-face complete-square certificate at
the strict-interior Schur pivot.  The Bargmann cross term has a clean
common-defect interpretation:
\[
 \boxed{\qquad
  -m=\Delta(b,b'),
 \qquad
  \Delta(x,y)=2\langle x,y\rangle
  -\langle S^{-1/2}Tx,S^{-1/2}Ty\rangle .
 \qquad}                                                   \tag{1}
\]
After expanding the two complementary face certificates, the pivot
feature cancels exactly.  What remains is precisely the pair of
missing-frame leakage pairings
\[
 \boxed{\qquad
 m=\langle z,T_3B_3\rangle
   =\langle T_2B_2,z'\rangle .
 \qquad}                                                   \tag{2}
\]

There is also an exact obstruction to closing the argument from the
three face decompositions separately.  The scalar frame model
\[
 S=1,\qquad F_1=F_2=F_3=\frac25
\]
satisfies every individual strengthened face identity
\[
 S-F_e-F_f=\frac12F_g
\]
with the rank-six and Haar slacks set to zero, but its full residual is
\[
 S-F_1-F_2-F_3=-\frac15.
\]
At the Schur pivot it gives
\[
 A=B=\frac23,\qquad m=\frac43,
\]
so \(|m|^2=4AB\).  Thus no contraction obtained only by placing the
three independent nonnegative face features in an abstract direct sum
can prove \(|m|^2\leq AB\).  A successful proof must use an additional
cross-site common-code relation coupling the \(r\)- and \(s\)-features
of different missing edges.

The scalar model is not asserted to arise from a physical rank-two
code.  It is an exact counterexample only to the independent-face
feature-map route.  The dependency-free checker is
`verification/verify_n3_triangle_face_polarization_obstruction.py`.

## 1. Triangle notation

Fix the code plane and retain the notation of the lossless low-sector
Schur reduction.  Let
\[
 T=(T_1,T_2,T_3),\qquad
 F_e=\frac12T_eT_e^\dagger,\qquad S\succ0.                \tag{3}
\]
For fixed coefficient directions \(B_e\), put
\[
 Y_e=S^{-1/2}T_eB_e,
\]
\[
 d_e=2\|B_e\|^2-\|Y_e\|^2,\qquad
 c_{ef}=\langle Y_e,Y_f\rangle .                         \tag{4}
\]
Assume \(d_1>0\), and define
\[
\begin{aligned}
 A&=d_2-\frac{|c_{12}|^2}{d_1},\\
 B&=d_3-\frac{|c_{13}|^2}{d_1},\\
 m&=c_{23}+\frac{\overline{c_{12}}c_{13}}{d_1}.
\end{aligned}                                             \tag{5}
\]
Use the residualized inputs
\[
\begin{aligned}
 b&=\left(\frac{c_{12}}{d_1}B_1,B_2,0\right),\\
 b'&=\left(\frac{c_{13}}{d_1}B_1,0,B_3\right),
\end{aligned}                                             \tag{6}
\]
and set
\[
 z=S^{-1}Tb,\qquad z'=S^{-1}Tb'.                         \tag{7}
\]

Direct expansion of (4)--(7) gives
\[
 \Delta(b,b)=A,\qquad
 \Delta(b',b')=B,\qquad
 \boxed{\Delta(b,b')=-m},                                \tag{8}
\]
where \(\Delta\) is (1).  Hence the missing determinant inequality is
exactly Cauchy--Schwarz for \(\Delta\) on these two residualized
directions.  The difficulty is that the full form \(\Delta\) is the
unknown three-edge residual and need not be positive a priori.

## 2. Polarized complete squares

Put
\[
 H=S-F_1-F_2-F_3                                        \tag{9}
\]
and, for every edge,
\[
 a_e=b_e-\frac12T_e^\dagger z,\qquad
 a'_e=b'_e-\frac12T_e^\dagger z'.                       \tag{10}
\]
Polarizing the complete-square identity gives
\[
 \boxed{\qquad
 -m=2\sum_{e=1}^3\langle a_e,a'_e\rangle
       +\langle z,Hz'\rangle .
 \qquad}                                                  \tag{11}
\]
Because \(b_3=0\) and \(b'_2=0\), define
\[
 p_3=\frac12T_3^\dagger z=-a_3,\qquad
 p'_2=\frac12T_2^\dagger z'=-a'_2.                      \tag{12}
\]
Then (11) becomes
\[
\boxed{
 -m=
 2\langle a_1,a'_1\rangle
 -2\langle a_2,p'_2\rangle
 -2\langle p_3,a'_3\rangle
 +\langle z,Hz'\rangle .
}                                                        \tag{13}
\]

The two diagonal face identities are
\[
\begin{aligned}
 A={}&2\|a_1\|^2+2\|a_2\|^2
      +\langle z,(H+F_3)z\rangle,\\
 B={}&2\|a'_1\|^2+2\|a'_3\|^2
      +\langle z',(H+F_2)z'\rangle.                      \tag{14}
\end{aligned}
\]
The exact face-slack decomposition supplies positive quadratic forms
\(r_g,s_g\) such that
\[
\begin{aligned}
\langle z,(H+F_3)z\rangle
 &=\frac12w_3(z)+\frac13r_3(z)+\frac23s_3(z),\\
\langle z',(H+F_2)z'\rangle
 &=\frac12w_2(z')+\frac13r_2(z')+\frac23s_2(z'),
\end{aligned}                                             \tag{15}
\]
where
\[
 w_g(x)=\langle x,F_gx\rangle
       =\frac12\|T_g^\dagger x\|^2.                     \tag{16}
\]
Consequently
\[
\boxed{
\begin{aligned}
 A={}&2\|a_1\|^2+2\|a_2\|^2+\|p_3\|^2
      +\frac13r_3(z)+\frac23s_3(z),\\
 B={}&2\|a'_1\|^2+2\|a'_3\|^2+\|p'_2\|^2
      +\frac13r_2(z')+\frac23s_2(z').
\end{aligned}}                                           \tag{17}
\]

This displays the initial obstruction to a termwise feature pairing:
the term \(-2\langle a_2,p'_2\rangle\) pairs features of squared
norms \(2\|a_2\|^2\) and \(\|p'_2\|^2\), and therefore carries the
coefficient \(\sqrt2\) after normalization.  The companion term has
the same mismatch.  Any contraction must use the remaining
\(H,r,s\) correlations coherently; bounding the displayed terms
separately loses exactly a factor two after squaring.

## 3. Exact cancellation of the pivot feature

The residualization in (6) says that \(b\) and \(b'\) are orthogonal
to the pivot direction in the corresponding two-face defect forms.
Equivalently,
\[
 \langle B_1,a_1\rangle
 =\langle B_1,a'_1\rangle=0.                             \tag{18}
\]
Indeed,
\[
\begin{aligned}
2\langle B_1,a_1\rangle
&=2\frac{c_{12}}{d_1}\|B_1\|^2
 -\langle Y_1,
   \frac{c_{12}}{d_1}Y_1+Y_2\rangle\\
&=\frac{c_{12}}{d_1}
  \left(2\|B_1\|^2-\|Y_1\|^2\right)-c_{12}=0,
\end{aligned}                                             \tag{19}
\]
and the other equation is identical.

Using (18), a direct expansion of
\(\langle z,Hz'\rangle\) gives
\[
\boxed{\qquad
\langle z,Hz'\rangle
=m-2\langle a_1,a'_1\rangle
 -\langle z,(F_2+F_3)z'\rangle .
\qquad}                                                   \tag{20}
\]
Substitution into (13), followed by
\[
\langle z,F_ez'\rangle
=\frac12\langle T_e^\dagger z,T_e^\dagger z'\rangle,
\]
cancels the entire pivot feature and yields
\[
\boxed{
\begin{aligned}
m
&=\langle B_2,\tfrac12T_2^\dagger z'\rangle
  +\langle\tfrac12T_3^\dagger z,B_3\rangle\\
&=\frac12\left(
 \langle T_2B_2,z'\rangle+\langle z,T_3B_3\rangle
\right).
\end{aligned}}                                           \tag{21}
\]
Each term in parentheses is in fact \(m\) separately:
\[
\boxed{\qquad
 m=\langle T_2B_2,z'\rangle
  =\langle z,T_3B_3\rangle .
\qquad}                                                   \tag{22}
\]
Equation (22) is the symmetric polarization of the two quantitative
missing-frame estimates.  It also shows precisely what is not yet
controlled: the two leakage functionals agree, but the independent
face decompositions do not supply a contractive identification
between their complementary \(r\)- and \(s\)-feature spaces.

## 4. Exact abstract obstruction

It remains possible that the physical common-code origin enforces the
needed identification.  It is not a consequence of the face
certificates themselves.

Take one-dimensional output and coefficient spaces and set
\[
 S=1,\qquad T_1=T_2=T_3=\frac2{\sqrt5},\qquad
 F_e=\frac12T_eT_e^\dagger=\frac25.                     \tag{23}
\]
For every missing edge \(g\),
\[
 S-F_e-F_f=\frac15=\frac12F_g.                          \tag{24}
\]
Thus (15) holds exactly with
\[
 r_g=s_g=0,\qquad w_g(x)=\frac25|x|^2.                  \tag{25}
\]
All one- and two-edge operators are positive, and the strengthened
face lower bound by half the missing frame is saturated.  Nevertheless
\[
\boxed{\qquad
 H=S-F_1-F_2-F_3=-\frac15<0.
\qquad}                                                   \tag{26}
\]

Choose \(B_1=B_2=B_3=1\).  Then
\[
 d_e=2-\frac45=\frac65,\qquad
 c_{ef}=\frac45.                                        \tag{27}
\]
The triangle matrix is
\[
 G=
 \begin{pmatrix}
 6/5&-4/5&-4/5\\
 -4/5&6/5&-4/5\\
 -4/5&-4/5&6/5
 \end{pmatrix},
 \qquad
 \operatorname{spec}G=
 \left(-\frac25,2,2\right).                             \tag{28}
\]
At the pivot,
\[
 A=B=\frac23,\qquad m=\frac43,                           \tag{29}
\]
and hence
\[
\boxed{\qquad |m|^2=\frac{16}{9}=4AB. \qquad}           \tag{30}
\]

Therefore the exact diagonal decompositions (17), their
missing-frame stability, and positivity of all proper triangle faces
still permit a factor-two failure in the unsquared cross estimate.
The remaining physical lemma must prohibit the simultaneous abstract
configuration
\[
 r_1=r_2=r_3=s_1=s_2=s_3=0,\qquad
 F_1=F_2=F_3=\frac25S,                                  \tag{31}
\]
or replace it by an explicit cyclic cross-site inequality.  This is a
strictly more precise obstruction than treating the six face slacks
as unrelated nonnegative scalars.
