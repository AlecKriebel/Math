# Research log: 30000971 / OWR-1971-004

Date: 2026-10-04. All times below are UTC from the session clock, not file modification times. Five substantive approach families are recorded. Source lookups and reproducibility checks are not separate proof turns. No remote files or queue statuses were changed during this research.

## Readiness: 11:43--11:46

The catalogue URL was attempted first and was unavailable (later confirmed HTTP 403). The supplied pinned record was recovered by numeric ID. Both bundled questions were checked against OWR 26/2008 and Beheshti--Eisenbud arXiv:0806.1928v3. The primary characteristic-zero hypothesis and ideal-sheaf regularity convention were restored. The source report is from the June 2008 workshop; the compact catalogue's 2009 title label is not the workshop date.

The live row was queued, 0/5. No target attempt directory or ID-matching PR was found. The historical repository desk review proposed controlling noncurvilinear fibers but provided no proof. The pinned prior-report corpus lacks the matching OWR record; absence was not treated as evidence of a successful previous attempt. The related-target register has no entry for this target. Related rank 600 concerns a different primary-powers problem.

Research preparation complete; mathematical completion estimate toward the full bundled target: 0%.

## Approach 1: linkage and conormal tangent dimensions, 11:46

Mechanism: combine the source's licci equality q=length with a self-contained interpolation proof reg<=length. The latter uses strict growth of the affine degree filtration until it spans the finite coordinate algebra.

Result: a complete derivation of both inequalities for all-licci fibers, including embedding dimension <=2. Credited inputs: Beheshti--Eisenbud Theorems 1.1 and 4.4, Proposition 4.5. Recorded in PARTIALS.md P1--P2.

Exact gap: general fibers need not be licci; neither q=length nor q>=length is available outside that class. Stop this extension unless a new mechanism supplies the missing estimate. Full-target completion estimate: 5%, consisting of a verified scope reduction, not a resolution probability.

## Approach 2: corank and multijet restrictions, 11:46--11:47

Mechanism: use the Mather corank inequality e(e+c)<=n to force the fiber into the licci classes from approach 1, rather than trying to estimate all finite algebras directly.

Result: both bounds follow for n<3(c+3); for c=1 the four-generator linkage input improves the range to n<20. The c>n embedding range is immediate from the multigerm bound. Recorded in PARTIALS.md P3, with explicit credited input and endpoints.

Exact gap: the boundary permits higher embedding dimension. Corank alone does not control arbitrary higher-order nilpotents. Full-target completion estimate: 10%.

## Approach 3: square-zero Q modules and actual generic realization, 11:47--11:54

Mechanism: calculate Hom(m^2,A) for a square-zero algebra, rather than assume q behaves like length. For embedding dimension e, there are g=e(e+1)/2 generators and g*e homomorphism dimensions. At excess c=g-e this gives length(Q)=g and q=(e+1)/(e-1), below regularity two when e>=4.

The first observation concerned a special smooth intersection and was explicitly not accepted as a general-projection counterexample. The geometric construction then used X=v_2(P^n), n=e*g, and a quadratic jet with normal determinant 2^e. That yields an etale incidence point and a nonempty open of genuine projection parameters. A separate first-jet-plus-second-value incidence eliminates additional support points, with codimension c. Formal elimination and Nakayama force the exact square-zero ideal. Frame invariance descends the result to an open set of projection centers.

Result: complete candidate refutation of the second original question. The e=4 member has n=40, c=6, length(Z)=5, length(Q)=10, reg(Z)=2, and q=5/3. All exact calculations passed for e=2,...,6. The jet with all cross terms removed has rank e instead of n, a successful negative control for the generality argument. Full details: PROOF.md and check.py.

Exact gap for the original target: the weaker inequality remains intact; its right side is 23/3 in the first example. Candidate novelty and correctness require independent audit. Full-target completion estimate: 45%, recognizing that one of the two bundled assertions has a complete candidate negative answer, not a fully reviewed result.

## Approach 4: interpolation by local nilpotency, 11:55--11:56

Mechanism: replace length by each local algebra's nilpotency exponent, combine separating linear forms with local polynomial truncation, and prove reg(Z)<=sum nu_i.

Result: the interpolation lemma is proved in PARTIALS.md P4. It handles square-zero components sharply and explains why their high length is irrelevant to the weaker bound. The tempting condition q_i>=nu_i is invalid by approach 3. Fixed corank alone is insufficient for arbitrary Artinian schemes, as k[t]/(t^M) illustrates.

Exact gap: there is no established all-dimensional genericity estimate sum nu_i<=n/c+1. The curvilinear example is a diagnostic against an unrestricted local inference, not a claimed fiber counterexample. Full-target completion estimate remains 45%.

## Approach 5: the asymptotic powers route, 11:56--11:57

Mechanism: apply Eisenbud--Harris Theorem 0.1 to the actual coordinate ring and the projection ideal. The maximum regularity is epsilon+1, where epsilon is the least eventual containment exponent.

Result: the first question is precisely the sharp bound epsilon<=floor(n/c). This is an exact algebraic reformulation, recorded in PARTIALS.md P5. It is not implied by mere eventual linearity and does not follow by substituting the unrelated rank-600 primary-powers setting.

Exact gap: no proof of the uniform intercept bound was obtained. This route transfers the central difficulty and is therefore closed without claiming progress beyond the equivalence. Five substantive approaches are exhausted. Overall status remains unsolved; full-target completion estimate remains 45%. Research execution and deliverable preparation: 100% pending audit.

## Literature and freeze boundary

The bounded literature pass checked the original OWR report, the main 2009-revised Beheshti--Eisenbud paper and its 2009/2012 sequel, Eisenbud--Harris on ideal powers, Ran's embedding-dimension-two paper, the authors' publication index and the 2024 Ein--Lazarsfeld lecture draft. The latter still calls the weak inequality a conjecture. Targeted searches found no primary source settling the full target or documenting this exact stronger-comparison counterexample. This is not an exhaustive novelty or continuing-openness certification.

The frozen public packet contains original proofs, credited partial deductions, small exact scripts, output and provenance. Primary PDFs, the imported corpus, raw connector records, and private coordination remain outside it. No outside individual was contacted. No independent external human peer review or new public release is claimed. A fresh independent audit and final repository gate are required before any remote publication.
