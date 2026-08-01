# Exact constrained first-level DTH pseudomoment

## Scope and logical correction

The original holomorphic five-replica proposal tried to impose both DTH
equations directly on the ket

\[
h=w\otimes w\otimes z.
\]

That formulation has a conjugation defect: the support equation contains
\(W^\dagger z\), so it cannot be represented by the proposed complex-linear
map on the holomorphic ket.  The correct relation is at density level.  Put

\[
m=\bar w\otimes w\otimes z,
\qquad
|m\rangle\langle m|
=
(|h\rangle\langle h|)^{\Gamma_1},
\]

where \(\Gamma_1\) transposes the first bivector slot.  The specified
\(\Gamma_1\)-PPT corrected first-level relaxation is

\[
\rho\succeq0,
\qquad
\rho^{\Gamma_1}\succeq0,
\qquad
\operatorname{ran}\rho\subseteq\mathscr K_{\rm hol},
\qquad
\mathcal C_{\rm supp}\rho^{\Gamma_1}=0.
\tag{1}
\]

Here \(\mathscr K_{\rm hol}\) contains pair symmetry, the first Plücker
equation, and the polarized Omega equation.  Rank-one feasible densities in
(1), when nonzero and up to positive scale, are exactly the physical DTH
monomials, but higher-rank feasible densities are only pseudomoments.

## Exact certificate candidate

The local-unitary invariant density is stored in 125 exact rational
holomorphic support charts

\[
H_{\lambda_1\lambda_2\lambda_3}
=E_{\lambda_1\lambda_2\lambda_3}
 A_{\lambda_1\lambda_2\lambda_3}
 E_{\lambda_1\lambda_2\lambda_3}^{\mathsf T}.
\tag{2}
\]

The total real symmetric chart dimension is 4139.  Starting from a strict
numerical point, every chart entry was rounded at denominator \(2^{100}\).
A literal exact 334 by 334 face-defect minor was then used to correct 334
coordinates over \(\mathbb Q\).  With the common integral scalings

\[
E\longmapsto360E,
\qquad
C_{\rm cross}\longmapsto14400C_{\rm cross},
\]

the correction matrix and right-hand side are integral.  The minor has rank
334 modulo both 1,000,003 and 1,000,033.  PARI exact linear algebra produced
a rational correction satisfying every selected equation identically.  The
largest coordinate change is

\[
4.34534\times10^{-16}.
\]

The canonical compact certificate is

```text
verification/certificates/dth_constrained_pseudomoment.json.gz
```

with SHA-256

```text
707e183995f1963aebe9eef732530396b2baa53421aaa9fcbf9f5cb31c36e9da
```

and size 163,447 bytes.  It uses deterministic canonical JSON, decimal-string
per-entry rationals, and gzip with timestamp zero.

## Exact verification

The following statements are exact:

1. the selected 334 rational face equations vanish identically;
2. the defect minor has rank 334 over each of two prime fields;
3. the trace is a positive rational;
4. the witness pairing is a negative rational;
5. all 118 nonzero holomorphic coordinate blocks are positive definite,
   with total reduced block dimension 768;
6. the crossed mixed moment lies in the exact 2266-dimensional physical
   product-DTH face; and
7. all 198 nonzero mixed face-coordinate blocks are positive definite.

Their decimal values are

\[
\operatorname{Tr}\rho
=0.999999999975263939564253583975\ldots,
\]

and

\[
\operatorname{Tr}(\widetilde{\mathcal O}_0\rho)
=-0.000452547029060465552919005860848\ldots.
\tag{3}
\]

After conceptual normalization by the positive trace, the pairing is

\[
-0.000452547029071659783580139927555\ldots.
\]

The full mixed-face statement in item 6 was checked without a rank tolerance.
After clearing the 1595-bit common coordinate denominator, all 826,573
primitive face equations were replayed modulo 85 deterministic primes.  The
resulting modulus has 1695 bits, while an explicit bound on every integer
residual has 1683 bits.  Vanishing modulo that modulus therefore implies
literal vanishing over the integers.

For item 7, the same CRT pass reconstructed all 64,900 pivot-principal
entries of the 216 mixed blocks.  Each nonzero coordinate matrix was scaled
by an exact power of two and compared with a 100-bit dyadic reference.  An
80-bit dyadic inverse-Cholesky proposal makes every reference strictly
diagonally dominant by exact congruence.  Exact Frobenius perturbation then
transfers positivity to the reconstructed rational matrix.  The worst
squared perturbation-to-certified-gap ratio is

\[
2.691975\times10^{-41}<1.
\]

As an independent hostile check, direct fraction-free Sylvester arithmetic
also proves positivity of the numerically hardest raw-coordinate block,
the \(42\times42\) block \((2,2,4)\); its final determinant has 108,888 bits.
The exact local crossing additionally satisfies the transpose intertwining
identity \(C T_{\rm hol}=T_{\rm mixed}C\), so symmetry of the mixed blocks is
not inferred from their pivot submatrices.

The mixed positivity reference certificate is

```text
verification/certificates/dth_mixed_pd_reference.json.gz
```

with SHA-256

```text
648186810cd9e9becc71eb6d319749c2a2c956d3f152f116ff17a1cdd1bcdf33
```

The independent floating audit, retained only as a diagnostic, found:

- smallest holomorphic chart eigenvalue
  \(1.392662703188779\times10^{-12}\), in block \((4,3,3)\);
- smallest mixed product-face chart eigenvalue
  \(3.3294526318695295\times10^{-8}\), in block \((1,1,3)\);
- maximum mixed face reconstruction residual
  \(2.24258\times10^{-13}\);
- total mixed reduced block dimension 2266.

## Theorem

> **Theorem.** The specified \(\Gamma_1\)-PPT corrected, five-replica DTH
> relaxation (1) contains a nonzero rational feasible density \(\rho\) with
> \(\operatorname{Tr}(\widetilde{\mathcal O}_0\rho)<0\).

Indeed, items 1, 5, and the support chart (2) prove
\(\rho\succeq0\) with the required holomorphic range.  Items 6 and 7 prove
\(\rho^{\Gamma_1}\succeq0\) and the corrected mixed support equation.
Items 3 and 4 permit normalization by the positive trace while preserving
the strict negative sign.

This is a certificate-degree obstruction.  It proves that the specified
first corrected Plücker/support/\(\Omega\) lift fails to certify DTH.  Any
proof staying within this architecture must strengthen it, for example with
the final-slot Segre/PPT localizer identified in the companion note or with a
higher prolongation.

It does **not** provide a rank-one density or a physical vector
\((w\otimes w)\otimes z\).  Therefore it is not a counterexample to DTH,
square-zero positivity, unrestricted three-copy Werner positivity, or the
all-copy Werner problem.

The deterministic entry point is

```text
python3 verification/verify_dth_constrained_pseudomoment.py
```

It rebuilds the exact support charts and crossing from the defining
permutation actions, checks the two artifact hashes, certifies the rational
signs and both PSD systems, and performs the bounded CRT face replay.
