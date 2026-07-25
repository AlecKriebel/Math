# Hostile audit: unmarked finite resonance \(c^2=9\)

**Verdict:** **PASS**.

**Audited:** 2026-07-25T09:55:40Z.

This audit is intentionally independent of the package verifier.  It rebuilds
the weighted Jacobian determinant in PARI/GP with a hand-written \(3\times3\)
determinant, reverses the monomial and raw-variable orders, and treats every
compatibility assertion as a polynomial identity before using any computed
left kernel.

The audit targets the exact theorem in the parent directory:
\[
H_4=((p-q)^2,(p+q)^2,0),\qquad
(H_3)_3=x(p-3q),\qquad p=x^2,\ q=y^2+xz.
\]
It does not audit the exhaustiveness of the surrounding leading-orbit
taxonomy.

## Audit result

No missing specialization, illegal division, or counterexample was found.
The theorem in the parent directory survives the hostile audit.

### Raw orbit and gauge

The audit rebuilt \(E_7\) from the full determinant.  Its coefficient matrix
has rank \(14\) and nullity \(12\).  The four gauge vectors and eight normal
vectors lie in the kernel and have joint rank \(12\), so they span the
complete kernel.  A coordinate minor on the four gauge vectors is a nonzero
integer.  Thus the normal form does not divide by a leading-form parameter.

The two \(R\)-directions are legal target shears.  The other two gauge
directions are source-translation jets.  The audit uses a different gauge
order, raw-variable order, and monomial order from the primary checker.

### \(E_6\) specialization chart

The following ranks were recomputed over the fraction field of the
parameters remaining in each row.

| imposed locus | coefficient rank | augmented rank before next condition |
|---|---:|---:|
| none | 8 | 9 |
| \(g=0\) | 8 | 9 |
| \(g=f=0\) | 8 | 9 |
| \(g=f=0,\ D=-2e\) | 8 | 9 |
| \(g=f=C=0,\ D=-2e\) | 8 | 8 |

More strongly, the same \(8\times8\) coefficient minor is the constant
\(5159780352\) at every row of the chart.  Hence no special values of
\(A,B,e,w\), or of the preceding compatibility parameters, create a hidden
coefficient-rank drop.

The successive obstructions were independently recovered as the literal
polynomial identities
\[
192g^2,\qquad 144f^2,\qquad -48(D+2e)^2,\qquad 24C^2.
\]
These use coefficient vectors with entries \(0,\pm1,\pm2\), not rational
left-kernel pivots.  In addition, the checker computed the full left kernel
at all five stages, multiplied out every rational-function denominator, and
verified that every cleared vector remains a polynomial left syzygy with a
polynomial pairing.  Thus denominator clearing introduces no component and
is not needed by the proof.

On the final locus, direct substitution verifies the displayed
six-parameter \(E_6\) solution.  The constant minor proves it is complete.

### Complete \(E_5\)-\(E_4\) branch cover

Put
\[
S=-6A+3B+48e+16w.
\]
The three column-two equations have determinant \(-96S\).

- If \(S\ne0\), their rank is three and
  \(\ell_{12}=\ell_{22}=\ell_{32}=0\); hence the second column of \(L\)
  vanishes.
- If \(S=0\), a constant \(2\times2\) minor equal to \(72\) makes their rank
  exactly two for every parameter value.  On the subbranch
  \(\ell_{32}=0\), two numeric pivots force
  \(\ell_{12}=\ell_{22}=0\), again making \(\det L=0\).
- If \(S=0\) and \(\ell_{32}\ne0\), the full resonant \(E_5\) system has a
  constant \(4\times4\) minor \(20736\).  Its verified solution has no
  parameter denominator.  The literal \(E_4\) coefficient
  \[
  \frac{16}{3}\ell_{32}(3e^2-\ell_{33})
  \]
  first forces \(\ell_{33}=3e^2\), and the next literal coefficient is
  \[
  \frac{16}{3}\ell_{32}^2,
  \]
  contradicting \(\ell_{32}\ne0\).

These cases exhaust \(S=0\) versus \(S\ne0\), and then
\(\ell_{32}=0\) versus \(\ell_{32}\ne0\).  No determinant-compatible branch
remains.

### The two signs

The checker verifies exactly that
\[
(x,y,z)\longmapsto(x,iy,-z)
\]
fixes \(p\), negates \(q\), swaps \((p-q)^2\) with \((p+q)^2\), and sends
\(x(p-3q)\) to \(x(p+3q)\), as well as conversely.  The source determinant
is \(-i\), the first-two-target swap has determinant \(-1\), and their
product is \(i\ne0\).  Thus the equivalence preserves the Keller property
and really covers both \(c=3\) and \(c=-3\) over \(\mathbb C\).

## Execution and fail-closed behavior

The commands

```text
./verify_hostile_pari_strict.sh
./test_fail_closed.sh
```

returned, respectively,

```text
ALL HOSTILE UNMARKED c^2=9 PARI AUDIT CHECKS PASSED
```

and

```text
PASS: corrupted final E4 pivot rejected
PASS: corrupted c=-3 symmetry rejected
PASS: corrupted resonance divisor rejected
PASS: strict hostile baseline accepted
PASS: strict wrapper rejected a forged extra line
ALL HOSTILE UNMARKED c^2=9 FAIL-CLOSED TESTS PASSED
```

Afterward, both primary exact checkers were rerun and passed unchanged.

## Scope and independence

This PASS is only for the exact joint orbit stated above.  It does not prove
that the surrounding orbit taxonomy is exhaustive, and it does not promote
the statement to all degree-four Keller maps.

The hostile script is an independent implementation inside PARI/GP: it uses
a hand-written determinant and reversed coefficient orders, rather than
calling or importing the parent scripts.  PARI/GP and the primary SymPy
checker are distinct exact-algebra backends.  They nevertheless encode the
same mathematical reduction, so this is evidence about the encoded algebra,
not peer review.

No claim in this report is peer reviewed.  Exact algebra checks evidence the
encoded identities only.
