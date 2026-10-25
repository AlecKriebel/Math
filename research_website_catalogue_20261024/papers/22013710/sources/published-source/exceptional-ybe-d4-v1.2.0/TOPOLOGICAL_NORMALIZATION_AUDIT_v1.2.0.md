# Topological normalization audit — version 1.2.0

This record fixes the conventions behind the enhanced trace, HOMFLYPT
specialization, and triple-cyclic-branched-cover formula in the manuscript.
It was prepared from the original typeset sources, not from a secondary
summary.

## Primary sources inspected

1. V. G. Turaev, “The Yang–Baxter equation and invariants of links,”
   *Inventiones Mathematicae* **92** (1988), no. 3, 527–553,
   [doi:10.1007/BF01393746](https://doi.org/10.1007/BF01393746).
   The audited GDZ scan had SHA-256
   `d59c4f4de43d62a21a7ce07c261e1bd3ab9ed2c1cad7af74a5ae2bf5e0c148d8`.
2. W. B. R. Lickorish and K. C. Millett, “Some evaluations of link
   polynomials,” *Commentarii Mathematici Helvetici* **61** (1986), no. 1,
   349–359,
   [doi:10.1007/BF02621920](https://doi.org/10.1007/BF02621920).
   The audited GDZ scan had SHA-256
   `a5acc50000f17616a1af076eac16769505272ab41ab4eec40a959c74e9cdb437`.

The scans themselves are not redistributed in this package.

## Turaev enhancement, line by line

- Section 2.2, printed p. 529, defines the partial operator trace
  `Sp_n` by tracing the final tensor factor.
- Section 2.3, p. 529, defines an enhanced Yang–Baxter operator
  `(R, mu, alpha, beta)` by
  `R(mu tensor mu)=(mu tensor mu)R` and
  `Sp_2(R(mu tensor mu))=alpha beta mu`,
  `Sp_2(R^{-1}(mu tensor mu))=alpha^{-1} beta mu`.
- Section 3.1, p. 530, defines
  `T_S(xi)=alpha^{-w(xi)} beta^{-n}
  Tr(rho_R(xi) mu^{tensor n})`.
- Theorem 3.1.2, pp. 530–531, proves Markov invariance.
- Section 3.2 and formula (4), p. 532, give the oriented-link invariant and
  `T_S(unknot)=beta^{-1}Tr(mu)`.

For the five-word matrix, `mu=I_4`, `alpha=kappa`, and `beta=2`. The exact
partial traces are

```text
Tr_2(R)      = 2 kappa I_4,
Tr_2(R^{-1}) = 2 kappa^{-1} I_4.
```

The package checks both tensor legs, which is stronger than the one-leg
condition in the definition. Turaev’s formula therefore becomes exactly

```text
J_R(cl(xi)) = kappa^{-wr(xi)} 2^{-n} Tr(rho_n(xi)),
```

with ordinary unnormalized matrix trace and `J_R(unknot)=2`.

## HOMFLYPT sign crosswalk

The manuscript uses

```text
a P_H(L_+) - a^{-1} P_H(L_-) = z P_H(L_0),
P_H(unknot)=1.
```

At `(a,z)=(i,i)`, this is

```text
P_H(L_+) + P_H(L_-) = P_H(L_0).
```

The matrix Hecke relation gives

```text
R - q R^{-1} = kappa I,
q kappa^{-2} = -1,
```

so the enhanced trace obeys the same plus-sign skein relation. Since its
unknot value is 2,

```text
J_R(L) = 2 P_H(L;i,i).
```

## Lickorish–Millett crosswalk

On printed p. 349, Lickorish–Millett use

```text
P_U=1,
ell P_+ + ell^{-1} P_- + m P_0 = 0.
```

Thus `P_+(1,1)+P_-(1,1)+P_0(1,1)=0`. Their Theorem 2 is announced on
p. 350 and stated with the cover definition on p. 353:

```text
P_L(1,1) = (-2)^{d_2(L)/2},
d_2(L)=dim_{F_2} H_1(T_L;F_2).
```

Here `T_L` is obtained by completing the cover of `S^3 minus L` associated
with the kernel of the homomorphism to `Z/3` that sends each positively
oriented meridian to 1. The manuscript writes this oriented cover as
`Sigma_3(L)`. For a multi-component link the orientation qualifier is
retained; the word “canonical” is not used without it.

In an oriented skein triple, `c(L_+)=c(L_-)`, while `c(L_0)` differs by one.
Consequently

```text
Q(L)=(-1)^{c(L)-1} P_L(1,1)
```

obeys the manuscript’s plus-sign skein relation and has `Q(unknot)=1`.
Therefore

```text
P_H(L;i,i)=(-1)^{c(L)-1}(-2)^{d_2(L)/2},
J_R(L)=2(-1)^{c(L)-1}(-2)^{d_2(L)/2}.
```

The source does not isolate evenness of `d_2` as a numbered lemma. Theorem 2
prints the exponent `d_2/2`, and its proof on pp. 354–355 shows that the three
skein dimensions occur as `N,N-2,N-2`; the induction therefore preserves even
parity from the base case. This is the parity input cited by the manuscript.

## Exact small-link checks

| Oriented braid closure | Writhe | Matrix trace | `J_R` |
|---|---:|---:|---:|
| identity in `B_1` (unknot) | 0 | 4 | 2 |
| identity in `B_2` (two-unlink) | 0 | 16 | 4 |
| `sigma_1^{2}` (positive Hopf) | 2 | `8q` | -2 |
| `sigma_1^{-2}` (negative Hopf) | -2 | `8q^{-1}` | -2 |
| `sigma_1^{3}` (positive trefoil) | 3 | -16 | -4 |
| `sigma_1^{-3}` (negative trefoil) | -3 | -16 | -4 |

The exact verifier independently reproduces these values.

## Gate decision

All five gated issues were resolved: the original article was inspected; its
variables and normalization were crosswalked; the sign and factor 2 were
derived; the oriented cover was defined unambiguously; and even parity was
checked in the proof. The exact branched-cover formula is therefore included.
No new HOMFLYPT or branched-cover evaluation theorem is claimed.
