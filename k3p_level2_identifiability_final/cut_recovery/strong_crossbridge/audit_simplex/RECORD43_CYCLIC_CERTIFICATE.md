# Target 127 / record 43: exact transported cyclic certificate

## Claim

For target direction 127 (record 43, ordered split `01|23`), the quartet K3P
Fourier flattening has rank strictly greater than four at every strict
principal-domain parameter point.

The proof is an exact transport of the target-174 cyclic eliminant, but the
transport has two essential features that are replayed rather than assumed:

1. every selected minor has an additional factor \(1-\lambda _0\); and
2. the ordered cross-minor indices are transposed.

## Exact division and transported variables

Rebuild target 127 from the frozen record-43 switching signatures.  In the
zero-character Fourier block, select the nine minors with row pair \((0,s)\)
and column pair \((0,t)\), where \(s,t\in\{C,G,T\}\).

First remove the greatest common monomial from each minor.  It is strictly
positive on \(\mathcal D_{3,+}\).  Exact sparse polynomial division then gives

\[
\text{reduced minor}=(1-\lambda _0)\,\text{quotient}
\]

with zero remainder in all nine cases.  Since \(0<\lambda _0<1\), the second
factor is also strictly positive and may be divided out without changing the
vanishing set.

Put

\[
p=\lambda _1,\qquad q=1-p,
\]

and let \(a_s,b_s,c_s,d_s\) denote the sector-\(s\) spectra of edge classes
1, 4, 8, and 9, respectively.  Define

\[
K_s=p a_s b_s+q c_s,
\qquad
L_s=p a_s+q b_s c_s.
\]

The three diagonal quotients are exactly

\[
F_s=b_s-d_s^2K_sL_s.
\]

For distinct \(s,t\), let \(r=s\mathbin\oplus t\) and define

\[
M_{st}=p b_s a_r+q b_t c_r,
\qquad
E_{st}=d_rM_{st}-d_sd_tK_sL_t.
\]

The minor whose row sector is \(s\) and column sector is \(t\) has quotient
\(E_{ts}\), not \(E_{st}\).  All six ordered coefficient dictionaries verify
this transposed action.

## Elimination

For each cyclic ordering of distinct \(r,s,t\), set

\[
C_r=d_r^2M_{st}M_{ts}-b_sb_t.
\]

Exact sparse expansion gives

\[
\begin{aligned}
C_r={}&E_{st}\,d_rM_{ts}
      +d_sd_tK_sL_t\,E_{ts}\\
    &-b_sF_t-b_tF_s+F_sF_t,
\end{aligned}
\]

and

\[
\boxed{
b_rC_r+b_sb_tF_r
=d_r^2pqa_rc_r
 (b_t-b_sb_r)(b_tb_r-b_s).
}
\]

Therefore, if the nine original minors vanished, all transported \(F_s\) and
\(E_{st}\) would vanish, so

\[
(b_t-b_sb_r)(b_tb_r-b_s)=0
\]

for every \(r\).  The prefactor \(d_r^2pqa_rc_r\) is strictly positive.
Hence

\[
b_r\in\left\{\frac{b_t}{b_s},\frac{b_s}{b_t}\right\}.
\]

Since \(0<b_s<1\), the numbers \(B_s=-\log b_s\) are positive and would obey

\[
B_r=|B_t-B_s| \qquad (r=C,G,T).
\]

For a maximal \(B_r\), the absolute difference of the other two positive
numbers is strictly smaller than \(B_r\), a contradiction.

## Flattening consequence

The conservation-supported flattening is the direct sum of four nonzero
\(4\times4\) Fourier blocks.  Total rank at most four would force each block
to have rank one and would therefore force the nine selected zero-block
minors to vanish.  The cyclic contradiction proves total rank greater than
four throughout the strict domain.

## Replay

From the project root run

```text
.venv/bin/python cut_recovery/strong_crossbridge/audit_simplex/verify_record43_cyclic_transport.py
```

The replay rebuilds the frozen descriptor and checks:

- three exact diagonal divisions and quotient formulas;
- six exact ordered cross divisions, including the index transpose;
- three eliminant ideal-membership identities;
- three cyclic factorizations; and
- nine rejected mutations, including omission and sign alteration of the
  \(1-\lambda _0\) factor, failure to transpose \(E\), wrong inheritance and
  edge roles, a wrong block and target, an omitted eliminant term, and a
  changed ratio-factor sign.
