# Primary-source and qualification audit

This audit was performed after the independently written reconstruction was sealed. Prior reviewer reports and recorded PASS assertions were not premises. The primary bodies are kept only in this review's private source directory; the public receipt lists URL, size, and SHA-256, without redistributing those bodies.

## Exact question and bounded historical evidence

Both [AIM 2024 capture](https://web.archive.org/web/20240828224508id_/http://aimpl.org/freebycyclic/5/) and [AIM 2026 capture](https://web.archive.org/web/20260310215532id_/http://www.aimpl.org/freebycyclic/5/) were retrieved independently. They state Question 5.2 for a→a, b→ab, c→bcb, attributed to Rylee Lyman, asking for a proper cocompact cubical action. The current [HTTP AIM page](http://www.aimpl.org/freebycyclic/5/) also returned 200 with the same 25,734-byte body and SHA-256. This verifies accessible formulation evidence; HTTP transport and archive replay do not prove historical completeness or present community consensus. The passage giving an existing CAT(0) space is not an existing cocompact cubulation theorem.

The [AIM workshop report](https://aimath.org/pastworkshops/freebycyclicrep.pdf) gives a nearby b→aba, c→bcb formulation and discusses a hoped-for three-dimensional candidate. The monodromy differs from this exact target. It is acknowledged as nearby context, not silently identified with it.

Focused searches and direct reading of these primary works supplied no exact previously published construction with this model's cell counts. That is bounded search evidence only. No exhaustive priority certificate or first-resolution assertion is justified. The paper and native metadata correctly make the small explicit finite construction their concrete contribution and explicitly decline firstness, absolute novelty, minimality, and virtual specialness.

## Cubical global input

[Leary, arXiv:1009.1540v3](https://arxiv.org/abs/1009.1540v3), Appendix C: Theorem C.9 supplies the flag-link NPC criterion and CAT(0) universal cover for the general cube-complex convention, allowing the quotient identifications used here. Theorem C.4 supplies strict cube intersection properties in CAT(0). The finite-dimensional lifted unit-cube complex also has completeness by the finite-shape metric theorem in Appendix A; finite links give local compactness. The resulting complete locally compact geodesic length space is proper. These are compatible inputs; quotient self-identifications do not need to be asserted strict downstairs.

## Independent earlier-tools deduction

The following is my checked application of the cited inputs, not a claim that their authors published this assembled example.

Let H=⟨x,y,b | [x,y]=1, bxb⁻¹=y⟩ and A=⟨x,y⟩. Britton normal form embeds A≅Z² in H. In its Bass–Serre tree, the edge from H to bH has stabilizer ⟨y⟩. The element g=bx translates its axis by one edge. The incoming and outgoing edge stabilizers at H are ⟨x⟩ and ⟨y⟩, with trivial intersection; hence an axis segment has trivial pointwise stabilizer.

[Martin–Osin, arXiv:1310.6289v6](https://arxiv.org/abs/1310.6289v6), Corollary 4.3 applies to this tree action and gives WPD. The corrected v6 statement was checked. [Dahmani–Guirardel–Osin, arXiv:1111.7048v5](https://arxiv.org/abs/1111.7048v5), Theorem 6.8 and Corollary 2.9 supply a virtually cyclic hyperbolically embedded subgroup containing this infinite-order loxodromic WPD element; no finite-index replacement of the target is inferred. [Sisto, arXiv:1310.7753v1](https://arxiv.org/abs/1310.7753v1), Theorem 1 then makes g Morse. It follows that C=⟨bx⟩ is quasiconvex in the word metric on the edge generators {x,y,b}.

[Bena–Kropholler–Lyman, arXiv:2011.05374v1](https://arxiv.org/abs/2011.05374v1), Theorem 1.1 preserves the exact subgroup image in completion, and Theorem 5.1 makes the completion finite for a finite input and a subgroup quasiconvex in the specified maximal-tree edge generators. Here K has one vertex, so its lifted one-skeleton is precisely that Cayley graph. The lift of the bx circle stays within one edge of C; this verifies the required metric hypothesis instead of substituting an unrelated word metric. The resulting finite NPC completion Q₀ has π₁=Z and a local isometry j₀:Q₀→K representing bx itself. The cubical involution λ gives the second local isometry on the same Q₀. Gluing Q₀×I gives the same HNN presentation and a finite NPC complex of dimension at most three by the full-cone link argument. This establishes qualitative existence from earlier tools while leaving the explicit counts unsupported by those tools alone. BKL appeared online in 2021 and in the 2022 print volume; the bibliography's 2022 date is consistent.

## Nearby results checked against their actual strength

[Hagen–Wise, arXiv:1605.07879v3](https://arxiv.org/abs/1605.07879v3) is the corrected version. Its general result is a free cubical action; it does not supply the proper cocompact full-group conclusion for this exact example merely by being quoted. Its graph-of-spaces observation is consistent with the elementary local-isometry gluing used here.

[Lyman, arXiv:1909.03097v3](https://arxiv.org/abs/1909.03097v3) treats CAT(0) two-complexes for symmetric/palindromic families and discusses cocompact cubulation questions. A CAT(0) two-complex is not already the required cubulation. [BGGH, arXiv:2508.15738v3](https://arxiv.org/abs/2508.15738v3) discusses quasi-isometry to finite-dimensional CAT(0) cube complexes and hierarchical properties; it does not supply an equivariant proper cocompact action by inference. [Wu–Ye, arXiv:2504.14192v1](https://arxiv.org/abs/2504.14192v1) analyzes a linear symmetric family with specialness criteria; this quadratic monodromy is not that family.

## Native deposit metadata

The selected local adapter's bytes were independently pinned and its actual load/verify implementation read. [Current Zenodo developer documentation](https://developers.zenodo.org/#deposit-metadata) explicitly supports optional string version and ISO language fields, including eng; its 2017 change log records their addition. The older linked legacyrecord.json omits them, so that link is not a complete current field specification.

The current [Zenodo deserializer](https://github.com/zenodo/zenodo-rdm/blob/master/site/zenodo_rdm/legacy/deserializers/metadata.py) loads version and language, and the [serializer](https://github.com/zenodo/zenodo-rdm/blob/master/site/zenodo_rdm/legacy/serializers/schemas/common.py) emits both. This resolves the suspected schema issue. Offline adapter probes independently accepted the exact reviewed metadata/files and rejected all 20 corruptions in both normal and optimized modes. No API client, credential read, stage, or publication was used. A future authenticated server read-back remains necessary operational evidence of actual live acceptance; this review does not pretend to have performed it.

Result: source/theorem applicability, bounded priority language, citations, AI disclosure, and reviewed native metadata pass. The stale PR description is the sole required edit, recorded separately as R1.
