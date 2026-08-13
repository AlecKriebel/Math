# Hostile requirements for a global 18,496-pair hybrid-potential theorem

**Proof-first obstruction and repair note, 2026-08-12 PDT.** This note audits
the proposed global potential

\[
 {\cal V}(x,t)=(K+P(x))^4+\alpha(K+F(x,t))^4,
 \quad
 P(x)=\sum_i\log(x_i!),
 \quad
 F(x,t)=\sum_i\log((x_i-t_i)!).                       \tag{1.1}
\]

The exact 18,496-pair finite classification is independently frozen at

~~~text
src/outside_mixed_remaining_18496_certificate.py
314f378664052cabe23910e118c9a43acf99884ccb5c63b61daf014a206e4c63
tests/test_outside_mixed_remaining_18496_certificate.py
28d3cf0087bcd77e24d6dbfa280b226b34d3d026c35e743bc10487c829667769
research_notes/proof_first_outside_mixed_remaining_18496_certificate_exact_byte_audit.md
2539d8eee4d1d584ed5566f7494c7262843676dc368078647db12481d6a5822f
~~~

That certificate proves only the finite identity

\[
 18{,}496=11{,}842\ {\rm no\ failure}
          +6{,}654\ {\rm failed},                    \tag{1.2}
\]

with 21,906 failure rows, exactly 15,204 B/F0, 3,618 B/B, and
3,084 AA. The present note identifies the analytic theorem still required.
It makes no recurrence claim.

## 1. Exact population increment and the enabled-target lemma

For a reaction \(e:y\to u\), with endpoint \(x'=x-y+u\), factorial
cancellation gives

\[
 P(x')-P(x)=\log\frac{(x')_u}{(x)_y}.                 \tag{1.3}
\]

If \(u\) is already enabled at \(x\), binary bounded-shift comparison gives

\[
 K_u(x')_u\le C_eK_u(x)_u.
\]

Writing \(p_v=K_v(x)_v/\Lambda(x)\), (1.3) implies

\[
 [\Delta P]_+
 \le C_e+\left[\log\frac{p_u}{p_y}\right]_+.          \tag{1.4}
\]

Consequently, for every fixed \(q<\infty\), summing over the finite labelled
reaction set gives

\[
 \sum_e p_{s(e)}\,[(\Delta_eP)_+]^q\le C_q,           \tag{1.5}
\]

**provided every included target was enabled before its jump**. Indeed,
\(r(C+\log(1/r))^q\) is bounded for \(r=p_y/p_u\), and the remaining
factor \(p_u\) sums over a finite source menu.

Equation (1.5) is the valid source-target comparison. It does not extend to
a newly enabled target.

## 2. Literal in-scope counterexample to a one-jump bound

Let the active species be B and take the exact remainder pair

\[
 L_b=\{0,A,2A,A+B\},
 \qquad
 L_0=\{C,2C,A+C\}.                                   \tag{2.1}
\]

It has a certified B/F0 failure at weight \((0,1,0)\) and caps
\((0,2,0)\). Choose on \(L_b\) a strong orientation containing

\[
                    0\longrightarrow A+B             \tag{2.2}
\]

(for example, include it in a directed cycle through the other vertices).
At

\[
                         x=(0,n,0),                   \tag{2.3}
\]

every source except zero is disabled. Thus (2.2) is the next reaction with
probability one, yet

\[
 P(1,n+1,0)-P(0,n,0)=\log(n+1).                      \tag{2.4}
\]

The marked state with target zero is physically reachable, for example
after a \(2A\to0\) reaction from an A-population of two. Therefore

\[
 \sup_{x,t}\mathbb E_{x,t}[(\Delta P)_+]^q=\infty
\]

even within the exact 18,496 family. Source entropy cannot pay (2.4):
\(p_0=1\). The obstruction is precisely that the disabled target \(A+B\)
becomes a source of order \(n\) only after the jump.

For a favorable simple cycle the complete Bellman word repairs the debt:

\[
 0\to A+B\to A,\qquad\hbox{then one ordinary jump at }A. \tag{2.5}
\]

The activation first adds one B, the transition to A removes it, and the
final fast \(A+B\)-sourced jump removes another B with high probability.
Thus (2.4) is not evidence against recurrence; it proves that the episode
may not stop or reclassify immediately after activation.

## 3. Why common potential alone does not repair the gap

On a failure chart, the marked Bellman theorem gives
\(\mathbb E\Delta F=-a(x)\), where \(a(x)\to\infty\), but the divergence may
be only an iterated logarithm. A newly enabled target can cost
\(\Delta P=\Theta(\log R)\), as in (2.4). Hence no fixed coefficient
\(\alpha\) in (1.1) can absorb the activation merely from
\(a(x)\to\infty\).

Stopping at that jump and invoking a common potential in the next chart is
also invalid. A finite chart graph can contain a closed cycle made entirely
of exit-only nodes. Common potential removes a comparison toll but does not
create negative reward on such a cycle. This is the same finite-circulation
obstruction already exhibited by the biased birth-death/parity example.

The repair must be an unconditional physical episode, not a terminal-chart
argument.

## 4. Required killed top-source completion

Every jump whose target was disabled must be classified as a hazard
activation. The episode must continue from its actual target through the
finite high-source kernel. It may stop only when one of the following has
occurred:

1. a genuine lower-degree or D-descending service jump has paid the
   accumulated population-factorial debt;
2. a separately proved population-generator region has been entered and
   its first charged service has been included; or
3. the physical class has entered a closed invariant reduction that is
   proved recurrent independently.

In particular, a deviation from a prescribed Bellman path to another
degree-preserving top complex is not a stopping event. It is another state
of the killed top kernel. Strong connectivity implies that a closed top
subset has an outgoing edge to a lower complex, but the proof must convert
this graph fact into an all-clock estimate while retaining the competing
linkage.

The exact load-bearing stochastic statement is:

> **Missing episode-level population-moment lemma.** For every B/B, B/F0,
> or AA failure state, there is an all-clock stopping time \(\tau\), selected
> from a finite support-dependent menu and not stopped by a descriptor
> change, such that its endpoint is physical and
> \[
> \begin{aligned}
> &\mathbb E\Delta F\le-a(x),\qquad a(x)\to\infty,\\
> &\sup\mathbb E[((\Delta P)^+)^4]<\infty,\\
> &\mathbb E|\Delta F|^4+\mathbb E|\Delta P|^4
>       \le C\{1+\log(2+|x|)\}^4,
> \end{aligned}                                      \tag{4.1}
> \]
> with an integrable duration and a positive-duration physical tiling.

The second line is episode-level; the counterexample in Section 2 rules out
its one-jump version. A geometric event-count bound for the killed top
kernel and exact telescoping of activation/service increments are sufficient
ways to prove (4.1).

## 5. Conditional fourth-power lift

The episode lemma (4.1) is the missing failure-side input.  The no-failure
side is a separate pointwise population-generator theorem, not a conclusion
of the frozen corrected-tier *marked* theorem.  It follows from the
corrected S-tier and affine-feasibility theorem together with the universal
fourth-power passing-cone calculation, exactly as in Section 5 of the frozen
432-pair theorem.  The relevant publication pins are

~~~text
research_notes/s_tier_superlevel_cut_and_affine151_corrected.md
d91f369d34cadfb28ddb872df8fb9f6d17799ec207da29933037f55ae95f0407
research_notes/stoichiometric_gate_feasibility.md
27b40b61903ae6c2e223d007ec08323ec9aec10e9198deb99d2d7c60d878d007
research_notes/universal_fourth_power_one_active_interface.md
9d4239f4fc6b45a9522b94b09523c9f98ac7a3b089c919bd9594f12409c78cc2
~~~

On every feasible no-failure escaping sequence, these inputs give

\[
 {\cal L}(K+P)^4\le-c(K+P)^3A(x)g(x),
 \qquad g(x)\longrightarrow\infty,                  \tag{5.1}
\]

where \(A(x)\) is the top-hazard scale.  The marked one-jump moment identity
bounds the positive generator contribution of \((K+F)^4\) by
\(C(K+F)^3A(x)\).  This is a pointwise generator statement, not a
drift-or-structural-exit alternative.

If (4.1) is proved, these no-failure inputs make the hybrid potential
strategy sound. Since marks are binary and finite,

\[
 K+P(x)\asymp K+F(x,t)\asymp |x|\log(2+|x|).          \tag{5.2}
\]

The fourth-power expansion and (4.1) give, on a failure sequence,

\[
 \mathbb E\Delta{\cal V}
 \le C(K+P)^3-\alpha\,4(K+F)^3a(x)
 +o\!\left((K+F)^3a(x)\right)\longrightarrow-\infty. \tag{5.3}
\]

The logarithmic fourth-moment remainder is lower order even when \(a(x)\)
diverges arbitrarily slowly.

On a no-failure sequence, the two pointwise generator bounds above show that
the negative population term dominates the positive marked term
for every fixed finite \(\alpha>0\). The 11,842 no-failure branch and the
failure episodes would then use one proper potential without a chart exit.

This is a conditional proof, not a substitute for the missing episode lemma
(4.1).

## 6. Exact invariant/rank reductions

The failed-pair rank histogram is

\[
 \begin{array}{c|rrr}
 \operatorname{rank}&1&2&3\\ \hline
 \text{pairs}&6&228&6420.
 \end{array}                                         \tag{6.1}
\]

The six rank-one pairs form one species-permutation/linkage-reversal orbit
with representative

\[
                    \{A,A+B\}\mid\{C,B+C\}.           \tag{6.2}
\]

They have only B/B failures. A and C are fixed catalysts on every class, so
the remaining B-chain is an elementary linear birth-death chain or an
absorbing singleton.

Of the 228 rank-two pairs, 120 are B/F0 and 108 are B/B. For every rank-two
B/F0 failure, the unique primitive nonnegative invariant has zero
coefficient exactly at the active coordinate. Hence both inactive
coordinates are globally bounded on a fixed class. These 120 pairs reduce
to a genuinely finite inactive phase, not a chart-local padded box.

The rank-two B/B pairs conserve only one inactive coordinate in general;
they do not inherit the same finite-phase reduction. The 6,420 rank-three
pairs have no linear invariant reduction. The killed top-source lemma
remains load-bearing for those branches.

## 7. The B/F0 closed no-kill alternative

Before top access, relabel so the B witness is \(q=X+U\). If no
positive-X-degree B source is enabled, then \(U=0\). Any continued
nonaccess reaction has source and target among

\[
                         \{0,V,2V\};                  \tag{7.1}
\]

a target containing U or X is itself access and must be charged as in
Section 4. Thus the nonaccess motion is a killed one-species binary chain.

A closed no-kill component preserves X, but that fact alone does not make
the physical class finite: V may remain unbounded. The required final step
is a one-species factorial Foster argument. In any unbounded closed no-kill
class, take the largest source degree \(d\in\{1,2\}\). Strong connectivity
and closedness force a \(d\)-degree source to have a nonkill edge to a
strictly lower degree; its negative rate is order \(V^d\), while every
positive jump has lower source degree. Hence the one-species population
factorial has negative drift outside a finite set. If no such unbounded
class exists, the component is finite.

Accordingly, ``X is class-invariant'' must be followed by this one-dimensional
service proof; it is not by itself a recurrence theorem.

## 8. Strict audit verdict

The exact 18,496 support classification is complete. The proposed hybrid
potential is **not yet a theorem** because the one-jump population-moment
claim is false and structural-exit reclassification does not repair it.
The exact repair is the unconditional killed top-source completion (4.1),
together with the one-dimensional closed-phase argument in Section 7.
Absolutely no terminal chart-exit shortcut is admissible.
