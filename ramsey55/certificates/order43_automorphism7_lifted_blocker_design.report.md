# Selector-lifted certificate design for the order-7 pair quotient

Evidence status: **TWELVE-SAMPLE TRANSFORMATION CERTIFIED; FULL 37,194-PAIR
DESIGN AUDITED BUT FROZEN**

This report concerns only the normalized order-43 automorphism type
\(7^6 1^1\).  No full order-7 proof was launched, and nothing here changes
the public bounds on \(R(5,5)\).

## The lifting transformation

Let \(B\) be the 273,696-clause global orbit CNF together with the six units
that normalize the fixed vertex to see the first three moved cycles.  A pair
representative adds a 60-literal side cube

\[
C=c_1\wedge\cdots\wedge c_{60}.
\]

Introduce a fresh selector \(s\) with the exact definition

\[
(\neg s\vee c_j)\quad(1\le j\le60),\qquad
(s\vee\neg c_1\vee\cdots\vee\neg c_{60}).
\]

Given a DRUP proof of \(B\wedge C\vdash\bot\), discard its deletion records
and replace every learned clause \(D\) by \(D\vee\neg s\).  The final empty
clause becomes \(\neg s\).  This guarded derivation is sound because assuming
\(s\) propagates every literal of \(C\).

The temporary \(\neg s\) and the reverse selector definition make the
ordinary cube blocker

\[
\neg C=\neg c_1\vee\cdots\vee\neg c_{60}
\]

RUP.  The stream then deletes every temporary guarded learned clause,
including that first copy of \(\neg s\).  It rederives \(\neg s\) from the
retained blocker and the implications \(s\to c_j\).  This last step ensures
that a subsequent selector-cover contradiction genuinely depends on the
blocking clause rather than bypassing it through the temporary derivation.

For selectors \(s_1,\ldots,s_k\), the input clause
\(s_1\vee\cdots\vee s_k\) asserts that at least one covered cube holds.
After the stream derives every blocker and rederives every \(\neg s_i\), the
cover clause unit-propagates to contradiction.

## Certified test on the existing twelve samples

The preregistered test regenerated exactly the same twelve Glucose3 proofs
used in the earlier evenly spaced proof-size sample.  Every cube-formula hash,
raw proof hash, byte count, and record count matched the earlier result.

The raw proofs contained 3,198,756 records.  Of these, 3,178,562 were solver
deletion records and only 20,194 were learned additions.  Removing the
irrelevant deletions and applying selector lifting produced one 1,353,389-byte
DRAT stream.  It contains twelve exact blockers, cleans every temporary
guarded derivation, rederives all twelve selector refutations from those
blockers, and closes one exact twelve-selector cover clause.

| artifact | raw bytes | zstd-19 bytes | SHA-256 |
|---|---:|---:|---|
| sample wrapper CNF | 10,288,816 | — | `e5b3d592effc4d27fe85357c2179da312e645c0d8d5d57b234d9bd093338bdd7` |
| lifted DRAT | 1,353,389 | 222,872 | `21f45915e7bbb84c1bf93292c7aee014947d8e603695edd4a63e50a4a0be413f` |
| lifted DRAT, zstd-19 | — | 222,872 | `aac8ef9ed41ed465a8d42a05b65a038126dd609ccbdf401f75b75782d8b34f71` |
| converted LRAT | 8,345,121 | 1,190,987 | `07bd1eadbcfe5c0a19984905449d34bf63334ef78b96ff90b96102c0cfecb264` |
| converted LRAT, zstd-19 | — | 1,190,987 | `725b593fba84b52bbf6f0bdd8b501dca17b04364901ae3ff7986a1e7b1b6cd29` |

`drat-trim` accepted the lifted stream and converted it to LRAT.
`lrat-check` accepted that LRAT.  A separate checker then:

1. rebuilt the 274,435-clause, 141-variable wrapper byte for byte;
2. checked the exact byte range and SHA-256 of every lifted segment;
3. checked that each segment consists of guarded additions, the exact
   60-literal blocker, exact guarded-clause deletions, and blocker-dependent
   selector rederivation;
4. decompressed both zstd artifacts and matched the raw files;
5. reran `drat-trim`, regenerated the identical LRAT byte for byte, and reran
   `lrat-check`.

The independent result reports `valid: true`.  The sample result SHA-256 is
`2961f48127ce5628d69d15b0d586ccefb34f1b0480329fa1abb2446350ab6382`;
the independent check SHA-256 is
`72be0d62ed38a4aba6d8b3b087894ab38e2e02fe40280b24f2b6eb395f6870a5`.

This certifies only the disjunction of the twelve sampled cubes.

## Full exact-cover architecture

A global certificate needs more than 37,194 cube proofs.  It must also certify
that the quotient really covers every possible side pair.  The present model
enumeration is exact as a computation but proof-free, so treating its
191,394-model count as an axiom would leave a logical gap.

The frozen design closes that gap in four independently checkable stages:

1. Reconstruct the 30-variable, 3,618-clause side formula \(S\).  Retain the
   191,394 listed assignments and directly check that every one satisfies
   \(S\).
2. Form \(S\) plus the 30-literal blocking clause of every listed assignment
   and certify this formula UNSAT through DRAT-to-LRAT.  This proves that no
   additional side model exists.
3. Partition that now-certified model list under the 294 independent
   shift/block actions, then partition class pairs under the common
   multiplier and the color-complementing side swap.  Independently recheck
   every global formula and fixed-unit symmetry.  This yields the exact
   37,194-representative schedule.
4. Certify 128 pair-index shards.  Each shard wrapper contains selector
   definitions for exactly its schedule subset and one selector-cover clause.
   Checked UNSAT of all shard wrappers eliminates every representative; the
   certified finite quotient then lifts the conclusion to the normalized
   order-7 branch.

The prospective monolithic wrapper has 37,323 variables, 2,542,537 clauses,
47,178,247 bytes, and SHA-256
`b04067d3bd3c1e4b68f88a29a4271695128afc8008c9f4768261f4266281dabd`.
It need not be retained.  Under the audited rule `pair_index mod 128`, each
shard contains 290 or 291 pairs; its deterministically regenerated wrapper is
at most 10,566,888 bytes and 291,454 clauses.

## Storage findings and gates

Average scaling of the twelve-sample artifacts to all 37,194 representatives
gives:

| artifact | average-scaled bytes |
|---|---:|
| lifted DRAT, raw | 4,194,829,206 |
| lifted DRAT, zstd-19 | 690,791,764 |
| converted LRAT, raw | 25,865,702,540 |
| converted LRAT, zstd-19 | 3,691,464,207 |

The largest sampled raw lifted segment alone scales to 20,609,604,534 bytes.
Therefore a monolithic raw proof is not safe; streaming and sharding are
mandatory.

The materially new design retains only zstd-19 DRAT shards.  Verification
decompresses one shard at a time, converts it to LRAT, checks both formats,
then removes the transient raw proof files.  Its hard caps are:

- 2,147,483,648 bytes for all retained compressed pair-proof shards;
- 536,870,912 bytes for the certified exact-cover artifacts;
- 2,147,483,648 bytes maximum transient working storage;
- 4,294,967,296 bytes that must remain free.

The resulting prelaunch requirement is 9,126,805,504 bytes.  At the audit,
12,110,962,688 bytes were available, so the **storage subgate** passed.
Passing that subgate only bounds storage safety: it does not predict that
every proof fits the caps and does not authorize execution.

The earlier conservative LRAT-only gate remains unchanged and frozen at
20,317,547,392 required bytes.

## Why the full run remains frozen

The audited design reports `FROZEN_NOT_LAUNCH_READY`.  Three substantive
components do not yet exist:

- a checked side-model exhaustion LRAT;
- a hash-pinned full sharded runner and independent checker;
- one full-size 290/291-pair shard pilot proving that the hard transient caps
  are operationally realistic.

No unsampled pair was solved or certified in this work.

## Reproducibility

- sample plan SHA-256:
  `d37bb6f336898bda14c026e9d537adee44bea9ca11df9e67ec87c7bb15153e8b`
- lifting runner SHA-256:
  `3904c326936fb1a3662d4cde1c81db93c1ed309c0a0f0cc494c4d30229bd78fe`
- independent sample checker SHA-256:
  `db3982d14ccfa01f87fb546c246cb7a731625c126d5adc95b25c46fa00f91fed`
- unit tests SHA-256:
  `adeef0bd564e20d997e5ee61bd4c8458794693dd7f81574e15d3c60cdb646932`
  (3/3 passed)
- frozen full-design file SHA-256:
  `36bb3b19006df33086857daaac6ab693d6d63a1bb1d14eab2ebc9b13950c78c0`
- design audit SHA-256:
  `df320ee2c2d7daa338740b4f5dbe898e03ae160d48ea725111f0255deafd60b4`
- design-audit result SHA-256:
  `ecba883848d6f40760c84abbd01c599fd13646f63ca06f84e862bbb43ff3b589`
