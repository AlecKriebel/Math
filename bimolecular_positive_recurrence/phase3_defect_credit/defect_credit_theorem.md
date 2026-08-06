# Defect-credit theorem

This note states and proves the finite theorem that closes the safe-support
case. It is the quantitative replacement for the qualitative assertion that
a trigger should eventually activate a drain.

## 1. Safe dominant sets

Fix a nonempty species set \(I\) and write

\[
q_I(y)=\sum_{i\in I}y_i,
\qquad
M_I(x)=\sum_{i\in I}x_i,
\qquad
J=\mathcal S\setminus I.
\]

In a mixed one-linkage network, quadratic safety of \(I\) implies
\(q_I(y)\in\{0,1\}\) for every complex and

\[
q_I(y')\le q_I(y)
\quad\hbox{whenever }q_I(y)>0.
\]

Thus reactions with a positive-\(I\) source never reproduce an \(I\)-particle.
The four reaction types are

\[
R_{00},\ R_{01},\ R_{10},\ R_{11},
\]

with \(M_I\)-increments \(0,+1,-1,0\), respectively.

## 2. Linear alternative

Let \(S\) be the stoichiometric subspace and let \(\pi_J\) denote projection
onto the \(J\)-coordinates. For \(v\in S\), set

\[
m(v)=\sum_{i\in I}v_i.
\]

### Lemma 2.1 - weak-reversibility cone equality

For a weakly reversible reaction network,

\[
\operatorname{cone}\{y'-y:y\to y'\in\mathcal R\}
=
\operatorname{span}\{y'-y:y\to y'\in\mathcal R\}.
\]

**Proof.** Fix an edge \(y\to y'\), with vector \(v=y'-y\). A directed
return path

\[
y'=y_1\to y_2\to\cdots\to y_m=y
\]

exists. Summing its reaction vectors gives \(-v\). Hence the negative of
every generating vector belongs to the nonnegative reaction cone. The cone
is therefore a vector space and equals the span. \(\square\)

### Lemma 2.2 - buffered drain or conservation

Exactly one of the following holds.

**L.** There is \(b\in\mathbb Q^J\) such that

\[
m(v)+b\cdot\pi_J(v)=0
\qquad(v\in S).
\]

Then

\[
W_I(x)=M_I(x)+b\cdot x_J
\]

is an exact conservation law.

**D.** There is a nonzero vector \(c\in\mathbb N_0^{\mathcal R}\) such that

\[
\sum_r c_r\pi_J(\zeta_r)=0,
\qquad
\sum_r c_r m(\zeta_r)=-k
\]

for an integer \(k\ge1\). Moreover the multiset can be ordered and supplied
with a finite enabling buffer so that it is an executable word returning to
the same \(J\)-coordinate and decreasing \(M_I\) by \(k\).

**Proof.** Write \(A\) for the matrix whose columns are
\(\pi_J(\zeta_r)\), and write \(m\) for the row vector
\((m(\zeta_r))_r\). Alternative L is exactly

\[
m\in\operatorname{row}(A).
\]

If it fails, there is a rational \(h\in\ker A\) with \(mh<0\). Clear
denomimators to make \(h\) integral. Split its positive and negative parts.
For every negative copy of a reaction vector, replace its negative by the
nonnegative sum along a directed return path supplied by Lemma 2.1. This
produces \(c\ge0\), with \(Ac=0\) and \(mc<0\). Divide by the gcd and set
\(k=-mc\).

Choose any ordering \(r_1,\ldots,r_L\) of the multiset. If
\(s_\ell=\sum_{j<\ell}\zeta_{r_j}\), define the buffer coordinatewise by

\[
a_i=\max_{1\le\ell\le L}(y_{r_\ell,i}-s_{\ell,i})_+.
\]

Then \(a+s_\ell\ge y_{r_\ell}\) for every prefix, so the word is enabled.
Its endpoint is \(a+\sum_r c_r\zeta_r\). The \(J\)-coordinate is unchanged
and the \(I\)-mass falls by \(k\). Mutual exclusivity follows because a
conservation extension annihilates every \(J\)-balanced multiset. \(\square\)

The exact construction is implemented by `conservation_or_drain.py` and
`buffered_word.py`.

## 3. Expanded target/source automaton

A raw defect state is not enough: after a reaction fires, its target complex
is known to be present, even when the same population vector enables several
other source complexes. The expanded automaton therefore records

\[
(\sigma,t),
\]

where \(\sigma\) is the finite face/tier phase and \(t\) is the target
complex carried by the most recent reaction. An execution alternates:

1. a **source switch**, choosing an enabled source \(s\) at the current
   population state; and
2. a reaction edge \(s\to t'\), after which the carried target is \(t'\).

For a cyclic execution with reactions \(s_k\to t_k\), the total
\(I\)-reward can be written in two exactly equal ways:

\[
\sum_k\big(q_I(t_k)-q_I(s_k)\big)
=
\sum_k\big(q_I(t_k)-q_I(s_{k+1})\big).
\]

The second expression assigns reward to source switches. A switch
\(q_I(t)=1\to q_I(s)=0\) is a **leak** and has reward \(+1\). A switch
\(0\to1\) spends one unit of defect credit and has reward \(-1\).

The target-retention fact is exact: immediately after \(s_k\to t_k\), the
complex \(t_k\) is enabled. Hence, when \(q_I(t_k)=1\), every outgoing edge
of \(t_k\) is a fast nonbranching option at that phase.

## 4. Priority-cycle trichotomy

For a divergent sequence, pass to a subsequence on which all source
propensities have a fixed weak order. Equal-order sources are retained as one
tier; no numerical approximation is made. Refine the order whenever a ratio
inside a tied tier tends to zero or infinity. Since there are finitely many
source monomials, this process terminates.

A functional graph on the expanded automaton has one selected outgoing edge
at each phase. A connected functional graph has one directed cycle and will
be called a unicycle. Its priority signature is the decreasing list of the
source tiers of all selected reaction edges.

### Lemma 4.1 - cycle pivot

If the unique cycle of a unicycle has a positive first nonzero reward tier,
then a cycle vertex contains a leak switch from a carried target \(t\) to a
strictly lower-priority source \(s\). Replacing the selected continuation at
that vertex by an outgoing reaction from \(t\) produces a unicycle with a
strictly larger priority signature. At a tied source tier, the same operation
removes the first nonzero positive switch reward and leaves all earlier
reward coordinates unchanged.

**Proof.** For the cycle reactions \(s_k\to t_k\), cyclic telescoping gives

\[
R=\sum_k(\omega(t_k)-\omega(s_{k+1})),
\]

where \(\omega\) is the vector of monomial-tier exponents, followed by the
integer \(I\)-credit coordinate. If the first nonzero coordinate of \(R\) is
positive, at least one switch has a positive first nonzero coordinate. Thus
its carried target has strictly higher source priority than the source
chosen next, or they are tied in every earlier coordinate and the switch is
a leak in the current credit coordinate.

The carried target is enabled and has an outgoing reaction because the
one-linkage graph is strongly connected. Replace the outgoing choice at that
cycle vertex by such a reaction. Replacing an outgoing edge of the unique
cycle breaks the old cycle; following the new edge and then the old
successor map reaches the old cycle and creates exactly one new cycle. The
result is again a unicycle. In the strict-priority case its signature is
larger. In the tied case the finite target-source refinement records the
carried target before the lower source, so the first positive switch is
removed at the current refinement level. \(\square\)

### Lemma 4.2 - finite priority reduction

On every closed component of the expanded automaton, exactly one of the
following occurs.

1. At the first nonzero priority/reward layer, every recurrent cycle has
   nonpositive reward and at least one recurrent cycle has strictly negative
   reward.
2. Every executable cycle has zero reward. In that case the reward is a
   coboundary on phases.

**Proof.** Order all unicycle signatures lexicographically and inspect them
from largest to smallest. Lemma 4.1 excludes a positive cycle at the largest
signature. If every cycle there has zero reward, its zero-reward strongly
connected components are contracted and their phase potentials are recorded.
The quotient has strictly fewer recurrent components or moves to the next
finite source/reward tier. Apply Lemma 4.1 again. The process terminates
because the automaton, the source tiers, and the reward coordinates are
finite.

If no negative layer is encountered, every directed cycle has zero total
reward after restoring the recorded phase potentials. Path sums are then
independent of path, so fixing one root in each component defines a potential
\(h\) with

\[
r(e)=h(e^+)-h(e^-).
\]

That is exactly the coboundary alternative. \(\square\)

The contraction proof is constructive. At each layer it is the standard
finite difference-constraints theorem: absence of positive cycles is
necessary and sufficient for a Bellman potential. `reward_cycle.py`,
`bellman_certificate.py`, and `tier_induction.py` implement the exact finite
steps.

## 5. Why the zero branch is conservation

Suppose every cycle in the defect automaton has zero \(I\)-reward. Then every
executable reaction multiset with zero \(J\)-displacement has zero
\(I\)-reward. Lemma 2.2 rules out Alternative D, so Alternative L holds:

\[
M_I+b\cdot X_J=\text{constant on }\Gamma.
\]

If \(I\) is the top population tier of a divergent sequence, then
\(M_I\to\infty\) while \(|X_J|=o(M_I)\). The conservation identity is
impossible. Hence the zero branch cannot occur on a divergent sequence in a
fixed communicating class.

## 6. Quantitative certificate

The remaining branch has a first negative layer. The finite contraction
proof supplies:

- a finite hierarchy depth \(H\);
- rational phase credits \(h_0,\ldots,h_H\);
- a positive margin at the first nonzero layer; and
- a finite set of source-rate comparisons.

Let \(F(x)=\sum_i\log(x_i!)\). Its exact reaction increment is

\[
F(x+y'-y)-F(x)
=
\log\frac{(x+y'-y)_{y'}}{(x)_y}.
\]

Consequently the leading logarithmic reward is precisely the target/source
monomial reward used by the automaton. Choose an integer
\(P>H+2\). The recorded Bellman credits lift, after clearing positive
monomial denominators, to a phase-dependent generalized polynomial
\(V_\rho\) with positive leading coefficient and

\[
\mathcal L V_\rho(x)\le-2
\]

deep in the stabilized regime. The construction is finite: expand the
generator, order its finitely many monomials, and choose the coefficients
successively from the Bellman inequalities. A lower layer cannot alter a
sign fixed at a higher layer. If a coefficient choice were infeasible,
Farkas' lemma would produce a positive cycle at the first failing layer,
contradicting Lemma 4.2.

The inequality is an exact eventual inequality, not a formal heuristic. If
it failed arbitrarily far into the regime, a bad sequence could be chosen.
Dividing by the largest positive monomial and passing to the stabilized tier
limit would contradict the strict Bellman margin.

This is the trigger-and-drain conclusion: catalytic cycles give an early
negative layer; one-for-one deaths are absorbed as finite phase credit; a
chain of leaks moves to lower layers; and the first non-credit layer is
strictly draining. The hierarchy has finite depth because the expanded
automaton is finite.
