# Hostile audit report: rank-two \(e=2\) triple companion

## Verdict

**PASS**, as of 2026-07-25T09:42:15Z, after three
specialization-unsafe steps in the provisional proof were repaired.

The theorem in the parent `NOTE.md` survives an independent exact PARI/GP
reconstruction.  No counter-specialization remains in the audited normal
form.  This is not peer review.  It is an adversarial algebra audit of the
encoded homogeneous Jacobian identities.

## Independent backend

`verify_ranktwo_triple_pari.gp` constructs the monomial bases, Jacobians,
weighted determinant, coefficient matrices, fixed minors, kernel
directions, left syzygies, resultants, localized solves, fresh
specializations, and determinant exits directly in PARI/GP.  It imports
neither SymPy output nor serialized matrices.

Run:

```sh
./verify_ranktwo_triple_pari_strict.sh
./test_fail_closed.sh
```

The strict runner uses the fixed PARI executable
`/opt/homebrew/bin/gp`, rejects PARI diagnostics, and requires eleven
unique progress and terminal markers.  The injection test confirms that
it rejects both a corrupted raw-\(E_7\) maximal minor and a successful
PARI run with its terminal attestation removed.

## Raw \(E_7\), gauges, and normal completeness

The independently reconstructed raw matrix is \(36\times26\), has rank
\(8\), and has the fixed nonzero maximal minor
\[
236196.
\]
Thus its nullity is \(18\).  The displayed eighteen kernel directions
have an independent minor \(256/27\), so they span the full kernel.

The first five directions are genuinely legal and independent:

- two target shears add the third cubic component \(R=x^3\) to the first
  or second component without changing \(H_4\);
- the three source translations contribute
  \((\partial_vP,\partial_vQ,\partial_vR)\) at degrees \((3,3,2)\),
  for \(v=x,y,z\).

Their rank is exactly five, not four.  Together with the thirteen normal
directions they form a direct sum of dimension eighteen.  The remaining
changes caused by finite translations and target shears occur in lower
terms, which are arbitrary in the theorem.

## Global \(E_6\) split

The \(E_6\) system has rank \(4\) with the constant maximal minor \(324\).
Solving only on that constant pivot gives global, specialization-safe
residual equations.  Two are nonzero multiples of \(w_3^2,w_5^2\).
After setting \(w_3=w_5=0\), the remaining four are exactly
\[
KB_4,\quad KB_5+Mw_1,\quad KB_6+Mw_2,\quad KB_7,
\]
up to nonzero rational factors, where
\[
K=9A-12w_4,\qquad M=-3A+8w_4.
\]

## The \(K\ne0\) branch

On \(K\ne0\), the audit independently recovers all six nonzero \(E_5\)
compatibility equations used in the proof.  Eliminating \(B_1\), and
symmetrically \(B_3\), gives
\[
\operatorname{Res}_{B_1}
\bigl(3B_1K+4w_1^2,\,-B_1S+4Kw_1^2\bigr)
=4w_1^2(81A^2-27AK+5K^2),
\]
with \(S=(9A-2K)(9A-K)\).  On the three alternatives forced by the
third compatibility equation, the last quadratic equals respectively
\(5K^2,3K^2,3K^2\).  Hence \(w_1=w_2=0\).

For the aligned form, the fixed \(E_5\) pivot is
\[
-\frac49(3A-8w_4)^2(3A-4w_4)^4.
\]
This both validates the \(S\ne0\) aligned solve and exposes the first
rank drop below.

### The two \(S=0\) resonances

At \(9A=2K\), the nonzero-end solve has pivot
\(-81B_3A^3/2\), and
\[
[z^4]E_4=\frac38A^2B_3^2.
\]
The \(y/z\) involution covers a nonzero \(B_1\).  When
\(B_1=B_3=0\), the generic aligned pivot vanishes.  A fresh solve has
\(E_5\)-rank \(4\) and pivot \(81A^4/4\).  It gives the two squares
\[
-\frac43\ell_{32}^2,\qquad \frac43\ell_{33}^2,
\]
followed by two rows whose elimination is
\[
\frac32A(\ell_{12}\ell_{23}-\ell_{13}\ell_{22})=0.
\]
Thus this formerly omitted aligned resonance also forces
\(\det L=0\).

At \(9A=K\), the \(B_3\ne0\) solve has pivot \(324B_3A^5\).
The reconstructed \(E_4\) pair forces the same \(2\times2\) minor to
vanish.  A \(B_1\)-only end is equivalent by \(y/z\), and the zero pair
is the valid aligned leaf because both aligned pivot factors equal
\(3A\ne0\).

## The \(K=0,\ A\ne0\) branch

Six independently reconstructed \(E_5\) compatibility equations are
nonzero multiples of
\[
A^2B_1,\ A^2B_3,\ A^2B_4,\ A^2B_5,\ A^2B_6,\ A^2B_7.
\]
The remaining aligned form has a fresh \(E_5\) pivot \(9A^2\) and zeros
\(\ell_{12},\ell_{13},\ell_{32},\ell_{33}\).

## The \(K=A=0\) branch

After cross-multiplying the PARI left-kernel vectors and checking that
their entries are polynomial, the audit obtains the three global
syzygies that give
\[
B_5=3B_4r+\frac23s,\qquad
B_6=3B_4r^2+\frac23rs,\qquad
B_7=B_4r^3
\]
when \(w_1=s\ne0,\ w_2=rs\).

On \(B_4rs\ne0\), a complete solve uses the exact pivot
\[
384B_4r^2s^3
\]
and gives \([y^4]E_4=4s^4/27\).

The complementary charts are exhaustive:

- \(B_4=0\): a polynomial, division-free left syzygy has right side
  \(-4s^3/9\);
- \(B_4\ne0,\ r=0,\ B_3\ne0\): the explicit pivot is
  \(-96B_3s^2\), and cross-multiplication gives the polynomial
  obstruction \(-4B_3s^3/9\);
- \(B_4\ne0,\ r=0,\ B_3=0\): a fresh \(E_5\) system has rank \(4\),
  pivot \(144B_4s^2\), no compatibility obstruction, and then the
  literal coefficient \([y^4]E_4=4s^4/27\).

The \(y/z\) involution fixes \(P,Q,R\) and justifies choosing \(w_1\ne0\)
when \((w_1,w_2)\ne(0,0)\).

## Terminal \(w_1=w_2=0\) chart

A generic rank-three \(E_5\) solve has a pivot \(54B_1\) and therefore
cannot be specialized globally.  The repaired argument instead uses
literal rows.  Globally,
\[
[x^4y]E_5=3\ell_{12},\qquad [x^4z]E_5=-3\ell_{13},
\]
and the six other rows are
\[
-6B_1a_4,\ 6B_3a_4,\ -9B_4a_4,\ -3B_5a_4,\
3B_6a_4,\ 9B_7a_4.
\]
If \(a_4=0\), two \(E_4\) squares kill
\(\ell_{32},\ell_{33}\).  If \(a_4\ne0\), the six product rows leave
only \(V=B_2xyz\), and the fresh \(E_4\) rows
\[
2a_4\ell_{32},\qquad -2a_4\ell_{33}
\]
kill the same entries.  Together with
\(\ell_{12}=\ell_{13}=0\), this makes \(\det L=0\) on every terminal
specialization.

## Repairs forced by the hostile audit

The provisional proof initially contained three unsafe generic
specializations:

1. the aligned solve at \(9A=2K,\ B_1=B_3=0\);
2. the \(r=0,\ B_3=0\) tail chart;
3. the terminal \(B_1=0\) chart.

Each was detected from an exact vanishing pivot, repaired by a fresh
branch calculation, encoded in the primary SymPy verifier, and then
rechecked independently in PARI/GP.  The current parent `NOTE.md` and
primary verifier include all three repairs.

## Scope and circularity

- The result excludes only the normalized shape
  \(H_4=(x^4,x^2yz,0)\), \((H_3)_3=x^3\).
- It does not by itself classify every quartic Keller map or address the
  rank-one pencil \(\langle x^2,y^2+xz\rangle\).
- The proof uses explicit homogeneous Jacobian identities and exact
  algebra over a characteristic-zero field.
- It does not assume the Jacobian Conjecture or inherit a result whose
  hypothesis includes it.
