# Independent historical-priority audit: PR #480 / problem 30003656

Audit date: 2026-10-11 America/Los_Angeles (2026-10-12 UTC). This initial verdict was formed without reading other newly commissioned priority reports. Mathematical validity of the current proof is a separate review family.

**Verdict: historical priority HOLD; a novel-first-resolution preprint is not certified.** The exact candidate follows by a routine, checkable specialization of published 2017 machinery. Moreover, the literal question already admits the classical-tautology mechanism documented in a dated 2019 author draft. The draft's warning applies to algebraic signatures too. This does not show that the exact one-constant formula was explicitly printed earlier; that narrower historical question remains unresolved. It does show why absence of that exact formula from the searched literature is insufficient evidence of novelty. **This verdict does not by itself certify `already_solved` in the documentary sense of an earlier author explicitly announcing a resolution of the algebraic refinement.**

## What the historical evidence actually classifies

| Classification | Evidence-supported conclusion |
|---|---|
| Earlier explicit, recognized algebraic negative resolution | **Not located.** The 2017 source explicitly asks the algebraic question; the general 2019 warning does not expressly label its algebraic restriction. |
| Earlier explicit printing of this exact one-constant alpha | **Not located.** This remains a bounded-search gap, not a novelty certificate. |
| Exact candidate as a routine consequence of pre-existing theorems | **Established by the derivation below.** This is a credited mathematical specialization, not documentary evidence that the earlier authors recognized it as an algebraic resolution. |
| Literal algebraic question defeated by earlier excluded-middle machinery | **Established by our explicit specialization of an old published mechanism.** That inference is not represented as an earlier author's expressly stated algebraic solution. |
| New, strengthened intended question solved | **Not established.** No precise additional exclusion condition was identified and checked. |

The mathematical question of implication from an older theorem and the historical question of explicit recognition are different. An overlooked corollary may be a useful observation. Its degree of originality and acceptable paper framing require an accurate statement of that limited contribution, not an assertion that this audit found an earlier explicit algebraic solution.

## Exact comparison target

Let T have one sort, one constant c, logical equality, and no nonlogical axioms. Write

    beta = forall x notnot(x=c),       alpha = not beta.

A sentence is redundant when adding it yields no new original-language geometric sequents, allowing equality and small infinitary disjunctions. The candidate says alpha is redundant while the generic T-model validates beta and therefore not alpha.

Separate questions must not be conflated:

1. Is there an algebraic T with any redundant sentence that fails in its generic model? This is the displayed literal universal assertion.
2. Is there such a witness that is not classically valid? The candidate supplies this extra property; it is not an extra condition in the displayed assertion.
3. Was this exact formula for this exact signature explicitly published earlier? No such explicit historical printing was established by this reviewer.
4. Does this exact example require a new mathematical mechanism beyond prior theorems and examples? The specialization below shows that it does not.

## Primary citation and claim map

The source summaries below are deliberately bounded; the detailed specialization is this reviewer's own deduction. Full third-party texts and rendered pages are retained only under ignored `private_sources/`.

| Source, dated identity, exact locator | Checked source claim | Priority implication and limit |
|---|---|---|
| G. C. Wraith, *Intuitionistic Algebra: Some Recent Developments in Topos Theory*, ICM Helsinki 1978, vol. 1, published Helsinki 1980, pp. 331-337; pp. 332, 333, 336. [Official full volume](https://www.mathunion.org/fileadmin/ICM/Proceedings/ICM1978.1/ICM1978.1.ocr.pdf) | p. 332 includes equality and arbitrary disjunctions in geometric sentences and states classical-to-intuitionistic geometric conservativity. p. 333 states Barr's surjective Boolean/choice cover. p. 336 asks the generic-model/redundancy question. | The source asks the general question and supplies the mechanism making classical tautologies redundant. It does not impose a restriction excluding classical tautologies, and it does not itself state the later algebraic refinement. |
| Ulrik Buchholtz, *Syntactic Forcing Models for Coherent Logic*, OWR 53/2017, pp. 3134-3136, final paragraph p. 3136 (report internal p. 16). [Report DOI](https://doi.org/10.4171/owr/2017/53), [institutional full text](https://oa.tib.eu/renate/server/api/core/bitstreams/f754efe0-f461-4dc6-8e01-be4de222b790/content) | The report gives a relational negative example, discusses equality, and explicitly leaves the algebraic case open. | This is the target's source, not evidence that all literal algebraic instances remained mathematically unresolved after 2017. The final open-problem wording must be compared with theorems as well as later claims. |
| Marc Bezem, Ulrik Buchholtz, Thierry Coquand, *Syntactic Forcing Models for Coherent Logic*, arXiv:1712.07743v1, submitted 2017-12-20T23:00:28Z; journal 2018, DOI 10.1016/j.indag.2018.06.004. Sections 5-7, pp. 22-26. [Primary preprint record](https://arxiv.org/abs/1712.07743), [fixed v1 PDF](https://arxiv.org/pdf/1712.07743v1) | Theorem 5.11 gives geometric equality-completeness for T+; constructor axioms define T+ at p. 22. Example 6.2 compares constant-language presheaf models, with the double-negated universal constant formula and its negation at pp. 23-24. Section 7 calls the purely equational refinement open. | This is the direct prior machinery. The one-constant specialization eliminates every extra constructor axiom. The apparent conflict between the final question and the easy specialization is a scope/priority warning, not evidence of a missing theorem. |
| Ingo Blechschmidt, *A general Nullstellensatz for generalized spaces*, author rough draft, historical source/PDF at commit cc39bd8b06aecbe2ecd08a86344a5bcc1b7ed596, dated 2019-05-03T00:55:46Z, Introduction, historical PDF p. 3. [Fixed historical source](https://github.com/iblech/internal-methods/blob/cc39bd8b06aecbe2ecd08a86344a5bcc1b7ed596/paper-qcoh.tex), [introduction commit](https://github.com/iblech/internal-methods/commit/cc39bd8b06aecbe2ecd08a86344a5bcc1b7ed596), [fixed historical PDF](https://raw.githubusercontent.com/iblech/internal-methods/cc39bd8b06aecbe2ecd08a86344a5bcc1b7ed596/paper-qcoh.pdf) | The author explains that excluded-middle instances give negative answers to the bare question, and that BBC also defeat it after suitable care to exclude those examples. No precise strengthened definition is stated in that paragraph. | This is explicit historical notice of the literal-definition issue. It is 2019 evidence, not pre-2019. It does not identify the exact alpha, nor prove that every plausible strengthened algebraic question was already solved. |

### Blechschmidt version-history check

The GitHub file-history endpoint returned 83 entries (below the requested page size 100). The oldest returned introduction commit is 72ed8ef03510dba74ae44c02d164fc707c92073d, dated 2019-03-05T00:50:09Z. It attributes the general negative answer to BBC but does not contain the excluded-middle paragraph. The paragraph is a literal addition in cc39bd8b06aecbe2ecd08a86344a5bcc1b7ed596. Its immediate parent, 97cbc605dffd9f70ddc86f0caedec376d32f13a4, lacks it. Both the historical TeX and historical PDF at that commit contain it. The current last file-changing commit d2309f04afbe6d40836712359ea7bdb6244fe20c, dated 2025-09-22T10:46:37Z, retains it. Source-reported Git dates are ordinary version-history evidence; they are not independently certified timestamps of public availability.

## Checkable specialization of the 2017 result

This section derives the exact candidate from BBC's stated results. It distinguishes a mathematical corollary from an explicitly asserted historical resolution.

**Step 1: the extra theory disappears.** Begin with the empty nonlogical theory in the signature containing only c, then equip it with logical equality. In BBC notation this is T=.

- Constructor axiom (I) has no instance, because there are no two distinct operation symbols.
- Constructor axiom (II) for the nullary symbol has no arguments to compare; it is the logical tautology c=c implies true.
- Constructor axiom (III) has no instance, because there is no positive-arity operation and c contains no occurrence of a variable.

Therefore T+ and T= have identical deductive consequences. This is the crucial difference from the published two-constant example, where the constructor axiom excluding equality of the constants really adds an axiom.

**Step 2: identify the old sites exactly.** In the empty theory, the forcing conditions have a finite variable set X and no predicate facts. Terms are exactly X disjoint-union {c}. A term substitution sends variables to variables or c, fixing c. Reversing the condition-category arrows gives every pointed map between finite pointed sets. An injective renaming sends distinct variables to distinct variables and fixes c, giving every pointed injection. The topology is trivial because the theory has no axioms. Thus BBC's term-substitution and injective-renaming models are precisely

    U in [finite pointed sets and all pointed maps, Set],
    V in [finite pointed sets and pointed injections, Set].

The object with X empty is the singleton pointed set, not an omitted stage. No new relation, nontriviality axiom, or topology is being smuggled into T.

**Step 3: compute the opposite first-order truth values.** For all-map stages, any element can be sent to c by a pointed collapse. Consequently no successor can force negation of equality to c, and every stage forces beta. For injection stages, an added fresh element stays unequal to c along every later injection. Thus no stage forces beta, and every stage forces alpha. This is the one-constant form of the mechanism displayed in the existing two-constant example. It covers the singleton stage via an extension adding a variable.

**Step 4: invoke the old completeness theorem.** If T+alpha proves a geometric sequent sigma, soundness puts sigma in the injection model V. BBC Theorem 5.11 puts sigma in T+. Step 1 puts sigma in T. Geometric sequents are universal closures of positive-formula implications, so this is the theorem's geometric-sentence scope, including equality antecedents. Its underlying geometric language allows small infinitary disjunctions, and Remark 5.12 explicitly addresses such disjunctions in normal-form sentences. No classical completeness or choice principle has been added to this deduction.

**Step 5: identify the generic model.** With only c, finite pointed sets are precisely finite free pointed algebras. The all-map model is the standard generic pointed object; equivalently it is the above term-substitution generic model for T+, which equals T here. It validates beta and hence not alpha. The constructed alpha is classically false in the singleton pointed set and classically true in a two-element pointed set, so it is not a classical tautology.

All central mathematical ingredients of the candidate are consequently within the specialization. The explicit finite-quotient proof in the PR is valuable as an independent verification, but it is not evidence that the underlying theorem was absent from prior mathematics.

## Why the excluded-middle history matters for the exact target

This reviewer's concrete specialization of the historical warning uses

    delta = forall x ((x=c) or not(x=c)).

Delta is classically valid, so any intuitionistically derived geometric consequence of T+delta is a classical consequence of T. Wraith's geometric conservativity metatheorem then removes the classical logic. This proves literal T-redundancy, with equality and infinitary geometric disjunctions covered by the source's definitions.

Delta fails in the genuine generic pointed object. At a stage with a nonbasepoint a, neither a=c nor its negation is forced: equality fails pointwise, while a collapse map to the singleton defeats the negation. At the singleton stage the universal clause also considers extension stages. Thus delta is not globally valid in U. The theory is algebraic; adding a constant is an allowed nullary operation and introduces no nonequational axiom.

Therefore the historical bare mechanism already furnishes a negative instance inside the literal algebraic class. Requiring the newer witness alpha not to be classically valid is a meaningful improvement of the witness but does not make the displayed existential counterexample problem newly open. Nor may the phrase about excluding counterexamples be converted into an invented strengthened formal definition: no such definition was established in the examined paragraph.

## Broad follow-up screen and its limits

Queries combined the exact paper title, Wraith/redundant/algebraic/purely equational, generic-model equality/constants, and the announced companion paper. They recovered the original report, BBC, Blechschmidt's draft and 2019 talks, and the 2019 Bezem-Coquand follow-up *Skolem's Theorem in Coherent Logic* (DOI 10.3233/FI-2019-1853). The publisher identifies only Marc Bezem and Thierry Coquand as authors; Thorsten Altenkirch and Aleksy Schubert are editors. After the initial independent verdict, the root supplied an author-owned source location. This reviewer independently retrieved and read [the author-hosted FI version](https://github.com/marcbezem/skolem/blob/master/FIversion.pdf). Its first-page header reports volume 167 and DOI 10.3233/FI-2019-1800; it must not be identified with the final journal file. Root subsequently supplied the separate final filename, and this reviewer independently retrieved [the final published file](https://github.com/marcbezem/skolem/blob/master/fi-170%281-3%2902.pdf), SHA256 5b040c354408db36489a72f6fccb1ef607f4d6ad97fed08bff96bf5f4cabc93a, whose header agrees with the publisher's volume 170 / DOI 10.3233/FI-2019-1853. Sections 6.1-6.3, pp. 11-13, were read in both files. The negative examples use a propositional predicate or total binary relation; the field and local-ring applications add nonequational axioms. Neither file prints the exact pointed alpha or expressly resolves the purely equational refinement in those sections. The coherent/geometric scope footnote is not used to weaken the present target. Thus the suspected 2019 direct collision was checked against the actual final file, while the 2017 specialization remains. Other retrieved generic-model/Nullstellensatz references did not supply an explicit strengthened algebraic redundancy condition in the checked snippets. Absence from these bounded searches is not proof of absence from the literature.

## Falsification checks and exact remaining gap

| Challenge | Result |
|---|---|
| Maybe the two-constant example cannot be specialized because T+ adds inequations. | Checked symbol-by-symbol: the obstruction vanishes with exactly one constant. Keeping two constants would fail this check. |
| Maybe candidate sites differ from the old models. | Their objects, terms, maps, trivial topology, and canonical model coincide after reversing the site arrows. |
| Maybe equality or infinite disjunctions invalidate the corollary. | Theorem 5.11 includes equality; the paper's geometric language and Remark 5.12 include the necessary infinitary disjunctions. |
| Maybe all pointed stages have a nonbasepoint. | False; the singleton stage is included and extension stages handle both alpha and delta. |
| Maybe the older EM witness does not lie in the algebraic class. | It uses the same one-constant empty equational theory. The nonequational formula is an added sentence, not an axiom of the base theory. |
| Maybe the candidate is merely the same classical tautology. | False: alpha is not classically valid. The distinction improves the witness but does not erase the earlier negative answer to the literal universal target. |
| Maybe the 2017 final open-problem wording proves novelty. | It is evidence about the authors' stated question, not a barrier to a corollary of their own theorem. This audit supplies the corollary explicitly. |
| Maybe Blechschmidt's warning predates 2019. | Not established; inspected file history begins in 2019, and the warning addition is dated 2019-05-03. Do not misdate it. |

The exact narrower historical gap is whether this particular nonclassically-valid alpha was explicitly stated by another author, and what precisely formulated exclusion condition the original authors intended. External scholarly input might help resolve that intention, but independent-research policy permits no outreach and no outreach preparation. This note simply records that fact.

## Recommended disposition

Do not release a preprint framed as the novel decisive first solution of an unsolved literal algebraic problem. A credited short expository observation or independently reproduced specialization may be mathematically useful, but would require a different, accurately limited claim and destination from the user's requested new open-problem-resolution preprint. The existing `claimed_solved` eligibility did authorize this audit; this reviewer does not change QUEUE or decide the PR's operational disposition.

Strongest verified result: the exact candidate is a checkable corollary of 2017 BBC machinery, and the displayed algebraic existence question also succumbs to the historical bare excluded-middle mechanism. Assigned bounded historical audit completion estimate: 100%; confidence that first-resolution novelty is not established: high. An exhaustive history-wide novelty certificate is not claimed. Open gap: explicit earlier publication of the exact formula and any formally strengthened intended question. A new mechanism or newly retrieved primary evidence could refine the historical verdict; negative searching alone cannot do so.
