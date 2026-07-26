# Canonical reconciliation freeze

**Frozen (UTC):** 2026-07-26T01:31:00Z.

**Canonical main denominator:** 19 exact-\(\delta=3\) families, 6
exact-\(\delta=4\) families, and 1 dependent power-fibre orbit.

**Boundary registry:** 12 retained pivots and 24 exit arrows, each with a
stable identifier.  Boundary identifiers do not increment the 26 main
families.

The strict replay passed with terminal marker

```text
DELTA_GE3_RECONCILIATION_STRICT_PASS_26
```

SHA-256:

```text
d29089bd3debcb053923b762d6269cd52134df12b657258040c89a77e056dd37  RECONCILIATION.md
f5eba5f66fac8c0465e4b4d673d99166e8c96e3ae7b1297656c608cf51e4236b  PRIMARY_COMPARISON.md
ba8a5afe10eac65e3cdfad0f3228a692bb736d8cc99f6efa394234c461c53079  canonical_mapping.json
0b726f5344955e2ad0920b96d89292ef91e4326c7780ca54211aee1416625ca4  BOUNDARY_CHARTS.json
01af9eb6bd40c89087d1aa927ea707b277fcc623bf0f45aa3fec1e7d9b89f282  verify_reconciliation.py
371e23ac9e2d72800af027f37104a444bee86809f3d548edcc79dc20671b5266  verify_freeze.py
0b32effe398ffdd637d4e0b356c544b5108a329e5eff0a0f22cb3ab6888962ee  verify_strict.sh
440df4694f98b1b361a09e136afb4365c3aa302c5532e5291f4b76a2a068c65a  ../audit_delta_ge3_denominator/DENOMINATOR.json
527ef0112edef3c60ca6e3e1207f47ed79b8da298ff333dbab9993ec617354fe  ../audit_delta_ge3_denominator/FREEZE.md
affa2a4e37c4089a11e3c8e50ca93d84227069ebfcbbe98ba8484b11a1ef7fc1  ../binary_locus/delta_ge3_universal/FREEZE.json
```

The primary \(17+6+1\) package remains immutable evidence of the
independent derivation.  It is superseded for enumeration purposes because
the reconciliation found two quotient splits, two missing
doubled-nonbranch guard factors, and one omitted oriented squarefree
point-orbit.  The blinded \(19+6+1\) package is canonical.

This freeze was produced with substantial AI assistance.  It is not peer
reviewed, and exact checks are evidence about the encoded algebra rather
than peer review.
