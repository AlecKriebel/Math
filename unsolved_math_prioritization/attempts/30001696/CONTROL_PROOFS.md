# Controls against unsupported priority adapters

These are tests of proposed implications between prior results and the exact target. They are not additional original attempts to solve Question 4, and they are not counterexamples to the candidate proof. The universal deductions below are proved directly; the small exact-arithmetic replay is only a check against transcription mistakes.

## 1. The coordinate collapse core is not an interior spine

The coordinate copy of B(i,i+1) in B(i,d) contains e_1. At e_1, zero-deleted sign variation s^- is zero, whereas maximal sign variation s^+ is d-1: fill the trailing zero coordinates with alternating signs. For every 0<=i<=d-2, vectors (1,-epsilon,+epsilon,-epsilon,...) with epsilon>0 arbitrarily small have d-1 variations and lie outside the bounded-variation cone. After radial normalization they still lie outside its spherical section and approach e_1. Therefore e_1 lies on the boundary of B(i,d), and B(i,d) is not an ambient neighborhood of that coordinate core.

This blocks the direct use of the regular-neighborhood characterization in Bryant, Theorem 3.16, or the original Rourke--Sanderson, Corollary 3.30: its input is a **neighborhood** of the collapsed polyhedron in the interior of the ambient manifold. Collapse alone does not supply that input for the original complex. The obstruction does not deny the disc-bundle assertion of Klee--Novik Remark 3.7; it denies this direct shortcut to a *trivial* bundle.

**Post-seal repair:** CLASSICAL_PRIOR_ADAPTER_INDEPENDENT_CHECK.md verifies that adding an outward collar in the complementary PL manifold yields N, PL homeomorphic to B, with B contained in int N and N collapsing to the same coordinate sphere. Corollary 3.30 then applies to N. This control remains true but no longer blocks the repaired classical subsumption route. No new pushed-in spine or stable bundle classification is needed.

## 2. A Chebyshev subspace does not make the cone translation-convex

For the ordinary degree-one polynomial evaluation space on four increasing nodes, take y=(-3,-1,1,3), which has one sign change. Take x=(4,1/10,1/10,1/10), which has no sign changes. Their sum is (1,-9/10,11/10,31/10), which has two. Thus containing all nonzero vectors of a low-variation linear subspace does not imply C_1+E is contained in C_1. Positive diagonal changes of coordinates transport this example to weighted evaluation spaces.

This is only a control against an unproved global star-shaped or translation-convex adapter. It says nothing about a fixed spectral fiber, a suitably chosen local tube, or the candidate's flow-hitting construction.

## 3. Rank-k strict positivity of one linear map does not classify the cone section

In R^4=R^2_y direct-sum R^2_z set

    C_0 = {(y,z): ||z|| <= ||y||},
    L = R(1,0,2,0),
    C = C_0 union L,
    T = diag(4,3,1,1/2).

C is closed, invariant under multiplication by every real scalar, and has nonempty interior. E=R^2_y direct-sum {0} lies in C. F={0} direct-sum R^2_z intersects C only at zero. Every three-dimensional linear subspace intersects F nontrivially, so no such subspace can lie in C; consequently C has rank exactly two.

For a nonzero point of C_0, ||Tz||<=||z||<=||y||<=||Ty||/3, so its image lies in the interior of C_0. T sends a nonzero point of L to a vector proportional to (4,0,2,0), also strictly inside C_0. Thus T(C minus {0}) is contained in int(C). This meets the cone hypotheses printed in Oliva--Kuhl--Magalhaes, Theorem 2.11 (attributed there to Fusco--Oliva), and Mostajeran--Sepulchre, Theorem 1.2.

Nevertheless C intersect S^3 consists of the connected section C_0 intersect S^3 together with two isolated antipodal points from L. It is disconnected, unlike S^1 times D^2. The cited theorems correctly give invariant E,F and a spectral gap; they cannot by themselves imply the desired whole-section product.

This control concerns one strictly positive linear map and the explicitly printed general-cone hypotheses. It does **not** assert strict positivity under every positive time of a continuous semigroup and is **not** a counterexample to the candidate's bounded-variation cone.

## 4. The normalized sphere flow does not satisfy the point-attractor flow definition

The flow Phi_t(x)=exp(tA)x/||exp(tA)x|| preserves norm one. Every unit eigenvector of A, and its negative, is fixed. Hence it is not a strictly norm-shrinking flow on R^N with a unique fixed origin as required by Galashin--Karp--Lam, Definition 2.1 and Lemma 2.2. In particular, the attracting sphere for i>=1 contains more than one fixed eigenvector pair. A direct global application of Lemma 2.3 would give a closed ball, contrary to the already established S^i homology for i>=1.

The candidate can borrow the continuous hitting-time mechanism of Lemma 2.3, but a sphere-attractor extension and continuity at that entire sphere are additional arguments. A fiberwise invocation would also require a verified invariant fiber structure and compatible trivialization; those inputs are not consequences of the point-attractor lemma alone.

## 5. A cited stable-range assertion has a real range restriction

Wall's 1962--1964 lecture notes, retyped in 2011, Corollary IV.6.14 on printed page 131, uses c>=m+1. With sphere dimension m=i and intended disk rank c=d-i-1, this condition need not hold; for example (d,i)=(6,3) gives c=2 and m=3. Corollary IV.6.9 also has n>=6 and c>=3 and requires a suitable smooth embedded core, simple homotopy equivalence, and boundary fundamental-group condition. These specific results therefore do not supply an all-dimensional PL trivialization merely from the words 'disc bundle' and 'stably trivial'.

This does not assert that no stronger theorem exists. It records the actual missing hypotheses of the accessible classical source checked in this family.
