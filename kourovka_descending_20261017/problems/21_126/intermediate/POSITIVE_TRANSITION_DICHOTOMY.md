# Constant finite positive transitions cannot supply an intermediate scale

October 24, 2026 UTC. Independently proved model obstruction; elementary and not claimed novel. **This is not a theorem about all Dehn functions, all finite recurrences, or all finite presentations.**

## Exact transition model

Let A be a fixed d×d matrix with entries in the nonnegative integers, and let b,c be nonnegative integral vectors. Regard A_ij as the number of distinct directed edges from i to j. Set

    C(n)=Σ_(k=0)^n b^T A^k c.

Thus C counts successful walks of length at most n, with the initial and terminal multiplicities prescribed by b,c. Remove every vertex that is not reachable from supp(b) or cannot reach supp(c); these vertices contribute zero to C. Call the resulting directed multigraph the trim graph T.

Exactly one of the following holds:

1. T is empty, and C≡0.
2. Every strongly connected component of T with a cycle is a single directed cycle, with edge multiplicities one. Then C(n)=Θ((n+1)^r) as n→∞, where r is the largest number of cyclic strongly connected components visited by any successful path in the condensation DAG. For r=0 this means C is eventually a positive constant.
3. Some strongly connected component has a vertex with at least two outgoing internal edges, counted with multiplicity. Then there are integers L≥1 and a≥0 such that C(n)≥2^floor((n−a)/L) for n≥a. There is also an exponential upper bound.

In particular C cannot have superpolynomial subexponential growth.

## Proof

Any nontrivial strongly connected component has internal outdegree at least one at every vertex. If each such outdegree equals one, strong connectivity forces exactly one directed cycle through all its vertices. For a singleton, distinguish the absence of a self-loop from exactly one self-loop and at least two parallel self-loops.

Suppose a component has a vertex v with two distinct outgoing internal edges. Follow each edge by an internal return path to v. This gives two nonempty closed walks W_1,W_2 whose first edges differ. Write their lengths p,q. The walks U=W_1^q and V=W_2^p both have length L=pq and remain distinct. Every binary word of length m in U,V gives a different length-mL walk at v, because fixed blocks have the same length and different first edges. Since T is trim, fixed successful entry and exit paths through v exist. If their total length is a, concatenation gives C(a+mL)≥2^m. Monotonicity proves the displayed bound. A fixed finite graph has at most exponentially many walks, proving the upper estimate.

Now suppose no such branching component exists. A walk visits a chain of strongly connected components without returning to one after leaving it. There are finitely many possible component chains and intercomponent edge choices. Within a cyclic component, after fixing its entry vertex and exit vertex (or final vertex), the walk consists of a unique partial traverse of length less than the cycle length, preceded by a nonnegative number of full circuits. Consequently every successful walk is described by one of finitely many skeletons, together with loop counts ℓ_1,…,ℓ_s≥0, where s≤r. If the cycle lengths are d_i, its length is a_skel+Σd_iℓ_i. Thus there are at most K(n+1)^r walks of length at most n. Initial and terminal multiplicities only change K.

Conversely choose a successful skeleton visiting r cyclic components. If r>0, let D be the largest of its cycle lengths and choose each ℓ_i between zero and floor((n−a_skel)/(rD)). This gives Θ(n^r) different walks of length at most n. If r=0, at least one successful walk exists and the total number is positive and finite. This proves all cases.

## Application to positive substitutions — and its strict limit

For one fixed substitution σ on a finite alphabet, including erasing substitutions, counts of letters in σ^k(w) are powers of a fixed nonnegative integer incidence matrix. Hence the cumulative number of output letters through time n has the dichotomy above. The maximal output length M(n)=max_(0≤k≤n)|σ^k(w)| satisfies

    C(n)/(n+1) ≤ M(n) ≤ C(n),

so it too is either polynomially bounded or bounded below exponentially. A proposed group construction whose filling function is actually proved coarsely equivalent to such an M cannot answer the intermediate branch.

The comparison with a group's Dehn function is an extra hypothesis. Incidence counts can ignore free cancellation, make noninjective substitutions, or measure only lengths and distortion. None of these counts alone proves an intrinsic Dehn lower bound. Nor does the argument cover arbitrary products chosen from several matrices merely by summing their entries: the sum counts all choices, whereas the desired quantity may be a maximum. For instance two identity transition matrices have exponentially many choice words but constant maximal product norm.

For completeness, a narrower multitransition class still has a direct polynomial bound. If every allowed matrix is I+N with N strictly upper triangular in a common fixed basis, and every strict upper triangular entry satisfies 0≤N_ij≤M, then a product of n such matrices expands as a sum of products of at most d−1 strict upper triangular factors. Each entry is bounded by

    Σ_(j=0)^(d−1) binom(n,j) d^(j−1) M^j

(with the j=0 term interpreted as 1). This is O(n^(d−1)). The reason is that a product of d strict upper triangular d×d matrices vanishes, even if the factors differ. This model cannot create an intermediate scale either. No claim is made for unrestricted switching matrices.

## A genuinely intermediate finite recurrence remains possible

One must not conclude that finite descriptions force this dichotomy. The recurrence

    T(1)=1,   T(2^k)=2^k T(2^(k−1))

has the exact solution

    T(2^k)=2^(k(k+1)/2).

Its monotone extension T(n)=T(2^floor(log_2 n)) is superpolynomial and subexponential. Indeed, for 2^k≤n<2^(k+1), we have log T(n)/log n≥k/2→∞, whereas log T(n)/n≤k(k+1)log(2)/(2·2^k)→0. A finite recurrence with scale-dependent multiplication therefore escapes the constant-transition proof. Such a recursion remains a possible target mechanism for group diagrams. The missing work is a finite presentation, a rigorous lower bound for every filling rather than one recursively produced filling, a subexponential global upper bound, and an actual RAAG injection. None is supplied by writing the recurrence.
