# Research log

## 2026-07-24 09:29 PDT

- Created this isolated lane to test structured phase constructions against
  the five exact shell-two profile orbits.
- Selected four distinct bounded families: a quadratic `C3` residue law, a
  separable `C4` CRT law, an antipodal `C6` template, and a multiaffine
  cocyclic/Fourier law.
- Derived each first-digit restriction as an affine system over `F_3`.
- Preliminary exhaustive run:
  - two profile orbits fail every family at the first digit;
  - the other three leave 729, 9, 19,683, and 59,049 distinct placements per
    profile in the four respective families;
  - no retained point passes the second placement digit;
  - strongest near-misses pass 19 of the 20 displayed rows.
- Peak resident memory stayed far below 1 GB.  No external communication,
  commit, or push was performed.

## 2026-07-24 10:08 PDT

- Audited the July 2026 fixed-common-multiplier result against every
  structured point, using the five minimal proper supergroups of `<10>`
  (stable IDs 8, 11, 12, 13, 14).
- Found that every first-digit survivor of the four initial low-period
  families is automatically fixed by the already-excluded ID-8 group.
  Reclassified these families as calibration controls.
- Added three opposite-class-twisted families that deliberately escape
  fixed `j -> j+6` symmetry.
- Exhausted the new families:
  - planar-quadratic envelope: 5,103 digit-one points, 2,916 outside all
    five supergroups, no digit-two point;
  - opposite-twisted C6: 177,147 digit-one points, 174,960 outside all five
    supergroups, no digit-two point;
  - opposite-helical C4: 178,605 digit-one points, 1,458 outside all five
    supergroups, one digit-two point.
- Replayed the unique digit-two point.  It is ID-8 fixed and fails six
  displayed rows at digit three.

## 2026-07-24 10:24 PDT

- Reconstructed the two six-dimensional central modules of the certified
  `F_27 x F_27` class-operator algebra.
- Enumerated and verified all 28 minimal three-dimensional invariant
  submodules in each central component.
- Tested all `56^2=3,136` channel-asymmetric submodule choices on every
  shell-two profile.
- Exactly 436 distinct placements pass digit one, six lie outside every
  excluded proper supergroup, and none passes digit two.
- Pinned both semantic hashes and added a combined theorem statement.
- No external contact, commit, or push was performed.
