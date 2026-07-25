# Hostile audit report: fixed-divisor \(e=2\) mixed companions

## Verdict

**PASS**, as of 2026-07-25T08:52:17Z.

The theorem in the parent `NOTE.md` survives an independent exact
PARI/GP reconstruction.  No counter-specialization was found.  The result
has the scope stated there: it excludes the mixed companion \(R=xq\) for
the two displayed fixed-divisor \(e=2\) normal forms.  It does not exclude
the triple companion \(R=x^3\), close the entire fixed-divisor row, or say
anything by itself about every quartic Keller map.

This is not peer review.  It is an adversarial algebra audit of the encoded
normal forms and Jacobian identities.

## Independent backend

`verify_mixed_orbits_pari.gp` reconstructs the homogeneous monomial bases,
Jacobians, weighted determinant, coefficient matrices, fixed minors,
kernel directions, affine solves, left syzygies, resultants, and
determinant exits directly in PARI/GP.  It does not import SymPy output or
serialized matrices.

Run:

```sh
./verify_mixed_orbits_pari_strict.sh
./test_fail_closed.sh
```

The strict runner rejects PARI diagnostics, requires six unique progress
and terminal markers, and uses the machine's fixed PARI executable rather
than a `PATH`-resolved shim.  The injection test verifies rejection of:

1. a corrupted raw-\(E_7\) maximal minor; and
2. a successful PARI run with its terminal attestation removed.

## Findings

### Raw \(E_7\) completeness and gauges

For each pencil, the reconstructed raw matrix is \(36\times26\), has rank
\(14\), and therefore has nullity \(12\).  Independent nonzero maximal
minors are checked:

\[
-5308416\quad\text{and}\quad -849346560.
\]

The twelve displayed directions lie in the kernel and have independent
minors \(64\) and \(-128\).  Their first five directions are legal:

- \((R,0,0)\) and \((0,R,0)\) come from target shears by the third
  component;
- \((\partial_vP,\partial_vQ,\partial_vR)\), for
  \(v=x,y,z\), are the degree-\((3,3,2)\) effects of source
  translations.

The accompanying changes in the first two quadratic components and in
lower terms are harmless because those terms remain arbitrary.  A target
translation can remove the new constant term.  Thus the seven displayed
normal directions form a genuine complement to a legal five-dimensional
gauge space.

### Global \(E_6\) compatibility and specialization safety

Both \(E_6\) systems have rank \(8\) with constant, nonzero pivot minors:

\[
4096\quad\text{and}\quad49152.
\]

Solving only on those constant pivots and reducing every remaining row
gives exactly

\[
Cw_3,\ Dw_5
\]

in the rank-two case and

\[
Dw_5,\ Cw_5+Dw_4
\]

in the rank-one case, up to nonzero rational factors.  Because the pivots
are constant, these are global residual identities; no parameter
specialization can create an omitted \(E_6\) rank-drop branch.

### Rank-two branches

The audit reconstructs polynomial \(E_5\) left syzygies forcing \(C^3=0\)
on both the \(D=0\) chart with arbitrary \(w_5\) and the \(w_5=0\) chart
with arbitrary \(D\).  The involution \(y\leftrightarrow z\) fixes
\(p=x^2\), \(q=yz\), and \(R=xyz\), and exchanges the \(C\)-only and
\(D\)-only branches.  This exhausts every branch with \(C\ne0\) or
\(D\ne0\).

On \(C=D=0\), the constant \(E_6\) pivot gives the stated complete solve.
The four literal \(E_5\) coefficients are independently recovered and
force

\[
\ell_{12}=\ell_{13}=0,\qquad
\ell_{22}=-w_4\ell_{32},\qquad
\ell_{23}=-w_4\ell_{33}.
\]

The reconstructed determinant then vanishes identically.

### Rank-one nonzero-normal branches

If \(D\ne0\), the \(E_6\) residuals force \(w_4=w_5=0\); a polynomial
\(E_5\) syzygy forces \(D^3=0\).

If \(D=0,C\ne0\), the residuals force \(w_5=0\).  A generic PARI left
kernel basis initially displayed a denominator \(C-w_4\).  Treating that
basis naively would leave the specialization \(w_4=C\) unaudited.  The
audit multiplies the two relevant vectors by \(C-w_4\), simplifies every
entry, and verifies the resulting polynomial identities directly:

\[
C f(C,w_4)=0,\qquad C g(C,w_4)=0.
\]

It then substitutes \(w_4=C\) into the cross-multiplied vectors and the
entire \(E_5\) system.  The two right-hand sides become respectively
\(2C^4\) and \(-6C^4\), so the resonance is excluded rather than lost.
The independently computed resultant is

\[
\operatorname{Res}_{w_4}(f,g)=-250C^9.
\]

Thus the division by \(C\) used in the branch argument is justified by
the branch hypothesis \(C\ne0\), while no division by \(C-w_4\) is used.

### Rank-one zero-normal branches

The audit rebuilds \(E_6\) and \(E_5\) separately on every leaf rather
than specializing a parameter-dependent pivot:

| leaf | exact \(E_5\) rank minor | conclusion |
|---|---:|---|
| \(w_4\ne0\) | \(768w_4^2\) | the four row relations in (13) |
| \(w_4=0,\ w_5\ne0\) | \(-4096w_5^2\) | the four row relations in (13) |
| \(w_4=w_5=0,\ d=0\) | \(64\) | the four row relations in (13) |
| \(w_4=w_5=0,\ d\ne0\) | \(-64d^2\) | the matrix form (14) |

Here \(d=w_2-w_3\).  These four leaves are exhaustive.  On the final leaf,
the audit independently obtains

\[
c_{x^4}=-\frac4d\,\ell_{32}
(\ell_{23}+w_3\ell_{33}),\qquad
c_{x^3z}=\frac1d\,\ell_{13}\ell_{32}.
\]

More strongly, it verifies the exact identity

\[
\det L
=\frac{d\ell_{11}}4c_{x^4}
+d(\ell_{21}+w_3\ell_{31})c_{x^3z}.
\]

Consequently \(E_4=0\) forces \(\det L=0\) without an omitted subcase.

## Scope and circularity audit

- The proof uses only explicit homogeneous Jacobian identities and exact
  linear algebra over characteristic zero.
- It does not assume the Jacobian Conjecture or inherit a result whose
  hypothesis includes it.
- It distinguishes the fixed-divisor \(e=2\) row from the genuine
  \(e=0\) line-\((2,2)\) packages.
- It proves a statement about the two normalized shapes, not about an
  arbitrary Keller counterexample before the preceding classification
  steps are invoked.
- No resultants from denominator clearing are used to construct a new
  branch; the only resultant is applied to two globally verified
  polynomial syzygies on \(C\ne0\).

## Conclusion

The parent theorem and its stated scope are fit for promotion from
“provisional” to “audited,” provided the parent artifact records this
independent backend.  No correction to the theorem statement or proof is
required.
