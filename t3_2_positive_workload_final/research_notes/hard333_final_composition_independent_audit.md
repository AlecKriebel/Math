# Independent hostile audit of the frozen hard-333 composition

**Verdict (2026-08-12 PDT): STRICT PASS.**  At the exact bytes below, the
hard-333 theorem proves positive recurrence on every closed irreducible
population class of each of the 333 hard support pairs, for every strongly
connected orientation and every fixed positive rate vector.  The proof uses
one literal corrected-factorial fourth power for each fixed pair, retains
physical time and actual endpoints, and closes by a valid random-time Foster
argument.

This is a proof-first verdict.  Finite computation was used only to replay
the descriptor partition, analytic premises, physical multiplicities, and
literal correction masks.  It was not used to search orientations,
histories, population boxes, or stochastic paths.  The audit does not certify
the global T3-2 theorem; other classwise branches, in particular the separate
single-linkage branch, are outside its scope.

The frozen targets are

```text
theorem  ddcc1f054febae9f08bb4d78bd66569ff4eebdd367b5cb4479b9029c960ecf84
source   de618c831152352f0898cdb6cd6a0bfc286e73c6b15d28c507ad4fd8ecde9049
tests    fb1becfc2183ec691d711375459ef75bc824668a6b348ad4530cd6d11bb09e0a
```

The independent finite replay is frozen at

```text
source   77deb4e4ac1963a2f8a7b1ce6bea10fb9bbada0279dea1789ec453777af24c41
tests    49771d289ecd5639e4d09bb6f411daaae2a59836f93e35ec18a45267f50d207d
payload  1fa6a38cc95437183d159376e120284594af3bf417c2a4bc9ae8ec909abd11f9
```

The replay source pins every local proof dependency used here.  In
particular it pins the audited one-active 1,104 theorem and its 105-row
multi-service repair, physical 188, enabled 181, rank-one 114, the discrete
powered all-active theorem, the directed-triple estimate, and the two
switch theorems.  A later edit to any of those files cannot silently inherit
this verdict.

## 1. One literal potential on each pair

Fix one support pair, its directed reaction graphs and rates, and one closed
irreducible class.  The proposed state function is

\[
 G_\ell(x)=K_\ell+\sum_{i=1}^3\log(x_i!)+\ell\mathbin\cdot x\ge1,
 \qquad W_\ell(x)=G_\ell(x)^4.                         \tag{1.1}
\]

There is no chart-dependent normalization in (1.1).  On a reversible
two-node top, detailed balance prescribes one scalar equation for
\(\ell\); on a homogeneous directed triple, the audited fluid construction
prescribes its fixed correction.  The same physical top linkage, orientation,
and rates are present whenever that top reappears in another dimension.  On
an \(H_w\) pair the theorem makes the explicit common choice \(\ell=0\).
All remaining pairs may, and for definiteness can, take \(\ell=0\).

The independent support replay proves a stronger statement than the frozen
candidate test records:

\[
\begin{array}{c|r|r}
\text{correction-bearing scope}&\text{pairs}&
                    \text{pairs with exactly one top mask}\\ \hline
\text{two-active rank-one}&38&38\\
\text{all-active}&46&46\\
\text{union}&46&46.
\end{array}                                             \tag{1.2}
\]

All 38 rank-one/all-active overlaps have identical masks.  This includes,
but is stronger than, the twelve \(H_b\) seam checks.  The four \(H_w\)
pairs have no rank-one mask.  Hence a pair cannot hide two different
detailed-balance vectors under the same correction-family label.  The exact
pair menu is

\[
 291\ \text{arbitrary},\qquad34\ \text{reversible},\qquad
 8\ \text{directed triple}.                           \tag{1.3}
\]

Finally, the factorial term dominates every fixed linear correction.  Thus
one finite \(K_\ell\), independent of shells and episodes, makes
\(G_\ell\ge1\), and \(W_\ell\) is proper.

## 2. Reflected debt and the repaired multi-service timing

On the reachable lift from \((x^\circ,0)\), the update

\[
 D_i^+=(D_i+\zeta_i)^+,
 \qquad H_i=X_i-D_i                                      \tag{2.1}
\]

has the exact induction

\[
 0\le D_i\le X_i,\qquad H_i^+\le H_i\le x_i^\circ.       \tag{2.2}
\]

If reflection is inactive, \(H_i\) is unchanged; if it is active,
\(H_i\) decreases.  Consequently a divergent one-active sequence with old
active species \(V\) cannot have \(D_V=0\), because then
\(V=H_V\le x_V^\circ\).  A structural no-history face, on which \(V\)
never changed, likewise cannot carry positive selected debt.  Thus the
positive-debt premise is derived from reachability; it is not imposed on an
arbitrary unmarked start.

For each of the repaired 99 direct and six open rows, let \(u\) be the
initial inactive cloud and run

\[
                             K=1+u                         \tag{2.3}
\]

net physical services.  The first service \(D_1\) is internal: it lowers
incoming old debt but is not substituted for the stopped endpoint.  The
included \(K\)-th service \(D_K\) is the terminal clean endpoint.  If
reflection reaches zero before \(D_K\), all intervening services are
ordinary surplus physical services and lower the historical residual.
No hypothesis \(D_V\ge K\) is used.

On the direct rows, stripping the common active molecule leaves a
unimolecular labelled-particle system.  A simple directed path from the
pure active complex to its first active-free vertex supplies a tagged
service event of fixed positive probability in a fixed active-time
interval, uniformly over all background particles.  Background services
are already successes, while background top-to-top reactions cannot move
the tag.  Therefore the active time to \(K\) services has negative-binomial
moments.  The inactive mass is bounded pathwise by its initial value, a
Poisson immigration count, and twice the service count.  Integrating every
active-free-source clock against that bound preserves an endpoint-weighted
factor \(n^{-1}\); the moving-cutoff endpoint is superpolynomially rare.

On the six open rows, the unlocalized stop is autonomous in \((B,C)\).
It is independent of the clocks driving \(A\), so conditional on the whole
stopped \((B,C)\)-path the endpoint identity

\[
 A_\tau\ \stackrel d=
 \operatorname{Bin}(u,e^{-\beta S})+
 \operatorname{Pois}\!\left({\alpha\over\beta}(1-e^{-\beta S})\right)
                                                               \tag{2.4}
\]

is exact.  It is not a terminal-time formula applied after an
\(A\)-dependent localization.  Strong connectivity makes the aggregate
origin-launch parameter positive: otherwise \(\{0,B+C\}\) would be a
closed proper subset of the four-vertex linkage.  Neutral attempts are
geometric, a complete macrocycle has net active change \(-1\), and only
after constructing the autonomous stop is the \(A\)-cutoff imposed.

On clean completion the active factorial reward is

\[
 \log{(n-K)!\over n!}=-K\log n+O(K^2/n),              \tag{2.5}
\]

whereas the complete inactive factorial-linear endpoint cost is at most
\(C K\log(2+K)\).  Since \(K=n^{o(1)}\), (2.5) wins.  The correction is
the telescoping endpoint difference
\(\ell\cdot(X_\tau-X_0)\), not the sum of absolute corrections of internal
jumps.  Polynomially endpoint-weighted defect bounds, superpolynomial
boundary bounds, and the exact fourth-power identity give

\[
 \mathbb E[W_\ell(X_\tau)-W_\ell(X_0)+\tau]
 \le-cG_\ell(X_0)^3(1+u)\log n.                    \tag{2.6}
\]

Every completion, defect, and cutoff includes its causing reaction.  Both
mechanisms provide all fixed endpoint moments and physical-duration
moments, hence in particular one common required order \(q>8\).  This
closes the only gap found by the earlier hostile one-active audit.

## 3. Two-active and all-active interfaces

The two-active partition is analytic, not probabilistic enumeration.

1. The 407 dormant incidences normalize, with physical multiplicity, to
   188 carrier templates.  The exact 19 and nonexact 169 stopped theorems
   both quantify over arbitrary fixed \(\ell\), retain every physical
   holding interval and boundary-causing reaction, and return the actual
   endpoint with all required moments.  The independent replay verifies
   the literal \(407\to188=19+169\) support identity.
2. Each of the 181 enabled incidences has an enabled vertex in the exact
   top D-tier.  Strong connectivity supplies a simple directed path to the
   first vertex outside that tier.  At most four all-clock races have a
   fixed positive success probability; every competitor is the actual
   endpoint.  Its positive factorial cost is controlled sourcewise by
   \(r\{1+\log(1/r)\}^q\), so endpoint moments above order eight are
   available for arbitrary fixed \(\ell\).
3. Each of the 114 closed rank-one rows uses the audited powered carrier
   endpoint.  The shell exponential-overshoot estimate survives polynomial
   killing size bias, the actual lower jump is included, and all four
   activation rows are physical.  The unique rank-one mask is the same
   mask used by every all-active overlap, so the correction is literally
   the pair correction from Section 1.

For the all-active rows, the 110 safe reversible incidences use the
**discrete** corrected-factorial theorem.  This is important: the proof does
not identify continuous entropy with \(\sum_i\log(x_i!)\).  The pinned
discrete theorem separately proves that their bounded-reaction jump
difference is \(o(1)\), pairs the two top directions, absorbs the top carré
term with reversible dissipation, and lets the diverging lower-tier exit
absorb the remaining fourth-power terms.

The 24 directed-triple rows use the fixed directed-fluid correction.  On
the flat top, corrected-entropy jumps are \(O(1)\), total top rate is
\(O(N^2)\), and the lower negative rate is at least order \(N\) with a
diverging gap.  Since \(G\ge cN\log N\), the largest top remainder divided
by the leading negative term is at most
\(C/(a_N\log N)\to0\).

The sixteen \(H_b\) incidences use the guard-free same-state shell
resolvent.  Its physical \(K_\ell\) is shell-independent; only the
normalizing rewrite of the shell law varies.  The bounded-energy Kac block
uses only relaxation divided by killing, while outside the core the top
flux and lower high cut absorb their own fourth-power remainders separately.
Its actual lower jump and duration have moments through an integer
\(p>8\).  If that jump reaches a lower-dimensional face, its appended
route lies in the now-audited common-\(W_\ell\) menu.

The four \(H_w\) rows use \(\ell=0\).  The patched dyadic theorem covers
both dormant and activated starts, all competing clocks, unsuccessful
attempts, high exits, overshoots, and physical duration.  Its fractional
population return is converted by the deterministic factorial envelope to
a decrease of the same \(W_0\), not an auxiliary workload.  The only
orientation fact needed by that proof has a direct graph argument.  Among
the two minimum-height vertices, at least one has an edge to a higher vertex,
or else the minimum pair would be a closed proper subset of the strongly
connected graph; a minimum vertex without such a direct edge must have an
edge to the other minimum vertex.  Thus the stochastic proof does not rely
on exhausting the 1,606 directed masks.  Their executable histogram is only
a finite regression replay of this structural trichotomy.

Thus every lower-dimensional handoff begins at the actual population and
uses the identical state function.  No comparison toll or artificial
restart remains.

## 4. Passing descriptors and exhaustion

For a passing descriptor let \(A_s\) be the maximal enabled source
propensity and let \(g_s\to\infty\) be its forced logarithmic exit gap.
The fixed correction changes a bounded reaction by only \(O(1)\), so the
standard source-tier estimate gives

\[
 \mathcal LG_\ell\le-cA_sg_s,
 \qquad \sum_r a_r\le CA_s,
 \qquad |\Delta_rG_\ell|\le C\log(1+|x|).             \tag{4.1}
\]

Because \(G_\ell\asymp |x|\log(1+|x|)\), inserting (4.1) into the exact
fourth-power generator identity makes every second-through-fourth term
lower order than \(-G_\ell^3A_sg_s\).  Hence
\(\mathcal LW_\ell\to-\infty\) on every divergent passing sequence.

The independent finite replay reconstructs the failed rows from the
lower-level one-, two-, and three-active tables and agrees byte-for-byte
with the candidate row payload:

\[
 1104+702+154=1960\quad\text{failed incidences on 333 pairs}.   \tag{4.2}
\]

Its route histogram is exactly

\[
\begin{array}{c|r@{\qquad}c|r}
\text{one-active generalized}&951&\text{direct multi-service}&99\\
\text{mixed Schur}&44&\text{frozen}&4\\
\text{open multi-service}&6&\text{physical carrier}&407\\
\text{enabled word}&181&\text{rank-one endpoint}&114\\
\text{safe reversible}&110&\text{directed triple}&24\\
H_b&16&H_w&4.
\end{array}                                             \tag{4.3}
\]

This table establishes only exhaustion and premise membership.  The
stochastic estimates in Sections 2--3 are analytic and quantify directly
over every strong orientation and positive rate vector.

Exact descriptor compactness now has the correct role.  If infinitely many
reachable marked states were neither generator-good nor episode-good,
properness would give a divergent sequence.  A fixed-descriptor subsequence
would be passing or enter one of the analytic cases above, a contradiction.
Since the chart library is finite and every local negative magnitude
diverges on its escaping sequences, one finite enlargement yields constants
\(a,\eta,\delta>0\) with

\[
 \mathcal LW_\ell\le-a                                  \tag{4.4}
\]

on generator-good states and

\[
 \mathbb E_z[W_\ell(X_{\tau_z})-W_\ell(x)+\eta\tau_z]
 \le-\delta                                             \tag{4.5}
\]

on the episode-good complement outside a finite target.

## 5. Random-time Foster replay

The gluing argument does not assume recurrence of a boundary chart.  From a
generator-good state, stop at first entrance into the episode-good set or
the finite target.  Localized Dynkin and nonnegativity of \(W_\ell\) give

\[
 \mathbb E[W_\ell(X_\sigma)-W_\ell(x)+\eta\sigma]\le0. \tag{5.1}
\]

In particular \(\mathbb E\sigma<\infty\), so this segment cannot remain
generator-good forever.  At an episode-good endpoint, append its selected
physical stop from (4.5), then repeat from its actual endpoint.  Summing the
conditional inequalities up to the \(m\)-th episode gives

\[
 \delta\,\mathbb E N_m+
 \eta\,\mathbb E S_m\le W_\ell(x)+\delta,             \tag{5.2}
\]

where \(N_m\) is the truncated number of completed exceptional episodes
and \(S_m\) includes all intervening physical time.  If the finite target
is visited inside an episode, completing that episode for drift accounting
only enlarges \(S_m\), so (5.2) still bounds the true hitting time.

Monotone convergence gives finite expected episode count and accumulated
time.  Failure to hit the target would require either infinitely many
episodes, contradicted by finite expected count, or a final generator-good
segment that never exits, contradicted by (5.1).  Therefore every reachable
marked state has finite mean physical hitting time of the finite target.

The lifted target is genuinely finite: for each population
\(0\le D_i\le X_i\), and properness gives finitely many populations in a
\(W_\ell\)-sublevel.  From the finite target, take one physical jump and
apply the same hitting estimate to its finitely many possible successors.
The resulting finite trace has a recurrent state with finite mean positive
return.  A marked return implies a return of its physical projection, and
irreducibility of the fixed population class promotes positive recurrence
to every physical state.

## 6. Nonexplosion

Let \(N=|X|_1\).  In a binary network, a population-increasing reaction
cannot have a bimolecular source because every target also has molecularity
at most two.  Hence the total rate of population-increasing reactions is at
most \(C(1+N)\).  Stopping at population level \(m\), the generator bound
for \(N\) and Gronwall make the probability of reaching level \(m\) before
any fixed time tend to zero.  Inside a fixed population sublevel there are
finitely many states and bounded total rates, so population-preserving or
decreasing quadratic reactions cannot accumulate there.  This proves
nonexplosion independently of the Foster construction.

## 7. Verdict boundary and reproduction

All proof obligations in the frozen hard-333 theorem pass: common scalar,
historical-debt eligibility, \(D_1/D_K\) timing, actual endpoints, moments
above order eight, dimensional handoffs, passing-descriptor descent,
properness, nonexplosion, random-time gluing, and finite-mean return.
Therefore the strict mathematical conclusion is the pair-level theorem:
all 333 hard pairs are positive recurrent on every closed irreducible
class under the stated arbitrary-orientation and positive-rate quantifiers.

The frozen candidate correctly kept its own audit, pair, and global flags
false before this replay; this audit did not edit or promote them.  Global
T3-2 remains false here because it requires the independent classwise union
outside the hard-333 scope.

Reproduce the finite premise replay with

```text
PYTHONPATH=src /opt/homebrew/bin/python3.14 -B \
  src/hard333_final_composition_independent_audit.py
PYTHONPATH=src /opt/homebrew/bin/python3.14 -B -m unittest \
  tests/test_hard333_final_composition_independent_audit.py -v
```
