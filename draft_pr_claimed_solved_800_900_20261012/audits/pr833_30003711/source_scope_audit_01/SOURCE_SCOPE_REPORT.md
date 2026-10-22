# PR 833 / problem 30003711: independent source-scope audit

Decision: **REPAIR_REQUIRED for promoting equality at 8; source-scope match CLEAR.** The curated target and cited theorem concern the same invariant, but the inspected preprint’s lower-bound calculation has a substantive unresolved challenge described below. Equality requires a valid lower bound as well as the separately checked upper bound. This is a source and dependency audit, not a novelty certificate.

The intended exact claim is: **The ordinary unnormalized, section-based Schwarz genus of the nine-flex cover over the space of smooth homogeneous ternary cubic equations modulo nonzero scalar is 8; its normalized sectional category is 7.** This exact equality is conditional on resolving the lower-bound dependency challenge; the submitted construction alone supplies an upper bound of 8, conditional on its separate mathematical verification. The complete supplied curated record supports this target. A headline claiming an unqualified solution of the literal definition in OWR Question 5 would exceed the result.

The stronger literal OWR invariant, with connected open domains that trivialize all nine sheets simultaneously, remains unresolved by this manuscript. Exact algorithmic branching complexity also remains outside the theorem. These qualifications are already present in the frozen proof and package README, and must remain attached to any status or promotion.

## Independence, frozen inputs, and success criterion

The audit first read the entire private complete_queue_show.json, including the original and cleaned statements, full background, and empty prior_research object; author/PROOF.md; author/SOURCE_METADATA.json; and SOURCE_MANIFEST.json. An interpretation checkpoint was written before reading earlier independent_audit or second_review verdicts. Later review records were used to compare provenance and historical source access, not as evidence of mathematical correctness.

The freeze is 0e6e23213494ecb4a7208f920d25d7b49502a5cb. All 28 source-manifest files match their recorded byte sizes and SHA-256 hashes. FROZEN_SOURCE_CHECK.json records the individual results. The statement hash independently recomputes to 23a9b0fbd1ac1c8e7e5835e77428953266944c826aa92b94b987484768fb6488, and the complete-problem/empty-prior-report combined serialization recomputes to 21251c11ee8a6d003fb2e0e5142b9089314bfbb982d88e5f254bad178a79a049, exactly the supplied review hash. This auditor did not rehash the three entire catalog datasets; their historical verification remains a separate frozen record.

The success criterion here is that the actual curated claim, its space, covering, normalization, and cited lower bound agree with the submitted theorem; that the Hesse and triangulation inputs are accurately located and applicable; and that inaccessible sources, stronger historical wording, and unrelated algorithmic claims are not silently certified. No central proof search or additional substantive approach was undertaken; the original effort remains 1/5.

## What the sources actually ask

The complete curated statement explicitly specifies smooth homogeneous ternary cubic polynomials modulo C×, and a degree-nine cover recording one flex. It asks for Schwarz genus without adding a connected-domain or full-trivialization definition. Its full dated literature assessment identifies an 8-versus-9 problem and cites Chen–Wan. This positively identifies the conventional section-genus target independently of the submitted author's disclaimer.

In contrast, OWR printed 114, Definition 1 immediately preceding Question 5, explicitly requires both connected open domains and trivial restrictions of the entire cover. The rest of Question 5 and its continuation on 115 were read. The report records a historical 3-to-9 bound and motivation from algorithmic lower bounds. A literal reading of this definition is stronger than choosing one local sheet. Its comment relating the invariant to sectional category points toward the conventional intended terminology, but does not erase the written requirements. The original historical intent cannot be conclusively reconstructed from these texts alone, and no outreach was attempted or prepared.

Accordingly:

| Target | Disposition, conditional on valid upper and lower bounds |
|---|---|
| Complete curated coefficient-space problem, with ordinary Schwarz genus as clarified by its Chen–Wan 8-versus-9 background | Settled by genus 8 |
| Chen–Wan Conjecture 1.3 in arXiv v2 | Settled by the same theorem |
| Literal OWR connected/full-nine-sheet trivialization minimum | Not determined by the manuscript |
| Exact minimum branching-node count for flex-finding algorithms | Not determined |
| A theorem on the coarse PGL3 moduli quotient | Not the stated target; no such result is established here |

Thus, if both bounds are valid, this would be a full resolution of the *curated section-genus target*, rather than a narrowed substitute for that curated statement. Relative to the *literal original OWR definition*, it is a strictly scoped result and must be described that way. A `claimed_solved` label would also require a secure lower bound after the dependency challenge is resolved; the invariant qualification must remain bound to it.

The gap between the invariants is concrete. A local section fixes only one point in the fiber; a trivial nine-cover requires trivial monodromy on all nine points. The displayed element C has fixed flexes and nontrivial three-cycles on others. Projectively it is conjugate to an element of the selected circle. A path in that circle ending at this isotropy element gives a loop on the orbit with nontrivial full-fiber monodromy. Therefore the orbit-neighborhood section mechanism does not simultaneously label every sheet. The color-domain gluing also does not establish connectedness. These observations explain the qualification; they do not compute the stronger minimum.

## Space and cover: coefficient equations, not coarse moduli

OWR Question 5 and the earlier Chen contribution printed 69–71 define the same coefficient parameter space. Chen’s earlier contribution introduces the universal cubic curve over homogeneous equations modulo scalar and its flex multisection. Neither of these cubic parameter spaces is divided by changes of projective coordinates. The neighboring OWR quartic discussion on 115 explicitly introduces a PGL3 quotient for a different problem; that definition must not be imported into Question 5.

Chen–Wan arXiv v2 page 1 defines precisely this X, and page 2 identifies it as CP9 minus the discriminant. There are ten cubic coefficients, with only their common nonzero scalar removed. The nine-flex incidence is an actual degree-nine covering in the usual complex topology. In characteristic zero the flex scheme on a smooth cubic consists of nine distinct points; locally in a smooth family it is a finite étale 3-torsion torsor after choosing a local origin. This gives the genuine local sheets. Special smooth cubics with additional projective automorphisms do not change this statement over the coefficient space. A coarse projective-moduli quotient can identify points through such automorphisms, and should not be substituted as the base of this ordinary cover.

Chen–Wan’s page 1 definition counts the least number of open sets with continuous sections. It places no connectedness requirement on these domains. This is the unnormalized convention; subtracting 1 gives normalized sectional category. The submitted author’s 8 and 7 are therefore consistently normalized.

## Chen–Wan theorem and the absence of circularity

All 10 pages of arXiv:2306.17303v2 were read, including sections 1–6 and references. The theorem actually used is Theorem 4.1, printed 5: the flex cover over this X has ordinary genus at least 8. Theorem 1.2 on 2 states lower 8 and upper 9, and Conjecture 1.3 proposes equality 8. The lower-bound dependency is not an assumed version of that conjecture.

The lower-bound chain is explicit. Proposition 4.2 on 5 asserts nonzero degree-seven pullback from BK for the principal translation cover PU3→PU3/K, with K=C3×C3. Its proof runs through the central circle extension of K, Leary’s cohomology computation (Theorem 4.3 on 6), and the universal U3 transgression calculation on 6–7. The general genus lower bound, Theorem 2.4 on 3, is applied to this **principal K-cover**, so its regular/Galois hypothesis is not silently applied to the nonregular flex cover. The Fermat orbit map PU3/K→X pulls the flex cover back to that principal cover because K acts freely and transitively on the nine flexes. Pullback monotonicity, Proposition 2.1, then purports to give the required lower 8 for X; the validity challenge is discussed in the final addendum.

None of this lower-bound chain uses Theorem 3.1’s upper 9, Conjecture 1.3, Proposition 6.1’s obstruction criterion, Proposition 6.4’s upper 8 for the smaller K-cover, or the submitted circle-isotropy construction. There is no circular dependence on the missing upper 8.

The same lower input also applies to the compact homogeneous cover PU3/Γ0→PU3/Γ: pull it back along PU3/K→PU3/Γ. Since K acts transitively on Γ/Γ0 and K∩Γ0 is trivial, the pullback is PU3→PU3/K. If Proposition 4.2 is valid, this supplies compact-model lower 8 independently of the unknown global upper 8. The source is not asserting that X itself is homotopy equivalent to PU3/Γ.

The lower theorem is an external mathematical dependency, not a cohomology computation independently re-proved by this source audit. No added hypothesis on generic j-invariant, a free Γ-circle action, or a full-sheet trivialization is needed for its stated application. A printed inconsistency was noticed in v2: Theorem 4.3 displays c2y′ with x², whereas equation 4.9 uses x′² in the corresponding calculation. This audit records the inconsistency without claiming to repair or recertify Leary’s theorem. It does not turn the independent lower-bound theorem into the unresolved upper-bound conjecture.

Section 5 is a separate algorithmic discussion. Its claim that the Fubini–Study metric is invariant under all PGL3(C), printed 7, is false: a nonunitary diagonal projective transformation changes angles/distances. It must not be imported as an algorithmic certificate. This issue is outside the lower-bound proof in section 4 and outside the submitted genus upper bound. Even a valid genus-minus-one algorithmic lower bound would not by itself give a matching algorithm or exact branching equality.

## Hesse quotient and polar pullback: exact locators

The classical normal form and common flex configuration are in Chen–Wan section 2.2, printed 3–4, with matrices A, B, C, D in (2.4). The order 216 special affine group and point stabilizer 24 are the groups needed by the submitted proof.

The actual coefficient and incidence quotients are Chen–Wan Lemma 3.2 and Proposition 3.3, printed 4. With P=PGL3(C) and T=C minus the three singular finite Hesse parameters, they give X=(P×T)/Γ and Y=(P×T)/Γ0. The diagonal convention pairs right multiplication on P with the inverse action on the parameter. The proof of Theorem 3.1, printed 4–5, then exhibits pullback from P/Γ0→P/Γ and passes to the compact PU3 quotient. Proposition 3.3 alone is the noncompact quotient statement; the compact reduction should be attributed to section 3 as a whole or specifically to the proof of Theorem 3.1.

The author’s polar formula provides the right-equivariant map needed to make the compact pullback explicit. The unitary factor M(M*M)^(-1/2) changes by a unit scalar when M is rescaled, and satisfies r(MU)=r(M)U for unitary U. Thus it descends to P and is right-Γ-equivariant. The map [(g,λ)]↦r(g)Γ sends X to PU3/Γ; the matching total-space map sends [(g,λ)] to r(g)Γ0 and is a bijection on each nine-point fiber. This is compatible with an actual covering pullback. It does not require or assert that the nonfree circle quotient of the total space is itself a cover.

Artebani–Dolgachev was checked for source linkage, rather than used as a substitute for the separate finite-group audit. Relevant text is section 2, printed 238–240 (nine common flexes and Lemma 2.1 with proof), and section 4, printed 246–248 (generators, Proposition 4.1 and point stabilizer). Proposition 4.1 gives the semidirect product by the natural SL2(F3) action. The next paragraphs explicitly distinguish this order 216 group from the full affine group of order 432. The submitted proof uses the correct smaller group. Chen–Wan’s displayed identification of the entire affine-configuration automorphism group with the special affine group should not be generalized to erase that index-two distinction. AD uses different point labels/coordinates and reuses Γ for its translation subgroup and K for a larger pencil-action kernel; these symbols should not be copied across papers without translation. The submitted A, B, C and p0 are directly linked by CW (2.4), avoiding that notation collision.

## Illman’s exact applicability

The complete digitized article is available from the Göttingen archive: 22 mathematical pages plus one archive cover sheet. This auditor visually read printed 199–202 and 216–218, not the entire article.

The opening theorem on 199 supplies an equivariant triangulation for a smooth action of a finite group on a smooth manifold, with or without boundary. Section 1 on 201 describes the quotient of an equivariant simplicial complex as an ordinary simplicial complex and says each simplex projects homeomorphically to its image simplex. Theorem 3.6, printed 216–218, gives the existence statement for smooth invariant manifold pairs, including the needed manifold case.

Here H\PU3 is a compact smooth 7-manifold and Γ acts smoothly on the right. The theorem allows finite isotropy; it does not require a free Γ-action. Consequently its quotient is a polyhedron of dimension at most 7. This is the justified source route to the manuscript’s dimension bound. The reasoning does not use an invalid generic claim that every continuous quotient of a 7-dimensional space has dimension at most 7. Standard finite-dimensional cover refinement and partitions of unity remain ordinary foundational inputs.

The author freeze’s statement that Illman full text had not then been retrieved is historically preserved. The first earlier audit’s later addendum reports recovery of the article. This audit independently inspected the same scanned primary source. No author, review, or frozen metadata files were rewritten.

## Current bibliography and access limits

- **Weiyan Chen and Zheyan Wan**, *Topological complexity of finding flex points on cubic plane curves*. The inspected theorem source is [arXiv:2306.17303v2](https://arxiv.org/pdf/2306.17303v2), 10 pages, revised 21 July 2023 at 20:59:16 UTC; v1 was submitted 29 June 2023 at 21:03:17 UTC. The [current arXiv record](https://arxiv.org/abs/2306.17303) still lists v2 and the journal reference **Proc. Amer. Math. Soc. 153(2025), no. 5, 2255–2267**, [DOI 10.1090/proc/17184](https://doi.org/10.1090/proc/17184). Author/institutional records corroborate issue 5. Crossref’s publisher-deposited record gives online publication 5 March 2025 and record creation 30 December 2024; creation is not the issue date. The final page span is 13 pages and is not evidence of any particular textual change.
- Standard public retrieval was attempted at the correct AMS article/PDF paths, the Crossref-registered version-of-record path, and corresponding `/journals/` variants. All five returned 403; web retrieval also failed. The [author research page](https://www.weiyanc.com/research) links the same arXiv preprint and DOI, with no separately available final text found there. **The final article was not read or compared.** No inference is made that its definitions, theorem numbering, section 5, or the printed inconsistency are unchanged or corrected.
- The source report is [*Topology of Arrangements and Representation Stability*](https://ems.press/journals/owr/articles/15987), **Oberwolfach Rep. 15(2018), no. 1, 43–123**, DOI 10.4171/OWR/2018/2. Workshop 14–20 January 2018; the publisher page reports publication 5 January 2019, whereas Crossref reports 4 January 2019. The 2018 volume/workshop date and 2019 publication date explain the curated citation’s two years; neither is silently replaced.
- **Michela Artebani and Igor Dolgachev**, *The Hesse pencil of plane cubic curves*, Enseign. Math. (2) 55 (2009), 235–273, [DOI 10.4171/LEM/55-3-3](https://doi.org/10.4171/LEM/55-3-3); primary [publisher PDF](https://ems.press/content/serial-article-files/44190).
- **Sören Illman**, *Smooth equivariant triangulations of G-manifolds for G a finite group*, Math. Ann. 233 (1978), 199–220, [DOI 10.1007/BF01405351](https://doi.org/10.1007/BF01405351); primary digitized [archive PDF](https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0233/LOG_0044.pdf).
- The metadata’s later related work is **Weiyan Chen and Xing Gu**, *Topological complexity of enumerative problems and classifying spaces of PU_n*, **Bull. Lond. Math. Soc. 58 (2026), no. 6, e70415**, online 9 June 2026, [DOI 10.1112/blms.70415](https://doi.org/10.1112/blms.70415), [arXiv:2411.00497v1](https://arxiv.org/abs/2411.00497), submitted 1 November 2024. Current primary abstracts/metadata concern cubic-surface lines and quartic bitangents/flexes. Only metadata/abstract scope was checked here; no full-paper or broad priority search was performed. This work is not a theorem dependency and is not evidence of an exhaustive absence of an earlier cubic-flex genus resolution.

## Receipts, required wording, and disposition

SOURCE_RECEIPTS.json gives precise inspected extents, all four primary PDF sizes and hashes, current version/publication metadata, dataset statement/review receipts, and failed final-text routes. The fresh arXiv v2 retrieval is 173395 bytes with SHA-256 be48f13fbffd76508dff6b37f8becc853c9a3f1c80e4068b2ee5652c36c1bbc8, matching the original pin. Source identity checks do not substitute for the content reading recorded above.

The target-definition qualifications in the frozen package are appropriate. The newly audited lower-bound dependency requires repair or an independently valid justification before promoting exact equality. Mandatory continuing rules for any integrated disposition are:

1. Bind genus 8 to ordinary unnormalized **section-based** genus on CP9 minus the cubic discriminant; normalized value 7.
2. Say the curated Chen–Wan 8-versus-9 target is resolved, conditional on mathematical acceptance; do not claim the literal connected/full-trivialization OWR minimum was computed.
3. Preserve the absence of an exact algorithmic branching-complexity equality and of a novelty/priority certification.
4. Cite the inspected arXiv **v2** for exact theorem/definition locators and state that the final journal text was not obtained. Update access records additively; do not rewrite historically accurate earlier limitations.
5. Do not call coefficient space the coarse PGL3 moduli space without an immediate clarification of what “moduli” means.

All scholarly PDFs, text extractions, renders, raw metadata responses and the complete dataset record remain in ignored private locations and are excluded from the public manifest. No communication with individuals, service/PR/queue changes, Git/index/branch operation, commit, push, or release was performed by this audit.


## Reopened dependency check: degree-seven lower-bound calculation

The source-scope match does not validate a theorem merely because the theorem has appeared in a journal. An independently checkable concern arises in the inspected arXiv v2 Proposition 4.2(1), which asserts that the characteristic map c:M=PU3/K→BK is nonzero on H7 with F3 coefficients. The following diagnostic tests that precise assertion, rather than declaring the lower-bound theorem false.

1. The preimage of K in SU3 is the order-27 Heisenberg group generated by lifts of A and B. Their commutator is a nonidentity scalar cube root of unity. Consequently the abelianization is K and c*:H1(BK;F3)→H1(M;F3) is an isomorphism, with basis the pullbacks of y and y′.
2. M is a closed connected orientable real 8-manifold: it is a quotient of the connected oriented Lie group PU3 by finite right translations, which preserve orientation. Its mod 3 Poincaré pairing H7(M)×H1(M)→F3 is nondegenerate.
3. The v2 source identifies c1 with yy′ in H2(BPtilde;F3), and its pullback to M is zero. The vanishing is also geometric: the associated rank-three bundle over U3/Ptilde is trivial because the representation extends to U3. Thus c*(yy′)=0.
4. Every degree-seven class of H*(BK;F3)=Λ(y,y′)⊗F3[x,x′] has exactly one exterior generator. Its product with either y or y′ is zero or divisible by yy′. After pullback, it therefore pairs to zero with both basis elements of H1(M).
5. Poincaré duality would then imply c*H7(BK;F3)=0, in conflict with the printed Proposition 4.2(1).

These are concrete structural checks on the source argument. They leave two important distinctions: failure of this displayed constant-coefficient detector would not prove that the genus lower bound itself is false; and the inaccessible final paper could contain a different proof. The contradiction needs adjudication in the separate mathematical lower-bound audit. This source audit cannot treat the cited v2 lower bound as an unquestioned verified input while that contradiction remains unresolved. No additional hypothesis on the base or a connected-domain convention resolves this issue, and there is still no circular dependence on an upper bound.

A valid independent lower bound, a justified correction to the detector calculation, or inspected final text containing a valid replacement would resolve this dependency gap. Until then, the strongest claim supported by the submitted new construction is genus at most 8, conditional on verification of that construction; exact equality 8 is on hold.

### Final-text and correction search after reopening

The correct official AMS identifier is S0002-9939-2025-17184-2. Five standard article/PDF paths had returned 403, and a standard full-text HTML path also failed. Both authors’ public records were inspected: Chen’s research page provides the arXiv preprint and DOI; Wan’s institutional CV likewise points to arXiv, and the personal page did not provide a final article copy. Crossref’s deposited record has no update-to or correction relation. Discovery-only checks of OpenAlex and Semantic Scholar led only to the same submitted arXiv version; these indexes are not used as theorem authorities. Targeted title/arXiv/DOI searches did not identify an explicit correction or a separately accessible authorized final text. This is a bounded retrieval result, not an assertion that no correction or authorized copy exists. No access controls were bypassed and no outreach was prepared or initiated.

The current arXiv record remains v2, 21 July 2023, and the fresh versioned PDF matches the original pin. There is no basis to call that 10-page file the 13-page published final or to assert whether the final retains or repairs the degree-seven argument. Source access has therefore not removed the dependency gap.

### Obstruction-class scope

CW section 6 discusses the eightfold join of the nine-point fiber. Its first possible section obstruction is degree 8 with coefficient module Htilde0(F;Z) tensor-powered eight times, of rank 8^8. This large coefficient rank is not itself a computation of the obstruction class. A verified explicit eight-domain section cover gives a section of the join bundle and forces its primary obstruction to vanish without calculating that group or class. The submitted upper construction does not need CW’s converse obstruction criterion or an assumption that arbitrary higher obstruction choices vanish. None of this supplies the missing independent lower bound.
