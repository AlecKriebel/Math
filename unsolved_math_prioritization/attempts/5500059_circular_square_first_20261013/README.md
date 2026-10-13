# Most Circular Partition of a Square: first authored edition

Problem 5500059 / AMR-054-0059 / TOPP 59. Status: unresolved. Date: 13 October 2026.

This is the first newly documented substantive investigation in the present continuation. Recovered earlier material established source triage only; the lifetime number of substantive attempts is unknown. This edition neither claims that no earlier attempts occurred nor resets an investigation budget.

## Main result

There is a complete finite partition of the square into 92 positive-area closed convex polygons, every one having smallest-enclosing-circle radius divided by largest-inscribed-disk radius strictly below

649161/500000 = 1.298322.

The full rational coordinate and disk certificate proves this feasible upper bound. It improves the identified source-reported complete-square upper bound 1.29950 by 0.001178. The combinatorial layout is credited to Figure 16 of Damian and O'Rourke, [arXiv cs/0304023v2](https://arxiv.org/abs/cs/0304023v2); the optimized rational coordinates and independent disk witnesses are authored here. No exhaustive-literature priority claim is made.

A complete finite-case proof also reconstructs the intended source lower bound. Define t0 as the unique root in (0.82,0.83) of

t^8 - 2t^6 - 16t^5 + 3t^4 + 6t^2 + 1 = 0,

and let G=(1+t0)/sqrt(2)=1.2886844618704579013258751580333... . Every finite admissible partition has worst ratio strictly greater than G. For the infimum Gamma_fin over all finite admissible partitions, the accepted results give

G <= Gamma_fin < 1.298322.

The strict upper inequality follows because the explicit finite construction has 92 strict bounds and hence a maximum strictly below the stated rational constant. The lower inequality for the infimum is not made strict by the per-partition theorem.

For each fixed positive integer N, a best partition with at most N cells exists and its value exceeds G. This does not establish a positive gap uniform in N or attainment of Gamma_fin over unrestricted finite cell counts.

## Admissibility and local results

All full-square results here concern finite families of positive-area compact convex polygons covering every point of the square with pairwise disjoint interiors. Steiner points are unrestricted. Incenter and enclosing-circle center may differ; adjacent indisks need not be tangent. No equality with an arbitrary infinite-partition formulation is assumed or established.

The separate local result constructs a non-tangent two-cell boundary junction with upper opening at least 4 atan(1/2)>90 degrees. An exact finite rational realization has 208 and 162 vertices and ratios at most 1.28878. This two-cell patch is not a full-square partition or a full-square upper bound. It does not disprove the source's restricted tangent-indisk conjecture.

The 2026 v2 revision explicitly changes the restricted 1.28939 statement from a lemma to a conjecture. Its general reported lower bound was not withdrawn. The reconstructed proof repairs specific presentation gaps and the valid-range restriction of a local formula; those defects alone do not show the intended bound false.

## Complete evidence and reading order

1. [Full 92-piece construction proof](CONSTRUCTIVE_UPPER_BOUND.md), [complete rational coordinate and disk certificate](rational_partition_certificate.json), and [authored diagram](partition.svg).
2. [All 4,186 exact separation witnesses](pair_separation_witnesses.json), [all 92 per-face margin rows](exact_face_margin_table.json), and [exact construction summary](exact_verification_summary.json).
3. [Independent construction review](INDEPENDENT_CONSTRUCTION_REVIEW.md), [exact acceptance results](EXACT_CONSTRUCTION_AUDIT.json), and [independent checking guide](CERTIFICATE_GUIDE.md).
4. [Complete finite lower-bound, compactness and local-junction proofs](THEORY_REPORT.md), [independent theory review](INDEPENDENT_THEORY_REVIEW.md), [exact scalar controls](EXACT_THEORY_CONTROLS.json), and [universal symbolic identity audit](SYMBOLIC_THEORY_AUDIT.json).
5. [Complete local rational polygon certificate](local_patch_certificate.json), [exact local acceptance](EXACT_LOCAL_PATCH_AUDIT.json), and [local checking guide](LOCAL_CERTIFICATE_GUIDE.md).
6. [Bounded source audit](SOURCE_BOUND_AUDIT.md), [actual scholarly PDF identities](SOURCE_IDENTITIES.json), [integration and acceptance](INTEGRATION_AND_ACCEPTANCE.md), and [public byte manifest](PUBLIC_MANIFEST.json).

These are authored proofs, mathematical certificates, an illustration, source metadata and independent mathematical/computational reviews. The reviews are not human peer review. The exact optimum, unrestricted finite attainment, infinite admissibility and global novelty remain unresolved. Copied source documents, source text, dataset contents, programs and private coordination are excluded.
