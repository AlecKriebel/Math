# Independent second adversarial preprint review

Review date: 23 September 2026. Main review and source checks completed at
13:41 UTC; final report checkpoint follows below.

Scope: mathematical correctness and readiness for circulation as an unrefereed
preprint, not suitability for journal acceptance. I independently reconstructed
the rigidity argument from finite polytopes retaining two fixed simplices before
checking the countable construction. I did not read any previous audit report or
reviewer conclusion. The other review's reasoning and verdict were not supplied
to me. No manuscript, source, verifier, or publication material was changed.

## Exact reviewed artifacts

SHA-256:

| Artifact | Hash |
| --- | --- |
| `manuscript/paper.tex` | `ce8a48dc12ac9d80144a7de7391f2583c6d567c5d4d1067c3be122bf10283b29` |
| `output/pdf/paper.pdf` | `62982a0e0508edabbfea63f4b5dc69ffe928d7c657103ee3d31296a6393e5d8c` |
| `sources/fps2012.pdf` | `1338d24d5b312a80a45ff6b173108648517bbdca141f66ff14c58613e9e77d16` |
| `sources/owr2009.pdf` | `e3c62551bf9bb9fadefc98d7f6bb82661a254ba6ff93c42b4afbf8eef21bf6cd` |
| `verification/verify.py` | `9896313fe2cebcd5ed0bed6aef77b649a7c369fe72a56e768d3dda28489e4764` |

The TeX was read in full. All four preprint PDF pages were rendered and visually
inspected, and their extracted text was compared with the argument in the TeX.
The published FPS statement, simplex lemma, and proof on printed pages 499 and
502--504 were read directly. The OWR contribution on printed pages 2907--2909
was read directly. The central source statement pages and FPS simplex lemma
were also visually inspected.

## Verdict and necessary changes

**No required mathematical or preprint-presentation correction found.** The
theorem, countable decomposition, deficit identity, both directions of the
equality characterization, and finite retained-pair bound withstand this review.
The current manuscript is ready to circulate as an unrefereed preprint with its
existing explicit qualification about priority and AI assistance.

There is no identified unsupported claim carrying the mathematical argument.
The proof does not merely replace the original equality problem by an equivalent
unproved decomposition claim: the decomposition is established by an explicit
finite insertion construction. The finite alternative independently preserves a
strictly positive defect through approximation.

## First attack: a fixed finite witness survives approximation

Relevant manuscript locations: lines 73--118 and 170--186; equations (2) and (5).

Start with a nondegenerate simplex
\(S=\operatorname{conv}(v_0,\ldots,v_n)\) whose vertices are extreme in \(K\).
If \(K\ne S\), there is an extreme point \(u\notin S\): otherwise the closed
convex hull of all extreme points would be contained in the closed set \(S\),
contradicting \(K\ne S\). Some facet of \(S\) is strictly violated by \(u\).
For a violated facet opposite \(v_i\), set
\(T=\operatorname{conv}(u,\{v_j:j\ne i\})\). Strict visibility gives positive
volume for \(T\) and disjoint interiors of \(S,T\). Their centroids satisfy
\(c_T-c_S=(u-v_i)/(n+1)\ne0\).

Choose the dense extreme-point sequence with these vertices first. At every
later finite stage retain the earlier simplices and subdivide only newly added
visible pyramids. This gives a finite decomposition of each \(P_m\) containing
the same \(S,T\), whose volumes \(a,b\) never change. No retriangulation of the
whole polytope is required. Thus the concern that the witness volumes could
shrink with the approximation is inapplicable to this construction.

Independently, for any point \(z\), completing the square gives

\[
a\|c_S-z\|^2+b\|c_T-z\|^2
=\frac{ab}{a+b}\|c_S-c_T\|^2
+(a+b)\left\|\frac{ac_S+bc_T}{a+b}-z\right\|^2.
\]

The finite simplex moment formula and weighted variance identity, with
\(z=g_{P_m}\), therefore imply

\[
\Delta_r(P_m)\ge
\frac{ab\|u-v_i\|^2}{(n+1)(n+2)|P_m|(a+b)}
\ge\frac{ab\|u-v_i\|^2}{(n+1)(n+2)|K|(a+b)}>0.
\]

All simplex vertices at every stage are actual extreme points of \(K\), so
their squared norms are at least \(r^2\). There is no use of continuity of the
extreme-point norm hypothesis under arbitrary Hausdorff approximation.

The increasing convex union \(C=\bigcup_mP_m\) is dense in \(K\) and contains
its interior. Hence \(1_{P_m}\to1_K\) almost everywhere. Boundedness of \(K\)
and dominated convergence give convergence of volume, every first moment, and
the second moment. Since \(|P_m|\ge a>0\), their normalized versions converge
as well. Consequently \(\Delta_r(P_m)\to\Delta_r(K)\), preserving the fixed
strict lower bound. This proves nonsimplex strictness without first invoking
countable integration. The coefficient in (5) is correct, and both sides scale
as length squared.

For \(K=S\), the same simplex identity shows that equality is equivalent to
the average vertex squared norm being \(r^2\), which under the individual
lower bounds is equivalent to every vertex norm being \(r\). Thus this route
also proves the full if-and-only-if statement, not just nonsimplex strictness.

## Second attack: construction, first intersections, and infinite sums

**Existence of the first intersection (lines 92--100).** This is valid, including
points whose ray first hits an edge or lower-dimensional face. For
\(x\in\operatorname{conv}(v,P_m)\setminus(P_m\cup\{v\})\), write
\(x=(1-t)v+tp\) with \(p\in P_m\) and \(0<t<1\). The ray from \(v\)
through \(x\) therefore meets \(P_m\); compactness supplies its first meeting
point \(y\), beyond \(x\). If every facet active at \(y\) were satisfied at
\(v\), those active inequalities would hold along \([v,y]\), while the
finitely many inactive inequalities would remain strict sufficiently close to
\(y\). This contradicts first intersection. At least one active facet is
strictly visible. Coplanar facets need not be called visible.

An interior point of a visible pyramid has its first intersection in the
relative interior of the pyramid's base facet. Thus two distinct visible
pyramids cannot have intersecting interiors. Coning vertex subdivisions of
the facets gives full-dimensional simplices. The elementary induction used to
subdivide a finite polytope needs no new vertices and works down to dimension
zero. It also handles nonsimplicial facets; matching triangulations along
shared lower-dimensional faces is unnecessary for the stated, measure-based
partition. Every later inserted extreme point is outside the previous hull,
since membership would express it as a convex combination of distinct other
points of \(K\).

**Density and coverage (lines 73--84 and 113--118).** A subspace of Euclidean
space is second countable and has a countable dense subset; closedness of
\(\operatorname{ext}K\) is not needed. The selected initial vertices, and the
additional witness point if wanted, can be included in that subset. Density
implies \(\overline{\operatorname{conv}D}=K\). The manuscript's small-simplex
perturbation argument establishes \(\operatorname{int}K\subset\operatorname{conv}D\).
The omitted set lies on the null boundary of the convex body. This supplies
actual almost-everywhere coverage, rather than merely dense coverage.

**Integration and equality (lines 123--166).** Each simplex is measurable, the
family is countable, and pairwise intersections are null since interiors are
disjoint. Countably many such null intersections remain null. With
\(M=\max_{x\in K}\|x\|\), we have \(\|c_j\|\le M\), \(0\le q_j\le M^2\),
and \(\sum_jw_j=1\). These bounds justify the absolute convergence of every
weighted moment and variance series used. The barycentric factorial formula
and the coefficient \((n+1)/(n+2)\) in the variance term are correct.

Every weight is positive. A zero sum of nonnegative terms therefore forces
each radial term and each centroid term to vanish, even for infinitely many
pieces. Equal centroids of two nondegenerate simplices would lie in both
interiors, contradicting disjointness. A single surviving simplex is closed
and dense in \(K\), hence equals \(K\). No positive-volume piece can disappear
through a limiting zero-weight argument. Conversely, the simplex formula
immediately gives equality for every inscribed nondegenerate simplex.

## Boundary and limiting cases

- **Dimension one.** For \(K=[\alpha,\beta]\), direct integration gives
  \(\Delta_r(K)=(\alpha^2+\beta^2-2r^2)/6\). Under the endpoint norm bounds,
  equality requires \(\alpha=-r,\beta=r\). This matches the manuscript.
- **Origin outside the body.** The triangle with vertices
  \((1,0),(3/5,4/5),(3/5,-4/5)\) is contained in \(x\ge3/5\), has all vertex
  norms one, centroid \((11/15,0)\), and second moment \(49/75\). It gives
  equality in the strengthened inequality while excluding the origin. Thus
  no centering or origin-containment assumption is hidden in the theorem.
- **Nonclosed extreme-point set and no uniform strict radial margin.** Consider
  the compact convex hull in \(\mathbb R^3\) of
  \((\pm1,0,3)\), \((0,0,3)\), and
  \(p_k=(0,1/k,3+1/k^2)\), \(k\ge1\). It is full-dimensional. The linear
  functional \((z-3)-2y/k\) uniquely minimizes at \(p_k\), so every \(p_k\)
  is exposed. Its limit \((0,0,3)\) is the midpoint of the two first points
  and is not extreme. Every point lies in \(z\ge3\), and the only possible
  point of norm three is that nonextreme midpoint. Hence every extreme point
  has norm strictly greater than three, although the extreme norms have
  infimum three. The proof needs neither a closed extreme set nor a uniform
  positive radial gap, and still gives strictness for this nonsimplex.
- **Weaker inequality and regularity.** The corollary correctly additionally
  requires zero centroid. The displayed nonregular triangle in the manuscript
  has centroid \((0,1/3)\) and second moment \(1/3\), and illustrates only the
  strengthened inequality. There is no conflation of its equality case with
  the zero-centroid case.
- **Excluded degeneracies.** Positive volume, nondegenerate simplices, and
  \(r>0\) are explicit assumptions. All divisions by volume and all uses of
  an interior centroid respect them.

## Sources, computation, and publication claims

FPS Theorem 1.1 on printed page 499 gives precisely the strengthened inequality
and the polytope equality characterization. Its following paragraph explicitly
leaves the general-body equality case conjectural. FPS Lemma 3.2 on page 502
is algebraically the manuscript's simplex formula. The finite polytope proof
and approximation passage on pages 503--504 substantiate the manuscript's
description of the earlier method. OWR printed page 2908 gives the same
inequality, polytope equality statement, and general-body conjecture. The
manuscript correctly distinguishes its contribution from the earlier
inequality and simplex computation. The sources' strict prose and their
on-sphere equality statement are faithfully described; the manuscript's
explicit non-strict interpretation removes the ambiguity.

The verifier was read and run without modification using
`python3 verification/verify.py`: **298 checks passed**, using exact rational
arithmetic. Its polynomial expansion and monomial integration are a different
computational path from the vertex-sum formula being checked. The polygon
moment formulas give independent finite area and moment checks of shell
updates. The script correctly limits its claims to finite checks; it does not
claim to establish the countable construction, universal theorem, or priority.
No additional examples were added to the verifier.

The four-page PDF has legible equations and references, consistent numbering,
and no clipping, overlapping text, missing closure bars, or broken displayed
mathematics. Its text agrees with the reviewed TeX. The supplied ORCID is used
consistently. The stated unrefereed and AI-assisted status is appropriate for
preprint circulation; this review is another AI check, not human peer review
or a proof-assistant formalization.

The historical claim about a bounded literature audit is explicitly limited
and does not certify priority. I did not repeat that literature audit or read
its conclusions. A direct attempt to retrieve the UnsolvedMath catalogue page
was blocked by a Vercel security checkpoint, so this round independently
confirms the original conjecture through FPS and OWR, but does **not** newly
authenticate the catalogue's precise version `v1.7`, title, or dimension
metadata. This is a limit of this review, not evidence that the citation is
wrong and not a mathematical release blocker. The parent review can rely on
its separately retained catalogue evidence.

## Optional editorial suggestions, distinct from required fixes

At lines 92--93, one could make first-hit existence explicit with one sentence:
write the new-shell point as a convex combination of the apex and a point of
the old polytope, then use compactness. At lines 183--186, one could spell out
that volume and both moments converge and that the volumes stay bounded below
by \(|S|\). Both facts follow directly from the written setup; these are
optional expansions for a less experienced reader, not missing hypotheses,
proof gaps, or conditions of this verdict. No stylistic reorganization is
requested.

## Final checkpoint and remaining gap

Final checkpoint: **2026-09-23T13:43:41Z**. All five reviewed artifact hashes
were recomputed at this checkpoint and remain exactly as listed above.

Completion estimate: **100% of this scoped second adversarial preprint review**.
Strongest independently verified result: the stated universal equality theorem
and its positive finite witness, under exactly the manuscript's hypotheses.
No mathematical gap was identified. Exhaustive priority certification, human
refereeing, and formal machine proof remain outside this review's scope and
are not represented as completed. Only this report is a repository change;
temporary PDF renders were made outside the repository. No commit, push,
release, submission, or communication with another individual was performed.
