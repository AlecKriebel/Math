# Hostile audit: marked mixed orbit \(R=xq\)

**Verdict:** PASS.  No defect, hidden division, exceptional \(d=0\)
branch, incomplete solve, or scope inflation was found.

**Audit date:** 2026-07-25 UTC.

This audit covers only the \(R=xq\) half of `marked_mixed_orbits`.
`verify_r_xq_pari.gp` is an independent exact PARI/GP reconstruction.  It
does not import the SymPy matrices: it differentiates the homogeneous
pieces, rebuilds the determinant, extracts monomial coefficients, and
performs its own exact linear algebra.

## Raw \(E_7\) kernel

With
\[
p=x^2,\qquad q=y^2+xz,\qquad P=p^2,\qquad Q=q^2,\qquad R=xq,
\]
the script first verifies \(\operatorname{Jac}(P,Q,R)=0\), then rebuilds
\[
E_7=\operatorname{Jac}(P,Q,W)+\operatorname{Jac}(P,V,R)
   +\operatorname{Jac}(U,Q,R).
\]
The resulting \(36\times26\) matrix has rank \(18\) and the stated
parameter-free maximal minor
\[
-5343626510991360.
\]

The two target shears, the three source-translation jets, and
\[
(0,x^3,0),\qquad(0,2zq,xz),\qquad(0,-2zq,y^2)
\]
are exact kernel vectors.  Their coefficient matrix has rank \(8\), with
minor \(32\).  The raw nullity is \(26-18=8\), so the list is complete.
The last three directions give exactly
\[
(U,V,W)=
\left(0,\;Ax^3+2(w_2-w_3)zq,\;w_2xz+w_3y^2\right).
\]

The first five vectors are legal gauges.  The target shears add the third
component to the first two, and affine source translations produce the
three directional-derivative jets.  These invertible affine operations
preserve the Keller property and only relabel lower homogeneous pieces.
No parameter is divided out.

## Complete \(E_6\) solve

Set \(d=w_2-w_3\).  PARI reconstructs the coefficient of \(t^6\) in
\[
\det\!\left(L+tJH_2+t^2JH_3+t^3JH_4\right).
\]
It is affine linear in the twelve claimed lower unknowns.  Its
\(28\times12\) coefficient matrix has symbolic rank \(10\) and the
parameter-free maximal minor
\[
-100663296.
\]
Thus its rank is exactly \(10\) for every value of \(A,w_2,w_3\), including
\(d=0\).

Direct substitution verifies the full solution
\[
\begin{gathered}
a_1=0,\quad a_2=a_3,\quad a_4=a_5=0,\\
b_1=0,\quad b_2=b_3,\quad b_4=0,\quad b_5=d^2,\\
\ell_{32}=0,\qquad \ell_{33}=w_3d.
\end{gathered}
\]
The \(a_3\)- and \(b_3\)-directions are two independent kernel vectors.
Since the nullity is exactly two, these are all solutions.  Substitution
annihilates every \(E_6\) coefficient, establishing the converse.

## Complete \(E_5\) solve and the \(d=0\) specialization

After the complete \(E_6\) substitution, \(E_5\) is affine linear in
\[
\ell_{12},\ell_{13},\ell_{22},\ell_{23}.
\]
Its \(21\times4\) coefficient matrix has rank \(4\) and the
parameter-free maximal minor \(256\).  Hence the solve is unique at every
parameter specialization.  PARI recovers
\[
\ell_{12}=\ell_{22}=0,\qquad
\ell_{13}=a_3d,\qquad \ell_{23}=b_3d,
\]
and direct substitution kills the full \(E_5\) polynomial.

The script then sets \(w_2=w_3\) in the independently rebuilt matrices,
not in a formula obtained by dividing by \(d\).  At \(d=0\):

- the \(E_6\) rank remains \(10\), with the same minor
  \(-100663296\);
- \(b_5=\ell_{33}=0\), and the complete \(E_6\) converse still vanishes;
- the \(E_5\) rank remains \(4\), with the same minor \(256\);
- its unique solution specializes to
  \(\ell_{12}=\ell_{13}=\ell_{22}=\ell_{23}=0\);
- the complete specialized \(E_5\) converse still vanishes.

Thus \(d=0\) is genuinely included.  No step divides by \(d\) or assumes it
nonzero.

## Determinant exit and scope

For every \(d\), the lower solves force
\[
\ell_{12}=\ell_{22}=\ell_{32}=0.
\]
These are the entries of the second column of \(L\), so \(\det L=0\).
Since the constant term of \(\det JF\) is \(\det L\), this contradicts
the Keller condition.

No resultants, denominator clearing, saturation, or irreducibility
assumptions occur.  The only scalar divisions implicit in row reduction
are by nonzero integers, valid in characteristic zero.

This audit establishes the exclusion only under the exact displayed
leading data \(H_4=(p^2,q^2,0)\), \(R=xq\).  It does not audit the
\(R=x(p-q)\) case, the classification placing maps into these orbits, or
priority.

## Reproduction

Run:

```text
./verify_r_xq_pari_strict.sh
```

A clean run ends with:

```text
ALL HOSTILE PARI/GP R=xq AUDIT CHECKS PASSED
```

This exact computation is evidence about the encoded algebra, not peer
review.
