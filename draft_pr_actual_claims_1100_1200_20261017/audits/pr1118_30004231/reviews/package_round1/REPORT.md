# Fresh adversarial whole-package review, round 1

Problem 30004231 / OWR-17135-028, PR #1118, original head `8592fb7297d3c4973f2778c47cfa8972cba896a6`.

**Verdict: NEEDS_REPAIR.** One concrete priority-audit version omission must be repaired before publication. I found no mathematical, verification, archive-integrity, metadata, disclosure, or PDF defect in the original frozen package. This report is historical: it does not approve a subsequently rebuilt archive automatically.

## Actionable finding R1: the latest relevant 2026 version was omitted

The distributed `audits/priority_01/PRIORITY_AUDIT.md`, `COMPARISON_MATRIX.md`, `DIRECT_CONSEQUENCE_CHECK.md`, and source ledger analyze Hiatt–Simpson–Wang–Wu arXiv:2606.10817 **v1**, dated 9 June 2026. The live [arXiv record](https://arxiv.org/abs/2606.10817) instead lists **v2, 24 July 2026**, with an improved counterexample. The note says its supplement considers current versions. A public relevant revision with a changed counterexample cannot be left unexamined while making that representation.

I read the complete current [v2 §8](https://arxiv.org/pdf/2606.10817v2), including Propositions 8.1, 8.2 and 8.7 and its construction. It now uses the three-skeleton of the projective-nine-space fan, stellar subdivisions at two three-ray cones, and a quotient from nine to eight real dimensions identifying their new rays. Its link is a wedge of eighty-four two-spheres with two points identified. It constructs a schön variety with a disconnected orbit intersection. It supplies no pair of Minkowski summands or identification with the exact positive-plus-additive face poset in this note. Such a representation is a substantive missing bridge; it does not follow from being a tropical fan. This reading identifies no full-target priority block, but the old v1-only comparison is incomplete. This is a scope comparison, not an independent validation of every theorem of that paper.

**Required repair:** add the current version identity, retrieval hash and accurate construction comparison to every current operative audit/source/version record; distinguish the old v1 analysis as historical. Update any current-version or coverage language globally, preserve truthful query counts and source-inspection limits, rebuild the source ZIP, kit and their manifests/receipts, then submit the new frozen package to a new fresh whole-package reviewer. The analytic note need not change if its existing bounded statement is supported by the repaired supplement. No other actionable finding was identified.

Current v2 PDF: 410,046 bytes, SHA256 `eef59d8ec20601addb6c243b64b23b84ef64726b7e78acc444e045c9068c6d53`.

## Independence and scope

I read the applicable repository policy and PDF skill. I reconstructed the entire proof and authored `check_independent.py` before consulting earlier mathematical review conclusions or their code. Only afterward did I read the distributed programs, bounded priority report, matrix and direct-consequence discussion. My files are confined to this review directory; I changed no input, PR, Git ref, publication, tracker or other worker's files. No external communication, purchase or access-control bypass occurred. The parent handles repository checkpoints.

Success requires a counterexample to both assertions under the literal printed definition. It does not require a common counterexample in the prior literature to trigger an already-solved exclusion: any earlier exact-poset nonshellability implication plus the classical homology antecedent would suffice. The current uninspected 2024 journal body remains a disclosed literature-coverage limitation, not an assertion that it contains no relevant remark.

## Independent analytic reconstruction

1. **Target match.** I fetched the primary [OWR39/2019 PDF](https://ems.press/content/serial-article-files/46818), read and visually inspected physical page 70 / printed 2464. Problem 3 imposes positive individual dimensions and equality between sum dimension and the sum of individual dimensions. No general-position condition appears. It asks shellability and the rational homology of a wedge of `(n-2)`-spheres. The note uses precisely its ordinary order complex. Adding an extremum would change the object and make it a cone; it is correctly avoided.

2. **Canonical summands and existential ambiguity.** A supporting functional exposing a sum face must maximize separately on both summands. Any alternative nonempty summand sets whose sum equals that face must lie in the canonical exposed faces. For any other functional their support deficits are nonnegative and add to zero, so both vanish. Equality of all support functions gives equality of the compact convex summand faces. No uniqueness of Minkowski decomposition for arbitrary unrelated convex bodies is being assumed. The cited [Fukuda–Weibel v4 Lemma 4](https://arxiv.org/pdf/math/0510470v4) states the required standard face decomposition and uniqueness.

3. **All base faces.** The affine-basis heights on the five simplex vertices completely parameterize functionals up to an additive constant. Every nonzero functional has disjoint nonempty maximum and minimum index sets. Assigning those sets the high and low values and every other vertex an intermediate value realizes all pairs. Disjoint direction spaces follow from affine independence with zero coefficient sum on each set. Thus dimensions are exactly `|A|+|B|-2`; positivity selects precisely sizes `(2,2)`, `(2,3)`, `(3,2)`. Whole and empty faces are separately addressed.

4. **Order and topology of the base.** Evaluating all differences `v_i-v_j` on a functional exposing a purported larger face forces both extremal index containments; hence inclusion is exactly componentwise inclusion. There are 30 minima, 20 maxima and 60 comparisons, with no three-element strict chain. Every vertex meets an edge, so the complex is pure. Suppression of each degree-two minimum gives the graph of signed two-subsets with opposite signs adjacent exactly for disjoint subsets. The same-sign intersecting-pair/complement path in the note connects all vertices; a disjoint pair is connected through an intermediate two-subset meeting both. A spanning tree leaves eleven independent cycles.

5. **Product exhaustiveness and boundary cases.** Every face of the product sum is exposed by `(u,t)`. Nonzero `t` gives the two endpoint copies. Zero `t` adds one interval direction to the sum but one to each summand, so the sum dimension is strictly below the sum of summand dimensions, including base vertices and the whole base. The two full horizontal ends have dimensions `(4,4,4)`; the full sum `(5,5,5)`; neither qualifies. Empty faces fail positivity. Endpoint coordinates prohibit any cross-comparison. The polytopes are full-dimensional lattice polytopes in actual ambient dimension five.

6. **Shellability and homology.** The order complex is therefore two connected pure graphs, each `f=(50,60)`. The incidence rank is 98 for the union, so ordinary rational Betti numbers are `(2,22)` and all higher groups vanish. The first edge from the other component meets all earlier edges in the complex consisting only of the empty face, of dimension -1. A new edge requires an intersection pure of dimension zero under both pure shellability and [Björner–Wachs Definition 2.1](https://www.math.miami.edu/~wachs/papers/nonpure1.pdf). This cannot be repaired by reordering. A wedge of three-spheres is connected with vanishing first homology, as is the zero-fold point; both obstructions are decisive. Replacing the printed sphere dimension by `n-3` does not help. The six-point three-dimensional control is correctly described as shellable, so it is not misused to settle nonshellability.

No central claim is transferred to an equivalent unsupported proposition; all of these arguments are finite or elementary exact deductions.

## New exact checks and adverse controls

`check_independent.py` is authored for this review and imports neither distributed verifier nor expected output. It enumerates **all 541 ordered height types** on the five affine-basis vertices and all three signs of the interval functional. Every functional has one of these weak-order types, making the normal-fan census exhaustive rather than numerical sampling. It maximizes directly over the coordinate point sets of both summands and their sum, computes dimensions over `Fraction`, and deduplicates actual exposed point sets.

Both ordinary and optimized Python produce the identical `INDEPENDENT_RESULTS.json`: **2,941 explicit checks**, all 543 nonempty faces, face dimensions `(40,140,200,130,32,1)`, 181 vertical faces all failing additivity, 100 selected faces and 120 graph edges. The graph has two components of 50 vertices, degree counts 60 of degree two and 40 of degree three, rational incidence rank 98, and 22 explicitly constructed independent fundamental cycles. Each cycle is tested to have zero signed boundary; unique non-tree coordinates prove independence, and rank proves completeness.

Independent controls include a cross-component edge, which changes Betti numbers to `(1,22)`; deletion of a component, which gives `(1,11)`; six isolated points, a tree, and a circle. The broader subset-dimension filter retains 30 proper vertical `(sum,summand,summand)=(3,2,2)` witnesses that the exact filter excludes. The diagnostic count including its whole face is not asserted to be the stable theorem's precise face-convention object.

I then read both distributed programs in full and ran each from the extracted source ZIP with `python3 -B` and `python3 -B -O`. All four outputs agree exactly with distributed expectations. Their explicit validation is not removed by optimization. The geometry program independently starts from supporting facets and intersection closures, checks all 8,649 summand-face pairs, all product inclusions and affine controls. The topology program constructs chains and signed rational boundaries, tests nonvacuous boundary-squared-zero on a filled triangle, catches a sign mutation, tests shelling conventions and confirms that an artificial maximum changes homology. Their checks support the note's computational descriptions.

## Sources, priority framing and limitations

The bibliography's six core sources were checked against primary records or accessible primary texts. The Fukuda–Weibel citation is pinned to v4, where Lemma 4 is the indicated uniqueness statement; its title, authors, journal volume and pages match the record. The Sturmfels–Tevelev examples cited are correctly **1.3 and 4.10**: they already give scaled opposite tetrahedra and the corresponding six-ray geometry. The note credits that antecedent and does not present the graph or simplex-difference classification as new.

The actual published Adiprasito et al. HTML was fetched from the publisher's official CDN. Section 1.2 uses summand facets in its totally mixed-face definition; the note's comparison is accurate. The published version has Lemma 3.8 and the corrected ambient formula, and the note does not import the old formula. The arXiv record has only v1; publication metadata, six authors and 2019 issue/2017 online distinction are correctly recorded.

The relevant definition and introductory scope in the accessible [Adiprasito 2020 manuscript](https://webusers.imj-prg.fr/~karim.adiprasito/cint.pdf) were read, including its page-two mixed criterion, and that page was visually inspected. For two summands its subset lower bounds are strictly broader than full additivity, as the note's explicit proper vertical face proves. The [institutional 2024 record](https://cris.huji.ac.il/en/publications/a-note-on-the-topology-of-minkowski-sums-and-complete-intersectio/) verifies the successor's changed title, DOI, volume, pages and advertised stable-intersection scope. This does not prove body identity or absence of an extra remark in the uninspected paywalled version. The paper, metadata and README properly disclose that limit and avoid a generic/stable resolution claim or worldwide-first certificate.

I independently executed ten discovery/priority search strings, screened additional primary leads, and checked the distributed audit's stated counts: 99 numbered plus six supplemental queries are indeed 105 distinct strings, with the five inherited strings kept separate. These finite searches do not certify absence of prior work. The only concrete coverage defect I identified is R1 above; it must be corrected in the operative distributed package.

## Archives, metadata and provenance

All six top-level package receipt entries matched exact byte counts and SHA256 values. Both ZIPs have unique, relative, non-traversing ordinary-file member paths. The source archive has 27 payload files and its manifest; every member hash and length matches, and the manifest covers precisely all other files. It includes the complete TeX, PDF, standalone verifiers, expectations, audit evidence, author license and provenance. No third-party source body, credential, private state, absolute dependency path or executable binary is distributed.

The five-member portable kit supplies the two exact upload files, metadata, portable manifest and README. Its metadata object is identical to the source metadata and repository manifest. Each portable path resolves to the intended file. Title, full negative scope, nongeneric nature, publication type, author spelling/ORCID, independent affiliation, version, date, English language and CC-BY-4.0 license agree across relevant representations. AI use and unrefereed/no human peer review status are explicit. Source citations do not purport to relicense third-party works. All eight original input-file hashes agree with local frozen inputs; the original proof SHA256 and PR head agree with the instructed identity. Historical proof-only assertions are correctly distinguished from the new package.

Frozen inputs reviewed:

| File | Bytes | SHA256 |
|---|---:|---|
| main.tex | 12033 | e6169d9ca403144fa876c37de8ca08bcbd84ef0e403ee00112cfe88854a1d817 |
| PDF | 65177 | 67ff7aae342c892fd7f7a7fa1c7c337ec0db11115b020f1832ce1b84b072569f |
| source ZIP | 143925 | c4b8ca96165f89eb64fe3db781897193d0feef3fa308af210cd2673f6aca6b67 |
| upload kit | 209846 | f310b19205191e757e67172275124a4e07e4de4c8c230c36f988522822ac66da |
| deposit manifest | 3169 | 23eb359183656ba7a55b03d0fd9fe8b765fa9247124e352e91fc0ab263888a56 |
| metadata | 2856 | 7a188ea6026e7876ffdfd9eb5af73d0c5bba33ecc9e76db98b66dfd99042b9cf |

## PDF reproducibility and visual review

I extracted the standalone source and compiled it with an isolated APFS-cloned Tectonic cache, cached-resources-only and untrusted-input modes. It compiles successfully without warnings. All four pages' full extracted text, decoded PDF drawing streams, and 105-dpi PNG bytes are identical to the frozen PDF. Whole-PDF bytes differ through compiler metadata, which the README anticipates. `PDF_QA.json` records the individual page hashes. I visually inspected every page: equations and text are legible, fonts and spacing are consistent, no overlap or clipping occurs, the author footnote fits, and all references are together and readable on page four.

**Final disposition of this frozen package:** mathematical and technical checks pass, but publication readiness remains **NEEDS_REPAIR for R1**. Repair and rebuild first, then use new independent reviewers as the user requires. The disclosed 2024 body-access limit remains a bounded priority limitation and must not be silently erased.
