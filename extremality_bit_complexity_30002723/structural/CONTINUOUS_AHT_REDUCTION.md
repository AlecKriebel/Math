# Candidate polynomial-bit reduction for continuous rational input

20 October 2026. Authored derivation for independent audit; not a claim that the full discontinuous target is resolved.

## Result and boundary

For the subclass in which the input minimal valid function is continuous, the following reduction appears to give a deterministic polynomial-bit-time extremality test, even against unrestricted valid-function competitors. The key imported algorithm is weighted interval-pairing orbit counting. The rest of this note supplies the reduction and its correctness obligations.

The reduction does **not** extend immediately to discontinuous input: integration of slopes no longer represents every perturbation, and zero-dimensional values/jumps require extra control. It therefore does not by itself resolve the queued target.

## Imported results and primary sources

1. Basu–Hildebrand–Köppe, Part I, arXiv:1206.2079v2: Theorem 2.9 gives continuity/Lipschitz continuity of arbitrary valid competitors in a decomposition of a continuous piecewise-linear minimal function. Lemmas 4.1 and 4.5 impose affine behavior on directly covered grid intervals and propagate it through additive-edge relations. Lemma 4.8 constructs a nonzero effective perturbation when a grid interval is not covered. Theorem 3.2 turns a nonzero kernel vector for a finite piecewise-linear active-equality system into non-extremality. Source: https://arxiv.org/html/1206.2079v2
2. Agol–Hass–Thurston, *The Computational Complexity of Knot Genus and Spanning Area*, arXiv:math/0205057v2, Theorems 12 and 16. Interval pairings are integer translations/reflections between integer subintervals. Their orbit count, and orbit sums for piecewise-constant vector weights, are computable in time polynomial in the number of pairings, the weight description, and the binary integer sizes. Output uses multiplicity intervals when many orbits have identical weights; it must not be read as an exponentially long explicit orbit list. Source: https://arxiv.org/html/math/0205057v2 (Section 6, especially the paragraph defining the output list before Lemma 15 and Theorem 16).

Only these theorem interfaces are needed. In particular, no claim is made that a practical unweighted AHT implementation already implements the required weighted version.

## 1. Sparse geometry

Let B contain 0, 1, f and all input breakpoints, with n=|B|, and let q be their least common denominator. The bit length of q is at most the sum of the denominator bit lengths, hence O(L), although its value may be exponential in input size L.

Use the arrangement inside [0,1]^2 of x=b, y=b and x+y=b+k, for b in B and relevant k in {0,1}. It has O(n^2) faces and vertices, and all vertex coordinates and coordinate sums lie on q^{-1}Z. A naive polynomial enumeration of triples of intervals also suffices. On every face F, Delta pi(x,y)=pi(x)+pi(y)-pi(x+y) is affine and nonnegative. Its zero set is therefore a union of arrangement faces. Identify all additive 2-faces and 1-faces, and all additive vertices, using exact rational arithmetic.

The following argument uses the conceptual q grid but never expands it. Its open cells are I_k=(k/q,(k+1)/q), 0 <= k < q. All projections below are reduced modulo one, splitting an interval at an integer when necessary.

## 2. Polynomial-size pairing presentation of slope components

Construct a graph H on the q conceptual cells, encoded by interval pairings on their integer indices.

### Additive 1-faces

For a horizontal or vertical additive face, the two nontrivial projections are related by a translation x -> x+t. Encode the induced pairing k -> k+qt, reducing modulo q and splitting at a wrap.

For an additive diagonal face x+y=t, encode k -> qt-k-1, again reducing modulo q and splitting at a wrap. Reflection reverses the cell order, but it does not negate slopes: differentiating h(x)+h(t-x)=h(t) gives h'(x)=h'(t-x).

Each coarse face gives O(1) pairings. Zero-dimensional faces are not included here; their equations are retained for the final linear system.

### Additive 2-faces and seeds

For each additive 2-face F and each projection p_i(int F)=(a,b), impose equality among all cell slopes whose cells lie in this projection. If A=qa and B=qb, this is represented by the single shift-by-one pairing [A,B-2] -> [A+1,B-1], omitted when there is only one cell. Join one representative from each of the three projected cell intervals by singleton pairings. These links enforce the common slope supplied by the interval lemma.

Mark one representative cell of F as its seed. There are O(n^2) such seeds and pairings. Multiple seeds may occupy the same cell without any difficulty.

The artificial shift-by-one and singleton links have been added only among cells already directly covered by a 2-dimensional additive region. Therefore they do not make an originally uncovered component appear covered. They legitimately merge equal-slope covered components.

### Exactness relative to the fine-grid test

An additive fine-grid 1-face is either contained in an additive coarse 1-face, or lies in a coarse 2-face on which Delta pi is identically zero. Indeed, a nonnegative affine function cannot vanish on an interior line segment without vanishing on the full 2-face. Fine-grid segments on coarse boundaries are handled by the first case. Thus coarse edge pairings, together with the directly covered seeds, detect precisely whether every fine-grid cell is connected to a directly covered cell.

Consequently:

- If an H orbit has no seed, BHK Lemma 4.8 supplies a nonzero effective perturbation, and pi is not extreme.
- If every orbit has a seed, every valid competitor in a decomposition of pi is affine on every I_k, and its slope is constant on each H orbit.
- In the second case H has at most as many orbits as there are additive 2-faces, hence polynomially many slope variables.

This is the first important compression: the output need not describe the cell-by-cell component coloring.

## 3. Obtain all integrals needed for the rank test

Let T consist of 0, 1, f, and the reductions modulo one of all x, y and x+y coordinates of arrangement vertices. It has polynomial cardinality.

Assign each conceptual cell k the following vector weight:

- one coordinate for each seed, equal to 1 at that seed's cell and 0 elsewhere;
- one coordinate for each t in T, equal to 1 when k < qt and 0 otherwise.

This weight function is piecewise constant on polynomially many integer intervals, even though q may be huge. Its description and vector dimension have polynomial size. Apply weighted AHT to H.

The sum of the seed coordinates on an orbit determines whether it is covered and gives a unique nonempty seed signature for each covered orbit. Distinct covered orbits cannot share a seed signature because a seed belongs to only one orbit. A nontrivial multiplicity in the AHT output can thus arise only for unseeded orbits; it must not be expanded. If any unseeded orbit appears, return non-extreme.

Otherwise enumerate the polynomially many covered orbits C and extract

N_C(t) = |{k in C : k < qt}|.

All counts are integers at most q. These are sufficient statistics for integrating a slope-constant perturbation:

h_s(t) = q^{-1} sum_C N_C(t) s_C.

The full h_s is defined mathematically by integrating the piecewise-constant slope function s_C on the conceptual q grid, with h_s(0)=0. It need not be explicitly materialized.

## 4. Polynomial-size linear system

Introduce one slope variable s_C per H orbit. Impose

1. h_s(1)=0 (periodicity),
2. h_s(f)=0 (normalization),
3. h_s(x)+h_s(y)-h_s(x+y)=0 at every additive coarse vertex (x,y), interpreting h_s at x+y>1 by periodic reduction.

Every coefficient is a signed sum of at most three orbit prefix counts, divided by q. Multiplying rows by q gives an integer matrix with polynomially many rows and columns and O(log q) coefficient bit lengths. Exact rank computation is polynomial in L.

Return extreme if and only if the kernel is zero.

## 5. Why coarse vertex equations suffice

The main possible gap in this reduction is that h_s can have slope changes at q-grid points that are not coarse input breakpoints. They do not invalidate the following argument.

For an additive coarse 2-face F, all cells in each of its three projection intervals are joined, and the three intervals are joined to one another. Thus h_s is affine with the same slope on each whole projection interval, including across fine-grid points. Delta h_s is therefore constant on F. The coarse vertex equations force that constant to vanish.

For an additive coarse 1-face E, the edge pairings give equal derivatives in the paired cells almost everywhere along E. As h_s is continuous and piecewise linear, its restriction Delta h_s|E is absolutely continuous with derivative zero almost everywhere. It is therefore constant on the whole edge; the coarse endpoint equations force it to vanish. For reflection edges the two sign changes cancel, as recorded in Section 2.

At an isolated additive coarse vertex the equation was imposed explicitly.

These cases exhaust {Delta pi=0}. Hence Delta h_s vanishes wherever Delta pi vanishes, including all active vertices of the full q-grid complex. Together with h_s(0)=h_s(1)=h_s(f)=0, the function h_s is a kernel vector for the ordinary finite q-grid active system. BHK Theorem 3.2 gives an effective perturbation whenever s is nonzero. Nonzero slope data imply h_s is not the zero function.

## 6. Both directions of correctness

**Nonzero compressed kernel => non-extreme.** Section 5 and the finite-grid perturbation theorem show that pi +/- epsilon h_s are distinct valid functions for some epsilon>0. Existence of epsilon is enough for the decision problem; no q-long certificate is output.

**Non-extreme => nonzero compressed kernel, when every orbit is covered.** Write pi=(pi^+ + pi^-)/2 for arbitrary distinct valid competitors. Minimality makes the competitors minimal. BHK Theorem 2.9 makes them Lipschitz continuous because the continuous PL pi has bounded local slopes at the origin. Direct coverage and propagation make h=(pi^+-pi^-)/2 affine on every q cell, with a common slope on each H orbit. Global continuity, h(0)=0 and periodicity then imply h=h_s for those slopes. It obeys every active coarse equation. If its slope vector were zero, continuity and h(0)=0 would force h=0, a contradiction.

**An uncovered orbit => non-extreme.** This is the exact fine-grid uncovered-component theorem discussed in Section 2. The coarse presentation must use every additive coarse edge; omitting some is safe only for a sufficient positive certificate, not for this full decision equivalence.

## 7. Bit complexity and output caveats

- Arrangement enumeration and all exact sign/equality tests have polynomial bit complexity in sparse rational input size.
- There are polynomially many interval pairings, weight pieces, seed coordinates and prefix coordinates.
- q, all pairing endpoints, all prefix counts, and all accumulated nonnegative orbit weights have polynomial bit length.
- Weighted AHT therefore has polynomial bit complexity in this instance. It is not necessary to know a small explicit exponent to establish membership in P.
- In the all-covered case the number of orbits is polynomial. Uncovered orbits are handled in grouped output, not expanded.
- Exact integer matrix rank has polynomial bit complexity.
- The algorithm decides extremality. A conventional explicitly tabulated q-grid non-extremality witness could still have exponential output size, which does not contradict this decision bound.

## 8. Remaining audit work

The proof imports the published weighted AHT theorem, not a newly implemented variant. An independent audit should check the interface details, especially its grouped output and bit-size interpretation. It should also scrutinize the exactness argument for replacing all fine-grid additive edges by the sparse arrangement edges, and the separate continuity use in Section 6.

No unrestricted discontinuous theorem follows from this note. An extension must handle independent values and jumps on fine-grid points; setting them to zero without proof would restrict the valid competitors illegitimately.

## 9. Finite-size validation performed

The accompanying `test_continuous_reduction.py` uses exact rational coarse geometry, a dense union-find substitute for the proposed AHT interface, and exact integer matrix rank. Its reference is the standard 4q-grid continuous extremality system. This tests the reduction, not the polynomial-time AHT implementation.

- 70 rational minimal inputs, q=3 through 16, including finite-group LP vertices and convex averages: every compressed decision agreed with the 4q reference. All 38 covered cases had matching nullity (zero); 32 uncovered cases were non-extreme in the reference. Results: `CONTINUOUS_TEST_RESULTS.json`.
- A separate all-covered but non-extreme example has q=9, f=1/9 and values at k/9 equal to (0, 1, 11/16, 3/8, 13/16, 1/2, 3/16, 5/8, 5/16). After removing collinear breakpoints, seven listed breakpoints remain. The compressed system has three component-slope variables, rank two, and nullity one; the 36-grid reference also has nullity one. Results: `COVERED_NONEXTREME_TEST.json`.

These finite tests do not establish the theorem or its bit complexity. They do exercise the two different rejection branches and the case in which all coverage is present but a genuine finite-dimensional perturbation remains.
