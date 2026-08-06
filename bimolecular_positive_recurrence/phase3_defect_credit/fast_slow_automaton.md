# Fast-slow automaton and reward cycles

## 1. What the automaton records

For a safe dominant set \(I\), every complex contains zero or one
\(I\)-particle. A bounded defect box is therefore sufficient to determine
which \(q_I=0\) and \(q_I=1\) source types are enabled. The automaton records:

- the exact capped defect configuration;
- the active coordinate face;
- the carried target complex from the preceding reaction;
- the strongly connected component of the currently higher-priority
  reaction graph; and
- the finite Bellman credit attached to previously collapsed components.

No population ratio is hidden in a vertex. Ratios appear only as an ordered
label on source rates. When a lower coordinate becomes unbounded or changes
rate tier, the process exits to another finite regime.

## 2. Fast edges and rewards

Within a safe top tier,

- \(R_{10}\) and \(R_{11}\) have a positive top-particle source and never
  increase \(M_I\);
- \(R_{00}\) and \(R_{01}\) have no top-particle source; and
- only \(R_{01}\) has reward \(+1\).

The finite fast graph uses the positive-source edges. A fast SCC containing a
negative edge contains a negative directed cycle, because every edge in an
SCC lies on a cycle. It is therefore catalytic: while the top composition
remains in the regime, the cycle can be repeated and removes top particles.

If a fast SCC has no negative edge, every edge in it has zero reward. On the
condensation DAG, a death can occur only while moving to a strictly lower
component. Hence the number of such deaths before a terminal SCC is at most
the number of SCCs. This is the exact finite defect-credit bound.

## 3. Slow normalization

A slow \(+1\) reaction leaves its target \(q_I=1\) complex enabled. A directed
complex path from that target to a \(q_I=0\) complex consists of zero-reward
fast steps followed by a death. Therefore a slow birth followed by complete
higher-priority relaxation has reward at most zero. A slow zero-reward event
followed by relaxation also has reward at most zero.

The only way to retain positive reward is to fire a lower-priority source
while the carried positive-source target is still available. This is a leak.
The expanded target/source automaton records the leak explicitly rather than
hiding it inside an averaged transition.

## 4. Cycle-pivot rule

A positive reward cycle has more leaks than service switches. At the first
positive source tier, choose a leak whose carried target strictly outranks the
source fired next. Re-selecting an outgoing reaction from the carried target
raises the functional graph's priority signature. Thus a positive reward
cycle cannot be maximal. Zero maximal cycles are contracted, and the same
argument is repeated on the quotient. The first nonzero quotient cycle is
negative; if none exists, all reward is phase credit and extends to a linear
conservation law.

This is why a positive local reward does not survive the complete hierarchy.
It is also why a fixed number of embedded jumps is the wrong unit: the proof
orders physical reaction rates, contracts faster recurrent components, and
only then studies the next source tier.

## 5. Quantitative bounds

On a compact composition sector in which each designated top species has
fraction at least \(\eta>0\), every enabled positive-source reaction has rate
between

\[
c_\rho R a(x_J)
\quad\hbox{and}\quad
C_\rho R a(x_J),
\]

where \(R\) is the top scale and \(a(x_J)\) is the exact lower-tier source
factor. Equal-tier coefficients range over a compact positive projective
set. The Bellman margins are therefore uniform on a closed regime. If a
coefficient tends to zero or infinity, that sequence belongs to a refined
adjacent tier and is handled there.

Clearing denominators in the finite Bellman hierarchy gives an exact
piecewise generalized-polynomial generator certificate. The proof never
assumes uniform mixing of a fast subsystem. Mixing, transient relaxation,
and rare interruptions are all encoded by finite SCC contraction and the
successive reward layers.
