# Independent audit: third-homology generated seminorm

Problem 30001812 / OWR-5158-013. Audit date: 9 October 2026 UTC.

## Verdict

**Accept the corrected partial comparison and the supporting reductions. The original equality remains unresolved.**

The audited argument establishes, for every topological space X and every alpha in H_3(X; R),

    ||alpha||_1 <= G_X(alpha) <= (v_8/v_3) ||alpha||_1.

Here G is defined by exact finite real linear combinations of images of fundamental classes of oriented closed connected 3-manifolds, weighted by their ordinary real simplicial volumes. The comparison is not an equality theorem, an optimality result, or a novelty claim. The five-approach research limit stays 5/5; this is verification and correction, with no additional research approach.

No fatal defect was found in the main mathematical derivation. The frozen presentation needs the following bounded corrections, supplied in CORRECTIONS.patch:

1. A single connected-manifold realization of a rational class requires a path-connected target. For a general target, use a finite sum over path components. The unqualified sentence in source interface 1 is false as written: on S^3 disjoint-union S^3 the class (1,1) cannot come from one connected source. The proof already allows finite sums, so this does not change the theorem.
2. Löh–Moraschini state their symmetrization homotopy over R. The displayed formula preserves Q-chains, and real homology preservation suffices here. The patch makes this exact rather than attributing a rational chain-homotopy statement directly to that source.
3. Make the finite support, Delta-complex convention, and component/orientation arguments explicit. Restore the finite-2-skeleton and hyperbolic-source hypotheses when describing other source interfaces.
4. The original diagnostic relies on Python assert. Its checks disappear under -O/-OO. A real false-count mutation is accepted in those modes. The patch replaces assertions with explicit exceptions; the independent checker also uses no removable assertions.

Acceptance is of the mathematical theorem with these source/convention clarifications and corrected diagnostic claims. It does not certify every sentence of an unpatched frozen file as literally accurate.

## 1. Scope and input integrity

The seven authored files listed in the supplied FREEZE.json were independently hashed before and after testing. All sizes and SHA-256 values match the frozen inventory. The originals were not edited. No queue, GitHub branch, PR, or publication was changed by this audit.

The independent implementation does not import the original checker or use its reported PASS as evidence. It uses exact rational arithmetic and a different permutation-sign algorithm. The original script is executed only in a separate comparative test, including an actual mutated copy.

Seven supplied scholarly PDFs were independently byte-checked against SOURCE_METADATA.json; all match. Their relevant text was inspected locally, and the primary public URLs were also opened using the web reader. The Gromov statement was checked through the public PDF, without claiming a local download or hash. SOURCE_AUDIT.json records this distinction. No third-party source PDF or extracted source text belongs to this audit's authored publication packet.

## 2. Primary source interfaces

### 2.1 The exact problem and the generated seminorm

Löh's OWR 30/2011 contribution, printed p. 1693, Theorem 32 and Question 5, gives the finite-real-expression target. Crowley–Löh Definition 4.1 and Theorem 4.2 give its finiteness and functoriality. Corollary 3.2(1) supplies a rational scalar realization on a path-connected target. Their Proposition 4.3 explicitly excludes dimension 3. Their Theorem 3.1(2) additionally requires a connected CW target with the stated finite-2-skeleton homotopy condition and dimension at least 4.

Sources: https://ems.press/content/serial-article-files/46346 ; https://loeh.app.uni-regensburg.de/preprints/funcseminorms.pdf .

### 2.2 The normalization mechanism

Löh–Moraschini, arXiv:2003.02584v2, Definition 3.1 and Lemmas 3.2–3.3, p. 3, provide the real chain map S, its homotopy to the identity, contractivity, and the relation partial_i S = (-1)^i partial_0 S. Hence a cycle satisfies

    0 = partial S(c) = (n+1) partial_0 S(c),

and every separate face vanishes. The formula uses rational coefficients 1/(n+1)!, so it sends a rational chain to a rational chain. The argument does not need a rational homotopy: rational output and equality of real homology classes are sufficient. This source's equality for a different normalized-chain seminorm is not used as an answer to the present question.

Source: https://arxiv.org/abs/2003.02584v2 .

### 2.3 Realization and the numerical constant

Lafont–Pittet, pp. 376–377, explicitly extend the coloured realization to Delta-complexes. Their counts are d=KB/2 and q=2^(n-1)B. Lemma A.2 gives ||T_3||=8v_8/v_3. These yield d/q=K/8 in dimension 3. The published factor with barycentric subdivision includes an additional 24.

Source: https://people.math.osu.edu/lafont.1/pjm-259.pdf .

The independent count check in Gaifullin's 2008 construction is |V|=K B 2^(n-1) permutahedra; the Tomei base has 2^n tiles. Thus d=KB/2, while q=2^(n-1)B. The total constructed cover may be disconnected; retaining it preserves both counts. Gaifullin's 2012 paper, section 6, p. 12, independently gives the tile equation qK=2^n d. Neither source forces choosing one component in this application.

Sources: https://arxiv.org/abs/0806.3580 ; https://arxiv.org/abs/1204.0208 .

### 2.4 Other route checks

Derbez–Liu–Sun–Wang, Theorem 1.9, starts with a closed oriented hyperbolic source M and gives a source-dependent constant c(M) for manifold targets. It does not assert c(M)=1 or realize arbitrary third-homology classes. Gromov's connected-sum additivity in dimensions at least 3 validates the pinch-map and doubled-handlebody volume calculations used in the report.

Sources: https://msp.org/gt/2017/21-5/gt-v21-n5-p13-p.pdf ; https://people.math.harvard.edu/~ctm/home/text/others/gromov/vol_bounded_cohom/vol_bounded_cohom.pdf .

## 3. Detailed audit of the comparison proof

### 3.1 Lower bound, finiteness, and arbitrary spaces

For each admissible representation, functoriality of the ordinary seminorm bounds the image of each manifold fundamental class by the manifold's simplicial volume. The triangle inequality gives p<=G. No efficient realization claim is hidden here.

Singular chains split as a direct sum over path components, even when those components are not open. Every singular simplex has path-connected image. Every connected manifold used here is path connected and maps into one such component. Therefore both seminorms are additive on the finitely supported component decomposition of a class. The arbitrary-space argument does not assume X is a CW-complex, locally connected, or Hausdorff.

Finiteness follows from rational realization component by component and the coefficient-change isomorphism

    H_3(X; Q) tensor_Q R = H_3(X; R).

The singular chain groups are free and field extension is flat. Every vector in the tensor product is a finite sum, including for infinite-dimensional homology. This establishes exactly the finiteness needed for the subsequent finite-span limit.

### 3.2 Rational near-minimizers

Fix a rational cycle z. A real homologous near-minimizer c_0 differs by the boundary of a finite real 4-chain b_0. Include all singular 3-simplices in c_0 and z and every face in partial b_0, and all 4-simplices in b_0. On those finite bases, c-z=partial b is a finite affine system with integer matrix and rational right-hand side.

Gaussian elimination yields a rational particular solution and rational direction basis whenever a real solution exists. Rational coordinates approximate the coordinates of (c_0,b_0), preserving the equation exactly. The l1 norm is continuous in finitely many chain coefficients. Thus one can preserve the strict near-minimal inequality while using a rational chain. No assumption that an infimum is attained is made. No global homology topology or integrality conclusion is inferred from this approximation.

### 3.3 Pairing, orientations, and quotient topology

Let c'=S_3(c), let m>0 clear its reduced coefficients, and take the absolute coefficient number of signed tetrahedron copies. A coefficient sign is an orientation relative to the vertex ordering 0,1,2,3; it is not a claim that the map to X preserves an ambient orientation.

For every fixed omitted index i and every actual singular face map tau, partial_i(mc')=0 gives equal numbers of positive and negative occurrences. An arbitrary bijection pairs these finite sets. Equality must be equality of the complete singular face maps in standard coordinates, not just equality of vertex images. The proof uses the former. Thus the map to X descends continuously through the quotient.

The induced orientation of an i-face is the top sign times (-1)^i. Opposite top signs at equal i give opposite face orientations. The identity in face coordinates sends colour j to colour j for every remaining vertex. All induced identifications of lower faces preserve their colour sets and barycentric coordinates. A tetrahedron contains only one vertex of each colour and only one face of each colour set. Consequently no two vertices of a tetrahedron or two distinct faces of that tetrahedron are identified with each other, and no nontrivial folding inside a simplex is introduced.

The resulting finite quotient has the required Delta-complex structure. Every codimension-one open face is incident to the prescribed two top faces. The complex is pure, boundaryless, and oriented. Taking each dual-graph component separately gives strong top-dimensional connectivity. This is the pseudomanifold convention used for the cited construction; connected or spherical lower-dimensional links are not required. A normal pseudomanifold or a genuine manifold is not silently assumed.

On a dual component, cellular top cycles have coefficients determined from one tetrahedron by orientation propagation, because adjacent faces occur exactly twice. Hence the signed top chain represents its integral fundamental class. Its image is exactly the relevant portion of mc', and summing components gives m beta in real homology. The theorem needs this real identity only.

Counting positive and negative tetrahedra through the faces of any fixed omitted colour shows that each nonempty component has equally many positive and negative top copies. In particular K_l is even, consistent with the degree KB/2. Repetitions among singular maps, equality of vertices in X, and degenerate singular simplices do not change this argument. Colours belong to the domain copies, not X.

### 3.4 Disconnected covers and cost

For each P_l, use the entire oriented cover N_l supplied by the theorem with total sheet number d_l and total map degree q_l. The covering orientation is compatible with the source count convention. Its simplicial volume is d_l ||T_3||, by multiplicativity on connected covers and additivity on their disjoint union.

If N_l is disconnected, split it into connected manifold sources in the definition of G and give every such component the coefficient 1/(m q_l). There is no need for every component's map to have the same degree, or for the q_l to agree across different P_l. The equality is about the sum of their fundamental classes. The resulting cost is

    sum_l ||N_l||/(m q_l)
      = sum_l K_l ||T_3||/(8m)
      = (v_8/v_3) ||c'||_1.

Clearing a chain denominator multiplies K and the represented homology class by the same m. There is no residual 24 factor: symmetrization is contractive, while denominator clearing is canceled by the 1/m coefficient. This is the essential successful point in the proof. The fixed cost ||T_3||/8 remains; the argument does not make it 1.

### 3.5 Passing to real classes

On any fixed finite rational span, for either finite seminorm F,

    |F(sum_i t_i beta_i)-F(sum_i s_i beta_i)|
      <= sum_i |t_i-s_i| F(beta_i).

Rational coefficient approximants therefore converge in both p and G. The constant is uniform in X and the rational class, so the rational inequality extends to every real class. The zero class uses the empty expression. Combining both comparisons proves equality of zero sets, which by itself gives no equality of the seminorms.

## 4. Other propositions in MATHEMATICAL_REPORT.md

### 4.1 Integral stabilization and torsion

Proposition 2.1 is correct with the explicitly allowed finite disjoint union. The easy direction uses each integral representative of m beta with coefficients 1/m. For the other direction, restrict the finite set of integral image classes and beta to their rational span. Injectivity after Q-to-R scalar extension makes the exact real relation an equation over a rational affine solution space. Approximate its coefficients rationally without changing the relation, then clear denominators.

The resulting error in H_3(X; Z) is in the kernel of rationalization, hence is torsion. One additional integer t kills this single error element. Taking t times the signed multiplicities produces an exact representative of tm beta; orientation reversal changes fundamental classes' signs and leaves simplicial volume unchanged. The normalized cost is exactly the rational coefficient cost. Its limit gives S<=G.

The finite union may be empty for a zero class. Torsion beta has G(beta_R)=0 and S(beta)=0 because a positive multiple is zero. No uniformly bounded torsion exponent is required. A general non-torsion group need not be finitely generated; only one error element is killed. The topological/smooth source conventions coincide in dimension 3. Connecting components by 1-handles is optional and unused.

### 4.2 Isometric realizations and pinch maps

Proposition 3.1 is an immediate valid squeeze. On connected CW targets the cited bounded-cohomology mapping mechanism supports the stated sufficient isometry condition. It does not supply a dimension-3 realization theorem. The dimension and finite-2-skeleton hypotheses must remain attached to the surgery source.

For M#rH, the degree-one pinch preserves the mapped class [M], whereas connected-sum additivity gives ||M||+r||H||. This disproves a proposed inference from class preservation to cost control. It does not give a strict inequality for G, since M itself is an available optimal source.

### 4.3 Suspension example

The double of the genus-g handlebody maps onto the suspension of its boundary. On a collar, the map contracts each boundary point toward its cone apex; the remaining interior is sent to that apex. These maps agree on the common boundary. Orient the two halves as the double and the cones as the suspension. The boundary identity gives relative degree +1 on the two correctly oriented halves, hence global fundamental-class degree +1.

The source is the connected sum of g copies of S^1 x S^2. A degree-two self-map on its S^1 factor forces ||S^1 x S^2||=0, and connected-sum additivity gives source volume zero. Thus both target seminorms vanish despite nonspherical vertex links. Barycentric subdivision of a finite suspension triangulation gives regular colours and separately vanishing face operators without changing its singular links. This is a valid counterexample to a link-genus-only lower-bound proposal, not to the original equality.

### 4.4 Finite witness family

Proposition 5.2 is correct under the Delta-pseudomanifold convention made explicit above. Universal equality implies the K bound because the signed characteristic tetrahedra form a singular fundamental cycle of norm K. Conversely, applying the hypothesized K bound to each component of the coloured realization gives G(beta)<=||c'||_1, and the near-minimizer and real-limit arguments give equality everywhere.

For the strict witness statement, a strict gap persists on a rational coefficient approximant in the same finite span. Choose c with ||c||_1<G(beta), normalize, and clear denominators. Functoriality and subadditivity yield

    sum_l G_(P_l)([P_l]) >= mG_X(beta) > sum_l K_l.

A finite sum strictly exceeding the sum of the K_l has at least one component exceeding its own K_l. This is the correct direction of the inequality. The criterion is an exact reduction, not a proof that such a component exists or an algorithm that decides the condition.

### 4.5 Duality and bounded cocycles

Proposition 6.1 correctly identifies D_M with all algebraic linear functionals dominated by G in absolute value. One implication evaluates a functional on every admissible finite expression and infimizes; the converse uses the one-term cost bound. Real Hahn–Banach extends the functional t alpha -> tG(alpha) from the line through a positive-G class. Symmetry of the seminorm converts one-sided domination to absolute domination. At G(alpha)=0, the zero functional attains the supremum. No compactness of an infinite-dimensional dual ball is assumed.

Proposition 6.2 starts from a well-defined functional on cycles, vanishing on boundaries. Its bound by the homology seminorm implies the same bound by the chain l1 norm. Hahn–Banach extends it to all finite singular chains. Vanishing on all boundaries of 4-chains makes the extension a cocycle. A bound on basis simplices is exactly its l1 operator bound. Conversely, evaluate a bounded cocycle on all representing cycles and infimize. This works also for C=0 and without completing the chain space.

Therefore D_M=D_1 is equivalent to equality of the seminorms, and the unit-bound representative condition is exact. The comparison only gives bound v_8/v_3 for members of D_M. It supplies no hidden unit-bound conclusion.

## 5. Computational evidence and its limits

TEST_RESULTS.json records the executed matrix. The main checks run in ordinary Python, -O, and -OO. Each uses 80 exact chain cases in dimensions 1 through 5, including repeated vertices, rational denominators, arbitrary chains and boundaries. Tests check boundary-squared, chain-map and separate-face identities, l1 contractivity, exact pairing coverage, signs, colours, global vertex identifications, fundamental-chain pushforward, denominator cancellation, disconnected component counts, and conditional degree arithmetic.

The basic 4-simplex-boundary fixture has original l1 norm 5, denominator 24, 120 tetrahedra and 240 face pairs. A disjoint-support duplicate has two 120-tetrahedron components and 480 pairs. Algebraic toy fixtures check that clearing rational coefficients alone need not clear integral torsion and that component-dependent q values cancel separately. These are diagnostics, not substitutes for proofs in Sections 3–4.

Eleven actual negative controls mutate the algorithm or input: unsigned averaging, lost averaging denominator, skipped normalization, same-orientation pairing, wrong omitted index, a colour-breaking gluing, missing and duplicate face pairs, wrong chain denominator, wrong cover/map ratio, and omitted torsion multiplier. Every one failed in every optimization mode, for 33 rejections. A separately tampered frozen-input copy was also rejected in all three modes. A separate false-count mutation demonstrates the original assertion problem and verifies the supplied explicit-exception repair.

The read-only test executes as actual non-root uid 1000, from a copied directory with directories mode 0555 and files mode 0444, including a copied frozen input tree. In each optimization mode the independent checker runs successfully, and real attempts to append to an existing sentinel and create a new file fail with PermissionError. Thus six write attempts are actually denied; no result is inferred from mode bits alone. The copied tree and frozen authored files are hashed before and after. This is a POSIX non-root read-only probe, not a claim that root or the file owner could never change permissions.

No finite diagnostic proves the realization theorem, the topology of every quotient, a universal homology inequality, or existence/nonexistence of a strict witness. Those conclusions above rest on the mathematical arguments and precisely scoped primary-source interfaces.

## 6. Acceptance boundary

Accepted after the explicit presentation/diagnostic corrections:

- The all-space real-class v_8/v_3 comparison, and equality of zero sets.
- Exact integral stabilization with torsion clearing and finite-span real reduction.
- The stated sufficient isometric-realization criterion and negative route checks.
- The suspension example and finite coloured Delta-pseudomanifold witness equivalence.
- The attained algebraic dual formula and the bounded-cocycle extension criterion.

Not established:

- Equality G=||.||_1, a strict counterexample, a unit-cost realization, or a unit-bound dual extension.
- Optimality or novelty of v_8/v_3; exhaustive worldwide literature status.
- A universal theorem certified by a numerical or finite combinatorial test.

This audit adds no research turn. The final original-problem status remains unresolved after 5/5 approaches.
