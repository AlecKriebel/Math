# Exact dB classification of symmetric complete-support weighted K4 families

Timestamp: 2026-08-01 (America/Los_Angeles)

**[SCOPE]** This report derives everything from the death--birth rule in the
research prompt.  No literature search or external graph catalogue was used.

**[STATUS KEY]** `PROVED` marks a complete mathematical argument;
`EXACTLY DERIVED` marks exact symbolic elimination from the displayed chain;
`CERTIFIED IDENTITY` marks a replayable polynomial identity;
`INDEPENDENTLY VERIFIED` marks comparison with the separate full subset-state
solver; and `OBSERVATION, NOT PROOF` marks finite exact-rational sampling.

## Results

**[PROVED] 1+3 theorem.**  Let one vertex be the core, give every core--satellite
edge weight one, and give every edge among the three satellites weight `x>0`.
For every `r>1`,

```text
rho_dB(G_13(x),r) <= rho_dB(K_4,r),
```

with equality if and only if `x=1`.

**[PROVED] Parameter-count clarification.**  A fully `S_3`-symmetric 1+3
loopless graph has only two nonempty edge orbits: core--satellite and
satellite--satellite.  The nominal within-core weight in a generic three-weight
two-class notation never occurs because the core class has size one.  After
common scaling, this is therefore a one-parameter family, not a genuinely
two-parameter family.

**[PROVED] 2+2 theorem.**  Partition the vertices into two pairs.  Give the
edge inside the first pair weight `x>0`, the edge inside the second pair weight
`y>0`, and each of the four cross edges weight one.  For every `r>1`,

```text
rho_dB(G_22(x,y),r) <= rho_dB(K_4,r),
```

with equality if and only if `x=y=1`.

**[PROVED] Family-level classification.**  Neither of these two most symmetric
nontrivial complete-support K4 families contains a finite-fitness dB amplifier.
Every nonuniform member is a strict suppressor over the full interval `r>1`.

**[OPEN OUTSIDE THE TWO FAMILIES]**  This report does not prove the same statement
for the unrestricted six-edge weighted `K_4` family.  The exact search reported
at the end found no counterexample, but sampling is not a universal proof.

## Exact orbit chain

**[PROVED] Strong lumpability.**  Let class A have size `p`, class B have size
`q`, and let their internal edge weights be `alpha,beta`, with cross-edge
weight `gamma`.  The group `S_p x S_q` preserves every weighted adjacency and
acts transitively on mutant sets with the same pair of counts `(i,j)`.
The transition probabilities below depend only on `(i,j)`, proving strong
lumpability directly.

**[EXACTLY DERIVED]**  For dB updating, the four possible count changes are

```text
P[(i,j)->(i+1,j)]
 = (p-i)/(p+q)
   * r(i alpha+j gamma)
     / [r(i alpha+j gamma)+(p-i-1)alpha+(q-j)gamma],

P[(i,j)->(i-1,j)]
 = i/(p+q)
   * [(p-i)alpha+(q-j)gamma]
     / [r((i-1)alpha+j gamma)+(p-i)alpha+(q-j)gamma],

P[(i,j)->(i,j+1)]
 = (q-j)/(p+q)
   * r(j beta+i gamma)
     / [r(j beta+i gamma)+(q-j-1)beta+(p-i)gamma],

P[(i,j)->(i,j-1)]
 = j/(p+q)
   * [(q-j)beta+(p-i)gamma]
     / [r((j-1)beta+i gamma)+(q-j)beta+(p-i)gamma].       (1)
```

Terms with zero multiplicity are omitted.  The absorbing states are `(0,0)`
and `(p,q)`.  Thus 1+3 has six transient orbit states and 2+2 has seven.

**[EXACTLY DERIVED] Complete-graph baseline.**  The K4 dB count chain gives

```text
rho_dB(K_4,r) = 3 r^2/[4(r^2+r+1)].                      (2)
```

## Complete 1+3 sign calculation

**[DEFINITION]** Put

```text
F13 = 2r^4x^2 + 2r^4x
      + 11r^3x^2 + 14r^3x + 3r^3
      + 21r^2x^2 + 29r^2x + 12r^2
      + 16rx^2 + 22rx + 8r
      + 4x^2 + 5x + 1,

P13 = 8x^2(x+1)(r^6+1)
      +(6x^4+36x^3+46x^2+16x)(r^5+r)
      +(27x^4+73x^3+85x^2+59x+12)(r^4+r^2)
      +(42x^4+90x^3+106x^2+66x+24)r^3.                (3)
```

**[EXACTLY DERIVED]** Solving the six orbit equations built from (1) gives

```text
rho_dB(G_13(x),r)-rho_dB(K_4,r)
 = -3r^2(r-1)(x-1)^2 F13
   / [4(r^2+r+1)P13].                                 (4)
```

**[PROVED] Sign.**  Every coefficient of `F13` and `P13` is strictly positive.
For `x>0,r>1`, the denominator of (4) is positive and the numerator is negative
unless `x=1`.  At `x=1`, the graph is the unit-weight complete graph and (4)
vanishes identically.  This proves the 1+3 theorem.

## Complete 2+2 sign calculation

**[EXACTLY DERIVED] Rational comparison.**  Solving the seven orbit equations
from (1), cancelling common factors, and writing the reduced positive
denominator polynomial as `P22` gives

```text
rho_dB(G_22(x,y),r)-rho_dB(K_4,r)
 = -r^2(r-1) H22(x,y,r)
   / [4(r^2+r+1)P22(x,y,r)].                          (5)
```

**[CERTIFIED POSITIVITY] Denominator.**  The exact `P22` has 123 strictly
positive integer monomials.  A shorter defining certificate uses the seven by
seven transient state-change matrix `M22` from (1).  Exact determinant
expansion gives

```text
det(M22) = P22/(128 L22),

L22 = (2r+x)(2r+y)(rx+2)(ry+2)
      (r+x+1)(r+y+1)(rx+r+1)(ry+r+1).                (6)
```

Every factor of `L22` is positive.  The finite quotient chain reaches an
absorbing state almost surely, so `M22` is a nonsingular M-matrix and its
determinant is positive.  Thus `P22>0`.  The derivation script independently
checks both (6) and coefficientwise positivity.

### Numerator certificate

**[DEFINITION]** For `x,y>0`, set

```text
g = sqrt(xy) > 0,
d = (sqrt(x)-sqrt(y))^2 = x+y-2g >= 0,
t = r-1 > 0.                                         (7)
```

Because `H22` is symmetric in `x,y`, it is a polynomial in `x+y` and `xy`.
Substituting `x+y=2g+d`, `xy=g^2` is therefore exact.

**[CERTIFIED IDENTITY]** Under (7), exact symmetrization and expansion gives

```text
H22 = C0(g,t) + C1(g,t)d + C2(g,t)d^2
      + C3(g,t)d^3 + C4(g,t)d^4.                     (8)
```

The coefficients are as follows.  First,

```text
C0 = 2t(g-1)^2(g+1)(t+1)R0,

R0 = (2g^2+2g)t^4
     +(g^3+10g^2+21g+6)t^3
     +(3g^3+26g^2+61g+38)t^2
     +(4g^3+32g^2+80g+64)t
     +2g^3+16g^2+40g+32.                             (9)
```

Next,

```text
C1 = 2(g^4+4g^3-2g^2+4g+1)t^6
     +(11g^4+108g^3+76g^2+60g+17)t^5
     +2(40g^4+288g^3+393g^2+176g+19)t^4
     +(16g^5+331g^4+1704g^3+2766g^2+1360g+39)t^3
     +2(28g^5+337g^4+1426g^3+2399g^2+1378g+12)t^2
     +2(g+2)(32g^4+263g^3+722g^2+661g+2)t
     +24g(g+2)(g+4)(g^2+4g+5),                       (10)

C2 = 2(g^2+1)t^6
     +3(9g^2+26g+5)t^5
     +2(18g^3+120g^2+321g+44)t^4
     +2(2g^4+105g^3+525g^2+1071g+170)t^3
     +(14g^4+474g^3+2201g^2+3648g+689)t^2
     +2(8g^4+240g^3+1080g^2+1587g+331)t
     +6(g^4+30g^3+133g^2+186g+40),                   (11)

C3 = 13t^5 +(6g^2+48g+107)t^4
     +(35g^2+312g+357)t^3
     +(79g^2+744g+608)t^2
     +(80g^2+768g+529)t
     +6(5g^2+48g+31),                                (12)

C4 = 6t^4+39t^3+93t^2+96t+36.                       (13)
```

**[PROVED] Coefficient signs.**  Every coefficient of `R0,C2,C3,C4` is
strictly positive.  In `C1`, the only superficially negative monomial occurs
inside its leading coefficient, but

```text
g^4+4g^3-2g^2+4g+1
 = (g^2-1)^2 + 4g(g^2+1) > 0                        (14)
```

for `g>0`.  All other coefficients of `C1` are strictly positive.  Therefore

```text
C0 >= 0,       C1,C2,C3,C4 > 0                      (15)
```

for `g>0,t>0`.

**[PROVED] Strictness.**  If `d>0`, the term `C1 d` makes `H22>0`.  If `d=0`,
then `x=y=g`; equation (9) makes `H22=C0>0` unless `g=1`.  The sole zero is
therefore `g=1,d=0`, equivalently `x=y=1`.  Combining this with (5)--(6)
proves the 2+2 theorem.

## Exact finite-r search beyond the two families

**[EXACT GRID OBSERVATION, NOT PROOF]**  The script `search_exact_k4.py` checked
all 1,352 combinations from 13 rational `x` values, 13 rational `y` values,
and eight rational fitness values in the 2+2 family.  It found zero positive
comparisons.  The theorem above supersedes this observation for 2+2.

**[EXACT RANDOM OBSERVATION, NOT PROOF]**  With deterministic seed `20260801`,
the same script checked 5,000 unrestricted positive six-edge K4 trials with
rational fitness values.  Every Markov chain and comparison was solved using
`fractions.Fraction`, without floating point.  It found no dB amplifier.
This does not classify the unrestricted six-parameter family.

## Replay and independent verification

**[EXACTLY COMPUTED]**  Run the independent orbit derivation and sign
certificates with

```bash
./.venv/bin/python phase2_n4/derive_lumped_certificates.py
```

The script constructs (1), solves both quotient chains, verifies (3)--(14),
checks all claimed coefficient signs, and verifies the determinant identity
(6).  It does not import `src.exact_markov`.

**[INDEPENDENTLY VERIFIED]**  Run

```bash
./.venv/bin/python phase2_n4/crosscheck_full_chain.py
```

This uses the separate full subset-state implementation.  It checks every
transition row, proves both count partitions strongly lumpable symbolically,
solves the resulting quotient independently, and compares four full
14-transient-state rational-weight solutions to the family formulas.

**[OBSERVATION REPLAY]**  Run the finite exact search with

```bash
./.venv/bin/python phase2_n4/search_exact_k4.py
```

The default 5,000-trial unrestricted search and the 1,352-point family grid
complete using exact rational arithmetic.
