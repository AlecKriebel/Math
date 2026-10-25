# Acquisition and scope — Zenodo 23572690

Disposition: **SCOPE_COMPLETE. No mathematical PASS or publication clearance.** This role authenticates the edition and maps its original question, assumptions, structural imports and conditional presentation. Independent mathematical reviews and root assessment remain required.

## Identity and public assets

The frozen queue identifies row 66, inventory index 82, work Z-23572689, record **23572690**, *BV generators for polynomial Weyl subalgebras*, Alec Kriebel. Fresh Zenodo metadata and the current six-page PDF both give **version 1.0.0, 22 October 2026**. The PDF labels itself a preprint. This named Zenodo work is eligible; no unrelated Keller paper or non-Zenodo archive was imported.

| Public asset | Bytes | SHA-256 |
| --- | ---: | --- |
| bv-generators.pdf | 78,866 | 2c344b0baff06088f04f4468bd8f6365405e879f7004b169055aebedbdecd4e7 |
| bv-generators-source-and-verification.zip | 100,928 | a7ab72e55fd0952d363f78f92bc418b9f1331ccefb1f75eaea8dda32868601e6 |

Both files were freshly fetched from actual record file links and authenticated against Zenodo size and MD5, then bound by SHA-256. ZIP CRC, safe paths, duplicate names, regular-file types and extracted bytes were checked. Its 12 regular members are under `sources/published-source/bv-generators-source-and-verification/`. The embedded `paper.pdf` is identical to the top-level six-page PDF. There is one distinct reader and no extra supplement PDF. The final custody check rehashes all assets/members and independently checks the source manifest.

I read all six current PDF pages, all 389 lines of `main.tex`, the complete 165-line exact-check program, the complete 97-line build program and `DEPENDENCIES.md`. Pages 1 and 4 were also rendered and visually inspected to check the statement/signs and the displayed obstruction. The current main source contains the entire proof; there is no necessary missing mathematical supplement.

`PRIORITY.md`, `CHECK_RESULTS.json`, historical assessment bodies and current sibling findings were kept opaque. The current manuscript, record description, dependency note and build script contain historical reading/priority or workflow assertions, encountered incidentally while reading necessary scope/support. Those assertions are not used as fresh validation evidence. The dependency note's actual URLs were followed, but its claimed prior reading was independently replaced by the current primary-body reading listed below. The packaging script's old `publication_ready` language is not a current mathematical verdict or a contradiction of the fresh public deposit. No mathematical checker was executed or adopted by this scope role.

## Exact mathematical scope

For **any field k of characteristic zero** and **any nonzero polynomial h∈k[x]**, the unital associative algebra is

`A_h = k⟨x,Y⟩/(Yx−xY−h(x))`.

For h≠0 it is embedded in the first Weyl algebra with `[y,x]=1` by `Y=yh(x)`. The original question uses `h(x)y`; these generate the same subalgebra because `yh−hy=h′`. The parameter is a polynomial in one variable, not a multivariable polynomial map. The theorem does not concern arbitrary Weyl subalgebras, all differential-operator algebras, local analytic algebras, formal power series, or étale extensions.

The object is **ordinary Hochschild cohomology HH•(A_h,A_h)** with its canonical cup product and Gerstenhaber bracket. A bracket generator is any k-linear degree −1 operator satisfying the exact sign convention in equation (1); a BV generator additionally has Δ²=0. Negative cohomology is zero. The negative statement excludes every bracket generator, not merely a chosen differential/geometric ansatz or only square-zero candidates. It does not concern changing the cup product/bracket or twisted coefficients.

Theorem 1 claims the equivalence of four conditions: h squarefree; the whole canonical bracket zero; existence of a bracket generator; existence of a BV generator. Nonzero constants are units and count as squarefree. If squarefree, Δ=0 suffices. If h has a repeated irreducible factor over k, the paper claims no bracket generator at all. Characteristic zero is indispensable to the stated argument: integration, nonzero derivatives of nonconstant irreducibles, coefficient division and the characteristic-zero structural statements are used. No algebraic closure, real/complex restriction, root splitting or scalar-descent theorem is assumed.

This is an unconditional classification within the declared hypotheses, using named published structural theorems. It is not conditional on a Jacobian or Dixmier conjecture, and claims no implication for either conjecture. There is no Keller-map hypothesis or polynomial-map invertibility conclusion. Auxiliary localization of the ambient Weyl algebra is used only to express normalizing elements and extend derivations; the cohomology being classified remains that of the original polynomial algebra A_h, not its localization.

The literal **embedded h=0** specialization generates k[x], treated separately by `Δ(f∂x)=−f′` and Δ(k[x])=0. Substituting h=0 in the abstract two-generator presentation instead produces k[x,Y], a different algebra. The nonzero-h theorem and its HH⁰=k obstruction must not be applied unchanged to either zero-parameter interpretation.

For nonconstant h, the recorded Nakayama automorphism `ν(x)=x, ν(Y)=Y+h′` restricts to a nontrivial unipotent block on span{Y,h′}; nonzero constant h gives the identity. Thus both squarefree and repeated-factor cases occur in the original nonsemisimple branch. Failure of semisimplicity alone is neither the claimed sufficient nor necessary obstruction; repeated factors distinguish the two outcomes.

## Current proof and computation interfaces

The paper defines the monic gcd d=gcd(h,h′) and π=h/d. Its load-bearing inherited structure is a length-two free bimodule resolution, HH²=A/dA, vanishing above degree two, the polynomial/PBW bases, and a derivation spanning description. Its own bridge is a comparison to normalized bars that computes the **canonical** cup product, including the right-hand polynomial factors that cannot be freely moved through E(x).

The proof then maps as follows, without this scope role asserting correctness:

1. The center is k. A derivation D_f with D_f(x)=0, D_f(Y)=f is inner exactly when h divides f. The characteristic-zero centralizer and polynomial-integration arguments are explicit.
2. The class c=[D_d] is Lie-central in HH¹, and, when d≠1, is nonzero with a linearly independent companion. Normalizer formulas and their derivatives are used only to establish this for all degree-one classes through the published spanning theorem.
3. The normalized-bar comparison yields `[D_f]∪[E]=[fE(x)]∈A/dA`; hence c annihilates all HH¹ under the cup product. The s=0 and s=1 terms, normalized constants, signs and right factors are stated explicitly.
4. The abstract obstruction uses HH⁰=k, c≠0, dim HH¹>1, Lie-centrality and the cup annihilator. For λ=Δ|HH¹ it forces λ=0; any cup-zero pair would then commute. It never assumes Δ²=0 or fixes Δ on HH².
5. For an irreducible u|d, the paper sets g=d/u and defines b directly by b(x)=π, b(Y)=(πd′/d)Y. The pair [D_g],[b] has zero cup and purported nonzero bracket `[D_q]`, where q=(h/u²)u′ has degree less than deg h. This works over the original field and allows nonsplit irreducibles. The definition deliberately avoids identifying b literally with ad(πy) in the chosen ambient convention.
6. For d=1, HH² vanishes and the derivation spanning reduces HH¹ to commuting D_f classes; the entire bracket is zero, giving Δ=0. The separate embedded h=0 calculation has nonconstant HH⁰ and uses its own divergence operator.

`exact_checks.py` provides finite rational-polynomial identities, normalized-bar telescoping, selected nonsplit quadratic and nonmonic examples, embedded-zero Leibniz cases, and deliberately false controls for signs/omitted factors/ambient identification/right-factor movement. It neither computes universal Hochschild cohomology nor verifies the full published resolution/spanning result. It was read, not executed. No stored PASS, count or `CHECK_RESULTS.json` is evidence for this scope disposition. The build script copies the frozen PDF and packages files; it does not recompile or mathematically validate the manuscript and was not executed.

## Fresh primary-body interfaces

All successful acquisitions below are fresh, byte-bound local PDFs with adjacent text and receipt records in `cache/primary-sources`. No historical reviewer opinion was consulted to settle an interface.

**Original question: Lopes, joint with Solotar, OWR46/2023.** The complete contribution at printed pp.2702–2703 was read in the fresh publisher PDF. It specifies the subalgebra generated by x and h(x)y over characteristic zero, defines BV with the same bracket signs (its extra `aΔ(1)b` is zero here), and asks in Question (2) about nonsemisimple Nakayama automorphisms. Questions (1) for general algebras and (3) for Poisson analogues are separate and not answered by this note. The workshop ran 15–20 October 2023; the publisher page dates publication to 23 July 2024. Do not invent a different 2023 publication date.

**Lopes–Solotar, JNCG15(2021),1373–1407, DOI10.4171/JNCG/439.** Fresh final publisher PDF read at Proposition2.1, complete Section3 through the characteristic-zero Proposition3.9/Corollary3.11 and the Nakayama paragraph, plus Section6.1/Theorem6.2. These give the ambient basis, center/commutator conventions, explicit resolution differential, quotient HH² and higher vanishing, and derivation/center description. The cohomology quotient and spanning apply over arbitrary characteristic-zero fields. The characteristic-positive branches are different and not transferred. Exactness of the free resolution is a published import; this scope role does not claim to independently reprove every later contracting-homotopy calculation or the Virasoro-module classification.

**Benkart–Lopes–Ondrus, J.Algebra424(2015),46–97, DOI10.1016/j.jalgebra.2014.11.007.** The journal identity was checked on the publisher page. The fresh mathematical body is **arXiv1406.1508v2**, not falsely labeled a final journal PDF. Read Theorem4.9/proof, Lemma4.11/proof, Theorems5.1/5.3/5.7, Lemma5.6, Proposition5.9 and Theorem5.13 with the displayed decomposition/center arguments, and Section5.5's conclusion. These establish the precise normalizer/derivation spanning and innerness conditions used. Its monic radical convention differs from π=h/monic_gcd by a nonzero scalar when h is nonmonic; scalar multiplication does not change the indicated spans or divisibility tests. The nonzero-parameter and characteristic-zero hypotheses remain essential. No independent audit of all 48 pages or every internal normalizer lemma is claimed.

**Herscovich–Li, Doc.Math.27(2022),1773–1804, DOI10.4171/DM/X18.** Fresh publisher PDF acquired after an author-host TLS failure; no security bypass was used. Read the opening scope and the complete Proposition4.15/proof with its cup/bracket obstruction. It excludes every degree −1 bracket generator for FK(3) over characteristic different from2,3, without assuming square-zero. This is a genuine older ordinary-Hochschild nonexistence result and an obstruction-strategy predecessor. It concerns a different finite-dimensional algebra; the current contribution cannot be called the first such phenomenon. The structural table underlying that separate theorem is not independently recomputed here.

**Kowalzig–Krähmer, Ext and Tor.** Fresh author-hosted manuscript acquired; its bibliographic journal record is J.ReineAngew.Math.697(2014),159–219, DOI10.1515/crelle-2012-0086. Read Theorem1.7 and Sections7.3–7.4, including Definition7.5 and the proof interface. The ordinary HH•(A,A) conclusion assumes a twisted Calabi–Yau algebra with a semisimple modular automorphism; twisted-coefficient homology enters through duality. The nonsemisimple A_h branch is not covered by silently dropping semisimplicity. This is a comparison/scope boundary, not a theorem used to prove the negative case. The author manuscript is not asserted byte-identical to the 61-page published edition.

**Bian–Itagaki–Kou–Lyu–Zhou, arXiv2603.04834v2.** Fresh version-specific PDF acquired. Read introductory scope and Criterion7.7, its stated hypotheses and proof interface, Theorem7.8, and Theorem7.11. Its family is truncated basic cycle algebras KZ_e/J^N, N≥2, and its criterion requires the indicated odd homogeneous generators to have zero mutual cup products **and** zero mutual brackets. The current noncommuting obstruction pair cannot be made to satisfy that criterion by omitting the bracket assumption. This recent positive result is a separate-family comparison, not an imported proof of this classification. Its full computation is not independently re-audited here.

The proof's load-bearing structural interfaces were located in actual primary bodies. Final-publisher-equivalence for BLO/KK, comprehensive historical priority, every internal proof of the imported results, and correctness of the current deduction are not claimed by this scope assignment. The primary-interface ledger records exact versions, hashes, portions read and these limits. No mathematical finding depends on absence from a literature search.

## Conditional presentation and remaining gates

`content.json` preserves the complete original abstract from actual `main.tex`, with explicit mathematical typography normalization, and gives a conditional explanation of the squarefree/repeated-factor distinction. It credits the original question, published structure and older FK(3) obstruction; keeps characteristic zero, h≠0, ordinary canonical cohomology, and the separate embedded-zero case visible; avoids Jacobian/Dixmier/Keller implications; and labels the work unrefereed and extensively AI-assisted. It invites substantive collaboration without preparing or initiating outreach. No dated audit replay or finite-check counts appear in the public candidate.

Follow-up is null: no unusually strong new paper-worthy question was independently justified by this scope work. No source repair, site/page/promotion change, spreadsheet write, Git operation, deployment, UI action or external contact occurred. `verdict.json` is source-bound **scope completion only**. Promotion must await the independent mathematical gates and root's explicit disposition.
