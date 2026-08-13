# The minimal paired trace-cone lift of BDM

Date: 2026-08-13 (America/Los_Angeles)

No literature search, graph search, or external communication was used.

## Status

**PROVED REDUCTION; EXACT MARGINAL-CONE OBSTRUCTION.**  Pointwise BDM at
`R_hyb` rules out every response-scale dilute limit as soon as the two rules
have a common positive measure on physical module responses.  Equality of
the Bd and dB trace measures is stronger than necessary: one explicit
signed synchronization charge is the minimal remaining condition.

The existing first-exit Schur theorem is rule-by-rule.  It proves positive
marginal trace decompositions but does not prove the required cross-rule
synchronization.  This is a real logical gap.  A leaf and the closed
small-gate `K_2` ray give an exact physical obstruction: separate Bd and dB
marginal measures can assemble a vector in the open positive quadrant even
though every paired generator obeys the BDM separator.

This note proves the BDM lift for the separated dilute normal form and
isolates one scalar inequality that an arbitrary trace-compactness theorem
must add.  It does not prove that every graph sequence admits such a paired
trace.

## 1. Module response space

Fix a fitness `r>1` and put `c=r-1`.  A bounded physical module datum

\[
                     \theta=(H,x,z)                     \tag{1}
\]

consists of its internal weighted graph, positive portal vector, and Bd gate
odds.  The dB gate odds are then `K_theta/z`, with the exact invariant

\[
 K_\theta={r(r-1)^2\over q_Bq_D}.                       \tag{2}
\]

Write its paired normalized dilute response as

\[
 v(\theta)=(B(\theta),D(\theta))                       \tag{3}
\]

and define the leaf-annihilating support

\[
 \mathcal L(B,D)=D+cB.                                  \tag{4}
\]

In the dual coordinates

\[
 b=\rho_{Bd}(H,r),\qquad
 a={\rho_{dB}(H,r)\over r-1},                           \tag{5}
\]

the exact bounded-module formula is

\[
 {\mathcal L(v(\theta))\over |H|}
 =ra{K_\theta\over K_\theta+z}
  +rb{z\over1+z}-r.                                    \tag{6}
\]

BDM at `r=R_hyb` is exactly the assertion that (6) is nonpositive
for every admissible `theta`.

## 2. Exact paired-cone lift

For a graph sequence at the fixed fitness, put

\[
 \Delta_k=(X_k-1,Y_k-1),\qquad
 \epsilon_k=\|\Delta_k\|_\infty.                       \tag{7}
\]

> **Paired trace-cone lift.**  Suppose there are finite positive measures
> `mu_k` on the physical module space and remainders `e_k` such that
>
> \[
> \Delta_k=\int v(\theta)\,d\mu_k(\theta)+e_k,
> \qquad \|e_k\|=o(\epsilon_k).                         \tag{8}
> \]
>
> If BDM holds on the support of every `mu_k`, the sequence cannot satisfy
> `X_k>1` and `Y_k>1` for all sufficiently large `k`.

Indeed, BDM and positivity of `mu_k` give

\[
 \mathcal L(\Delta_k)
 =\int\mathcal L(v(\theta))\,d\mu_k(\theta)
   +o(\epsilon_k)
 \le o(\epsilon_k).                                    \tag{9}
\]

If both coordinates of `Delta_k` are positive, however,

\[
 \mathcal L(\Delta_k)
 \ge\min\{1,c\}\epsilon_k.                             \tag{10}
\]

Equations (9)--(10) contradict one another.  Notice that the error must be
small at the actual response scale, not merely at vertex-density scale.

The exact separated-module normal form has (8): each physical module count
is a common nonnegative coefficient multiplying its already paired vector
`(B,D)`.  Thus BDM, once proved for the admitted modules, already excludes
all separated dilute mixtures, their positive-measure limits, and mixtures
with ordinary leaves, since a leaf has `mathcal L=0`.

### Common-coefficient first-exit lemma

The common coefficient follows from the exact Schur trace; it is not an
extra symmetry assumption.  Partition the fast transient states by physical
module instance,

\[
 A=\bigsqcup_j\bigsqcup_{m=1}^{q_{k,j}}A_{j,m}.         \tag{10a}
\]

Retain the reservoir and every intermodule state in `B`.  If a leading
excursion reaches `B` or absorbs before entering another module, then for
either update rule

\[
 L_{AA}^U=\bigoplus_j\bigoplus_{m=1}^{q_{k,j}}L_j^U.   \tag{10b}
\]

Applying (11) below makes both the local occupation and the first-exit load
additive over the `q_{k,j}` identical blocks.  All rule-dependence --
entrance hazard, reciprocal recovery, local fixation, and baseline
normalization -- belongs inside the coordinate `v_U(theta_j)`.  The
multiplicity/core factor `lambda_{k,j}` is physical and common to both
rules.  Therefore

\[
 \Delta_k=\sum_j\lambda_{k,j}v(\theta_j)+e_k.           \tag{10c}
\]

If paths with two unresolved modules, or with another boundary arrival
before local absorption, contribute `o(epsilon_k)` after uniform averaging,
then `e_k=o(epsilon_k)` and (10c) is (8) with
`mu_k=sum_j lambda_{k,j}delta_{theta_j}`.  This proves the paired lift for
the separated first-exit alternative.  If those paths have
order-`epsilon_k` mass, they remain in the coupled trace and cannot be
declared dilute.

## 3. What first-exit Schur elimination gives by itself

For one rule `U`, the exact killed-chain block identity is

\[
 h_A=\tau_A+H_Ah_B,
 \qquad
 \ell_U^Th_U=\ell_{U,A}^T\tau_{U,A}
 +(\ell_{U,B}^T+\ell_{U,A}^TH_{U,A})h_{U,B}.             \tag{11}
\]

All terms are nonnegative.  After a response-scale module collapse, the two
rule-by-rule identities can therefore yield marginal representations

\[
 \begin{aligned}
 X_k-1&=\int B(\theta)\,d\mu_k^B(\theta)+o(\epsilon_k),\\
 Y_k-1&=\int D(\theta)\,d\mu_k^D(\theta)+o(\epsilon_k),
 \end{aligned}                                         \tag{12}
\]

where both measures are positive.  Equation (12) is not (8).

Put `nu_k=mu_k^B-mu_k^D` and define the nonnegative BDM slack

\[
                        g(\theta)=-\mathcal L(v(\theta)). \tag{13}
\]

Then (12) gives the exact bookkeeping identity

\[
 \boxed{
 \mathcal L(\Delta_k)
 =-\int g\,d\mu_k^D
   +c\int B\,d\nu_k+o(\epsilon_k).}                    \tag{14}
\]

Consequently the weakest synchronization statement needed in this
orientation is the single scalar charge inequality

\[
 \boxed{
 c\int B\,d(\mu_k^B-\mu_k^D)
 \le\int g\,d\mu_k^D+o(\epsilon_k).}                   \tag{15}
\]

The symmetric orientation is

\[
 \int D\,d(\mu_k^D-\mu_k^B)
 \le\int g\,d\mu_k^B+o(\epsilon_k).                    \tag{16}
\]

Either (15) or (16) closes the lift.  A common measure makes the mismatch
term vanish, while total-variation convergence of the measures is more than
is required.  Conversely, no conclusion follows from pointwise BDM and
positivity of the two marginal measures alone.

The obstacle in proving (15) directly from (11) is visible before taking a
limit.  The exact neutral Bd pair load is edge-supported, whereas the dB
load is wedge-supported; their killed Green kernels and first-exit kernels
are also different.  On the frozen path with weights `5,1,1,5`, the exact
local Bd occupation is `12/259` while the local dB occupation is zero.
Thus a common trace measure cannot be obtained by matching the two local
occupation terms atom by atom.  A proof of (15) needs a genuine cross-rule
first-exit change of measure or an adjoint balance across the retained trace.

## 4. Exact obstruction to separate marginal cones

The failure is already physical and algebraic.  Let

\[
                         {3\over2}<r<2,qquad c=r-1.     \tag{17}
\]

An ordinary leaf has response

\[
                         \ell=\left({1\over c},-1\right),
 \qquad \mathcal L(\ell)=0.                             \tag{18}
\]

For `H=K_2`, take the closed response-cone limit `z downarrow 0`.  Since
`rho_dB(K_2,r)=1/2`, formula (6) gives

\[
 v_0=\left(-2,{2-r\over c}\right),qquad
 \mathcal L(v_0)={r(3-2r)\over c}<0.                   \tag{19}
\]

Both rays therefore obey the BDM separator.  Nevertheless, let the Bd
marginal measure select only the leaf and the dB marginal measure select
only `v_0`.  The vector assembled by (12) is

\[
             \left(B(\ell),D(v_0)\right)
             =\left({1\over c},{2-r\over c}\right)>0.  \tag{20}
\]

This is an exact obstruction for every `r` in (17), hence at `R_hyb`.
Although `z=0` is a boundary ray, the same signs hold for every sufficiently
small positive `z`; using the boundary ray is natural because the target in
(8) is the closed response cone.

Thus a theorem asserting only that each rule lies in its own positive
module cone cannot lift BDM.  The physical trace weights must be paired, or
their mismatch must satisfy (15).

## 5. Uniform strict branch and density dilution

There is one useful exact strengthening on the trivial BDM branch.  If a
module satisfies

\[
                              a+b\le1-\gamma             \tag{21}
\]

for `gamma>0`, then both fractions in (6) are at most one, and hence

\[
 \boxed{
 \mathcal L(v(\theta))\le-|H|r\gamma}                  \tag{22}
\]

uniformly over every portal law and gate scale.  If copies of this module
have density `delta_k` and their exact paired trace expansion has error
`o(delta_k)`, (22) produces a negative support of order `delta_k`.  Sending
the density to zero cannot reverse its sign.  Any reversal must have a
trace mismatch or interaction error of the same first response order and
therefore lies outside the paired dilute hypothesis.

More generally, if a nonzero paired packet `v` is replicated at density
`delta_k->0`, then

\[
 \Delta_k=\delta_kv+o(\delta_k),\qquad
 \epsilon_k=\delta_k\|v\|_\infty+o(\delta_k).           \tag{23}
\]

The packet vertices occupy `o(n_k)` source mass but a nonzero fraction of
the response scale.  They may be Schur-traced, but they cannot be deleted.
This is why an upper argument based only on vanishing vertex density, or on
`liminf min(X_k,Y_k)<=1`, misses the actual obligation.

## 6. Remaining exact upper obligation

After the local BDM theorem, the dilute upper bound reduces to one of the
following equivalent-scale tasks:

1. construct a common positive physical-module measure satisfying (8);
2. prove the scalar first-exit synchronization charge (15) or (16);
3. show that every order-`epsilon_k` failure of that charge leaves a
   nonvanishing coupled trace and must be assigned to the bulk alternative.

The rule-by-rule Schur theorem proves none of these automatically.  The
next proof-first target is therefore a cross-rule adjoint identity on the
retained first-exit trace, not a larger catalogue of bounded modules.

## 7. Exact replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
lower_global_tradeoff/verify_paired_trace_cone_lift.py
```

The replay checks (6), the one-charge identity (14), the leaf/`K_2`
obstruction (18)--(20), and the strict-branch factor in (22) over the exact
symbolic field.
