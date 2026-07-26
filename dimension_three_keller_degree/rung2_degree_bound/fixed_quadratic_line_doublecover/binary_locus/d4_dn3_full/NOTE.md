# D4-DN-3: bounded scope audit

First banked: `2026-07-26T04:02:00Z`.

## Outcome

The requested complete \(E_7/E_6\) contact denominator is **not certified**.
The earlier apparent two-plane denominator is only the slice obtained by
setting eleven arbitrary binary lower coefficients to zero.  All eleven
coefficients occur in the full \(E_6\) equations.  Consequently this package
does not close D4-DN-3, L07, the frozen quartic row, or any rung.

This scope failure was found by rebuilding the determinant for
\[
 h=(p+q)^2,\qquad R=(p+q)^3,\qquad
 H_4=(hp^2,hq^2,0)
\]
while retaining arbitrary binary cubic terms in the first two entries of
\(H_3\), an arbitrary binary quadratic term in the third entry of \(H_2\),
arbitrary quadratic terms in the first two entries of \(H_2\), and all nine
entries of the linear part.

## What is exactly certified

Use the exact \(E_7\)-syzygy bases
\[
\begin{aligned}
S_1&=\langle(-p,q,0),(4p/3,0,1)\rangle,\\
S_2&=\langle(-p^2,pq,0),(-pq,q^2,0),
              (4p^2/3,0,p),(4pq/3,0,q)\rangle.
\end{aligned}
\]
Write \(x_0,x_1\) for the \(S_1\) coordinates and \(y_0,\ldots,y_3\)
for the \(S_2\) coordinates.

The full \(E_6\) system is a \(28\times18\) linear system in seven
nonbinary/lower-linear coefficients and the eleven binary coefficients
\[
u_0,\ldots,u_3,\quad v_0,\ldots,v_3,\quad t_0,t_1,t_2.
\]
The verifier asserts that every one of these eleven coefficients occurs.
At the exact contact point \((1,2,3,4,5,6)\), the coefficient and augmented
ranks are \(9\) and \(10\); at \((0,0,1,1,0,0)\), both are \(6\).
Thus consistency is genuinely parameter-dependent.

Only after imposing
\[
u_i=v_i=t_j=0
\]
does exact elimination give the restricted radical
\[
\left(
x_0,x_1,\ y_2-y_3,\
9(y_0-y_1)^2+24(y_0-y_1)y_3+8y_3^2
\right).
\]
Over \(\mathbb Q(\sqrt2)\), that **slice** is two planes meeting in one
line.  The verifier proves the radical equality in both directions and
checks squarefreeness.

Stable slice-only IDs are:

| ID | Restricted locus | Status |
|---|---|---|
| `DN3-ZB-PPLUS` | plus plane minus the common line | slice only |
| `DN3-ZB-PMINUS` | minus plane minus the common line | slice only |
| `DN3-ZB-LINE` | punctured common line | prior complete \(E_4\) descent forces \(\det L=0\) |
| `DN3-ZB-ORIGIN` | origin | open |

These are not asserted to be components of the full contact variety.

## Open denominator

The full contact component count is unknown.  A correct continuation must
eliminate all 18 lower variables in the parameter-dependent \(E_6\) system
and certify every rank chart.  The previous generic transverse-plane solves
cannot supply that completeness proof.  At the demanded all-lower-equation
scope, only the prior punctured-line calculation currently forces
\(\det L=0\); the origin and every possible full transverse component remain
open.

## Reproduction

Run:

```sh
./verify_strict.sh
```

The terminal markers are:

```text
D4_DN3_BOUNDED_SCOPE_AUDIT_STRICT_PASS
D4_DN3_FULL_AUDIT_BOUNDED_PASS
```

Assertions must remain enabled.  The checks certify the algebra encoded by
the script; they are not peer review.

## Disclosure

The derivation and verification code were produced with AI assistance.  This
work is not peer reviewed.
