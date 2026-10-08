# 2. Compact-leaf stabilizers and geometric finiteness

## Attempt

Use a surface subgroup and its well-controlled Kleinian limit set to create the boundary gap. This differs from the direct side-domain route: the certificate is an algebraic stabilizer with a cocompact action on a leaf.

## Lemma 2: orbit and compact-leaf limit sets agree

Let Gamma act properly discontinuously by isometries on H^3. Let L be a nonempty proper plane, with H <= Gamma its stabilizer. Assume H acts cocompactly on L. Then Lambda(L)=Lambda(H), where Lambda(H) is the accumulation set of Hx for any x in L.

Proof. Choose a compact K subset L with HK=L and x in L. The continuous distance to x has a maximum R on K. For y=hk in L, d(y,hx)<=R, so L lies in the R-neighborhood of Hx. Conversely Hx is a subset of L. Sets at bounded Hausdorff distance have identical ideal limit sets. To verify the last statement, use the hyperbolic distance formula in a ball model, or the Gromov-product inequality (y_n|z_n)_o >= d(o,y_n)-R when d(y_n,z_n)<=R. If y_n goes to a visual-boundary point and z_n stays within R, z_n goes to the same point. Both inclusions follow.

For a compact incompressible leaf of a foliation, a lift is its universal cover, the stabilizer is its image fundamental group, and the quotient of that lift by the stabilizer is the compact leaf. Thus the hypothesis applies. This is a statement about the actual leaf subgroup, not an arbitrary surface subgroup elsewhere in the manifold.

## Restricted consequence

Suppose the foliation is closed, taut, and two-sided branched, and it has a compact leaf with quasifuchsian stabilizer H. By the definition/standard characterization of a quasifuchsian surface group, Lambda(H) is a Jordan curve. A Jordan curve is a proper closed subset of S^2 with empty interior. Lemma 2 and Calegari's credited Section 2.5 alternative give the requested asymptotic separation. More generally the same conclusion holds if the stabilizer is already known to have a proper limit set.

No universal classification of all leaf stabilizers is used. In particular, infinitely generated stabilizers and trivial stabilizers of noncompact leaves cannot be treated by replacing the leaf with a cocompact group orbit: that replacement fails its hypothesis.

## Why virtual fibering does not finish this route

A finite cover of the ambient manifold admitting some fibration supplies a different foliation. The question concerns the pullback of the specified foliation. Its universal lifted planes and their visual limit sets are unchanged by passing to that cover. Thus existence of a fibered finite cover does not produce a compact quasifuchsian leaf of the given foliation. Fiber subgroups themselves have full ambient limit set in the closed hyperbolic mapping-torus case, so they are not the intended gap-producing certificate.

Remaining gap: establish the existence of an appropriate cocompact leaf subgroup for an arbitrary two-sided taut foliation, or replace the orbit argument with control on noncompact leaves. Neither is done here. The restricted theorem is an elementary consequence of credited theory, not a new general solution.
