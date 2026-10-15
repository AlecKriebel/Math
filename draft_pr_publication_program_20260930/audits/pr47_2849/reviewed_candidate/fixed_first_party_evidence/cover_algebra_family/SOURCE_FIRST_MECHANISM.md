# Independent cover and local-system mechanism (before candidate read)

This note was authored before reading A47 candidate, helper, receipts, old review or other mathematical family findings. Exact head under audit: 487327b2412c436ae69e8c52bf353a9a1fb7594e. Audit completion estimate at this checkpoint: 30%; target discovery remains unproved.

## Claim and source boundary

For a closed connected oriented rational homology 3-sphere Y with every pi1(Y) -> SU(2) abelian, does dim_C I#(Y;C)=|H1(Y;Z)|? The AIM kirbylistrep.pdf supplied URL is a workshop summary, not the target. The author K3 list, printed pp167–168, Problem3.51, confirms this claim and says the known conclusion requires reducible Morse–Bott nondegeneracy, equivalent in this setting to cyclic finiteness. Published Baldwin–Sivek (2018), Prop4.4–4.5 and Thm4.6, pp4353–4356, gives the precise boundary.

## Independently reconstructed algebra

Write A=H1(Y;Z), finite, and rho_chi(g)=diag(chi(g),chi(g)^-1). Its real adjoint local system splits as R plus the realification of C_(chi^2); complexification splits as C plus C_(chi^2) plus C_(chi^-2). Thus H1(Y;ad rho) vanishes exactly when H1(Y;C_(chi^2)) vanishes (the inverse character has the same dimension by complex conjugation, since chi is unitary). The trivial real summand contributes zero because Y is a rational homology sphere. Central chi^2=1 yields no degeneracy.

For a finite regular cyclic cover X->Y with deck group D, complex group-algebra Fourier idempotents split its cellular cochains into rank-one character local-system cochains. Hence H1(X;C) is the direct sum over eta in D-hat of H1(Y;C_eta), up to the harmless convention eta/inverse. Transfer embeds H1(Y;C) into deck-invariant H1(X;C). This controls twists, but only if vanishing of cover cohomology is independently established. A finite cover with positive b1 is not excluded by the base being a rational sphere.

The relevant cyclic covers are kernels of adjoint characters chi^2, not arbitrary covers chosen without an SU(2) character lift. Requiring all such covers to have b1=0 is equivalent to requiring all corresponding twisted cohomology groups to vanish: one implication uses decomposition; for the converse a nonzero eigensummand on the cover is a power (chi^2)^k, hence the adjoint twist of rho_(chi^k). This quantifies over all rho; it does not assert that the largest cover having positive b1 forces its particular primitive twist nonzero. Primitive eigenspaces can vanish while proper-divisor eigenspaces survive.

The set of representations under the target premise is a disjoint union of central point orbits and noncentral S2 orbits. If h=|A| and c=|A[2]|, there are c points and (h-c)/2 spheres, contributing total ordinary homology dimension c+2(h-c)/2=h. This is the critical-set count, not the conclusion about Floer homology until the Morse–Bott hypothesis supplies the appropriate spectral sequence. Isolated characters do not entail zero infinitesimal H1: nonreduced/obstructed local equations can have excess linear tangent directions. The model x^2+y^2=0 over R has one real solution and a 2-dimensional equation-linearized tangent, but is only a toy and realizes no 3-manifold premise.

## Genuine target-premise degeneracy example

Sivek–Zentner, A menagerie of SU(2)-cyclic 3-manifolds, Prop6.1, produces rational spheres with base S2(3,3,3), even |H1|, all SU(2) representations abelian, and a regular 3-fold cover which is a circle bundle over T2 with b1=2. Thus the implication 'SU(2)-abelian rational sphere => cyclically finite' is false, not merely unsupported.

A concrete choice in their presentation convention is Y=S2((3,1),(3,1),(3,2)). Its abelian presentation determinant is -36 and invariant factors are 1,1,3,12. Its Euler number is -4/3. The torus orbifold cover has degree3 and the pulled back circle bundle Euler number -4, so b1=2. To verify the SU(2) premise directly, suppose a representation were nonabelian; central h must map to +/-1. If h=1, the ci cube to1 and any noncentral ci has angle2pi/3. If any ci is central, the product relation forces the other two to commute. Otherwise c1c2=c3^-1 has real part -1/2, while multiplication gives 1/4-(3/4)<v1,v2>, forcing <v1,v2>=1 and commuting images. If h=-1, c1 and c2 cube to-1 (noncentral anglepi/3) while c3 cubes to1 (noncentral angle2pi/3). Central cases commute; in the remaining case the same real-part equality forces the first two axes equal. Every case contradicts nonabelianity. This does not compute I# or falsify KP3.51.

Lens spaces and any rational sphere with finite pi1 have vanishing H1 for all finite covers, hence lie in the known cyclically finite boundary. Integral homology spheres have only the trivial abelian character, so the target premise immediately places them in the known boundary. For nonzero p/q surgery on a knot in S3, published BS Prop4.7 says cyclic finiteness is equivalent to no pth root z satisfying Delta_K(z^2)=0. Even-p root selection must use squares rather than all pth roots of Delta_K.

## Falsifiable checks and remaining gap

Check determinant/invariant factors and quaternion endpoint equalities; reconstruct character squares and inverse-orbit counts independently; inspect all claimed polynomial root predicates; replay unchanged helpers with actual captures. Nothing above controls Floer generators born under perturbation at the degenerate genuine examples. The exact target gap is a valid argument controlling degenerate reducible contributions without the Morse–Bott assumption; proving cyclic finiteness from the premise is already blocked by the genuine example.
