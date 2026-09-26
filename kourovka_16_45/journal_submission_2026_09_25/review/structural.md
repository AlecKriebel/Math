# Independent adversarial structural review

Checkpoint: **2026-09-25 21:05:51 PDT** (2026-09-26 04:05:51 UTC).  
Scoped completion estimate: **100% of the requested independent structural audit**.  
Reviewer: a separate OpenAI Codex review agent; this is an AI-assisted audit, not external human peer review or formal proof-assistant verification.

## Scope, independence, and verdict

The reviewer first read `proof.tex` in full, without reading previous review verdicts or any supplied verification implementation. All structural arguments were re-derived. A fresh small checker, `structural_scratch.py`, was then written directly from the displayed matrices. It imports only the Python standard library and does not read generated group tables or other code.

**No mathematical defect was found in the stated counterexample or its upper bounds.** The independently checked conclusion is

\[
G=\mathbf F_{29}^2\rtimes\langle A,B\rangle,
\qquad |G|=100920,
\qquad b_{\mathrm f}(G)=b(G)=3<4=\mu'(G).
\]

The proof is structural. In particular, its all-actions upper bound does not assume that a meet-irredundant family has normal bottom, that subgroup core replacement preserves irredundancy, that actions are faithful, that subgroups are maximal, or that they are mutually conjugate. The affine subgroup lattice is not needed.

This audit does not establish bibliographic novelty, verify current journal policies, or inspect the full supplied verifier implementations. Those require separate audits. It does verify the mathematical content of the characteristic-11 boundary construction. It supplies no guarantee of acceptance.

## Claim and assumptions

The claimed invariant maximizes **inclusion-minimal** base size over all actions, permitting nonfaithful actions, and takes the kernel as the pointwise stabilizer defining a base. The faithful variant maximizes over faithful actions only. The independence invariant permits sets that generate proper subgroups. These conventions are consistently maintained in the proof.

The construction requires the actual displayed matrices over the prime field of order 29, rather than merely an unspecified abstract semidirect product. Critical properties are:

1. `H/Z` is isomorphic to `A_5`, `|H|=120`, and `Z={I,-I}`.
2. Every even-order subgroup of `H` contains `Z`; every odd-order subgroup is trivial or cyclic of order 3 or 5.
3. Every line stabilizer of `H` injects into the multiplicative field group and therefore has order dividing `gcd(120,28)=4`.
4. The additive group of the two-dimensional space has only dimensions 0, 1, or 2 as possible subgroup dimensions, because the field is prime.

All four assumptions are proved in the manuscript, rather than posited.

## Foundational subgroup arguments

### Base families and action kernels

For an actual minimal base the stabilizer intersection is the action kernel, hence normal. Conversely the disjoint union of left coset actions for `L_i` has kernel

\[
\bigcap_i\operatorname{Core}_X(L_i)
=\operatorname{Core}_X(\bigcap_iL_i)=N
\]

when the intersection is the normal subgroup `N`. Deleting an identity coset enlarges the stabilizer exactly when deleting the corresponding subgroup enlarges the intersection. This proves both directions without replacing the family itself by its cores. Factoring through a kernel and pulling back a faithful quotient action prove the quotient formula.

The empty-family conventions are correct: its intersection is `X`, corresponding to a trivial image, and the empty faithful base occurs only for the trivial group. The finite-image argument also handles arbitrary infinite point sets: choose one moved point for each nonidentity permutation-image element, obtaining a finite subbase. An inclusion-minimal base must equal a finite subbase.

### Independence equals unrestricted intersection breadth

If a family is irredundant, its deletion witness `x_i` lies in every `L_j`, `j != i`, and outside `L_i`. Hence every other witness lies in `L_i`, which excludes `x_i` from their generated subgroup. Witnesses are necessarily distinct. Conversely an independent set gives its omission-generated subgroups, with exactly the same witnesses. Neither direction requires normal bottom.

The proposed map from a Boolean lattice sends `A` to the intersection of `L_i` with `i` outside `A`. It preserves meets because the union of the two complementary index sets is the complement of their intersection. If two index sets differ at `i`, witness `x_i` belongs to the image of the set containing `i`, but not the other image. Thus the map is injective and top-preserving. No preservation of joins was used.

### Restriction and subgroup monotonicity

On restricting to `L_i`, each other original witness still lies in `L_i`, so the restricted family stays irredundant. Its total intersection equals the original total intersection. This also works for a family of size one: the restricted empty intersection is `L_i`, which equals the original intersection in that case. For trivial total intersection, the faithful invariant is therefore the correct sharper bound.

Independence is subgroup-monotone because generated subgroups are unchanged by embedding in an overgroup. The faithful base invariant is subgroup-monotone because a family with trivial intersection and the same witnesses remains such a family in the overgroup. The possible empty family causes no exception. The analogous arbitrary-action monotonicity is not needed or asserted.

## Complement audit

### Identification and elementary subgroup facts

The displayed matrices have determinant one and satisfy `A^2=B^3=(AB)^5=-I`. Since `Z` is contained in `H`, the projective image is a nontrivial quotient of the standard `(2,3,5)` triangle presentation of `A_5`, and simplicity gives `H/Z=A_5`. The central kernel has two elements, giving `|H|=120`. This reasoning is valid. The alternative explicit identification with `SL_2(5)` is not needed by the structural upper bound.

The classification needed for proper subgroups of `A_5` is sufficient and correct. An intransitive subgroup either fixes a letter or has orbit partition `2+3`, embedding respectively in `A_4` or `(S_2 x S_3) cap A_5`, the latter isomorphic to `S_3`. A proper transitive subgroup has order 5, 10, 15, 20, or 30. Orders 15 and 20 force a normal Sylow 5-subgroup; its normalizer in `A_5` has order 10, ruling them out. Order 30 would be index two, contradicting generation by elements of order three. Orders 5 and 10 lie in a Sylow-5 normalizer. Thus the asserted containing groups are indeed exhaustive.

`A_4` has independence number two: its proper subgroups have independence number at most two; an independent generating set for the whole group contains a 3-cycle and an element outside that cycle's subgroup, and these two generate `A_4` since no subgroup has order 6. In a dihedral group of order `2q`, `q` an odd prime, either a nonidentity rotation and a reflection or two distinct reflections generate. The same statement covers `S_3`. Deleting any element of an independent set in `A_5` leaves a set generating a proper subgroup, so its size is at most two and the original size is at most three. Fixing three points in the natural degree-five action gives a minimal base of size three. All uses of simplicity are valid.

### The two complement base invariants

Over a field of odd characteristic, a matrix squaring to the identity is diagonalizable with eigenvalues in `{1,-1}`. In `SL_2(29)` the determinant condition forces equal signs, so the only element of order two is `-I`. Cauchy's theorem now forces every even-order subgroup to contain `Z`. Odd-order subgroups inject into `A_5`; the classification just checked makes them trivial or cyclic of prime order 3 or 5.

For an independent set whose quotient images are not independent as an indexed family, choose `s` whose image lies in the group generated by the other images, and put `K=<S\{s}>`. Then `s` lies in `KZ` but not in `K`, forcing `Z` not to lie in `K`. Thus `K` is odd-order, hence trivial or cyclic of prime order. The remaining independent set has size at most one, giving original size at most two. This argument correctly covers repeated quotient images, identity quotient images, and singleton sets. If the quotient images are independent, their number is at most three. Hence `mu'(H)<=3`.

A family with identity intersection must have an odd-order member. If it is trivial, minimality leaves only that member. If it has prime order, identity intersection forces some second member to meet it trivially, and minimality leaves at most two members. Subgroups of orders 3 and 5 exist by Cauchy's theorem and furnish the matching lower bound. Hence `b_f(H)=2`.

### Explicit triple

Fresh calculations verify the displayed words for `R_2` and `R_3`, the three squares `-I`, pair orders 8, 12, 20, and product orders 4, 3, 10. Projective pairs have respective product orders 2, 3, 5 and generate dihedral groups of orders 4, 6, 10. As the original pair groups contain `Z`, their orders are twice these values. The three-generator group has order divisible by `lcm(8,12,20)=120`, so is all of `H`; each pair is proper. This proves independence.

The order-8 and order-12 pair groups intersect in the cyclic order-4 subgroup generated by `R_3`: containment gives the lower bound and the greatest common divisor gives the upper bound. The order-20 pair group omitting `R_3` cannot contain `R_3`, since otherwise it would generate all of `H`. It does contain `Z`, giving total intersection exactly `Z`. Thus this is an irredundant rank-three family with normal bottom in `H`, and `b(H)=mu'(H)=3`.

## Affine upper bounds

### Scalar-line lemma

In `P rtimes C` with `|P|=p` and faithful scalar cyclic 2-group `C`, a subgroup either injects into `C` or contains `P`. In the former case it is a cyclic prime-power group and has independence number at most one. In the latter case it equals the full inverse image `P rtimes D` of its projection. If `D=1`, it is cyclic of prime order. Otherwise every generating set has a member whose projection generates `D`, because a cyclic prime-power group has a unique maximal subgroup. For that member the geometric-series identity gives order exactly `|D|`, so its cyclic subgroup is a complement. Any further generator outside this complement, together with that member, has full projection and nontrivial intersection with `P`, and therefore generates the whole subgroup. This proves the bound two for every subgroup, hence for arbitrary independent sets. The proof correctly includes `C=1` and `D=1`.

### Line stabilizers and subgroups missing the translation group

The action of a line stabilizer on its line is a homomorphism to `F_29^*`. Its kernel consists of determinant-one upper triangular matrices with both diagonal entries one. Every nonidentity such matrix has order 29, impossible in a group of order 120. Thus this scalar action is faithful, its image is cyclic, and its order divides four. The whole complement cannot preserve a line, proving irreducibility.

If `K cap V=1`, projection embeds `K` in `H`; the subgroup-monotone bounds above give `mu'(K)<=3` and `b_f(K)<=2`. If `K cap V=W` is a line, then the projected group stabilizes `W` and has cyclic order 1, 2, or 4. By the first isomorphism theorem, `|K|=29|pi(K)|`; a Sylow 2-subgroup has order `|pi(K)|`, intersects `W` trivially, and projects isomorphically onto `pi(K)`. It therefore complements `W`. Its action on `W` is the faithful scalar action already proved. The line lemma applies. No unproved splitting theorem, affine conjugacy classification, or cohomological vanishing is hidden here.

### Faithful versus arbitrary actions

A family with identity intersection has a member missing `V`. Restriction to that member gives `t-1<=b_f(K)<=2`, yielding `b_f(G)<=3`.

If `N` is normal, `N cap V` is an `H`-invariant subspace. Irreducibility forces it to be zero or all of `V`. In the zero case, `[N,V]` lies in `N cap V`, hence is trivial. The centralizer of all translations consists exactly of translations, because the matrix action is faithful. Consequently `N<=V` and `N=N cap V=1`. Every nontrivial normal subgroup therefore contains `V`. An arbitrary nonfaithful action consequently factors through `H`, so its base sizes are at most `b(H)=3`. This includes the trivial action. Together with the faithful bound, it establishes `b(G)<=3` without assuming that `b` is subgroup-monotone.

For arbitrary meet-irredundant families, if all members contain `V`, the subgroup correspondence for the genuinely normal subgroup `V` preserves intersections and witnesses, giving rank at most `mu'(H)=3`. Otherwise restriction to a member missing `V` gives rank at most four (and at most three when its translation intersection is a line). Thus `mu'(G)<=4`.

## Affine lower bounds and obstruction

The three linear elements of the displayed four-set remain independent after adjoining a translation: projection would otherwise contradict independence of the three `R_i`. The nonzero translation does not belong to the zero-translation complement. Thus the four-set is independent. It generates `G` because its linear elements generate `H` and the linear span of the orbit of a nonzero vector is a nonzero invariant subspace, hence all of `V`.

Each omission pair in `H` has order greater than four and hence is irreducible by the line-stabilizer bound. Therefore the three affine omission groups containing the nonzero translation contain all translations; their orders are exactly `841` times 8, 12, and 20. Their intersection with the complement is precisely the corresponding pair subgroup. Intersecting all four omission groups gives the displayed order-two `Z_0`.

For the faithful lower bound, the first two order-58 groups consist of translations on the coordinate lines and inversions with translation parts on those same lines. The third consists of translations `t(1,1)` and affine inversions with translation parts `(2,0)+t(1,1)`. Pairwise intersections contain only the identity translation and respectively inversions with translation parts `(0,0)`, `(2,0)`, and `(0,-2)`. These parts are distinct over the field of order 29, so the triple intersection is the identity while all deletion intersections have order two. This verifies all three printed intersections, minimality, faithfulness, and degree `3*100920/58=5220`.

Conjugating the zero-translation `-I` by the nonzero translation `e_1` gives translation part `2e_1`, which is nonzero in odd characteristic. Hence `Z_0` is not normal. The proper pair subgroups of `H` have core `Z`, since their projective cores are normal proper subgroups of simple `A_5`. Their affine inverse images have cores `V rtimes Z`. The complement has trivial core by the already-proved normal-subgroup classification. Thus the four core replacements have lost irredundancy exactly as stated.

## Boundary case and finite checks

The fresh checker independently finds 120 matrices in each displayed characteristic-29 and characteristic-11 complement. For characteristic 29 it verifies all matrix words, pair orders, pair intersections, generation by the three `R_i`, thirty line stabilizers each cyclic of order four, and all three faithful-family intersections.

In characteristic 11 it confirms that the printed `C` lies in the generated complement, has order ten, and preserves both printed lines. The eigenvalues on the two lines are 6 and 2. Intersecting the first two subgroups of the four-family gives the zero-translation complement `<C>`; its subgroups `<C^5>` and `<C^2>` have relatively prime orders two and five. Therefore the total intersection is trivial. Omitting either line subgroup leaves the other translation line, of order 11; omitting the order-two projected subgroup leaves `<C^2>`, of order five; omitting the order-five projected subgroup leaves `<C^5>`, of order two. The claimed boundary counterexample is valid.

Invocation:

```
python3 journal_submission_2026_09_25/review/structural_scratch.py
```

Recorded result: exit code 0. Printed stabilizer distributions are `{4: 30}` over characteristic 29 and `{10: 12}` over characteristic 11. No large affine multiplication table, subgroup-lattice enumeration, or floating-point optimizer is used by this scratch check.

## Findings and optional improvements

**Required mathematical repairs: none found.**

Optional expository improvements for submission:

- State once that a finite cyclic prime-power group has independence number at most one; its unique maximal subgroup proves that every generating set contains a generator. The manuscript already relies on this elementary fact correctly.
- Name the use of Cauchy's theorem when passing from even subgroup order to containment of the unique involution, and when producing the faithful order-3/order-5 pair. This is clarity rather than a missing premise.
- Move detailed verifier census, computational provenance, previous optimization history, AI audit logistics, and possibly the characteristic-11 construction into supplementary material. Retain a concise reproducibility statement and every structural lemma needed for the theorem. The theorem does not depend on that longer material.
- The phrase “the equality `gcd(120,28)=4` is essential” is best understood as essential to this proof mechanism. A slightly more precise phrase is “The cyclic 2-group bound on line stabilizers is essential to this argument.” The characteristic-11 example disproves omission of all characteristic restrictions, but it does not classify every other characteristic.

Strongest verified result: the exact strict inequality and both matching base lower bounds as stated above. Remaining gap within this audit's mathematical scope: **none identified**. Remaining limitations: verification is not formalized, and bibliographic priority and editorial acceptance are separate questions.
