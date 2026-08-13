# Consolidated exact-byte audit of three two-linkage pair theorems

**Audit date:** 2026-08-12 PDT  
**Method:** proof-first hostile replay; no orientation or population
enumeration.  Finite computation was used only to recover and compare the
three ordered support-pair sets.

## 1. Exact targets and verdicts

The audited targets are

```text
821478a8c4410a371f99fa9df02e18ab5dbcc7c24aafa78f7d0db20cb6ab0bbe
    research_notes/rank_two_global_return_all14.md
3f8c3662ed55d13133ef67f5e4e75e7ef9057075fa6e755faf33420e71ea0a26
    research_notes/all_active_only_reversible_top.md
2f52d0ed580c70916fbe75f13e8ea09d77af53940bdf21048b43423830620f97
    research_notes/two_active_promotion_36_pair_theorem.md
```

The separate verdicts are:

1. **Rank-two fourteen-partner theorem: STRICT PASS as a standalone
   classwise recurrence theorem.**  It uses a proved finite handoff between
   two workloads.  It is not, and must not be cited as, a one-common-potential
   local episode interface.
2. **All-active-only 51-pair theorem: STRICT PASS.**  One proper
   rate-adjusted entropy is used on every generator chart and every fixed
   class.
3. **Promotion-only 36-pair theorem: STRICT PASS.**  One proper
   factorial-linear potential is used on passing cones and at every physical
   episode endpoint.

Every verdict includes arbitrary strongly connected orientations, arbitrary
positive rates on present edges, all physical clocks, actual endpoints,
physical duration, nonexplosion, and finite mean positive return in each
closed irreducible population class.

## 2. Mechanical derivative of the fourteen-partner target

The mathematical target initially inspected had SHA-256

```text
2abe5e1266286a90853a952be71706329c7869277f9b64c3c07965919725a597
```

Pandoc exposed invalid placement of equation tags inside `split`
environments.  The derivative audited above changes no numerical
expression, inequality, stopping rule, or argument.  The exact mechanical
changes were:

* move the tags for displays (3.4), (4.3), (5.4), (6.5), and (6.6) from an
  internal row to the enclosing display;
* separate the two rows (4.7)--(4.8) into two displays, preserving both
  formulas and labels; and
* replace the three rendered set-difference commands
  `\setminus` by the semantically identical
  `\mathbin{\backslash}`, because the default Latin Modern math font omitted
  Pandoc's chosen setminus glyph.

The resulting exact derivative is `821478...`.  The proof replay below is
against those current bytes, so the verdict does not rely merely on
inheritance from the earlier file.

## 3. Finite scope and disjointness only

The three current selector sources have exact hashes

```text
b2a96061516ad3348e7dc997121d2acb989488077a3f03495e58c09ad5890363
    src/rank_two_return_certificate.py
c25c18fc85f37a54e02028f4ac8afd389f60c56bad3aa5a40f8b875b99c2eed1
    src/all_active_only_recurrence.py
952f28d4900ccadaf535a08fcb995488828ef8e274c12b4043009a9904de948a
    src/two_active_promotion_obstruction.py
```

They were invoked only to form the three pair sets and compare them.  The
replay returned

```text
scope                         pairs  pair fingerprint
rank-two partners                14  d169edd59dd5acbead528a02cb14e9fcc00cc6ff4fb0203e97139844226d07b6
all-active-only                  51  cc1d4b0941588f7b664a3266076789e548ae1f675924854eff18c9552d86e3ea
promotion-only                   36  f2ad8cbe4b9ca7f36c39bed4bfe5aaafc6a9152eaf300390b5c25ba546519137
```

Every pairwise intersection has cardinality zero.  The union has 101 pairs
and fingerprint

```text
6ff214ff5965bf3ec54a2098eb82d28bbbf941a124f9de1412ba7be096ac7fee
```

No finite result in this section is used to prove a stochastic estimate.
In particular, no orientation, rate vector, reaction history, or population
box was generated or tested.

## 4. Rank-two fourteen-partner theorem

### 4.1 Arbitrary orientations and the outer workload

Write the rates of the fast support

\[
                         \{B,2A,B+C\}
\]

as in target (2.1), allowing a missing directed edge to have coefficient
zero.  Strong connectivity makes

\[
 I_0=\left(\frac r{s+r},\frac{t+v}{v}\right)
\]

nonempty and places points of \(I_0\) arbitrarily close to one.  If both
endpoints were one, no fast edge would enter \(B\), contradicting strong
connectivity.  Hence one can choose \(\lambda\in I_0\) and \(\rho>0\), both
near one, with \(p_B=2\rho-\lambda>0\).

For the lower linkage, molecularity makes every quadratic-source coefficient
nonpositive at \(\rho=1\).  Equality at both possible quadratic sources
\(2C,A+C\) would make them a closed directed subset.  If only one equality
occurs, perturbing \(\rho\) to the indicated side makes it strict while
preserving all already strict inequalities.  Thus

\[
                         U=\rho A+p_BB+C
\]

has positive coefficients and is proper, and target (2.12) gives strict
physical-time generator drift outside the return region.  The bounded-jump
power estimates control both the outer-return duration and its actual
endpoint.  This argument permits every strong orientation and every fixed
positive present-edge rate; its constants may depend on that fixed graph and
rate vector.

### 4.2 The unbounded vertical faces retain every clock

When \(2C\) is present, the bounded-\(q\) part of the return region is finite.
The only unbounded vertical supports are the four displayed in target (4.1).
For the three containing \(C\), the \(C=n+O(1)\), \(t=\tau/n\) phase limit is
the literal linear phase process in (4.3).  The alternatives after (4.5)
use only strong connectivity: either a stable phase has positive limiting
service, an unstable \(A\)-phase accumulates service quadratically, a direct
\(C\to0\) edge services, or the fast \(BC\)-exit services.  Thus one fixed
window has a strictly negative expected \(U\)-increment uniformly over the
finite \(q\)-phase.

The finite-\(n\) window is run with the full generator.  Reactions not
sourced at a \(C\)-order complex have integrated rate \(o(1)\); localization
exits have super-polynomial tails, and the total-population moment bound pays
their actual endpoints.  For the dormant support \(\{0,A,A+C\}\), the
leading \(AC/BC\) race includes every competing reaction.  At the sole phase
with no \(C\)-order source, an actual \(0\)-launch followed by an actual
\(AC\)-exit has a fixed chance of service; neutral trials are geometric, and
lower competitors occur with probability \(O(C^{-1})\).  Equations
(4.7)--(4.12) therefore give physical durations and actual-endpoint moments,
not a thinned-chain estimate.

Appending the outer return uses the same \(U\).  Its nonpositive expected
increment, squared-workload estimate, and higher-power bounds prove (5.4)
and (5.5): from every state the process reaches the moving core or a finite
set in finite mean physical time, with polynomial duration, workload,
and \(q\)-endpoint moments.

### 4.3 The \(U\)-to-\(q\) handoff is proved, not assumed

The core coordinate is

\[
                             q=A+2B.
\]

It is not proper on the full lattice because it ignores \(C\), and the
fourteen-partner theorem does not claim otherwise.  It is proper on the
core

\[
 \mathcal K=\{A\le K\sqrt{q+1},\ C\le C_*\},
\]

because a \(q\)-sublevel bounds \(A,B\) and \(C\le C_*\).

The independently audited local Riccati input is

```text
f2b9a9196b0d6ca52d1c31d567fcfdffb364b7325ad089520a0cef7f3c027e38
    research_notes/two_active_rank_two_window_audit.md
```

and the underlying current phase note is

```text
6c7f4cced7ab5e5c01c712c44306994c932fb949789c6a8120d7660eb2f8fd03
    research_notes/two_active_promotion_phase.md
```

That input runs the full chain for physical time
\(T/\sqrt{N+1}\), gives a uniform strict \(q\)-decrement, controls the
number of \(q\)-changing reactions, and gives an exponential \(C\)-moment.
The current target does not stop there.  Its cleanup compares \(C\) with an
immigration--death process while \(B\asymp N\).  It includes the lower
sources, absorbs the only potentially linear \(A+C\to2C\) immigration into
the order-\(NC\) fast death, and proves (6.5).  Consequently the typical
cleanup has \(o(1)\) duration and \(q\)-cost.  On the complementary event,
the polynomial outer-return bound (5.5), arbitrarily high input moments, and
Hölder give \(o(1)\) duration, endpoint, and \(q\)-cost as well.

Thus the complete core episode starts in \(\mathcal K\), runs all clocks,
and ends in \(\mathcal K\cup F_V\) with the uniform drift, duration, and
second-moment bounds (6.6).  This is the charged handoff between \(U\) and
\(q\).  No switch toll is omitted: \(U\) forces and controls the return to
the core, while \(q\) is evaluated only at consecutive core endpoints.

Iteration of these core episodes gives finite expected episode count and
finite mean physical time to the finite set (7.1).  One ordinary physical
jump from that finite target, followed by the already proved return bound
for each of its finitely many successors, gives a finite mean positive
return.  Nonexplosion follows from the affine bound on positive total-mass
growth.  This proves the rank-two theorem on every fixed closed irreducible
class.

**Qualification.**  The theorem is a valid nested two-workload regenerative
proof.  It does not export one common \(W\) satisfying a local random-time
Foster inequality on arbitrary charts.  Any later composition which demands
such an interface must use a different theorem or reprove that stronger
property.

## 5. All-active-only 51-pair theorem

For a fixed pair, the whole-top linkage has two distinct vertices
\(T=\{y,z\}\).  A strong graph on two vertices contains both directions.
After aggregating parallel channels, a positive vector \(\theta\) can always
be chosen so that

\[
                    \kappa_{yz}\theta^y=\kappa_{zy}\theta^z.
\]

The single rate-adjusted entropy

\[
 V_\theta(x)=\sum_i\left[
 x_i\left(\log\frac{x_i}{\theta_i}-1\right)+\theta_i
 \right]
\]

is bounded below and proper.  Proposition 5.2 of the exact current
all-active shell note,

```text
b6b6388ccb4a58d1c63cc8108bdffd4e0955d6c40decfbf3d20361fb84f6b512
    research_notes/three_active_shell_gluing_gate.md
```

proves \(\mathcal LV_\theta\to-\infty\) on every selected feasible failed
all-active sequence.  The cofactor hypothesis exactly bounds the positive
discrete curvature of the reversible top at the other linkage's maximal
source scale, while a strong-orientation exit from the proper lower maximal
tier supplies a negative logarithmic factor.  The proof is rate- and
orientation-uniform in the required sense: constants may depend on the fixed
rates, but no edge beyond strong connectivity is prescribed.

On a passing descriptor, ordinary entropy has a top stochastic source with
a strict deterministic-tier exit.  The difference between ordinary entropy
and \(V_\theta\) is affine, so every reaction changes it by a bounded
constant.  That \(O(1)\) sourcewise correction cannot cancel the divergent
negative logarithmic exit.  If a descriptor is affine-infeasible, it cannot
occur in the fixed class.  Since the exact selector says every feasible
failure is three-active, this also covers every boundary sequence.

Hence every divergent sequence in a fixed class has a subsequence along
which \(\mathcal LV_\theta\to-\infty\).  A bad-sequence contradiction makes
\(\mathcal LV_\theta\le-1\) outside a finite classwise set.  Localized Dynkin
then gives finite mean *physical* hitting time.  There is no embedded or
thinned chain: the generator contains every physical clock, and the stopped
endpoint is the actual state at first entrance.  Binary molecularity gives
nonexplosion.  Taking one physical jump from the finite target and returning
from its finitely many successors supplies a finite mean positive return.

Thus the same proper \(V_\theta\) proves the theorem for every chart and
every closed irreducible class.  No duration or endpoint interface is left
implicit.

## 6. Promotion-only 36-pair theorem

### 6.1 One common factorial-linear potential

For the eight seeded rows with no whole-top linkage, take \(\ell=0\).  Every
other selected network has one reversible two-complex whole-top linkage;
choose the fixed correction by

\[
 \ell\mathbin\cdot(z-y)=\log\frac{\kappa_{zy}}{\kappa_{yz}}.
\]

After adding a constant,

\[
 \mathcal F_\ell(x)=\sum_i\log(x_i!)+\ell\mathbin\cdot x
\]

is nonnegative and proper: factorial growth dominates every fixed linear
correction.  The correction is network-dependent but neither state- nor
chart-dependent.  It preserves every strict tier gap and is therefore the
same potential on ordinary passing cones and at every episode endpoint.

### 6.2 Twenty enabled-seed episodes

On a seeded failed sequence, exact tier equivalence makes every top-source
monomial comparable with one scale \(N\to\infty\).  From an enabled top seed,
strong connectivity supplies a simple physical path to the first exit from
the proper top block.  Each target creates the next source, including the
inactive cofactor.  Every prescribed rate is at least \(cN\), every
top-source competitor is at most \(CN\), and every lower-source competitor
has rate \(O(1)\).  Stopping at the first competitor retains all clocks.

The path succeeds with fixed positive probability and its last edge has
factorial reward \(-\log N+O(1)\).  Top competitors have bounded corrected
factorial cost; a lower competitor has probability \(O(N^{-1})\), and
\(u\log^+(v/u)\le v/e\) also covers an arbitrarily slow refined separation.
Thus the actual endpoint has the needed moments,
\(\mathbb E\Delta\mathcal F_\ell\to-\infty\), and every physical-duration
moment is \(O(N^{-m})\).  No preferred orientation or deleted clock enters
this argument.

### 6.3 Sixteen dormant episodes

The current dormant audit is

```text
d342db13f800a08a8f84a81bac86c92481876a010cca043ea7cdc0adca8a6dc8
    research_notes/dormant_promotion_priority_macrochain_audit.md
```

and the common corrected-factorial endpoint input is supported by

```text
af5516b5169047b0de069a5a49b8986875cc40926e1bf92d0d4abd2bbd35b110
    research_notes/rank_one_multichannel_carrier.md
4aa0297c6236eb80d565e2bdf76289ec23e34d79b137c3d484880a988230a615
    research_notes/rank_one_corrected_factorial_endpoint.md
```

The unequal scales in the \(\{B,2A\}\) shell are treated explicitly.  When
\(A\) is a proper-linkage source it is used before the order-one \(0\)-clock;
when \(BC\) is enabled, its order-\(N^2\) reaction has priority over the
order-\(N\) lower clocks.  Those lower clocks are retained as physical
interruptions, with probability \(O(N^{-1})\), rather than suppressed.

In both shell templates, the reflected debt is bounded by two.  Contracting
only the conservative whole-shell motion gives a finite priority macrochain.
If a service-free macroclass were closed, its underlying source vertices
would form a proper closed subset of the strongly connected proper linkage,
contradicting the presence of \(2C\).  Therefore a surplus exit has fixed
positive probability within a fixed number of macrotransitions for every
strong orientation and positive rate vector.  The resulting workload drift
is strictly negative.

Every physical wait remains in the block.  Constant-rate launches have
fixed exponential moments, \(A\)-windows and equal-scale exits have
order-\(N^{-1}\) duration, and \(BC\)-priority exits have order-\(N^{-2}\)
duration.  Internal equal-scale proper reactions have a uniform geometric
count.  Whole-shell endpoint estimates, the fixed transition cap, and the
corrected-factorial lift turn the workload service into

\[
                 \mathbb E\Delta\mathcal F_\ell
                    \le-c\log N+O(1).
\]

Interior exits are super-polynomially rare, and retained priority
interruptions cost only \(O(\log N/N)\).  The two disabled rows cannot be
divergent in one fixed class because the only active whole shell preserves a
fixed finite workload level.

### 6.4 Uniform fixed-class return

The exact selector gives each of the 36 pairs one feasible failed descriptor.
Along every passing divergent sequence the generator drift of the same
\(\mathcal F_\ell\) tends to \(-\infty\); along the failed sequence one fixed
physical episode has drift tending to \(-\infty\), physical-duration
moments, and actual-endpoint integrability.  If the set of states admitting
neither a common generator inequality nor a common episode inequality were
infinite, an escaping bad sequence and a proper tier subsequence would
contradict one of those two conclusions.  Hence one uniform inequality holds
outside a finite classwise set.

The exact common-entropy gluing input is

```text
7550c81b6a2a3085a34deaa9654517b7b00bb46bbd9e76898ee2220f6d53d194
    research_notes/physical_entropy_gluing_lemma.md
```

It records a target hit occurring inside an episode immediately, completes
that one episode only for drift accounting, and pays actual physical time.
It therefore gives finite mean hitting of the finite target.  Binary
nonexplosion and the one-jump finite-return trace then give positive
recurrence of every state in the fixed irreducible class.

## 7. Render and final disposition

Each exact target was independently converted from Markdown with
single-backslash TeX math and compiled with Tectonic:

```text
rank_two_global_return_all14.md          10 pages
all_active_only_reversible_top.md         3 pages
two_active_promotion_36_pair_theorem.md   8 pages
```

There was no missing character, invalid tag, undefined control sequence, or
TeX error.  The consolidated result is therefore **STRICT PASS / STRICT
PASS / STRICT PASS** at the separate 14-, 51-, and 36-pair scopes, with the
rank-two two-workload qualification stated above.  This audit does not
certify their union with any other two-linkage branch and does not assert the
full global \((\mathrm{T3})\text{--}(2)\) theorem.
