# Exact-byte audit of the 6,654-pair common-marked recurrence theorem

**Independent proof-first audit, 2026-08-12 PDT.**  The immutable target is

~~~text
research_notes/proof_first_remaining_18496_failure_6654_common_marked_recurrence_theorem.md
SHA-256 69521a82eb05f1287fa43a9224e11e94c6bf0245720225bc777e1f7572144e58
420 lines, 15006 bytes
~~~

The verdict is **STRICT PASS** at these exact bytes.  The target proves
nonexplosion and classwise positive recurrence for all 6,654 pairs in the
failed subset of the exact outside-mixed 18,496-pair remainder.  Its local
rules all use the same proper actual-target marked factorial.  No chart-exit
circulation, finite cap graph, orientation enumeration, or potential switch
enters the proof.

### Exact derivative transfer

Relative to the already math-audited target

~~~text
SHA-256 655242b2b5456ffaedd2c77dde461f2020507e0c70d2bd3338e451c21ece5ae0
~~~

the immutable target makes exactly three publication repairs: it inserts the
missing backslash before `\qquad` in displays (4.1) and (5.1), and it replaces
the informal endpoint-UI phrase by the precise statement that each episode
has integrable duration and integrable positive part of its endpoint
increment.  Reversing exactly those three hunks reproduces that prior SHA-256
byte for byte (419 lines, 14981 bytes).  The two display repairs have no
mathematical content, and the final wording states exactly the integrability
hypothesis used below.  The full mathematical audit therefore transfers
without weakening.

## 1. Exact set scope and symbolic bridge

The failed set and its complete corrected-cut profile are pinned by

~~~text
src/outside_mixed_remaining_18496_certificate.py
SHA-256 314f378664052cabe23910e118c9a43acf99884ccb5c63b61daf014a206e4c63

tests/test_outside_mixed_remaining_18496_certificate.py
SHA-256 28d3cf0087bcd77e24d6dbfa280b226b34d3d026c35e743bc10487c829667769
~~~

The exact 21,906 failed incidences are 15,204 B/F0, 3,618 B/B, and
3,084 two-active AA incidences.  There is no all-active failure.

The load-bearing bridge from this named remainder to the symbolic
one-active theorem is literal:

~~~text
src/remaining_18496_globally_nonmixed_certificate.py
SHA-256 54e0a5c96c2fe5e0e54c48bbb91f0f2eccbd140d62bce39ed55df54dd5a486fb

tests/test_remaining_18496_globally_nonmixed_certificate.py
SHA-256 9228597561617ef92b93f6387a43cd954f534796e7de1b51f542613bfce06060

research_notes/proof_first_remaining_18496_globally_nonmixed_bridge_exact_byte_audit.md
SHA-256 b2e54902d95f4fa52bb3857acc2b4d5e7fa247138c21a1064aa06b40db140fc2
~~~

The classifier is checked in all twenty-one active-pair/workload cells.
Every one of the 18,496 pairs is globally nonmixed, with zero violations.
Thus every one-active sequence of a failed pair is covered by the frozen
Q/flat/B/D symbolic exhaustion; the target does not infer that fact merely
from the phrase “outside mixed.”

## 2. One marked potential and exact jump identity

After every physical reaction, the actual target \(t\) is carried as the
mark, so \(x\ge t\).  The common potential is

\[
 W(x,t)=1+\sum_i\log((x_i-t_i)!).                         \tag{2.1}
\]

For a reaction with source (y), exact factorial cancellation gives

\[
 \Delta F=\log\frac{(x)_t}{(x)_y}.                         \tag{2.2}
\]

Averaging over every physical clock yields the source-entropy identity

\[
 D(x,t)=\log p_t-\sum_y p_y\log p_y-log K_t
                   +\sum_y p_y\log K_y
        \le\log p_t+C.                                    \tag{2.3}
\]

The sourcewise bound \(p_y\le C/R\) when
\(R=(x)_t/(x)_y\ge1\) gives every fixed moment of the positive increment.
This is the uniform-integrability input used in the final localization; no
separate local potential or entrance toll appears.

## 3. All-active and two-active branches

Every feasible all-active descriptor passes the corrected S-superlevel cut.
In the all-active domain, bounded displacement cannot disable any binary
source.  The certified edge has top-S source probability bounded below and
strictly D-lower target.  Consequently the target takes one ordinary jump
and, only on that labelled success, one final ordinary jump; its literal
reward

\[
 D(x,t)+a_e(x)D(x-y+z,z)\longrightarrow-\infty            \tag{3.1}
\]

has no structural-exit alternative.

Every feasible two-active descriptor is AA by the exact certificate and
audit pinned in the target.  The same-linkage target-following path ends at
\(c\), and the comparison source \(q\) satisfies \(q_b\le c_b\) in the
bounded coordinate.  Hence \(q\) remains physically enabled at
\(x-t+c\), even after a cap change, while the strict active-coordinate
D-comparison gives \(p_c(x-t+c)\to0\).  The finite Bellman recursion is
therefore unconditional.  Both branches terminate at actual marked
endpoints and have bounded physical depth.

## 4. Complete one-active exhaustion

On a one-active subsequence, the exact log-flag compactification gives

\[
 X\to\infty,\qquad
 \log(1+U)+\log(1+V)=o(\log X).                         \tag{4.1}
\]

The globally-nonmixed theorem leaves exactly four analytic outcomes.

1. If \(2X\) occurs, its quadratic source dominates.  A non-\(2X\) mark is
   immediately rare; from the \(2X\) mark, one fixed nonself labelled edge
   plus one final jump makes its target rare.  The rule is unconditional.
2. Flat/flat support preserves \(X\), and the five dormant D/F0 shapes
   preserve \(X-U-V\).  These exact invariants exclude a one-active escape
   in the fixed class.
3. A B mark follows its linkage to the lower witness \(c\); the successful
   endpoint enables \(q\), so the finite Bellman recursion is coercive.
   This closes B/B and the B-mark half of B/F0 without an exit.
4. A Flat0 mark uses the independently audited cap-free killed resolvent:

~~~text
research_notes/proof_first_remaining_18496_cap_free_bf0_killed_resolvent_theorem.md
SHA-256 5e8ce1d09c794014093bc9b84b9563f9348530acc741bb12b2c8446e2a560783

research_notes/proof_first_remaining_18496_cap_free_bf0_killed_resolvent_exact_byte_audit.md
SHA-256 7ad5cc50c4e538c0e6e2fd119fc9f01bf29eb9f86c18faf7e1c9592c28145194
~~~

The killed phase carries the actual pure target degree.  Its relative
factorial resolvent controls positive endpoint reward, its stopped-survival
estimate controls the inactive maximum without hiding behind a favorable
\(X^{-\theta}\) terminal factor, and its physical duration is
\(O((1+\log(2+V))^m)\).  Either the completed access/B episode has reward
tending to minus infinity with a physical-time toll, or the full fixed-
\(X\) one-species class is directly positive recurrent.

These alternatives are support-symbolic and analytic; no population range
or reaction history is searched.

## 5. State selection and random-time Foster summation

The target explicitly includes the ordinary one-jump rule, so at least one
positive-duration rule is applicable at every marked state.  Longer rules
are applicable only when their literal first source is enabled; every later
required source is enabled by the actual target of the preceding successful
label.  There are no zero-time classifier handoffs.

If no finite set admitted the uniform score

\[
 \mathbb E[\Delta W+\eta\tau]\le-1,                       \tag{5.1}
\]

properness would supply an escaping countersequence.  Finite subsequence
selection fixes its mark, active mask, tier type, source-ratio limits, and
menu rule.  Sections 3--4 then give coercion, an invariant contradiction,
or an already recurrent closed Flat0 class.  Thus (5.1) holds outside a
finite marked set.

Let \(N\) be the first completed episode whose physical path visits that
set.  The event that episode \(j\) is begun before \(N\) is measurable at
its start.  Conditional summation of (5.1), first under finite-\(W\)
localization, gives

\[
 \mathbb E W_{S_{n\wedge N}}+
 \eta\mathbb E S_{n\wedge N}+
 \mathbb E(n\wedge N)\le W_0+1.                        \tag{5.2}
\]

Positive-increment uniform integrability removes localization.  Every
episode contains at least one actual jump.  Therefore infinitely many
episodes completed in finite time would force infinitely many physical
jumps in finite time, which nonexplosion excludes.  Fatou and monotone
convergence consequently give finite mean hitting of the finite marked set.

The physical class is locally finite.  From the finitely many physical
states under that marked set, irreducibility gives a finite labelled path
to one reference state.  The finite path menu has a positive minimum
success probability and finite mean duration.  Geometric repetition using
the already proved finite-mean returns gives a finite mean positive return
to the reference state, hence positive recurrence of the closed class.

## 6. Nonexplosion and exact verdict

Population-increasing binary reactions have source degree at most one and
total rate \(O(1+|x|_1)\).  Quadratic-source reactions cannot increase total
population; within a fixed population sublevel they have bounded total
rate.  Standard comparison therefore proves nonexplosion independently of
the Foster summation.

All local branches use the same proper \(W\), include every causing jump
exactly once, and terminate at actual marked endpoints.  The complete
6,654-pair theorem at SHA \(69521a82\ldots\) is therefore a strict proof of
nonexplosion and positive recurrence on every closed irreducible population
class in its exact support scope.
