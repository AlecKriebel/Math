# Author verification of the imported analytic route

This is the author's mathematical check, not the required independent audit. The Bi manuscript is credited, recent, and unrefereed here. No use is made of WXY's singular-corner index calculation. The following are the concrete points checked, including details useful to an adversarial reviewer.

## Dependency boundary

The existence input is Brendle, arXiv:2301.05087v4, Propositions 2.14–2.15 (§2, pp.10–12): on an odd-dimensional smooth compact convex domain, a smooth sphere-valued boundary map homotopic to the Euclidean Gauss map gives a Fredholm Dirac boundary problem of positive index. Its proof was read. The boundary symbol has complementary half-dimensional eigenspaces; in the flat case the kernel contains the identity spinor tuple and a cokernel tuple would anticommute with every Clifford generator, impossible in odd dimension. Homotopy preserves the index. The underlying standard smooth elliptic Fredholm and Sobolev theorems are imported mathematical foundations, not newly formalized here. The matching-angle hypothesis of Brendle's separate polytope theorem is not needed for this smooth-domain proposition. https://arxiv.org/abs/2301.05087v4

## A. Polyhedral geometry and corners

Write P={u_a≤0}, with irredundant affine inequalities and unit Euclidean normals N_a. Pick p inside P, δ=min_a(−u_a(p))>0. If u_a(x)>−2/λ and λ≥4/δ, then

    N_a·(x−p) ≥ δ/2.

Consequently for t_a≥0,

    |Σ t_a N_a| ≥ (δ/(2 diam P)) Σ t_a.

Uniform equivalence of a fixed smooth positive metric with the Euclidean metric gives the analogous covector estimate. This prevents cancellation in the smoothing gradient. With a smooth convex cutoff Φ vanishing on (−∞,−2], positive derivative afterwards and Φ(0)=1, the level set Σ_λ of Σ_a Φ(λu_a)=1 is smooth and convex. It lies in P, contains a fixed interior ball, and has a uniform radial Lipschitz parametrization. Moving a point of P inward toward p by order λ^−1 enters the strict inner sublevel. Thus its radial discrepancy from ∂P is O(λ^−1).

The needed error bound for an intersection face F_I is linear rather than Hölder: dist(x,F_I)≤C max_{a∈I}|u_a(x)|. One verification uses the finitely many normal cones at faces: if a unit limiting vector were both a normal-cone vector and annihilated every equality covector while satisfying the remaining feasible inequalities, pairing that vector with its normal-cone representation would give 1≤0. Finiteness of the face types gives a uniform constant.

Irredundancy matters. An intersection of three distinct facets of a full-dimensional convex polytope has codimension at least three. Indeed a codimension-two transverse section is a pointed two-dimensional convex cone with exactly two boundary rays; its two supporting facets are the only facets containing the given ridge. Thus the union K of triple intersections really is a codimension-at-least-three set, even at nonsimple vertices. The method does not quietly replace a nonsimple polytope with a simple one.

## B. The angle interpolation check

Away from an O(λ^−1) neighborhood of K, at most two cutoff terms are active. The rounded normal lies on the minor spherical arc between their g-unit normals. If that g-arc has length α and the reference Euclidean normal arc has length α_0, the hypothesis is α≥α_0. Transferring the same fractional arclength to the reference arc contracts its leading transverse derivative by α_0/α≤1. The leading mean curvature is κ≥0 of order at most λ; moving the endpoint normals to the nearby ridge changes the normal by O(λ^−1), its derivative by O(1), and hence the comparison error by O(1). Tangential-to-ridge derivatives stay bounded. Thus the leading potentially unbounded term cancels with the correct sign. Reversing interior and exterior angles would invalidate this step.

There is a genuinely uniform margin from 0 and π for each pair of g-normals: the two defining covectors are linearly independent; positive definiteness and compactness prevent their normalized angle from tending to 0 or π. Transition to one active facet is smooth because Φ and all its derivatives vanish at the cutoff endpoint. The ratio defining the interpolated arclength can there be written using arctan with a positive denominator, avoiding the apparent endpoint singularity of arccos.

## C. Spherical homotopy does not lose degree

Let q(x)=(x−p)/|x−p|. The estimate in A gives q·N_a≥c>0 for every active facet. A point on the minor reference arc is a positive sine-weighted combination of its endpoints. Its dot product with q is also bounded below by c, because the sum of the two sine weights is at least one. Hence interpolation to q never meets an antipodal singularity.

Use a regularized distance r to K, with |dr| bounded, and a transition that runs from r=δ_λ² to r=δ_λ, where δ_λ=λ^−1/4. Choose its derivative bounded by C/(r|log δ_λ|). The resulting boundary map η_λ is homotopic to q and therefore has degree one. It equals the fixed facet normal on every fixed compact subset of the relative interior of a facet for sufficiently large λ.

The interpolation in the target sphere does not amplify the leading derivative. In polar coordinates about q it is (θ,ω)↦(tθ,ω), 0≤t≤1, 0≤θ<π/2. Radial derivative is t≤1; angular derivative ratio is sin(tθ)/sin θ≤1 because sine is increasing on this interval. Dependence of q and t adds only a bounded term and the displayed logarithmic-cutoff term. This hemisphere restriction is essential and has been verified, rather than presumed globally on a sphere.

## D. Critical logarithmic trace term

Here is a direct check of the analytic estimate that removes the higher corners. On a flat boundary chart containing a codimension-three face, choose coordinates (y,z,t) in R^(n−3)×R²×R so that the boundary facet has t=0 and the lower-dimensional face lies in {z=t=0}. If a(y) is its distance from (y,0,0), then the squared distance from (y,z,0) to that face is a(y)²+|z|². For any fixed positive constants c,C and 0<δ sufficiently small, set

    b_δ(y,z) = 1_{cδ² < sqrt(a(y)²+|z|²) < Cδ}
                 / [sqrt(a(y)²+|z|²) |log δ|].

Polar integration in the z-plane, using s=sqrt(a²+ρ²) and ρ dρ=s ds, gives uniformly in y

    ∫_(R²) b_δ(y,z)² dz
      ≤ (2π/|log δ|²) ∫_(cδ²)^(Cδ) ds/s
      = O(1/|log δ|).

Also the L²_z norm of the indicator of distance<Cδ is O(δ). For a scalar v in W^(1,2)(R^n), Hölder in z and the three-dimensional Sobolev trace inequality yield

    ∫ b_δ |v(y,z,0)|² dz dy
      ≤ C |log δ|^(−1/2) ∫ ||v(y,·,·)||²_(W^(1,2)(R³)) dy
      ≤ C |log δ|^(−1/2) ||v||²_(W^(1,2)(R^n)).

The indicator contributes Cδ times the same norm. There are finitely many intersection faces. Distances to faces incident with the current facet can be used: if a nearest triple-intersection face is sufficiently close to that facet, they intersect; the finite normal-cone bound in A controls the distance to their intersection. The radial bi-Lipschitz maps between P and the inner domains distort surface measure and gradients by fixed factors, and their O(λ^−1) displacement is negligible compared with δ_λ². These observations justify applying this sliced estimate to every higher corner without an unproved small-volume-to-small-operator-norm inference.

For the ridge strip, surface measure is O(λ^−1); Hölder with boundary exponent 2(n−1)/(n−2) contributes λ^(−1/(n−1)). Together the three errors tend to zero. Kato's inequality permits applying the scalar estimates to norms of spinor sections. A uniform extension operator follows from the uniform radial bi-Lipschitz parametrizations; a fixed interior ball controls the constant mode by Poincaré's inequality.

## E. Boundary energy, limit and equality

Let A_λ be a nonzero harmonic spinor homomorphism with the degree-one local boundary condition, normalized in L² on P_λ. The Clifford anticommutator calculation and the integrated Schrödinger–Lichnerowicz identity give

    ∫|∇A_λ|² + (1/4)∫R_g|A_λ|²
      ≤ (1/2)∫_(Σ_λ) (||dη_λ||_tr − H_g)_+ |A_λ|².

The estimate in D makes the right-hand side at most ε_λ/2 times the sum of gradient energy and L² mass on a fixed interior ball, with ε_λ→0. Nonnegative scalar curvature and normalization imply gradient energy≤ε_λ/(2−ε_λ)→0. This is an absorption argument; small area by itself would not suffice.

Uniform W^(1,2) extensions give a strongly L²-convergent subsequence and a parallel limit A inside P. No mass is lost: if E_λ→A strongly in L² on a fixed neighborhood and P_λ converges to P with the same interior and vanishing boundary layer, then

    |∫_(P_λ)|E_λ|² − ∫_P|A|²|
      ≤ || |E_λ|²−|A|² ||_(L¹) + ∫_(P\P_λ)|A|² → 0.

The first term follows from Cauchy–Schwarz and strong L² convergence; the second follows from absolute continuity of the integral. Thus ||A||²_(L²(P))=1.

On a fixed compact subset of a facet interior, Σ_λ equals that facet and η_λ equals its reference normal. Compact trace convergence on that fixed boundary patch therefore passes the boundary relation to A. Parallel transport along segments from an interior point extends A smoothly to all of P and a neighborhood; the relation holds on closed facets by continuity. This extension need not remain parallel outside P, and none of the argument requires that.

Let c be Clifford multiplication for g and ω that for the fixed Euclidean reference. The boundary relation is c(ν_a)A=Aω(N_a). The matrix A* A is constant because A is parallel. Taking adjoints and composing shows it commutes with every ω(N_a). The normals span R^n: otherwise translation in a common orthogonal direction would preserve P, contradicting compactness. Irreducibility gives A* A=tI; t>0 because A is nonzero. Source and target spinor ranks agree, so A is invertible. At an intersection of two facets, applying the Clifford anticommutator now gives

    −2<ν_a,ν_b>_g A = −2<N_a,N_b> A.

Cancel A to get equality of the normal inner products. This directly yields the angle conclusion, without relying on the stronger flatness conclusion. For even n, apply the odd-dimensional argument to P×[−1,1] with g+dt²: scalar curvature is unchanged, side mean curvatures are unchanged, end faces are totally geodesic, and new angles are π/2. Restrict the resulting angle equalities back to P.

## Review outcome and limits

The author found no remaining mathematical gap in this smooth-category route on inspection of Bi's full argument and Brendle's stated smooth-domain dependency. This is not a certification of a recent preprint by the mathematical community. The independent reviewer should particularly rederive D, verify the precise boundary-index convention, and challenge the original problem's smoothness interpretation. The proof-application remains conditional until that independent gate accepts it. Neither the current UnsolvedMath detail page nor its missing AI notes were read.
