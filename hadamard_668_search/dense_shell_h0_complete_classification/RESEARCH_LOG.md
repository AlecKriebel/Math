# Research log

## 2026-07-24 PDT — final \(h=0\) classification frozen

- Consumed the completed strict
  `dense-shell-production-aggregate-v2` result only as source material.
- Confirmed the aggregate reports all 729 prefix shards complete and 18
  distinct canonical exact-profile orbits.
- Built a compact certificate containing the 18 representatives, their
  production digests, source shards, targets, stabilizers, orbit sizes, and
  independent replay hashes.
- Froze the complete global counter vector and SHA-256 provenance for the
  aggregate, manifest, classifier source, and compiled binary.
- Wrote a dependency-free verifier that imports no production code and
  reads no ignored production output.
- Reconstructed the exact 24-element action as a faithful group action and
  verified its full multiplication table.
- Replayed all 666 physical correlations in integer Eisenstein arithmetic.
  Every representative has zero lag \((167,0)\) and 36 zero nontrivial
  correlations.
- Recomputed shell counts, target aggregates, canonicality, stabilizers,
  orbit sizes, production digests, orbit hashes, and physical replay hashes.
- Checked all 153 pairwise orbit comparisons: zero intersections.
- Found 12 size-24 orbits and six size-12 orbits.  Their total size 360
  exactly equals the frozen weighted exact-zero counter.
- Final verifier run: `PASS`, approximately 0.11 seconds wall time and
  22.2 MB maximum resident set size.

### Scope

This closes the exact compressed-profile classification for the enumerated
dense \(h=0\) shell.  It does not lift any representative to a labelled
\(LP(333)\) and does not construct \(H(668)\).
