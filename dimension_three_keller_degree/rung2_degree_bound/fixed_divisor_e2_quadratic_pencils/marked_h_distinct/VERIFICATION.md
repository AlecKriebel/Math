# Verification record

## Scope

This package verifies six marked-\(h\)-distinct **endpoint slices** through
\(E_6\), and independently verifies that those six slices do not form a
complete companion taxonomy.  It does not exclude any branch, close the
fixed-divisor row, or prove a degree bound.

Run:

```sh
./verify_all_strict.sh
./test_fail_closed.sh
```

The aggregate requires both exact reconstructions:

- `verify_e7_e6_sympy.py` constructs the weighted determinant directly
  in SymPy, certifies each raw \(E_7\) matrix, proves completeness of the
  five legal gauges plus the displayed normal complement, reconstructs
  the \(E_6\) lower-data matrix, checks the full compatibility generators,
  and verifies the six sharp witnesses.
- `verify_e7_e6_pari.gp` independently rebuilds the Jacobians,
  coefficient matrices, pivot solves, residual generators, and witnesses
  in PARI/GP.
- `verify_companion_moduli_sympy.py` and
  `verify_companion_moduli_pari.gp` independently reconstruct the two
  pencil discriminants, explicit base actions, full projective top
  kernels, and rank-separated counterexamples to endpoint exhaustion.
- `verify_tau_family_sympy.py` and `verify_tau_family_pari.gp`
  independently reconstruct the finite smooth-secant family
  \(R=x(h+\tau s)\), its two-chart pivot cover, complete \(E_7\) normal
  form for \(\tau\ne0\), and compatibility-free \(E_6\) system.
- `test_fail_closed.sh` changes a pinned \(E_6\) determinant in temporary
  copies and requires both exact certificates to reject the mutation.

The exploratory generator `explore_e7_e6.py` is retained for provenance
but is not part of the strict pass condition.

## Monomial and variable orders

For degree \(d\), both scripts use
\[
x^iy^jz^{d-i-j},\qquad
i=d,d-1,\ldots,0,\quad j=d-i,d-i-1,\ldots,0.
\]
Thus
\[
\begin{aligned}
\mathcal M_3={}&(x^3,x^2y,x^2z,xy^2,xyz,xz^2,
                  y^3,y^2z,yz^2,z^3),\\
\mathcal M_2={}&(x^2,xy,xz,y^2,yz,z^2).
\end{aligned}
\]
The raw \(E_7\) columns are the coefficients of
\((U,V,W)\) in
\(\mathcal M_3,\mathcal M_3,\mathcal M_2\).
The \(E_6\) lower columns are the six coefficients of each of the first
two components of \(H_2\), followed by the nine row-major coefficients
of \(L\).

## Pinned minors

The indices below are zero-based, as in the SymPy certificate.  PARI
pins the identical minors with every index increased by one.

| Branch | Raw \(E_7\) rows | Raw \(E_7\) columns | determinant |
|---|---|---|---:|
| RT-reducible/H | 7,8,11,13,16,17,18,19,23,25,30,31,32,33 | 1,2,3,5,6,7,8,9,13,15,16,17,18,19 | \(-82944\) |
| RT-reducible/S | 1,2,3,5,6,7,8,9,11,13,16,17,18,19,23,25 | 1,2,3,5,6,7,8,9,13,15,16,17,18,19,23,25 | \(25389989167104\) |
| RT-smooth/H | 1,2,3,5,6,7,8,9,11,13,16,17,18,19 | 1,2,3,5,6,7,8,9,13,15,16,17,18,19 | \(-82944\) |
| RT-smooth/S | 1,2,3,5,6,7,8,9,11,13,16,17,18,19,23,25 | 1,2,3,5,6,7,8,9,13,15,16,17,18,19,23,25 | \(25389989167104\) |
| RO-smooth/H | 2,4,5,7,8,9,11,12,13,14,16,17,19,22 | 1,2,4,5,6,7,8,9,14,15,16,17,18,19 | \(-13271040\) |
| RO-smooth/S | 0,1,2,3,4,5,6,7,8,9,10,11,12,13,15,17 | 1,2,4,5,6,7,8,9,14,15,16,17,18,19,24,25 | \(12187194800209920\) |

For the legal-basis matrix whose columns are the five gauges followed by
the displayed normal directions:

| Branch | rows | determinant |
|---|---|---:|
| RT-reducible/H | 0,4,7,8,10,11,12,13,14,15,20,24 | \(64\) |
| RT-reducible/S | 0,4,7,8,10,14,17,18,20,24 | \(16/3\) |
| RT-smooth/H | 0,1,2,4,10,11,12,13,14,15,20,24 | \(64\) |
| RT-smooth/S | 0,1,2,4,10,11,12,14,20,24 | \(16/3\) |
| RO-smooth/H | 0,2,4,5,10,11,12,13,14,15,20,22 | \(-128\) |
| RO-smooth/S | 0,2,4,5,10,12,14,15,20,22 | \(64/3\) |

For the \(28\times21\) \(E_6\) lower-data matrix:

| Branch | rows | columns | determinant |
|---|---|---|---:|
| RT-reducible/H | 7,8,11,13,17,18,23,25 | 1,2,3,5,7,8,9,11 | \(256\) |
| RT-reducible/S | 1,2,3,5,7,8,11,13,17,18 | 1,2,3,5,7,8,9,11,19,20 | \(-26873856\) |
| RT-smooth/H | 1,2,3,5,7,8,11,13 | 1,2,3,5,7,8,9,11 | \(256\) |
| RT-smooth/S | 1,2,3,5,7,8,11,13,17,18 | 1,2,3,5,7,8,9,11,19,20 | \(-26873856\) |
| RO-smooth/H | 2,4,5,7,8,9,11,13 | 1,2,4,5,7,8,10,11 | \(3072\) |
| RO-smooth/S | 0,1,2,3,4,5,6,7,8,11 | 1,2,4,5,7,8,10,11,19,20 | \(1934917632\) |

All pinned minors in the six endpoint-slice tables above are nonzero
rational constants.  Hence those six computations make no localization
in a normal parameter.

For the separately verified smooth-secant family, put
\[
q(\tau)=9\tau^2+6\tau-1.
\]
On \(\tau\ne0\), the two pinned \(E_7\) minors are
\[
-557256278016\,\tau^8q(\tau)^2,\qquad
-557256278016\,\tau^8(3\tau-1)^2,
\]
and the two \(E_6\) minors are
\[
-331776\,\tau^4q(\tau)^2,\qquad
-331776\,\tau^4(3\tau-1)^2.
\]
The scripts check
\(\gcd(q(\tau),3\tau-1)=1\), so these pairs cover the whole punctured
finite chart.  The divisor \(\tau=0\) and the projective boundary
\(\tau=\infty\) are rebuilt in the endpoint packages rather than
specialized through these pivots.

## Independence and limitations

SymPy and PARI/GP independently construct the polynomial Jacobian
determinants and coefficient matrices.  They do not exchange exported
matrices or residual vectors.  This is methodologically stronger than
running the same serialized calculation in two interpreters.

All checks are exact characteristic-zero algebra.  Their agreement is
evidence about the encoded statements, not peer review.  In particular,
they do not certify the candidate stabilizer quotient in
`COMPANION_MODULI_GAP.md`; that quotient still requires an independent
hostile reconstruction before it can be frozen.
