# LP(333) exact integral primitive-nine sieve

## Status

The six-digit primitive-nine jet over `F_3` is only a congruence shadow of a
stronger exact condition over the cyclotomic integers.  For each invariant
column-lag class, the exact condition is simply equality of three
correlation counts at row lags separated by three.

Both fully labelled mod-three certificates currently pinned in the
repository fail this exact condition in every nonzero column-class/residue
group.  This proves that the integral layer is strictly stronger on actual
catalog lifts.

It does not yet exclude catalog row 695, because the certificates are
existential witnesses for the weaker sieve rather than an exhaustion of all
labelled lifts of that row.  No `LP(333)` or Hadamard matrix is claimed.

## 1. Exact ninth-root equation

For plus supports `P,Q` in `Z/9 x F_37`, the Legendre difference-family
identity is

```text
P P^(-1) + Q Q^(-1) = 167 G + 167 e.             (1)
```

Evaluate the row coordinate at a primitive ninth root `z`, while retaining
the `F_37` column coordinate.  The group-sum term disappears:

```text
A A* + B B* = 167 e  in Z[z][F_37].              (2)
```

For a fixed column lag `b`, let `c_(b,a)` be the exact plus-intersection
count at row lag `a`, after subtracting 167 at `(b,a)=(0,0)`.  Equation (2)
requires

```text
C_b(z)=0,    C_b(x)=sum_(a=0)^8 c_(b,a) x^a.     (3)
```

## 2. Vanishing is triple equidistribution

The primitive ninth cyclotomic polynomial is

```text
Phi_9(x)=x^6+x^3+1.
```

Since `deg C_b <= 8`, exact vanishing in (3) is equivalent to divisibility
by `Phi_9`.  Reducing `x^6,x^7,x^8` gives the six-coordinate remainder

```text
c_0-c_6, c_1-c_7, c_2-c_8,
c_3-c_6, c_4-c_7, c_5-c_8.
```

Therefore the exact criterion is

```text
c_(b,s) = c_(b,s+3) = c_(b,s+6),    s=0,1,2.    (4)
```

This replaces cyclotomic arithmetic by exact integer equidistribution.

Order-three column invariance leaves 13 column-lag parts.  Hence (4)
displays

```text
13 x 6 = 78 integer equations.
```

The zero column class already satisfies its six equations because the
labelled certificates impose the four reversal-independent exact
row-direction correlations.  The genuinely new layer consists of

```text
12 x 6 = 72 integer equations
```

or 36 triple-equality groups.

## 3. Relation to the mod-three jet

Modulo three,

```text
Phi_9(x) = (x-1)^6.
```

Thus the existing six-digit jet proves only that the six integer remainders
above vanish modulo three.  It does not force them to vanish over the
integers.  The exact verifier confirms this distinction directly: every
defect of both known modular certificates is divisible by three, yet many
are nonzero.

## 4. Exact audit of the two modular certificates

For the original row-695 labelled certificate:

```text
bad nonzero column-class/residue groups = 36 of 36
nonzero displayed integer equations    = 59 of 72
maximum absolute defect                = 24
gcd of all displayed defects           = 3
correlation-table SHA-256
  4f9d704942b8105fda93ee4672a388fff0b830ec2fbcc9ef85685893bbc19244
```

For the independently reconstructed trit certificate:

```text
bad nonzero column-class/residue groups = 36 of 36
nonzero displayed integer equations    = 66 of 72
maximum absolute defect                = 21
gcd of all displayed defects           = 3
correlation-table SHA-256
  063254151ec2c77b0ee806cb1e485963182ecece696f34f8bc175d115b478ab7
```

Each audit first replays all 222 mod-three jet equations and the four exact
zero-column correlations.  It then independently reconstructs all 333
physical correlation positions, checks order-three class invariance, and
performs integer division by `Phi_9`.

The result is a strict refinement on explicit fully labelled lifts, not a
timeout statement or a catalog exclusion.

## Reproduction

```text
python3 verify_lp333_order3_integral9.py
python3 -m unittest -v test_lp333_order3_integral9.py
```

Both commands are dependency-free and use exact integer arithmetic.
