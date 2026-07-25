# Independent hostile audit of the marked triple orbit

**Audit verdict:** the orbit-exclusion theorem survives.  The originally
submitted `NOTE.md` and SymPy certificate contained two genuine
rank-specialization defects: their claims of complete lower solves were
false on closed strata.  The parent note and primary verifier have since
been corrected using the branches below.  Both corrected exact backends
and both fail-closed tests now pass, so the repaired package is audited.

**Audit date:** 2026-07-25 UTC.

## Checks that pass unchanged

PARI independently reconstructs the raw \(E_7\) matrix.  It has rank \(8\),
nullity \(18\), fixed maximal minor \(483729408\), and the displayed
five gauge plus thirteen normal directions form a complete kernel basis
with minor \(-2048/27\).

The general \(E_6\) matrix has constant rank \(4\) and fixed minor \(10368\).
Polynomial left syzygies give
\[
w_5^2,\qquad 3Aw_5+2w_4^2,
\]
so \(w_4=w_5=0\).  With \(d=w_2-w_3\) and
\(K=4w_3-3A\), the remaining pairings are exactly
\[
Aw_1,\ Ad,\ KB_1,\ KB_2,\ KB_3,\ K(B_4-B_5),\
KB_6,\ KB_7.
\]
The two \(B_6\) equations combine to \(5Aw_1=0\), and the \(B_7\)
equation differs from the \(Ad\) row by \(-6KB_7\).  Only nonzero integer
scalars are used.

The open \(K\ne0\) branch closes.  In particular, the \(A=0,C\ne0\)
specialization must be rebuilt rather than obtained from the generic
\(A\)-pivot solve.  Its fresh \(E_5\) solve leaves
\(\ell_{32},\ell_{33}\) free, and the resulting \(E_4\) system is
nonlinear in those remaining variables.  Literal coefficients give,
successively,
\[
\frac43(2\ell_{33}-w_3C)^2,\qquad
-\frac83\ell_{32}^2,\qquad
4w_3\ell_{22}.
\]
They force
\(\ell_{33}=w_3C/2,\ell_{32}=\ell_{22}=0\), so the second column of
\(L\) vanishes.

## Defect 1: \(K=0,\ A\ne0\)

After degree-five compatibility reduces
\[
V=B_1x^2y+B_2x^2z+Czq,
\]
the generic \(E_5/E_4\) solve has rank-five pivots proportional to
\(B_1\), or on the fresh \(B_1=0\) chart proportional to \(B_2\):
\[
\begin{array}{c|c|c}
 &E_5&E_4\\ \hline
B_1\ne0&-1728A^2B_1&243A^9B_1/64\\
B_1=0,\ B_2\ne0&3456A^2B_2&-243A^9B_2/32.
\end{array}
\]
Literal \(E_3\) rows give
\[
[xyz]-[y^3]=-\frac38A^3B_2^2,
\qquad
[x^2y]_{B_2=0}=\frac3{16}A^3B_1^2.
\]
Thus the open stratum \((B_1,B_2)\ne(0,0)\) is impossible.

The original certificate then specializes its generic solve to
\(B_1=B_2=0\).  This is invalid: both \(E_5\) and \(E_4\) drop rank from
\(5\) to \(4\).

For \(C\ne0\), the fresh complete solve is
\[
\ell_{12}=\ell_{32}=0,\qquad
\ell_{33}=\frac38AC,\qquad
a_3=\frac{2\ell_{13}}{C},
\]
with \(\ell_{13}\) free.  The \(E_5\) pivot is \(288A^2C\).
Consequently the assertion
\[
\ell_{13}=-\frac18A^2B_2=0
\]
in equation (12) is false on this stratum.

Fresh \(E_4\), in \(b_1,b_2,b_4,b_5\), has pivot
\(-81A^8/32\) and gives
\[
b_1=0,\quad b_2=b_3,\quad b_4=0,\quad b_5=C^2/4.
\]
It leaves \(\ell_{13}\) free.  The literal residual \(E_3\) contains
\[
[x^2z]=[xy^2]=\frac34A^2\ell_{22},
\]
so \(\ell_{22}=0\), and the second column of \(L\) vanishes.

For \(C=0\), a fresh \(E_5\) pivot \(576A^2\) forces
\(\ell_{12}=\ell_{13}=\ell_{32}=\ell_{33}=0\), giving
\(\det L=0\) immediately.

## Defect 2: \(K=A=0\)

After the division-free \(E_5\) cube rows force \(w_1=w_2=0\), leave
the seven coefficients of \(V\) arbitrary.  The literal \(E_5\)
coefficients include
\[
\begin{gathered}
-3B_1a_3,\quad 6B_2a_3,\quad
9B_3a_3,\quad 12(B_4-B_5)a_3,\\
-3B_6a_3,\quad18B_7a_3.
\end{gathered}
\]
Hence the exhaustive split is:

- \(a_3=0\), in which case the paired rows force
  \(\ell_{12}=\ell_{13}=0\); or
- \(a_3\ne0\), in which case necessarily
  \(V=Czq\), \(\ell_{12}=0\), and
  \(\ell_{13}=Ca_3/2\).

Thus the statement in Section 6 that the complete \(E_6,E_5\) solve
always gives \(a_3=0\) is false.  The unique exceptional shape is
\(V=Czq\); there are no omitted seven-parameter leaves.

In both leaves \(E_4\) gives
\[
[y^3z]=\frac{16}{3}\ell_{33}^2,\qquad
[xy^3]_{\ell_{33}=0}=-\frac83\ell_{32}^2.
\]
For \(a_3=0\), this already gives \(\det L=0\).
For \(a_3\ne0,\ C\ne0\), fresh \(E_4\) has pivot
\(648a_3^4\) and gives
\[
b_1=0,\quad b_2=b_3,\quad b_4=0,\quad b_5=C^2/4.
\]
Then
\[
[x^3]E_3=-3a_3\ell_{22},
\]
so \(\ell_{22}=0\) and the second column vanishes.  If \(C=0\),
\(\ell_{13}=0\) and the determinant vanishes immediately after the
square exit.

## Other audit observations

Formula (4) in `NOTE.md` is also missing printed plus signs before the
\(w_4xyz\) and \(B_6yz^2\) terms.  The SymPy code and this audit use the
intended sums.

No resultants, saturation, or denominator clearing occurs.  Every
division in the corrected tree is either by a nonzero integer or is made
only on an explicitly open branch such as \(A\ne0\), \(C\ne0\),
\(K\ne0\), \(B_1\ne0\), or \(B_2\ne0\).

## Reproduction

Run:

```text
./verify_marked_triple_pari_strict.sh
```

The strict run ends with:

```text
ALL HOSTILE PARI/GP MARKED-TRIPLE AUDIT CHECKS PASSED
```

This exact computation is evidence about the encoded algebra, not peer
review.
