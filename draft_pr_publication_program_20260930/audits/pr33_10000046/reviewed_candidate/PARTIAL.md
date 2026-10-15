# 10000046: verified finite transport partial; three-dimensional gap

**Outcome: unsolved.** The standard finite transport and compactness reformulation and the elementary bounds below are verified. They do not decide the three-dimensional question. A 2024 preprint states the intended four-dimensional result, but this package does not certify its complete proof. No novel resolution, paper or DOI is claimed.

## Exact target and scope

[Benjamini, *Coarse Geometry and Randomness*](https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf), dated October 30, 2013, Open Problem 12.33 on printed/PDF p.104, asks about couplings of simple random walks in dimensions 3 or 4, starting at graph distance 10, with positive probability of disjoint paths. Page 5 defines nearest-neighbour simple random walk and graph distance. The recovered archived author PDF and rendered question were checked. This package records separate dimension-3 and dimension-4 components and treats every pair of starts at lattice distance ten; the latter is an explicit stronger interpretation of the terse question.

Fix x,y in Z^d with l1 distance ten, and the laws mu_x,mu_y of the complete walks, including time zero. The desired coupling must give strictly positive probability to X_i != Y_j for **every** i,j >= 0. Both entire marginal path laws must have iid uniform nearest-neighbour increments. Correct one-time distributions alone do not suffice. Simultaneous avoidance X_n != Y_n is weaker than the full-range condition. No joint Markovian or co-adapted restriction is imposed by the source.

## Current literature qualification

[Benjamini–Kozma, *Coupled but distant*](https://arxiv.org/abs/2412.16600v1), December 21, 2024, states a positive four-dimensional theorem on p.2 and leaves dimension three unresolved in its introduction. Its definitions include initial vertices and intersections at unequal times, and its final proof writes a fixed nonzero starting displacement. It uses Hall matching and annular coupling. These are statements and proof intentions of that preprint, not a complete proof certificate supplied here.

The independent probability audit read the complete main proof and appendix against the freshly retrieved v1 PDF and TeX. It found more literal auxiliary-statement errors than the original package listed: reversed exceptional-event polarity, the wrong alphabet normalization, omitted path losses and strict Hall margins, singular good-time kernels at returns, undefined or overrun near-exit times, negative spatial-logarithm bounds, temporal multiplicity in a trace count, boundary conventions and conditioning issues. The conditional Hall repair and averaged final recursion check out **assuming** corrected quantitative lemmas and initialization. Corrected good-time/rare-hittability estimates (Lemmas 5/6), the old-prefix estimate (Lemma 9), and the required arbitrary-fixed-start initialization remain unverified here. These gaps do not refute the intended theorem; they prevent an unqualified assertion that this audit has established the four-dimensional result.

[Lawler–Limic, *Random Walk: A Modern Introduction*](https://math.uchicago.edu/~lawler/srwbook10.pdf), Theorem 4.3.1, Lemma 6.3.7 and Theorem 6.3.9, supports the regularized Green/hitting and exterior-boundary estimates with its stated hypotheses. That book is different from Lawler's *Intersections of Random Walks*, cited by the preprint for initialization. Neither the conditional repair nor this source check supplies the missing full quantitative certificate. See CURRENT_SOURCE_QUALIFICATION.md and the closed probability audit for exact locations and distinctions.

The bounded search did not locate a verified three-dimensional solution. [Shi et al., *Intersection Exponents of Simple Random Walks in Two and Three Dimensions*](https://arxiv.org/abs/2609.25968v1), September 2026, studies independent-walk numerical exponents, not unrestricted couplings. Its computations are not certified by this package. The upstream OPEN-TRIAGE report is retained as historical source metadata; it missed the 2024 preprint and is not evidence that all dimensions have no prior progress or that worldwide current openness has been proved.

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

The accompanying program checks exact finite matching/minimum-cover certificates in small dimension/horizon controls, the range-versus-simultaneous distinction, and the first-hit count. These diagnostics do not certify any uniform lower bound. The investigation stops after one substantive transport route: the central three-dimensional Hall-deficiency estimate remains unproved. The combined target stays unresolved. The four-dimensional preprint is credited for its stated intended theorem; a complete independently checked proof, including corrected quantitative estimates and initialization for arbitrary fixed starts, is not supplied by this package.
