# Acceptance: a negative answer to KOU-21.107

Date: 8 October 2026. Record 2616, rank 1038. Queue classification: `claimed_solved`; substantive proof-attempt count: `1/5`.

## Accepted mathematical result

The frozen report proves in ZFC that a countably infinite Hausdorff nondiscrete Boolean topological group can have a partition into countably infinitely many dense subsets and nevertheless have no expansive sequence of pairwise-disjoint finite subsets. This is a full negative answer to KOU-21.107, with the usual meaningful convention that the open sets being hit are nonempty.

The group consists of finite subsets of the natural numbers under symmetric difference. For an arbitrary free ultrafilter, the finite subsets of each ultrafilter member form a neighborhood subgroup. The dense partition is given by the exponent of 2 in the support cardinality plus one. For any disjoint finite-block sequence, the finite fibers of the maximum-support map produce a point-finite family of maxima sets. An infinite disjoint subsequence and a parity split give an ultrafilter-complement neighborhood missing infinitely many entire blocks. The written proof supplies the infinite quantifiers and ultrafilter existence; no special ultrafilter, continuum hypothesis, metrizability, or first countability is assumed.

Two independent authored audits accept the complete infinite proof. The final report is 9,338 bytes with SHA-256 `ddde58f03f320c881b78e59b60a40f315e1811c7c88aaa25ce620c427afbb6ca`. The first audit is 11,198 bytes, SHA-256 `4342d824640fde88bfcd492841b365955456764d4c99eca61d788e3fa6e65f73`; the second is 14,229 bytes, SHA-256 `9993b954dd21a2666eebef1a6653aa52a49b98ad14ac4007b1f7e9e62eb724e4`. These assessments are AI-assisted mathematical review, not human peer review, editorial confirmation, formal mechanization, or a priority determination.

## Source and attribution boundaries

The exact target was inspected in [Kourovka Notebook version 48](https://arxiv.org/pdf/1401.0300v48), p.193. Predecessor 15.80 is on p.97 of that version, and on p.98 of version 47. Its uncountable box-product example does not decide this countable target. Its additional Zelenyuk remark concerns dense partitions for infinite abelian groups with finitely many involutions; it neither supplies the needed nonexpansive countable example in the inspected passage nor applies to this Boolean group with infinitely many involutions.

The topology is standard and credited to the Mathias/free Boolean linear construction described in [Sipacheva, Section 8, p.25](https://arxiv.org/pdf/1612.04878v1). No new-topology or priority claim is made. Literature and published-status observations are bounded historical checks, not exhaustive certification.

## Frozen evidence and verification boundary

The six author public files, six author external files, original 13,488-byte archive, first audit, and six second-audit files are preserved byte for byte. Historical statements that the initial author submission was pending audit, or that publication had not yet occurred during an audit, are retained. This acceptance document records the later assessment without rewriting those historical flags.

The author checker covers 43,533 finite cases per mode. Its harness rejects 18 malformed fixtures and 10 tampering cases in each of normal, -O, and -OO modes. The second checker independently uses explicit sets for 192,528 finite checks and rejects 91 malformed variants per mode. The separate publication wrapper authenticates the complete allowed inventory and archive before executing these pinned tools, uses exact JSON schemas and integer types, rejects duplicate keys and nonfinite/overflowed floats, and checks real nonroot read-only execution. These controls do not simulate a free ultrafilter or mechanize the infinite proof.

Default publication replay is source-free. Fresh source-PDF and corpus matching are `NOT_RUN`; historical public hash/size/inspection metadata remains available. Copied source documents, source text, dataset contents, private sources, and private coordination material are excluded.
