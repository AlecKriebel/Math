# Root reconstruction of PR374's five scoped results

2026-10-03 UTC. Source-first baseline and its immutable seal precede candidate
TURN/code reads. This reconstruction follows reading all five full proofs and
all eight programs. Historical review is corroboration only. Distinct fresh
agents separately sealed multipartite/triangle, local/rank-one, and recursive
cograph derivations before candidate code and historical review. No full
solution or novelty certification is claimed.

## Multipartite optimization, including sequences

The source-first baseline supplies the constrained fourth-moment argument.
The remaining endpoint issue is resolved by Holder:
sum a_i^2 <= (sum a_i^4)^(1/3)(sum a_i)^(2/3).
At q=1/k this forces fourth moment >=q^3, with equality exactly at uniform
positive parts. At nonreciprocal q, the support minimum is regular, its positive
roots have two sizes and the smaller size occurs once by the negative tangent
Hessian. This fixes r=floor(1/q) and the source vector, not just a stationary
branch. Cauchy forces any feasible dimension to admit its support size, so all
finite numbers of parts are covered by the same theorem.

For n_i/n=a_i, direct binomial expansion of sum_{i<j}binom(n_i,2)binom(n_j,2)
gives 24N/n^4=3(q^2-p4)+6(p3-q)/n+3(1-q)/n^2. Its error is <=6/n+3/n^2
uniformly in part count. Edge density is n(1-q)/(n-1). The piecewise moment
minimum L is continuous at reciprocal knots and0 (0<=L<=q^2). Thus arbitrary
sequences, even with increasing part counts, satisfy c<=F. Fixed-density
matching sequences come from rounding the optimal masses. For a countable
mass vector, merge a tail of mass t into one part; sum2/sum4 change by at most
t^2/t^4 plus original tail moments, tending to0. The finite theorem and
continuity extend to this vector. No infinite-dimensional KKT theorem is used.

## Joins and all near-minimum-triangle sequences

The pointwise inequality 1_C4<=M/2, where M counts the three present perfect
matchings, yields c<=3p^2/2: each matching uses disjoint pairs whose edge
probabilities multiply to p^2. It is valid for every graphon and reproduces
the credited LMR special case without assuming independence of incident edges.

For a complete join, the exact formula in the baseline permits replacement of
each internal density p_i<=1/2 by a complete bipartite model at the SAME p_i.
The cross contributions depend only on q_i=1-p_i. The gain is
sum w_i^4[(3/2)p_i^2-c_i]>=0. The replacement is multipartite, hence bounded
by F. Countable cases follow by absolute summability and the moment-tail
argument above. There is no replacement theorem for arbitrary hosts.

For finite adjacency graphons p=2e/n^2=(1-1/n)x; any four-point sampling
collision has probability <=6/n. A triangle-free block has p_i<=1/2 by Mantel,
so PR2017's extremal family lies in the controlled join class. Its Theorem1.1
applies at the graph's ACTUAL edge density, uniformly once epsilon is fixed.
An epsilon*binom(n,2) edge edit changes at most that many times binom(n-2,2)
induced four-sets; divided by binom(n,4) this is exactly6epsilon. Since the
input triangle excess tends to0, every fixed epsilon eventually applies.
The resulting edge difference <=epsilon suffices via continuity of F even
without using the stronger construction-rounding fact. Let epsilon tend to0.
Endpoints follow from c<=3p^2/2 at0 and missing-edge probability at1.
Thus ALL asymptotic triangle-minimizing sequences are controlled, conditional
on the credited published stability theorem. Its full flag-algebra machinery
was not independently reproved here. Positive triangle excess remains a gap.

## Equality flexibility and perturbation topology

Replace the final a,b parts by an internal bipartite component u,v and isolated
mass z, with uv=ab,u+v+z=a+b. Edge/C4 internal contributions are exactly2ab
and6a^2b^2; complete-join cross contributions do not change. For interior
u in(b,a), z>0. A one-edge triple can only use u,v,z and has density6abz.
Multipartite graphons have none. Coupling three edge states gives motif change
<=3 times L1 graphon distance, so every relabeling is separated by >=2abz.
The rational example (4,2,2,1)/9 gives x=16/27,c=64/243,triangle=32/243,
one-edge triple8/243 and separation8/729. Tying the source value does not
assert unrestricted optimality. The prior triangle-extremal family already
allows this flexibility; no new priority for it is claimed.

The conditional edge-switch kernel is Kii=-(q-ai^2) and
Kij=(ai+aj)^2-q. The six-edge linear variation is6 integral hK. On a valid
perturbation of a 0/1 multipartite model, signs force h>=0 inside and<=0
outside; integral h=0 splits its L1 mass equally. The maximum within K minus
minimum cross K is -gamma=-b(2a+b), so the derivative is <=-3gamma||h||1.
The exact six-factor, three-pattern expansion has171 higher-degree terms.
For each, integrate one |h| factor and bound the others by eta=||h||infty;
unaffected factors are bounded by1. This gives171eta||h||1 regardless of
shared endpoints. At eta<=gamma/114 the deficit is >=(3/2)gamma||h||1.
It applies to arbitrary measurable symmetric h; it is an L-infinity theorem.

For the fixed-space path, u=a-s,e=bs/(a-s),z=s-e,0<s<a-b. The added and
deleted ordered-pair masses are each2bs, hence L1 distance4bs and amplitude1.
Its product uv=ab makes the actual C4 change0, while the derivative equals
-3gamma*4bs. The remainder is therefore +3gamma*4bs, not uniform little-o
of L1. Thus strict small-amplitude local optimality coexists with L1-close
ties, also close in cut distance since cut norm<=L1. No edit uniqueness follows.

## Universal recursive cographs

Differentiate the mass constraints to obtain L'(q)=2(a^2+ab+b^2), hence
F'(x)=-6[(r-1)a^2-ab]<=0 above1/2. Continuity supplies knots/endpoints.
Together with the known bipartite branch, 0<=F<=3/8. At q<=1/2 each optimal
part is at most a with q>=2a^2; L<=a^2q<=q^2/2, so F>=3q^2/2.

Join closure replaces each controlled child by its same-density multipartite
optimizer, then applies the multipartite theorem. A density-one child is
approximated by balanced finite multipartite children; the exact join formula
and continuity pass the limit. It is not represented by an invented finite
mass vector at density1.

For a union at global x>1/2, x=sum w_i^2p_i<=max w_i=w, so the largest
child is unique and w>=x>1/2. Others have squared-mass sum <=(1-w)^2.
The large child's density is >=[x-(1-w)^2]/w^2>=x because
(1-w)[x(1+w)-(1-w)]>=0. Thus its F-value is <=F(x). The union C4 value is
at most w^4F(x)+(3/8)(1-w)^4. Since1-w<=q=1-x, its deficit is at least
(3/8)(1-w)q^2(4-q)>0 whenever w<1 and x<1. At x<=1/2 the universal
matching inequality gives closure directly. Induct on every finite weighted
cotree, with independent zero-density leaves. Zero mass can be omitted.
The collision estimate is uniform in leaf count and depth, so EVERY finite
cograph sequence is bounded. Density convergence also supplies limits of
finite weighted cotrees. This proof uses the recursive definition; no P4
removal theorem, finite enumeration, or fixed-depth hypothesis substitutes for
it. Non-cographs remain outside this route.

## Rank-one universal profile and strict achievable comparison

The baseline gives an independent moment parametrization proving the same two
branches as the candidate's z=m2^2/p parametrization. Both cover ALL measurable
f in[0,1], including equality and boundary cases. The low branch maximizer has
f=1/sqrt2 on mass sqrt(2p), zero elsewhere; the high branch is constant sqrtp.
For fixed p, choosing f=d on mass sqrtp/d gives
c=3p^2d^4(1-d^2)^2; continuity from optimal d to1 attains every value[0,R(p)].
Finite random graph realizations have normalized fixed-motif variance O(1/n):
only intersecting vertex sets contribute covariance, each bounded by1.
Convergence in probability permits deterministic selections. Exact finite-n
extremality is not asserted.

For 0<p<=1/2, F-R=(21/16)p^2. For1/2<=p<=3/4, F>=3q^2/2 gives
F-R>=141q^2/256. Above3/4, the largest optimal part a<=1/r<=q/p since
r=floor(1/q)>=p/q. Then L<=a^2q<=q^3/p^2 and
F-R>=[3q^3/p^2][p^2(1+p+p^2+p^3)-1]>=1653q^3/1024.
The bracket is increasing and equals551/1024 at3/4; all operations preserve
signs for interior p. These are strict comparisons with an ACHIEVABLE F,
without assuming its conjectured all-host upper bound. The derivative
6p^3(1-p)(2-3p) gives restricted maximum16/243 at p=2/3.

## Verdict and quantitative evidence

All five scoped mathematical claims PASS root reconstruction; no mandatory
candidate correction found. root_original_replay.py checks all46 actual Git
bindings, all45 targetfiles, 36 immutable WIP author paths, nested manifests,
five historical commits and literal two-cell original queue change. It reruns
all eight programs privately and compares ENTIRE stored outputs:93,505 author
assertions,1,080 historical independent assertions, both frozen reviewer
streams and portable publication wrapper. Five fresh pinned PDFs are verified
separately; portable code does not itself fetch sources, and historical PNG,
HTML/text records must not be counted as fresh reproduced source bytes.

Finite controls corroborate the proofs. They do not establish missing universal
steps. The strongest verified result remains the collection above; arbitrary
non-cograph, non-rank-one hosts with positive triangle excess are not bounded
by F. Classify unsolved5/5, accept only a partial result, no preprint/DOI/tracker.
Workflow75%; unrestricted discovery0%. Fresh whole-package audit and actual
refreshed-head gate remain required before acceptance.
