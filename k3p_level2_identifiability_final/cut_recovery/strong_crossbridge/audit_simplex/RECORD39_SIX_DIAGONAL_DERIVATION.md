# Exact reduction of the record-39 six-diagonal system

This note concerns target direction 117 (record 39), normalized to the split
`01|23`.  It analyzes only the six principal 2x2 minors of the
zero-character Fourier block.  It does not replace the full 144-minor rank-one
condition.

## Core zero-block matrix

For a zero-block coordinate `(i,i,j,j)`, edges 3, 5, 7, and 10 contribute
strictly positive separable row/column factors.  Remove those factors and name
the remaining edge spectra

```text
P=edge0, X=edge1, Q=edge2, A=edge4,
B=edge6, Y=edge8, R=edge9.
```

Let `u=lambda0`, `l=lambda1`, and let every spectrum have character-zero
coordinate one.  If `k=i xor j`, the reduced block entry is

```text
C_ij = (1-u)(1-l) Q_i A_j B_j Y_j
     + (1-u)l     X_j Q_i B_j
     + u(1-l)     P_i A_k B_k Y_j R_i
     + ul          P_i X_k B_k Y_i R_i.
```

For each nonzero sector `s`, define

```text
p_s = l B_s X_s,
q_s = (1-l) B_s A_s,
V_s = p_s + q_s Y_s,
W_s = q_s + p_s Y_s,
S_s = (1-u)Q_s + u P_s R_s W_s.
```

Then

```text
C_00 = 1,
C_0s = V_s,
C_s0 = S_s,
C_ss = (1-u)Q_s V_s + u P_s R_s Y_s.
```

Consequently the three within-sector principal minors are

```text
F_s = C_00 C_ss - C_0s C_s0
    = u P_s R_s (Y_s - V_s W_s).
```

All factors outside the final parenthesis are strictly positive.  Thus
`F_s=0` is exactly `Y_s=V_s W_s`.

## Mixed-sector equations

For distinct nonzero sectors `i,j`, put `k=i xor j` and

```text
T_ij = q_k Y_j + p_k Y_i,
d_ij = T_ij/(W_i V_j) - 1,
theta_i = u P_i R_i W_i / S_i.
```

Under the three equations `F_s=0`,

```text
C_ii = V_i S_i,
C_ij = (1-u)Q_i V_j + u P_i R_i T_ij,
C_ij/(S_i V_j) = 1 + theta_i d_ij.
```

Therefore the mixed principal minor `H_ij=C_ii C_jj-C_ij C_ji`
vanishes exactly when

```text
(1+theta_i d_ij)(1+theta_j d_ji)=1.
```

Writing

```text
a=d_CG, b=d_GC, c=d_CT,
d=d_TC, e=d_GT, f=d_TG,
N=a d e + b c f,
```

the generic nonzero solution of the three bilinear equations is

```text
theta_C = -N/[a c (b f + d e - e f)],
theta_G = -N/[b e (a d - c d + c f)],
theta_T =  N/[d f (a b - a e - b c)].
```

The zero solution corresponds to the forbidden boundary `u=0`.  The exact
rational construction in `construct_record39_six_diagonal_counterexample.py`
chooses `V,W` for which the displayed nonzero solution lies strictly in
`(0,1)^3`, then realizes every named quantity with strict rational D3+ edge
triples.

## Certified conclusion

At the constructed point all six `F_s,H_ij` vanish exactly, while all four
complete Fourier blocks have exact rank four.  Hence the six-diagonal system
is feasible in the strict physical domain and cannot by itself prove
pointwise cut recovery.
