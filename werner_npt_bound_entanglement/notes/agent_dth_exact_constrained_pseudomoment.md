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

where \(\Gamma_1\) transposes the first bivector slot.  The corrected
first-level relaxation is

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

Here \(\mathscr K_{\rm hol}\) contains pair symmetry, the first Pluecker
equation, and the polarized Omega equation.  Rank-one feasible densities in
(1) are exactly the physical DTH monomials, but higher-rank feasible
densities are only pseudomoments.

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

## Audits completed at reconstruction time

The following statements are exact:

1. the selected 334 rational face equations vanish identically;
2. the defect minor has rank 334 over each of two prime fields;
3. the trace is a positive rational;
4. the witness pairing is a negative rational.

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

The independent floating audit, used only as a diagnostic, found:

- smallest holomorphic chart eigenvalue
  \(1.392662703188779\times10^{-12}\), in block \((4,3,3)\);
- smallest mixed product-face chart eigenvalue
  \(3.3294526318695295\times10^{-8}\), in block \((1,1,3)\);
- maximum mixed face reconstruction residual
  \(2.24258\times10^{-13}\);
- total mixed face rank 2266.

The exact full-face crossing replay and exact mixed-chart positive-
definiteness audit are the remaining certificate checks at this checkpoint.
They must pass before (1)--(3) are promoted to the theorem below.

## The theorem certified after the remaining replay

If the exact full-face and mixed-positivity checks pass, the certificate
proves:

> **Theorem.** The corrected first-level, five-replica, density/PPT DTH
> relaxation (1) contains a nonzero rational feasible density \(\rho\) with
> \(\operatorname{Tr}(\widetilde{\mathcal O}_0\rho)<0\).

This is a certificate-degree obstruction.  It proves that the complete
first corrected Pluecker/DTH lift is insufficient and that an additional
Veronese--Segre relation or a higher prolongation is necessary.

It does **not** provide a rank-one density or a physical vector
\((w\otimes w)\otimes z\).  Therefore it is not a counterexample to DTH,
square-zero positivity, unrestricted three-copy Werner positivity, or the
all-copy Werner problem.

