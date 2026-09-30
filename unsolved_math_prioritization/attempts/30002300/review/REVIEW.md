# Independent source review: removing the simplex general-position condition

**Verdict: PASS_CREDITED_KNOWN_RESULT.** The assigned general-position
condition can be removed, by the published theorem of Akopyan, Bárány and
Robins. The frozen source application matches the original question.
Recommend **already_solved, 0/5 new attempts**. No mandatory mathematical
correction was identified.

This separate review used GPT-6 Astra at xhigh effort on 2026-09-30.
The reviewed SOURCE_STATUS.md has SHA-256
48d460bed68baef63064bab715d4148cedf9c42d28436a3e30eda7f17c728b34.
Its unchanged bytes are preserved in author_replay/SOURCE_STATUS.md.
This is a credited source audit, not a new decomposition theorem or a
human peer review.

## 1. Exact source match

The complete Pasechnik contribution in
[OWR 11/2013, pp.637–640](https://ems.press/content/serial-article-files/46446)
was inspected, including the displayed theorem and Question 3 on
pp.638–639. The vertex set is the intersection of the vertex sets of
triangulations of the compact polyhedron. The condition to remove is that
each $(d+2)$-subset spans the ambient space. The conclusion permits real
signed coefficients on nondegenerate simplices using those vertices.

The source switches between unit-density and probability terminology. The
existence of real coefficients is unchanged by normalization, so this does
not obstruct a source match. It does affect coefficient claims, which the
submitted artifact treats separately and correctly.

The [published 2018 version of *On moments of a polytope*](https://link.springer.com/article/10.1007/s13324-018-0226-8)
explicitly identifies Conjecture 7 as a corollary of Akopyan–Bárány–Robins
Theorem 1. The acknowledgment, integer-coefficient strengthening, subsequent
Conjecture 8 and older weak-nondegeneracy Theorem 9 were inspected directly
on printed p.262. The retained historical word “Conjecture” does not make
the general-position removal an unresolved claim in that publication.

## 2. Published theorem and allowed vertex set

[Akopyan–Bárány–Robins, *Algebraic vertices of non-convex polyhedra*,
Theorem 1](https://arxiv.org/abs/1508.07594v2) applies to bounded finite
unions of convex polyhedra. It gives an almost-everywhere indicator
decomposition with integer coefficients, using only algebraic vertices.
The complete relevant proof in Section 3 and its definitions were read
in the January 2017 author manuscript. The published 2018 paper independently
confirms the cited 2017 theorem and its application. No claim to have
retrieved a separate publisher-formatted 2017 PDF is needed.

The inclusion in the exact original vertex set is sound. Fix a triangulation
and a point $v$ that is not any simplex vertex. If a simplex contains $v$,
its minimal face at $v$ has positive dimension, and its tangent cone is
invariant along the linear span of that face. A simplex not containing $v$
has empty tangent cone there. The indicator decomposition of the
triangulation passes to tangent cones, up to null boundaries. Thus the
tangent indicator at $v$ is a sum of line-cone indicators, and $v$ is not
algebraic. Applying this to every triangulation proves
$A(P)\subseteq V(P)$.

This argument is also the necessity direction of the published theorem.
It neither identifies algebraic vertices with convex-hull vertices nor
chooses an arbitrary triangulation's extra vertices as allowed data.
Consequently the theorem supplies exactly

\[
\mathbf1_P=\sum_T a_T\mathbf1_T\quad\text{a.e.},\qquad
a_T\in\mathbb Z,\qquad \operatorname{Vert}(T)\subseteq V(P).
\]

No general-position assumption is present. For positive-volume $P$, the
allowed set necessarily spans the ambient space; this is consistent with
the theorem and does not reinstate a condition on every small subset.
The simplices that contribute ambient volume are nondegenerate. Origin
vertices are allowed normally in this representation; the origin exception
in the separate affine-denominator problem is not a restriction here.

## 3. Degeneracies in the proof

The induction on dimension in Theorem 1' applies to compactly supported
polyhedral step functions. Its signed sections have algebraic vertices only
where the original function has algebraic vertices. The line-cone
argument survives signs: if its invariant direction is transverse to the
section hyperplane the jump vanishes almost everywhere; if it is tangent,
the signed section remains a finite signed combination invariant in that
direction.

A nonzero bounded-support function has an algebraic vertex, allowing an
apex to be chosen from the original allowed set. Coning the section
representations and telescoping jumps on generic rays gives the stated
representation. A supporting hyperplane containing the apex contributes
only a lower-dimensional cone and can be omitted in the ambient
almost-everywhere identity. Therefore the proof does not require
perturbing vertices into general position. Integer-valued sections remain
integer-valued, and the induction introduces no division, giving the
integer conclusion for indicators.

The artifact's explanation of these details is valid. It does not turn a
signed representation into an unsigned triangulation. Simplices may
overlap or extend outside the original set, with cancellation of the
corresponding measures.

## 4. Measures, normalization and separate questions

Integrating the almost-everywhere identity over arbitrary Borel sets gives
the unit-density measure equality. Boundaries and lower-dimensional pieces
have zero ambient Lebesgue measure. If $P$ has zero volume, this measure
is zero and the empty representation suffices; there is no associated
ambient uniform probability measure to normalize.

For positive volume, putting $\nu_T=\lambda_T/\operatorname{Vol}(T)$ and
$\nu_P=\lambda_P/\operatorname{Vol}(P)$ gives coefficients

\[
b_T=a_T\frac{\operatorname{Vol}(T)}{\operatorname{Vol}(P)}.
\]

They are real, may be negative, and sum to one. They need not be integers.
The artifact does not conflate this with the integer unit-density result.
No singular measure supported on a degenerate simplex is introduced.

Integer coefficients do not prove that a *set* of distinct simplices can
always be assigned coefficients only in $\{-1,1\}$. Repeating a simplex
would not establish that separate assertion. The later published
Conjecture 8 and neighboring source Question 2 are correctly excluded
from this verdict. The related Fantappiè-denominator target is likewise a
different question, despite using some of the same source definitions.

## 5. Exact checks and disposition

All 699 submitted exact assertions reproduce their receipt byte for byte.
The independent checker imports no submitted code. It evaluates polygon
moments using Green's boundary formula, compares signed fan coverage with
winding number, varies the apex and affine coordinates while allowing
degenerate fan terms, and verifies the three-tetrahedron prism partition
through its exact barycentric inequalities. Probability normalization is
checked independently through the moment identities.

All **4,314 independent exact assertions pass**, including 960 signed
coverage comparisons and 336 prism partition points. These examples
support the source application and its handling of degeneracy; they do
not replace the published general theorem or resolve the separate
universal $\pm1$ question.

The exact assigned question has a known affirmative answer, with credit
to Akopyan–Bárány–Robins (2017), explicitly corroborated by the 2018
publication. Preserve zero new proof-search attempts and make no
campaign discovery claim. No mathematical revision to the frozen
source artifact is required.

Run python author_replay/verify.py and python independent_checks.py to
reproduce the respective JSON receipts. Keep the source snapshot required
by the independent hash check. Third-party PDFs and rendered source pages
are excluded from the public review bundle.
