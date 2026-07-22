# Why Eliahou's fixed-q repair cannot be exact

This note closes one sharply defined search lane.  Keep Eliahou's published
length-167 sequence `q=(83,2,81,1)` fixed, retain his special quadruple

```text
(s, s', sq, (sq)'),
```

and allow every sign of `s` to change.  No choice of `s` makes this quadruple
Golay.  This does **not** rule out changing both `s` and `q`, a nonspecial
Golay quadruple, a Legendre pair of length 333, or a general Hadamard matrix
of order 668.

The new reduction below is checked by `verify_fixed_q_obstruction.py`.  The
last nonexistence step uses a published Turyn-sequence theorem; the checker
does not pretend to formalize or re-prove that literature result.

## 1. Fixed-q equations

Write

```text
X = s[0:83],       |X|=83,
u = s[84],
Y = s[85:166],     |Y|=81,
v = s[166].
```

The coordinate `s[83]` is isolated.  Exact complementarity is equivalent to

```text
c_k(X)+c_k(Y)=0                 (1 <= k <= 80),
c_81(X)=x_0*x_81+x_1*x_82=0,
x_0*x_82+u*v=0.
```

Here `c_k` is aperiodic autocorrelation at lag `k`.

For `0 <= k <= 81`, let `P_k` be the product of all individual sign terms in
`c_k(X)+c_k(Y)`; the `Y` product is empty at lag 81.  At every positive lag
the zero sum contains `2(82-k)` signs, exactly half negative.  Thus

```text
P_k=(-1)^k,        0 <= k <= 81.
```

On the other hand, cancellation between consecutive products gives

```text
P_(i+1)/P_i
  = (x_i*x_(82-i)) (y_i*y_(80-i)) = -1,    0 <= i <= 80.
```

Set `r_i=x_i*x_(82-i)` and `t_i=y_i*y_(80-i)`.  Reflection gives
`r_i=r_(82-i)` and `t_i=t_(80-i)`.  Comparing the equations at `i` and
`80-i`, then reflecting once more, yields `r_i=r_(i+2)`.  The central
products are `r_41=t_40=1`, so all signs are forced:

```text
x_(82-i)=(-1)^(i+1) x_i,        0 <= i <= 82,
y_(80-i)=(-1)^i y_i,            0 <= i <= 80.
```

The endpoint equation now gives `u*v=1`, hence `u=v`.

## 2. Decimation produces TU(41)

Split the two sequences by parity and add the two endpoint signs to the odd
part of `Y`:

```text
E = (x_0,x_2,...,x_82),           |E|=42,  reverse(E)=-E,
O = (x_1,x_3,...,x_81),           |O|=41,  reverse(O)= O,
P = (y_0,y_2,...,y_80),           |P|=41,  reverse(P)= P,
Q = (y_1,y_3,...,y_79),           |Q|=40,  reverse(Q)=-Q,
B = (u,Q,v),                       |B|=42.
```

Because `Q` is skew and `u=v`, its two endpoint contributions in `c_k(B)`
cancel for `1 <= k <= 40`, leaving `c_k(B)=c_k(Q)`.  Therefore the even-lag
fixed-q equations give

```text
c_k(E)+c_k(B)+c_k(O)+c_k(P)=0,    1 <= k <= 40.
```

At lag 41 the sum is `x_0*x_82+u*v=0`, and the lag-zero energy is 166.
Consequently

```text
(E; B; O; P) in BS(42,41).
```

In the standard definition of Turyn sequences, an element of `BS(n+1,n)` is
in `TU(n)` when its first long sequence is skew and its first short sequence
is symmetric for odd `n`.  Thus the hypothesized fixed-q repair would be an
element of `TU(41)`.

## 3. TU(41) is empty

Đoković records the standard necessary condition: if `n` is odd and
`2n+1` is not a sum of two squares, then both `TU(n)` and `TU(n+1)` are
empty.  Here

```text
2*41+1 = 83,
```

and 83, a prime congruent to 3 modulo 4, is not a sum of two integer squares.
Hence `TU(41)` is empty.  Independently, Edmondson, Seberry, and Anderson's
exhaustive enumeration through long length 42 found Turyn sequences only at
long lengths `2,...,8,13,15`, again excluding `TU(41)`.

Sources:

- Dragomir Ž. Đoković, [Classification of Turyn
  sequences](https://combinatorialpress.com/article/jcmcc/Volume%20027/vol-27-paper%201.pdf),
  *J. Combin. Math. Combin. Comput.* 27 (1998), Sections 10-11, pp. 14-15.
- G. M. Edmondson, Jennifer Seberry, and M. R. Anderson,
  [Turyn sequences of length less than
  43](https://documents.uow.edu.au/~jennie/WEBPDF/1994_03.pdf),
  *J. Statist. Plann. Inference* 40 (1994), Results 3.2.2, p. 358.

## Reproduce the checked reduction

```sh
python3 verify_fixed_q_obstruction.py
```

The expected final line is:

```text
PASS all mechanically checkable obstruction steps
```
