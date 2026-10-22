# Acceptance of the established Rubel planar equilibrium resolution

## Decision

Accept the exact prior resolution of problem 2307078 / AMR-022-7078, corresponding to Hayman and Lingham Problem 7.78. No mathematical correction to the reviewed argument is required. This is an established result, not a novel resolution of an open problem.

## Accepted theorem

For every infinite sequence \((z_n)_{n\geq1}\) of pairwise distinct nonzero complex numbers satisfying

\[
\sum_{n\geq1}|z_n|^{-1}<\infty,
\]

the meromorphic function

\[
S(z)=\sum_{n\geq1}(z-z_n)^{-1}
\]

has simple residue-one poles exactly at the charge locations and infinitely many distinct zeros elsewhere. Consequently, a zero-free sum under the original assumptions does not exist.

## Basis for acceptance

The complete argument in [PROOF.md](PROOF.md) and the mathematical audit in [AUDIT.md](AUDIT.md) retain all assumptions. Normal convergence defines the field and the genus-zero canonical product \(F(z)=\prod_n(1-z/z_n)\). The product has exactly the charge locations as simple zeros and satisfies \(F'/F=S\) off those zeros.

A finite-head and summable-tail estimate proves \(\log M_F(r)=o(r)\); Cauchy's unit-circle estimate gives the needed bound for \(F'\). The finite-zero lemma is proved directly: after division by the polynomial recording a finite zero set, an entire logarithm exists, and a one-sided harmonic Fourier-coefficient estimate forces that logarithm to be constant. No factorization theorem is assumed.

If \(F'\) had only finitely many distinct zeros, the lemma would force both \(F'\) and \(F\) to be polynomials, contradicting the infinite zero set of \(F\). Simplicity of the product zeros separates every derivative zero from the poles of \(S\). The normalized potential \(U=\sum_n\log|1-z/z_n|=\log|F|\) has \(U_x-iU_y=S\), so these zeros are precisely its planar equilibrium points.

## Prior attribution

Clunie, Eremenko and Rossi state the distinct-point unit-charge case on printed p. 310, immediately before Theorem 2.1, in their [1993 journal paper](https://www.math.purdue.edu/~eremenko/dvi/cer.pdf), DOI [10.1112/jlms/s2-47.2.309](https://doi.org/10.1112/jlms/s2-47.2.309). [Hayman and Lingham's 2018 version 2](https://arxiv.org/abs/1809.07200v2), Update 7.78 on printed p. 186, already credits the planar resolution.

## Verification and limits

Public source identities and inspected locations are recorded in [SOURCE_PINS.json](SOURCE_PINS.json). The underlying input, authored-artifact, and sealed-artifact pins match. The existing integrity checks pass under normal Python, `-O`, and `-OO`, with deliberate one-byte alteration and truncation rejected in every mode. Public packet checks also bind the complete proof, protected audit text, editorial changes, and closed file inventory.

These checks establish document identity and the reported review outcome, not computer-assisted theorem verification. Acceptance is restricted to the stated unit-charge planar case. This report makes no claim about arbitrary positive real charges, higher-dimensional Newtonian potentials, or their current status.
