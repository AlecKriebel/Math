# Independent audit: generalized hive integral-point obstruction

This AI-assisted, unrefereed edition records an internal AI mathematical audit. Acceptance means the explicit counterexamples and their stated scope passed that audit; it is not external human peer review or formal proof-assistant certification. The complete hand-checkable inequalities are part of the authored proof. This is a written proof/correction/audit edition, not a computational reproduction package. Source inspection and exact certificate verification occurred in the preceding investigation on 11 October 2026; editorial preparation authenticated retained bytes without a fresh scholarly-source inspection or mathematical-program rerun.

## Verdict

**PASS, with a precisely limited theorem-level conclusion.** The pinned r=7 instance is a nonempty generalized hive polytope with integral boundary values and integral rhombus bounds, but no integral point. Its designated coordinate is forced to equal 1/2 at every feasible real point. This disproves the arbitrary-integral-right-hand-side integral-point assertion, not merely an assertion about all vertices being integral.

The pinned r=6 instance independently passes the same checks. It contradicts the explicit generalized integral-vertex conclusion of De Loera–McAllister's published Theorem 4.6 when the displayed primitive hive matrices and the paper's definition of a generalized hive polytope are used. It also rules out a unimodular **conical cover** of that matrix's columns. The r=7 instance alone is outside the theorem's stated small-size range.

The source conflict is real under those definitions. No discrepancy in rhombus orientation, triangular indexing, nonnegativity, zero-boundary normalization, or slack integrality was found. This audit does **not** identify an error in the authors' computational implementation, claim historical priority, establish a corrected maximum valid rank, or decide a separately interpreted affine convex-hull triangulation claim. Standard Littlewood–Richardson saturation, which has zero rhombus right-hand sides and its prescribed boundary data, is not challenged.

At the time of the original audit, no publication had been performed. No candidate-generation code, candidate-verification code, scholarly author code, or numerical solver was executed by the auditor.

## 1. Inputs and independent work

The closed candidate manifest has SHA-256
`d91023283208e09a0f3e32535f5b4ff7b9a868c23eb7ead10f7c8883b00da83d`.
All 20 listed members also match.

Exact audited certificate inputs:

| Input | Bytes | SHA-256 |
|---|---:|---|
| certificate_r6.json | 17643 | 50dce88518e72cd6a469e3e502176a006d355d6f50d33977d6a77980dc79335f |
| certificate_r7.json | 28875 | f3247f80e59069121350be920116431b67d65edddebd74f6b49cbc15a3695c64 |

The independent verifier is `independent_verify.py`. It uses only Python's standard library, exact integers, and rational numbers. It reconstructs elementary triangles and their adjacency in three-dimensional Euclidean coordinates, instead of using the candidate verifier's diagonal-enumeration method. It then separately checks the published indexed formulas against the geometric reconstruction and the JSON matrix.

Normal, `-O`, and `-OO` executions all pass, producing identical verification receipts. Each execution rejects nine deliberately corrupted inputs per rank: changed matrix, integer bound, fractional bound, witness, boundary index, negative dual weight, changed nonnegative dual weight, target, and direction. Validation uses explicit exceptions rather than assertions, so optimization cannot remove guards. Source text and page images retained during inspection are excluded from this edition. The original audit manifest lists 14 selected members; it is not a complete retained-directory inventory. A later external inventory separately authenticates all 23 retained files: the selected 14, their manifest, five excluded copied-source files and three excluded interpreter caches. This does not expand distribution permission. Only the eight authored prose/public-metadata files identified by this edition’s MANIFEST.json are distributed; raw certificates, checker code, receipts and retained source bodies are excluded.

## 2. Genuine rhombi, signs, and complete indexing

Let

H_r = {(i,j,k) in Z_{≥0}^3 : i+j+k=r}.

Order its points lexicographically. Its boundary consists of points with at least one zero coordinate; B is their coordinate projection. There are (r+1)(r+2)/2 points and 3r boundary points.

View H_r in the Euclidean plane i+j+k=r in R^3. Two points are adjacent exactly when their squared Euclidean distance is 2. The elementary triangles are the triples whose three edges are adjacent. There are r^2 such triangles. Every interior edge is shared by exactly two triangles. Their union is one elementary rhombus: the common edge is its short diagonal (squared length 2), and the two remaining vertices form its long diagonal (squared length 6). Assign coefficient -1 to each short-diagonal endpoint and +1 to each long-diagonal endpoint. The standard inequality is long-diagonal sum minus short-diagonal sum ≤ 0.

This reconstructs exactly 3r(r-1)/2 distinct rows, with no omissions or duplicates. These rows agree one-for-one with the following three indexed formulas for i,j≥1 and i+j+k=r:

R1(i,j,k)h = h(i,j-1,k+1)+h(i-1,j+1,k)-h(i,j,k)-h(i-1,j,k+1).

R2(i,j,k)h = h(i,j,k)+h(i-1,j-1,k+2)-h(i,j-1,k+1)-h(i-1,j,k+1).

R3(i,j,k)h = h(i+1,j-1,k)+h(i-1,j,k+1)-h(i,j,k)-h(i,j-1,k+1).

The certificate orders triples lexicographically and emits types 1,2,3 for each triple. At r=6 the counts are 28 points, 18 boundary points, 10 interior points, 36 triangles, and 45 rhombi. At r=7 they are 36,21,15,49,63.

## 3. Feasibility and all right-hand sides

Both instances have every boundary value equal to zero. Set h*=1/2 on the following four points, and h*=0 everywhere else:

- r=6: (1,1,4), (1,3,2), (2,1,3), (2,3,1)
- r=7: (1,4,2), (1,5,1), (2,1,4), (2,2,3)

For each rhombus row t, define the bound C_t = ceil(R_t h*). This is a complete exact specification of integral right-hand sides and makes Rh*≤C immediate. Direct rational verification gives:

| r | Bounds -1 / 0 / 1 | Slacks 0 / 1/2 |
|---|---|---|
| 6 | 2 / 33 / 10 | 24 / 21 |
| 7 | 2 / 50 / 11 | 41 / 22 |

For an explicit listing, the nonzero bounds are below. A label `(t;i,j,k)` means row Rt(i,j,k). Every unlisted bound is zero.

r=6, bound +1:
(2;1,1,4), (1;1,2,3), (2;1,3,2), (1;1,4,1),
(1;2,2,2), (1;2,4,0), (3;3,1,2), (1;3,2,1),
(2;3,2,1), (3;3,3,0).

r=6, bound -1: (1;2,1,3), (1;2,3,1).

r=7, bound +1:
(3;1,2,4), (3;1,3,3), (2;1,4,2), (1;1,6,0),
(2;2,1,4), (1;2,3,2), (3;2,4,1), (3;2,5,0),
(3;3,1,3), (3;3,2,2), (2;3,3,1).

r=7, bound -1: (3;1,5,1), (3;2,2,3).

The witnesses and their slacks are nonnegative. Thus they also yield nonnegative solutions of M(h,s)=(0,C), where M=[B 0; R I] and s=C-Rh. Their reality and their nonnegativity are proved exactly; integer infeasibility is not inferred from a solver's message.

## 4. Human-checkable r=7 obstruction

Write the 15 interior coordinates as a,b,c,d,e,f,g,h,i,j,k,l,m,n,o at

(1,1,5), (1,2,4), (1,3,3), (1,4,2), (1,5,1),
(2,1,4), (2,2,3), (2,3,2), (2,4,1),
(3,1,3), (3,2,2), (3,3,1), (4,1,2), (4,2,1), (5,1,1).

Here the lowercase c is a coordinate; C remains the bound vector.

For a lower bound on d, add these six inequalities, each once:

| Row | Inequality |
|---|---|
| R2(1,5,1) | e-d ≤ 0 |
| R3(1,5,1) | i-d-e ≤ -1 |
| R1(3,4,0) | l-i ≤ 0 |
| R1(4,3,0) | n-l ≤ 0 |
| R1(5,2,0) | o-n ≤ 0 |
| R1(6,1,0) | -o ≤ 0 |

Their sum is -2d≤-1.

For an upper bound, use the nonnegative weights below:

| Row | Inequality | Weight |
|---|---|---:|
| R2(1,1,5) | a ≤ 0 | 1 |
| R2(1,2,4) | b-a ≤ 0 | 1 |
| R2(1,3,3) | c-b ≤ 0 | 1 |
| R1(2,2,3) | c+f-b-g ≤ 0 | 1 |
| R3(2,2,3) | b+j-f-g ≤ -1 | 1 |
| R1(2,3,2) | d+g-c-h ≤ 1 | 2 |
| R3(3,3,1) | h+n-k-l ≤ 0 | 2 |
| R2(4,1,2) | m-j ≤ 0 | 1 |
| R3(4,2,1) | k+o-m-n ≤ 0 | 2 |
| R3(4,3,0) | l-n ≤ 0 | 2 |
| R3(5,1,1) | m-o ≤ 0 | 1 |
| R3(5,2,0) | n-o ≤ 0 | 2 |
| R3(6,1,0) | o ≤ 0 | 1 |

The weighted sum is 2d≤1. Consequently h(1,4,2)=d=1/2 in every feasible point. An integer point is impossible.

## 5. Human-checkable r=6 obstruction

Write a,b,c,d,e,f,g,h,i,j for the 10 interior coordinates at

(1,1,4), (1,2,3), (1,3,2), (1,4,1), (2,1,3),
(2,2,2), (2,3,1), (3,1,2), (3,2,1), (4,1,1).

The specified witness has a=c=e=g=1/2 and all other coordinates zero. As in Section 3, the complete bound vector is integral and this witness is feasible.

First use the following eight rows, with weight 2 only on the indicated row and weight 1 on every other row:

| Row | Inequality | Weight |
|---|---|---:|
| R3(1,4,1) | g-c-d ≤ 0 | 1 |
| R1(1,5,0) | d ≤ 0 | 1 |
| R1(2,1,3) | b-a-e ≤ -1 | 1 |
| R2(2,1,3) | e-a ≤ 0 | 2 |
| R2(2,2,2) | a+f-b-e ≤ 0 | 1 |
| R3(2,3,1) | c+i-f-g ≤ 0 | 1 |
| R1(4,2,0) | j-i ≤ 0 | 1 |
| R1(5,1,0) | -j ≤ 0 | 1 |

Their weighted sum is -2a≤-1.

For the reverse bound, use these nine rows:

| Row | Inequality | Weight |
|---|---|---:|
| R3(2,1,3) | a-e ≤ 0 | 2 |
| R1(2,2,2) | c+e-b-f ≤ 1 | 2 |
| R1(2,3,1) | d+f-c-g ≤ -1 | 1 |
| R2(2,3,1) | b+g-c-f ≤ 0 | 2 |
| R2(2,4,0) | c-d-g ≤ 0 | 1 |
| R3(3,2,1) | f+j-h-i ≤ 0 | 3 |
| R3(4,1,1) | h-j ≤ 0 | 3 |
| R3(4,2,0) | i-j ≤ 0 | 3 |
| R3(5,1,0) | j ≤ 0 | 3 |

Their weighted sum is 2a≤1. Hence h(1,1,4)=a=1/2 at every feasible real point. This is an exact obstruction to any integral point at triangular side parameter r=6.

Both arguments permit unrestricted real interior coordinates. Nonnegativity is needed only to place the already feasible witnesses directly in the paper's augmented formulation; it is not used to exclude integral points.

## 6. Potential convention loopholes

### Boundary normalization and reduced coordinates

The array has r+1 horizontal levels when its triples sum to r. Therefore the r=6 example has seven levels, consistent with the defining triangular parameter. Relabeling coordinates or rhombus rows has no mathematical effect if the bounds are permuted with them.

Deleting the fixed top coordinate h(0,0,r)=0 is an integral coordinate elimination; restoring it by zero gives exactly the same feasible integer points. Replacing boundary coordinate values by cumulative edge differences together with one anchored value is also an integral change of coordinates. For the examples, all such boundary values and differences are zero.

Even if all boundary differences are specified as zero but the common boundary level t is left free, the obstruction survives. Every boundary value is then t. Since each row of R sums to zero, subtracting t from every entry produces the zero-boundary instance. If the original array were integral, its boundary value t would be integral, so subtraction would preserve integrality, contradicting the certificate. Thus leaving the constant direction unanchored does not restore an integer point.

This reasoning concerns the ordinary boundary values or connected boundary-difference encodings. It does not endorse arbitrary non-unimodular transformations, arbitrary rescaling of primitive inequalities, or arbitrary matrices of the same dimensions.

### Nonnegative versus unrestricted arrays; slack variables

For fixed b,C, projection maps Q={(h,s)≥0: Bh=b, Rh+s=C} bijectively to the nonnegative part of P={h: Bh=b, Rh≤C}. It need not map onto all of P. We do not assume that it does. Our witness h* is nonnegative and its uniquely determined slack s=C-Rh* is nonnegative, so Q is nonempty directly.

For integer h, integer R and C force s=C-Rh to be integer. Therefore there is no missing slack-integrality assumption: any integer point of P with h≥0 would automatically give an integer point of Q. Conversely an integer point of Q has integer h. Since the certificates exclude every integer h in P, they exclude integer points of Q under either interpretation.

Nor does a proper column-lattice restriction remove these right-hand sides. Select from M the boundary h columns and all slack columns. In the corresponding row/column order, this square submatrix is [I 0; R_boundary I], of determinant 1. Thus M's integer column lattice is the full ambient lattice. The right-hand side is also in its nonnegative real cone, by the displayed witness.

### Negative bounds and boundedness

Set q(i,j,k)=i^2+j^2+k^2. Direct substitution gives Rq=2 for every primitive rhombus row, as independently checked. Translation h↦h+q sends the example to integral boundary Bq and bound C+2. Every boundary value and every bound in this translated instance is strictly positive, and h*+q is positive. Integral points translate bijectively. Its forced coordinate is 43/2 for r=7 and 37/2 for r=6. Hence negative components of C or nonnegative coordinates cannot explain away the obstruction.

These are genuine bounded polyhedra. To see this without a solver, a recession array u has zero boundary and Ru≤0. Write U(i,j)=u(i,j,r-i-j). Summing R2(p,q,r-p-q)≤0 over 1≤p≤i and 1≤q≤j telescopes to U(i,j)≤0. The rectangle lies in the triangle because p+q≤i+j≤r. On the other hand, adding R1(i,j,k) and R3(i,j,k) gives

u(i-1,j+1,k)+u(i+1,j-1,k)≤2u(i,j,k).

For each fixed k this is discrete concavity on a segment whose endpoint values are zero, so all its values are nonnegative. Therefore u=0. Every nonempty fixed-boundary fiber is bounded; the obstruction is not caused by calling an unbounded object a polytope.

## 7. Source findings and exact conflict

The original report [1], printed p.2073/PDF p.7, proposes arbitrary integral boundary and rhombus right-hand sides and reports small-size computational verification. The later paper [2], Definition 2.2, defines triples summing to r and the three primitive inequalities checked above. Definition 4.2 uses nonnegative augmented variables and arbitrary integral right-hand sides. Corollary 4.4 concerns unimodular covers; Conjecture 4.5 includes existence of an integral vertex in every nonempty generalized fiber. Its Theorem 4.6 says: “Conjecture 4.5 is true for r ≤ 6.” The arXiv version [3] has the same bound. The published example is labeled r=4, correcting its earlier r=5 label.

These facts were checked from retained PDFs and, for the published definitions and theorem, by visual page inspection. No additional partition, dominance, positivity, or zero-rhombus-RHS condition is stated for the generalized fiber. Those extra conditions belong to the special standard hive family. This paragraph describes the inspected text, not an audit of historical computations.

The r=6 certificate satisfies the generalized fiber's actual displayed conditions. It follows directly that the asserted integral-vertex consequence is false for those matrices: there is not even an integral point. If cone(M) were covered by cones on determinant-±1 maximal column submatrices, an integral right-hand side in one such cone would have nonnegative integral coefficients in that basis. This would give an integer point, a contradiction. Thus such a conical unimodular cover, and a fortiori such a conical unimodular triangulation, is impossible.

### Separate affine-triangulation caution

An affine unimodular triangulation of conv(columns M) is a different statement from a conical cover by determinant-±1 column bases. It should not be silently substituted for the latter. For this M the columns do not all have affine height one: a functional equal to one on every slack column must have coefficient one on every rhombus row. On an interior h column its value is then the sum of that column of R, which in these examples is -2, -1, or 0, never 1. Boundary-row coefficients cannot change its value there.

As a general elementary warning, the segment conv{2,3} has an affine unimodular triangulation, but the nonnegative integer semigroup generated by 2 and 3 misses the integer 1 in its real cone. This audit consequently makes no standalone verdict about an affine convex-hull triangulation interpretation. The explicit integral-vertex conclusion and the conical-cover assertion are already settled by the exact witnesses and dual sums. The difference between these triangulation notions is not asserted to be the cause of the historical discrepancy.

## 8. Static review of the generator and limits

The pinned `make_certificate.py` was read, not run. It proposes dual coefficients using floating-point linear programming and rational reconstruction. Its sign convention is consistent: minimizing minus the requested coordinate direction with inequalities Ax≤C gives nonpositive inequality marginals, whose negatives are nonnegative dual weights. It scales them to integers and checks coefficient cancellation and the right-hand side exactly.

Those generator checks use Python assertions and only target the supplied reduced system. They are not sufficient on their own as an independent mathematical audit, and assertions disappear under optimized Python. This audit instead verifies the complete geometry, integral inputs, feasible witness, and weighted identities from frozen data with an independently authored, optimization-safe checker. No numerical status, including the JSON's stored MILP message, is used as evidence of integer infeasibility.

The generator hardcodes denominator 2, correctly for these two pinned inputs. This observation is not a correctness claim for arbitrary future inputs or a reason to modify a closed candidate packet.

A bounded public search for a correction or earlier obstruction found the primary paper and related literature but no verified erratum resolving this exact conflict. This is not an exhaustive novelty search. Acceptance here is mathematical acceptance of the stated explicit counterexamples and their exact scope, not historical or bibliographic priority.

## References

[1] T. B. McAllister (joint work with J. De Loera), “Two Conjectured Generalizations of the Saturation Theorem,” Oberwolfach Report 39/2004, contribution pp.2072–2073. https://ems.press/content/serial-article-files/45962?nt=1

[2] J. A. De Loera and T. B. McAllister, “On the Computation of Clebsch–Gordan Coefficients and the Dilation Effect,” Experimental Mathematics 15(1) (2006), 7–19. DOI: 10.1080/10586458.2006.10128948. Published PDF: https://www.maths.tcd.ie/EMIS/journals/EM/expmath/volumes/15/15.1/DeLoera.pdf . Definition 2.2: printed p.9/PDF p.3. Definition 4.2: printed p.14/PDF p.8. Corollary 4.4, Conjecture 4.5, Theorem 4.6: printed p.15/PDF p.9.

[3] The same authors and title, arXiv:math/0501446v1, 25 January 2005. https://arxiv.org/abs/math/0501446 . Definition 2.2: PDF p.4; generalized formulation: p.12; conjecture and theorem: p.14.
