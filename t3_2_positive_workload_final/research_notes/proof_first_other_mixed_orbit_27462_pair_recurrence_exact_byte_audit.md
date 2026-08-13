# Exact-byte audit of the 27,462-pair completed mixed-orbit theorem

**Independent proof-first hostile audit, 2026-08-12 PDT.**  The immutable
target is

~~~text
research_notes/proof_first_other_mixed_orbit_27462_pair_recurrence_theorem.md
SHA-256 a91e8c31f35312ef4b9063e8f5a48af534861145db2236e662ea6cc1eff8e30e
200 lines, 7856 bytes
~~~

The verdict is **STRICT PASS** at these exact bytes.  The target proves
nonexplosion and classwise positive recurrence for the exact 27,462-pair
symmetry orbit of the 5,059 analytically completed seeds.  It removes the 110
active-only-invariant seeds before orbit closure and never uses their invalid
all-active inference.

## 1. Independent finite-set replay

The target pins the finite certificate and test at

~~~text
src/other_mixed_orbit_27462_certificate.py
SHA-256 57d8904dd86cd0bf626e344dbfd7b7f248b239cdeaace48489796058c6875f08

tests/test_other_mixed_orbit_27462_certificate.py
SHA-256 e708c52f6cbc1bbc4dabf33f246d72379dff58c74cc97a38fdd8076ac3ae7d13
~~~

All five dedicated tests pass.  I also replayed the defining sets directly,
independently of the certificate's final payload.  The inherited union has
5,169 seeds, the active-only-invariant subset has 110, and subtraction leaves
5,059 eligible seeds.  The five analytic sets are pairwise disjoint, have
cardinalities

\[
                 187,\quad 974,\quad 9,\quad 1378,\quad 2511,
\]

and their union is exactly the eligible set.  The eligible fingerprint is

~~~text
c45f67990ff841e1ba7b7d5d8a2795539f495f2434d68135ad3b2483d2fda44f
~~~

and the branch-manifest fingerprint is

~~~text
22f10cf6ea09a7b36650df174a866fd15470c770b3da6079728cfe5301f61c76
~~~

The finite computation performs support, descriptor, and set identities
only.  It does not enumerate orientations, rates, population boxes, reaction
histories, or communicating classes.

## 2. The five seed-level analytic branches

### 2.1 Strictly positive invariant

For each of the 187 seeds, the support stoichiometric span has a vector
\(h>0\) in its annihilator.  Strong connectivity within each linkage makes
every possible labelled reaction vector lie in that same support span.
Consequently \(h\mathbin\cdot x\) is constant for every allowed orientation.
Its nonnegative-integer level set is finite, so every closed class is finite.

### 2.2 Full deficiency zero

The 974 networks are weakly reversible and have full-network deficiency
zero.  The deficiency-zero theorem gives a positive complex-balanced point
for every positive rate vector.  The stochastic product form restricted to
a closed class is normalizable because its mass is bounded by the full
product-Poisson sum.  With the independent nonexplosion argument in Section
5 below, this proves positive recurrence rather than merely a sigma-finite
stationary measure.

### 2.3 The nine literal physical seams

The branch contains exactly six new seven-support seeds, two new signed
service seeds, and one residual-pair seed.  The target pins the three
standalone arbitrary-orientation, physical-time proofs and the independent
scope audit

~~~text
research_notes/proof_first_exact_physical_seams_independent_audit.md
SHA-256 e7e76b76cd1371f98d19da0a1f5362ab4a0696548fba62028b29ccd2950617c9
~~~

That audit passes precisely the literal supports.  In particular, the target
does not promote signed service to support supersets.

### 2.4 The 1,378 corrected tier-pass seeds

There are exactly 259 support-independent tier descriptors.  I replayed all
\(1378\times259=356902\) seed--descriptor incidences: every incidence
satisfies the corrected S-tier-superlevel cut.  For a fixed descriptor the
cut theorem is exact: in some linkage, the nonempty proper D-superlevel at the
top-S level lies inside the top S-tier.  The first edge leaving that
superlevel in any strong orientation is therefore sourced in the top S-tier
and is D-descending.

Thus every escaping tier sequence meets the Anderson--Kim descending-source
hypothesis.  If the entropy generator failed to be uniformly negative
outside a finite subset of a closed class, properness would supply an
escaping bad sequence in that class.  Tier extraction and the descending
source force its entropy drift to minus infinity, a contradiction.  This is
a statewise generator argument; it contains no chart-exit or weighted-seam
composition.

### 2.5 The 2,511-pair residual union

The target pins the publication-safe union certificate

~~~text
src/corrected_t3_2_two_linkage_union.py
SHA-256 501d96c4cea2de33ed34db2c31702d3104e8ed80c1abb8cf15e895c56201593f
~~~

Its exact dependency verification rehashes both theorem and audit bytes for
all fourteen analytic branches.  Those fourteen pair scopes are disjoint and
their union is the exact corrected 2,511-pair residual, with fingerprint

~~~text
0c57f530eb44a688520cc1706f830afa18063f4d08d24e5006f47a5666edd0b3
~~~

Every dependency is a standalone fixed-support recurrence theorem.  Since a
network's support pair is fixed once and for all, this finite union does not
switch potentials or splice local episodes along a trajectory.

## 3. Symmetry transfer and the active-invariant boundary

I independently reconstructed the orbit using all six species permutations
and linkage reversal.  The eligible orbit has 27,462 distinct ordered pairs
and fingerprint

~~~text
1bf337cf143c6eb4cee5088827bb9e9b9cec704f01a1b1f57bde6aed856d2812
~~~

The active-only-invariant seed orbit has 714 pairs.  Its intersection with
the eligible orbit has 282 pairs, and its complement relative to the eligible
orbit has exactly 432 pairs.  Hence the eligible orbit is disjoint from the
exclusive 432-pair gap.

There is no overreach at the 282 overlap points.  Membership in the eligible
orbit supplies an eligible seed and an explicit symmetry carrying that seed
to the pair.  A species permutation bijects population states, carries each
closed irreducible class to a closed irreducible class, relabels arbitrary
positive rates, and intertwines the two generators.  Linkage reversal changes
only the ordering of two components of the same network.  Positive recurrence
therefore transfers from the eligible seed theorem.  The active-only
invariant representation is unused.

## 4. Exhaustion of the eligible seeds

The five branch predicates are applied at seed level before any orbit is
taken.  Their disjoint union is the complete 5,059-seed eligible set, so every
pair in the 27,462 orbit has at least one completed analytic preimage.  The
argument needs no uniqueness of that preimage and is unaffected by overlaps
among symmetry images.  Conversely, no point of the exclusive 432-pair gap
has such a preimage, and the theorem expressly makes no claim for it.

## 5. Nonexplosion and verdict

In a binary network, a degree-two source cannot have a target of larger total
molecularity.  Every population-increasing reaction therefore has source
degree at most one, bounded jump size, and total increasing rate
\(O(1+|x|_1)\).  Linear pure-birth comparison prevents population escape in
finite time.  On each bounded-population set there are finitely many states
and bounded total rates, so population-neutral quadratic reactions cannot
accumulate there.  This proves nonexplosion for every branch and every
symmetry image.

The exact target at SHA \(a91e8c31\ldots\) is therefore a strict pairwise
proof of nonexplosion and positive recurrence on every closed irreducible
population class for precisely the 27,462 completed mixed-orbit pairs.  It
does not use finite search as stochastic proof and does not claim the
separately repaired 432-pair orbit gap.
