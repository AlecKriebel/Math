# Source-first reconstruction and effective finite test

This reconstruction was written before reading any candidate, root, family verdict, old review, or historical review artifact. The assignment disclosed problem/PR identity, mechanism names (effective finite-degree Bezout/genus/curve testing), expected reported totals 214070 and 93918, source URLs and frozen head. Those are prior exposure, not independent findings. Literal OWR pages 3295--3297 were fetched, extracted, rendered locally, and inspected before any candidate read. No other researcher's analysis was consulted. Independence is source-fresh and semantic/mechanistic within that disclosed scope, not an unqualified blind audit.

## Exact target and source scope

The target is the complex projective plane with coefficient line bundle O(1): for a reduced arrangement of finitely many distinct projective lines with nonempty finite singular set Z, define r=|Z| and k=max over ALL projective lines ell of |ell intersect Z|. The source conjecture is epsilon(P^2,O(1);Z)=1/k. Curve multiplicities in its denominator are those of the test curve C, not the number of arrangement components through the point. The infimum may be restricted to reduced irreducible curves meeting Z.

Literal source: Tomasz Szemberg's contribution, printed 3295--3297, Conjecture 1 printed 3297, https://ems.press/content/serial-article-files/46833 . The displayed mpl(Z) is explicitly the maximal collinearity count; no restriction to arrangement components is printed. The surrounding contribution discusses the complex plane. Distinct reduced components and nonempty Z are necessary conventions for a finite singular-point Seshadri problem; the one-sentence conjecture does not separately list them. A repeated component treated scheme-theoretically makes the singular locus nonfinite and is outside this interpretation.

OWR report label/year: 53/2019, workshop 10--16 November 2019, submitted 10 November 2019, EMS publication 19 November 2020 (https://ems.press/journals/owr/articles/17296). The report's organizers say on printed 3272 that a workshop method resolved arrangements with at most 12 lines, with a special treatment needed for dual Hesse. This is a historical source assertion, not reproduced here and not a present global-status claim. Bibliographic year and publication date are distinct.

Comparison: Pokora, https://arxiv.org/pdf/1711.09364v3 , Question 3.1 printed page 6 defines s(L)=max over ell IN L of the number of singular points on ell. This component version is stronger than the all-line target unless the maxima are shown equal. The paper says it works exclusively over C. arXiv v1 submitted 26 November 2017, v3 submitted 7 October 2018; displayed manuscript date 9 October 2018; journal reference Rocky Mountain J. Math. 49(3), 963--978 (2019), corroborated by https://arxiv.org/abs/1711.09364 . These dates are not interchangeable.

Comparison: Hanumanthu--Roy--Subramaniam, https://www.cmi.ac.in/~krishna/sc-curve-config.pdf , dated 19 July 2024 in the PDF, Question 1.1 printed page 2 uses maximum points on a line, excludes pencils, and works over C. That exclusion does not invalidate the trivial pencil boundary: at least two distinct concurrent lines have Z={p}, k=1 and epsilon=1 because mult_p(C)<=deg(C), with a line through p attaining equality. A single distinct line has Z empty, so 1/k is undefined and the nonempty-point target excludes it. No precise publication day for the CMI manuscript is inferred from its creation metadata.

## Independent deduction

Let Z be any nonempty finite set of r distinct complex projective points. Let k be its all-line maximum. A maximizing line gives epsilon<=1/k. All degree-one curves have total multiplicity at Z at most k. If equality fails, an irreducible reduced degree-d curve with d>=2 has multiplicities m_i in {0,...,d}, M=sum m_i>=kd+1.

Arithmetic genus and nonnegative geometric genus give

    Q=sum m_i(m_i-1) <= (d-1)(d-2).

This remains valid for arbitrary singularities: their delta-invariants are at least m_i(m_i-1)/2. Additional or infinitely near singularities only consume more genus. The m_i are allowed to be 0 or 1. No assumption that Z comprises singularities of C is made.

For fixed M and r, the minimum Q occurs when m_i differ by at most one. Writing M=qr+s, 0<=s<r, this is

    g_r(M)=r*q*(q-1)+2*q*s.

This integer function is nondecreasing. Consequently Q>=g_r(kd+1)>=(kd+1)^2/r-(kd+1), and every strict counterexample satisfies

    (k^2-r)d^2 + (2k+3r-rk)d + 1-3r <= 0.       (A)

The use of g avoids an unjustified monotonicity substitution in x^2/r-x when x<r/2. If 0<r<k^2, put a=k^2-r, b=2k+3r-rk and c=1-3r. Since a>0 and c<0, all counterexample degrees are at most

    D=floor((-b+sqrt(b^2-4ac))/(2a)).

The bound is exactly computable using the integer square root of b^2-4ac. D<2 immediately proves epsilon=1/k. The stronger integer genus screen g_r(kd+1)<=(d-1)(d-2) can remove more degrees or vectors. This theorem is a finite reduction, not a proof that every arrangement passes its finite tests.

## Exact coordinate and curve decision regime

Given distinct projective coordinates over an explicitly presented exact field K contained in C with decidable equality, compute all pair cross products, normalize/deduplicate, and count point incidence; every maximizing line containing at least two Z points arises from a pair. Handle r=1 separately. This computes k over ALL C-projective lines, not only lines over an assumed list; a line containing two K-points has K-coefficients. Arrangement input may instead be distinct line coefficients over K; pairwise intersections compute Z.

For every 2<=d<=D, enumerate vectors m_i in {0,...,d} with sum m_i=kd+1. Build the homogeneous degree-d coefficient matrix imposing local Taylor coefficients of total order<m_i equal to zero in a chosen affine chart at each point. A nonzero nullspace is equivalent to a polynomial of degree d vanishing to the required orders, since the constraints are linear and rank is invariant under field extension. Gaussian elimination over K is a terminating exact decision. Algebraic coordinates represented by exact number fields or algebraic-number algorithms suffice. Rational coefficients are a special case. Known effectively presented transcendental extensions can also suffice. Algebraicity itself is not logically essential; exact arithmetic and decidable equality are.

It is legitimate to test all polynomials, including reducible/nonreduced ones: if f=product C_j^{e_j} and its total multiplicity exceeds k deg(f), then additivity gives some reduced irreducible component C_j with M_j>k deg(C_j). Conversely an irreducible counterexample has a tested multiplicity subvector of exact sum kd+1. No factorization is needed for yes/no decision, though factoring produces an explicit irreducible witness. Genus may be used to screen vectors for possible irreducible counterexamples, but must not be asserted for arbitrary reducible forms. Enumerating all exact-sum vectors without the genus screen is the simplest complete decision specification.

Merely computable real/complex coordinates supplied by approximation algorithms do NOT give a uniform terminating rank/incidence algorithm: equality to zero is undecidable in that representation. Numerical tolerances may change incidence or rank. Thus an unqualified 'effective complex coordinates' claim needs an exact field presentation or a suitable equality oracle, beyond finite precision or computable approximations.

## Boundary attacks and checkable controls

At r=k^2 the leading coefficient in (A) vanishes. For k>=4 its remaining linear coefficient 2k+3k^2-k^3 is negative, so the inequality places no upper bound on positive degrees. Indeed for r=16,k=4,d=4t,m=(t+1,t,...,t), M=16t+1>4d and Q=16t^2-14t<=(d-1)(d-2) for every t>=1. These are surviving necessary numerical classes, not constructed curves. For small k the equality case can have a cutoff from the remaining linear inequality; r<k^2 is a sufficient uniform regime, not a necessary classification.

The independent standard-library exact program independent_controls.py produces full matrices, row reductions, nullspaces, projective point/pair-line incidences and cutoff values in independent_full_output.json. Controls include an empty single-line singular set; a pencil; a triangle; five distinct rational lines; a nodal cubic with an actual order-two point; a reducible xy form where applying the irreducible degree-two genus inequality would be false; and an arbitrary-point conic countercontrol. The conic control has seven points on x^2-yz=0 and one off it, r=8<k^2=9, k=3, D=2 and a 2/7 curve ratio below 1/3. It prevents accidental generalization of the finite reduction to a universal equality theorem for arbitrary point sets. It is NOT a line-arrangement counterexample. A 2850-case cutoff grid through k=20 checks integer cutoffs against the genus screen, retaining complete output. Each matrix/nullspace is verified by exact multiplication.

No novelty, current-global-open, journal-acceptance or full-conjecture certification is made. The strongest independent result is the finite decision regime under an exact-field hypothesis and r<k^2; the remaining arrangement-level gap is proving that all its finite curve tests are negative (or otherwise proving the inequality) uniformly across arrangements.
