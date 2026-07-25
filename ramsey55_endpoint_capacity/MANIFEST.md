# Claim and evidence manifest

## Publication claim

Conditional on the completeness and nonisomorphism of the publisher-supplied
edge-85 `R(4,5;18)` catalog and complete `R(4,5;24)` catalog, no 18-regular
`(5,5;43)`-graph has a vertex whose neighborhood spans 85 edges.

Together with the published extremal bound, every vertex of such a graph lies
in at most 84 triangles.

## Evidence map

| Claim | Evidence |
|---|---|
| General transversal-capacity inequality | Elementary proof in Sections 2-3 of the manuscript |
| Ramsey cross-neighborhood conditions | Direct independent-five-set argument in Section 3 |
| Column size `|X_b| = d_H(b)-5` | 18-regularity |
| Edge balance `e(H)=213-e(A)` | Two-sided cross-edge count in Section 3 |
| 74 edge-85 order-18 records | Pinned publisher-supplied catalog |
| 843 edge-128 order-24 records | Filter of the pinned complete 352,366-record catalog |
| 61,939 strict exclusions | Deterministic producer and separately written checker |
| 443 equality cases | Complete classification stream and checker |
| Unique size-six minimizer | Exact subset enumeration in producer and checker |
| High-high-edge contradiction | Elementary equality-rigidity proof |
| 17/17 semantic tests | Compact verifier bundle |
| Far-side archive integrity | Downloaded archive SHA-256 and clean replay |

## Frozen identifiers

- Source research checkpoint:
  `b14f50dd3b048b2d0e51e6aabd63bb608662f053`
- Compact verifier commit:
  `b6d7f1a87382d63debeb8c96c76caa230e44331d`
- Bundle manifest SHA-256:
  `7aac9cf56dad8787bef798dc7507ca437ec2e662645d77f7ddaf565932e671fe`
- Classification stream SHA-256:
  `3c72e75506a43bed6ca44213c5bf540f0370c39b85597259738709fd2345c785`
- Independent saved check SHA-256:
  `71d165f4e281aa943129e4367b9123f4bac9f8af19a187e6a3fd4d07132bad86`
- Normalized archive SHA-256:
  `de541d6c7ed8be496784397ea0ee3f1b12c2b93cdbc42ba908160095c1d79cc4`

## Explicit boundary

The local verification does not re-enumerate the complete `R(4,5)` catalogs.
The theorem excludes only `(e(A),e(H))=(85,128)` inside the regular degree-18
branch. It does not exclude the `(84,129)` layer or any other remaining layer,
close a global branch, or change the known bounds on `R(5,5)`.
