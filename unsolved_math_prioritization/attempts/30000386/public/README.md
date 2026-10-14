# Time Bomb conjecture partial results

**Status: UNSOLVED after five shared research passes, as of 14 October 2026.**
This package contains authored proofs of restricted results, exact reductions,
scoped counterexamples to proposed methods, and independent mathematical audits.
It contains no proof or disproof of the unrestricted two-dimensional speed-one
Time-Bomb conjecture. No novelty claim or exhaustive claim about the current
literature is made.

## Start here

1. [Game rules](CONSTRUCTION_CONTRACT.md) and
   [source acceptance contract](TIME_BOMB_ACCEPTANCE_CONTRACT.md).
2. [Accepted results index](RESULTS_INDEX.md), with proof and audit links.
3. [Exact unresolved obligation](STATUS_AND_REMAINING_GAP.md).
4. [Reproducibility and check limitations](REPRODUCIBILITY.md).
5. [Public source scope and identifiers](SOURCES.md).

## Main positive results

- **Infinite online safety with maximum announcement lead 16.** From empty
  history, one strategy avoids every adaptive announcement with effective lead
  at most sixteen. Read the self-contained
  [exact two-move invariant proof](pass4_devil/EXACT_TWO_MOVE_INVARIANT.md)
  and its [independent audit](pass4_survival/TWO_MOVE_INVARIANT_INDEPENDENT_AUDIT.md).
  The [chronology-triggered rescue proof](pass4_invariant/LEAD16_RESCUE.md)
  gives another construction of the same bounded-lead result.
- **Lead-16 bounded tracking.** A controller avoids those short bombs while
  staying within Euclidean distance 80 of any successively supplied reference
  starting at the origin and moving at speed at most 1/100. Read the
  [canonical corrected proof](pass4_invariant/LEAD16_BOUNDED_TRACKING.md)
  and [acceptance](pass4_survival/LEAD16_TRACKER_INDEPENDENT_AUDIT.md).
- **A genuine mixed short/distant theorem.** The tracker combines with fresh
  reference blocks to handle arbitrary mixtures of lead-at-most-16 bombs and
  bombs satisfying the explicit distant-target restriction. The original
  [mixed-lead proof](pass3_independent/MIXED_LEAD_COROLLARY.md) has short cutoff
  fifteen; Section 5 of the lead-16 tracker and its audit extend that cutoff
  to sixteen without changing the distant condition. The long-hit bound is
  strictly below 25921/30000. Intermediate leads remain excluded.
- **Four arbitrary known allowed detonation times.** For any prescribed four
  positive times, an online strategy survives every adaptive announcement
  restricted to them. The [proof](pass3_deadlines/FOUR_DEADLINES.md) combines
  analytic parameter coverage with 180 exact rational cases; the
  [independent acceptance and replay](pass3_devil/FOUR_DEADLINES_INDEPENDENT_AUDIT.md)
  verifies that finite proof component. This is not induction over arbitrary
  finite time sets.

Other accepted outcomes include survival through move 17 in the unrestricted
game; sparse prescribed deadline schedules; terminal-only weighted reserves;
exact finite arenas and compactness; restricted-policy defeats; and the
structural envelopes and composition obstructions indexed below.

## What remains missing

For every finite maximum lead H, it would suffice to construct a complete-state
family containing the genuine empty initial state and closed under one safe
Angel move followed by every legal Devil reply. H-dependent strategies need not
agree. Neither this all-H initial membership plus invariant, nor a legal
Devil forcing certificate rooted at the empty state, is supplied. Conditional
criteria and losing preloads do not settle that alternative.

## How to read preserved evidence

The `pass1` through `pass5` directory prefixes label research iterations, not
independent solutions. Most evidence files are preserved byte-for-byte.
Historical labels such as “candidate” or “submitted for audit” remain in those
originals; the linked acceptance documents and this index state their accepted
scope. Earlier statements that a particular construction does not handle three
or four deadlines describe that construction at that stage, not the strongest
later restricted result in this package.

[ORIGINAL_IDENTITIES.json](ORIGINAL_IDENTITIES.json) records original and public
file hashes and identifies the few public adaptations.
[MANIFEST.json](MANIFEST.json) binds the delivered public files. The newly
written public rules document is explicitly different from the historical
contract whose hash appears in preserved proofs. Package-root references in
original audit prose are resolved by the paths in the index and manifest.

Only authored mathematics, audits, checkers, certificates, and public source
metadata are included. The archive contains this public package alone.
