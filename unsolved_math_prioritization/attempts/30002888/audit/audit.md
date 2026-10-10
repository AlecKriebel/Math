# Independent audit: mixed-perverse forgetful functors

Problem 30002888; OWR-13682-010. Review date: 2026-10-06.

## Verdict

**Accept the unchanged author freeze as an honest partial, conditional investigation. Do not classify the general problem as solved.** No mandatory mathematical correction was found. No correction patch is needed. The acceptance concerns the propositions actually stated, their hypotheses, and the bounded literature/status account. It is neither a proof that a general forgetful functor exists nor a proof that no such functor exists.

Reviewed author archive: `MIXED_PERVERSE_30002888_AUTHOR_SAFE_FREEZE.zip`, 11,285 bytes, SHA-256 `feb85b4fd09b96aced2438889fbc0866302a56478fef12ad447f95fc8da336be`.
Its external manifest has SHA-256 `4bc74cfa1a957a2f9a6d87e5c0251bd30fc05195b1da8e86503da30d4611e56c`.
All four members were read; exact membership, hashes, sizes, text encodings, JSON syntax and ZIP CRCs were checked independently. The author archive, manifest, and validation receipt were unchanged at the end of review.

## 1. Original question and source boundary

The conventions and question agree with Achar's contribution in [OWR], printed pp. 1427–1429. The grading definition uses an exact heart functor, a grading-shift trivialization, and the direct sum of Yoneda Ext groups in every nonnegative degree. Essential surjectivity is not an additional requirement in that displayed definition. The ordinary and homotopy shifts are different, and the Tate twist is their specified combination. The finite-flag affirmative case is already present under good-characteristic assumptions; it is not new work in the submitted package. The report year is 2015, while the publisher dates publication to 2016-02-15. The question page was checked both as text and as a rendered image. [OWR]

The discussion of [AR] correctly distinguishes constant pariversity, existence of parity extensions, the mixed perverse t-structure, the later standard/costandard perversity assumption, realization statements, and the finite-flag forgetful construction. Its cited preprint is version 2 of 2014-12-20; the journal article is Duke Mathematical Journal 165 (2016), 161–215. These are not general existence hypotheses that can silently be added to the original question. [AR]

## 2. Proposition 2.1: independent proof check

Write S for the homotopy shift and Q for the termwise inherited shift, so the Tate twist is Q^{-1}S. The assumption that P is shift-stable is used as stability under the inherited shift autoequivalence and its inverse. The functor R, its triangle structure, its restriction isomorphism on P, and its Tate-trivialization are all hypotheses. None is manufactured from the notation K^b(P).

For stalk objects P_0,P_1 and integers n,k,

    P_1<n>[k] = P_1{-n}[n+k].

A degree-zero chain map between these stalk complexes can exist only when n+k=0. There are no nonzero homotopies to quotient out in the surviving stalk-to-stalk Hom space. The surviving group is exactly

    Hom_P(P_0,P_1{k}) = Hom_T(P_0,P_1[k]_T).

Fullness of P is essential. It is not enough to identify objects or merely compare dimensions. Naturality of the restriction isomorphism identifies R on every morphism in this group with the inclusion up to conjugation. The triangle structure of R and the iterated Tate-trivialization add only isomorphisms. Hence the actual generator comparison is invertible, including negative k.

The iterates of the given natural isomorphism are taken with identity at n=0 and inverses for negative n. The fact that the isomorphism is between triangle functors supplies compatibility with suspension and connecting morphisms. An objectwise collection of unrelated isomorphisms would not be enough. The usual compatible power identifications give the Z-action coherence; no additional independent choice for every n is needed.

For fixed first argument, the source is a direct sum of cohomological Hom functors in the second argument. Direct sums preserve exact sequences of abelian groups, and therefore also of vector spaces. The target is cohomological. Naturality with connecting maps gives a morphism of long exact sequences. If the comparison is an isomorphism for two vertices of a triangle in all k, a five-term exact-sequence argument gives it for the third vertex in every k. Shift closure follows by reindexing k. Induct on brutal truncations of a bounded complex to pass from stalks to all second arguments. Apply the same argument contravariantly to the first argument. This establishes exactly the all-pairs, all-k claim.

There is also a direct finiteness check omitted as unnecessary from the author's proof. If representatives of M and N have terms only in degrees [a,b] and [c,d], respectively, then a map to N<n>[k] can occur only for

    c-b-k <= n <= d-a-k.

Indeed, some source degree i must have both M^i and N^{i+n+k} nonzero. Thus for fixed M,N,k only finitely many grading summands occur. The written direct sum does not hide a completion, infinite-product totalization, or convergence argument. The generation used here is finite triangulated generation from all objects of P. One need not assume idempotent completeness or an infinite-coproduct compact-generation theorem. If retracts are considered, the comparison property is retract-stable as well.

At k=0, the n=0 summand is the ordinary map induced by R, so injectivity proves faithfulness. If R(M)=0, the comparison kills id_M and hence M is zero. To make the final conservativity step explicit, an exact functor sends a cone of f to a cone of R(f); if R(f) is invertible, the cone vanishes by reflection of zero objects, so f is invertible. The author's conclusion is valid.

The comparison is at least an isomorphism of abelian groups with the stated additive hypotheses. Under the usual F-linear-functor convention it is an F-linear isomorphism. The argument and the grading conclusion need no extra assertion about linearity beyond that convention.

## 3. Proposition 3.1 and Lemma 3.2

A t-exact triangle functor restricts to an exact functor on hearts. This follows by applying heart cohomology to the image of the triangle of a short exact sequence. The canonical Yoneda-to-triangulated-Hom maps are isomorphisms in degrees zero and one for any t-structure. In degree one, completing a morphism M -> N[1] to a triangle yields an extension with middle term in the heart; this is inverse to the connecting-morphism construction.

These identifications are natural under the t-exact functor. Tate twist must preserve the source heart, as expressly assumed, so the same statement applies to N<n>. Higher extensions map to compositions of degree-one connecting morphisms. Consequently the diagram involving graded Yoneda Ext, graded derived Hom, ordinary derived Hom, and ordinary Yoneda Ext commutes. When the vertical canonical comparisons are isomorphisms, Proposition 2.1 yields the required Ext comparison. Canonical derived-realization equivalences provide a sufficient condition. An arbitrary abstract equivalence with no realization compatibility would not supply that conclusion.

The manuscript does not infer higher Yoneda Ext from a Hom dimension formula or from the mere existence of a heart. This is a substantive and correct limitation. It also does not infer t-exactness from the orbit-Hom comparison alone. Its shifted one-stratum example demonstrates the latter point; that shifted functor is not being claimed to extend the parity inclusion.

The gluing test is correct: all stratum *-restrictions test the nonpositive aisle and all !-restrictions test the nonnegative aisle. The assumed compatible local functors transport both tests. Constructing separate local functors without the restriction comparisons would leave a gap, and the manuscript explicitly says so.

## 4. One-stratum construction

On C^d, finite-rank local systems are constant and higher cohomology of the constant sheaf vanishes. The usual bounded Postnikov construction then splits: at each step its connecting morphisms between the already split cohomology objects are in positive-degree Hom groups and vanish. This justifies the equivalence with the bounded derived category of finite-dimensional vector spaces, not just an identification of its Grothendieck group.

Parity objects are finite sums of ordinary shifts of the constant sheaf, with no maps between distinct shifts. A bounded complex in this semisimple additive category splits into its homotopy cohomology terms. If L=F_X{d}, the bookkeeping identity is

    F_X{r}[i] = L<d-r>[i+r-d].

Applying exact forgetfulness from graded vector spaces and passing to derived categories therefore sends this object to F_X{r+i}. It is the parity inclusion when i=0, preserves the local perverse heart, and trivializes Tate twist. These equivalences and derived functors yield actual functors, not an unsupported choice of cones.

Finite-dimensional graded spaces have finite grading support, so each ungraded linear map is the unique finite sum of its homogeneous components. Both hearts are semisimple, and positive Yoneda Ext vanishes. The asserted grading is therefore complete in this case and in the finite open-and-closed disjoint-union case. No gluing across a nontrivial stratum boundary has thereby been solved.

## 5. Coherence calculation and five-approach status

The differential calculation for z=f_3 h_21-h_32 f_1 is correct: the two degree-zero triple composites cancel. The prospective next filler has degree -2. Its existence requires the degree -1 closed class for those chosen null-homotopies to vanish, with the usual sign convention understood. Changing choices can change the class. The author neither presents a choice-independent obstruction nor supplies a geometric nonvanishing example. Accordingly this explains why a naive totalization is unjustified; it is not a counterexample.

The five recorded approaches have distinct purposes and appropriately bounded outcomes. Only the conditional categorical arguments and elementary special case are claimed as proved. The established geometric constructions are literature checks, not independently reproved here. No asserted computational experiment replaces a missing mathematical construction. The count of five is an investigation log, not evidence of general solvability.

## 6. Current-literature check

Riche's affine-flag paper is published in Revista de la Union Matematica Argentina 69(1) (2026), 373–410, online 2026-04-20. Theorem 5.5 gives the degrading derived functor and perverse t-exactness under the paper's assumptions. I checked Section 3.3, the beginning of Section 5, Section 2.7 and Lemma 2.10, and visually checked Figure 1. The manuscript correctly records the lattice restrictions, component bounds, dual invariant self-duality, and pseudo-logarithm/isogeny condition. This is a restricted positive-characteristic etale affine-flag result. The introduction still identifies the general comparison problem; the theorem is not a theorem for arbitrary complex affine-stratified varieties. [R]

Eberhardt–Scholbach's inspected version identifies the reduced-motivic mixed category with the Achar–Riche construction under its stated resolution assumptions. Section 1.6.1 expressly separates the modular/integral realization problem from the complex-coefficient case. Thus this comparison cannot simply be relabelled as the desired general ordinary-perverse forgetful functor. [ES]

Targeted current searches and the primary sources support the limited status statement, not a proof that no later solution exists. The acceptance preserves this bounded-literature qualification.

## 7. Integrity and release boundary

The independent verifier checks a fixed external archive and manifest identity before reading ZIP members, rejects duplicate JSON keys and non-finite JSON constants, checks UTF-8 and member identity, never extracts members, and never executes author content. The utility itself was tested with isolated normal and optimized interpreters, relocation, and a hostile working directory containing import/cache decoys. Altered, truncated, absent, and symlinked inputs were rejected; parser unit checks rejected duplicate keys, non-finite numbers and invalid UTF-8. See `integrity.json` for all 14 results and their explicit scope.

The four source PDF hashes and sizes were recomputed locally and matched the author's source metadata. The complete target catalog/problem/report records were independently matched, including the absence of an inherited report entry and the complete-pair review hash. Only dataset identity and match metadata appear in this audit package. The author validation receipt's historical retrieval details were not treated as independent proof of retrieval.

This separate audit includes authored assessment, acceptance, public bibliographic/identity metadata, and a read-only verification utility. It contains no copied source PDFs, screenshots, extracted source text, raw datasets, or private coordination material. Byte tests and hashes are not mathematical proof certificates. No general construction, general counterexample, novelty, or exhaustive literature search is certified.

## Primary references

- [OWR] Achar, joint with Riche, contribution to *Enveloping Algebras and Geometric Representation Theory*. [Publisher](https://ems.press/journals/owr/articles/13682), [DOI](https://doi.org/10.4171/OWR/2015/25).
- [AR] Achar–Riche, *Modular perverse sheaves on flag varieties II: Koszul duality and formality*. [Preprint v2](https://arxiv.org/abs/1401.7256v2), [journal DOI](https://doi.org/10.1215/00127094-3165541).
- [R] Riche, *Mixed modular perverse sheaves on affine flag varieties and Koszul duality*. [Published PDF](https://www.inmabb.criba.edu.ar/revuma/pdf/v69n1/v69n1a24.pdf), [DOI](https://doi.org/10.33044/revuma.5035).
- [ES] Eberhardt–Scholbach, *Integral motivic sheaves and geometric representation theory*. [Preprint v2](https://arxiv.org/abs/2202.11477v2), [journal DOI](https://doi.org/10.1016/j.aim.2022.108811).
