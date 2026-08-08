# Diffuse rank-one clone blow-ups have no Bd catalyst response

Date: 2026-08-08 (America/Los_Angeles)

## Status and scope

This note proves a growing-rank class obstruction tailored to the exact
catalyst-ray target.  It is not a fixed-cell screen.

An arbitrary finite propensity profile is blown up into clone classes, with
every distinct pair joined by the rank-one weight `a_i a_j`.  The class
number, class proportions, and propensity ratios may all vary from stage to
stage.  At each stage the clone multiplier is then sent far enough out that
every fixed rare-mutant trace is resolved.  The graph has complete loopless
support, so it is connected, and rational profiles give rational weights.

For every fitness `r>1`, the exact rare-mutant limit has uniformly averaged
Bd and dB survival probabilities `beta(r)` and `sigma(r)` satisfying

\[
 \boxed{\displaystyle
     \beta(r)={r-1\over r},\qquad
     \sigma(r)\le {r-1\over r}.}                    \tag{1}
\]

The dB inequality is strict unless all propensities are equal.  Thus this
entire growing-rank architecture has **zero Bd catalyst gain**, not merely a
dB cost comparable to its Bd gain.  A stopped-chain argument includes
uniform initialization and every post-establishment path: fixation is
bounded by reaching a fixed mutant cutoff, whose law converges exactly to the
branching trace.  Consequently no trace-resolved diagonal in this
architecture can have

\[
 {B_k(r)\over c_k}\longrightarrow b(r)>0,
 \qquad {D_k(r)\over c_k}\longrightarrow0           \tag{2}
\]

even locally uniformly on a compact subinterval of `(1,infinity)`.

This closes diffuse rank-one degree-gradient gateways and arbitrary
multiscale rank-one clone blow-ups.  It does not cover non-rank-one
incidence, sparse order-one shared edges, profiles kept non-diffuse on the
mutant cutoff scale, or correlations deliberately retained below every
growing cutoff.

## 1. Explicit graph family

Fix a finite type set `I`, positive rational proportions `p_i` summing to
one, and positive rational propensities `a_i`.  Take a common multiple `m`
of the proportion denominators and form

\[
                         n_i=mp_i                    \tag{3}
\]

clones of type `i`.  Thus the total population is `m`.  For two distinct
vertices `u,v` of types `i,j`, put

\[
                         w_{uv}=a_i a_j.             \tag{4}
\]

There are no loops.  Write

\[
 \bar a=\sum_i p_i a_i,\qquad x_i={a_i\over\bar a},
 \qquad E f=\sum_i p_i f_i.                         \tag{5}
\]

Then `Ex=1`.  The weighted degree of a type-`i` vertex is

\[
                         d_i=a_i(m\bar a-a_i).       \tag{6}
\]

The profile may depend arbitrarily on an outer rank parameter `k`.  The
limit below first fixes that finite profile and sends `m` to infinity.  A
final diagonal may choose `m=m_k` as rapidly as needed.  Equivalently, the
scope is the trace-resolved regime in which all fixed-cutoff collision,
depletion, and self-omission errors vanish.

## 2. Atomic rates and the exact stopped limit

Use the equivalent continuous-time chains obtained by deleting common
statewise normalization factors.

### Bd

A rare type-`i` mutant gives birth at total rate `r`.  Its child has type
`j` with probability

\[
 {mp_j a_j-\mathbf1_{i=j}a_i\over m\bar a-a_i}
       \longrightarrow {p_j a_j\over\bar a}=p_jx_j. \tag{7}
\]

The incoming resident replacement rate at that mutant is

\[
 t_i^{(m)}=a_i\left[
   \sum_j{mp_j\over m\bar a-a_j}-{1\over m\bar a-a_i}
                         \right]\longrightarrow x_i. \tag{8}
\]

Thus the limiting Bd branching particle of type `i` dies at rate `x_i`,
gives birth at rate `r`, and samples the child type from `p_jx_j`.

### dB

A rare mutant dies at rate one.  If its type is `i`, then for a resident
target of type `j` its parent-selection probability is

\[
 {r a_i\over m\bar a-a_j+(r-1)a_i}.                 \tag{9}
\]

There are `mp_j+O(1)` such targets, so type-`j` children are born at limiting
rate

\[
                              r p_jx_i.              \tag{10}
\]

Equations (7)--(10) follow directly from the two Moran rules.  For a fixed
mutant cutoff `K`, resident depletion, mutant targets, and omitted self
targets change the type-count transition rates by `O_{K,I,a}(1/m)`.  The
finite type-count chain stopped on reaching `0` or `K` therefore converges
entrywise to these multitype branching chains.  The stopped state space is
finite, so its absorption probabilities converge as well.  No
independent-lineage claim is made after `K` is reached.

Uniform singleton initialization chooses type `i` with probability `p_i`,
exactly the averaging law in (5).

## 3. Exact survival systems for every fitness

Let `b_i` and `s_i` be the Bd and dB branching survival probabilities, and
put

\[
 \beta=E b,\qquad \sigma=E s,\qquad M=E[xb].        \tag{11}
\]

For Bd, a birth retains the parent and creates a child whose mean survival
probability is `M`.  Direct first-event conditioning gives

\[
                  b_i={rM\over x_i+rM}.              \tag{12}
\]

For dB, the total birth rate of a type-`i` particle is `rx_i`, and its child
has the unbiased type law `p_j`.  Hence

\[
                  s_i={rx_i\sigma\over1+rx_i\sigma}.\tag{13}
\]

Both branching systems have Perron root `r`, so for `r>1` their nonzero
survival solutions are unique.  Substitution into (11), followed by division
by the positive scalar, gives

\[
             1=E{rx\over x+rM},\qquad
             1=E{rx\over1+rx\sigma}.                \tag{14}
\]

These equations retain the full type distribution.  They are not obtained
by replacing the lineages with identically distributed particles.

## 4. The all-fitness obstruction

The first equation in (14) immediately fixes the uniform Bd average:

\[
 E(1-b)=E{x\over x+rM}={1\over r},
 \qquad
 \boxed{\beta=1-{1\over r}}.                        \tag{15}
\]

This exact cancellation is the obstruction's main mechanism.  Reproductive
value heterogeneity changes the typewise Bd survival probabilities but not
their uniform-singleton average.

For dB, evaluate the second left side of (14) at
`p=(r-1)/r`:

\[
 E{rx\over1+(r-1)x}\le
 {rEx\over1+(r-1)Ex}=1.                             \tag{16}
\]

The integrand is strictly concave on `(0,infinity)`, and the left side of
the dB equation is strictly decreasing in `sigma`.  Its positive root
therefore satisfies

\[
                         \boxed{\sigma\le p},        \tag{17}
\]

with equality exactly when `x_i=1` for every type of positive mass.  That
equality case is the unit-complete graph up to a common edge scaling.

At the endpoint `r=2` there is also a useful typewise refinement.  Put
`c=1/(2\sigma)` and `F(z)=E[2x/(x+z)]`.  Equations (14) give

\[
 F(2M)=1,\qquad F(c)=1/c\le1,
\]

so monotonicity of `F` yields `4M\sigma\le1`.  Consequently

\[
 {b_i\over1-b_i}{s_i\over1-s_i}=4M\sigma\le1,
 \qquad b_i+s_i\le1.                                \tag{18}
\]

This endpoint certificate is stronger than the averaged statement but is
not needed for the all-fitness Bd obstruction.

## 5. From the stopped trace to full fixation

Let `H_K` be the event that the finite Moran chain reaches `K` mutants before
extinction.  Fixation implies `H_K`, so for either rule and every singleton
type `i`,

\[
             \rho_U^{(m)}(i)\le\Pr_i^{(m)}(H_K).     \tag{19}
\]

For fixed profile and fixed `K`, Section 2 gives convergence of the right
side to the corresponding branching hitting probability.  Letting first
`m->infinity` and then `K->infinity` yields

\[
 \limsup_m\rho_{Bd}^{(m)}\le {r-1\over r},\qquad
 \limsup_m\rho_{dB}^{(m)}\le\sigma\le {r-1\over r}.\tag{20}
\]

This is the required post-establishment control for an obstruction: no
behavior after the first `K` mutants can increase fixation beyond the event
of reaching `K`.  The argument never asserts that the full finite process is
globally dominated by independent particles.

For the catalyst-scale statement, let the finite profile, positive response
scale `c_k`, and compact fitness interval `J` vary with `k`.  Choose `K_k`
so the branching hitting probabilities are within `o(c_k)` of survival on
`J`, and then choose `m_k` so the finite stopped chains are within `o(c_k)`.
For a fixed finite profile, compact-uniformity follows from monotone
convergence in `K` and continuity away from `r=1`, followed by uniform
finite-state convergence in `m`.

The exact complete-graph Bd fixation probability is

\[
 \rho_{Bd}(K_n,r)={1-r^{-1}\over1-r^{-n}}>{r-1\over r}. \tag{21}
\]

It follows from (15), (19), and the diagonal choices that

\[
 \sup_{r\in J}
 {\bigl(\rho_{Bd}(G_k,r)-\rho_{Bd}(K_{n_k},r)\bigr)_+
       \over c_k}\longrightarrow0.                 \tag{22}
\]

Thus a positive normalized Bd catalyst limit is impossible throughout this
architecture, regardless of its dB response.  Equation (22) contains the
entire uniform-singleton response and discards no gateway, relay, or
far-field starts.

## 6. What this eliminates and what remains

**PROVED:** the finite atomic rates, exact stopped branching limit,
all-fitness scalar survival equations, identity (15), sharp dB comparison
(17), endpoint pointwise inequality (18), full-fixation upper passage, and
the trace-resolved response obstruction (22).

**ELIMINATED:** arbitrary diffuse rank-one complete-support blow-ups,
including growing numbers of positive or vanishing clone classes, unbounded
propensity ratios at each finite stage, and every trace-resolved multiscale
diagonal built from them.

**OPEN:** non-rank-one portal incidence; sparse gateways retaining an
order-one shared edge; profiles kept non-diffuse on the relevant mutant
cutoff scale; correlations that survive below every growing cutoff; and
architectures whose core response cannot be represented by a diffuse
rank-one clone law.

In particular, this theorem does not rule out a singular fitness boundary
layer generated by one of those non-diffuse mechanisms.  It says that a
rank-one degree gradient alone cannot supply the required catalyst ray.

## 7. Exact replay

`verify_rank_one_clone_catalyst.py` independently reconstructs (7)--(10),
checks the all-fitness Bd cancellation, certifies the dB comparison on a
nonconstant rational profile, checks the endpoint factorization in (18),
and solves exact sample systems.
