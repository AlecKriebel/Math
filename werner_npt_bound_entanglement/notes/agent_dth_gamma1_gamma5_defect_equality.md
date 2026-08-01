# Exact finite-field equality of the two DTH defect spaces

## Result and scope

Let \(\mathscr S\) be the 4,139-dimensional rational space of real
symmetric coordinates in the exact holomorphic five-replica DTH charts.
There are two face-defect systems on \(\mathscr S\):

1. the first-bivector partial transpose \(\Gamma_1\), tested against the
   exact physical product-DTH face; and
2. the final-replica partial transpose \(\Gamma_5\), tested against the
   exact face
   \[
     K_5\cap\ker\mathcal D_5.
   \]

The exact verifier proves, for both

\[
 p=1{,}000{,}003,
 \qquad
 p=1{,}000{,}033,
\]

that the literal pulled-back defect matrices satisfy

\[
 \boxed{
 \operatorname{rank}_{\mathbb F_p}D_1
 =\operatorname{rank}_{\mathbb F_p}D_5
 =\operatorname{rank}_{\mathbb F_p}
   \begin{bmatrix}D_1\\D_5\end{bmatrix}
 =334.
 }
\tag{1}
\]

More strongly, if \(J\) is the already certified set of 334 source pivot
coordinates, the verifier forms

\[
 A_p=(D_5)_{:,J}(D_1)_{:,J}^{-1}
\]

and checks the complete entrywise identity

\[
 \boxed{D_5=A_pD_1}
 \qquad\text{on all 4,139 source coordinates.}
\tag{2}
\]

No floating-point arithmetic enters (1)--(2).  This is an exact theorem
over the two displayed finite fields.  It is strong independent evidence
for the rational row-space identity suggested by the numerical principal
angles, but it is not by itself a bounded-CRT proof of equality over
\(\mathbb Q\).  The primary rational obstruction does not rely on making
that stronger claim: its full \(\Gamma_5\) membership is separately proved
by an 85-prime residual-bound CRT replay.

## Canonical \(\Gamma_5\) equations

Only nineteen ordered final-slot Schur blocks have nonzero
\(\mathcal D_5\) defect.  Their exact pair/Pluecker support ranks sum to
253, their removed ranks sum to 21, and their face ranks sum to 232.

For one such block, write

\[
 E_{\rm pair}\in\mathbb Z^{n\times r},
 \qquad
 E_{\rm face}\in\mathbb Z^{n\times(r-\delta)}.
\]

The verifier chooses \(\delta\) exact interpolation rows spanning the
quotient of the pair support by the face and pairs each with the \(r\)
recorded support pivot columns.  This gives

\[
 \sum_{\text{19 blocks}}\delta r=339
\]

literal target equations.  After pullback to \(\mathscr S\), their rank is
334 at both primes.  Three internal skew relations reduce the 339 formal
equations to 336, and two additional directions vanish on the exact
holomorphic source, giving 334.
The deterministic equation-label SHA-256 is

```text
e7b6fd688c9f0033dae3852fd4bbdeb741c63da796bc4cb79648a3d54941e61b
```

## Exact construction

For each prime, the verifier independently rebuilds:

- all 125 rational holomorphic support charts, scaled integrally by 360;
- the exact \(\Gamma_1\) crossing with denominator 14,400;
- the exact \(\Gamma_5\) crossing from the final-slot restriction bridge;
- the 334 literal \(\Gamma_1\) interpolation equations;
- all 216 exact \(\Gamma_5\) face charts and the nineteen exact support
  charts; and
- every pullback coefficient in the 4,139 source coordinates.

The artifact hashes used in the replay are

```text
5ac03d9bd7b942d8e928921614d7b612f320063e869ff0d3c63d4323eaf5368f
  dth_defect_labels334.json.gz
6caf453f0043a2e7296b31e2f14bc90b01f38163b1d89ece39276ac625ded9aa
  dth_gamma5_face_integer_charts.json.gz
05ead1ec64ccb0e6858e2b65c7d6cbda08e3aee452783fcfcc88705ce23fa3a8
  dth_gamma5_defect_support_charts.json.gz
```

Run

```text
python3 verification/verify_dth_gamma1_gamma5_defect_equality.py
```

The test is auxiliary to the complete tripartition-PPT obstruction.  It is
not a physical DTH counterexample and has no direct implication for the
unrestricted three-copy or all-copy Werner questions.
