# Hostile audit of the marked triple-companion orbit

**Audit timestamp:** 2026-07-25T08:24:10Z.

**Original verdict:** **FAIL AS WRITTEN; THE EXCLUSION THEOREM SURVIVES
AFTER REPAIR.**  The submitted `NOTE.md` and primary SymPy certificate
silently specialized generic rational-function solves across rank-drop
strata.  Two displayed "complete" solves were false there.

**Resolution:** the parent note and primary SymPy verifier have now been
revised to include every fresh rank-drop chart below.  The corrected
primary strict run, primary corruption test, independent PARI/GP strict
run, and independent corruption test all pass.  The current repaired
package is therefore **PASS / audited**; the defect descriptions below
are retained as the audit trail.

This audit is independent PARI/GP code reconstructed directly from the
weighted Jacobian determinant.  The original SymPy program is the
methodologically separate check.  Both are exact encoded-algebra checks,
not peer review.

## Confirmed global algebra

The audit independently reconstructs all of the following.

* The raw \(E_7\) matrix is \(36\times26\), has rank \(8\) and nullity
  \(18\), and has fixed maximal minor \(483729408\).
* The five gauge directions and thirteen displayed normal directions
  span the full kernel.  Their fixed independence minor is
  \(-2048/27\).
* The general \(E_6\) lower system is \(28\times14\), has constant rank
  \(4\), and has parameter-free pivot minor \(10368\).
* Its literal residual contains
  \[
  \frac{32}{3}w_5^2,\qquad
  \frac{8}{3}(2w_4^2+3Aw_5).
  \]
  After \(w_5=w_4=0\), the full residual vector spans exactly the same
  eight-dimensional vector space of quadrics as
  \[
  Aw_1,\ A(w_2-w_3),\
  KB_1,\ KB_2,\ KB_3,\ K(B_4-B_5),\ KB_6,\ KB_7,
  \quad K=4w_3-3A.
  \]
  Thus this is equality of compatibility ideals here, not merely a list
  of necessary equations.

## Defect 1: the open branch \(K\ne0,\ C\ne0,\ A=0\)

The original \(E_5\) solve for \(C\ne0\) uses a pivot proportional to
\[
C A^2(3A-4w_3)^4.
\]
It therefore does not cover \(A=0\), contrary to the branch statement.
On the fresh \(A=0\) specialization the \(E_5\) rank drops from \(8\) to
\(6\); in particular it leaves \(\ell_{32}\) and \(\ell_{33}\) free.

The branch is nevertheless closed without dividing by either of them.
Here \(w_3\ne0\).  Fresh \(E_5\) gives
\[
\ell_{12}=0,\quad
b_1=b_4=0,\quad b_2=b_3,\quad b_5=C^2/4,
\quad a_3=2\ell_{13}/C.
\]
The literal \(E_4\) coefficients then contain, successively,
\[
\frac43(2\ell_{33}-w_3C)^2,\qquad
-\frac83\ell_{32}^2,\qquad
4w_3\ell_{22}.
\]
They force
\(\ell_{33}=w_3C/2,\ell_{32}=\ell_{22}=0\); the second column of \(L\)
vanishes.  Thus the theorem survives this omitted specialization.

## Defect 2: the resonant branch \(K=0,\ A\ne0\)

After \(E_5\) reduces
\[
V=B_1x^2y+B_2x^2z+Czq,
\]
the original lower solve uses pivots proportional to \(B_1\).  A fresh
second pivot covers \(B_1=0,B_2\ne0\).  On these two opens, exact \(E_3\)
compatibility forces respectively
\[
\frac{3}{16}A^3B_1^2=0,\qquad
-\frac38A^3B_2^2=0.
\]
Hence every possible solution lies on the closed stratum
\(B_1=B_2=0\), which must be recomputed rather than obtained by
specializing the generic formulas.

On that closed stratum, fresh \(E_5\) has rank \(4\), not \(5\).  If
\(C\ne0\), its complete solution is
\[
\ell_{12}=\ell_{32}=0,\qquad
\ell_{33}=\frac38AC,\qquad
a_3=\frac{2\ell_{13}}{C};
\]
\(\ell_{13}\) is free.  This directly contradicts equation (12) of the
original note, which asserts \(\ell_{13}=0\) after \(B_2=0\).  Fresh
\(E_4\) gives
\[
b_1=b_4=0,\qquad b_2=b_3,\qquad b_5=C^2/4
\]
without constraining \(\ell_{13}\).  The literal \(E_3\) coefficients
include
\[
[x^2z]E_3=[xy^2]E_3=\frac34A^2\ell_{22}.
\]
Since \(A\ne0\), \(\ell_{22}=0\), and the second column of \(L\)
vanishes.  If \(C=0\), fresh \(E_5\) directly forces
\(\ell_{12}=\ell_{13}=\ell_{32}=\ell_{33}=0\), so \(\det L=0\).

## Defect 3: the branch \(K=A=0\)

After the two verified \(E_5\) cube compatibilities force
\(w_1=w_2=0\), write
\[
V=B_1x^2y+B_2x^2z+B_3xyz+B_4xz^2+B_5y^2z+B_6yz^2+B_7z^3.
\]
The literal fresh \(E_5\) equations are
\[
\begin{array}{rclcrcl}
-3B_1a_3&=&0,&&6B_2a_3&=&0,\\
-3B_3a_3+6\ell_{12}&=&0,&&
6B_3a_3+6\ell_{12}&=&0,\\
(12B_4-6B_5)a_3-12\ell_{13}&=&0,&&
6B_5a_3-12\ell_{13}&=&0,\\
-3B_6a_3&=&0,&&12B_6a_3&=&0,\\
18B_7a_3&=&0.&&&&
\end{array}
\]
Consequently either \(a_3=0\), giving
\(\ell_{12}=\ell_{13}=0\), or the only exceptional stratum is
\[
V=Czq,\qquad
\ell_{12}=0,\qquad \ell_{13}=Ca_3/2.
\]
Thus the original claim that the complete \(E_6,E_5\) solve forces
\(a_3=0\) for arbitrary \(V\) is false.

The repair is exhaustive.  In both branches the literal \(E_4\)
coefficients first force
\[
\ell_{33}=0,\qquad \ell_{32}=0
\]
by the same \(16\ell_{33}^2/3\) and
\(-8\ell_{32}^2/3\) squares.  If \(a_3=0\), or if \(C=0\), this already
gives \(\det L=0\).  On the sole remaining open stratum
\(Ca_3\ne0\), fresh \(E_4\) gives
\[
b_1=b_4=0,\qquad b_2=b_3,\qquad b_5=C^2/4
\]
from a \(4\times4\) minor \(648a_3^4\).  The literal \(E_3\)
coefficient
\[
[x^3]E_3=-3a_3\ell_{22}
\]
then forces \(\ell_{22}=0\), so the second column of \(L\) vanishes.

## Editorial defect

Equation (4) of the original note is missing a `+` before the \(w_4xyz\)
term and another `+` before the \(B_6yz^2\) term.  The programs encode
the intended plus signs, so this is typographical rather than algebraic.

## Promotion condition — satisfied

The note and primary verifier now use the fresh rank-stratified arguments
above, and both exact backends pass strict and fail-closed wrappers.
