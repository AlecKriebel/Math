# Independent audit of graded rigidity and lattice transports

14 October 2026 UTC. Row 1775 / 30004611, the same shared substantive pass 4. This is an independent mathematical acceptance of the two specified artifacts, not another approach, a full solution of the broad source problem, or a novelty certificate.

## 1. Frozen artifacts and verdict

The accepted artifacts are:

1. `natural_sequence_rigidity.md`: 23,349 bytes; SHA-256 `ec3765d624575a0c047a9c81195bafd3923a342ce4fbf4ad3b8baadec7d5a237`.
2. `alternative_lattice_transports.md`: 17,696 bytes; SHA-256 `88de85b0ba24d5bc34899a227e53784c7df5b4429e12c7eb74fbb75a3745c94d`.

**Qualified mathematical acceptance.** No correction to either final artifact is required. The rigidity artifact's final revision strengthens its initial ordinary-map conclusion by proving epimorphism rigidity for reducible restrictions as well. I independently checked that added block argument rather than treating the earlier review as acceptance of the addition.

Accepted conclusions include:

- Complete degree-zero S-linear fixed-poset map classifications for D to ordinary restriction, E to Ziegler restriction, and D directly to Ziegler restriction.
- For each of the first two domains and targets, existence of any such sheaf epimorphism if and only if the canonical map is already onto. The ordinary assertion includes reducible global restriction arrangements.
- Explicit Hilbert-series obstructions independent of either arrow, including every stalkwise graded-free rank-one tensor twist in the specified shapes.
- Genuine ordinary and Ziegler short exact sequences for every marked hyperplane containing no nonzero deletion flat, with a rank-five example outside both previous local-freeness sufficient classes.
- The exact underived open-direct-image identification, its explicit nonzero higher-direct-image correction, and the failure of the usual recollement terms to equal the named deletion and restriction terms.
- The conditional obstruction to erasing a canonical defect by exact transport equipped with a compatible derived-global-sections comparison.
- The stated limited comparison with Everitt–Turner homology, including the different lattice endpoint and atom operation after graded dualization.

These conclusions remain scoped partials. They do not classify ungraded maps, arbitrary new modules, arbitrary comparison spaces, or all possible answers to Problem 6.3. No unrestricted freeness/cohomology criterion from Mücksch's retained v3 is used.

The audit read the accepted pass-1 construction and audit, both pass-2 authored components and their audits, and the pass-3 coloop proof and adversarial audit. The calculations below use the actual geometric-inclusion functors and retain every nonzero flat, including the bad line stalks.

## 2. Fixed-poset map classification: top stalk, all hyperplane stalks, and normal terms

Use the rigidity artifact's assumptions: A is central essential, ell>=3, H=ker(alpha), P is the nonzero-flat poset, and Q consists of flats in H. The target is extension by zero from Q. No arrow enters Q from its complement. Arrows leaving Q have zero target transition, so they impose no extra condition on a morphism with that target.

The top relevant stalk is H, not the ambient top V, where the target is zero. On Q every target map to H is an inclusion into Der(R), R=S/(alpha). Therefore a map at H determines all other components uniquely, and no nonzero map hidden at a smaller stalk can have zero H-component.

At H,

    D_H=(S tensor_K H) direct-sum S alpha partial_alpha,
    E_H=S tensor_K H,
    T_H=Z_H=Der(R).

A degree-zero S-linear map D_H->Der(R) is specified by a constant matrix A and a degree-one vector field v. It is exactly A rho+v nu, with nu(theta)=theta(alpha)/alpha modulo alpha. The normal term cannot be omitted. Changing the normal complement changes alpha partial_alpha by alpha times a tangential constant derivation, which every map to an R-module kills. Thus the parameter v, as well as rho and nu, is complement-independent. The map nu has coefficient degree -1; multiplication by v restores degree zero.

For every restricted hyperplane K, dim K=ell-2>=1, so its stalk remains in P. Put alpha=z and write its fiber equations as t+c_j z. The complete local logarithmic basis is

    z partial_z+t partial_t,   q partial_t,   partial_{u_i},
    q=product_j(t+c_j z).

The constant common directions force A(K) to lie in K. This is equivalent to beta_K A=lambda_K beta_K. The local Euler vector then forces beta_K(v) to be divisible by beta_K. Running over all K proves v in D(B)_1. Conversely these conditions preserve every ordinary tangency condition at every smaller flat. This checks necessity and sufficiency on all stalks, not only at a generic module prime.

For E, the top map contains only A. The same common directions force hyperplane preservation, which is sufficient for every multiplicity: beta_K(A eta)=lambda_K beta_K(eta) preserves divisibility by beta_K^{m(K)}. No characteristic-dependent multiplicity coefficient appears.

For a direct D-to-Z map, inclusion Z into T first gives the ordinary classification. At K, the degree-one Euler vector has beta_K-component (lambda_K(A)+lambda_K(v)) beta_K. When m(K)>1 this must vanish; the remaining generator reduces with exactly beta_K^{m(K)}, and common directions contribute zero. These conditions are sufficient because Ziegler membership is the intersection of these separate divisibility conditions. This verifies Theorem 3.3, including the additional normal-term cancellation at a multiple fiber.

As an additional kernel check, retaining the actual canonical ordinary injection I tensor F->D forces v=0: at H its image contains alpha partial_alpha, whose image under A rho+v nu is v. The final artifact does not confuse general maps with maps compatible with that chosen injection.

## 3. Epimorphism rigidity, including reducible ordinary restriction

For E->i_*Z, surjectivity at H in degree zero forces A invertible. An invertible constant matrix preserving each hyperplane has an inverse preserving each hyperplane, hence is an automorphism of the entire multiarrangement target. Therefore coker(A pi) is isomorphic to coker(pi). This is fixed-poset rigidity, with no additional family naturality.

The ordinary case genuinely needs the final block argument. Essentiality of A implies essentiality of B in H. Choose a basis of restricted normals. An endomorphism preserving each normal line is diagonal in this basis; every additional normal forces equality of the diagonal entries appearing in its support. The resulting equivalence classes are the indecomposable spans of the normal configuration. Thus H decomposes into blocks H_j and End_B(H) is exactly the independent scalar action on those blocks. The degree-one logarithmic fields are correspondingly sums b_j epsilon_j.

After choosing a normal complement, an original hyperplane over a factor in block j has equation beta_j(t_j)+c alpha. A derivation killing alpha differentiates this equation using only its j-th tangential component. Consequently projecting E_X to an individual block preserves every tangency condition. This proves, on every X in Q, an actual direct-sum decomposition of E_X and of its reduced image M_X inside T_X. It does not assume the original arrangement itself is a product. T_X also decomposes by these same blocks, including any localized free directions.

For an epimorphism Phi=A rho+v nu, the H-stalk forces every scalar a_j of A to be nonzero. Hence A M_X=M_X. The quotient C_X=T_X/M_X inherits the block decomposition. Modulo M_X, canonical restriction contributes the cyclic submodule generated by e=sum[epsilon_j], while Phi contributes the cyclic submodule generated by h=sum(a_j+b_j)[epsilon_j]. The diagonal endomorphism B0 of C_X satisfies h=B0 e.

If Rh=C_X, then B0 is onto. A block on which its scalar is zero must itself vanish; on every other block the scalar is a field unit. Therefore B0 is an automorphism of C_X, and applying its inverse gives Re=C_X. This proves rho_X onto. The argument applies separately at every stalk and does not assume finite length, irreducibility of the local restriction, or a nonzero quotient in each block.

Thus both ordinary and Ziegler epimorphism-rigidity statements hold in the asserted graded category. The stronger conclusion is existence equivalence, not a claim that every ordinary map has image contained in the canonical image. The final proof preserves that distinction.

## 4. Additional family naturality and the dimension boundary

The scalar classification across arrangements explicitly requires an assignment on possibly nonessential marked localizations, compatible with localization to {H} and all linear isomorphisms. This is stronger than compatibility with arrows of one fixed poset. The use of geometric nonzero-flat posets retains the H-stalk of {H}; it does not silently apply an essential-only source convention there.

The common top map must commute with GL(H). Commuting with elementary transvections forces a scalar matrix over every field when dim H>=2, including finite fields of characteristic two. The same argument applies to the matrix of v. This gives a rho+b epsilon_H nu. The actual Euler splitting D_X=S epsilon_V direct-sum E_X on Q proves the claimed image formula. For direct D-to-Z families valid across all marked arrangements, one multiple-fiber example imposes b=-a. None of these family hypotheses is silently used in the fixed-poset epimorphism theorems.

The rigidity artifact assumes ell>=3 throughout. It therefore never uses a nonexistent nonzero restricted-hyperplane stalk in ell=2. The transport artifact includes ell=2 correctly: Q is then the single point H and the retained target is Der(R), not the full logarithmic module on the removed zero flat. Its generic-incidence and local-lifting arguments still apply to the defined sheaves. Neither artifact transfers a dimension-at-least-two source global-section or freeness theorem across this boundary.

## 5. Exact defects, Hilbert obstructions, and characteristic checks

### Seven-plane ordinary calculation

In characteristic different from two, the seven listed hyperplanes remain distinct. The normal-annihilating module is exactly the syzygy model p u-q v=r h, with p=x(x-z), q=y(y-z), r=(x-y)^2-z^2. The displayed linear syzygy is correct, and reducing it gives -(x+y) as its coefficient of eta modulo Euler. The Koszul pair gives -xy. The absence of a constant syzygy, the one-dimensional linear syzygy space, and the fact that (x+y,xy) contains every form of degree at least two prove the full ideal equality J=(x+y,xy), rather than only a lower bound on a defect.

My independent integer coefficient matrices have Smith diagonals (1,1,1) for constant syzygies and eight ones followed by zero for linear syzygies. In particular, the claimed one-dimensional linear-syzygy space does not acquire an exceptional odd characteristic.

I independently verified all six Buchberger S-pair reductions for the monic displayed basis. Every quotient coefficient has denominator a power of two, so the calculation is a certificate over Z[1/2], not only a rational or sampled-characteristic check. Membership of the extra cubic follows explicitly from

    xyz=(x-2y+z)p+xq-xr,
    xz^2+yz^2-z^3=2xyz-z(p+q-r).

The leading ideal is (x^2,xy,y^2,xz^2), giving standard-monomial dimensions 1,3,3,2,2,... . The resulting original and deletion Hilbert series agree with the artifact. Promotion to the retained w-axis adds one free derivation and one polynomial variable, giving exactly the positive discrepancy (t^2+t^3)/(1-t). An exact graded sequence with those three stalk modules would force that discrepancy to vanish, irrespective of either arrow.

### Four-plane Ziegler calculation

The accepted characteristic-free three-generator/one-relation presentation gives Hilb(E_X)=(1+3t^2-t^3)/(1-t)^4 after promotion. The named restriction has Hilbert series (1+t+t^2)/(1-t)^3, and the discrepancy is t/(1-t), agreeing with the full defect K[w](-1). This concerns the normal-annihilating domain E. The artifact correctly notes that the ordinary D/deletion sequence in this particular example is onto and that multiplicity-one Z equals the ordinary target; no contradiction between those different domains is claimed.

### Arbitrary rank-one graded tensor twists

The tangency cokernel has no support at height-zero or height-one primes of S: at height one, at most one distinct linear-factor row survives, and a constant derivative hits it. Therefore the first two numerator coefficients are N_D(1)=ell and N_D'(1)=number of hyperplanes. This works for nonessential localizations and arbitrary fields. In a proposed ordinary exact sequence, differentiation of the Hilbert identity gives a_X=1 on Q. Off Q the target vanishes and D_X=F_X, so a_X=0. For E, the rank ell-1 calculation gives the same shifts. These are identities of integer Hilbert coefficients, not arithmetic in the coefficient field.

Hence the explicit discrepancies exclude every stalkwise graded-free rank-one tensor twist in the stated shapes, with arbitrary transition maps. The direct D/deletion/Z shape at a multiple fiber has the nonzero discrepancy (t^m-t)/(1-t)^{ell-1}, already at a retained rank-two stalk. The reversal of the two torsion-free terms forces ell a_H=ell-2 at H, impossible for integral a_H when ell>=3. A restriction module cannot be the submodule of a torsion-free S-module because alpha kills it. Each conclusion is limited to its specified module shape.

## 6. The positive class and the nonfree rank-five witness

For a nonzero X in Q, let C_X be its deletion closure. Then C_X is a nonzero deletion flat and C_X intersect H=X: represent X as an intersection including H and use the defining minimality of C_X. If H contains no nonzero deletion flat, C_X is not contained in H. Thus dim C_X=dim X+1, exactly the condition that adding H increases the local rank by one.

Choose v in C_X with alpha(v)=1. Every local deletion equation vanishes on v, so V=H direct-sum Kv makes those equations independent of alpha. Ordinary target derivations lift with alpha-independent coefficients; those lifts kill alpha and give the Ziegler surjection too. Distinct deletion hyperplanes containing v cannot have the same restriction to H. This proves both actual canonical short exact sequences at every target-bearing stalk. The choices of v need not, and are not claimed to, form a compatible global splitting.

The converse incidence characterization also checks: if a nonzero deletion flat Y lies in H, then its deletion closure is itself, so H does not increase the localization rank. Over an infinite field the finitely many forbidden annihilator subspaces do not cover the dual vector space. Over finite fields existence is correctly left conditional.

For the Q^5 example with deletion xyz(x+y+z)uv and alpha=x+2y+3z+u+v, the eight deletion line flats are the six factor lines and the u- and v-axes. Alpha is nonzero on every one. Every nonzero deletion flat contains a line flat, proving the condition. My independent enumeration found all 48 deletion flats and all 39 nonzero original flats in H; at each of the latter the deletion-localization rank is exactly one lower.

At X={x=y=z=0,u+v=0}, precisely the four equations x,y,z,x+y+z survive deletion localization. The factor has rank three but at least four minimal generators: its degree-one logarithmic space is Euler, while its six-dimensional degree-two space has only three Euler multiples. Polynomial extension and free summands preserve the excess. Both the deletion localization and its marked local-coloop extension are nonfree. Thus this is genuinely outside the earlier local-free-deletion and local-free-original sufficient classes, and H is not a global coloop since deletion is essential.

The positive construction retains the actual pass-1 deletion closure transport and closed restriction transport. The ideal I cannot be discarded; the resulting long exact sequence still has the identified ideal-twisted deletion term and its separate comparison sequence. Nonessential deletion retains the previously stated center-removal qualification.

## 7. Open direct image, its higher correction, and recollement

For U=P minus Q, every flat outside H is already a deletion flat. At any X, the section space on U intersect P_{>=X} is an intersection of actual derivation submodules inside the V-stalk. All deletion hyperplanes containing X occur in this set, and their tangencies impose exactly D(A'_X). Other points impose only subsets of those tangencies. This proves u_*(D|U)=F with compatible structure maps, including all points on and off H.

It does not prove exactness of u_* in general. In the marked example A'=xyz(x+y+z)w and H:x+2y+3z=0, at the w-axis the open fiber is exactly the nonzero-flat lattice of the three-dimensional four-plane factor. Its local tangency maps are onto because every retained localization has at most two independent equations. The global four-row tangency cokernel is Q, since the derivative columns identify all rows up to sign and the row relations then kill x,y,z. Termwise acyclicity gives H^1(D_C)=Q in coefficient degree zero and no higher positive cohomology.

Polynomial extension and the acyclic constant w-derivation summand give (R^1u_*(D|U))_X=Q[w], with all higher direct images zero at that stalk. My independent rational cochain construction obtains coefficient-degree-zero cohomology (0,1,0) for the factor and (1,1,0) for the open fiber, detecting precisely the extra constant w direction and the unchanged nonzero H^1.

Under the incidence condition of Section 6, U is the whole geometric deletion poset and every such fiber has minimum C_X. Direct image is then exact and preserves derived sections, recovering the accepted deletion transport. The general example shows why that argument cannot be used without checking the fiber.

The ordinary open/closed exact sequence is valid, but its closed term has the original S-modules D(A_X), not the alpha-annihilated restriction modules. Its open-extension term has zero global sections: the arrow H->V forces the V component to vanish, and injectivity of all remaining maps into V forces every component to vanish. The actual deletion functor has a nonzero Euler section. These are genuine coefficient and cohomology mismatches.

## 8. The exact scope of the transport obstruction

Place the canonical three-term complex in degrees 0,1,2. Its only cohomology sheaf is its restriction defect C in degree two, hence the complex is quasi-isomorphic to C[-2]. If an exact transport makes this complex short exact and a functorial compatible derived-sections comparison identifies its transported and original derived sections, then RΓ(P,C)=0. This verifies Proposition 3 exactly as stated.

Abstract isomorphisms between individual endpoint cohomology groups would not supply the needed comparison of the complex and its arrows. The artifact explicitly excludes that shortcut. It also does not assert that derived sections are conservative for arbitrary sheaves.

In rank four, the actual canonical defects are supported only at minimal line flats. They are an exact extension from a discrete lower ideal, so H^0 is the direct sum of their stalks and all positive cohomology vanishes. Any nonzero such defect is therefore visible to derived sections. The promoted ordinary and Ziegler witnesses consequently cannot be repaired by a transport satisfying the proposition's stated compatibility.

Separately, inverse image along a surjective monotone map is exact and conservative by stalk evaluation. Such a base change cannot erase any nonzero cokernel. A correspondence involving another nonconservative operation or different maps is not ruled out merely by this observation; the final artifact limits its conclusion to faithful pullback legs and base change alone.

## 9. Everitt–Turner source comparison

I independently read the retained primary text of Everitt–Turner, arXiv:1902.00399v2, at its functor definition, higher-colimit definition, reduced endpoint, Theorem 2, and proof. The PDF has 215,202 bytes and SHA-256 `a3685d87977b333574fa45715580bcba6f8698e6112062439ae8e60ee92f0a39`. Public source: https://arxiv.org/abs/1902.00399v2 .

Its functors are contravariant, its homology is derived colimit, and the theorem removes the lattice minimum and deletes an atom, retaining the inherited coefficients. In the usual reverse-inclusion intersection lattice, those are V and a hyperplane. The audited logarithmic cohomology instead uses geometric inclusion and removes zero.

For a fixed coefficient degree the stalks are finite-dimensional, so dualizing the finite cochain complex indeed gives the homology of the contravariant dual on the same geometrically ordered poset. This does not reverse which endpoint has been removed. The geometric-order lattice is graded and atomic: in a k-dimensional flat, choose k independent restrictions of arrangement forms; their coordinate-line intersections are arrangement flats and span the original flat. Its atoms are lines. The resulting valid Everitt–Turner operation therefore deletes a line, with interval above that line, rather than the marked hyperplane and the restriction flats inside it, except at the ell=2 boundary.

The inherited-coefficient warning also checks directly. At a deletion flat Y contained in H, q partial_v is logarithmic for deletion when q is the product of its local deletion forms and alpha(v)=1, but its alpha derivative q is not divisible by alpha. Therefore it is absent from the original localization module. In addition, inherited original modules are S-torsion-free while restriction modules are killed by alpha. Neither discrepancy can be removed by relabeling a lattice operation.

This verifies the reported comparison, not a literature-wide impossibility claim or a source freeness theorem.

## 10. Independent controls and acceptance limits

The independent programs do not import or run either author's control implementation. They use exact rational linear algebra, integer Smith normal forms, polynomial identities, and explicit finite-poset cochains. Their artifacts are:

- `independent_audit/check_rigidity.py`: 3,978 bytes; SHA-256 `77246b16954df207ccded6b21a9bb245152bbcfbff829c505ad1ae8bb7103b21`.
- `independent_audit/rigidity_checks.json`: 2,738 bytes; SHA-256 `bd626fbcca623c021aaf01cae018473c94b61fa39de8db111c40ce235fba7dfd`.
- `independent_audit/check_transports.py`: 4,422 bytes; SHA-256 `77547d50ecc9d0cf8403d17c3bff2d3efde851497195e5915ec0e1caf8b002fc`.
- `independent_audit/transport_checks.json`: 7,827 bytes; SHA-256 `2f85d7ca6ca7cd35d0506de4f2b8e2241cd65261fcd958b5f64c002ac3d7a07a`.

Both scripts passed. They require Python 3 and SymPy; the audit used SymPy 1.14.0. The controls corroborate the proofs, rather than replacing all-field or all-degree arguments with bounded experiments.

The two pinned reports advance the constructive partial answer and exclude substantially more fixed-poset graded repairs than failure of selected canonical arrows alone. They do not resolve the unrestricted source question, assert novelty of credited examples, or make a claim about an uninspected version of record. Ungraded extensions and wider constructions are outside this acceptance.
