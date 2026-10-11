# Exact counterexamples for generalized hive right-hand sides

This AI-assisted, unrefereed edition records an internal AI mathematical audit. Acceptance means the explicit counterexamples and their stated scope passed that audit; it is not external human peer review or formal proof-assistant certification. The complete hand-checkable inequalities are part of the authored proof. This is a written proof/correction/audit edition, not a computational reproduction package. Source inspection and exact certificate verification occurred in the preceding investigation on 11 October 2026; editorial preparation authenticated retained bytes without a fresh scholarly-source inspection or mathematical-program rerun.

Editorial acceptance note: the candidate report below originally required a separate audit. That subsequent audit has now accepted both the r=6 and r=7 exact integral-point counterexamples. Its full report is [AUDIT.md](AUDIT.md), and its complete r=6 proof and convention safeguards are included as supplements below. The original pending-review language is retained to distinguish the historical candidate status from the later audit decision. The source conflict concerns the explicit integral-vertex conclusion under the displayed primitive definitions; no historical computational error or priority is diagnosed. Standard Littlewood–Richardson saturation is unaffected.

## Result and acceptance boundary

For the primitive hive boundary and rhombus matrices specified below, the arbitrary-integral-right-hand-side integral-point assertion is false. At triangular side parameter r=7, take zero boundary values and the integer rhombus bounds described in Section 3. A feasible rational labeling exists, but every feasible real labeling has h(1,4,2)=1/2. Therefore there is no integral labeling.

This is an obstruction to the existence of **any** integer point, not merely a nonintegral vertex. The argument is an exact addition of rhombus inequalities and does not rely on a solver's infeasibility report. The certificate was also checked against an independently generated geometric list of all elementary rhombi.

**Review status:** independently authored candidate proof; separate independent mathematical audit is still required before acceptance. There is an important source discrepancy: an auxiliary r=6 certificate conflicts with the literal small-r conclusion of De Loera–McAllister's Theorem 4.6 under the very same displayed matrix convention. The discrepancy is documented rather than concealed or explained away. This report does not claim to identify the error in the authors' computations or to establish historical novelty.

## 1. The exact matrices and normalization

Let

H_r = {(i,j,k) in Z_{≥0}^3 : i+j+k=r}.

Coordinates are ordered first by increasing i, then increasing j. The boundary is the set with min(i,j,k)=0. It has 3r coordinates for r>0. B is coordinate projection onto this boundary, in the inherited order. Thus B has 3r rows and n=(r+1)(r+2)/2 columns. Boundary values include the top vertex (0,0,r); no additional nonnegativity or hidden normalization is imposed on the real variable h. In this example Bh=0, so the usual top-vertex normalization is satisfied.

For every (i,j,k) in H_r with i,j≥1, take the following three row functionals, in the order written:

R_1(i,j,k)h = h(i,j-1,k+1)+h(i-1,j+1,k)-h(i,j,k)-h(i-1,j,k+1).

R_2(i,j,k)h = h(i,j,k)+h(i-1,j-1,k+2)-h(i,j-1,k+1)-h(i-1,j,k+1).

R_3(i,j,k)h = h(i+1,j-1,k)+h(i-1,j,k+1)-h(i,j,k)-h(i,j-1,k+1).

R is the matrix of these m=3r(r-1)/2 primitive rows. The standard hive inequalities are Rh≤0. These are exactly the three formulas in Definition 2.2 of [DM05, DM06], with the short-diagonal entries subtracted from the long-diagonal entries.

Independent geometric check: embed a point (i,j,k) as (x,y)=(j-i,i+j), with physical squared distance x^2+3y^2. Every elementary rhombus has perpendicular diagonals with squared lengths 12 and 4 and the same midpoint. Enumerate these diagonal pairs and assign +1 to long-diagonal endpoints and -1 to short-diagonal endpoints. This generates exactly the same 63 rows at r=7 and 45 rows at r=6, without using the source's index formulas.

Permuting boundary coordinates or rhombus rows only permutes the corresponding right-hand sides. Normalized boundary-difference encodings are related to the boundary-coordinate encoding by integral changes of boundary coordinates: all boundary differences and the top value are zero here. We do not replace these hive matrices by arbitrary integer matrices of matching dimensions.

## 2. The nonnegative augmented convention and prior claims

Write

P(b,c) = {h in R^n : Bh=b, Rh≤c},

and

Q(b,c) = {(h,s) in R_{≥0}^{n+m} : Bh=b, Rh+s=c}.

The latter is the generalized hive polytope of Definition 4.2 in [DM05, DM06]. For fixed b,c, projection identifies Q(b,c) with P(b,c) intersected with the nonnegative orthant, **not automatically with all of P(b,c)**. Adding slack alone does not justify h≥0 for arbitrary generalized right-hand sides.

There is nevertheless a rigorous one-way transfer for the integral-point assertion. Every row of R sums to zero, so R1=0. If P(b,c) has a feasible h*, choose an integer K such that h*+K1≥0. Then Q(b+KB1,c) is nonempty. If every nonempty nonnegative Q at this r has an integer point, such a point (u,s) gives the integer point u-K1 in P(b,c). The change in boundary data remains integral. Thus the universal nonnegative integral-point assertion implies the unrestricted-real assertion at the same r. This argument does not identify the two polyhedra, does not assert the converse, and does not transfer a vertex claim through an orthant cut.

Conjecture 4.5 in [DM05, DM06] asserts a unimodular triangulation and concludes that every nonempty generalized nonnegative hive polytope has an integer vertex. Theorem 4.6 reports this for r≤6, using TOPCOM placing triangulations. These are source claims, not a fresh result of this investigation. If the stated matrix and parameter conventions are the ones frozen above, the transfer just proved would imply the unrestricted integral-point assertion for r≤6.

The r=7 obstruction below already lies in the nonnegative orthant. Its slack vector c-Rh* is nonnegative. Consequently it also obstructs the conclusion about all nonnegative generalized hive polytopes at r=7. No equivalence of free and nonnegative formulations is assumed to reach this conclusion.

An additional independently checkable r=6 certificate is included. It uses h*=1/2 at (1,1,4), (1,3,2), (2,1,3), and (2,3,1), zero elsewhere, again c=ceil(Rh*), and forces h(1,1,4)=1/2. Hence the literal r≤6 source statement and these exact formulas/certificates cannot all be valid together. The arXiv version mislabels its five-row example as r=5, but the published version corrects that example to r=4 while retaining Theorem 4.6. This visible correction does **not** establish a different convention for the theorem and does **not** resolve the conflict. No author implementation or triangulation data was executed or used to conjecture an explanation. The cause of the source discrepancy remains unresolved.

## 3. Complete r=7 instance

There are n=36 hive coordinates, 21 boundary coordinates, and 63 rhombus rows. Set b=0. Define h* by

h*(1,4,2)=h*(1,5,1)=h*(2,1,4)=h*(2,2,3)=1/2,

and h*=0 at every other point of H_7. Set c_t=ceil((Rh*)_t) for every row t. This completely specifies an integer vector c, and immediately proves real feasibility.

For a directly listed specification, the only nonzero entries of c are:

| row type | (i,j,k) | bound c |
|---|---|---:|
| 3 | (1,2,4) | 1 |
| 3 | (1,3,3) | 1 |
| 2 | (1,4,2) | 1 |
| 3 | (1,5,1) | -1 |
| 1 | (1,6,0) | 1 |
| 2 | (2,1,4) | 1 |
| 3 | (2,2,3) | -1 |
| 1 | (2,3,2) | 1 |
| 3 | (2,4,1) | 1 |
| 3 | (2,5,0) | 1 |
| 3 | (3,1,3) | 1 |
| 3 | (3,2,2) | 1 |
| 2 | (3,3,1) | 1 |

All other 50 rhombus bounds are zero. The construction uses arbitrary integral right-hand sides as asked; it is not a standard c=0 saturation instance.

## 4. Human-checkable proof that every feasible point has a half-integral coordinate

After setting boundary coordinates to zero, denote the 15 interior coordinates, in order, by

(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o)

at

((1,1,5),(1,2,4),(1,3,3),(1,4,2),(1,5,1),
 (2,1,4),(2,2,3),(2,3,2),(2,4,1),
 (3,1,3),(3,2,2),(3,3,1),(4,1,2),(4,2,1),(5,1,1)).

Here the scalar c is an interior-coordinate label only within this section; the right-hand-side vector is referred to as the vector of bounds.

First, the following six rhombus inequalities hold:

| source row | inequality |
|---|---|
| R_2(1,5,1) | e-d ≤ 0 |
| R_3(1,5,1) | i-d-e ≤ -1 |
| R_1(3,4,0) | l-i ≤ 0 |
| R_1(4,3,0) | n-l ≤ 0 |
| R_1(5,2,0) | o-n ≤ 0 |
| R_1(6,1,0) | -o ≤ 0 |

Adding gives -2d≤-1, hence d≥1/2.

For the opposite inequality, add the following rows with the indicated nonnegative integer weights:

| source row | inequality | weight |
|---|---|---:|
| R_2(1,1,5) | a ≤ 0 | 1 |
| R_2(1,2,4) | b-a ≤ 0 | 1 |
| R_2(1,3,3) | c-b ≤ 0 | 1 |
| R_1(2,2,3) | c+f-b-g ≤ 0 | 1 |
| R_3(2,2,3) | b+j-f-g ≤ -1 | 1 |
| R_1(2,3,2) | d+g-c-h ≤ 1 | 2 |
| R_3(3,3,1) | h+n-k-l ≤ 0 | 2 |
| R_2(4,1,2) | m-j ≤ 0 | 1 |
| R_3(4,2,1) | k+o-m-n ≤ 0 | 2 |
| R_3(4,3,0) | l-n ≤ 0 | 2 |
| R_3(5,1,1) | m-o ≤ 0 | 1 |
| R_3(5,2,0) | n-o ≤ 0 | 2 |
| R_3(6,1,0) | o ≤ 0 | 1 |

All variables except d cancel; the sum is 2d≤1. Thus d=1/2. In particular, P(0,c) has no integer point. This concludes the exact obstruction proof.

Equivalently, letting A be the submatrix of R on interior columns, the two certificate vectors λ_-,λ_+ are nonnegative integers and satisfy

λ_- A=-2e_d,  λ_- c=-1;
λ_+ A= 2e_d,  λ_+ c= 1.

The JSON certificate records every matrix row, point, bound, and weight. The verifier recalculates all these identities using integer arithmetic.

## 5. Further convention robustness

The obstruction is not dependent on allowing negative coordinates in h. The exhibited feasible h* is already nonnegative, and an integer point in the augmented polytope would project to an integer point in the free polytope, which the proof excludes.

Nor is it necessary to retain negative components of the right-hand side. Let q(i,j,k)=i^2+j^2+k^2. Direct substitution in each of the three formulas gives Rq=2·1. Translation by the integral array q maps this example to

Bh=Bq, Rh≤c+2·1.

All boundary values and all rhombus bounds in this translated example are positive; h*+q is positive. An integral point would translate back to an integral point of the original example. The forced coordinate becomes h(1,4,2)=43/2. Thus nonnegativity of the augmented variable or positivity of the right-hand side cannot resolve this counterexample.

## 6. Reproduction, sources, and limits

Historical verification used an independently authored standard-library Python certificate checker, which is not distributed in this prose edition. The historical checker needed only the Python standard library. It checks both r=7 and the source-discrepancy r=6 instance. In particular it verifies the actual triangular grid, all boundary coordinates, all row formulas, the independent geometric rhombus enumeration, the exact ceil construction, real feasibility, and both integer weighted-sum identities. There is no solver dependence in the proof check.

The exploration used independently authored Python code and SciPy 1.17.0/HiGHS to search half-grid labelings and propose dual weights; SymPy 1.14.0 was used for an exploratory active-row rank calculation. Floating-point search output is not a certificate and is not used as an inference in the proof. The first r=7 candidate was encountered after testing half-grid bit patterns 0 through 120. An auxiliary check found the r=6 pattern 85. Exhaustion of half-grid patterns at r=3,4,5 found no obstruction, but that is neither a theorem for all right-hand sides nor a novelty claim.

Primary references:

[OWR04] Tyrrell B. McAllister, joint work with J. De Loera, “Two Conjectured Generalizations of the Saturation Theorem,” Oberwolfach Report 39/2004, contribution starting printed p. 2072. The displayed generalized problem and associated conjecture are on printed p. 2073, PDF p. 7. https://ems.press/content/serial-article-files/45962?nt=1 . The preceding saturation sentence literally says “nonintegral vertex”; its conflict with the surrounding discussion is retained as a source typo, not used to redefine the target.

[DM05] Jesús A. De Loera and Tyrrell B. McAllister, “On the Computation of Clebsch–Gordan Coefficients and the Dilation Effect,” arXiv:math/0501446v1, 25 January 2005. Definition 2.2 on PDF p. 4; nonnegative generalized formulation on p. 12; Conjecture 4.5 and Theorem 4.6 on p. 14. https://arxiv.org/abs/math/0501446 . The typeset October 3, 2018 date is not evidence of a new 2018 result.

[DM06] The published version, Experimental Mathematics 15(1) (2006), pp. 7–19, DOI 10.1080/10586458.2006.10128948. Definition 2.2 on printed p. 9/PDF p. 3; Section 4.1 on printed p. 14/PDF p. 8; Conjecture 4.5 and Theorem 4.6 on printed p. 15/PDF p. 9. Retrieved from the Trinity College Dublin EMIS mirror: https://www.maths.tcd.ie/EMIS/journals/EM/expmath/volumes/15/15.1/DeLoera.pdf . This independently available primary copy was retrieved successfully, without bypassing the earlier Kyoto-host restriction.

A bounded public search did not locate an erratum resolving the small-r discrepancy. That is not proof that no correction or prior counterexample exists. The exact counterexample is supplied for mathematical review; no claim of precedence is made.

## Accepted audit supplements

The following material comes from the subsequent independent audit. It supplies the complete r=6 dual-sum proof, both complete bound specifications, boundedness, full column-lattice and boundary/slack arguments, and the precise conical-versus-affine distinction. The original candidate report above is preserved as a historical mathematical report; its pending-review statement is superseded by the accepted audit, while its unresolved historical-source-cause warning remains valid. Section numbers in these retained audit excerpts are the audit’s numbers. References [1]–[3] in these excerpts refer to the audit reference list at the end below.

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

## References

[1] T. B. McAllister (joint work with J. De Loera), “Two Conjectured Generalizations of the Saturation Theorem,” Oberwolfach Report 39/2004, contribution pp.2072–2073. https://ems.press/content/serial-article-files/45962?nt=1

[2] J. A. De Loera and T. B. McAllister, “On the Computation of Clebsch–Gordan Coefficients and the Dilation Effect,” Experimental Mathematics 15(1) (2006), 7–19. DOI: 10.1080/10586458.2006.10128948. Published PDF: https://www.maths.tcd.ie/EMIS/journals/EM/expmath/volumes/15/15.1/DeLoera.pdf . Definition 2.2: printed p.9/PDF p.3. Definition 4.2: printed p.14/PDF p.8. Corollary 4.4, Conjecture 4.5, Theorem 4.6: printed p.15/PDF p.9.

[3] The same authors and title, arXiv:math/0501446v1, 25 January 2005. https://arxiv.org/abs/math/0501446 . Definition 2.2: PDF p.4; generalized formulation: p.12; conjecture and theorem: p.14.
