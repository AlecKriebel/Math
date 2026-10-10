# Independent five-turn review: opposite vertices of bases

2026-10-02. **PASS for the bounded-base partial results, conditional on the mandatory additive source-scope correction now supplied. The bounded research target remains unsolved after 5/5 substantive author turns.** No further mathematical revision is required to the scoped positive proofs. This is AI-assisted review, not formal verification, human peer review or historical-novelty certification.

## 1. Mandatory source correction and final scope

The exact [Egres question](https://oldlemon.cs.elte.hu/egres/open/Opposite_vertices_of_base_polyhedra) was independently downloaded in full. It assumes only that every vertex is ternary and that the origin belongs to the base. It does **not** explicitly assume containment of the entire base in the cube. Its linked [definition](https://oldlemon.cs.elte.hu/egres/open/Base_polyhedron), also independently retrieved, permits extended values +infinity and distinguishes finite-valued ranks as the bounded base-polytope case.

Consequently the frozen TURN_1 introduction silently narrowed the source by taking b finite. The inference from ternary vertices to whole-polyhedron cube containment is valid for a bounded polytope, but is false in the extended-valued setting. This required correction is substantive to applicability, even though it does not invalidate the bounded proofs.

The pointed ray B={(t,-t):t<=1}, defined by b(empty)=b(V)=0, b({1})=1 and b({2})=+infinity, is admissible under the current literal linked definition. Its unique vertex is (1,-1); the negative is a nonextreme interior point of the ray. Thus the literal broad wording is false. The example does not resolve the nontrivial bounded-base question. The question page is dated 2011 and the linked definition's recorded modification is 2014, so neither the example nor the present link determines the original author's intended convention.

The additive SOURCE_SCOPE_CORRECTION.md, SHA256 `1ca27005229a2ee9a637dabe0a593a801273f2bd29ab84271c122ffd6e61c2b1`, correctly acknowledges the error, proves the ray assertion and restricts all finite-ground-set, zero-face and minimum-counterexample claims to bounded bases. Its correction manifest is `33008977a4fe04780364d4b2971963c1ea7a256dc9c67b547d21eb7ec97acd9e`. All historical files remain unchanged. Any public README, status file or PR summary must lead with this distinction and must not repeat the unrestricted n<=5 claim without qualification.

The four bounded positive classes and the general bounded conjecture are audited below. Frank's related 2-polymatroid question and the stronger generalized-polymatroid suggestion are separate questions, not alternate formulations silently substituted here. The source allows the zero vector to serve as both opposite vertices.

## 2. Canonical ranks, zero-chain factors and complete small cases

For a finite rank function, greedy maximization gives its exact canonical bound on every subset. Integral ternary vertices therefore imply integer canonical ranks between zero and min(|S|,n-|S|). The claimed bound relies on boundedness, now explicitly supplied.

The maximal zero-chain face is exactly the product of the stated restriction/contraction factors. In the nontrivial direction, diminishing returns compares each factor increment with the increment over the smaller portion of the requested subset; summing yields the original inequality. Every factor contains zero. Its vertices extend to vertices of the product face and hence to vertices of the original polytope. An opposite pair in every factor therefore supplies an opposite pair in the original base. Maximality of the chain makes every proper nonempty factor rank positive.

After reduction the finite search space is complete: one table for n<=3, 64 for n=4 and 2^20 for n=5. Elementary square inequalities are equivalent to submodularity. Strict greedy objective orders yield genuine vertices, even when different permutations repeat a vertex. Ternary negation and encoding are correct. The submitted enumeration was recompiled with assertions enabled and reproduced exactly.

A separate implementation tested all submodular inequalities for arbitrary pairs of subsets, then recovered vertices by active-constraint rank rather than the author's greedy enumeration. It independently obtains accepted counts 1,1,1,64,4209 and maximum vertex counts 1,2,6,14,31, and verifies an opposite pair for every accepted table. Its rank calculations modulo 101 are exact rational-rank tests here: all minors are 0/1 determinants of size at most five, whose absolute value is less than 101 by Hadamard's bound. This establishes the stated computer-assisted bounded theorem with independently checked coverage. The rolling checksum is not treated as a retained witness certificate.

## 3. Integral root-direction zonotopes

The representation argument is valid. Each combined generating direction occurs as an edge direction, and the primitive root length is integral because the corresponding endpoints are integral. Changing orientations only changes the integral translation. The standard base-edge direction fact agrees with the greedy normal-fan argument and does not require a central-symmetry assumption about the origin.

Coordinate widths are exactly the weighted graph degrees. Cube containment forces degree at most two, hence isolated coordinates, unit paths, unit cycles or doubled edges. Centers of degree-two coordinates vanish; path endpoints have opposite half-integer centers because each component has zero total at the feasible origin. The displayed path corner is zero and is a vertex by independence of its root directions. Centered cycles and doubled edges give genuine opposite vertex pairs. Cartesian products preserve vertexhood. This proves the whole stated zonotopal class.

## 4. Laminar upper-constraint representations

The zero-bound residual atoms partition the ground set, including nested zero sets and empty residuals. A positive-bound set meeting a zero child either contains it or lies inside it; minimality of its zero ancestor removes the latter case. On the zero-equality face only its residual atom portion contributes.

The tree pairing lemma leaves at most one unmatched leaf at each node and at most one zero coordinate at an odd root atom. Thus every relevant set has signed sum between -1 and 1, and both signs satisfy every positive integer bound. Each nonzero coordinate is fixed by an active cube constraint. Each remaining zero coordinate is separately fixed by its own atom equality. This gives full vertex certificates for both signs even with several odd atoms. No global laminar representation is inferred from a vertex's local tight-set chain.

The author's exact rank checks replayed. Independent controls additionally cover 6,561 laminar-family/zero-versus-one-bound cases on four coordinates, directly searching and certifying both opposite vertices.

## 5. Translated sums of coordinate simplices

Each nonsingleton summand contributes an exact coordinate interval [0,1], so summand multiplicities give widths d_i and the asserted integral translation choices. The dual graph has no loops; repeated summands can produce parallel edges. Zero feasibility gives h=m+r separately in every component. Together with connectedness, this forces a tree with one required stub or a unicyclic component with none.

In a tree the required stub and depth-decreasing weights create one unique selection per simplex and give the zero vertex. In a unicyclic component, the reversed cycle ordering makes every cycle vertex choose its other cycle edge; the two selection counts add to two on cycle edges and to twice the required translation elsewhere. The argument includes the two-parallel-edge cycle. Unique maximization on every summand proves unique maximization on the sum, so the two points are vertices rather than merely opposite allocations.

The proof handles every stated hypergraphic instance. It does not assert that arbitrary submodular bases admit such a decomposition. Independent finite controls verify 200 small translated coordinate-simplex instances, including 100 graphical cases, beyond replay of the author's larger fixture collection.

## 6. Tight partitions, intersection integrality and the failed shortcut

The lattice of tight sets is closed under union and intersection. A maximal tight chain has blocks that no tight set can split; conversely its row span contains every block indicator. Finite slack gives precisely the asserted affine hull. For two bases, the signed joint block-sum matrix is the bipartite incidence matrix, of rank k+l-c. Thus the face dimension equals cycle rank, and intersection vertexhood is exactly the forest criterion. Leaf elimination gives integer coordinates at such a vertex. The self-contained proof does not assume that intersections of integral polytopes are automatically integral.

For a maximum-support symmetric feasible integer point, saturated coordinates are singleton blocks in both partitions. A residual cycle would provide a nonzero direction supported on the zero coordinates. Intersecting the two minimal faces remains an integral base intersection and has a distinct integral vertex, retaining every old nonzero coordinate and increasing support. This contradiction proves the residual forest conclusion. It does not make every residual component an isolated edge, and therefore does not prove individual endpoint vertexhood.

The explicit four-coordinate warning is valid. The positive endpoint is the midpoint of two different greedy vertices, while its negative is a vertex. The complementary positive-pair constraints rule out support four, so its support is maximal. Another opposite vertex pair exists, preserving the original bounded conjecture for that example.

The independent active-rank/signature-partition implementation reproduces all 44,879 maximum-support points and all 912 failures of the overstrong endpoint shortcut, with the forest criterion holding throughout. It confirms that the finite checks actively detect the false shortcut rather than endorse it.

## 7. Integrity, controls and disposition

The original 25-file packet is bound by final manifest `6cd9cb8a73c84843aa11e936f4d52e9d1eb921f78f3c559dfcc9ef62b5ab5de8` and remote head `e0fcc7fd54a387270adc9d30340be52bd4812066`. All 25 files passed exact remote content and Git-blob comparison. The additive correction's three bound files and its manifest were checked separately; they are not misrepresented as part of that earlier head.

All five original outputs replay byte-for-byte. The three Python turns report 24,646, 685,860 and 133,240 assertions respectively. The two C++ turns have their separately defined enumeration, coordinate and edge-check counts; these are not combined into a misleading assertion total. The correction's 344 exact controls also replayed.

Separate independent code supplies 142,934 finite assertions and 26 exact controls for the ray diagnosis. The finite C++ implementation, ray checker, outputs, replay receipts and integrity record accompany this report. Downloaded source HTML/PDF files and compiled executables are excluded.

Final recommendation: **unsolved, 5/5 for the bounded-base research target**, with the literal extended-valued ray obstruction prominently recorded as a formulation correction. The bounded positive classes and residual-forest theory pass. No unresolved general result, historical priority, or solution of the intended bounded conjecture is claimed, and no sixth author search is warranted.

Classical foundations were checked against Bach's *Learning with Submodular Functions*, Propositions 3.2–3.3 and 4.2, and the credited [Cunningham exposition of polymatroid intersection](https://ems.press/content/book-chapter-files/27359?nt=1). The archived Egres open label is not treated as a current literature certificate.
