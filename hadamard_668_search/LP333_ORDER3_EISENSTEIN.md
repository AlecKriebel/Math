# Eisenstein reduction for the order-three LP(333) quotient

## Status

The modulo-three row compression of the viable order-three column-multiplier
quotient has an exact factorization that is substantially smaller than its
direct Gaussian formulation.

Each of the 100 Gaussian states in one cyclotomic class is exactly a pair of
ten-state binary residue profiles. After taking the nontrivial Fourier
coefficient on the three compressed rows, the full problem becomes:

> Find two `H`-invariant Eisenstein-integer sequences on `F_37` whose summed
> Hermitian periodic autocorrelation is `167` at zero and `0` elsewhere.

Here `H={1,26,10}`. The twenty reversal-independent real correlation
equations contain seven fixed-sum dependencies, leaving one real energy
equation and six Eisenstein equations, or thirteen integer equations.

An exact local reduction modulo three keeps 3,334 of the 10,000 choices on
each of the six pairs of opposite cyclotomic classes. This is a real finite
sieve, but it is not decisive: it neither supplies a compressed witness nor
proves the compressed system infeasible.

Every exact count and identity in this note is replayed by
`verify_lp333_order3_mod3_sieve.py` using only the Python standard library.

## 1. The ten-state factorization

Write a fourth root of unity as a pair of binary signs:

```text
q = (A+B + i(B-A))/2,       A,B in {+1,-1}.
```

For a normalized binary word of length nine and plus-weight three, let

```text
p=(p0,p1,p2),       p0+p1+p2=3,
```

where `pa` counts plus signs in rows congruent to `a modulo 3`. Its compressed
binary triple is

```text
v(p)=(2p0-3, 2p1-3, 2p2-3).
```

There are exactly ten such profiles. In an even cyclotomic class, `A` is the
complement of a normalized word and `B` is normalized; in an odd class the
roles reverse. With

```text
epsilon_j=(-1)^j,
```

the actual compressed triples are therefore

```text
A_j = -epsilon_j v(p_A,j),
B_j =  epsilon_j v(p_B,j).
```

Choosing `p_A,j` and `p_B,j` independently gives exactly `10*10=100`
Gaussian compressed states. The lift count of a profile is

```text
L(p)=binom(3,p0) binom(3,p1) binom(3,p2).
```

The ten lift counts sum to `84=binom(9,3)`, so the 100 state multiplicities
sum to `84^2=7,056`, the exact number of class words with phase sum `-3i` or
`+3i`. Their multiplicity histogram is

```text
 multiplicity     states
            1          9
            9         36
           27          6
           81         36
          243         12
          729          1
```

## 2. Eisenstein coefficients

Let `omega^2+omega+1=0`. Associate to a profile

```text
z(p)=p0+p1 omega+p2 omega^2
    =(p0-p2)+(p1-p2) omega.
```

The ten values consist of

```text
one value of norm 0,
six values of norm 3,
three values of norm 9.
```

For any binary compressed triple `v=(v0,v1,v2)` with even pairwise
differences, define

```text
F(v)=(v0+v1 omega+v2 omega^2)/2
    =((v0-v2)+(v1-v2) omega)/2.
```

Then `F(v(p))=z(p)`. The canonical zero column has compressed binary triples

```text
A_0=(-1,1,1),       B_0=(3,-1,-1),
```

and hence

```text
F(A_0)=-1,          F(B_0)=2.
```

Define two Eisenstein sequences on `F_37` by

```text
a(0)=-1,       b(0)=2,

a(c)=-epsilon_j z(p_A,j),
b(c)= epsilon_j z(p_B,j),       c in C_j.
```

They are constant on the twelve classes `C_j=2^j H`.

## 3. Exact correlation equivalence

For two binary triples `v,u`, put

```text
d_h(v,u)=sum_r v_r u_(r+h),       h=0,1,2.
```

Direct expansion in the basis `1,omega` gives the bilinear identity

```text
4 F(v) conjugate(F(u))
  = (d_0-d_1) + (d_2-d_1) omega.                 (1)
```

Let `D_h(t)` be the sum of the compressed `A` and `B` correlations at row
lag `h` and column lag `t`. Let

```text
R(t)=sum_c [
  a(c) conjugate(a(c+t)) +
  b(c) conjugate(b(c+t))
].
```

Summing (1) over the columns yields

```text
4 R(t) =
  (D_0(t)-D_1(t)) +
  (D_2(t)-D_1(t)) omega.                         (2)
```

The QPSK/sign-pair identity gives `D_h(t)=2 C_h(t)`, where `C_h` is the real
QPSK correlation of the `3 by 37` compressed array.

The trivial row Fourier channel is already fixed by the alternating phase
sums. Its two binary column sequences have summed autocorrelation

```text
D_0+D_1+D_2 =
    650,       t=0,
    -18,       t!=0.                             (3)
```

Equations (2) and (3) are invertible over the integers. Consequently,

```text
R(0)=167, R(t)=0 for t!=0
```

is equivalent to

```text
(D_0,D_1,D_2)=(662,-6,-6),       t=0,
(D_0,D_1,D_2)=(-6,-6,-6),        t!=0,
```

and hence to the exact QPSK targets

```text
(C_0,C_1,C_2)=(331,-3,-3),       t=0,
(C_0,C_1,C_2)=(-3,-3,-3),        t!=0.
```

Thus the entire compressed problem is precisely the complementary
Eisenstein-autocorrelation equation

```text
a*a^* + b*b^* = 167 delta_0.                    (4)
```

This is an equivalence, not a relaxation.

## 4. Why twenty equations reduce to thirteen

Before using the fixed trivial Fourier channel, reversal leaves:

```text
2 equations at column lag zero,
6 row-lag-zero equations on nonzero opposite-class pairs,
12 row-lag-one equations on the twelve nonzero classes,
```

for a total of twenty.

At column lag zero, (3) makes one of the two equations dependent. For each
of the six pairs `C_s,-C_s`, (3) makes one of the three displayed real
equations dependent. This accounts for

```text
1 + 6 = 7
```

dependencies. Equation (4) retains one real origin equation and six complex
nonzero-class equations:

```text
1 + 6*2 = 13
```

independent integer conditions.

## 5. The 22 aggregate shards

The exact 1,756-word row-sum catalog has SHA-256

```text
e8631dc0ae2f65c475af1c2e13429778f666a0fa8a13c9f1153d07d7883a98ea
```

Compressing its class aggregate to the three row residues yields exactly
22 distinct states. Each fixes the values `a(1),b(1)`. Their Eisenstein norm
pairs are:

```text
(19,148)   multiplicity 4
(28,139)   multiplicity 4
(64,103)   multiplicity 2
(91, 76)   multiplicity 8
(100,67)   multiplicity 2
(163, 4)   multiplicity 2.
```

Every pair sums to 167, as (4) requires at the trivial additive character.
The compact replay hash of the full 22-shard table, including shard sizes,
binary aggregates, Eisenstein values, and norms, is

```text
fe575c38060412cd15fa0bad385c1aaee988bbb3303b9b2493463d2feb421e4d
```

## 6. Exact local sieve modulo three

Put `pi=1-omega`, so `pi conjugate(pi)=3`. For every profile,

```text
z(p) is divisible by pi
```

because substituting `omega=1 modulo pi` gives
`p0+p1+p2=3`. Therefore every product
`z(p) conjugate(z(q))` is divisible by three.

Fix a nonzero shift in `C_s`. In its correlation equation, all summands
whose two column positions are nonzero vanish modulo three. Only the terms
through columns `0` and `-t`, the latter lying in `C_(s+6)`, remain. After
substituting `a(0)=-1`, `b(0)=2`, and the parity signs, their vanishing is
equivalent to

```text
f(p_A,s,p_A,s+6) = f(p_B,s,p_B,s+6) modulo 3,   (5)

f(p,q)=conjugate(z(p))+z(q).
```

Across the 100 ordered profile pairs, `f` has exactly three values:

```text
(0,0)   34 times,
(1,2)   33 times,
(2,1)   33 times
```

in the basis `1,omega` modulo three. Joining equal signatures in (5) leaves

```text
34^2+33^2+33^2 = 3,334
```

of the `10^4=10,000` four-profile choices on each opposite-class pair.
Across all six pairs this changes the raw profile space from

```text
10^24 = 1,000,000,000,000,000,000,000,000
```

to the exact necessary-condition space

```text
3334^6 = 1,373,389,026,282,611,799,616.
```

This factor `about 729` reduction is useful but plainly not an exhaustive
solution. Cross-pair correlation equations remain.

The compact hash of the mod-three signature table and space counts is

```text
77cdcd5adc7fd8d301b8a66d5edc91810e2a2861e395e75fe2244b1b25aeacdb
```

The sieve can also be joined exactly with the 22 aggregate targets and the
origin norm `54` for the 24 nonzero-class profile coefficients. A pinned
profile-ID witness exists for every target: all 22 aggregate shards survive
this combined local reduction. Their compact witness-table hash is

```text
4903107d03fc757a72d14d52d555cb9cc257aa0e8480ca22c7474ba365cf6ddc
```

These witnesses satisfy only the aggregate, origin-energy, and local
mod-three conditions. They are not witnesses for the six remaining complex
cross-pair correlations.

## 7. Bounded solver pilot

An exploratory CP-SAT model used the ten-state factorization, the 22-state
aggregate join, the energy equation, and the thirteen independent integer
conditions. Its exact model counts were

```text
variables                 1,344
constraints               1,287
cached product variables  1,242
workers                        4
time limit                  120 s
```

At `120.024` seconds it returned

```text
UNKNOWN
conflicts  387,475
branches   708,771
max RSS    188.5 MiB
```

It found no feasible point. `UNKNOWN` proves neither infeasibility nor
feasibility, so no mathematical claim depends on this pilot.

## 8. Replay and scope

Run:

```sh
python3 verify_lp333_order3_mod3_sieve.py
python3 -m unittest -v test_lp333_order3_mod3_sieve.py
```

The verifier pins:

```text
profile catalog:
1caec75c4e44fc144fcb86e89db63a1b8d7c9acd92ebb05d417ef1cafd2708f0

100-state lift multiplicities:
7e04ca5139fb759d663d2b2263951f81accc21ef98def39733ba4d9e93165489
```

What is established:

- the 100-to-`10 by 10` state factorization;
- the exact Eisenstein complementary-autocorrelation equivalence;
- the reduction from twenty to thirteen independent integer equations;
- the complete 22-shard norm-pair census;
- the exact 3,334-of-10,000 local mod-three sieve;
- explicit proof that all 22 aggregate shards survive that local sieve plus
  the origin energy.

What is not established:

- no compressed witness has been found;
- the compressed system has not been proved infeasible;
- no `LP(333)`, `H(668)`, or Hadamard candidate is claimed.
