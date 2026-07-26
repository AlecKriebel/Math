# Research log — D4-DN-2C full descent

All timestamps are UTC.

## 2026-07-26T05:49:00Z

Started from the frozen four-chart \(E_6\) atlas.  Retained all free lower
coefficients after each chart pivot.

## 2026-07-26T05:56:00Z

Found two pure \(E_5,r^2\) coefficients on each transverse plane.  Their
quadratic factors have an exact univariate Bézout identity after \(k\ne0\);
the \(k=0\) chart is separately nonzero.  Both plane interiors are excluded.

## 2026-07-26T06:05:00Z

On the punctured intersection, the \(E_5\) equations reduce exactly to the
ideal \(\langle\mathcal Q,\mathcal A\mathcal B\rangle\).  The safe pivots
are \(-64k^3/9\) and \(-32k^3\).

## 2026-07-26T06:14:00Z

\(E_4\) forces \(\mathcal S=0\), after which
\(\mathcal Q=\mathcal D^2\).  The \(\mathcal B\)-branch closes by a
determinant factor except on the already-listed \(\mathcal A=0\) boundary.

## 2026-07-26T06:20:00Z

The surviving \(\mathcal A\)-branch initially appeared to be a possible
construction target.  At \(E_3\), however, localization away from the
displayed determinant factor has pivot \(k^2\mathcal F_A^2/144\), while the
remaining equations equal \(k\mathcal F_A^2/288\).  This closes the entire
punctured intersection without an unrecorded pivot boundary.

## 2026-07-26T06:23:00Z

At the origin, two exact \(E_4\) squares force
\(b_{qr}=\ell_8=0\).  All six nonbinary quadratic coefficients collapse
literally.  The remaining map reduces by linear target normalization to a
degree-at-most-four plane Keller map and a triangular coordinate; Moh's
unconditional bounded-degree theorem gives the automorphism exit.

## 2026-07-26T06:30:02Z

The complete exact verifier passed with markers for the transverse planes,
punctured intersection, and origin.  Began strict mutation and priority
packaging.  No claim beyond the single frozen family is authorized.

## 2026-07-26T06:36:40Z

The aggregate strict wrapper passed.  Both required-failure mutations were
rejected, optimized Python was rejected, and the terminal marker was
`D4_DN2C_FULL_DESCENT_STRICT_PASS`.

## 2026-07-26T06:44:11Z

After hostile review, restricted the stated theorem to \(\mathbb C\), fixed
four malformed alignment rows in the displayed determinant factors, and
replaced tautological quotient checks by exact polynomial-normalization
assertions:
\[
\det L=-\mathcal F_B\mathcal H_B/216,\qquad
\det L=\mathcal F_A\mathcal H_A/1152,
\]
with denominator-one checks on both \(\mathcal H\)'s.  The aggregate wrapper
now also invokes the independent direct PARI/GP lower descent and adjugate
check.  The fully corrected aggregate rerun ended with both
`D4_DN2C_DIRECT_PARI_LOWER_STRICT_PASS` and
`D4_DN2C_FULL_DESCENT_STRICT_PASS`.

## 2026-07-26T07:29:16Z

The method-independence gap is closed.  The source PARI package now derives
the full contact atlas from raw top forms, including all 18 lower variables,
and ends with `D4_DN2C_DIRECT_PARI_FULL_FAMILY_STRICT_PASS`.  A separate
hostile wrapper added a second PARI contact reconstruction, checked every
scope and formula repair, rejected scope/contact mutations, and ended with
`D4_DN2C_FULL_EXCLUSION_HOSTILE_AUDIT_STRICT_PASS`.  The single-family
theorem is promoted.
