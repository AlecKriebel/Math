# Independent exact-byte audit: unconditional two-active AA contraction

**Audit date:** 2026-08-12 PDT.

## 1. Frozen target and strict verdict

The audited target is

~~~text
research_notes/proof_first_remaining_18496_two_active_unconditional_aa_and_cap_scc_obstruction.md
fd55879fe932e9389b6b468a00c046b59ec3c214ad08afdd0eb696b3f42844e3
362 lines / 14075 bytes
~~~

The verdict on these exact bytes is **STRICT PASS AS A LOCAL TWO-ACTIVE
CONTRACT**.

The target proves two logically distinct statements.

1. A finite cap/descriptor SCC is not a Markov reward quotient and cannot
   prove Foster contraction from graph reachability alone.
2. Every affine-feasible two-active sequence in the exact 18,496-pair
   remainder instead admits an unconditional bounded-depth all-clock
   marked-factorial episode.  The episode does not stop on cap, tier,
   enabled-support, or active-set bookkeeping changes.

The second statement closes the entire two-active analytic seam locally,
including the 3,084 corrected-cut failures.  It is deliberately not a
global pair-recurrence theorem: complementary all-active and one-active
sequences still require compatible common-potential rules.

## 2. Exact finite identity

The target pins the finite inputs

~~~text
src/remaining_18496_all_feasible_two_active_aa_certificate.py
25e5c2fce812d2e3d3f02c0c9377533cf16c68313b77bc0d1e7a485052bd68ee

tests/test_remaining_18496_all_feasible_two_active_aa_certificate.py
2445edcbcf66ff2204c821baec455b4f8a416180360a39a6d757712af5fc22e0
~~~

The independent exact-byte audit of those inputs is

~~~text
research_notes/proof_first_remaining_18496_all_feasible_two_active_aa_exact_byte_audit.md
27bfc707721fab03d829d14ca764505694556dbf0d2fd325ea25aa8573b2beef
~~~

The dedicated tests replayed independently in 92.312 seconds.  They find
1,140,984 flag-feasible two-active incidences: 1,137,900 corrected-cut
passes and 3,084 failures.  Every linkage in every row is Q, U, or C;
the number of rows with any unavailable linkage is zero.  The incidence and
summary fingerprints are

~~~text
a4c4aa42dadabe7e73d46a690f29fe1d457bf57c5bece422b8c0a3fafe72eb99
bc9195d09dc8717381486ae114fcd59e22786c729d957fe209ceac432deaaac8
~~~

This is support/descriptor/affine geometry only.  The target correctly
supplies the stochastic argument separately.

## 3. Hostile replay of the no-exit path

Fix one escaping marked sequence with active coordinates \(i,j\), bounded
coordinate \(b\), and actual mark \(t\).  The frozen Q/U/C bridge supplies a
lower terminal \(c\) and a faster source \(q\) in the same linkage with

\[
                        q_b\le c_b,\qquad q\succ_D c.       \tag{3.1}
\]

Strong connectivity gives a simple target-following word

\[
                  t=y_0\longrightarrow y_1\longrightarrow\cdots
                    \longrightarrow y_m=c.                \tag{3.2}
\]

After a successful prefix, the population is exactly

\[
                         x_r=x-t+y_r\ge y_r.                \tag{3.3}
\]

Thus every designated source is enabled by the preceding actual target;
there is no activation hypothesis.  At the terminal success population

\[
                         z=x-t+c\ge c,                      \tag{3.4}
\]

both active coordinates still diverge and
\(z_b\ge c_b\ge q_b\).  Hence \(q\) is enabled even when the bounded cap has
changed along the word.  The displacement from \(x\) to \(z\) is fixed, so
the strict active-coordinate D-comparison is preserved.  Consequently

\[
             p_c(z)\le {K_c(z)_c\over K_q(z)_q}\longrightarrow0.   \tag{3.5}
\]

This proves the load-bearing repair.  The earlier structural-exit test was
proof bookkeeping, not a physical necessity for Q/U/C paths.  Removing it
does not condition away any competing clock and does not require a cap
transition graph.

The statement that the endpoint remains two-active is correctly scoped to
the fixed escaping sequence: a bounded number of bounded jumps cannot
destroy either diverging coordinate, and it cannot turn the uniformly
bounded coordinate into a diverging one.  The target does not claim
pointwise invariance of a cap node.

## 4. Exact Bellman and moment audit

With the actual reaction target carried as the mark, put

\[
 F(x,t)=\sum_r\log((x_r-t_r)!),\qquad W=1+F.          \tag{4.1}
\]

For one ordinary all-clock jump, the exact marked cancellation gives

\[
 D(x,t)=\log p_t-\sum_y p_y\log p_y-\log K_t
                   +\sum_y p_y\log K_y
       \le\log p_t+C_K.                              \tag{4.2}
\]

If \(a_r\) is the probability of the designated label at stage \(r\), the
stopped expected reward satisfies the literal recursion

\[
                     J_m=D_m,\qquad J_r=D_r+a_rJ_{r+1}.     \tag{4.3}
\]

Every deviation clock is already averaged in \(D_r\) and its actual
endpoint terminates the current episode.  The causing jump is not counted
again when its actual target selects the next episode.

On a compact source-ratio subsequence, all designated probabilities before
the first rare source are bounded below.  At that first rare source,
\(D_r\to-\infty\), while \(a_r=O(p_{y_r})\) suppresses the bounded positive
tail.  If no prefix source is rare, (3.5) supplies the rare terminal.  The
finite recursion therefore gives \(J_0\to-\infty\) with no exit alternative.

The episode contains at most ten ordinary jumps.  The marked source is
enabled at every stage, so total hazard is bounded below by a fixed positive
label rate.  Source entropy supplies all fixed moments of the positive
marked-factorial increment, and the finite sum of holding times has all
fixed moments.  Actual endpoints are integrable and have bounded population
displacement.  These facts justify adding a fixed positive physical-time
coefficient to the stopped drift.

## 5. Finite-menu coercivity and tiling

For a fixed pair, orientation, and rate vector there are finitely many
active masks, tier types, actual targets, admissible terminals, and simple
paths.  At each marked state the target selects the menu rule with least
exact expected stopped reward.

If uniform coercivity failed along a two-active escaping sequence, finite
compactness would give a subsequence with fixed descriptor data, terminal,
path, and limiting source ratios.  The valid path for that subsequence has
reward tending to minus infinity by Section 4, and the selected minimum is
no larger.  This contradiction proves the state-selected estimate

\[
 \mathbb E_{x,t}
 [W(X_\tau,T_\tau)-W(x,t)+\eta\tau]\le-1            \tag{5.1}
\]

outside a finite part of every two-active escaping family.

Every episode contains at least one physical jump, terminates at an actual
marked endpoint, and uses the same proper \(W\).  Episodes therefore tile
the marked physical chain without a recharge toll, overlap, activation
wait, or terminal-chart-exit seam.  The selection is legitimate on the
countable marked state space; no computability of the exact score is needed
for the existence theorem.

## 6. Strict failure of the finite cap-SCC proposal

The target's witness lies inside the exact 18,496 remainder:

\[
 L_b=\{0,A,2A,A+B\},\qquad L_0=\{C,2C,A+C\},          \tag{6.1}
\]

with \(B\) active, \(A\)-cap zero, and \(C\)-caps zero, one, and two.  An
independent replay confirms all three B/F0 descriptor rows.  In a strong
orientation containing \(2C\to C\), the same cap-two node has different
endpoints:

\[
 C=2\Longrightarrow\hbox{cap one},\qquad
 C\ge3\Longrightarrow\hbox{cap two}.                 \tag{6.2}
\]

The reaction probabilities also vary within the node because the \(2C\)
and \(C\) hazards scale respectively as \(C(C-1)\) and \(C\).  Thus the cap
node plus reaction label determines neither the next node nor its transition
probability.  Refining cap two to exact population yields a countable, not
finite, phase.

Even for a genuine finite Markov-additive quotient, the directed support is
insufficient.  For example, a deterministic two-node cycle with rewards
\(M\) and \(-1\) contains a negative-reward node but has stationary mean
\((M-1)/2>0\) when \(M>1\).  A bounded Foster corrector exists only after
checking the rate-weighted mean reward of every closed recurrent class (or
equivalently solving the appropriate Poisson inequalities).  Therefore the
claim “every closed SCC contains a coercive node” is not a valid contraction
criterion.

## 7. Publication boundary

The exact publishable conclusion is:

> Every flag-feasible two-active escaping sequence of every pair in the
> 18,496 remainder has an unconditional common-marked-\(W\), bounded-depth,
> all-clock Foster episode.  This includes all 3,084 two-active corrected-cut
> failures and requires no cap-SCC or structural-exit circulation.

The theorem does not close the remaining one-active B/F0 countable phase,
does not supply a common interface with a different population potential,
and does not by itself imply recurrence of all 18,496 pairs.  Those limits
are stated literally in the frozen target.  Any final composition must
either cover all complementary sequences with compatible marked-\(W\) rules
or prove a separate population-level handoff.  No terminal chart-exit
shortcut is licensed by this audit.
