# Paired high-mode Schur feedback at `r=3/2`

Date: 2026-08-08 (America/Los_Angeles)

Status: **EXACT ROUTE REFUTATION AND SHARPER EXACT REDUCTION**.

No literature search, outside contact, or floating-point sign assertion was
used.  The exact verifier is `verify_schur_feedback_exact.py`.

## 1. Exact block setup

Let `L_U` be the row generator of the continuous type-changing chain on the
transient mutant sets and put

\[
 A_U=-L_U^{\mathsf T}.
\]

Let \(\mathcal L\) be the direct sum, over ranks, of Johnson degrees zero,
one, and two, and let \(\mathcal H=\mathcal L^\perp\) in counting measure.
Write \(P,Q\) for the two orthogonal projections.  If the columns of `H`
are any basis of \(\mathcal H\), eliminating the high coordinates gives the
basis-independent low operator

\[
 A_{U,\mathrm{eff}}
 =P A_U P-\Sigma_U,
 \qquad
 \Sigma_U
 =P A_UH(H^{\mathsf T}A_UH)^{-1}H^{\mathsf T}A_UP.       \tag{1}
\]

Thus the degree-two observable is low, but its Green expectation is not a
degree-two process: it sees every higher Johnson mode through \(\Sigma_U\).

## 2. The canonical diagonal weight

For the complete graph, an up flip from a rank-\(k\) state and its reverse
down flip have the same ratio under both update rules:

\[
 {L_U(S,S+j)\over L_U(S+j,S)}={r k\over n-k-1}.
\]

The common reversible weight per state is therefore, up to scale,

\[
 \pi_k={r^{k-1}\over\binom{n-2}{k-1}}.
\]

Because the Green operator is the *transpose* operator \(A=-L^{\mathsf T}\),
the canonical adjoint diagonal is the inverse weight

\[
 D_k=\pi_k^{-1}=\binom{n-2}{k-1}r^{1-k}.               \tag{2}
\]

The verifier checks directly over `QQ` that

\[
 D A_U=A_U^{\mathsf T}D
\]

on `K_6` for both rules.  This orientation matters: using \(\pi\) rather
than \(\pi^{-1}\) would be the wrong adjoint for the occupation equation.

More generally, if two full operators obeyed

\[
 D A_B=A_D^{\mathsf T}D,                               \tag{3}
\]

then block elimination, using that the rank diagonal commutes with `P` and
`Q`, would give

\[
 D_{\mathcal L}\Sigma_B
   =\Sigma_D^{\mathsf T}D_{\mathcal L}.                \tag{4}
\]

This makes (4), or a one-sided Loewner version of it, the canonical paired
Schur conjecture to test.

## 3. Exact six-cycle refutation

Take the unweighted cycle `C_6`.  The high space has dimension five and is
supported entirely at rank three.  Put

\[
 \chi_{k,ij}(S)=\mathbf1\{|S|=k,\ i,j\in S\},
 \qquad q_U(f)=f^{\mathsf T}D\Sigma_U f .
\]

Direct exact elimination gives:

| witness \(f\) | \(q_B(f)\) | \(q_D(f)\) | paired value |
|---|---:|---:|---:|
| \(\chi_{4,04}-\chi_{4,13}\) | \(-64/25\) | \(-6848/3375\) | \(q_B+q_D=-15488/3375\) |
| \(\chi_{3,02}-\chi_{3,35}\) | \(32/3\) | \(128/15\) | \(q_B+q_D=96/5\) |
| \(\chi_{4,02}-\chi_{4,35}\) | \(-64/25\) | \(-6848/3375\) | \(q_B-q_D=-1792/3375\) |
| \(\chi_{3,04}-\chi_{3,13}\) | \(32/3\) | \(128/15\) | \(q_B-q_D=32/15\) |

Consequently:

1. the symmetric part of \(D(\Sigma_B+\Sigma_D)\) is indefinite;
2. the symmetric part of \(D(\Sigma_B-\Sigma_D)\) is indefinite;
3. the weighted-adjoint identity (4) is false;
4. the two corrections are not order-opposite: they have the **same**
   negative sign on the first witness and the **same** positive sign on the
   second.

This is an exact counterexample on a connected, regular, unweighted graph.
It rules out a graph-independent proof based only on adjointness or a
Loewner sign of the paired high-mode corrections.

## 4. Exact hostile-corpus screen

The same failure was checked over `QQ`, not merely sampled numerically, on
the frozen seven-vertex fake-Green witness and on two true hostile graphs.
The table gives exact quadratic values rounded only for display; the replay
prints a SHA-256 hash of each reduced rational.

| graph | \(q_B+q_D\), negative witness | \(q_B+q_D\), positive witness | \(q_B-q_D\), negative witness | \(q_B-q_D\), positive witness |
|---|---:|---:|---:|---:|
| degree-two fake-Green witness | -3.422972552 | 28.89031409 | -2.361134053 | 16.57318562 |
| exact dB-amplifying windmill | -40.71263375 | 117.2181772 | -3.862441481 | 18.50773236 |
| affine lower-multiplier witness | -44.42826137 | 127.1485915 | -3.718136497 | 19.98889299 |

The explicit rank-pair witnesses and all rational hashes are in the
verifier.  Thus the six-cycle failure is not a symmetry accident that
disappears on the endpoint-hostile mechanisms.

## 5. Exact scalar refutation: high feedback can help both rules

The operator counterexample alone does not decide whether the particular
source and fixation observable might still force opposite scalar effects.
That stronger hope is also false.

Let `X` be any basis of \(\mathcal L\), let \(\mu\) be the uniform-singleton
source, and let \(\ell_U\) be the top absorption flux divided by the
complete-graph fixation baseline.  Define the low-only Galerkin score

\[
 s_U^{(0)}
 =\ell_U^{\mathsf T}X
  (X^{\mathsf T}A_UX)^{-1}X^{\mathsf T}\mu,            \tag{5}
\]

and the true normalized score

\[
 s_U=\ell_U^{\mathsf T}A_U^{-1}\mu.                    \tag{6}
\]

On the exact seven-vertex dB-amplifying windmill, exact rational arithmetic
gives

| rule | low-only \(s_U^{(0)}\) | true \(s_U\) | \(\Delta_U=s_U-s_U^{(0)}\) |
|---|---:|---:|---:|
| Bd | 0.736005425738... | 0.750430142538... | **+0.0144247167995...** |
| dB | 0.984306556384... | 1.013848220752... | **+0.0295416643673...** |

Both signs are exact.  The hashes of the two reduced positive rationals are

```text
Bd  18746ccdf5e150a146e08e27c128061723f0ede0a22cf10224243c5ab1c5ec8a
dB  faa2b5fe7a6f81aea809e97b400b439f189cf47069b006254133b80d694dee76
```

In particular, the high feedback is what moves dB from a low-only value
below one to a true value above one, while it simultaneously improves Bd.
Therefore no theorem of the form “the higher Johnson modes cannot improve
both endpoint scores” is available.

## 6. The minimal remaining global sign

In low coordinates define

\[
 B_U=X^{\mathsf T}A_UX,
 \qquad
 C_U=X^{\mathsf T}A_UH(H^{\mathsf T}A_UH)^{-1}H^{\mathsf T}A_UX,
\]

\[
 b=X^{\mathsf T}\mu,
 \qquad c_U=X^{\mathsf T}\ell_U.
\]

Then the exact endpoint problem is

\[
 c_B^{\mathsf T}(B_B-C_B)^{-1}b
 +c_D^{\mathsf T}(B_D-C_D)^{-1}b\le 2.               \tag{7}
\]

The resolvent identity separates the feedback contribution:

\[
 s_U=s_U^{(0)}+\Delta_U,
 \qquad
 \Delta_U=
 c_U^{\mathsf T}(B_U-C_U)^{-1}C_UB_U^{-1}b.           \tag{8}
\]

The exact windmill calculation proves that neither \(\Delta_B\) nor
\(\Delta_D\), nor their joint sign, supplies the separator.  A surviving
global proof must instead couple the **low-mode deficit** to the fully
resolvent-dressed feedback:

\[
 \{1-s_B^{(0)}\}+\{1-s_D^{(0)}\}
 \;\ge\;\Delta_B+\Delta_D.                            \tag{9}
\]

Equation (9), equivalently (7), is the minimal open sign after this audit.
It is source-and-observable specific and cross-rule; every stronger
operator-order or separate-feedback sign tested here is exactly false.

## 7. Classification

- Canonical complete-graph Green adjoint weight: **PROVED**.
- Paired Schur weighted-adjoint identity: **EXACTLY FALSIFIED**.
- Loewner sign for the sum or difference of corrections: **EXACTLY
  FALSIFIED**.
- Claim that high feedback cannot improve both normalized scores:
  **EXACTLY FALSIFIED**.
- Endpoint separator (7)/(9): **OPEN**.

