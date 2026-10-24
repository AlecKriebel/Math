# A checkable obstruction to raw parabolic-coset rigidity

Date: 2026-10-24. Status: proved route obstruction; not a counterexample to Kourovka 21.129. The groups on both sides below are the same group.

**Terminology in this note:** two embedded subgroups are *internally commensurable* if their intersection has finite index in both. This is stronger than abstract commensurability. The image subgroup constructed here is isomorphic to a finite-index subgroup of a standard `A2` parabolic, so those groups **are abstractly commensurable**. The obstruction is solely to internal commensurability and finite Hausdorff distance of their embeddings.

## Statement

Let `K = A[A3]/Z(A[A3]) = B4/Z(B4)`. There is a self-quasi-isometry `F: K -> K` and a standard maximal proper parabolic subgroup `C` of type `A2` such that `F(C)` is not at finite Hausdorff distance from any left coset of any conjugate of a standard maximal proper parabolic subgroup of `K`.

Consequently, a proposed proof of Kourovka 21.129 cannot assume that arbitrary quasi-isometries coarsely permute the **raw** standard maximal-proper-parabolic cosets. Additional geometric structures, or a larger intrinsically defined family, would be required.

## Construction

View `K` as the orientation-preserving mapping class group of a sphere with five marked punctures `0,1,2,3,4`, fixing puncture `0`. Here `0` is obtained by capping the boundary of the four-punctured braid disk. Let

`H = P4/Z(P4) = PMod(S0,5)`.

This is a normal finite-index subgroup of `K`. Choose an orientation-preserving sphere mapping class `f` interchanging `0` and `1`. Since `H` is the kernel of the full puncture-permutation homomorphism in `Mod(S0,5)`, conjugation by `f` defines an automorphism `alpha` of `H`.

Take `C` to be the image of the standard `B3` on disk punctures `{1,2,3}`; thus `C` is a standard maximal proper parabolic of type `A2`. Put `D=C intersect H`, and `Q=alpha(D)`.

An automorphism of a finitely generated group is a quasi-isometry. Choose finitely many right coset representatives for `H` in `K`, and send `hr` to `alpha(h)`. This defines a self-quasi-isometry `F` of `K`, restricting to `alpha` on `H`. Since `D` has finite index in `C`, `F(C)` has finite Hausdorff distance from `Q`.

The support description is intuitive: `D` is a pure braid group supported on a disk containing `{1,2,3}` and avoiding `0`; `Q` is supported on the disk containing `{0,2,3}`. The latter is not conjugate by a mapping class fixing `0` to the former kind. The following homology computation proves failure of internal commensurability without relying on support terminology.

## Rational homology certificate

Write `e_ij`, for `1 <= i < j <= 4`, for the standard pairwise pure-braid linking classes. The elementary abelianization calculation gives

`V = H_1(H;Q) = Q^{ {12,13,14,23,24,34} } / Q v`,

where `v=e_12+e_13+e_14+e_23+e_24+e_34` is the class of the full twist, which is killed in `H`.

The image of `D` in `V` spans

`U = span(e_12,e_13,e_23)`.

Conjugation by `f` sends the class of a twist around a pair to the class of a twist around the permuted pair. A twist enclosing `0` and `i` is also the boundary twist enclosing the complementary three finite punctures, so

```
alpha(e_12) = e_02 = e_13+e_14+e_34
alpha(e_13) = e_03 = e_12+e_14+e_24
alpha(e_23) = e_23.
```

Thus the rational homology image of `Q` is

`U' = span(e_13+e_14+e_34, e_12+e_14+e_24, e_23)`.

It has dimension three: if a linear combination of these three displayed vectors is a multiple `lambda v`, comparison of the `12,24` coefficients and of the `13,34` coefficients gives the two first coefficients equal to `lambda`; comparison of `14` then gives `2 lambda=lambda`, hence all coefficients vanish. Moreover,

`(e_13+e_14+e_34)+(e_12+e_14+e_24)+e_23 = v+e_14`,

so `U'` contains both `e_14` and `e_23`.

There are two types of standard maximal proper parabolics in `A3`:

1. Type `A2`. After conjugating by any element of `K` and intersecting with `H`, its rational homology image is `U_T = span(e_ij : i,j in T)`, where `T` is a three-element subset of `{1,2,3,4}`. Indeed the action of `B4` on the linking classes is just permutation of finite puncture indices. A coordinate vector `e_ab` belongs to `U_T` only if `{a,b}` is contained in `T`: otherwise compare its coordinates outside the three edges of `T`, of which at least two are available, in any equality modulo `Qv`. Since no three-element `T` contains both disjoint pairs `{1,4}` and `{2,3}`, `U_T` cannot equal `U'`.
2. Type `A1 x A1`. Its pure intersection, and every conjugate's pure intersection, has rational homology image of dimension at most two, so its image cannot equal the three-dimensional `U'`.

If two subgroups of `H` are internally commensurable, their images in `H_1(H;Q)` have the same rational span: a finite-index subgroup contains a positive power of each element, and positive powers span the same rational homology image. It follows that `Q` is not internally commensurable with any `K`-conjugate of any standard maximal proper parabolic after intersecting with `H`. Normality and finite index of `H` then give the same failure of internal commensurability before that intersection.

Finally, for subgroups of a finitely generated group, finite Hausdorff distance of one subgroup from a left coset `gL` forces internal commensurability with `gLg^-1`: the finite distance bound gives a finite cover by cosets of the intersection. Hence `Q`, and therefore `F(C)`, cannot have finite Hausdorff distance from any of the asserted cosets. This proves the statement.

## What this does and does not rule out

This disproves the raw preservation lemma even in a braid group. It does not disprove preservation of a suitably enlarged family, such as centralizers of geometrically defined twists, and it does not produce two noncommensurable quasi-isometric spherical Artin groups. A larger family would need an independent intrinsic characterization and a full inventory before its patterns could distinguish the residual `D/E` or `F/H` pairs.
