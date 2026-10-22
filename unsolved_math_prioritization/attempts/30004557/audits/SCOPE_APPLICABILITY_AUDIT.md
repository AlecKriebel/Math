# Independent source and applicability audit

Problem 30004557 / OWR-2654830-012, queue rank 452.
Audit date: 2026-10-03 UTC.
Frozen author-manifest SHA-256: `554df04a0a694bc49234aeb92ff84269b72854b7183f76865d1ad7be1357da2b`.

## Decision

**HOLD: the frozen packet does not establish that the original constructive question is already resolved.**

**PASS, in a narrower and useful sense:** the packet correctly identifies the established ordinary coherent Morita characterization, correctly credits Dimitris Tsementzis, and substantially correctly matches Lombardi's elementary extension rules to coherent definitional and sort extensions. Its direct forward argument is sound in pretoposes, subject to an explicit functor convention. The standard coherent result should be retained as credited prior work.

These are different audit questions. A known result for coherent theories in the usual categorical metatheory is not, solely because the object logic is constructive, an established answer to the constructive-mathematics scope of Lombardi's question. Conversely, this audit does not establish that the original question is mathematically open, or demand a new theorem in a particular named foundation. It finds an unclosed applicability gap in this packet.

No `already_solved`, original-scope `PASS`, or prior-resolution-at-zero-turns disposition is supported by the supplied evidence. The packet's zero substantive original proof-attempt count is supportable as preparation accounting: the five-turn attempt budget remains unspent. A source repair may still establish an existing resolution without spending original proof turns; otherwise a substantive constructive bridge must be attempted and recorded honestly.

## Evidence and integrity

All seven entries of `AUTHOR_MANIFEST.json` match their frozen SHA-256 and byte count. All four source PDFs match `SOURCE_MANIFEST.json`. The audit did not change author files. It reran `verify_finite_controls.py`; all 2,032 advertised controls passed, with the same category counts as the frozen verification output.

Primary material inspected:

1. Henri Lombardi, *Geometric theories for constructive algebra*, OWR 34/2020, printed pp. 1744–1747, particularly pp. 1744–1746. The report is [DOI 10.4171/OWR/2020/34](https://doi.org/10.4171/OWR/2020/34). The exact question is an unnumbered sentence on p. 1746, not a separately titled theorem.
2. Lombardi–Mahboubi, *Valuative lattices and spectra*, [arXiv:2210.16558v3](https://arxiv.org/abs/2210.16558v3), especially English pp. E19–E22, §§3.2–3.3. The external-foundation discussion immediately before the extension rules is material evidence, not background to omit.
3. Tsementzis, *A syntactic characterization of Morita equivalence*, [arXiv:1507.02302v1](https://arxiv.org/abs/1507.02302v1), pp. 3–6, 7–9, 14–16, and 22–23. The journal [record](https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/abs/syntactic-characterization-of-morita-equivalence/2AB10C921C8084665316509AA6B3267D) independently confirms single authorship, JSL 82(4), 1181–1198, DOI 10.1017/jsl.2017.59, and publication online on 9 January 2018. No full published proof was obtained during this audit.
4. D'Arienzo–Pagano–McInnis, *Bicategories, Biequivalence, and Bi-Interpretability*, [arXiv:2011.14056v2](https://arxiv.org/abs/2011.14056v2), §6.3, printed p. 40. The arXiv record confirms the 9 July 2023 revision and the correct current authors/title.

The OWR question page, Lombardi–Mahboubi E19, and Tsementzis p. 5 were also rendered from the verified PDFs and visually checked. This confirms the decisive text and sort restriction independently of text-extraction formatting.

The live catalogue detail page was not independently read. Its pinned record was read only as catalogue evidence; its prior `open` label is not a mathematical premise. The mistaken catalogue coauthor attribution to Rynasiewicz is correctly rejected. No remote write, contact with authors, or retry of the cancelled source-PDF retrieval was made. A bounded current primary-source search did not yield an explicit author-issued closure of the constructive question; this is not a claim that none exists.

## 1. Exact original scope

### 1.1 What is clear

OWR p. 1745 identifies the finitary dynamical/coherent fragment. Premises are finite lists of atomic formulas; each rule has a finite disjunction of branches, each with finitely many existential witnesses and atomic conclusions. Empty disjunctions are permitted. The context of a sequent does not add universal quantification to the permitted formula constructors.

The four listed extension families are abbreviations, positive logical constructors, uniquely specified terms, and Bishop-style subsorts, quotients, finite products, and finite disjoint unions. Classical logic and Skolemization appear subsequently as separate headings. The certificate correctly keeps them separate.

The source does not define constructive Morita equivalence formally. It also does not explicitly ask for equivalence of Set-model categories, ordinary single-piece bi-interpretability, a finite total signature, or a theorem formalized in CZF, IZF, or a particular type theory. None of those should be silently inserted.

### 1.2 Why constructive metatheory cannot be dismissed as an optional stronger target

The original OWR contribution does more than choose intuitionistic object syntax. Its general aims on p. 1744 include avoiding nonpredicative definitions and obtaining a constructive treatment of Grothendieck toposes and their equivalence with geometric theories. On p. 1746 it explicitly situates the sort constructions in Bishop set theory.

More decisively, Lombardi–Mahboubi E19 says that the external reasoning about dynamical algebraic structures is conducted in informal Bishop set theory. At the beginning of §3.3 it distinguishes its intuitive Bishop sets of language symbols and axioms from the formal ZFC framework usually used in categorical logic. This is the same later source that the certificate relies on for the exact extension rules. One cannot import its rules while treating its explicit foundational setting as unrelated.

This does **not** justify imposing an arbitrary stronger target such as a machine-checked CZF formalization, a recursive decision procedure for Morita equivalence, or a uniform algorithm for every presentation of a topos. The minimum repair is narrower: explain why the cited converse and the chosen meaning of Morita equivalence can be used in the source's constructive setting, or find an explicit source establishing that identification. The frozen certificate currently disclaims precisely that bridge.

Accordingly, CERTIFICATE §6 should not frame constructive external mathematics solely as an alternative intended reading with no source support. There is direct support for it. The absence of a named formal axiom system limits what can be demanded, but does not erase the demand for constructive justification.

## 2. Rule-by-rule audit

The following passes concern the elementary rule bridges, not the converse theorem or global source applicability.

### Abbreviations: PASS

A term abbreviation is removable by substitution. Naming a relation by an already coherent formula with both implication sequents is an explicit coherent definition. This is exactly the role of Lombardi–Mahboubi's introduction and elimination rules. Names and substitutions must be hygienic; no new axiom about old symbols is introduced.

### Conjunction, disjunction, and existential constructors: PASS

The source gives introduction and elimination rules. With finite arity and recursive application, they name arbitrary coherent formulas. For disjunction, elimination branches rather than supplying a logical disjunction among antecedents. For existential quantification, the syntactically similar rules have different roles: one names the existential formula, the other supplies local witnesses. Their coherent interpretation is correct.

Finite conjunction/disjunction must include the source's truth/falsity conventions. No arbitrary implication, negation, or universal formula constructor enters this bridge.

### Unique-existence functions: PASS

Given proof of totality and single-valuedness for R(x,y), adding R(x,y) entails y=f(x) yields the full graph definition. A totality witness z gives R(x,z), then z=f(x), and equality substitution gives R(x,f(x)); substitution then gives the reverse graph implication. This argument is intuitionistic and local in the context. It does not choose an arbitrary witness of a nonfunctional relation and does not give quotient representatives.

### Subsorts: PASS

Lombardi–Mahboubi's inclusion j:U→A, image membership, image coverage, and definition of U-equality by equality under j translate into a mono whose image is exactly the definable predicate. Tsementzis's `(sub1)` and `(sub2)` say the same in coherent notation. An empty predicate is allowed; no inhabitance premise is added by the bridge.

### Finite products: PASS, with the nullary convention recorded

The source uses projections, equality determined by projections, and a tuple constructor. Coherent product existence and uniqueness follow immediately. Conversely, existence and uniqueness define the tuple function by the allowed unique-existence extension. The identity u=Pr(pi_1(u),...,pi_n(u)) follows from coordinate equality, so there is no missing product axiom.

For n=0 the source-style constructor is a constant and equality is the empty conjunction, yielding exactly a terminal singleton sort. The certificate's choice to include n=0 is the ordinary meaning of finite products and is mathematically coherent. The original short question does not separately state the convention, so it must remain explicit, particularly when using it to remove a preprint hypothesis.

### Effective quotients: PASS

The two source implications between E(a,b) and q(a)=q(b), together with q's internal surjectivity, are the effective-quotient axioms. The kernel pair is the specified relation. In a pretopos, the surjection is a regular epimorphism and realizes its coequalizer. If the original sort is empty, the quotient is empty. Neither the axioms nor their semantics produce a section Q→A.

### Finite disjoint sums: PASS

The source axioms are injectivity, pairwise disjointness, and a cover by a disjunction whose branches each carry their own existential witness. The certificate correctly retains this placement. Pulling every summand's witness outside the disjunction is invalid when a summand can be empty. With zero summands the cover forces an initial sort; equivalently an initial sort is a false subsort of the terminal sort.

## 3. Forward categorical implication

**PASS in the stated categorical setting.**

For a T-model in a pretopos, the new sorts exist by the relevant finite limits, disjoint finite coproducts, and effective quotients. A total single-valued coherent relation has projection to its domain both mono and regular epi, hence is invertible; it defines the unique function. Any expansion is uniquely isomorphic over its reduct to the canonical construction.

A homomorphism preserves coherent formulas. It therefore induces maps on subsorts, products, sums, and unique-function graphs. For a quotient, q_N h coequalizes the relation on M and factors uniquely through q_M. This proves fullness and faithfulness as well as essential surjectivity of the reduct. Identity and composition follow by uniqueness. This is stronger and more appropriate than a bijection on model isomorphism classes.

One terminology correction is required. The sentence that exact functors between pretoposes preserve all the constructions is ambiguous and false if exact means merely Barr-exact/regular. For example the constant-terminal functor Set→Set preserves finite limits, regular epimorphisms and equivalence-relation quotients, but not the empty object or binary coproducts. Say **pretopos functors**, or explicitly coherent functors preserving disjoint finite coproducts and effective quotients. Inverse-image functors of geometric morphisms do preserve the required constructions, so the intended topos-pseudonaturality conclusion is unaffected.

This is a valid constructive-style categorical argument relative to the ambient category and its operations. It does not by itself prove that the category of all source-intended constructive models is the selected categorical environment, or construct all the syntactic/pretopos/topos machinery in Bishop mathematics.

## 4. The known converse and the inhabited-sort issue

### 4.1 Established ordinary result: PASS

The preprint's Theorem 4.7 equates its syntactic T-Morita relation with equivalent classifying toposes; Corollary 4.8 gives model-category equivalence natural in arbitrary Grothendieck toposes, and Corollary 4.9 gives the pretopos formulation. The 2023 D'Arienzo–Pagano–McInnis statement expressly attributes the coherent Morita/pretopos characterization to the **published Theorem 3.9** of Tsementzis. The certificate's separation of numbering and its attribution are correct.

This is good evidence for the ordinary categorical theorem. Reading the full journal proof is not an absolute prerequisite to citing it. But a restatement is not evidence that a particular changed convention was checked unless its hypotheses or proof resolve that change.

### 4.2 Literal preprint application to all the source's sorts: HOLD

Tsementzis p. 5 explicitly permits empty subsorts but requires the *base sorts used to define each new sort* to be provably inhabited, and it requires each theory to have an inhabited sort. These are distinct restrictions. Adding a singleton removes the second restriction; it does not make every old sort inhabited and does not remove the first.

Lombardi–Mahboubi has no such base-sort restriction. Therefore “the source uses coherent logic” is not enough to apply the preprint literally. Nor may an uninhabited sort be replaced by a nonempty one: that changes the theory. The packet correctly flags this issue, but its flagged status must have consequences for closure.

### 4.3 The proposed completion mechanism: sound roadmap, insufficient original-scope certificate

The normal form `(finite coproduct of coherent definable tuple objects)/E` is the standard exact/pretopos-completion mechanism. It naturally accommodates empty definable objects and empty contexts. It makes a convincing explanation for why the unrestricted ordinary coherent theorem has the same generators. The expected direct route is:

1. Add all finite tuple products, including the empty tuple object, in one set-indexed stage.
2. Add the definable subobjects of those tuple objects.
3. Add finite disjoint sums of those definable objects.
4. Add quotients of the definable equivalence relations on such sums.
5. Add the needed function and relation names by provably functional graphs and coherent predicate definitions.

This is finite **stage** complexity even when the language and the family of definitions are infinite. It does not require adding an element to an empty old sort.

However, the frozen packet does not prove the requisite closure/normal-form theorem, nor does it prove that simultaneous presentations, arrows and subobjects, and comparison isomorphisms yield a common finite-stage definitional extension on both sides. It gestures at those established mechanisms. That is satisfactory explanatory background to the ordinary theorem, but cannot simultaneously be treated as a new constructive proof that repairs the restrictions and foundations. A repaired certificate needs an exact reference with matching hypotheses or enough explicit construction to discharge those claims.

The nullary convention is genuinely relevant. If only positive-arity products/sums were allowed and all old sorts were empty, the listed operations could never introduce an inhabited singleton. A theory with just a necessarily empty sort and the corresponding theory expanded by a singleton have the same usual classifying topos but would not be connected by those artificially restricted positive-arity operations. This is a convention-control example, **not** a counterexample to the original problem, whose natural finite-product convention includes arity zero.

## 5. Finite chains, language size, and equivalence relations

The preprint explicitly defines finite Morita chains and spans, then deals with renaming/transitive closure. The 2023 §6.3 warns that n-ary products and coproducts must be addable at once. This matters for infinite languages: finitely many elementary stages may add infinitely many independently defined symbols, and there is no bound on the largest finite arity across the stage.

The certificate correctly rejects a finite-total-signature requirement. Its sentence permitting well-founded finite-depth construction stages is nevertheless too loose. Every individual new symbol can have finite depth while the collection has unbounded depths; that alone does not establish a globally finite chain. Replace it by a genuine finite-stage convention, or prove a uniform normalization such as the tuple/subobject/sum/quotient construction above. The certificate should not equate these alternatives by assertion.

The original question speaks informally of intuitively equivalent theories; Lombardi–Mahboubi Definition 3.3.6 describes a common extension, up to renaming. The packet's equivalence relation generated by operations is a natural formalization, but the finite zigzag/common-span equivalence must be stated and justified if it is used. Theory-language collisions should be removed by tagged fresh copies, rather than suppressed. A proof of common extension must exhibit expansions conservative over each original theory; adding arbitrary comparison axioms to a combined language is not sufficient on its own.

## 6. Semantic versus syntactic equivalence

The packet makes the right distinctions:

- Same provable old-language rules is conservativity; it is not by itself a converse Morita theorem.
- Equivalence of categories of models in Set alone is not the relation characterized here.
- The semantic statement needs equivalence in every Grothendieck topos with the appropriate pseudonaturality, or an equivalent classifying-pretopos/topos formulation.
- Single-piece ordinary bi-interpretability can be strictly stronger; finite disjoint sums matter. The 2023 article expressly distinguishes exact completion from pretopos completion.
- Infinitary geometric logic needs infinitary sums and is outside this finite-sum question.

A categorical equivalence of pretoposes preserves their intrinsic finite-limit, disjoint-coproduct and quotient structure up to isomorphism. But a constructive proof should specify whether an equivalence is supplied as functors in both directions with natural inverse isomorphisms. Replacing a fully faithful, essentially surjective functor by a chosen inverse can conceal choice in constructive foundations. Similarly, selecting a common skeleton and picking representatives for all objects/arrows requires either a constructive presentation or justification. These are concrete obligations in the proposed proof; they are not reasons to declare the theorem false.

## 7. Minimum repairs and next mathematical work

### R1. Repair the disposition now

Retain the established ordinary coherent theorem and attribution. State that application to the original constructive scope remains unverified. Do not close the queue row on the strength of the qualified certificate. The packet already contains caveats, so this is largely an accounting/disposition correction rather than deletion of useful mathematics.

### R2. Repair source framing

Include Lombardi–Mahboubi E19 and the OWR p. 1744 aims alongside the extension-rule citation. Explain that constructive external reasoning is positively evidenced, although no formal foundation is specified. Do not create a new mandatory CZF/Bishop formalization challenge and then count failure of that invented challenge as failure of the original.

### R3. Seek an exact theorem-hypothesis match, without access-policy retries

A legitimately available complete journal proof, another primary treatment of the unrestricted coherent theorem, or a primary account expressly constructivizing the comparison could repair part or all of the gap. An abstract or broad theorem restatement alone does not certify the inhabited-sort change or the metatheory. Do not retry the already-cancelled source retrieval or bypass access controls. Existing local material is sufficient for the current HOLD.

### R4. If no source resolves it, make one substantive constructive bridge attempt

Give an explicit, finite-stage syntactic construction with empty sorts and empty contexts; prove the relevant normal forms for objects, morphisms, and predicates; form a common extension in both directions; and identify which constructive principles and equivalence data are used. Avoid global skeleton/representative choices by working with formal presentations and proof-carrying arrows if possible. Explain how this categorical formulation represents the source's intended constructive Morita notion rather than defining that notion to mean the desired conclusion.

An informal constructive proof is potentially sufficient for the informal source. A new formal proof assistant development, a prescribed foundation, or an effective decision procedure is not required merely by this audit. Any genuinely new proof work here should be logged as such; it cannot simultaneously be an original repair and a zero-turn already-known resolution.

### R5. Small mathematical/terminological corrections

Specify pretopos functors; retain branch-local existential witnesses; explicitly include nullary products or state and justify a harmless singleton adjunction; use finite stages rather than unbounded finite-depth wording; explain finite zigzag/common-span normalization; preserve the distinction between preprint and journal numbering.

## 8. Finite controls and accounting

The 2,032 controls verify finite set instances of the elementary constructions, including empties, unique quotient-map descent, and the invalid global-witness coproduct formulation. They do not range over arbitrary theories or toposes, prove conservativity/normal-form theorems, validate the cited theorem's hypotheses, establish pseudonaturality, or justify the metatheory. The frozen packet correctly says this; the successful rerun cannot change the HOLD.

The local prior-attempt-gate record reports the queue at 0/5 and bounded exact-ID searches returning no prior attempts. This audit did not redo the repository/private-chat searches and does not turn bounded negatives into exhaustive historical claims. Nothing in the mathematical audit contradicts the preparation-only zero count. Thus:

- **Original substantive author proof-attempts recorded so far:** 0, according to the supplied verified packet/gate record.
- **Remaining original attempt budget:** 5.
- **Already-resolved-at-zero-turns classification for the original question:** not established.
- **Permissible current mathematical finding:** known standard coherent characterization plus a source-applicability gap.
- **Recommended gate:** HOLD for original-scope closure; PASS for credited related coherent result, elementary bridges, and finite controls.
