# Independent full mathematical review of PR1155 / problem 30000214

Reviewer family: `finite_quotient_01`. The mechanism focus is the finite congruence quotient and its unchanged simplicial links; this report also checks the complete spectral, Cohen–Macaulay, deletion, and sphere-obstruction argument. The original target was sealed before candidate access. No other new reviewer report was read. The mathematical assessment below was completed and sealed before access to old audit, validation, acceptance, or reviewer verdict bodies.

**Mathematical decision: PASS.** The pinned `inputs/PROOF.md` gives a valid existential negative answer over the fixed coefficient field Q to Nevo's original homology-sphere decomposition question. The complex is finite, abstract simplicial, pure of dimension two, and 2-CM over Q; it contains no two-dimensional homology sphere subcomplex over any field. No mathematical repair is required. This decision uses the unconditional lattice construction in LSV, not a Ramanujan or automorphic theorem. It does not certify historical priority, a publication package, or enumerate the enormous finite quotient.

## 1. Original claim and the strength of the counterexample

I read the primary Oberwolfach contribution, PDF pages 36–37 (printed pages 960–961), including Definition 1, Theorem 7 and Problem 8, and visually inspected those two pages before reading the candidate. I also read Nevo's preprint Definition 3.1, Theorem 3.4 and Problem 3.7. The field k is fixed in the definition of 2-CM: K is CM over k and each induced vertex deletion is CM over k of the same dimension. The theorem covers K by minimal d-cycle complexes with successive intersections containing a d-face and with the stated ability to begin at any prescribed piece. The question asks whether those pieces can be homology spheres.

Here a d-dimensional homology k-sphere has the sphere homology in every face link, including the empty face; the local-link requirement matters. A complex having only the global homology of a sphere would be a different, weaker condition. A single finite 2-CM complex over Q with no allowed sphere piece is sufficient to disprove the universal statement. There is no need to produce examples over every field, and no need to analyze overlap order once every possible piece is absent. The candidate establishes this stronger absence over every field for the same K. It makes no unsupported positive-characteristic 2-CM claim.

## 2. Precise unconditional LSV input and its hypotheses

The source is the authenticated local primary manuscript `lsv_0406217v2.pdf` / `.txt`. I read Section 2, the algebra definitions in Section 3, its conjugation embedding and Propositions 3.1–3.5 as needed to inspect the proof of Proposition 4.8, and Section 4 through Proposition 4.9. I visually inspected PDF page 13 to resolve Equation (9) and its indices. No source from LSV Section 6 or later is necessary for this construction.

Specialize LSV's prime-power q and integer d to q=11, d=3. Let F=F_11((y)), O=F_11[[y]], k=F_11(y), t=1/y, R=F_11[y,1/y,1/(1+y)], R_T=F_11[y,1/(1+y)] and R_0=F_11[t]. Let E=F_(11^3), let phi generate Gal(E/F_11), and form the cyclic algebra A(k), with coefficient field E(y), relations z alpha = phi(alpha) z and z^3=1+y. Its dimension over k is nine, and its center is k. The local splitting at F gives A(F)=M_3(F). Conjugation on A(k) embeds A(k)^*/k^* into GL_9(k): an element in its kernel commutes with the entire algebra and is central, hence trivial in the projective quotient. This is a faithful representation of the same group that acts on the building, not a representation with an unexamined central kernel.

For b=1-z^(-1), b_u=u b u^(-1), with u ranging over E^*/F_11^*, LSV Definition 4.4 defines Gamma by the projective classes of those generators. Proposition 4.8 states, without an automorphic conditional hypothesis, that Gamma acts simply transitively on the vertices of the building of PGL_3(F). I inspected its proof: index-q neighbors are the b_u images (Propositions 4.1–4.3), and induction along index-q sublattices gives transitivity (Proposition 4.5 and Corollary 4.6). The stabilizer calculation uses Gamma within the subgroup Gamma' of polynomial conjugation matrices that reduce to upper triangular matrices with identity diagonal blocks at t=0. The intersection of G'(R) with the vertex stabilizer is G'(R_T), whose elements are projective classes alpha z^j by Proposition 3.5. Its intersection with Gamma' is central: the z diagonal block forces alpha in F_11, and the coefficient-field diagonal block forces j=0 mod 3. Thus the vertex stabilizer in Gamma is trivial. This verifies the stated import's mechanism and excludes reliance on the later Ramanujan spectrum.

Equation (9) shows that every conjugation matrix b_u is affine in t, in the nine-dimensional basis alpha_i z^j. All coefficients other than the displayed 1/y are in E, and z^j has 0<=j<3, so there is no implicit further power of y in those coordinates. LSV's Gamma=Gamma' places the whole group, including inverses, in GL_9(R_0). R_0 need not support the cyclic algebra A(R_0); reduction is performed on the faithful polynomial matrix representation, which is fully defined.

The building is the abstract flag complex of lattice homothety classes. A neighbor of [L_0] is uniquely represented by yL_0 < L < L_0, and L/yL_0 is a one- or two-dimensional proper nonzero subspace of F_11^3. Therefore the neighbor index [L_0:L] is 11 or 11^2. Corollary 4.6 gives a representative word in respectively one or two b_u's. Simple transitivity identifies that word with the unique group element taking o to this neighbor. This covers **both adjacency types**, including the inverse direction of an edge. Their polynomial matrices have degree at most two. It would be erroneous to count every graph edge as a single degree-one generator; the candidate does not make that error.

## 3. Finite congruence quotient, displacement, and every local face type

Reduce matrices modulo (t^9). Since Gamma is contained in GL_9(F_11[t]), this is a group homomorphism to GL_9(F_11[t]/(t^9)). The target is finite; no irreducibility of t^9 or splitting theorem over the quotient ring is needed. Let N be its kernel. It is a finite-index normal subgroup of Gamma.

If a graph path of length r<=4 joins o to gamma o, successively translate each edge back to o. Its steps are the neighbor elements described above. Their product has degree at most 2r<=8 and takes o to gamma o. Simple transitivity makes it equal to gamma. For gamma in N, all entries of rho(gamma)-I are divisible by t^9. A polynomial of degree at most eight divisible by t^9 is zero. Thus rho(gamma)=I, and faithfulness implies gamma=1. Normality transports this statement to every vertex: for x=g o and h in N, g^(-1)h g belongs to N, so every nonidentity h has dist(x,hx)>4.

This argument does not assume that N preserves building colors, does not equate vertex freeness with local injectivity, and does not invoke a torsion-free quotient theorem. It directly proves the displacement required for the orbit construction. In particular no nonidentity element can stabilize a simplex while permuting its vertices, because then a vertex would move graph distance at most one.

Define K's vertices to be N-orbits of vertices, and its faces to be vertex images of building faces. Finite index and Gamma's vertex transitivity give finitely many vertices (in fact their set is the finite image Gamma/N). There are consequently finitely many abstract faces. A building simplex has distinct orbit vertices: any pair in it is adjacent and cannot be identified. Images of subsets are faces, so this is an abstract simplicial complex. No face can have more than three vertices. Every face is the image of a building face, extends to the image of a triangle, and that triangle retains three distinct vertices. Hence K is pure of dimension exactly two. Connectivity descends from the connected lattice graph.

Fix a lift x of a quotient vertex v. All vertices in its closed star are pairwise at graph distance at most two, so no two can lie in the same N-orbit. An edge incident to v has a lift; translating the lift's endpoint in orbit v to x gives an edge at x. The other endpoint is the unique neighbor of x in its orbit. A quotient triangle incident to v likewise has a lift that can be translated to a triangle through x; both other vertices are then uniquely determined. Conversely every edge or triangle at x has its prescribed image. These two directions prove an isomorphism of the abstract links, with their vertices and edges, rather than only a graph covering or a surjection.

This addresses loops, parallel local edges, collapsed triangles, identification of different incident triangles, and possible extra link edges. No extra clique faces are adjoined: the quotient is defined from images of building faces. An arbitrary orbit of a distant edge or triangle cannot create a new local face, because the preceding normalization and uniqueness force it to be the image of the unique local lift. The same reasoning covers both color classes and every vertex. It follows that each vertex link is exactly the point–line incidence graph G of PG(2,11). Each edge has exactly 12 triangles; the 12 third vertices remain distinct in the quotient. The displacement bound four is more than sufficient for this argument and is harmless.

## 4. Independent exact local arithmetic checks

The authored `diagnostics.py` provides an independent finite computation, without copying candidate code or old audit calculations. It uses the rootless cubic X^3+X+4 over F_11 to construct E=F_(11^3); rootlessness is an exact irreducibility check for a cubic. It constructs 133 representatives of E^*/F_11^* and works in the basis {1,X,X^2}z^j. Changing the coefficient-field basis from LSV's normal basis is a constant basis change and cannot alter polynomial degree.

For u=1, direct multiplication of

    (1-z^(-1)) (alpha z^k) (1+t(1+z+z^2))

using z^3=1+1/t gives

    alpha z^k + (alpha-phi^(-1)(alpha))
      [sum_(i<k) z^i + t sum_(i<3) z^i].

This supplies the degree-one matrix B(t)=B_0+tB_1 without relying on a transcribed form of Equation (9). Conjugation by u is a constant block-diagonal matrix C_u, with blocks multiplication by u/phi^k(u), so all generators are C_u B C_u^(-1). The script constructs the inverse polynomial of degree two and checks both matrix products with B are exactly I coefficient by coefficient modulo 11. It then verifies 133 generators and 133 inverses are all distinct, and checks every ordered pair among these 266 neighbors by testing whether s_i^(-1)s_j equals a neighbor matrix. These are exact polynomial identities of degree at most four. Equality after reduction modulo t^9 is therefore the same equality in every one of these tests.

The arithmetic link has 266 vertices, 1596 edges, degree 12 everywhere, no same-color edges, and its 133-by-133 incidence block N satisfies N N^T=11I+J exactly. A separate projective-coordinate enumeration of PG(2,11), using dot products over F_11 and no extension-field representation, produces the same degree and Gram identities. The script also checks the two local energy counting factors in Section 6 below on an explicit finite triangulation with integer coboundary values.

These calculations are informative checks of both neighbor directions, the degree bounds, and the link arithmetic. They are **not** an enumeration of Gamma/N or a direct computation of H_1(K). The proof of the finite quotient and global homology remains the symbolic argument and the verified LSV lattice theorem. Numerical eigenvalues in `DIAGNOSTICS.json` are diagnostics only; the inequalities used in the proof follow from exact identities.

## 5. Spectral inequalities, including the irregular deleted graph

There are n=11^2+11+1=133 points and n lines. Each point is on 12 lines. Distinct points have exactly one common line, so the square incidence matrix M satisfies M M^T=11I+J. Its singular values are 12 once and sqrt(11) with multiplicity 132. The bipartite adjacency matrix therefore has eigenvalues +12, -12, +sqrt(11), -sqrt(11), with the stated multiplicities. In particular the ordinary Laplacian has smallest positive eigenvalue 12-sqrt(11)>0, and for unweighted-mean-zero f,

    E_G(f) >= (12-sqrt(11)) sum f^2.

Bipartiteness forbids odd cycles; two points having only one common line forbids 4-cycles. Thus every simple cycle has length at least six.

For H=G-w, take any function x of zero unweighted mean on H, and extend it by zero at w. The extension has zero mean on G. Removing w subtracts sum_(a~w) x(a)^2 from the energy, which is at most sum_H x(a)^2. Thus

    E_H(x) >= (11-sqrt(11)) sum_H x^2.

This strictly positive bound proves H is connected. Its degrees are 11 or 12, not a common degree. For any nonconstant f, let x=f minus its unweighted mean. The weighted variance V_H(f)=min_c sum_a deg_H(a)(f(a)-c)^2 is at most 12 sum_H x^2. Hence E_H(f)/V_H(f)>=(11-sqrt(11))/12>7/12>1/2. For G the exact normalized gap is (12-sqrt(11))/12>1/2. The distinction between unweighted centering for the auxiliary bound and weighted centering for the normalized Laplacian is correct and essential. There is no unjustified regularity assumption after deletion.

The exact lower bounds are approximately 0.7236146 for G and 0.6402813 for H. Direct numerical calculations for deleting a point or a line give about 0.7113249 for the latter's actual normalized gap, consistent with the conservative bound. The strict inequality needed by the proof is established exactly via sqrt(11)<4. Nothing relies on floating-point rounding.

## 6. Weighted cocycle vanishing, with all normalization factors

For any finite pure two-dimensional X, give an edge e weight m(e), its number of triangles. All weights are positive. In each real 1-cohomology class choose the representative a minimizing sum_e m(e)a_e^2. The affine space of representatives is a translate of the finite-dimensional linear coboundary space, hence is closed and admits this orthogonal projection. Varying a by the coboundary of each vertex indicator yields

    sum_(u~v) m(vu) a_vu = 0

at every vertex v. On lk_X(v), f_v(u)=a_vu has weighted mean zero since its local degree is exactly m(vu). For each triangle vuw, the cocycle equation gives f_v(u)-f_v(w)=-a_uw, whose square is a_uw^2. The link Poincare inequality gives local energy at least lambda_v times sum_u m(vu)a_vu^2.

Let lambda be the minimum of the finitely many link gaps. Summing all local energies counts edge uw once for each triangle through it, so it is precisely E(a). Summing the local weighted norms counts each unoriented edge at its two endpoints, so it is 2E(a). Thus E(a)>=2 lambda E(a). If all gaps exceed 1/2 then E(a)=0, a=0, and H^1(X;R)=0. The factor two is verified; no global expansion hypothesis, orientability assumption, or unweighted-edge normalization has been imported. The formula uses each X's own surviving triangle counts and is valid after vertex deletion.

By finite-dimensional linear algebra H^1=0 implies H_1=0 over R. Integer simplicial boundary matrices have the same ranks over Q and R, so H_1(X;Q)=0. The same rank argument applies to any characteristic-zero field. It gives no conclusion for every positive characteristic, and the candidate does not assert one.

## 7. All CM and deletion requirements

For K, purity and dimension are established above; it is connected, every vertex link is G, and every edge link is a nonempty zero-dimensional complex of 12 vertices. The cocycle lemma applies and gives H_1(K;Q)=0.

Fix an arbitrary vertex z and let X=K-z be the induced deletion. Each surviving edge belonged to 12 triangles of K; at most one of those triangles contains z, because K is abstract simplicial. Hence it still has at least 11 triangles. Every vertex has 266 neighbors in K and retains at least 265. Thus X has no isolated vertices and every edge or vertex lies in a triangle; it remains pure of dimension two.

To connect two surviving vertices, start with a K graph path. Each subpath a-z-b can be replaced by a path in the connected graph lk_K(z), whose vertices all survive. Erasing repetitions gives a path in X. Thus X is connected. For a surviving u, its link is G if uz is not an edge, and G with the single link vertex z deleted otherwise. These links are connected and have normalized gap strictly exceeding 1/2 by Section 5. The cocycle lemma therefore yields H_1(X;Q)=0. Edge links remain nonempty with at least 11 vertices; facet links are {empty face}.

Reisner's criterion in pure dimension two now holds over Q face by face: the empty face requires reduced H_0=0 and H_1=0 (as well as nonemptiness); a vertex requires nonempty connected link; an edge requires nonempty link; a facet has no required homology vanishing in degrees below -1. K and every X satisfy these conditions and have the same dimension. This proves exactly that K is 2-CM over Q. The argument treats the induced deletion, not a topological puncture or deletion of an entire closed star.

## 8. Sphere obstruction and quantifiers

Let S be any two-dimensional homology sphere subcomplex over a field k. For each edge e, lk_S(e) has the reduced homology of S^0; a zero-dimensional complex with that homology has exactly two vertices. Thus e belongs to exactly two S triangles. Each vertex link is consequently a finite simple graph with every vertex of degree two. Its required sphere-link homology includes connectedness, so it is a single simple cycle. This is a subgraph of G, and has length at least six. S need not be induced, and no induced-subgraph claim is used.

Writing f_i for the face numbers, the cycle bound gives 2f_1>=6f_0, and double counting triangle-edge incidences gives 3f_2=2f_1. Therefore

    chi(S)=f_0-f_1+f_2=f_0-f_1/3<=0.

The global homology of a two-dimensional k-homology sphere gives Betti numbers (1,0,1), hence chi(S)=2 over any field, a contradiction. This does not first identify a rational homology sphere with a topological sphere; it derives just the incidence conditions needed from the local links. No orientability or characteristic restriction is hidden in the Euler calculation. Thus no eligible sphere piece exists over Q or any other field, and even an unordered cover is impossible.

## 9. Adversarial boundary checks and exact remaining limits

I explicitly considered loss of faithfulness through projectivization; use of a ring without inverses; both index-11 and index-11^2 neighbor classes; path orientations; stabilizers that permute a simplex's vertices; non-color-preserving congruence actions; collapse or merging of quotient triangles; new local edges from distant lifts; confusing orbit faces with a newly formed clique complex; failure of purity or dimension after deletion; unequal deleted-link degrees; the weighted/unweighted variance inequality direction; the global factor of two in the cocycle proof; change of coefficient field; disconnected vertex links in a purported sphere; and noninduced sphere subcomplexes. The preceding derivations resolve these tests without strengthening an unsupported claim.

The strict gap requirement is real: equality 1/2 would not force E=0. The chosen q=11 gives a comfortable exact strict inequality. The truncated ring F_11[t]/(t^9) has zero divisors, but a matrix group homomorphism exists over it because the unreduced matrices are invertible; an ideal need not be prime. The displacement proof uses faithful equality over F_11[t], not an unjustified lifting of invertibility from a finite ring.

The strongest verified result is the entire mathematical statement in the candidate, conditional only on the explicitly checked, unconditional LSV theorem as a standard primary-source import. No central mathematical gap remains. The computation checks the local arithmetic exactly and the global argument symbolically; it does not supply a full quotient face list or a directly computed homology certificate for that quotient. Such an enumeration is not required for this existence proof. Historical novelty and the integrity of any future public package require separate review and are outside this mathematical decision.

## 10. Post-seal old-record consistency and authentication disclosure

Only after `MATHEMATICAL_SEAL` was saved, I read the original `inputs/MANIFEST.json`, the root retrieval receipt, and the old `MATHEMATICAL_AUDIT.md`, `VALIDATION.md`, `VALIDATION_REPORT.md`, `ACCEPTANCE.md`, and `SOURCE_AUDIT.md`. Their mathematical conclusions agree with the independently sealed analysis. Their additional sharper deleted-gap calculation and adverse-control claims are not represented as this review's independent preseal work. The same small irreducible cubic arose by my script's own ordered search; this was written and run before those old diagnostic descriptions were opened.

An independent hash authentication now verifies all 13 operative input files against the root retrieval receipt's byte counts, SHA-256 values and Git blob SHA-1 identities; all 12 nonself entries of the original manifest match, and its inventory is exact. The proof is 12,704 bytes with SHA-256 `87a377daac3eb3c7399debeae7fdbcbb45e00999fe2fcbefd7ce3b103b0d3160`, pinned to PR head `7bc343bc88e5211e06841e375e97015fa8e5d155` by that receipt. `private/INPUT_AUTHENTICATION.json` records the checks. I made no operative-input changes and no Git, GitHub, Zenodo or GWS mutations. I did not read root or new family/reviewer verdict bodies.
