# Equal-pressure foam cells: curvature transport and realization gaps

## Disposition

This is a scoped partial analysis of Sullivan's Problem 21, not a solution. It neither proves finiteness of cell types nor decides whether a tetrahedral or dodecahedral cell occurs in a global equal-pressure foam in Euclidean three-space. No new global foam is constructed. No claim of mathematical novelty is made for consequences of classical Gauss–Bonnet or first variation.

The useful conclusions are an explicit necessary edge-curvature budget for low-face-count cells, a local minimal-surface example showing why one cannot discard the edge term cell by cell, a compact-support obstruction, and precise gaps in two possible routes to finiteness or construction.

## 1. Target and hypotheses

The primary problem asks about the possible combinatorial types in an equal-pressure foam, and singles out tetrahedral and dodecahedral types. Its next-page note also raises a two-faced cell. The source gives a geometric question, not an exhaustive list of technical conventions. [SM96]

We keep the ambient object global: a locally finite partition of R³ by embedded interfaces, smooth on face interiors, with only the usual triple-curve and tetrahedral-point Plateau junctions. Every interface has zero mean curvature, since the pressures agree. Equal cell volumes, periodicity, congruence, convexity and global area minimality are not part of the target. Sullivan's later definition allows nonsimple cells before making a separate simplicity restriction. [S98]

For the proved cellwise statements below, assume explicitly that the cell closure is a ball, its finitely many closed faces are disks, its borders are intervals, its boundary vertices have valence three, and ordinary facewise Gauss–Bonnet with finite curvature terms applies. Piecewise C² faces with the stipulated tangent angles suffice. Thus these statements apply to sufficiently regular realizations of the tetrahedral and dodecahedral combinatorial types; they do not classify nonsimple cells, circular-border two-faced cells, or unbounded cells. A proof in this restricted class alone would not be a resolution of the broad source question.

At a Plateau corner, the angle within a face is

α = arccos(−1/3),  θ = π−α = arccos(1/3),  δ = 3θ−π > 0.

Here θ is the exterior turning angle of a face boundary and δ is the intrinsic angle defect of one cell corner. For a cell with F faces, E edges and V vertices,

V = 2F−4,  E = 3F−6.

These follow from F−E+V=2 and 3V=2E.

## 2. Approach 1: the cellwise curvature transport identity

For each face f let K be Gaussian curvature. Define

Q(C) = −Σ_f ∫_f K dA ≥ 0,

because a Euclidean minimal surface has K≤0. Along a border e let κ_e be its space curvature vector, parametrized by arclength. For either incident face of C, let η_{f,e} be the unit conormal pointing from the border into that face. Put

B(C) = Σ_{f⊂∂C} Σ_{e⊂∂f} ∫_e κ_e·η_{f,e} ds,

T(C) = Σ_{e⊂∂C} ∫_e |κ_e| ds,

where T counts every cell edge once. Q, B and T are dimensionless and invariant under homotheties.

**Proposition 1.** Under the stated simple-cell hypotheses,

B(C) = 4π + Q(C) − (2F−4)δ,

and therefore

T(C) ≥ |4π + Q(C) − (2F−4)δ|.

**Proof.** Facewise Gauss–Bonnet is

∫_f K + Σ_{e⊂∂f} ∫_e κ_e·η_{f,e} + n_f θ = 2π.

Summing over the F faces gives −Q+B+3Vθ=2πF. Substitute F=2+V/2 to obtain −Q+B+Vδ=4π.

At a triple curve there are three sheet conormals η₁,η₂,η₃, with pairwise inner product −1/2 and sum zero. A given cell is bounded by two sheets. Their conormal sum has norm one:

|η_i+η_j|² = 1+1+2(−1/2)=1.

Consequently the absolute value of that cell's integrand along this edge is at most |κ_e|. Integrating and summing proves |B|≤T. ∎

The Gauss–Bonnet mechanism and cancellation in an average are classical, due to Kusner. [K92] The point here is to retain and quantitatively control the uncancelled cellwise term.

For F≤13 the zero-Q deficit is positive, so the proposition in particular gives

T(C) ≥ D_F + Q(C),  D_F = 4π − (2F−4)δ.

Certified rational enclosures in the accompanying checker imply the following decimal displays:

- Tetrahedral type, F=4: D₄ ≈ 10.3612282206
- Dodecahedral type, F=12: D₁₂ ≈ 1.5406586457
- F=13: D₁₃ ≈ 0.4380874488
- F=14: D₁₄ ≈ −0.6644837480

These are necessary amounts of total edge curvature, not nonexistence results. No bound contradicting them is proved.

**Corollary 1.** Such a simple bounded cell cannot have every border straight. In particular it cannot be convex.

**Proof.** If all borders are straight, their geodesic curvatures vanish in every incident face. A face with m sides would satisfy −Q_f+mθ=2π, and hence mθ≥2π. Since 5θ<2π, every face has at least six sides. But Σm=2E=6F−12<6F, a contradiction. For a convex cell, both principal curvatures of every smooth face have the same sign. Their zero sum forces each face to be planar. Adjacent planar faces at angle 120° meet along straight borders, reducing to the contradiction just obtained. ∎

This does not exclude a cell merely because its *combinatorial* name is that of a convex polyhedron. Its actual interfaces may be saddle-shaped and its borders curved.

## 3. Approach 2: an exact local obstruction to the sign shortcut

One tempting but invalid strengthening would assert B(C)≤0 for each cell and then use Proposition 1 to force F≥14. The local Plateau and zero-mean-curvature equations do not supply that sign.

Let Γ be the unit circle in z=0, let a=√3/2 and b=log(√3), and take the following three small sheets on one side of their common boundary Γ:

- The planar annulus z=0, 1≤r≤1+ε, truncated at its outer circle.
- The catenoid annulus r=a cosh(z/a−b), 0≤z≤ε.
- Its reflection in z=0, −ε≤z≤0.

Choose ε>0 sufficiently small, for example ε<ab. These annuli are embedded and otherwise disjoint. A surface of revolution r=r(z) is minimal precisely when rr″=1+(r′)²; the given catenoid satisfies this identically: with u=z/a−b, one has r′=sinh u and r″=cosh u/a, hence rr″−(r′)²=cosh²u−sinh²u=1 for every z. Also r(0)=1 and r′(0)=−1/√3.

Writing e_r and e_z for the radial and vertical unit vectors, the three inward sheet conormals on Γ are

η₀=e_r,  η₊=−e_r/2+√3 e_z/2,  η₋=−e_r/2−√3 e_z/2.

Their pairwise dot products are −1/2. Thus this is an exact minimal-surface Plateau triple junction. Since κ_Γ=−e_r, the three sheet geodesic curvatures are −1, 1/2, 1/2. The contributions of the three adjacent local regions, each bounded by a pair of sheets, are consequently

2π, −π, −π

after integration around Γ. They cancel only after summing over all three regions. The positive region also realizes equality in the local estimate |B_e|≤∫_Γ|κ|.

This is a local construction with artificial outer boundary curves. It is not a bounded cell, is not a space-filling foam, and is not a counterexample to Sullivan's conjecture. It proves only that a sign argument based solely on the local minimal/Plateau equations is insufficient. Whether global realizability imposes a useful additional sign or transport restriction is left open.

## 4. Approach 3: dilation and the finite-cluster obstruction

**Proposition 2.** There is no nonempty compactly supported, finite-area, boundaryless regular Plateau film system in R³ whose interfaces are all minimal and whose triple-curve conormals balance.

**Proof.** Count each interface once. For every compactly supported smooth vector field X, the first variation is

δA(X)=Σ_f ∫_f div_f X.

The interior mean-curvature terms vanish. Along internal borders the three boundary conormal terms cancel; isolated vertices contribute no line boundary term. Thus δA(X)=0. Choose X equal to the position vector x on a neighborhood of the compact support, with a smooth cutoff farther away. Since div_f x=2 on each two-dimensional tangent plane,

0=δA(X)=2A,

which is impossible for a nonempty regular film system. ∎

This is the standard no-compact-stationary-surface argument, written here to audit a proposed finite construction. It does not apply to an infinite foam or to a patch attached to a frame. A finite cluster of bubbles can also have equal *interior* pressures different from the exterior pressure; that case does not satisfy the proposition's all-interface minimality assumption.

**Remaining gap.** A finite local collection of zero-mean-curvature faces with correct angles needs a global extension. Free finite truncation cannot provide it, and a wire frame changes the problem.

## 5. Approach 4: a conditional finite-type criterion

**Proposition 3.** Consider a class of cells satisfying the hypotheses of Section 1. If a common finite constant M obeys Q(C)+T(C)≤M for every cell in this class, then the class has only finitely many combinatorial cell types.

**Proof.** Proposition 1 gives

(2F−4)δ = 4π+Q−B ≤ 4π+Q+T ≤ 4π+M.

Hence F≤2+(4π+M)/(2δ), and V=2F−4 and E=3F−6 are uniformly bounded too. There are only finitely many ways to pair finitely many half-edges and choose cyclic orders at the resulting vertices. Restricting this finite set to the spherical disk-face embeddings in the class leaves finitely many incidence types. ∎

The exact identity shows that a face-count bound is equivalent, in this category, to a bound on Q−B. Controlling Q+T is a stronger sufficient condition. This is a reduction, not an a priori curvature estimate. Scaling cells to unit size does not create one: all three integrated quantities are scale invariant. No argument here prevents curvature concentration, thin features, or degeneration across a family of cells. An average curvature estimate would likewise not automatically give the required per-cell bound.

## 6. Approach 5: a periodic stellar-insertion obstruction

Start at the combinatorial level with a periodic simple cell decomposition, dual to a triangulation. Subdivide a dual tetrahedron by inserting an interior vertex and coning it to its four faces. The dual operation inserts a tetrahedral cell at a foam corner. It creates one new cell with four faces and adds one face to each of the four adjacent old cells, counted with multiplicity if needed in a quotient. Therefore

N′=N+1,  S′=S+8,

where S is the sum of cell face counts in a periodic quotient. After t such operations, N_t=N+t and S_t=S+8t. This is a topological operation already described by Sullivan; it does not construct minimal surfaces. [S98]

For a starting decomposition having 14 faces per cell, the new average is

f̄_t=(14N+8t)/(N+t).

For any eventual simple equal-pressure geometric realization in a compact flat quotient, summing Proposition 1 cancels B and yields Kusner's necessary average bound

f̄ ≥ f_* := 2+2π/δ = 13.3973325714376… .

Consequently the insertion density must satisfy

t/N ≤ (14−f_*)/(f_*−8) = 0.1116602359750… .

The checker proves the following arithmetic comparisons with rational interval bounds, not floating-point decisions:

- A single insertion fails this necessary average test when N≤8.
- At N=9, the arithmetic average is 134/10=13.4>f_* and passes the test.
- Full corner decoration has t=6N and average 62/7, far below f_*.

The N=9 line is only a count threshold. It is not a constructed nine-cell periodic quotient, and passing the inequality is not evidence of a geometric realization. At sufficiently large quotient size the average obstruction leaves room for a sparse tetrahedral defect. No Plateau/minimal-surface gluing or existence argument for that defect is established. This makes explicit why an average theorem alone cannot exclude the occurrence question.

## 7. What is and is not established

Five distinct bounded approaches have now been used: cellwise curvature transport, an exact local minimal junction, dilation/extension, curvature compactness, and periodic combinatorial insertion. None produces a full candidate or a verified prior resolution. The original three conclusions remain undecided in this work. The two-faced continuation is also unresolved; the annular local example does not provide two complete minimal disks spanning a common curve or a global foam containing such a cell.

The partial results are analytic proofs under explicit hypotheses. The checker validates supporting incidence algebra, exact conormal calculations and rigorous scalar interval comparisons. It does not verify PDE existence, embedded global extension, stability, or exhaustive classification. There are no numerical foam simulations in this packet.

The best next mathematical requirement is substantive: either prove a uniform per-cell geometric bound sufficient for Proposition 3, or construct and verify a globally space-filling equal-pressure foam outside the currently controlled types. The local catenoid patch and topological subdivisions do not meet that requirement.

## References and inspected source scope

- [SM96] J. M. Sullivan and F. Morgan, editors, *Open Problems in Soap Bubble Geometry*, International Journal of Mathematics 7(6) (1996), 833–842. DOI: https://doi.org/10.1142/S0129167X9600044X . Author PDF: https://page.math.tu-berlin.de/~sullivan/Papers/foams/soap-prob.pdf . Entire 8-page author version read; Problem 21 and its continuation visually inspected on pp.4–5. Publication pagination differs from this author version.
- [K92] R. Kusner, *The Number of Faces in a Minimal Foam*, Proceedings of the Royal Society A 439 (1992), 683–686. DOI: https://doi.org/10.1098/rspa.1992.0177 . ResearchGate full-text representation inspected at https://www.researchgate.net/publication/2348802_The_number_of_faces_in_a_minimal_foam , especially Theorem 1, its proof and the noncompact qualification. The page labels its text a publisher-provided preview; that provenance was not independently verified. Equations were rederived above because extraction is imperfect. No downloaded/inspected Kusner PDF is claimed.
- [S98] J. M. Sullivan, *The Geometry of Bubbles and Foams*, in *Foams and Emulsions*, 379–402. DOI: https://doi.org/10.1007/978-94-015-9157-7_23 . Author PDF: https://page.math.tu-berlin.de/~sullivan/Papers/cargese/cargese.pdf . Sections 5–6, printed pp.388–393, inspected for the category, average cancellation and topological subdivision discussion.

The fresh literature check on 8 October 2026 was bounded. Failure to locate a full resolution is not a certificate of worldwide openness. Contemporary finite-cluster isoperimetric results, idealized spherical-cap cells, and equal-volume numerical foams do not by themselves settle this global equal-pressure classification.

## Independent audit clarification

The derivative retains the original mathematical conclusions. The planar sheet now has an explicit artificial outer boundary, the minimal-surface ODE is expanded for every z, and the two-faced continuation is explicitly carried into the final unresolved status. The original checker retains its 56 checks and 7 input-validation controls; its catenoid ODE check is only at the common circle. The independent audit separately verifies the all-parameter algebraic ODE identity, exact scalar intervals, and semantic controls. Neither checker certifies the analytic proofs or global realizability by computation.
