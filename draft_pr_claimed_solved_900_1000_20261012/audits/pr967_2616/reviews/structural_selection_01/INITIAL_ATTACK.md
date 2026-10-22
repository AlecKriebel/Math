# Independent initial attack: finite-to-one selection obstruction

Saved UTC: 2026-10-16T20:27:54.885381+00:00

This was written before intake of the research charter, submitted report, original source records, prior assessments, or other families. The only mathematical inputs read were the authenticated neutral brief and primary Kourovka v48 problem 21.107 (printed page 193). No preferred verdict was supplied.

## Claim and success criterion

Interpret open as nonempty open. We seek a countably infinite Hausdorff topological group with a partition into infinitely many dense pieces but with no sequence of pairwise disjoint finite blocks meeting every nonempty open set eventually (the threshold may depend on that open set). Work in ZFC; the ultrafilter lemma used below follows from Zorn's lemma and requires no additional set-theoretic hypothesis beyond ZFC.

## General structural obstruction (fully proved here)

Let X have a finite-to-one map f:X→N. Suppose a free ultrafilter p on N has the property that for every A∈p there is a nonempty open O_A⊂f^{-1}(A). Then X admits no expansive sequence of pairwise disjoint finite subsets.

Proof. If infinitely many blocks are empty, they already fail every nonempty open set. Otherwise work beyond all empty blocks. From any disjoint finite blocks F_n, extract n_0<n_1<… such that M_k=f(F_{n_k}) are nonempty, finite, and pairwise disjoint. Indeed, the preimage of the finite union of previously selected M_k is finite, and by disjointness it meets only finitely many F_n. Let E=⋃_{k even}M_k. If E∈p take A=E and the odd selected blocks. Otherwise take A=N\E∈p and the even selected blocks. Infinitely many selected blocks miss f^{-1}(A), hence miss O_A. This contradicts eventual hitting. QED.

The finite-to-one condition is substantive: it makes a finite coordinate set exclude only finitely many disjoint blocks. No assumption about bounded block sizes or block coverage occurs.

## Boolean group realization

Fix a free ultrafilter p on N. Such a p exists in ZFC by extending the cofinite filter to a maximal proper filter; it cannot contain a finite set since it contains that finite set's cofinite complement. Set G=[N]^{<ω} with symmetric difference and identity ∅. For A∈p put H_A=[A]^{<ω}. Declare cosets x△H_A a base. We have H_A∩H_B=H_{A∩B}, H_A△H_A=H_A, and each H_A is a subgroup. Thus translations are homeomorphisms and group addition is continuous (the sum of two H_A-neighborhoods is in H_A); inversion is identity. This defines a topological group.

It is Hausdorff: if x≠y choose i∈x△y and A=N\{i}∈p. Then x△y∉H_A, so the disjoint cosets x△H_A and y△H_A separate x,y. Every basic open set is infinite since A is infinite, so the group is nondiscrete. The set of finite subsets of N is countably infinite.

Define f(∅)=0, f(x)=max x when x≠∅, using N={0,1,…}. Each fiber is finite: f^{-1}({j}) has 2^j nonzero elements (and the fiber at 0 also contains ∅). For A∈p the set O_A=H_A\{∅} is nonempty and open: H_A is open and the singleton {∅} is closed by Hausdorffness. Every x∈O_A has f(x)∈A. The general structural obstruction applies.

For an even more direct formulation, beyond the at most one block containing ∅, extract blocks with pairwise disjoint sets of maximum coordinates. The ultrafilter decides the union of the even maximum sets. Either H_E or H_{N\E} then misses infinitely many whole selected blocks, as each point in those blocks has maximum outside the chosen coordinate set. This avoids any concern about deleting the identity from an open subgroup.

## Dense partition

Partition N into disjoint infinite, hence unbounded, sets C_k; explicitly C_k={m≥0: the exponent of 2 dividing m+1 is k}. Put D_k={x∈G: |x|∈C_k}. These form a countably infinite partition of G. For any coset x△H_A let r=|x\A|. For every integer t≥r there exists E⊂A finite with |E|=t-r, and (x\A)∪E belongs to x△H_A, since its symmetric difference with x is (x∩A)△E⊂A. Thus every basic open set contains points of every cardinality t≥r. Since C_k is unbounded, each D_k meets every basic open set and is dense. This proves a negative answer under a stronger Hausdorff assumption.

## Positive boundary and blocked routes

If a countable space has a countable π-base U_0,U_1,… and a partition into dense pieces D_n, choose a finite F_n⊂D_n meeting U_0,…,U_n. The F_n are disjoint, and each nonempty open set contains a U_i, so F_n eventually meet it. This is a complete positive result under the extra countable π-base assumption. Countability of the underlying group supplies no countable π-base. The Boolean group above witnesses the failure of that shortcut.

Attempting to diagonalize arbitrary open sets from a countable enumeration of points merely replaces the problem with an unsupported simultaneous selection principle. Mark this route blocked absent countable π-base or another proven mechanism. No category/compactness selection theorem is imported.

## Adversarial self-checks at this checkpoint

- The open set missing infinitely many blocks is allowed to depend on the entire proposed sequence, as required by the negation of expansiveness.
- Its missing block indices are unbounded; this defeats every open-dependent threshold.
- Arbitrarily large block sizes and an incomplete union of blocks do not affect the argument.
- Empty blocks and the unique identity-containing block are handled explicitly.
- Every dense piece is a union of cardinality levels with unbounded level sizes, not one fixed finite level.
- Every coordinate ultrafilter set is infinite; Hausdorffness uses cofinite members only.
- No finite computation proves the free ultrafilter or the universal quantifier. The proof is symbolic and uses ZFC choice.

Strongest current result: a complete candidate-independent construction and proof of a Hausdorff counterexample, subject to another careful audit. Estimated completion toward independent mathematical assessment: 80%. This is neither a priority statement nor a present open-status certificate.
