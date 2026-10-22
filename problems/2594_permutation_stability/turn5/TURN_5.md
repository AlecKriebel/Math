# Turn 5: deletion-location transport and the fractional matching obstruction

**2594 / KOU-21.85. Fifth and final substantive author turn: 5/5. Original implication remains unresolved. No further author search follows this freeze.**

The final mechanism exploits freedom to choose the deleted set and reformulates the residual finite problem as an exact injection-matching problem. It identifies why a natural convex relaxation loses the needed cardinality information. These reductions do not prove the remaining vanishing modulus or produce a fixed counterexample group.

## 1. Moving the deleted set costs at most three discrepancies per exchanged point

Let p be a permutation of a finite Y. Let X,Z⊂Y have the same positive cardinality n and put I=X∩Z, d=|X\Z|=|Z\X|. Let θ:X→Z be any bijection fixing I. Then

    |{x∈X : c_X(p)x ≠ θ⁻¹ c_Z(p)θ(x)}| ≤ 3d.             (1)

**Proof.** At most d starting points lie outside I. If I is empty the bound is immediate, so suppose I≠∅. For each x∈I, follow its p-cycle up to the next return to I. If that segment has no interior point in X△Z, both compressed maps first return to the same I-point, and θ fixes source and target. Every other exceptional starting point in I has an interior marked point from X△Z on its segment. The segments' interiors are disjoint for different x∈I, including when there are several p-cycles. Thus at most |X△Z|=2d such starting points occur. Add the d points outside I. ∎

The constant 3 is sharp for comparison of these transported compressed permutations. Take Y={0,1,2,3,4}, p=(0 3 1 4 2), X={0,1,2,3}, Z={0,1,2,4}, and θ fixing 0,1,2 while sending 3 to 4. The maps on X disagree at exactly 0,1,3. This sharpness statement concerns (1), not the minimum distance to an arbitrary repairing group action.

For a fixed genuine action ρ:G→Sym(Y), define

    R_ρ(X)=min_{τ:G→Sym(X)} max_{s∈S} d_X(c_X(ρ(s)),τ(s)).

Conjugating candidate actions by θ and using (1) gives

    |R_ρ(X)−R_ρ(Z)| ≤ 3d/n.                                (2)

If |Y|=n+k, then d≤k. Therefore choosing the most favorable k-point puncture rather than the least favorable changes the repair distance by at most 3k/n. A vanishing-deletion obstruction cannot be explained by a uniquely unlucky location of the deleted points.

In particular, define a best-location transitive modulus U_{G,S}(δ) as follows: for each transitive finite ρ on Y and each integer 0≤k<|Y| with k/(|Y|−k)≤δ, first minimize R_ρ(X) over subsets X of cardinality |Y|−k, then take the supremum over ρ,k. The transitive modulus T from Turn 3 instead takes the supremum over such subsets. Equation (2) yields

    U(δ)≤T(δ)≤U(δ)+3δ.                                    (3)

Consequently U and T vanish at zero simultaneously. This is location freedom, not existence of a good puncture.

## 2. A finite injection-matching formulation

Let ρ:G→Sym(Y), |Y|=M, and 1≤n<M. Define E_ρ(n) by minimizing

    max_{s∈S} (1/n)|{w∈W : ρ(s)j(w)≠j(τ(s)w)}|           (4)

over all genuine G-actions τ on a set W of cardinality n and all injections j:W→Y. The finite generating set S ensures that there are finitely many such actions on a fixed W=[n], and there are finitely many injections, so the minimum is attained. No assumption of transitivity is needed for this definition.

For every X⊂Y of size n, putting k=M−n,

    E_ρ(n) ≤ R_ρ(X)+k/n,
    R_ρ(X) ≤ E_ρ(n)+2k/n.                                  (5)

**First inequality.** Use a minimizing action τ on X and the inclusion j. The difference between ρ(s)|X and c_X(ρ(s)) affects at most k inputs. The raw intertwining error is therefore at most nR_ρ(X)+k.

**Second inequality.** Choose a minimizing injection j and transport its action to Z=j(W). Let τ_Z be the resulting action and I=X∩Z. Choose θ:X→Z fixing I, and transport τ_Z to an action τ_X on X. Write d=|X\Z|≤k. For a fixed s, an x∈I causes no discrepancy between τ_X(s) and c_X(ρ(s)) if both

    ρ(s)x=τ_Z(s)x   and   τ_Z(s)x∈I.

At most nE_ρ(n) points violate the first condition. At most d points of I map under τ_Z(s) into Z\I, since τ_Z(s) is a permutation. There are at most d additional starting points outside I. Hence the raw error is at most nE_ρ(n)+2d≤nE_ρ(n)+2k. ∎

Thus the residual transitive problem can equivalently be formulated without choosing a deleted subset in advance: find an exact action on n slightly fewer points and an injection into the original orbit whose generator equivariance defect tends to zero. The injection and the action must both be integral, genuine finite objects.

Combining (3)–(5) with previous turns, the original implication for flexibly stable groups would follow from a uniform vanishing bound for these integral matching defects on their transitive finite actions. No such general bound has been proved here.

## 3. The standard fractional relaxation has zero cost in every instance

Write an injection j:W→Y as an M×n matrix B, with B_{y,w}=1 if y=j(w) and 0 otherwise. Each column sum is 1, each row sum is at most 1, and distinct columns have disjoint supports. With permutation matrices P_ρ(s),P_τ(s),

    |{w : ρ(s)j(w)≠j(τ(s)w)}|
        = (1/2)||P_ρ(s)B−B P_τ(s)||_F².                  (6)

Each mismatching column is the difference of two distinct standard basis vectors and contributes 2; a matching column contributes zero.

Dropping the zero-one requirement and merely asking for B≥0, column sums 1 and row sums ≤1 destroys this obstruction completely. The constant matrix

    B_{y,w}=1/M

is always feasible because its row sums are n/M≤1. It satisfies

    P_ρ(g)B=B=B P_τ(g)   for every g∈G,

for **every pair** of genuine actions. Thus the relaxed intertwining objective is identically zero, including when the integral optimum in (4) is bounded away from zero.

The matching polytope having integral vertices does not rescue a convex residual minimization: a convex function can attain its minimum at a nonvertex. Adding the nonlinear constraint BᵀB=I_n would restore injection matrices under nonnegativity and the column-sum constraints. Indeed, in each nonnegative column with sum 1, squared norm 1 forces one entry to be 1 and the others zero; orthogonality forces different occupied rows. But this reintroduces the nonconvex integral obstruction instead of solving it.

## 4. An exact finite-instance integrality gap, with changing domain groups

Let p≥3 be prime, let G_p=C_p, and let ρ_p be its regular p-cycle action on Y=[p]. Take n=p−1.

Every genuine C_p-action on n points is trivial: every cycle of the generator has length dividing p, and a p-cycle cannot fit on fewer than p points. Therefore, for every injection j and every w,

    ρ_p(t)j(w)≠j(w)=j(τ(t)w).

It follows that

    E_{ρ_p}(p−1)=1,

whereas the fractional optimum from Section 3 is zero. Also every compression of the generator to p−1 points is a (p−1)-cycle, so R_{ρ_p}(X)=1 when p≥3.

Although the deletion ratio 1/(p−1) tends to zero, **this is not a counterexample to KOU-21.85**: the group G_p varies with p. For each fixed finite group C_p, strict permutation stability is known, and the obstruction above lives at one bounded degree for that fixed group. If instead one takes many copies of its p-point orbit and deletes a vanishing proportion of points, the bounded-orbit repair estimate of Turn 1 applies. If one uses the single fixed group Z mapping onto these C_p, new smaller exact Z-actions are available and repair the puncture, as in Turn 1. Domain quantifiers cannot be exchanged.

This gap establishes only that the indicated fractional matching relaxation cannot be used to prove a dimension-uniform integral rounding theorem for arbitrary finite domain groups or arbitrary single finite action instances.

## 5. Exact finite certificates under a finite-presentation hypothesis

When a finite presentation G=⟨s₁,…,s_d | r₁,…,r_ℓ⟩ is supplied, along with the finite action ρ, E_ρ(n) is exactly computable in principle:

1. Enumerate every d-tuple of permutations of [n].
2. Keep exactly those tuples for which every supplied relator evaluates to the identity; these are precisely the genuine G-actions on [n].
3. Enumerate every injection [n]→Y.
4. Evaluate the integer discrepancy counts in (4) and take the finite minimum.

This is an exhaustive finite certificate scheme, with no polynomial-time claim. It must not be extended automatically to an arbitrary finitely generated group with unspecified or infinitely many relations: a bounded relator check can then admit false “actions”. Nor does a sequence of numerical minima establish a uniform asymptotic bound without an argument controlling all finite actions and dimensions.

The accompanying checker computes the prime-cyclic instances exactly at small primes, verifies every transported compression through five-point permutations and equal-cardinality subset pairs, verifies the sharp 3d example, and checks the injection-matrix and transport bounds. Its finite tests do not constitute the missing source-wide theorem.

## Final outcome after five substantive turns

The exact strongest structural reduction is now:

- within the flexible class, pass to the maximal residually finite quotient;
- if the target fails, a finitely generated residually finite nonamenable counterexample exists;
- its strict failure is witnessed by small deletions from transitive finite actions;
- the location of those deletions can be chosen optimally up to an asymptotically negligible cost;
- the remaining question is vanishing of an **integral** equivariant injection-matching defect on slightly smaller exact actions.

The packet proves conditional orbit/reservoir repair bounds and identifies spectral, replication, uniform-metric, and convex-relaxation failures. It does **not** establish that every flexibly stable group satisfies the final matching condition, and supplies **no fixed globally flexibly stable counterexample group**. Original status: **unsolved after 5/5**, subject to independent review of the scoped partial claims. The known amenable implication, classical spectral instability mechanism, and earlier results remain credited; no historical novelty or full solution is claimed.
