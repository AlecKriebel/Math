# Source interfaces and corrected membership inequality

This document supplements the independent derivation frozen before historical
audit labels were read. It records direct inspection of the retained primary
bodies, distinguishes source facts from fresh deductions, and makes no priority
decision. The submitted argument is evaluated at Git head
`f37a3ff66595fcf75bb18bf859be8594c3662242`.

## Target and model

Farrell and Levine, *CoEulerian graphs*,
[arXiv:1502.04690v3](https://arxiv.org/pdf/1502.04690v3), PDF page 2, defines the
conservative strongly connected halting problem with a nonnegative input and an
adjacency-matrix representation. Section 3.1 and Table 1, PDF page 13, distinguish
the simple strongly connected case from binary multigraph hardness. The simple
case permits each ordered-pair multiplicity to be zero or one. The candidate
proves hardness on its loopless subclass, and its separate oriented subclass
also excludes antiparallel pairs. Thus neither possible convention for opposite
arcs prevents the claimed answer. Loops, if admitted in the larger question,
are not needed for hardness. The NP-membership proof covers the stated loopless
language and the credited multigraph membership result covers the larger model.

The Egres target URL was tried afresh during this resumed review and the web
tool reported it inaccessible. No successful current page inspection is
claimed. The submitted historical Egres observations are not new evidence.
The complete explicit source question in the directly read FL body suffices
to reconcile mathematical target and scope. Neither an old question mark nor
a failed page fetch proves present-day openness.

Hujter, Kiss and Tóthmérész, *On the complexity of the chip-firing reachability
problem*, [arXiv:1507.03209v4](https://arxiv.org/pdf/1507.03209v4), Sections 2.1
and 2.2, PDF pages 2–3, confirms the loopless multigraph, binary adjacency and
nonnegative asynchronous conventions, including the ordinary meaning of a
terminating maximal legal game. Its Laplacian is the negative of the candidate's
positive-diagonal Delta. The review never mixes those signs. The halting
discussion on PDF page 13 concerns Eulerian graphs; no Eulerian result is
inferred for this construction.

The exact retained PDF identities are in SOURCE_ACQUISITION.json and rechecked
in REPRODUCTION_RECEIPT.json. SOURCE_VISUAL_RECEIPTS.json records six actual
pre-interruption page views, with image hashes recorded before deleting only
the disposable rendered images. This resumed review additionally read the FL
definition, least-action, tree/period, membership and simple-question text and
the HKT model and dichotomy text. It does not claim publisher-PDF identity or
to have verified every theorem in either whole paper.

## A false intermediate source inequality

FL PDF page 10 informally bounds a predecessor's firing count by the head's
outdegree times its firing count, omitting residual stable chips. That
intermediate assertion is false even on a three-vertex loopless simple strongly
connected graph. Use arcs

    0 -> 1,   1 -> 0,   1 -> 2,   2 -> 0.

Start with `x=(1,0,0)`. The legal word consisting only of vertex 0 terminates
at `z=(0,1,0)`, since the outdegrees are `(1,2,1)`. Its odometer is
`f=(1,0,0)`. On `0 -> 1`, the uncorrected bound would assert `1 <= 2*0`.
This explicit counterexample is independently checked in both runtimes.

The candidate already retains the necessary slack. With nonnegative `x`, stable
nonnegative `z=x-Delta f`, and an arc `u -> v`, balance gives

    sum_(a -> v) f_a = d_v f_v + z_v - x_v,
    f_u <= d_v f_v + d_v - 1,
    f_u + 1 <= d_v (f_v + 1).

No incoming firing count is negative. The last `-1` uses integrality and
`z_v<d_v`, and the nonnegative initial input is essential for dropping `-x_v`.
This is a proof of the exact inequality needed in the candidate, not a blanket
certification of every printed line of the cited paper.

## Complete certificate bound

A certificate is a binary vector `f>=0` for which `z=x-Delta f` is stable and
nonnegative. At a first firing exceeding `f` in coordinate `v`, the other counts
are at most their prescribed values and its own is exactly `f_v`; its chip
count is at most `z_v<d_v`. This proves soundness even if the supplied vector is
not itself a legal firing word. Every legal word has length at most `sum f`,
so every maximal legal play stops. No fairness condition enters.

For a halting instance take its actual legal odometer `f`. Let `pi` be the
primitive positive kernel vector of Delta. Directed rooted-tree cofactors give
`pi_v=kappa_v/gcd(kappa)`. Each non-root tree vertex chooses one of at most
`N-1` outgoing neighbors, so `1<=pi_v<=(N-1)^(N-1)`. If `f>=pi` coordinatewise,
then `f-pi` is a smaller nonnegative stabilizing vector with the same `z`.
Applying the preceding first-excess argument to the actual word contradicts
that assertion. Hence some `w` has `f_w<pi_w`.

Follow a simple directed path **from** any `u` **to** `w`. Iterating the corrected
edge inequality along its at most `N-1` arcs yields

    f_u+1 <= (N-1)^(N-1) (f_w+1)
           <= (N-1)^(N-1) pi_w
           <= (N-1)^(2N-2).

The direction of the path matters. Each coordinate therefore has `O(N log N)`
bits. Binary verification uses polynomially many additions and multiplications
on numbers of polynomial bit length, also accounting for the input chips'
own bit lengths. An exponentially long stabilizing word is never supplied.
For `N=2` the graph is the two-cycle, stable capacity is zero, and nonnegative
halting input and odometer are both zero; the displayed bound gives `f+1<=1`.

The source defect therefore creates no unresolved candidate issue: the
candidate's self-contained corrected specialization establishes the credited
membership conclusion independently. Attribution to the established
least-action/period/tree method remains necessary. This review makes no new
membership claim and no judgment about the full literature's priority.
