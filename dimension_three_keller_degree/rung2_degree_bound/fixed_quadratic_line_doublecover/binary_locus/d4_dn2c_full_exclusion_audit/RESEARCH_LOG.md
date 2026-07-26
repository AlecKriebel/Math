# Research log — hostile final audit of `D4-DN-2C`

All timestamps are UTC.

## 2026-07-26T06:37:00Z

Started a source-only hostile read of the frozen contact atlas, primary
descent, and direct PARI lower package.  The authorized scope was fixed to
one normalized family over \(\mathbb C\).

## 2026-07-26T06:40:00Z

Found four missing plus signs in the displayed \(\mathcal F_B,\mathcal F_A\)
formulas.  The executable polynomial had the correct signs.  Reported the
transcription defect and required source correction.

## 2026-07-26T06:43:00Z

The primary aggregate strict wrapper passed.  It ran the frozen contact
rebuild, the full SymPy descent, both primary required-failure mutations, and
the independent direct PARI lower replay with its two mutations.

## 2026-07-26T06:46:00Z

Found two documentation inconsistencies: \(H_A\) was said to be “recorded”
although it is computed exactly but not printed, and \(K(k)\) remained after
the note was scoped to \(\mathbb C\).  Both were corrected in source.

## 2026-07-26T06:51:00Z

Audited the method-independence boundary.  The source PARI package explicitly
assumes the frozen contact atlas, so it independently certifies only the lower
descent.  Began a direct PARI reconstruction of contact exhaustiveness rather
than silently treating a second SymPy derivation as methodologically
independent.

## 2026-07-26T06:55:00Z

The direct PARI contact reconstruction passed.  It found the constant
\(-144\) pivot, the double hyperplane \(2b+3y=0\), the residual quadratic
\(f_0\), its two-plane split over \(\sqrt{-2}\), and the frozen line/origin
boundary.  No SymPy data were imported.

## 2026-07-26T06:59:00Z

Added the strict aggregate audit with a family-scope mutation and an
independent contact-quadratic mutation.  The optional clean-room SymPy package
also passed after its mutation wrapper was repaired; it is supplemental and
is not counted as the independent method.

## 2026-07-26T07:07:00Z

The source PARI package completed its own full contact-atlas reconstruction
with a different constant \(-144\) solve, all four specialization-safe rank
charts, and a required-failure contact mutation.  Its strict wrapper passed
`D4_DN2C_DIRECT_PARI_FULL_FAMILY_STRICT_PASS`.  The source package therefore
now supplies two-method coverage of the whole family theorem, not only of its
lower descent.

## 2026-07-26T07:29:16Z

The final aggregate audit passed
`D4_DN2C_FULL_EXCLUSION_HOSTILE_AUDIT_STRICT_PASS`.  Before the terminal
PASS, the required-failure tests exposed and forced correction of two bugs in
the audit wrapper itself: shell conditional fall-through in the scope checker
and an over-escaped contact-mutation pattern.  A fresh full run then passed
both source packages, the second PARI contact reconstruction, every
documentation/formula binding, and both hostile mutations.
