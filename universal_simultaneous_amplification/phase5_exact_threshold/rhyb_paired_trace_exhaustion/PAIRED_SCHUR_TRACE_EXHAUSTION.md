# Paired Schur-trace exhaustion at the hybrid endpoint

Date: 2026-08-13 (America/Los_Angeles)

No graph search, literature search, or external communication was used.

## 1. Status

**PROVED CONDITIONAL REDUCTION.**  Assume the bounded dual-moment
inequality (BDM) at

\[
                         r=R_{\rm hyb},\qquad c=r-1,
\]

for every finite physical module and every portal law.  Then a hypothetical
simultaneous amplifier sequence has the following exact dichotomy for every
attempted physical Schur peeling:

1. the paired separated packets exhaust the response at its first nonzero
   scale, in which case BDM gives an immediate contradiction; or
2. the retained, still-coupled Schur trace carries positive
   `D+cB` charge of order the full response scale.

More precisely, if

\[
 \Delta_k=(X_k-1,Y_k-1),\qquad
 \epsilon_k=\|\Delta_k\|_\infty,
\]

and the exact physical peeling is

\[
 \Delta_k=\int v(\theta)\,d\mu_k(\theta)+\tau_k,       \tag{1}
\]

where `mu_k` is a positive measure with one **common physical coefficient**
for the Bd and dB coordinates, then every eventually simultaneous amplifier
satisfies

\[
 \boxed{
 \mathcal L(\tau_k)
 \ge c\epsilon_k+\int g(\theta)\,d\mu_k(\theta),
 \qquad
 g=-\mathcal L(v)\ge0,\quad
 \mathcal L(B,D)=D+cB.}                               \tag{2}
\]

In particular,

\[
 \boxed{\|\tau_k\|_\infty\ge {c\over1+c}\epsilon_k
       ={r-1\over r}\epsilon_k.}                      \tag{3}
\]

At `R_hyb` the constant in (3) is
`0.3346006585928684...`.  Thus the unresolved trace cannot be hidden in an
`o(epsilon_k)` error.

This eliminates a previously apparent compactness obligation: no tightness
or weak limit of the module measures is needed.  The affine BDM support can
be integrated at each finite stage.  What remains global is **trace
exhaustion**, not compactness of the already separated atoms.

The theorem does not prove trace exhaustion for arbitrary graph sequences.
It isolates the exact escape object: a response-scale retained trace with
positive `D+cB` charge.  This object includes all intermodule boundary flux,
exceptional starts, metastable modules, and bulk configurations; none is
deleted.

## 2. Finite-stage paired charge lemma

Let `Theta` be the closed physical module-response space.  Its points may
include ordinary leaves and singular gate limits, provided they are limits
of finite positive modules.  Write

\[
                         v(\theta)=(B(\theta),D(\theta)). \tag{4}
\]

BDM is exactly

\[
              \mathcal L(v(\theta))\le0                \tag{5}
\]

for every `theta`.  Define the BDM slack

\[
                         g(\theta)=-\mathcal L(v(\theta))\ge0. \tag{6}
\]

Suppose `Delta=(Delta_B,Delta_D)` has both coordinates positive and set
`epsilon=||Delta||_infty`.  Since `0<c<1` at `R_hyb`,

\[
                 \mathcal L(\Delta)=\Delta_D+c\Delta_B
                 \ge c\epsilon.                        \tag{7}
\]

For any finite positive physical measure `mu` and any exact residual `tau`
satisfying

\[
                         \Delta=\int v\,d\mu+\tau,      \tag{8}
\]

linearity and (6) give

\[
 \mathcal L(\tau)
 =\mathcal L(\Delta)-\int\mathcal L(v)\,d\mu
 =\mathcal L(\Delta)+\int g\,d\mu
 \ge c\epsilon+\int g\,d\mu.                          \tag{9}
\]

Finally,

\[
 \mathcal L(\tau)\le |\tau_D|+c|\tau_B|
                    \le(1+c)\|\tau\|_\infty,          \tag{10}
\]

which proves (2)--(3).  Equality in the constant of (3) is approached when
the positive response is Bd-dominated and the residual coordinates have
the same sign.  No compactness assumption enters.

There is also a version with a controlled normal-form error.  If

\[
 \Delta_k=\int v\,d\mu_k+\tau_k+e_k,                  \tag{11}
\]

then

\[
 \mathcal L(\tau_k)
 \ge c\epsilon_k+\int g\,d\mu_k-(1+c)\|e_k\|_\infty. \tag{12}
\]

Thus `e_k=o(epsilon_k)` leaves the response-scale lower bound unchanged.

## 3. Why the coefficients in (1) must be physical and common

A positive measure in (1) has the form

\[
                    \mu_k=\sum_a\lambda_{k,a}\delta_{\theta_{k,a}},
                    \qquad \lambda_{k,a}\ge0,          \tag{13}
\]

where `lambda_{k,a}` is a physical multiplicity/core-density coefficient.
The same coefficient multiplies the full paired vector
`(B(theta),D(theta))`.  The entrance law, reciprocal recovery, gate odds,
and update-rule dependence all belong inside the two coordinates of
`v(theta)`.

Replacing (13) by separate measures `mu_k^B` and `mu_k^D` invalidates (9).
The leaf/closed-`K_2` obstruction shows that the two marginal cones can
assemble a vector in the open positive quadrant.  The present theorem makes
no attempt to identify rule-specific local Green occupation terms.  It
requires the already proved common-coefficient separated first-exit packet
and assigns every unmatched boundary term to `tau_k`.

This is also why `tau_k` must be an **exact Schur residual**.  It is not a
generic asymptotic error that can silently absorb signed terms.  Its
contents are the retained trace states and their full first-exit loads.

## 4. Exact finite-fitness Schur boundary flux

The needed trace identity holds directly for the fixation committor, not
only for the neutral pair genealogy.

Fix either update rule and a finite graph.  Let `S` be the transient mutant
configuration space, let `Q` be the substochastic transition matrix on
`S`, and let `a` be the one-step probability of absorption at all-mutant.
The fixation committor is the unique solution

\[
                              h=a+Qh.                   \tag{14}
\]

Partition `S=A sqcup B`, where `A` contains the configurations admitted to
the separated packet and `B` contains every still-coupled configuration.
Assume a trajectory started in `A` reaches `B` or absorbs almost surely.
Set

\[
 G_A=(I-Q_{AA})^{-1},\qquad
 \xi_A=G_Aa_A,\qquad
 H_A=G_AQ_{AB}.                                        \tag{15}
\]

Then `G_A`, `xi_A`, and `H_A` are entrywise nonnegative, `H_A` is the
subprobability first-hit kernel on `B`, and

\[
                         h_A=\xi_A+H_Ah_B.              \tag{16}
\]

For every nonnegative initial load `ell`,

\[
 \boxed{
 \ell^Th
 =\ell_A^T\xi_A+
  (\ell_B^T+\ell_A^TH_A)h_B.}                          \tag{17}
\]

The row vector

\[
                         m_B^T=\ell_B^T+\ell_A^TH_A    \tag{18}
\]

is the exact retained first-exit load.  In particular,

\[
 m_B^T\mathbf1
 =\Pr_\ell\{\text{start in `B`, or hit `B` before absorption}\}. \tag{19}
\]

Here `ell` is a probability row vector.  For a nonunit nonnegative load,
the right side of (19) is the corresponding load mass, or becomes a
probability after division by `ell^T1`.  The complete-baseline
normalization in (20)--(21) is then applied separately; no unit-mass
assumption is hidden in `beta_U`.

Since `0<=h_B<=1`, the entire retained contribution in (17) lies between
zero and (19).  Exceptional initial vertices appear in the first term
`ell_B^T 1`; they are retained rather than deleted.  Portal exits appear in
`ell_A^T H_A`; they too are retained.

Equation (17) follows by solving the `A` block row of (14).  Equation (19)
is the standard first-step interpretation of the killed Green kernel.
These are exact finite identities.

## 5. Quantitative trace-event alternative

Let

\[
 \kappa_{B,k}=\rho_{Bd}(K_{n_k},r),\qquad
 \kappa_{D,k}=\rho_{dB}(K_{n_k},r)                     \tag{20}
\]

be the two complete baselines.  Couple the true chain for rule `U` to its
paired separated surrogate so that they agree until the retained set
`B_{U,k}` is reached.  The retained set, configuration space, and first-exit
kernel may be rule-specific; physical pairing is required only for the
coefficients of the separated packets in (23).  Let

\[
 \beta_{U,k}={1\over\kappa_{U,k}}
 \Pr_{\ell_{U,k}}\{B_{U,k}\text{ is reached before absorption}\}. \tag{21}
\]

By (17)--(19), or directly because two Bernoulli fixation outcomes can
differ only on the displayed event,

\[
                    |\Delta_{U,k}-\widetilde\Delta_{U,k}|
                    \le\beta_{U,k}.                    \tag{22}
\]

Suppose the surrogate has the common physical expansion

\[
 \widetilde\Delta_k=\int v\,d\mu_k+e_k.               \tag{23}
\]

Combining (7), BDM, and (22) yields the scalar alternative

\[
 \boxed{
 \beta_{D,k}+c\beta_{B,k}
 \ge c\epsilon_k+\int g\,d\mu_k
      -(1+c)\|e_k\|_\infty.}                          \tag{24}
\]

Consequently, if `e_k=o(epsilon_k)`, every hypothetical simultaneous
amplifier obeys

\[
 \liminf_k {\beta_{D,k}+c\beta_{B,k}\over\epsilon_k}\ge c. \tag{25}
\]

In particular at least one rule has

\[
 \max\{\beta_{B,k},\beta_{D,k}\}
 \ge {c\over1+c}\epsilon_k-o(\epsilon_k).             \tag{26}
\]

At an individual peeling level the event budget itself has an exact local
Green form.  If

\[
                         A=\bigsqcup_m A_m,
 \qquad Q_{AA}=\bigoplus_m Q_{A_mA_m},
\]

put `G_m=(I-Q_{A_mA_m})^{-1}` and
`b_m=Q_{A_mB}1`.  For the nonnegative incoming load at that level,

\[
 \boxed{
 m_B^T\mathbf1
 =\ell_B^T\mathbf1+
  \sum_m\ell_{A_m}^TG_mb_m.}                           \tag{26a}
\]

Consequently

\[
 m_B^T\mathbf1
 \le\ell_B^T\mathbf1+
 \sum_m\|\ell_{A_m}\|_1\,\|G_m\|_\infty\,
                         \|b_m\|_\infty.              \tag{26b}
\]

In continuous time, `G_m` is the killed occupation Green kernel and `b_m`
is the vector of exit rates, so (26a) is unchanged.  This is the exact
source-weighted version of the familiar
`escape scale x killed Green norm` criterion.  It is sufficient, but not
necessary, to prove that the right side of (26b), divided by the complete
baseline, is `o(epsilon_k)` for both rules.  Importantly, the incoming load
in (26a) is the full load delivered by the preceding trace level; it is not
replaced by uniform initialization inside each module.

Thus the sole surviving escape in a separated attempt is not an abstract
failure of tightness.  It is a concrete event: with probability comparable
to the entire amplification response, the fixation genealogy reaches a
retained configuration before the proposed local packet has resolved.
Such a configuration may contain two unresolved modules, a premature
boundary arrival, a metastable growing block, or non-diffuse bulk.  These
are descriptions of the same mathematical object, the retained trace load
(18), rather than separate loopholes.

## 6. Iterated peeling and absence of a measure-compactness problem

The argument iterates.  Suppose that after `J` physical Schur levels one has
the exact identity

\[
 \Delta_k=
 \sum_{j=1}^J\int v(\theta)\,d\mu_{k,j}(\theta)
 +\tau_{k,J}+e_{k,J},                                  \tag{27}
\]

where every `mu_{k,j}` is positive and paired.  Then

\[
 \mathcal L(\tau_{k,J})
 \ge c\epsilon_k+
 \sum_{j=1}^J\int g\,d\mu_{k,j}
 -(1+c)\|e_{k,J}\|_\infty.                            \tag{28}
\]

Therefore a simultaneous amplifier leaves positive response-scale charge
in the retained trace after **every** finite number of certified BDM
peelings.  If an exhaustion theorem supplied depths `J_k` with

\[
 \|\tau_{k,J_k}\|_\infty=o(\epsilon_k),\qquad
 \|e_{k,J_k}\|_\infty=o(\epsilon_k),                  \tag{29}
\]

BDM would immediately give the desired contradiction.

No subsequential limit of the measures in (27) is necessary.  Their module
orders, portal laws, gate scales, and total masses may all drift with `k`.
At every finite `k`, inequality (5) has the same affine normal and hence
integrates before any limit is taken.  If one nevertheless assumes
response-weighted tightness, (27) produces the previously requested common
paired limiting measure; that is a corollary, not a prerequisite.

## 7. Exact remaining global obligation

Conditional on universal BDM, the arbitrary-sequence upper problem is
reduced to one statement:

> **Paired Schur-trace exhaustion target.**  Every graph sequence has a
> physical, common-coefficient Schur peeling for which the normalized
> retained trace load in (21), plus the separated normal-form error, is
> `o(epsilon_k)`.

Equivalently, if this target is false, there exists a graph sequence and a
retained coupled trace whose `D+(r-1)B` charge is bounded below by
`(r-1)epsilon_k` at every certified scale.  That is the exact escape
mechanism which a bulk theorem must rule out or turn into a new
construction.

This note does not prove the exhaustion target.  It proves that module
measure compactness, separate marginal trace measures, and deletion of
exceptional states are not the missing ingredients.

## 8. Replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B \
  verify_paired_schur_trace_exhaustion.py
```

The replay checks the affine charge bounds (2)--(3), the controlled-error
form (12), and the trace-event alternative (24)--(26) over exact symbolic
variables.  It is an algebraic replay, not a graph search.
