# Turn 4: reduction to maximal lattices

AI-assisted proof attempt; independent review pending. Original unresolved.

This turn isolates where a failure would have to occur. Throughout G is a fixed connected higher-rank simple linear real Lie group with finite center.

## Maximal reduction theorem
The source conjecture for all lattices in G is equivalent to the same assertion restricted to maximal lattices.

Every lattice Γ lies in a maximal lattice Λ. Indeed any strict lattice overgroup has finite index at least2, and covolume divides by that index. Kazhdan–Margulis gives a positive lower bound c_G for lattice covolumes, so an ascending chain starting at Γ has length at most log_2(v(Γ)/c_G). Successively choosing a proper overgroup must terminate.

For finite index n=[Λ:Γ], Schreier's elementary generator bound yields d(Γ)−1≤n(d(Λ)−1). Since v(Γ)=n v(Λ),
(d(Γ)−1)/v(Γ)≤(d(Λ)−1)/v(Λ).
This inequality alone does not resolve sequences lying ever deeper inside a fixed maximal lattice: the right side then is constant. That case needs the independent turn1 deduction from FMW.

Suppose now the maximal-lattice conjecture holds, but there were Γ_i with v(Γ_i)→infinity and normalized ranks at least ε>0. Choose maximal Λ_i containing them. If the volumes v(Λ_i) are unbounded along this bad sequence, pass to a subsequence tending to infinity and use the displayed inequality, a contradiction. Otherwise pass to an infinite bounded-volume subsequence. Wang's finiteness theorem supplies only finitely many conjugacy classes of such Λ_i. After a further subsequence and conjugation all Γ_i are finite-index subgroups of one fixed Λ. Turn1 gives their normalized ranks tending to0, again a contradiction. The reverse implication is immediate.

Primary statement of the classical Wang input: Gelander–Levit, Local rigidity of uniform lattices, Comment.Math.Helv.93(2018),781–827, printed784 and Section10, https://ems.press/content/serial-article-files/43480 . Its hypotheses exclude factors locally isomorphic to SL_2(R) or SL_2(C); higher real rank simple G satisfies that exclusion. The theorem is used as a credited input, not reproved here. Schreier, Kazhdan–Margulis and FMW are likewise credited.

## Location of any counterexample sequence
Any sequence contradicting the source conjecture would therefore yield maximal lattices of volumes tending to infinity with normalized rank bounded away from0. By the prior nonuniform theorem, infinitely many of these must be cocompact. By turn1 their minimal torsion-free subgroup indices cannot remain bounded. By turn2 they cannot admit the displayed arithmetic models with both uniformly bounded field degree and representation dimension. These are necessary features of a hypothetical counterexample; none constructs one.

This reduction does not bound ranks of maximal arithmetic lattices. Counting maximal lattices or bounding their finite-index covers is not a replacement for that missing estimate.
