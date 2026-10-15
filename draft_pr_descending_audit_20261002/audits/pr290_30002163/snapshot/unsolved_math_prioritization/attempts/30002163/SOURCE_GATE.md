# Exact source gate: spherical Fibonacci minimum distance

2026-10-01 15:55 UTC. Problem 30002163 / OWR-12012-001, queue rank 313. Source-only checkpoint, 0/5 substantive author turns. Estimated progress toward resolving the target: 10%.

## Original statement and construction

Johann S. Brauchart's contribution, *Spherical Nets, Sequences and Lattice rules — construction of low-discrepancy sequences on spheres*, OWR 40/2012, printed pp. 2436–2439, explicitly poses the finite minimum-distance conjecture on p. 2438. The entire contribution was read and the target page visually inspected. The workshop took place in August 2012; the volume was published May 29, 2013. No discrepancy asymptotic is being substituted for this finite separation problem.

Let F_1=F_2=1 and F_n=F_(n-1)+F_(n-2), and set q=F_n, p=F_(n-1). For q>=2, use exactly

    z_k=(r_k cos(2pi p k/q), r_k sin(2pi p k/q), 1-2k/q),
    r_k=2 sqrt[(k/q)(1-k/q)],  0<=k<q.

These lie on the unit sphere. Distance is the ordinary Euclidean chord in R^3, not geodesic arc length, squared distance, planar lattice distance or half the separation. The conjecture is

    min_(0<=i<j<q) |z_i-z_j| = |z_0-z_1| = 2/sqrt(q).

The single-point cases q=1 have no pairwise minimum and are excluded as vacuous construction endpoints. No shift of the heights or replacement of the rational rotation p/q by the irrational golden angle is allowed.

## Source indexing and companion-paper correspondence

The report first defines 0<=k<q but then prints the set as {z_1,...,z_q}; the conjectured pair explicitly uses z_0. We preserve and disclose this indexing slip. If the displayed formula is instead evaluated at 1<=k<=q, the resulting set is congruent: k maps to q-k under the orthogonal transformation (x,y,z)->(x,-y,-z). Thus the minimum value is the same under either endpoint convention; the stated attaining pair z_0,z_1 belongs to the zero-based one.

The cited complete paper Aistleitner–Brauchart–Dick, *Point sets on the sphere S^2 with small spherical cap discrepancy*, arXiv:1109.3265v1, later Discrete & Computational Geometry 48 (2012), 990–1024, gives F_1=F_2=1, zero-based indexing and the Lambert map in §5.2 (author PDF p. 14) and equation (7) (p. 5). Its planar lattice is written with the two coordinates interchanged relative to the OWR parametrization. This is not a different metric target: reindex by multiplication by p modulo q. Cassini gives p^2 congruent to (-1)^n modulo q, so p^(-1) is congruent to (-1)^n p. The resulting angular orientation agrees with OWR or differs by reflection. The unordered spherical point sets are isometric. Its Lemma 17 computes planar shortest distances for a discrepancy proof; those planar distances do not establish the desired spherical minimum.

## Literature and prior-attempt gate

The full original report and full 2011 companion PDF were recovered from primary sources. The report's reference 'Brauchart and Dick, Spherical Fibonacci points' was in preparation; the imported dataset incorrectly labels arXiv:1109.3265 with that title. Its actual title and three authors are given above.

Targeted primary searches for the exact separation formula, spherical Fibonacci minimum distance, and later Brauchart–Dick work found the original conjecture plus subsequent work/talks on discrepancy and hyperuniformity. The 2022 primary conference abstract *Spherical Fibonacci Points: Hyperuniformity, and more* and the 2024 AMS–UMI abstract discuss those distinct quantities; neither supplies an exact minimum-distance theorem. This is limited literature checking, not proof that no later resolution exists. Recent graphics constructions with shifted heights, golden-angle rotations or planar-grid minima are not interchangeable with the present source.

Exact ID, source code and spherical-Fibonacci-title PR searches were empty. The target branch search, both main attempt-directory commit histories and local all-ref histories were empty. The complete pinned imported record was read; its prior report is empty. Related-target-group screening found no matching group. The imported automated literature paragraph is not a prior campaign proof attempt.

Success requires either a proof for every nontrivial Fibonacci size q, with exact endpoint/metric conventions, or a rigorously certified violating pair in this actual construction. Numerical sampling alone is insufficient. Five substantive author turns are available; source validation does not consume one. Independent full review is required before any claimed-result PR.
