# Proof-first local algebra supplement

Status: **DELIBERATELY PARTIAL — EXACTLY VERIFIED WITHIN THE SCOPE BELOW**

## Scope

This supplement independently rebuilds the displayed-tree JC tensors for one
three-port cycle support and five four-port minimum theta supports.  It uses
explicit edge lists and the Fourier displayed-tree sum; it imports no graph,
tensor, invariant, rank, or atlas code from the discovery implementation.

The supplement proves several compact identities and strict open-cube
separations for the most dangerous *canonical* rank-8 versus rank-9
comparisons.  It does **not** prove the bounded local atlas, the
arbitrary-port theorem, or the global identifiability theorem.

The five-port TT-separated core is intentionally excluded.  No topology
census, completion search, elimination, or larger symbolic calculation is
performed.

## Explicit supports

The incoming port is `I`; a repair on segment `j` is `Rj`; a path-sink child
is `K_Xj`.  The four theta supports checked are obtained from these directed
segment lists:

- TR-separated:
  `S->U, S->V, U->X0, V->X0, U->V`, with repairs `{2,3}` (short) or
  `{3,4}` (long);
- TR-nested:
  `S->U, S->X0, V->X0, U->V, U->V`, with repair `{2,3}`;
- TT-nested:
  `S->U, S->X0, V->X0, U->X1, V->X1, U->V`, with repair `{2}` (short)
  or `{4}` (long).

Every repaired edge `u->v` is replaced by `u->Pj->v` and `Pj->Rj`.
Each sink `Xj` has child `K_Xj`, and `I` is pendant at `S`.

## Fourier coordinates

For four ordered ports write `q_i` for the JC coordinate in this fixed order:

| i | character | i | character | i | character |
|---:|:---:|---:|:---:|---:|:---:|
| 0 | 0000 | 5 | 1001 | 10 | 1122 |
| 1 | 0011 | 6 | 1010 | 11 | 1203 |
| 2 | 0101 | 7 | 1023 | 12 | 1212 |
| 3 | 0110 | 8 | 1100 | 13 | 1221 |
| 4 | 0123 | 9 | 1111 | 14 | 1230 |

Here `q_0=1`.  Define the three separated and three nested contrasts

\[
\begin{aligned}
L^S_1&=q_9-q_{10}-q_{12}+q_{13},\\
L^S_2&=q_9-q_{10}+q_{12}-q_{13},\\
L^S_3&=q_9+q_{10}-q_{12}-q_{13},\\
L^N_1&=-q_9-q_{10}+q_{12}+q_{13},\\
L^N_2&=-q_9+q_{10}-q_{12}+q_{13},\\
L^N_3&=-q_9+q_{10}+q_{12}-q_{13}.
\end{aligned}
\]

The two four-term cubics are

\[
\begin{aligned}
C_{TR}={}&q_3q_7q_8+q_4q_6q_8-q_1q_8q_{14}-q_3q_6q_{11},\\
C_{TT}={}&q_2q_7q_8+q_4q_5q_8-q_1q_8q_{11}-q_2q_5q_{14}.
\end{aligned}
\]

## Exact identities

Direct sparse-polynomial expansion proves:

| support and ordered ports | identity |
|---|---|
| TR-separated-short `(I,R2,R3,K_X0)` | `L^S_1=0` |
| TR-nested `(I,R2,R3,K_X0)` | `L^N_1=0`, `C_TR=0` |
| TT-nested-short `(I,R2,K_X0,K_X1)` | `L^N_1=0`, `C_TT=0` |
| TT-nested-long `(I,R4,K_X0,K_X1)` | `L^N_1=0` |

An additional 18-term homogeneous cubic `H`, recorded literally in
`verify_completed.py` as `H_TR_SEP_LONG`, vanishes on TR-separated-long in
the order `(I,R3,K_X0,R4)`.  The script derives its pullback from the graph;
it is not used to claim an ideal or rank upper bound.

The opposite cubics are not identities.  At the deterministic rational point
used by the verifier,

\[
C_{TT}(TR\text{-nested})
=-\frac{309620476890625}{5950856194709078016},
\]

and

\[
C_{TR}(TT\text{-nested-short})
=-\frac{8571875}{218884571136}.
\]

Thus the two nested short supports have distinct complex closures in the
displayed coordinate order.

## Strict open-cube factorizations

All variables below lie strictly between zero and one.  For the
TR-separated-long support, put

\[
B=x_{V P3}
  \bigl(\lambda_Vx_{P4V}+(1-\lambda_V)x_{SV}\bigr)-1<0.
\]

Exact pullback gives

\[
\begin{aligned}
L^S_1={}&2\lambda_V x_{P3R3}x_{P4R4}x_{P4V}x_{SI}x_{SU}
 x_{UX0}x_{VP3}x_{X0K0}
 (\lambda_{X0}-1)(x_{UP4}-1)>0,\\
L^S_2={}&-2\lambda_{X0}x_{P3R3}x_{P3X0}x_{P4R4}x_{SI}x_{SU}
 x_{UP4}x_{X0K0}B>0,\\
L^S_3={}&-2x_{P3R3}x_{P4R4}x_{SI}x_{SV}x_{UP4}x_{UX0}x_{VP3}x_{X0K0}
 (\lambda_V-1)(\lambda_{X0}-1)(x_{SU}-1)>0.
\end{aligned}
\]

Moreover

\[
(L^N_1,L^N_2,L^N_3)=(-L^S_3,-L^S_2,-L^S_1)<0.
\]

Consequently an aligned support on which one of these contrasts vanishes
cannot meet the open TR-separated-long image.  This converts the apparent
lower-to-higher algebraic danger into strict stochastic separation.

For TT-nested-long, direct pullback gives

\[
\begin{aligned}
C_{TR}={}&M_{TR}
(\lambda_{X0}-1)(\lambda_{X1}-1)
(x_{SU}-1)(x_{UV}-1)(x_{SU}x_{UV}-1)<0,\\
C_{TT}={}&M_{TT}
(\lambda_{X0}-1)(\lambda_{X1}-1)
(x_{UV}-1)(x_{VP4}-1)(x_{UV}x_{VP4}-1)<0,
\end{aligned}
\]

where

\[
\begin{aligned}
M_{TR}={}&\lambda_{X0}x_{P4R4}^2x_{SI}^2x_{SU}x_{SX0}x_{UV}x_{UX1}
x_{VP4}^2x_{VX0}x_{X0K0}^2x_{X1K1}>0,\\
M_{TT}={}&\lambda_{X1}x_{P4R4}^2x_{P4X1}x_{SI}^2x_{SU}^2x_{UV}x_{UX1}
x_{VP4}x_{VX0}x_{X0K0}x_{X1K1}^2>0.
\end{aligned}
\]

Since `C_TR=0` on TR-nested and `C_TT=0` on TT-nested-short, these canonical
rank-8 candidates cannot meet the corresponding rank-9 open stochastic
image.  The factors show that the obstruction can disappear only on a
parameter boundary such as `x=1`; no boundary-containment claim is made here.

## Exact Jacobian lower-rank certificates

Parameters are sorted by name and specialized to
`p_j=(j+2)/(j+7)`, which is strictly inside `(0,1)`.  The verifier extracts
the following nonzero exact minors:

| support | rank at the point | certified minor determinant |
|---|---:|---:|
| cycle | 4 | exact rank 4 by the four-dimensional normalized trinet ambient space |
| TR-separated-short | 8 | `-21891891370375/1708031224299477228060672` |
| TR-separated-long | 9 | `652015641829296875/287006551464286815759160915968` |
| TR-nested | 8 | `-410131245200421875/2581288331057650769231609856` |
| TT-nested-short | 8 | `202596695640625/1118902365169455986638848` |
| TT-nested-long | 9 | `-829174082470703125/24472932396820206753969302667264` |

For the cycle, rank 4 is exact because the normalized three-port JC tensor
has only four nonconstant orbit coordinates.  For each four-port support the
minor proves only the displayed generic-rank **lower bound**.  This supplement
does not supply the upper-rank theorem needed to promote 8 and 9 to exact
generic model dimensions.

## What remains unresolved

This supplement does not establish:

1. an upper-rank certificate for the four-port supports;
2. the five-port TT-separated support or its labelled roles;
3. all port permutations, non-core-retaining target marginals, or completion
   directions;
4. a uniform two-sided local-containment theorem;
5. arbitrary-subdivision or local-to-global promotion;
6. the positive standard-strong JC identifiability theorem.

Accordingly, these calculations are a conceptual partial input, not a
replacement for the missing local theorem and not a preprint-level final
classification.

## Reproduction

From the project root:

```sh
bash reviews/proof_first_local_algebra/verify.sh
```

The verifier uses only the Python standard library and normally finishes in
well under one second.
