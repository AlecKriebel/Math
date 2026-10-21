# Likelihood fiber audit: five approaches and precise partial conclusions

Queue 1864, ID 20001237 / AIM-COMPUTATION-0075. Authored mathematical analysis, 21 October 2026. No claim of novelty or complete solution of the historical general problem. Source/status gate: `source_gate.md`. All results below concern explicitly specified complex algebraic families; statistical conclusions require separate nonnegative-real hypotheses. An independent mathematical audit accepted the explicitly bounded scope below.

## 1. Direct score approach: exact complete-independence classification

Consider k factors with sizes d_s≥2 and normalized complete independence
p_(i_1,...,i_k)=∏_s a^(s)_(i_s), where ∑_i a^(s)_i=1 and every a^(s)_i≠0. This is exactly the coordinate-torus, p_+≠0 part of the projective Segre variety, in its unique normalization p_+=1. Let N=∑u and M^(s)_i=∑_{other indices}u. Each marginal sums to N. Set m=∑_s(d_s−1).

The logarithmic likelihood differential is ∑_(s,i) M^(s)_i da^(s)_i/a^(s)_i. A linear functional vanishes on the tangent hyperplane ∑_i da_i=0 iff its coefficients are constant. Thus criticality is equivalent to M^(s)_i/a^(s)_i=λ_s for every i. Summing gives λ_s=N, hence the exact equations M^(s)_i=N a^(s)_i.

Consequently:
- If N≠0, the valid fiber consists of one reduced point iff every marginal entry M^(s)_i is nonzero. Its coordinates are a^(s)_i=M^(s)_i/N and p_I=∏_s M^(s)_(i_s)/N^k. If any marginal is zero the valid fiber is empty.
- If N=0 and every marginal is zero, the entire smooth open model is critical, of dimension m.
- If N=0 and some marginal is nonzero, the valid fiber is empty.

Reducedness in the singleton case follows from the affine-linear equations in independent factor coordinates with coefficient N≠0. Thus the positive-dimensional valid-fiber locus in affine data space is exactly the kernel of the marginal map, assuming m>0. In projective data space it is its projectivization, empty if that kernel is zero. This is a consequence of standard independence formulas, not a new result.

For 2×2, take N=sum u, r=u11+u12, c=u11+u21, and factor coordinates a,b. The equations are r−Na=c−Nb=0 on D=a(1−a)b(1−b)≠0. Positive-dimensional valid fibers occur precisely at (N,r,c)=(0,0,0), with dimension 2. The nonzero data u=(1,−1,−1,1) have these statistics; their rational likelihood p11 p22/(p12 p21) is identically 1 on independence. A nonzero data vector can therefore be lost if statistics are projectivized before retaining the kernel stratum.

Failure of an alternative route: generic ML degree 1 controls the generic fiber, not all complex fibers. Positive-real uniqueness does not rule out the complex zero-statistic fiber.

## 2. Toric tangent approach: a general zero-total theorem, not a general classification

Let A be an integral d×n matrix of rank d whose row span contains the all-ones vector, and X_A the projective toric closure of [θ^(a_1):...:θ^(a_n)]. Work over C on U=X_A∩{p1⋯pn p_+≠0}. The coordinate-torus part is the dense algebraic torus of X_A and is smooth, even if its boundary is singular or the closure is nonnormal. Let b=Au and N=∑u. Normalize p_+=1.

Pull back the log-likelihood differential to the parameter torus:
 d log L_u = ∑_j (b_j−N(Ap)_j) d log θ_j.
The torus parametrization surjects onto the dense torus and has surjective tangent map in characteristic zero. Therefore its pullback vanishes iff the model differential vanishes. The redundant scaling direction contributes zero automatically because 1 is in rowspan(A). Hence the exact critical equations on U are
 Au=N Ap.

At N=0 the equations are independent of p: the fiber is all U if Au=0 and empty otherwise. The first case has dimension d−1. When d=1 this is zero-dimensional, so the phrase positive-dimensional must not be used without d≥2. When ker A={0}, no nonzero projective datum lies in the full-critical stratum. U is nonempty since θ_j=1 gives p_+=n≠0.

For N≠0, the problem reduces exactly to the fibers of the regular map μ:U→{b: corresponding total=1}, p↦Ap, with target Au/N. This reformulation leaves the central model-dependent issue unresolved: which nonzero-total fibers of μ have positive dimension? No theorem here says those fibers are always finite for arbitrary A.

For real nonnegative nonzero data, N>0. The zero-total complex phenomenon is absent. Strict concavity in identifiable natural parameters supplies at most one finite positive MLE when one exists; existence and boundary attainment are separate issues.

Failure of an alternative route: positivity/Hessian definiteness over the positive real locus cannot be extended to all complex parameters. A complex covariance/Hessian may be singular; its determinant identifies possible nonreduced or ramified finite fibers as well as potential dimension jumps, not the latter exactly.

## 3. Rank-one expected-count approach: exact matrix classification

This is a different family. Fix an m×n matrix q of rank at most 1, with row sums R∈C^m and column sums C∈C^n. Assume compatible totals ∑R_i=∑C_j=N and m,n≥2. No normalization q_+=1 is imposed.

If N≠0, every solution has q=RC^T/N and this is the unique solution. To see this, write a nonzero rank-one q=x y^T, so R=x(∑y), C=y(∑x), N=(∑x)(∑y). Both sums are nonzero and substitution gives the formula. The point is in the cell torus iff all entries of R and C are nonzero.

If N=0:
(a) R≠0 and C≠0: no solutions, since both sums in that factorization would have to be nonzero.
(b) R≠0 and C=0: all solutions are q=R v^T with ∑v=1, an affine space of dimension n−1. Its cell-torus open is nonempty iff every R_i≠0, and then is dense and has the same dimension.
(c) R=0 and C≠0: transpose (b), dimension m−1; cell-torus nonempty iff every C_j≠0.
(d) R=C=0: the solutions are the rank-at-most-one cone in H_m⊗H_n, where H_m={x:∑x=0} and H_n={y:∑y=0}. Indeed nonzero q=x y^T forces ∑x=∑y=0; conversely these conditions suffice. The cone is irreducible of dimension (m−1)+(n−1)−1=m+n−3. Its cell-torus open is nonempty and dense: each H has a vector with all coordinates nonzero over C. The zero matrix belongs to its closure, not the cell-torus open.

For 2×2 write q=(t,r−t,c−t,N−r−c+t). The determinant is Nt−rc. Thus the affine positive-dimensional locus is V(N,rc), with line fibers, including the origin statistic. It is not the valid normalized likelihood locus V(N,r,c), whose nonempty exceptional fiber has dimension 2.

Explicit mismatch: N=0,r=1,c=0 gives q(t)=(t,1−t,−t,t−1), a line with four nonzero cells for t∉{0,1}; normalized likelihood has no critical point. For actual data choose u=(0,1,0,−1). Thus even cell-torus saturation does not repair the comparison.

Failure of an alternative route: q=Np is an isomorphism only over N≠0. It cannot identify zero-total fibers and it collapses every normalized p to q=0 at N=0.

## 4. Projective closure and specialization: boundary fibers explicitly recovered

Use Segre coordinates p=[x0y0:x0y1:x1y0:x1y1] with [x0:x1],[y0:y1]∈P1. Over affine statistics (N,r,c), the closure of the actual critical incidence is the closed incidence
 r x1−(N−r)x0=0,
 c y1−(N−c)y0=0.
This is a set-theoretic description of every fiber (and the standard incidence scheme is reduced globally). The valid open additionally requires x0x1y0y1(x0+x1)(y0+y1)≠0. On that open the equations give r=N x0/(x0+x1), c=N y0/(y0+y1), exactly the scores.

Why this is the closure, not an arbitrary enlarged incidence: if N≠0 each factor is uniquely [r:N−r] and [c:N−c], including boundary values. At N=0 with r,c nonzero the factor pair is ([1:−1],[1:−1]), reached from generic data. At N=0,r=0,c≠0, the second factor is [1:−1] and the first factor is arbitrary. For a first factor with x0+x1≠0, take N=t and r=t x0/(x0+x1), c fixed. For first factor [1:−1], take N=t² and r=t. Both paths approach the required point and generic perturbation avoids cell zeros. The transpose handles the other case. At the zero statistic every factor pair belongs to the closure because all valid model points already lie in that critical fiber and the valid open is dense in Segre. Hence every point of the incidence is in the closure. Reducedness can also be checked locally: near x0=y0=1, x1=y1=−1 set s=1+x1 and t=1+y1; the equations become rs=N=ct, giving the integral-domain chart C[r,c,s,t]/(rs−ct). Away from the point where both factor sums vanish, the two linear equations in (N,r,c) have rank two and give a line bundle over an irreducible open. Thus there are no hidden nonreduced components in the total incidence.

Its fiber classification:
- N≠0: one projective point, possibly outside the valid open.
- N=0,r c≠0: the single point [1:−1:−1:1], with p_+=0.
- N=0,r=0,c≠0: a projective line, entirely in p_+=0.
- N=0,r≠0,c=0: the other ruling line, entirely in p_+=0.
- N=r=c=0: the full Segre surface, dimension 2; its valid open is the all-critical fiber.
Thus the closure's positive-dimensional locus is V(N,rc), but its fibers are NOT those of the affine expected-count family. Equality of these two loci in this example is not equality of families and not equality with the actual likelihood jump locus.

Saturation and base change do not commute. In C[N,r,c,a,b], let I=(r−Na,c−Nb) and D=a(1−a)b(1−b). I is prime by eliminating r,c; D∉I, so I:D^∞=I. Specialize to N=1,r=0,c=1/2: the specialization of the saturated ideal is (a,b−1/2), a boundary point, whereas saturating that specialized ideal by D gives the unit ideal, correctly recording an empty valid fiber. Global saturation closes an open family; it does not remove all excluded points from all special fibers.

Likewise I:N^∞=I. Inverting N and then taking closure does not guarantee empty zero-total fibers. A genuine restriction to N≠0 must be maintained as an open condition (or with an inverse variable), rather than interpreted from its closure ideal alone. Inverting p_+ is a model-space restriction and never implies N≠0 in data space.

Failure of an alternative route: specializing an already saturated correspondence and counting its whole fiber may count invalid boundary points or components. The projective closure is proper and has closed dimension-jump loci, but this does not establish closedness of every open critical-family jump locus.

## 5. Fiberwise localization and algorithmic stratification

For a fixed homogeneous A with known toric ideal I_A, use normalized model coordinates and the ideal
 J=(I_A(p), ∑p_i−1, Au−N Ap, z∏p_i−1).
Here u or independent statistics are parameters and p,z are unknowns. The auxiliary variable z is uniquely determined on the valid open; its use changes neither emptiness nor dimension. Since the toric coordinate-torus locus is smooth, no further smoothness exclusion is needed for this toric family. For a non-toric singular model, cover its smooth locus by suitable nonvanishing Jacobian minors; a single arbitrary minor is not in general the entire smooth locus.

Specialize J at each data parameter, or compute a comprehensive Gröbner stratification retaining nonvanishing parameter conditions. On each stratum, a valid Gröbner basis determines whether 1 lies in the ideal and otherwise the dimension via the initial ideal. This is a finite algorithmic route to a constructible stratification for fixed finite input. It is not a uniform structural closed formula in A, and complexity can make it impractical. In particular a leading coefficient vanishing merely says a chosen generic elimination calculation needs a new branch: it is not by itself a certificate of a positive-dimensional fiber.

A simple cautionary family is f_t(x)=t x−1. Its generic elimination leading coefficient vanishes at t=0, but that fiber is empty, not positive-dimensional. A second is f_t(x)=x²−t: the discriminant vanishes at t=0, but the special fiber remains zero-dimensional (a nonreduced point). The likelihood example at N=1,r=0,c=1/2 supplies the boundary-disappearance version.

The exact 2×2 inverse-variable family is (r−Na,c−Nb,zD−1). It yields 1 on the two empty branches (N=0 with (r,c)≠0; N≠0 with r(N−r)c(N−c)=0), a reduced singleton on the generic valid branch, and a 2-dimensional hypersurface zD=1 at (N,r,c)=0. These classifications agree with the direct proof, independently of compactification.

## Prior-art and status boundary

Barnhill–Cobb–Faust, *Likelihood Correspondence of Toric Statistical Models*, Theorems 3.1 and 3.2, already construct toric likelihood ideals and explicit complete-independence Gröbner bases. Their arXiv v3 text was checked directly: https://arxiv.org/html/2312.08501v3 . The source gate records the ISSAC 2026 publication: https://doi.org/10.1145/3815436.3815479 . The derivations in this report are consistency audits and elementary corollaries, not asserted novel theorems.

The historical general question is recovered at https://aimath.org/WWN/compalgstat/articles/html/2a/ and https://aimath.org/WWN/compalgstat/compalgstat.pdf . Its conventions are not sufficient to identify it with the generated 2×2 expected-count question. The correct conclusion is a precise specialization audit plus a general zero-total observation, not resolution of the original general classification.

For finite-presentation families fiber-dimension levels are locally constructible; proper families have upper-semicontinuous fiber dimension. These statements and their hypotheses were checked in https://stacks.math.columbia.edu/tag/05F6 . They support the algorithmic distinction above and do not supply a structural model-by-model answer.

## Acceptance scope

Independently accepted scope: exact open complete-independence fibers; homogeneous toric zero-total theorem; matrix expected-count strata; set-theoretic 2×2 projective closure fibers; specialization counterexample; inverse-variable computational checks. Do not accept a new-general-theorem/novelty claim, certification that AIM Q60 is still open, or a resolution of nonzero-total exceptional fibers for arbitrary A. This package records mathematical results only. The accompanying `exact_checks.py` runs 22 exact rational/symbolic checks; all passed, with results in `exact_check_results.json`. These checks supplement the proofs and do not replace independent review.
