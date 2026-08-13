# Hostile symbolic audit of the no-mixed one-active exhaustion

**Proof-first diagnostic, 2026-08-12 PDT.**  This note attacks the proposed
one-active support alternative for a two-linkage binary network after every
pair having a raw mixed two-active occurrence has already been routed to the
pair-specific pipeline.  It proves the support geometry symbolically and
isolates the analytic lemma still required.  It does not enumerate reaction
orientations, rate vectors, histories, population boxes, or stochastic paths.

## 1. Verdict

No residual support-pair counterexample exists to the proposed symbolic
exhaustion.  Fix active species (X) and bounded species (U,V).  A disjoint
support pair having no mixed available/shielded occurrence in any two-active
chart falls into exactly one of:

1. a linkage contains (2X), giving direct quadratic descent;
2. both linkages are constant in (X)-degree, so (X) is invariant;
3. both nonflat linkages have a lower terminal which enables a faster
   (X)-degree-one source;
4. one linkage has that terminal and the other is flat of (X)-degree zero;
5. the pair has a common signed invariant positive on (X).

The fifth case consists of only five literal support shapes.  There is no
dormant/Bellman or dormant/dormant residue.

There is, however, a load-bearing analytic seam in item 4.  Such a pair is not
literally within the scoped both-available theorem, because a mark in the
flat linkage has no rare same-linkage terminal.  A finite all-clock flat-phase
prelude must be proved and appended to the Bellman episode.  Terminal-chart
terminology alone does not supply that estimate.

## 2. One-linkage token geometry

Exclude the direct quadratic case (2X\in L).  The (X)-degree-one menu is

\[
                         X,qquad X+U,qquad X+V,       \tag{2.1}
\]

and the degree-zero menu is

\[
                         0,U,V,2U,U+V,2V.              \tag{2.2}
\]

Call a nonflat linkage **Bellman** if it contains (q) of (X)-degree one
and (c) of degree zero such that

\[
                         q_U\le c_U,qquad q_V\le c_V. \tag{2.3}
\]

Otherwise call it **dormant**.  If (X\in L), (2.3) holds with every lower
complex, so a dormant linkage cannot contain (X).  If (X+U\in L), no
lower complex can contain (U); similarly, if (X+V\in L), no lower complex
can contain (V).  Consequently every dormant support has exactly one of
the following forms:

\[
\begin{array}{c|c|c}
\text{degree-one block}&\text{degree-zero block}&\text{linkage invariant}\\ \hline
\{X+U\}&\varnothing\ne S\subseteq\{0,V,2V\}&X-U\\
\{X+V\}&\varnothing\ne S\subseteq\{0,U,2U\}&X-V\\
\{X+U,X+V\}&\{0\}&X-U-V.
\end{array}                                             \tag{2.4}
\]

This is a three-line consequence of binaryity and (2.3), not a stochastic
classification.

## 3. What the absence of a mixed two-active chart forces

Apply the exact ordered Q/U/C/S top classifier in the three possible
two-active projections ((X,U)), ((X,V)), and ((U,V)), including the
equality wall and the two adjacent chambers.  The first two rows of (2.4)
have no disjoint partner with the same A/S status in every one of these
cells.  This follows by inspecting the nonempty lower subset of the
three-vertex set ({0,V,2V}), or its (U,V)-symmetric copy: there are only
seven subsets, and the Q status in the ((X,U)) chart conflicts with the
wall/chamber status forced on any disjoint partner in ((X,V)) or ((U,V)).
Thus either a raw mixed two-active occurrence exists or the dormant linkage
is the last row of (2.4):

\[
                         L_d=\{0,X+U,X+V\}.            \tag{3.1}
\]

For (3.1), the classifier is available throughout the ((X,U)) and ((X,V))
charts.  In the ((U,V)) chart it is shielded on the equality wall and
available in both open chambers.  A disjoint linkage matches that exact
status signature if and only if it is one of

\[
\begin{split}
 L_f\in\{&\{U,V\},\ \{2U,2V\},\ \{2U,U+V\},\\
          &\{2V,U+V\},\ \{2U,2V,U+V\}\}.
                                                               \tag{3.2}
\end{split}
\]

Indeed, the first support in (3.2) is a nontrivial subset of the unary
inactive shell ({U,V}), while the other four are precisely the subsets of
size at least two of the quadratic inactive shell
({2U,U+V,2V}).  Such a shell is flat on the equality wall and has a
quadratic top off it.  No other disjoint binary support has this signature.

Every complex of (L_d) has the same value zero under

\[
                         H=X-U-V,                      \tag{3.3}
\]

and every support in (3.2) lies in one level set of (U+V).  Hence (3.3) is
a common physical invariant of the whole pair.  It is positive on the active
coordinate (X).  Since (U,V) are bounded in the chart and (H) is fixed
on the communicating class, (X) cannot escape.  No Foster-potential handoff
is involved.

For orientation, an independent exact classifier replay on unordered
disjoint support pairs returned, for each fixed (X),

\[
\begin{array}{c|r}
\text{category pair}&\text{pairs with no mixed two-active occurrence}\\ \hline
Q/B&6,050\\
Q/F_0&1,352\\
Q/F_1&54\\
B/B&1,224\\
B/F_0&731\\
F_0/F_0&19\\
F_0/F_1&54\\
D/F_0&5\\ \hline
\text{total}&9,489.
\end{array}                                             \tag{3.4}
\]

Here (F_k) means flat of constant (X)-degree (k).  Equation (3.4) is
regression evidence only.  The symbolic proof of the dormant residue is
(2.4)--(3.3).

## 4. Direct quadratic and flat alternatives

If (2X) belongs to either linkage, it is the unique binary complex of
(X)-degree two and is enabled throughout the one-active chart.  Every
outgoing edge from (2X) has target (X)-degree at most one.  Its propensity
is of order (X^2), and its factorial-entropy decrement has order
(-\log X).  All other sources have propensity at most order (X) and
one-jump factorial increment (O(\log X)), uniformly in the fixed inactive
box.  Hence the (2X) contribution, of order (-X^2\log X), dominates the
total (O(X\log X)) positive remainder.  This proof uses strong connectivity
only to ensure an outgoing nonzero edge and is orientation independent.

If both linkages are flat, every reaction preserves (X) exactly.  The fixed
class value of (X) then rules out a one-active escape.  The two flat
linkages need not lie at the same (X)-degree; disjointness permits the
(F_0/F_1) case, but every within-linkage reaction still has zero
(X)-increment.

## 5. Bellman/Bellman: exact one-active corollary required

For a Bellman linkage choose (q,c) satisfying (2.3) and a simple path from
the actual carried target to (c).  On designated success the endpoint
(z=x-t+c) enables (q), while (q) has (X)-degree one and (c) degree
zero.  Thus

\[
                         p_c(z)\le{\lambda_c(z)\over\lambda_q(z)}
                                  \longrightarrow0.     \tag{5.1}
\]

The exact marked identity and stopped-on-first-deviation Bellman recursion
then give coercive negative reward exactly as in the both-available theorem.
Both linkages use the same marked potential

\[
                         W(x,t)=1+\sum_i\log((x_i-t_i)!). \tag{5.2}
\]

The current frozen theorem is stated for a terminal **two-active** chart.
Its algebra proves (5.1)--(5.2) verbatim in a one-active chart, but publication
composition must state and audit this one-active corollary rather than cite
the two-active scope silently.

## 6. The 731 Bellman/flat pairs need a finite-phase prelude

The absence of every raw mixed two-active occurrence forces the flat partner
in a Bellman/flat pair to have (X)-degree zero; there is no (B/F_1) row in
(3.4).  This fact is load bearing.

At a mark in the Bellman linkage, run its same-linkage path directly.  At a
mark in the flat linkage, retain every physical clock and run the finite
inactive phase until the first of:

1. an actual Bellman-linkage reaction, including that reaction;
2. an inactive-box, support, source-cell, or active-set exit; or
3. entrance into a closed phase in which no Bellman-linkage source can ever
   become enabled.

On the fixed padded inactive box, flat-linkage propensities are uniformly
bounded because every flat source has (X)-degree zero.  Every positive
enabled rate is at least a fixed labelled rate.  A finite killed-chain
argument therefore gives a uniform finite mean physical duration and
reaction count up to alternatives 1--3.

All pre-activation flat marks and flat sources have (X)-degree zero.  Their
marked factorial rewards have no (log X) positive term, and the bounded
inactive phase makes their positive reward uniformly integrable.  If the
absorbing Bellman-linkage source has degree zero, its included activation
jump also has bounded positive reward; if it has degree one, that jump has a
negative (-\log X+O(1)) contribution.  Append the Bellman path from its
actual target.  The activation probability remains unconditioned, and the
finite phase gives it a positive lower bound on every nonclosed transient
class.  The combined all-clock prelude plus Bellman episode is therefore
coercively negative or records the physical exit in alternative 2.

In alternative 3, only the degree-zero flat linkage acts forever, so (X)
is constant on that closed physical phase.  Such a phase cannot carry a
one-active escaping occupation in one fixed communicating class.  This is
the exact no-history conclusion.

This finite-phase construction is the necessary repair theorem.  Calling the
pair “Bellman AA” without it is incorrect: the flat linkage has no rare
terminal and an actual target in that linkage lies outside the literal start
domain of the both-available episode.

## 7. Does terminal-chart contradiction avoid a global common potential?

Yes, at a precisely limited scope.  In a Green-occupation proof, first select
one positive-mass terminal chart with zero normalized structural-exit flux.
The alternatives above are mutually exclusive on that fixed chart.

* Quadratic descent uses its one direct entropy function.
* Bellman/Bellman uses the single marked potential (5.2).
* Bellman/flat uses the same marked potential through both the finite prelude
  and the appended Bellman episode.
* Flat/flat and dormant/flat are excluded by exact fixed-class invariants.

If a local episode leaves the chart, its causing physical reaction has
positive exit flux and contradicts terminality; the proof does not follow it
into a new chart and switch potentials there.  Thus no common potential
across different terminal-chart alternatives is needed for the Green
contradiction.

This does **not** justify a direct global state-selected Foster theorem which
reclassifies arbitrary endpoints under different potentials.  Such a theorem
still needs one common proper potential or an explicit comparison toll.  The
publication proof must choose the terminal-Green contradiction route, retain
episode/reaction-count mass, and verify truncation or endpoint uniform
integrability for the unbounded marked factorial reward.

## 8. Final repair requirements

The one-active support exhaustion has no symbolic hole.  To make it a proved
dependency, the composition must still contain exact statements of:

1. the one-active Bellman/Bellman corollary of the marked theorem;
2. the Bellman/degree-zero-flat finite-phase prelude of Section 6, with all
   clocks, the activation jump, actual endpoint, reward, count, and physical
   duration included;
3. the closed-phase/no-history fixed-class conclusion;
4. the exact small support lemma (2.4)--(3.3); and
5. a terminal-chart Green handoff rather than an unsupported switch among
   different Foster potentials.

Subject to these repairs, the proposed one-active exhaustion passes hostile
symbolic audit.  Without item 2, it is not yet a complete stochastic proof.

