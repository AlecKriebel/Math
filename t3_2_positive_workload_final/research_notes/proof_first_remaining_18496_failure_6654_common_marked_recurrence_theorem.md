# Recurrence of the 6,654 failure pairs under one common marked factorial

**Proof-first composition candidate, 2026-08-12 PDT.**  This note proves a
standalone pair theorem for the 6,654 support pairs in the exact outside-mixed
18,496-pair remainder which have at least one affine-feasible corrected-cut
failure.  A single proper marked factorial is used on every noninvariant
scale.  No descriptor exit is discarded, no terminal-chart circulation is
invoked, and no finite cap graph is used.

Finite computation below certifies only support, tier, affine-feasibility,
and set identities.  Orientations, rate vectors, population states, and
reaction histories are not enumerated.

## 1. Scope and exact finite inputs

Fix an ordered pair of disjoint nontrivial binary linkage supports from the
6,654-pair failed set in

~~~text
src/outside_mixed_remaining_18496_certificate.py
SHA-256 314f378664052cabe23910e118c9a43acf99884ccb5c63b61daf014a206e4c63

tests/test_outside_mixed_remaining_18496_certificate.py
SHA-256 28d3cf0087bcd77e24d6dbfa280b226b34d3d026c35e743bc10487c829667769
~~~

The independent support-only audit has SHA-256

~~~text
2539d8eee4d1d584ed5566f7494c7262843676dc368078647db12481d6a5822f.
~~~

The exact failure data are

\[
\begin{array}{c|r}
\text{pair set}&\text{pairs}\ \\ \hline
\text{outside-mixed remainder}&18{,}496\\
\text{no affine-feasible cut failure}&11{,}842\\
\text{at least one feasible failure}&6{,}654
\end{array}                                                     \tag{1.1}
\]

and the 21,906 failed incidences split as

\[
        15{,}204\ \mathrm{B/F0}
        \;\dot\cup\;3{,}618\ \mathrm{B/B}
        \;\dot\cup\;3{,}084\ \mathrm{AA}.          \tag{1.2}
\]

There are no failed all-active descriptors.  The AA rows are exactly the
two-active rows; B/F0 and B/B are exactly the one-active rows.

The literal global-nonmixing definition used by the one-active symbolic
theorem has been replayed independently on all 18,496 pairs.  The focused
support-only certificate is

~~~text
src/remaining_18496_globally_nonmixed_certificate.py
SHA-256 54e0a5c96c2fe5e0e54c48bbb91f0f2eccbd140d62bce39ed55df54dd5a486fb

tests/test_remaining_18496_globally_nonmixed_certificate.py
SHA-256 9228597561617ef92b93f6387a43cd954f534796e7de1b51f542613bfce06060
~~~

It checks all three active-coordinate pairs and all seven ordered primitive
workload representatives.  The exact result is 18,496 globally nonmixed
pairs and zero violations.  Its pair manifest is

~~~text
eb7db151e42eb9562b1a1d519ea7dad212df52c6df368ffa08edbf79410db4ad
~~~

and its support-signature fingerprint is

~~~text
216a07ec3265cd9c072ff6975235198b839ab44b9dfd832c51ff70dd304459c1.
~~~

Its independent exact-byte audit has SHA-256

~~~text
b2e54902d95f4fa52bb3857acc2b4d5e7fa247138c21a1064aa06b40db140fc2.
~~~

The exact all-feasible-two-active AA identity is frozen at source/test
SHA-256 values

~~~text
25e5c2fce812d2e3d3f02c0c9377533cf16c68313b77bc0d1e7a485052bd68ee
2445edcbcf66ff2204c821baec455b4f8a416180360a39a6d757712af5fc22e0,
~~~

with exact-byte audit SHA-256

~~~text
27bfc707721fab03d829d14ca764505694556dbf0d2fd325ea25aa8573b2beef.
~~~

It gives 1,140,984 affine-feasible two-active incidences, all AA, including
all 3,084 failures.

## 2. The common marked chain

Fix arbitrary strongly connected orientations, arbitrary positive labelled
rates, and one closed irreducible population class \(\Gamma\).  After every
physical reaction carry its actual target \(t\) as a mark.  Then \(x\ge t\).
Put

\[
 F(x,t)=\sum_{i=1}^3\log((x_i-t_i)!),
 \qquad W(x,t)=1+F(x,t).                              \tag{2.1}
\]

Marks range over the finite binary complex set, so \(W\ge1\) is proper on
the reachable marked state space.  For a source \(y\), write

\[
 K_y=\sum_{e:s(e)=y}\kappa_e,\qquad
 p_y(x)=\frac{K_y(x)_y}{\sum_zK_z(x)_z}.             \tag{2.2}
\]

If the next reaction is \(y\to u\), factorial cancellation gives

\[
 F(x-y+u,u)-F(x,t)=\log\frac{(x)_t}{(x)_y}.          \tag{2.3}
\]

Thus one ordinary all-clock jump has expected reward

\[
 D(x,t)=\log p_t-\sum_yp_y\log p_y-\log K_t+\sum_yp_y\log K_y
       \le\log p_t+C_K.                              \tag{2.4}
\]

For every fixed \(m<\infty\), its positive reward has a uniform \(m\)-th
moment.  Indeed, on a positive sourcewise term with
\(R=(x)_t/(x)_y\ge1\), one has \(p_y\le C/R\), and
\(R^{-1}(\log R)^m\) is bounded.

## 3. All-active sequences: unconditional corrected-cut reward

Take any all-active escaping marked sequence in \(\Gamma\).  Its descriptor
is affine feasible.  By (1.2), it passes the corrected S-superlevel cut.
Let \(E\) be the global top S-tier, and choose the certified edge

\[
                         e:y\longrightarrow z        \tag{3.1}
\]

whose source \(y\in E\) and whose target is in a strictly lower D-tier.
After a source-ratio subsequence,

\[
                     p_y(x_n)\ge b>0.                \tag{3.2}
\]

Take the next ordinary all-clock jump.  Continue only if the labelled edge
\(e\) fires; on that event, take one final ordinary jump from the actual
marked endpoint \((x_n-y+z,z)\).  Stop on a competitor at its actual
endpoint.  There is no structural-exit test.

Every coordinate diverges on the sequence.  A bounded displacement cannot
disable any source, and it preserves every strict tier comparison.  Hence,
for any \(q\in E\),

\[
 p_z(x_n-y+z)
 \le \frac{K_z(x_n-y+z)_z}{K_q(x_n-y+z)_q}
 \longrightarrow0.                                  \tag{3.3}
\]

If \(a_e\) is the physical probability of the labelled edge, first-step
conditioning and (2.4) give

\[
 J_n=D(x_n,t)+a_e(x_n)D(x_n-y+z,z)\longrightarrow-\infty. \tag{3.4}
\]

This is the depth-two corrected-tier theorem with its former boundary-exit
alternative removed for the all-active domain, where no such source loss is
possible.

## 4. Two-active sequences: unconditional AA reward

Every affine-feasible two-active descriptor is Q/U/C available on both
linkages by the exact certificate in Section 1.  The cap-free actual-target
AA theorem is frozen at

~~~text
research_notes/proof_first_remaining_18496_two_active_unconditional_aa_and_cap_scc_obstruction.md
SHA-256 fd55879fe932e9389b6b468a00c046b59ec3c214ad08afdd0eb696b3f42844e3
~~~

with independent exact-byte audit SHA-256

~~~text
2de8466793c774eaccfde4d0160c39dbafe49f581b68154a6a39419e5fd74a8a.
~~~

For completeness, its decisive endpoint identity is short.  If \(t\) is
the actual mark, the symbolic Q/U/C bridge supplies a same-linkage simple
path from \(t\) to \(c\) and a comparison source \(q\) such that

\[
                         q_b\le c_b,\qquad q\succ_Dc, \tag{4.1}
\]

where \(b\) is the bounded coordinate.  At successful endpoint
\(x-t+c\), both active coordinates still diverge and \(q_b\le c_b\) makes
\(q\) literally enabled.  Thus \(p_c(x-t+c)\to0\).  The exact finite
Bellman recursion along the simple path makes the total common-\(W\) reward
tend to minus infinity.  All clocks compete, and cap changes are retained
inside the same episode rather than treated as exits.

## 5. One-active sequences: the globally-nonmixed exhaustion

Let \(X\) be the unique active coordinate, so, after the exact logarithmic
compactification,

\[
 X_n\longrightarrow\infty,\qquad
 \log(1+U_n)+\log(1+V_n)=o(\log X_n).                \tag{5.1}
\]

Because the pair is globally nonmixed, the audited symbolic exhaustion in

~~~text
research_notes/proof_first_one_active_no_mixed_exhaustion_repaired.md
SHA-256 9fb1828f5660ffae83e6e1a08a0cb33ce8bd2813d7394a90187d9bccc64895c4
~~~

applies.  Its exact-byte audit SHA-256 is

~~~text
6f7619e7696d1dfe3ab332746eea0be54899416dff3b3488f5ef53f43672e682.
~~~

It gives the following exhaustive support alternatives.

### 5.1 Quadratic branch

If a linkage contains \(q=2X\), it is the unique source with active degree
two.  Every other binary source has propensity \(X^{1+o(1)}\), while
\(\lambda_q=\Theta(X^2)\).  Hence \(p_q\to1\) and \(p_t\to0\) for every
mark \(t\ne q\); one ordinary jump is coercive by (2.4).

For \(t=q\), choose a fixed nonself edge \(e:q\to u\) supplied by strong
connectivity.  Take one ordinary jump and, only if \(e\) fires, one final
jump.  The edge probability stays bounded below, \(q\) remains enabled at
the bounded-displacement endpoint, and \(p_u(x-q+u)\to0\).  The exact
identity

\[
                    J=D(x,q)+a_e(x)D(x-q+u,u)        \tag{5.2}
\]

therefore tends to minus infinity.  No cap or active-set exit is tested.

### 5.2 Flat and dormant invariant branches

If both linkages have constant \(X\)-degree on their supports, every
reaction preserves \(X\), so an escaping one-active sequence cannot lie in
one fixed class.

The only dormant residue consists, up to exchanging \(U,V\), of

\[
 L_D=\{0,X+U,X+V\}                                  \tag{5.3}
\]

paired with one of

\[
 \{U,V\},\ \{2U,2V\},\ \{2U,U+V\},\
 \{2V,U+V\},\ \{2U,2V,U+V\}.                       \tag{5.4}
\]

Every reaction preserves \(H=X-U-V\).  Equation (5.1) and constancy of
\(H\) exclude \(X\to\infty\) in the fixed class.

### 5.3 B/B and B/F0 branches

For a Bellman linkage choose \(q,c\) with

\[
 q_X=1,\qquad c_X=0,\qquad q_U\le c_U,\quad q_V\le c_V. \tag{5.5}
\]

From an actual mark in that linkage, follow a same-linkage simple path to
\(c\), retaining every competing clock, and then take one final ordinary
jump.  The successful endpoint \(x-t+c\) enables \(q\), and

\[
 p_c(x-t+c)\le \frac{C(1+U+V)^2}{X}\longrightarrow0. \tag{5.6}
\]

The finite Bellman recursion gives coercive common-\(W\) reward.  This is
unconditional for B/B and for a B/F0 state whose actual mark lies in the B
linkage.

If the actual mark lies in the Flat0 linkage, use the cap-free killed
resolvent theorem

~~~text
research_notes/proof_first_remaining_18496_cap_free_bf0_killed_resolvent_theorem.md
SHA-256 5e8ce1d09c794014093bc9b84b9563f9348530acc741bb12b2c8446e2a560783
~~~

with independent exact-byte audit SHA-256

~~~text
7ad5cc50c4e538c0e6e2fd119fc9f01bf29eb9f86c18faf7e1c9592c28145194.
~~~

If the B witness is \(X\), it is immediate.  Otherwise write it as \(X+U\).
Before access \(U=0\), and every nonabsorbed source and target is in
\(\{0,V,2V\}\), with the actual target degree retained as part of the
countable state.  The killed marked weight

\[
                  w_\theta(v,s)=((v-s)!)^\theta       \tag{5.7}
\]

has strict multiplicative outer drift.  Removing closed no-kill components
makes the finite core a nonsingular M-matrix.  The resulting killed Green
bound controls the exact relative marked-factorial overshoot and the
pre-absorption maximum; physical duration has moments
\(O((1+\log(2+v))^m)\).  A closed no-kill component is a fixed-\(X\)
one-species binary class and is positive recurrent directly.  Otherwise the
first access or B-linkage firing is included and its actual-target Bellman
payoff appended.  The completed estimate is

\[
 \mathbb E[\Delta W+\eta\tau]\longrightarrow-\infty \tag{5.8}
\]

along every one-active B/F0 sequence, with uniform positive-reward moments
and integrable actual endpoints.

## 6. State selection and random-time Foster recurrence

The preceding rules form a finite support-dependent menu: marks, simple
paths, certified edges, active-coordinate choices, witnesses, and tie
orders all range over finite sets.  The Flat0 rule is one countable-state
stopping algorithm, not an enumeration of its populations.

Include in the menu the ordinary one-jump rule, which is defined at every
marked state.  A longer template is declared applicable exactly when its
literal first required source is enabled.  Every later continuation begins
only after the preceding labelled reaction has made its actual target the
new mark, so the next prescribed source is then literally enabled.  Thus the
menu defines at least one positive-duration stopping rule at every state;
no zero-time reclassification or asymptotic descriptor is used to define
the finite-state dynamics.

Choose one common \(\eta>0\), smaller than all finitely many local values.
At a marked state select an applicable rule minimizing its exact score

\[
       \mathbb E_{x,t}[W(X_\tau,T_\tau)-W(x,t)+\eta\tau], \tag{6.1}
\]

with deterministic tie breaking.  If no finite set \(K\) made the selected
score at most \(-1\) outside \(K\), a violating sequence would escape by
properness of \(W\).  Pass to a subsequence with fixed mark, active mask,
tier type, source ratios, and support rule.  It has one, two, or three active
coordinates.  Sections 3--5 give a score tending to minus infinity, unless
the one-active sequence is excluded by a fixed-class invariant or the class
is already positive recurrent by the closed Flat0 alternative.  This is a
contradiction.  Hence

\[
 \mathbb E_{x,t}[W(X_\tau,T_\tau)-W(x,t)+\eta\tau]\le-1
                 \qquad((x,t)\notin K).             \tag{6.2}
\]

Every episode contains at least one actual physical jump, every endpoint is
the actual endpoint and target of its last included reaction, and every
episode has integrable duration and integrable positive part of its endpoint
increment.  Complete
an episode even if its interior visits \(K\), solely for accounting.  At
successive episode endpoints \(S_j\), conditional summation of (6.2),
localized first to a finite \(W\)-sublevel, gives

\[
 \mathbb E W(X_{S_{n\wedge N}} ,T_{S_{n\wedge N}})
 +\eta\mathbb E S_{n\wedge N}+\mathbb E(n\wedge N)
 \le W(x,t)+1.                                      \tag{6.3}
\]

Here \(N\) is the first completed episode whose path visits \(K\).  Fatou
and monotone convergence give finite expected accounting time and episode
count.  On nonhitting, the episode endpoints contain an infinite subsequence
of genuine physical jump times; nonexplosion forces their times to diverge,
contradicting (6.3).  Thus the finite marked set \(K\) has finite mean
hitting time.

From the finitely many physical states below \(K\), irreducibility supplies
finite labelled paths to one fixed state.  Each has positive success
probability and finite mean duration; geometric repetition, using the
finite-mean return to \(K\), gives a finite mean return to that state.  The
closed physical class is positive recurrent.  Forgetting the target mark
does not change the physical generator.

Binaryity separately gives nonexplosion: population-increasing channels
have source degree at most one and aggregate rate \(O(1+|x|_1)\), while
population-preserving quadratic clocks cannot accumulate inside a finite
population sublevel.

> **Theorem 6.1 (the exact 6,654 failure-pair theorem).**  Every ordered
> support pair in the exact 6,654 failed subset of the outside-mixed
> 18,496-pair remainder, under every strongly connected orientation and
> every positive labelled rate vector, is nonexplosive and positive
> recurrent on each closed irreducible population class.

No orientation, rate vector, population box, or reaction history is
enumerated.  The finite certificates establish only the exact support and
tier scopes used by the analytic alternatives above.
