# Independent hand derivations before support / foreign proofs

2026-11-17 UTC. These controls use only the actual original manuscript
plus ordinary prior mathematical knowledge. No code, stored result,
archived review, support proof or foreign mathematical body has been
opened or run. The imported FPRAS premise is not proved by this file.

## A. Signature via a directed flow, including W=1

Read the binary expansion of W>=1 from its leading1. An initial s->t
path counts1. For a following digit b, add fresh a,z with t->z,
t->a and a->z; if b=1 add s->z. Old paths gain two distinct tails, and
the extra direct s->z path is new. The count is therefore w->2w+b.
All new vertices follow the old ones in a topological order, so no
directed cycle is introduced. The new sink is fresh, and the old sink
is never s, so no duplicate arc is introduced.

With ell binary digits, the DAG has2ell vertices. Removing s,t leaves
2ell−2 internal vertices. Replace each internal i by Li,Ri and an
identity edge LiRi; retain only Ls=u and Rt=v at the ends. Each directed
arc i->j becomes LiRj. There are4ell−2 graph vertices and at most
(4ell−3)+(2ell−2)=6ell−5 edges. Acyclicity excludes loops/identity-edge
duplicates, so the graph is simple and bipartite.

A full perfect matching makes every internal i either an identity pair
or a node with one selected incoming arc and one selected outgoing arc.
The source has one outgoing arc and the sink one incoming arc. The
selected arcs are one s-to-t path plus directed cycles; no cycles exist.
Conversely, a directed path fixes all its arc edges and all off-path
identity edges. This is a bijection, hence #PM=W.

After deleting both terminals, all selected arcs would have equal in/out
degree at every remaining node. Any nonempty finite circulation contains
a directed cycle. Thus there are no arcs and exactly the all-identity
matching. Deleting just u or v leaves odd vertex count and zero perfect
matchings. The complete signature is (W,1,0,0), not just a full-count
identity that could fail under gluing.

Small hand controls, using the recurrence and actual graph-size counts:

| W | Binary | Path counts after each digit | H vertices | H edges |
|---|---|---|---:|---:|
|1|1|1|2|1|
|2|10|1,2|6|6|
|3|11|1,3|6|7|
|4|100|1,2,4|10|11|
|5|101|1,2,5|10|12|
|7|111|1,3,7|10|13|
|8|1000|1,2,4,8|14|16|

In particular W=1 has no internal vertex: selected gives its one edge,
unselected gives the empty graph's unique matching. The formulas remain
valid. W=0 is not a gadget case and must be removed from support first.

## B. Global fibers and nonbipartite input

Assign each original unordered positive edge e a fresh gadget, sharing
only its two original endpoint vertices. Any gadget's internal vertex
count is even, and all its internal vertices can be matched only through
that gadget. Therefore the number of original endpoints covered by
edges assigned to this gadget is even, either0 or2. Original vertices
are globally covered exactly once. Hence the gadgets covering both ends
form an original perfect matching M. Their full-signature choices are
independent; all unselected gadgets have their unique both-terminals-
deleted matching. This accounts for every global matching, with no
double count.

For p_e/q_e>0, D=product q_e and W_e=p_e(D/q_e) are positive integers.
Consequently each fiber has product W_e=D^m product A_e matchings and
#PM(H)=D^m haf(A). Direct u-v edges from W=1 or a final1 digit cannot
create parallel edges across gadgets: only one original support edge
has that pair of endpoints. Internal vertices are all fresh. The final
graph need not be bipartite: taking unweighted K4 makes every W_e=1
and H=K4, with three perfect matchings. A bipartite permanent FPRAS
cannot be silently used as the external general-graph input.

## C. Rational/zero/unused-edge control with actual arithmetic

Use four vertices and positive entries
A12=1/2, A34=2/3, A14=5/7, A23=3/5, A24=17/5;
put A13=0 and make the matrix symmetric. Diagonal entries are irrelevant.
The only positive perfect matching products are
(12,34):1/3 and (14,23):3/7. Thus haf(A)=1/3+3/7=16/21.
The positive edge24 is unused in any support perfect matching because
its complementary edge13 is absent.

The prescribed common denominator is D=2*3*7*5*5=1050, including that
irrelevant positive edge's denominator. The integer weights are
W12=525, W34=700, W14=750, W23=630, W24=3570.
Their relevant products are525*700=367500 and750*630=472500.
The expanded count is840000, and
D^2 haf(A)=1102500*(16/21)=52500*16=840000, as required.
Uniform expanded matching projects to probabilities7/16 and9/16,
exactly the normalized original products. It is not in general uniform
on the two original matchings. Reducible fractions would change D and
all fiber multiplicities by a common factor, not the normalized law.

For m=0: D=1 (empty product), H has no vertices, #PM=1, haf=1 and the
sample is empty. No division by k is invoked in this boundary case.
For m>0 and no support edge: H has2m isolated vertices, #PM=haf=0;
feasibility reports infeasible. A triangle plus an isolated fourth
vertex is another infeasible case despite positive edges. Added gadget
internals have even counts, so the odd component/isolated-vertex
obstruction cannot disappear.

Nonnegativity is essential. If A12=A34=A13=1, A24=−1 and A14=A23=0,
then the support has two perfect matchings but haf=1−1=0. This is a
signed boundary counterexample to extending positivity/zero detection,
not a counterexample within the paper's stated scope.

## D. Bit bounds, without unary expansion

For the ordinary explicit binary matrix representation, m and the
number r of positive unordered entries are bounded by O(L). In fact
the dense representation is larger, but only this weaker inequality is
needed. The model is not a succinctly described huge matrix with a
binary dimension and implicit exponentially many entries.

log2 D <= sum log2 q_e <= L. Also
log2 W_e <= log2 p_e + log2 D <= O(L), so ell_e=O(L).
This remains true when denominators are repeated, unreduced or enormous
in value. We use their bit lengths, not their numerical values.

There are2m+4 sum(ell_e−1)=O(L^2) vertices and O(sum ell_e)=O(L^2)
edges. Vertex indices cost O(log(L+2)) bits. Grade-school multiplication,
long division by q_e (exact because it divides D), and binary
exponentiation operate on polynomially many polynomial-length operands.
bits(D^m)<=1+m log2D=O(mL+1). If a perfect matching exists, at least
one integer fiber has size>=1, hence haf(A)>=D^-m. Tiny positive
weights do not force a denominator with superpolynomial bit length.

The final output count itself has polynomial bit length: log(#PM(H))
is bounded by the logarithm of (|V(H)|−1)!!, at most
O(|V(H)| log(|V(H)|+2)). The imported counting estimate must also have
polynomial length on failed tapes, which follows only from its required
every-tape bit-time contract, not just from the true count's size.

## E. Exact zero wrapper and relative approximation

For m>0, exact support feasibility decides whether Z=0, independently
of the random counter. On infeasible support return0 immediately. On
feasible support C=#PM(H)>=1. A successful epsilon-relative count with
epsilon<1 is strictly positive, since (1−epsilon)C>0. Replacing a zero
estimate on failed tapes by1 therefore changes no successful outcome.
Dividing by D^m preserves the successful relative inequality exactly:
|Chat/D^m−Z|=|Chat−C|/D^m <=epsilon Z.
On all tapes the feasible output is positive. delta'=min(delta,1/4)
is in the stated external parameter range and has failure<=delta.
No random zero is ever used as a certificate that a positive count is
zero. No unbiasedness or expectation guarantee is inferred.

## F. Adaptive conditional TV and finite-bit choice

Fix the history before a stage. The current graph and feasible child
graphs are now fixed. Exact witnesses ensure that every selectable edge
has a completable child. A single feasible child needs no count; if all
estimates are zero, appending the stored current witness still produces
a valid full matching. Already chosen edges have disjoint removed ends.
Every run has at most k stages, even on failed counting tapes.

For a stage with j feasible children, write true counts c_i>0 and
p_i=c_i/sum c. On simultaneous success,
(1−alpha)c_i <=a_i<=(1+alpha)c_i, and summing gives the same bounds
for totals. Therefore (1−alpha)/(1+alpha)<=q_i/p_i
<=(1+alpha)/(1−alpha), so
sum |q_i−p_i|/2 <=alpha/(1−alpha).

For the dyadic choice, floors of2^b Q_i are nondecreasing, start at0
and end at2^b, so the half-open bins cover every integer draw exactly
once. Empty bins have probability0; they do not cause an undefined
draw. Each mass differs from q_i by at most2*2^-b (a safe bound), hence
TV<=j2^-b. This is a bounded fair-bit construction with exact rational
floor division, not unbounded rejection sampling.

Fresh independent counting tapes give a conditional failure union bound
<=j gamma at THIS history. Integrate over the actual current estimates;
on the failure event use TV<=1. Do not condition the entire output law
on a global future-success event, which could bias branch probabilities.
Couple to the exact child-count recursion only until histories first
disagree. The stage discrepancy is at most
alpha/(1−alpha)+j gamma+j2^-b. Summing conditional first-disagreement
bounds uses no independence across all adaptive stages.

At a stage with2h remaining vertices, there are at most2h−1 candidate
neighbors. Hence both count calls and total outcome counts obey
sum_{h=1}^k(2h−1)=k^2=C. Feasibility needs at most C child checks plus
one initial witness. With alpha=eta/(4k), gamma=eta/(4C),
b=ceil(log2(4C/eta)),
k alpha/(1−alpha) < eta/3,
C gamma=eta/4 and C2^-b<=eta/4.
The full TV bound is <=5eta/6<eta. The ideal recursion is uniform
because a child completion corresponds bijectively to a matching
containing the selected edge. Oracle tape bits are additional to the
at-most-kb categorical bits.

## G. Explicit rational CDF controls on K4

For K4, k=2 and C=4. Choose eta=1/2, so alpha=1/16, gamma=1/32
and b=5. At the first vertex there are three feasible child counts,
each1. Exact estimates give q=(1/3,1/3,1/3), floor-CDF endpoints
(0,10,21,32), and output probabilities (10,11,11)/32. The TV from
uniform on the three perfect matchings is
(1/2)(1/48+1/96+1/96)=1/48. Each subsequent child is forced.

Successful perturbed rational estimates (15/16,1,17/16) give
q=(5/16,1/3,17/48). The CDF floors become (0,10,20,32), giving
law (5/16,5/16,3/8) and TV
(1/2)(1/48+1/48+1/24)=1/24. This checks the exact bin endpoints and
normalization with noninteger estimates at the allowed relative errors.

If all three estimates are0, the stored witness fallback is a point
mass whose TV from uniform is2/3. This is NOT itself an eta-close
conditional law. It is an explicitly failed-estimate event, whose
probability is bounded by3gamma at this history. The proof correctly
pays for that event rather than claiming every failed tape's law is
uniform. For a two-vertex feasible graph, j=1, so no counting call or
categorical randomness is needed at all.

## H. Arithmetic runtime and weighted projection

If each estimate has at most T bits, the sum of j rational estimates
can be formed over the product of their denominators with O(jT)
bits (plus polynomial overhead). Every cumulative rational, multiplying
by2^b and floor division therefore has polynomial bit cost in N,T,b.
The parameters alpha,gamma have polynomial encoding length in the
original accuracy encoding and log(k+2), and b=O(log(k+2)+log eta^-1).
This is worst-case polynomial in eta^-1, as claimed, not necessarily
in log eta^-1. It still requires the imported every-tape polynomial T.

Let pi map an expanded matching to its selected original edges.
Uniform fibers give pi_*Unif(H)(M)=D^m product A_e/(D^m Z)=mu_A(M).
For any two laws rho,sigma on expanded matchings,
sum_M |sum_{x:pi(x)=M}(rho(x)−sigma(x))|
<=sum_x |rho(x)−sigma(x)|.
Dividing by2 proves TV contraction. No equal-size-fiber assumption is
made; the unequal7/16 and9/16 control above demonstrates the needed
weighted law.

## Remaining original-claim gate

These local derivations support the reduction and wrappers CONDITIONAL
on the exact external approximation/witness interfaces. They do not
establish OpenAI's universal general-graph FPRAS, its bit model, every-
tape runtime, or the advertised formal scope. Substantive primary-proof
reading after the initial seal and explicit resume is indispensable.
Finite gadget/signature/sampling-law checks cannot discharge that
central obligation. No final PASS or DEFER has been inferred here.
