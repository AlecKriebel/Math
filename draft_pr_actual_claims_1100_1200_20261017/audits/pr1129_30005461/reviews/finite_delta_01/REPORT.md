# Independent finite-algebra / threshold / real-delta adversarial audit

**Verdict: PASS for the assigned interfaces.** No material correction to PROOF.md or REAL_DELTA_APPENDIX.md was found. The principal conclusion remains conditional on the separately audited published Positivstellensatz and section-lifting interface: for each real c<3, all sufficiently large odd powers of f_c are SOS, and the exact thresholds of the original question tend to 3. The optional real-delta calculation is independently valid under the actual v1 definition.

**Material source finding:** the stated Theorems 1.2/6.4 of *Stubborn Polynomials*, arXiv:2602.01191v1, already give the full target after the elementary parameter-wide delta calculation below. This is a deduction from an existing preprint theorem, not a sentence found explicitly answering the threshold limit. It must be separated from a claim of novelty. The principal proof already disclaims novelty and does not import that preprint theorem. I make no priority determination.

## Scope, inputs, and independence

Target: PR1129 / problem30005461 / OWR-12697710-007; frozen head supplied by the parent: `26fed29c1130e539ba018a37200f133870f0e036`.

I read the complete principal proof (10,963 bytes), complete real-delta appendix (3,457 bytes), and complete historical audit (13,253 bytes). Their SHA-256 digests match the supplied pins, reproduced in RESULTS.normal.json and RECEIPT.json. The historical acceptance and historical software claims were not used as authorities. I reconstructed the algebra, threshold topology, and blowups and wrote checker.py independently.

This audit does not re-prove Scheiderer's theorem, certify its geometric applicability or all cohomological references, re-audit the mixed-exponent published proof, or resolve literature priority. Those were assigned to distinct families. No assertion of an explicit odd exponent, convergence rate, uniform exponent over c<3, or SOS endpoint at c=3 is accepted here. No source body, copied extract, screenshot, or raw API response is public in this folder. Fresh source bytes are confined to ignored sources/private/ and renders to ignored tmp/.

## 1. Exact substitution and its entire kernel

Let R=R[A,B,C,D] and define Phi(A,B,C,D)=(x^2 y,xy^2,z^3,xyz). Direct expansion gives

- Phi(ABC-D^3)=x^3 y^3 z^3-x^3 y^3 z^3=0;
- Phi(A^2+B^2+C^2-cD^2)=x^4 y^2+x^2 y^4+z^6-cx^2 y^2 z^2=M_c.

For completeness, ker(Phi) is exactly (ABC-D^3), although the proof only needs containment of that ideal in the kernel. A source monomial A^a B^b C^h D^d maps to exponent triple

(2a+b+d, a+2b+d, 3h+d).

Equality between the images of two monomials forces their exponent difference to be (t,t,t,-3t): subtracting the first two equations makes the A and B differences equal; the first and third then determine D and C. Reduce every source monomial by D^3=ABC until 0<=d<3. Two such normal monomials have D-exponent difference between -2 and 2, so the only possible t is zero. Their images are distinct. Every polynomial has a unique remainder with D degree at most 2 after division by the monic polynomial D^3-ABC, and that remainder cannot map to zero unless all coefficients vanish. This proves the exact kernel without assuming projective image-surjectivity.

All four substitutions have total degree 3. A degree-m homogeneous H becomes degree 3m, its square has degree 6m, and q_c^m has the same degree after substitution. A homogeneous congruence q_c^m-sum H_j^2 in (G) therefore gives the exact identity M_c^m=sum Phi(H_j)^2, with no denominator or multiplier. The cubics have base points [1:0:0], [0:1:0]; the polynomial substitution is defined there and the identity is valid there. No globally defined projective morphism is required.

## 2. Density, all sign patterns, and all boundaries

The claimed real density has a direct algebraic proof. On D!=0 use the unique representative D=1. The coordinate ring is R[A^(+/-1),B^(+/-1)], with C=1/(AB). A Laurent polynomial vanishing on every real nonzero pair (a,b) becomes an ordinary polynomial after multiplication by a monomial. Fix any nonzero b; infinitely many nonzero a force every coefficient in a to vanish at that b. Applying the one-variable identity theorem again gives zero coefficients. Hence the real torus is Zariski dense. The same Gauss-lemma argument as in the input establishes that ABC-D^3 is irreducible, so this nonempty open chart is dense in the surface. This proof does not claim that the cubic parametrization from P^2 is surjective.

For every nonzero real projective representative on ABC=D^3, AM-GM on A^2,B^2,C^2 gives

A^2+B^2+C^2 >= 3 |ABC|^(2/3) = 3D^2.

This is independent of the signs of A,B,C,D. In particular:

- D!=0 and c<3 imply q_c >= (3-c)D^2 >0;
- D=0 implies q_c=A^2+B^2+C^2>0 because the projective tuple is nonzero.

The real boundary consists of ABC=0 in the plane D=0, not only the three singular vertices. The argument covers it all. At a coordinate-chart trivialization T!=0 the local representative is q_c/T^2, so it has the same strict sign. Rescaling a representative multiplies q_c by a nonzero square. Thus the argument verifies positivity of the square-bundle section at all real projective points, including negative coordinates, D<0, the boundary lines, and the singularities.

No lower bound on c is required. For c<=0 the original polynomial is even visibly SOS: f_c=(x^2y)^2+(xy^2)^2+1^2+(-c)(xy)^2. For c approaching 3 from below strictness persists pointwise in c, with a lower bound depending on c. At c=3, q_3 vanishes at all four points with D=1 and A,B,C in {+1,-1}, ABC=1. For c>3 it is negative at [1:1:1:1]. The strict-positive theorem therefore cannot be invoked at the endpoint or above it.

## 3. Parity and eventual propagation

The theorem's output as used in the input is q_c^(N+1)=sum s_j^2 for every sufficiently large integer N. The necessary choice is **N even**, making m=N+1 odd. The square roots have section degree m. Taking N odd gives an even power and cannot establish odd-power SOS. My check validates this interface; the all-sufficiently-large-N quantifier in the actual imported theorem is the geometry-family audit's responsibility.

After an odd SOS power f_c^(2k+1)=sum h_j^2 exists, every larger odd power is SOS by the exact identity

f_c^(2ell+1)=sum (f_c^(ell-k) h_j)^2, ell>=k.

This does not need strict positivity or even nonnegativity as an extra assumption. It preserves arbitrary real coefficients and introduces no rational functions.

## 4. The exact threshold convention, interval property, and closedness

The fresh [OWR 14/2023 source](https://ems.press/content/serial-article-files/47007), physical PDF page 40 / printed page 780, asks about precisely the affine coefficient family f_c=x^4y^2+x^2y^4+1-cx^2y^2 and defines its SOS-power sets as (-infinity,c_k]. I visually inspected that complete page. The different perturbation by a positive multiple of (x^2+y^2+z^2)^3 is a separate paragraph and is not interchangeable with this question.

The fresh [published Blekherman--Kozhasov--Reznick article](https://doi.org/10.1017/fms.2026.10221), PDF pages 23-24, Theorem 6.3, uses M_a=x^4y^2+x^2y^4+z^6-a x^2y^2z^2 and V_(2k+1)=(-infinity,c_k], with k>=0 and c_k in [0,3). The index 2k+1 is the exponent, not k itself. The same publication says c_0=0 and, in the following discussion, still poses the limit question. It was published online 27 April 2026, Volume 14, e65. These are source statements, not new results of this audit.

### 4.1 Homogeneous and affine SOS are equivalent here

Dehomogenization M_c^m(x,y,1)=f_c^m sends any homogeneous SOS to an affine SOS. Conversely, if f_c^m=sum h_j(x,y)^2, each h_j has degree at most 3m: a larger common maximal degree would give a nonzero sum of squares as the top homogeneous part, which cannot cancel to zero over R. Homogenizing each h_j to degree 3m therefore gives an identity M_c^m=sum (z^(3m) h_j(x/z,y/z))^2. The apparent expressions are polynomials because all h_j degrees are bounded. Thus the publisher's thresholds and the original affine thresholds coincide exactly.

### 4.2 Downward closure, with no monotonicity assumption on coefficients

Fix an odd positive integer m and any real polynomial p with p^m SOS. If g is SOS, define the homogeneous binary polynomial

Q_m(t,s)=sum_(j=0)^(m-1) binom(m,j+1) t^(m-1-j) s^j.

It satisfies s Q_m(t,s)=(t+s)^m-t^m. For s!=0, odd-power strict monotonicity makes this quotient positive; at s=0 its value is m t^(m-1)>=0. For m=1 it is the constant 1. Every nonnegative real binary form is SOS, as follows by factoring real roots with even multiplicity and multiplying the positive quadratic conjugate factors with the two-square product identity. Hence Q_m(p,g) is SOS, and

(p+g)^m=p^m+g Q_m(p,g)

is SOS. Apply this with p=f_c and g=(c-a)(xy)^2 when a<c. This proves that every fixed odd-power parameter set is downward closed. It avoids an invalid inference from mere pointwise positivity or from even powers.

### 4.3 Why the finite-dimensional SOS cone is closed

A linear image of the positive-semidefinite cone need not be closed, so that assertion alone would leave a gap. Here is a complete bounded-lift argument.

Let v be the finite vector of all monomials of the fixed square-root degree d (or all monomials of degree at most d for the affine version). Write any SOS polynomial p_j=v^T Q_j v with Q_j positive semidefinite. Set T=integral_([-1,1]^n) v v^T. For every nonzero coefficient vector a, a^T T a=integral (a.v)^2>0: a nonzero polynomial is nonzero on a nonempty open subset of the cube. Thus T is positive definite, with some eigenvalue lower bound lambda>0.

If p_j converges coefficientwise, its cube integral is bounded, and

lambda trace(Q_j) <= trace(T Q_j) = integral p_j.

The trace bound bounds every entry of the positive-semidefinite matrices Q_j. A convergent subsequence has a positive-semidefinite limit Q, and the limiting polynomial is v^T Q v. This proves closedness in precisely the fixed finite-dimensional coefficient space used here. No degree limit tends to infinity during this argument.

Continuity of c -> f_c^m now makes its SOS-parameter set closed in R. The set contains (-infinity,0], is bounded above by 3 because f_c(1,1)=3-c, and is downward closed. It consequently equals (-infinity,c_k] for a finite c_k>=0. The published endpoint-exclusion result gives c_k<3; the convergence proof itself only needs c_k<=3. The exact checker includes the nonclosed generic PSD-image example Q_n=[[1/n,1],[1,n]]: projected coordinates (1/n,1) tend to (0,1), which has no PSD lift. This tests the omitted-boundedness pitfall directly.

### 4.4 Limit and quantifiers

For any fixed c<3, the principal construction supplies an odd SOS power, so propagation gives c<=c_k eventually. Hence liminf c_k>=c for every c<3. Every c_k<=3, so limsup c_k<=3. Taking c upward to 3 proves the limit without selecting an exponent uniform in c.

The quantifier is `for every c<3, there exists K(c), for every k>=K(c)`. Interchanging its first two quantifiers is invalid. For example the model thresholds 3-1/(k+1) have the required pointwise eventual inclusion but omit parameters between each fixed threshold and 3. Moreover, for the actual family a common fixed odd SOS exponent for all c<3 would imply that endpoint power SOS by the just-proved closedness, contradicting the published c_k<3. The proof imports no explicit exponent or convergence rate.

## 5. Optional real delta: complete independent calculation

The only preprint input in this section is the definition in [Stubborn Polynomials v1](https://arxiv.org/abs/2602.01191v1), Definition 6.3, PDF/printed page 20: a center of multiplicity m contributes m(m-1)/2, with recursion over all real first-order infinitely near points of the strict transform; total delta sums local contributions. I inspected that complete page visually and in text. No Del Pezzo classification or resolution criterion is used in this calculation.

### 5.1 Every global real zero

For 0<c<3, AM-GM gives M_c >= (3-c)x^2y^2z^2. A real zero must have xyz=0. If z!=0 and x=0 or y=0, M_c=z^6>0, a contradiction. On z=0, M_c=x^2 y^2(x^2+y^2), which vanishes over R only at P=[1:0:0] and Q=[0:1:0]. These two charts cover every real zero. The argument in fact works for all c<3, but only the claimed range 0<c<3 is endorsed in the optional appendix. No numerical zero search is used as a completeness proof.

### 5.2 Every real direction and all multiplicities over P

On x=1 let u=y, v=z. The initial germ is F_0=u^2+u^4+v^6-c u^2v^2. Its multiplicity is 2, with tangent cone u^2. For each blowup, the two charts u=t v and v=s u cover the entire projectivized real tangent line; their overlap identifies reciprocal nonzero slopes. Divide by the exceptional coordinate to the exact multiplicity 2.

| Center equation | Chart u=t v, divided by v^2 | Exceptional equation | Chart v=s u, divided by u^2 | Exceptional equation |
| --- | --- | --- | --- | --- |
| F_0=u^2+u^4+v^6-c u^2v^2 | F_1=t^2+t^4v^2+v^4-c t^2v^2 | t^2 | 1+u^2+s^6u^4-c s^2u^2 | 1 |
| F_1=u^2+u^4v^2+v^4-c u^2v^2 | F_2=t^2+t^4v^4+v^2-c t^2v^2 | t^2 | 1+s^2u^4+(s^4-c s^2)u^2 | 1 |
| F_2=u^2+u^4v^4+v^2-c u^2v^2 | F_3=1+t^2-c t^2v^2+t^4v^6 | 1+t^2 | 1+s^2-c s^2u^2+s^4u^6 | 1+s^2 |

At each of the first two exceptional divisors there is exactly one real point on the strict transform, slope zero in the displayed vertical chart. The complementary chart's restriction 1 excludes its entire real exceptional divisor, including the direction absent from the vertical chart. The origin of F_1 has multiplicity 2 and tangent u^2. The origin of F_2 also has multiplicity 2, but tangent u^2+v^2. After blowing up that third double center, both exceptional restrictions are strictly positive at every real slope. Thus there is no real child in the recursion beyond it. This is true for every real c; the coefficient c never enters the lowest-degree terms or the exceptional restrictions that determine the tree.

The earlier exceptional curve meets the new exceptional divisor in the complementary direction. At the second step it is the horizontal direction s=0, where the strict-transform equation is 1. At the third step the corresponding check is again 1 at s=0. Older exceptional intersections away from the newly blown-up center are unaffected, and the strict transform already avoids those exceptional parts. Hence there are no unexamined real satellite centers or points at an older exceptional intersection. Equivalently, outside the exceptional divisor each blowup is an isomorphism, so any new point over the original center must occur in the two exceptional restrictions just exhausted.

Each of the three centers contributes 2(2-1)/2=1. Therefore delta_P^R=3. Swapping x and y preserves M_c and exchanges P with Q, giving delta_Q^R=3 with the identical full tree. The complete global total is delta^R(M_c)=6. The two complex slopes at the terminal real double center do not contribute to real recursion. No extrapolation from c=1 or finite sample of parameters is involved.

## 6. Precise prior-theorem bridge and its limitations

This is material to attribution even though it does not affect principal-proof correctness. The actual v1 Theorem 1.2 (PDF page 2) treats nonnegative ternary sextics that are not SOS and classifies stubbornness by the real delta threshold 9. Its Theorem 6.4 (pages 20-21) gives the direction needed here: real delta at most 8 implies some odd power is SOS. Neither statement adds irreducibility, reducedness, absence of nonreal singularities, general position, or an explicit exponent as a hypothesis. Their geometric proofs are imported in this paragraph only; they have not been independently audited here. They remain preprint results in the inspected records.

The elementary bridge checks every stated hypothesis:

1. M_c is a real nonnegative ternary sextic for 0<c<3, by AM-GM.
2. It is not SOS for any c>0. Half its Newton triangle has exactly the four lattice monomials x^2y, xy^2, z^3, xyz. Any SOS square root has Newton polytope within this half-triangle: if a weighted degree outside it occurred, the leading weighted sum of real squares could not cancel, contradicting the support of M_c. In this four-monomial space the coefficient of x^2y^2z^2 comes only from squaring the xyz coefficient and is nonnegative. Its actual coefficient is -c<0. This independently also recovers c_0=0.
3. Section 5 establishes the complete real delta 6, not merely a local lower bound.
4. The preprint's stated theorem therefore supplies an odd SOS power for every 0<c<3. The visible SOS for c<=0 supplies the remainder of the real half-line. Odd propagation and Section 4's threshold argument give all sufficiently large odd powers and limit 3.

This is a **full prior-theorem implication** conditional on that preprint theorem. The inspected preprint explicitly discusses M_1 as an example, while this parameter-wide calculation and the threshold-limit deduction are supplied here. The current published BKR paragraph still asks the limit question, so the source should not be described as explicitly stating the answer 3. Nothing here establishes a new theorem independent of those existing results or resolves who first noticed this particular application.

For the parent's additional complex-singularity cross-check, there is no hidden exceptional c<3. The gradients factor as

M_x=2xy^2(2x^2+y^2-cz^2), M_y=2x^2y(x^2+2y^2-cz^2), M_z=2z(3z^4-cx^2y^2).

Any complex singular point with a zero coordinate is P or Q. On xyz!=0 set u=x^2/z^2, v=y^2/z^2. The equations are E_1=2u+v-c=0, E_2=u+2v-c=0, E_3=3-cuv=0. Let L_1=2E_1-E_2=3u-c and L_2=2E_2-E_1=3v-c. The exact identity

27-c^3=9E_3+c L_1 L_2+c^2(L_1+L_2)

forces c^3=27. No real c<3 satisfies this. At P the analytic unit 1+u^2-cv^2 has a square root; U=u sqrt(1+u^2-cv^2) is a local analytic coordinate and F_0=U^2+v^6. Its two complex smooth branches U=+/-i v^3 have intersection multiplicity 3. The same holds at Q, so the complex delta is also 6. A repeated complex component would make infinitely many singular points, impossible here, hence the curve is reduced. In fact it is irreducible: any coprime split of degrees d and 6-d, 1<=d<=3, could meet only at P,Q. At either point a split can separate the two smooth branches only with intersection multiplicity 3. Bezout would require d(6-d) in {0,3,6}, whereas its values are 5,8,9. This contradiction proves irreducibility without a surface classification. This check is supplementary; the actual v1 real-delta theorem does not require it.

The unversioned arXiv record retrieved during this audit lists only v1, submitted 1 February 2026, and no journal reference. The PDF itself is dated 3 February 2026. A freshly retrieved [author publication page](https://sites.google.com/site/grrigg/) describes the work as submitted for publication. These are current-record observations, not proof that no other publication exists. They are kept separate from the exact v1 definition/theorems used above.

## 7. Exact finite checks and adversarial controls

checker.py uses only Python's standard library, sparse polynomials with exact Fraction coefficients, and explicit failures instead of assert. Both `python3 checker.py` and `python3 -O checker.py` exit successfully and produce byte-identical RESULTS.normal.json and RESULTS.optimized.json: **79,582 explicit checks and 14 negative controls**. The checks are falsification and transcription evidence; the universal arguments are in Sections 1-6.

Coverage includes symbolic substitution with c as an indeterminate; monomial-kernel normal forms; homogeneous degree tripling; parity and odd propagation; every admissible nonzero sign pattern (eight before projective identification), rational torus tests, all sampled boundary types, and square-bundle chart signs; exact half-Newton lattice support; signed divided differences for the downward-interval proof; positive-definite exact cube-moment matrices at several degrees; every blowup chart and exceptional restriction; geometric multiplicities and tangent cones independent of c; and complex gradient/elimination identities.

The adverse controls reject: C=z^2 replacing z^3; erasing c; a substitution with inconsistent degree; choosing odd N; applying AM-GM to signed coordinates instead of squares; claiming strictness at c=3; treating positive even powers as odd-power evidence; exchanging the pointwise/eventual quantifiers; assuming all PSD linear images closed; an even-exponent divided-difference shortcut; dropping the third double center; dividing by too few exceptional factors; omitting the tangent direction at infinity; and trying to locate the unique tangent direction using only the zero-free complementary chart. A separate uv tangent-cone example demonstrates why one finite blowup chart can miss a real direction. The actual finite samples do not establish positivity or chart completeness for all real numbers; the polynomial formulas and universal inequalities do.

## Final disposition

Strongest verified results in this family's scope: the entire ring-map kernel is (ABC-D^3); the projective positivity argument is valid for every real c<3; every degree/parity/propagation and threshold interface is correct; the optional real delta is exactly 6 for 0<c<3 with all real infinitely near points accounted for. Given the principal proof's separately audited geometric theorem and lifting step, its full threshold conclusion follows. There is no remaining algebraic or delta gap. The existing-preprint application described in Section 6 should accompany any discussion of attribution. All authoring, source receipts, input pins, ordinary/optimized results, and public-file hashes are recorded in RECEIPT.json.
