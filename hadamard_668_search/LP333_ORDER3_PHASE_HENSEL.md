# LP(333) first Eisenstein phase digit

## Status

Let `lambda=1-omega`.  Once a residue-profile tuple is fixed, every active
three-fiber phase is a signed cube root

```text
sigma omega^L(u),
```

where `L` is affine in one placement trit over `F_3`.  Reducing the exact
phase-frame equations modulo `lambda^2` therefore turns their first
placement-dependent digit into an affine linear system over `F_3`.

On the 22 stored ideal-compatible profile witnesses:

```text
placement variables per tuple                         54
displayed reversal-independent equations              20
identically zero displayed rows                        2
consistent tuples with rank 18 and nullity 36         21
inconsistent tuples with rank pair (16,17)              1
```

The inconsistent object is fixed-profile witness 3, whose aggregate shard
target is `(-3,0,0,3)`.  An explicit two-row linear-combination certificate
gives `0=1` over `F_3`.  This excludes that fixed profile assignment only,
not its aggregate shard.

All 22 objects in this census subsequently fail the stronger,
placement-independent full-LP gate `D_t=0`.  The present census is therefore
subsumed on this stored corpus.  Its lasting value is the reusable affine
first-digit formulation for a future profile that passes `D_t=0`; the
observed rank 18 must not be assumed universal.

No `LP(333)` or Hadamard matrix of order 668 is constructed.

## 1. First-digit linearization

For an exact phase coefficient

```text
F(u)=sum_t sigma_t omega^L_t(u)-target,
```

the profile data fixes the residue modulo `lambda`.  When that residue
vanishes, the expansion

```text
omega^L = 1-L lambda                 modulo lambda^2
```

gives

```text
F/lambda = -sum_t sigma_t L_t(u)     modulo lambda.
```

Because `Z[omega]/(lambda)` is `F_3`, this is an affine equation in the
placement trits.  The verifier constructs it directly from the signed
fiber phases rather than differentiating a precomputed table.

## 2. Displayed equation system

The diagonal component `E_0` is self-adjoint, so it contributes its origin
and six reversal representatives.  The directed component `E_1` contributes
all thirteen invariant column parts:

```text
E_0: origin plus C_0,...,C_5          7 rows
E_1: origin plus C_0,...,C_11        13 rows
                                      -------
                                      20 rows.
```

The two origin rows vanish identically at this digit.  For every consistent
stored tuple, a canonical solution is replayed through exact Eisenstein
arithmetic.  For witness 3, the retained row multipliers combine
`E_0(C_0)` and `E_1(C_6)` into the contradiction `0=1`.

## 3. Exact certificates

```text
rank/nullity census
db2a578380db873b9c7db711d7638fcf3b01b4155592a1e1584e5a2d2634d205

canonical solution corpus
5805264e94cef3ff8ce50e24a57261f736ac8ef688bb2948e2233331fdeb985a

inconsistency certificate
4d89429afda3af26471cb07f71e155d9763c03d314acf4d6cea3b5f9687bf27b
```

## Reproduction

```text
python3 verify_lp333_order3_phase_hensel.py
python3 -m unittest -v test_lp333_order3_phase_hensel.py
```

The verifier uses exact integer and Eisenstein arithmetic and the Python
standard library only.
