# Independent hostile exact-byte audit: recurrence of the 6,654 failure pairs

**Audit date:** 2026-08-12 PDT.

## 1. Exact target and verdict

~~~text
research_notes/proof_first_remaining_18496_failure_6654_common_marked_recurrence_theorem.md
69521a82eb05f1287fa43a9224e11e94c6bf0245720225bc777e1f7572144e58
420 lines / 15006 bytes
~~~

The verdict on these exact bytes is **STRICT PASS**.

For each of the exact 6,654 support pairs, every strongly connected
orientation, every positive labelled rate vector, and every closed
irreducible population class, the target proves nonexplosion and positive
recurrence.  All noninvariant branches use the same proper actual-target
marked factorial.  No terminal-chart exit, descriptor SCC, finite cap
quotient, or potential switch is used.

## 2. Exact finite scope

The pair universe and failure split are pinned at

~~~text
src/outside_mixed_remaining_18496_certificate.py
314f378664052cabe23910e118c9a43acf99884ccb5c63b61daf014a206e4c63

tests/test_outside_mixed_remaining_18496_certificate.py
28d3cf0087bcd77e24d6dbfa280b226b34d3d026c35e743bc10487c829667769

research_notes/proof_first_outside_mixed_remaining_18496_certificate_exact_byte_audit.md
2539d8eee4d1d584ed5566f7494c7262843676dc368078647db12481d6a5822f
~~~

The exact support identity is

\[
18{,}496=11{,}842\ \dot\cup\ 6{,}654.                       \tag{2.1}
\]

The 21,906 failed incidences split as

\[
15{,}204\ {\rm B/F0}\ \dot\cup\
3{,}618\ {\rm B/B}\ \dot\cup\
3{,}084\ {\rm AA}.                                         \tag{2.2}
\]

There is no failed all-active descriptor.  The exact globally-nonmixed
bridge is

~~~text
src/remaining_18496_globally_nonmixed_certificate.py
54e0a5c96c2fe5e0e54c48bbb91f0f2eccbd140d62bce39ed55df54dd5a486fb

tests/test_remaining_18496_globally_nonmixed_certificate.py
9228597561617ef92b93f6387a43cd954f534796e7de1b51f542613bfce06060

research_notes/proof_first_remaining_18496_globally_nonmixed_bridge_exact_byte_audit.md
b2e54902d95f4fa52bb3857acc2b4d5e7fa247138c21a1064aa06b40db140fc2
~~~

It checks the literal twenty-one-cell classifier signature and finds all
18,496 pairs globally nonmixed, with zero violations.  The two-active
certificate and audit,

~~~text
src/remaining_18496_all_feasible_two_active_aa_certificate.py
25e5c2fce812d2e3d3f02c0c9377533cf16c68313b77bc0d1e7a485052bd68ee

tests/test_remaining_18496_all_feasible_two_active_aa_certificate.py
2445edcbcf66ff2204c821baec455b4f8a416180360a39a6d757712af5fc22e0

research_notes/proof_first_remaining_18496_all_feasible_two_active_aa_exact_byte_audit.md
27bfc707721fab03d829d14ca764505694556dbf0d2fd325ea25aa8573b2beef
~~~

give 1,140,984 affine-feasible two-active incidences, all AA.  These are
support/tier/affine identities only; the target supplies the stochastic
arguments separately.

## 3. Common marked identity

After each physical reaction, carry its actual target \(t\) as the mark.
Then \(x\ge t\), and

\[
 F(x,t)=\sum_{i=1}^{3}\log((x_i-t_i)!),
 \qquad W(x,t)=1+F(x,t)                                  \tag{3.1}
\]

is nonnegative and proper on the reachable marked state space.  If the next
reaction is \(y\to u\), exact factorial cancellation gives

\[
 F(x-y+u,u)-F(x,t)=\log\frac{(x)_t}{(x)_y}.              \tag{3.2}
\]

With \(p_y=K_y(x)_y/\Lambda(x)\), the ordinary all-clock expectation is

\[
 D(x,t)=\log p_t-\sum_y p_y\log p_y-\log K_t
                   +\sum_y p_y\log K_y
       \le \log p_t+C_K.                                \tag{3.3}
\]

Thus every competitor is charged.  On a positive sourcewise increment,
\(R=(x)_t/(x)_y\ge1\) implies \(p_y\le C/R\); hence
\(R^{-1}(\log R)^m\) is bounded for every fixed \(m\).  This supplies the
positive-increment uniform integrability used in the final localization.

## 4. All-active and two-active contraction

Every affine-feasible all-active descriptor passes the corrected cut.  Its
certified edge \(e:y\to z\) has top-S source and strictly D-lower target.
On a fixed source-ratio subsequence its labelled probability \(a_e\) is
bounded below.  Take one ordinary jump and, only if \(e\) fires, one final
ordinary jump.  A competitor stops at its actual endpoint.

All coordinates diverge, so bounded displacement preserves every binary
source and every strict tier comparison.  At \(x-y+z\), a top-tier
comparison source remains enabled and

\[
 p_z(x-y+z)\longrightarrow0.
\]

Consequently

\[
 D(x,t)+a_eD(x-y+z,z)\longrightarrow-\infty.             \tag{4.1}
\]

There is no inactive cap and no structural-exit alternative.

For two-active sequences the target invokes

~~~text
research_notes/proof_first_remaining_18496_two_active_unconditional_aa_and_cap_scc_obstruction.md
fd55879fe932e9389b6b468a00c046b59ec3c214ad08afdd0eb696b3f42844e3

research_notes/proof_first_remaining_18496_two_active_unconditional_aa_exact_byte_audit.md
2de8466793c774eaccfde4d0160c39dbafe49f581b68154a6a39419e5fd74a8a
~~~

From the actual target \(t\), a same-linkage path reaches \(c\), and a
faster source \(q\) satisfies \(q_b\le c_b\) in the bounded coordinate.
Thus \(q\) is literally enabled at \(x-t+c\), even after a cap change, and
the strict active-coordinate comparison gives \(p_c(x-t+c)\to0\).  The
finite Bellman recursion is unconditional and uses the same \(W\).

## 5. One-active exhaustion

After logarithmic compactification, a one-active sequence has

\[
X\to\infty,\qquad
\log(1+U)+\log(1+V)=o(\log X).                            \tag{5.1}
\]

The exact bridge makes the symbolic theorem

~~~text
research_notes/proof_first_one_active_no_mixed_exhaustion_repaired.md
9fb1828f5660ffae83e6e1a08a0cb33ce8bd2813d7394a90187d9bccc64895c4

research_notes/proof_first_one_active_no_mixed_exhaustion_repaired_exact_byte_audit.md
6f7619e7696d1dfe3ab332746eea0be54899416dff3b3488f5ef53f43672e682
~~~

literally exhaustive.

1. In Q, the unique \(2X\) source dominates every other source.  A
   non-\(2X\) actual mark is immediately rare; from the \(2X\) mark, a
   fixed nonself edge and one final jump make its target rare.
2. Flat/flat preserves \(X\).  The five D/F0 shapes preserve
   \(X-U-V\).  Either invariant excludes a one-active escape in one fixed
   class.
3. In B/B, the actual-target same-linkage path reaches a lower source \(c\);
   its endpoint enables the degree-one comparison source and makes \(c\)
   rare.
4. In B/F0, a B mark uses the preceding B rule.  A Flat0 mark uses the
   cap-free killed resolvent.

The last theorem and its hostile audit are

~~~text
research_notes/proof_first_remaining_18496_cap_free_bf0_killed_resolvent_theorem.md
5e8ce1d09c794014093bc9b84b9563f9348530acc741bb12b2c8446e2a560783

research_notes/proof_first_remaining_18496_cap_free_bf0_killed_resolvent_exact_byte_audit.md
7ad5cc50c4e538c0e6e2fd119fc9f01bf29eb9f86c18faf7e1c9592c28145194
~~~

Its countable pure inactive phase carries the actual target degree.  The
killed Green bound controls terminal factorial overshoot, the stopped
first-hit estimate controls the pre-absorption maximum, and the physical
duration has logarithmic moments.  It includes the absorption-causing jump
once and appends the actual-target B/access payoff.  A closed no-kill phase
instead makes the whole fixed-\(X\) one-species class positive recurrent.
No one-active corrected-pass exit is followed.

## 6. Finite menu and sequential coercivity

The support-level menu is finite: marks, simple paths, labelled edges,
active-coordinate choices, witnesses, and tie orders range over finite
sets.  The countable Flat0 prefix is one fixed stopping algorithm, not a
population enumeration.

The ordinary one-jump fallback is defined at every marked state.  A longer
template is applicable when its literal first source is enabled.  Every
later prescribed source is the actual target of the preceding successful
label and is therefore enabled.  Thus at least one positive-duration rule
is defined at every state, with no zero-time reclassification.

Fix one common \(\eta>0\) below the finitely many local margins and select
the applicable rule of least exact score.  If no finite set made

\[
\mathbb E_{x,t}[\Delta W+\eta\tau]\le-1                     \tag{6.1}
\]

hold outside it, properness would give an escaping violating sequence.
Finite subsequence selection fixes its mark, active mask, tier cell,
source-ratio limits, and support rule.  Sections 4--5 then give coercion, an
invariant contradiction, or an already recurrent closed Flat0 class.  This
proves (6.1) off a finite marked set \(K\).  It is a state-selected
finite-menu argument, not a claim about descriptor graph circulation.

## 7. Random-time Foster and physical recurrence

Every episode has at least one physical jump, ends at the actual endpoint
and target, and has integrable duration and integrable positive part of its
endpoint increment.  Complete
an episode once even if its path visits \(K\).  Let \(N\) be the first
completed episode whose path visited \(K\).  For every episode before \(N\),
the start is outside \(K\), so conditional summation of (6.1), localized
first to finite \(W\)-sublevels, gives

\[
\mathbb E W_{S_{n\wedge N}}+
\eta\mathbb E S_{n\wedge N}+
\mathbb E(n\wedge N)\le W_0+1.                            \tag{7.1}
\]

Uniform integrability removes localization.  Fatou and monotone convergence
give finite expected episode count and accounting time.  Hence the physical
hitting time of the finite projection of \(K\) has finite mean.

From that finite physical set, irreducibility supplies finite labelled
paths to a fixed reference state.  Their minimum success probability is
positive and their durations have finite mean.  Geometric repetition using
the finite-mean returns gives a finite mean positive return to the reference
state.  Forgetting the mark does not change the physical generator.

Finally, only source degree zero or one can increase total population, so
the aggregate increasing rate is \(O(1+|x|_1)\).  Quadratic reactions
preserve or decrease total population.  Linear-birth comparison therefore
proves nonexplosion independently of the Foster summation.

## 8. Publication conclusion

The exact theorem at SHA \(69521a82\ldots\) is a complete common-potential
proof of nonexplosion and classwise positive recurrence for all 6,654
failure pairs.  It enumerates no orientations, rates, populations, or
histories, and invokes no chart-exit shortcut.
