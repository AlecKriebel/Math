# Research log: exact dense-shell `h=0` profile

## 24 July 2026

- The production prefix `h0-p00-p00` stopped after finding an exact-zero
  profile.  The raw candidate record was preserved by the fail-safe
  candidate path rather than being mislabeled as a completed exclusion.
- Archived the minimal profile certificate:

  ```text
  A = 1,1,2,4,4,5,1,1,2,4,4,5
  B = 5,5,1,7,4,1,5,5,1,7,4,1
  target = (2,-2,-4,-2)
  production digest = 0x81065cf5084f39f1.
  ```

- Wrote a dependency-free verifier with no production-classifier imports.
  It reconstructs the profile alphabet and cyclotomic geometry, expands both
  words to all 37 physical positions, recomputes every exact correlation,
  and verifies `D_0=167` and all 36 nonzero `D_t=0`.
- Independently verified shell counts `(0,18,6)`, canonicality, stabilizer
  order 2, orbit size 12, the production digest, and semantic hashes for the
  core certificate, full orbit, and full physical replay.
- First lift audit: 54 placement trits, 39 displayed physical upper
  coordinates, affine rank 18, nullity 36, consistent.
- Exact row-margin transfer: 64 compatible signatures, 72 compatible catalog
  rows, and `297,203,044,612,626,864,000` root-character assignments.
- A separate bounded exact endpoint pilot on row 17 used one worker, stayed
  below 160 MB RSS, and returned `UNKNOWN`.  This is recorded only as a
  scope/cost measurement; it is not evidence for or against a lift.
- The profile half-turn stabilizer is not imposed on labelled words.  The
  physical lift must retain independent placement variables across the two
  halves.
- No labelled `LP(333)` and no `H(668)` is claimed.  No external
  communication, commit, push, or further search occurred during archival.
