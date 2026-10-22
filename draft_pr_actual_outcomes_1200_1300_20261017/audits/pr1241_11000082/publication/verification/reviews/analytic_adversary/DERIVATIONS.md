# Independent derivation and adversarial checks

These calculations check the submitted proof's mechanism. They are analytic proof checks, not computational certification. The source theorem inspection and its limits are in `REPORT.md` and `SOURCES_RECEIPT.json`.

## 1. Parameter, squares, and sign issues

Put the separating filling pair in minimal position and let its geometric intersection be `n`. The union is a connected graph with `n` vertices and `2n` edges. Its `f >= 1` faces are disks. Therefore

`2 - 2g = n - 2n + f`, hence `n = 2g - 2 + f >= 2g - 1`.

A closed curve crosses a separating curve an even number of times, so `n` is even. For `g >= 2`, this forces `n >= 4`, precisely the strict inequality needed to exclude the critical two-parabolic case.

For a single curve in either family the intersection matrix is `[n]`. A positive eigenvector of `[n^2]` is `[1]`, and the corresponding other side parameter is `n^(-1)[n][1] = [1]`. The rectangles are thus squares. Choose unit square coordinates; edge identifications have the form `z -> +/- z + c` with integral `c`. Cone points are square vertices; some square vertices can instead be regular, which does not harm the integral-grid statement.

The horizontal annulus has circumference `n` and transverse width `1`. One twist changes horizontal coordinate by `n` times vertical coordinate, giving the matrix `A = [[1,n],[0,1]]`. With the indicated positive twist orientation the vertical annulus gives `B = [[1,0],[-n,1]]`.

The checked two-parabolic theorem supplies a free rank-two derivative image for this parameter and exactly two parabolic conjugacy types. To see why the twist subgroup itself is faithful, use the surjections

`F_2 -> <T_a,T_b> -> derivative image ~= F_2`.

Their composite is a surjective endomorphism of a rank-two free group, hence injective by Hopficity. Both intervening maps are consequently injective as well. In particular no nonidentity word can be lost in the derivative kernel on this subgroup.

## 2. Johnson centrality with the exact shift

Write the ordinary group lower central series as `gamma_1(G)=G`, `gamma_(r+1)(G)=[G,gamma_r(G)]`. The submission's `Gamma_j` is `gamma_(j+1)(G)`.

For `r >= 1` let `A_r` be the automorphisms of `G` acting identically on `G/gamma_(r+1)`. Standard commutator calculus gives

`[A_r, gamma_t(G)] <= gamma_(r+t)(G)` for `t >= 1`.

Here is the induction underlying that assertion. The case `t=1` is the definition of `A_r`. In the semidirect product of automorphisms with `G`, suppose the assertion holds at `t`. The three-subgroup commutator lemma controls the action on `[G,gamma_t]` by `[gamma_(r+1),gamma_t]` and `[G,gamma_(r+t)]`. Both lie in `gamma_(r+t+1)`. This proves the next step. The relevant lower-central subgroups are characteristic and hence normal in the semidirect product, so taking quotients in this argument is legitimate.

Apply the same lemma to `A_r,A_s,G`, modulo `gamma_(r+s+1)`. The two iterated commutators `[A_s,[A_r,G]]` and `[A_r,[A_s,G]]` lie in this subgroup by the preceding formula. Consequently

`[[A_r,A_s],G] <= gamma_(r+s+1)`, and `[A_r,A_s] <= A_(r+s)`.

For the outer-automorphism version, a representative of a class acting as an inner automorphism on `G/gamma_(r+1)` can be multiplied by an inner automorphism lifted from `G` so as to act identically on that quotient. Thus `I_g(r)` is the image of `A_r` in the relevant outer group, and

`[I_g(r),I_g(s)] <= I_g(r+s)`.

Only `r=1` is needed. Since both separating twists act trivially on homology, `F <= I_g(1)`. With `L_1(F)=F`, induction gives `L_j(F) <= I_g(j)`. In FLM's zero-indexed lower-central convention this same group is the `(j-1)`st term. This is not inferred merely from the weaker assertion that successive quotients are abelian.

## 3. The fixed nonabelian subgroup

Define `u_1=B` and `u_(j+1)=[A,u_j]`. Each `u_j` lies in `L_j(F)`. The word `u_2` is nonidentity because `A,B` freely generate `F`. If a later `u_(j+1)` vanished, the cyclic centralizer of `A` would give `u_j=A^e`. For `j >= 2`, abelianization of `u_j` is zero, so `e=0`, contradicting induction. Hence all `u_j` are nonidentity.

For fixed `k >= 3` put `u=u_k`, `v=B u B^(-1)`. Normality of `L_k(F)` puts both in that subgroup. Suppose they commute. Let `<r>` be the maximal cyclic subgroup containing `u`, say `u=r^e` for nonzero `e`. The commuting element `v` lies in `<r>`, while also lying in `B<r>B^(-1)`. Their nontrivial intersection and malnormality force `B` into `<r>`. But `e[r]=[u]=0` in the torsion-free abelianization `Z^2`, so `[r]=0` and then `[B]=0`, a contradiction.

Thus `H=<u,v>` is a nonabelian two-generated subgroup of a free group. Nielsen-Schreier makes it free. Its rank is at most two (use abelianization of a free group and the given generating set), and nonabelianness excludes rank one, so it has rank two. The epimorphism `F_2 -> H` defined by `u,v`, composed with any rank-two free-group identification, is a surjective endomorphism of `F_2`. Hopficity makes it an isomorphism: the displayed pair really is a basis.

Every element of `H` lies in `[F,F]`, so has zero `A,B`-abelianization. A conjugate of `A^e` or `B^e`, `e != 0`, has nonzero abelianization. Hence no nonidentity element of `H` has a parabolic derivative. Faithfulness, the checked classification, and the hyperbolic-derivative theorem show that all such elements are pseudo-Anosov. This establishes exactly the purely hyperbolic subgroup needed, without an extra geometric use of the word Schottky.

## 4. Full stabilizer arithmetic, not just two-twist arithmetic

Let `V` contain both signs of the holonomy of every saddle connection of `q`, and let `Lambda=<V>_Z`. Endpoints are singular square vertices. Developing a segment through the square atlas keeps the integral grid invariant, so `V` is contained in `Z^2`.

To verify rank two without assuming every square vertex is singular, start a horizontal separatrix from a genuine singularity and follow square edges. At regular vertices the straight continuation and its predecessor are unique. There are finitely many oriented edge states. A path avoiding all later singularities therefore cannot repeat a state: reversing from the first repetition would force the same unique predecessors back to the initial singularity, yielding an earlier encounter. It must reach a singularity in finitely many steps. Stopping at the first such encounter gives a nonzero horizontal saddle connection. The vertical direction is identical. Genuine singularities exist because a closed nonsingular Euclidean surface has Euler characteristic zero, whereas `2-2g < 0`. Thus `Lambda` has rank two and, as a subgroup of `Z^2`, is a lattice.

An affine automorphism preserves the singularity set and takes a saddle connection, with no singularity in its interior, to another one. Its globally defined derivative up to sign therefore maps `V` to `V`. Its inverse gives equality `M Lambda=Lambda`. This uses no orientability of the foliations. The total flat area is finite and unchanged by a bijective self-map; local area scaling by `det M > 0` then yields `det M=1`.

After an oriented lattice basis change every projective derivative belongs to

`L = SL(Lambda)/{+/-I} ~= PSL_2(Z)`.

This controls the full stabilizer, because the affine realization theorem is for that full stabilizer. Surjectivity onto `L`, faithfulness there, and finite index in `L` are all unnecessary.

The faithful derivative image `J` of `H` lies in `[L,L]`, since `H <= [F,F]`. Write `K=[L,L]`. From `L=C_2*C_3`, its abelianization is `C_2 x C_3` and `K` has index six. The kernel acts freely on the Bass-Serre tree: it intersects each conjugate of either finite vertex group trivially. Its quotient graph has six edges and `3+2` vertices, so `K` is free of rank `6-5+1=2`.

## 5. A fixed finite core bounds conjugacy fusion

Realize the finitely generated free group `K` by a finite rose. Let `X` be the connected covering associated to the finitely generated subgroup `J`, and let `Y` be its finite core supporting cyclically immersed closed paths. The basepoint tail is excluded. Nontrivial `J`-conjugacy classes correspond to oriented free homotopy classes of nontrivial loops in `X`.

Fix one `K`-conjugacy class meeting `J`, and choose a nonempty cyclically reduced representative word `w` in a fixed basis of `K`. Tighten a loop representing any `J`-class in this ambient class. Its projected cyclic word is `w` up to rotation. Choosing a point along the loop gives a based closed path with label exactly `w`. It lies in `Y`. For any specified initial vertex, the covering property makes the path with label `w` unique. Hence there are at most `|V(Y)|` possible loops and at most that many `J`-conjugacy classes.

This is an upper bound even if several vertices give the same free homotopy class. If `w=z^e`, the same path-uniqueness argument still applies at each initial vertex; the number of letters and the exponent never enter the bound. A potential counterexample based on long words or roots therefore fails. In the identity class there is only the identity, although the application uses only nonidentity classes.

For fixed representatives `r_1,...,r_6` of `L/K`, every `L`-conjugate of `x in K` lies in a `K`-conjugacy class of some `r_i x r_i^(-1)`. Normality ensures these are in `K`. There are at most six such classes, each meeting `J` in at most `|V(Y)|` classes. Therefore one `L`-class contains at most

`C = 6|V(Y)|`

intrinsic `J`-classes. Since `J` is fixed once `g,k,a,b` are fixed, `C` is independent of all equal-trace words, their lengths, and their spectral values.

## 6. Mapping-class conjugacy and derivative kernel

Let nonidentity `x,y in H` satisfy `t x t^(-1)=y` in the ambient orientation-preserving mapping class group. The element `y` preserves both `D(q)` and `tD(q)`. The unique invariant-disk theorem applies because `y` has already been shown pseudo-Anosov. It follows that `tD(q)=D(q)`, so `t` has an affine representative and its projective derivative belongs to `L`. In particular the derivatives of `x,y` are `L`-conjugate.

The derivative map restricted to `H` is an isomorphism onto `J`, so it is also a bijection on their intrinsic conjugacy classes: a `J`-conjugator lifts to `H`, and injectivity recovers the conjugacy upstairs. All intrinsic `H`-classes contained in one ambient mapping-class class therefore lie in one derivative `L`-class. The bound `C` applies.

There is no need to lift arbitrary `L`-conjugators, and there is no need for distinct elements in the full stabilizer to have distinct derivatives. Additional kernel elements do not invalidate a necessary implication. This also handles the possible ineffective finite center in genus two.

## 7. Last implication and normalization

The inspected Horowitz construction starts with a nonempty free word, keeps freely reduced nonempty words, and distinguishes cyclic conjugacy by a uniquely identifiable new syllable. Its sign choices give `2^m` classes. Its trace proof uses identities valid in arbitrary representations, rather than a generic-matrix argument. The visually checked recurrence uses exponents `2m` and `2m-1`, not `2^m`.

Since `H` is free on the checked pair, choose arbitrary `SL_2(R)` lifts of its two derivative generators and extend to a representation. The universal trace theorem applies to this actual representation. Every selected nonidentity word projects to a hyperbolic element, so its common lifted trace satisfies `|t_m|>2`.

For a determinant-one real matrix the characteristic polynomial is `z^2-t_m z+1`. Its two roots are real and reciprocal. For positive or negative trace the larger absolute eigenvalue is

`lambda_m = (|t_m| + sqrt(t_m^2-4))/2 > 1`.

The translation length in curvature `-1` hyperbolic space is `2 log(lambda_m)`, while the checked affine pseudo-Anosov formula takes one half of that length. Thus the actual pseudo-Anosov dilatation is `lambda_m`, and the logarithmic spectral value is `log(lambda_m)`.

Partition the `2^m` intrinsic `H`-classes into ambient classes. Each part has size at most the fixed `C`, so there are at least `ceil(2^m/C)` ambient classes with this spectral value. For any `N`, choose `m` with `2^m > C(N-1)`. This gives at least `N` classes with fixed `g,k` and `H`. It proves the target without selecting primitive words or requiring one spectral value for every `N`.
