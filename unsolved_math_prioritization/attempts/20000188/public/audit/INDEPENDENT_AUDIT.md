# Independent adversarial audit: fixed-camera complex curve residual

Audit date: 2026-10-16. This is an authored mathematical review of the shared first pass, not copied source material. The scope is exactly ../CONTRACT.md.

## Final conclusion

ACCEPTED FOR THE ADOPTED CONTRACT. Scoped disposition: scoped_resolved1/5. The assembled reports give an exhaustive existence and degree classification and necessary-and-sufficient embedded-smoothness criteria, including the common-epipolar-plane family. The finite-component construction is an input-derived algebraic procedure, not an unknown-lift tautology. Computability uses an explicit effective exact-coefficient input model; the geometric assertions themselves hold over C. All four principal mathematical reports and the supplementary sharpness families were independently reviewed, and the exact certificate and monomial-check programs were rerun successfully. No unresolved mathematical obligation was found within this contract.

No claim of novelty, exhaustive literature coverage, or resolution of every interpretation of the broad AIM question follows from this audit.

## 1. Independently derived exhaustive geometric split

Put the two cameras in the normal form

p1([x0:x1:x2:x3])=[x1:x2:x3],
p2([x0:x1:x2:x3])=[x0:x2:x3].

Their centers are c1=[1:0:0:0], c2=[0:1:0:0], and the baseline is B=V(x2,x3). Let the prescribed integral image equations be f1,f2 and the world cone equations F1=f1(x1,x2,x3), F2=f2(x0,x2,x3).

1. If one image is an epipolar line, every world lift lies in the plane through both centers that back-projects that line. Its other curve image must be the corresponding epipolar line. Thus mixed epipolar/non-epipolar pairs and noncorresponding epipolar pairs have no lifts.
2. If both images are corresponding epipolar lines, the allowed world curves are all integral curves in the common plane except lines through either center. A finite candidate list is false in this case.
3. If neither image is an epipolar line, the two integral cone surfaces are distinct. A common surface would force their irreducible equations to agree and depend only on x2,x3; over C an irreducible homogeneous binary form is linear, precisely the excluded common-plane case. Their intersection is consequently a pure one-dimensional complete intersection.
4. Every genuine lift is a support component of that intersection. Any component contracted by a camera is a line through its center. Unless it is B, the other camera maps it to an epipolar line, impossible in this case. Therefore exactly the nonbaseline support components qualify.
5. Normalizing the two image curves and taking the fiber product of their nonconstant epipolar maps produces at least one component, generically reduced in characteristic zero. Generic triangulation identifies these with the nonbaseline cone-intersection components. Thus there is always at least one lift when neither image is epipolar, and all genuine complete-intersection components have coefficient one.

These arguments verify necessity and sufficiency and include possible world curves through centers. Saturation by the baseline ideal removes the baseline component, not the baseline points of any surviving prime curve.

## 2. Degree and multiplicity checks

Let Gamma_i be the image normalizations, E_i their epipolar-pencil base divisors, m_i=deg(E_i), and delta_i=d_i-m_i. For one normalized fiber-product component T write k=deg(T->P1), r_i=deg(T->Gamma_i), so k=r_i delta_i. Pull E_i back to divisors D_i on T.

The triangulation sections lie in M(D1+D2), where M is the pullback of O_P1(1), and are

[a2 s1 : a1 s2 : s1 s2 u : s1 s2 v].

At a point of D_i the section a_i is a unit in a local frame, and u,v never vanish together. Hence their exact common base divisor is min(D1,D2), with no additional zeros. Since triangulation is generically one-to-one, this proves

deg(C_T)=k+deg max(D1,D2),
mult_c1(C_T)=deg(D2-D1)_+,
mult_c2(C_T)=deg(D1-D2)_+,
deg(C_T)=r_i d_i+mult_ci(C_T).

Here multiplicity means the sum of branch hyperplane multiplicities, not number of branches and not intersection length with an arbitrary chosen plane. The divisor of the pulled-back baseline ideal is max(D1,D2). It must not be silently identified with every possible scheme-theoretic baseline intersection length on a singular curve.

Bézout, together with genuine component coefficient one, proves

mu_B=m1*m2+sum_T deg min(D1,D2).

At an image-epipole branch pair with equal epipolar direction, let n1,n2 be branch multiplicities and a,b the epipolar ramification indices. The local normalized fiber product has gcd(a,b) branches, each with pulled-back multiplicities n1*b/gcd(a,b), n2*a/gcd(a,b). Its total correction is min(n1*b,n2*a). Distinct directions contribute zero correction.

Equivalently, for common tangent direction with tangent intersection orders q1,q2, a=q1-n1 and b=q2-n2, so the pair's complete baseline coefficient is min(n1*q2,n2*q1). For distinct tangents it is n1*n2. This equivalence was independently checked; the divisor proof avoids informal claims about generic Puiseux cancellation.

## 3. A mandatory adversarial fixture

Take F1=x1*x3-x2^2 and F2=x0*x3-x2^2. Each image is a smooth conic through its epipole, of epipole multiplicity one. Nevertheless the baseline has scheme multiplicity two, while the only genuine component is the smooth conic

x0=x1, x0*x3=x2^2.

At the generic baseline point x0-x1 is a unit, and the local intersection ideal is (x3,x2^2), of length two. Thus 4=2+2, not the false residual-degree prediction 4-1=3.

The exact primary decomposition is

(F1,F2)=(x1-x0,x1*x3-x2^2) intersect (x3,x2^2).

An independent algebraic proof is as follows. Write h=x1-x0 and f=x1*x3-x2^2, so I=(f,h*x3). Modulo f, the second ideal becomes (x3), while the first becomes (h). The quotient modulo h is the domain C[x0,x2,x3]/(x0*x3-x2^2), so x3 is not a zero divisor there. Therefore (h) intersect (x3)=(h*x3) modulo f, proving the equality. The first factor is prime, and the second is baseline-primary.

At [1:1:0:0] the Jacobian of (F1,F2) has rank one. The residual conic's prime ideal has Jacobian rank two there. Consequently checking only the original two cone gradients would wrongly reject a smooth valid lift. Reduced-component Jacobians are essential.

## 4. Embedded smoothness requirements

For each computed reduced homogeneous curve prime P, let J be the Jacobian matrix of any generating set. The correct projective singular ideal is P+I_2(J), saturated by the irrelevant ideal. Its projective zero set is empty exactly when this selected embedded curve is smooth. Equivalently check the four affine charts. Testing the whole possibly nonreduced cone intersection is incorrect.

For a normalization parametrization phi:T->P3, smoothness is equivalent to both:

- phi is injective on geometric points;
- its differential is nonzero at every point.

A smooth abstract T alone says nothing about singularities of its image. A cusp passes the point-injectivity condition but fails immersion; a node can be immersive at both preimages but fails injectivity. Conversely a proper, injective, unramified birational morphism of the smooth normalization is a closed immersion onto its curve image; equivalently the local branch criterion yields a regular local curve ring.

At a parameter point write alpha=ord(D1), beta=ord(D2). Independent cancellation gives:

- alpha<beta: the image is c1, with branch multiplicity beta-alpha;
- alpha>beta: the image is c2, with branch multiplicity alpha-beta;
- alpha=beta=k>0: the image is an interior baseline point, with branch multiplicity min(k,ord(rho-rho(0))) for the surviving baseline-coordinate ratio rho.

Immersion requires the listed branch multiplicity to be one. Multiple points of the same T mapping to a center or a common baseline point must still be excluded. Comparisons are within one chosen T, not across different candidate components: two smooth candidate curves may intersect without either becoming singular.

A finite exceptional parameter set may be formed from all branch values of the epipolar maps and all epipolar values over image singularities and epipoles. Outside its pullback, the epipolar parameter is a local uniformizer and both image normalization maps are locally injective. Failures therefore occur inside that finite set. Cross-fiber center/baseline collisions must be compared globally within T, not only within one epipolar fiber. A point in this finite set cannot collide with a point outside it: off the baseline equal world points have equal epipolar value, and every center/baseline preimage lies over an image epipole.

## 5. Common-plane family: exact target spectrum

Write world degree d and projection degrees r1,r2. For an integral plane curve not contracted by either camera,

r_i=d-mult_ci(C).

If d=1, the only allowed tuple is (r1,r2)=(1,1), obtained by lines avoiding both centers. For d>=2, the exact feasible tuples are

1<=r_i<=d and r1+r2>=d.

Necessity uses mult_ci<=d-1 and Bézout with the baseline: mult_c1+mult_c2<=d, since an integral degree>=2 curve cannot contain that line. Sufficiency follows from the nonempty open locus of irreducible forms in the linear system of degree d curves having the specified two center multiplicities. The constraints make this system have no fixed curve and a two-dimensional image; it contains z^d,x*z^(d-1),y*z^(d-1), and monomials attaining each required multiplicity, so Bertini irreducibility and the exact-multiplicity open conditions apply.

The smooth spectrum is d=1,r1=r2=1; for d>=2, independently r_i is either d or d-1. Smoothness makes each center multiplicity zero or one. Conversely general degree d curves through exactly the chosen subset of the two centers are smooth, including conics through both centers.

## 6. Effectivity and scope constraints

All geometric statements hold for complex coefficients. An actual terminating computation requires a finite effective exact coefficient representation and absolute factorization/decomposition. Algebraic-number coefficients with geometric decomposition over their algebraic closure are a safe explicit model. Approximate floating-point data or unspecified arbitrary complex constants cannot support exact equality, decomposition, or smoothness decisions.

The explicit radical/minimal-prime construction from (F1,F2), followed by a finite Jacobian emptiness test on each candidate, is a real input-derived criterion. It is not a restatement that an unspecified lift must exist. It is also a standard computational-algebra method, not a novelty certificate.

The adopted contract covers complex fixed full-rank pinhole cameras, distinct centers, and reduced integral closed image/world curves. It does not settle unknown cameras, real visibility, arbitrary camera models, positive characteristic, nonintegral input conventions, or every intended reading of the original informal problem. Any acceptance status must preserve that distinction.

## 7. Current artifact review status

- The adopted mathematical contract and prior-result screens were reviewed in full.
- global/GLOBAL_CLASSIFICATION.md: read in full; geometric, degree, baseline, and small-resolution arguments passed independent checking.
- local/EMBEDDED_SMOOTHNESS_CRITERION.md: read in full; cancellation, branch multiplicities, global separation, finite exceptional-set reduction, and reduced-prime Jacobian criteria passed.
- exceptions/EXCEPTIONAL_CLASSIFICATION.md: read in full; exact numerical spectrum, family dimensions, irreducible-and-reduced general-member argument, smooth existence, and baseline branch formula passed.
- algorithm/authored/FINITE_ALGEBRAIC_CRITERION.md: read in full; finite list, geometric decomposition requirement, center Hilbert-Samuel correction, raw cycle degree, and selected-prime smoothness algorithm passed.
- algorithm/authored/PRIOR_ART_AND_MONODROMY_AUDIT.md: read in full; its clean-case deductions and narrow prior-art claims are consistent with the adopted scope. This reviewer did not independently repeat every scholarly-PDF retrieval reported there.
- local/SHARPNESS_FAMILIES.md: read in full; the all-degree smooth baseline-tangent family, its constant-ratio cusp control, and all positive center-multiplicity family were independently checked. The degree-3/4 instances are also certified by E13.
- exact/EXACT_EXAMPLES_AUDIT.md: read in full; coordinate conventions, certificate methods, prime examples, and the exact scope of E12 agree with the script.
- exact/certify_examples.py: read in full and rerun; all 13 fixture groups passed under Python 3.12.14 and SymPy 1.14.0. The fixtures are checks, not substitutes for the proofs.
- exceptions/check_monomials.py: read in full and rerun; all 430 allowed multiplicity tuples of degrees 1 through 12 passed exact count and witness checks.
- The invoked Bertini statement was independently opened at https://stacks.math.columbia.edu/tag/0G4C (Lemma 37.32.3). Its codimension-two and no-fixed-divisor hypotheses apply exactly as stated in the exceptional-family proof.

The small-resolution description in the global note is sound: the blowup of the two disjoint camera centers resolves the camera pair, is an isomorphism over the epipolar incidence threefold except at its node, and contracts the strict baseline to that node. Copies of image curves inside exceptional divisors are not genuine world curves. In the common-plane case the exceptional lines can lie inside the strict transform of the common surface, so they should not invariably be called separate one-dimensional components.

## 8. Adversarial findings resolved before acceptance

1. A finite decomposition cannot handle a common cone surface. The assembled classification separates the matching-epipolar-plane family and supplies its full numerical and smooth spectra.
2. One epipolar line paired with a different curve has no lift. This is proved explicitly, rather than hidden in an elimination filter.
3. Smooth image epipoles can produce a multiple baseline. The doubled-baseline conic fixture and exact divisor formula rule out the incorrect product-only subtraction.
4. A smooth normalization is not a smooth embedded curve. Both injectivity and immersion are proved and made finite; the independent prime-Jacobian route gives an alternate exact certificate.
5. Jacobians of the original cone equations can falsely reject smooth selected components. All accepted tests use the reduced individual prime or its actual normalization map.
6. Baseline saturation must retain center/baseline points of nonbaseline components. The prime-level saturation argument does so.
7. Product saturation was initially described too broadly as incorrect. The report now states accurately that it is a different general operation, happens to retain the same candidates in the neither-epipolar branch, and is not a uniform substitute across the common-plane family. Exact fixture E12 belongs to that exceptional family.
8. Exact effectivity requires a represented coefficient field and absolute decomposition. The final reports state this and do not imply that approximate arbitrary complex input admits exact decisions.
9. Exceptional-divisor curves in a resolved correspondence are not valid world curves; in the common-plane case some such lines are contained in the surface rather than separate curve components.
10. Standard algebraic algorithms and clean-case monodromy are credited as prior methods. Acceptance is confined to this deliberately quantified residual and supplies no novelty or exhaustive source-status claim.

## 9. Decision criterion versus implemented software

The accepted result is a proved algebraic decision criterion with standard terminating subroutines under the stated effective exact-input assumptions. It is not a claim that a general-purpose camera reconstruction program, absolute primary-decomposition engine, normalization engine, or arbitrary-input smoothness solver was implemented in this pass. The implemented software consists of the disclosed finite exact fixture suite and monomial-combinatorics checker. Their successful runs certify the listed examples, while the written arguments establish the universal statements.

The frozen audit manifest records the exact reviewed artifact hashes, file sizes, scope, command results, and this distinction. New edits to a recorded artifact require review before its old manifest entry is treated as acceptance of the new bytes.

This is a mathematical acceptance report. Its scope and implementation limits remain binding in the public edition.
