# Independent mathematical acceptance audit: compactly supported Nijenhuis types

Date: 10 October 2026.
Target: problem 2100509 / AMR-020-0509, identified by the compact-support question in Problem 5.11 of arXiv:1804.03737v2.

## Verdict

**ACCEPTED as a complete mathematical solution of the stated smooth classification problem.** No mathematical gap was found in the accepted proof. The distributed [mathematical report](MATHEMATICAL_REPORT.md) is 10,006 bytes, SHA-256 `b8dda0f0c82f5f0f8bd0c8de608b2a6ddee4e11b4267311ba0ef1d8aedf4486f`. Its mathematical statements, analytic arguments, examples and scope qualifications are preserved in full. This audit is AI-assisted and unrefereed.

The exact conclusion is: a real Segre/Jordan type in dimension n >= 1 occurs on a nonempty open set of R^n for a globally smooth compactly supported Nijenhuis endomorphism field if and only if its spectrum is entirely real. Arbitrary real eigenvalue equality patterns and arbitrary Jordan block sizes are admitted. This is stronger on the existence side than a purely qualitative type realization, because arbitrary specified numerical real eigenvalues can be held constant on the realization domain.

Acceptance is of the proof and its cited prior theorem, not a certificate of bibliographic novelty, present-day openness before this work, formal proof-assistant verification, or external peer review. The nonreal obstruction, real semisimple cases, and size-two examples remain credited prior results.

## 1. Scope audit

The realization domain may be chosen after constructing the tensor. Its type need not persist outside that domain. The proof uses exactly that permission: its transition regions have deliberate eigenvalue collisions and Jordan-block splitting, and its exterior is zero. No global regularity or constant-rank assumption is being smuggled into the problem.

The problem is about the algebraic type of a tensor, hence is invariant under a smooth change of frame or coordinates. A prescribed Jordan matrix in a local commuting frame suffices. It need not remain the same matrix in the ambient Cartesian frame. The torus collar is connected and open in R^n; if “domain” is understood to require an ordinary coordinate neighborhood, a small ball inside the central collar provides one.

Constant numerical eigenvalues on the central domain are allowed. The source's surrounding examples permit nonconstant eigenvalues; they do not require them. Independently, Section 2.2 of *Nijenhuis Geometry* explicitly defines Segre type by the block grouping and sizes rather than specific numerical eigenvalue values. In any event, the construction even allows arbitrary fixed real numerical choices.

The theorem makes no claim about nonzero real-analytic compactly supported fields. The n=1 case is treated separately. The identically zero type is admitted, and the zero tensor already realizes it.

## 2. Independently derived torsion calculation

Let m=n-1. On T^m x I let e_1,...,e_m be the invariant angular translation vector fields, and let v=partial_t. These fields form a global commuting frame. The notation dtheta_i denotes a global invariant 1-form, although theta_i is only a locally real-valued angular coordinate. There is no requirement of a global real-valued coordinate chart on the torus.

For A:I -> Mat_m(R), b:I -> R^m, and lambda:I -> R, define

    L e_i = sum_a A_ai(t)e_a,
    L v   = sum_a b_a(t)e_a + lambda(t)v.

For angular indices i,j, all four bracket expressions in N_L(e_i,e_j) vanish. For an angular vector e_i and v, the defining brackets give

    [L e_i,L v] = -lambda sum_a A'_ai e_a,
    [L e_i,v]   = -sum_a A'_ai e_a,
    [e_i,L v]   = 0,
    [e_i,v]     = 0.

Therefore

    N_L(e_i,v) = (A-lambda I)A' e_i.                 (A)

Tensoriality and skew-symmetry account for every component. In particular, the condition is the ordered product `(A-lambda I)A'=0`, not `A'(A-lambda I)=0`. Terms involving b', lambda', or [A,A'] are not omitted: the displayed brackets show why none survives. No diagonalizability, constant rank, or invertibility is used.

The independent audit derives the identity directly from the defining brackets above. Recorded finite checks also evaluated Lie brackets from their definition rather than assuming (A).

## 3. Finite path for arbitrary real Jordan data

### 3.1 Initial invariant hyperplane

Place any real-spectrum Jordan representative J in upper-superdiagonal convention, reorder whole blocks so a chosen block is last, and designate the last vector of that block as v. The span of the remaining vectors is J-invariant. Consequently

    J = [[A_0,b_0],[0,lambda_0]],

and A_0 is a block sum of the other Jordan blocks and the final block shortened by one vector. A shortened size-one block disappears. The central full matrix, including b_0, is exactly J, so no Jordan multiplicity is lost at the realization stage.

### 3.2 Detaching the transverse vector

Keeping A=A_0 and lambda=lambda_0 constant while smoothly changing b_0 to zero satisfies (A) identically. This is a valid change outside the central plateau even when it splits the distinguished Jordan block. It does not make a claim about preserving the type throughout the support.

### 3.3 Choosing an active real block

For each angular Jordan block B=mu I_d+K, lambda can be moved to mu while A stays constant. This remains legal regardless of the eigenvalues of all other blocks. In particular, coincidence of lambda with another eigenvalue creates no denominator, inversion, or regularity issue.

### 3.4 Arrow deletion order

Write K=sum_{j=1}^{d-1} a_j E_{j,j+1}. With lambda=mu,

    (B-lambda I)B' = K K'
                   = sum_{j=1}^{d-2} a_j a'_{j+1} E_{j,j+2}.

Change a_1 from 1 to 0 first, then a_2, and so forth. When a_{j+1} varies, the preceding a_j is identically zero. The derivative of a_1 has no preceding factor. Thus every summand vanishes on every stage, in every block size. No simultaneous uncontrolled interpolation is used.

The direction of the deletion is essential. For instance, deleting E23 before E12 in a three-dimensional angular block gives a nonzero E13 term. This false variant was included as a negative computational control.

### 3.5 Scalar drift and other blocks

After deleting all its arrows, the active block is mu I_d. Let its scalar value c(s) move from mu to zero and set lambda(s)=c(s) on the same stage. The active diagonal block of A-lambda I is then zero, and A' vanishes in every other block. Since A remains block diagonal, there is no off-block cross term. The whole product in (A) is zero.

Previously processed blocks can stay zero while lambda later changes; their derivatives are zero. As-yet unprocessed blocks can keep their original matrices for the same reason. Repeated eigenvalues, positive or negative eigenvalues, zero eigenvalues, and size-one blocks are all covered. If mu=0, the scalar stage is simply constant. The finite list terminates with A=b=lambda=0.

### 3.6 Smoothness of the schedule

There are finitely many operations. Put each on a separate interval and replace its interpolation parameter u by a C-infinity step that is constant near both endpoints. Thus every stage is constant on neighborhoods of its endpoints, and adjacent stages have exactly matching values. Concatenation is C-infinity without any later smoothing operation that could destroy (A).

Polynomial identities checked in the raw parameter u remain true under the step replacement: A' acquires a scalar factor u'(s), and (A) is homogeneous of degree one in that derivative. There is no bound on allowable derivatives in the question, so fitting finitely many stages into [0,1] poses no problem.

The resulting path is constant J near s=0 and zero near s=1. Composing it with a smooth even q(t), equal to 0 near t=0 and 1 near the two ends of the collar, preserves (A) by the chain rule. This is the safest formulation of mirroring: no nonsmooth absolute-value corner is introduced. The alternative use of |t| is also valid if explicitly protected by a constant central plateau. Reflecting coefficients in a fixed collar frame must not be confused with pulling back the tensor by the reflection, which would change the transverse off-diagonal signs.

## 4. Same-dimensional torus collar and zero extension

The embedding T^{n-1} -> R^n exists for all n>=2. This is not an appeal to a high-codimension standard product torus. One proof starts with S^1 in R^2. If f:T^{d-1}->R^d is a smooth embedded hypersurface with unit normal nu, regard it as lying in R^d x {0}. Its rank-two normal bundle has the explicit frame (nu,0),(0,1). A small tubular disk bundle is therefore T^{d-1} x D^2, and its boundary is an embedded T^d in R^{d+1}.

To check the geometry more concretely, for small epsilon the next embedding is

    F(p,phi)=(f(p)+epsilon cos(phi)nu(p), epsilon sin(phi)).

The original tubular chart makes F injective: its first component determines p and cos(phi), and the last determines sin(phi). Its differential is injective because the tubular coordinates recover dp and -epsilon sin(phi)dphi, while the last component recovers epsilon cos(phi)dphi. Compactness then upgrades the injective immersion to an embedding. A global unit normal is

    (cos(phi)nu(p), sin(phi));

its orthogonality follows from nu being orthogonal to df and dnu. This also confirms two-sidedness at every induction step.

A small normal collar of the resulting T^{n-1} is diffeomorphic to T^{n-1} x (-1,1), after transverse rescaling. The pushforwards of the product frame still commute because diffeomorphisms preserve Lie brackets.

The constructed tensor vanishes for |t|>=3/4 inside this open collar. Its support is therefore contained in the image of the compact set T^{n-1} x [-3/4,3/4]. That image lies strictly inside the collar. Extending by zero is smooth because the tensor is already identically zero on an open overlap with the exterior, rather than because some finite number of derivatives happens to vanish at an edge. Naturality and locality of torsion prove N_L=0 throughout the extension. No global extension of the angular frame is needed.

For n=1, a bump function times the identity with the prescribed central scalar value suffices; the alternating vector-valued 2-form N_L vanishes automatically.

## 5. Nonreal obstruction: precise prior theorem

The necessary direction uses Bolsinov–Konyaev–Matveev, *Nijenhuis Geometry*, arXiv:1903.04603v2, Theorem 6.1, PDF page 41, published in Advances in Mathematics 394 (2022), 108001. It asserts persistence, with fixed algebraic multiplicity, of each nonreal eigenvalue across a closed connected manifold carrying a Nijenhuis field.

The source statement was independently read in the primary arXiv HTML and in a rendered image of PDF page 41. It has no assumption of analyticity, global gl-regularity, fixed Jordan type, or a nonreal eigenvalue at every point to begin with. The real-analytic discussion just above it finishes a different preceding proof. Applying that discussion as an extra hypothesis of Theorem 6.1 would be a mistake.

For a compactly supported smooth field on R^n, push it through the standard chart R^n=S^n minus one point and declare it zero near the missing point. Compact support means it is already zero on an entire neighborhood of that point. The extension is a smooth Nijenhuis field on the closed connected S^n. If a nonreal eigenvalue existed anywhere, the cited theorem would force it to exist at the point where the field is zero, a contradiction.

Thus the obstruction applies at every point, not merely to a generically regular stratum. Combined with the construction, it excludes exactly the remaining types. This audit relies on the published theorem; it does not claim to reprove all of *Nijenhuis Geometry*.

## 6. Recorded supporting checks and negative controls

The independent audit records exact symbolic checks of all 254 ordered positive block compositions in dimensions 2 through 8, for 2,688 individual stages. Each block has its own independent formal eigenvalue symbol, so equality or zero specializations are covered by the same polynomial identities. For every stage it checks endpoint agreement with the previous stage, (A), and final equality with zero. For dimensions 2 through 5 it additionally evaluates all torsion components through the Lie-bracket definition, totaling 192 directly checked stages.

The test also detects three intentionally invalid modifications:

1. Reversing the first two arrow deletions in a size-three angular block gives a nonzero E13 component.
2. Multiplying a size-three angular nilpotent block by one scalar cutoff gives a nonzero u E13 component in the raw parameter.
3. Moving an active scalar block without matching lambda produces a nonzero polynomial.

The recorded result is PASS. These finite exact checks support the algebra and catch indexing or schedule mistakes; the general-dimensional proof is the argument in Sections 2–4, not extrapolation from finite testing. Programs and raw computational outputs are not distributed, and no excluded file is a premise of any mathematical conclusion. Edition preparation did not rerun these checks.

## 7. Source identity, attribution, and bounded literature review

The exact original source is by A. Bolsinov, V. Matveev, E. Miranda and S. Tabachnikov. The present arXiv v2, dated 14 January 2020, has the compact-support problem as Problem 5.11 on PDF page 29. The earlier v1, dated 10 April 2018, has it as Problem 4.10 on PDF page 37. Both pages were independently visually inspected. The corpus label 5.9 is not silently used as the locator of either inspected version.

The source itself credits the semisimple real and two-dimensional Jordan examples and the exclusion of nonreal eigenvalues. The audited proof preserves this distinction. The constructive argument is presented without an unsupported priority claim. No mathematical correction was needed for acceptance.

A bounded public search on 10 October 2026 combined Nijenhuis with compact support, compactly supported, Segre, Jordan, torus, classification, and primary authors. It located no directly matching later complete compact-support classification. The 2024 research-problem survey was also checked; its full-page searches for “compact support” and “compactly” produced no match. Two 2026 primary papers were read to distinguish their claims:

- Akpan–Manenti, arXiv:2607.04913v1, 6 July 2026, studies local three-dimensional gl-regular normal forms. Its Bolsinov-conjecture result is a local real-analytic normal-form statement. It does not supply the compact-support construction.
- Akpan, arXiv:2609.05103v1, 4 September 2026, relates local two-dimensional normal-form classifications. It likewise does not supply a global compact-support classification.

Search-engine crawl dates were not treated as scholarly publication dates. The search is not exhaustive and does not prove novelty or current openness. The mathematical acceptance does not depend on such a claim.

## Primary references

1. A. Bolsinov, V. Matveev, E. Miranda, S. Tabachnikov, *Open Problems, Questions, and Challenges in Finite-Dimensional Integrable Systems*: https://arxiv.org/abs/1804.03737v2 ; earlier version https://arxiv.org/abs/1804.03737v1 .
2. A. V. Bolsinov, A. Yu. Konyaev, V. S. Matveev, *Nijenhuis Geometry*: https://arxiv.org/abs/1903.04603v2 and https://doi.org/10.1016/j.aim.2021.108001 .
3. A. V. Bolsinov, A. Yu. Konyaev, V. S. Matveev, *Research problems on relations between Nijenhuis geometry and integrable systems*: https://arxiv.org/abs/2410.04276v1 .
4. D. Akpan, M. Manenti, *On three-dimensional gl-regular Nijenhuis operators*: https://arxiv.org/abs/2607.04913v1 .
5. D. Akpan, *From quadratic integrals to Nijenhuis operators: two-dimensional dictionary*: https://arxiv.org/abs/2609.05103v1 .
