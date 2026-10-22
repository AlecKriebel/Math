# Independent construction-family adversarial audit

**Verdict: PASS — no required mathematical repair in the assigned family.**

This is an independent mathematical audit of Sections 4–6 and 8–9, their
parameter arithmetic, and their compatibility with the original target model.
The entire proof was read. Earlier MATHEMATICAL_AUDIT.md and review conclusions
were not read. Independent derivations and finite controls preceded reading
the input's source metadata. This report is not external peer review,
proof-assistant certification, or a novelty/priority determination.

## Identity and scope

- Problem: **30004127 / OWR-16931-012**, PR **1119**.
- Assigned immutable PR head: `786fff9ba06951209e8c1e3bc6114efbfa2c9d16`.
  The parent audit supplies the PR/head binding; this family made no Git/PR
  mutation and did not independently re-fetch Git objects.
- Audited input: `inputs/PROOF.md`, **25,005 bytes**, SHA-256
  `1483bcaa29473616799fa9c04937e55fc249bd27e293c45d580af236d38709f3`.
  This byte identity was independently recomputed and matches the manifest.
- Fixed property: `P = {K4-free graphs G : G-v is 3-colorable for some v,
  or G itself is 3-colorable}`. All graphs are finite and simple.
- Success criterion: validate all repairs permitted by the actual edit metric,
  prove the explicit arithmetic/triangle construction and its probabilistic
  consequences, and check the arbitrary-internal-edge blowup obstruction.
  Any unsupported equivalence or hidden change of model would fail the audit.
- All written artifacts are confined to this review folder. No other shard,
  person, GitHub state, tracker, release, or Zenodo record was contacted or
  changed. Parent-agent audit status messages are internal coordination.

## 1. Exact heavy-apex repair identity

Write `tau(H)` for the minimum number of edges that must be deleted to make H
triangle-free. This also equals minimum full symmetric-difference edit count:
if F is triangle-free, then `H intersect F` is triangle-free and requires only
deletions, no more than the edits from H to F.

Let H be 3-colorable on n>=1 vertices, and give its join J with apex a masses
`D(a)=1/2`, `D(v)=1/(2n)`. Each tail edit costs `1/(4n^2)`; each apex edit costs
`1/(4n)`. Deleting tau(H) tail edges makes a triangle-free, still 3-colorable
tail. Its join is K4-free and lies in A3 by deletion of a. Therefore

`dist_D(J,P) <= tau(H)/(4n^2)`.

For the converse, take **any** F in P on the same vertices. Let S be the tail
vertices whose formerly present apex edge is absent in F. No apex additions
are possible in the original join. All original tail vertices outside S are
still adjacent to a; K4-freeness forces `F[V(H) minus S]` to be triangle-free.
Retain precisely this graph and isolate S. Relative to H, changes on the
complement of S are a subset of F's tail edits; deleting H's edges incident
with S costs at most `n|S|` more. If t is the number of tail edits in F, then

`tau(H) <= t+n|S| = 4n^2 * cost_D(J,F)`.

This proves the claimed equality. The argument includes additions, isolating
any collection of vertices, deleting the apex's edges, and using any vertex
as the A3 exception. The lower bound only needs F to be K4-free. There is no
assumption that an optimal repair keeps the apex universal or uses deletions
alone. It also handles the empty S, full S, edgeless tail, and n=1 boundaries.

**Exact controls.** A Boolean-hypercube weighted distance transform minimizes
over all repair graphs, not just candidate deletion repairs. Its integer unit
is `1/(4n^2)`; apex coordinates cost n and tail coordinates cost 1. The transform
processes each coordinate once and minimizes independently over flipping or
keeping it, so it gives the exact distance to the full target set.

| Tail order | All 3-colorable tails | Positive triangle-distance tails | All possible repair graphs per tail |
|---|---:|---:|---:|
| 1 | 1 | 0 | 2 |
| 2 | 2 | 0 | 8 |
| 3 | 8 | 1 | 64 |
| 4 | 63 | 22 | 1,024 |
| 5 | 958 | 570 | 32,768 |

All **1,032** identities agree exactly. These finite checks supplement, rather
than replace, the general proof.

**Adverse controls.** Tail 3-colorability cannot be omitted: the 11-vertex
Mycielski graph of C5 is triangle-free and 4-chromatic, while its apex join is
outside P. The exact coloring routine verifies this explicitly. The weight
assumption also matters: for a triangle tail with apex mass 1/10 and each tail
mass 3/10, the full repair minimum is 3/100, obtained by deleting an apex edge;
every tail-only triangle repair costs at least 9/100. Neither adverse example
contradicts the stated lemma.

## 2. Sphere, digits, floors, and all triangles

For d>=4, `B=2^d`, `m=(2B)^d`, and `K=floor(B^(d-2)/d)` are positive integers.
There are B^d digit vectors and at most `d(B-1)^2+1 <= dB^2` squared norms.
Thus one norm class has at least `B^(d-2)/d` vectors and contains K of them.
The bound does not assume that this quotient is an integer. An entirely
deterministic implementation can choose the least norm among largest classes
and the first K vectors in lexicographic order; no efficient construction-time
claim is needed.

The shifted encoding `1+sum_i x_i(2B)^i` lies between 1 and m. In `a+b=2c`, the
two added units cancel first. Both sides then have base-2B digit coefficients
at most `2B-2`, so neither side carries. Equality implies `x+y=2z`
coordinatewise. Equal norms give

`||x-y||^2 = 2||x||^2+2||y||^2-4||z||^2 = 0`.

Hence the encoding set is three-term-progression-free, including equations
with repeated terms. No no-carry assertion is being applied to the shifted
encodings without first canceling their shifts.

The tripartite ranges are correct: `1<=x<=m`, `2<=x+a<=2m`, and
`3<=x+2a<=3m`. Every designated triangle has one vertex in each part. Each
XY edge determines `x,a`; each XZ edge determines `x,a=(z-x)/2`; each YZ edge
determines `a=z-y,x=2y-z`. Thus designated triangles share no edge.

Conversely, every triangle in a tripartite host uses one vertex from each
part. Its three edges yield `a=y-x`, `b=z-y`, `c=(z-x)/2` in A. They satisfy
`a+b=2c`, hence a=b=c. This identifies the original designated triangle,
including its legal x index. Consequently **all** triangles are precisely
the mK designated ones and the host has exactly 3mK edges. This checks the
complete triangle classification, rather than only designated-edge uniqueness.

**Exact controls.** For actual d=4 parameters the code enumerated all 65,536
digit vectors, selected norm 270 with 384 vectors, and took K=64 encodings.
It checked every ordered AP equation on those 64 encodings. The explicit
integer list is saved in actual_d4_A.txt. A host restricted to x=1,...,23
has 1,472 designated triangles and no extra triangles; all 4,416 edges have
multiplicity one. A complete smaller analogue with B=2,d=3,m=64 and
`A={2,5,17}` has exactly 192 triangles and 576 edges, also with no extras.

**Adverse control.** With `A={1,2,3}`, m=8, there are 24 designated triangles
but 36 triangles in total. For example `(1_X,4_Y,5_Z)` is extra. This verifies
that the triangle checker detects precisely the obstruction AP-freeness rules
out. The general proof, not the smaller analogues, certifies the enormous
untruncated hosts for every d.

## 3. Matched distributions and farness

GOOD is uniform even parity on three edge bits; BAD is uniform odd parity.
For any specified r<=2 coordinates, each assignment has exactly `2^(2-r)`
extensions in either parity class, hence probability `2^-r`. The full
three-coordinate distributions differ. Independence of triangle blocks is
legitimate even when triangles share vertices because their edge sets are
disjoint; no host edge receives two independent instructions.

Every GOOD tail is triangle-free by the complete host classification, and
remains 3-partite. Its apex join therefore lies in P. In BAD, the fully
retained designated triangles occur independently with probability 1/4.
All are edge-disjoint and there are no other triangles. Every triangle-free
repair must delete at least one original edge per fully retained triangle,
even if it also adds edges. Deleting one edge from each is sufficient.
Therefore, with `Z~Binomial(T,1/4)`, the **full weighted** distance is exactly
`Z/(4n^2)`.

For `mu=T/4` and `lambda=log(2)`, the exponential-moment bound gives

`Pr[Z<=mu/2] <= exp(mu*(lambda/2+exp(-lambda)-1))
                 <= exp(-mu/8) = exp(-T/32)`.

The numeric inequality follows from `log(2)<=3/4`; for instance
`exp(3/4) >= 1+3/4+(3/4)^2/2 > 2`. Thus the strict bad event `Z<T/8` has the
stated bound. With `epsilon_d=T/(32n^2)`, all remaining BAD realizations are
epsilon_d-far, with the boundary `Z=T/8` correctly included as far.

Exact controls enumerate all seven zero/one/two-coordinate projections and
all 16 pattern assignments for two disjoint BAD triangles. Exact binomial
failure probabilities were computed using integers/Fractions for T=1,...,64.
The computational probability comparison uses a weaker rational envelope
`(32/33)^T`; it is explicitly not substituted for the analytic exponential
bound above. No sampling experiment is used as proof.

## 4. Positive rational sequence and separation arithmetic

All weights are strictly positive rational numbers and sum to one. The
sequence is explicitly rational:

`epsilon_d = K/(1152m)`.

Since `x=2^(d^2-2d)/d >= 1` for d>=4, `x/2 <= floor(x) <= x`. Dividing by
1152m yields exactly

`1/(2304*d*2^(3d)) <= epsilon_d <= 1/(1152*d*2^(3d))`.

Both positivity and convergence to zero follow. The identities `n=6m`,
`T=mK`, `epsilon_d=T/(32n^2)`, and `n^3/(96T)=216m^2/(96K)>=m` hold exactly.
The last inequality uses K<=m and leaves a factor 216/96 of slack. For d=4,
`T=67,108,864`, already much larger than `32 log(4)`. No farness conditioning
or small-d exception is hidden in the claimed error gap. The code checks all
these rational identities for every integer d from 4 through 64.

For an explicit asymptotic constant, let `L=log(1/epsilon_d)`. The lower bound
on epsilon gives `L<=log(2304d)+3d log(2)<=12d log(2)` for all d>=4. The
auxiliary inequality `2304d<=2^(9d)` holds at d=4 and is preserved on
incrementing d, since `(d+1)/d<=5/4<2^9`. Consequently

`m^(1/3) = exp(log(2)*d(d+1)/3)
          >= exp(L^2/(432 log(2)))`.

Thus the Section 7 endpoint-exposure inequality implies the advertised
superpolynomial lower bound with the concrete allowed constant
`c=1/(432 log(2))`. This conclusion does not independently replace the
parent's separate adaptive-oracle audit of Section 7.

The standard tester's sample upper bound is `O(epsilon^-6 log(1/epsilon))`
and its query upper bound is its square. Any fixed polynomial in either
bound and `1/epsilon` has logarithm `O(L)`, while the lower bound has
logarithm at least cL^2. This contradiction persists at any fixed positive
rescaling of the classical proximity parameter. A subsequence of positive
rational epsilon values suffices to disprove a proposed bound valid for all
small epsilon. No irrational approximation or same-epsilon rounding transfer
is required. Sections 2–3 were also read: their two disjoint non-3-colorable
witnesses, small-input coupon collection, and unordered n^2 normalization
are consistent with this deduction.

## 5. Doubled wheel and arbitrary class edges

Let W be the apex join of C5. It has no K4; deletion of its center leaves C5,
which is 3-colorable. Thus W lies in P. Also W is not 3-colorable: its center
uses a color excluded from all C5 vertices, but C5 is not bipartite.

Every vertex of W lies in a triangle. In a blowup with class sizes all two,
an internal edge in any class, together with one vertex from each of two
adjacent neighbor classes, forms a K4. This works for the central class and
all five rim classes. Therefore any P-member blowup would have all six
classes independent. In that last case, deleting any single vertex leaves
every class nonempty; choosing a transversal produces an induced W. Hence
the remaining graph is not 3-colorable. The graph before any deletion also
contains W. The independent-class blowup is outside A3 and hence outside P.

For a hereditary property, every finite graph outside it contains a
vertex-minimal forbidden induced subgraph. If P were blowup-avoidable, an
allowed blowup of a P member could have no nontransversal minimal forbidden
copy; a transversal one would project to a forbidden induced copy in W,
contradicting W in P. Thus at least one allowed blowup of W would have to
lie in P, contradicting the complete two-per-class analysis. This proves
failure of blowup-avoidability under the exact arbitrary-internal-graph
definition, not merely under independent or clique class restrictions.

The code enumerates all `2^6=64` possible internal edge choices. Exactly 63
contain K4; the remaining one is K4-free but fails 3-colorability after every
one of the 12 possible single-vertex deletions. There are zero surviving
blowups. The argument does not rely on knowing or enumerating the full
infinite family of minimal forbidden induced subgraphs.

## 6. Primary source/definition ledger and credits

The original [OWR report](https://ems.press/content/serial-article-files/46798)
has Problem 5 on physical PDF p.27, printed p.1139, in Gishboliner's joint
contribution with Shapira. It asks the hereditary/extendable complexity
comparison. Its model on physical pp.25–26 uses unordered symmetric-difference
weight, counts vertex samples plus adjacency queries, and withholds input
size. The manuscript's target and normalization match. This inspection does
not assert that each fixed forbidden-subgraph property must exhibit the
separation. No source text or image is copied into this package.

The [current arXiv entry](https://arxiv.org/abs/1905.09903) identifies v5,
dated 28 September 2021. The [current PDF](https://arxiv.org/pdf/1905.09903)
and [historical v5 PDF](https://arxiv.org/pdf/1905.09903v5) are byte-identical.
Checked physical p.2 (model), p.20 (arbitrary internal graphs in blowup
classes and footnote 23), and pp.22–23 (Problem 5.6, blowup-avoidability,
Proposition 5.7, footnote 24). These agree with the scope used above:
arbitrary internal class edges are allowed, and rational weights avoid the
irrational-weight proximity relaxation. The separation does not invoke
Proposition 5.7 and its explicit wheel obstruction explains why that
proposition cannot settle this P positively.

[Behrend's primary archive record](https://pmc.ncbi.nlm.nih.gov/articles/PMC1078964/)
confirms the author/title, PNAS 32 (1946), 331–332. The
[Bolyai volume contents](https://www.bolyai.hu/files/kotetek_18_1978.pdf)
confirms the Ruzsa–Szemerédi title and start page 939. The full historical
Ruzsa–Szemerédi article was not retrieved, and the contents file is not
misrepresented as the article. This family does not claim to have newly
invented either classical construction; the manuscript explicitly credits
both methods and supplies the complete construction proof checked here.

Fresh response identities (source bodies discarded) are in SOURCE_LEDGER.json:

| Source | Bytes | SHA-256 |
|---|---:|---|
| OWR original PDF | 718,945 | `f88f89375b4b427312169552c106d6395dd249cacc6040b8eb8b23726a95d8de` |
| Current arXiv PDF and v5 PDF | 506,856 each | `6ddba2d03267d367dffb8dd3ce23f6f5f6afb36496ee68142c02119d398c2b4d` |
| Bolyai contents PDF | 131,756 | `2fc210b7338ef288297c18028c89fc46bddc8866c3c6fec61def817eb24d1399` |

This is a targeted primary definition/attribution audit, not an extensive
priority search or a claim that no earlier or later separation exists.

## 7. Reproduction, status, and exact remaining gap

From any working directory, run the local `exact_controls.py` with Python 3.
It uses only the standard library, fixed enumerations, integers and rational
arithmetic; the executed environment was Python 3.14.6. It writes RESULTS.json
and actual_d4_A.txt into its own directory. All assertions passed with exit
status 0. The separate collect_source_metadata.py records public retrieval
metadata and discards the retrieved bodies; live page HTML hashes may vary.
Artifact byte identities are in ARTIFACT_HASHES.json.

**Strongest independently verified result in this family:** the exact
arbitrary-repair heavy-apex identity, the complete AP-free tripartite host
construction, the exact GOOD/BAD triangle-distance formula, the farness
probability bound, the rational asymptotic separation arithmetic, and the
doubled-wheel non-blowup-avoidability claim are valid as stated.

**Exact remaining gap for this family:** none in its assigned claims. The
full theorem's adaptive lower bound additionally depends on Section 7's
exposure/coupling lemma; this family read it and found no inconsistency but
leaves its independent adversarial certification to the parent audit's
separate oracle family. No required patch to PROOF.md was identified.
