# Row143 paper-first independent source/coefficient reconstruction

This body follows complete personal reading of the actual3PDF pages, all192controlling manuscript/paper.tex lines, and3fresh own individual rasters. It precedes supplied scientific README/support/code/results, archived opinions, current peer/root findings and new foreign bodies. The manuscript's assertions about internal audits/priority are seen only as assertions, not evidence. Prior background is general real polynomial/calculus/multilinear algebra and unrelated programme reviews; no record143 scientific opinion was read. The old excluded-row134 opinion exposure was previously disclosed and is neither reread nor imported.

## Exact original target and success conditions

For each m>=1 and positive definite real homogeneous form p of positive integer degree d>=2, let A be the unique symmetric d-linear polarization with p(x)=A(x,...,x). The claim is that some basis z1,...,zm in GL_m(R) satisfies p(zi)=1 and 0<A(zj1,...,zjd)<1 for every mixed ordered tuple, with equality in the requested absolute-value/geometric-diagonal bound precisely for pure tuples. Positive definiteness over all nonzero real x forces even d. The theorem includes all dimensions, repeated arguments, arbitrary real coefficients and nonconvex positive definite forms. It allows near-singular conditioning and does not assert orthogonality, integral unimodularity, final rational unit-diagonal coordinates, semidefinite forms or global priority.

A successful review must verify the full strict original statement, coefficient normalization, exact substitution orientation, all common/column scaling constants, simultaneous epsilon selection and source-question convention. It must not silently replace mixed positivity by an absolute-value-only or non-strict result, assume convexity, or confuse ordered tensor entries with ordinary monomial coefficients. A substantive failure must be preserved rather than repaired into a narrower theorem.

## Family1: ordered coefficients and multinomial normalization

If alpha=(alpha1,...,alpham), |alpha|=d, the ordinary coefficient c_alpha of t^alpha is (d!/(alpha1!...alpham!)) A(e1^alpha1,...,em^alpham). Symmetric ordered expansion counts each permutation of repeated indices; it has no additional multinomial in each tensor entry. Thus after the claimed normalization, ordinary mixed coefficients lie in(0,multinomial(d;alpha)), not necessarily(0,1). The diagonal has multinomial1. The exact Brandes source convention must be personally checked; the title or informal word 'coefficient' does not establish it. Falsifier: p=x^4+12x^2y^2+y^4 has c22=12 but A1122=12/6=2, not12. Any check dropping this factor is invalid.

## Family2: positivity, degree and sphere minimization

For odd d, p(-x)=-p(x), contradicting strict positivity off0; d is therefore even. Compactness of the Euclidean unit sphere in finite dimension and continuity of p give a minimum c>0, at a unit v. Homogeneity gives p(x)>=c||x||^d for every x, including0. This uses positive definiteness, not convexity or a computational certificate. The auxiliary norm is chosen for proof convenience; the theorem does not require its linear change to preserve that norm. Falsifiers: a merely nonnegative form can have c=0, while nonhomogeneous positive polynomials need not obey this radial comparison.

## Family3: common scaling and invariant ratio

Write P=p/c and B=A/c, so P(v)=1 and P(x)>=||x||^d. The unnormalized requested ratio A(xj1,...,xjd)/product_r p(xjr)^(1/d) is invariant under a common positive scale: its numerator scales by c and each of the d denominator factors contributes c^(1/d), giving exactly c, not c^m or c^d. The polynomial gap product_r p(xjr)-A(xj1,...,xjd)^d scales by c^d, so its sign is unchanged. Negative scales are irrelevant and would violate positivity. Unit-diagonal normalization must later use the *original* p, or include c^(-1/d) explicitly.

## Family4: tangent derivative and exact Hessian constant

For u perpendicular to v, g(t)=P(v+tu)-(1+t^2||u||^2)^(d/2) is nonnegative and vanishes at0. Its first derivative gives d B(v^(d-1),u)=0. Its second derivative is d(d-1)B(v^(d-2),u,u)-d||u||^2>=0. Thus Q(u,u)=B(v^(d-2),u,u)>=||u||^2/(d-1), with the exact denominator d-1. No factor d/2 survives this division. Q(v,v)=1 and Q(v,u)=0 for tangent u; consequently Q is positive definite on the full space as well. This is a local property at the minimum, not a claim that p is globally convex. Falsifier: choosing an arbitrary direction rather than a minimum may destroy tangent positivity.

## Family5: an invertible cluster of basis vectors and determinant order

Choose orthonormal w1,...,w_(m-1) in v-perp and wm=0; set xi=v+epsilon wi. In coordinates(w1,...,w_(m-1),v), their matrix has top epsilon I with a zero final column and bottom row all1, so determinant epsilon^(m-1). In coordinates(v,w1,...,w_(m-1)) its sign is(-1)^(m-1). Either way it is nonzero for every epsilon!=0. Mixed tuples correspond to distinct wi somewhere because all m chosen wi are distinct. For m1 the determinant exponent is0 and mixed tuples do not exist. Conditioning degenerates as epsilon->0 when m>1, which the statement expressly permits.

## Family6: expansion of the numerator and diagonal product

For ar=wjr, N_J(epsilon)=B(v+epsilon a1,...,v+epsilon ad) has constant1, vanishing linear coefficient, and quadratic coefficient sum_(r<s)Q(ar,as). Each P(v+epsilon ar) has quadratic coefficient binom(d,2)Q(ar,ar). Therefore F_J=product_r P(v+epsilon ar)-N_J^d has quadratic coefficient d(d-1)/2 sum_r Q(ar,ar)-d sum_(r<s)Q(ar,as). Expanding pair differences gives exactly(d/2)sum_(r<s)Q(ar-as,ar-as), because each diagonal occurs d-1 times. These factors must be checked independently of source code output. Falsifier: confusing the coefficient of epsilon^2 with the second derivative would insert an extra factor2.

## Family7: strict mixed gap, pure identity and simultaneous small epsilon

For mixed J, at least one ar-as is a nonzero tangent vector and Q is strictly positive on it. Every other pair term is nonnegative. Thus F_J has a positive quadratic leading coefficient and is positive for all sufficiently small positive epsilon. A pure tuple has N_J=P(xi) and F_J=P(xi)^d-P(xi)^d identically0, not just to second order. There are finitely many tuples (or equivalently multiindices), so a common epsilon works for all mixed gaps. N_J(0)=1 and continuity/finiteness separately make every numerator positive at that same smaller epsilon. The finite-set step is essential: no uniform epsilon for all p/m/d is being asserted.

## Family8: direct normalized-coefficient mechanism for own-result stage

The actual coordinate coefficient is C_J(epsilon)=N_J(epsilon)/product_r P(v+epsilon ar)^(1/d), defined near0 with positive denominators and numerator. Taking its log near0 should give log C_J=-(epsilon^2/2)sum_(r<s)Q(ar-as,ar-as)+O(epsilon^3). Hence its quadratic *deficit*1-C_J has factor1/2, as opposed to the gap F_J factor d/2. I will complete this direct curve/weighted-variance derivation and meaningful hand controls separately before support/code/results/foreign exposure. It audits the scale constants and removes a possible confusion between a dth-power gap and an actual normalized tensor entry. It must not assume an unproved global tensor Holder inequality.

## Family9: original p normalization and coordinate direction

Set zi=xi/p_original(xi)^(1/d); the positive real root exists by definiteness. Positive individual column rescaling preserves linear independence and gives p_original(zi)=1. Multilinearity divides each ordered coefficient by the product of the corresponding d column scales, including repetitions. If using P instead, a further common c^(-1/d) on every zi is necessary; otherwise the diagonal would remain c. With S's columns zi, old x=S t and new polynomial p'(t)=p(S t); polarization is A'(e_j1,...,e_jd)=A(z_j1,...,z_jd). Substituting S^-1 or transposing this pullback would be a different change and could invalidate a claimed coefficient certificate.

## Family10: boundary and mutant cases

For d2 and p=||x||^2 the clustered normalized columns have mixed Gram entries in(0,1), whereas an orthogonal change has mixed0 and does not satisfy the stronger strict-positivity conclusion. For p=2x^2 in m1, unit normalization requires an irrational column plus/minus1/sqrt2; final rational coordinates cannot be inferred. For semidefinite p=x1^d in m2, any unit-diagonal columns have first coordinates of absolute value1, forcing mixed entries of absolute value1; strict mixed<1 fails. These are hypothesis/exclusion controls, not defects of the stated theorem. Pure tuple equality and the m1 vacuity must remain explicit.

## Family11: rational unnormalized basis, strict openness and no integral extension

Once a real unnormalized S has nonzero determinant, positive N_J and strict polynomial gaps for the finite mixed set, those conditions define an open neighborhood in R^(m*m). Rational matrices are dense, so some rational unnormalized matrix lies in it, regardless of whether p has rational coefficients. This does not make the nonlinear final unit-diagonal scalings rational, nor imply any unimodular integral basis. There is no quantitative conditioning or specified epsilon in the theorem. A finite rational example does not prove this universal existence argument; conversely, inability to approximate radicals rationally exactly would not refute it.

## Family12: critical classical interfaces and bounded novelty

The actual OWR16(2019)Report50 ProblemSession Problem11 on printed3182 must be read with its exact definition of coefficients, repeated-index geometric diagonal product, degree notation and GL(R) substitution requirement. Its literal absolute-value inequality must match the ordered convention, not an ordinary-monomial surrogate. Brandes's JLMS92(2015)393–410 paper must be read for pseudo-diagonal definitions and Lemma2.1's precise quadratic hypothesis/conclusion and any stated higher-degree interface. Degree symbols may differ and must be mapped explicitly. The manuscript's assertion that it answers the question and its23Sep2026 literature-search/no-first-priority assertions are not assumed. Existing raw bodies may be reused by authenticated reference only after both families' actual independent result freezes. No current/archived agreement is evidence of truth.

## Custody, edition and next gate

The entire source108files/14dirs is authenticated, with105manifest payloads+3exactterminals,48regular ZIP occurrences, sole3page PDF/192line controlling TeX. Native version is present string1.0; personal reading finds printed(version1.0) and23September2026. Source-only old printed-null/unread/currentSheet-unobserved flags remain unchanged. Primary/raw/rasters ignores precede all derived-file creation; future external excerpts must stay within those preignored locations. Qualified core is17 originals plus sole authorized405b checkpoint via0f285e35 contract, not18 originals unchanged, with no generated-cache immutability claim. Only own metadata/Poppler preparation has run, exit0 with exact streams retained. No scientific programme/README/support/result/archive opinion/new foreign/current peer/root finding or GET has been exposed/executed. Root143 remains CLOSED.

The printed proof is internally reconstructible and the main constants appear consistent at this stage. This is not a final disposition: separate actual own normalized-curve proof/control results and exact primary question/coefficient interfaces remain to be established before later static support inspection. No narrowed theorem or follow-up is promoted. Default followup null, publication/canonical/AA authority absent.
