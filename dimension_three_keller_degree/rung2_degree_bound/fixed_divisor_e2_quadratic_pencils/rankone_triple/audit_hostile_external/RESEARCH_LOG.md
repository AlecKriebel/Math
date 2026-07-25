# External hostile-audit log

All timestamps are UTC.

## 2026-07-25T10:12:00Z — audit opened

- Restricted all new work to `audit_hostile_external/`.
- Began from the raw \(E_7\) coefficient system rather than imported
  matrices.
- Required every localized solve to display a pivot supported only on
  variables declared nonzero in that chart.

## 2026-07-25T10:21:00Z — effective gauge space and \(A=0\) cover

- Reconstructed raw rank \(8\), nullity \(18\), and the eighteen-vector
  kernel.
- Confirmed that the five named transformations span only four top-gauge
  directions because \(z\)-translation equals the second target-shear
  direction.
- Denominator-free \(E_6\) syzygies gave the exhaustive \(w_3\)-open,
  origin, \(xz\), and \(xy\) cover.

## 2026-07-25T10:27:00Z — hidden \(r=0\) pivot audited

- Found that the primary displayed \(E_4\) pivot on the
  \(w_3\ne0,D\ne0\) leaf carried \(r^4\), although the parametrization
  was asserted for \(r=0\).
- Rebuilt \(r=0\) before solving.  The new rank-four system has pivot
  \(-4096s^8/81\), and \(E_3\) forces the determinant factor to vanish.
- Found a second external monomial-order pivot \(4096s^8/81\), proving
  uniform completeness in \(r\).

## 2026-07-25T10:32:00Z — legal shear compensation corrected

- Verified the \(q\)-preserving shear has determinant one.
- Tracked its \(x^2\) residue exactly.
- Confirmed that the legal compensation is an \(x\)-translation plus
  relabeling of the free \(V\)-tail, not the target shear named in an
  early comment.

## 2026-07-25T10:38:00Z — every axis rank drop closed

- Recomputed all \(xz\) augmented-rank drops, including the terminal
  \(C_7=0\) leaf.
- Recomputed the \(xy\) \(C_7,C_6,C_5,C_3,h\) drops.
- Closed both \(E_4\) factors, both \(C_1\)-descendants, the \(G\)-split,
  and all factor intersections.

## 2026-07-25T10:42:11Z — scoped PASS

- The strict external PARI transcript passes.
- Seven injected mutations are rejected fail-closed.
- The combined coverage runner passes the external \(A=0\) audit and the
  previously completed \(A\ne0\) audit.
- Verdict: no theorem defect; two certificate gaps and one prose
  misidentification were repaired by the external package.
