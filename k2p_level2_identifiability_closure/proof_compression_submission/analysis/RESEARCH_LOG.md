# Proof-compression research log

## 2026-08-21 — PC-PARTIAL baseline and first direct compression checkpoint

- Bound the work to the immutable principal-
  \(\mathcal D_+\) release lock with file SHA-256
  `0c17eeaa3344f0982998ea694c1eb92f72f5ced0841e2acad0d39566e2ec71c3`
  and semantic payload
  `0e146ccee2352b80a5ceb605ff7aaa612ed28fd3122744b056c891d1e2ed2690`.
- Derived the conservative proof-surface census and separated theorem-facing
  code from independent consumers, mutation code, and release/hash machinery.
- Parsed the locked primitive `CORES` literal and independently enumerated
  every directed completion-record key.  Verified exact target counts
  \(289,831,1983,4155\) and Cartesian raw universes of
  \(405{,}216\), \(2{,}946{,}240\), and \(13{,}440\) rows.
- Recorded an important boundary: uniqueness is for completion
  records/presentations, not distinct graphs.  A repair choice can leave an
  already occupied arc unchanged, so graph-level deduplication is invalid.
- Compressed 839 raw4, 96 theta2, 54 cycle, and 6 restoration quadratic
  classes into 8, 4, 6, and 5 literal bodies respectively.  Every assignment
  retains enough residual data to reconstruct its exact frozen certificate.
- Preserved all 27 direction-specific direct-36 polynomial bodies within the
  three proposition-level families.  Source-1 classes 24 and 38 remain the two
  zero-source quintic orbit rows and are excluded from the 36 separators.
- Preserved the full-map \(T_i\) direction bit: raw4 is source-sign/target-zero,
  theta2 is source-zero/target-sign, and all 614 restoration sign leaves retain
  their mixed zero side, signed side, orientation, triple, and pullback hashes.
- The independent consumer verified all 369 transitively locked evidence
  hashes, every raw Cartesian coordinate, reversible template expansion, all
  997 restoration parents / 2,540 member roots / 36,824 forest edges, and the
  32-by-8 continuation branching census.
- Adversarial correction during verification: a separated first-level forest
  leaf may retain dummy roles that no longer need restoration.  Only a
  continuation row must carry exactly one remaining role; every second-level
  terminal has none.  The verifier now follows the exact frozen semantics.

Checkpoint completion: **100%** of the requested PC-PARTIAL baseline,
finite-universe completeness, direct-template table, and first equivalence
verifier.  Best-guess completion toward a fully compressed referee-facing
proof program: **42%**.  Higher restoration/probe archetype compression and
manuscript integration remain deliberately unopened.

## 2026-08-24 — atlas-scope rebinding

- Rebound the weak-sharpness column crosswalk to the hardened current atlas
  and independently recomputed both descriptors, named columns, and exact
  nine-by-nine determinants.  All 15 targeted mutations remain rejected.
- Replaced the primitive-count analyzer's redundant whole-atlas input binding
  with the exact `CORES`-literal semantic fingerprint
  `d5e7608f70a2243df605dee6e35d0ea6af74e4e47b42142e91ddfa4cbcbad09b`.
  The immutable theorem release still binds every compiler byte separately;
  this narrower binding states the dependency actually used by the count.
- No weak-sharpness coordinate, determinant, completion count, classification,
  or finite census changed.
- The baseline/equivalence artifacts will be regenerated once the parent
  final-release lock is sealed, because their purpose is to inventory that
  complete transitive lock rather than an intermediate working tree.
