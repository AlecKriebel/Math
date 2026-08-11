# Independent audit of the thirteen-pair common scalar

## Scope

This audit covers exactly the thirteen all-active-only rank-two switch pairs
with fingerprint

```text
f089ad4dbf064da8512d4854e824c36216e3eb74655ec435d06eecc69fb4f27e
```

It does not cover the seven mixed-profile switch pairs or global T3-2.

## Verdict

**PASS.**  Independent enumeration reproduced all thirteen pairs, their
thirteen unique failed all-active descriptors, and the frozen workload and
row hashes.  Every possible top edge preserves the listed rank-two workload.

For the eleven homogeneous supports, the scalar

\[
 (1+F)^4+\eta(1+H_w)^6
\]

has an all-active negative workload-power term one full polynomial order
larger than the positive powered-factorial term.  For the two weighted
supports, the fifth power gives a strict half-order gap.  On passing cones
with unbounded \(C\), both terms are eventually nonpositive.  With bounded
\(C\), the exact pure-source menu supplies a powered factorial descent of
order \(H^{q-1}\log^3(H)g(H)\), which dominates the \(O(H^{q-1})\)
workload cost.

Properness, the finite descriptor bad-sequence argument, nonexplosion, and
localized Dynkin then give classwise positive recurrence for arbitrary
strong orientations and positive rates.  No support, rate, orientation,
scaling, or communication-class counterexample was found.

Frozen evidence:

```text
pair SHA-256    f089ad4dbf064da8512d4854e824c36216e3eb74655ec435d06eecc69fb4f27e
base-row SHA    674cfbd62561207b275036b4830521df499d9062c735a4296d4d93654360a8ec
scalar-row SHA  cd78e50b5749b6feb35e459df5e7df690d235919e64336c1e1dde13370fae9e0
```

The exact contribution is thirteen positive-invariant pairs and zero signed
pairs, changing the post-416 remainder from \((319,34)\) to \((306,34)\).
Global T3-2 remains uncertified.
