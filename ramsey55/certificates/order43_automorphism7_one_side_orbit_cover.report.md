# One-side orbit cover for the order-7 automorphism branch

Evidence status: **EXACT FORMULA/ACTION REPLAY; PROOF-FREE MODEL ENUMERATION**

This report refines only the order-43 branch whose prescribed automorphism has
cycle structure \(7^6 1^1\). It does not cover arbitrary order-43 graphs.

After the fixed vertex is normalized to be adjacent to the first three
7-cycles, its 21-vertex neighborhood is described by a 30-variable side
formula: no four vertices induce a clique and no five vertices induce an
independent set. Direct reconstruction gives 843 negative clique signatures
and 2,775 positive independent-set signatures, hence 3,618 clauses.

## Complete one-side quotient

Proof-free CaDiCaL enumeration exhausts 191,394 distinct satisfying assignments
of the side formula. The standalone audit then checks the following actions
directly on variables and clauses:

1. Independent shifts of the three cycles modulo the trivial diagonal shift,
   together with all six block permutations, give 294 distinct actions.
   They partition the enumerated assignments into 664 orbits: 3 of size 49,
   21 of size 147, and 640 of size 294.
2. The six common nonzero offset multipliers modulo seven act on those 664
   classes. They yield 122 quotient orbits: 1 of size 1, 21 of size 3, and
   100 of size 6.
3. For each multiplier, the independently reconstructed global variable map is
   a bijection and maps the full set of 273,696 global clauses exactly onto
   itself, with zero missing or extra clauses.

Consequently, solving the global formula under the fixed-vertex units and one
representative neighborhood assignment from each of the 122 quotient orbits
is a symmetry-complete SAT search of this automorphism branch. The
nonneighbor-side and all cross-edge variables remain free in every cube.

- global CNF SHA-256:
  `8045d463f68d78a745e18bb02ccc7d49fa02b47176a7282b1ef6f436fb109eb1`
- metadata SHA-256:
  `04f18fdcf4d50bda27580e1653f99f423d9799ba1ddbf0e95b1683542e6b7a56`
- side formula SHA-256:
  `f59be7024c4b15cba7238da38d865a4f8ea8dd631ed5c096300054679cd65c96`
- standalone audit SHA-256:
  `b4531da9785fb98a668b3ea9876660f46500c47115f9aa582d19455081071543`
- audit result SHA-256:
  `cc60b19d2b955062d41061eb7d0f201e404eb2c082ce1a6490add500ad976e0b`

## Complete fixed-pair quotient

The two sides admit independent shift/block actions, but the nonzero offset
multiplier must act simultaneously on both sides. Global color complementation
combined with swapping the neighbor and nonneighbor sides reverses an ordered
pair while preserving the normalized fixed-vertex units.

A second standalone audit checks this rather than assuming it:

- the 664 side classes give 440,896 ordered or 220,780 unordered class pairs;
- quotienting unordered pairs by the diagonal six-element multiplier action
  gives exactly 37,194 representatives;
- eight generators for the independent side actions, a generator for the
  common multiplier, and the color-complementing side swap all map the full
  273,696-clause global formula exactly onto itself;
- all ten generators preserve the six fixed-vertex units;
- all 37,194 retained representatives pass a direct signed-unit check showing
  that the color-complementing side swap implements pair reversal under the
  convention that the second side model is complemented.

- pair schedule SHA-256:
  `cbcb78bd7c2b58669d2241eb109a0cfb9c5b61bb916a151d953ffdacf03cc1ae`
- pair audit SHA-256:
  `ebd5c3c02ac642e702d45d3f58b23aac97fbc93ad8792e0c877591b4809c3b37`
- pair audit result SHA-256:
  `cd29189badf8d01f8f02704c14ad9edb19c63bb96ac4b2402d51e5b03b975294`
- in-memory sweep runner SHA-256:
  `016ba250cea7d51e6b95b45c599514ccd25f904af2b8957599d1c2b57702ec72`

## Proof-free search outcomes

A symmetry-complete one-side pass fixed only the normalized vertex and one of
the 122 neighborhood representatives, leaving the second side and all cross
variables free. Every cube exhausted a 50,000-conflict CaDiCaL budget:

- 122 `BUDGET_EXHAUSTED`;
- zero SAT and zero solver-reported UNSAT;
- 6,100,097 observed conflicts in 314.479 seconds.

A subsequent fresh 5,000-conflict probe also exhausted the budget on all 122
cubes. Its residual-formula and decisions/propagations rankings were used only
as heuristics.

The stronger fixed-pair sweep then visited the complete 37,194-representative
schedule in two interleaved in-memory shards. Both shards completed without a
SAT result or a budget exhaustion:

| Shard | Visited | Observed UNSAT | Conflicts | Runtime |
|---|---:|---:|---:|---:|
| 0 of 2 | 18,597 | 18,597 | 16,860,975 | 1,225.022 s |
| 1 of 2 | 18,597 | 18,597 | 16,553,236 | 1,189.957 s |
| combined | 37,194 | 37,194 | 33,414,211 | — |

No full stdout transcript was retained because the sweep was deliberately
no-write under disk pressure. The hash-pinned runner and the exact aggregate
summary retain the schedule, sharding rule, final counts, and conflict totals.

- sweep summary SHA-256:
  `1e68fe4d91dc11359e58ef93edf199e299b6efe925d4013032768c5664792bb2`

This is complete construction-search coverage relative to the proof-free side
enumeration. It is not an UNSAT certificate for the automorphism class.

## Checked proof-size sample and full-bundle gate

A preregistered 12-pair sample took evenly spaced quantiles of the 37,194-pair
schedule, including both endpoints. Every sample solved UNSAT with Glucose3,
passed `drat-trim`, converted to LRAT, and passed `lrat-check`. Proofs and
formulas were transient; only their measurements and hashes were retained.

| Artifact | Median raw | Maximum raw | Median zstd-19 | Maximum zstd-19 |
|---|---:|---:|---:|---:|
| DRAT | 10,493,869 B | 10,841,327 B | 820,377 B | 912,752 B |
| LRAT | 2,137,858.5 B | 4,061,323 B | 129,564 B | 430,784 B |

Extrapolating the sampled compressed sizes to all 37,194 pairs gives:

- DRAT median projection: 30,513,102,138 bytes;
- LRAT median projection: 4,819,003,416 bytes;
- combined median projection: 35,353,510,701 bytes;
- combined maximum-sample projection: 49,971,477,984 bytes.

The projected full bundle is far beyond the current safe storage envelope, so
it was not launched.

- proof-size plan SHA-256:
  `1985867d2291f780120f22386d7c51920aa0412a545b272e36acc11b5121637e`
- proof-size result SHA-256:
  `816509592ffd17d293e571bf1a857bc7983706926d50168b4d93ed67b10631dc`

The same 12 proofs were then regenerated and checked for a preregistered
indexed-concatenation benchmark. Cross-proof compression barely changed DRAT
(9,936,804 individually compressed bytes versus 9,858,334 concatenated
bytes), but materially improved LRAT (1,806,339 versus 1,008,300 bytes).
Scaling the concatenated LRAT average gives a 3,125,225,850-byte estimate for
37,194 pairs.

The launch gate deliberately remains more conservative: it uses the largest
per-file compressed LRAT in the sample, projecting 16,022,580,096 retained
bytes, plus a 4,294,967,296-byte working reserve. The required prelaunch free
space is therefore 20,317,547,392 bytes. Only 12,266,602,496 bytes were free
at the benchmark launch, so the full LRAT-only run remains frozen.

The permitted retention policy, if that gate later passes, is LRAT-only:
delete each transient DRAT only after successful DRAT-to-LRAT conversion and
successful checks of both formats.

- concatenation plan SHA-256:
  `d802112df73aa38844ee91f98e4c80148c1b80de4fdc97e67ff8a43b00e4b1cc`
- concatenation result SHA-256:
  `f2aac44403c007fc7cef8d72f396e4eff857ef7aef06b3b60721f55285819a97`

## Claim boundary

The action sizes, orbit coverage relative to the enumerated model set, and
global clause-set invariance are exact replay checks. The count and exhaustion
of the 30-variable side models rely on a proof-free SAT solver run. No
DRAT/LRAT certificate accompanies that exhaustion.

Likewise, budgeted solves of the 122 global cubes are construction searches.
A dual-verified SAT model would be a valid order-43 construction. A timeout or
solver-reported negative result without proof is only a computational
observation and does not certify nonexistence, even if all 122 cubes are
visited.
