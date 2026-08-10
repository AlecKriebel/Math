# The 36 promotion-only support pairs

## 1. Exact scope and provisional status

After the four already certified disjoint branches are removed, the exact
promotion selector contains 36 support pairs with no affine-feasible
one-active failure. Every selected pair has exactly one feasible failed
descriptor, and that descriptor is two-active. The disjoint split is

\[
\begin{array}{c|r|r}
\text{failed phase}&\text{incidences}&\text{pairs}\\ \hline
\text{enabled top seed}&20&20\\
\text{dormant finite shell}&16&16
\end{array}                                             \tag{1.1}
\]

There are 32 positive-invariant pairs and four signed pairs. Their pair
fingerprint is

```text
f2ad8cbe4b9ca7f36c39bed4bfe5aaafc6a9152eaf300390b5c25ba546519137
```

This note gives a proof-level candidate physical-time theorem for exactly
these 36 pairs. Its executable flags remain false until an independent
audit checks the stopping rules and endpoint estimates.

## 2. One common proper potential

For a fixed selected network, put

\[
 {\cal F}_\ell(x)=\sum_{i=1}^3\log(x_i!)+\ell\cdot x.   \tag{2.1}
\]

Choose \(\ell=0\) in the eight seeded rows with no wholly top linkage. In
the other rows there is one reversible two-complex whole-top linkage. Choose
\(\ell\) by detailed balance on that linkage:

\[
 \ell\cdot(z-y)=\log{\kappa_{zy}\over\kappa_{yz}}.     \tag{2.2}
\]

The supports which occur are

\[
 \{A,B+C\},\ \{B,A+C\}\quad\hbox{in twelve seeded rows}, \tag{2.3}
\]

and

\[
 \{A,B\}\quad(5\text{ dormant rows}),\qquad
 \{B,2A\}\quad(11\text{ dormant rows}).               \tag{2.4}
\]

After adding a network-dependent constant, (2.1) is nonnegative and proper
on \(\mathbb N_0^3\). A fixed linear correction does not change any strict
D-tier logarithmic gap. Consequently the usual Anderson--Kim source-tier
argument applies to every passing descriptor for the same \({\cal F}_\ell\).
Only the single failed descriptor listed in (1.1) needs a stopped episode.

## 3. The twenty enabled-seed rows

All network complexes in these rows have descriptor weight zero or one.
Along an exact realizing sequence write \(N\) for any top source monomial.
Exact D-tier equivalence gives finite positive ratios between all top source
monomials, while every enabled lower source has rate \(O(1)=o(N)\).

Choose an enabled vertex \(y_0\) in the proper top subset of one linkage.
Strong connectivity supplies a simple directed path

\[
 y_0\longrightarrow y_1\longrightarrow\cdots
 \longrightarrow y_j,                                 \tag{3.1}
\]

stopped at the first target outside the global top tier. If an intermediate
top target needs the inactive species, it is an actual target and therefore
is enabled for the next edge. Along the prescribed path the inactive count
never exceeds a support-dependent constant and active populations change by
only \(O(1)\). Thus every prescribed edge has rate at least \(cN\), and the
total rate of all top-sourced competitors is at most \(CN\). The path length
is at most the number of complexes in its linkage. It follows from the
successive exponential races that

\[
 \mathbb P\{\text{(3.1) fires before every competitor}\}\ge p>0. \tag{3.2}
\]

Stop on completion of (3.1) or on the first competing reaction. The duration
is stochastically bounded by a fixed sum of exponentials of mean \(C/N\).
Every top-to-top competitor changes \({\cal F}_\ell\) by \(O(1)\): exact
tier equivalence controls its factorial ratio, including a newly created
inactive molecule. A top-to-lower competitor is already favorable. A
lower-source competitor has probability \(O(N^{-1})\); its positive
factorial cost is at most \(O(\log N)\), and the sharper
propensity-times-log estimate

\[
 u\log^+(v/u)\le v/e                                  \tag{3.3}
\]

also covers a refined subpower subsequence.

The final edge in (3.1) has a top source and a weight-zero target. Hence

\[
 \Delta_{y_{j-1}\to y_j}{\cal F}_\ell
 =-\log N+O(1).                                        \tag{3.4}
\]

Combining (3.2)--(3.4) gives a physical stopping time \(\tau_N\) with

\[
 \mathbb E\Delta{\cal F}_\ell\le-p\log N+O(1),
 \qquad
 \mathbb E\tau_N^m=O(N^{-m})                           \tag{3.5}
\]

for every fixed \(m\). The number of population jumps before the endpoint
is pathwise bounded, so every endpoint moment required for localization is
automatic after scaling the two active coordinates.

## 4. The sixteen dormant finite-shell rows

The inactive coordinate is \(C\) in all sixteen rows. The exact support
certificate proves:

1. the wholly top linkage is one of the two supports in (2.4);
2. the proper linkage contains \(2C\);
3. at \(C=0\), its enabled source set is one of
   \(\{0\},\{A\},\{0,A\}\), or is empty; and
4. the empty case occurs in exactly two incidences.

### 4.1 Whole-shell endpoint and interior estimates

For \(A\leftrightarrow B\), put \(H=A+B\) and use the correction (2.2).
The exact generator identity and \(\log u\le u-1\) give

\[
 {\cal L}_*{\cal F}_\ell\le\kappa_{AB}+\kappa_{BA}.    \tag{4.1}
\]

The chain is an Ehrenfest birth--death chain on its finite \(H\)-shell. An
exponential supermartingale in the two boundary strips gives, from every
exact-tier compact interior start and for every fixed \(L,m\),

\[
 \mathbb P\{(A_t/H,B_t/H)\text{ leaves a fixed larger interior set}
              \text{ for some }t\le L\log H\}
 \le C_{L,m}H^{-m}.                                    \tag{4.2}
\]

For \(B\leftrightarrow2A\), put \(H=A+2B\) and
\(N\asymp\sqrt H\). The independently audited estimates (3.4), (6.4), and
(6.5) of *rank_one_multichannel_carrier.md* give the corresponding
statements: uniform scaled endpoint moments at independent bounded-rate
clocks, super-polynomial interior retention through \(L\log N\), and
uniformly bounded expected net \({\cal F}_\ell\)-cost. Thus, in both
templates,

\[
 \mathbb E[{\cal F}_\ell(X_S)-{\cal F}_\ell(X_0)]\le C \tag{4.3}
\]

at a bounded finite sequence of independent \(0\)-source waits or killed
\(A\)-source occupation windows. Equation (4.1) proves this directly for
the unimolecular shell; the stopped semigroup estimate proved in the
corrected-factorial endpoint theorem gives it for \(\{B,2A\}\).

### 4.2 A finite actual-target activation block

Fix a simple directed path in the proper linkage from an enabled base
vertex in \(\{0,A\}\) to \(2C\). At an actual target on this path, use the
following physical block before proceeding.

- A \(0\)-source edge is an independent bounded-rate clock while the whole
  shell evolves. Equations (4.2)--(4.3) control that wait.
- An \(A\)-source edge is sampled on an \(O(N^{-1})\) occupation window.
  The interior estimate keeps \(A\ge cN\), so its integrated clock has a
  fixed positive success probability and all other lower clocks are retained
  by the conditional Poisson construction.
- At a source in the global top subset \(\{AC,BC\}\), the actual target keeps
  the next source enabled, but the clocks need not have the same leading
  scale. In the \(\{B,2A\}\) shell, a \(BC\)-source clock can be
  \(\Theta(N^2)\) while \(AC\)- and \(A\)-source clocks are only
  \(\Theta(N)\).
- If a faster top exit consumes the carried \(C\) before the next slower
  edge, it either gives the desired strict active-workload exit or returns
  to an earlier base vertex. Restart the finite path. It is not discarded
  as a skipped fast jump.

**Audit boundary.** Independent review validates Sections 2--4.1 but shows
that the direct-race argument below is not yet proved in the
\(\{B,2A\}\) shell: the scale separation just displayed does not supply a
uniform \(p>0\), so the proposed \((1-p)^K\) bound cannot currently be used.
A viable repair would contract the fast whole-shell motion to a finite
priority macrochain carrying the actual target and at most two units of
reflected workload debt. The rest of this subsection records the conclusion
that such a macrochain lemma must establish; it is not a certified proof.

There are only finitely many path vertices. The proposed completion caps the
number of attempts at each vertex by one deterministic integer \(K\) and must
prove that the probability of reaching a \(C\)-only target is at least
\(a>0\), while the probability of stopping with unresolved active-workload
debt is at most \(C(1-p)^K\).

If the path began at \(A\), its total lower-linkage displacement from \(A\)
to \(2C\) already lowers the descriptor workload by one. If it began at
\(0\), reaching \(2C\) is workload-neutral. In the latter case append one
additional unpaired exit from an enabled \(AC\) or \(BC\) source to the
complement of the proper top set. On the interior event its source rate has
the full top scale, and a deterministically capped carrier gives this exit
with probability \(s>0\). Increase \(K\) once more so that the unresolved
debt probability is at most \(as/8\). Conditional on the missing
priority-macrochain estimate, the workload bookkeeping would be

\[
 \mathbb E\Delta H_w\le-as/2<0,
 \qquad |\Delta H_w|\le C.                             \tag{4.4}
\]

Only a fixed number of lower reactions and killed windows occur. Their
duration has moments of every fixed order, uniformly in the shell. The
whole-shell endpoint has every fixed scaled active moment, and \(C\) is
bounded by the deterministic carrier length. There is no inactive-coordinate
truncation.

On the interior event,

\[
 \log(A\vee1)=\log N+O(1),\qquad
 \log(B\vee1)=
 \begin{cases}
   \log N+O(1),&L_*=\{A,B\},\\
   2\log N+O(1),&L_*=\{B,2A\}.
 \end{cases}                                           \tag{4.5}
\]

Hence every bounded lower jump has

\[
 \Delta{\cal F}_\ell=\Delta H_w\log N+O(1).           \tag{4.6}
\]

Equations (4.2)--(4.3), the deterministic attempt cap, and (4.4)--(4.6)
would then give

\[
 \mathbb E\Delta{\cal F}_\ell\le-c\log N+O(1).        \tag{4.7}
\]

The exceptional interior-exit probability is super-polynomial, while the
factorial oscillation on the finite whole shell is polynomial times
\(\log N\); its endpoint contribution is therefore \(o(1)\).

### 4.3 The two disabled rows

If the enabled set in item 3 is empty, the proper linkage is identically
disabled at \(C=0\), and the whole linkage preserves \(C=0\) and its finite
workload shell. On a fixed closed irreducible class, that workload has one
fixed value. The class is therefore finite, so no divergent sequence in the
class realizes the displayed descriptor.

## 5. Classwise composition

> **Candidate Theorem 5.1.** Give either linkage of any of the 36 selected
> support pairs an arbitrary strongly connected orientation and arbitrary
> positive rates on its present edges. Then every closed irreducible
> population class is positive recurrent.

Fix a closed irreducible class \(\Gamma\). If a divergent sequence in
\(\Gamma\) lies in a passing source-tier cone, the standard generator
estimate for the fixed potential (2.1) tends to \(-\infty\). If it lies in
the unique failed cone, Section 3 or Section 4 gives a physical episode with

\[
 \mathbb E_x\{\Delta{\cal F}_\ell+\eta\tau\}\le-1      \tag{5.1}
\]

outside a finite set; the disabled alternative is not divergent in
\(\Gamma\). A bad-sequence contradiction turns these sequence estimates
into one finite exceptional set. The common-entropy physical-time gluing
theorem then gives finite mean hitting of that set.

Nonexplosion is elementary here and in the full binary class: a reaction
which increases total population has a source of molecularity at most one,
so the positive part of the total-population generator is bounded by
\(C(1+|x|)\). Local finiteness and finite mean return from the finite target
give positive recurrence of \(\Gamma\).

No pair count is promoted by this note before independent audit. If the
candidate theorem passes, the ordered residual arithmetic would be

\[
 (1871,191)\longmapsto(1839,187).                       \tag{5.2}
\]

## 6. Audit obligations

An independent replay should check, in this order:

1. that every prescribed seeded path retains all top competitors and that
   its lower-source positive logarithmic cost is uniformly integrable;
2. the exact unimolecular endpoint inequality (4.1) and the boundary
   supermartingale (4.2);
3. that the dormant actual-target path can be restarted after every faster
   top exit without silently deleting a reaction;
4. the unresolved-debt coefficient in (4.4), including paths started from
   \(A\) rather than \(0\);
5. the lift from (4.4) to the common factorial drift (4.7); and
6. the fixed-class treatment of the two disabled rows and the disjoint
   36-pair selector.

Until those six checks pass, all analytic and pair-level flags stay false.
