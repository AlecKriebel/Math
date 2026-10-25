# Exact quartic obstructions for three lower-rank theta records

Date: 2026-08-20 PDT

The original three-record gate and its exact symmetry transport to all twelve
residual theta records are **complete (100%)**.

## Result

Let `q_i` denote the K2P Fourier coordinate in the exact order
`orbit_assignments(4)` recorded in
`theta_quartic_obstruction_certificates.json`.  For each row below, the listed
quartic `F` satisfies

\[
F\circ\phi_{\rm target}=0,
\qquad
F\circ\phi_{\rm source}\ne0
\]

as an exact characteristic-zero polynomial identity/nonidentity.

### Source 2, class 112

This is `theta1` repair 0 directed to target 822, `theta3` repair 1, with the
identity port match.  Its obstruction is

\[
\begin{aligned}
F_{2,112}={}&q_0q_{15}q_{16}q_{18}
+q_0q_{16}q_{18}q_{23}
-q_0q_{20}q_{22}q_{23}
+q_1q_{14}q_{16}q_{18}\\
&-2q_3q_{11}q_{16}q_{18}
+q_3q_{11}q_{20}q_{22}
-q_4q_{12}q_{18}q_{22}
-q_8q_{10}q_{14}q_{16}
+q_8q_{12}q_{14}q_{22}.
\end{aligned}
\]

The target pullback has zero terms.  The source pullback has 630 nonzero
terms.  The common port multidegree is `(3,0,2,1,1,1,2,1)`.

### Source 2, class 113

This has the same source and target presentations with port match
`(0,1,3,2)`.  Its obstruction is

\[
\begin{aligned}
F_{2,113}={}&q_0q_{16}q_{17}q_{29}
-q_0q_{16}q_{23}q_{29}
-q_0q_{17}q_{22}q_{31}
+q_0q_{22}q_{23}q_{31}\\
&-q_1q_{14}q_{16}q_{29}
+q_1q_{14}q_{22}q_{31}
+2q_3q_{11}q_{16}q_{29}
-q_3q_{11}q_{22}q_{31}\\
&-q_3q_{14}q_{16}q_{27}
-q_5q_{11}q_{22}q_{29}
+q_5q_{14}q_{22}q_{27}.
\end{aligned}
\]

The target pullback has zero terms.  The source pullback has 342 nonzero
terms.  The common port multidegree is `(2,1,3,0,1,1,2,1)`.

### Source 4, class 8

This is `theta3` repair 0 directed to target 822, `theta3` repair 1, with the
identity port match.  Its obstruction is

\[
\begin{aligned}
F_{4,8}={}&q_0q_{15}q_{16}q_{32}
+q_0q_{16}q_{23}q_{32}
-q_0q_{23}q_{24}q_{30}
+q_1q_{14}q_{16}q_{32}\\
&-2q_3q_{11}q_{16}q_{32}
+q_3q_{11}q_{24}q_{30}
-q_4q_{14}q_{16}q_{27}
-q_6q_{10}q_{24}q_{32}
+q_6q_{14}q_{24}q_{27}.
\end{aligned}
\]

The target pullback has zero terms.  The source pullback has 96 nonzero
terms.  The common port multidegree is `(2,1,3,0,2,1,1,1)`.

## Explicit source monomial witnesses

In the canonical descriptor parameter order
`(s0,g0,...,s7,g7,lambda0,lambda1)`, the following coefficients occur in the
source pullbacks.  A single nonzero coefficient is already an exact proof that
the pullback polynomial is not identically zero.

| Base quartic | Exponent | Coefficient |
|---|---|---:|
| `F_(2,112)` | `(0,0,0,1,3,0,2,0,2,1,1,0,1,1,2,1,0,1)` | `-1` |
| `F_(2,113)` | `(2,0,0,1,2,1,1,0,1,1,1,1,2,1,0,1,2,1)` | `-1` |
| `F_(4,8)` | `(2,0,0,1,2,1,1,1,1,1,0,1,2,1,1,0,2,1)` | `1` |

## Exact symmetry transport and twelve-record coverage

Write `e=(0,1,2,3)`, `a=(1,0,2,3)`, `b=(0,1,3,2)`, and
`h=(1,0,3,2)`.  Direct graph replay proves that source 2 (`theta1`, repair 0)
and source 3 (`theta1`, repair 1) have the same descriptor; target 822 has the
label symmetry `h`; and source 4 has the label symmetry `a`.

| Sources | Class | Target port match | Certificate | Coordinate permutation | Source terms |
|---|---:|---|---|---|---:|
| 2 and 3 | 112 | `e` | `F_(2,112)` | identity | 630 |
| 2 and 3 | 113 | `b` | `F_(2,113)` | identity | 342 |
| 2 and 3 | 114 | `a` | `F_(2,113)` | identity | 342 |
| 2 and 3 | 115 | `h` | `F_(2,112)` | identity | 630 |
| 4 | 8 | `e` | `F_(4,8)` | identity | 96 |
| 4 | 9 | `b` | `A_a^*F_(4,8)` | swap ports 0 and 1 | 224 |
| 4 | 10 | `a` | `A_a^*F_(4,8)` | swap ports 0 and 1 | 224 |
| 4 | 11 | `h` | `F_(4,8)` | identity | 96 |

The only new polynomial created by transport is

\[
\begin{aligned}
A_a^*F_{4,8}={}&q_0q_{15}q_{16}q_{21}
+q_0q_{16}q_{21}q_{25}
-q_0q_{19}q_{24}q_{25}
+q_1q_{14}q_{16}q_{21}\\
&-2q_4q_{10}q_{16}q_{21}
+q_4q_{10}q_{19}q_{24}
-q_8q_{11}q_{14}q_{16}
-q_3q_{13}q_{21}q_{24}
+q_8q_{13}q_{14}q_{24}.
\end{aligned}
\]

Its canonical source pullback has 224 terms and contains the monomial with
exponent `(0,0,0,1,3,0,2,1,2,0,2,1,1,1,1,0,0,1)` with coefficient `-1`.

## Why these are physical directed-separation certificates

Every monomial of each `F` has the displayed common eight-entry port weight
(the `s`- and `g`-sector weight at each of four ports).  Consequently the full
two-sector incidence action multiplies `F` by one common nonzero monomial.
Its zero locus is therefore invariant under all physical port/bridge scales;
the obstruction cannot be removed by a bridge gauge.

The source pullback is a nonzero polynomial.  The strict positive K2P domain
is a nonempty Euclidean-open parameter set, so that pullback cannot vanish on
all strict source parameters.  Its zero locus is proper.  Thus a generic
strict source point violates a polynomial identity satisfied by every target
point.  In particular, none of the three directed source images is contained
in its target image or target variety.  The lower source ranks (14, 14, and
15 versus target rank 16) do not imply containment.

There is also a common explicit strict-domain witness: edge class `i` uses
`s_i=1/4` and `g_i=(i+1)/10`, while the two inheritance probabilities are
`1/3` and `2/3`.  Every pair lies in `D_+`.  At that point the exact source
values are, respectively,

- `57443/7644119040000000` for sources 2/3 with `F_(2,112)`;
- `-1046129/20384317440000000` for sources 2/3 with `F_(2,113)`;
- `-1183/9059696640000` for source 4 with `F_(4,8)`; and
- `1729/3397386240000` for source 4 with `A_a^*F_(4,8)`.

## Validation architecture

The low-memory modular calculation is only a candidate generator.  It accepts
a candidate only after expanding its target pullback over characteristic zero
and checking exact cancellation, while also checking a nonzero exact source
pullback.

An independent verifier bypasses `MapDescriptor`, homogeneous-block builders,
kernel routines, and separator routines.  It reconstructs the three bound
graphs, directly expands the four displayed-tree switch sums, checks every
port weight, binds every certificate to the completed production record, and
substitutes all terms exactly.  Its terminal result is:

```
THETA_QUARTIC_OBSTRUCTIONS_INDEPENDENT_REPLAY_PASS
```

A separately authored adversarial verifier also reconstructs the descriptors,
checks all twelve transported records, and mutates every load-bearing term.
All 29 single-coefficient mutations and all 116 single-coordinate mutations
destroy target vanishing; there are zero mutation survivors.

The machine-readable certificate contains the complete 36-coordinate order,
record and graph hashes, sparse terms, pullback sizes, and replay-script hashes.
