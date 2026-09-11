# Proof route and conventions

**Source draft; all Lean proofs remain uncompiled.**

## 1. Global reduction

The physical parameter space is described using Gram factors. Trace and POVM
normalization bound every factor entry, and all constraints are polynomial.
This yields compact raw images. A finite-slot Carathéodory argument establishes
compactness of the ordinary convex hull, not merely its closure. Convex
separation then supplies an extreme maximizing behavior at a hypothetical
strict POVM-over-PVM separator.

A mixed two-qubit density matrix gives a finite assemblage of steered qubit
operators. If the reduced state is singular, the whole assemblage lies on a
single positive ray and the behavior is local. Otherwise an explicit qubit
purification reproduces the entire behavior with a full-Schmidt-rank coefficient
matrix. This is a replacement of the realization, not a same-state assertion.

At an extreme behavior, scalar perturbations detect dependence among nonzero
local effects through strictly positive marginals. Nondeterministic effects are
rank one. A common-span filter is applied to both inputs with the same operator;
its two branch weights are the changed state normalizations. Complete-behavior
extremality forces common-span operators to be scalar. The four-dimensional
Hermitian span count then leaves two or three active outcomes per input and at
least one binary input per party.

## 2. Binary-party case

When one party has two binary-support PVMs, a spatial compression preserves all
its trace pairings. Compressed future vectors are split into null rays in one
three-dimensional hyperplane. Normalized nonnegative balanced weights form a
compact convex polytope. Its extreme points have at most four active rays; a
one-versus-three split is excluded by strict convexity of the null cone, so each
side has at most two rays. Each circuit is whitened and purified into a genuine
qubit PVM strategy. Coarsening restores every original output label.

The same balanced weight vector governs both inputs and all table entries.
The final general one-binary-POVM-party statement also follows from the full
arbitrary-output equality; no circular use of that corollary occurs in the main
proof, which uses only the independently proved binary-PVM case.

## 3. Genuine residual chart

In coefficient space, use

```
r0=e0, r1=e1, r2=e2, r3=e3, r4=e0+e1−e2−e3,
u=e0+e1.
```

Pauli coordinates retain the imaginary component:

```
pauli(t,x,y,z) = [[t+z, x−iy], [x+iy, t−z]],
J = diag(1,−1,−1,−1).
```

The physical effect frame E satisfies `E u=(1,0,0,0)` and `g=Eᵀ J E`.
The four-parameter normalized metric has zero diagonal, `g01=1/2`, and
`g23=g02+g03+g12+g13−1/2`.

Use polynomial coordinates `(p,Y)` with `P=g(p)Y`. The five null constraints are
`(Y rj)ᵀ g(p)(Y rj)=0`; the sixth is `uᵀ P u=1`.

The differential has an explicit right inverse. To prescribe five null values
c, form a symmetric seed with diagonal `c0/2,...,c3/2` and entries
`M01=M10=(c4−c0−c1−c2−c3)/4`. Then `2 rjᵀ M rj=cj`.
The frame increment `P⁻ᵀ M` provides the five desired derivatives. Adding a
multiple of the radial frame Y changes mass by exactly that multiple and leaves
all null derivatives zero. Hence all six derivatives are jointly surjective.

A separate Gram map `E ↦ EᵀJE` has derivative
`D ↦ DᵀJE+EᵀJD`, with right inverse `H ↦ (1/2)J E⁻ᵀH` for symmetric H.
The finite-dimensional implicit-function theorem gives a local Gram lift.
Open future conditions persist, and pointwise normalization plus purification
reconstruct actual complex-qubit strategies. No differentiable choice of
matrix square root or spinor is assumed.

## 4. Stationarity and positive multipliers

Lagrange stationarity is derived from an actual physical maximum transferred
to the local feasible chart. Surjectivity rules out an abnormal objective
multiplier. Frame-only and metric-only variations give

```
F(Q)=α·mass(Q)−2 Σj λj (Y rj)ᵀQ rj,
Σj λj (Y rj)ᵀH(h)(Y rj)=0.
```

A complete deterministic measurement reset Tj preserves u. Its physical behavior
is local, so at a strict separator it has strictly lower Bell value. Exactly,

```
F(P)−F(P Tj)=2 λj (Y rj)ᵀ g(Y u).
```

The final pairing is strictly positive for a nonzero future-null ray and the
future-timelike reduced state. Therefore every λj is positive. The derivation
uses the actual physical reset, not just an algebraic table replacement.

## 5. Rank cases and the C¹ replacement for second variation

For another normalized feasible point `(g',Y')`, stationarity and nullness give
an exact finite identity:

```
F(g'Y')−F(gY)=Σj λj ((Y'−Y)rj)ᵀ g'((Y'−Y)rj).
```

At metric-row rank at least two, the multiplier kernel has dimension at most
three. A four-dimensional positive family of frame directions supplies a
nonzero compatible uphill direction. A compensating metric increment solves
the null derivatives, and a radial correction enforces the *full* normalization
derivative, including its metric term.

The surjective strict derivative produces a C¹ feasible curve with that tangent.
Its scaled exact gap has a strictly positive limit, contradicting local
maximality. No second derivative of matrix inverse is needed.

Rank one is contradicted by the projective-fiber obstruction and positive
multipliers. Rank zero has an explicit labelled common PVM mixture. These
cases exhaust all ranks and close the genuine residual case.

## 6. Final assembly and attained values

Input permutations, zero removal, three-label padding, and output coarsening
are applied to whole strategies. They transport the residual contradiction back
to the original arbitrary finite alphabets. Assembly combines this equality
with the inherited unconditional-source 3×2 separation and the one-input result.

The strengthened witness uses q=√7813, a²=(q+1)/(2q), b²=(q−1)/(2q), k=3b/(5a),
state coefficient diag(a,b), and Alice locking observables with coordinates
z=q/125 and x=2qab/125. The direct Born expansion gives the attained value
`(16+8q)/25`. This is a lower bound, not a claim of global POVM optimality.

## Review boundary

This route explains what the source attempts to establish. It is not an
independent certificate of the long analytic or extremal arguments. The exact
checker addresses finite algebra and rational fixtures only. Every source proof
still requires Lean elaboration and kernel checking, followed by review that
its formal statement matches this intended route.
