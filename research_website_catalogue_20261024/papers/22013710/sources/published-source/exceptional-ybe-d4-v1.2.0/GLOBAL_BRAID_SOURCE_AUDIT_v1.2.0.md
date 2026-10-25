# Global braid source audit — version 1.2.0

This table records the source and normalization for each result transported
from the quaternionic Family III realization. Direct deductions in the
manuscript are distinguished from cited results.

## Source table

| Claim | Primary locator | Use in this paper |
|---|---|---|
| Literal Family III operator | Galindo–Rowell, §13.2, PDF pp. 54–55 | Independently encoded as `R_GR` and compared exactly with the five-word matrix. |
| Family III normalizes the Pauli group | Galindo–Rowell, Proposition 8.1, PDF pp. 35–37 | Supports the Clifford statement. The displayed Pauli quarter-turn factorization is also proved directly. |
| Finite quaternionic braid images | Rowell, Theorem 3.1, p. 175, and Lemma 3.3, p. 177; also Galindo–Rowell, Theorem 8.4 | Transferred by the exact all-strand unitary conjugacy. No image group is named. |
| Quaternionic twisted tower and normal basis | Galindo–Rowell, §13.1, PDF pp. 53–54 | Gives `A_n(Q_8)`, its normal monomials, and dimension `4^{n-1}`. |
| Hecke quotient as braid-generated subalgebra | Rowell, Lemma 3.2, p. 176 | Used only as an embedding/subalgebra statement, never as equality with the full tower. |
| Coefficient trace versus matrix trace | Galindo–Rowell, Theorem 7.3, PDF p. 28 | Gives `Tr o Phi_n=4^n epsilon_n` for `A=Z/2`. |
| Exact deterministic evaluation | Galindo–Rowell, Theorem 7.10, PDF pp. 32–34 | Gives exact deterministic polynomial time in strand number plus word length for fixed Family III data. |

The Galindo–Rowell source audited here is arXiv:2608.16865v1, “Unitary
Yang–Baxter Operators: Towards a Classification,” submitted 17 August 2026.
The Rowell source is E. C. Rowell, “A quaternionic braid representation (after
Goldschmidt and Jones),” *Quantum Topology* **2** (2011), 173–182,
[doi:10.4171/QT/18](https://doi.org/10.4171/QT/18).

## Locator correction

Galindo–Rowell v1 cites “Rowell’s Lemma 3.4” for the Hecke embedding. In the
published *Quantum Topology* article the required statement is Lemma 3.2 on
p. 176; Remark 3.4 is unrelated. The manuscript uses the published locator.

## Direct all-strand argument

Let `T_n=Rev_n S^{tensor n}`. The exact two-site identity implies, for every
Artin generator,

```text
T_n rho_n^K(sigma_i) T_n^* = rho_n^GR(sigma_{n-i}).
```

The half twist

```text
Delta_n=(sigma_1...sigma_{n-1})(sigma_1...sigma_{n-2})...sigma_1
```

satisfies `Delta_n sigma_i Delta_n^{-1}=sigma_{n-i}`. With
`D_n=rho_n^GR(Delta_n)` and `U_n=D_n^* T_n`, one gets

```text
U_n rho_n^K(xi) U_n^* = rho_n^GR(xi)
```

for every braid word. This argument is printed in full and does not depend on
a finite verification at `n=3,4`.

## Clifford and phase normalization

For the literal Pauli placements, `U=iP_Z`, `V=iP_X`, and

```text
R_GR = kappa ((I+U)/sqrt(2)) ((I+V)/sqrt(2))
     = kappa exp(i pi P_Z/4) exp(i pi P_X/4).
```

The order of the two factors is fixed. Each is a Pauli quarter-turn. The
five-word representation is therefore Clifford with respect to the conjugated
frame `(Rev_n S^{tensor n})^* P_{2n} (Rev_n S^{tensor n})`; the package does
not claim that `S` itself is a standard computational Clifford matrix.

## Algorithm normalization

Galindo–Rowell’s algorithm applies to the unphased operator
`r_0=(I+U+V+UV)/2`, while `R_GR=kappa r_0`. Thus

```text
rho_R(xi)=kappa^{wr(xi)} Phi_n(rho_{r_0}(xi)).
```

For `A=Z/2`, Theorem 7.3 gives `Tr o Phi_n=4^n epsilon_n`, so

```text
kappa^{-wr(xi)} 2^{-n} Tr(rho_R(xi))
=2^n epsilon_n(rho_{r_0}(xi)).
```

This is exactly the coefficient-trace invariant covered by Theorem 7.10.
Polynomial time is not inferred from the exponentially growing tower
dimension.

## Deliberate limitations

The paper does not identify the finite image group for general `n`, prove
direct two-site equivalence without the opposite, call `S` a standard
Clifford, or classify the remaining exceptional dimensions.
