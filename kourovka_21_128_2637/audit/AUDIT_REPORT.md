# Independent audit of the F4 and H4 commensurability dossier

Audit date: 3 October 2026 UTC.

## Verdict

**PASS as a five-attempt, explicitly unresolved partial-results dossier. HOLD any claim to have resolved KOU-21.128.** No false mathematical conclusion was found in the frozen release. The computations and their limitations withstand independent reconstruction. The central-quotient reduction, necessary index ratios, torsion-free kernels, three first-homology calculations, elementary finite-quotient separation, virtual free quotients, L2 calculation and conditional commensurator obstruction are valid at the stated scope.

The remaining gap is substantive: no argument treats arbitrary finite-index subgroups on both sides. Rejecting one subgroup of relative index five, distinguishing full finite quotients, or classifying torsion in the ambient central quotient does not fill that gap.

No source, release file, remote service or external record was changed. This audit does not constitute a sixth proof attempt, a novelty assertion, or an independent reconstruction of every theorem in the cited literature.

## Frozen input and independent controls

The audit used the original 24-file author release preserved in this package and its frozen author manifest. Every file size and SHA256 matched, with exactly 24 files and 49,705 bytes. The SHA256 of `MANIFEST.json` is:

`7e2b93458975bfafb1141847cfd878cd4be801e8b1a8b058bcf66e63cffd3c2b`

No author's verification script was executed or imported. The new controls are in this audit directory:

- `independent_controls.py` and its JSON/log: independently generated positive-word relation differences; exact character decomposition for the cyclic covers; a separately constructed 300-point cover; a spanning-tree reduction followed by dense finite-field elimination; independent enumeration of all S3 assignments; complete frozen-integrity checks.
- `reflection_arithmetic_controls.py` and its JSON/log: exact standard reflection matrices, central Coxeter powers, torsion-word weights, Euler polynomials and necessary index arithmetic.

The character calculation works over Q[x]/Phi_d(x) for every d dividing the covering degree, weighting each block rank by phi(d). The 300-point calculation uses neither the author's signed-word traversal nor the author's sparse elimination routine. Its rank calculation instead projects closed relation cycles to the 901 non-tree edges of an independently chosen spanning tree and uses a dense column-oriented elimination. No floating-point rank was used.

## 1 Problem identity and literature scope

**PASS.** The live October 2026 Notebook, printed page 196, states Problem 21.128 for A[F4] and A[H4], with unequal finite indices allowed. It attributes the question to I. Soroko and has no solution marker on this entry. The primary PDF was reached through the editors' update notice after an initial direct fetch failure. Its relevant text matches the locally available primary PDF whose SHA256 is `31baec1b36ec3a956e787355eccfffa2e89df5b1fe31b22a3123377d8103baab`.

Sources: [October Notebook](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt.pdf), [editors' update](https://kourovkanotebookorg.wordpress.com/2026/09/30/october-2026-update-for-the-21st-edition/).

The supplied catalogue identity is consistent with this primary statement. The release correctly says that the exact live catalogue page was not successfully read. That access limitation does not undermine the mathematical identity verified from the Notebook.

The Soroko paper separates each of F4 and H4 from D4 and explicitly leaves F4 versus H4 undecided. Its title must not be truncated after “not commensurable.” The June 2024 author file corrects reference numbering; it is not a new F4/H4 theorem. The Cumplido–Paris journal version likewise leaves the pair open.

The September 2026 papers have been checked in their primary v1 records and PDFs. Gavazzi–Haladjian–Paris Theorem 1.1 compares complete profinite completions of spherical Artin groups, assuming one irreducible input. Hughes–Ng–Ragosta–Scherich–Verberne Theorem C compares irreducible spherical Artin groups; its Theorem A gives the smallest nonabelian quotients used here. Neither statement identifies arbitrary finite-index subgroups as spherical Artin groups or rules out isomorphic open subgroups. Their full profinite rigidity therefore does not decide this commensurability question. The latter record is expressly preliminary. A bounded fresh search found no contrary resolution; this is not a completeness claim about all literature.

Sources: [Gavazzi–Haladjian–Paris v1](https://arxiv.org/abs/2609.25940v1), [Hughes et al. v1](https://arxiv.org/abs/2609.27171v1).

## 2 Central quotient and torsion-free reduction

**PASS.** Cumplido–Paris Proposition 3.1(1) identifies the center of a finite-index subgroup with its intersection with the original center. Parts (2)–(4), and Soroko Proposition 3/Theorem 4, give the pure central splitting, commensurability equivalence and commensurator injection used in the release. These are precisely the needed hypotheses; cancellation of an arbitrary direct Z factor has not been assumed.

Source: [Cumplido–Paris, pp. 508–510](https://ems.press/content/serial-article-files/39000?nt=1).

Both centers are generated by Delta, rather than Delta squared. The source formula for the standard generator is (s1 s2 s3 s4)^(h/2), with h=12 and 30. Independent exact reflection matrices gave Coxeter elements of orders 12 and 30 and yielded -I at powers 6 and 15. Thus the pure group's intersection with the Artin center is generated by Delta squared and its image Q in G has index |W|/2, giving 576 and 7200.

Soroko's Theorem 7 and Table 1 give basic periodic orders 6 and 4 for F4, and 15, 10 and 6 for H4, with every torsion element conjugate to a power of one of those representatives. The source words and diagram numbering match the release. The F4 weights are 2 and 3 modulo 12, of orders 6 and 4. The H4 weights are 4, 6 and 10 modulo 60, of orders 15, 10 and 6. Each cyclic map is therefore injective on every basic cyclic torsion subgroup. Its kernel has no nonidentity torsion. Surjectivity follows from a generator of weight one. This proves the claimed indices 12 and 60.

Source: [Soroko, Theorem 7 and Table 1, pp. 7–9](https://sites.math.unt.edu/~soroko/ArtinFHD4.pdf).

## 3 Geometry and Euler characteristics

**PASS, with a citation improvement recommended.** The complements of the complexified finite real reflection arrangements are aspherical by Deligne. Choosing one arrangement hyperplane gives a scalar product decomposition M(A) = C* times its decone; the decone is also the projective complement. Consequently the projective complement is aspherical and its group is P/Z(P). Hyperplane complements have finite CW homotopy type.

Deligne's theorem applies because finite real reflection chambers are simplicial; H4 being noncrystallographic does not obstruct the theorem. This supplies the K(pi,1) input that the release uses but does not cite explicitly by name. Source: [Deligne, 1972, introduction theorem, p. 273](https://publications.ias.edu/sites/default/files/Number18.pdf).

The exponent lists (1,5,7,11) and (1,11,19,29), the arrangement factorization theorem, and division by the scalar (1+t) factor give the claimed decone polynomials. Their exact expansions are 1+23t+167t^2+385t^3 and 1+59t+1079t^2+6061t^3. The resulting Euler characteristics are -240 and -5040. The products of degrees are 1152 and 14400, and division by the indices 576 and 7200 gives -5/12 and -7/10.

Sources: [exponent table, p. 9](https://homeweb.unifr.ch/kellerha/pub/Naomi_Ruth-arxiv.pdf), [Hoge–Röhrle, Sections 2.1–2.2](https://www.jstage.jst.go.jp/article/tmj/65/3/65_313/_pdf/-char/en).

For a common finite-index subgroup, equality of rational Euler characteristics gives 25 i_F = 42 i_H, hence i_F=42t and i_H=25t. A torsion-free subgroup has index divisible by every order of finite cyclic torsion: a finite cyclic group acts freely on its cosets. The respective least common multiples are 12 and 30. The simultaneous divisibility conditions are exactly 6 dividing t, hence (252k,150k).

Inside the displayed kernels, the Euler equation is 5a=42b, giving (a,b)=(42s,5s). The corresponding absolute indices in G are (504s,300s), a subfamily of the earlier necessary pairs. Passing to the intersections needed for a commensurability witness can refine indices. There is no inconsistency between the two statements and no proof of existence at any of these indices.

## 4 Exact cyclic-cover homology

**PASS.** The quotient presentation has precisely six pairwise Artin relations, including the three commuting nonedges, plus the central word. Every defining relation was included. For each relation L=R, the independent control constructs the difference of the two positive paths from the same initial vertex. This is the same cellular relation cycle as L R^-1 without using the author's traversal code.

The group-algebra Fox identity is checked symbolically before imposing x^n=1. Because the weights generate the cyclic deck group, rank(d1)=n-1. H1 of any connected presentation complex is group H1; omitted higher-dimensional cells cannot affect this calculation.

For F4, the exact ranks of d2 in the cyclotomic character blocks of orders 1,2,3,4,6,12 are respectively 3,3,3,3,2,3. Weighting by 1,1,2,2,2,4 gives total rank 34. H1 has one dimension in the trivial character and one in each of the two primitive order-six characters. Hence b1=3 and 48-11-34=3.

For H4, the trivial character has d2 rank four, and every nontrivial character has rank three. Thus total rank is 4+3(59)=181 and 240-59-181=0.

These are exact characteristic-zero computations. They independently establish rational first Betti numbers only; no claim about integral homology or perfectness follows just from these ranks.

## 5 The 300-point action and modular rank

**PASS.** The displayed five-letter permutations were used as input, rather than rediscovered by the author's search. All four 300-point maps are bijections. The independently generated positive-word sides of each of the six braid relations agree at every point, and the central word fixes every point. All 2,100 relation lifts close. The generated graph has one orbit of size 300.

The layer coordinate increases by one under each positive generator and decreases by one under each inverse. A point stabilizer therefore lies in the weight kernel K_H; its relative index is 300/60=5. Since K_H is torsion-free, so is its stabilizer V. This argument concerns the subgroup of G_H, not the finite permutation image.

The independent boundary construction verifies integer boundary zero for every cycle. A spanning tree has 299 edges; the complement has 901 edges. Projection onto those non-tree coordinates is injective on the graph's cycle space: a cycle supported on a tree is zero. Therefore this projection preserves the relation rank and gives a separate characteristic-zero upper bound of 901.

Dense exact elimination produces rank 901 modulo 101 and again modulo 103. The first prime alone suffices: an integral minor nonzero modulo 101 is nonzero over Q. Hence the Q-rank is at least 901 and at most 901. Thus b1(V)=0 exactly. The result is not a probabilistic rank estimate and does not rely on assuming a modular rank equals a rational rank in general.

## 6 Transfer and the scope of the candidate exclusion

**PASS.** The precise transfer identity is cor_U^K composed with res_U^K = [K:U] times the identity on H1 cohomology with trivial rational coefficients. Thus restriction is injective and every finite-index subgroup U of K_F has b1(U)>=3.

The displayed V cannot be isomorphic to any such U, in particular not one of relative index 42. Nothing makes b1(V)=0 hereditary under further covers. Nor does a single transitive degree-five action classify all degree-five subgroups of K_H. The text correctly retains both limitations. The intersection Q_H with K_H already has b1 at least 59 by transfer from Q_H, directly illustrating why virtual vanishing cannot be inferred.

## 7 Finite quotients and virtual free quotients

**PASS.** Independent enumeration of the 6^4 assignments in S3 gives:

- F4 central quotient: image-order counts 1:1, 2:9, 3:8, 6:12.
- H4 central quotient: image-order counts 1:1, 2:3, 3:2.

The elementary argument in the release is also valid. On the connected odd-edge H4 path the generator images are conjugate. Distinct transpositions cannot satisfy the length-five relation, and the commuting nonedges then force equality. Images in A3 are already cyclic. The F4 assignment to two generating transpositions and two identities satisfies all relations, including the central word.

The localization argument is valid. In each arrangement, a terminal simple pair joined by a 3-edge gives a standard rank-two A2 parabolic localization with three hyperplanes. Inclusion of the full complement into that subarrangement complement induces a surjection on fundamental groups: general position perturbs a based loop off the finitely many extra real-codimension-two hyperplanes while preserving its class in the larger complement.

The map preserves scalar loops. The scalar factor is exactly the pure group's center, so quotienting it gives Q_X surjecting onto F2. One may choose a hyperplane from the A2 localization as the common deconing hyperplane, making this factor compatibility explicit.

Pullbacks of index-d subgroups F_(d+1) give unbounded virtual b1. Pulling back a free subgroup of sufficiently large rank and then mapping to any given finite group proves the existential virtual finite-quotient claim. Passing to the corresponding subgroup of P_X, or taking its product with the central Z under the known splitting, gives the same conclusions for the original Artin group. No assertion about compatibility of all open subgroups or equality of virtual profinite systems is warranted, and none is made.

## 8 L2 invariants

**PASS.** A decone of these essential rank-four central arrangements has rank three. Deligne's theorem and the scalar product decomposition supply the required asphericity, so the space L2-Betti numbers are group L2-Betti numbers. Davis–Januszkiewicz–Leary Theorem A/6.2 applies to the affine decones and concentrates them in degree three. Alternating Euler sum gives 240 and 5040 there.

Finite-index scaling then gives 5/12 and 7/10 for G_F and G_H, and 5 and 42 for their kernels. At relative indices (42s,5s), both top entries become 210s and all other entries vanish. Thus the full L2-Betti vector supplies precisely the Euler ratio and no further obstruction. Infinite central Z makes the original Artin groups' L2-Betti numbers vanish, consistently with their virtual product splitting.

Source: [Davis–Januszkiewicz–Leary v2, Theorem A and 6.2](https://arxiv.org/pdf/math/0612404). The v2 record is a 2007 correction; the PDF's later rebuild date is not a new theorem date.

## 9 Commensurator premise and virtual torsion

**PASS as a conditional argument; HOLD the missing premise.** Commensurable groups have isomorphic abstract commensurators, and the relevant central quotients inject into theirs by the cited theorem. Since G_H has order-five torsion, absence of such torsion in Comm(G_F) would obstruct commensurability. That premise is neither established nor implied by the ambient torsion table.

The alternative finite-index premise is also sufficient: if embedded G_F has index d in its commensurator with 5 not dividing d, an order-five cyclic subgroup would act freely on those cosets, contradicting the degree. No such finite-index theorem has been supplied.

The free-group counterexample is sound. The stated index-fourteen kernel in F2 has the fifteen-element Schreier basis displayed in the release. A 15-cycle of that basis has order fifteen. No nonidentity power becomes the identity on a finite-index subgroup: that subgroup contains a positive power of a moved basis element, and equality of that power with the corresponding power of a different basis element contradicts unique roots in a free group. Thus the induced commensurator element still has order fifteen. This refutes the ambient-torsion inference without establishing any torsion in Comm(G_F).

## 10 Packaging and recommended refinements

**PASS.** The frozen release contains authored Markdown, Python scripts, text logs/configuration and derived JSON data only. No source PDF, screenshot, raw catalogue corpus or private correspondence is inside it. Its explicit unresolved status, five-attempt count and lack of a priority claim are appropriate.

No mathematical repair is required to retain the stated partial conclusions. Recommended small improvements for a future, separately versioned release are:

1. Add Deligne's 1972 paper as an explicit source for asphericity and explain that the scalar C* factor makes the projective complement a K(Q_X,1).
2. Replace “the complements are finite aspherical complexes” by “the complements have finite aspherical CW models” or “are aspherical and have finite CW homotopy type.” The intended use is correct, but the present literal wording identifies a noncompact manifold with a finite complex.
3. Write the transfer composition explicitly as cor composed with res, avoiding the verbal ambiguity of “corestriction followed by restriction in the appropriate order.”
4. Optionally include the H4 periodic representative words, rather than only their lengths, near the kernel proof. The cited table already supplies them and the numerical weights are correct.

Preserve the following unresolved boundaries: no classification of all index-five candidates; no exclusion of larger relative indices; no virtual rigidity theorem; no identification of Comm(G_F); and no promotion of full profinite rigidity to commensurability rigidity. These are research gaps, not issues that can be repaired by stronger wording.
