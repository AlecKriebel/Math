# Product route and the exact `r=3/2` drift bridge

Date: 2026-08-02 (America/Los_Angeles)

No literature search or external contact was used.

## Status

The proposed universal product inequality

\[
 \rho_{\rm Bd}(G,3/2)\rho_{\rm dB}(G,3/2)
 \le
 \rho_{\rm Bd}(K_n,3/2)\rho_{\rm dB}(K_n,3/2)                 \tag{1}
\]

is **OPEN**.  It would immediately rule out simultaneous amplification at
`r=3/2`, and hence combine with the proved lower construction to give
`R_sim=3/2`.

This note records two exact advances and the finite diagnostics:

1. (1) is **PROVED** for every positively weighted triangle, with a
   manifestly nonnegative 24-atom polynomial certificate.
2. The complete-graph dB harmonic at `r=3/2` has an unexpectedly simple
   closed form.  Applying it on an arbitrary graph gives an exact bridge
   between the dB harmonic defect and the Bd cut imbalance, with only one
   signed cut deviation and two explicit dispersion losses left over.

Neither statement proves (1) in arbitrary order.

## 0. Exact local log-product audit

The complete graph is a critical point of each uniformly initialized
fixation probability by permutation symmetry and scale invariance.  The
space of zero-sum symmetric edge perturbations splits into two irreducible
permutation modes:

* a vertex-degree mode `H_ij=a_i+a_j`, with `sum_i a_i=0`;
* a zero-row-sum cycle mode.

The exact full-chain differentiator constructs `A(epsilon)u(epsilon)=
b(epsilon)` and solves

\[
 A_0u_1=b_1-A_1u_0,
 \qquad
 A_0u_2=b_2-A_2u_0-2A_1u_1.                           \tag{0}
\]

For `n=4,5,6,7`, both eigenvalues of the Hessian of
`log(rho_Bd rho_dB)` are exact negative rationals.  In the cycle mode the Bd
second variation is exactly zero, as required by the isothermal theorem,
and the dB term is strictly negative.  The companion verifier prints all
exact fractions.

This is an **EXACT LOCAL RESULT** only.  No claim of global log concavity is
made; radial monotonicity toward the complete graph is numerically false far
from it.

## 1. Exact complete dB harmonic

Put `q=2/3`.  For the dB chain on `K_n`, let `Phi_D(k)` be the fixation
probability from `k` mutants.  Directly solving its one-dimensional harmonic
recurrence gives

\[
 \boxed{
 \Phi_D(k)=
 {n-(n+k/2)q^k\over n(1-q^{n-1})}.}                    \tag{2}
\]

Indeed, if `Delta_k=Phi_D(k)-Phi_D(k-1)`, the complete dB up/down rates give

\[
 {\Delta_{k+1}\over\Delta_k}
 =q\,{n+k/2-1\over n+k/2-3/2}.
\]

Consequently

\[
 \Delta_k={q^{k-1}(n+(k-3)/2)\over
                 3n(1-q^{n-1})}.                       \tag{3}
\]

Formula (2) yields the usual complete baseline at `k=1`, but it was derived
here from the update rule rather than imported as a fixation formula.

## 2. Arbitrary-graph defect decomposition

Fix a nonabsorbing mutant set `S` of size `k`.  Write

\[
 x_i={\sum_{j\in S}w_{ij}\over d_i},\qquad
 T_S=\sum_i x_i=\sum_{j\in S}t_j,
\]

and let

\[
 B(S)=\sum_{i\notin S}x_i,
 \qquad B_0(k)={k(n-k)\over n-1}.
\]

Thus the unnormalized Bd complete-harmonic defect is

\[
 A(S)-B(S)=k-T_S.                                      \tag{4}
\]

Set

\[
 \alpha={k\over n-1},\quad
 \beta={k-1\over n-1},\quad
 A_k=n+k/2-1,\quad A_{k-1}=n+k/2-3/2,
\]

and

\[
 C_R={4A_k\over(2+\alpha)^2}
     ={2(n-1)^2\over2n+k-2},
 \qquad
 C_M={6A_{k-1}\over(2+\beta)^2}
     ={3(n-1)^2\over2n+k-3}.
\]

After removing the positive common factor in (3), the drift of `Phi_D` on
the arbitrary dB chain is

\[
 \mathcal D(S)=
 A_k\sum_{i\notin S}{x_i\over1+x_i/2}
 -A_{k-1}\sum_{i\in S}{1-x_i\over1+x_i/2}.             \tag{5}
\]

The elementary exact tangent identities

\[
 {2x\over2+x}-{2y\over2+y}-{4(x-y)\over(2+y)^2}
 =-{4(x-y)^2\over(2+x)(2+y)^2},
\]

\[
 {2(1-x)\over2+x}-{2(1-y)\over2+y}
 +{6(x-y)\over(2+y)^2}
 ={6(x-y)^2\over(2+x)(2+y)^2}
\]

give the exact decomposition

\[
 \boxed{
 \begin{aligned}
 \mathcal D(S)
 &=C_M(T_S-k)-(C_M-C_R)\{B(S)-B_0(k)\}\\
 &\quad-C_R\sum_{i\notin S}{(x_i-\alpha)^2\over2+x_i}
       -C_M\sum_{i\in S}{(x_i-\beta)^2\over2+x_i}.
 \end{aligned}}                                       \tag{6}
\]

Moreover

\[
 C_M-C_R
 ={(n-1)^2(2n+k)\over(2n+k-3)(2n+k-2)}>0.             \tag{7}
\]

Combining (4) and (6) cancels the temperature imbalance exactly:

\[
 \boxed{
 \mathcal D(S)+C_M\{A(S)-B(S)\}
 =-(C_M-C_R)\{B(S)-B_0(k)\}-\mathcal E(S),}            \tag{8}
\]

where `E(S)` is the sum of the two nonnegative dispersion terms in (6).

Equation (8) is the sharpest statewise Bd--dB bridge found in this route.
It also displays the unresolved obstruction precisely: the signed row-cut
deviation `B(S)-B_0(k)` can be negative.  For example, on the four-cycle
with two adjacent mutants the dB complete-harmonic drift is positive.  Thus
discarding the cut term, or asserting a common pointwise superharmonic
correction, is invalid.

## 3. Exact weighted-triangle product certificate

For a triangle with positive edge weights `a,b,c`, direct solution of both
six-state absorbing chains gives

\[
 \rho_{\rm Bd}(K_3,3/2)\rho_{\rm dB}(K_3,3/2)
 -\rho_{\rm Bd}(G,3/2)\rho_{\rm dB}(G,3/2)
 ={N(a,b,c)\over Q(a,b,c)}.                            \tag{9}
\]

Every coefficient of `Q` is strictly positive.  The numerator has the
manifestly nonnegative representation

\[
 N=\sum_{(i,j,k),\gamma\in\mathcal C}
 \gamma\sum_{(x,y,z)\in\operatorname{Perm}(a,b,c)}
 x^iy^jz^k(x-y)^2,                                    \tag{10}
\]

where the exact 24-term coefficient table `C` is embedded in the verifier.
All coefficients are positive.  Its first atom has `(i,j,k)=(0,8,8)`, so
for positive weights equality forces `a=b=c`.  Hence (1) is strict on every
nonconstant positively weighted triangle.

## 4. Diagnostics and falsified stronger routes

The independent numerical programs build both full subset chains and delete
only state-dependent self-loops.

* Every connected unweighted graph through order seven was evaluated: 995
  isomorphism classes in total, including all 853 classes of order seven.
  No sum, product, or complete-tangent violation was found; the complete
  graphs attained equality.
* Weighted dense/sparse random and multistart searches covered more than one
  million order-four instances, several hundred thousand instances of
  orders five and six, and tens of thousands of order seven, with edge
  scales separated by as much as `exp(20)` in the stable runs.  No verified
  product violation was found.
* A much more extreme floating candidate, with effective edge ratios around
  `10^25`, was a pivoted-double-precision artifact.  Re-evaluation after
  deleting self-loops analytically and with resolvable rational scales gave a
  negative gap.  It is not a counterexample.
* The common-correction ansatz
  `L_B(Phi_B+h)<=0`, `L_D(Phi_D-h)<=0` is infeasible already on weighted
  paths.  The baseline-weighted version that would prove the tangent product
  bound is also infeasible.  This falsifies that certificate architecture,
  not the fixation inequality.

All search statements are **NUMERICALLY OBSERVED**.  Only Sections 1--3 are
proved exactly.
