# Physical obstruction to the trivial zero phase-cone branch

## Status

The zero branch of the trivial factor in the prime-167 ninth-root phase
cone cannot contain a physical order-three `LP(333)` frame.

In fact, the trivial coordinate of **each** binary channel is nonzero.  A
vanishing coordinate would force the channel's nine plus-count row margins
to repeat with period three.  Their total would then be divisible by three,
contrary to the exact per-channel plus count

```text
(333+1)/2 = 167.
```

The complete pinned 1,756-word row-margin catalog sharpens the surviving
nonzero branch to 1,411 exact ordered coordinate pairs.  These pairs have
1,411 distinct norm-minus-one projective ratios, compared with 4,657,464
ratios in the unrestricted finite-field cone.

This removes only the joint trivial-zero cone branch.  It does not remove
any of the three primitive degenerate branches, construct a physical phase
frame, construct an `LP(333)`, or construct `H(668)`.

## 1. The coordinate is a row-margin polynomial

For one binary channel `X`, let

```text
m_(X,r) = number of plus entries in CRT row r across 37 columns,
                                              r=0,...,8.
```

The original sign sequence has length 333 and sum one, so its plus support
has size 167.  Consequently, separately for `X=A` and `X=B`,

```text
0 <= m_(X,r) <= 37,
sum_r m_(X,r) = 167.                                  (1)
```

Let `alpha` be the primitive ninth root used in the recombined phase
factorization.  Summing its column word at the trivial character gives

```text
c_X = sum_(r=0)^8 m_(X,r) alpha^r
        in F_167(alpha) = F_(167^6).                   (2)
```

This identity follows directly by reversing the two Fourier groupings.
If

```text
U_s(c) = sum_(q=0)^2 x_(s+3q,c) omega^q
```

and

```text
W_X(c)=U_0(c)+alpha U_1(c)+alpha^2 U_2(c),
```

then `omega=alpha^3`, and hence

```text
sum_c W_X(c)
  = sum_(c,s,q) x_(s+3q,c) alpha^(s+3q)
  = sum_r m_(X,r) alpha^r.
```

Thus the `c_X` in (2) is exactly the trivial coordinate in the certified
cone equation, not a new relaxation of it.

## 2. Exact kernel and the `[0,37]` lift

Modulo 167,

```text
ord_9(167)=6,
Phi_9(z)=z^6+z^3+1
```

is irreducible.  Reducing (2) in the basis
`1,alpha,...,alpha^5` gives

```text
c_X =
  (m_0-m_6)
 + (m_1-m_7) alpha
 + (m_2-m_8) alpha^2
 + (m_3-m_6) alpha^3
 + (m_4-m_7) alpha^4
 + (m_5-m_8) alpha^5.                                (3)
```

The verifier independently constructs the `6 x 9` evaluation matrix.  It
has rank six, and its full three-dimensional kernel is spanned by

```text
(1,0,0,1,0,0,1,0,0),
(0,1,0,0,1,0,0,1,0),
(0,0,1,0,0,1,0,0,1).
```

Therefore `c_X=0` is equivalent to

```text
m_s = m_(s+3) = m_(s+6) modulo 167,     s=0,1,2.      (4)
```

The modular-to-integral step is exact.  Each difference in (4) lies in
`[-37,37]`, and the only multiple of 167 in this interval is zero.  Hence
(4) holds over the integers.  Equation (1) would then become

```text
167 = 3(m_0+m_1+m_2),
```

which is impossible.  We have proved, independently in each channel,

```text
c_A != 0,                    c_B != 0.                 (5)
```

The trivial cone equation is

```text
c_A c_A^(167^3) + c_B c_B^(167^3) = 0.
```

Its zero branch is `(c_A,c_B)=(0,0)`.  Statement (5) eliminates that entire
branch; only the nonzero norm-minus-one branch can be physical.

## 3. Exact row-margin image of the nonzero branch

The complete order-three row-sum catalog is pinned at

```text
output/lp333_order3_row_sum_catalog.csv
SHA-256
e8631dc0ae2f65c475af1c2e13429778f666a0fa8a13c9f1153d07d7883a98ea
```

For a Gaussian catalog entry `s_r`, the QPSK/sign-pair identity is

```text
s_r = (A_r+B_r + i(B_r-A_r))/2.
```

Thus the two binary sign row sums and plus margins are recovered exactly:

```text
A_r = Re(s_r)-Im(s_r),
B_r = Re(s_r)+Im(s_r),

m_(A,r) = (37+A_r)/2,
m_(B,r) = (37+B_r)/2.                                 (6)
```

The verifier checks (6) on every catalog entry, including the exact
per-channel total 167.  It also checks compatibility with the fixed zero
column:

```text
zero A plus word = (1,1,1,0,0,1,0,1,0),
zero B plus word = (1,1,1,1,0,0,1,0,0),
```

and proves that `(m_r-zero_r)/3` is an integer in `[0,12]` in every row.

Mapping all 1,756 entries through (2) gives:

```text
catalog rows                                  1,756
distinct ordered pairs (c_A,c_B)              1,411
distinct ratios R=c_B/c_A                     1,411

pair/ratio multiplicity one                   1,066
pair/ratio multiplicity two                     345
```

Every pair satisfies the finite-field norm equation, every coordinate is
nonzero, and every ratio obeys

```text
R R^(167^3) = -1.                              (7)
```

Moreover, on this catalog each of the 1,411 ratios determines a unique
ordered pair, so the row margins fix the scale as well as the projective
point.  The abstract norm-minus-one fiber in
`F_(167^6)/F_(167^3)` has

```text
167^3+1 = 4,657,464
```

ratios.  A physical solution in this order-three lane must use one of the
1,411 pinned ratio/scale pairs, a reduction by a factor greater than 3,300
at the trivial coordinate before the primitive inverse-CRT intersection is
considered.

The complete cone-image certificate is

```text
50f3d0f090187ded04c9bce52cfb6900c451dd005d48e4db965046c8d71edb26
```

## 4. Search consequence and scope

The finite-field search should no longer allocate a branch selector for the
trivial factor.  It should:

1. load one of the 1,411 exact nonzero `(c_A,c_B)` pairs induced by the
   complete row-margin catalog;
2. solve the three primitive paired factors subject to the physical
   coefficient alphabet, profile constraints, and that fixed margin pair;
3. replay any survivor over the integers.

No analogous certified exclusion is presently established for a primitive
degenerate branch.  The three primitive branch selectors therefore remain
part of a complete search.

## Reproduction

From this directory:

```text
python3 verify_lp333_phase_cone_trivial_branch.py
python3 -m unittest -v test_lp333_phase_cone_trivial_branch.py
```

The verifier uses exact arithmetic and Python's standard library only.
