# Exact rank-three coupled-direction stress test

**An independently checked physical example, not a Lean theorem and not a
POVM–PVM separation.** The source proof's general rank-at-least-two argument
remains uncompiled. This example stress-tests its mathematical interfaces by
constructing an exact stationary strategy and an explicit increasing physical
path, without using the implicit-function theorem as a black box.

The complete machine-readable matrices and identities are in
`reports/semantic_audit/rank_three_saddle_certificate.json`. Reproduce them with:

```bash
python3 scripts/semantic_audit.py --suite saddle
```

The checker imports no other project checker and does not interpret Lean. It
uses exact rational/symbolic complex arithmetic, with no numerical tolerances.

## 1. Architecture and base strategy

Both parties have two inputs with output counts **(2,3)**. Index the first four
effects as binary labels 0,1 and ternary labels 0,1. The third ternary label has
zero Bell coefficients. There is **no extra freely available binary label with
zero coefficients**: adding one would change the optimization problem. A padded
source representation must pull the functional back through its coarsening map.

Let I,X,Y,Z be the usual Pauli matrices, including
`Y=[[0,-i],[i,0]]`. Use the singlet density matrix

```
ρ = 1/2 * [[0, 0,  0, 0],
           [0, 1, -1, 0],
           [0,-1,  1, 0],
           [0, 0,  0, 0]].
```

Alice's binary effects are `diag(1,0)` and `diag(0,1)`. Her ternary effects are

```
M0 = (3/8)  (I+X),
M1 = (5/16) (I-(3/5)X+(4/5)Y),
M2 = (5/16) (I-(3/5)X-(4/5)Y).
```

Bob's effects are `U M U†`, input by input, where `U=(3I+4iX)/5`. They are
normalized positive qubit measurements; the ternary effects have rank one.
Define the Bell score by `sum_{i,j=0}^3 Fij Tr(ρ(Ai⊗Bj))`, with

```
F = [[ -9/10,     -2,    6/5,    2/5],
     [ -2/25, -9/10,   6/25, -38/25],
     [  6/25,    6/5, -68/25,  14/25],
     [-38/25,    2/5,  14/25,  28/25]].
```

This convention defines all four input blocks, including the cross-input
blocks, in one fixed functional.

## 2. Exact incidence stationarity of rank three

Let the coefficient rays be `r0=e0`, `r1=e1`, `r2=e2`, `r3=e3`,
`r4=e0+e1-e2-e3`, and `u=e0+e1`. Alice's effect-coordinate matrix E gives

```
g = Eᵀ diag(1,-1,-1,-1) E
  = [[0,    1/2, 3/16, 5/32],
     [1/2,  0,   3/16, 5/32],
     [3/16, 3/16,0,    3/16],
     [5/32, 5/32,3/16, 0   ]].
```

For the physical first-four-effect block P, the frame `Y0=g⁻¹P` is

```
Y0 = [[ -3/5,   8/5, 0,    2/5],
      [-8/25, 33/25, 0,  22/25],
      [24/25,-24/25, 1, -16/25],
      [48/25,-48/25, 0,  -7/25]].
```

The checker derives P directly from the joint-space Born trace, rather than
assuming this frame. All five null equations and positive future pairings hold.
The 4-by-5 matrix with columns `Φ(Y0 rj)` has rank **3**, and its kernel contains

```
λ = (1/4,1/4,1,1,1),  with every entry positive.
```

Set `Λ=sum_j λj rj rjᵀ`. The exact score stationarity identity is
`F=-2Y0Λ`, with normalization multiplier zero. This supplies a concrete
nontrivial fixture for the source's metric-kernel, sign, and normalization
conventions.

## 3. All individual optimization blocks are optimal

With these measurements fixed, the Bell operator is

```
B = (1/64) * [[-75, -3, -3,-11],
              [ -3,-43,-43, -3],
              [ -3,-43,-43, -3],
              [-11, -3, -3,-75]].
```

It has the exact negative Gram certificate

```
-B = (1/2) v1 v1ᵀ + (5/16) v2 v2ᵀ + (23/64) v3 v3ᵀ,
v1=(1,0,0,-1), v2=(1,-1,-1,1), v3=(1,1,1,1).
```

Hence no change of the density matrix alone can exceed score zero, and the
singlet attains zero.

Each of the four individual measurement optimization problems is also optimal
when the state and all other measurements are fixed. The JSON certificate
records its score operators Kj and Hermitian dual Γ. The checker verifies
`Γ-Kj` is positive semidefinite and `(Γ-Kj)Mj=0` for **every actual output**.
Weak duality then certifies global optimality of that one measurement block.
These are not assertions of joint optimality.

## 4. An explicit coupled physical path

For real `|t|≤1/2`, put

```
S(t) = I-(3/10)i t Y,
ρ(t) = (S(t)⊗I) ρ (S(t)†⊗I) / (1+9t²/100).
```

The equality `S†S=(1+9t²/100)I` proves exact normalization; the state stays pure
and positive by its displayed Gram construction.

Keep both binary measurements fixed. Conjugate Alice's ternary effects by

```
UA(t) = [[(100-t²)/(100+t²), -20t/(100+t²)],
         [20t/(100+t²),     (100-t²)/(100+t²)]].
```

For Bob, set `p=2-t`, `q=-2-t` and use planar unit directions

```
n0=(1,0),
n1=((1-p²)/(1+p²),2p/(1+p²)),
n2=((1-q²)/(1+q²),2q/(1+q²)).
```

Their weights are

```
w0=(3-t²)/(2(4-t²)),
w1=((t-2)²+1)/(8(2-t)),
w2=((t+2)²+1)/(8(2+t)).
```

Bob's ternary effects are `U wj(I+nj,x X+nj,y Y) U†`. The checker verifies their
sum is I, their determinants are zero, and each direction is a unit vector.
On the stated interval every weight is positive and every denominator is
nonzero. The positive-factor certificates in the JSON give, for example,
`3-t²≥11/4`, `4-t²≥15/4`, and `2±t≥3/2`. Thus this is an actual qubit strategy
for the whole interval, not merely an incidence solution with assumed physical
reconstruction.

## 5. Direct exact score and increase

Direct substitution into the **full joint-space Born trace** gives

```
f(t) = t²(850000-955000t²-58595t⁴+252t⁶)
       / [40(4-t²)(100+t²)²(100+9t²)].
```

The numerator factor N(t) has the exact certificate

```
N(t) = 9721405/16
       +(1/4-t²)[955000+58595(1/4+t²)]
       +252t⁶.
```

Every term except the positive constant is nonnegative on `|t|≤1/2`. The
denominator is positive. Therefore **f(t)>f(0)=0 for 0<|t|≤1/2**. In particular,

```
f′(0)=0,  f″(0)=17/1600>0,
f(1/2)=f(-1/2)=4860734/4932570675.
```

Additional exact physical evaluations at `t=±1/10` and `±1/100` are recorded.
At all six nonzero test values the checker independently rebuilds the frames
and verifies the finite incidence identity

```
f(t)-f(0) = sum_j λj ((Y(t)-Y0)rj)ᵀ g(t) ((Y(t)-Y0)rj).
```

This is a direct consistency check connecting the physical path to the source's
finite-gap formula. The general differentiable-curve theorem is not thereby
proved.

## 6. Why this is not a POVM–PVM separation

A deterministic local PVM strategy already has score **3/10**: Alice outputs
`(0,0)` on her two inputs and Bob outputs `(0,1)`. Exhausting all 36 local
deterministic assignments confirms their maximum is 3/10 (this is only the
local deterministic maximum, not the complete qubit-PVM optimum).

For the whole interval, the path score satisfies the coarse bound

```
0 ≤ f(t) ≤ 13600063/9600000000 < 3/10.
```

Indeed `t²≤1/4`, `N(t)≤13600063/16`, and the denominator is at least 150000000.
The upper numerator difference is certified as
`955000t²+58595t⁴+252(1/64-t⁶)≥0`. Thus the path does not beat even the displayed
deterministic PVM. The point of the example is precisely that **individual
state/measurement optimality does not eliminate coordinated physical uphill
directions**. It is a stress test, not a counterexample to the main theorem.

## 7. Discovery and verification boundary

A floating-point Hessian exploration suggested a sparse rational direction;
that optional discovery script is retained in `research/`. All reported
identities, matrices, signs, ranks, dual certificates, and finite values were
then recomputed independently by the exact checker. Numerical discovery is not
used as verification evidence.

The positive interval conclusion follows from the displayed symbolic identities
and elementary sign certificates. No Lean elaboration or kernel audit was run.
The example does not prove the all-points rank trichotomy, local Gram lift,
implicit-function theorem application, or global convexified equality.
