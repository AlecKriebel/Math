# Independent hostile audit of the current one-active fourth-power composition

**Verdict (2026-08-12 PDT): STRICT PASS.**  At the exact current bytes
listed below, Theorem 5.1 of the target proves positive recurrence on every
closed irreducible population class of each of the 1,227 selected support
pairs, for every strongly connected orientation and every fixed positive
rate vector.  Removing the already certified fifteen-pair overlap therefore
gives a valid disjoint contribution of 1,212 pairs.

This verdict does not use the older SHA attestation printed in the target or
certificate.  It is a fresh proof replay of the current theorem and its
current analytic interfaces.  No orientation, reaction-history, or
population search is used.  Finite computation is used only for the exact
support/descriptor and pair-set identities.

## 1. Frozen targets and inputs

The audited target bytes are

```text
theorem  0ab1cff97dee0594db9981db451a9f26799a6f2cdd5cf5d00a19f03e12c6ea9c
source   88537bc32673591b8d8c5f84609c097771cb77f587e0be7e97829c4638911c0c
tests    d31a410a7fc4b47db69430fe148e10f3db5b738dd64940a1ae10bc3c68f8385c
payload  85847255a93aafd1a6fb4fde862f7e35cc3aadffa04cce01794541e0841ef8d6
```

The proof inputs used in this replay are

```text
universal fourth-power interface
  9d4239f4fc6b45a9522b94b09523c9f98ac7a3b089c919bd9594f12409c78cc2
arbitrary-orientation graph theorem
  c86bea36ccbdf6319e259fd397023ba69a0fb31346c6ffe8d51261ef9bd7d625
all-species reflected target
  c87aa83b798e2a69bcc94f8de885b5b6bb403dd0898caaf9b6dfd43c26519e8a
countable-phase service theorem
  2b777de747b6fba53002daca4da0b6c584c3dd7f91adf4a85f7b423518fd74b5
moving-cutoff fourth-power lemma
  e60b8d7075d353303c08f60a503d728fffaf0770e8fcbb567c43bc9e83a38950
stoichiometric feasibility theorem
  27b40b61903ae6c2e223d007ec08323ec9aec10e9198deb99d2d7c60d878d007
exact-tier atlas interface
  3b80734707dcac833621770c881da2be9782efc5658605179cd18e327a3c07d9
```

The current finite sources used for the selector and local-interface replay
are

```text
one_active_phase_shape.py
  781c1e6b5106cc6785ec6902d932fb319ef2078fb40b4e4f983fdc6f7bc45be4
one_active_relative_debt_cegar.py
  32d2313f428663c09a3d14e658f4c72a6ccbcaeb99c2b0cbf92dcce3c8b843ba
universal_fourth_power_interface_regression.py
  7daf079419a0000e8156178b3ef162c3736ba8b02a891ffe86ebbe19d371bed2
one_active_prospective_composition.py
  032670b1177295b3d901de97ad74bb0b299b273c25e0008619dbfeeb5f3f12f0
```

The old audited-note field
`652e41ccd7ae36183862a798fcdfd3bd5acf92ab2528bb356816d14df003b09a`
is historical metadata.  It is not inherited by, and was not used for, this
verdict.

## 2. Descriptor cover and one common potential

Fix one selected pair, one actual strong directed graph on each linkage,
its positive rates, and a closed irreducible class (Gamma).  The proof uses
the single population function

\[
 F(x)=K+\sum_i\log(x_i!),\qquad G=1+F\ge1,
 \qquad W(x)=G(x)^4.                                  \tag{2.1}
\]

There is no chart-dependent linear correction.  Stirling growth makes (W)
proper on population space and, since (0\le D_i\le X_i), on the reachable
marked space as well.

Exact descriptor extraction has finitely many outcomes.  A descriptor
realized by a sequence in (Gamma) is affine-feasible.  The selector's
defining property is that all 3,297 affine-feasible failures on its 1,227
pairs are one-active.  Hence every divergent sequence has a subsequence that
is either one-active failed or Anderson--Kim passing.

On a passing subsequence the exact fourth-power identity is

\[
 {cal L}W=4G^3{cal L}F
 +6G^2\sum_ra_r(\Delta_rF)^2
 +4G\sum_ra_r(\Delta_rF)^3
 +\sum_ra_r(\Delta_rF)^4.                            \tag{2.2}
\]

The descending-source estimate gives
({\cal L}F\le-cA_ng_n), with (g_n\to\infty), while
(\sum_ra_r\le CA_n), (|\Delta_rF|\le C\log R_n), and
(G\asymp R_n\log R_n).  Every term after the first in (2.2) is therefore
lower order.  In particular, on every divergent passing subsequence,

\[
 {cal L}W\to-\infty,
 \qquad {-{cal L}W\over G^3}\to\infty.              \tag{2.3}
\]

The bad-sequence argument is used correctly.  If non-(W)-good states had
unbounded second-largest population, a subsequence would have at least two
active coordinates and would contradict (2.3).  Thus, outside a finite set,
each non-good state lies in one of finitely many tubes

\[
 B_{X,e}=\{x:(x_i)_{i\ne X}=e\},
 \qquad e\in\{0,\ldots,M_\Gamma\}^2.                 \tag{2.4}
\]

This step does not infer a phase box from tightness.  For fixed (e), only
the integer level (X=n) diverges.  The local theorem is uniform along that
literal tube; there are finitely many (X,e), templates, and access rules.
Taking their minimum gives common classwise constants.  This justifies the
uniformity assertion in target Lemma 4.1; compactness is not being used to
manufacture a margin from unrelated pointwise inequalities.

## 3. From graph resistance to an all-clock physical kernel

The graph input quantifies directly over every strong orientation.  From a
historically consistent positive-debt base it gives either

\[
 0\le m_-=m\le2,
 \qquad m_+\ge m+1,                                  \tag{3.1}
\]

with a positive down witness, or a frozen/no-history alternative.  A chosen
word is not treated as a probability estimate.  The universal interface
lifts (3.1) to the aggregate stopped kernel after all zero-resistance loops
are summed.

For mixed rows, the finite or factorially weighted killed Green operator
gives, at active level (n),

\[
 p_D(n)\ge an^{-m},\qquad
 p_U(n)\le bn^{-(m+1)},                              \tag{3.2}
\]

and, for every fixed (q), the event-size-biased bound

\[
 \mathbb E[(1+Z+R_E)^q;E]
 \le C_{\Gamma,q}\mathbb P(E),
 \qquad E\in\{D,U\}.                                \tag{3.3}
\]

The finite Family-II base is the exact invariant slice (a_\Gamma), not an
asserted universal box.  Constants may depend on this fixed class value.
Direct-(X) rows use a killed unimolecular phase with nested exponential
weights.  Unbounded no-fast SCCs reduce analytically to a one-species strong
network on a subset of ({0,U,2U}), whose factorial Foster function gives
return, occupation, and size-biased endpoint moments.  Thus (3.2)--(3.3)
hold for aggregate kernels rather than selected histories.

At (m=2), the absence of low-order up words alone would not suffice.  The
proof separately bounds the unweighted three-paid-interruption remainder by
(Cn^{-3}), so (p_U=O(n^{-3})) literally.  The fixed minimal down witness
stays below the moving boundary, so the leading negative probability is not
borrowed from a boundary tie.

The 222 wholly-top rows use a different, valid input.  Their stripped phase
is the open immigration--death pair ({0,U}).  The Poisson-averaged
all-reaction block has a fixed positive service probability, (O(n^{-1}))
unresolved-entry probability, bounded physical duration, and every fixed
endpoint moment.  Geometric repetition therefore has effective (m=0).
The theorem does not substitute the wordwise resistance-one label for this
aggregate exponent.

Repeating neutral returns until the first nonneutral endpoint gives

\[
 \mathbb E K_n\le Cn^m,qquad
 \mathbb P\{\hbox{first nonneutral endpoint is up}\}\le Cn^{-1},
 \qquad \mathbb E\tau_n\le Cn^{m+r},                 \tag{3.4}
\]

with (m+r\le3).  Neutral population endpoints telescope inside one
episode.  They are not stopped and charged individually, which would create
positive fourth-power curvature.  A down endpoint yields

\[
 -c n^3(\log n)^4+O(n^3(\log n)^3),                 \tag{3.5}
\]

whereas the probability-weighted up cost is
(O(n^2(\log n)^4)).  The moment order (q>8) controls random active
overshoot and inactive factorial cost.  Physical duration in (3.4) is lower
order even at exponent three because (3.5) retains four logarithmic powers.

## 4. Actual endpoints and the moving boundary

The raw attempt stops at inactive mass (L_n=n^{1/8}), at the first
post-jump state.  The boundary-causing reaction is included.  A jump which
simultaneously causes a (D) or (U) return and crosses the boundary keeps
its terminal label but is charged by the boundary event, not by the bounded
nonboundary moment estimate.

For zero, one, or two paid interruptions, the phase maximum has an
exponential or factorial tail.  Every other boundary history has at least
three interruptions, and the endpoint-weighted ordered remainder gives

\[
 \mathbb E[(1+\sigma+J)^q;{cal B},J\ge3]
 \le C_qn^{-3+6/8}.                                  \tag{4.1}
\]

After at most (Cn^2) expected attempts, the complete boundary endpoint
cost is

\[
 \mathbb E[(\Delta W)^+;{cal B}]
 \le Cn^{2+7/8}(\log n)^4
 =o(n^3(\log n)^4).                                  \tag{4.2}
\]

This estimate includes nested active entries through the (J)-moment.  It
does not use the false pathwise claim that bounded inactive mass bounds
active overshoot.

At every genuine boundary endpoint the old active population is at least
(n-1), and another coordinate equals or exceeds (n^{1/8}).  Hence every
divergent boundary sequence has an at-least-two-active refinement.  Such a
descriptor passes on this selector, so (2.3) applies from the actual
endpoint.  No cleanup, forced same-axis return, or potential switch is made.
Equations (3.5) and (4.2), together with the up and duration bounds, prove

\[
 \mathbb E[W(X_\tau)-W(x)+\tau]\le-1                \tag{4.3}
\]

outside a finite subset of every fixed bad tube.

## 5. Reflected eligibility and classwise gluing

On every physical jump, all marks are propagated by

\[
 D_i^+=(D_i+\zeta_i)^+,
 \qquad H_i=X_i-D_i.                                 \tag{5.1}
\]

Induction gives (0\le D_i\le X_i) and (H_i\le x_i^\circ).  Therefore
the (D_X=0) part of a fixed-width (X)-tube is finite.  Every divergent
reachable bad-tube state has (D_X>0), exactly the premise of the local
kernel.  A graph-theoretic no-history face cannot carry that positive mark;
a completely frozen state is a singleton class.  A down endpoint reduces
existing old debt even when one unit merely reaches zero.  No surplus
service beyond zero is assumed.

Outside a finite marked target, use the disjoint statewise priority:

1. if ({\cal L}W\le-1), run generator-good motion to the target or the
   bad-tube set;
2. otherwise run the selected all-clock episode (4.3) from its actual
   endpoint data.

There is one common (W) and common constants (eta=delta=1) after a
finite enlargement.  If the finite target is visited inside an episode,
record that physical hit immediately; completing that episode only for
drift accounting gives an upper bound on the true hitting time.  Conditional
iteration and (W\ge0) yield, for the accounting time (S_m) and truncated
exceptional-episode count (N_m),

\[
 \mathbb E N_m+\mathbb E S_m\le W(x)+1.              \tag{5.2}
\]

Thus neither infinitely many episodes nor a final generator-good segment
of infinite duration can avoid the target.  The mean physical hitting time
is finite.

The all-zero-debt set is finite because (D=0) implies
(X=H\le x^\circ).  To justify the final recurrence step without a hidden
mark reset, take one ordinary physical jump from the finite marked target,
update every mark by (5.1), and apply the hitting estimate from each of the
finitely many marked successors.  This gives a finite mean positive return
to a finite marked set.  A finite recurrent return class has a finite cycle
occupation measure; projecting that measure gives an invariant probability
for the physical chain.  Physical irreducibility promotes positive
recurrence to every state of (Gamma).  An absorbing singleton is already
positive recurrent.

Finally, nonexplosion is independent of the Foster conclusion.  Any reaction
which increases total population has source degree at most one, so its
aggregate positive-jump rate is bounded by (C(1+|x|_1)).  Localization and
Gronwall prevent population escape in finite time.  Within a fixed
population sublevel there are finitely many states and bounded total rates,
so population-preserving quadratic clocks cannot accumulate.

## 6. Counterexample attempts and finite arithmetic

The hostile replay specifically tested the proof against the known failure
modes:

1. charging neutral returns separately (invalid fourth-power curvature);
2. replacing aggregate resistance by one selected word;
3. treating the open Poisson phase as a finite box;
4. using only coefficient cancellation at resistance two;
5. bounding active overshoot solely by instantaneous inactive mass;
6. omitting the boundary-causing jump or a simultaneous boundary tie;
7. treating a cap-two Family-II spectator as uniformly bounded; and
8. requiring service from zero debt or resetting the mark at a chart handoff.

The current proof explicitly avoids all eight.  No adverse strong
orientation, rate choice, fixed-class invariant, endpoint, or duration seam
remains.

The finite replay was restricted to set identity.  It gives

```text
candidate 1,227       3ab28358663c45a089a5bdf4144c28573718b0c4f8b05472a0af208ca919fcf8
prior overlap 15      6ec74f95e50e39ecda002b988d8233ae74c040ff9bb3518892dfd980bfad06d3
new disjoint 1,212    a7784a1f98da2fbadd70a62bc97fe852393cb410a24e666a6d6c246998f0f579
remainder 795         6a1327e6c38bfcab30d334691415ba457e84d45d1dfe53d81df4c02aad868123
```

The twelve focused selector/interface tests pass.  They confirm only the
finite identities and frozen exponent arithmetic; the analytic verdict is
the proof replay above.  Global T3-2 remains outside this audit.
