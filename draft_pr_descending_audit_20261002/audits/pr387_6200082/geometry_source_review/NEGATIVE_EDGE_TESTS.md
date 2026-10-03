# Negative and boundary checks for PR387

These are analytic edge tests, not finite computations claimed to prove an existence constant.

| Check | Explicit calculation/mechanism | Audit result |
|---|---|---|
| Rank0 or rank1 | Empty/two-point limit set has Hausdorff dimension0. A cyclic convex-cocompact generator is loxodromic, not parabolic. | Included; no exception. |
| Wrong spectral branch | At delta=0, delta(3-delta)=0; the correct lower branch is9/4. At delta=1, the wrong quadratic gives2 rather than9/4. | Applying the upper formula to every delta would fail; candidate correctly splits. |
| Threshold | At delta=3/2, delta(3-delta)=9/4. | Branches join, with no strict-threshold gap. |
| Claimed approach to3 | delta=3-epsilon gives lambda0=3epsilon-epsilon^2 ->0. | Contradicts any common c>0; confirms the required quantifier is uniform in G. |
| c truncation | c=min(h_*^2/4,1) gives9-4c>=5 and D>3/2. | Square root is real; low branch fits; no need to assume an unproved bound h_*<=3. |
| Quadratic sign | For delta>=3/2,2delta-3>=0; (2delta-3)^2<=9-4c implies the upper-root inequality. | Correct root chosen; without branch condition only an interval follows. |
| Degree choice | For finite-index N of F_r, rank(N)=1+[F_r:N](r-1). Thus b1(N)/index = r-1+1/index, which does not vanish for r>=2; b2(N)=0. | Degree2 is essential. This does not extend the same mechanism to degree1/H2. |
| Missing subgroup quantifier | Showing b2(G)=0 alone says nothing generally about all finite covers of all finitely generated subgroups. Here each is a free graph group, so every ratio is0. | Full G2 condition verified, not inferred from one Betti number. |
| Torsion/reflections | A reflection has order2; a free group is torsion-free. Any point stabilizer is finite. | Reflections excluded by hypotheses; action free. |
| Orientation | Infinite-order glide/loxodromic orientation reversal can occur without a fixed point. Pass to orientation subgroup of index<=2 if desired; limit set unchanged. | Full Isom scope retained. |
| Compact Cheeger misuse | A compact complete hyperbolic manifold has lambda0=0 while its half-volume Cheeger constant is positive. | Completeness by itself does not justify bottom-spectrum inequality; target quotient is infinite volume. |
| Convex-core boundary misuse | The spectral formula concerns complete H4/G, not the compact convex core equipped with arbitrary boundary conditions. | Candidate uses the right ambient quotient. |
| Parabolic elementary impostor | For cyclic parabolic G, Hausdorff dimension is0 but critical exponent is1/2. | No universal delta=HD statement for all discrete groups; convex cocompact excludes this case. |
| Snowflake metric | dim_H(X,d^a)=dim_H(X,d)/a. | Metric normalization needed; candidate correctly fixes round/normalized visual metric. |
| Classical-only source | A dimension gap for round-ball classical Schottky generators need not control all free convex-cocompact representations. | Candidate instead uses full free-G2 class, so no restricted-class leap. |
| Arbitrary free infinite-volume group | Cheeger alone controls spectral bottom, while full-limit-set Hausdorff dimension need not equal critical exponent outside the geometrically finite/convex-cocompact regime. | No unproved extension to geometrically infinite full limit sets. |
| General G2 status without residual finiteness | Betti vanishing does not itself imply residual finiteness. | Verified independently via actual finite-generation/linearity or free-group residual finiteness. |
| Lattice witness mismatch | A free target is not a positive-middle-Betti uniform lattice. The theorem uses a separate fixed Lambda. | Separate witness, correctly selected; no circularity. |

Source scope and precise formulas are in GEOMETRY_SOURCE_REVIEW.md. Negative tests do not independently certify the all-net approximation construction; that central step requires its own adversarial audit.
