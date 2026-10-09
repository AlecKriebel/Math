# Independent acceptance audit: the credited degree-12 canonical cover

## Verdict

**ACCEPTED as a complete, credited prior counterexample to the stated bound in OWR-1971-010 / 30000977.** The construction of Christian Gleissner, Roberto Pignatelli and Carlos Rito gives a normal connected projective complex surface with exactly nine canonical A2 singularities, Cartier ample base-point-free canonical bundle, and complete canonical morphism of degree 12 onto a singular quadric cone. Thus the proposed bound 4 is false with the question's actual hypotheses.

The original audited proof is identified by SHA-256 `5914c757c3c8d4790690193964ba1220ede502a6d5a7835527086d424407778c` (14,226 bytes). Its mathematical argument passes. A separate contextual patch clarifies the inverse-eigenline convention and records completed independent review. This is an expository clarification, not a change to the construction or result. No source files or original candidate files were modified.

This verdict does **not** establish the source's classification, an upper bound on all canonical degrees, novelty, or a Galois property of the canonical morphism.

## 1. Exact question and prior attribution

I independently retrieved the original [OWR 26/2008 report](https://ems.press/content/serial-article-files/46169), extracted its text, and visually inspected PDF pages 38 and 40, printed pages 1462 and 1464. The definition uses the **complete** canonical linear system on a surface of general type with canonical singularities and ample base-point-free K. The later question adds a singular minimal-degree target and asks for degree at most four. The nearby classification discussions are explicitly Galois where intended; the question itself does not impose that restriction. Neither regularity nor smoothness of the source is an extra hypothesis.

I independently retrieved and visually inspected Section 6, PDF page 8, of [Gleissner--Pignatelli--Rito, arXiv:1807.11854v2](https://arxiv.org/pdf/1807.11854v2). The exact branch vectors, four canonical divisors, nine A2 points, K squared 24, and degree-12 cone image are already present there. The rank-two group and the incorrect relation involving the third rather than fourth section are genuine typeset inconsistencies. They are repaired by the construction below, not by silently trusting the stated conclusion.

The work is published as *New surfaces with canonical map of high degree*, *Communications in Analysis and Geometry* 30 (2022), no. 8, 1811--1823, [DOI 10.4310/cag.2022.v30.n8.a5](https://doi.org/10.4310/cag.2022.v30.n8.a5). Fresh [Crossref registration](https://api.crossref.org/works/10.4310/cag.2022.v30.n8.a5) and [Rito's publication list](https://www.crito.utad.pt/publications.html) agree on that pagination. [Pignatelli's list](https://pignatelli.maths.unitn.it/papers.html) confirms publication but has different page numbers. The publisher text was not inspected, and no claim is made that its version retains the preprint's typos.

Fresh OWR and GPR downloads are byte-identical to the saved originals:

- OWR: 565,554 bytes; SHA-256 `9ce9e544d53970793f36c5fd486e7f066c85f34c92db9307bc3749ec8f5176b7`.
- GPR v2: 151,250 bytes; SHA-256 `05e088d868a25c9b55911ae3275ff284ec6451212041f7596d2d9431da9d1a19`.

The source PDFs and page images remain separate from the authored acceptance packet. The proof below is independently checked mathematics, not a republication of source prose or code.

## 2. Existence and connectedness of the actual projective surface

Use G = F3 cubed and the Kummer fields in the candidate. Written as rows of radical exponents at 0,1,2, the two matrices are

E: (1,2,1), (1,2,2), (2,0,1),

F: (2,0,1), (1,1,2), (1,2,1).

Their determinants are 4 and -5, both 1 modulo 3. If a product of the three radicands with exponents in {0,1,2} were a cube, its valuations at 0,1,2 would vanish modulo 3. Invertibility forces all exponents to vanish. Kummer theory over C therefore gives connected degree-27 fields, with the stated independent deck actions on their three radicals. Their smooth projective normalizations A and B exist and are integral; over C a normal curve is smooth. The valuation at infinity is minus the sum of finite valuations, so the four inertia generators are exactly the claimed E and F vectors, including infinity.

Every listed inertia group has order three. Locally the remaining unit factors have cube roots in C[[t]], and a nonzero exponent gives the single ramified parameter a with t = a cubed. There is no additional branch point or additional constant-field component. Riemann--Hurwitz gives 2g-2 = 27(-2+4 times 2/3) = 18 on each curve, hence g(A)=g(B)=10.

The product A times B is an integral smooth projective surface. The finite group H = {(g,-g)} acts faithfully. Its projective quotient X exists: a tensor product of translates of an ample bundle provides an H-linearized ample bundle, and the invariant section ring gives the projective finite quotient. Invariant subrings of normal domains are normal, so X is integral and normal. The residual quotient (G times G)/H is G via (g,h) mapping to g+h. Consequently the map psi from X to P1 times P1 is finite of degree 27 and has precisely the desired local monodromies. This is a global construction, not an inference from an unverified classification or a numerical cover datum.

## 3. Stabilizers, singularities, and Cartierness

Normalize each nonzero vector by making its first nonzero coordinate 1. The four inertia lines for A are

(1,1,2), (1,1,0), (1,2,1), (1,2,0),

and those for B are

(1,2,2), (0,1,2), (1,2,1), (0,1,1).

Thus the unique common line among all sixteen crossings is E3/F3. The actual chosen generators there agree, rather than being opposite: e3=f3=(1,2,1). At every other crossing the H-stabilizer is trivial. A nontrivial automorphism of either smooth curve has finitely many fixed points; because every nonidentity H element acts nontrivially on both factors, its fixed locus on the product is finite. There is no divisorial ramification for pi: A times B to X.

At E3/F3 choose a,b with e3 acting as a mapping to zeta a and f3 acting as b mapping to zeta b. The H generator (e3,-e3) has tangent weights (1,2), not (1,1). Therefore the completed quotient ring is

C[[a,b]]^(1,2) = C[[U,V,T]]/(UV-T cubed),

with U=a cubed, V=b cubed and T=ab. Every invariant monomial has a unique form U^i V^j T^k with 0 <= k < 3. This proves both the invariant-ring presentation and its rank-three free module structure over C[[U,V]]. The checker's bounded monomial enumeration only checks this interface; the unrestricted monomial argument proves it.

This is the A2 rational double point. One can also verify canonical discrepancies directly from the toric lattice Z squared plus Z(1,2)/3. Subdivide its first-quadrant cone by (2,1)/3 and (1,2)/3. Consecutive primitive rays are lattice bases, giving a resolution, and both inserted rays lie on x+y=1. Their discrepancies are zero. The hypersurface ring is Gorenstein, so K_X is Cartier. The resolution consists of two (-2)-curves; further exceptional divisors have nonnegative discrepancies. No noncanonical quotient singularity is being admitted.

Each curve has nine points over its third branch point. The 81 pairs have stabilizer order three, H-orbits of size nine, and thus give exactly nine A2 points on X. At each of the other fifteen branch crossings there are three smooth quotient points, each with local degree nine over the base. The latter points introduce no further singularities.

## 4. Ampleness, general type, and intersection numbers

The quotient pi is unramified in codimension one. As K_X is already known to be Cartier, the canonical ramification formula yields pi pullback K_X = K_(A times B). This equality is global: equality on the complement of finitely many points determines the corresponding divisors/line bundles on the smooth product.

The product canonical bundle is the exterior tensor product of two degree-18 ample curve bundles; it is ample. The hypotheses of finite-surjective ampleness descent hold, so K_X is ample. This application is exactly the situation of [Stacks, Tag 0B5V](https://stacks.math.columbia.edu/tag/0B5V). Thus X is of general type, and its minimal resolution has the same canonical ring with X as its canonical model. We do not incorrectly replace ample K_X by the merely nef canonical bundle on that resolution.

The product self-intersection is 2 times 18 times 18 = 648. Dividing by the degree 27 of pi gives K_X squared = 24. Independently, for psi the ramification formula gives the rational numerical pullback class (2/3,2/3); its square times 27 is again 24. Neither argument assumes fractional line bundles exist on P1 times P1.

## 5. Eigensheaves, flatness, and finite duality

For a function character c, let r_i be the least residues c dot e_i and s_j the least residues c dot f_j. The function eigensheaf on a curve is M_c=O(-d(c)), where 3d(c) is the sum of the four residues. The multiplication map M_c cubed to O vanishes to those residue orders. Equivalently the **dual** building-data line L_c=M_c dual satisfies L_c cubed = O(sum residues times branch points). This distinction is the only wording clarification in the contextual patch.

For H, a pair of function characters (c,d) is invariant precisely when c=d. Therefore

psi_* O_X = direct sum over c of O(-d_E(c),-d_F(c)).

This is a global equality of sheaves, not just an equality away from the crossings: pushforward along the product cover splits into exterior tensor products of the curve eigensheaves, and the characteristic-zero invariant projector selects exactly the equal pairs. The resulting direct sum is locally free of rank 27. In particular psi is flat. The same conclusion follows from the CM local rings and the regular base using [miracle flatness, Tag 00R4](https://stacks.math.columbia.edu/tag/00R4). More explicitly, the singular crossing has nine local rank-three free modules, independent crossings have three rank-nine free modules, and the remaining branch/unbranched strata have the expected rank 27 in total.

Finite duality then identifies psi_* omega_X with Hom(psi_* O_X,omega_Y), hence with the direct sum of O(d_E(c)-2,d_F(c)-2). The hypotheses are satisfied: psi is finite flat between equidimensional projective schemes, the base is smooth, and X is CM and Gorenstein. The local dual-module formula is [Stacks, Tag 0BUK](https://stacks.math.columbia.edu/tag/0BUK). Duality reverses the character sign, so c labels the duality summand, whose section transforms by -c. There is no mismatch between function characters and differential characters.

## 6. Independent derivation of all canonical sections from the equations

The following derivation independently verifies the eigensheaf computation, including its signs and completeness. On A let U_c=u1^c1 u2^c2 u3^c3. Write w_i for its finite branch valuations before reduction, and n_i=floor(w_i/3). Then

eta_E,c = product over i=0,1,2 of (t-i)^n_i times dt/U_c.

At a finite branch point its zero order is 3n_i+2-w_i = 2-r_i. Its order at infinity is sum w_i - 3 sum n_i - 4 = 3d_E-r_infinity-4. Every rational differential of this character is q(t) eta_E,c. Regularity away from infinity forces q to be a polynomial: a finite pole would subtract at least three from a branch zero order at most two, or would create a pole at an unbranched point. At infinity a polynomial of degree k subtracts 3k. Hence regular differentials of character -c have basis t^k eta_E,c for 0 <= k <= d_E-2. The same reasoning applies to B.

This shows the dimension is max(d_E-1,0) on A and max(d_F-1,0) on B. Summing over all 27 characters gives ten on each curve, independently matching the genus. On the product, the Kunneth isomorphism gives all global 2-forms as tensor products of curve differentials. H-invariance requires the two duality labels to agree. At an A2 point da wedge db is invariant and is the pullback of one third of the hypersurface dualizing generator dU wedge dT/U. Thus invariant regular product forms descend to regular sections of the invertible omega_X even at the singularities. Conversely every canonical section pulls back to an invariant regular product form. No sections supported only at the singular points and no extra characters are possible.

The independently recomputed 27 pairs (d_E,d_F), in lexicographic order, are:

000:(0,0), 001:(1,2), 002:(1,2), 010:(2,2), 011:(1,1), 012:(2,1), 020:(2,2), 021:(2,1), 022:(1,1).

100:(2,1), 101:(2,2), 102:(2,1), 110:(1,1), 111:(1,1), 112:(1,2), 120:(1,2), 121:(1,1), 122:(1,1).

200:(2,1), 201:(1,2), 202:(1,1), 210:(1,2), 211:(2,1), 212:(1,1), 220:(1,1), 221:(1,1), 222:(2,2).

Only 010,101,020,222 contribute, each once. Thus the **full** canonical system has dimension four, not merely a chosen subsystem of dimension four. The function splitting also gives H1(O_X)=0 by the Kunneth formula: both factors have negative degree for every nontrivial character. This is a consistency check, not an added hypothesis.

For further explicitness the four curve differentials on each side, in that order, can be chosen as

- A side: dt/u2; t dt/(u1 u3); (t-1)(t-2) dt/u2 squared; t squared (t-1) squared (t-2) squared dt/(u1 u2 u3) squared.
- B side: ds/v2; s ds/(v1 v3); (s-2) ds/v2 squared; s squared (s-1) squared (s-2) squared ds/(v1 v2 v3) squared.

Their equal-label tensor products are the four canonical sections on X. These formulas fix the sign convention without appealing to terminology about characters.

## 7. Divisors and every base-point stratum

The zero-order calculation yields, in the ordered supports Ehat1 through Ehat4 followed by Fhat1 through Fhat4, the coefficient vectors

A=(1,0,0,1;1,1,0,0),

B=(2,0,0,0;2,0,0,0),

C=(0,1,1,0;0,0,1,1),

D=(0,0,0,2;0,2,0,0).

The Ehat and Fhat are reduced Weil divisors, and their individual Cartierness is neither asserted nor needed. The four combinations are effective Cartier divisors because they arise as divisors of sections of omega_X. The direct differential construction rules out unlisted divisorial zeros.

For a common zero of B and D, the only possible base locations are E1/F2 and E4/F1. At both, C is nonzero. All other points have B or D nonzero. At E3/F3 the sections A,B,D are locally units times the canonical generator, while C is a unit times T=ab times that generator. Thus all nine singular points are explicitly covered by nonvanishing canonical sections.

The absence of hidden isolated zeros is justified, not assumed: in a normal local integral ring a nonzero section of an invertible sheaf is represented by a regular function. If it is not a unit, a minimal prime over its principal ideal has height one. It therefore lies on the effective divisor's support. There is no isolated zero outside that support. These observations prove base-point-freeness on the entire surface, including codimension two. The exact checker separately enumerates all 25 combinations of the four branch fibers or the unbranched stratum in each ruling.

## 8. The exact quadric and the canonical degree

Coefficient comparison gives 2A=B+D, while 2A is not B+C. The ratio of the corresponding product sections has zero divisor; normality and projectivity make it a nonzero constant. There is an even more concrete check: using the explicit differentials above, eta_A squared/(eta_B eta_D) is exactly 1 on each curve after substitution of the Kummer equations. Thus the product canonical sections can already be normalized to satisfy x0 squared = x1 x3.

The quadratic form has rank three, with unique projective singular point [0:0:1:0]. It is irreducible, nondegenerate as a surface in P3, and of degree 2 = codimension+1. It is therefore an actual singular surface of minimal degree, not a smooth quadric described imprecisely.

Because the complete system is base-point-free, its morphism phi has pullback O(1)=K_X. A positive-dimensional projective fiber would contain a curve on which K_X had degree zero, contradicting ampleness. The morphism is therefore quasi-finite and proper, and hence finite onto its image; see [Stacks, Tag 02LS](https://stacks.math.columbia.edu/tag/02LS). Its image has dimension two, is irreducible, and is contained in the irreducible quadric surface. The image is the whole cone. The intersection projection formula now gives 24 = degree(phi) times 2, so degree(phi)=12.

The degree-27 cover psi constructs X; it is not the canonical morphism phi. In characteristic zero the finite degree is separable, and no unproved Galois assertion enters the argument.

## 9. Executed checks and adversarial tests

The independently authored `independent_exact_checks.py` does not import the original checker. It starts with the six Kummer exponent rows, derives the branch vectors and normalized differentials, checks all 729 character pairs against all 27 group elements (19,683 character evaluations), all sixteen crossing stabilizers, all 27 canonical summands, all eight coefficients of each canonical divisor, all 25 base-point strata, the exact rational differential relation, the quadric rank, and the degree arithmetic. It also tests 625 local invariant-monomial interfaces. Those finite tests supplement the unrestricted geometric proofs above.

The original and independent checkers were both executed in normal Python, -O, and -OO, with bytecode writes disabled. The final recorded suite has:

- 6 successful positive checker executions;
- 15 expected rejections from the original five mutants;
- 36 expected rejections from twelve independent mutants;
- 3 successful actual read-only probe executions, denying 6 writes with EACCES;
- real UID=1000 and effective UID=1000 for every independent checker and permission probe;
- identical original candidate hashes/modes before and after, and unchanged read-only fixtures.

The independent mutants cover a rank-two group claim, dependent Kummer classes, the diagonal rather than anti-diagonal quotient, opposite F inertia generators, a duality sign error, a missing canonical section, an extra canonical section, wrong divisor coefficients, omission of the singular stratum, the printed wrong quadric relation, a smooth-quadric claim, and confusion of construction degree with canonical degree. They are rejected by the relevant mathematical interfaces; Python assertions are not used.

`FULL_CHECK_LOGS.json` contains every stdout/stderr, exit code, expected exit code, optimization mode, full positive output, and input/script hashes. `run_audit_checks.py` accepts explicit candidate, new fixture, and output paths. It copies inputs into 0444 files within a 0555 directory, tests actual append/create denials as the unprivileged user, and captures logs elsewhere. It refuses to reuse an existing fixture. Running a finite checker in a read-only directory is not claimed to formally verify algebraic geometry or provide a general sandbox.

## 10. Acceptance boundary and deliverables

Every target hypothesis is established: complex projective normal integral surface; canonical singularities; Cartier ample base-point-free K; complete canonical system; finite canonical morphism; singular minimal-degree image; degree 12 greater than 4. The audit has no unresolved geometric blocker.

The reviewed `PROOF_AUDIT.md` and `CONTEXTUAL_PATCH.diff` are separate from the unchanged original. The patch makes the inverse-eigenline convention explicit and replaces pending-review language with this acceptance. `SECOND_AUDIT.md` supplies the independent differential, local-ring, and completeness arguments. The packet contains only authored mathematics, authored verification programs/results, and public-source metadata. Credit remains with Gleissner, Pignatelli, and Rito.
