# Independent spectral reconstruction (sealed before inherited verdicts)

Audit: PR214 / 30005244 / OWR-11101924-008, submitted head
36d5ef15098163e74bf14c2e696f560ce592affd. Family: spectral/Fredholm/Riesz.
First seal completed before the clock check at 2026-10-15T07:58:22Z (UTC).

This reconstruction was made after reading the complete submitted CANDIDATE.md,
TURN_2.md, the complete original OWR contribution (printed 2580--2582), and CDN
v3 introduction and static theorem passages. No inherited independent_review or
FINAL_DISPOSITION verdict was read before this seal. This is verification, not an
additional author proof-attempt turn. It neither supplies missing kernel lemmas
nor changes the author packet.

## Exact abstract claim

Let H be a complex Hilbert space and I=[a,b] a bounded real closed interval.
Let B_n and B be bounded selfadjoint operators with spectrum in I, and suppose
B_n -> B strongly. Let C_n -> C in norm, with C compact. Write A_n=B_n+C_n
and A=B+C. In the application C_n is finite rank (and compact); the conclusions
below do not require that extra fact once norm convergence is assumed.

For every compact K contained in C minus (I union spectrum(A)), z-A_n is
eventually invertible on K and the inverse norms are uniformly bounded. Every
spectral point of A outside I is an isolated eigenvalue of finite algebraic
multiplicity. For an isolating disk with closed disk outside I, the Riesz
projections for A_n and A converge in operator norm. Their ranks are eventually
equal, and the total algebraic multiplicity in the disk equals that of the limit.
All eigenvalues in the cluster converge to the central eigenvalue as n->infinity.
The corresponding total generalized spectral subspaces converge in both gap
directions. This does not assert preservation of an individual Jordan block or
of each split eigenspace. Norms ||A_n|| are uniformly bounded, so eigenvalues
cannot escape to infinity.

The same assertion holds with h->0 along any mesh sequence satisfying these
premises. Proving the premises for a particular kernel scheme is a separate task.

## Resolvents and compact products

Put D=C\I and R_n(z)=(z-B_n)^(-1), R(z)=(z-B)^(-1). For z in a compact
K subset D, their norms are at most delta^(-1), delta=dist(K,I)>0. The identity

    R_n(z)-R(z)=R_n(z)(B_n-B)R(z)

gives strong convergence at each z. Uniform convergence on K on each fixed
vector follows either by a finite net and the resolvent identity, or because
{R(z)u:z in K} is norm compact and a uniformly bounded strongly convergent
operator sequence converges uniformly on compact vector sets. Selfadjointness
gives R_n(z)*=R_n(conj(z)); the adjoints therefore have the same uniform strong
convergence on K.

If X_n -> X strongly with a common bound and L is compact, then
||(X_n-X)L|| -> 0: prove this first for finite-rank L, then approximate L in
norm. If X_n* -> X* strongly, adjointing the same argument gives
||L(X_n-X)|| -> 0. Compact norm-continuous parameter families admit uniform
versions by finite-net approximation. Both the side of multiplication and the
adjoint hypothesis matter.

Consequently F_n(z)=R_n(z)C_n -> F(z)=R(z)C in norm uniformly on compact
subsets of D. The operator F(z) is analytic and compact. The factorization is

    z-A=(z-B)(1-F(z)),
    z-A_n=(z-B_n)(1-F_n(z)).

## Local finite-dimensional analytic reduction (Fredholm step)

This paragraph derives the needed analytic Fredholm fact rather than importing
an uncited theorem. Fix z0 in D. Since F(z0) is compact, choose a finite-rank
orthogonal projection E with ||(1-E)F(z0)(1-E)||<1/2. Decompose
H=EH plus (1-E)H. The lower-right block of 1-F(z) remains invertible for z
near z0, by continuity and a Neumann series. Block Gaussian elimination by
analytic bounded invertible factors reduces 1-F(z) to diag(S(z),D(z)), where
S(z) is a finite-dimensional analytic Schur complement and D(z) is invertible.
Thus invertibility is equivalent to det S(z) != 0. Unless this determinant
vanishes identically, its zeros are isolated and its inverse is meromorphic;
all singular Laurent coefficients of (1-F(z))^(-1) have finite rank because
the only singular block factors through EH.

For completeness, local identically singular alternatives are globally excluded
here. Let U be the set of points that have a neighborhood on which singular
points are discrete. U is open and nonempty, because 1-F is invertible for large
|z| (equivalently |z|>||A|| and z outside I). If a point z0 lies in the closure
of U, its local determinant cannot be identically zero: that would make an
entire neighborhood singular, contradicting the existence of points of U in
that neighborhood and their locally discrete singular sets. Hence z0 is in U.
U is closed relative to D, and D is connected, so U=D. Connectedness follows
directly by connecting points around either endpoint of the removed finite
real segment. This fails for an arbitrary separating excluded real set, so the
interval/complement geometry is an actual hypothesis used by the proof.

It follows that (z-A)^(-1) is meromorphic on D with finite-rank principal
parts at isolated singularities. A spectral point there cannot be a removable
singularity: an analytic extension of the inverse, multiplied by z-A and
evaluated at that point, would be an inverse. Thus these are genuine poles.
The usual resolvent identity and two nested contour integrals give P^2=P for
the residue P=(2*pi*i)^(-1) integral (z-A)^(-1)dz. A commutes with P. On
ker P the resolvent has no singular principal part and extends invertibly
through the isolated point; on ran P it is a finite-dimensional resolvent.
Equivalently compare Laurent coefficients in (z-A)R_A(z)=1: the negative
coefficients are successive powers of A-lambda times P, and terminate after
the pole order. Thus (A-lambda)^m P=0 for some m, P has positive finite rank,
and ran P is exactly the total generalized eigenspace. If P were zero, the
same coefficient recursion would make every higher principal coefficient zero,
contradicting the genuine pole. This supplies finite
algebraic multiplicity without an assumption of diagonalizability.

## Stability and Riesz projection convergence

On a compact K in D\spectrum(A), (1-F(z))^(-1) is uniformly bounded.
Uniform norm convergence F_n -> F and a Neumann series give invertibility and
a common inverse bound for 1-F_n, hence for z-A_n. In particular a convergent
sequence of discrete spectral points cannot converge to a point of D in the
resolvent of A. This assertion needs no fixed-index labeling of eigenvalues.

Let Gamma be an isolating circle whose closed disk lies in D. Define on Gamma

    G_n=(1-F_n)^(-1)F_n,   G=(1-F)^(-1)F.

Then G_n -> G in norm uniformly on Gamma, and G is compact and norm continuous.
The inverse formula gives

    (z-A_n)^(-1)=R_n+G_n R_n,   (z-A)^(-1)=R+G R.

The analytic terms R_n and R integrate to zero around Gamma, since the whole
disk misses I. For the other terms,

    ||G_n R_n-G R|| <= ||G_n-G|| ||R_n||+||G(R_n-R)|| -> 0.

The second term uses uniform strong convergence of the adjoint resolvents.
It cannot be deduced from ordinary strong convergence alone. Integrating yields
||P_n-P|| -> 0. If their distance is <1, P_n restricted to ran P and P
restricted to ran P_n are injective. Since ran P is finite dimensional, these
two injections imply rank P_n=rank P<infinity. This argument itself proves that
the approximate spectral subspace in this disk is finite dimensional even if
C_n was not assumed compact. Its finite-dimensional restricted spectrum has
the asserted total algebraic multiplicity.

Repeat for any smaller isolating circle and use stability on the compact closed
annulus between the two circles. The same number of eigenvalues is in the
smaller disk, and none remain in the annulus, so the entire cluster converges
to lambda. For unit u in ran P, dist(u,ran P_n)<=||(P_n-P)u||; the reverse
gap has the same bound. This is the precise generalized-subspace assertion.
Because norm-convergent C_n are bounded and ||B_n||<=max(|a|,|b|), ||A_n||
is uniformly bounded. No cluster can escape to infinity. All proofs apply
unchanged along every subsequence satisfying the premises.

## Embedded finite matrices and continuum masks

For a bounded support there are finitely many occupied grid cells for each h.
Let V_h be their three-component cellwise constant space. The submitted
operators B_h and C_h preserve V_h and vanish on V_h perpendicular; they are
exactly T_0^h and T_kappa^h-T_0^h on V_h. Thus

    embedded A_h = T_kappa^h on V_h, plus 0 on V_h perpendicular.

The weighted sequence norm has only a scalar factor h^3, so the matrix norm
is its usual Euclidean operator norm. The complement contributes an
infinite-dimensional zero eigenspace. Since 0 belongs to I_lat and every
contour under discussion has closed interior outside I_lat, it contributes
neither spectral points nor Riesz rank to any claim made here. The same
observation applies to zero extension of L2(Omega) in the continuum. One must
not use a contour enclosing 0 on the globally extended ball operator to claim
a rank-three static projection; TURN_2 explicitly works on L2(B) for that step.

For TURN_2 masks, F_j increases to B up to a null set because |B\F_j|->0.
Consequently M_j -> M_B strongly (indeed this follows from measure convergence
and absolute continuity on |u|^2). With bounded selfadjoint D,
M_j D M_j -> M_B D M_B strongly with adjoints. Common quadratic-form bounds
are preserved by compression because [-1/3,2/3] contains 0. If the dynamic
kernel is in L2(B times B), multiplying by the converging bounded product masks
gives Hilbert--Schmidt norm convergence by dominated convergence. The abstract
theorem therefore applies to an isolating disk around the nonreal ball
eigenvalue. The infinite zero complement is harmless there. This verifies the
abstract transport step conditionally on the independently established ball
eigenvalue and kernel premises. It does not use static operator-norm convergence
or DDA voxel consistency of these pathological supports.

## Attempted falsifications: assumptions that cannot be weakened silently

1. Strong convergence does not imply norm resolvent convergence. On l2, let
   B_n be projection onto e_n, B=0, I=[0,1], and C_n=C=0. Then B_n->0
   strongly, but at z=2 the resolvent difference is (1/2)B_n, norm 1/2.
   The submitted proof only integrates away this analytic part and is valid.
2. Strong convergence alone does not justify right compact multiplication.
   X_n u=<u,e_n>e_1 tends strongly to 0, but for K the projection onto e_1,
   K X_n=X_n has norm 1. The adjoints do not converge strongly. Selfadjoint
   B_n supplies the missing adjoint convergence for the submitted resolvents.
3. Strong convergence plus compactness of each C_n is insufficient if norm
   convergence is dropped: B_n=B=0, C_n=2 projection onto e_n, C=0, and
   I=[-1,1] has a polluted eigenvalue 2 for every n. The author proves the
   stronger compact norm premise rather than relying on this false implication.
4. Arbitrarily small support removal does not give norm-small static errors.
   On H=L2([0,1]), D=identity, M_j=1_[1/j,1], one has M_j->1 strongly but
   ||M_j D M_j-D||=1 for every j. TURN_2 correctly uses strong convergence.
5. A defective cluster can split: the matrices [[lambda,1],[epsilon,lambda]]
   converge in norm to a size-two Jordan block, while for epsilon>0 they have
   two simple eigenvalues lambda +/- sqrt(epsilon). The cluster subspace is
   correctly approximated; individual Jordan structure need not be preserved.

No counterexample was found to the stated abstract theorem with its full
premises. Remaining application validation: static lattice boundedness and
exact interval input; static strong kernel consistency; dynamic norm kernel
consistency; independent ball spectral/perturbative calculation; exact source
scope. None is silently certified by this abstract derivation.
