# Independent adversarial audit of PR 1155 / problem 30000214

Sealed UTC: 2026-10-18T01:24:02.127614+00:00
Final mathematical decision: **PASS**. No required mathematical repair found.
This report preserves the complete mathematical core sealed before accessing any candidate audit, validation, acceptance, root notes, or other reviewer report/verdict. It is a supplied-candidate review: PROOF.md was read after the independent target seal. No blind-rediscovery claim is made.

## 1. Original-target sufficiency

The original statement is universal over finite d-dimensional 2-CM complexes over a fixed coefficient field, d>=1. A single d=2 example over Q with no homology 2-sphere subcomplex over Q suffices to refute it. The candidate proves the stronger no-sphere assertion over any field. It does not need to disprove all prescribed positive-characteristic 2-CM variants. No overlap, reordering, minimal-cycle decomposition, or subdivision issue is left once there is not one possible sphere piece.

## 2. Construction and primary import verification

The affine building for PGL_3(F_11((y))) has vertices homothety classes of rank-three lattices. Neighbors of a lattice L are the nonzero proper subspaces of L/yL; a triangle through L is a maximal flag. Its link is precisely the simple bipartite incidence graph of PG(2,11), with 133 vertices in each class, degree 12, and 1596 edges. Connectedness, purity, and local finiteness follow from this lattice description (LSV Section 2, PDF3 and associated text).

LSV's adjoint/conjugation embedding on the ordered basis of its dimension-d^2 algebra is explicitly an embedding into GL_(d^2), not only a projective representation (PDF9). Its kernel on algebra units is the center, already divided out in G'. The specialization d=3 and q=11 is allowed. LSV Definition 4.7 and Proposition 4.8 prove Gamma=Gamma' and simple transitivity; R_0=F_q[1/y] is used as a matrix-entry ring even though A(R_0) is not defined. This distinction is explicitly handled in the source. The candidate likewise reduces the actual GL_9 matrix representation, not an undefined algebra over R_0.

LSV Equation (9), visually checked on PDF13, is constant plus 1/y times a constant, in the fixed F_q-basis. Therefore each generator's adjoint matrix has polynomial t=1/y degree <=1. Corollary 4.6 gives positive products of one or two generators for every undirected neighbor of the base vertex: representatives of adjacent homothety classes have lattice index q or q^2. A path of length r thus writes its endpoint's unique group element as a product of <=2r generators; inverse-generator degree is not silently assumed. Products of polynomial matrices have entry degrees <=sum of degrees, so displacement <=4 implies degree <=8.

Reduction modulo t^9 is a genuine group homomorphism to a finite GL_9 group; all matrix inverses lie in the polynomial ring since the representation is into GL_9(R_0). Its kernel Gamma_9 is finite index and normal. For a kernel element of displacement <=4, rho(gamma)-I has degree <=8 and is entrywise divisible by t^9, hence it is zero. Faithfulness implies gamma=1. Conjugating by the unique element taking the base vertex to an arbitrary vertex uses normality and yields the same displacement lower bound at every vertex. This is a constructive residual argument; residual finiteness is not an unsupported import.

In the orbit complex, a simplex has no repeated orbit vertices because two of its vertices have distance one. More generally no two distinct vertices of a closed star can share an orbit since their distance is <=2. Every image simplex through an orbit representative lifts through the chosen actual vertex by translating a lift. This provides both surjectivity and injectivity of the vertex-link map, including its edges: a triangle lift through the vertex has its other endpoints uniquely determined by their orbit labels. Therefore no false quotient edge or link edge is created. The orbit-defined complex is finite (finite index plus vertex transitivity), pure two-dimensional, and connected. The proof never needs a type-preserving action, a separately proved torsion-free property, a clique completion, or contractibility. A face inversion would violate the displacement bound. LSV's conditional Ramanujan/Jacquet-Langlands theorem in Section 6 is not a dependency.

## 3. Spectral normalization and deletion

For the 133x133 real incidence matrix M, the exact identity MM^T=11I+J gives singular values 12 and sqrt(11), hence the adjacency eigenvalues of G are +/-12 and +/-sqrt(11). With unoriented energy E(f)=sum_edges(f(u)-f(v))^2, the combinatorial Laplacian gap on counting-mean-zero functions is 12-sqrt(11), and the normalized gap is 1-sqrt(11)/12.

For H=G-w, subtract the counting mean of f on H and extend the centered function x by zero at w. It is counting-mean-zero on G. Removing the w-incident edge energy subtracts precisely sum_(u~w)x_u^2, bounded by sum_H x_u^2, and gives E_H(x)>=(11-sqrt(11))||x||_2^2. The weighted variance satisfies min_c sum_H d_H(u)(x_u-c)^2 <= sum_H d_H(u)x_u^2 <=12||x||_2^2. Thus the candidate's normalized lower bound (11-sqrt(11))/12 is correct even though H is not regular. It exceeds 7/12 and 1/2. The positive counting gap also proves H connected. There is no substitution of counting-mean-zero for weighted-mean-zero in the actual link-cocycle application.

Independent stronger check: delete a point w, let C be the 132x12 incidence submatrix on remaining points and lines through w. Then C1=1, C^TC=11I; C C^T is a block matrix of twelve J_11 blocks. The normalized incidence matrix B of H obeys BB^T=(11I+J)/144 + CC^T/1584. Its eigenvalues are 1 (once), 1/12 (eleven times), 11/144 (120 times). One line-side null vector contributes one zero adjacency eigenvalue. Therefore lambda(H)=1-1/sqrt(12), about .7113248654, for point or line deletion by duality. This corroborates but is not needed for the weaker proved bound .6402812675.

## 4. Weighted cocycle mechanism

Let m(e) be surviving triangle multiplicity. Purity guarantees m(e)>0, so sum_e m(e)a_e^2 is a positive norm. The affine set of cocycles representing one class is a translate of the finite-dimensional closed subspace of coboundaries and has a unique norm-minimizer modulo that subspace. Orthogonality to the coboundary of each vertex indicator is exactly sum_u m(vu)a_vu=0 (the sign is immaterial to zero). On lk(v), the degree of neighbor u is m(vu), so the link function f_v(u)=a_vu has the required degree-weighted mean zero. On every triangle the cocycle equation gives f_v(u)-f_v(w)=-a_uw. The Poincare inequality at each v is therefore exactly the candidate's inequality.

The sum of its left sides is sum_e m(e)a_e^2 because an edge is opposite exactly one vertex in each triangle containing it. The sum of its right weighted norms is twice that same quantity because each edge has two endpoints. Thus E>=2lambda E. Strict lambda>1/2 forces E=0, and hence the class vanishes. There is no lost orientation factor, no missing factor 1/2, no regularity assumption, and no global connectedness assumption hidden in this H^1 lemma.

Independent sharp-boundary test: the periodic 4x4 triangulated torus has all links C6 with normalized gap 1/2 and a nonzero degree-weighted coclosed cocycle. Exact energy is 64, summed link energy 64, and summed link weighted norm 128. Boundary ranks modulo 1009 and 1013 are (15,31), giving beta_1=2 in each. Thus equality lambda=1/2 really fails to force vanishing, and the strict margin used here matters. The test verifies the normalization mechanism instead of merely recomputing the candidate's inequality.

## 5. Every CM and deletion condition

Each edge of K lies in 12 triangles from the degree of the corresponding link vertex. A surviving edge after deleting z loses at most the one triangle with third vertex z, and thus still lies in >=11 triangles. A surviving vertex originally had 266 distinct neighbors and loses at most one, so still has an edge; every face is consequently in a triangle, and deletion preserves pure dimension two. The complex has at least 267 vertices; no empty/singleton deletion pathology occurs.

Deleting z preserves connectedness: take a simple graph path joining surviving endpoints, and replace any a-z-b portion by a path inside the connected graph lk_K(z). That path's vertices are all surviving neighbors of z and its edges are actual K edges. The links of surviving vertices are G or G-z, exactly, because induced deletion commutes with taking links and removes only the vertex z when it belongs to the link. Their positive degree and >1/2 spectral gaps have already been checked. Apply the weighted lemma separately to K and every induced deletion, with freshly defined triangle weights; the argument does not retain obsolete weights.

Finite-dimensional cohomology-homology duality over R gives H_1(-;R)=0. Integer boundary matrices have identical ranks over Q and R, so H_1(-;Q)=0. The same ranks persist in any characteristic-zero field; no assertion is made that they persist in characteristic 11 (the residue-field parameter q) or arbitrary positive characteristic.

Reisner's criterion for pure dimension two asks: empty face, reduced H_0 and H_1 vanish; vertex faces, reduced H_0 of their dimension-one links vanish; edge faces, reduced H_-1 of their dimension-zero links vanish; facet faces, no lower-degree vanishing below -1. Nonemptiness supplies all further negative-degree conditions. Connectedness and first-homology vanishing supply the global conditions, vertex links are connected, edge links have at least 11 or 12 vertices, and facet links consist of the empty face. Thus K and every deletion are CM over Q with unchanged dimension: K is 2-CM.

As a consistency check, if N=f_0(K), local incidence counts force f(K)=(N,133N,532N), chi(K)=400N. H_1=0 is consistent with beta_2=400N-1. Deleting one vertex removes (1,266,1596), changing chi by -1331. The link cycle rank is 1596-266+1=1331, consistent with this loss of top homology and the deletion proof. There is no Euler or dimension obstruction to the constructed CM complex.

## 6. No sphere over any field

Let S be any finite two-dimensional subcomplex satisfying the full k-homology sphere face-link definition. For each edge, its zero-dimensional link has reduced H_0 dimension one and so has exactly two vertices. Thus every edge belongs to two triangles, irrespective of characteristic. Every vertex-link graph is connected (its reduced H_0 is zero), and each of its vertices has degree two by the same edge condition. It is a finite connected simple 2-regular graph, hence a simple cycle. It is a subgraph of G, whose bipartiteness and unique line through two points forbid cycles below length six. Thus every vertex in S has at least six neighbors, 2f_1>=6f_0, and 3f_2=2f_1. Consequently chi(S)=f_0-f_1/3<=0. The global sphere homology over any field instead gives chi=2. Euler characteristic equals alternating Betti sum over every field. No orientability, surface classification, or characteristic assumption is needed. The contradiction excludes every possible allowed piece and hence excludes the original cover.

## 7. Diagnostics, limitations, and final independent conclusion

The independent script builds PG(2,11) from projective triples and dual covectors, verifies MM^T=11I+J in exact integer arithmetic, checks all 266 vertex deletions connected using graph search, constructs a 6-cycle, and numerically checks G and both dual deletion spectra. It also performs the strict-threshold torus test above. Floating eigenvalues corroborate analytic exact arguments and do not carry the proof. The enormous finite global quotient is defined and verified mathematically, not enumerated by this script. No numerical result is presented as a proof of its global homology.

No central unsupported claim, target mismatch, invalid external hypothesis, coefficient gap, missing face-link condition, or invalid deletion inference was found. The strongest verified result is the complete stated counterexample, conditional only on the standard unconditional LSV building/lattice inputs actually verified in the cited primary paper. Novelty, priority, and exhaustive literature status are outside this mathematical correctness verdict.

## Evidence pins at seal time

- `draft_pr_actual_claims_1100_1200_20261017/audits/pr1155_30000214/inputs/PROOF.md` SHA-256 `87a377daac3eb3c7399debeae7fdbcbb45e00999fe2fcbefd7ce3b103b0d3160`
- `draft_pr_actual_claims_1100_1200_20261017/audits/pr1155_30000214/families/spectral_cm_01/TARGET_SEAL.md` SHA-256 `981a36287036035d0e9e16d59b10a54f264f4d20847094a0355b12d7ab873cff`
- `draft_pr_actual_claims_1100_1200_20261017/audits/pr1155_30000214/families/spectral_cm_01/private/independent_diagnostics.py` SHA-256 `acb722968bb711f01f6693700106384a5fd4d51c4019dae4d4d13725aac03f3d`
- `draft_pr_actual_claims_1100_1200_20261017/audits/pr1155_30000214/families/spectral_cm_01/private/diagnostic_results.json` SHA-256 `6f2af796a42db6f7cf3b6087ea5dd59de60c4a0a3242cc7ad1c7379a9b252950`
- `draft_pr_actual_claims_1100_1200_20261017/audits/pr1155_30000214/private/sources/nevo_owr2005.pdf` SHA-256 `f0200fe70e287441d0fd3dbb0b6b564f4ed5bbdc04eb7513612ad0edf7fa95dc`
- `draft_pr_actual_claims_1100_1200_20261017/audits/pr1155_30000214/private/sources/nevo_owr2005.txt` SHA-256 `2a584d6880aafeb228c01b53ff67461ab71585bd748e448a181df214ec4566ad`
- `draft_pr_actual_claims_1100_1200_20261017/audits/pr1155_30000214/private/sources/nevo_0505334v2.pdf` SHA-256 `767106ae250aeb094bb80234e298ceec3d5534ff3ad74b1e049b1ee7cd734f36`
- `draft_pr_actual_claims_1100_1200_20261017/audits/pr1155_30000214/private/sources/nevo_0505334v2.txt` SHA-256 `7ae201768389fd25374fb4e436747f5132141424b357c5e5877a4b063607368b`
- `draft_pr_actual_claims_1100_1200_20261017/audits/pr1155_30000214/private/sources/lsv_0406217v2.pdf` SHA-256 `599cb3ccebdfda4d0b6ab25d0fba4e9f72575833c226bba5337ab5209ae6324b`
- `draft_pr_actual_claims_1100_1200_20261017/audits/pr1155_30000214/private/sources/lsv_0406217v2.txt` SHA-256 `47dcaa4de0576e48f7d27bbe0a064817aac6dc896e4fd54d3b4477e12391dc2a`

Exposure boundary: no inputs/*AUDIT*, VALIDATION*, ACCEPTANCE*, root notes, other family/review report or verdict bodies have been read. No other reviewer will be read before final decision. Third-party sources/extracts/renders and temporary diagnostics are private. Only the assigning parent receives updates.


## Final provenance and verdict boundary

The primary source material was reused from the assigning parent's freshly authenticated source directory; I independently read and checked the mathematical statements and their relevant proofs. I did not independently perform another network download. The retrieved candidate is pinned to PR head `7bc343bc88e5211e06841e375e97015fa8e5d155`. Its PROOF.md is SHA-256 `87a377daac3eb3c7399debeae7fdbcbb45e00999fe2fcbefd7ce3b103b0d3160`. After the mathematical seal, the only additional candidate-related semantic reads were MANIFEST.json and the parent's RETRIEVAL_RECEIPT.json for provenance. The LSV PDF3 building-page image and the seal result were exposed in the same tool return; I conservatively record that image as post-seal visual exposure, while its building text had already been checked before sealing. All thirteen input files were byte-hashed and matched both the receipt and manifest, except that the manifest correctly excludes its own entry from its self-hash list. Hashing other input bytes did not expose their bodies to the reviewer. No supplied audit, validation, acceptance, other-family report, or other-reviewer verdict body was semantically read at any stage.

The target seal SHA-256 is `981a36287036035d0e9e16d59b10a54f264f4d20847094a0355b12d7ab873cff`; the mathematical seal SHA-256 is `2e9d3cf0a78d39bd732485f982eab0e2edccbcc5818791fb3163961a38cfe8d7`. The final decision is scoped to this candidate proof and its original-target applicability. It verifies a finite Q-2-CM complex with no homology 2-sphere subcomplex over any field. The exact remaining mathematical gap in this proof is **none identified**. No required operative repair is requested. The independent stronger deleted-link spectrum may be retained as a useful corroboration; the candidate's existing lower bound already suffices.

The finite global quotient was not enumerated. This is a limitation of the computational corroboration, not a missing existence step: the degree/divisibility and star arguments prove the stated construction directly. Global higher homology beyond what is needed for CM was not independently enumerated. Priority and exhaustive novelty remain outside this audit. No Git, GitHub, Zenodo, GWS, or outreach mutation was performed; all writes are in this reviewer directory.

Final report UTC: 2026-10-18T01:25:27.642344+00:00. Completion estimate: 100% of this assigned independent mathematical audit.


## Supplementary adversarial characteristic boundary check

This deduction was made after the complete core was sealed, using only the already inspected LSV definitions and color map; it does not alter the PASS verdict. The construction's restriction to characteristic zero is substantive. In fact the particular t^9 quotient has nonzero first cohomology over F_3.

By LSV Definition 4.7, the reduction of Gamma modulo t lies in the block upper unitriangular subgroup with three identity blocks of size three. That is an 11-group (there are 27 free entries). The kernel of reduction GL_9(F_11[t]/t^9) to GL_9(F_11) is also an 11-group: its filtration by 1+t^j Mat_9 has additive F_11-vector-space quotients. Thus Gamma/Gamma_9 is a finite 11-group and its order is coprime to three. The building color map delta:Gamma->Z/3 is surjective, as LSV's Figure 3 and Corollary 4.10 state. Therefore delta(Gamma_9)=Z/3: if it were zero, delta would factor through an 11-group, which has no quotient of order three.

Assign to an oriented quotient edge the difference in Z/3 between the building colors of its endpoints. This is well defined: translating an edge lift adds the same delta(h) to both endpoint colors, and uniqueness of lifts through an initial vertex follows from the proved star injectivity. The sum around every triangle is zero, so this is a simplicial F_3 1-cocycle. Choose h in Gamma_9 with delta(h) nonzero and a building path from o to ho. It projects to a closed path in K on which the cocycle sums to delta(h), hence is nonzero. No coboundary has nonzero sum around a closed path. Consequently H^1(K;F_3) is nonzero, and K is not CM over F_3.

This boundary check uses no building contractibility theorem or group-cohomology identification. It reinforces that the candidate correctly claims Q-2-CM (and all characteristic zero) rather than an all-fields 2-CM example; the no-homology-sphere assertion still holds over every field independently of this failure.
