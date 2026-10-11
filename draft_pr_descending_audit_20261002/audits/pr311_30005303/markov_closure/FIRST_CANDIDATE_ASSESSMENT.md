# First independent candidate assessment: Markov/closure family

Prepared at 2026-10-04 16:01:58 UTC. This assessment is frozen before access to
candidate checker code, checker output, historical reviews, other-family
conclusions, or the root's current mathematical reasoning. Only TURN_1.md,
TURN_2.md, SOURCE_GATE.md, and SOURCE_RECHECK_2.md were released and read,
after the source criteria's immutable hash had been accepted by the root.

The frozen source criteria SHA256 is
`dab23a2c8f753dced42b7d93ed06564eecdf1bc36be3ae272ba4ec0611e42b9b`.
Candidate prose hashes:

- TURN_1.md: `909ea0bb5330c037fabda8dfc468bfdc7af5e95809db516d3d20fb303b061374`
- TURN_2.md: `d2594ebda66841fd57355e4bbc41cc48c0c2a73033a6979a201abb967e69d20b`

## Independent assessment

**Both candidate mathematical conclusions pass this family's prose audit.**
The proposed C4 law refutes the exact source Conjecture 2 (and Conjecture 3).
The support reduction and residual-cut normalization prove Conjecture 1 in
the finite binary source setting, with zeros and literal isolated-vertex
conventions included. I found no unsupported central lemma, circular step,
missing limit normalization, or source-scope enlargement. This is a
mathematical audit conclusion, not a historical priority or publication claim.

The candidate's bounded literature and repository searches have not been
independently reproduced in this family. No priority inference is made from
them. Checker-code correctness remains a separate unreleased audit stage.

## C4 counterexample: independent verification

Take source C4 with edges 12,23,34,41. Identifying x1=x2=a gives the support
cube (a,b,c), b=x3 and c=x4. The function abc is the top-atom indicator. When
one of two inputs is the top, its supermodular inequality is an equality;
when neither is the top, the right side is zero and the left side is
nonnegative. Exponentiating and pulling back through the equality embedding
therefore proves MTP2 on support. Off-support inputs make the MTP2 right
side zero. Seven weights are 1 and the top weight is 2, so the normalized
mass has denominator 9.

I independently enumerated source graph separations. The only nontrivial
ones are the two opposite-vertex pairs conditioned on the other opposite
pair, with four ordered choices. Each CI follows from one tested variable
being determined by the conditioning variables. No hidden faithfulness,
positive-support, or minimal-graph hypothesis exists in the source.

On the quotient cube, the four even-parity atoms and four odd-parity atoms
have equal projection multisets onto every source edge, singleton, and empty
clique. Thus every finite real clique product has equal even and odd products;
zeros and signs do not affect this substitution argument. For this law the
products are exactly 1/6561 and 2/6561. The polynomial identity also excludes
membership in the factorizing model's pointwise closure. This distinction is
consistent with the source's explicit M_E versus M_F models.

## Closure proof: independent derivation of the critical steps

### 1. Pairwise support produces a poset

After absolute values, finite factors are nonnegative. For a factorizing law,
support is exactly the intersection of the allowed unary and edge
projections: if all projected patterns occur on positive atoms, every
corresponding factor is positive. Global minimum and maximum of a nonempty
sublattice are support atoms. Hence each active edge projection contains
00 and 11; its only possible remaining restrictions are directed
implications or equality. Fixed-active edges add no restriction beyond the
fixed coordinate, since both active values occur.

Directed implication cycles force equality, and their strongly connected
components are connected through original graph edges. Quotient reachability
is a poset. The support consists exactly of its upper sets with the fixed
coordinates appended, since the local support identity leaves no additional
constraints. This handles nonsubcube supports and empty active sets.

### 2. Aggregate MTP2 interactions can be lifted to original edges

Each factor's logarithm is finite on the patterns that actually occur. On
equal coordinates it is unary. On comparable distinct components, the
three patterns 00,01,11 span affine functions of the two bits; equivalently
their product equals the lower bit on that support. Only incomparable
component pairs need quadratic coefficients. Combining all original edges
between one component pair produces an aggregate K_AB.

For incomparable A,B, the strict successors of either component form an
upper set U omitting both. U, U+A, U+B, and U+A+B are all support upper sets.
Their mixed log difference cancels every constant, unary term, and term
involving other components, leaving exactly K_AB. MTP2 gives K_AB>=0.
This argument requires aggregation and does not assume that a masked
original edge factor is itself MTP2.

Put a component's unary coefficient on one original vertex and each
nonnegative aggregate on one original edge joining those components. On
support this gives the correct log density up to its constant. Penalizing
each active-edge implication violation by -t*x_i*(1-x_j), and fixed-bit
violations by unary terms, adds only nonnegative original-edge quadratic
couplings. The penalty is zero precisely on support. The resulting positive
attractive law converges to the original density after finite normalization.

### 3. The residual representation removes degeneration of normalization

For a strictly positive attractive law, its negative log energy is a sum of
directed nonnegative disagreement penalties and real unary terms. Source
and sink capacities encode the unary signs. Each cube state is a cut, and
cut capacity equals energy plus a constant.

A maximum flow exists by compactness of the bounded feasible flow polytope.
If its combined residual graph had a source-to-sink path of positive
capacities, a sufficiently small augmentation along a simple path would
increase its value while preserving feasibility. Thus the reachable cut has
zero residual capacity. Summing conservation across any cut gives residual
cut capacity equal to original cut capacity minus the maximum-flow value.
Consequently every residual cut cost is exactly E(x)-min E.

Exponentials of residual capacities give finite unary and original-edge
factor values in (0,1]. At a minimizing state the product is 1. The sum of
products lies in [1,2^|V|], uniformly over all parameters. A subsequence of
the finitely many factors converges in [0,1], with each state selecting
factors by a polynomial rather than an ambiguous 0^0. The limiting product
sum is still at least 1, so it gives exact finite edge factorization after
normalizing. MTP2 and global Markov persist by the independently frozen
polynomial arguments.

The forward and reverse inclusions give F_2(G)=closure(A(G)). F_2(G) is
therefore closed; alternatively selecting an attractive approximation
within 1/n for each original sequence member proves the closure statement
directly. This is a genuine mechanism, not an assumption that factor images
are closed.

### 4. Literal source conventions

On a graph without isolated vertices, assign every unary factor to an
incident edge and absorb the scalar normalizer into any edge. With isolated
vertices and at least one edge, the literal source model forces the uniform
product on isolates; this condition is closed and independent of the
nonisolated model. The candidate explicitly handles the source's nonempty
edgeless empty class, optional scalar-uniform convention, and V=empty.
All yield the same affirmative closure answer. No arbitrary unary factors
at isolates are silently added to the literal conclusion.

## Independent exact controls

Authored and run `independent_controls.py` with no candidate checker read.
It reads no input artifacts and uses only exact integers and fractions.

1. Exhaustively enumerate every nonempty subset of binary cubes of dimensions
   0 through 4, select all sublattices, and enumerate every simple graph on
   each cube. Whenever the support is recoverable from its unary/edge
   projections, check exact recovery by fixed coordinates and active-edge
   implications. At dimension 4 this includes all 731 nonempty sublattices
   and 17,672 graph/support representations. Across dimensions 0-4 there
   are 18,067 passing graph/support representations.
2. Independently implement augmenting-path residual networks and compare
   cut minima to brute-force cube energy minima for 600 generated integer
   attractive energies on dimensions 0-7. All 19,125 state-wise residual
   identities, exact base-two local factor products, and nondegenerate
   normalization bounds pass. Each resulting probability table is tested
   against every MTP2 pair.
3. Independently enumerate the C4 counterexample's MTP2 pairs, graph
   separations, conditional-independence identities, and all clique
   projection balances. Confirm exact unequal products above.
4. Recheck source-first controls: thin equality supports separate global
   from full-conditioning pairwise Markov; complementary three-bit atoms
   defeat adjacent-square-only MTP2 tests; adding a constant to product
   weights (2,4,1,2) destroys MTP2.
5. Include equality-block weights with original couplings -3 and +5 so
   the aggregate +2 is MTP2 despite a negative individual coefficient.
6. Include the antiferromagnetic K3 boundary support containing its six
   nonconstant states. It is a limit of ordinary positive edge models but
   cannot be edge-factorized, since every edge projection is full. It
   fails MTP2, isolating the role of attraction in the closure mechanism.

Independent-control SHA256:
`c7107a16077b2af89a7c094bb4c7f358321548f6e85f4f75bce65b5dab9c2e69`.
Result JSON SHA256:
`1f302ead79a4bde6f89fc48526d7b813ce796e700fd8d9f07c6d50137a1fd720`.

The finite controls validate boundary behavior and implementation of proof
mechanisms, not the all-graph quantifiers. The proof arguments above supply
those quantifiers independently of the tested range.

## Exact remaining gap and next authorized stage

No mathematical gap remains in this family's verification of the released
prose for the original finite binary two-conjecture target. Remaining audit
work is candidate checker/source-consistency inspection after an explicit
code release. Priority, literature exhaustiveness, repository readiness,
and editorial integration are outside this family's present certification.
Best-guess completion of this family's full audit at this checkpoint: **85%**.
