# Turn 3: no reduction whose Ramsey instances have finite global arity

Substantive author turn **3/5**. This turn tests a broad finitary coding strategy for the original reductions. It proves a complete negative result for that restricted strategy, including when the arity has no supplied bound. The full open-set problem permits unbounded arity and is not separated.

Say an open P⊆[N]^N has **finite global arity** if there is an integer m>=1 such that membership f∈P depends only on f's first m entries. The number m may depend on P. It is not required to be supplied, computable from the open name, or uniformly bounded over inputs. Only a positive open-set name is supplied; a negative/clopen name is not assumed.

Let R_fin be Sigma^0_1-RT restricted to this semantic class. Let A_fin be the corresponding restriction of promised avoidance A. Then

                  C_{N^N} not<=_W R_fin,
                  C_{N^N} not<=_W A_fin.                           (7)

Equivalently, neither original question can be solved by a preprocessing that always outputs a finite-global-arity open set. This is an ordinary-reduction obstruction, with the original tree available to the postprocessor.

## 1. From a positive open name to a finite-tuple coloring

Fix a name p for P of global arity m. For an increasing m-tuple τ, let c(τ)=1 iff every infinite extension of τ belongs to P. By the arity promise, this is equivalent to the existence of at least one extension in P. It is therefore equivalent to some enumerated basic cylinder [σ] having nonempty intersection with [τ]. Compatibility of two finite increasing prefixes is decidable.

Consequently c is a {0,1}-valued coloring computable from p', the ordinary Turing jump of the name. Explicitly p' decides whether the p-computable enumeration search finds such a σ. No uniform way to discover m has been used. Every infinite c-homogeneous set yields a homogeneous solution for P. If P also satisfies the avoidance promise, its color must be 0.

## 2. An elementary uniform arithmetical Ramsey bound

We prove a deliberately nonoptimal bound: for any oracle B, every B-computable finite coloring of [N]^r has a homogeneous sequence uniformly computable from B^{(2r)}, given r and a finite color bound. This uses only finite Turing jumps. The proof supplies the bound rather than relying on an unstated effective-Ramsey theorem.

For r=1, whether a color class is infinite is a Pi^0_2(B) question, decidable in B''. Choose the least infinite class and enumerate it. This is uniform in B''.

Assume r>1. Build an increasing sequence x_0,x_1,... and nested infinite reservoirs. At stage s choose x_s from the current reservoir and restrict to points above x_s. For each newly formed (r−1)-tuple τ among x_0,...,x_s, partition the current reservoir according to the finitely many values c(τ together with y), and retain the least infinite color class. There are only finitely many such refinements per stage. Each reservoir is described by a B-decidable predicate with finitely many numerical parameters and recorded color choices. Its infinitude is therefore uniformly Pi^0_2(B); B'' makes all choices and computes the entire sequence and color records.

For each (r−1)-tuple of indices i_1<...<i_{r−1}, record the color selected when the last indexed point was inserted. Every later x_j has that color with the corresponding tuple, since reservoirs remain nested. This defines a B''-computable coloring of [N]^{r−1}. By induction it has a homogeneous index sequence computable in

                 (B'')^{(2(r−1))}=B^{(2r)}.

The corresponding subsequence of the x_j is homogeneous for c: the first r−1 points of any r-tuple determine its recorded color, and the last point lies in the preserved reservoir. This completes the induction.

Combining with §1, P has a homogeneous solution computable in p^{(2m+1)}. For a computable p this is arithmetical. If m is only known to exist, this conclusion is nonuniform in m but still gives the existence of an arithmetical solution for each computable instance. That is exactly what the separation below requires; no uniform finite jump level for the whole class is claimed.

## 3. The classical hard Baire-choice instance

Use the credited classical Kleene theorem: there is a computable nonempty closed subset of Baire space with no hyperarithmetical point, equivalently a computable ill-founded tree with no hyperarithmetical path. The exact theorem is explicitly stated as Theorem3.5 in Kihara–Marcone–Pauly, *Searching for an analogue of ATR_0 in the Weihrauch lattice*, arXiv1812.01549v2 (2020), p.8, and yields their Corollary3.6. It is also the background for Marcone–Valenti's Corollary6.6. We use this established theorem as a credited dependency; we do not claim to reconstruct its higher-recursion proof or a finite certificate for it.

Suppose an ordinary reduction of C_{N^N} to R_fin were witnessed by computable forward and backward functionals. Apply it to a computable name of this fixed hard tree. The forward output is a computable open name p of a finite-global-arity P. By §2, there exists an arithmetical homogeneous solution h for P. Correctness for every allowed oracle output forces the backward functional, using only the computable input and h, to produce a path through the hard tree. Such a path is arithmetical, hence hyperarithmetical, a contradiction.

The same proof applies to A_fin: the promised domain guarantees that the arithmetical homogeneous solution is an allowed avoiding solution. This proves both parts of (7). It does not suffice to argue only that some other oracle solutions might be complicated; a Weihrauch reduction must also handle the low-complexity one.

## 4. Scope and consequence for further attempts

For the fixed hard computable Baire-choice instance, any successful reduction to either full target must output a computably open set with genuinely unbounded global arity. Merely letting a finite arity vary from input to input, concealing the bound, or withholding a negative open-set name does not avoid this obstruction.

This is not a separation for arbitrary computably open sets. Such sets can require unbounded initial segments and may have no hyperarithmetical homogeneous solutions; the primary literature explicitly supplies that phenomenon. The original two questions remain unresolved after three author turns. The finite-jump Ramsey reasoning and the hard-instance theorem are classical ingredients, not claimed as new literature results.
