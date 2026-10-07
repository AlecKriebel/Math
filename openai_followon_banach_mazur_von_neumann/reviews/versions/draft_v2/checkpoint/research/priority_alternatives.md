# Independent priority and alternative-route audit

Audit checkpoint: 2026-10-06 22:14 PDT (2026-10-07 05:14 UTC).
Auditor scope: primary literature status, public provenance, companion
manuscripts, and alternative mechanisms. This is independent of the separate
mathematical and Lean audits of source family 295. No external person was
contacted. No Git index, branch, commit, or upstream clone was changed.

## Strongest checked findings

1. Roydor's exact conditional ordinary-distance theorem is directly readable
   in the primary-author CIRM slides, not merely a search snippet. It includes
   both the algebra and its canonical predual, with an algebra-dependent
   positive threshold. The journal's bibliographic metadata is verified;
   independent access to the full journal article is not claimed here.
2. The unconditional completely bounded result is older and materially
   different. Its exact theorem was read in Ricard--Roydor's arXiv v2 PDF.
3. No duplicate ordinary-distance consequence was found in any upstream
   preprint's searchable TeX/Markdown/BibTeX at the pinned commit. The most
   relevant companion claims strong Kadison--Kastler stability, which does
   not directly supply the required abstract ordinary-distance bridge.
4. An elementary adjoint argument transfers any algebra threshold to the
   canonical-predual implication with the same threshold. This is a verified
   deduction, not a novel priority claim.
5. No independent all-algebra ordinary-distance theorem bypassing the
   cohomological input was established by this audit. A failed search is not
   evidence of novelty or a proof that no such theorem exists.

## Primary statement and conventions: Roydor

Source: Jean Roydor, *Banach--Mazur stability of von Neumann algebras*,
[CIRM slides](https://www.cirm-math.fr/RepOrga/2169/Slides/Roydor_Slides.pdf),
October 2020. Saved original PDF is `sources/roydor/roydor_slides.pdf`; this
audit's text extraction is `sources/priority/roydor_slides.txt`.

Theorem 2 appears on PDF pages 28--29 and is repeated on pages 57--62.
In mathematical notation its statement is:

If \(M\) is a von Neumann algebra and
\(H^2(M,M)=H^3(M,M)=0\), then there is \(\varepsilon_M>0\) such that,
for every von Neumann algebra \(N\), the following are equivalent:

- \(M\) and \(N\) are Jordan \(*\)-isomorphic;
- \(M\) and \(N\) are linearly isometric;
- \(L^1(M)\) and \(L^1(N)\) are linearly isometric;
- \(d(L^1(M),L^1(N))<1+\varepsilon_M\);
- \(d(M,N)<1+\varepsilon_M\).

Here the source expressly calls \(L^1(M)\) the predual. There is no
separability hypothesis in this statement. Pages 18--19 define the
multiplicative Banach--Mazur distance as the infimum of
\(\|T\|\|T^{-1}\|\) over linear isomorphisms. Pages 30--32 define cochains
as **all bounded** multilinear maps into the coefficient bimodule and
cohomology as kernel divided by the actual image. Completely bounded
cochains are introduced as a separate restriction. Thus the stated input
is ordinary bounded Hochschild cohomology with self-coefficients, not just
normal, completely bounded, reduced, or ambient-operator coefficients.

One caution concerns the slides rather than the theorem: their displayed
Hochschild differential on pages 31--32 has apparent indexing/sign typos
(the interior sum stops at \(k-1\), with last sign \((-1)^k\)). The standard
degree-\(k\) differential has the interior sum through \(k\) and final
sign \((-1)^{k+1}\). The formula must be checked against the journal or
standard cohomology source before reproducing it. The theorem's ordinary
bounded cochain convention remains explicit.

The journal citation is Roydor, *Journal of Topology and Analysis* **14**
(3) (2022), 767--792,
[DOI 10.1142/S1793525321500151](https://doi.org/10.1142/S1793525321500151).
The publisher-deposited Crossref record, downloaded to
`sources/priority/roydor_crossref.json`, confirms issue 03 and pages
767--792, online publication 2020-12-11, and print publication 2022-09.
Its record-creation timestamp is 2020-10-22; that is metadata provenance,
not itself a theorem-disclosure date. This corrects unreliable secondary
indexing that lists issue 2. Publisher full and abstract URLs returned 403
through the web reader during this audit. The dedicated primary-source
auditor is separately pursuing full-article access.

The [CIRM conference page](https://conferences.cirm-math.fr/2169.html)
dates the meeting to 12--16 October 2020. Together with the source title
page this verifies a public October 2020 disclosure of the conditional
reduction, before the 2022 print issue. It does not establish its earliest
possible disclosure anywhere.

The same slides, pages 47--48, already give unconditional ordinary-distance
stability when the type \(\mathrm{II}_1\) summand has property \(\Gamma\),
a Cartan MASA, or absorbs the hyperfinite factor. These established cases
must not be advertised as new. The numerical bounds in the slides belong
to that source version; they are unnecessary for the proposed
algebra-dependent qualitative consequence.

## Exact older completely bounded theorem

Source: E. Ricard and J. Roydor,
[*A non-commutative Amir--Cambern theorem for von Neumann algebras and
nuclear \(C^*\)-algebras*](https://arxiv.org/abs/1108.1970), arXiv v2,
2013-06-24. Exact theorem and proof were read from the saved PDF
`sources/roydor/ricard_roydor_1108.1970v2.pdf`; extraction is
`sources/priority/ricard_roydor_1108.1970v2.txt`.

Theorem A, PDF page 1, says that if \(A\) is a separable nuclear
\(C^*\)-algebra **or any von Neumann algebra**, some
\(\varepsilon_0>0\) satisfies

\[
 d_{cb}(A,B)<1+\varepsilon_0\quad\Longrightarrow\quad
 A\cong B\text{ as }C^*\text{-algebras}
\]

for **every \(C^*\)-algebra** \(B\). In this exact v2 theorem one may
take \(\varepsilon_0=4\cdot10^{-6}\) for von Neumann algebras. The
definition of \(d_{cb}\) uses completely bounded complex-linear
isomorphisms and their completely bounded inverses. The proof's
cohomological input is completely bounded cohomology. Page 2 explicitly
distinguishes this from then-unknown ordinary bounded cohomology.

The published article is *Journal of Functional Analysis* **267** (4)
(2014), 1121--1136,
[DOI 10.1016/j.jfa.2014.05.018](https://doi.org/10.1016/j.jfa.2014.05.018).
The exact v2 numerical constant should not silently be represented as
the final journal theorem's constant. Roydor's later slides use a smaller
safe constant for their cb comparison.

The arXiv record verifies v1 submitted 2011-08-09 and v2 revised
2013-06-24. A [Glasgow seminar notice](https://www.gla.ac.uk/schools/mathematicsstatistics/events/details/?id=8634)
already announced discreteness for the cb distance on 2011-05-24.
This earlier public notice is weaker evidence than the exact readable
arXiv theorem, but suffices to avoid attributing the cb breakthrough to
this project.

The inequality \(d_{BM}\le d_{cb}\) has the wrong direction for using
this theorem from a small ordinary distance. Moreover, opposite algebras
are Jordan \(*\)-isomorphic and linearly isometric while a von Neumann
algebra need not be \(*\)-isomorphic to its opposite. The ordinary target
therefore correctly asks for a Jordan conclusion.

## Upstream versions, public provenance, and companion overlap

Pinned and independently checked remote-main commit:
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
The read-only command `git ls-remote` returned this same hash for
`refs/heads/main`; saved output is
`sources/priority/upstream_remote_main.txt`. The local log calls it
the initial commit, with committer date 2026-10-06T14:58:50-07:00.
No later correction on remote main was visible at the audit checkpoint.
This is a version check, not a statement that no correction could exist
elsewhere. Manuscript dates in folder names do not prove earlier public
priority. Public availability at this repository hash was directly
verified on the audit date.

The upstream [repository README](https://github.com/openai/math) says
the manuscripts were produced by an internal OpenAI model, warns that
unformalized results may have issues, and promises preservation of
released versions. The family-295 README supplies authorship **OpenAI**
and a manuscript-specific BibTeX entry. Any consequence note must cite
that supplied attribution and make the dependence explicit.

A case-insensitive full search over all upstream preprints' `.tex`,
`.md`, and `.bib` files for `Banach.Mazur`, `Banach.Stone`, `Roydor`, and
`Amir.Cambern` found no ordinary-distance consequence duplicate. The
only relevant hits outside family 295 are references to Ricard--Roydor
in the strong Kadison--Kastler companion. This search includes the
actual source TeX, not only the catalog or abstracts.

Relevant exact statements inspected:

| Companion | Statement inspected | Effect on this project |
| --- | --- | --- |
| *Universal strong Kadison--Kastler stability* | Introduction's main theorem: uniformly small common-representation unit-ball gap gives conjugacy by a small unitary, for arbitrary Hilbert spaces and algebras. Foundations use a **cb** multiplication correction and a UCP map already close in **cb** norm to a faithful normal representation. | Different hypothesis. An arbitrary ordinary nearly isometric Banach-space isomorphism is not such a UCP correspondence. No direct duplicate or checked bypass follows. |
| *Kadison's similarity theorem through uniform derivation estimates* | Introduction's main theorem: every bounded unital algebra homomorphism of a complex unital \(C^*\)-algebra into \(B(H)\) is similar to a \(*\)-homomorphism. | Requires exact multiplicativity. Our Banach-space map need not be multiplicative, so invoking similarity alone transfers the central correction problem rather than solving it. |
| *A positive solution to Tingley's problem* | Main theorem in `build/main.tex`: an exact onto sphere isometry of nonzero real Banach spaces extends to an exact onto real-linear isometry. | Exact sphere isometry is unavailable from fixed distortion \(1+\varepsilon\). An unproved quantitative upgrade would be the missing step. |
| *Near inclusions of von Neumann algebras without small spatial embeddings* | Introduction's main theorem constructs small **one-sided** gaps without small implementing unitaries; it expressly provides no reverse gap. | It neither disproves the two-sided ordinary BM target nor supplies its proof. |

These companion assertions were inspected for semantic overlap; their
proofs were not independently validated by this priority audit. Promoting
any of them to a replacement dependency would require a fresh proof audit.

Proposed attribution if family 295 passes mathematical verification:
the all-algebra ordinary-distance conclusion is an **immediate consequence
of the newly available cohomology input and Roydor's published reduction**.
The reduction, predual transfer, Jordan/isometry equivalences, and cb
stability are inherited. No claim of inventing a new perturbation method,
independently proving the base cohomology conjecture, or being first is
justified by this search alone.

## Independent elementary transfer to canonical preduals

Let \(S:M_*\to N_*\) be any bounded complex-linear Banach-space
isomorphism. The canonical dual identifications give
\(S^*:N\to M\). Its inverse is \((S^{-1})^*\), and

\[
 \|S^*\|=\|S\|,\qquad
 \|(S^*)^{-1}\|=\|S^{-1}\|.
\]

Taking infima and using symmetry gives the extended-distance inequality

\[
 d_{BM}(M,N)\le d_{BM}(M_*,N_*).
\]

Consequently, once an algebra threshold \(\varepsilon_M\) is proved,
the exact same threshold proves the predual implication. No converse
inequality is needed. The argument works for arbitrary cardinalities.
If no bounded isomorphism exists, the relevant distance is infinity and
the assertion is automatic.

For completeness, a Jordan \(*\)-isomorphism \(J:M\to N\) is an order
isomorphism on the self-adjoint parts: positivity is preserved because a
positive element is the square of a self-adjoint element, and the inverse
has the same property. An order isomorphism preserves every existing
bounded increasing supremum. Hence \(J\) and \(J^{-1}\) are normal. Their
preadjoints are inverse linear isometries of the canonical preduals. The
linear-isometry/Jordan equivalence itself is the established Kadison
isometry theorem, and is also explicitly stated in Roydor's Theorem 2.

The zero algebra can be handled separately. If the distance is literally
defined by the infimum of norm products, its self-distance is zero rather
than one; this harmless degeneracy must not be obscured by a blanket
claim that every Banach--Mazur distance is at least one.

## Materially distinct route ledger

| Route | Mechanism and evidence | Status | Exact remaining gap |
| --- | --- | --- | --- |
| Roydor plus family 295 | Ordinary bounded \(H^2,H^3\) implies Jordan rigidity; exact source theorem directly read. | Conditional reduction verified here. | Separate full verification of family 295 and actual journal theorem. |
| Convert ordinary to cb and invoke Ricard--Roydor | Older cb theorem has stronger \(*\)-isomorphism conclusion; ordinary maps provide no matrix norm estimates. | Blocked as an automatic reduction. | An ordinary-to-cb correction after a legitimate Jordan orientation split. The inequality between distances alone cannot provide it. |
| Use strong Kadison--Kastler companion | Construct faithful representations with small two-sided unit-ball gap, then use spatial stability. | Blocked as a bypass. | The representation bridge from abstract ordinary near-isometry is absent; Roydor's displayed Jordan-KK comparison itself assumes \(H^2,H^3=0\). |
| Use similarity companion | Correct a bounded homomorphism by conjugating its representation. | Blocked as a bypass. | Exact bounded homomorphism must first be constructed from a map with a nonzero multiplication defect. |
| Use Tingley/sphere geometry | Convert exact sphere data to linear isometry. | Blocked as a bypass. | Quantitative rigidity for almost sphere isometries; replacing that by an assumption is the core problem again. |
| Finite-dimensional compactness | Finitely many finite-dimensional \(C^*\)-algebra types at each vector-space dimension; BM distance one is attained in finite dimensions. | Independent proof below; established subcase only. | Does not treat infinite-dimensional factors or their direct integrals. |

### Checked finite-dimensional argument

Fix a finite-dimensional complex von Neumann algebra \(M\) of dimension
\(D>0\). Every complex von Neumann algebra linearly isomorphic to it
has the same finite dimension, hence is a direct sum of full matrix
algebras with \(D=\sum_j n_j^2\). There are finitely many such multisets.

In equal finite dimensions, if \(d_{BM}(X,Y)=1\), choose isomorphisms
\(T_k\) with \(\|T_k\|=1\) and
\(\|T_k^{-1}\|\to1\). A subsequence converges in operator norm to
\(T\). For every \(x\), the inequalities
\(\|x\|/\|T_k^{-1}\|\le\|T_kx\|\le\|x\|\) pass to the limit,
so \(T\) is an isometry; equal dimensions make it onto. Kadison's
isometry theorem then gives Jordan \(*\)-isomorphism for the algebras.

Therefore each of the finitely many non-Jordan-isomorphic algebra types
of dimension \(D\) is at BM distance strictly greater than one from
\(M\). Half the smallest positive gap supplies \(\varepsilon_M>0\).
If there are no other types, take any positive threshold. A close
comparison algebra must have dimension \(D\), so this proves the algebra
target for this \(M\). The adjoint inequality proves its predual target.
No cohomological input was used. This argument is preserved as a boundary
check and a genuine distinct proof mechanism, not as a novel result.

## Search record and limitations

Searches on 2026-10-06 PDT included exact-title and DOI queries; combinations
of ordinary Banach--Mazur, Jordan, von Neumann, predual, and Hochschild;
Amir--Cambern/JB-algebra variants; current 2024--2026 variants; Roydor's
institutional homepage; publisher pages; arXiv history; and the complete
upstream source-tree search described above. Technical conclusions rely
on primary sources and explicitly checked deductions. Secondary indexes
were used only to discover source locations and were not accepted as proof
of hypotheses, priority, or constants.

The target's unconditional all-algebra status is not certified by this
priority file. There is no identified duplicate full consequence at the
checked upstream version, but the audit does not prove absolute novelty.
Mathematical completion and publication readiness remain subject to the
parent effort's dependency checks and complete-package reviews.

Checkpoint estimates for this assigned audit: priority/overlap task 90%;
independent alternative route for the full mathematical target 15%.
These estimates are not proof evidence. Full-project mathematical and
publication estimates belong in the central research log.
