# Independent adversarial audit: circumscribed 2n-facet polytopes

Public projection: one paragraph concerning non-mathematical eligibility/provenance checks has been omitted. All mathematical findings, limitations, corrections, and reproducibility results are preserved. The original audit remains unchanged; its manifest SHA-256 is recorded in PUBLIC_AUDIT_MANIFEST.json.

## Frozen verdict

**PASS AS SCOPED PARTIAL WORK; ORIGINAL CONJECTURE UNRESOLVED.**

Problem 30001070 / OWR-2090-023. Reviewed on 2026-10-03 against commit `9b837c4a9a21c35bb69d0313dbc06e83904695e0`, directory `circumscribed_2n_facets_30001070`, repository AlecKriebel/Math. All 23 published files were independently fetched at that exact commit and matched the supplied local bytes and Git blob hashes. The 22 payload SHA-256 values in WIP_MANIFEST also match. All five exact scripts pass and reproduce their captured JSON exactly.

No substantive mathematical error was found in the scoped reductions, local lemma, moment lemma, necessary stationarity identities, or exact finite counterexamples to proposed shortcuts, with the existing n>=2 corrections applied. This does not certify a solution, novelty, priority, a complete literature search, or readiness for a result PR. The five author turns remain exhausted. This audit tested existing claims and supplied controls; it did not conduct a sixth solution-search turn. No remote write or PR was made.

The packet correctly separates: (a) unrestricted target; (b) proved restricted statements; (c) necessary conditions insufficient for the target; (d) counterexamples to intermediate shortcuts; and (e) bounded numerical probes.

## 1. Source and exact scope

The live primary PDF confirms Zong's Conjecture 2 in Section 4, printed p2547: a polytope with 2n facets containing the origin-centered unit ball has maximum origin-distance at least sqrt(n), with equality precisely for a circumscribed cube. Its note identifies n>=5 as open. The neighboring blocking-number statement is a different conjecture. The packet's correction of the imported background is justified.

Source: https://ems.press/content/serial-article-files/46191?nt=1

Borodachov's paper states the antipodal restriction explicitly in Theorem 2.2 and discusses prior dimensions 2, 3, 4 separately. It does not settle arbitrary non-antipodal configurations in n>=5. Its cross-polytopal/triangulated-facet discussion is compatible with the packet's local calculation, but is not a novelty assessment of that calculation.

Source: https://arxiv.org/abs/2210.12472

The live Springer article page confirms publication on 20 August 2026 and, in its introduction, still describes the cross-polytope's spherical-covering optimum as conjectural. Its sphere dimension d corresponds to ambient dimension n=d+1 here, and its point count 2d+2 becomes 2n. Thus this is directly relevant recent evidence. The article does not prove absence of all unlocated results, nor does its brief covering-optimum passage independently certify the full equality classification.

Source: https://link.springer.com/article/10.1007/s00454-025-00812-8

The maximum over P is the maximum over its vertices: expressing a point as a convex combination of vertices and applying convexity of the Euclidean norm gives the equality of these maxima. Consequently the packet's max-over-P formulation matches a max-vertex-norm target.

## 2. Turn 1: reduction, equality, antipodal baseline, local cube

### Tangency and polarity: accepted

An irredundant facet representation with unit outward normals has support numbers h_i>=1. Replacing every h_i by 1 gives B subset T subset P. The recession cone depends only on the normals, so boundedness is preserved. Distinct oriented unit normals ensure that u_i itself is on only its own equality plane: u_j dot u_i<1 for j!=i. A relative neighborhood in that plane therefore remains in T, proving the inequality is an actual facet, not just a supporting inequality. Thus the exact 2n facet count survives.

Positive spanning and 0 in the interior of conv{u_i} are equivalent by separation. Each unit normal is an exposed vertex of that convex hull. T is its polar, and along a unit direction v its radial extent is 1/h_Q(v). Therefore R_0(T)=1/min h_Q(v). The cap-covering relation follows from max_v min_i arccos(u_i dot v)=arccos(min_v max_i u_i dot v). Configurations that fail positive spanning have a nonpositive minimum support and cannot supply a strict violation of the positive threshold.

The equality transfer is complete and essential. Assuming the normalized theorem, R_0(P)=sqrt(n) forces R_0(T)=sqrt(n), hence the normal directions are an orthonormal opposite-pair system. P is then a box with each positive and negative support number at least 1. Its radius squared is the sum of the squared larger support number in each pair. Equality n forces all support numbers to be 1. No hidden free recentering, symmetry assumption, or weaker objective appears in this reduction.

### Antipodal trace baseline: accepted, prior credit retained

For unit independent rows A, averaging ||A^-1 s||^2 over signs gives tr((AA^T)^-1). Trace AA^T=n and the scalar harmonic-arithmetic mean inequality give at least n. Radius equality forces AA^T=I. No extension to arbitrarily paired non-antipodal normals is justified; the packet does not make one.

### Cube Hessian and local conclusion: accepted

I independently differentiated the selected-plane equation A_s(t)x_s(t)=1 twice rather than using the packet's expansion as input. In dimension three the resulting full symbolic polynomial in all 12 off-diagonal tangent variables equals

2||P||_F^2 + 4||Sym Q||_F^2.

The coefficient's Hessian has eigenvalues 4 (multiplicity 6), 8 (multiplicity 3), and 0 (multiplicity 3). The nullspace is exactly P=0, Q skew, matching infinitesimal rotations. The packet's sign-moment derivation gives the same formula in general dimension; all odd-sign terms vanish and the zero diagonal eliminates the extra P-square contraction.

Every selected intersection remains feasible in a sufficiently small common neighborhood because the unselected inequalities have strict margin 2 at the cube and there are finitely many selectors. The averaged function is smooth and rotation invariant there. A transverse slice has positive definite Hessian, which justifies the strict local minimum modulo rotations. This argument is stronger than merely checking directional second derivatives, because the slice removes precisely the symmetry kernel. It is a fixed-dimension local result. It gives no global deformation, no guarantee through combinatorial changes, and no uniform neighborhood in dimension. The packet maintains those limits.

## 3. Turn 2: centered equal-weight tight frames

### Sharp restricted theorem and equality: accepted

At a vertex there are at least n linearly independent active normals, so the number k of active listed normals is at least n. Centering makes the inactive scalar products sum to -k; k<N. Isotropy converts their squared sum to (N/n)||x||^2. Cauchy-Schwarz gives the stated lower bound nk/(N-k), hence n^2/(N-n).

For N=2n and radius sqrt(n), every vertex must have exactly n active normals and all inactive scalar products -1. Consequently each linear functional u_i dot x stays in [-1,1] on the whole polytope, and T=-T. In the distinct-normal setting inherited from Turn 1, its exactly 2n facets form n opposite pairs; boundedness implies independent directions, and the antipodal argument forces orthogonality. The claim is correct. To use the lemma completely standalone, explicitly retain distinctness or note that equality k=n also rules out duplicated active normals, so duplicated rows cannot create an equality exception.

The six-normal rational example is valid, centered, unit, isotropic, and non-antipodal. Independent enumeration finds five distinct vertices: two of squared norm 3 and three of squared norm 6. It verifies genuine non-antipodal coverage of the restricted lemma; it is not an original counterexample.

### Weighted and anisotropic statements: accepted only as scoped

For positive c_i with centered moment and covariance I, trace gives total weight n. At a vertex the inactive weight is positive. Weighted Cauchy-Schwarz gives ||x||^2>=na/(n-a). Thus active weight at least n/2 is sufficient. Neither the existence of these weights for an arbitrary original configuration nor the requisite active-mass conclusion has been established.

For merely centered normals, replacing exact isotropy by lambda_max(S) gives exactly the stated weaker radius-squared bound Nn/((N-n)lambda_max(S)); for N=2n it is 2n/lambda_max(S). Its direction is correct. Rotations cannot repair anisotropy or a nonzero centroid. Linear transformations followed by row normalization do not preserve this Euclidean target. The packet does not assume an illicit normalization.

## 4. Turn 3: failed combinatorial shortcut and stationarity

### Stacked-polytope counterexample: accepted

The original rational supporting-hyperplane enumeration and an independent hull control give eight vertices and 14 facets in dimension four. Each facet contains at most one of the three added weight-1 vertices. Total weight is 4 and maximum facet weight is 8/5, strictly below 2. The original simplex proves full affine dimension; the facet list also verifies all eight displayed points are vertices. This is a counterexample only to the purely combinatorial weighted-facet assertion. The vectors are not unit normals with the required centered isotropic weighting. No original-conjecture counterexample follows.

### Necessary stationarity identity: accepted under the stated regular setting

For a minimal-distance facet, the point r w lies in its relative interior: it belongs to the inscribed ball; equality in any different support plane would contradict Cauchy-Schwarz and distinctness of the support planes. A simplicial facet therefore has strictly positive barycentric coefficients. Differentiating its equations and using the barycentric relation eliminates dw, yielding dr_F=sum alpha_i w dot du_i.

At a local maximum of the minimum of finitely many smooth facet-distance functions, separation gives a convex combination of their tangent gradients equal to zero. The stated lambda, d, and A definitions then yield A U=r^2 D U. A is symmetric, entrywise nonnegative and PSD, with A1=d. Summation gives the weighted centroid zero for r<1. Multiplying the tangent-gradient relation by the normal vectors gives the displayed equality of second moments. It gives no isotropic covariance assertion.

The n>=2 qualification in CORRECTIONS is necessary and sufficient here: an inscribed full-dimensional finite polytope has r<1 for n>=2, whereas [-1,1] has r=1 in dimension one.

If d_i>0, the symmetric matrix B is similar to the row-stochastic D^-1 A. Its Perron eigenvector is sqrt(d), and the n independent coordinate columns have eigenvalue r^2. Their orthogonality follows from the weighted centroid. Hence tr B>=1+n r^2. The tangential-vector triangle inequality proves each alpha_i<=1/2, so tr B<=N/2 and only r^2<=(n-1)/n follows at N=2n. This is not the sharp n-dimensional target. There is no proof of tr B<=2 in the packet.

An independent exact cube control gives tr B=2 and spectrum 1, 1/3 (three times), 0 (twice) for n=3, and verifies both the stationary equation and second-moment equation. This is a control, not an optimizer classification.

The zero-d caution is conservative: in this regular simplicial setting a facet with positive lambda supplies n linearly independent rows in the support of d, so support rank can in fact be checked immediately. This does not rescue the missing sharp trace bound or extend the argument to nonsimplicial optimizers. Do not describe the identity as a sufficient optimality certificate.

## 5. Turn 4: anisotropic two-simplex family

The normalized family is valid for n>=2 and 0<z<1. H is invertible; Q fixes e and, being orthogonal, also has column sums 1. Each row has the claimed unit length, the total row sum is zero, and full rank plus strictly positive zero-sum coefficients imply positive spanning. Within each group rows are distinct; opposite heights make the two groups disjoint. Consequently there are exactly 2n genuine polar facets. The frame operator is 2H^2, isotropic exactly at z=1/n.

The pole and edge formulas follow by writing y=Hx. On the edge y=1-te_i, a lower inequality becomes -1+t Q_ji<=1, so first contact is 2/max_j Q_ji. Positivity of the maximum follows from column sum 1. Decomposing H^-2 into its e and e-perpendicular eigenspaces gives the stated f(t). The monotonicity on t>=2 for z>=1/n is valid. At n=5,z=3/11, the one-flip norm squared is 121/25<5 whereas the two-flip norm squared is 407/75>5. These facts defeat the edge-only inference and do not defeat the conjecture.

Independent exact RREF enumeration of the supplied rational ten-normal example gives:

- 252 five-row subsets: 4 singular, 189 invertible infeasible, 59 invertible feasible.
- Exactly 34 distinct feasible vertices, with maximum norm squared 340657525/23222761 and minimum 21125/6241.
- 32 vertices have five active facets, one has six, and one has seven. Thus this example is not simple; its polar normal hull is not simplicial.
- No antipodal normal pairs.
- An independent floating-point halfspace-intersection calculation returns the same 34 vertices with maximum matching error below 1.4e-15.
- The normal hull triangulation has 40 simplices, which must not be conflated with its 34 true facets.

The maximum vector in the packet matches exactly. Full enumeration is complete because every vertex of a full-dimensional bounded intersection has an independent n-element subset of its active constraints. Deduplicating the 59 feasible bases is necessary. The packet does this correctly. The n=5 cube control gives 32 vertices, all squared norm 5, from 32 feasible and 220 singular bases.

The exact anisotropic example cannot be inserted into the regular simplicial stationarity argument without addressing its nonsimplicial hull. The packet does not claim that it can.

## 6. Turn 5: determinant mechanism

The determinant identity is correct under its explicit all-bases-nonsingular assumption. One independent derivation decomposes 1=U c+z, where c=G^-1 b and U^T z=0. Replacing the j-th column gives squared volume det G times [c_j^2+||z||^2(G^-1)_jj]. Since ||z||^2=N-b^T G^-1 b, summing over j yields (D). This argument checks the noncentered b terms as well as the centered specialization.

An independent noncentered rational unit-row control gives total determinant weight 15811/4225 and mean 62790/15811, agreeing exactly with (D). This is an identity test, not a conjecture search.

For the supplied six-normal example, all 20 bases are nonsingular. The 14 feasible bases produce only five distinct vertices. The determinant averages 9 over all bases and 57/11 over feasible bases, and maximum actual vertex squared norm 6, are all correct. Each of the six infeasible intersections has squared norm 51 and weight 1/9. Thus their total numerator contribution is 34; total numerator is 72 and feasible numerator is 38. This directly explains the failure of the transfer from the all-bases average.

The singular-basis warning is also correct. For the square normals, the sum of the actual invertible-base numerators is 8, while the all-base adjugate/Cramer numerator sum is 16; singular bases contribute the missing 8. Zero determinant does not justify dropping a nonzero Cramer numerator and retaining (D).

For a bounded polar, the feasible set of bases is nonempty. A true (V) would therefore force at least one actual vertex's squared norm to be at least n. The statement is genuinely sufficient, not shown equivalent to the original conjecture; equality classification would require more work. Neither (D) nor the counterexample to transferring (D) proves or disproves (V). Its status remains unproved here.

## 7. Reproducibility, limitations, and corrections

All exact scripts replayed with exit code zero and exact JSON agreement. The controls use Python 3.12.14, SymPy 1.14.0, NumPy 2.3.5 and SciPy 1.17.0; exact and floating calculations are separately labeled.

Both existing diagnostic scripts were rerun without expanding their search domains or trial budgets. The two-simplex diagnostic reproduced its saved JSON exactly, including 125 grid evaluations and 2111 local-search evaluations. The weighted-mass diagnostic retained the same 8,7,8,6 cases and the same minimum masses to reported precision; its largest numeric difference from the capture is 3.3306690738754696e-15. This is expected floating-point variation, not an exact replay. Its whitening enforces weighted centering/covariance algebraically but unit-length and optimizer tests remain floating-point. No certified optimum or proof comes from either script.

Corrections required to the mathematical claims: **none beyond the existing n>=2 errata**. Recommended precision when summarizing or reusing:

1. Distinguish vertices, feasible bases, true facets, and triangulated facets using the counts above.
2. Keep the nonsingular-bases hypothesis attached to (D) and the regular simplicial hypotheses attached to the stationarity analysis.
3. Keep equal-weight centering/isotropy attached to Turn 2; they are not a normalization of the unrestricted problem.
4. Preserve the dimension-one exclusions in Turns 3 and 4, already recorded in CORRECTIONS.
5. Do not imply all diagnostic JSON replays are bit-identical; only the exact scripts and Turn 4 diagnostic were identical in this environment.
6. Treat the original final-status statement that no independent review had yet occurred as a historical status at the frozen commit. This separate audit supersedes that fact only for these scoped claims and does not supply novelty clearance or a solution review.

This report and its manifest are separate from the untouched author packet. The final status remains exhausted/unresolved, with no original counterexample, global proof, equality classification in the unrestricted open range, novelty certificate, or result PR.
