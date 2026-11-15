# Independent paper-only analytic reconstruction — record23385145

This is my substantive reconstruction from the complete actual five-page
published PDF, its complete311-line controlling TeX and all five fresh page
images. It is written before foreign primary bodies, source code, results,
triage and old/current scientific review opinions. Eight reasoning families
below are mechanisms within this single analytic review, not eight separate
reviewers. Claims, including imported algorithmic interfaces, are hypotheses
to verify rather than conclusions licensed by the manuscript's assertions.

## Exact original claim, criteria and prior exposure

Theorem1 promises a deterministic `O(n log^5(2n))` exact-operation algorithm
which, from adjacency lists of a finite nonempty connected simple unit-edge
graph promised median and finite nonnegative real vertex weights, returns
the minimum multiplicative radius, a vertex center and all vertex centers.
No bound on cube dimension, embedding or recognition procedure is supplied.
Original-profile operations compare only `k*w(u)` with integer `0<=k<=n-1`.
The radius may be represented by such a pair. Rational bit costs are
separately charged; the statement is not a uniform bit-time theorem.

Success requires the whole theorem, its precise additive-oracle interface,
the complete-output and complexity arguments and the appendix's reliance on
a corrected imported recursion to be justified. A meaningful defect is to
be recorded without repairing or promoting a weakened theorem. It would
not suffice to test small graphs or just the threshold lemma.

I previously acquired these sources under a custody-only assignment. That
exposed the title, author/ORCID, printed October14,2026 date, absence of an
explicit version in retained front matter, native API version string1.0,
creation15October, asset names/hashes, archive member filenames/types and
opaque byte custody. It exposed no mathematical body or code semantics.
The frozen whole API descriptions and93 payloads were hashed but not read
scientifically. Those historical acquisition flags are preserved exactly.
No scope118 findings or any sibling scientific opinions have been read.

## Family1 — category, objective and boundaries

The objective is `r_w(x)=max_u w(u)d(x,u)` over vertices x of the same graph;
it is not additive arrival eccentricity and not a continuous edge-center
problem. Every distance is integral and between0 and D=n-1 by connectedness
and unit edges. Nonemptiness makes all minima/maxima attained. Finite
nonnegative weights give nondecreasing candidate rows and nonnegative
radii; infinity/NaN and unspecified infinite graphs are outside the domain.

At n=1, the sole distance is0, so rho=0 and its vertex is the only center
without reading/comparing a positive multiple with coefficient1>D=0.
For all-zero weights all n vertices are centers and rho=0. With exactly one
positive weight at u, rho=0 and the unique center is u; zero vertices still
belong to the graph and cannot be deleted as geometric intermediates. With
positive weights at two distinct vertices no center has zero radius.
These are useful falsifiable end tests. At an exact threshold ties must
be feasible. For R<0 the feasible set is empty. Arbitrary positive edge
lengths do not have the needed bounded integral distances and are expressly
excluded. Median recognition is a promise, not hidden work in the theorem.

## Family2 — threshold conversion on every bounded integral graph metric

For R>=0 define b_u=max{k in[0,D] integer:k*w(u)<=R}, a_u=D-b_u.
For positive w, monotonicity makes the true predicate an initial integer
interval, so upper-bound binary search finds its final index without real
division or an unbounded floor. For zero w, b_u=D by definition. For an
actual integer distance j in[0,D],

`w(u)*j<=R iff j<=b_u iff j+a_u<=D`.

Taking the conjunction over u yields exactly
`r_w(x)<=R iff max_u(d(x,u)+a_u)<=D`.
This proof needs no convexity, Helly condition or median graph property;
medianity is used only by the fast additive oracle. Labels a are integral,
nonnegative and at most D, including equality R=0 and w=0. It returns every
feasible vertex by testing the oracle's every-vertex output, not merely a
yes/no decision. One call plus n binary searches/scanning costs
`O(n log^4(2n))` only if the full stated additive interface is actually
available including preprocessing and the model of its integer labels.
That is a precise post-seal primary-source obligation.

## Family3 — implicit optimization correctness, witnesses and all centers

For each x, at least one u attains its maximum. Therefore r_w(x), and hence
rho, occurs in a conceptual row `0,w(u),...,D*w(u)`. The row family has n^2
entries counting duplicates, but interval endpoints suffice to represent it.
`B=D*max w` is a feasible bound witnessed by any vertex, since every
distance<=D. At n>=2 the initial max compares coefficient1 values within
the allowed range; n=1 is handled before this comparison. B=0 is handled
without calling the oracle.

The proposed search maintains feasible B and either B=rho or an active
entry with value rho. At a feasible q, rho<=q. If equality holds, min(B,q)
becomes rho (B cannot be below rho) and a returned feasible vertex gives
a correct witness. If rho<q, deleting entries>=q retains every optimum
copy. At an infeasible q, rho>q, so deleting entries<=q preserves all copies.
If feasible q exceeds an already smaller B, retaining the old witness is
correct. On termination no active optimum copy remains, forcing B=rho.
One final threshold query yields `F_B={x:r_w(x)<=rho}=C_w`. Thus all ties and
all centers are included. A final scan costs O(n), even if every vertex is
a center. A faulty variant deleting the opposite side would lose the
invariant; confusing strict and weak thresholds would lose equality centers.

## Family4 — progress, comparison model and bit size

A lower-middle entry in a nonempty row interval of length L has at least
L/2 entries on either weak side, including L=1 and even L. A weighted
median of row middles, with row lengths as selection weights, can be
chosen from their sorted list so both weak sides carry total length>=M/2.
If q is infeasible, rows with middle<=q contribute at least half their
length to entries<=q, so at least M/4 entries are deleted. For a feasible q
use middles>=q and delete>=q. Equal values only strengthen this statement;
all-zero rows are well defined. The integer M falls to at most3M/4 from
M0=n^2, giving O(log(2n)) queries. For example, a safe integer bound is
the least t with `(3/4)^t*n^2<1`; no numerical log primitive is needed by
the actual loop.

Per query: sort up to n row middles in O(n log n) exact comparisons,
form budgets by n upper-bound binary searches and update/delete intervals
by n bounded searches. Each compares bounded integer multiples of original
weights, with indices only[0,D]. Store the incumbent and pivots as pairs,
so no addition/division of arbitrary input reals is introduced. Total
original-weight comparisons are O(n log^2(2n)), storage O(n) beyond oracle.
O(log n) oracle calls at O(n log^4 n), including repeated preprocessing,
then the final complete-output call give the claimed O(n log^5 n).

For rationals p_u/q_u, q_u>0, a comparison of pairs is comparison of
`k*p_u*q_v` and `j*p_v*q_u`. These integers have at most2B+O(log n) bits
when numerator/denominator components have B bits. Thus the bit complexity
must charge such product/comparison costs plus input reading. Uncomputable
arbitrary reals are meaningful here only through the stated exact comparison
interface; the theorem does not claim an encoding-independent Turing bound.

## Family5 — median geometry, input size and preprocessing promise

The imported algorithm must work on an arbitrary median graph, not just
cube-free graphs, trees, or a supplied product-of-trees embedding. The
claimed m<=n log2 n input-size bound is compatible with median graphs
being partial cubes. A self-contained consequence of that structural
interface is the cube edge-isoperimetric bound: splitting n points in a
hypercube into coordinate parts of sizes a,b adds at most min(a,b) edges;
inductively `m<=(a log2 a+b log2 b)/2+min(a,b)<=n log2 n/2`.
The final inequality is the binary-entropy chord bound
`H(p)>=2min(p,1-p)`. Thus adjacency-list reading is absorbed by the
theorem once the classical partial-cube/preprocessing interface is verified.
It would not hold for an arbitrary dense graph under a false median promise.

For recursion geometry the relevant facts are: Theta halfspaces are gated
median graphs; slices formed by intersections are nonempty gated graphs;
pairwise orthogonal incident classes span a cube. Gating permits distance
factorization and exact reweighting of whole fibres, rather than deleting
vertices or assuming arrival weights preserve convexity. These are genuine
classical imported results to inspect in their actual primary proofs.

## Family6 — corrected additive recursion: volume, depth and integer labels

The manuscript's repair changes only the size-balance parameter to
`f(s)=2*ceil(log2 s)` for recursive orders s>=3; direct base cases s<=2
remain. A balanced cut has each child at least s/f(s), so its larger child
has size<=s*(1-1/f(s)); the children partition s. In an unbalanced graph,
each minority halfspace has size<s/f(s)<=s/2, so the chosen majority
halfspaces have size>s/2. They pairwise intersect; the median convex-Helly
and separating-class interfaces would give a unique majority-median vertex.
Those existence and uniqueness implications do not need an ln-base estimate.

A wide ladder of ell pairwise orthogonal incident classes spans Q_ell,
so `2^ell<=s`, `ell<=log2 s<=L(s)`. If each chosen slice S_i is in its
minority halfspace, `|S_i|<s/f(s)`. The two recursive calls per slice have
combined volume `<2ell*s/f(s)<=s`. One must retain **both** original-weight
and fibre-reweighted calls; no dominance of fibre weights has been proved.
Their sizes are also <s/f(s)<=s*(1-1/f(s)), since f>=2.

For s>=3, ceil(log2 s)<=2log2 s, so with lambda=4/ln2,
`f(s)<=lambda ln s`. Along a nonterminal path from N,
`s_(i+1)<=s_i*(1-1/(lambda ln N))`. After h steps,
`s_h<=N*exp(-h/(lambda ln N))`. For
`h=ceil(lambda*(ln N)^2)`, the right side<=1, so an s<=2 base case was
already reached. This is an upper-bound depth argument, independent of the
wrong-direction product estimate described in the original preprint.
At each depth the total recursive vertex volume is at most N; charging
the asserted O(s log^2(2s)) local work gives O(N log^4(2N)).

Initial arrival labels satisfy0<=a<=N-1. A fibre update of the form
`a'(gate)=max_u(a(u)+d(u,gate))` increases the maximum by at most N-1.
Along O(log^2 N) levels labels are O(N log^2(2N)) and hence O(log N) bits.
This remains an obligation to inspect the **actual** update formula and all
recursive calls: an unmentioned extra graph call, changed structural
hypothesis or nonconstant arithmetic cost could invalidate this deduction.
The actual BDH primary algorithm and local-work proof are load-bearing;
the appendix's assertions alone are not a verified oracle implementation.

## Family7 — independent interpretation of the compressed estimate witness

The appendix example is a compact mathematical graph specification, not a
trillion-vertex file to construct. Start with Q_30, attach L=17000000000
leaves at each unit vertex, and Z=488926258176 leaves at zero. Its vertex
count is `2^30+30L+Z=10^12`. Attaching a tree at one vertex preserves medianity:
intervals between pieces pass through the attachment gate, giving the median
in the appropriate tree or original median piece.

Each coordinate minority consists of2^29 cube vertices and L leaves at its
unit vertex, hence17536870912 vertices. Every pendant-edge cut has minority1.
A finite positive Taylor lower bound for exp7 proves exp7>1000 and therefore
ln(10^12)=4ln1000<28. Multiplying the coordinate minority by56 gives
982064771072<N; hence all cuts are unbalanced at the written2ln N threshold.
The unit/zero pendant cuts also satisfy this immediately. All coordinate
majorities and all pendant majorities intersect uniquely at zero.

With arrival a=N-1 only at the cube antipode, that antipode has additive
distance N+29 from zero, while all other vertices with zero arrival have
ordinary distance at most30. Thus it is uniquely farthest. Its 30 coordinate
classes are pairwise orthogonal and all incident at zero. Their minority
union contains every nonzero cube vertex and all30L unit-vertex leaves,
but none of the zero leaves. Its size is511073741823; two copies total
1022147483646>N. Slices that partition that union can be understood as
first-nonzero-coordinate sets, with cube sizes2^29,2^28,...,1 plus L leaves
each. Matching these to the actual BDH slice definition remains a primary
check. The example refutes the literal natural-log volume estimate, not
the corrected parameter or the advertised theorem. Exact arithmetic and
the finite Taylor witness should be checked after this initial seal.

## Family8 — contribution boundaries and strongest provisional result

The mathematical reduction is general for bounded integral graph distances;
the fast median-graph consequence depends on a credited additive algorithm.
Optimization uses a credited method, with the explicit self-contained
comparison-only variant reconstructed above. The paper does not claim a new
median decomposition or a new source algorithm, does not improve the known
cube-free bound and does not settle unimodality, arbitrary edge lengths,
continuous facilities or infinite graphs. Actual OWR wording and the actual
prior optimization/special-case theorems must be checked to substantiate
the claimed scope connection. They cannot establish worldwide firstness
or October2026 openness merely from absence of a found predecessor.

My strongest paper-only deduction is the exact threshold identity and the
full-output comparison optimization, together with a correct abstract
volume/depth recurrence **conditional on the stated structural/oracle
interfaces**. I see no counterexample yet in those elementary mechanisms.
This is not a final pass: the imported additive interface, changed-parameter
structural validity, internal-label arithmetic and actual primary claims
remain the central post-seal checks. If a substantive gap is found there,
record its exact evidence and stop that repair route rather than inventing
a new fast oracle or promoting the conditional elementary reduction alone.
