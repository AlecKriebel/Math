# A nilpotent-overlap counterexample to the first principal-angle correction

## Status

This note gives an exact counterexample to an intermediate inequality.
It is **not** a square-zero counterexample and is not a negative
three-copy Werner witness.

For a full-column factorization
\[
 C=XY^\dagger,\qquad
 A=X^\dagger X,\quad B=Y^\dagger Y,\quad G=Y^\dagger X,
\]
put
\[
\begin{aligned}
 N&=\|C\|_2^2,\\
 S&=\sum_i\|\operatorname{Tr}_iC\|_2^2,\\
 P&=\sum_{i<j}\|\operatorname{Tr}_{ij}C\|_2^2,\\
 D&=s_1(C)s_2(C)=\sqrt{\det A\,\det B},
\end{aligned}
\]
and define the factorization-invariant principal-plane overlap
\[
 \kappa
 =
 \operatorname{Tr}\left(
 A^{-1}G^\dagger B^{-1}G
 \right)
 =
 \operatorname{Tr}(P_XP_Y).
\tag{1}
\]
Here \(P_X,P_Y\) are the orthogonal projections onto the two column
planes.  Thus \(\kappa=\cos^2\theta_1+\cos^2\theta_2\), where
\(\theta_1,\theta_2\) are their principal angles.

The proposed overlap-corrected inequality was
\[
\boxed{
 3N-2S+P+2D+\frac D4\kappa\geq0.}
\tag{2}
\]
It would have implied the surviving square-zero exterior inequality,
because \(C^2=0\) is equivalent, in the singular-plane
factorization, to \(G=0\), hence \(\kappa=0\).

The Gaussian-integer construction below violates (2).  Moreover,
\[
 \operatorname{Tr}G=\det G=0,\qquad G\ne0.
\tag{3}
\]
Thus the overlap is a nonzero nilpotent matrix.  This simultaneously
shows why corrections depending only on the characteristic
coefficients \(\operatorname{Tr}G,\det G\) cannot repair the
unrestricted exterior inequality.  Even the first correction which
sees the complete principal-angle mass, with coefficient \(1/4\), is
too small.

The dependency-free exact checker is
`verification/verify_n3_principal_overlap_correction_counterexample.py`.

## 1. Compact exact construction

Use binary-word order
\[
 000,001,010,011,100,101,110,111
\]
inside three qutrits.  Let
\[
X=
\begin{pmatrix}
15+11i&1+2i\\
-5-i&5i\\
5&-2-5i\\
12+i&-3-10i\\
-4-3i&-2+5i\\
-7-9i&-5+10i\\
10+6i&2-11i\\
-30-10i&-2-15i
\end{pmatrix},
\tag{4}
\]
and
\[
Z=
\begin{pmatrix}
2+19i&20-11i\\
-6-16i&4-4i\\
10+13i&-2+5i\\
-9-9i&3-4i\\
2-16i&5-2i\\
13i&-5+i\\
-4-12i&4-2i\\
3+9i&4-7i
\end{pmatrix}.
\tag{5}
\]
Take
\[
 a=8+5i,\qquad b=8-15i,
\]
and form the nonzero nilpotent matrix
\[
 G_0=
\begin{pmatrix}
-ab&a^2\\
-b^2&ab
\end{pmatrix}
=
\begin{pmatrix}
-139+80i&39+80i\\
161+240i&139-80i
\end{pmatrix}.
\tag{6}
\]
The polynomial parametrization in (6) gives
\[
 \operatorname{Tr}G_0=\det G_0=0
\tag{7}
\]
identically.

Set
\[
 A=X^\dagger X,\qquad
 \Delta=\det A=1232663,
\]
and define the Gaussian-integer matrix
\[
\boxed{
 Y=
 X\operatorname{adj}(A)G_0^\dagger
 \Delta Z
 -X\operatorname{adj}(A)X^\dagger Z.}
\tag{8}
\]
Since
\(\operatorname{adj}(A)A=\Delta I_2\), direct multiplication gives
\[
\boxed{Y^\dagger X=\Delta G_0.}
\tag{9}
\]
Consequently (3) holds exactly.

For reference, (8) is
\[
\begin{pmatrix}
2796130+23291231i&24762449-13947340i\\
-7440040-19477708i&5034703-4730775i\\
12287826+15775869i&-2625444+6002621i\\
-11107921-11621731i&3394987-5316298i\\
2327306-19505990i&6181213-2235678i\\
-355208+16421493i&-6215262+1717644i\\
-4707786-15290448i&4823441-2953433i\\
3234015+11074667i&4790609-8176340i
\end{pmatrix}.
\tag{10}
\]

Both \(X\) and \(Y\) have column rank two.  Hence \(C=XY^\dagger\)
has rank exactly two.

## 2. Exact sign certificate

Exact binary partial contraction gives
\[
\boxed{
\begin{aligned}
N&=5687218642840734153,\\
S&=11750875477966803914,\\
P&=2477784354164963891.
\end{aligned}}
\tag{11}
\]
Therefore
\[
 A_0:=3N-2S+P=-3962310673246441478<0.
\tag{12}
\]
The two Gram determinants give
\[
\boxed{
D^2=\det(X^\dagger X)\det(Y^\dagger Y)
=3783106952961465581191141499318975771.}
\tag{13}
\]
Finally, the principal overlap in (1) is the exact positive rational
\[
\boxed{
\kappa=
\frac{
491280799491106687496457081302285190
}{
3783106952961465581191141499318975771
}.}
\tag{14}
\]

Since \(A_0<0\), inequality (2) fails exactly when
\[
 A_0^2>D^2\left(2+\frac\kappa4\right)^2.
\]
After clearing the positive denominator \(4D^2\) from (14), the
difference between the two sides is the positive integer
\[
\boxed{\begin{aligned}
&1178385817096270686310864285696206375051688931213891192722859855833435685\\
&\hspace{20mm}>0.
\end{aligned}}
\tag{15}
\]
Equations (12)--(15) are a rational/integer sign certificate; no
floating-point comparison or algebraic-number approximation is used.

## 3. Consequence for the surviving problem

The example does not satisfy \(G=0\), so it does not test the
square-zero locus itself.  Its role is to separate three levels of
overlap information:
\[
\begin{array}{c|c}
\text{correction data}&\text{status}\\ \hline
\operatorname{Tr}G,\det G&\text{insufficient, even both zero},\\
\frac14D\,\operatorname{Tr}(P_XP_Y)
&\text{insufficient by (4)--(15)},\\
G=0&\text{surviving square-zero frontier}.
\end{array}
\]
Thus an overlap-defect proof, if one exists, needs either a strictly
stronger nonlinear function of both principal angles or the full
common-code relations, rather than only the first principal-angle
moment.
