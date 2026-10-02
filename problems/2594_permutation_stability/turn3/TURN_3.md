# Turn 3: orbit balancing and reduction to transitive deletion

**2594 / KOU-21.85. Substantive author turn 3/5. Original implication remains unresolved.**

This turn improves the naive untouched-orbit method. An orbit used to absorb a cardinality defect need not contain any deleted point: old and new labels can be exchanged. It then proves that only transitive genuine finite actions need be tested for the deletion modulus of Turn 1.

## 1. Discarding an arbitrary invariant reservoir

Let ρ:G→Sym(Y) be a genuine finite action, X⊂Y nonempty, B=Y\X, |X|=n and |B|=k. Choose any invariant subset U⊂Y of size D≥k. Unlike the intact-core construction, there is no assumption B⊂U.

Introduce a fresh set T of D−k points and define

    V=(Y\U) ⊔ T,

with G acting by ρ on Y\U and trivially on T. Then |V|=n. Put I=X\U, which is the intersection of X and Y\U, and choose a bijection θ:X→V fixing I. Such a bijection exists because the complements both have cardinality D−|B∩U|:

    |X\I|=|X∩U|=D−|B∩U|,
    |V\I|=|B\U|+|T|=k−|B∩U|+D−k.

Transport the genuine action on V through θ to an action τ on X. For every g∈G,

    |{x∈X : τ(g)x ≠ c_X(ρ(g))x}|
       ≤ D+k−2|B∩U| ≤ D+k.                               (1)

**Proof.** There are |X∩U|=D−|B∩U| possibly bad starting points outside I. If x∈I and ρ(g)x∈I, both maps equal ρ(g)x, since θ fixes source and target and compression does not change a step landing in X. As U is invariant, a point of I can fail this condition only when ρ(g)x belongs to B\U. There are at most |B\U| such points. Adding these bounds proves (1). ∎

The estimate holds uniformly in g for this particular construction. It uses a relabeling of the surviving action, not an assertion that the original X is invariant. It is valid even when B meets a giant transitive orbit and U is a disjoint union of entirely different, smaller orbits.

Define the orbit-packing number

    P_ρ(k)=min{|U| : U is invariant and |U|≥k}.

For k=0 choose U=∅. For positive k≤|Y|, the minimum exists because U=Y is available. It depends only on the multiset of orbit sizes. The generator-error distance from the compression to some exact same-size action is at most

    min{1,(P_ρ(k)+k)/n}.                                   (2)

No flexibility assumption is used in this finite statement.

## 2. Consequences that do not require tightness of the whole orbit distribution

Suppose the total size of all orbits of size at most L is at least k. Greedily add such orbits until their total D first reaches k. Then

    k≤D≤k+L−1,

so (1) gives an exact repair with error at most

    (2k+L−1)/n.                                            (3)

In a sequence with k/n→0, it is therefore enough to have some L=o(n) for which the small-orbit mass is at least k. The rest of the action may consist of a giant orbit containing almost all points. This is strictly less restrictive as a sufficient hypothesis on the chosen repairs than the tight-orbit condition in Turn 1.

For instance, if there are at least k global fixed points anywhere in Y, choose k of them as U. Then D=k and the error is at most 2k/n. They need not be among the originally added points. This is the geometric reason the reservoir absorption in Turn 2 works when enough common fixed points are available.

Another useful conclusion concerns a hypothetical obstruction. Suppose the compression is at generator-error distance at least ε>0 from every exact action on X. If k/n<ε/8, then the total mass of orbits of size at most floor(εn/2) is strictly less than k. Otherwise (3), with L=floor(εn/2), would give error at most 2k/n+ε/2<3ε/4, a contradiction.

Consequently, along an obstructing sequence with k/n→0 and a fixed positive error gap, all but fewer than k points lie in orbits of size >εn/2. There are at most 2|Y|/(εn) such orbits. Thus the obstruction is concentrated in a bounded number of macroscopic orbits. This is a necessary structure theorem for a deletion witness, not the construction of a flexibly stable counterexample.

## 3. Transitive actions suffice

Fix a nonempty finite symmetric generating set S. Let D_{G,S}(δ) be the deletion modulus from Turn 1. Define T_{G,S}(δ) by the same formula, except that ρ is required to be transitive on Y. In both definitions the retained subset X is nonempty and |Y\X|≤δ|X|, and the error is the minimum over exact actions on X of the maximum normalized Hamming error on S.

Clearly 0≤T(δ)≤D(δ)≤1 and T(0)=0. For all δ≥0 and η>0,

    D(δ) ≤ min{1, T(η)+δ/η}.                               (4)

**Proof.** Take an arbitrary action ρ on Y and a retained subset X, and decompose Y into its transitive orbits O_i. Put X_i=X∩O_i, n_i=|X_i| and k_i=|O_i\X_i|. Ignore empty X_i, which contribute no retained points. Compression preserves each nonempty X_i.

Call an index good when k_i/n_i≤η, and bad otherwise. The total retained mass of the bad indices is bounded by

    Σ_bad n_i < (1/η)Σ_bad k_i ≤ k/η.                       (5)

For each good orbit, the definition of T(η) supplies an exact action τ_i on X_i with maximum generator error at most T(η). The defining minimum is attained for every finite X_i; the supremum in T need not be attained. Use the trivial action on every bad X_i. Their disjoint union is an exact G-action τ on X. For each s∈S, raw disagreement counts add, giving

    d_X(c_X(ρ(s)),τ(s))
      ≤ (1/n)Σ_good n_i T(η) + (1/n)Σ_bad n_i
      ≤ T(η)+k/(ηn) ≤ T(η)+δ/η.

Take the maximum over S, the minimum over repairs, and the supremum over input actions. ∎

Thus

    lim_{δ↓0} D_{G,S}(δ)=0
       ⇔ lim_{δ↓0} T_{G,S}(δ)=0.                           (6)

For the nontrivial direction choose η=√δ in (4) for δ>0. The reverse follows from T≤D. Combining with Turn 1:

### Theorem

For a flexibly permutation-stable finitely generated group G, ordinary permutation stability is equivalent to the vanishing small-deletion modulus **for transitive finite actions alone**.

Combining additionally with Turn 2, any negative answer to the original question can be sought in a finitely generated residually finite nonamenable group and witnessed by a sequence of transitive finite actions with o(|Y|) deleted points whose compressions stay a fixed positive generator-error distance from every same-size action.

For precision, if D(δ_j) is bounded below while δ_j→0, use (4) with η_j=√δ_j to see that T(η_j) is bounded below. Choose actions approximating this supremum with a smaller fixed positive threshold. Their retained sizes necessarily tend to infinity because positive error entails at least one deleted point. Hence these form a legitimate increasing-dimension subsequence, as explained in Turn 1. No finite transitive action is claimed to witness failure of an asymptotic group property by itself.

## 4. What orbit replication does and does not establish

Making disjoint copies of an action duplicates its orbit-size multiset; it does not shrink a transitive orbit. If every orbit has the same size M and the required deletion is 0<k<M, the packing number is P_ρ(k)=M. Repetition leaves this same arithmetic obstruction when comparing one almost-complete orbit to a set of size M−k.

At a much larger ambient size tM, discarding a whole orbit of size M may be negligible. That alone does not yield a repair for the original M-point-scale challenge: an exact action on the enlarged tM−k or t(M−k) points need not split into t invariant pieces of the desired smaller size. Selecting an arbitrary block would again require an unsupported invariant-subset or constraint-stability argument.

This turn therefore does not claim that stability can be de-amplified from replicated actions, or that a favorable orbit-packing bound always exists for the flexible repairs supplied by the definition. In the transitive case, the only invariant reservoirs are ∅ and Y, so the packing construction itself gives no useful small-error bound.

The residual task is concrete: repair the punctured Schreier action on a single large coset space G/H without adding points. A positive statement for all such actions would solve the implication by (4)–(6); merely restating that statement is not a proof. The transitive deletion route remains blocked without a new geometric, algebraic, or spectral mechanism.

## 5. Check scope

The portable exact verifier reconstructs common orbits of all two-generator permutation actions through four points, deletes every proper subset, tests every invariant reservoir of sufficient size, builds the new action and relabeling, and checks (1) on the generators. Independent arithmetic loops check the packing and orbit-mass inequalities on integer partitions. The pointwise group conclusion and all unbounded quantifiers are proved above, not inferred from these finite controls. No historical novelty is asserted for orbit surgery, disjoint unions, or the elementary packing argument.

**Status:** original target unresolved after 3/5. Next author work should address genuine transitive obstructions, while distinguishing an obstruction for one finite-action family from the global flexible stability required of a counterexample group.
