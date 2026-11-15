# Independent analytic derivation — full original theorem23385145

This closes the obligations identified in the sealed paper-only reconstruction.
It concerns the original promised-median, finite unit-edge vertex-center
theorem and its exact-operation model. No smaller graph category, positive-only
weight restriction, fixed cube dimension or supplied embedding is substituted.

## 1. The reduction and complete-output optimization

In a nonempty connected simple unit-edge graph of order n, put D=n-1. All
distances j are integers in[0,D]. For R>=0 and a nonnegative finite weight w(u),
the set of indices k with k*w(u)<=R is a nonempty initial interval of[0,D].
Let b_R(u) be its last index and a_R(u)=D-b_R(u). When w(u)=0, b_R(u)=D.
Consequently, for every x,u,

`w(u)d(x,u)<=R iff d(x,u)<=b_R(u) iff d(x,u)+a_R(u)<=D`.

Taking the conjunction over u gives the exact full vector identity

`F_R={x:r_w(x)<=R}={x:E_(a_R)(x)<=D}`.                   (1)

It holds for every bounded integral graph distance, without any median
geometry. Medianity is used solely to obtain the fast additive vector E.
All converted arrivals are integers0<=a<=D. The graph, including zero-weight
vertices, is retained. Upper-bound binary search on k computes b in O(log(2n))
comparisons, never using real division or an unbounded floor.

Each r_w(x) is an attained maximum k*w(u), so rho lies among n sorted rows
S_u=(0,w(u),...,D*w(u)). Store only inclusive active intervals[l_u,h_u],
not the n^2 entries. Initially B=D*max w is feasible, witnessed by any vertex.
For n=1 return rho=0 and the sole vertex before comparing coefficient1
values; for B=0 all vertices are centers. Otherwise keep a feasible incumbent
and witness and the invariant: B=rho or an active entry equals rho.

At an iteration let M be the total active length, and choose a weighted
median q of row lower-middle values, weighting each by its row length L_u.
Both weak sides of q carry row-length mass at least M/2. Query(1).
If feasible, replace B by min(B,q), retaining an appropriate witness, and
delete entries>=q. If infeasible, delete entries<=q. The invariant survives:
at feasible equality rho=q it is saved; when rho<q it survives the deletion;
at infeasibility rho>q every optimum copy survives. A middle of a row of
length L has at least L/2 entries on either weak side. Thus at least M/4
entries are deleted in either branch, including all tie and singleton cases.
Starting at M=n^2 gives O(log(2n)) queries. Empty intervals force B=rho;
the final full query F_B is exactly C_w, and its witness is a center.

All pivots/incumbents are represented by pairs(k,u),0<=k<=D. The algorithm
only compares such bounded multiples. Abstract threshold identity(1) allows
any R, but the optimization calls it only at these candidate pairs; it does
not introduce a comparison with a new arbitrary real expression.

## 2. Actual additive primary interface and geometric correctness

I personally read BDH arXiv2410.10235v1 pages1–24, including all material
for its Theorem1: problem/interface, prerequisites, sections3–4, Algorithm1
and complexity proof. It is the actual October14,2024 v1 body, not a later
mixed edition or a secondary summary. Pages2–3 explicitly permit natural
nonnegative integer arrival values and return **every** additive eccentricity
`max_v(d(u,v)+omega(v))` in O(n log^4 n). Page6 explicitly includes zero
arrivals. There is no cube-dimension or embedding promise in that interface.

The relevant classical structure is also checked in the authors' actual
Bénéteau–Chalopin–Chepoi–Vaxès v2 primary body,1907.10398v2, pages5–13 and
30–32, including the Θ/halfspace and majority preprocessing arguments and
the auxiliary structural proofs. This author version is distinguished from
the inaccessible final JCSS typesetting; it is not silently called that PDF.
The classical facts imported are convex=gated in median graphs, gated
halfspaces and their boundaries, orthogonal incident classes spanning a cube,
Θ-class preprocessing and halfspace cardinalities/median computation.

For clarity, the load-bearing BDH identities can be checked directly.
If a convex halfspace H has gate g_H(x), then for every v in H,
`d(x,v)=d(x,g_H(x))+d(g_H(x),v)`. Thus for a split H,K,

`E_G(x)=max(E_H(x), d(x,g_K(x))+E_K(g_K(x)))`, x in H.   (2)

The other half is symmetric. This is BDH Theorem3, pages13–14, and contains
no balance constant or weight-size hypothesis.

In an unbalanced node choose the unique graph majority median v0. Let umax
maximize d(v0,u)+omega(u), preferring v0 in a tie. If umax=v0, the triangle
inequality gives `E_G(x)=d(x,v0)+omega(v0)` for every x. Otherwise choose
the wide ladder of Θ-classes adjacent to v0 and separating it from umax.
It is an orthogonal incident family. The source's Lemma19 proves that when
the ladder of x from v0 is disjoint from that wide ladder, v0 lies on a
shortest x–umax path. Hence the triangle inequality is attained at umax and
`E_G(x)=d(x,v0)+E_G(v0)` there. This is a geometric identity; it does not
require a numerical ln-based balance constant.

Number the wide classes E_1,...,E_ell with minority halfspaces H_i'.
The large graphs are G_i=intersection of the first i majority halfspaces;
slices are S_i=G_i intersect H_(i+1)'. They are gated median subgraphs,
pairwise disjoint, and partition the wide-minority union. G_i contains v0;
each S_i is nonempty because the incident orthogonal classes span a cube,
whose appropriate unit corner lies in that slice. In particular recursive
calls are on nonempty graphs and intrinsic distances equal original ones.

For a slice S in G_i, define its boundary arrival omega* at g as the maximum
`d(g,z)+omega(z)` over its **open** fibre z in G_i outside S; at other slice
vertices retain omega. Open fibres at boundary gates are nonempty. For x
in S, gating factors every outside distance through the corresponding gate.
Therefore

`E_(G_i)(x)=max(E_(S,omega)(x),E_(S,omega*)(x))`.          (3)

No domination of omega by omega* is needed or generally true. The original
call is essential: in an unbalanced17-vertex star with weight100 at leaf1
and zero elsewhere, its wide slice{leaf1} has original arrival100 and open
fibre arrival2. Dropping the original call would incorrectly return2 at
leaf1 rather than100. The source Algorithm1 retains both calls.

For x outside S, (2) merges its already-known E_(G_(i+1))(x) with the plain
slice E_(S,omega) through its gate. Reverse peeling through all slices thus
returns all E_G. These are exactly source Theorem4/Corollary3, pages19–21.
I checked all their cases, the dominance shortcut and both recursive calls
in Algorithm1, page22. None needs a fixed original f(s)=2ln s; they need
the stated gated geometry and strict-majority existence.

## 3. The paper's corrected recursion, without transferring the difficulty

The actual v1 states log=ln on page4, but bounds cube dimension by log2 s
on page7. Its page18 large-set and page24 duplicated-volume conclusions
use ell<=ln s. The latter inequality is false in general. Its page13
Lemma16 product comparison also has the wrong direction: if s_i>=s_h,
then `1-1/(lambda ln s_i)>=1-1/(lambda ln s_h)`, not <=. These are actual
displayed v1 issues, visually confirmed against fresh page pixels. The target
already addresses them; this review is checking that existing correction,
not undertaking a new repair of a defective target.

For each recursive order s>=3 the target uses
`L(s)=ceil(log2 s)`, `f(s)=2L(s)`; direct s<=2 cases stay unchanged.
Balance is tested exactly by `f(s)*min(|H|,|K|)>=s`. If unbalanced, each
minority is strictly smaller than s/f(s)<=s/2. BDH Lemma17 is expressly
stated for **any** f(s)>=2, and its majority-rule proof applies. The cube
spanned by the wide ladder has2^ell vertices, so ell<=log2 s<=L(s).

Each slice has |S_i|<s/f(s), and there are two calls per slice. Hence

`sum_child |V(child)|=2 sum_i |S_i| < 2ell*s/f(s)<=s`.     (4)

This also corrects the large-set assertion used locally:
`|G_i|>=s-i*s/f(s)`, so `|G_ell|>=s/2`. Balanced children partition s.
Every balanced child has size<=s(1-1/f(s)); every unbalanced slice has
size<s/f(s)<=s(1-1/f(s)). No extra call on G_ell is present: its labels
are given directly by the disjoint-ladder identity. All source recursive
branches have now been accounted for, not merely the threshold lemma.

For s>=3, `f(s)<=4log2 s=lambda ln s`, lambda=4/ln2. Along an arbitrary
nonterminal path from N, each s_i<=N and

`s_(i+1)<=s_i(1-1/(lambda ln s_i))`
`          <=s_i(1-1/(lambda ln N))`.

Thus `s_h<=N exp(-h/(lambda ln N))`. At
`h=ceil(lambda (ln N)^2)` the bound is<=1, so the path must already have
reached its s<=2 base case. This is a direct path proof. It needs neither
the erroneous product direction nor a possibly discontinuous global-max
recurrence for the rounded f(s).

The checked primary local work is O(s log^2(2s)): deterministic Θ/halfspace
preprocessing, one ladder BFS with O(log s)-size class lists, and at most
ell scans/gate BFSs over the G_i. Computing each open-fibre maximum is one
such BFS/scan before the corresponding recursive call. From (4), each
recursion depth has total vertex volume<=N, even with both arrival calls.
There are O(log^2 N) depths. Therefore total additive time is
O(N log^4(2N)). This is the full existing additive mechanism with the
manuscript's rounded balance parameter; the central difficulty is not
assigned to an unspecified faster subroutine.

## 4. Input size, exact arithmetic and the final exponent

Median graphs are partial cubes; the actual sources also give the stronger
local indegree/cube proof `m<=d*n`, `d<=log2 n`. Thus adjacency input is
O(n log(2n)). All recursively gated graphs satisfy the same bounds at their
own order. The credited preprocessing is deterministic; no randomness or
supplied embedding is imported. Standard graph/word operations and integer
labels are counted in the source model, not arbitrary-precision unit-cost
input-weight arithmetic. The target promises O(n) row storage **beyond**
the additive oracle and makes no linear-space claim about that oracle.

The converted initial arrivals are at most N-1. A recursive open-fibre
update replaces an arrival by a maximum of arrival+distance, increasing its
maximum by at most N-1. No merge feeds an eccentricity back as a new arrival
except this explicit formula. Along the proved O(log^2 N) depth, every
arrival is O(N log^2(2N)), hence O(log(2N)) bits; eccentricity outputs differ
by at most another N-1. These integer-label calculations do not multiply
or add arbitrary original-profile values. Computing L(s) by bit length or
a bounded integer loop fits the local O(s log^2(2s)) budget.

Each outer iteration uses O(n log(2n)) original-profile comparisons for
sorting, budget searches and row deletions. Over O(log n) iterations the
total is O(n log^2(2n)). Its O(log n) complete additive calls cost
O(n log^5(2n)); the final all-centers call and O(n) output scan fit. For
rational inputs with B-bit components, pair comparison uses products
`k*p_u*q_v`, `j*p_v*q_u` with O(B+log n) bits. Their arithmetic and input
reading must be paid separately. No encoding-independent bit complexity,
recognition, continuous facility, arbitrary edge length or infinite-input
algorithm is implied.

## 5. Exact appendix witness and bounded falsification evidence

For the original v1 estimate take Q_30, L=17000000000 leaves at each unit
vertex, and Z=488926258176 leaves at zero. Pendant attachment preserves
medianity by gated amalgamation, or directly by taking interval medians in
the attached tree/original graph. The count is `2^30+30L+Z=10^12=N`.
Each coordinate minority has `2^29+L=17536870912` vertices; each pendant
minority has1. The exact positive Taylor sum through29 for e^7 exceeds1000,
so ln N=4ln1000<28. Multiplying the coordinate minority by56 yields
982064771072<N. Thus all cuts are unbalanced under the literal2ln N rule.
All majority sides intersect uniquely at zero.

Set arrival N-1 at the cube antipode and0 elsewhere. It has additive distance
N+29 from zero, while every other vertex has ordinary distance<=30, so it
is uniquely farthest. The wide ladder is all30 coordinate classes. The
actual BDH slices partition the first-nonzero-coordinate sets: their cube
sizes are2^29,2^28,...,1, with L leaves at the corresponding unit each.
Their union has511073741823 vertices; two slice copies have
1022147483646>N. This refutes the **literal intermediate volume estimate**.
For the corrected rule L(N)=40,f(N)=80; each such coordinate cut is instead
balanced since80*17536870912=1402949672960>N. The example does not refute
the target theorem or its corrected recursive bound.

Own exact controls checked10004 profiles on every connected labelled graph
through4 vertices, including all median ones and deliberate nonmedian
controls of (1). A binary-search-only pair comparator enforced every real
multiplier in[0,D], verified33394 search progress/invariant steps and the
complete center set, plus1617 middle-rounding cases,4103 recursion parameter
cases and four large-bit/boundary profiles. These are finite falsification
controls, not a proof of the universal running time.

One inspected native verifier was copied byte-identically and only its two
bounded functions were run:17 structural profiles up to408 vertices plus
its succinct volume calculation. They exercised balanced, unbalanced and
dominance branches, including both slice calls. Its compressed control uses
arrival N instead of the manuscript's N-1; either is uniquely farthest and
has the same volume, while the exact N-1 argument is given above. Native
all_small/main/run_all/builders were not run. The fast classical Θ machinery
was not reimplemented as executable code here; it was checked at its actual
primary proof interface and remains a credited classical dependency.

The whole original theorem is supported by these deductions and imports.
No substantive in-scope mathematical gap was found. The ordinary classical
algorithmic theorems are not proof-assistant certified here, and no finite
experiment certifies the asymptotic result. The full final SODA chapter
was not recovered (actual publisher403 retained); the full relevant v1
algorithm/proof and existing correction were checked without attributing
the v1 errors to the uninspected final typesetting. Worldwide historical
firstness and continued October2026 openness remain uncertified, as the
manuscript itself states.
