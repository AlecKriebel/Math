# Scope and denominator audit

## Frozen input

`INPUT_MANIFEST.sha256` pins:

- the immutable thirteen-stratum marked-companion taxonomy;
- its hostile-audit freeze certificate;
- the released exact SymPy and PARI normal-form certificates for the
  parameterized family and six endpoints.

The strict verifier fails closed if any pinned input changes.

## Legal normalizations

The \(E_7\) normal forms quotient only:

- invertible target shears by the third component; and
- affine source translations.

Both preserve the property that the Jacobian determinant is a nonzero
constant.  A source translation changes lower homogeneous pieces, but those
pieces remain completely arbitrary in the normal-form calculation.  If the
original Jacobian determinant is nonzero constant, the linear part at every
translated origin is invertible.  Thus deriving \(\det L=0\) after these
normalizations is a valid contradiction.

No nonlinear coordinate change or normalization of \(L\) is used.

## Parameter coverage

For finite \(k\ne0\), the released `CTAU` \(E_7\) rank proof uses pivots
whose nontrivial factors are
\[
q=9k^2+6k-1,\qquad r=3k-1.
\]
The exact recovery certificate is
\[
\frac12q-\frac32(k+1)r=1,\qquad
\operatorname{Res}_k(q,r)=18.
\]
Hence the charts cover every finite \(k\ne0\), including the roots of
either pivot factor and the `CT` point \(k=-1\).

The new \(E_6\) elimination is division-free except for the implication
\[
k^2\ell_7=k^2\ell_8=0\Longrightarrow \ell_7=\ell_8=0.
\]
Its only exceptional divisor is \(k=0\), already frozen separately as
`CH`.  The `CS` point is the separate \(k=\infty\) chart.  Both endpoints
are covered in `ENDPOINTS_NOTE.md`.

All endpoint \(E_6\) pivots are nonzero rational constants.  Their radical
components are handled without division by a normal parameter.

## Lower-term coverage

In every calculation:

- the first two components of \(H_2\) contain all twelve quadratic
  coefficients;
- the third component is exactly the complete released normal form;
- all nine entries of \(L\) remain variables;
- constants are omitted only because they do not affect the Jacobian.

The `CTAU` obstruction is independent of the surviving \(A,B,T\) and free
lower coefficients.  The endpoint calculation treats every component of
the released field-valued \(E_6\) radical.

## Adversarial sharpness check

The rank-one-pencil `CH` endpoint does **not** die at \(E_5\).  The explicit
map data in Section 5.3 of `ENDPOINTS_NOTE.md` have invertible \(L\) and
satisfy \(E_9,\ldots,E_5\).  The first failure is \(E_4\).

This witness is retained as a regression against any shortened proof that
silently discards the \(A=C=D=0,\ T\ne0\) component.

## Exact scope ledger

Certified by this directory:

- the parameterized `MD-P21-HSM-CTAU` stratum;
- its finite `CT` boundary;
- all six `CH/CS` endpoints.

Not certified here:

- the three `C0` strata;
- the two outer `CO` strata;
- any other internal or global quartic row.

Therefore this package alone does not close the parent row and does not
change the frozen global count of fourteen rows.
