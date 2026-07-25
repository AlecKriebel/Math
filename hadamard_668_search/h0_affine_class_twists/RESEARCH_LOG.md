# Research log

## 2026-07-24 16:11 PDT

- Introduced affine-in-class pairings
  `q -> epsilon*q+a*j+b` independently in the two binary channels.
- Classified all `18^2=324` paired families at the exact first placement
  digit.
- Found 161 inconsistent systems, 162 affine dimension-nine systems, and
  only the identity/identity system at dimension 21.
- Exhausted `162*3^9=3,188,646` assignments through the complete second
  placement digit.  There were zero survivors.
- Split off the 288 cases with at least one nonzero class slope: 144 are
  first-digit inconsistent and 144 fail completely at digit two.
- Peak memory in the discovery run was about 26 MB and elapsed time about
  14 seconds on the local Apple M1 Pro.
- This is a structured-family obstruction only.  No `LP(333)` or `H(668)`
  is claimed.

## 2026-07-24 16:35 PDT

- Extended the shift `a*j+b` to an arbitrary function of `j mod 3`,
  equivalently a quadratic polynomial over `F_3`.
- Classified all `54^2=2,916` paired families.
- Exhausted all 1,458 generic dimension-nine systems through digit two:
  zero survivors among `28,697,814` points.
- Found one dimension-15 exception.  Its six zero-polar combinations have
  affine rank six, reducing it to `3^9` points; none survives digit two.
- Found two nonidentity dimension-21 exceptions.  The same six hidden
  affine equations reduce each to dimension 15.  Exact three-block
  enumeration of `2*3^15=28,697,814` points gives 24 digit-two survivors
  in each family.
- Replayed all 48 survivors exactly.  None reaches digit three and none
  lies in the 1,756-word exact row-margin catalog.
- Therefore all 2,915 nonidentity families in the quadratic-class
  extension are locally excluded at digits one, two, or three.  The sole
  unclassified local control is the identity/identity order-six branch.
