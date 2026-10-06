# PR 21: independent exact-target priority audit

Audit completed 2026-10-01 UTC. Problem 30001696; frozen candidate head `096aacd71a1dc6dd3a73bea3c1055877dc8c0451`. This is a first-party mathematical and bibliographic audit, not a quotation of an earlier review. Source copies and the temporary reader remain under ignored `tmp/`; no foreign source is part of this report package.

## Verdict and exact remaining boundary

**A serious positive classical-subsumption priority objection was verified in this audit. A prior explicitly stated universal whole-product theorem was not verified.** Klee–Novik's dated original source contains an actual embedded collapse to the standard coordinate sphere, stronger than homology or collapse to an abstract sphere. Together with its theorem that the complementary complex is a PL manifold, the classical PL collar and regular-neighborhood machinery yields the entire product by a short fully typed argument. That argument is written and independently sealed in [EXACT_PRIOR_ADAPTER.md](EXACT_PRIOR_ADAPTER.md).

The audit's sealed criterion allows a general prior theorem to subsume the target when its hypotheses and category/space adapter are checked and no unsupported central geometry is imported. The adapter meets that criterion in this author's assessment. It is nevertheless a newly written deduction here, not evidence that Klee–Novik or another author explicitly printed, recognized, or claimed the final answer. The parent has commissioned an independent adversary to try to falsify the adapter; its outcome was not used in this report. Final project classification is reserved for that verification and the parent's decision.

Consequently the candidate should **not presently be promoted as a concerns-free novel resolution of a still-open problem**. If the independent check accepts the adapter and the project treats a direct classical consequence of the dated stronger statement as already settled, the user-prescribed `already_solved` route applies: record the priority correction and accept the mathematical progress as a partial result, without a new paper or DOI. This report does not itself alter `QUEUE.md`, a PR, or any publication.

## Frozen question and independence

The exact target is all integers `d>=2`, `0<=i<=d-2`, the WHOLE pure facet-generated subcomplex `B(i,d)` of the cross-polytope boundary, with ordinary NONCYCLIC switches between positions `j` and `j+1` for `1<=j<=d-1`, in the PL category:

`|B(i,d)| ≅PL S^i × D^(d-i-1)`.

The endpoint `i=d-1` is the whole sphere and elementary. Homology, a product boundary, or an arbitrary disk-bundle conclusion is insufficient to identify the entire product. The original full [OWR 08/2011 source](https://publications.mfo.de/bitstream/handle/mfo/3223/OWR_2011_08.pdf?isAllowed=y&sequence=1), Klee contribution printed pp.370–372, Question 4 p.372, states this whole-space question separately from its manifold/homology/boundary theorem. Its switch definition is noncyclic.

The exact original question and candidate `source_snapshot/PROOF.md` were read first. The criterion was sealed at `2026-10-01T18:51:01.102350Z`, before historical source-audit/review, root reconstruction, or sibling outcome details. [FIRST_PASS_SEAL.json](FIRST_PASS_SEAL.json) binds the original source, candidate proof and criterion hashes; [CRITERION_AND_FIRST_PASS.md](CRITERION_AND_FIRST_PASS.md) preserves the distinct answer/mechanism novelty boundaries. The historical `SOURCE_AUDIT.md` was consulted only after this seal; its conclusions were not treated as mathematical authority. No sibling proof or review was consulted in constructing the adapter.

## Strongest checked dated prior

The relevant primary paper is **Steven Klee and Isabella Novik, “Centrally symmetric manifolds with few vertices,” Advances in Mathematics 229(1) (2012), 487–500, DOI [10.1016/j.aim.2011.07.024](https://doi.org/10.1016/j.aim.2011.07.024)**. The candidate and historical audit give the wrong journal; Indiana University Mathematics Journal is not the publication for this paper.

Both complete [original arXiv v1](https://arxiv.org/pdf/1102.0542v1) and [author-final dated July 27, 2011](https://sites.math.washington.edu/~novik/publications/sphere-products.pdf) were retrieved. Relevant definitions and the full §3 proof, Remark 3.7, §4 boundary arguments, and bibliography were checked. In particular:

- Theorem 1.2(c),(d) and §3 give the complementary complex simplicially isomorphic to `B(d-i-2,d)`, and both complexes as PL manifolds with boundary.
- Lemma 3.4 gives shellable vertex stars.
- **Remark 3.7, printed p.9**, asserts elementary collapses `B(i,d) → B(i,d-1) → ... → B(i,i+1)=C*_(i+1)`, and a disc bundle over `S^i`, citing Rourke–Sanderson Chapter 3.

This is an embedded coordinate sequence in the actual cross-polytope complexes. It is not only an abstract homotopy equivalence. The remark's terse collapse assertion was independently expanded in the adapter: shellable links are proper shellable balls; relative cone collapses at the two last-coordinate vertices leave their base union, exactly `B(i,d-1)`. Iterating verifies the strong claim for every required parameter, including `i=0` and `d-i-1=1`.

No checked KN body explicitly states the universal trivial product for the whole complex. The explicitly discussed low-dimensional cases and the two-facet-complement case are already known special cases and do not support a new universal priority claim.

## Full primary classical theorem access and typed implication

The full **Rourke–Sanderson, Introduction to Piecewise-Linear Topology (1972)** was obtained through a direct book reference on a university topology course page. Its [primary DjVu copy](https://www.maths.gla.ac.uk/~mpowell/Rourke%20C.P.%2C%20Sanderson%20B.J.%20Introduction%20to%20piecewise-linear%20topology%20%28Springer%2C%201972%29.djvu) was decoded locally with isolated official DjVu.js 0.5.4. All 131 pages were decoded; the actual Chapter 3 pp.31–49, collar theorem 2.25 p.24, and relevant category convention p.7 were read. The key theorem p.41 and proof page p.42 were additionally inspected as pixels. The book's convention is that map, embedding and homeomorphism mean PL unless explicitly designated topological.

The crucial exact statement is **Corollary 3.30 p.41**: an actual neighborhood `N` of `X` in `int M` is regular precisely when it is a compact manifold with boundary and collapses to `X`. **The original B cannot be inserted naively**, because its coordinate collapse core can meet its boundary. The adapter explicitly repairs this condition:

1. The common frontier of B and its complementary PL manifold is their common boundary. A connected ambient-link facet graph verifies the equality for all shared lower-dimensional faces; no global boundary unknotting is assumed.
2. Add a short outward collar from the complementary manifold. The enlarged `N` is PL homeomorphic to B, is now an actual ambient neighborhood of the coordinate sphere, and collapses to B relative to the collar base, then to that sphere.
3. Apply actual Corollary 3.30 and regular-neighborhood uniqueness, Theorem 3.8 p.33 or 3.24 pp.38–39.
4. The standard coordinate sphere has a standard neighborhood in `C*_(i+1) * C*_(d-i-1)`. The epsilon-neighborhood construction pp.32–33 applies. Compatible truncated-join cells have the face lattices of `simplex × cone(simplex)`; barycentric subdivisions give a PL product `S^i × D^(d-i-1)`. This avoids the common mistake of calling a bilinear radial or join-coordinate formula PL.

Thus the conclusion follows from the old source's **strong embedded statement**, not from “a sphere homotopy type implies a product,” an unsupported disk-bundle trivialization, or the candidate's flow/Hauptvermutung mechanism. The entire universal construction is in the sealed adapter, SHA256 `74feb57d88d1c05733635768c89bf6f2308d06ad8efe1b3cde264eca0a14fe82`.

Primary **Rourke–Sanderson, Block Bundles I (1968)**, §§4–5 pp.14–24, was also checked. Its local-flat/proper hypotheses and block/disc distinctions do not silently trivialize every disk bundle. It is not needed for the repaired direct collar argument.

## Chronology and historical caution

The official [arXiv history](https://arxiv.org/abs/1102.0542) has only v1, submitted **February 2, 2011, 20:09:33 UTC**. That version already contains Remark 3.7 with the collapse and disc-bundle statement. The original OWR workshop took place **February 6–12, 2011**, and its report nevertheless asks Question 4 for the whole product. The July 27 author-final retains the remark. The publisher metadata identifies the journal issue as January 15, 2012.

The chronology does not justify claiming that the authors recognized the product consequence or that the question had an explicitly published answer before being asked. It also prevents explaining the discrepancy by a collapse result appearing only after the workshop. Why the whole-product question remained in the report is not determined by the inspected sources. The checkable mathematical implication and the historical recognition question must remain separate; no speculative explanation is offered.

## Equivalent-target and later-literature checks

[SUBSUMPTION_MATRIX.md](SUBSUMPTION_MATRIX.md) gives the object/category/parameter distinctions and exact proof locators. The most important checks are:

- **Machacek, published 2022** ([full EMS article](https://ems.press/content/serial-article-files/39446), DOI [10.4171/AIHPD/125](https://doi.org/10.4171/AIHPD/125)): the ordinary sign-variation projective space is exactly the antipodal quotient of B. The full topology proof, §§3.2–3.3 pp.551–556, was checked, including its acyclic matching. Theorem 3.6 p.556 gives an **actual collapse to coordinate projective space**, stronger than the candidate's homotopy-only summary. Its lift supplies another embedded-sphere-collapse route; the paper does not explicitly state the universal trivial product. The later networks portion and complete bibliography were also screened.
- **Bergeron–Dermenjian–Machacek, Sign variation and descents (2020)** ([published full body](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v27i4p50/pdf/), DOI [10.37236/9801](https://doi.org/10.37236/9801)): same quotient/order complex, partitionability and h-vector results, not a universal product theorem.
- **Karp–Machacek, accepted v2 (2022), published 2023** ([full accepted body](https://arxiv.org/pdf/2104.02786), journal DOI [10.5070/C63160419](https://doi.org/10.5070/C63160419)): `P_(n,l)` is the at-most-variation quotient of B and explicitly cites KN. Its closed-ball theorem applies instead to `R_(n,l)`, the exactly-variation complex with different face-poset grading. These targets cannot be conflated. The P-specific §5 pp.16–18 concerns log-concavity and Sperner questions.
- **Wang–Zheng, accepted v2 (2019), journal 2020** ([full body](https://arxiv.org/pdf/1811.08505), DOI [10.1016/j.ejc.2019.103043](https://doi.org/10.1016/j.ejc.2019.103043)) and its full FPSAC2019 antecedent: Example 3.14 recursively reconstructs the actual B family, but the sphere-product statement is for its boundary.
- **Bagchi–Datta**, both full original preprint and later sphere-focused version: exact B occurs under `M(k,d)`; the overbar denotes its boundary. The boundary is the product, and the filling is locally stacked. OCR loss of overbars would create a false full-space priority hit.
- **Murai–Nevo**, full FPSAC2013 primary Example 3.4 p.187, and **Klee–Novik's face-enumeration survey** p.13: exact complex, boundary/product and stackedness results, no explicit total-space upgrade at the checked loci.
- **Browder–Klee** binary-word simplicial posets and disk bundles are different objects; the actual construction was checked. **Generalized Heawood Numbers** uses closed boundary examples. **Small triangulations of simply connected 4-manifolds**, published 2025 full body, concerns different closed manifolds. Related stackedness, tightness, balanced, neighborly and enumeration sources were screened in their complete available PDFs and relevant citation/construction contexts; unrelated proofs were not represented as line-by-line audits.

The current primary Novik publication list, including entries through 2026, was inspected. Later titles and relevant primary bodies were followed where the exact-family/citation trail supplied a lead. This is not a claim to have audited every 2026 paper or every author's complete output.

## Search and access limitations

[QUERY_LOG.json](QUERY_LOG.json) records 67 mathematical discovery queries and two software-reader queries. [KN_CITERS_SCREENING.json](KN_CITERS_SCREENING.json) records 22 KN citation records; [MACH_CITERS_SCREENING.json](MACH_CITERS_SCREENING.json) records the one DOI-resolved Machacek citation record returned. OpenAlex is a discovery index, not mathematical authority and not exhaustive: the independently found 2020 Sign variation and descents paper cites the earlier preprint yet is absent from the one-item Machacek DOI list. No mathematical conclusion rests on an abstract or citation-count silence.

Material limits for a claim that nobody explicitly published the answer remain:

- The KN publisher full PDF and author-manuscript endpoints returned access challenges. The full original preprint and dated author-final were checked; they are not claimed byte-identical to the final journal PDF.
- The 2015 short book chapter **Balanced Manifolds and Pseudomanifolds**, DOI 10.1007/978-3-319-20155-9_21, returned a subscription page rather than its body. Its metadata is not proof evidence of absence.
- Karp–Machacek's publisher PDF endpoint returned an empty 202 response; the complete accepted v2 was checked, not asserted identical to the journal's pagination.
- Mandelshtam's 2024 Berkeley thesis was available as an actual full PDF through the web reader; its relevant Chapter 5 §§5.2–5.3 definitions and introduction were inspected. The local byte download failed. This was a related-target screen, not a full thesis proof audit; the inspected grasstope ambient dimension and variation inequality differ from the target.
- The initially inaccessible Springer regular-neighborhood chapter is **no longer an obstacle to the positive adapter**: the complete actual 1972 book was subsequently obtained and its required body verified.

These limits preclude a worldwide negative priority certificate, but do not remove the positive classical-subsumption objection whose source bodies and full hypotheses were checked.

## Required global repairs and permitted outcome

Any subsequent repository or PR revision should correct the KN journal and DOI, cite and accurately describe Remark 3.7's embedded collapse/disc bundle, upgrade the Machacek description from bare homotopy to actual coordinate collapse, and state the old-ingredient collar/RN implication with its actual-neighborhood repair. Remove unsupported assertions that only homology/boundary facts were previously available or that this audit certifies worldwide novelty. Distinguish any new candidate mechanism from priority of the final product answer.

This mathematical result is not identified as false by the priority audit. The issue is the proposed novelty/open-status framing. The exact remaining decision is whether the independently checked classical adapter satisfies the project's already-settled criterion; the parent controls that decision after the fresh adversary reports. No paper, upload, DOI, sheet row, merge, close, branch operation, or external-individual communication was performed by this agent.

## Reproducibility bindings

All retrieved-byte hashes and access results are in `SOURCE_RECEIPTS*.json`; [SOURCE_LOCATORS.json](SOURCE_LOCATORS.json) binds audited loci and access scope. The first pass and exact adapter have separate dated seals. [TOOL_RECEIPTS.json](TOOL_RECEIPTS.json) identifies the isolated extraction reader; it is never a mathematical source and is not redistributed. [MANIFEST.json](MANIFEST.json) inventories only first-party files, excluding itself and all ignored source/library caches. The parent can re-fetch the listed primary URLs, verify hashes, inspect the exact old proof loci, and independently check the short adapter without any candidate flow code or finite-case computation.
