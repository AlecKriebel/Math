# Audit: flat-end rigidity under the candidate’s weak asymptotics

## Verdict

**Pass.** The claim used in Sections 2–3 of `public/PROOF.md` is correct. The cited positive mass theorem is an appropriate source, provided that the sentence about changing the flat end to Euclidean coordinates is justified. That justification needs only the stated bounds on the metric and its first derivatives; it does not require weighted second-derivative decay or even the extra unweighted smooth convergence hypothesis.

Here “one end” means, as in the actual candidate, that the entire complement of a compact subset of M is the displayed coordinate exterior. The proof below is not an argument for a manifold with additional uncontrolled ends.

## 1. Flat asymptotically Euclidean end is exactly Euclidean near infinity

Assume for contradiction that Rm(g)=0 outside a compact subset of M. Enlarge the original compact subset so that the whole coordinate domain

E = {x in R^3 : |x| > R_0}

is flat, and g = delta + h there, with h=O(r^-1), Dh=O(r^-2). Increase R_0 if necessary so that g and delta are uniformly equivalent. The Christoffel symbols in these coordinates satisfy Gamma=O(r^-2).

The exterior E is simply connected. Flatness of the Levi-Civita connection therefore produces a global parallel orthonormal coframe theta^1, theta^2, theta^3 on E. Torsion-freeness implies d theta^a=0, and simple connectivity implies theta^a=dF^a for globally defined smooth functions. Consequently the map F=(F^1,F^2,F^3) is a local diffeomorphism and

g = sum_a dF^a tensor dF^a = F^*delta.

Write theta^a = A^a_i dx^i, so DF=A and A^T A=g. In particular A is uniformly bounded. Parallelness gives

partial_j A^a_i = Gamma^k_{ji} A^a_k = O(r^-2).

For each unit vector omega, radial integration shows that A(r omega) converges to a matrix A_infinity(omega), with error O(r^-1), uniformly in omega. For any two directions omega and eta, integration along a shortest great-circle arc of the coordinate sphere gives

|A(r omega)-A(r eta)| <= C/r.

Hence A_infinity is one constant matrix Q. Since A^T A=g approaches delta, Q is orthogonal. Replace F by Q^{-1}F. We then have

DF = I + O(r^-1),                 F(x) = x + O(log r).

The second estimate follows by integrating DF-I along radial rays from one fixed sphere, whose starting values are uniformly bounded. In particular |F(x)| tends to infinity as |x| tends to infinity.

### Global injectivity after shrinking the end

Choose R_1>R_0 such that |DF-I| <= epsilon on {r>=R_1}, with epsilon*pi/2<1. Any two points x,y in this closed exterior can be joined within it by a rectifiable curve of length at most (pi/2)|x-y|: use the straight segment, replacing its portion inside the ball by the shorter great-circle arc between entry and exit. Integration yields

|F(x)-F(y)-(x-y)| <= epsilon*(pi/2)*|x-y|.

Thus F is injective on {r>=R_1}. Notice that this argument avoids the invalid inference that a local developing map is automatically globally injective.

### The image contains an exact Euclidean exterior

Choose S > max_{r=R_1}|F(x)|. Let U={y:|y|>S}. The set F({r>R_1}) intersect U is nonempty because F tends to infinity, and it is relatively open in U because F is a local diffeomorphism. It is relatively closed in U as well: for a convergent sequence of image points in U, the preimages remain bounded by the proper-at-infinity estimate; a subsequential limit cannot lie on r=R_1 because that sphere maps inside B_S. Since U is connected, F({r>R_1}) contains U.

Injectivity now makes

F : F^{-1}(U) -> U

a diffeomorphism and an isometry. The complement of F^{-1}(U) in M is compact, again by F(x)=x+O(log r). This is the claimed genuine Euclidean exterior. Its inner boundary need not be an original coordinate sphere; shrinking the end is essential to the precise formulation.

## 2. Match the positive mass theorem’s hypotheses

In the new coordinates y=F(x), the metric equals delta identically for |y|>S. Thus it satisfies every weighted derivative asymptotic condition required in the cited theorem, in particular g-delta=O_2(|y|^-tau) for any tau>1/2. The ADM integral on each sufficiently large y-sphere is exactly zero.

Scalar curvature vanishes outside a compact subset. Smoothness therefore implies R_g is integrable with respect to dV_g. Completeness, connectedness, absence of boundary, and nonnegative scalar curvature are unchanged by the coordinate construction. All hypotheses of the three-dimensional zero-mass rigidity theorem are now met, so (M,g) is isometric to Euclidean R^3, contrary to the candidate’s assumption.

There is no need to assert mass invariance between the original weak coordinate chart and the Euclidean chart. Compute the mass in the latter chart, where all standard hypotheses hold. Nor is the positive mass theorem being applied to the auxiliary transplanted metric later in the candidate.

It follows contrapositively that nonzero Riemann curvature occurs arbitrarily far out in the original end.

## 3. Orientability and topology

The cited AMO Theorem 2.1 is stated for complete asymptotically flat 3-manifolds without a restriction on orientability, fundamental group, or H_2. The H_2=0 assumption of their earlier Green-function Theorem 1.1 is not an assumption of Theorem 2.1. Their proof explicitly invokes the general-topology reduction from Bray–Kazaras–Khuri–Stern, Proposition 2.1; that proposition’s proof begins by passing to the orientable double cover when needed.

For an independently explicit orientation check, if M were nonorientable, its connected orientation double cover would be complete and boundary-free, with nonnegative scalar curvature. The simply connected Euclidean end lifts to two Euclidean ends, each of ADM mass zero; the compact core lifts to a compact core. The orientable, multiple-ended positive mass theorem would then force this cover to be Euclidean R^3, contradicting its two ends. Thus restricting a preferred formulation of PMT to orientable manifolds creates no gap here.

## 4. Verified primary sources and exact locations

1. Virginia Agostiniani, Lorenzo Mazzieri, Francesca Oronzio, *A Green’s Function Proof of the Positive Mass Theorem*, Communications in Mathematical Physics 405, article 54 (2024), DOI 10.1007/s00220-024-04941-8.
   - Published Theorem 2.1, PDF p. 10: nonnegative ADM mass and zero-mass Euclidean rigidity for complete AF 3-manifolds with nonnegative scalar curvature.
   - PDF p. 11, Eq. (2.1) and accompanying paragraph: O_2(r^-tau), tau>1/2, and integrable scalar curvature.
   - PDF p. 13, final paragraph of Section 2: general rigidity follows by the standard Schoen–Yau argument from positivity.
   - Published article: https://link.springer.com/article/10.1007/s00220-024-04941-8
   - Published PDF: https://link.springer.com/content/pdf/10.1007/s00220-024-04941-8.pdf

2. Hubert L. Bray, Demetre P. Kazaras, Marcus A. Khuri, Daniel L. Stern, *Harmonic Functions and the Mass of 3-Dimensional Asymptotically Flat Riemannian Manifolds*, Journal of Geometric Analysis 32, article 184 (2022), DOI 10.1007/s12220-022-00924-0.
   - Author-hosted paper p. 1: AF definition allows finitely many ends and requires scalar-curvature integrability; Theorem 1.1 includes zero-mass rigidity.
   - Proposition 2.1 on pp. 2–3: reduction to R^3 with Schwarzschild asymptotics; the first sentence of its proof on p. 3 explicitly handles nonorientability by a double cover.
   - Author-hosted primary PDF: https://www.math.stonybrook.edu/~khuri/Bray_Kazaras_Khuri_Stern_PMT.pdf
   - arXiv record: https://arxiv.org/abs/1911.06754

The developing-map argument in Section 1 above is supplied directly, rather than attributed to an unverified auxiliary source.

## Suggested candidate amendment

The current compact sentence is mathematically sound but suppresses a nontrivial step. Add a lemma or short appendix giving the parallel-coframe/developing-map argument. At minimum state: flatness and simple connectivity provide developing coordinates with DF=Q+O(r^-1); these are injective sufficiently far out and contain a Euclidean exterior, so the PMT is applied in exactly Euclidean coordinates. Explicitly add that scalar curvature is then compactly supported and hence integrable.
