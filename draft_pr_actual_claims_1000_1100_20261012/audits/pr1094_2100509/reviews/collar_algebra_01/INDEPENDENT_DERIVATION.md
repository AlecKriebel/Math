# Independent derivation, before companion-file review

Frozen 2026-10-14 04:59 UTC. Only AGENTS, SUBMITTED_PINS and the full MATHEMATICAL_REPORT had been read when deriving the following. This is a mathematical assessment, not a vote inherited from acceptance labels.

## Target and falsification criteria

For each n >= 1 and each real Jordan representative J with real numerical eigenvalues, construct a smooth compactly supported real (1,1) tensor L on R^n with vanishing Nijenhuis torsion, whose matrix equals J in a commuting local frame on a nonempty open set. Also exclude every nonreal eigenvalue anywhere for such a tensor. Counterexamples to the mixed torsion identity, an uncovered real block, failure of a torus hypersurface embedding, loss of smoothness on extension, or unmet rigidity hypotheses would refute the stated classification. Analytic support, fixed global rank/type and a prescribed Cartesian frame are outside the claim.

## Frame calculation

Write E_i for angular fields and T for the transverse field. Their pairwise brackets vanish. A,b,lambda are functions only of t. For i,j <= n-1, brackets of LE_i with LE_j and angular derivatives of all coefficients vanish. For an angular index i,

[LE_i,LT] = -lambda A' E_i,
[LE_i,T] = -A' E_i,
[E_i,LT] = 0,
[E_i,T] = 0.

The angular term b has no transverse derivative contribution because LE_i has no transverse component. Inserting into the defined torsion gives N(E_i,T)=(A-lambda I)A'E_i. No b' or lambda' term remains. Skew symmetry gives N(T,T)=0. Tensoriality gives all vector fields from these frame values. Thus the constraint is both necessary and sufficient within this ansatz. This reasoning needs neither coordinates globally defined on the torus nor any inverse/rank hypothesis.

## Universal matrix path

A block permutation may place the final vector of one Jordan chain in the transverse slot. The restricted angular A_0 consists of all other blocks and the shortened distinguished chain; the only removed arrow lies in b_0. Changing b with A fixed removes that arrow without torsion. Changing lambda with A fixed is equally free. For any active block mu I+sum a_j E_(j,j+1), lambda=mu eliminates its scalar part from the constraint. Direct multiplication gives K K'=sum a_j a'_(j+1) E_(j,j+2). During the kth arrow removal, only a'_k may be nonzero. If k=1 the sum has no term containing a'_1. If k>1 its sole possible term has coefficient a_(k-1)=0 from the preceding stage. Therefore all stages satisfy the constraint.

Once all arrows in a block are zero, let its scalar value and lambda share the same scalar interpolation. A' is block supported and A-lambda I vanishes there. Other block products vanish because their derivatives are zero, even when they have eigenvalues equal to lambda or zero. Process finitely many blocks, preserving previously zero blocks. After the last scalar operation all three data are zero. If n=1, A and b are empty and arbitrary lambda is allowed. If the angular block list is empty the final scalar move remains legal. Zero eigenvalues and singleton blocks produce constant/empty operations. No eigenvalue difference is divided by.

Smooth switches constant on open endpoint neighborhoods produce genuine smooth concatenations, not just piecewise differentiable paths. A smooth even q with q=0 on the central band and q=1 on both end bands gives A_t'=q' A_s' and hence preserves the constraint under either direction of traversal. Its endpoint values make L exactly zero near each open collar end. A direct scalar cutoff of the original matrix would usually fail, so this path constraint is essential.

A specified block ordering may be restored by a constant permutation of the final commuting frame; any constant change of frame preserves commutation. Thus positioning one chain terminal last costs no claimed numerical Jordan representative. The support goal for zero J is also valid: the zero tensor has empty compact support and attains zero on any nonempty open set.

## Geometry and smooth extension

Inductively, start with a circle in R^2. An oriented embedded T^(d-1) hypersurface in R^d has a smooth global normal nu. In R^(d+1) its normal bundle is spanned by nu and the new constant coordinate vector, so a sufficiently small disk neighborhood is T^(d-1) x D^2. The boundary is T^d, smoothly embedded as a hypersurface. Compactness allows one common positive disk radius; the tubular-neighborhood theorem gives injection and smooth inverse, not merely an immersion. This is valid for every finite d. The product boundary is oriented, therefore the resulting codimension-one embedding is two-sided and has a normal collar. The collar image is open in R^n, and its central band is nonempty and open.

Transporting the global angular frame and T through the collar diffeomorphism preserves pairwise commutation and gives a smooth frame throughout its image. The image of T^(n-1) x [-3/4,3/4] is compact. The support lies inside this image, separated from both collar ends by open zero bands. Define zero at every exterior point. Local neighborhoods at collar boundary points see only zero, giving all-order smoothness. Torsion is local and natural under diffeomorphism, so it vanishes on the image and exterior, including the boundary. For n=1, direct skew symmetry on a one-dimensional tangent space proves torsion zero for f(x)Id; a smooth plateau bump realizes any scalar.

## Necessity pending primary-source verification

If the invoked theorem indeed applies to every smooth Nijenhuis tensor on a closed connected manifold, constant nonreal eigenvalues with constant multiplicity would exclude nonreal spectra. Compact support in R^n gives a tensor identically zero on the complement of a ball. On the one-point compactification S^n, the standard R^n chart covers all but infinity; assigning zero near infinity is smooth in the other chart since the tensor is exactly zero there. Torsion remains zero by locality. The only pending mathematical dependency at this checkpoint is the exact statement and hypotheses of the prior rigidity theorem.

## Initial conclusion

No algebraic or geometric contradiction has been found. The constructive direction has a checkable universal derivation including all stated boundary cases. Finite symbolic controls will supplement it but cannot prove a universal dimension statement. The source rigidity and target wording still need fresh authentication. Completion estimate: 35%.
