# The complete tripartition-PPT strengthening of the DTH lift

## Result

Write the five-replica monomial space as

\[
\mathcal A\otimes\mathcal B\otimes\mathcal C
=
(\wedge^2\mathcal H)_{12}
\otimes(\wedge^2\mathcal H)_{34}
\otimes\mathcal H_5.
\]

The physical ket is

\[
h(w,z)=w_{12}\otimes w_{34}\otimes z_5,
\]

with the same bivector in the first two factors.  The holomorphic support
therefore lies in the positive eigenspace of the real pair-exchange operator
\(S_{\mathcal A\mathcal B}\).

Let \(\Gamma_{\mathcal A},\Gamma_{\mathcal B},\Gamma_{\mathcal C}\)
denote transpose on these three factors.  For every operator \(R\), direct
calculation on matrix units gives

\[
S_{\mathcal A\mathcal B}R^{\Gamma_{\mathcal A}}
S_{\mathcal A\mathcal B}
=
(S_{\mathcal A\mathcal B}RS_{\mathcal A\mathcal B})
^{\Gamma_{\mathcal B}}.
\tag{1}
\]

Hence a pair-exchange-invariant density is PPT under
\(\Gamma_{\mathcal A}\) if and only if it is PPT under
\(\Gamma_{\mathcal B}\).

Let \(T\) be full transpose.  The other exact identity is

\[
R^{\Gamma_{\mathcal A}\Gamma_{\mathcal B}}
=T(R^{\Gamma_{\mathcal C}}).
\tag{2}
\]

Full transpose preserves positive semidefiniteness.  Its two cyclic analogues
show that complementary partial transposes have the same positivity status.
Consequently, on the pair-symmetric DTH moment space,

\[
\boxed{
R\succeq0,\quad
R^{\Gamma_{\mathcal A}}\succeq0,\quad
R^{\Gamma_{\mathcal C}}\succeq0
}
\tag{3}
\]

imply positivity under every one-factor, two-factor, and three-factor partial
transpose.  In replica notation these are precisely the existing
\(\Gamma_1\) condition (transpose of replicas 1 and 2 together) and the new
\(\Gamma_5\) condition.  Thus adding \(\Gamma_5\)-PPT completes all PPT cuts
of the physical tripartition \((w):(w):(z)\); there is no third independent
PPT cut to add.

This does **not** impose separability or the missing rank-one
Veronese--Segre equations.  Positivity of the resulting relaxation would be
a certificate for DTH, while a negative point would be a stronger
pseudomoment obstruction rather than a physical counterexample.

## Exact final-slot crossing census

Partial transpose of the final replica changes each local five-qutrit module
from five covariant slots to four covariant and one contravariant slot.  A
direct exact highest-weight calculation gives

\[
3^{\otimes4}\otimes\bar3
\cong
V_{00}^{\oplus3}
\oplus V_{03}^{\oplus2}
\oplus V_{11}^{\oplus8}
\oplus V_{22}^{\oplus3}
\oplus V_{30}^{\oplus4}
\oplus V_{41}.
\tag{4}
\]

The corresponding carrier dimensions are

\[
1,\ 10,\ 8,\ 27,\ 10,\ 35.
\]

Both exact checks close:

\[
3(1)+2(10)+8(8)+3(27)+4(10)+1(35)=243,
\]

and the invariant local commutant dimension is

\[
3^2+2^2+8^2+3^2+4^2+1^2=103.
\]

Therefore the final-slot partial transpose is represented by another exact
\(103\times103\) local crossing.  Globally it produces \(6^3=216\) PSD
blocks, with total reduced block dimension

\[
(3+2+8+3+4+1)^3=21^3=9261
\]

and maximum block size \(8^3=512\).

The dependency-free exact verifier is

```text
python3 verification/verify_dth_gamma5_census.py
```

It computes all raising-map ranks over \(\mathbb Q\), verifies (4), and
audits (1)--(2) on every matrix unit of a small generic tripartite model.
