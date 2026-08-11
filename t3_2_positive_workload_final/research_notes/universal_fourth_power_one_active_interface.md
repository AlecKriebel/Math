# A fourth-power interface for the unresolved one-active kernels

## 1. Scope and claim boundary

This note proves the physical-time gluing theorem used by the exact
1,227-pair one-active table.  The support-specific graph theorem is certified
separately, and their independently audited pair-level composition is
recorded in
`research_notes/one_active_fourth_power_pair_composition.md`.

For a fixed network and positive rate vector, let

\[
 {\cal F}_{\ell}(x)
 =K+\sum_{i=1}^d\log(x_i!)+\ell\mathbin{\cdot}x,
 \qquad
 G=1+{\cal F}_{\ell}\ge1,
 \qquad W=G^4.                                        \tag{1.1}
\]

The constant \(K\) makes \(G\) positive.  The same fixed vector \(\ell\)
must be used in every region of the composition.  The all-23
moving-cutoff promotion-access lemma below is certified as a local analytic
interface.  The arbitrary-orientation resistance theorem is separately
certified in
`research_notes/one_active_arbitrary_orientation_graph_theorem.md`.
The exact 1,227-pair recurrence theorem is now certified.  Global T3-2
remains uncertified.

For the universal branch one may, and below does, take \(\ell=0\).  A fixed
linear correction changes every bounded reaction increment by only
\(O(1)\), so it neither changes a strict tier gap nor any exponent below;
choosing zero avoids an otherwise unnecessary compatibility question
between local interfaces.

The conclusions are:

1. the fourth-power lift is automatic on every quantitative
   Anderson--Kim passing cone;
2. a repeated one-active base kernel closes when its **aggregate** downward
   resistance is at most two, aggregate upward resistance is one larger,
   neutral attempts return to a regenerative base phase, and endpoint
   moments are uniform; and
3. on the exact 23-template menu, a \(n^{1/8}\) terminal boundary supplies
   the stopped high-power promotion-access bound with the same \(W\),
   conditional only on the aggregate resistance ordering.

## 2. Fourth-power drift on a passing descriptor

For reaction \(r\), write \(a_r(x)\) for its propensity and

\[
 d_r(x)={\cal F}_{\ell}(x+\zeta_r)-{\cal F}_{\ell}(x).
\]

The exact binomial identity is

\[
 \begin{split}
 {\cal L}W={}&4G^3{\cal L}{\cal F}_{\ell}
 +6G^2\sum_ra_r d_r^2
 +4G\sum_ra_r d_r^3
 +\sum_ra_r d_r^4.                                   \tag{2.1}
 \end{split}
\]

Consider a divergent state sequence \(x_n\) which realizes a passing
source/D-tier descriptor.  Let \(R_n=1+\lVert x_n\rVert_1\), let \(A_n\)
be the largest enabled source propensity, and let \(g_n\to\infty\) be the
logarithmic gap of a certified top-S, top-D source to its lower-D target.
The quantitative Anderson--Kim calculation gives

\[
 {\cal L}{\cal F}_{\ell}(x_n)\le-cA_ng_n.             \tag{2.2}
\]

The finite binary reaction menu gives, uniformly in \(r\),

\[
 \sum_ra_r(x_n)\le CA_n,qquad
 |d_r(x_n)|\le C\log R_n,qquad
 cR_n\log R_n\le G(x_n)\le CR_n\log R_n.             \tag{2.3}
\]

The first inequality uses the top stochastic-source tier: every other
source propensity is bounded by a fixed multiple of \(A_n\).  The second
is the exact factorial-ratio bound for a bounded reaction vector; a fixed
linear correction changes it only by \(O(1)\).

Substitution in (2.1) gives

\[
 \begin{split}
 {\cal L}W(x_n)
 \le{}&-4cG^3A_ng_n\\
 &+CA_n\{G^2(\log R_n)^2
          +G(\log R_n)^3+(log R_n)^4\}.              \tag{2.4}
 \end{split}
\]

The ratio of the first remainder to the negative term is at most

\[
 {C(\log R_n)^2\over Gg_n}\longrightarrow0,          \tag{2.5}
\]

and the other two ratios are smaller.  Hence

\[
 {\cal L}W(x_n)\longrightarrow-\infty.                \tag{2.6}
\]

This proves item (i) in the question.  In particular, on a support pair
whose affine-feasible failures are all one-active, every divergent
sequence with at least two active coordinates is eventually \(W\)-good.
The usual bad-sequence contradiction turns (2.6) into a finite-exception
generator bound on the complement of the one-active interfaces.  No
tight coordinate is replaced by a finite box.

The same contradiction gives the quantitative form needed for physical
gluing.  There are a finite set \(K_0\) and \(c_0>0\) such that, throughout
the at-least-two-active region outside \(K_0\),

\[
 {\cal L}W\le-c_0W^{3/4}.                            \tag{2.7}
\]

Otherwise a violating sequence has a passing tier subsequence.  On that
subsequence (2.4), the positivity of every enabled rate constant, and
\(g_n\to\infty\) give
\(-{\cal L}W/G^3\to\infty\), contradicting the violation.  In particular,
the concave function
\(H(w)=4c_0^{-1}w^{1/4}\) satisfies
\({\cal L}H(W)\le-1\) before exit from this region: concavity gives
\(H(W(x+\zeta))-H(W(x))\le H'(W(x))\Delta W\).
Localization followed by Fatou therefore controls both the physical exit
time and the endpoint \(W\)-moment without an upper-boundary uniform-
integrability assumption.

## 3. Repeating a one-active base kernel

Fix one active coordinate \(X\), a finite set of regenerative base marks
\(E\), and base populations

\[
 b_{n,e},\qquad X(b_{n,e})=n,qquad e\in E.            \tag{3.1}
\]

The inactive factorial part of \({\cal F}_{\ell}(b_{n,e})\) is uniformly
bounded over \(E\).  A raw physical attempt starts at \(b_{n,e}\), retains
every reaction, and stops in one of three classes:

* \(D\): the relative active level is lower by at least one;
* \(U\): the relative active level is higher, with no deterministic
  overshoot bound assumed; or
* \(N\): the active level is unchanged and the endpoint is another base
  mark in \(E\).

Promotion is postponed to Section 4.  The probabilities below are
**aggregate stopped-kernel probabilities**, not probabilities of one
selected reaction word.

> **Hypotheses K(m,r).**  Uniformly in \(e\), for some
> \(m\in\{0,1,2\}\), \(r\ge0\), and positive constants \(a,b,T\),
> \[
> \begin{aligned}
>  {\mathbb P}_{b_{n,e}}(D)&\ge an^{-m},\\
>  {\mathbb P}_{b_{n,e}}(U)&\le bn^{-(m+1)},          \tag{3.2}\\
>  {\mathbb E}_{b_{n,e}}\sigma&\le Tn^r,
>  \qquad m+r\le3.                                   \tag{3.3}
> \end{aligned}
> \]
> Let \(Z\) be the absolute change of the inactive-coordinate part of
> \({\cal F}_{\ell}\) between the initial base mark and the endpoint, and
> put
> \[
>  R_D=(n-X_\sigma)^+,
>  \qquad R_U=(X_\sigma-n)^+.
> \]
> For some fixed \(q>8\) (and, in the application below, for every fixed
> \(q\)), the terminal size-biased moments satisfy
> \[
> \begin{aligned}
>  {\mathbb E}[(1+Z+R_D)^q;D]&\le C_q{\mathbb P}(D),\\
>  {\mathbb E}[(1+Z+R_U)^q;U]&\le C_q{\mathbb P}(U). \tag{3.4}
> \end{aligned}
> \]

Starting from \(b_{n,e}\), repeat raw attempts through their neutral base
marks and stop at the first \(D\) or \(U\) endpoint.  Call the complete
physical stopping time \(\tau_n\).

> **Theorem 3.1 (repeated-base fourth-power episode).**  Under
> K(m,r), for all sufficiently large \(n\),
> \[
>  {\mathbb E}_{b_{n,e}}
>  [W(X_{\tau_n})-W(b_{n,e})+\tau_n]\le-1             \tag{3.5}
> \]
> uniformly in \(e\).

### Proof

Let \(K_n\) be the number of raw attempts.  At every neutral endpoint the
strong Markov property restarts (3.2), possibly with a different mark in
the same finite set.  Therefore

\[
 {\mathbb E}K_n\le a^{-1}n^m,qquad
 {\mathbb P}\{\hbox{the first nonneutral endpoint is }U\}
 \le {b\over a}n^{-1}.                               \tag{3.6}
\]

The second inequality follows by summing the conditional upward
probability over the attempts before absorption.  Similarly,

\[
 {\mathbb E}\tau_n\le (T/a)n^{m+r}.                  \tag{3.7}
\]

This is where physical duration, rather than a count of fast ordinary
jumps, enters.

At a base state,

\[
 G(b_{n,e})=n\log n+O(n),                             \tag{3.8}
\]

uniformly in \(e\).  A unit active decrease changes the factorial part by
\(-\log n+O(1)\).  Expanding the fourth power and using (3.4) gives

\[
 {\mathbb E}[W(X_{\tau_n})-W(b_{n,e})\mid D]
 \le-c_1n^3(\log n)^4+C_1n^3(\log n)^3.              \tag{3.9}
\]

The random inactive endpoint occurs only once.  Its \(q\)-moment creates
the second term in (3.9), one logarithm below the active decrement.  For an
upward endpoint, set \(S=Z+R_U\).  On \(S\le n\), the exact factorial
finite-difference formula and fourth-power Taylor expansion give
\[
 (W(X_{\tau_n})-W(b_{n,e}))^+
 \le Cn^3(\log n)^4(1+S)^4.
\]
On \(S>n\),
\[
 W(X_{\tau_n})
 \le C\{n^4(\log n)^4+S^4\log^4(2S)\}.
\]
Conditional Markov and Hölder inequalities applied to (3.4), with
\(q>8\), make the expectation of the latter display on \(S>n\)
\(O(n^{4-q}(\log n)^4)+O(1)\).  Thus (3.4), without a deterministic
overshoot bound, gives

\[
 {\mathbb E}[(W(X_{\tau_n})-W(b_{n,e}))^+\mid U]
 \le C_2n^3(\log n)^4.                               \tag{3.10}
\]

Equations (3.6), (3.9), and (3.10) imply

\[
 {\mathbb E}[W(X_{\tau_n})-W(b_{n,e})]
 \le-c_2n^3(\log n)^4+C_3n^2(\log n)^4.              \tag{3.11}
\]

Because \(m+r\le3\), (3.7) is smaller than the negative term in (3.11),
including at equality because of the fourth logarithmic power.  This proves
(3.5).  \(\square\)

The neutral attempts in this proof are not charged separately to \(W\).
Their population endpoints telescope inside one stopping episode.  Stopping
after each neutral attempt would be invalid: even a bounded mean-zero
increment \(\xi=\pm1\) has

\[
 {1\over2}\{(G+1)^4+(G-1)^4\}-G^4=6G^2+1>0.         \tag{3.12}
\]

For \(m=2\), this curvature is much larger than the drift of one rare raw
attempt.  Repetition to the first nonneutral relative return is therefore
load-bearing, not cosmetic.

## 4. Countable phases and promotion exits

The finite graph resistance does not itself prove K(m,r).  Two analytic
phase estimates are sufficient in the present reaction menu.

### 4.1 Phase contract

1. A finite killed phase with generator
   \(nQ_{\mathrm{fast}}+Q_{\mathrm{slow}}\)
   must have all fast closed classes contracted.  Finite first-step
   equations then give the aggregate absorption expansions in (3.2), while
   finite-state exponential tails give (3.3)--(3.4).
2. More generally, every unbounded neutral zero-resistance SCC in the
   frozen reaction menu is one dimensional and strongly connected on a
   subset of \(\{0,U,2U\}\).  This includes, but is not limited to, the
   stripped \(0\rightleftarrows U\) immigration--death phase.  Such a phase
   can be treated directly, without a fixed truncation.

The one-dimensional assertion is a consequence of the binary complex
menu, not a tightness assumption.  At a no-fast base every cofactor of an
active-bearing top source is zero.  If both inactive species occur as top
cofactors, the inactive base is \((0,0)\); if the top source is
active-free, there is no no-fast base; and in the sole-cofactor case, call
that absent cofactor \(V\), so the base has \(V=0\).  A neutral
zero-resistance excursion then either uses only the other inactive species
\(U\), or has the two-step form
\(y\to X+V\to z\), with \(y,z\in\{0,U,2U\}\).  If the target \(z\)
contains \(V\), the newly positive top cofactor enables the next unpaired
top exit, so that state is an absorbing descent/promotion outcome rather
than part of the neutral SCC.  Removing those outcomes leaves exactly a
one-species SCC on a subset of \(\{0,U,2U\}\).

Here is the analytic statement used in item 2.  Let \(Q_0\) be the
one-species mass-action generator of a strongly connected graph on a
subset of \(\{0,U,2U\}\), restricted to one irreducible population class.
If that class is infinite, then for some \(\theta\in(0,1)\), \(c,C>0\),

\[
 H_\theta(u)=\exp\{\theta u\log(u+e)\},\qquad
 Q_0H_\theta(u)\le C-cu^pH_\theta(u),               \tag{4.1a}
\]

where \(p=1\) or \(2\) is the maximal source degree of the unbounded
class.

Indeed, if \(2U\) is present, every reaction sourced at \(2U\) has a
nonpositive population increment and strong connectivity supplies at
least one strictly negative such edge.  A downward jump multiplies
\(H_\theta\) by a factor tending to zero, whereas an upward jump multiplies
it by only \(O(u^\theta)\).  Thus the negative quadratic term dominates
every possible \(O(u^{1+\theta})\) positive term.  If \(2U\) is absent,
infinitude and strong connectivity supply a negative \(U\)-source edge;
its negative linear term dominates the \(O(u^\theta)\) constant births.
The same proof covers the two-complex subsets
\(\{0,2U\}\) and \(\{U,2U\}\).  Finite classes need no estimate.

Stopped Dynkin applied to (4.1a) gives the factorial tail
\(C\exp[-cM\log M]\) for the maximum
before regeneration at a fixed finite atom, exponential return-time
moments, and moments of every polynomial occupation integral.  These
bounds remain valid after polynomial size-biasing by a killed reaction
intensity.

For completeness, finite-\(n\) interference does not require a hidden
fixed box.  On the active clock its total coefficient is at most
\(C(1+u)^2/n\).  Choose a moving cutoff \(L_n=n^\delta\) with
\(\delta=1/8\).  For a regeneration cycle begun at its fixed atom, or
from a family with a uniform exponential moment, the probability of
hitting \(L_n\) is \(O(e^{-cL_n\log L_n})\).  Iterate the ordered
compensation formula in the factorially weighted space.  Equation (4.1a)
supplies every polynomial occupation moment, so the first two killed-
resolvent coefficients are finite and the third ordered remainder stopped
below \(L_n\) is bounded by \(C(L_n^2/n)^3\).  No unweighted sup-norm
Neumann estimate on a growing box is used.  Thus the positive coefficient
and the vanishing
lower-order coefficients computed by the graph resistance calculation
lift to the **aggregate** stopped probabilities in (3.2), and (3.3)--(3.4)
follow with uniform endpoint moments.  What remains open here is the graph
calculation of those coefficients, not the countable-phase truncation.
This tail estimate is deliberately not asserted for a start comparable to
\(L_n\).  Such a start may reach the moving boundary with order-one
probability and is routed as a genuine promotion outcome under Section
4.2, rather than discarded as a rare phase excursion.

An individual word of resistance \(m+1\) is not an aggregate estimate.
For example, suppose each visit has upward probability \(n^{-(m+1)}\),
neutral-exit probability \(n^{-1}\), and otherwise loops.  The eventual
upward probability is

\[
 {n^{-(m+1)}\over n^{-(m+1)}+n^{-1}}
 ={1\over n^m+1}=\Theta(n^{-m}).                     \tag{4.1}
\]

Thus a killed-resolvent or regeneration estimate is indispensable.

### 4.2 The all-23 moving-boundary lift

The exact support reduction has 23 analytic templates.  The following
result removes promotion access as a separate hypothesis.  Its sole
unproved input is the arbitrary-orientation **aggregate resistance
ordering**.

Fix \(\delta=1/8\) and \(L_n=n^\delta\).  Contract zero-resistance fast
classes.  Start with positive reflected mark \(D_X>0\) and measure relative
active displacement from zero; until its first negative value, reflection
is inactive and that event is exactly a strict reduction of old \(X\)-debt.
Suppose the resulting all-reaction formal kernel, from each regenerative
base mark, has

\[
 p_D(n)\ge an^{-m},\qquad
 p_U(n)\le bn^{-(m+1)},\qquad
 {\mathbb E}\sigma\le Tn^r,                         \tag{4.2}
\]

for some \(m\in\{0,1,2\}\), \(m+r\le3\).  Here \(D\) is the first
post-jump state with negative relative active displacement, wherever it
occurs; \(U\) is the first positive relative return to a no-fast base.  The
coefficients are aggregate killed-kernel coefficients, after every neutral
loop, not the weight of one reaction word.  Stop a raw physical attempt
also at \(P\), the first post-jump state at which an inactive population
reaches \(L_n\) strictly before \(D\) or \(U\).  The boundary-causing jump
is part of the attempt and hence part of its endpoint cost.  If one jump
both crosses the boundary and triggers \(D\) or \(U\), retain its \(D/U\)
terminal label but put its endpoint in the boundary charge event
\({\cal B}\).  Thus \({\cal B}\) consists of \(P\) and all simultaneous
boundary ties; no boundary-sized endpoint is charged using the bounded
\(D/U\) moment estimate.

> **Theorem 4.1 (network-specific analytic lift, conditional on (4.2)).**
> For every nonfrozen one of the 23 templates, every strong orientation,
> and every positive rate vector satisfying the aggregate ordering (4.2), the raw
> kernel has the phase, endpoint, and duration estimates needed by
> Theorem 3.1.  Repeating neutral base returns until \(D\), \(U\), or
> \(P\) gives, for all sufficiently large \(n\),
> \[
>  {\mathbb E}_{b_{n,e}}
>  [W(X_{\tau_n})-W(b_{n,e})+\tau_n]\le-1.           \tag{4.3}
> \]
> Every endpoint in the boundary charge event \({\cal B}\) is an
> at-least-two-active, generator-good state.
> Thus ordinary common-\(W\) gluing, rather than a return to the old axis,
> continues the physical process from that endpoint.

The exact access partition is also exhaustive.  The 123 frozen incidences
have no enabled reaction on their displayed face and are a finite-class
alternative.  The 2,471 direct incidences and the 461 zero-source plus 20
nonzero-source seeds have fixed finite initial phases, which are included
among the base marks in \(E\).  The remaining 222 incidences are precisely
the wholly-top open phase treated below.  Thus no unlisted initial-access
mechanism is hidden by the 23-template quotient.

There is a sharper architecture corollary.  Among the 3,075 mixed-phase
incidences, the 1,695 rows containing the mixed source \(X\) are immediate
killed phases.  Families I and III have only the origin as a no-fast base.
In Family II the apparent spectator has an exact linkage invariant.  On a
fixed irreducible class \(\Gamma\), write its conserved value as
\(a_\Gamma\).  The atlas cap \(0,1,2\) records only the availability type
\(a_\Gamma=0\), \(a_\Gamma=1\), or \(a_\Gamma\ge2\); it does not assert
\(a_\Gamma\le2\).  For each fixed \(\Gamma\) the resulting axis base is
finite, with constants allowed to depend on \(a_\Gamma\).  After fast SCC contraction,
the Duhamel/ordered-compensation expansion is therefore finite in these
rows.  If the graph theorem supplies a minimal down resistance \(m\), a
positive down coefficient, and no up word through resistance \(m\), that
expansion gives

\[
 p_D(n)\ge a n^{-m},\qquad
 p_U(n)=O(n^{-(m+1)}),                               \tag{4.3a}
\]

with all neutral loops already summed by the resolvent.  The sole
unbounded base phase is the set of 222 wholly-top
\(\{X,X+U\}\) incidences.  Theorem 6.1 and Lemma 7.1 of
`research_notes/one_active_countable_phase_service.md` give their full
Poisson-averaged all-reaction block: it has \(m=0\) whenever historical
old debt is possible, and otherwise is a no-debt/frozen alternative.
The word resistance recorded for this open family is one, but it must not
be substituted for the aggregate exponent: Poisson recurrence supplies
order-one repeated service, hence the effective block value \(m=0\).
Consequently (4.2) is an analytic corollary of the arbitrary-orientation
graph resistance statement; it is not an additional stochastic
hypothesis.

> **Proposition 4.2 (resistance-to-aggregate kernel).**  In every mixed
> row, let \({\mathsf P}_n\) be the endpoint kernel of one complete local
> block: a no-fast-base regeneration cycle when such a base exists, and
> the immediate killed block in a direct-\(X\) row.  Stop it at inactive mass
> \(L_n=n^{1/8}\).  In every fixed endpoint-polynomial norm,
> \[
>  {\mathsf P}_n
>   ={\mathsf P}^{(0)}+n^{-1}{\mathsf P}^{(1)}
>    +n^{-2}{\mathsf P}^{(2)}+{\mathsf R}^{(3)}_n.   \tag{4.3b}
> \]
> If the graph down/up resistances are \(m_- =m\le2\) and
> \(m_+\ge m+1\), then
> \[
>  p_D(n)\ge an^{-m},\qquad
>  p_U(n)\le bn^{-(m+1)},                            \tag{4.3c}
> \]
> the raw duration is bounded uniformly in \(n\), and every fixed
> \(q\) has a constant \(C_{\Gamma,q}\) such that each nonboundary
> terminal \(E\in\{D,U\}\) satisfies
> \[
>  {\mathbb E}[(1+Z+R_E)^q;E]
>  \le C_{\Gamma,q}{\mathbb P}(E).                  \tag{4.3c'}
> \]
> Moreover, for every fixed \(q\),
> \[
>  \|{\mathsf R}^{(3)}_n\|_q
>  \le C_q(L_n^2/n)^3.                               \tag{4.3d}
> \]

To prove the proposition, a direct-\(X\) row first uses its immediate
killed unimolecular burst.  The stripped process may be open, but its
active-time Green operator and polynomially size-biased endpoints have
uniform exponential moments; the strict exit is an \(m=0\) event.  In the
remaining rows, begin a cycle on its exact zero-order no-fast slice: the
origin in Families I and III, or the fixed invariant slice
\(a_\Gamma\) in Family II.  After \(k\le2\) suppressed lower firings,
carrier conservation gives total transient inactive/carrier mass at most
\(a_\Gamma+3k+6\) (with \(a_\Gamma=0\) in Families I and III).

Here is the endpoint-weighted Green estimate used below.  For fixed
\(\Gamma\), orientation, and rates, let \({\cal E}_{\Gamma,k}\) be the
finite contracted phase reachable before a terminal mark after
\(k\le2\) paid firings.  In active time
\(s=\int_0^t X_u\,du\), contract every closed zero-reward class as a
regenerative base terminal and let \(Q^{(0)}_{\Gamma,k}\) be the remaining
killed top-only subgenerator.  Every transient communicating class has a
directed path to a killed or regenerative terminal.  Hence, by finiteness,
there are \(c,C>0\) such that

\[
 \|e^{sQ^{(0)}_{\Gamma,k}}f\|_q
 \le Ce^{-cs}\|f\|_q,
 \qquad
 \|G^{(0)}_{\Gamma,k}f\|_q
 \le C\|f\|_q,                                      \tag{4.3b'}
\]

for every fixed endpoint-polynomial norm
\(\|f\|_q=\max_{z\in{\cal E}_{\Gamma,k}}
|f(z)|/(1+M(z))^q\).  The actual active-time subgenerator converges
entrywise to \(Q^{(0)}_{\Gamma,k}\); the same inequalities, with
\(c/2,2C\), hold uniformly for all large \(n\).  This follows either from
the finite spectral bound or directly by multiplying the positive exit
probabilities along the finitely many terminal paths.  Thus (4.3b') covers
every finite contracted mixed orientation and every allowed finite base
start; it is not a bare finite-box assertion.

In a direct-\(X\) row the stripped phase may be infinite, and its paid
intensity can grow like \(M^2\).  It would therefore be false to treat the
paid multiplication operator as bounded in one fixed polynomial sup norm.
Instead choose
\(0<\theta_3<\theta_2<\theta_1<\theta_0<\theta_*\), where the exponential
Foster estimate (4.4) holds up to \(\theta_*\), and write
\(H_\theta(M)=\exp\{\theta q\mathbin{\cdot}(A,B)\}\) for its weight.
Dynkin's formula and
\((1+M)^2H_{\theta_{j+1}}(M)\le C_jH_{\theta_j}(M)\) give the nested
occupation hierarchy

\[
 {\mathbb E}_z\int_0^{\sigma_0}
 (1+M_s)^2H_{\theta_{j+1}}(M_s)\,ds
 \le C_jH_{\theta_j}(M(z)),
 \qquad j=0,1,2.                                    \tag{4.3b*}
\]

Here \(\sigma_0\) is the next killed/regenerative endpoint in active time.
Compensation applies (4.3b*) successively after each paid firing.  Starting
from the fixed base set, all zero-, one-, and two-interruption coefficients
have a uniform \(H_{\theta_3}\)-moment, hence every polynomial endpoint
moment; the three-interruption remainder has the corresponding nested
exponential weight.  This is the direct-phase substitute for the finite
\(q\to q\) estimate (4.3b').

For a finite mixed phase, define the stopped one-interruption kernel
\({\mathsf K}_{n,k}\) as follows: from a phase in
\({\cal E}_{\Gamma,k}\), run the zero-order top process until its next
terminal mark or its first paid lower-source clock; on the latter event,
apply the physical jump and record the new phase in
\({\cal E}_{\Gamma,k+1}\).  One paid clock has active-time rate at most
\(C_\Gamma(1+M)^2/n\), so (4.3b') gives

\[
 \|{\mathsf K}_{n,k}\|_{q\to q}\le C_{\Gamma,q}/n,
 \qquad k=0,1,2.                                    \tag{4.3b''}
\]

Let \({\mathsf A}_{n,k}\) be the endpoint kernel obtained when the
zero-order process reaches a terminal before the next paid clock.  The
strong Markov property gives the exact stopped renewal identity

\[
 {\mathsf P}_n
 = {\mathsf A}_{n,0}
 +{\mathsf K}_{n,0}{\mathsf A}_{n,1}
 +{\mathsf K}_{n,0}{\mathsf K}_{n,1}{\mathsf A}_{n,2}
 +{\mathsf K}_{n,0}{\mathsf K}_{n,1}{\mathsf K}_{n,2}
   {\mathsf P}^{[3]}_n.                             \tag{4.3b'''}
\]

On the finite phases, the falling-factorial rates divided by the active
level have a uniform expansion in \(n^{-1}\); hence
\({\mathsf A}_{n,k}\) and \(n{\mathsf K}_{n,k}\) converge in every norm
in (4.3b').  Expanding the first three terms of (4.3b''') gives (4.3b).
Equivalently, these coefficients are finite sums of marked physical
histories with exactly zero, one, or two paid firings.  Every history
weight is nonnegative; killing by the competing paid clocks only changes
higher orders.  Therefore terms below a graph resistance vanish, while a
minimal graph witness contributes a strictly positive leading
coefficient.  Apply the same expansion after multiplying an \(E\)-endpoint
by \((1+Z+R_E)^q\).  Its first nonzero order is no smaller than the
unweighted \(E\)-probability order, and the Green hierarchy makes its
coefficient finite.  Dividing by the positive leading probability
coefficient (or taking both sides zero when \(E\) is inaccessible) proves
(4.3c').  The final term in (4.3b''') is the endpoint-weighted remainder.
This is the promised uniform killed-resolvent lemma, rather
than an appeal to unspecified ``standard'' first-step equations.
At resistance \(m_-\), at least one physical graph witness has a product of
strictly positive rates, so the first nonzero down coefficient is positive;
the condition \(m_+\ge m+1\) removes every up coefficient through order
\(m\).  When \(m=2\), the coefficient cancellation alone is not enough:
one also needs an unweighted third-order remainder.  Before the \(k\)-th
paid interruption, \(k\le3\), the carrier estimate above bounds the
transient mass by \(a_\Gamma+3(k-1)+6\).  Therefore (4.3b') gives

\[
 \big\|G_{n,\Gamma,k}^{(0)}Q_{{\rm paid},n}\big\|_\infty
 \le {C_\Gamma\over n},
 \qquad k=1,2,3.
\]

Multiplying the three ordered kernels yields

\[
 {\mathbb P}_{b_{n,e}}
 \{J_{\rm raw}\ge3\hbox{ by the raw }D/U/N/P\hbox{ terminal}\}
 \le C_\Gamma n^{-3}.                               \tag{4.3e}
\]

Here any zero-resistance free launch is part of
\({\mathsf P}^{(0)}\), while \(J_{\rm raw}\) counts paid/suppressed
operators.  An \(m=2\) up-return has resistance at least three and is
contained in (4.3e).  Thus (4.3e), not the weaker weighted moving-cutoff
estimate below, supplies \(p_U=O(n^{-3})\).  Together with the finite-order
coefficients this proves (4.3c).  The same Green bounds prove the duration
and nonboundary endpoint assertions.  The fixed minimal down witness uses
at most \(m\le2\) paid firings and remains in mass
\(a_\Gamma+3m+6\); hence it is nonboundary once
\(L_n>a_\Gamma+12\).  After decreasing the leading constant if necessary,
\(p_{D\setminus{\cal B}}(n)\ge (a/2)n^{-m}\).  Thus the strict down reward
is never inferred from a boundary-sized \(D\)-tie.

For three or more firings, stop at mass \(L_n\).  Each ordered
interruption operator has weighted norm at most \(CL_n^2/n\); the
factorial/unimolecular occupation hierarchy absorbs every endpoint
polynomial.  Three iterations give (4.3d), including the ordered count
moment used in (4.9).  This is the precise aggregate argument which a
selected reaction word alone could not supply.  In the 222 open rows,
Proposition 4.2 is replaced, not imitated, by the Poisson service theorem:
geometric repetition of its fixed-positive service block has effective
\(m=0\), \(O(n^{-1})\) unresolved-arrival probability, bounded duration,
and all endpoint moments.

#### Phase dichotomy

There are only two possible unbounded pieces between suppressed
lower-source interruptions.

1. While an active-bearing source is enabled, stripping the common active
   molecule leaves a killed unimolecular graph on a subset of
   \(\{0,A,B\}\).  A closed conservative class has fixed \(A+B\) and is
   finite.  An open closed class is an immigration--death--conversion
   network.  Strong connectivity gives a positive linear weight \(q\) for
   which its linear drift is at most \(C-cq\mathbin{\cdot}(A,B)\).  For
   small \(\theta>0\), the exponential Lyapunov function
   \[
    \exp\{\theta s\},
    \qquad s=q\mathbin{\cdot}(A,B),                  \tag{4.4}
   \]
   has negative linear-times-exponential drift outside a finite set.
2. At a no-fast base, Section 4.1 reduces every unbounded neutral SCC to a
   strongly connected one-species graph on a subset of
   \(\{0,U,2U\}\).  The factorial Lyapunov function used in (4.1a) is
   \[
    H_\theta(u)=\exp\{\theta u\log(u+e)\},
    \qquad 0<\theta<1,                               \tag{4.5}
   \]
   gives
   \(Q_0H_\theta\le C-cu^pH_\theta\), with
   \(p=1\) or \(2\).  A negative maximal-degree edge dominates because
   an upward jump multiplies \(H_\theta\) by only \(O(u^\theta)\).

Consequently a regeneration cycle begun at its fixed atom has

\[
 {\mathbb P}\{\max(A+B)\ge L\}
 +{\mathbb P}\{\max U\ge L\}
 \le C\exp[-cL].                                    \tag{4.6}
\]

The same bound, with changed constants, survives every fixed polynomial
size bias and every sequence of at most two suppressed interruptions.
Transient components either enter one of these closed classes or hit
\(D\cup U\) in finitely many phase transitions.  This proves the claimed
dichotomy without replacing an inactive population by a fixed box.

#### Carrier and endpoint bounds

Bounded stoichiometric jumps alone would not control active overshoot.  Let
\(J\) be the total number of paid/suppressed lower-source firings in one raw
attempt (including lower-to-lower and lower-to-top firings, but excluding
any zero-resistance free launch already included in
\({\mathsf P}^{(0)}\)).  The exact
23-template support table supplies the correct carrier
statement: after at most one free launch, every further positive relative
active increment before a base return is a lower-to-top member of that
count.
Thus

\[
 (X_t-n)^+\le C(1+J).                               \tag{4.7}
\]

This formulation is necessary.  Nested entries can repeatedly raise the
active count while keeping the instantaneous inactive mass bounded, so a
pathwise estimate solely by \(A+B\) would be false.

If the pure active complex \(X\) is itself a top source, no no-fast base
exists and the row is handled by the direct killed unimolecular block.
The wholly-top rows are exactly the open pairs
\(\{X,X+U\}\); their top reactions preserve the active count and their
stripped immigration--death process regenerates at \(U=0\).  These two
separate routes prove the carrier alternative in every intended template;
no unsupported ``bounded jumps imply bounded overshoot'' assertion is
used.

On \((D\cup U)\setminus{\cal B}\), the factorial tails above give (3.4),
including after the killing-intensity size bias.  On
\({\cal B}\cap\{J\le2\}\), (4.7) and the factorial finite-difference
formula give the deterministic stopped bound

\[
 (W(X_{\tau_n})-W(b_{n,e}))^+
 \le Cn^{3+\delta}(\log n)^4.                       \tag{4.8}
\]

#### Three-interruption remainder

After zero, one, or two suppressed interruptions, (4.6) makes a boundary
hit superpolynomially unlikely.  Every other path in the boundary charge
event \({\cal B}\) contains at least three interruptions.  Below \(L_n\),
each interruption kernel is
bounded in the factorially weighted resolvent norm by
\(CL_n^2/n\).  Iterating the ordered compensation formula three times,
using the all-order occupation bounds from (4.4)--(4.6), gives the
**stopped, endpoint-weighted** remainder

\[
 \begin{split}
 {\mathbb P}_{b_{n,e}}({\cal B}\hbox{ in one raw attempt})
   &\le Cn^{-3+6\delta},\\
 {\mathbb E}_{b_{n,e}}
  [(1+\sigma+J)^q;{\cal B},J\ge3]
   &\le C_qn^{-3+6\delta}                            \tag{4.9}
 \end{split}
\]

for every fixed \(q\).  A nonboundary large-\(J\) up-return is controlled
by the finite Green expansion and, when \(m=2\), by the separate
unweighted estimate (4.3e).  The \(J\)-weight in (4.9) controls nested
active entries at a boundary endpoint; this is not an unweighted
finite-box Neumann assertion.  More explicitly,
the factorial finite-difference and fourth-power expansion give
\[
 (\Delta W)^+
 \le Cn^3(\log n)^4(L_n+J)
   +C(L_n+J)^4\log^4(n+L_n+J).                      \tag{4.9a}
\]
Use (4.9) first with \(q=1\) in the leading term and then with a fixed
\(q>8\) to absorb the second term and its logarithm.  The inactive
boundary contribution is \(L_n\) times the probability in (4.9), while
the active contribution is controlled by the \(J\)-moment.  The positive
\(W\)-cost per raw attempt is therefore at most
\(Cn^{7\delta}(\log n)^4\), up to a superpolynomial term.

The completed episode uses at most \(Cn^m\le Cn^2\) raw attempts in
expectation.  Therefore

\[
 {\mathbb P}({\cal B})\le Cn^{-1+6\delta},
 \qquad
 {\mathbb E}[(\Delta W)^+;{\cal B}]
 \le Cn^{2+7\delta}(\log n)^4.                     \tag{4.10}
\]

For \(\delta=1/8\), the last power is \(23/8<3\).  It is lower order than
the down-return reward \(-cn^3(\log n)^4\).  Likewise the up-return cost is
\(O(n^2(\log n)^4)\), neutral base endpoints telescope exactly, and

\[
 {\mathbb E}\tau_n\le Cn^{m+r}\le Cn^3.             \tag{4.11}
\]

In the 222 open rows, a fixed geometric number of Poisson service blocks
replaces exact base-mark telescoping.  Their uniformly bounded factorial
endpoint moments make the total neutral inactive contribution only
\(O(n^3(\log n)^3)\), again one logarithm below service.

Equations (3.9)--(3.11) and (4.8)--(4.11) prove (4.3).  The exponent
arithmetic is frozen independently in
`research_notes/moving_cutoff_fourth_power_lemma.md`.

#### Why no promotion return is needed

At a genuine \(P\)-endpoint, \(D\) has not occurred, so the active
coordinate is at least \(n\); no upper bound is asserted because \(J\)
can be large.  At a simultaneous boundary--\(D\) tie, the unit active exit
in the one-active menu leaves active population \(n-1\); a boundary--\(U\)
tie has active population above \(n\).  In every case another coordinate
has reached at least \(n^{1/8}\).  Thus every \({\cal B}\)-sequence has an
at-least-two-active tier refinement.  On the exact selector all such
descriptors pass, so (2.7) applies.  The local episode stops at the
post-jump boundary state; (4.8)--(4.10) include both the promotion entry
jump and every simultaneous boundary tie.  The global stopping policy
then uses the ordinary generator rule
until a finite target or a one-active interface is reached.  Localization
and Fatou applied to \(W\), and to the concave transform following (2.7),
control the endpoint and physical duration.  A return at a different
active level is simply reclassified from its actual population; it is not
forced back to the old axis and creates no hidden same-axis endpoint cost.

## 5. Conditional global gluing theorem

> **Theorem 5.1 (one-active interface composition).**  Fix a closed
> irreducible class and one common \(W\) from (1.1).  Suppose:
>
> 1. every divergent at-least-two-active sequence has the quantitative
>    passing margin (2.2);
> 2. every nonfrozen one-active interface satisfies the aggregate graph
>    ordering (4.2); and
> 3. the common population potential is (1.1) with \(\ell=0\).
>
> Then the physical CTMC is positive recurrent on that class.

Work on the all-species reflected marked chain of
`research_notes/all_species_reflected_debt_target.md`.  If \(X\) is the
selected coordinate of a fixed-width one-active tube and its mark
\(D_X=0\), then \(X=H_X\le x_X^\circ\); the inactive coordinates are
tube-bounded, so these states form a finite class-dependent exception.
Invoke Theorem 4.1 only when \(D_X>0\).  Its \(D\)-endpoint then strictly
reduces existing old debt; no surplus reaction at zero debt is required.
When every mark is zero, the pathwise monotonicity
\(H_i=X_i-D_i\le x_i^\circ\) puts the marked state in a finite target.

Indeed, (2.7) gives \({\cal L}W\le-1\) outside the one-active interfaces and
a finite set.  Theorems 3.1 and 4.1 give
\({\mathbb E}[\Delta W+\tau]\le-1\) on every nonfrozen interface, including
the terminal moving-boundary cost.  Alternating these
physical stopping rules and localizing at finite \(W\)-sublevels gives a
nonnegative supermartingale.  Bounded-index telescoping, followed by Fatou,
proves finite mean hit of the finite target.  The finite-set trace then
gives positive recurrence.  Population-increasing propensities are at most
linear, so the process is nonexplosive.

This theorem is an interface theorem.  The separately certified
arbitrary-orientation result supplies a strict reduction resistance
\(m\le2\), no same-base upward term through order \(m\), and a positive
down coefficient in every finite mixed family; the Poisson theorem supplies
the distinct effective \(m=0\) open-family block.  Sections 3--4 lift those
inputs to the aggregate physical kernel, endpoint moments, duration, and
moving promotion boundary.  The combined selector/common-potential theorem
has received an independent pair-level PASS and certifies the exact
1,227-pair branch.  Global T3-2 remains uncertified regardless.

## 6. Counterexamples to weaker formulations

The proof above also isolates four exact failure modes.

1. **Raw neutral curvature.**  Equation (3.12) shows that bounded,
   mean-zero inactive motion is not harmless after taking a fourth power.
   One must telescope to the first nonneutral return or prove the powered
   neutral cost directly.
2. **Wordwise resistance.**  Equation (4.1) shows that countably many loops
   can lose one full resistance order.  Only the aggregate killed kernel is
   relevant.
3. **Duration without regeneration.**  A neutral branch may enter a null
   recurrent countable phase with infinite mean return.  Endpoint
   probabilities alone then do not define a physical Foster episode.
4. **Uncontrolled promotion tails.**  A probability \(n^{-(m+1)}\) can
   still carry an endpoint of superpolynomial size.  Resistance alone does
   not bound \({\mathbb E}W(X_\rho)\); the stopped, endpoint-weighted
   estimate (4.9), and not a bare boundary probability, is necessary.

The companion claim-neutral executable is
`src/universal_fourth_power_interface_regression.py`, with focused tests in
`tests/test_universal_fourth_power_interface_regression.py`.
