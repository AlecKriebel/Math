# A nonvanishing homogeneous pair relay cannot carry both rules

Date: 2026-08-08 (America/Los_Angeles)

## Status and scope

This note exactly closes the smallest nonvanishing relay suggested by the
two-channel entrance obstruction: a density-one population of equally
protected `K_2` cells over a dense regular background.  Every singleton,
every discordant pair, every repaired pair, and every external child is
retained in the limiting rare-colony process.

For every fixed fitness `r>1` and every fixed positive normalized partner
strength `z`, the uniformly averaged establishment vector is

\[
                         (E_{Bd},E_{dB})=(p,T_D(z)),
 \qquad p=1-{1\over r},\qquad 0<T_D(z)<p.       \tag{1}
\]

Thus the homogeneous protected-pair population ties the Bd limiting
baseline and is strictly dB-suppressing at establishment.  It cannot be the
positive-density relay class missing from the complementary two-channel
construction.

This is a class theorem, not a universal fixation obstruction.  It does not
cover a nonregular external network, heterogeneous pair strengths, or a
finite-population diagonal in which `z` tends to zero with population size.

## 1. Dense pair population and exact colony trace

Take `M` labelled pairs, put a common dense edge between vertices in
different pairs, and give each partner edge normalized strength `z>0` on the
dense degree scale.  Send `M` to infinity with `r,z` fixed.  Write

\[
 x={1\over1+z},\qquad h={z\over1+z}.             \tag{2}
\]

An occupied pair has only two nonempty local types: a singleton `1` and a
doubleton `2`.  Descendants entering new pairs are singletons.  Let `q_1,q_2`
be extinction from these types, put `Q=q_1` by homogeneity, and set
`T=1-Q`.

### Bd

Directly from the update rule, the exact first-event equations reduce to

\[
 {q_2\over q_1}={x\over x+r xT},                       \tag{3}
\]

\[
 q_1={x+h\over
 x+h+rh+rxT-rh(q_2/q_1)}.                              \tag{4}
\]

The terms in (4) are respectively external recovery, internal recovery,
internal mutant repair, external mutant birth, and the continuation after
repair.  No independence is assumed between the two vertices of a pair.

Substitution of `q_1=1-T` into (3)--(4) gives

\[
 {T(Tr-r+1)(Tr+rz+z+1)\over
 T^2r^2+Tr^2z+Trz+2Tr+z+1}=0.                         \tag{5}
\]

The only positive survival root is

\[
                         \boxed{T_B=p}.                \tag{6}
\]

This agrees with the exact finite-graph fact that the homogeneous pair
population is weighted regular and therefore has the complete-graph Bd
fixation probability.

### dB

A mutant singleton dies at rate one.  Its partner becomes mutant at rate

\[
                         g={rz\over1+rz}.               \tag{7}
\]

A doubleton shrinks at rate

\[
                         \ell={2\over1+rz}.             \tag{8}
\]

Each mutant vertex emits external singleton children at rate `rx`.  Hence

\[
 {q_2\over q_1}={\ell\over\ell+2rxT},                 \tag{9}
\]

\[
 q_1={1\over1+g+rxT-g(q_2/q_1)}.                       \tag{10}
\]

Putting `q_1=1-T`, the nonzero survival root is the positive root of

\[
\begin{aligned}
 F_{r,z}(T)={}&r^2(rz+1)T^2\\
 &+[-r^3z+2r^2z^2+2r^2z-r^2+2rz+2r]T\\
 &-r^2z^2-r^2z-rz-r+z^2+2z+1.             \tag{11}
\end{aligned}
\]

The sign certificate is immediate:

\[
 F_{r,z}(0)=-(r-1)(z+1)(rz+z+1)<0,                    \tag{12}
\]

\[
 F_{r,z}(p)=z^2(r-1)^2>0.                              \tag{13}
\]

The leading coefficient is positive, while the constant term is negative,
so the two roots have opposite signs.  There is exactly one positive root,
and (12)--(13) place it strictly in `(0,p)`.  This proves (1).

For reference, the discriminant also factors positively:

\[
 \operatorname{disc}_T F
 =r^3(rz+1)(r^2z+r+4z^3+8z^2+4z)>0.                  \tag{14}
\]

## 2. Why this answers the relay test

The relay population here is not discarded as a vanishing overhead: it is
the entire population, and uniform starts on every relay vertex are included.
Pair collisions do protect a mutant lineage, but resident recovery through
the dense background offsets that protection under dB by the strict amount
certified in (13).  Equal protection keeps the graph weighted regular, so Bd
cannot be strict either.

Consequently the positive-density escape identified by the temperature
theorem requires more than homogeneous `K_2` protection.  It must use a
nonregular or hierarchical external network in a way that gives the same
positive-density starts substantial fixation under both rules.

## 3. Exact replay

`verify_dense_pair_relay.py` reconstructs (3)--(11), checks all displayed
factorizations, isolates the positive dB root in `(0,p)`, and verifies the
first-event equations at exact rational instances.  Numerical fixation
plots are not used in the theorem.
