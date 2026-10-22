# Independent audit: unit-square covering, ID 3086

Date: 2026-10-05 UTC. Target: OPG-37327, rank 775.

## Verdict

**PASS for the frozen, explicitly limited mathematical claims.** The local-lemma
counterexample, elementary partial results, and stated failure to resolve the
original conjecture survive this audit. There is no blocking mathematical
correction to the author's package. This is not acceptance of an all-n solution,
a 17-tile covering counterexample, a novelty claim, or a journal-acceptance claim.

The author archive is preserved unchanged: 15,344 bytes, SHA-256
`61b8680c989c6eec5574b818781b217b038349f222ab2089d6678a7a1eaffae3`.
Its manifest SHA-256 is
`0ba8810ca9f043c64021a39b9a4c75bc8d2c435644515f40356eb64a9e5c8091`.
All eight archive entries agree byte-for-byte with the inspected author release.
Both author-side checkers pass.

## 1. Source scope and downstream dependence

[The September preprint, v1](https://arxiv.org/html/2609.15876v1), Section 2,
uses the full boundary-inclusive grid, with spacing h=(n+epsilon)/n. Its
single-sided category requires intersection with exactly one boundary side.
Section 3, Lemma 2 bounds such a tile's grid length by 3 sqrt(2)/2, without a
stated restriction on the number of tiles or irredundancy. The definitions are
introduced in a covering context. That context is fulfilled below.

PDF pages 2-3 were visually checked against the HTML; page 6 was independently
rendered and checked. In Section 5, inequality (2) explicitly uses Lemma 2's
coefficient for single-sided tiles. The resulting restrictions lead to Theorem 1
and the subsequent area contradiction. The false local bound leaves that proof
without a valid justification at this step. A corrected global argument might
still establish the n=4 conclusion.

The [current arXiv record](https://arxiv.org/abs/2609.15876) lists only v1,
submitted September 14, 2026, with an intention to seek journal publication.
No acceptance or corrected version was established in this inspection.

## 2. Independent reconstruction of the geometric certificate

Set h=101/100, s=4h, r=sqrt(2)/2 and delta=1/100. The tile Q is

    |x-2h| + |y-(r-delta)| <= r.

Its four edges have squared length 1 and consecutive edges have dot product 0.
Its area is 1. Its x-range is [2h-r,2h+r], strictly within (0,s); its y-range is
[-delta,2r-delta], strictly below s and crossing y=0. Thus it meets only the bottom
target side, and does so over a segment of length 2delta=1/50.

Independent edge/line intersection, rather than the author's half-plane clipping,
finds these and only these positive-length grid intersections:

- x=2h: the y-interval [0,sqrt(2)-1/100], length sqrt(2)-1/100.
- y=0: the x-interval [201/100,203/100], length 1/50.
- y=h: the x-interval [76/25-sqrt(2),1+sqrt(2)], length 2sqrt(2)-51/25.

The other seven grid segments have empty intersection. Crossings between the
three chords are isolated points, with zero length, so there is no length
overcount. Summing gives

    L = 3sqrt(2)-203/100,
    L - 3sqrt(2)/2 = 3sqrt(2)/2-203/100 > 0.

The final comparison is exact: 9/2 > 41209/10000. The outside cap is a triangle
of base 2delta and height delta, so its area is 1/10000.

The same formula L=3sqrt(2)-2h-delta holds for delta=1/100 and
1<h<211/200. Since 2h+delta<53/25<3sqrt(2)/2, the violation persists for
arbitrarily small positive s-4. The fixed example is therefore not an artifact
of interpreting an arbitrarily small enlargement too broadly.

## 3. Does the tile belong to a genuine covering?

Yes. The author's 25 axis-parallel unit squares at integer lower-left corners
(i,j), 0<=i,j<=4, cover [0,5]^2, hence the target. Appending Q gives a 26-tile
cover containing a single-sided tile that violates the stated local estimate.
There is no minimum-cardinality hypothesis in that estimate.

A stronger independent witness removes even a possible concern about Q being
redundant. Put eta=1/200, l=2h-eta and u=2h+eta. Use:

- 25 unit squares with lower-left corners (i,eta+j), 0<=i,j<=4;
- six unit squares with lower-left corners (a,0), where
  a is 0, 1, l-1, u, u+1, or u+2;
- Q itself.

The first group covers the target at heights y>=eta. The second covers the
remaining bottom strip outside the slit [l,u] x [0,eta]. The slit lies in Q:
at its four vertices |x-2h|+|y-(r-delta)|<=r, and Q is convex. Hence these 32 tiles
cover every target point. The point (2h,0) belongs to Q and to no other tile,
so Q is indispensable. Removing other redundant tiles one by one produces an
inclusion-minimal covering that still contains Q, if that were desired.

Neither witness has 17 tiles. Neither refutes the original covering conjecture,
nor proves that this local configuration can occur in a hypothetical 17-tile
cover. A lemma restricted to the latter setting would require a new argument.

## 4. Supplementary proofs audited

### Area identity

Summing tile indicators and integrating over the target and its complement gives
N-s^2 as the sum of outside areas and multiplicity-weighted overlap inside. The
outside contribution is a sum, not an area of the union. It is nonnegative and
less than 1 when N=n^2+1 and s>n. This argument is valid but not a contradiction.

### Separated points and rotations

For h=s/n>1, three points of the (n+1)-by-(n+1) test grid either have a coordinate
range of at least 2h or include diagonal corners of a cell. Either case supplies
a pair farther apart than sqrt(2). A unit square holds at most two test points;
an axis-parallel unit square holds at most one. Covering all test points with
n^2+1 tiles therefore needs at least 2n non-axis-parallel tiles. Assigning each
point to one tile gives at least 2n paired tiles. The only permissible pair types
are horizontal or vertical neighbors. The projection inequalities
h cos(theta)<=1 and h sin(theta)<=1 yield the claimed angle threshold.
All these deductions remain necessary conditions, not sufficient conditions.

### n=1 argument

A tile cannot hold three target corners or an opposite pair. Two tiles covering
all four corners must therefore take opposite adjacent pairs. For a tile holding
the left pair, reflections and axis relabeling allow c>=t>0, c^2+t^2=1. The
upper u-coordinate is at most 1 and the lower v-coordinate at least sc-1.
These give bottom and top edge lengths at most (1-sc)/t and (1-st)/c. Their sum
is (c+t-s)/(ct)<2/(c+t+1)<1. Applying the reflected argument to the other tile
leaves less than 2 units of the two horizontal edges covered, although their
total length is 2s>2. The proof is sound, including the exclusion of t=0.

### Coarse grid bound

When two parallel lines at distance h>1 meet a unit square, its chord profile
has rising, constant, and falling pieces. With c>=t>0 and c^2+t^2=1, the two
nonempty chords lie in opposite sloping pieces because h>1>=c. Their sum is
(c+t-h)/(ct)<2/(c+t+1)<1. Three parallel grid lines are impossible because
2h>sqrt(2). A single chord has length at most sqrt(2), proving the bound
2sqrt(2) per tile for the full orthogonal grid. This yields the stated necessary
inequality 2(n+1)s<=2sqrt(2)(n^2+1).

The family's scalar relaxation test s=n+1/(4n), n>=2, is valid. The area gap is
1/2-1/(16n^2); incidence is tight. For the length inequality the exact polynomial
8n^3-20n^2+23n-5 equals 8k^3+28k^2+39k+25 at n=k+2, proving strict positivity.
These numbers are not geometric placements.

## 5. Literature and provenance

The [original 2009 page 174](https://www.cs.umb.edu/~eb/458/final/pinasco.pdf)
of Januszewski's article explicitly records both exclusions: five unit squares
cannot cover a square larger than side 2, and ten cannot cover a square larger
than side 3. The retrieved PDF is a three-page excerpt, with only the beginning
of this article. The complete 174-178 proof has not been audited here. The
publication identity is [DOI 10.1080/00029890.2009.11920925](https://doi.org/10.1080/00029890.2009.11920925).

[Dosa, Langi and Tuza, v3](https://arxiv.org/html/2601.16535v3) distinguishes its
proved S(5)=2 from Conjecture 1.1, S(6)=2. It also cites the 2009 small cases.
The author's literature boundary is appropriately cautious; the imported
source note's suggestion that n=3 was unresolved is stale.

`provenance.json` records fresh downloads, metadata and independent checks:
all three retrieved PDFs agree with the author hashes and byte counts. Both
local dataset files match a freshly retrieved pinned Hugging Face tree's LFS
identities. The target statement hash, record counts, rank, and lack of a target
research-results entry were recomputed. The catalog's local Git blob SHA-1 and
byte count match a fresh read of the pinned public GitHub API metadata.

The failed UnsolvedMath page remains a retrieval limitation, with the
[primary OPG statement](https://www.openproblemgarden.org/op/covering_a_square_with_unit_squares)
read directly instead. Prior broad repository negative searches were not
repeated; their absence-of-found-attempt result remains a scoped historical
observation, not an exhaustive search of all branches and deleted material.

## 6. Reproduction and release boundary

Run `python3 independent_check.py` and `python3 verify_manifest.py` from this
release. The independent program uses only the standard library, rational
root isolation for signs in Q(sqrt(2)), and edge/line intersections for geometry.
It imports no author implementation. It verifies recorded output and retains
its checks under `python3 -O`. Controls include boundary-centered equality,
nonviolations, wrong-boundary cases, tangency rejection, nearby rational
examples, 299 scalar relaxation cases, and 40 exact rational-angle controls.
Finite controls supplement the written proofs; they do not prove all-n claims.

The archive is an explicit allowlist of original audit prose, code, results,
and public verification metadata. It excludes PDFs, source extracts, images,
raw datasets, private coordination, and private local paths. No repository write
or third-party communication was made during this audit.
