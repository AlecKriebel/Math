# Turn5: exact finite decisions for rational affine dynamics and polyhedral quantizers

AI-assisted proof attempt; independent review pending. This is an effective subclass result, not a computability assertion for arbitrary source maps and cells.

Assume f(x)=Ax+b with rational coefficients on R^n, n≥1. Every observation cell is described by finitely many rational strict or weak linear inequalities, and its weak relaxation is bounded. Cells may be half-open, as ordinary disjoint quantizers often are. The horizon T and a rational threshold ε≥0 are given.

## Exact initial cylinder
Compute B_0=I,c_0=0 and B_(j+1)=AB_j,c_(j+1)=Ac_j+b. Then f^j(z)=B_j z+c_j. Substitute this in every inequality defining the observed cell P_j. The resulting finite rational linear system, with its original strict/weak signs retained, defines C_0, the exact feasible initial set. This follows directly from turn1; it includes constraints that the entire observed trajectory remains in X.

Its nonemptiness is decidable by a finite exact procedure. Relax all strict inequalities to weak ones to obtain K. If there are strict rows a_l z<b_l, introduce0≤σ≤1 and replace them by a_l z≤b_l−σ, retaining the weak rows. The original system is feasible iff this augmented bounded polyhedron has a point withσ>0, equivalently iff its largest vertexσ-coordinate is positive. Any feasible strict point has positive minimum slack among finitely many strict rows. If there are no strict rows, feasibility is just nonemptiness of K. All calculations are rational.

For clarity, a bounded rational weak-inequality polyhedron can be handled without an oracle: enumerate all subsets of n linearly independent active rows, solve the equalities exactly and retain solutions satisfying all rows. For the augmented problem use n+1 rows. The retained list is exactly the vertex list and is nonempty whenever the polyhedron is nonempty. This includes lower-dimensional polyhedra, because at a vertex the active row normals span the ambient space. Equalities may be represented by two weak inequalities.

The classical vertex assertion has an elementary finite proof: if the active normals at a point fail to span, choose a nonzero orthogonal direction. Boundedness permits movement in both directions only up to finite endpoints, where a new independent constraint becomes active. The starting point is a convex combination of the endpoints. Recursing in increasing active rank reaches vertices after at most n levels. Thus every point is in their convex hull. This proves the finite enumeration and linear-objective maximum claims used here; no efficiency bound is asserted.

## Exact diameter despite half-open boundaries
If C_0 is nonempty, then closure(C_0)=K. Indeed fix one z_* satisfying all strict inequalities. For any z∈K and0<r≤1, the blend (1−r)z+r z_* satisfies every weak inequality and all strict inequalities, and tends to z as r↓0. The reverse inclusion follows by closedness of K.

Consequently closure(Q_t)=B_t K+c_t. One inclusion follows by continuity; the other uses compactness of K to ensure that its image is closed, together with density of C_0 in K. Therefore
 diam(Q_t)^2=max_(v,w vertices of K) ||B_t(v−w)||_2^2.
The formula is valid even if B_t is singular, Q_t is lower dimensional, or a maximizing endpoint is excluded by a strict cell boundary: diameter is a supremum, not necessarily an attained maximum in Q_t. For convex combinations, B_t(z−z') is a convex combination of the differences B_t(v−w), so its norm is at most the largest vertex-pair norm; the reverse follows from the closure identity.

All squared distances are rational. Thus whether diam(Q_t)≤ε, or whether some t has diameter≤ε, is decidable by finitely many rational comparisons. Empty observations are reported inconsistent rather than described as a successful reconstruction. Singleton feasible sets have diameter0.

## Exact set output if desired
The equation x_t=B_t z+c_t together with the strict/weak linear system for z is already an exact finite description of Q_t. To eliminate z, use Fourier–Motzkin elimination, retaining strictness: collect upper and lower bounds for one variable, compare every lower/upper pair, mark the resulting comparison strict if either contributing bound was strict, and retain all constraints not involving that variable. A missing upper or lower family imposes no pair constraints. This is equivalent to existence of a real value between finitely many bounds, including endpoint cases. Repeating eliminates all initial variables in finitely many steps and gives an exact rational strict/weak inequality description in x_t. Complexity can grow sharply; no polynomial-time claim is made.

## Final boundary of the five-turn program
The exact finest marginal is proved for all source maps. Literal nontriviality has the exact adjacent-image criterion. The continuous counterexample shows why injective infinite codes alone do not give uniform finite localization. Closed pair-orbit criteria and explicit nonlinear hyperbolic estimates give genuine geometric sufficient conditions. The present affine-polyhedral subclass has an exact finite small-diameter decision procedure, including half-open and degenerate cases.

These conclusions do not provide a universal effective geometric classification for every arbitrary map and quantizer admitted by the source, or identify a unique intended numerical meaning of its word “small.” The proposed full-source disposition remains unresolved5/5 with the complete marginal-optimality subquestion and the scoped positive/negative conditions prominent. Classical smoothing, compactness, hyperbolic dichotomy and polyhedral-elimination mechanisms are credited; no new-priority claim. No sixth author search.
