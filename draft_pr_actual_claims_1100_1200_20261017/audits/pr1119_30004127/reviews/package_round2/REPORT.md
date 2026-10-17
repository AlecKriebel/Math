# Fresh independent whole-package audit, round 2

**PASS — no required mathematical or publication-package repair found.**

Date: 17 October 2026. This disposition covers the exact frozen publication
package identified below, including the operative five-page note, unchanged
original proof, all six verification programs, both archives, metadata,
primary-source dependency and bounded priority statements. The full original
comparison target is met mathematically. The verdict is not a novelty
certificate, external peer review, formal proof-assistant certificate, or an
instruction to publish. Publication remains for the parent/human assessment.

I first reconstructed the note and original proof and checked the original
model and imported theorem independently. I read the six earlier family
reports and priority ledgers only afterward, as objects to audit and compare,
not as premises for mathematical soundness. I did not coordinate with other
reviewers, contact any individual, mutate Git/index/PR/tracker/publication
state, or alter an operative package asset. All outputs are in this folder;
all third-party bodies, extracts and renderings are in its ignored `tmp/`.

## Frozen identity

The received `PACKAGE_RECEIPT.json` and `FIRST_FREEZE.json` agree with the
actual bytes, independently recomputed:

| Asset | Bytes | SHA256 |
|---|---:|---|
| `main.tex` | 15,976 | `4ab7d27fc11bba6d21ada7782834ef72442e1c3d8fac2a7253547eaa4c6ec9e4` |
| `output/pdf/vdf-testing-gap.pdf` | 80,465 | `a9d81e3b765adc8ee9bee044d23008515e31bbeb57a916358f32e8d3c021a1f0` |
| `output/vdf-testing-gap-source-and-verification.zip` | 301,162 | `4367fad39640b11fb1809c2302a91947a9343dd8179590a51ef87e5756caa5cb` |
| `output/zenodo-upload-kit.zip` | 374,039 | `c749466c7322d3cb1b6b97d31961170d76596ea901bb0d915a700ade18a0d55c` |
| `zenodo-metadata.json` | 3,575 | `1c890f0b57cd23cad96555bd73baf422d33b54a36ae267ee5bf5445f35e0e60d` |
| `zenodo-deposit.json` | 3,866 | `9ec7a0d847180c0417e789efc999f44707318e211e542152053ca36149eab559` |

The retained original `PROOF.md` is 25,005 bytes with SHA256
`1483bcaa29473616799fa9c04937e55fc249bd27e293c45d580af236d38709f3`.
Its archive copy equals the pinned input exactly. The declared source head is
`786fff9ba06951209e8c1e3bc6114efbfa2c9d16`; this audit checks the supplied
provenance and byte pin, and does not independently authenticate remote Git
history. Full member evidence is in `FROZEN_INPUT_RECEIPT.json`.

## Exact target and assumptions

The original target is Gishboliner's joint contribution with Shapira,
[OWR 19/2019](https://ems.press/content/serial-article-files/46798), Problem 5,
physical page 27 / printed 1139. I freshly inspected its preceding model on
physical page 26 / printed 1138: it counts vertex samples plus edge queries,
does not provide the graph order, and uses unordered vertex-product edit
distance. The later question remains Problem 5.6 in
[GS arXiv v5](https://arxiv.org/abs/1905.09903v5), Section 5.3. The claim is
not reduced to a sample-only lower bound with unlimited arbitrary-name edge
queries.

The fixed property is

    P = K4-freeness intersect {deletion of at most one vertex leaves a 3-colorable graph}.

All graphs are finite simple undirected graphs. Sampling inputs are nonempty;
proximity is positive. All repair graphs have the same vertex set, with both
edge additions and deletions allowed. The theorem concerns oracle cost,
with no polynomial computation-time claim. The hard distribution has positive
rational masses. Lower bounds use worst-case call budgets and hold with the
vertex set/order, full masses and apex supplied. A lower bound along a rational
sequence tending to zero already defeats every fixed polynomial comparison
that would hold for all sufficiently small proximities.

## Classical side: independent proof check

Heredity, edge-deletion closure and isolated-vertex extendability hold directly.
If the old exceptional vertex is absent from an induced subgraph, that
subgraph is already 3-colorable. Every 3-colorable graph is in P, so farness
from P implies farness from 3-colorability, in the direction used by the note.

For each proper partial coloring, assigning a minimizing available color to
every nonempty-list vertex and arbitrary colors to empty-list vertices gives
a deletion repair costing at most

    n |U| + sum_v delta(v).

Edges to the colored set have no conflict outside U. Double counting in the
sum is harmless. Farness therefore gives `|U union W| >= epsilon n/2`.
Coloring any W-vertex with any feasible color decreases the nonnegative list
potential by at least `epsilon n/2`. This verifies the crucial universal
color-choice assertion; it is not merely a favorable greedy choice.

With `h=floor(6/epsilon)+1`, the potential cannot support h feasible steps.
At every fixed ternary-tree address the next sample block is independent of
its partial coloring, with miss probability at most `1/(12*3^h)`. Unrealized
addresses contribute zero. Fewer than `3^h` addresses occur before depth h;
the union bound needs no independence between nodes sharing the same block.
A proper coloring on all distinct sampled labels would follow a feasible
branch, proving the sampling lemma with probability at least 11/12. Chosen
path vertices are distinct because they lie outside the path's colored set.

For `N=12 r^2`, the two initial r-blocks give disjoint non-3-colorable
witnesses with probability at least `1-1/12-1/12-r^2/n >= 3/4` for `n>=N`.
One deleted vertex cannot remove both. For `1<n<N`, the one fixed sample
size `M=ceil(N log(3N))` covers the whole graph with probability at least
2/3, since `n exp(-M/n) <= N exp(-M/N)`. At n=1 there is no far instance;
the single label is always sampled. The algorithm does not need to detect
its size case. `M>=2r`, h is O(epsilon^-1), ell is O(epsilon^-2), and r is
O(epsilon^-3), giving the stated exponent-6 sample bound and exponent-12
adjacency bound. Above 1/8, using parameter 1/8 is valid by monotonicity.
An explicitly represented empty graph may be accepted without invoking a
nonexistent empty-set sampling distribution. No boundary failure was found.

## Short lower bound: full-repair and access-model audit

Write tau(X) for the minimum triangle-hitting deletion count. It also equals
the minimum arbitrary-edit count: intersect a triangle-free target's edge set
with the input's edge set. This preserves triangle-freeness and discards
additions without increasing cost.

For the cover L(H), each source edge has six distinct lifts. A cover triangle
uses three parts and three distinct source vertices, so projects to a source
triangle; repeated source coordinates would require a source loop. Given a
triangle-hitting cover deletion set, delete a source edge if any lift was
deleted. This removes at most as many source edges and hits all source
triangles. Consequently

    tau(L(H)) >= tau(H),
    dist_uniform(L(H), TF) >= dist_uniform(H, TF)/9.

The original H can be arbitrary, including non-3-colorable graphs. Its cover
is always 3-colorable. This is the needed guard for the next lemma.

For a 3-colorable tail X of order m, the heavy-apex identity is exact:

    dist_D(J(X), P) = tau(X)/(4m^2),
    D(apex)=1/2, D(x)=1/(2m).

Deleting a minimum triangle-hitting tail set proves the upper bound and
preserves the tail coloring. For the lower bound, take any repaired F in P;
let S lose its apex edge and let t count all tail pair changes, including
additions. F outside S has no triangle because the apex still sees all its
vertices. Keeping that restriction and isolating S repairs the original
tail with at most `t+m|S|` edits. The original F costs exactly
`(t+m|S|)/(4m^2)`. This handles a changed exceptional vertex, arbitrary
additions, the empty/full S, and apex erasure. Only the K4-free condition on
F is needed for the reverse bound. Thus the two reductions give the stated
factor-36 farness guarantee, without asserting equality for the cover.

The oracle simulation is exact. Sampling from masses 1/2 and 1/(6n) is local
randomness given n. Self-pairs, same-part pairs, and distinct copies of a
single source vertex give zero; distinct apex-tail pairs give one. Each
other adjacency uses at most one source adjacency query. Repeated samples
retain their identity. Adaptation, randomized choices and early stopping
cause no change in marginal oracle laws or success probabilities.

If the VDF execution has s sample calls and e adjacency calls, at most
`s+2e <= 2Q` source indices are inspected when its total budget is Q. This
explicit bound is essential: an inspected-vertex cost must not be identified
silently with an edge-query count. The simulator may be given the whole
cover representation and all the advertised gifts, since these convey no
unknown edge information beyond its simulated oracle.

I freshly obtained both AS04 author PDFs. In the
[asafico manuscript](https://www.math.tau.ac.il/~asafico/subdir.pdf), the
definitions on p.2 supply n and arbitrary adjacency queries; p.4 defines the
vertex/full-induced convention. Theorem 4(ii) on physical p.5 and the explicit
undirected consequence at the start of Section 7, physical p.24, give the
needed two-sided superpolynomial bound. The two-sided proof on pp.26-27 was
read; those four critical pages were additionally rendered and viewed. Its
hard worlds use random permutations and small-set exposure. The
[alternate manuscript](https://www.cs.tau.ac.il/~nogaa/PDFS/testdig5.pdf)
has the same relevant result with different pagination and bytes. I do not
identify these author copies with a publisher version of record.

The source lower bound applied to at most 2Q inspected indices yields
`Q=exp(Omega(log^2(1/epsilon)))`. Fixed normalization or strict-threshold
changes only rescale proximity by a constant. An empty source graph is
accepted directly; the constructed distribution is used only for n>=1.
There is no circular appeal to the proposed separation.

## Original direct proof: independent adversarial check

I also checked the entire pinned original proof; the short reduction does
not excuse a defect in the retained supporting argument.

* The sphere argument supplies K encodings for every d>=4. The additive
  encoding shift cancels before applying no-carry base-2B arithmetic. Equal
  norms and `x+y=2z` force equality. All encodings and the three part ranges
  fit their stated intervals. Each host edge determines its designated
  triangle, while the AP-free equation excludes every undesignated triangle.
* GOOD and BAD are independent local even/odd parity worlds on edge-disjoint
  designated triangles. Every proper coordinate projection agrees jointly,
  including when triangles share vertices. All GOOD tails are triangle-free;
  BAD's full triangles are exactly Z~Bin(T,1/4), with full weighted distance
  `Z/(4n^2)`. The exponential-moment estimate gives the claimed
  `Pr[Z<T/8] <= exp(-T/32)`. Equality at T/8 is on the far side. The BAD
  distribution remains unconditional, so no unjustified farness conditioning
  destroys local independence.
* Conditional on exact exposed host images and observed pattern restrictions,
  the remaining name-to-host bijection is uniform. Choosing an unused name
  adaptively cannot prefer a host vertex, though already exposed images may
  have a biased posterior. The public full weight vector gives no map
  information, since tail weights are equal. Joint transcript coupling
  stops before the first complete designated triangle is exposed. Marginals
  can then be completed correctly. Continuing/padding with uniform unused
  images makes the unconditional k-image list uniform. This is not a claim
  that it stays uniform conditional only on avoiding a triangle.
* The probability of exposing a designated triangle is at most
  `T (k)_3/(n)_3`, hence TV is at most that quantity capped at one. For n>=6,
  the coarse `2Tk^3/n^3` bound is valid, including the trivial k>=n regime.
  Repetitions and self-pairs do not create fresh labels. Variable s/e splits
  are handled by applying the exposure argument directly with k=2Q.
* Pointwise success averaged over unconditional BAD gives a rejection gap
  at least `1/3-2 exp(-T/32)/3 >= 1/6`, for the actual d>=4 family. Thus
  `s+2e >= (n^3/(12T))^(1/3)` and
  `Q >= (n^3/(96T))^(1/3) >= m^(1/3)`. The constants, floors and
  `epsilon_d=K/(1152m)` bounds check: its logarithmic inverse is Theta(d),
  whereas `log m^(1/3)=Theta(d^2)`. This supplies a separate direct proof of
  the same full two-sided worst-case total-cost separation.
* The doubled odd wheel proves failure of blowup-avoidability under the
  actual arbitrary-internal-edge definition. Any internal class edge yields
  K4 because every wheel vertex lies in a triangle. If all six doubled
  classes are independent, every single-vertex deletion leaves an induced
  odd wheel. Minimal forbidden induced graphs then contradict an alleged
  blowup-avoidable P. Failure of that sufficient condition is used only as
  context, not as a hardness proof.

The separate original sample-only lower bound restricts all query endpoints
to sampled labels; it does not give free arbitrary-name queries. The note
states this distinction accurately. No mathematical repair is required here.

## Reproduction, archives and visual QA

The six public programs were read. Their imports are standard-library only.
Their finite searches test the relevant claims, rather than purporting to
prove the universal theorem: all graphs through order six and the stated
color-list subfamilies; parameter/coupon boundaries; arbitrary weighted
repairs and arithmetic/parity/wheel controls; exact adaptive Bellman trees
and posterior symmetry; 76 cover cases including order zero; and 75 nonempty
cover/apex cases with all target repairs on at most five vertices.

The extracted package's portable runner freshly passed all **12** ordinary
and optimized runs under **Python 3.14.6**. Its shallow normalization removes
only elapsed time and the cover program's self-reported script hash; every
case, witness and optimal cost remains in the JSON equality comparison. The
public code hash is independently checked. Re-running the builder executes
another 12 successful runs. See `VERIFICATION_RUN.json`.

Mechanically converting the archived originals reproduces all six public
programs byte for byte, with exactly **53** assertion replacements and no
other AST changes. An intentionally false converted guard fails in both
modes. All nine public Python sources parse under the Python 3.10 grammar;
I did not run an actual Python 3.10 interpreter and make no such claim.
See `GUARD_AND_PORTABILITY_QA.json`. I do not claim the parent's separate
runtime checks as my own executions.

Every source-archive member is unique and safely relative. Its manifest has
97 entries covering the other members, for 98 members total; every byte
count and hash matches both the manifest and package receipt. The upload kit
has precisely five members. Its PDF/source payloads, metadata and README
match, and its deposit paths are portable filenames beside the manifest.
The live deposit uses the correct relative `output/` paths. Metadata title,
Alec Kriebel/ORCID `0009-0001-9320-500X`, affiliation, date 2026-10-17,
version 1.0.0, preprint/open-access status and CC BY 4.0 license are mutually
consistent. No third-party full paper, extract or rendering is included;
the only archived PDF is the authored note. Historical path-bearing receipts
are documented as such and identified by suffix and hash.

Running `build_package.py` inside the extracted source package reproduced
both archives **byte for byte**. It used the supplied frozen PDF payload;
this separately tests portable packaging rather than conflating it with
compiler metadata reproducibility. See `PORTABLE_REBUILD_QA.json`.

I separately compiled the extracted TeX with Tectonic 0.16.9, cached-only and
untrusted, using an isolated copy of the existing cache. Compilation succeeded
without selected warning/error, overfull/underfull or missing-glyph messages.
The fresh PDF is 80,466 bytes, SHA256
`fb0f667d872cc54e5cfba3eeb125d929b4b2e660d8fe6a2d8b295060d93ec0e6`;
CreationDate and PDF identifiers differ from the frozen PDF. The complete
extracted text, all 10 URL annotations and all five 110-dpi rendered PNGs are
identical. I viewed every frozen page; pixel identity covers the freshly
compiled pages too. All equations/symbols, proof continuation, references,
margins and page numbers are readable without clipping or overlap. See
`PDF_QA.json`.

## Current priority scan and publication scope

The fresh scan used 19 actual search strings in five batches on 2026-10-17,
plus direct primary-source and current-history retrievals. The exact strings
and limits are in `QUERY_LEDGER.json`; hashes, versions, actual inspection
coverage and failures are in `SOURCE_VERSION_LEDGER.json` and
`SOURCE_FETCH_RECEIPTS.json`. I critically read the older 72-query broad and
24-query focused ledgers afterward, checked their counts and limitations,
and did not sum overlapping searches into an artificial distinct total.

Current arXiv/ECCC histories still identify GS v5 / revision 2, dated
28 September 2021. The current TAU author body retains the question. The
Springer PDF request again returned subscription/cookie preview HTML, so
the full 2021 journal VoR body remains unavailable. The stale ETH URL
returned 404; neither cached search text nor a manuscript was silently
substituted for an inspected journal body. This is consistent with the
package's explicit access limitation.

The recent nearby paper is [Fei v2](https://arxiv.org/abs/2603.22702v2),
12 August 2026, still current. Its Sections 1 and 7.1 and query distinction
in Section 8 were freshly read. The sample oracle and arbitrary edge
distribution do not automatically yield this vertex-product, arbitrary-name
query result. In its fixed host, three queries on a known host triangle
reveal the three lift bits and their parity. Thus its stated sample-hard
worlds do not certify the present total-query claim without another
argument. Its parity ancestry is explicitly classical.

[Goldreich R3](https://www.wisdom.weizmann.ac.il/~oded/R3/vdf.pdf), dated
4 October 2021 with the same last revision on the current author page, already
contains heavy centers, one-sided conversion and easy-classical/hard-VDF
examples. Its two-star example is not hereditary: deleting one component
leaves a single star. Those antecedents do not answer the restricted target.
The GS blowup transfer requires a hypothesis that the candidate fails by the
wheel proof. [AKKR08](https://www.math.tau.ac.il/~krivelev/testtria.pdf),
Section 6, already supplies the two-fold local parity/independence principle.
The main note credits these ingredients and imports AS04 rather than
claiming a new triangle lower bound or parity principle.

The current [2026 container paper](https://arxiv.org/abs/2608.01523), v1,
has uniform-model partition and fixed-fraction induced-substructure theorems.
Its partition hypothesis requires extendable constituent classes, which the
class of graphs on at most one vertex is not. Its fixed-fraction statement
does not identify deletion of at most one vertex as an input-size independent
property. No weighted bridge or full separation was found in the inspected
parts. The current [2025 polynomial-testing survey](https://arxiv.org/abs/2508.16878),
v1, is classical-model context; absence of a result from a survey is not
evidence of novelty.

**Bounded finding:** no earlier full original-target answer or verified
published full implication was identified. Possible novelty is limited to
the particular fixed property and its weighted comparison bridge assembled
with the easy classical side. Priority and novelty remain uncertified. No
exhaustive fresh forward-citation list was obtained; the older incomplete
OpenAlex/Semantic Scholar receipts were read as limitations only. The
historical original full Behrend/RS papers were not newly recovered here;
their combinatorial mechanism is proved directly in the supporting proof.
The package preserves these caveats and extensive-AI-use/unrefereed status.

## Disposition and exact remaining limitations

Required repairs: **none**. There is no remaining mathematical gap identified
in the stated full original-target solution or the checked frozen package.
Its literature absence claim remains deliberately bounded, its journal-body
and citation limits remain open, and its finite programs remain evidence
rather than proof certificates. A later changed asset requires a new
fingerprint disposition; this PASS applies only to the frozen bytes above.

Completion estimate: **100% of this independent audit**, not a probability
of mathematical truth or first-ever priority. The authored artifact manifest
and final integrity receipt record the completed review.
