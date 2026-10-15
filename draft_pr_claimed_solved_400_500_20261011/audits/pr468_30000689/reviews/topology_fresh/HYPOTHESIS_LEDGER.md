# Hypothesis ledger — assigned topology dependencies

All entries refer to the frozen proof together with its explanatory addendum. `Verified` means the hypothesis or implication was independently checked in this audit; it is not a novelty or full-manuscript certification.

| Dependency | Exact input needed | Evidence / check | Status |
|---|---|---|---|
| Source local structure | Finite triangulation of a topological 4-manifold is combinatorial | Low-dimensional links; nested coordinate/conical neighborhoods force simply connected vertex links; 3D Poincaré and PL uniqueness; DFL p. 797 | Verified |
| Move ball | A legal bistellar support `α*∂β` is a standard PL 4-ball with common boundary `∂α*∂β` | Join formula; legal link and missing-face conditions | Verified |
| Local flatness | Boundary is locally flat in the ambient PL 4-manifold | Vertex link is a PL 2-sphere in a PL 3-sphere; 3D PL Schoenflies and lower link pairs | Verified |
| Complement manifold | Compact PL 4-manifold with boundary and collar | Local flatness of the support boundary | Verified |
| Complement connectedness and `π_1=0` | For extending the prescribed triangle boundary | Collared van Kampen decomposition of `S^4`; reduced `H_0` Mayer–Vietoris | Verified |
| Complement acyclicity | Integral homology, including degree-four-to-relative-degree-four map | Relative fundamental class restricts with degree `±1`; pair homology sequence | Verified |
| Complement contractibility | CW type, simple connectivity, acyclicity | Hurewicz and Whitehead | Verified; no PL standard-ball claim |
| NW structural support | `T` induced in augmented old complex | Old induced ball; a common missing triangle cannot lie entirely on its vertices | Verified |
| NW removed star | All old simplices containing `α` remain in `T` | Legal move plus common triangle cannot contain `α` | Verified |
| NW `(I.a)` | Old intersection cochain zero for disjoint pairs involving old support | Complementary filling disk with interior in complement; embedded old skeleton | Verified |
| NW `(I.b)` and agreement | New cochain zero on new support pairs; same map on `K∩L` | Boundary-fixed ball homeomorphism and common exterior map | Verified |
| General position | Continuous maps may be replaced by general-position representatives without losing support conditions or agreement | One map on finite union `K∪L`; sufficiently close common approximation; finitely many separated compact image pairs | Verified |
| Disk regularity | Only a map of the added triangle is required | Its interior avoids the 1-skeleton by relative PL general position; self-intersections are allowed | Verified; no embedded-disk assumption |
| NW `(II.a)` | Vertex outside old and new supports | Induced proper ball cannot exhaust a closed sphere; insertion/deletion support vertex cases accounted for | Verified |
| NW `(II.b)` | `H̃_i(K-W;Z2)=0` for `i=0,1` and specified common support faces | Cone `Q[W]`; Alexander duality; complementary induced deformation retraction; 2-skeleton homology; triangle attachment | Verified |
| Homological cones | Cone chains avoid support vertices not in their original face | NW Lemma 5.2 with the exact low homology just verified | Verified |
| Common triangle transfer | Nonzero old obstruction implies nonzero new one | NW Theorem 5.3, including preceding structural hypotheses | Verified |
| New triangle classification | Only `(p,q)=(2,2), M=α` or `(3,1), M=v*β` | Face-change and minimal-nonface analysis; vertex insertion/deletion checked | Verified |
| `(2,2)` case | Same augmented abstract 2-complex | Old plus `β` equals new plus `α` | Verified |
| `(3,1)` cone complex | Old unaugmented skeleton, with no old missing triangle assumed | Same cone/Alexander-duality calculation; old skeleton embeds as subcomplex of new | Verified |
| Witness cycle | Replacements preserve boundary formula and disjoint supports | Chain map from formal 2-skeleton on seven vertices; support-avoiding cones | Verified |
| Added triangle partner | Added `M` occurs in no other replacement chain, and pairs only with `∂α` | All cones are in old skeleton; complementary four vertices are exactly `α_0` | Verified |
| Local linking | `lk_2(∂M,∂α)=1` in punctured topological sphere | Complementary-space geometric local ball, one intersection; exterior edges avoid support | Verified |
| Evaluation | Witness pairing with obstruction equals one | Embedded unaugmented skeleton; linking/intersection boundary relation | Verified |
| Flag base | `sd(S)` has no missing triangles | Order-complex chain characterization | Verified |
| Pachner theorem | Two closed combinatorial manifolds in same PL class | `sd(S)` is subdivision of this `S`; Lickorish 5.9 | Verified; exotic class allowed |
| Topological obstruction | Nonzero mod-2 van Kampen class prevents arbitrary topological embedding | Normalized difference equivariant map forces class to vanish; NW Section 2 | Verified |
| Weber source category | Finite polyhedron; semilinear equals PL | Weber Section 1 | Verified |
| Weber existence bound | `2m≥3(n+1)` | Original Theorem 1, printed p. 2 | Verified |
| First metastable case | `n=3,m=6` | `12=12`; inequality is non-strict | Verified |
| Deleted product input | Full continuous equivariant map exists | Normalized differences from putative topological embedding in `R^{2d}` | Verified |
| Omitted ambient point | Image is proper in `S^{2d}` for `d≥1` | Invariance of topological dimension | Verified |
| Final contradiction for `d≥3` | No PL embedding from Section 2 | Algebraic and ambient-extension inputs are outside this assigned audit | Conditional on separate verification |

No unresolved topological hypothesis was found. No empirical computation is used as a substitute for these deductions.
