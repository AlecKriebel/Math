# Independent support and restricted-design closure derivation

This is an audit derivation, not a publication or a priority claim. Its mechanism was frozen in INDEPENDENT_SOURCE_CRITERIA.md before any candidate proof was read. The present file spells out its assumptions and the exact gap it avoids. It applies to finite binary variables; a nonbinary generalization is not asserted.

## 1. Binary sublattice representation

Let S be a nonempty subset of {0,1}^V closed under meet and join. Its bottom b and top t belong to S. A coordinate is free when b_i=0 and t_i=1; other coordinates are pinned. For each free i, define m_i as the meet of all s in S with s_i=1. Define i=>j for free coordinates when (m_i)_j=1, equivalently s_i<=s_j for every s in S.

Then
S={x in [b,t]: x_i<=x_j for every implication i=>j}.
The forward inclusion is immediate. For the reverse, each m_i with x_i=1 is at most x by the implication constraints and pinned coordinates. The join of b and those m_i is a support point and equals x coordinate by coordinate: every x_i=1 free coordinate appears in its own m_i, and no zero coordinate is introduced. If no free coordinate is 1, the join is b.

The implication relation is reflexive and transitive. Mutual implication partitions free coordinates into equality classes. The quotient is a finite partial order, where U=>W means activating U forces W. Covers generate all its strict implications.

## 2. A global Markov support must realize these constraints on G

Let p have support exactly S, with p(x)>0 for every x in S, and assume full global Markov with respect to finite G. No MTP2 assumption on the weights is needed in this section; the lattice assumption on support is explicit.

For free j, let n_j be the join of all support states with j=0. For free k,
(n_j)_k=0 iff k=>j.
Indeed, n_j has k=1 precisely when some support state has k=1,j=0. For i=>j, let l=n_j and h=n_j join m_i. They are support points, agree outside
D={k free: i=>k=>j},
and differ exactly by l_k=0,h_k=1 for k in D. This follows by combining (m_i)_k=1 iff i=>k with the displayed identity for n_j. Pinned coordinates agree automatically.

If some C=V minus D separates sets A,B partitioning D, then conditional independence plus the positive l and h atoms forces the mixed state h on A, l on B, and their common C assignment into S. Its conditional marginal events both have positive probability; the CI product therefore gives a positive joint event. Since A,B,C partition V, that event is a single full state. This argument uses full global Markov, not potentially vacuous pairwise conditions.

**Equality classes are connected in G.** Suppose a free equality class K has disconnected induced graph. Choose i,j in distinct components. Their implication interval D is exactly K. Let A be the component containing i, B=K minus A, C=V minus K. The graph separation is valid, but its forced mixed state has i=1,j=0 despite mutual implication. Contradiction.

**Every cover has a graph edge.** If U=>W is a cover between distinct classes, take i in U and j in W; then D=U union W. If no original G edge joins the two classes, C=V minus D separates A=U and B=W. The forced mixed state again has i=1,j=0, contradicting i=>j.

Choose a connected set of equality edges in each class, and one G edge across every cover. Equality edges enforce common values inside each class. A cover edge has projected support {00,01,11} in the direction U=>W: 00/11 occur at bottom/top, 10 is forbidden, and 01 occurs because the reverse implication fails. Thus these edge constraints enforce every implication by transitivity. Together with unary pins they describe S exactly. Since S satisfies every unary and edge projection condition, adding the remaining projection constraints leaves S unchanged:

S={x: x_i occurs in S_i for every i; x_e occurs in S_e for every e in E}.

Important limitation: this theorem describes support only. It does not claim that arbitrary positive weights on S have a graph log-factor representation. The independent C4/C6 MTP2 globally Markov examples fail the corresponding weight-design condition.

## 3. Restricted design-space closure

Let p_n be normalized nonnegative unary-and-edge factorizing mass functions on the same finite binary graph, all MTP2, with p_n tending pointwise to p. Factorization implies global Markov even with zeros: conditioning at a positive assignment leaves independent graph components, and their finite normalizers separate. Every finite conditional independence is the polynomial relation
p_ABC(a,b,c) p_C(c)=p_AC(a,c) p_BC(b,c).
All marginal sums are finite, so the relation survives pointwise limits. The finite MTP2 polynomial inequalities also survive. Thus p is globally Markov and MTP2, and S=supp(p) is a nonempty sublattice.

Let A_S be the fixed design matrix whose rows are x in S and whose columns are the unary/edge cells occurring in S, with entries 1 when that cell occurs in the row and 0 otherwise. Because S is finite and each p(x)>0, all p_n(x) are positive on S for every sufficiently large n. Every involved factor cell is then positive; for real source factors use its nonzero absolute value. Taking finite logarithms on S gives
log(p_n)|S in column(A_S).
The same remains true if a normalizing constant is present: a constant column is supplied by the sum of the two cells at any unary coordinate; the empty-V case is the singleton law.

Column(A_S) is a finite-dimensional linear subspace and hence closed. Since log(p_n(x)) tends to log(p(x)) at each x in S,
log(p)|S=A_S lambda
for some finite real lambda. Set the corresponding occurring local factors to exp(lambda), and every nonoccurring cell to zero. On S this reproduces p. Off S at least one unary/edge projection fails by Section 2, so the product is zero. The resulting finite nonnegative local factors therefore give exact factorization of p, proving pointwise closure of the unary-and-edge MTP2 class.

## 4. Literal edge-only source convention

For E nonempty, let I0 be the isolated vertices. A literal edge product is constant in x_I0, so every p_n and its limit equal a fixed uniform factor 2^(-|I0|) times a density on nonisolated vertices. Restrict to those vertices. Every pin there has an incident edge, so unary support conditions are already encoded in edge projection conditions. The argument in Section 3 uses only edge columns, because the approximating p_n are literal edge products. It then supplies exact edge factors, including any needed scalar normalization, on the nonisolated graph. Reattach the uniform isolated factor and absorb its scalar into any existing edge. This proves the literal source closure claim.

If E is empty and V nonempty, the literal empty product is 1 everywhere, so there are no normalized laws in that displayed family; closure is trivial. For V empty there is one state and one law. If a tacit scalar normalization is allowed for an edgeless graph, the literal edge model is instead the singleton uniform law, also closed.

## 5. Exact assumptions and checkable conclusion

Assumptions: finite V; binary product cube; simple undirected G; full graph-separation Markov property; coordinate meet/join lattice support; finite real local factors; pointwise convergence of normalized mass functions. No positivity off S, faithfulness, generic graph, support-connectivity hypothesis, or min-cut machinery is assumed.

Conclusion: the original edge-MTP2 intersection is pointwise closed. The broader lattice-support factorization claim is not proved and is false: its weights need not lie in the restricted graph-design column space. This derivation does not prove the candidate's stronger attractive-approximation characterization, whose direct prose proof was audited separately. Priority and nonbinary extensions remain unassessed.
