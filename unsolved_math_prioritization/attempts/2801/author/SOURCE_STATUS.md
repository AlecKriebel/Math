# Source identity, chronology and prior-attempt gate

## 1. The exact target

- Queue rank: **477**.
- Numeric ID: **2801**.
- Code: **KP-3.3**.
- Catalog title: **Kirby Problem 3.3**.
- Concrete subject: existence of geometric ideal tetrahedral triangulations of
  cusped hyperbolic 3-manifolds.
- Category: **Topology**, specifically hyperbolic 3-manifold geometry.
- Observed queue state: `queued`, `0/5`.
- Canonical numeric URL: <https://www.unsolvedmath.com/problems/2801>.
- Indexed alias: <https://www.unsolvedmath.com/problems/KP-3.3>.

The source asks:

> Does every cusped hyperbolic 3-manifold have a geometric ideal triangulation?

This wording was visually checked in **K3: A New Problem List in
Low-Dimensional Topology**, edited by R. İnanç Baykur, Robion C. Kirby and Daniel
Ruberman, **Problem 3.3, printed page 134**, scribed by Marc Lackenby. The author's
preliminary book version is hosted by Berkeley:

<https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf>

The relevant numbering is the **2026 K3 list**, not an unqualified reference to
Problem 3.3 of the 1997 list. Section 3.1, printed page 131, makes completeness
part of its hyperbolic-metric convention. The finite-volume, noncompact reading
is also explicit in Yoshida's original printed conjecture (1996, p.37).

The remark's reference to a 3-sphere at infinity of hyperbolic 3-space is a
source typo: that visual boundary is S². It does not change the existence
question or Ge's correctly formulated geometric target.

## 2. Retrieval and version limits

The exact numeric URL returned 403 via direct HTTP and in the cloud browser;
the indexed alias was readable through web search and matches the catalog.
The source identification does not assert that the exact numeric page was read
successfully on 3 October. No CAPTCHA was solved and no access restriction was
bypassed.

The imported corpus revision supplied for this task was
`37e53eabe540fb458758e198be61634bd02ee008`. Both supplied byte hashes were checked:

- problems.json SHA-256:
  `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`
- research_results.json SHA-256:
  `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`

The ID 2801 problem record has the displayed statement and category. Its dated
17 August 2026 literature triage reported partial progress, predating Ge's
23 September preprint. That triage linked
<https://aimath.org/pastworkshops/kirbylistrep.pdf>, which is a **four-page workshop
report**, not the 436-page K3 book. The book itself was therefore obtained and
checked rather than relying on the imported reference label.

## 3. Precise mathematical scope

The target concerns a complete, finite-volume, noncompact hyperbolic metric on
a 3-manifold without geodesic boundary. Orientability is not assumed. An ideal
triangulation is understood in the usual face-pairing sense: distinct ideal
vertices, edges or faces of an abstract tetrahedron may become identified in the
quotient. The requirement is not an embedded simplicial triangulation of the
cusp compactification with distinct global vertices.

Each constituent tetrahedron must be geometric and nonflat. In the orientable
case, compatible orientation choices give shape parameters in the upper
half-plane. Merely obtaining a finite cover, a flat/negatively oriented
tetrahedral subdivision, a topological triangulation, or an angle structure
alone would not settle the exact target. Incomplete metrics are excluded.

Ge's Theorem 1.1 and Section 2.2 explicitly cover all of the above scope,
including the nonorientable case. Sections 5–6 contain additional assertions
about boundary and applications; those are not needed for this certificate and
are not certified here.

## 4. Relevant chronology and primary sources

1. **Yoshida, 1996:** *Ideal tetrahedral decompositions of hyperbolic
   3-manifolds*, Osaka J. Math. 33(1), 37–46. The introduction prints the
   finite-volume noncompact conjecture and proves a special two-polyhedron
   case. The paper was received 17 October 1994; this is not an assertion that
   the conjecture first arose that day. Original article and publication
   metadata: <https://ir.library.osaka-u.ac.jp/repo/ouka/all/10590/> and
   <https://ir.library.osaka-u.ac.jp/repo/ouka/all/10590/ojm33_01_03.pdf>.
2. **Epstein–Penner, 1988:** *Euclidean decompositions of noncompact hyperbolic
   manifolds*, J. Differential Geom. 27(1), 67–80,
   <https://doi.org/10.4310/jdg/1214441650>. This is the classical input producing
   finite geometric ideal polyhedral decompositions. The original PDF endpoint
   returned an HTML block page in this session; the input's precise role was
   checked in Ge Section 2.2 and independently corroborated in the published
   Luo–Schleimer–Tillmann article. This audit does not claim to have reproved
   or fully reread the original Epstein–Penner paper.
3. **Luo–Schleimer–Tillmann, 2008:** *Geodesic ideal triangulations exist
   virtually*, Proc. AMS 136(7), 2625–2630, Theorem 1. The result is a finite
   regular-cover theorem and is not the base-manifold conclusion. Published
   primary text: <https://sschleimer.warwick.ac.uk/Maths/2008geodesic_ideal_tri.pdf>.
4. **Futer–Hamilton–Hoffman, 2022:** *Infinitely many virtual geometric
   triangulations*, Journal of Topology 15(4), 2352–2388. The published abstract
   strengthens the finite-cover conclusion, not the exact base-manifold target:
   <https://londmathsoc.onlinelibrary.wiley.com/doi/abs/10.1112/topo.12271>.
5. **K3, 2026:** Problem 3.3 still lists the question with classical and virtual
   progress, as checked in the book linked above. Its dated statement must not
   override subsequently posted work.
6. **Huabin Ge, 23 September 2026:** *Geometric ideal triangulations of
   hyperbolic 3-manifolds*, **arXiv:2609.27635v1**, Theorem 1.1; compatibility
   machinery in Lemma 2.1, Lemma 3.2, Proposition 3.3 and Theorem 3.4; geometric
   descent in Section 4. The full primary text was read:
   <https://arxiv.org/abs/2609.27635v1>,
   <https://arxiv.org/html/2609.27635v1>,
   <https://arxiv.org/pdf/2609.27635v1>.

The arXiv page showed v1 submitted at 10:00:09 UTC on 23 September, 20 pages,
and no subsequent version, withdrawal or journal reference. Focused searches
for the exact identifier and correction/gap/withdrawal terms did not locate a
primary correction. This is bounded negative evidence, not a guarantee that no
unindexed critique or correction exists. All credit for the proposed full
resolution remains with Ge; the record does not establish historical first
priority beyond locating this exact prior theorem.

## 5. Genuine prior-attempt accounting

The live `AlecKriebel/Math` queue was read through the GitHub connector and
showed rank 477 at queued 0/5. The canonical attempts-directory listing contains
no ID 2801 directory; a direct ID 2801 path lookup returned 404. Bounded default-
branch code searches for 2801 and KP-3.3 and repository issue/PR search for 2801
returned no matches. Current state, history and research-log files contained
no 2801/KP-3.3 entry. The hash-verified research-results dictionary contains no
KP-3.3 record; the problem's imported background contains literature triage,
not a mathematical campaign attempt.

Accordingly, no genuine earlier substantive attempt was recovered and no new
original attempt has been spent. This source-verification activity is counted
separately at **0/5 original turns**. The negative repository search is not
presented as proof that no private or off-repository attempt ever existed.

## 6. Recommended disposition after the independent gate

If a fresh full audit accepts the argument, record an **attributed full
affirmative result from Ge's recent preprint**, with the campaign status
`already_solved` qualified as preprint-based and original budget 0/5. Do not label
this campaign a solver, create a new paper or DOI, silently treat the result as
peer-reviewed, or claim the exact numeric webpage was successfully retrieved.
Until that gate, this is a held source-certificate candidate.
