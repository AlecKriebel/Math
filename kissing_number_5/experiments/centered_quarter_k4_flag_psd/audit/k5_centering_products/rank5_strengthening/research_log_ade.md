# Research log: exact ADE and moment audits

## 2026-07-24 02:07 PDT

* Strengthened the centered H2 empirical lattice from
  \(X_2\equiv12\pmod {35}\) to \(X_2\equiv82\pmod {210}\), using
  \(b_a^2\equiv16+15a\pmod {30}\).
* Proved the joint centered selector
  \(X_2\equiv21X_1+40\pmod {2100}\), using
  \(b_a^2\equiv15a^2-150a+256\pmod {300}\).
* Generalized both selectors to arbitrary centroid parameter
  \(A=\sum a m_a\):
  \[
  X_1\equiv5A+2\pmod {10},\quad
  X_2\equiv105A+82\pmod {210},\quad
  X_2\equiv21X_1-1050A+40\pmod {2100}.
  \]
* Checked the noncentered `r12` vector exactly:
  \(A=-81,Q=2363,S=162115,X_1=7,X_2=1237\).
* Audited the 12-antipodal ADE reduction.  The generated lattice is exactly
  its ADE root lattice; discriminant forms force every full-rank dual
  norm-two vector to be a root.  The residual shell sizes are therefore
  \(6,16,2\) in \(A_5,D_5,D_4+A_1\).
* Independently enumerated all 455 \(A_5\), 125970 \(D_5\), and 13
  \(D_4+A_1\) twelve-line subsets with exact rational arithmetic.  Results
  agree with the conceptual proof.
* Audited rank-four \(D_4\): projected candidates are \(0\) plus the
  24-cell.  Poles cannot join a large quarter-grid residual set; each height
  layer has compatibility graph \(3K_8\), so 17 residual points are
  impossible.
* Exact direct verifier invocations pass.  Normal module-import unit tests
  remain blocked by the transient macOS TCC/provenance lock, so no
  `COMPUTATIONALLY CERTIFIED` status is claimed yet.

## 2026-07-24 02:41 PDT

* Imported and hash-checked the exact 38-vector `r11` global-profile export
  for \(Q=2362,\ldots,2368\).  Every profile has \(m_{+1}\le6\).
* Closed the line-line half-integrality loophole.  A defect graph edge uses
  two color-\(+1\) edges, so there are at most three defects.  Deleting a
  minimum vertex cover leaves at least eight integral root lines.
* Proved that this integral remainder cannot have rank four when defects are
  present: nonzero character supports in \(A_4,D_4\), combined with minimum
  vertex-cover minimality, force \(d(5-d)=4,6,6\) crossing defects.
* For a rank-five remainder, enumerated the possible ADE types and verified
  that every norm-two dual shell has at most 20 antipodal lines.  Ordinary
  residuals plus the remaining half-integral exceptions total at most 15.
* Closed the defect-free rank-four \(D_4\) case using the exact projected
  shell and the universal height-layer inequality
  \(k^2/4\le\operatorname{tr}H^2\le2k\), hence \(k\le8\).
* Conclusion: all 38 exact `r11` global profiles are eliminated, subject to
  independent adversarial review of the character/defect argument.

## 2026-07-24 02:47 PDT

* Independent adversarial review by the integer-degree audit passed each
  requested point: the minimum-cover neighbor property, the \(k-6\)
  character-support lower bound after omitted root lines, the 20-line
  \(A_3+2A_1\) dual shell, and the exact \(2e+h\) color-\(+1\)
  bookkeeping.
* The independent audit produced a standalone package with manifest SHA-256
  `2e963affee970e3086e8466a11d152fe98a8d24e11fe7e6301b40201b8aa6853`;
  its tests pass.
* Re-ran both local exact verifiers by absolute path.  The ADE shell
  enumeration and all 38 profile bounds pass.  Normal test discovery still
  fails at directory traversal because of the macOS TCC/provenance lock;
  this is an environment-access failure, not a mathematical or verifier
  failure, and `COMPUTATIONALLY CERTIFIED` remains intentionally withheld.
* Clarified the proof note's boundary section to distinguish the `r12`
  zero-defect exclusions from the `r11` defect-budget argument.
