# The finite-time harmonic-baseline frontier at fitness two

Date: 2026-08-08 (America/Los_Angeles)

## Status

The following single sign is a sufficient replacement for all of the
pointwise PGF and active-CDF conjectures refuted in this folder:

\[
 \boxed{a_t:=\nu_KK_P^tH\ge a_0={1\over m_K}
        \quad\hbox{for every integer }t\ge0.}        \tag{FT-H}
\]

Here `K_P` is the exact forward active chain, `nu_K` is the complete active
law, and `H(B,v)=1/|B|`.  The status of `(FT-H)` is **OPEN**.  It has been
proved at `t=0,1,2`; the `t=2` case is the inherited exact sum-of-squares
theorem.  It survives the exact and numerical screens recorded below.

This note proves three useful reductions.

1. `(FT-H)` implies the universal stationary collision inequality by Cesaro
   averaging.
2. At each time, `(FT-H)` is exactly one weighted sum of active-rank CDF
   excesses, not pointwise CDF domination.
3. Pointwise finite-time CDF domination is **EXACTLY FALSE**: on the frozen
   reversible six-vertex rank-tail graph, the singleton CDF excess first
   becomes negative at time `88`, while the weighted harmonic gap remains
   strictly positive.

Thus the named remaining sign is `(FT-H)`, equivalently the cumulative
weighted rank-flux inequality `(FT-FLUX)` below.

## 1. Exact active chain and baseline

Let `n>=3`, `N=n-1`, and let `P` be any loopless row-stochastic replacement
kernel.  The active states are

\[
 \mathcal Y=\{(B,v):\varnothing\ne B\subseteq V\setminus\{v\}\}.
\]

From `(B,v)`, the active chain has the following direct experiment.

- With probability `1/2`, retain `v`, sample `i` from row `P_v`, and move to
  `(B union {i},v)`.
- With probability `1/2`, choose `w` uniformly from `B`, delete `w`, sample
  `i` from row `P_w`, and move to `((B minus {w}) union {i},w)`.

The complete active law and harmonic observable are

\[
 \nu_K(B,v)={|B|\over nN2^{N-1}},
 \qquad H(B,v)={1\over|B|}.                          \tag{1}
\]

Consequently

\[
 a_0=\nu_KH={2^N-1\over N2^{N-1}}={1\over m_K}.     \tag{2}
\]

Conjugating `P` by a vertex permutation conjugates `K_P`, while both
`nu_K` and `H` are invariant.  Averaging all conjugates of `P` gives the
complete replacement kernel.  Linearity in one step therefore gives

\[
                            a_1=a_0.                 \tag{3}
\]

The inherited two-step calculation gives

\[
 a_2-a_0=A_nD_1(P)+B_nD_2(P)\ge0,                  \tag{4}
\]

with positive constants and the previously certified squared row,
column, and reversal defects.  No all-time inference is made from (4).

## 2. Exact implication by Cesaro averaging

For a connected undirected weighted graph, the active chain has a unique
stationary law `nu` (periodicity is harmless).  The exact marked-lift
identity is

\[
                            \nu H={1\over m}.         \tag{5}
\]

The finite-chain Cesaro theorem gives

\[
 \lim_{T\to\infty}{1\over T}\sum_{t=0}^{T-1}a_t
 =\nu H={1\over m}.                                 \tag{6}
\]

If `(FT-H)` holds, (6) yields

\[
 {1\over m}\ge {1\over m_K},\qquad m\le m_K,       \tag{7}
\]

which is exactly complete-graph maximality for dB fixation at fitness two.
The conclusion needed for the threshold obstruction is non-strict, so no
separate persistence-of-strictness argument is required.

## 3. The weakest rank statement at a fixed time

Let `q_{t,k}` be the rank law of `nu_KK_P^t` and let

\[
 q^K_k={\binom{N-1}{k-1}\over2^{N-1}},
 \qquad
 C_{t,j}=\sum_{k=1}^j(q_{t,k}-q^K_k).               \tag{8}
\]

Discrete summation by parts, using total mass zero, gives the exact identity

\[
 \boxed{
 a_t-a_0
 =\sum_{j=1}^{N-1}{C_{t,j}\over j(j+1)}.}           \tag{9}
\]

Thus `(FT-H)` asks for only the weighted aggregate in (9).  It does not ask
for `C_{t,j}>=0` separately.

There is an equivalent flux form.  Under the law at time `s`, let
`U_{s,j}` be the total probability flux from rank `j` to rank `j+1`, and
let `D_{s,j+1}` be the total reverse-rank flux.  The exact active transition
rule gives

\[
 U_{s,j}={1\over2}\sum_{|B|=j}\mu_s(B,v)(1-P_{vB}),                 \tag{10}
\]

\[
 D_{s,j+1}={1\over2(j+1)}
 \sum_{|B|=j+1}\mu_s(B,v)\sum_{w\in B}P_{wB}.       \tag{11}
\]

Rank conservation across a cut says

\[
 C_{s+1,j}-C_{s,j}=D_{s,j+1}-U_{s,j}.               \tag{12}
\]

Combining (9) and (12), and using `C_{0,j}=0`, makes `(FT-H)` exactly

\[
 \boxed{
 \sum_{s=0}^{t-1}\sum_{j=1}^{N-1}
 {D_{s,j+1}-U_{s,j}\over j(j+1)}\ge0
 \quad(t\ge1).}                                    \tag{FT-FLUX}
\]

This is the minimal finite-history sign isolated here.  Individual flux
packets and individual rank cuts can have either sign; only their fixed-time
weighted aggregate is conjectured nonnegative.

## 4. Exact finite-time CDF counterexample

Take the complete weighted graph on six vertices with lexicographic edge
weights

```text
(1,3,3,1000,30,1000,300,3,1,10,1,30,1,300,30).
```

This is the frozen stationary rank-tail witness.  Starting the exact
186-state active chain from `nu_K`, rational iteration gives

\[
 C_{87,1}=3.8892605923\ldots\times10^{-5}>0,         \tag{13}
\]

but

\[
 C_{88,1}=-7.6403241333\ldots\times10^{-7}<0.       \tag{14}
\]

The verifier checks the sign in (14) over `QQ`; its reduced numerator has
1062 decimal digits.  At the same time,

\[
 a_{88}-a_0=0.0473650197701\ldots>0.                \tag{15}
\]

and (9) holds exactly.  Therefore the stronger assertion

\[
 C_{t,j}\ge0\quad\hbox{for every }t,j
\]

is **EXACTLY REFUTED**, even on a positive complete-support reversible
kernel.  This explains why a proof of `(FT-H)` must group rank cuts with the
specific harmonic weights in (9), or group the fluxes in `(FT-FLUX)`.

## 5. Verification and remaining sign

Run

```text
.venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/r2_pgf_order/verify_finite_time_harmonic_frontier.py
```

The verifier independently:

1. constructs all 186 active transition rows over `QQ` from the update rule;
2. checks row normalization and the complete active law;
3. checks (9) and `(FT-FLUX)` at every step through time 88;
4. certifies `a_0=a_1`, the positive two-step gap on the witness, (13)--(15),
   and nonnegativity of every sampled harmonic gap.

The last item is finite evidence only.  The single universal proof
obligation left by this route is:

\[
 \boxed{\text{OPEN `(FT-H)`: prove }\nu_KK_P^tH\ge\nu_KH
 \text{ for every }t\ge0\text{ and every reversible loopless }P.}
\]
