# Hostile audit of the unmarked triple-companion \(c=0\) orbit

**Verdict:** PASS.  No algebraic defect, hidden division, exceptional
rank-drop branch, extraneous component, or scope inflation was found.

**Audit date:** 2026-07-25 UTC.

This is an independent exact reconstruction in PARI/GP.  The script does
not import any matrix or row reduction from the SymPy certificate: it
differentiates the displayed homogeneous pieces, expands the determinant,
extracts monomial coefficients, and rebuilds every matrix.

## 1. Raw \(E_7\) kernel and the five-direction gauge

For
\[
p=x^2,\quad q=y^2+xz,\quad
P=(p-q)^2,\quad Q=(p+q)^2,\quad R=x^3,
\]
PARI reconstructs
\[
E_7=\operatorname{Jac}(P,Q,W)+\operatorname{Jac}(P,V,R)
   +\operatorname{Jac}(U,Q,R).
\]
In the 26 raw coefficients of two cubics and one quadratic, the coefficient
matrix is \(36\times26\), has rank \(16\), and has the stated nonzero
maximal minor
\[
3194799993706229268480.
\]

The two target-shear directions, the three translation jets, and the five
normal directions in `NOTE.md` all lie in this kernel.  Their \(26\times10\)
coefficient matrix has rank \(10\), with the stated minor
\[
-4096/9.
\]
Since the raw nullity is exactly \(10\), this list is a complete kernel
basis.  The script also verifies directly that the linear combination of
the last five directions with coefficients \(S,w_0,w_1,w_2,w_3\) is
exactly the displayed normal form (5).

The first five directions are genuine gauges: adding the third target
component to either of the first two components removes the two \(R=x^3\)
directions, and affine source translation removes the three directional
derivatives of \((P,Q,R)\).  These invertible affine operations preserve
the Keller property and do not change \(H_4\) or \(R=(H_3)_3\).  They only
relabel lower homogeneous pieces.  No parameter is divided out in taking
this gauge.

## 2. Degree-six compatibility

The determinant is reconstructed as
\[
\det\!\left(L+tJH_2+t^2JH_3+t^3JH_4\right).
\]
Its \(t^6\)-coefficient gives a \(28\times12\) affine-linear system.  Its
symbolic rank is \(10\), while the parameter-free \(10\times10\) minor is
\[
7925422620672.
\]
Consequently the rank is exactly \(10\) at every parameter specialization;
there is no rank-drop branch.

More strongly than needed, the fourteenth coefficient row has zero
coefficient vector in all twelve lower unknowns.  Its right side is
\[
-\frac{32}{3}(w_2-w_3)^2.
\]
Equivalently, the standard basis vector \(e_{14}\) is an integral left
syzygy and its compatibility pairing is the displayed square.  This is a
parameter-free identity, so \(w_2=w_3\) follows without dividing by
\(w_1\), \(w_2-w_3\), or any other parameter.

After substituting \(w_3=w_2\), PARI verifies all twelve formulas (9) by
direct substitution.  The two free directions, corresponding to \(a_3\)
and \(b_3\), are independent kernel vectors; rank \(10\) proves they span
the full kernel.  Thus the displayed affine solution is complete.

## 3. Degree-five compatibility

After the complete \(E_6\) substitution, the degree-five system has rank
\(5\) in the nine listed lower variables.  If the degree-five monomials are
ordered as in the certificate, the constant integer vector
\[
-e_3+e_4
\]
is a left syzygy.  Its compatibility pairing is
\[
\frac89w_1^3.
\]
Here rows \(3\) and \(4\) correspond to \(x^4z\) and \(x^3y^2\),
respectively.  Again, the conclusion \(w_1=0\) uses no parameter division
and survives every specialization.

With \(w_1=0\), PARI independently recovers the residual polynomial (12).
The four columns \(\ell_{12},\ell_{13},\ell_{22},\ell_{23}\) have the
parameter-free pivot minor \(20736\), and their unique solution is
\[
\ell_{12}=\ell_{22}=0,\qquad
2\ell_{13}=Sa_3,\qquad 2\ell_{23}=Sb_3.
\]
Direct converse substitution annihilates every coefficient of \(E_5\).

## 4. Determinant exit and scope

The \(E_6\) formula
\[
\ell_{32}=\frac23w_1(w_0-w_2)
\]
gives \(\ell_{32}=0\).  Together with the degree-five solve,
\[
\ell_{12}=\ell_{22}=\ell_{32}=0,
\]
so the second column of \(L\) is zero and \(\det L=0\).  For
\(F=LX+H_2+H_3+H_4\), the constant term of \(\det JF\) is \(\det L\).
Therefore this branch cannot be Keller.

No resultants, denominator clearing, saturation, or irreducibility
assumptions occur, so there are no extraneous branches to audit.  The only
divisions are by nonzero rational integers, valid in characteristic zero.

The conclusion is exactly scoped to the displayed \(c=0\) joint orbit.
This audit does **not** certify that this orbit exhausts any larger
classification of quartic leading forms, and it makes no priority claim.

## 5. Reproduction

Run:

```text
./verify_hostile_pari_strict.sh
```

The strict wrapper rejects PARI syntax/type diagnostics and requires the
final success marker.  A clean run ends with:

```text
ALL HOSTILE PARI/GP c=0 AUDIT CHECKS PASSED
```

This exact computation is evidence about the encoded algebra, not peer
review.
