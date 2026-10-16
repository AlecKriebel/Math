# 10000046: four-dimensional prior progress; three-dimensional gap

**Outcome: unresolved as a combined target.** A directly relevant 2024 preprint gives the four-dimensional result. No three-dimensional solution is established here. The transport reduction below is a standard matching/compactness reformulation, not a new resolution. Model: gpt-6-astra, xhigh; checked2026-09-30.

## Exact target and scope

[Benjamini, *Coarse Geometry and Randomness*](https://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf), dated October30,2013, Open Problem12.33 on printed/PDF p104, asks for couplings of simple random walks in dimensions3 or4, starting distance10 apart, with positive probability of disjoint paths. The recovered [archived author PDF](https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf) was read in its section12 context.

Fix vertices \(x,y\in\mathbb Z^d\), \(\|x-y\|_1=10\), and the laws \(\mu_x,\mu_y\) of the complete walks, including time0. The desired coupling \(\pi\) must satisfy
\[
\pi\{X_i\ne Y_j\text{ for every }i,j\ge0\}>0.
\]
The source imposes no Markovian or co-adapted restriction on the coupling. Correct one-time distributions alone do not suffice: both complete marginal path laws must be those of simple random walk. Simultaneous avoidance \(X_n\ne Y_n\) is much weaker than this full-range condition.

## Corrected literature status

[Benjamini–Kozma, *Coupled but distant*](https://arxiv.org/abs/2412.16600v1), December21,2024, states the positive four-dimensional theorem on p2 and explicitly leaves dimension3 unresolved on p1. Its introduction specifies intersections at different times, and §1.2 includes the initial vertices in each trace. Although the introduction mentions neighbouring starts, the proof on pp17–18 begins with0 and an arbitrary fixed \(x\ne0\); thus the intended theorem includes distance10. The argument uses Hall matching and annular coupling, rather than providing a Markovian construction; p2 asks about Markovian couplings separately.

The full preprint and its TeX source were obtained; the theorem, matching construction and final induction were inspected. This is attribution to an existing preprint, not independent certification of every estimate. Literal typographical inconsistencies require care: Lemma8 says the exceptional events occur despite assuming their probabilities are small, and p17 prints a growing \(Cn_1^6\) where its preceding estimate requires \(C/n_1^6\). These observations neither supply a refutation nor constitute a complete repair audit.

No later solution of dimension3 was located in the bounded search. [Shi et al., *Intersection Exponents of Simple Random Walks in Two and Three Dimensions*](https://arxiv.org/abs/2609.25968), September2026, concerns independent-walk exponent estimates; its stated scope does not resolve unrestricted couplings. The upstream report missed the 2024 preprint, so retaining an undifferentiated “no progress found” status would be misleading.

## A precise finite-transport formulation

Let \(\mathcal P_N(x)\) be the \((2d)^N=L_N\) length-\(N\) walks from \(x\), and define \(\mathcal P_N(y)\) similarly. Join two paths in a bipartite graph exactly when their vertex ranges, including initial vertices, are disjoint. Write \(M_N\) for its maximum matching size and
\[
a_N=M_N/L_N.
\]

**Proposition.** The largest possible probability of disjoint infinite ranges among all couplings of \(\mu_x,\mu_y\) equals
\[
\alpha(x,y)=\lim_{N\to\infty}a_N=\inf_Na_N.
\tag{1}
\]

**Proof.** Every finite path has probability \(1/L_N\). Finite couplings are therefore doubly stochastic matrices after multiplication by \(L_N\). Decomposition into permutation matrices shows that the maximum mass on disjoint pairs is the maximum number of disjoint pairs in a permutation, divided by \(L_N\). A maximum matching can be completed arbitrarily to a permutation, so this value is \(a_N\).

Use increment sequences to identify each infinite path space with the compact space \(\{\pm e_1,\ldots,\pm e_d\}^{\mathbb N}\). Couplings with the prescribed marginals form a weakly compact set. Let \(R_N\) be disjointness through time\(N\); these sets are clopen and decrease to the full-disjointness event \(R\). The numbers \(a_N\) decrease, since any coupling through\(N+1\) restricts to one through\(N\). For each\(N\), extend an optimal finite coupling using independent random-walk tails. Choose a weakly convergent subsequence of the resulting infinite couplings, with limit \(\pi\). For fixed\(k\) and every sufficiently large index,
\[
\pi_N(R_k)\ge\pi_N(R_N)=a_N.
\]
Clopen continuity yields \(\pi(R_k)\ge\inf_Na_N\). Continuity from above gives the same lower bound for \(\pi(R)\). Conversely every coupling has \(\pi(R)\le a_N\) for each\(N\). This proves(1). \(\square\)

Equivalently, finite matching duality gives
\[
a_N=1-\frac1{L_N}\max_{A\subseteq\mathcal P_N(x)}
\bigl(|A|-|\mathcal N(A)|\bigr),
\tag{2}
\]
where \(\mathcal N(A)\) is the set of paths disjoint from at least one member of\(A\). A three-dimensional proof still needs a uniform positive lower bound in(1), or a proof that the limit is zero. Equations(1)–(2) do not evaluate that limit. Hall's theorem is already central to the cited four-dimensional work, so this route must not be promoted as a novel solution mechanism by itself.

## Exact checks and the remaining obstruction

For the actual distance10, synchronous translation \(Y_n=X_n+(y-x)\) makes the first\(N\) ranges disjoint whenever \(N<10\): a displacement between two points of one length-\(N\) nearest-neighbour path has graph distance at most\(N\). Consequently \(a_N=1\) for \(N\le9\). This supplies no infinite-time conclusion. In fact, for this same translation coupling, choose any fixed length10 increment word with displacement\(y-x\). Independent disjoint blocks of the increment sequence equal that word infinitely often almost surely. Each occurrence gives \(X_{10k+10}=Y_{10k}\), so full-range avoidance has probability zero.

Every coupling also satisfies
\[
\alpha(x,y)\le1-\mathbb P_x(T_y<\infty)<1,
\]
because visiting the other initial vertex already forces an intersection. If \(a_i=|y_i-x_i|\) and \(\sum_i a_i=10\), then
\[
\mathbb P_x(T_y\le10)=\frac{10!}{a_1!\cdots a_d!}(2d)^{-10},
\]
a strict, though small, finite-horizon upper obstruction.

The accompanying program checks exact finite matching/minimum-cover certificates in small dimension/horizon controls, the range-versus-simultaneous distinction, and the first-hit count. These diagnostics do not certify any uniform lower bound. The investigation stops after one substantive transport route: the central three-dimensional Hall-deficiency estimate remains unproved. The combined target stays unresolved, with credited four-dimensional prior progress.
