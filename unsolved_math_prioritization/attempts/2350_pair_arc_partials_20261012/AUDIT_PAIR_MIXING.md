# Independent audit: Bose–Chowla pair mixing and nonlinear retention

Audit date: 12 October 2026 (UTC).

## Verdict

**ACCEPTED UNCHANGED.** The operator-norm theorem, its arbitrary-subset two-source law, the finite-to-continuum nonlinear constraint, and the combined construction-specific retention corollary are correct with their stated uniformity and scope. No correction to either submitted proof is required.

The accepted arithmetic theorem applies to every nonprincipal multiplicative character of the quadratic extension, with no character-order restriction. It proves

    ||K_gamma|| <= sqrt(5 p^(3/2)+2p)+sqrt(2p) <= 4 p^(3/4).

Combining the resulting nonlinear constraint with the separately, independently accepted continuum certificate proves, for the specified canonical Bose–Chowla lifts,

    retained fraction <= 4859/6075 + o(1)
                      = 4/5 - 1/6075 + o(1).

The optional, slightly stronger leading constant

    4/5 - (18-8 sqrt(5))/675

is also accepted. These are uniform asymptotic bounds as the odd field order tends to infinity. No effective threshold, actual sharpness, novelty, arbitrary-Sidon theorem, arbitrary-lift theorem, or resolution of Erdős 864 is established.

## 1. Exact objects and dependency closure

The primary accepted mathematical texts are the [spectral pair proof](SPECTRAL_PAIR_PROOF.md), [retention corollary](RETENTION_COROLLARY.md), [corrected accepted one-vertex dependency](../2350_stronger_partials_20261012/BOSE_FOUR_FIFTHS_PROOF.md) and [continuum proof](CONTINUUM_GAP_PROOF.md). Their public dependency relationships are recorded in DEPENDENCIES.md.

The one-vertex dependency is the [accepted proof](../2350_stronger_partials_20261012/BOSE_FOUR_FIFTHS_PROOF.md), with its [complete independent audit](../2350_stronger_partials_20261012/AUDIT_BOSE_RETENTION.md). In particular, it is the final corrected edition, containing the exceptional-endpoint correction and the everywhere-uniform **upper** degree bound. It is not the superseded original proof.

The continuum dependency has independently been accepted **unchanged** by the separate continuum audit. I read that report and verified its exact accepted proof matches this packet. The complete report is [included here](AUDIT_CONTINUUM_GAP.md). That audit accepts exactly the almost-everywhere nonlinear hypothesis used below, including both rational and optimized conclusions. Its original arithmetic-applicability boundary is discharged by Sections 2–8 of this audit.

This report supplies an independent expanded justification; it is not a replacement proof or a changed edition.

## 2. Rational parametrization and all singular pairs

Use the source notation: F has odd order p, K=F(theta), theta^2=delta nonsquare, and mu is nonzero. For a column b, write

    M_b=mu(theta+b)=u_b theta+v_b.

Then

    M_b(theta+a)=U theta+V,
    U=u_b a+v_b, V=v_b a+u_b delta.

Multiplication by theta+c shows directly that the desired product theta+d is equivalent to

    Uc+V=1, d=U delta+Vc.

Thus a regular pair U!=0 has exactly the stated unique c,d. A singular pair has solutions exactly when V=1; then all p choices of c work and d=c.

If u_b=0, then v_b!=0 because M_b!=0; hence the constant denominator is nonzero and that column has no singular pair. If u_b!=0, the only singular a is -v_b/u_b, and there

    V=(u_b^2 delta-v_b^2)/u_b=-N(M_b)/u_b.

Consequently a p-point singular fiber occurs exactly when N(M_b)=-u_b. There are at most p singular pairs altogether, and at most two with solutions, by the quadratic calculation below. The entire modular variety has

    p^2 - number_of_singular_pairs + p * number_of_p_point_fibers

points, and therefore p^2+O(p) points with an absolute constant. Discarding singular fibers costs O(p) against any fixed bounded weight, uniformly in all seed choices and arbitrary source restrictions.

For genuine positive zero-carry equations these fibers actually contribute nothing: d=c implies B_a+B_b=0. This exact positivity observation is valid for both positive lift conventions. The argument only requires the weaker O(p) bound, so it does not depend on exploiting this extra cancellation.

## 3. Column roots and every degeneracy

Define r_b=theta+1/conjugate(M_b). The numerator identity

    -conjugate(M_b)(a-r_b)
      = 1-a conjugate(M_b)+theta conjugate(M_b)
      = 1-V+U theta

proves the submitted rational factorization at every regular pair.

Writing N=N(M_b), one has

    r_b = (1+u_b/N)theta+v_b/N,
    r_b-conjugate(r_b)=2theta(1+u_b/N).

Because the characteristic is odd, r_b is in F exactly when N=-u_b. If mu=alpha+beta theta, then

    u_b=alpha+beta b,
    N(M_b)=N(mu)(b^2-delta).

The exception equation has degree exactly two and nonzero leading coefficient N(mu). It has at most two roots over every allowed base field, including nonprime fields and characteristic three. No division by u_b was used to count them.

The map b to M_b is injective and never zero. Conjugation, inversion and translation preserve injectivity, so b to r_b is injective. Every remaining r_b has irreducible quadratic minimal polynomial. Two such minimal polynomials coincide if and only if their roots are equal or conjugate. Equality forces the same column; conjugacy gives at most one other column for each fixed column. The collision relation is symmetric, so treating these pairs as an exceptional matching in the Gram matrix is valid.

The collision r_b=-theta is not an omitted case. Column correlations contain only the two column roots and denominator factors; they contain no separate a+theta character factor. Any row phases introduced later are diagonal unitaries and cancel in a Gram calculation. Thus this collision needs no extra exception.

For completeness, distinct columns with u_b,u_b' nonzero actually have distinct denominator roots. Equality v_b/u_b=v_b'/u_b' would force

    N(mu)(b-b')=0,

by cross multiplication, and hence b=b'. Therefore the submitted allowance for combining repeated linear factors is safe but not needed for off-diagonal pairs in this specific family. If such a repeated factor were present, combining local characters while retaining the factor in the modulus would correctly keep the common zero omitted, even if the combined character became principal.

## 4. Dirichlet character construction and unrestricted character orders

For nonexceptional columns with distinct quadratic minimal polynomials, the Gram correlation, up to a scalar of modulus one, is

    sum_a gamma((a-r_b')/(a-r_b))
          gamma((u_b a+v_b)/(u_b' a+v_b')).

The sum omits precisely the roots of the original denominators. Complex conjugation of a unit-modulus character is its inverse, so this orientation agrees with the Gram convention; reversing the columns has no effect on the absolute bound.

At the minimal polynomial of -r_b', evaluation of T at -r_b' identifies its quadratic residue field with K. The local character is gamma. At the distinct polynomial of -r_b, use gamma inverse. On T+a these give the first ratio. Each nonconstant denominator is represented by the linear factor T-v_b/u_b, whose evaluation on T+a is a+v_b/u_b. The corresponding local character is the restriction of gamma, or its inverse, to F*. Nonzero leading coefficients supply only harmless scalar character factors.

The linear factors are retained even when their characters are principal. Extension by zero on nonunits then removes exactly the unavailable a-values. Constant nonzero denominators need no modulus factor. Irreducible quadratics cannot meet these linear factors. The squarefree modulus has total degree at most six.

Most importantly, the resulting Dirichlet character is nonprincipal. Evaluation at either quadratic root is onto all of K, so a nonprincipal gamma gives a nonprincipal character on that full local unit group. By CRT, its coordinate can vary independently of the other quadratic and linear coordinates. No other local character can cancel it. This argument applies to every character order, to characters trivial on F*, to norm-lifted characters, and to arbitrarily high orders. It does not assert a generic nonresonance principle about one shared quadratic factor; all shared-quadratic pairs were explicitly removed and bounded trivially.

### External theorem inspected

I directly opened and inspected the primary exposition:

Swastik Kopparty, *The zeta function, L-functions, and irreducible polynomials*, 13 October 2013, https://www.math.toronto.edu/swastik/courses/rutgers/finitefields-F13/zeta.pdf .

Printed page 3 defines characters for general polynomial moduli and extension by zero; page 4, Lemma 1 gives polynomial degree at most deg(M)-1 for every nonprincipal character; page 5, Theorem 4 and page 6's factorization give inverse roots of absolute value at most sqrt(p). Therefore the coefficient of the degree-one term, which is the sum over monic linear polynomials T+a, is bounded by (deg(M)-1)sqrt(p). This applies to imprimitive characters and to principal local factors in a nonprincipal global character. There is no missing primitivity or irreducibility hypothesis on M.

Only this degree-one coefficient consequence is used for the new spectral theorem. The printed source's later prime-counting manipulations are irrelevant to this deduction. Its application yields the required off-collision bound 5 sqrt(p).

## 5. Matrix norm and subset quantifiers

Split the matrix into good columns and the at most two exceptional columns. The latter matrix has Frobenius norm at most sqrt(2p), hence operator norm at most this quantity.

For the good-column Gram matrix, each row has at most the diagonal and one conjugate partner bounded trivially by p. All other entries have absolute value at most 5 sqrt(p). The absolute row sum is therefore at most

    2p+5p sqrt(p).

The Gram matrix is Hermitian positive semidefinite. Its operator norm is bounded by the maximum absolute row sum, by the Hermitian spectral-radius bound or Schur's test. Taking the square root and using the triangle inequality gives the first claimed norm bound. After division by p^(3/4), its right side is

    sqrt(5+2/sqrt(p))+sqrt(2)/p^(1/4).

Both terms decrease with p, and already at p=3 their sum is less than four. The simplified constant is consequently valid for every odd field order.

For any complex vectors f,h supported on arbitrary row and column sets D,E, with coordinate magnitudes at most one, the actual operator norm yields

    |sum_ab f_a K_gamma(a,b) h_b|
       <= 4p^(3/4) sqrt(|D||E|) <= 4p^(7/4).

Conjugating f if needed converts the written bilinear sum into the usual sesquilinear norm estimate. The sets can coincide, depend on all field parameters, or vary adversarially with p. No distributional assumption on them enters. This is the necessary strengthening beyond an estimate for unweighted row sums.

## 6. Fourier approximation, seams and half-coset carry

For a fixed continuous W compactly supported in the open simplex, its zero extension is continuous across all torus seams. Uniform trigonometric approximation is therefore available. The modular variety has p^2+O(p) points, so replacing W by a uniformly approximating trigonometric polynomial introduces at most (p^2+O(p)) times the uniform error. The product empirical measures on the proposed main term have total mass at most one, giving the corresponding normalized error bound there. These error estimates are uniform in D,E and the seed parameters.

For each fixed Fourier monomial, the a and b factors are bounded diagonal weights. A nonzero fixed frequency k in the c coordinate gives a nonprincipal character chi^k once p^2-1>|k|. Its regular contribution is O(p^(7/4)) by Section 5. Adding back the O(p) singular-fiber contribution remains o(p^2). Its integral in the c coordinate is zero.

When k=0, the unrestricted a,b sum factors exactly into the two restricted empirical Fourier sums. Removing at most p singular pairs changes it by O(p), as does the singular-fiber correction. This gives exactly the stated product empirical main term. The number of modes and their coefficients are fixed while p tends to infinity. One first takes that limit and only then improves the uniform approximation. There is no growing-frequency or field-dependent cutoff assumption.

The phase formula is exact for the integer zero residue represented by B=q: exp(2 pi i k)=1. For the half-integer convention, the added phase is exp(2 pi i k/(2q)), and comparing three sources with one target gives mu=lambda^2 g. More generally the two conventions have mu=lambda^2 g^(2 epsilon), with epsilon equal to zero or one half. This derivation needs no division by two modulo the even number q.

The modular equation makes (B_a+B_b+B_c-B_d)/q an integer in either convention: in the half-integer case the half offsets combine to an integer. Wherever W is nonzero, the source sum divided by q is strictly between zero and one, while 0<B_d/q<=1. The normalized difference thus belongs to (-1,1), and its being integral forces zero. This proves that the modular weighted count is exactly the genuine count. It also shows that the seam and carry boundaries cause no unaccounted mass. Permuting source roles proves the other two pair laws with the correspondingly permuted test weight.

## 7. Limit measures and the finite coverage inequality

The full seed empirical measures converge uniformly in the seed parameters to Lebesgue measure. Indeed each fixed nonzero Fourier character on the affine quadratic line has O(sqrt(p)) sum by the irreducible degree-two case of the inspected Dirichlet theorem; the constant character has mass one. Constant lambda and half-coset factors are phases, and arbitrary generators merely choose another primitive character.

Torus convergence also implies the asserted convergence on the compact interval [0,1]. A small torus neighborhood of the seam bounds the combined mass near both interval endpoints by its small Haar mass plus a vanishing error. Continuous interval tests can be made periodic outside this neighborhood. Thus no atom can hide at either endpoint when selecting positive representatives.

For deleted empirical measures nu_p<=nu_full,p, compactness of finite measures on [0,1] supplies a subsequence converging weakly to nu. Integrating nonnegative continuous tests gives 0<=nu<=dx. Radon–Nikodym then gives nu=d(x)dx with 0<=d<=1 almost everywhere, and testing against one identifies its total mass with the limiting deletion fraction.

On a covered ordered edge, let r be the number of deleted source **roles** and t the deleted target indicator. The seven admissible pairs (r,t), excluding (0,0), give the following values of

    r+t-(2/3) binomial(r,2):

    (0,1):1; (1,0):1; (1,1):2;
    (2,0):4/3; (2,1):7/3;
    (3,0):1; (3,1):2.

Every value is at least one. Counting roles is crucial and correct. Repeated source vertices have identical deletion indicators, and the sum of their three pair-indicator products is still exactly binomial(r,2). Repeated appearances do not invalidate the inequality or require distinct vertices. The independent diagnostic additionally checks all set partitions of the four roles and all covered deletion assignments.

Multiply this exact inequality by any fixed nonnegative smooth interior W and sum. The linear deleted-role contribution is bounded **above** using the corrected accepted per-vertex estimate

    role_degree_i(v) <= p D_i(X_v)+p epsilon_W(p),
    epsilon_W(p)->0 uniformly.

There are at most p deleted vertices in each role, so the aggregate error is o(p^2). Each D_i is continuous; weak convergence then identifies the limit of the upper bound. The target profile D_4 gives exactly the integral of W times d(x+y+z), by the change of variable from target to third source. The accepted exceptional-source degree zero and exceptional-target bounded degree are already included in the uniform upper estimate; no false equality at an exceptional point is used.

Each subtracted source-pair contribution has an actual asymptotic equality from the pair theorem. Product measure convergence is legitimate despite the changing subsets: for continuous H on [0,1]^2, uniformly approximate H by finite sums f_i(x)g_i(y). Each separated integral factors into two weakly convergent integrals, and the measure masses are uniformly bounded. Hence nu_p tensor nu_p converges weakly to nu tensor nu. Applied to the continuous integrated kernel H_W, it yields the terms containing d(x)d(y), and likewise the other two source pairs. Repeated-coordinate diagonal mass causes no hidden limit: it is covered by this product-measure argument and also has at most O(1/p) normalized empirical product mass.

## 8. The almost-everywhere nonlinear conclusion

After dividing by p^2 and passing to the subsequence, the preceding argument gives, for every nonnegative smooth W compactly supported in the open simplex,

    integral W [d(x)+d(y)+d(z)+d(x+y+z)-1
                -(2/3)(d(x)d(y)+d(x)d(z)+d(y)d(z))] >= 0.

All functions are bounded and measurable. The sum map pulls null sets back to null sets locally, by the invertible change of variables (x,y,z) to (x,y,x+y+z) and Fubini, so the target term is independent of the chosen density representative. The positive-test-function characterization of nonnegative distributions now proves precisely the submitted nonlinear inequality for three-dimensional Lebesgue almost every point of the open simplex.

There is no need to choose a new subsequence for each W: the one weak measure limit has already been selected, and all fixed-weight estimates hold along that same subsequence. The argument proves the inequality for any selected test W, hence for all such tests. If preferred, a countable dense test family and uniform boundedness give the identical conclusion.

The optional compactness comment in the source is also correct. The interval 0<=d<=1 is weak-* compact in L-infinity. For each fixed smooth W, the linear terms are continuous in that topology. Each quadratic term uses the continuous two-variable kernel H_W and is weak-* continuous by the same finite-separated-kernel approximation. Thus the intersection of these inequality sets is weak-* closed. This observation is not used to restrict an almost-everywhere inequality directly to a singular curve.

## 9. Closing the retention corollary

The separately accepted continuum theorem applies to exactly the density and almost-everywhere hypothesis established in Section 8. Its measurable smoothing, fixed-function L1 translations, positive level-set argument, and rational six-inequality certificate were audited independently; I read the report and checked exact dependency identity before accepting the combined statement.

To see uniformity, a failure of the stated asymptotic would supply a fixed eta>0 and a sequence of allowed fields, affine seed parameters, either lift choice, and retained sets with retained fraction at least 4859/6075+eta. The compactness argument gives a deletion limit d with integral at most 1216/6075-eta. Section 8 supplies the nonlinear hypothesis, while the accepted continuum certificate gives integral at least 1216/6075, a contradiction. The optional irrational bound follows by exactly the same argument using the stronger accepted continuum conclusion.

Arbitrary translations are absorbed by lambda; unit dilations correspond to changing the generator, since an invertible exponent has an inverse modulo q. All spectral and fixed-frequency estimates were uniform in these choices. If lift conventions vary along the contradiction sequence, one can take a constant-convention subsequence; all constants already cover both conventions separately. No assertion about mixed lattice cosets follows.

All limits occur in the lawful order: first p tends to infinity for fixed test weights and a fixed weak measure limit, and only then the separate continuum certificate refines its smooth approximations for that single measurable density. The proof does not take nonlinear products through mere one-variable weak-* convergence without a continuous kernel, and it does not use field-dependent shrinking weights.

## 10. Fresh diagnostics and integrity boundary

The independent diagnostic was written from scratch for this audit. It imports no producer checker and does not execute a producer verifier. It builds base fields as polynomial quotients, verifies inverses, constructs quadratic extensions, finds a primitive element, and generates discrete logarithms independently. All polynomial equalities, exceptions, singular fibers and lift comparisons use exact finite-field/integer arithmetic. Complex matrix computations use double precision with explicit tolerances; they are supplementary diagnostics, not the proof of RH or the asymptotic theorem.

Each complete run checks:

- 23,304 nonprincipal character matrices at field orders 3, 5, 7, 9, 11, 13, 25, 27, 31, 49, 67, 101 and 257; two nonsquare models are used at order five.
- Every nonzero mu and every nonprincipal character for the tested orders up to nine, and every nonprincipal character for the selected mu values at orders 11, 13, 25 and 27.
- At larger orders, explicit and deterministic sampled characters including quadratic, primitive, norm-lifted, and base-field-trivial characters. Sampling is not presented as exhaustive coverage of all larger fields or parameters.
- Exact parametrization, rational factorization, r-injectivity, norm exceptions, quadratic conjugate-collision classification, distinct linear denominator roots, and singular-fiber counts.
- The off-collision Gram bound, the stated norm bound, the good-Gram absolute-row bound, and bounded complex row/column restrictions.
- 1,196 generator/affine/lift cases at small field orders, checking cubic membership against genuine positive equations, the carry congruence, the integer seam, and exact Fourier phase identities. No positive singular-fiber equation occurs.
- All 15 set partitions of the four roles and all 79 covered deletion patterns on them, verifying the finite coverage inequality including repeated vertices.

Ordinary Python, `-O`, and `-OO` all pass the full diagnostic. Every check uses explicit exceptions and survives optimized modes. The result files record each parameter group and observed bounds, not just a single PASS label.

Independent integrity checks and negative controls passed; the accepted mathematical inputs were not edited. No branch, PR, repository, or other remote state is mutated by this audit.

## Final scope

Accepted are the submitted spectral proof and retention corollary exactly as pinned, closed against the corrected one-vertex theorem and the separately accepted exact continuum certificate. Acceptance does not convert finite diagnostics into an asymptotic proof or expand the theorem beyond the positive canonical integer and single-coset half-integer Bose–Chowla constructions over odd finite fields.


## Public editorial notice

All mathematical statements, proofs, examples, substantive audit arguments and scope limitations are retained. EDITION_NOTES.md describes the nonmathematical editorial changes: updated acceptance history, public dependency links and removal of excluded provenance metadata. The distributed edition is identified by MANIFEST.json. The complete one-vertex dependency and its audits are linked in DEPENDENCIES.md. Diagnostic summaries report checks rather than replacing mathematical proof. Independent internal AI acceptance is not external human peer review or proof-assistant certification.
