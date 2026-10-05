# Independent audit of the inverse Frobenius counterexample

Problem 30005356, OWR-12697685-001, catalogue rank 778. Audit date: 5 October 2026.

## Verdict

PASS for the literal assertion without a characteristic restriction. The frozen argument proves that every positive-characteristic ACFH model has a parameter-free definable multiplicative endomorphism outside Z[theta]. The proof has no identified mathematical gap. The independent reconstruction in INDEPENDENT_PROOF.md supplies an additional self-contained existence argument and spells out the existential witness without an inverse-function symbol.

The author freeze is preserved unchanged. Its SHA-256 is b5d4c852204b60d7a91cfa0d1c6125bd9deac64d460fc1a0f49a196df01a9d96, its size is 16,791 bytes, and it contains nine files. Every manifest entry and both original verification programs were checked from a fresh extraction.

This is an independent AI audit, not formal proof-assistant certification or human peer review. Neither novelty nor editorial acceptance is asserted. The characteristic-zero and positive-characteristic localized-coefficient classifications remain unresolved by this work.

## Source scope

The entire two-page OWR contribution, printed pp. 97-98, was independently read and visually inspected after a fresh publisher download. Its setup places no restriction on characteristic, and its polynomial ring is integral. The motivation involving complex ultraproducts does not restrict the preceding theory. Source: https://ems.press/content/serial-article-files/46996

The latest version shown in the live arXiv submission history was v4, revised 17 January 2025. Its introduction, global notation, positive-characteristic discussion, and complete Section 5.1 were checked. PDF pp. 22-25 were also visually inspected. The definition on pp. 22-23 uses definable endomorphisms of K* and explicitly defines Z[theta] as the image of Z[X]; Question 5.8 uses this ring. The introduction on p. 4 states the conjecture for any ACFH model. No fixed-characteristic-zero convention, implicit localization, or semiring replacement was found. Source: https://arxiv.org/abs/2212.02115v4

The quantifier-free graph y^p=x is a definition of a function because p-th roots are unique in characteristic p. It does not need to be a term or a regular morphism of algebraic groups. The source asks about definability, so those stricter notions cannot silently replace its target. Allowing or disallowing parameters makes no difference to this counterexample.

The journal landing-page retrieval returned 403. The inspected full research article is the versioned arXiv PDF; no comparison against inaccessible final journal full text is claimed. The publication identity is Annals of Pure and Applied Logic 176(4), 103554 (2025), https://doi.org/10.1016/j.apal.2025.103554 .

## Mathematical stress tests

1. Non-vacuity passes. Corollary 3.16 embeds the algebraic closure of F_p with an identity operator into an ACFH model, preserving p. Independently, the chain construction in INDEPENDENT_PROOF.md produces an existentially closed positive-characteristic T-model directly.
2. The abelian-group extension lemma passes. The least-positive-exponent case handles every relation by the subgroup nZ of integer exponents. Divisibility of the codomain suffices; no field-additivity assumption is introduced.
3. The free-iterate extension passes. Algebraic independence makes H the indicated direct product, so prescribing successive generator images is compatible with theta on K*. The extension has values in L*, hence it preserves nonvanishing. Its behavior outside H is unrestricted in T.
4. Existential transfer passes. After negative powers are cleared, a witness to Q(theta)(x) != 1 is a single existential formula with a quantifier-free matrix. It holds in a T-extension and therefore in an existentially closed base. Constants, negative coefficients, p-divisible coefficients, and degree zero are all covered.
5. The endomorphism-ring conventions pass. Ring addition is multiplication of values; ring zero is the constant-one map; integer p is Frobenius. The field equation p*1_K=0 does not make the endomorphism [p] zero. The ring itself has characteristic zero by polynomial faithfulness.
6. Definability and multiplicativity pass. Algebraic closedness gives a p-th root, field reducedness gives uniqueness, and uniqueness proves multiplicativity. The extra additive and commutation claims in the freeze also follow from uniqueness and are correct.
7. Exclusion from Z[theta] passes. The relation rho=P(theta) gives (pP-1)(theta)=0. Injectivity contradicts the nonzero integer constant coefficient p a_0-1. This is a global functional argument and is not inferred from finite simulations.
8. The localized inclusion passes. Inverting the central Frobenius map yields a faithful copy of Z[1/p][X]. This proves an inclusion, not a classification. No result about characteristic zero follows.
9. Semiring and naming ambiguities do not rescue the unrestricted assertion. The inspected definitions specify a ring over Z. A restriction to nonnegative coefficients would be a smaller proposed collection and still miss rho. A change to Z[1/p] would be a genuinely different question, expressly left open here.

## Independent computational checks

The audit program implements finite fields by general polynomial reduction, independently of the author's quadratic-field implementation. It exhaustively checks uniqueness of the p-th-root graph, additivity, multiplicativity, and commutation with every power endomorphism on fields of orders 4, 8, 16, 9, 27, 25, and 49. Modulus irreducibility is checked by exhaustive monic trial division. It checks 117,642 integer coefficient vectors for pP-1 and 19,602 nonzero free-shift vectors.

Two deliberate controls prevent misleading conclusions: [p] is checked not to be the ring-zero map, and inverse Frobenius is checked to equal an integer power on each finite test field. The latter demonstrates why these tests cannot establish non-polynomiality in an ACFH model. None of the finite fields is claimed to model ACFH. The proof is the written universal argument.

## Provenance and correction

The complete public problem and research-report corpora were independently hashed and parsed. Their sizes and hashes match both a freshly retrieved pinned Hugging Face LFS tree and the repository manifest at the stated commit. The selected identity, index, canonical record hash, statement hash, rank, and exact absence of the prior-report key were checked. A fresh selected-row retrieval provides an additional live identity check; it is not claimed to be bound to an immutable revision.

The only requested addendum is provenance: the author freeze omitted the catalogue review hash. It is 00c719d497159151748580b116c2a138f20956fbd106b60808c144bf4ca63de8. It was independently reconstructed using the repository's actual recipe, SHA-256 of UTF-8 json.dumps([problem_record, {}], sort_keys=True) with other Python defaults. The empty dictionary is the normalization for an absent prior research report; null would give a different hash. PUBLIC_EVIDENCE_RESULTS.json records the verified value. No mathematical correction to the author proof is required.

Fresh bounded repository searches found no target PR, branch, indexed code, or commit under the exact-ID/code/topic queries recorded in SOURCE_AUDIT.json. Existing author receipts for the attempts-tree and related-target check were also inspected. These checks do not prove that no unpublished, deleted, or unindexed attempt exists. The dataset's dated open-status label is background and was not used as mathematical evidence.

The current arXiv version history, the author's public publication list, and a bounded targeted search did not reveal a later correction or resolution of this exact question. This establishes no novelty claim. The named 2025 article is the paper used for scope and existence, not a later independent endorsement of this counterexample.

## Publication boundary and stopping point

The packet contains authored proof, authored audit, authored programs, exact-control outputs, and public verification metadata only. No source PDFs, rendered source pages, extracted scholarly text, raw datasets, selected raw records, or private coordination files are included. No remote write was performed.

One substantive proof approach was used in the author work. The audit did not continue proof search on the two remaining classification variants. Its stopping condition is met: the specific frozen claim has been independently checked, the provenance omission is repaired in this addendum, and the safe packet is reproducible and integrity-checked.
