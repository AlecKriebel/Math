# Turn1: exact optimality and a sharp nontrivial-information criterion

AI-assisted mathematical proof attempt, independent review pending. This resolves the exact marginal-optimality subquestion and the source's literal proper-containment criterion; quantitative geometric smallness remains separate. Forward/backward smoothing is credited prior mathematics (SOURCE_GATE).

Let S be any set, f:S→S any function, T≥0, and P_0,...,P_T subsets. No topology or measurability is needed. Define the source's forward A_0=P_0, A_t=f(A_(t−1))∩P_t, backward B_T=P_T, B_t=P_t∩f^(-1)(B_(t+1)), and Q_t=A_t∩B_t.

## Exact feasible marginal
Let C be the set of all tuples (x_0,...,x_T) with x_j∈P_j and x_(j+1)=f(x_j). Then
Q_t={x_t:(x_0,...,x_T)∈C}.

Proof. Induction identifies A_t as precisely the endpoints of admissible prefixes through time t. Backward induction identifies B_t as the starts of admissible suffixes from t. Every full trajectory gives membership in both. Conversely, an x in their intersection has one admissible prefix ending at x and one admissible suffix beginning at x. Concatenating at that identical state gives a full trajectory. Finite existence, not an infinite inverse-branch choice or invertibility assumption, suffices.

Therefore any guaranteed state enclosure based solely on these exact observations and f must contain Q_t: every point in Q_t is realized by some indistinguishable full trajectory. This proves marginal “finest” optimality. It does not say arbitrary points chosen independently from different Q_t can be combined into one trajectory. For example f=identity and P_0=P_1={0,1} have Q_0=Q_1={0,1}, but (0,1) is not feasible.

Equivalently C is parameterized by z∈intersection_(j=0)^T f^(-j)(P_j), with x_t=f^t(z). This is an exact characterization, not a promise that images/preimages are efficiently computable for an arbitrary presented map.

## When is there literally any extra information?
Assume the observed word is realizable, so C≠empty. Then
[Q_t=P_t for every0≤t≤T] iff [f(P_t)=P_(t+1) for every0≤t<T].

For the forward implication, every x∈P_t is the t-th state of a full trajectory, hence f(x)∈P_(t+1). Every y∈P_(t+1) has a full trajectory and therefore a predecessor in P_t. These give the two inclusions. Conversely the equalities f(P_t)=P_(t+1) make all forward sets A_t=P_t and all backward sets B_t=P_t by induction. The T=0 case is the empty conjunction, correctly giving no dynamic information.

Thus at least one Q_t is a proper subset of P_t exactly when at least one adjacent equality fails. This is a necessary-and-sufficient condition on f relative to the observed cells, not a hyperbolicity assumption or a uniform diameter estimate. Points of P_t whose images leave X are legitimately excluded if the actual trajectory was observed to remain in X. No forward-invariance hypothesis was added.

## Relation to the primary smoothing theorem and remaining work
In Li–Cong–Zhou–Dong Theorem1 take process/measurement noises to have singleton ranges, initial range X and measurement equal to the cell index. The non-stochastic independence conditions become automatic. The filtered range is A_t, and their optimal backward recursion is A_t∩f^(-1)(smoothed_(t+1)). The displayed gluing proof identifies it with the source's A_t∩B_t for measurable source data; the purely set-theoretic proof also covers arbitrary subsets/maps. Their theorem and classical chain-consistency reasoning are credited; no novelty claim.

Proper containment alone can remove one point and leave diameter unchanged. Nor does a finite partition provide a universal numerical scale of smallness. The following turns investigate genuine geometric conditions and the boundary/uniformity obstacles rather than relabeling this exact optimality as an all-purpose quantitative solution.
