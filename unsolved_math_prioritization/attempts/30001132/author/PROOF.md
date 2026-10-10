# A smooth class with no admissible face

## Scope and conventions

We reconstruct the published negative result using the definition in Kiritchenko, *Gelfand–Zetlin Polytopes and Flag Varieties*, Sections 3.1–3.2 and 5.1–5.3, DOI 10.1093/imrn/rnp223. Her p. 2522 already reports existence of a smooth counterexample. No novelty is claimed for the negative conclusion.

Take G=GL4(C), the upper triangular subgroup B+, and the diagonal torus T. Write permutations as functions in one-line notation; composition ab means a composed with b. Set X_w=closure(B+ w B+/B+), so dim X_w is the inversion number of w. Every Borel containing T has the form B_b=bB+b^-1 for a unique b in S4. The orbit B_b(bwB+) is the translate by b of the usual Schubert cell. It represents the same Schubert cycle as X_w. The same flag variety and orbits can be obtained with SL4: scalar matrices have no effect on complete flags.

Take any strictly increasing integral top row lambda_1<lambda_2<lambda_3<lambda_4. The Gelfand–Zetlin polytope has coordinates x_(r,k), with r=1,2,3 and k=1,...,4-r, together with fixed x_(0,k)=lambda_k. Its inequalities are

x_(r-1,k) <= x_(r,k) <= x_(r-1,k+1).

Kiritchenko associates a face Gamma(v,B) to an extremal-weight vertex v and a Borel B containing T. It is spanned by those edges from v whose root direction belongs to the Lie algebra of B. Admissibility requires Gamma(u,B) to be contained in Gamma(v,B) for every codimension-one boundary orbit O(u,B) of O(v,B). In particular, the predecessor vertex u itself must belong to Gamma(v,B).

This is a condition on the specific orbit-to-face correspondence, not an arbitrary claim that a cohomology class equals a face in a polytope ring. For a fixed B there is exactly one orbit representing each Schubert basis class. Thus the 24 choices b exhaust the representatives relevant here.

## The smooth variety

Let w=2413. Its inversions are (1,3), (2,3), (2,4), so dim X_w=3. Its lower Bruhat covers are

1423, 2143, 2314.

Indeed, each is obtained from w by a transposition of positions and has length 2; testing the six position transpositions gives no further length-two permutation.

Let E_i be the standard coordinate i-plane. The Schubert rank conditions say

dim(F_p intersect E_q) >= #{j<=p : w(j)<=q}.

For this w, these conditions reduce to

F_1 subset E_2 subset F_3.

For completeness, the rank rows for p=1,2,3 at q=1,2,3,4 are respectively (0,1,1,1), (0,1,1,2), and (1,2,2,3). The first containment gives all nonautomatic p=1 and p=2 conditions. The second gives p=3, including E_1 subset F_3. The remaining conditions follow from dimension bounds in C4 and nesting of the flag.

Choose first F_1 in P(E_2), then F_3 among hyperplanes containing E_2, parameterized by P((C4/E_2)^*). These are independent choices, giving a base P1 x P1. Over the base, F_3/F_1 is a rank-two vector bundle, and F_2/F_1 is an arbitrary line in it. Thus X_w is its projectivization, a P1-bundle over P1 x P1. In particular X_w is smooth, projective, irreducible, and three-dimensional. This proves smoothness directly, so inversion, opposite-Borel, and codimension indexing conventions cannot accidentally turn a singular class into the asserted example.

## Exact vertex and face construction

For sigma in S4 define V_sigma row r to be the sorted list of lambda_i with sigma(i)>r, with row 0 the full top row. Each child entry equals exactly one of its two parent entries. The resulting six equalities form disjoint chains, one starting at lambda_i and of length sigma(i). These equations determine the vertex uniquely and are independent: each child is connected upward to a fixed top entry and introduces one new variable. All other inequalities are strict, because the lambdas are distinct. Therefore V_sigma is simple. The source's extremal-weight labeling is p(V_sigma)=sigma lambda, and V_id is the highest-weight vertex.

An edge from V_sigma is obtained by releasing one of the six active equalities. Suppose this equality joins row r-1 to row r and lies in the chain of length j. If it is a left equality x_(r,k)=x_(r-1,k), the released edge increases each entry in the remainder of that chain, one in each row r,...,j-1. Its weight change is a positive multiple of alpha_r+...+alpha_(j-1)=epsilon_r-epsilon_j. For a right equality x_(r,k)=x_(r-1,k+1), these changes are negative, giving epsilon_j-epsilon_r. This also follows directly from the row-sum formula for p: the sum in each row r,...,j-1 changes by the same amount and all other row sums remain fixed.

For B_b the root epsilon_a-epsilon_c is positive exactly when b^-1(a)<b^-1(c). To obtain Gamma(V_sigma,B_b), delete from the vertex equations those whose released root is positive for B_b; retain the others. Simplicity ensures this determines exactly the face spanned by the selected edges, rather than only a superset.

The candidate for the class w with this Borel is Gamma(V_(bw),B_b). For every lower cover u of w, the orbit corresponding to V_(bu) is a codimension-one boundary orbit. If any equation retained for Gamma(V_(bw),B_b) fails at V_(bu), admissibility fails.

## Complete obstruction table

The following table uses x_(r,k) with one-based k and fixed x_(0,k)=lambda_k. Its final column gives the two top-row labels occurring on the left and right sides of the displayed retained equality when evaluated at the predecessor vertex V_(bu). Distinct labels imply distinct values for every strictly increasing lambda. All 24 b appear exactly once.

| b | bw | u | bu | Retained equality | Labels at V_(bu) |
|---|---|---|---|---|---|
| 1234 | 2413 | 1423 | 1423 | x_(2,1)=x_(1,2) | 2, 3 |
| 1243 | 2314 | 1423 | 1324 | x_(2,1)=x_(1,2) | 2, 3 |
| 1324 | 3412 | 1423 | 1432 | x_(3,1)=x_(2,2) | 2, 3 |
| 1342 | 3214 | 1423 | 1234 | x_(2,1)=x_(1,1) | 3, 2 |
| 1423 | 4312 | 1423 | 1342 | x_(3,1)=x_(2,1) | 3, 2 |
| 1432 | 4213 | 1423 | 1243 | x_(2,1)=x_(1,1) | 3, 2 |
| 2134 | 1423 | 1423 | 2413 | x_(1,1)=x_(0,2) | 1, 2 |
| 2143 | 1324 | 1423 | 2314 | x_(1,1)=x_(0,2) | 1, 2 |
| 2314 | 3421 | 1423 | 2431 | x_(3,1)=x_(2,2) | 2, 3 |
| 2341 | 3124 | 2314 | 3421 | x_(2,2)=x_(1,3) | 2, 3 |
| 2413 | 4321 | 1423 | 2341 | x_(3,1)=x_(2,1) | 3, 2 |
| 2431 | 4123 | 2314 | 4321 | x_(2,2)=x_(1,3) | 2, 3 |
| 3124 | 1432 | 1423 | 3412 | x_(1,1)=x_(0,2) | 1, 2 |
| 3142 | 1234 | 1423 | 3214 | x_(1,1)=x_(0,2) | 1, 2 |
| 3214 | 2431 | 1423 | 3421 | x_(2,1)=x_(1,2) | 1, 2 |
| 3241 | 2134 | 2314 | 2431 | x_(3,1)=x_(2,2) | 2, 3 |
| 3412 | 4231 | 2314 | 4132 | x_(1,3)=x_(0,3) | 4, 3 |
| 3421 | 4132 | 2314 | 4231 | x_(2,2)=x_(1,2) | 3, 2 |
| 4123 | 1342 | 1423 | 4312 | x_(1,1)=x_(0,2) | 1, 2 |
| 4132 | 1243 | 1423 | 4213 | x_(1,1)=x_(0,2) | 1, 2 |
| 4213 | 2341 | 1423 | 4321 | x_(2,1)=x_(1,2) | 1, 2 |
| 4231 | 2143 | 2314 | 2341 | x_(3,1)=x_(2,1) | 3, 2 |
| 4312 | 3241 | 2314 | 3142 | x_(1,3)=x_(0,3) | 4, 3 |
| 4321 | 3142 | 2314 | 3241 | x_(2,2)=x_(1,2) | 3, 2 |

For example, b=1234 gives sigma=2413 and predecessor u=1423. The candidate face retains x_(2,1)=x_(1,2), but at V_1423 these coordinates are lambda_2 and lambda_3. Hence V_1423 is outside the candidate. Each remaining row proves precisely the same kind of failure for its own Borel.

Since Gamma(V_(bu),B_b) contains V_(bu), each failed vertex test is already a failed required face inclusion. No unproved implication from vertex inclusion to face inclusion is used. Consequently none of the 24 representatives of the class [X_2413] is admissible. Together with the smoothness proof this disproves the universal assertion.

## Reproducible verification and scope

`verify_faces.py` generates the face equations by the chain diagram described above. Its exact enumeration is a useful control: all classes work for n=2,3, and for n=4 the failures are 2413,3412,4231, agreeing with the published statement of one smooth and two singular failures.

The proof does not require trusting that generator. `certificate.json` contains just the 24 displayed witnesses. `check_certificate.py` rebuilds active inequality matrices and obtains primitive edge directions by exact rational Gaussian elimination. It computes roots from row sums, verifies that each displayed equation is retained, checks the predecessor is a length-one drop, and checks its two coordinate values differ. It neither imports nor invokes the diagram generator. Its check of the eight T-fixed flags satisfying the incidence constraints is an additional finite consistency test; smoothness itself follows from the geometric argument above, not from checking fixed flags.

The argument is not an obstruction to Kogan-face sums, toric degenerations into a union, or single-face equalities in a separate quotient or module. Theorem 4.3 of Kiritchenko–Smirnov–Timorin, *Schubert calculus and Gelfand–Zetlin polytopes*, gives representations by sums in a polytope-ring framework; it does not restore the stronger admissibility statement tested here.
