# Independent audit: two low-multiplicity distances

Target: ID 30006556, OWR-14299905-031, rank 774. Audit date: 2026-10-05 UTC.

## Verdict and scope

**PASS for the scoped mathematical claims, with minor presentation/source
corrections below. The general problem remains unresolved, 5/5 approaches.**
In particular, Theorem 4 is valid: for every n >= 5, a planar set with at least
n-1 cocircular points has two distinct occurring distances of multiplicity
at most n. This audit supplies no priority claim, external peer-review status,
formal proof-assistant certification, or solution of the general conjecture.

The author freeze was preserved. Its 21,557-byte archive has SHA-256
315ca399e06f5ee40f519fd841150a90342b3391325782a2cd4bead04adaf6d0.
All 10 archive members match the frozen safe directory. The author checker
was read and replayed separately, reproducing CHECK_RESULTS.json byte for
byte. That replay is not the independent mathematical evidence: the proof
below was checked step by step, and new code was written before inspecting
the author checker. It imports neither author code nor author test results.

## 1. Target and source identity

The governing primary source is Question 1, presented by János Pach in the
Problem Session of Oberwolfach Report 1/2026, printed p.69 / PDF page 65.
The question's n>4 restriction, distinct planar points, two distinct occurring
distances, and at-most-n multiplicities match the imported target. The
explanation identifies the diameter as the first distance, and the four-point
joined-equilateral-triangle exception fixes the unordered-pair convention.
The page was independently rendered and visually inspected, as well as read
in text. Public source: https://doi.org/10.4171/OWR/2026/1 .

The complete pinned problems and prior-results files were independently
rehash-checked against a fresh read of the public repository manifest. Both
exact numeric IDs, 30006556 and 1949, occur once. Both statement and review
hashes were recomputed using the repository's actual review-hash formula.
Both match the repository-bound catalog. No exact prior-report key exists
for OWR-14299905-031 or EP-132 in the complete imported dictionary. EP-132's
first assertion is the same target once its contextual n>=5 qualification is
restored; its asymptotic diverging-number question is additional scope.
Source records and dataset contents are excluded from this packet.

Fresh downloads of the official OWR PDF, arXiv v5, and the public journal PDF
all returned HTTP 200 and exactly matched the author's recorded hashes and
byte counts. This is fresh retrieval of those three PDFs, not a claim that
the full datasets were freshly downloaded. The arXiv landing page still shows
v5, revised 3 February 2026. Relevant sections of CDL were read: Conjecture
1.1, Theorems 1.2 and 1.3, Corollary 1.4, Proposition 1.5, and the Section 2
proofs. The journal metadata and initial theorem statements were compared.
No claim is made to have re-proved every external classification or every
proof in either full publication.

A fresh read of the repository's 62-entry attempts directory, research logs,
related-target list, six all-state PR searches, exact-ID commit searches,
and an exact-ID branch search found no earlier selected-target attempt.
This bounded absence check does not cover deleted/unindexed work or private
working trees. The queue's 0/5 marker was not used as the sole evidence.
Detailed metadata, URLs, hashes, limits and query terms are in
SOURCE_AUDIT.json.

## 2. Pair-budget and collinearity audit

If there is only one sparse distance, Hopf-Pannwitz makes it the diameter.
With M distinct distances and diameter multiplicity t>=1, counting unordered
pairs gives n(n-1)/2 >= t+(M-1)(n+1). For both parities of n,
1+floor(n/2)(n+1)>n(n-1)/2. Thus M>=floor(n/2)+1 suffices.

For l collinear points, the endpoint already determines l-1 distinct
positive differences. If the whole set had only l-1 distances, those
positive differences are all the distances and the line-coordinate set is
closed under nonnegative differences. Repeated subtraction of the smallest
positive coordinate forces an arithmetic progression, with no missing
multiple below its largest member. An off-line point would have distances
to consecutive progression points that differ by strictly less than the
step, while each distance is an integer multiple of the step. They must all
be equal, contradicting two distinct perpendicular bisectors when l>=3.
The fully collinear case is also valid: a fixed-distance graph is a union
of paths, so has at most n-1 edges. A leftmost vertex in any proposed cycle
has at most one neighbor, ruling out the cycle. Proposition 1 passes.

CDL Section 2.2 proves the unconditional bound on the second-largest-distance
multiplicity displayed as (2), not merely the sufficient hypothesis in its
Theorem 1.3 statement. The author therefore uses the stronger displayed
inequality legitimately. Each of the first two convex layers contains at
most two vertices from a selected line. Off-line vertices across the two
layers total at most n-l. Hence h1+h2<=n-l+4, and l>=n/3+4 gives the stated
corollary. Degenerate segment layers retain two endpoints. Attribution to
CDL is appropriate; no original theorem is claimed for this corollary.

## 3. Theorem 4: complete adversarial proof check

Write m=n-1>=4, normalize the common circle to radius one, and call the
extra point p. Circle distance graphs have degree at most two. If p is
also on the circle, every multiplicity is at most n; at least two distance
classes exist since a single class would give vertex degree n-1>2.

### Center exception

If p is the center, every length except the radius has multiplicity at most
m. Failure would therefore require every circle chord to lie in {1,D}, with
D>1. If D=1, four or more circle points cannot all have chord 1, by the same
degree bound, so a shorter occurring chord would already give the second
sparse distance. If chord 1 does not occur, all classes are sparse. These
observations justify the short reduction in the frozen proof.

A two-distance set of m circle points has m-1<=4, hence m=4 or m=5. If m=5,
both chord graphs have degree two at every vertex. Chord 1 therefore closes
Q under both rotations by pi/3; its full six-point orbit cannot fit into Q.
If m=4, all four cyclic gaps are at least pi/3. None can exceed pi: the
other three gaps already sum to at least pi. Each gap is either pi/3 or
the angle theta corresponding to D. If k gaps are theta, their sum forces
theta/(pi/3)=1+2/k. For k=1,2,3,4 the indicated two-gap arcs in the frozen
proof have forbidden smaller central angles 2,3,8/3,3 respectively, in units
pi/3. All are at most pi and differ from the two allowed angles. The checker's
independent enumeration rejects every one of the 15 gap orderings. Both
n=5 and n=6 center boundary cases are therefore covered.

### Saturation

For noncentral p, each distance contributes at most two p-to-Q incidences
and at most m edges within Q. Failure requires every non-diameter class to
have at least n+1=m+2 edges, so both upper bounds are attained separately.
Its Q-graph is 2-regular, and each vertex's two neighbors are the two radial
reflections at the relevant chord angle. In particular, an antipodal chord
cannot be one of these saturated classes, since it has degree at most one.

Let s be the number of non-diameter classes and t the number of p-to-Q
pairs of diameter length. Counting p incidences gives m=2s+t, with t<=2.
Each circle vertex has 2s non-diameter neighbors, leaving m-1-2s=t-1 diameter
neighbors. Thus t cannot be zero. When t=1, there are no diameter edges
within Q; when t=2, they form a perfect matching. No distance class or
interior/exterior outlier position has been omitted.

### Centroid and radial reflection

Let S=sum Q and c=2 sum_j cos(theta_j). For t=1, S=(1+c)q at every q.
Subtracting this identity for two distinct q forces 1+c=0 and hence S=0.
Each remaining vertex is in a radial-reflection pair, so reflection about
every Q-radius preserves Q.

For t=2, let f(q) be the unique diameter partner. Then
S=(1+c)q+f(q). Summation gives (m-2-c)S=0. Since every occurring chord angle
is positive, cos(theta_j)<1; hence c<2s=m-2. Thus S=0. The ratio f(q)/q is
real, has modulus one, and is not +1, so it is -1. The leftover neighbor is
antipodal and fixed by the radial reflection. Reflection closure again holds.

### Regularity

Take a shortest cyclic gap a between two points. Reflections at already
obtained points extend the angle sequence 0,a,2a,... in both directions.
Finiteness makes a/(2pi) rational. If the resulting rotation orbit had a
smaller spacing, it would contradict the definition of a. Thus this orbit
has spacing a. An additional point would split one such gap into a smaller
one, also impossible. Q is a regular m-gon. This argument excludes unions
of unevenly spaced orbits; no unproved classification is being imported.

### Moment contradiction

The first two Fourier sums of a regular m-gon vanish for m>=3. Expanding
|p-q|^2 and its square yields sums m(1+x) and m(1+4x+x^2), x=|p|^2.
For a vertex row, including its zero self-entry, the corresponding sums are
2m and 6m. Saturation makes the p-row have the same two occurrences of each
non-diameter class and exactly one extra occurrence of the diameter. With
y=D^2, subtraction gives y=m(x-1) and
(x-1)((m-1)(x-1)-6)=0. Since y>0, x=1+6/(m-1) and y=6m/(m-1).

There is necessarily at least one p-to-Q diameter edge because t>=1, so
D<=|p|+1. Inserting these values reduces the inequality to
2<=sqrt(1+6/(m-1)), equivalently m<=3. This contradicts m>=4.
The all-n proof is symbolic; the finite moment controls are additional
checks, not extrapolation from tested values. The four-point rhombus has
squared-distance histogram {1:5,3:1}, independently confirming why n=4 is
excluded. Theorem 4 passes without changing its statement or proof.

## 4. Exact 61-point construction

The two 21-gon rings and nineteen-point triangular patch were rebuilt from
the formulas. The patch quadratic form gives 42 shortest pairs, and its
points lie within radius 2 delta. There are 21 radial ring pairs of length
delta. Independent rational intervals verify that all other ring/patch
separations exceed delta, proving multiplicity 63 exactly.

The outer polygon has 21 diameter pairs and 21 next-longest pairs. The
quadratic defining r makes the 42 largest cross-ring pairs equal to the
outer polygon's next-longest distance. Independent strict inequalities
place every inner-ring and patch-related distance below that value. Thus
minimum multiplicity=63, second-largest multiplicity=63, and diameter
multiplicity=21, on 61 points.

The new interval certificate uses pi=8 atan(1/3)+4 atan(1/7), justified by
tangent addition, alternating rational series and exact integer square-root
enclosures. It derives squared long chords from cos(alpha) and the triple
angle identity. Equalities use exact modular index counts and symbolic
identities, never rounded sorting. The construction is a credited finite
variant of CDL's idea. Its additional short edges are radial ring pairs;
it need not inherit the source's consecutive-inner-vertex description.
This is an obstruction to choosing only the minimum and second-largest
candidates, not a counterexample to the target.

## 5. Multiple-outlier limitation

For k extra points none at the center, the bound m+2k+binom(k,2) is valid.
Subtracting the non-circle contributions from n+1 yields exactly the
stated defect bound k+binom(k,2)-1. At k=2 the loss of two circle edges
permits four missing incidences; exact reflection closure is no longer
forced. A center has up to m incidences of the radius and must remain an
explicit exception. Nothing in the one-outlier proof resolves this gap.
The five approach descriptions represent scoped progress and obstructions,
not five solutions or an established progress percentage toward a theorem.

## 6. Corrections and source cautions

1. **Minor bibliographic correction.** The journal PDF and KIT landing page
   use the singular title *On multiplicities of interpoint distance*.
   The arXiv v5 title is plural, *On multiplicities of interpoint distances*.
   Distinguish those titles when citing the version of record. Authors, DOI,
   volume, pages, hashes, substantive attribution and journal status match.
2. **Proof exposition only.** For the center m=4 case, explicitly justify
   that a cyclic gap cannot exceed pi using the other three gaps. For the
   fully collinear case, the leftmost-vertex argument makes acyclicity
   immediate. These fill explanatory compression; neither changes a claim.
3. **External draft caution.** The author-uploaded Zeraoulia working draft
   was inspected through its public indexed full text. Its n>=2 formulation
   needs n>=5, as the frozen packet already warns. A further independent
   problem is Lemma 1(2): an eight-vertex, nine-edge graph need not have two
   vertices of degree at least three. A four-cycle and a five-cycle sharing
   exactly one vertex give degree sequence (4,2,2,2,2,2,2,2). The erroneous
   argument caps its sole high degree at three. The new checker certifies
   this graph. This does not refute a planar realization claim and does not
   invalidate the independent circle theorem, which uses none of that
   draft. Its n=7 classification input was not independently established
   in this audit; neither that claim nor its n=8 reduction is promoted here.

There are no required mathematical repairs to the frozen authored results.
Because bibliographic and external-source cautions exist, later publication
should include this audit addendum rather than silently altering the freeze.

## 7. Independent computational coverage and limitations

- All 30,827 subsets of the 3 by 5 integer grid of sizes 5 through 15.
  Exact squared distances, diameter bound, all-direction line criterion,
  and CDL's first-two-layer bound are checked. This differs from the author's
  4 by 4 enumeration; convex layers use gift wrapping.
- 186,053 radius-five integer-circle subsets with 49 off-circle even-grid
  outliers: 3,797 center, 75,940 noncentral interior, 106,316 exterior cases.
- Every subset of cyclic angle grids of orders 4 through 15 with size at
  least four: 63,019 candidates; all 26 reflection-closed candidates are
  regular. This is a control for the proved reflection lemma, not its proof.
- Fifteen center four-gap orderings, the center five-point orbit obstruction,
  3,500 exact evaluations of the moment identity, and 500 strict moment
  contradiction values.
- Exact rational interval and modular-index certificate for the 61-point
  example; exact graph certificate for the external-draft caution.

Zero counterexamples were found in the finite point controls. These finite
families do not classify all planar sets or establish novelty. The universal
problem and EP-132's stronger asymptotic assertion remain unresolved here.
All output is authored audit prose/code, generated certificate results and
public verification metadata. No source PDFs, source extracts, page images,
raw datasets, selected source records, or private coordination are included.
No remote write, commit, PR, external communication or nested worker occurred.
