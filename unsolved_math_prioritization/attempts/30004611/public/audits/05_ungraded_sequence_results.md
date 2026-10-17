# Independent acceptance of ungraded restriction rigidity and local obstructions

14 October 2026 UTC. Row 1775 / 30004611, the same final shared substantive pass 5.
This is an independent audit of the two specified mathematical components, not a novelty certificate or a solution of the broad source Problem 6.3.

## 1. Frozen artifacts, correction, and verdict

The accepted final artifacts are:

1. `ungraded_restriction_rigidity.md`: 17,093 bytes; SHA-256 `d9cddb15b64f592c2b26f6dd7585d5bf341b95a613f1dc445da5446b8857cc65`.
2. `local_obstructions/ungraded_local_obstructions.md`: 11,719 bytes; SHA-256 `b1752d1e1629e48f0be3f6098ea2aa4f64fa2880ce7653264a9cf08dac87b210`.

**Qualified mathematical acceptance.** The final versions require no further correction. One notation issue was independently identified during review: the original expression `Phi_X tensor_R K` did not directly make sense because its source D_X is naturally an S-module. The accepted version instead tensors the R-module cokernel with K. This correction does not change the proof or conclusion.

Accepted results:

- Complete classifications of arbitrary S-linear fixed-poset maps E to the Ziegler target, D to the ordinary target, and D directly to the Ziegler target.
- Ungraded epimorphism rigidity for the first two source/target pairs: an epimorphism exists precisely when their canonical map is onto.
- A characteristic-free Euler-independence lemma, including nonessential local restrictions and all common-flat directions, which supplies the previously missing ordinary argument.
- No arbitrary S-linear epimorphism even at the isolated four-plane E/Z stalk.
- An explicit arbitrary S-linear epimorphism at the isolated seven-plane D/T stalk, accompanied by a different, map-independent Ext obstruction to using its actual deletion module as kernel.
- Persistence of that fixed-kernel obstruction under any rank-one tensor twist that is free at the specified polynomial prime.
- Explicit ungraded exact sequences at rank-two D/F/Z stalks, showing why the earlier graded Hilbert obstruction cannot be promoted to an ungraded statement.

The classifications use the actual original common poset and require ell>=3. They do not require naturality across arrangements. The geometric nonessential extension is explicit; no source cohomology assertion is transferred to a differently punctured nonessential lattice. No retained-v3 freeness criterion, arbitrary new terms, or unrestricted comparison-space theorem is used.

## 2. Dependencies and two kinds of localization

I read the accepted pass-1 common-poset construction, the pass-3 four-plane presentation, the complete pass-4 graded-rigidity proof, and its independent audit `audit_sequence_rigidity_transports.md`. The pass-4 proof's accepted hash is `ec3765d624575a0c047a9c81195bafd3923a342ce4fbf4ad3b8baadec7d5a237`.

The present proof keeps the nonzero bad line flats. First one takes an arrangement localization A_X at a geometric flat X. In the promoted examples, X is the w-axis, so the plane w=0 is absent and partial_w is a free derivation. Later the local obstruction proof localizes these polynomial modules at the prime P=(x,y,z) in K[x,y,z,w], whose residue field is K(w). These operations are different and are used correctly.

The ordinary rigidity proof instead uses the homogeneous maximal ideal m_R of the entire restriction ring, including all common-flat variables. This fiber is a legitimate obstruction to surjectivity; it is not identified with the separate K(w)-fiber used for the Ext calculation.

Exactness of the Alexandrov functors is pointwise. On Q, every target transition to H is the actual inclusion into Der(R), so the H-component determines a morphism uniquely. There is no arrow from the complement of Q into Q. Arrows leaving Q have zero target transition and supply no missing condition.

## 3. Polynomial lattice classification and the Ziegler inverse argument

At H the normal-annihilating source is S tensor H, and its target is R tensor H. Thus every S-linear map is reduction followed by a polynomial matrix A, without any degree restriction. At a retained restricted hyperplane K0=ker(beta), the elementary rank-two normal-annihilating basis reduces onto

    L_beta^(m) = R beta^m n + R tensor K0,   beta(n)=1.

Therefore naturality forces A to preserve each individual lattice L_beta^(m). Conversely these separate conditions preserve their intersections, which are exactly the Ziegler stalks. This checks necessity and sufficiency at all original points, not merely at height-one primes of a coefficient ring.

The equivalent polynomial congruence is beta(Au)=0 modulo beta^m for every constant tangent vector u in K0. There is no assertion that beta A is a constant scalar multiple of beta; that would incorrectly import the graded theorem. The transverse generator beta^m n automatically satisfies the required divisibility after any polynomial A.

If A pi is onto at H, the square matrix A is surjective over R. Since its cokernel is zero, its determinant ideal is the unit ideal; equivalently a right inverse has determinant inverse, and det A is a unit. Let P_beta have columns beta^m n and the tangent constant basis. Although P_beta is only invertible over Frac(R), preservation says C=P_beta^-1 A P_beta is a polynomial matrix. Its determinant is the same unit det A. Consequently C^-1=adj(C)/det(C) is polynomial, proving A^-1 preserves the very same lattice. This is valid for arbitrary m and arbitrary fields, with no multivariate Smith-normal-form claim. Intersecting gives a target-sheaf automorphism, and hence coker(A pi) is isomorphic to coker(pi).

The proof also covers finite fields and characteristic two. Neither an infinite set of field points nor characteristic-dependent differentiation is involved.

## 4. Ordinary maps, the Euler lemma, and the missing dimension argument

The H-component of an arbitrary map from D is A rho+w nu. The normal generator z partial_z is independent of the tangential constant basis as an S-module generator, so omitting w would be incorrect. At each retained K0, constant tangent directions force A to preserve the ordinary lattice. Applying the map to z partial_z+beta partial_beta then forces beta(w) to be divisible by beta. Across all K0 this is exactly w in D(B). These conditions suffice at all smaller flats because A preserves each ordinary target intersection.

Surjectivity of [A w] does not force A invertible. An explicit ordinary Boolean example has

    A=diag(1-x,1),  w=(x,0)^T.

The rectangular matrix has right inverse with columns (1,0,1)^T and (0,1,0)^T, even though det A=1-x is not a unit. Both A and w satisfy the appropriate ordinary lattice conditions. The accepted proof avoids the false square-matrix shortcut.

Here is my independent check of the replacement argument. At a fixed X in Q put T=T_X, M=im(E_X->T), and let e be the restricted Euler derivation. Let U be the common-flat direction of the restricted arrangement. In this actual flat localization U=X. Split H=H' direct-sum U. The degree-zero part of T consists exactly of constant derivations in U. Consequently the H'-component of every element of (m_R T)_1 is zero.

Suppose e belongs to M+m_R T. Taking degree-one parts is legitimate because this step concerns the fixed graded modules and canonical reduction, not an arbitrary proposed map. A degree-one preimage in E_X then has H'-coefficient vector t+zv for a constant v. Its U-components are irrelevant to the tangency equations; these equations contain no U-coordinates. For every normalized deletion equation beta_i(t)+c_i z, tangency forces

    beta_i(t)+z beta_i(v) = beta_i(t)+c_i z,

since a degree-one divisibility quotient is constant and the nonzero t-part fixes it to 1. Therefore beta_i(v)=c_i. This remains valid over every field. Repeated restriction fibers must have identical slopes, so distinct hyperplanes cannot remain in a repeated fiber.

Changing coordinates to t'=t+zv makes every local deletion equation independent of z. Every target derivation now lifts by substitution in its polynomial coefficients, with zero z-component and unchanged tangential derivative basis. Thus M=T. Equivalently, the local deletion has a vector outside H annihilated by all its equations, making H a local coloop. The degenerate H'=0 case is simply A_X={H}, where lifting is immediate. This verifies all common-direction and nonessential cases.

If canonical ordinary restriction is not onto, its image is M+Re by the actual Euler splitting D_X=S epsilon_V direct-sum E_X. Its graded nonzero cokernel has nonzero homogeneous-maximal-ideal fiber. The lemma additionally makes e independent of the image Mbar in T/m_R T. Thus

    dim_K Mbar + 1 < dim_K T/m_R T.

For an arbitrary classified map, A induces an endomorphism of T/m_R T because A preserves T. Its image on E contributes at most dim Mbar dimensions, and its image on the single Euler generator contributes at most one. Hence its fiber cannot be onto. No assumption that A preserves M or is invertible appears here. Nor does the argument claim that the degree-zero component of an arbitrary epimorphism must itself be onto.

The corrected cokernel-fiber inequality follows from this same count. It is a statement about actual R-module cokernels, not an invalid R-tensor product of the S-module D_X. This proves the ordinary ungraded epimorphism equivalence, including reducible restrictions.

For the optional direct D-to-Z classification, restriction to E gives A in the multiplicity lattice algebra, while the Euler image is an arbitrary h in the global Ziegler module. The Euler splitting gives the stated formula and uniqueness. There is correctly no epimorphism-rigidity assertion for this different source/target pair.

## 5. Four-plane nonexistence versus seven-plane stalk freedom

For the four-plane example, the accepted characteristic-free presentation has relation column (x+y+z,-y,x). Modulo z, the determinant-one constant matrix

    [[1,1,-1],[0,0,1],[0,-1,0]]

takes it to (0,x,y). The two-component quotient by R(x,y) is the ideal (x,y), since the map (a,b)->-ya+xb has exactly that kernel. Adding the free w-direction gives

    E_X/zE_X = R^2 direct-sum (x,y).

This module is torsion-free of rank three. At (x,y), with residue K(w), it needs four generators and so is not free. Any epimorphism to the free rank-three Ziegler target splits. Its kernel would be torsion-free of rank zero and therefore zero, forcing the source to be free, a contradiction. This excludes arbitrary isolated-stalk maps, including characteristic two, and does not depend on the kernel one might propose.

For the seven-plane example, forgetting grading gives the original relation column (0,p,b,c), with p=x(x-z), b=3x-y-z, c=y-x. Modulo z the nonzero column is (x^2,3x-y,y-x). Subtracting x/2 times each of the last two entries from the first yields zero. The two remaining linear forms form an invertible coordinate change when 2 is invertible. With Euler and w free summands, this proves

    D_X/zD_X = R^3 direct-sum (x,y).

Projection yields a genuine arbitrary stalk epimorphism onto T_X=R^3. The explicitly specified images of h1,h2,h3 respect the relation because x^2-(x/2)(3x-y)-(x/2)(y-x)=0. In particular h1 of coefficient degree three maps to eta of degree two. Such a degree-lowering map need not extend to a polynomial-coefficient map at the H-stalk, and the example is consistent with the global sheaf-rigidity theorem.

## 6. Full presentations and the ungraded Ext obstruction

I independently reconstructed all six displayed original/deletion tangent generators, checked their tangencies by exact polynomial quotients, and checked both full relation identities. The independent nonzero pair minors are products of the explicitly distinct forms, proving the stated fraction-field independence. The original relation column is primitive because its two linear entries are coprime. The deletion column is primitive because its linear entry e=z-x-y does not divide d=y(x-y-z): modulo e, d=-2y^2. Thus in each case the full relation module among the displayed generators is the claimed single polynomial column.

Equal Hilbert series with the already accepted pass-4 exact computations then establishes that the generators span the whole logarithmic modules. This is a legitimate use of grading to certify fixed module presentations; it imposes no grading on hypothetical new arrows. The accepted pass-4 calculation holds over all fields with 2 invertible, so this step is not a rational computation extrapolated to other characteristics.

Applying Hom(-,S) to these length-one free resolutions gives

    Ext^1(D_X,S) = S/(p,b,c),
    Ext^1(F_X,S) = S/(a,d,e).

For D the equations y=x and z=2x leave p=-x^2, so the quotient has basis 1,x over K[w]. For F, substitution z=x+y gives a=2x^2+4y^2 and d=-2y^2. Thus its quotient has basis 1,x,y,xy over K[w]. Only division by 2 is required, so these calculations include characteristic three and every other odd characteristic.

At P=(x,y,z) the corresponding Ext lengths are 2 and 4 over S_P. Since T_X=(S/(z))^3 has projective dimension one, an exact sequence

    0 -> F_X -> D_X -> T_X -> 0

would give Ext^1(D_X,S)_P onto Ext^1(F_X,S)_P: the following term is Ext^2(T_X,S)_P=0. A module of length two cannot surject onto one of length four. The direction of this inequality is essential and is correct.

If a tensor twist L is free of rank one at P, then (L tensor F_X)_P is isomorphic to (F_X)_P and the same obstruction applies. This includes all specified stalkwise locally free rank-one twists, regardless of transition maps. It does not claim invariance for arbitrary rank-one torsion-free modules that fail to be free at P.

At an isolated rank-two D/F/Z stalk, all three ungraded modules are abstractly S^ell, S^ell, and (S/(alpha))^(ell-1). The displayed injection diag(1,alpha,...,alpha) and quotient reduction really form an exact sequence. Hence the previous Hilbert discrepancy is only a degree-preserving obstruction there. No gluing of these arbitrary basis choices or universal direct D/F/Z sequence is claimed. Similarly, graded shift arguments alone must not be reused as ungraded obstructions to other reordered shapes.

## 7. Boundary, independent controls, and final limits

The fixed-poset classification is explicitly scoped to ell>=3, exactly where each restricted hyperplane is a retained nonzero flat. At ell=2, Q={H}; the restriction target at that sole point is Der(R), not the full logarithmic module at the removed zero flat. Canonical reduction is onto there. Arbitrary maps are classified just by the H-component, without the absent restricted-hyperplane constraints. No claim in the accepted reports silently crosses this boundary.

No finite-field issue remains: the classification, lattice inverse proof, and Euler lemma are polynomial identities or vector-space arguments over an arbitrary field. The four-plane presentation is characteristic-free. The seven-plane arrangement, presentation, and Ext obstruction explicitly require char K != 2. No classification of polynomial families commuting with all GL(H) actions is inferred from the earlier constant-matrix centralizer argument.

My independent script neither imports nor runs either author's implementation. Its exact controls include all six generator tangencies, both relation identities, both reduced Ext ideals and lengths, the explicit ungraded epimorphism relation, the four-plane unimodular operation, a concrete ordinary epimorphism with nonunit det A, and a polynomial inverse preserving multiplicity-two lattices. The last example is only a control; the general inverse theorem is proved in Section 3.

Independent artifacts:

- `independent_audit/check_ungraded.py`: 4,120 bytes; SHA-256 `6f89acfa2b11a09538dbe5b49b2efd316bb018ff1c4d17c48b24e5ccab6c0af6`.
- `independent_audit/ungraded_checks.json`: 1,079 bytes; SHA-256 `b151005a3bf1178c866f5d2b8cc6d25ee231a4a2da2ee7dc6023954ba01b07b9`.

All independent controls passed with Python 3 and SymPy 1.14.0. They corroborate the symbolic proofs rather than replacing all-degree and all-characteristic statements with sampled computation. The separately reviewed author controls also pass, but are not represented as independent checks.

This audit closes the ungraded-map gap for the stated fixed terms and actual common poset. The broad source question still permits genuinely different terms and comparison constructions. No universal impossibility claim, uninspected version-of-record claim, or novel-source-example claim is part of this acceptance.
