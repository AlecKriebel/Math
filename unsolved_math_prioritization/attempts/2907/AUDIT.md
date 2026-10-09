# Independent audit of the reconstructed KP 4.31 / 2907 turn-3 report

Edition note: the full mathematical audit and its qualifications are retained. The single local-storage pathname in its input identification has been replaced with a descriptive filename. REPORT.md now applies the required Section 7 correction and the optional common-collar strengthening; this audit originally examined the reconstructed input digest below, not the later editorial byte sequence. PRECISION_OVERLAY.md is preserved verbatim.

## Verdict and exact scope

**ACCEPTED AS A PARTIAL LOCAL RESULT, WITH THE SCOPE CLARIFICATION IN `PRECISION_OVERLAY.md`.**

The reconstructed report correctly proves that every nonzero power of the specified boundary twist has no continuous extension to the open complement of Zhang's two annuli. Its resulting annular family is pairwise inequivalent by homeomorphisms fixed pointwise on the entire boundary sphere. The abstract complement groups and first homology groups are, respectively, `F_2` and `Z^2` throughout. The fixed cobordism construction realizes any specified smooth oriented knot as the exact boundary, with common genus `h+2`.

This is not an acceptance of a solution of KP 4.31. Neither outer-boundary-relative topological equivalence of the connected grafts nor survival of smooth inequivalence after grafting has been established. The original problem remains **UNSOLVED, turn 3/5**. This audit does not add a turn, propose a new approach, publish anything, or authorize a queue change.

One sentence needs a precise reading: being the identity on the **surface** cobordism `S` does not imply being the identity on the entire internal `S^3`. The local obstruction applies when an ambient comparison actually fixes that entire sphere, for example by being the identity on the **ambient** product shell `S^3 x [0,1]`. Section 7, item 3 of the frozen report must not be read as asserting the stronger implication about the surface alone. The overlay supplies replacement wording. This does not change the local theorem or the unresolved global status.

## 1. Frozen object and independence of this examination

The object audited is:

- Reconstructed input titled `TURN3_PARTIAL_REPORT_RECONSTRUCTED.md`
- Byte count: `15061`
- SHA-256: `e5f6b869aac42975f0f2a05f9cd3e8ba57b20547377c142c2e9ab6c4ed22fcaa`

Those values were independently recomputed before the mathematical examination. The report was read in full. The earlier report, any lost bytes, any preliminary reading, and any prior acceptance were not treated as evidence that this object is correct. The frozen report and its supplied manifests have not been edited. The audit's final manifest records the recheck of their preservation.

This is a mathematical audit of the stated argument and the source geometry it needs. It is not a formalized proof, an exhaustive check of every theorem in Zhang's paper, or an independent proof of the Smale conjecture. Standard facts used explicitly below are van Kampen, product tubular neighborhoods and collars, elementary free-group theory, and elementary oriented surface-cobordism constructions.

## 2. Primary sources actually checked

### Zhang

Cindy (Suixin) Zhang, *Exotic Surfaces in 4-manifolds and Surface Corks*, arXiv:2604.27545v2, May 25, 2026.

- [Version record](https://arxiv.org/abs/2604.27545v2)
- [Versioned PDF](https://arxiv.org/pdf/2604.27545v2)
- [Versioned HTML](https://arxiv.org/html/2604.27545v2)

The version record, HTML, and public PDF were opened independently in this audit. The record identifies v2 and its May 25 revision date; the PDF has 24 pages. The supplied local PDF was separately hashed and its metadata checked:

- Bytes: `4993293`
- SHA-256: `2204ba0bf4a5946526281ab80e147013a4058827a3f976907903eddabb2c51d1`

The local extracted text of Sections 4.3 through 6 was examined. Visual inspection covered PDF/printed pages 8-9 and 11-17, in particular Figures 2-3, 6-11, and 12-14. Pages 8-9 were freshly rendered from the checked PDF during this audit; pages 11-17 were read in the supplied local rendered images. The decisive checks are Proposition 4.2, Sections 5.1 and 6, Theorem 5.1, Corollary 5.2, and Figures 8-10 and 13. Source images are inspection material, not part of a publication payload.

The source is a preprint. No assertion about journal acceptance, publication, or wider expert validation is needed here. This audit did not independently download a second local byte stream of the PDF; its local-byte assertions are hash checks of the supplied copy, supplemented by independent inspection of the official online version.

### Hatcher

Allen Hatcher, *Algebraic Topology*, printed pages 23-24, PDF pages 32-33.

- [Author-hosted PDF](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf)

The official PDF was independently opened. Both relevant local page images were visually inspected. The local PDF identity is:

- Bytes: `8121741`
- SHA-256: `bebb3032bf9021b956da3bd070eb6c67dc662cf849be9cdf6679f677560e5618`

The Borromean diagram on printed page 23 and the group statement on page 24 verify that the remaining component is a nontrivial commutator in the free group of the other two-component unlink exterior. In particular, this is stronger than the statement that all pairwise linking numbers vanish.

## 3. Geometry: the required object really is a product of pairs

It would not suffice to know only that `C` is a standard ball or that its underlying manifold is `(I x P) union h_0`. The complement computation requires the two annuli to be the product traces of the correct circles in `P`. The source permits that stronger identification.

Start with the local coordinates of a traded two-handle,

`D^2_core x D^2_cocore`.

Removing a neighborhood of its extended core leaves, in the handle itself,

`D^2_core x (D^2_cocore minus an open central disk)`.

Write the punctured second disk as a circle times a radial interval. Each radial slice of this piece is a surgery solid torus. Its core is the circle at the center of `D^2_core`. The punctured cocore is exactly the union of those core circles as the radial parameter varies. The rest of the extended-core removal completes these slices across the old product region. Because the surgery framing is fixed, the completed slices have the same surgery identification. Thus the resulting identification with `I x P` can be chosen to carry the punctured cocore to the product of the surgery-dual core with `I`.

The two surgery curves are disjoint in `Q = Sigma x S^1`, since their circle coordinates are different. Consequently the two trades can be made in disjoint neighborhoods. One handle is attached at the negative end and the other at the positive end. Reversing the radial-to-interval identification for one of them changes its endpoint assignment, not the underlying product subset. This is consistent with the four endpoint assignments recorded on source page 15. That page explicitly identifies the radial interval of each punctured cocore with the interval of the product construction.

The cancellation must also track the dual cores. Figure 9 identifies the colored circles as meridians of the two additional surgery curves. In the passage to Figure 10, those colored circles are slid before the cancelling surgery pairs are removed. Figure 10 displays the surviving colored circles, together with the unfilled black component, in the Borromean crossing configuration. The two colored circles are therefore the components required in the product-pair model. They are not surviving copies of deleted framed components by unsupported relabeling.

One may apply the resulting three-dimensional identification of this marked `P` to every product slice. With `B_1,B_2` denoting these surviving dual cores and `B_3` the unfilled component, the relevant model is therefore

`(I x P, (I x B_1) disjoint union (I x B_2))`,

followed by the attachment of `h_0`. Here `P` is the exterior of the unknot `B_3`, with its boundary marking retained.

There is no need to mirror one end of this product when defining the product itself. The mirror in Figure 11 is the orientation convention for drawing the two ends as pieces of the oriented boundary of a four-manifold. Confusing that boundary-drawing convention with a change of the product identification could introduce a false monodromy. The report does not make that mistake.

**Finding:** the product-of-pairs input is supported, rather than merely assumed from an unmarked manifold identification.

## 4. The `h_0` attaching loop remains the meridian after the annuli are deleted

Knowing that the attaching curve generates `pi_1(P)` would not be enough. In a link exterior a generator of the filled solid torus can be altered by words in the two deleted components. This point therefore needs an argument in the complement of the tracked dual cores.

Before the two surgeries, the attaching circle of `h_0` is `{p} x S^1` in the upper copy of `Sigma x S^1`. For the standard two generating curves drawn in Figures 2-3, their spine has connected complement meeting the boundary of the punctured torus. Choose an arc `alpha` from `p` to `partial Sigma` avoiding that spine. Alternatively, the initial choice of `p` can be made in a boundary collar, as permitted by the construction. After making the surgery neighborhoods sufficiently small, the annulus

`alpha x S^1`

misses both surgery neighborhoods. It is contained in the unchanged portion of the surgery manifold and hence misses both surgery-dual cores. Its two boundary circles identify the attaching loop with the boundary `S^1` direction in the complement of those cores, not just after they are filled back in.

The peripheral identification in the Borromean model sends that boundary `S^1` direction to `mu_3`, while the `partial Sigma` direction is `lambda_3`. This agrees with Figure 8 and with the position of the extra red meridian in Figure 13; the latter is disjoint from the colored surface-boundary circles. The source also constructs `h_0` disjoint from the surface in Section 4.4.2.

All of these identifications can be based by a path in the same annulus and boundary torus. Other choices may conjugate the attaching word or reverse its orientation. They do not change its normal closure. Thus the relation added to the complement fundamental group is precisely the normal closure of `mu_3`.

The framing of `h_0` is needed for the standard-ball description, but it cannot add a second fundamental-group relation. For the group quotient a four-dimensional two-handle kills its attaching loop independently of its framing.

**Finding:** the meridional quotient used by the report is correct in the annulus complement, which is the stronger assertion the proof requires.

## 5. Complement group and noncentral longitude

Let

`M = S^3 minus int nu(B_1 union B_2 union B_3)`.

Product tubular neighborhoods of the annuli may be chosen disjoint from the `h_0` attachment. Up to the already checked marked identification and corner rounding, the compact exterior is

`E = (I x M) union h_0`.

Van Kampen gives

`pi_1(E) = pi_1(M) / normal_closure(mu_3)`.

This is the same group quotient as meridional Dehn filling on `B_3`. That filling restores the deleted solid torus in `S^3`, and the remaining two Borromean components form an unlink. Hence the quotient is the free group `F(x,y)`, with `x,y` a suitable based meridional free basis. This argument asserts a group identification; it does not assert a diffeomorphism between the four-dimensional exterior and a three-dimensional filling.

The image `d` of `lambda_3` is freely homotopic, after the filling, to the restored core `B_3`. The Borromean computation gives a conjugate of a commutator, up to orientation choices. The proof needs only:

1. `d` is nontrivial;
2. `d` has zero image in `F(x,y)_ab`;
3. `d` has infinite order.

The first two follow from the checked Borromean configuration and the standard calculation. The third follows because free groups are torsion-free, or directly by cyclically reducing a conjugate of the nontrivial commutator. Exact signs, order of the two meridians, and the conjugating path are immaterial.

For a free generator `x`, its centralizer is the cyclic subgroup generated by `x`. An elementary verification is to write any reduced word as `x^r u x^s`, where either `u` is empty or it begins and ends with a non-`x` letter. In the second case the reduced form of its conjugation of `x` retains letters from `u`, so it cannot equal `x`. If `d^k` commuted with `x`, it would therefore be `x^m`; zero abelianization forces `m=0`, which contradicts torsion-freeness for `k != 0`.

Consequently `[d^k,x]` is nontrivial for every nonzero integer `k`, including negative integers. No assertion that a particular based representative is literally `[x,y]` is necessary.

## 6. Boundary loop, upper face, and based naturality

Write `U = C minus A`, `Y = partial C minus L`, and let `j:Y -> U` be inclusion. The radial normal push gives a homotopy equivalence between `U` and a chosen compact exterior, so the computation above applies to `pi_1(U)`.

The upper face in `partial C` is not a complete, unchanged copy of `M`: the `h_0` attaching tube has been removed and replaced by the other boundary piece of the handle. The report explicitly acknowledges this. Its witness only needs a suitable based loop, not the missing full upper copy.

The lower inclusion `pi_1(M) -> pi_1(U)` is onto. Choose a loop `a` mapping to the selected free generator `x`. It can be taken disjoint from the attaching circle by general position in the three-manifold, keeping its basepoint on `T_3` fixed. Shrinking the attaching tube then makes the upper copy of `a` a boundary loop. Equivalently, with a tube already fixed, the usual displacement off a codimension-two circle gives a representative in its exterior. Thus `a_-` and `a_+` both genuinely belong to `Y`.

Choose the vertical path `v` on `I x T_3` from the lower basepoint to the upper one. Both endpoints are fixed by the twist. With left-to-right path traversal, the boundary loop

`q = v a_+ v^(-1) a_-^(-1)`

is null in `U`, using the product homotopy of `a`. That homotopy need not be contained in `Y`; containment in `U` is precisely what is required.

The actual twist direction is the `partial Sigma`, hence `lambda_3`, direction. A representative with torus coordinates `(s,u)` can be written

`f(t,s,u) = (t,s+rho(t),u)`,

where `rho` is 0 near the lower end and 1 near the upper end. Addition is modulo 1, so this is the identity near both end faces and pastes smoothly to the identity elsewhere on the boundary. It is supported away from `L`. Its `k`th power fixes the two chosen end loops and sends `v` to a path for which

`delta_k = f^k(v) v^(-1)`

represents `lambda_3^k` on the torus. Therefore

`j_*(f^k_*(q)) = d^k x d^(-k) x^(-1)`.

Inverting the convention for the twist merely changes `k` to `-k`. Changing a basepoint path conjugates the computation consistently and cannot turn a nontrivial element into the identity.

If a continuous map `G:U -> U` restricted to `f^k` on `Y`, it would fix the chosen lower basepoint and satisfy

`G_* j_* = j_* f^k_*`.

The left side sends `q` to the identity and the right side does not for `k != 0`. This proves the advertised continuous nonextension. It does not require `G` to be injective, proper, a homeomorphism, or a smooth map.

**Finding:** the null-loop obstruction is fully based and valid. The punctured upper face introduces no gap.

## 7. Pair invariance, collars, and arbitrary choices of smooth extension

A pair homeomorphism of `(C,A)` automatically restricts to a homeomorphism of `U`. It need not preserve a selected tubular neighborhood or compact exterior. Formulating the contradiction on `U` is therefore the correct fix for that possible invariance error.

Since the underlying ball is standard and the boundary twist is orientation preserving, a smooth extension of `f` exists. Here is an explicit way to remove any doubt about a common boundary collar for the entire family. Fix a collared presentation of `A` near `L`. Choose a smooth isotopy from the identity of `S^3` to `f`, stationary near both endpoints. Use its trace in a boundary collar, and extend by the identity on the remaining inner ball. Near the outer edge this extension is `f` times the normal-coordinate identity. Since `f` is the identity on a neighborhood of `L`, the extension is the identity on a fixed neighborhood of the collared `L`. Taking its integer powers gives extensions of all `f^k` with that same fixed collar.

The theorem is not dependent on this particular coherent choice. For any extensions `Psi_j,Psi_k`, a boundary-fixed homeomorphism `H` from `A_j=Psi_j(A)` to `A_k=Psi_k(A)` would give

`Psi_k^(-1) H Psi_j`

as a pair homeomorphism of `(C,A)` with boundary restriction `f^(j-k)`. Nonextension rules it out whenever `j != k`. This works even if the proposed pair homeomorphism is not required to label or orient the two annuli.

Moreover, two different extensions of the same `f^k` always yield boundary-relative equivalent pairs: `Psi'_k Psi_k^(-1)` is itself a boundary-fixed diffeomorphism between their images. Thus arbitrary smooth extension choices do not create a hidden ambiguity in the local equivalence classes.

The abstract complements are all diffeomorphic through the chosen ambient extensions, so their groups and homology do not change. What fails to be preserved is the inclusion kernel after fixing the boundary pointwise. The witness is therefore a marked-boundary invariant, not an abstract group or homology distinction.

No closed-pair contradiction follows. A homeomorphism between closed ambient pairs need not fix the exterior of this ball, preserve this separating sphere, or restrict to a homeomorphism of this particular local pair with its boundary marking.

## 8. Exact-knot shell and genus

The shell existence assertion is elementary and sufficient in the smooth oriented category. Give `L` the boundary orientation of `A`. Three oriented bands merge its four components to an oriented knot `J`. A finite sequence of crossing changes and isotopies takes `J` to a diagram of any specified oriented knot `K`. Each crossing change admits a smooth embedded oriented genus-one cobordism; equivalently, resolve the double point in a crossing-change trace by a local tube. A final ambient isotopy can end at the specified embedded representative of `K`, and product collars can be imposed at both ends.

The resulting connected cobordism `S` has five boundary components and some genus `h`, so

`chi(S) = 2 - 2h - 5 = -3 - 2h`.

The two annuli together have Euler characteristic zero. Gluing them to the four inner boundary circles of the connected `S` preserves Euler characteristic and gives a connected orientable surface with one remaining boundary component. It follows that

`1 - 2g = -3 - 2h`, hence `g = h+2`.

The orientations match because the inner boundary of the cobordism has the opposite orientation from the boundary of the annuli. The common boundary collar makes smoothing the seams uniform. Appending the ambient product collar to a standard ball again gives a standard ball, and the outer boundary identification can be fixed so that the remaining boundary is the requested exact `K`.

Nothing in this construction makes a topological comparison of the different grafts, nor does it provide an invariant that survives grafting. The calculation is a valid existence and genus calculation only.

## 9. Scope repair at the internal seam

The report calls `S` a shell, while it also uses an ambient shell `W = S^3 x [0,1]` in the construction. These must be distinguished.

- If an ambient homeomorphism of the grafted pairs is the identity on all of `W`, it fixes its inner sphere and its restriction to `C` contradicts the local theorem for distinct indices.
- More generally, a proposed comparison that preserves `C` and fixes all of `partial C` pointwise is ruled out directly.
- Being the identity on the two-dimensional `S` alone only fixes points of that surface; it does not imply pointwise fixation of the three-dimensional inner sphere.
- A homeomorphism fixed only on the outer `S^3` may move the internal sphere or induce a nontrivial map on it. The local argument says nothing conclusive about such a comparison.

The overlay replaces the ambiguous sentence. In particular, this audit does not treat the internal sphere, its torus cylinder, or any parametrization of the surface shell as an extra marking permitted in the original problem.

## 10. Final acceptance boundary

Accepted:

1. The marked product-of-pairs and peripheral meridional attachment in this specific source construction.
2. The complement quotient `F_2`, with `lambda_3` mapping to a nontrivial zero-abelianization element of infinite order.
3. Continuous nonextension for every nonzero twist power.
4. Boundary-pointwise pairwise inequivalence of the local annular images, independent of extension choices.
5. Constant abstract group and first homology across that local family.
6. The exact-boundary shell construction and genus `h+2`.

Not accepted or proved:

1. A solution of KP 4.31.
2. Outer-boundary-relative topological equivalence of the connected exact-knot grafts.
3. Smooth inequivalence surviving an arbitrary fixed cobordism shell.
4. Topological inequivalence of all those grafts.
5. The implication that fixing the surface shell alone fixes the full separating sphere.
6. Any inherited acceptance or byte-identical recovery of a lost report.

The correct disposition is a verified partial obstruction, with the one scope clarification supplied separately, while the original problem remains unresolved at turn 3/5.
