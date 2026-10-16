# Independent audit of the October 4 construction: combinatorics and probability

Reviewer: internal independent source-combinatorics agent. Completed 2026-10-06
22:12 PDT (2026-10-07 05:12 UTC). This is an automated mathematical audit,
not conventional human peer review and not formal proof verification.

## Scope and verdict

I read the original user request, the entire October 4 manuscript's
`introduction.tex`, `algebra.tex`, `random.tex`, `patterns.tex`, `planar.tex`,
`topology.tex`, `assembly.tex`, and bibliography. The detailed audit reported
here concerns every step of `random.tex` (449 lines), `patterns.tex` (594
lines), and `planar.tex` (440 lines), plus their interfaces to the algebra
and topology. I did not rely on the initial triage, the September 23
direct-finiteness theorem, or any Lean documentation as validation.

**Verdict:** no substantive mathematical defect found in the checked random,
bounded-pattern, or planar-extraction argument. These sections do provide
an existential finite pair of immersed labeled graphs satisfying the
stated parity conditions and having no reduced spherical arrangement, with
positive probability for all sufficiently large admissible parameters.
The argument is unusually delicate but the multiplicity-stage mechanism
does address repeated uses of an underlying graph edge. It does not count
repeated traversals as independent edge prescriptions, and it does not
assume independence of the stages.

This verdict is scoped: the assertion that these graphs yield a torsion-free
group and protected roots additionally requires the cone-picture and
surgery argument in `topology.tex`. I read that section and found no
obvious mismatch at the interface, but its independent detailed audit
belongs to the topology reviewer. No numerical matching outcome, complete
list of relators, or numeric group-algebra multiplication certificate has
been obtained by this audit.

All section-and-line citations below refer to the pinned folder
`sources/preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026/build/`.
The principal reviewed SHA-256 digests are:

| File | SHA-256 |
|---|---|
| `sections/random.tex` | `bb172b92ba622e262c2bf124e70c3cd55922200083c09db658615759b81323c4` |
| `sections/patterns.tex` | `20c6cc1f3fb035150831e5091c98313f04e7a9d8aaa347507020b176394ed4ea` |
| `sections/planar.tex` | `e3a1a4e23dd6871a9746ffde05d32297e695f3167b8efa0f0a4cad5da8c9ae6b` |
| `references.bib` | `67858582a3d034a0082b9b707b97b4ba9f418363d4aaa21d51253b92514bacdb` |

## 1. Finite type construction and word weights

`random.tex:14–112` fixes q=128, v=16513, p=129/16513, and a signed
alphabet of 16520 letters. The involution exists because the seven extra
letters are paired with distinct ordinary letters and v−7=16506 is even.
No compatibility between that involution and projective-plane incidence
is assumed or required. The turn calculation correctly uses the incoming
letter's inverse, rather than the incoming letter itself.

The seven complements of Fano lines have size four, distinct complements
intersect in two points, each extra letter occurs in four complements, and
each pair of extras occurs in two complements. Therefore the prescribed
counts

    a_m = (129m−1)/4,     b_m = 129(m−1)/4

are integral for m≡1 mod 4. Extra-letter balance is exactly
4a_m+1=129m and 4b_m=129(m−1). The distinguished vertex is responsible
for the +1 on the A side. Other vertices' extra intersections are even,
and its self-intersection is seven, so exactly the claimed single
even-degree exception occurs. The ordinary intersections have odd sizes
129 or 1. There is enough capacity for disjoint extra assignments in each
line class because 7·129/(4·16513)<1. The specification is eventual in m;
it does not claim to work for every small admissible m.

`random.tex:133–161` obtains the three turn-frequency estimates with
uniform O(1) errors. For ordinary–extra turns, balanced distribution of
each complement among line classes gives 4a_m/v+O(1) occurrences of
each extra letter per class, even though the seven assignments are
disjoint. Summation over 129 classes still gives O(1), since q and v are
fixed. For extra–extra turns, the exact A count is 2a_m+1=np/2+1/2;
the B count differs from np/2 by a fixed constant. Thus the common
normalization np on both sides is legitimate.

`random.tex:178–221` proves strict contraction of the squared-turn matrix.
I independently checked the numerical inequalities using exact rational
arithmetic:

    ordinary row bound = 71589573988/72026254783
                       = 0.9939371997570104 < 1;
    extra row bound    = 195474585/77908334
                       = 2.509033051585983 < 4.

Consequently one can take
λ=71589573988/72026254783 and δ=−log(λ)/4≈0.0015203134100908054.
The factor 4|T| in the matrix power bound is absorbed only for
sufficiently long words, as expressly stated. The proof of the word-bin
bound later uses only such long blocks. No issue arises at word lengths
one or two, where the eventual decay inequality need not hold.

These exact checks can be reproduced with Python's standard library:

```python
from fractions import Fraction
from itertools import combinations
q = 128
v = q*q + q + 1
p = Fraction(q+1, v)
r1 = Fraction(q, q+1) + 7*p*p + Fraction(21, (q+1)**2)
r2 = Fraction(6, 4) + (v+21)*p*p
assert r1 == Fraction(71589573988, 72026254783) < 1
assert r2 == Fraction(195474585, 77908334) < 4
points = frozenset(range(1, 8))
lines = {frozenset((a, b, a ^ b)) for a,b in combinations(points, 2)}
D = {points - line for line in lines}
assert len(lines) == len(D) == 7
assert {len(d) for d in D} == {4}
assert {len(a & b) for a,b in combinations(D, 2)} == {2}
assert {sum(x in d for d in D) for x in points} == {4}
assert {sum(a in d and b in d for d in D)
        for a,b in combinations(points, 2)} == {2}
```

## 2. Conditioning, switching, expansion, and diameter

`random.tex:223–294` genuinely proves nonemptiness of the girth event;
it does not condition on an event merely assumed to have positive
probability. The expected number of edges on short cycles is o(n) for
the first c₀ inequality. The ball of radius 2L around a bad edge has
o(n) incident edges for the second inequality. Since each label-pair
bijection has np−O(1) edges, a distant good edge of the same label is
available. The target-transposition switch preserves types and destroys
the chosen bad edge without introducing short cycles. For a new short
cycle using both replacement edges, the residual paths either cross the
distant endpoint sets or make the selected old good edge lie on a short
cycle; both are impossible. This includes the old-loop case.

`random.tex:300–360` gives the stronger and necessary conditioned
prescription estimate by a one-to-many injection. Given the output and
the requested edge x→y, its two displaced matches are uniquely recovered
as φ′(x) and (φ′)⁻¹(y). Overlap of the domain and codomain vertex sets
does not defeat this recovery, since the label slots are distinct. Thus
the switch count is valid for arbitrary already prescribed distinct
edges, provided the conditioning event for the prefix has positive
probability. An incompatible additional edge has probability zero. The
error E(E+r_n)/n is o(L) uniformly for E=O(L), because L=O(log n) and
r_n=o(n). The argument never divides by an uncontrolled probability
of the girth event.

`random.tex:375–428` legitimately applies the single-prescription
estimate to a small linear number of edges, not only to E=O(L). A
nonexpanding k-set lies within a 2k-set containing at least ceil(129k/2)
distinct edges. Counting the containing set is enough; one need not also
count the original k-set. Choosing 65ρ<p/4 keeps the denominators above
np/2 for these collections. The union-bound exponent is 129/2−2=62.5;
the split at k=√n makes its summation tend to zero.

`random.tex:430–447` turns small-set expansion into component diameter
O(log n). This does not assume either Γ_A or Γ_B is connected. Balls
must exceed ρn vertices; balls centered at distance 2R+1 on a geodesic
are disjoint; there can be fewer than 1/ρ of them on a side. Since
L∼c₀log n, a uniform dL diameter bound follows for every component.

## 3. Bounded image complexity and multiplicity levels

`patterns.tex:63–102` bounds the cycle rank of every image graph with
girth L and at most CL edges. Suppressing degree-two chains leaves a
weighted multigraph of minimum degree at least three. Uniform directed
edges are stationary for its nonbacktracking walk, including the
possible multigraph cases. The probability of each k-edge walk is at
most (2r)⁻¹2⁻⁽ᵏ⁻¹⁾. Markov's inequality gives enough short paths that
two distinct ones share endpoints; their union contains a cycle even
when either walk revisits vertices. The girth inequality bounds r by
O_C(log r), hence bounds r absolutely for fixed C. This proof does not
assume unit lengths after suppression.

`patterns.tex:104–151` correctly bounds the number of chains. Image
leaves can only be endpoints of the one permitted interval. Every
circle component receives a marked starting point from a path. Degree
sums and bounded cycle rank bound all other branching marks. Each
successive traversal of a fixed oriented underlying edge is separated
by a reduced closed walk containing a cycle, hence by at least L
positions. Therefore m_e≤2(C+K₀), including both orientations. Each
path uses whole chains; multiplicity is constant on a chain. These
facts, with fixed K₀,C,I, make the number of unlabelled patterns only
polynomial in L.

`patterns.tex:165–191` is a key estimate. At a vertex z, all incidences
except the interval endpoint incidences pair along path turns with a
different half-edge. Thus

    2 max_{e∋z} m_e ≤ sum_{e∋z} m_e + a(z).

For L>2 the original graph has no loops, so an edge contributes at its
two distinct endpoints. Summation yields sum_j V_j≤H+ι while
sum_j E_j=H. Fixing the interval root only in stage one gives the exact
−ι correction needed to ensure the total exponent of n is nonpositive.
There is no unaccounted free endpoint factor.

## 4. Aligned blocks, self-links, and the stage first moments

`patterns.tex:215–300` handles offsets and reflections by simultaneous
Diophantine approximation. With finitely many offsets, the selected
scale s satisfies s→∞, s=o(L), and every offset is o(s) from the chosen
grid. Both asymptotics are uniform in the patterns with fixed bounds.
Near-overlap links form a matching on occurrences because the compared
positions are disjoint and each overlap exceeds half a block. Only a
bounded number of occurrences near comparison or chain endpoints need
be excluded. The remaining unmatched occurrences are wholly unpaired,
which gives sb_*≤b₀+O(s+L/s). This error is o(L).

`patterns.tex:321–380` does not incorrectly treat self-comparisons as
comparisons of independent random words. A translation self-link has a
nonzero shift; zero shift would violate the distinct-underlying-edge
hypothesis. The equality graph has constant nonzero step, hence is a
forest, so an almost-full comparison leaves only O(κs) free letters.
A reflection self-link forces either a self-inverse middle letter or
adjacent inverse middle letters on the symmetric overlap, impossible
for a reduced word in a fixed-point-free signed alphabet. Without a
self-link, the maximal-multiplicity block's matched occurrences need
distinct partners on other blocks, which proves 2z≤S+b.

`patterns.tex:384–501` uses the squared-word estimate through bins.
For words in bin d, P(W)>exp(−d−1), yielding at most
exp(2d−δs) word choices. Bins number exp(o(L)) overall. A stage's label
assignments are projections of assignments satisfying the complete
string constraints, even for blocks absent at that stage. This permits
use of the minimum-bin block in the entire link component. The number
of possible projections never exceeds the number of full assignments.

The fixed-stage realization estimate counts **injective image-graph
embeddings**. It uses E_j distinct edge prescriptions, not the number
of traversals. Internal chain vertices contribute their required turn
frequencies; marked vertices have at most n choices; a marked fixed root
has one. The bounded number of chain junctions gives only exp(o(L))
error. Turn weights are at most one, so discarding junction and fragment
turns is a valid upper bound. All these errors are uniform for the fixed
bounds used in the theorem.

`patterns.tex:503–594` then applies Markov separately to every stage:
realization forces Z_j≥1 for every j, so its probability is at most
min_j B_j. Multiplying the deterministic B_j is valid without any
probabilistic independence. Componentwise 2z≤S+b, d_min≥δs/2, and
d_min≤a₀s give

    log product_j B_j ≤ −δH/2 + a₀b₀ + o(L).

The chosen ε depends only on the word weights, **before** K₀,C,I.
Since the number of stages is bounded and pattern entropy is o(L),
the final exp(−δL/(4M)+o(L)) bound tends to zero. The order of
quantifiers is correct despite potentially enormous fixed C and M.

## 5. Planar extraction and the external separator input

`planar.tex:68–119` closes an immersed segment without canceling original
occurrences. Two equal-length nonbacktracking walks ending at the same
vertex give a nonempty *linearly* reduced based loop. It need not be
cyclically reduced at its base, but that is not required: its first and
last edges avoid the prescribed segment/geodesic edges, making all joins
of S J_b R J_a nonbacktracking. Deleting two incident edges leaves minimum
degree at least 127. The stated D₀L bound follows from L∼c₀log n.

`planar.tex:130–231` correctly treats disconnected ribbon neighborhoods.
The complementary regions can have several boundary components, and the
identity sum_Q(ℓ_Q−2χ(Q))=2N₀−4 still holds. A disk monogon forces
neighboring inverse letters and is permitted only at the exceptional
break, so at most one exists. A same-band disk digon consumes degree-one
gaps, giving the coarse 2N₀ bound. Other disk regions have ℓ≥3, and
multiple-boundary regions have χ≤0. Thus B≤8N₀ bounds non-good gaps.
After indexing and piece cuts and their opposite cuts, at most 12N′
runs remain, paired into at most 6N′ interval comparisons. Self-paired
runs are impossible: their middle gives either a fixed occurrence or
adjacent inverse letters. This is also why the exceptional break must
be cut.

The only substantial external combinatorial theorem used here is
Lipton–Tarjan's planar separator theorem. On 2026-10-06 PDT I checked
the precise theorem statement in the publisher's primary record:
[Lipton and Tarjan, *A Separator Theorem for Planar Graphs*, SIAM J.
Appl. Math. 36 (1979), 177–189](https://epubs.siam.org/doi/10.1137/0136016).
It supplies a separator of size at most 2√(2s) with remaining components
of size at most 2s/3, exactly as used in `planar.tex:253–279`. I did not
reprove or independently audit the 1979 paper's entire proof. A separate
Princeton-hosted PDF request returned HTTP 403; the publisher statement
was accessible. Recursive charging gives
C_sep=2√2/(1−√(2/3))≈15.41348460451408. Removing loops and parallel
copies before application preserves components after vertex deletion.

`planar.tex:289–440` resolves the apparent circularity of choosing
ε after the separator scale: ε was already fixed independently of all
bounded-system parameters. U, η, K₀, C, I are then fixed before n.
Splitting long boundaries costs at most 3D₀H₀/U appended occurrences.
At most one intact exceptional path can have fewer than L original
occurrences, so N′L≤H₀+L≤2H₀. Splitting planar vertices into consecutive
blocks preserves planarity, including old loops. A deleted piece has
at most UL original positions; deleting ηN′ pieces destroys at most
2ηUH₀ surviving partner positions. Whole interval pairs can be kept
or discarded because each interval lies in a single piece.

The total-loss argument yields surviving total length ≥15H₀/16,
unpaired length ≤εH₀/16, and interval count ≤12H₀/L. Discarding the
bad-unpaired and bad-comparison clusters costs at most H₀/16 each.
A cluster shorter than L must consist solely of the unique intact
exceptional path and costs <H₀/2, because the original arrangement
also contains an ordinary boundary of length ≥L. A positive total
therefore remains. The chosen cluster meets one fixed triple
(K₀,C,I), however large the original spherical arrangement. This is
enough to exclude **all finite** arrangements probabilistically without
union-bounding over their unbounded sizes.

## 6. Interfaces, explicitness, and exact limits

The arrangement definition `planar.tex:15–33` includes inverse signed
letters, disjoint compared positions, distinct underlying graph edges,
at least one ordinary boundary, and at most one exceptional root-started
interval. These are precisely the hypotheses needed by the bounded-path
theorem and by the failures constructed in `topology.tex:121–284`.
Repeated uses of the same edge elsewhere in a path system remain allowed.

`assembly.tex:5–22` uses eventual positive probability to choose one
finite matching outcome with L≥3. The type parities hold on all vertices,
so they also hold after restriction to the root components A′ and B′
in `algebra.tex:43–83`. Distinct root-component vertices are not asserted
to have pairwise distinct group labels; only the absence of additional
identity labels is needed for c's identity coefficient. The algebraic
parity proof is valid under that weaker, exactly stated condition.

The correct strongest construction claim is: the manuscript specifies
a finite family of possible labeled graphs for each sufficiently large
admissible m and proves that some members have all required geometric
properties. A chosen member gives relators by a spanning-tree basis of
each graph component, and coefficients by root-to-vertex words. The
manuscript does not identify that member or list its coefficients.
Neither this audit nor the source produces a small or numeric witness.
The finite-presentation and scalar-witness claims are existential, not
matrix-witness or numerical-certificate claims.

No claim concerning odd characteristic, characteristic zero, a reduced
group C*-algebra, or a nonzero K₀ class follows from the sections checked
here. The source's own exact main theorem is in `introduction.tex:13–21`:
F₂, torsion-free finitely presented G, finite two-dimensional classifying
complex, ab=1, ac=0, c≠0. The eventual word-estimate constants and
probabilistic thresholds do not require a finite computational search to
make that existential theorem mathematically meaningful.

## Remaining review obligations

1. Independently verify the entire cone-picture/surgery argument and its
   torsion-free consequence; this report does not substitute for that pass.
2. Independently verify the module handedness and idempotent corollary.
3. Audit priority before attributing novelty to the immediate consequence.
4. Review the eventual publication package against these scope and
   explicitness limits.

No blocked route or substantive defect was found in this audit. A fresh
complete-package reviewer should nevertheless attempt to falsify the
source interface and the corollary rather than treat this verdict as a
certificate of correctness.
