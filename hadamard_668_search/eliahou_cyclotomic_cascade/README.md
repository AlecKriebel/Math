# Cyclotomic cascade for the distance-41 Eliahou anti-fold

## Status

This folder contains a bounded exact experiment, not a Hadamard matrix.
It classifies the first two cyclotomic layers of all 30 distinct
orientation-free anti-fold support instances at special distance 41.

The result is negative as a construction gate:

- all 30 instances survive `Phi_4`;
- all 30 instances survive the joint `Phi_4 Phi_12` layer;
- certified full-anti-fold case 0 still has
  `79,852,759,562,024,974` supports at the latter layer;
- solver-observed case 1 still has
  `75,920,209,690,765,723` supports there.

Thus neither low cyclotomic factor explains the known full infeasibility.
No exact anti-fold support, `BS(84,83)`, or `H(668)` is claimed.

## 1. Hermitian norm reduction

Let `D_A,D_B,D_C,D_D` be the four length-42 anti-fold rows.  Pair them by

```text
P=(D_A+D_B)/2,       Q=(D_C+D_D)/2,
R=(D_A-D_B)/2,       S=(D_C-D_D)/2.
```

At the distance-41 boundary, `R,S` are fixed sparse boundary polynomials.
The 39 support choices occur only in `P,Q`.  The anti-fold equation becomes

```text
P P* + Q Q* = 167 - R R* - S S*
                         in Z[z]/(z^42+1).              (1)
```

The relevant factorization is

```text
z^42+1 = Phi_4(z) Phi_12(z) Phi_28(z) Phi_84(z).       (2)
```

Because

```text
z^2+1  = Phi_4(z),
z^6+1  = Phi_4(z) Phi_12(z),
z^14+1 = Phi_4(z) Phi_28(z),
```

reduction modulo `z^2+1`, `z^6+1`, and `z^14+1` gives a natural exact
factor cascade.

For modulus `m=2` or `6`, each support block is first reduced to its `m`
coefficient sums.  The program groups choices independently by residue,
then records only

```text
(selected weight, independent coefficients of P P*).
```

The `P` and `Q` tables are joined against the fixed right side of (1).
Multiplicities are exact unsigned integers; the final counts use 128-bit
arithmetic.  This avoids the product literals and large pseudo-Boolean
formula of the exploratory SAT encoding.

## 2. Complete census

The exact per-case values are frozen in `EXPECTED_CENSUS.json`.  Across
the 30 canonical instances:

| layer | surviving cases | support-count range |
|---|---:|---:|
| `Phi_4` | 30/30 | `215,565,164,481,088,522,656` to `428,541,732,282,722,170,554` |
| `Phi_4 Phi_12` | 30/30 | `48,953,783,073,014,748` to `107,996,012,316,872,012` |

The low-factor cascade removes roughly three to four orders of magnitude
from the `Phi_4` inventories, but leaves tens of quadrillions of supports
in every case.  It is a useful exact classifier, not convergence to an
anti-fold solution.

Every emitted representative is reconstructed as four physical
42-coordinate anti-fold rows.  Direct integer replay verifies its claimed
factor equation and also verifies that it fails the full anti-fold
equation.  In particular, no factor witness is misreported as a complete
support.

## 3. Calibration on cases 0 and 1

The existing full census records:

- case 0, long `q` representative 0: certified full UNSAT;
- case 1, long `q` representative 2: one solver-UNSAT observation without
  a checked proof.

Their joint `Phi_4 Phi_12` inventories are respectively

```text
case 0: 79,852,759,562,024,974
case 1: 75,920,209,690,765,723.
```

For certified case 0 this proves that its obstruction occurs only after
the low-factor layer: it must involve `Phi_28`, `Phi_84`, or compatibility
between the factor conditions.  The same diagnosis for case 1 remains
conditional on its unproved full-UNSAT observation.

## 4. Why direct `Phi_28` enumeration was stopped

The same residue-vector method at modulus 14 is exact, but its state growth
is already too large for the bounded experiment.  Across the 26 distinct
arithmetic `P/Q` specifications it would enumerate

```text
328,470,183,936
```

reduced coefficient tuples.  The support-weight cap together with the
automatic zero-lag bound removes almost nothing:

```text
328,145,957,800
```

tuples remain.  One specification alone has `39,182,082,048` tuples.
These figures are computed exactly by `--growth 14`; they are not timing
extrapolations.  They describe the leaves of this particular
weakly-pruned residue-product method, not an inherent lower bound for every
`Phi_28` algorithm.  Building seven-dimensional norm histograms directly
from that frontier would violate the point of the bounded cascade, so no
such run is attempted.

The next justified decomposition pairs residues `j` and `j+7`.  At a
primitive 28th root `xi`,

```text
xi^7=i,
V(xi)=A(xi)+i B(xi),
```

so the 14-coordinate problem becomes a seven-coordinate Gaussian
Hermitian problem over `Z[i]`.

The joint `Phi_12`/`Phi_28` state must retain more than the collapsed
modulo-14 coefficient.  A residue contains at most the three cells
`r,r+14,r+28`, hence at most eight states after retaining

```text
(support weight, modulo-14 removal, full modulo-6 removal vector).
```

Pairing residues `j,j+7` therefore gives at most `8^2=64` refined states
per Gaussian coordinate.  Both bounds are attained.  In the natural split
`j=0,1,2 | j=3,4,5,6`, put the smaller final pair on the four-coordinate
side; exhaustive state counting over all 30 cases and both `P/Q` sides
then gives the sharp maxima

```text
64^3 = 262,144,       32*64^3 = 8,388,608
```

raw half assignments per block, rather than tens of billions of complete
tuples.  The generic bound for an arbitrary four-coordinate side is
`64^4=16,777,216`.

The modulo-6 refinement is necessary: in case `L0`, the `P`-side
modulo-14 residue 1 contains cells `1,15,29`; singleton supports `{1}` and
`{15}` have the same weight and modulo-14 removal, but different modulo-6
removal vectors.  A next implementation should carry:

1. the two half evaluations;
2. their self-norm signatures;
3. the explicit bilinear cross signature;
4. the already-computed `Phi_12` signature and support weight.

The cross term prevents a naive one-key hash join, but this is the precise
bounded frontier for a `Phi_12`/`Phi_28` intersection.

## 5. Reproduction

The full verifier compiles the C++ engine in a temporary directory, runs
both complete censuses, checks the frozen counts, independently recomputes
all `Phi_4` counts in Python, replays every representative, and enumerates
the 60 refined `P/Q` specifications to certify the Gaussian-frontier
bounds and the pinned modulo-14/modulo-6 collision:

```sh
python3 verify_cyclotomic_cascade.py
python3 -m unittest -v test_cyclotomic_cascade.py
```

On the 16 GB M1 Pro host, the full verifier took about 23 seconds and
peaked near 1.21 GB RSS.  The source-only algebra check is:

```sh
clang++ -O3 -std=c++20 audit_cyclotomic_cascade.cpp \
  -o /tmp/audit_cyclotomic_cascade
/tmp/audit_cyclotomic_cascade --self-test
```

No compiled binary is retained in this folder.
