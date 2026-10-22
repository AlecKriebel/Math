# Independent adversarial audit: rank 697 / 30001599 / OWR-4527-003

Audit date: 2026-10-05 UTC.

## Verdict

PASS for the frozen package as a bounded, **unsolved 5/5 investigation with rigorous partial results**. No mathematical correction to the authored arguments was found. This is not a proof of the universal target, a counterexample, a novelty certification, or a claim that the literature has no complete resolution.

The exact object audited is the eight-file archive FAT_POINTS_30001599_SAFE_FROZEN.zip, SHA-256 23445c65f62d9f1d06c140ec12378aac0ce6f2539303eeadf9e5ce7851e9c526, 17,179 bytes. Its eight members total 37,752 uncompressed bytes and match the frozen directory byte for byte. All seven manifest entries are correct; the manifest itself has SHA-256 675d0e15df109374d34bea061bb54ffc23e70fa87b344f9a2b3fc57acd40dc51. Inputs were compared again after all computations and remained unchanged. No helper was used, and no remote write was performed.

There are five genuinely different approaches, not five restatements of finite tests. Each reaches only the outcome described in the package. Their percentages are subjective author estimates and are not independently measurable proof-completion statistics.

## Target, source and category binding

The target is alpha(I^(n(r-1)+1)) >= r alpha(I)+(r-1)(n-1), for each integer r>=1, for the radical ideal of an arbitrary nonempty finite projective point set. Uniformity refers to the imposed multiplicity, not to a generic-position restriction. Nonempty support and n>=1 are the package's explicit natural conventions.

I independently downloaded the primary OWR report and inspected Cooper's contribution on printed pp. 2625-2626, including a rendered image of p. 2626. The formula and the arbitrary-support quantifier match. That contribution supplies no field assumption. The surrounding workshop contains other speakers' hypotheses, which cannot be silently imported. [OWR primary report](https://ems.press/content/serial-article-files/46305)

I independently downloaded and inspected Cooper–Hartke's version 3, including Section 1.1, Definition 1.17, Theorems 2.10 and 3.4, and a rendered image of p. 16. Section 1.1 explicitly works over an algebraically closed field of characteristic zero. The package correctly labels its differential, star and polar proofs with that scope, rather than claiming that this clarifies every possible interpretation of the unstated original field. [Cooper–Hartke, The Alpha Problem & Line Count Configurations](https://arxiv.org/abs/1312.4147)

The OWR staircase statement has r>=75. The 2014 Theorem 2.10 treats the same staircase family for every r>=1; reversing the enumeration changes (t,...,1) into (1,...,t). Theorem 3.4 extends this to line-count types (c_1,...,c_t) with c_i>=i in nondecreasing order. A line-count configuration here consists of points partitioned among distinct supporting lines, with no support point at an intersection of two of those lines. The update is neither for every line arrangement nor for every configuration having the same reduced Hilbert function. These qualifiers must be retained in any publication summary.

Harbourne–Huneke's Conjecture 4.1.8 matches the numerical target, distinct from the stronger containment conjecture. Corollaries 4.1.7 and 4.1.11 already supply relevant star and asymptotic cases. The fresh version-3 PDF matches the package's hash. [Harbourne–Huneke, Are symbolic powers highly evolved?](https://arxiv.org/abs/1103.5809)

The freshly downloaded Bisui–Nguyen version 2 matches its recorded hash. Its introduction and main results concern Demailly's multiplicity-2 asymptotic inequality with generic/general/very-general restrictions. The publisher confirms online publication on 9 May 2025 and volume 77, pp. 483-500 (2026). This source does not supply the missing arbitrary-support finite-exponent result. [Version 2](https://arxiv.org/abs/2401.11297v2), [publisher record](https://link.springer.com/article/10.1007/s13348-025-00477-9)

## Approach 1: differentiation and containment

Accepted. In characteristic zero, a nonconstant nonzero homogeneous polynomial admits a nonzero partial derivative. Repeating a chosen nonzero derivative t times is legitimate because d>=m+t and the degree never reaches zero prematurely. In a chart at any support point, an ambient partial lowers membership in the point-ideal power by at most one; linear coordinate changes preserve the span of first derivatives. This proves a_(m+t)>=a_m+t.

The resulting deficit is exactly (r-1)(a-1). The r=1, a=1 and projective-line cases are correctly settled. The a=1 and n=1 proofs do not require characteristic zero. The containment I^(nr) subset I^r and the differential inequality at the larger exponent cannot be reversed to obtain the target. A characteristic-2 regression example x^2 rejects transplanting the nonzero-derivative step to arbitrary characteristic.

Dependency: the general a_(m+t) statement relies on characteristic zero. It does not prove the original inequality for arbitrary support once a,r>1.

## Approach 2: Waldschmidt reduction

Accepted. The product inclusion gives subadditivity, and the written quotient-and-remainder proof establishes the limit/infimum relation. Consequently a_m>=m*w. With L=(a+n-1)/n and C=(n-1)(a-1)/n, direct expansion gives B_r=m_r*L+C.

Both the non-strict sufficient threshold w>=B_r/m_r and the strict integer-refined threshold w>(B_r-1)/m_r are correct. The eventual inequalities involving delta>0 are also correct. For n>=2 and a>1, C/m_r decreases strictly with r. Rounding the sole estimate a_m>=m*L settles the target exactly when C<1, equivalent to a<=2 in this range. The deliberate test n=2,a=3,r=2 leaves lower estimate 6 versus target 7 and rejects a spurious rounding proof.

The Demailly parameter is genuinely independent. Substitution placing a_(m_r) on its right-hand side cannot be treated as the desired lower bound on that quantity. The package does not claim that Chudnovsky, Demailly or Nagata resolves the target. The stated Nagata distinction is appropriate.

Dependency: an additional quantitative lower bound for w is missing. The asymptotic argument does not provide it.

## Approach 3: the entire star family

Accepted as a full proof within its stated characteristic-zero scope. The two nested inductions are well founded.

For n=1, a_m=ms follows from the product of distinct point equations. For n>=2, the intersections lying on H_i are exactly the point star of the other s-1 restricted hyperplanes in H_i. The linear-general-position hypotheses descend: any n-1 restricted hyperplanes meet at a single point and no n meet. This remains valid at the endpoint s=n.

The dimension induction gives the lower bound r(s-1)-n+2 at multiplicity (n-1)(r-1)+1. The derivative shift is precisely r-1, so it yields rs-n+1 at the required multiplicity n(r-1)+1. A restriction is either zero or retains at least the ambient vanishing order; it cannot violate that lower bound. Thus every L_i divides F, and the distinct linear factors imply their product Q divides F.

At r=1, deg F<s-n+1<=s contradicts divisibility by Q. At r>=2, exactly n factors of Q vanish at each star point. Local orders of products add, so F/Q has order at least n(r-2)+1. Its degree is below the inductive bound for r-1. This closes the second induction without any circular appeal to the unproved target for arbitrary points.

The product Q^(r-1)G, where G includes s-n+1 of the factors, has degree rs-n+1 and at least the required multiplicity. Hence the equality is proved. Independent controls additionally construct rational stars in projective dimensions 1,2,3,4 from dual Vandermonde hyperplanes and verify nine full-column-rank lower bounds, plus the product incidence counts. These checks supplement the proof; they do not replace induction over unbounded n,s,r.

Dependency: the incidence structure is essential. The proof makes no assertion that arbitrary supports can be placed in this family. Prior star results prevent any novelty inference from reproducing the formula.

## Approach 4: specialization, six-point examples and grids

Accepted. Matrix entries are polynomial in affine point coordinates. Nonzero minors prove a Zariski-open nonexistence assertion, not an assertion at every specialization. The package has the direction right.

The six points S are exactly the pairwise intersections of x=0, y=0, x+y=1 and x+2y=3; no three of these lines meet. A separate rational rank algorithm confirms rank 6 in degree 2 for S and T. Degree-zero and degree-one ranks are 1 and 3. Once affine evaluation is surjective in degree 2 it remains surjective in every higher degree, proving the entire common reduced Hilbert function (1,3,6,6,...), not just a sampled prefix.

Independent rational ranks at the lower test degrees are:

- S: rank 6 at (d,m)=(2,1); rank 28 at (6,3); rank 66 at (10,5).
- T: rank 6 at (2,1); rank 36 at (7,3); rank 78 at (11,5).
- The 3-by-3 grid: rank 6 at (2,1); rank 45 at (8,3).

These ranks also agree at primes 101, 1009 and 10007. Explicitly expanded star products verify upper witnesses of degrees 3,7,11. For T the dimensions at degrees 3,8,12 are 10,45,91 against at most 6,36,90 linear conditions. Thus the exact triples (a_1,a_3,a_5) are (3,7,11) for S and (3,8,12) for T. The grid products verify degrees 3 and 9; the written line-peeling induction proves a_m=tm for all m and every t-by-t grid in its stated characteristic-independent scope.

Adversarial controls find rank 32, rather than 36, when S is substituted into T's degree-7 triple-point test. Six collinear points have conic-evaluation rank 3. An invertible rational scaling y ->1009*y of T retains rational conic rank 6 while its reduction modulo 1009 has rank 3. The latter example specifically rejects treating a deficient modular rank as evidence of a rational kernel. No upper certificate in the package makes that error.

Dependency: matching the reduced Hilbert function does not determine symbolic powers. The line-count update gives no universal transfer inequality. None is claimed.

## Approach 5: squarefree plane curves and polar Bezout

Accepted. This is the strongest structural partial in the package, and its scope is correctly restricted.

For a=alpha(I(X)), injectivity of evaluation in degree a-1 gives |X|>=a(a+1)/2. If F is squarefree in characteristic zero, for each irreducible factor H some derivative of H is nonzero of smaller degree. Modulo H, the corresponding derivative of F is nonzero because the complementary product is not divisible by H. Hence the coefficient choices for a polar divisible by H form a proper linear subspace. An algebraically closed characteristic-zero field is infinite, so the finite union of these subspaces does not fill the coefficient space. There exists a nonzero polar coprime to F.

At each support point its order is at least m-1. Coprimality allows Bezout, and the local intersection inequality supplies d(d-1)>=|X|*m*(m-1). All curves and orders have the required plane/projective interpretation; no generic-position assumption about X enters this argument.

For a purported counterexample m=2r-1 and d<=D=r(a+1)-2. Since d>=m, increasing to D preserves the d(d-1) comparison. Independently expanding the resulting difference with r=3+t gives

E=(1-a^2)t^2+(1-2a-3a^2)t-a(a+7).

For a>=1 and t>=0, the quadratic coefficient is nonpositive, the linear coefficient is negative, and the constant term is strictly negative. This proves the contradiction for every r>=3. For r=2, E=a(a-5), strictly negative at a=1,2,3,4. The package already settles a=1 separately. The boundary a=5 gives E=0, so the proposed extension of this argument to r=2,a=5 was correctly rejected.

The conclusion means **every polynomial witness of a plane counterexample in the stated range has a repeated irreducible factor**. It does not mean that a counterexample exists or that excluding squarefree witnesses proves the conjecture.

The exact remaining gap is weighted, nonuniform component data. In F=product H_j^(e_j), uniform lower bounds on sum e_j*ord_P(H_j) do not give uniform lower bounds on each summand. Dividing a repeated factor does not preserve a uniform instance with the alpha parameter needed for induction. In an explicit sharp star witness, removing one occurrence of x yields point orders (3,3,2,4,3,3). This demonstrates the obstruction without pretending to construct a target counterexample. A bound handling arbitrary repeated components and their different supports is not supplied.

## Reproducibility and counts

Run python3 independent_checks.py from this audit directory, or supply its path from elsewhere. It writes only this audit's results.json. Do not run the original script's command-line entry point against the frozen directory: that entry point intentionally overwrites its results file. The audit instead replays the inspected original run() function in memory after completing its separate implementation.

Verified independently:

- 8 exact rational lower-degree rank checks and 24 corresponding modular checks.
- 10 reduced-Hilbert rank checks, with the all-degrees conclusion justified in writing.
- 5 explicit expanded upper polynomials and 3 dimension-count upper certificates.
- 9 further star rank controls in projective dimensions 1 through 4.
- 7,200 exact parameter tuples for the deficit/threshold identities.
- 9,800 parameter tuples for the polar polynomial identity and strict sign, plus 4 r=2 boundary cases.
- 18 negative controls: 11 binding/content mutations and 7 invalid mathematical inferences.
- Exact in-memory replay of all original output: 8 rank cases, 7,200 identity tuples and 9,702 polar tuples.
- Final byte-preservation check for all eight original files and the archive.

Finite arithmetic counts are regression evidence only. The universal claims depend on the written proofs reviewed above.

## Source and publication limitations

Four fresh primary PDFs match the four frozen hashes and byte counts. Exact source inspection/retrieval metadata is in SOURCE_AUDIT.json. Source PDFs, extracted text and rendered images are not included in this audit package. The safe audit contains only authored analysis, code, results, and public verification metadata.

This audit did not retrieve the UnsolvedMath page, raw dataset files, research-results corpus, catalog contents, prior conversations, or repository history. Their earlier retrieval and duplicate-check claims remain historical assertions in the frozen package, not independently reverified audit outcomes. In particular, the catalog's recorded statement hash is not promoted to an independently recomputed statement hash. These limitations do not prevent matching the authored mathematical statement to the primary OWR statement, but they matter to any later readiness or publication decision.

The source checks are bounded. A 2025/2026 related publication with different quantifiers is not proof that no later paper resolves the target. The exact overall outcome remains: the five recorded approaches did not resolve the stated arbitrary-support characteristic-zero problem, and the audit accepts the documented partials and limitations. No claim about worldwide openness or originality is licensed.

The audit verdict is bound to the frozen bytes. Any substantive change requires a new binding and review. Archive, script, report, binding, source metadata and result hashes are recorded in the separate audit manifest; the manifest does not attempt to hash itself.
