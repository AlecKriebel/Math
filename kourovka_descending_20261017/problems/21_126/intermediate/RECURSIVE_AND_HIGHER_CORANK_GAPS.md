# Remaining mechanisms: recursive scales and higher-corank kernels

October 24, 2026 UTC. Research attempt record. No intermediate RAAG subgroup is constructed.

## A scale recursion with the right growth, but no group realization

The exact recurrence T(2^k)=2^k T(2^(k−1)), T(1)=1, produces T(2^k)=2^(k(k+1)/2). Its monotone extension is superpolynomial and subexponential, as proved in POSITIVE_TRANSITION_DICHOTOMY.md. Thus a finite recursive rule is not by itself an obstruction to intermediate behavior.

Attempted group mechanism: recursively build disks whose boundary length doubles at stage k while the unavoidable filling cost multiplies by roughly 2^k. To turn this into a witness one needs **both** that every filling of a chosen null word incurs this recursive cost, and that arbitrary null words admit a global upper bound on the same subexponential scale. Producing one recursively expensive diagram supplies neither condition: it may have a much cheaper alternative filling, and unrelated words may require exponential fillings. An injection into a RAAG is a separate requirement.

A common shortcut would encode scale changes with a stable letter conjugating a cyclic clock x to a proper power x^q. This is not a viable RAAG mechanism. In a RAAG, a cyclically reduced conjugate u of a nontrivial element g has |u^n|=n|u| in standard normal form. Hence stable translation length τ(g)=lim |g^n|/n is positive, conjugacy invariant, and satisfies τ(g^q)=|q|τ(g). Conjugacy of g and g^q therefore forces |q|=1. In particular Baumslag–Solitar scaling with |q|>1 cannot embed faithfully with nontrivial clock x. This is a standard RAAG normal-form consequence, not a new theorem.

Even before considering embeddings, assigning a cyclic clock a superlinear **minimal** intrinsic cost cannot work in a finitely generated group: if x has finite generator length L, then |x^k|≤L|k| by repetition. In a finitely generated subgroup of a RAAG there is also a linear lower bound, because ambient stable translation length is positive and the subgroup generators have bounded ambient lengths. Thus every nontrivial cyclic subgroup is undistorted in that subgroup. A valid delayed-scale mechanism must use more than changing the word metric of powers of one fixed element.

Status: blocked for the simple cyclic-clock implementation. Reopen only with a noncyclic recursive mechanism, an actual injection, and independent filling lower/upper proofs. The existence of the intermediate numerical recurrence is not evidence that these missing claims hold.

## Why the rank-one induction does not automatically cover higher corank

POLYNOMIAL_ARTIN_KERNELS.md concerns φ:A(Γ)→Z. At its start all living vertices form a simply connected flag complex, so the nonzero-weight kernel is a finitely presented polynomial base. A general map A(Γ)→Z^m does not come with that rank-one base or with a height-one cyclic transversal. Intersecting m kernels is not a valid use of the theorem, because the second restricted character is defined on an Artin kernel, which need not itself be a RAAG.

Nor can one assume a high-rank coabelian quotient splits over a clique. There is an explicit finiteness countermodel to that structural assumption. For m≥4, take

    A=F_m×F_m×F_m,
    Φ(g_1,g_2,g_3)=ab(g_1)+ab(g_2)+ab(g_3) ∈Z^m,
    N=ker Φ,

where each factor abelianization uses the same standard Z^m basis. Then N is finitely presented, yet Φ has no group-theoretic section Z^m→A.

Finite presentation: apply the primary Bieri–Renz criterion stated as Theorem 2.1(i) in Meier–Meinert–VanWyk (1998), together with that paper's Main Theorem. For every nonzero real character λ:Z^m→R, each of the three free factors has at least one generator with λ∘ab≠0. Therefore the living flag complex is the join of three nonempty discrete sets. That join is simply connected: the join of the first two sets is a connected graph, and joining with the third nonempty set is a union of cones on that connected graph, whose cone intersections are connected; van Kampen gives trivial fundamental group. A living set consisting of one vertex also causes no exception, since it makes a cone. The living link at a dead vertex is the join of the other two nonempty sets and is connected. Every dead-dead edge joins different factors and has a living neighbor in the third factor. The exact n=2 link criterion therefore holds for every λ, so S(A,N)⊂Σ²(A), and N is of type F₂.

Nonsplitting: any abelian subgroup of A projects to an abelian subgroup of each free factor, hence to a cyclic subgroup of that factor. Its three coordinate maps jointly inject it into a product of three cyclic groups. Thus A has no free abelian subgroup of rank greater than three. A section would embed Z^m with m≥4, a contradiction.

This example only disproves a proposed universal splitting reduction. It is not an intermediate-Dehn candidate; the 2024 uniform polynomial bound for finitely presented subgroups of three free factors applies to N. A more general higher-corank kernel route would need fresh filling arguments and cannot be inferred from the rank-one induction or from this lack of splitting.

## No promotion

At present there is no finite presentation plus RAAG injection with the required intermediate filling scale. The strongest derived result in this family is a polynomial upper bound for rank-one Artin kernels, pending the fresh full-theorem audit. No solution of either branch of 21.126 and no originality claim is made.
