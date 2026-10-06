# Independent adversarial review of the flex point section genus

Problem 30003711 / OWR-15987-022. Review date: 2026-10-06.

## Decision and exact scope

The frozen author's proof establishes that the ordinary, unnormalized, section-based Schwarz genus of the nine-flex covering over the smooth cubic coefficient space is 8, using the cited Chen–Wan lower bound. I found no mathematical correction required in that proof. The new upper-bound argument has been reconstructed below independently of any other review.

This acceptance does not determine the stronger invariant obtained by insisting on connected domains and simultaneous trivialization of all nine sheets. It therefore does not authorize an unqualified claim that the literal definition in the original Oberwolfach question has been resolved. The author's manuscript already makes this distinction explicitly; no scope-correction patch is needed.

This is mathematical review with finite exact diagnostics, not a formal proof-assistant certificate. The lower bound, the classical Hesse description, and standard differential-topological and dimension-theoretic theorems remain identified theorem inputs. File hashes establish identity, not mathematical validity. No novelty or priority certification is made.

## Reviewed object

The reviewed archive is FLEX_POINT_GENUS_30003711_AUTHOR_SAFE_FREEZE.zip, 11,645 bytes, SHA-256 aebc26755d47059931adcc815cc5feb198c62346a317dfee665d878ef9b0066a. Its external manifest is 1,727 bytes, SHA-256 6c06a0e757dece40dd4d3176d64794f577f1621897cba2ca40be98859fadaaf6.

The central manuscript is flex_point_genus_30003711/PROOF.md inside that archive, 11,369 bytes, SHA-256 c42d7adb46caa0fd5fbaa4ad6006baf711a2a6674a69375671fa9cd86141b965. All five archive members were checked against the external manifest and against the supplied author files. The original archive, manifest, and author files were left unchanged. The audit package contains neither source PDFs nor source extracts nor a copy of the private diagnostic implementation.

## Base space and imported mathematical inputs

Set X = CP^9 minus the discriminant, so a point is a smooth ternary cubic equation modulo a nonzero scalar. Coordinates have not been quotiented by PGL_3(C). Let Y consist of pairs (F,p) with p a flex of F. The map Y to X is a genuine nine-sheeted covering. A section selects one flex and need not label the remaining eight.

The inspected source for the numerical lower bound is Chen–Wan, arXiv:2306.17303v2, Theorem 4.1. Its definition is the unnormalized section convention used here. The cited lower bound is accepted as an external theorem; this review does not re-prove the Leary cohomology calculation underlying it. The same version supplies the Hesse quotient model in Lemma 3.2 and Proposition 3.3. Only these applicable results and their hypotheses are imported; no algorithmic equality is inferred.

Artebani–Dolgachev, Sections 2 and 4, supplies the Hesse pencil, the common flex configuration, and the Hessian semidirect product. The relevant group is ASL_2(F_3), not the larger affine group AGL_2(F_3). Proposition 4.1 in that source and its surrounding discussion distinguish the two. Its labeling of the flex points differs from the Chen–Wan labeling, so the audit uses the latter's explicit origin and matrices consistently.

The topological inputs are the compact-group invariant-metric and tubular-neighborhood theorems, homotopy lifting for genuine covering maps, finite-group equivariant triangulation, and the finite-cover refinement/partition-of-unity facts for finite-dimensional compact metrizable spaces. The finite-group triangulation input is Illman's 1978 theorem. Its publisher record was inspected; its subscription full text was not retrieved. These are theorem dependencies rather than new claims proved by the finite diagnostic.

## Hesse model and the pullback to the compact homogeneous cover

Write P = PGL_3(C), G = PU(3), T = C minus the three cube roots of unity, and omega = exp(2 pi i/3). The pencil is F_lambda = x^3 + y^3 + z^3 - 3 lambda xyz. Its smooth members have a common nine-element flex set S. The Hessian group Gamma is a finite subgroup of G of order 216, acting on S as F_3^2 semidirect SL_2(F_3). For p_0 = [1:-1:0], the point stabilizer Gamma_0 has order 24 and is the linear complement SL_2(F_3).

The classical quotient descriptions are X = (P times T)/Gamma and Y = (P times T)/Gamma_0, with right multiplication in P accompanied by the inverse action in T. In particular, these are quotients of the parameterization space, not coarse quotients of X by projective coordinate change. The right action on the first factor is free even at the special pencil members with extra automorphisms.

For an invertible matrix M define u(M) = M(M* M)^(-1/2). For a nonzero scalar c, u(cM) = (c/|c|)u(M), so u induces r:P to G. If U is unitary, functional calculus gives (U* M* M U)^(-1/2) = U*(M* M)^(-1/2)U, hence r(MU) = r(M)U. This is the required right-G equivariance, not merely an unqualified homotopy equivalence.

Consequently the map [g,lambda]_Gamma to r(g)Gamma is well defined. Above it the map [g,lambda]_Gamma_0 to r(g)Gamma_0 identifies Y to X with the pullback of p:G/Gamma_0 to G/Gamma. To see the fiber identification explicitly, fix [g,lambda]_Gamma. Its nine lifts are represented by [g gamma,gamma^(-1)lambda]_Gamma_0, indexed by gamma Gamma_0 in Gamma/Gamma_0. Their images are r(g)gamma Gamma_0, the nine distinct points over r(g)Gamma. This continuous fiberwise bijection between covering spaces is an isomorphism of covers, as one sees in evenly covered neighborhoods.

Thus it suffices to construct eight section domains for p. The compact manifold M = G/Gamma has real dimension 8, and E = G/Gamma_0 to M is a genuine covering. There is no problematic quotient-cover assertion here.

## Algebraic reconstruction of the spectral lemma

Use the matrices

A = ((0,0,1),(1,0,0),(0,1,0)),
B = diag(1,omega,omega^2),
C = diag(1,1,omega).

The projective subgroup K generated by A and B is F_3^2. The noncommutation of matrix lifts is only a scalar: BA = omega AB. Hence projective elements A^a B^b give well-defined translation coordinates (a,b). Their action on p_0 is simply transitive on S. The element C fixes p_0, belongs to Gamma_0, and direct matrix multiplication gives C A C^(-1) = AB and C B C^(-1) = B, already for the displayed lifts. Therefore C acts on K by the matrix U_1 = ((1,0),(1,1)).

Let gamma act on F_3^2 by v to Lv+t, with L in SL_2(F_3). A fixed point solves (I-L)v=t. If I-L is invertible, a unique solution exists. Thus any fixed-point-free gamma has det(I-L)=0. Since det L=1, this implies trace L=2 and characteristic polynomial (z-1)^2. Cayley–Hamilton gives (L-I)^2=0.

If L=I, then t is a nonzero translation. For a=0 and b nonzero, B^b has three distinct eigenvalues. If a is nonzero, A^a B^b is a monomial matrix with a single 3-cycle as its underlying permutation.

If L is not I, put N=L-I. Its image and kernel are the same one-dimensional line. Choose a nonzero u in that line and v such that det(v,u)=1. Then Nv=c u with c equal to 1 or 2, while Nu=0. In the determinant-one basis (v,u), L becomes U_c = ((1,0),(c,1)). This proves that the two displayed shear forms suffice under SL_2 conjugacy; no unjustified GL_2 conjugation is substituted. A conjugating matrix in SL_2 lifts to an element of the complement Gamma_0. After that projective conjugation, gamma has the unique affine decomposition A^a B^b C^c.

When a=0 the affine action is (x,y) to (x,y+cx+b), which fixes all three points on x=-b/c. Thus in the fixed-point-free case a is nonzero. Its displayed matrix lift is again monomial with a 3-cycle. For such a matrix the characteristic polynomial is z^3-d_1 d_2 d_3, where the three weights are nonzero. The polynomial and its derivative 3z^2 have no common root, so its eigenvalues are distinct over C. Multiplying the matrix by any nonzero scalar or conjugating it preserves eigenvalue multiplicities. This establishes the lemma for every projective representative and every gamma, rather than only for an enumerated subset.

As an additional exact diagnostic, all 216 projective matrices generated by A, B, C, and the Chen–Wan matrix D were enumerated over Q(omega). Their actions on the nine points were reconstructed and checked to be affine with determinant-one linear part. There are 56 fixed-point-free elements, 135 with one fixed flex, 24 with three fixed flexes, and the identity with nine. None of the 56 has a repeated eigenvalue. The nonidentity unipotents in SL_2(F_3) split into two conjugacy classes of four. These counts support the hand argument; the argument does not depend on trusting the diagnostic implementation. FINITE_GROUP_DIAGNOSTICS.json records only mathematical results and verification scope, with no private checker digest.

## The common fixed sheet and the nonfree circle action

Take H = {diag(1,z,z): |z|=1} in G. The map from U(1) into G is injective, since a scalar equality of these diagonal matrices forces the first scalar to be 1 and then z to agree. Therefore H is a genuine embedded circle.

For any g in G, J_g = Gamma intersect g^(-1)Hg is finite and isomorphic to a finite subgroup of a circle; in particular it is cyclic. If it is nontrivial, a generator has a matrix representative with exactly two distinct eigenvalues, one repeated, because it is conjugate projectively to diag(1,z,z) with z not 1. The contrapositive of the spectral lemma says that this generator fixes a flex. The entire cyclic group fixes that same flex. The identity case is immediate. This reasoning genuinely proves a common fixed point for the whole stabilizer; separate elementwise fixed points would not suffice for a general noncyclic group.

The H action on M by left multiplication need not be free. At m=gGamma its isotropy group is L_m = H intersect gGamma g^(-1), conjugate to J_g. Under the fiber identification with Gamma/Gamma_0 = S, that stabilizer acts exactly by J_g. Consequently there is an e in p^(-1)(m) fixed by all of L_m.

This is the place where the candidate differs from a free-circle quotient proof: it allows isotropy which is nontrivial on the full fiber but trivial on one selected sheet. The manuscript does not assert that the coarse quotient of E to M is a covering.

## Sections near complete circle orbits

Every H orbit O_m is a compact embedded circle because its stabilizer is finite. Define s(hm)=he using the fixed e above. If h_1m=h_2m, then h_2^(-1)h_1 lies in L_m and fixes e; hence the formula is well defined. The quotient H/L_m gives its continuity, and p(s(hm))=hm.

Choose an H-invariant Riemannian metric by averaging a metric over H. An invariant tubular neighborhood W of O_m has an H-invariant radial deformation retraction rho onto O_m. For precision, take the homotopy R:W times [0,1] to W with R(x,0)=rho(x) and R(x,1)=x. The map x to s(rho(x)) lifts its time-zero map. Covering homotopy lifting for p:E to M extends this to a continuous lift of R, whose time-one map is a section over all of W. No local constancy of orbit stabilizer type is required. No quotient of the cover is used in this lifting step.

Let q:M to B=H backslash M be the orbit map. It is open: the full preimage of q(V), for V open, is the union of its H translates and hence is open. Since W is saturated, U=q(W) is open and q^(-1)(U)=W. Thus B has an open cover by sets whose complete inverse images admit a section of p. Compactness permits a finite subcover.

## Dimension and refinement into eight section domains

There is a natural homeomorphism B = (H backslash G)/Gamma. The left homogeneous space H backslash G is a compact smooth 7-manifold; right multiplication by Gamma acts smoothly on it and commutes with the left H quotient. Finite-group equivariant triangulation, followed by subdivision as needed to remove inversions, makes the quotient a polyhedron of dimension at most 7. Effectiveness of the finite action is not needed. In particular B is compact, metrizable, paracompact, and of covering dimension at most 7.

Choose a finite open refinement {V_j} of the finite section-neighborhood cover with multiplicity at most 8. Compactness allows this refinement to be finite. Choose i(j) with V_j contained in U_i(j), and a partition of unity {f_j} subordinate to {V_j}. Its barycentric map f:B to the finite nerve N is continuous. Multiplicity at most 8 gives dim N at most 7.

Vertices of the barycentric subdivision sd N are barycenters b_sigma of nonempty simplices sigma of N. Color b_sigma by dim sigma, using colors 0 through 7. The open stars of two distinct vertices with the same color are disjoint: any simplex in sd N is a strict chain of simplices of N and cannot contain distinct simplices of equal dimension. The open stars cover |N|.

For each sigma choose any vertex j(sigma) of sigma. A point in the open star of b_sigma has a strictly positive coefficient at b_sigma, so its original barycentric coordinate at every vertex of sigma is positive. It follows that W_sigma=f^(-1)(star(b_sigma)) is contained in {f_j(sigma)>0}, then in V_j(sigma), then in U_i(j(sigma)). Therefore p has a section on q^(-1)(W_sigma).

For color k take the union Z_k of q^(-1)(W_sigma) over all sigma of dimension k. It is open. Its pieces are pairwise disjoint open subsets, so the corresponding sections glue continuously without compatibility conditions at shared points. There are no shared points; possible boundary contacts lie outside the pieces in question. The eight sets Z_k cover M. Empty colors, if any, may be discarded. This proves g(p) at most 8. Pullback proves g(Y to X) at most 8, and the cited lower bound gives equality. The normalized sectional category is accordingly 7.

The eightfold fiberwise join then has a section, so its first obstruction class vanishes. This consequence follows from the explicit section-domain construction; the review does not endorse a calculation of the large obstruction module or a claim about arbitrary later obstruction choices.

## Why this is not an acceptance of full sheet trivialization

The distinction in the scope statement is necessary, not cosmetic. For C the affine action is (x,y) to (x,y+x). Its permutation on S has cycle lengths 1,1,1,3,3. It fixes selected sheets but does not act as the identity on the fiber. Projectively C is conjugate to diag(1,omega^2,omega^2), so C occurs in a conjugate of H. Choose g realizing that conjugacy. The isotropy of the orbit through gGamma contains this element. A path in H from the identity to that isotropy element projects to a closed loop in that orbit. Lifting the loop to E yields monodromy with the stated nontrivial permutation, up to inversion.

Thus the cover over that complete circle orbit, and over any neighborhood containing it, is not a trivial nine-sheet cover even though it has a section. The full-orbit construction cannot be relabeled as simultaneous trivialization. The final color domains are also not proved connected. This does not establish that the two numerical invariants differ; it establishes that the accepted argument does not compute the stronger one.

The original OWR printed page 114 specifies connected open domains with trivial restrictions. Chen–Wan v2 uses local sections. The author's statement, README, and status preserve that distinction. An appropriate public result description is “ordinary section-based Schwarz genus equals 8; stronger literal connected/full-trivialization formulation not settled by this argument.”

## Source verification and limitations

On 2026-10-06 the exact versioned Chen–Wan PDF and both EMS publisher PDFs were freshly retrieved for this review. Their byte counts and SHA-256 hashes match the author metadata. Relevant primary pages were read, and the explicit matrices, original OWR definition, and Artebani–Dolgachev Proposition 4.1 were also visually inspected in the downloaded PDFs. SOURCE_REVIEW.json records the public URLs, versions, hashes, sizes, and inspection boundaries without copying source material.

The arXiv record identifies Chen–Wan v2 as dated 21 July 2023 and records the later publication in Proceedings of the American Mathematical Society 153 (2025), 2255–2267, DOI 10.1090/proc/17184. The published full text was not retrieved in this review, so no claim of a line-by-line comparison with that version is made. Illman's full text was likewise not retrieved. This review does not claim an exhaustive literature search, independent reproduction of the inherited corpus selection, or priority over other work.

No publication or external message was performed as part of this review. No correction derivative is supplied because no correction to the frozen author's accepted, explicitly limited theorem was required.

## References

Chen, Weiyan, and Zheyan Wan. Topological complexity of finding flex points on cubic plane curves. arXiv:2306.17303v2 (21 July 2023). https://arxiv.org/pdf/2306.17303v2 . Version and publication record: https://arxiv.org/abs/2306.17303v2 .

Artebani, Michela, and Igor Dolgachev. The Hesse pencil of plane cubic curves. L'Enseignement Mathématique 55 (2009), 235–273. https://ems.press/content/serial-article-files/44190 . DOI https://doi.org/10.4171/LEM/55-3-3 .

Denham, Graham, Giovanni Gaiffi, Rita Jiménez Rolland, and Alexander Suciu, organizers. Topology of Arrangements and Representation Stability. Oberwolfach Reports 15 (2018), 43–123, Question 5, printed pages 114–115. https://ems.press/content/serial-article-files/46724 . DOI https://doi.org/10.4171/OWR/2018/2 .

Illman, Sören. Smooth equivariant triangulations of G-manifolds for G a finite group. Mathematische Annalen 233 (1978), 199–220. Publisher metadata: https://link.springer.com/article/10.1007/BF01405351 .
