# Independent audit: exact KS, spin tensors, cohomology and setup

Audit time: 2026-10-06T21:31:00-07:00. Source checkout read only, specified pin `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. No source clone writes, git operations, publications or external communications were performed.

## Scope and status

I read `introduction.tex`, `setup.tex`, `cohomology.tex`, `exactks.tex`, and `auxiliary.tex` in full, at:

`/Users/alec/Desktop/math/preprints/The-rational-Hodge-conjecture-for-products-of-K3-surfaces-October-4-2026/build/manuscript/`.

I also read the September 30 quadratic-locus companion's precise general criterion (`paper.tex:100–161`) and its ordinary-Hodge proof (`369–844`), plus the CM companion's introduction and theorem statement. I checked primary Pridham and Stacks sources for the cited semiregularity/effectivity scope. I did not audit `mixed.tex`, the later realization proof, the full CM proof, or any Lean declarations/builds. A satisfactory audit of these algebraic sections is **not** independent certification of the realization proposition or of the mixed-product theorem.

Conclusion of this slice: no confirmed counterexample or irreparable algebraic error was found in the assigned sections. The strongest independently checked implication is **conditional**: an algebraic exact full-even-Clifford KS tensor supplies the ordinary rational Hodge conjecture for all powers of its K3 surface through the companion criterion. The essential geometric realization premise remains outside the verified portion of this slice. Accordingly mathematical-resolution completion toward the unconditional original target is not established; this audit slice is approximately 90% complete, publication-package completion contributed by this slice is 0%.

## Exact statements and dependency graph

1. The Oct. 4 main claim (`introduction.tex:14–22`) is rational HC in every codimension of every finite product of arbitrary projective complex K3 surfaces; factors may repeat and no period/field relation is imposed (`24–28`). It is stronger than separate self-power HC.

2. The realization proposition (`setup.tex:65–92`) concerns a quartic symplectic K3 or a point times the standard torus. Its assumptions are even torus dimension parameter `g`, real dimension `2n` with `n >= 12` (`14–27`); a rational middle-degree class `a` killed by the product symplectic form; and injectivity of `H^1(D,Q) tensor Z -> H^3(D,Q)` for its degree-two annihilator `Z`. It concludes a perfect complex on an ordinary mirror after field extension/abstract embedding into C, a bound `dim Ext^2 <= b_2(D)-dim Z`, and Euler tests with one common **nonzero rational scalar**. Those tests alone do not identify a transcendental cohomology component.

3. The dictionary makes this limitation explicit: Euler tests determine `C|_{P_B}=C_*|_{P_B}`, and determine all of `C` only in the torus-only case (`cohomology.tex:113–138`). This is not circular identification of the mirror transcendental Hodge structure. That structure is instead determined by the Ext/cap rank calculation.

4. The exact KS theorem (`exactks.tex:32–43`) promises a cycle in `CH^2(S x A_S^2)_Q` acting on `T(S)` by the specified tensor form of

   `j_w(v)(x) = v x w`, with `H^1(A_S,Q)=C^+(T(S),q)`.

   The quantifiers include every rational nonisotropic `w`, every full even-Clifford realization and every rational polarization. This is much more specific than existence of some nonzero Hodge map from `T(S)` into an abelian realization. Its proof depends directly on the realization proposition (`253–258`), sharpness of the cap rank (`263–383`), and deformation/specialization (`395–515`).

5. The auxiliary proposition (`auxiliary.tex:12–72`) uses a totally real **Galois** field `F'`, an `F'` quadratic space of dimension `d' >= 5`, `d' = 5 mod 8`, signature `(2,d'-2)` at every real place, and Witt index at least two. It claims algebraicity of a trace contraction tensor in `(End W')^{tensor 2}`, `W'=Res C^+(V')`, converted to four ordered `H^1` slots. Independent period planes are allowed at all real places. This is a second use of the same realization proposition, now torus-only (`97–178`), plus the same semiregularity propagation (`180–192`); it is not a consequence of exact KS for a single K3.

6. The mixed proof has two additional theorem inputs visible already in the introduction (`99–106`): the AKS general self-power criterion and the full CM abelian HC theorem. The CM input is another upstream breakthrough, not a classical theorem established by the citations to Deligne/André alone. I checked its statement (`CM/sections/01-introduction.tex:17–29`) but not its proof, so it remains unverified here.

## Algebraic checks actually performed

### Exact Clifford tensor and rank rigidity

The full even Clifford construction has dimension `2^20` for the initial 21-dimensional primitive space, giving torus parameter `g=2^19` (`exactks.tex:66–123`). Restriction to the split rank-three `U` makes the weight-one space a multiple of the standard two-dimensional SL2 representation. Over C, the spin module is `M_1 tensor H`, with `dim M_1=2^9`, while the regular module has a multiplicity factor `R_0`.

The chosen separated powers (`156–164`) distinguish contraction, derivation and wedge terms. For exponents 4, 7 and 10 the nine resulting exterior degrees are distinct and are larger than degree two (`208–213`); the large torus dimension places the relevant symplectic wedge maps in their injective range. The scalar-commutant conditions on two extra invariant tensors remove the regular-representation multiplicity freedom. They are described as a nonempty rational Zariski-open condition (`137–146`), rather than silently treating the regular module as irreducible.

The formal annihilator proof (`192–248`) has a coherent dimension count: projection to `N plus Q t_0` is injective, and each of those 19 lowering directions occurs through simultaneous spin action. Its projection to the K3 degree-two factor also proves the required wedge-injectivity.

The subsequent rigidity argument has a real normalization step. The nonzero actual transcendental component gives a rational Hodge realization of the simple three-dimensional `T(B)` in tensor powers of the non-CM elliptic `H`. The resulting identification is a similarity; rational isometry of the underlying odd-dimensional forms makes the similarity multiplier a rational square (`301–314`). The image in `N_C` has dimension at least 14, exceeding the maximal isotropic dimension nine (`319–327`), so a nonisotropic direction can be chosen. Its 17-dimensional perpendicular Clifford algebra has two-dimensional commutant on `M_1`, spanned by `1` and `Delta Gamma_x` (`329–338`). The final equation forces `c^2=1` (`351–373`). Thus the proof does not stop at an unspecified scalar multiple of a KS map.

All this remains contingent on the existence and extension bound of the perfect complex. It does not itself construct that complex.

### Realization choices

Right multiplication by an even Clifford element is a Hodge endomorphism for the left spin action. The change from volume-element right multiplication to arbitrary `w` is therefore made by an algebraic abelian endomorphism (`exactks.tex:436–445`). Restriction of `C^+(h^perp)` to `C^+(T(S))` is a rational weight-one sub-Hodge structure, split by abelian correspondences (`497–514`); the action `v x w` preserves the subspace. Changing lattice/isogeny realization or rational polarization uses weight-one Hodge morphisms, hence rational abelian homomorphisms. This justifies the stated realization dependence, provided the initial full primitive exact tensor is algebraic.

The polarization-degree comparison keeps only a polarization **line**: a rational ample vector of square `2d` need not be primitive integral with that square (`447–460`). The text correctly says its primitive integral representative can differ by a rational square and uses Witt extension to compare lines. Buskin then supplies an algebraic rational Hodge isometry on the two K3s, and the Clifford Hodge isomorphism is induced by an abelian isogeny up to rational multiple (`461–481`). I found no dropped integral assumption in this step.

### Auxiliary tensor boundary conditions

The torus for four copies has `g=[F':Q] 2^{d'} >= 32` (`auxiliary.tex:97–136`), consistent with the dimension of `C^+(V')`. The 6, 9 and 12 powers give disjoint degree triples `(10,12,14)`, `(16,18,20)` and `(22,24,26)`, disjoint also from `(2,4,6)` of the degree-four tensor (`138–149`). The copy matrices force an annihilator with identical diagonal blocks on the four copies. The off-copy multidegree projection then proves wedge-injectivity (`151–169`): an `H^1` input from copy i is paired with an injective degree-two projection on copy j != i, while other inputs land in different multidegrees. This addresses an actual boundary requirement rather than assuming wedge-injectivity from primitiveness alone.

The Witt-index assumption provides the common split ternary SL2 starting point (`75–95`). Without that hypothesis the proof as written does not apply. The proposition cannot be quoted for arbitrary spin abelian varieties after deleting it.

## Semiregularity and propagation

The cap action factorization through `Ext^2` and the rank implication are explicit (`cohomology.tex:230–260`); equality of the cap rank with the upper bound forces injectivity of the trace, not simply existence of a small Ext space.

For the propagation proposition (`272–291`), the premises are a smooth projective family over a smooth complex algebraic base, a perfect complex at one fiber, a horizontal Chern character staying Hodge on the base germ, and injectivity of the **full** semiregularity trace to all `H^{j+2}(Omega^j)`. The concluding all-fibers assertion additionally requires a global parallel Hodge section and connected base. It is not an unrestricted variational-Hodge claim for arbitrary algebraic classes.

Primary-source checks on 2026-10-06:

- [Pridham, arXiv:1208.3111v4](https://arxiv.org/html/1208.3111v4), introduction and Corollaries 2.24–2.25, explicitly treats perfect complexes, all square-zero obstruction classes, and moving smooth ambient families; the obstruction image measures whether the horizontal Chern character remains in the Hodge filtration. This supports the scope of the formal lifting step.
- [Stacks Tag 0DIG](https://stacks.math.columbia.edu/tag/0DIG) provides effectivity for the compatible pseudo-coherent tower; [Tag 0DJZ](https://stacks.math.columbia.edu/tag/0DJZ) supplies relative perfectness for proper flat finite-presentation families when the closed-fiber restriction is relatively perfect. The manuscript checks the proper/flat/finitely presented and closed-fiber hypotheses (`348–358`).

The proof also separately spreads the formal complex and uses proper relative cycle parameters plus uncountability (`359–383`). This is needed to conclude algebraicity on all fibers; merely extending a perfect complex formally would not alone establish that conclusion. I found no decisive defect in those passages, but the paragraph-level spreading argument has not been formalized or independently rebuilt in this audit.

## Checked conditional self-power implication

The exact AKS input is the September 30 companion's `Theorem 1.1`, `paper.tex:151–158`: for one rational nonisotropic `w`, one rational polarization, and one **full even-Clifford** realization, a cycle inducing the exact `j_w` implies rational HC and GHC on every self-power. I only certified the ordinary-HC argument needed here, not its GHC extension.

Its key construction (`439–601`) alternates compositions of `j_w`:

`F_k(alpha)(1) = c_k(alpha) w^k`.

The Clifford PBW decomposition and invertibility of `w` prove injectivity of `F_k` for all `1 <= k <= dim T`; there is no stable-range omission. Composition contracts polarized `H^1` slots algebraically. The correspondence has codimension `k+1` from `S^k` to `A^2` (`518–540`). An algebraic adjoint using an ample class gives an invertible composite on the exterior summand; a rational polynomial inverse supplies an algebraic left inverse (`542–594`). A rational exterior Hodge class thus maps to a divisor, and its return is a codimension-k cycle. This avoids presuming all HC for the abelian target.

In particular the exterior-volume argument takes **operator composition**, not the scalar trace of a Clifford word, so it does not accidentally kill the SO determinant generator. At the top degree `t`, if `t` is odd, the volume `z` and `w^t` are both odd and their product is a nonzero even element; if `t` is even, `z` is even and `w^t` is a nonzero scalar. In either case evaluation at `1` already proves the nonzero image. The only subsequent scalar pairing is the polarized cohomological adjoint, whose restriction to a sub-Hodge structure is nondegenerate by Hodge–Riemann. The degree-two image is algebraic by the Lefschetz (1,1) theorem, not by any assertion that arbitrary Hodge classes on KS abelian powers are algebraic.

The remaining ordinary-HC assembly (`726–844`) uses the actual Zarhin Hodge groups. In the totally real case the newly algebraic exterior volume tensors supply the special-orthogonal generators and recover the individual endomorphism-field projectors. In the CM-field case norm-one elements span the endomorphism field, Buskin algebraicizes them, and general-linear invariants are generated by the standard-dual pairings. Coefficient extension is followed by explicit rational descent. The rank-two transcendental/CM case and repetitions are covered by the group statements and exterior-degree limits. This establishes a meaningful conditional theorem without presuming the restricted quadratic locus.

## Exact remaining gap and decision effect

The first unverified premise in this slice is `setup.tex:77–91`: existence of a perfect complex with the common Euler normalization and required second-extension bound for the particular constructed rational primitive inputs. The assigned files only state that proposition and use it; they do not prove it. The proof is deferred to topology/curvature/comparison/realization sections (`setup.tex:102–108`). A defect there invalidates both the exact-KS input (`exactks.tex:253–258`) and the auxiliary spin tensor (`auxiliary.tex:97–178`), and consequently prevents promoting the unconditional mixed-product assertion or any moduli transfer based on it.

The Oct. 3 universal KS companion explicitly promises fixed normalization and full even-Clifford target (`manuscript.tex:57`, theorem `109–120`), so its headline is sufficient in **scope** for AKS. Its mirror-realization mechanism overlaps this proof; simply citing its theorem instead would move the central problem to another unsupported claim unless that companion is separately validated. This audit does not establish an independent fallback proof.

The CM theorem's full proof and the relations among different K3 factors are additional unchecked premises. Separate self-power HC does not by itself imply HC for products of different surfaces (`introduction.tex:108–122` explicitly recognizes this).

I recommend retaining the conditional motive-transfer result and exact list of dependencies until the geometric realization, CM theorem where actually used, and mixed-product proof pass independent validation. This is an evidence boundary, not a claim that the main result is false.

## Source hashes

SHA-256:

| File | Hash |
| --- | --- |
| exactks.tex | a9a7aeaebd251e193e4790dc650504386404c13fb3fa91cadcad73ffc3b1fd87 |
| cohomology.tex | a1d4ec1325dcb9a4e618476e96927b2ba3396ba519547842e6f223f6db066e92 |
| auxiliary.tex | f22972ef19438c508be5fd929b3ef3c58c9f932b617c3f03bde09bc4f1b9935d |
| setup.tex | f5d66939d1eea98d1d2172f0c73746d32bd60f313cae0373879d091a1632e850 |
| introduction.tex | 42c25b383ddeae70cab529e89ffdf319880696eeaca2b640174c18855d6c4539 |
| AKS build/paper.tex | 9db1b5c004f313afa269e1cd2a918842460623df711c3b8500d36a5a024155d9 |
| CM 01-introduction.tex | cfaf3d085e9138e9818754cf3493a55be497e57a2c0432242f4dae5089f4720a |
