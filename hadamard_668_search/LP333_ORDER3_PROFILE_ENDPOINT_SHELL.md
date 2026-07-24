# Exact exclusion of the norm-nine endpoint profile shell

## Status

The order-three `LP(333)` profile equation has a finite energy
stratification.  If `n_3` and `n_9` count the 24 profile letters of
Eisenstein norm 3 and 9, then

```text
n_3+3 n_9=18,                    0 <= n_9 <= 6.
```

The endpoint `n_9=6` is now excluded exactly.  In that shell the remaining
eighteen letters have norm zero.  A local modulo-nine argument reduces each
opposite-class quartet from 256 states to 40.  Applying all 22 exact row-sum
targets and the endpoint energy leaves only

```text
288 assignments = 12 full profile-symmetry orbits.
```

Detached exact integer correlation excludes all twelve orbits.  One orbit
has ten bad nonzero classes and the other eleven have all twelve bad.

This removes one complete energy shell from the profile-zero problem.  It
does not exclude the other six shells, construct an `LP(333)`, or construct
an `H(668)`.

## 1. The endpoint alphabet

For a composition `p=(p_0,p_1,p_2)` of three, put

```text
z(p)=p_0+p_1 omega+p_2 omega^2.
```

The ten profile letters have norms `0`, `3`, or `9`.  Total normalized
profile norm is 54, so

```text
3 n_3+9 n_9=54.
```

At `n_9=6`, necessarily `n_3=0`.  The only allowed letters are therefore

```text
(1,1,1), (3,0,0), (0,3,0), (0,0,3).
```

After the fixed channel/parity signs are applied, every nonzero-column
coefficient is either zero or three times an Eisenstein unit.

## 2. A local modulo-nine condition

Let `a,b` be the two length-37 Eisenstein profile words.  Their fixed
zero-column values are

```text
a(0)=-1,                         b(0)=2.
```

For nonzero lag `t`, split the combined correlation into the four terms
incident with column zero and all remaining terms.  Every remaining term is
a product of two coefficients divisible by three, hence is divisible by
nine.  Exact complementarity therefore implies

```text
-a(t)-conjugate(a(-t))
 +2 b(t)+2 conjugate(b(-t)) = 0 modulo 9.              (1)
```

Negation sends class `j` to class `j+6`, so (1) is local on the quartet

```text
(A_j,A_(j+6),B_j,B_(j+6)).
```

There are `4^4=256` endpoint quartets.  Exhaustive exact Eisenstein
arithmetic gives precisely 40 satisfying (1), with active-letter census

```text
active letters in quartet       states
0                                   1
2                                  12
4                                  27.
```

In particular, activity is forced to be even in every opposite-class
quartet.  Six active letters globally must occur as either `4+2` or
`2+2+2`.

## 3. Complete finite closure

A six-layer dynamic program joins the 40-state local tables while carrying
only:

```text
the four exact aggregate coordinates,
the number of norm-nine letters.
```

At total activity six, eighteen of the 22 row-sum targets have no state.
The remaining four have 72 assignments each:

| aggregate target | assignments |
|---|---:|
| `(-3,0,-3,-3)` | 72 |
| `(-3,0,0,3)` | 72 |
| `(3,0,0,-3)` | 72 |
| `(3,0,3,3)` | 72 |

The exact profile group

```text
C6 x C2_A x C2_B
```

acts freely on these 288 assignments.  They form twelve orbits of size 24.
Thus only twelve orbit representatives require a correlation decision.

The verifier nevertheless reconstructs all 37 physical correlations of all
288 assignments independently, compares them with the existing
thirteen-class implementation, and checks divisibility by nine.  None has
zero nonzero-lag correlation:

```text
bad nonzero classes       assignments       symmetry orbits
10                              24                 1
12                             264                11.
```

Therefore no exact profile-zero point lies in the `n_9=6` endpoint shell.

The complete certificate SHA-256 is

```text
addf4ad655ca1ca16eaef5aebf8787eb14e8a56676e73e05f68e905fc9f45b5a
```

## 4. Search consequence

Any order-three profile constructor may add the exact categorical cut

```text
n_9 <= 5.
```

More importantly, the proof suggests treating the remaining norm shells
separately.  Whenever a shell makes all nonzero coefficients divisible by a
large common ideal, zero-column incidence yields local constraints before
the global cyclic correlations are introduced.

## Reproduction

```text
python3 verify_lp333_order3_profile_endpoint_shell.py
python3 -m unittest -v test_lp333_order3_profile_endpoint_shell.py
```

The verifier uses exact integer arithmetic and the Python standard library
only.
