# Structural priority audit: PR1283 / Problem30005434

Initial independent report. Research began 2026-10-18 03:59:24 UTC. The seal records the completion time. This family did not read sibling priority work before sealing, did not contact any outside individual, and made no Git, PR, sheet, release, or root-file changes. The audit completion estimate is 100% for this bounded independent review; the unrestricted historical priority question remains unresolved.

## Decisive finding

**The exact proposed universal multiplication is already in a dated 2016 primary source. It must not be presented as a new construction or first mechanism.** Castiglioni and San Martín, *On a symmetrization of hemiimplicative semilattices*, arXiv:1611.09589v1, submitted 29 November 2016, printed p. 7, Example 3.5, formula (4), gives

\[
a\to b=\begin{cases}1,&a\le b,\\a\wedge b,&a\nleq b.\end{cases}
\]

The actual PDF and rendered page were inspected. The source's p. 2 defines a bounded semilattice as one with a greatest element, so its formula has the required arbitrary top-semilattice scope. A bottom is mentioned only when needed for other examples. [Version and date](https://arxiv.org/abs/1611.09589v1), [actual v1 PDF](https://arxiv.org/pdf/1611.09589v1).

The final article is titled *l-Hemi-Implicative Semilattices*, Studia Logica **106**, 675–690 (2018), DOI 10.1007/s11225-017-9759-3; the publisher gives an online publication date of 3 October 2017. Its institutional indexed text renumbers the same formula as Example 3.1(4). The final complete body was not successfully downloaded here; the priority finding relies on the actual immutable 2016 v1 body, not an inference from final metadata. [Publisher record](https://link.springer.com/article/10.1007/s11225-017-9759-3).

The inspected v1 establishes hemiimplicative membership, an absorption identity, compatible order, and congruence results for this family. It does not state the cycloid equation or the pair of semibrace identities. Therefore the supported distinction is **old exact operation, current verification/application of additional identities**. No first application, earliest consequence, independent-discovery, worldwide openness, or general novelty clearance follows.

## Exact hypothesis map

| Target | Verified 2016 source | Assessment |
|---|---|---|
| Arbitrary nonempty meet semilattice with greatest element e | Arbitrary bounded meet semilattice (A,∧,1); bounded explicitly means greatest element | Same domain, after 1=e |
| Associative, commutative, idempotent meet | The source's semilattice operation | Same operation |
| x≤y iff x∧y=x | Its semilattice order | Same order |
| e when x≤y, otherwise x∧y | Example 3.5(4) exactly | Exact formula precedent |
| No distributivity, finiteness, joins, bottom, or cancellation | None needed for that example | No hidden extra restriction identified |
| Logical unit, diagonal, separation | Directly checkable from formula | This audit checks them below; source's broad class alone is insufficient |
| Meet preservation and mixed identity | Not identified as stated results in inspected v1 | Separate verification required |
| Every pointed nonempty semilattice, at arbitrary prescribed e, via right projection | Not the scope of this top-based formula | Separate elementary observation for the workshop's printed equations |

This identification is not merely an old ingredient resembling the target: it is the complete piecewise definition on the complete target domain for the simultaneous L-algebra case. Re-deriving it independently does not remove the attribution obligation.

## Classification of checked precedents

“Earliest verified” below means earliest dated content actually verified by this family for the listed fact. It does not mean the first origin of that fact.

| Source and date evidence | Actually inspected content | Relation to target | Exact remaining gap |
|---|---|---|---|
| Chajda–Kühr, *Algebraic structures derived from BCK-algebras*, Miskolc Math. Notes 8 (2007), 11–21; actual first page says received 17 Jan 2006 | Printed pp. 11–12: any top-poset carries implication 1 for x≤y, otherwise y; BCK properties | Old universal order-implication mechanism, different on incomparable pairs | It fails required meet identities in general; not a target precedent |
| Castiglioni–San Martín, arXiv v1 dated 29 Nov 2016; final online 3 Oct 2017, issue 2018 | Entire 15-page v1; p.7 formula (4) visually checked | **Exact universal target operation** | Full semibrace/L application not found as a stated theorem in this inspected source |
| Celani–Esteban, *Spectral-like duality for distributive Hilbert algebras with infimum*, Algebra Univers. 78 (2017), 193–213; actual front page gives 26 Jul 2017 | Definition 2.6 and Examples 2.7–2.9, printed p.200 | Any top-semilattice has the different order implication; the paper explicitly shows Boolean-four failure of second-coordinate meet preservation | Cannot substitute Hilbert-with-infimum for meet-closed L-algebra |
| Rump, *L-algebras and their groups*, AGTA 2019 program + author slide body | Slides 2, 5, 6: logical unit/cycloid, self-similar closure, both meet identities, ∧-closed characterization | Old precise L/meet framework requiring credit | Does not construct the target expansion on arbitrary semilattices in inspected passages |
| Dietzel, *Some problems on L-algebras*, OWR 9/2023, printed pp.544–547 | Definition 2, footnote defining semilattice, Problem 3 | Authoritative requested problem; printed Definition 2 has no meet-unit axiom | Historical question statement is not evidence it remained open in 2026 |
| Dietzel–Menchón–Vendramin, arXiv:2206.04955v4, 2 Jul 2023 | Actual v4 pp.3,5–6: Definition 3.1/Theorem 3.2 | A distinct monoid-with-neutral-e convention, plus Rump-attributed ∧-closure theorem | Earlier versions not inspected here; no claims about their contents |
| Rump–Vendramin, *The prime spectrum of an L-algebra*, final publication metadata 2024 | Actual VUB source p.8 Example 7: Boolean-four order and p·q=p·0=q·p=q·0=0; p.10 meet equations | **Exact non-chain particular case**, expressly an L-algebra; remaining entries follow from order/unit | Particular case, not arbitrary semilattice classification |
| San Martín, *Compatible operations on commutative weak residuated lattices*, 2015 institutional body | Definition 1.1 and weak Heyting requirements | Weaker-residuation background but retains first-coordinate antitonicity and lattice restrictions | Not an automatic general source of target, which need not be antitone |
| Properzi–Qin, arXiv:2512.08579v1, 9 Dec 2025 | Actual primary body: preliminaries, examples, linear/simple and Hilbert families; text searched throughout | Current primary work checked beyond direct Problem 3 searches | No universal target expansion identified; this is a bounded source observation |
| Rump 2008 J. Algebra; Rump 2008 JAA | Publisher metadata/abstract or first-page preview; author inventory and later attributions | Framework origins and credits | Relevant original full bodies unavailable to this family; do not treat as excluded precedents |

Primary links: [Chajda–Kühr body](https://real.mtak.hu/87453/1/150.pdf); [Celani–Esteban body](https://ri.conicet.gov.ar/bitstream/handle/11336/58915/CONICET_Digital_Nro.01849fbb-3c81-466b-9a32-2f75c2964595_B.pdf?isAllowed=y&sequence=5); [Rump slide body](https://www.advgrouptheory.com/agta2019/Talks/Rump.pdf) and [dated program](https://www.advgrouptheory.com/agta2019/program.html); [workshop primary](https://doi.org/10.4171/OWR/2023/9); [enumeration v4](https://arxiv.org/pdf/2206.04955v4); [Rump–Vendramin institutional body](https://cris.vub.be/ws/portalfiles/portal/119985346/wronski.pdf); [San Martín institutional body](https://sedici.unlp.edu.ar/bitstream/handle/10915/139191/Compatible_operations_on_commutative_weak_residuated_lattices.pdf-PDFA.pdf?sequence=1); [Properzi–Qin v1](https://arxiv.org/pdf/2512.08579v1).

## Independently checkable mathematical transfer

The following is an audit derivation of the additional identities for the already-published operation. It is not a claim that the old authors proved the following argument, or that this argument first occurred here.

Let S have top e. Define μ_x(z)=x∧z and define j_x on ↓x by j_x(x)=e and j_x(t)=t for t<x. The map j_x preserves binary meets: if either input is x this uses e∧t=t, and otherwise the meet remains strictly below x. Therefore F_x=j_x∘μ_x preserves meets. It is precisely the old piecewise operation F_x(z)=x·z. This proves the first semibrace identity.

If u≤x, then

\[
F_u\circ F_x=F_u. \tag{A}
\]

For a given z, x≤z makes both sides e. Otherwise F_x(z)=x∧z, and u≤x∧z iff u≤z. If that condition holds both sides are e; if it fails both sides are u∧z. This covers u=x, u=e, and x=e as well.

For t=x∧y, if x≤y then t=x and x·y=e, so F_{x·y}F_x=F_eF_x=F_x=F_t. Otherwise t<x and x·y=t, so (A) gives the same conclusion. Hence

\[
(x\wedge y)\cdot z=(x\cdot y)\cdot(x\cdot z).
\]

Its symmetry in x,y proves cycloid. Also F_e=id, F_x(e)=F_x(x)=e, and F_x(y)=e iff x≤y. Thus logical unit and separation hold and the logical and meet orders coincide. This is a complete elementary verification on arbitrary, including infinite and nondistributive, top-semilattices.

For necessity in the printed workshop convention, assume both a semibrace and L-algebra. Put t=e∧a. Meet preservation gives a·t=(a·e)∧(a·a)=e. The mixed identity gives t·a=(e·a)·(e·a)=e. Separation implies t=a, so e is greatest. If x∧y=x, the mixed identity at z=y gives x·y=e. Conversely x·y=e gives x·(x∧y)=e by meet preservation and (x∧y)·x=e by the mixed identity; separation gives x∧y=x. No hidden order-identification assumption is needed.

Finally, for arbitrary nonempty (S,∧) and prescribed e, x·y=y satisfies exactly the workshop's four equations by substitution. Its diagonal is x, so it is an L-algebra only on a singleton. Empty S admits no distinguished e.

## Falsifications of overly broad source reductions

The authored script and results distinguish exact K4 from larger preexisting classes. A four-chain 0<a<b<e with multiplication table

| · | 0 | a | b | e |
|---|---|---|---|---|
| 0 | e | e | e | e |
| a | 0 | e | e | e |
| b | 0 | 0 | e | e |
| e | 0 | a | b | e |

satisfies hemiimplication, H4, logical-unit/diagonal laws, separation, compatible order, and meet preservation. It fails cycloid at (a,b,0): the left side is 0 and the right side e. It also fails the mixed identity. Thus those general hIS results cannot be cited as already proving the full theorem merely by changing terminology.

The old poset operation on Boolean four gives a·(a∧b)=0 but (a·a)∧(a·b)=b for distinct atoms a,b. The target gives a·b=0, and violates a≤b·a. Thus BCK/Hilbert/residual constructions with the latter property are not equivalent under the same order. Dualizing gives a join-semilattice with bottom and subtraction r*s=0 for r≤s, otherwise r∨s; calling it standard BCK subtraction would still require an axiom check, not just a change of symbols.

The target was checked on a singleton, a four-chain, Boolean four, M3, and Boolean eight. These finite checks validate the maps and counterexamples; the proof above supplies universal scope.

## Required framing for the paper and all associated records

The exact old formula must be credited at its first mathematical use and in the surrounding contribution statement. A defensible concrete sentence is:

> We apply the hemiimplicative operation of Castiglioni and San Martín (2016, Example 3.5(4); final article Example 3.1(4)) and verify directly that it defines a meet-semibrace which is also an L-algebra on every meet semilattice with a greatest element.

The work may state and prove the classification, distinguish the two printed conventions, and supply checkable derivations and computations. It must not state that the multiplication is new. Whether the application itself is previously unrecorded remains a separate historical question; no affirmative novelty wording is supported by this audit.

For each of the eleven metadata/summary surfaces under root review, use the same factual framing: classification/application using an established hemiimplicative operation; attribution to Castiglioni–San Martín; Rump framework credits; exact printed-versus-monoid scope. Remove phrases asserting new construction, first universal mechanism, first non-chain example, current worldwide open status, earliest consequence, independent discovery, or novelty clearance. Recheck title, abstract, description, result summary, status tags, keywords implying firstness, references, provenance fields, reviewer-facing summary, release/DOI text, and any index record. This list is a synchronization checklist, not a claim about uninspected file names or their exact count.

## Limits and remaining historical work

The normal World Scientific article and PDF URLs returned 403. The ResearchGate page had only a World Scientific first-page preview, expressly requesting full-text access; no request was made. The 2008 J. Algebra full body and 2015 Rump body were not obtained. The final hemiimplicative institutional URL timed out/failed; the actual 2016 arXiv body supplies the decisive precedence independently. Earlier versions of enumeration were not inspected. These gaps forbid claiming the oldest origin or oldest implicit consequence.

Searches covered L-algebras, cycloids, semibraces, semilattice endomorphisms, BCK/Hilbert/order implication, hemiimplication, weak residuation, equality-to-implication, pseudocomplement variants, dual notation, Spanish terminology, Chinese terminology, and recent work. Search non-results are not absence proofs. This initial report is sealed before any cross-family challenge; subsequent challenge findings must be recorded separately.

No human author or other outside person was contacted, and no outreach was drafted. Access to some original bodies would improve historical coverage; that is a source gap for the research notes only.
