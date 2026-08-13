# Exact common-potential split inside the hard 333 family

## Scope

This note freezes the pair-level composition that would become available if
the repaired dormant/generalized local resolvent passes independent audit.
It makes no analytic or recurrence claim.

The hard family contains 333 pairs: 299 positive-invariant and 34 signed.
Exactly 317 of them admit one corrected-factorial fourth power across every
failed dimension.  The remaining sixteen require an all-active linear
workload switch.

## The common-\(W\) 317

The 317-pair subset contains 283 positive and all 34 signed pairs. Its failed
incidences split as

| active coordinates | incidences |
|---:|---:|
| 1 | 1,054 |
| 2 | 646 |
| 3 | 90 |

The two-active rows comprise 391 repaired dormant rows, 177 enabled access
words, and 78 closed rank-one shells. The all-active rows comprise 66 safe
reversible two-node incidences and 24 directed-triple incidences. Whenever a
pair has both a closed rank-one two-active top and an all-active top, their
top masks agree exactly.

Consequently the pair-fixed correction menu is

| correction | pairs |
|---|---:|
| arbitrary fixed \(\ell\) | 287 |
| reversible-top adjusted \(\ell\) | 22 |
| directed-triple adjusted \(\ell\) | 8 |

The repaired hard kernel is stated for arbitrary fixed \(\ell\), so it can
use whichever one of these corrections the other dimensions require. This
is a compatibility statement only; it becomes a recurrence proof only after
the repaired local theorem passes independent audit and the marked
fixed-class gluing is replayed at this exact 317-pair scope.

### Candidate fixed-class composition

Fix one of the 317 pairs, one strong orientation and positive rate vector,
and one closed irreducible class \(\Gamma\). Choose the pair-fixed
correction from the preceding table and put

\[
 G_\ell(x)=K_\ell+\sum_i\log(x_i!)+\ell\mathbin\cdot x,
 \qquad W_\ell=G_\ell^4,
\]

with \(K_\ell\) large enough that \(G_\ell\ge1\). The intended exhaustive
local routing is:

1. the 1,054 one-active incidences use the generalized/hard resolvent and
   its exact one-active-to-two-active handoff;
2. among the 646 two-active incidences, the 391 dormant rows use the hard
   resolvent, the 177 enabled rows use the bounded top-tier access word, and
   the 78 closed rank-one rows use the powered shell endpoint theorem;
3. the 66 safe reversible all-active incidences use the powered paired-top
   estimate, while the 24 directed-triple incidences use the powered
   factorial-linear estimate; and
4. every actual-orientation passing descriptor uses the quantitative
   powered descending-source generator estimate.

The correction is genuinely common. In every overlap between a closed
two-active shell and an all-active shell, the frozen top mask is identical.
The reversible and directed-triple endpoint theorems allow exactly the
correction chosen above, while the hard resolvent allows an arbitrary fixed
\(\ell\).

To obtain a pair theorem, mark all three species by reflected debts on the
reachable lift of \(\Gamma\). In a fixed-width bad tube, zero selected debt
makes the active population class-dependently bounded, hence contributes
only a finite exception. Every divergent reachable bad-tube sequence with
positive debt has one of the stopped episodes above. Moving-boundary jumps
and their endpoint \(W_\ell\)-costs are included in the originating
episode; the next rule starts at the same physical state, so the common
potential telescopes without a comparison inequality. The usual
bad-sequence extraction then reduces the complement to a finite union of
generator-good and episode-good sets. The all-debt physical-time gluing
theorem would yield finite mean return to a finite marked target, and hence
positive recurrence of \(\Gamma\). Binary mass action is nonexplosive by
the standard linear bound on population-increasing clocks.

This paragraph is a **candidate dependency-complete proof**, not a promoted
theorem. It requires a fresh independent PASS for the repaired hard
resolvent and for this exact 317-pair gluing replay.

## The remaining sixteen switches

The complement consists of twelve all-active curvature-seam pairs using the
rate-dependent workload \(H_b\), and four all-active rank-two pairs using
\(H_w\). They are disjoint and all sixteen are positive-invariant. The local
hard kernel uses factorial \(W\), so these pairs still require a genuine
scalarization or stopped workload-transfer theorem; support compatibility
alone is insufficient.

The separate final-seven theorem is now independently audited and certified.
A prospective 317-pair theorem would therefore leave exactly sixteen
positive pairs and no signed pairs. All hard-branch flags remain false.

The exact fingerprints are

| object | SHA-256 |
|---|---|
| common 317 pairs | `bc9d5ddd17f703b664b411f955dd6ae3b059729971428f922a40654fd6fd19e0` |
| switch 16 pairs | `35aa9260eedf3305abf6ec72704beec44394ecaa851ce7dc045e4d3c899d9896` |
| remaining 16 pairs | `35aa9260eedf3305abf6ec72704beec44394ecaa851ce7dc045e4d3c899d9896` |
| canonical 317 rows | `4cfe4964216dbec70989d6d4413161e170c9c0e8e8a54592c39d8c58dc7030aa` |
| certificate payload | `6ac4ef091ef771d377fb33e050fac9444236effe85c2838e11f48173d180ef75` |

## Reproduction

```text
PYTHONPATH=src python3 -B src/hard333_pair_composition.py
PYTHONPATH=src python3 -B -m unittest \
  tests/test_hard333_pair_composition.py -v
```
