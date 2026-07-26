# Hostile audit of the D4-DN-1CC exclusion

**Verdict:** pass; promote the family-level exclusion.

**Audit timestamp (UTC):** `2026-07-26T06:18:00Z`.

The normal form and the complete contact calculation were reconstructed
before the candidate `NOTE.md` or its two primary verifiers were read.  The
hostile verifier is separate and does not import either primary
implementation.  This work is not peer reviewed.

## Scope

The audited statement is:

> Every degree-four Keller map over an algebraically closed
> characteristic-zero field with canonical leading data in
> `D4-DN-1CC` is a polynomial automorphism.

This closes one isolated family in the high-incidence denominator.  It
does not close L07, the parent fixed-quadratic row, the quartic frontier,
or a program rung.

## Normal form and field

The frozen doubled-nonbranch point has the rational representative
\[
h=(p+q)^2,\qquad
R=(p+q)(2p^2+pq+2q^2),
\]
with \(P=hp^2\) and \(Q=hq^2\).  A diagonal binary source change
normalizes any nonbranch doubled line \(ap+bq\), \(ab\ne0\), to \(p+q\);
separate nonzero target scalings restore the coefficients of \(P,Q,R\).
The residual involution \(p\leftrightarrow q\) fixes both displayed forms.
No square root or field extension occurs in this orbit normalization.

The exact algebra is rational and therefore valid in characteristic zero.
For the final use of Moh over a general algebraically closed
characteristic-zero field, the finitely many coefficients lie in a
finitely generated subfield that embeds in \(\mathbb C\); the unique
polynomial inverse descends.  Restricting the statement to
\(\mathbb C\), the main program's normal base field, avoids even this
standard descent sentence.

## Independent full-contact calculation

The independent \(E_7\) calculation has syzygy nullities \(0,2,4\) in
degrees \(0,1,2\), so its displayed six coordinates are complete.
Throughout the hostile calculation the determinant retains:

- arbitrary binary cubic parts of the first two entries of \(H_3\);
- the arbitrary binary quadratic part of the third entry of \(H_2\);
- every quadratic coefficient of the first two entries of \(H_2\); and
- all nine entries of the linear part.

Thus the \(E_6\) equations form a \(28\times18\) linear system in the lower
coefficients that occur at that weight.

A global constant \(5\times5\) pivot has determinant \(2332800\).
Eliminating through it introduces no contact-dependent denominator.
Residual equations first force the two \(r^2\)-contact coordinates to
zero.  Four further residuals force three independent linear conditions
on the four \(r\)-contact coordinates.  Exact substitution proves both
necessity and sufficiency of the single line
\[
x_0=x_1=0,\qquad
(y_0,y_1,y_2,y_3)
=\left(\frac{2k}{3},\frac{2k}{3},-k,k\right).
\]
In polynomial form,
\[
U_r=-\frac23kp(p+q),\qquad
V_r=\frac23kq(p+q),\qquad
T_r=k(-p+q).
\]
This reconstructs the full projected contact locus, not a zero-binary or
sparse slice.

## Complete rank denominator

On the contact line the coefficient and augmented ranks agree:

| stable ID | chart | ranks | outcome |
|---|---|---|---|
| `DN1CC-C1-NZ` | \(k\ne0\) | \(6/6\) | excluded by \(E_4\) |
| `DN1CC-C1-Z` | \(k=0\) | \(5/5\) | binary exit |

A maximal rank-six minor is exactly \(-13996800k\).  Hence it is nonzero
at every point of the punctured line, and \(k=0\) is the only omitted
pivot.  The boundary was recomputed from the original equations; no
generic formula containing \(1/k\) was specialized there.

After a complete generic \(E_6\) solve, independent of every free lower
coefficient,
\[
[pr^3]E_4=[qr^3]E_4=\frac{16}{135}k^4.
\]
Therefore the whole \(k\ne0\) chart is empty.  No \(E_5\) specialization
can cancel a nonzero coefficient of the separate identity \(E_4=0\).

At \(k=0\), a fresh rank-five solve gives
\[
[p^3r]E_4=\frac2{135}(15b+2\lambda)^2,\qquad
[q^3r]E_4=\frac{10}{27}(3b-2\lambda)^2.
\]
These force \(b=\lambda=0\), and the complete \(E_6\) solution then forces
all six nonbinary quadratic coefficients to zero.  Since the contact
coordinates are also zero, every nonlinear homogeneous term depends only
on \(p,q\).

## Moh triangular exit

The primary exit is valid.  After subtracting \(F(0)\), the Keller
condition makes the linear part invertible.  A target-linear
postcomposition can send its \(r\)-column to \(e_3\), preserving binary
dependence of the nonlinear terms and giving
\[
(p,q,r)\longmapsto
\bigl(g_1(p,q),g_2(p,q),r+g_3(p,q)\bigr).
\]
The plane map \(\phi=(g_1,g_2)\) has constant nonzero Jacobian and degree
at most four.  Moh's unconditional theorem applies to plane Keller maps
of degree **strictly less than \(100\)**, so it applies here without any
assumption of the plane Jacobian Conjecture.  If \(\phi^{-1}\) is its
polynomial inverse, the threefold inverse is
\[
(u,v,w)\longmapsto
\left(\phi^{-1}(u,v),\
w-g_3(\phi^{-1}(u,v))\right).
\]

The candidate note already uses the correct “strictly less than \(100\)”
form and explicitly subtracts \(F(0)\).

## Exact replay

The primary package passes with

```text
D4_DN1CC_FAIL_CLOSED_STRICT_PASS
```

Run the separate hostile replay with:

```sh
./verify_hostile.sh
```

Its terminal marker is:

```text
D4_DN1CC_HOSTILE_AUDIT_STRICT_PASS
```

Assertions must remain enabled.  These scripts certify the encoded
algebra; they are evidence, not peer review.

## Disclosure

The reconstruction, audit, and verifier were produced with substantial AI
assistance.
