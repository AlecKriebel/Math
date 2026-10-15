# Independent adversarial mathematical audit of PR 905

Problem 30000717 / OWR-1465-011. Audit date: 13 October 2026 UTC.

**Verdict: PASS for the mathematical claims of the frozen v2 proof. No mathematical correction or unresolved proof gap was found.** In particular, the quantifier over every real epsilon >= 0 and arbitrary finite real polynomial SOS is justified. This verdict applies to the two explicitly defined ideals, not to an unverified interpretation of the publisher's ellipsis or to a claim of historical priority.

Reviewed author proof: SHA256 `a2e2109d45f7776103fc43cff554c7f49de1b9290b92dc62b3d3db5ad23050c1`. Historical Audit A, its epsilon supplement and frozen acceptance, and Audit B and its correction log were read as requested. Their favorable conclusions were not used as mathematical premises. The new exact checker imports none of the author or historical audit programs, outputs or polynomial data.

## 1. Exact claim and success criteria

Let S=R[x,y,z] and let R be the displayed Robinson sextic. Define

- J=(yR_x-xR_y, zR_x-xR_z, zR_y-yR_z);
- K=(yR_x, xR_y, zR_x, xR_z, zR_y, yR_z).

For L=J or K, write V_R(L) for its real common zero set, and I(V_R(L)) for all real polynomials vanishing there. The strongest main claim is

`R+c not in Sigma S^2 + I(V_R(L))` for every fixed real c>=0.

The ordinary-radical statement follows because sqrt(L) is contained in I(V_R(L)); the ideal-only positive-epsilon claim follows because L is contained in that vanishing ideal. No reverse inclusion, Nullstellensatz, radical computation, or complete classification of V_R(L) is needed.

The necessary assumptions are real polynomial coefficients, exact equality, finite polynomial SOS as defined in the target, entire real lines in the variety, and a constant perturbation c. There is no bound on ambient degrees or on the number of summands. No attained-global-infimum, genericity, isolated-zero, zero-dimensionality or strict-positivity assumption is imposed on the target replacement conjecture as stated in the supplied record.

Success means a deduction covering those universal quantifiers, supported by checkable exact algebra. A failure of a numerical solver, a low-degree SOS search, or a finite sample of parameter values would not suffice. None is used here.

## 2. Algebra and geometry reconstructed independently

With a=x^2,b=y^2,c=z^2, R becomes the symmetric cubic

F=a^3+b^3+c^3-a^2b-ab^2-a^2c-ac^2-b^2c-bc^2+3abc.

Expansion gives F=(a-b)^2(a+b-c)+c(a-c)(b-c). Symmetry allows a>=b>=c>=0. Then a+b-c>=a>=0 and all remaining displayed factors are nonnegative. Consequently R>=0 everywhere, and R(0)=0. This is a deduction from an exact identity, not an assumption that the classical non-SOS example has the needed positivity.

The ten listed directions consist of four (1,s,t) and two each of (1,s,0), (1,0,t), (0,1,t), for signs s,t in {-1,1}. The new checker recovered them independently as the zero-valued directions among the 13 nonzero sign-normalized directions from {-1,0,1}^3. It did not assume this was the entire zero set.

R(tv)=0 and each partial derivative is identically zero in t on every one of these ten lines. They therefore lie in both V_R(J) and V_R(K). The written proof also correctly deduces gradient vanishing from differentiable global minimality at a zero of a nonnegative polynomial. The arithmetic route verifies the same fact without depending on that deduction.

The first axis is a distinct necessary witness. There R(t,0,0)=t^6 and the gradient is (6t^5,0,0). Every off-diagonal product vanishes on it, as does every tangency difference. This is checked independently for every generator; its membership is not inferred from the ten zero lines. J is contained in K, but the argument does not need to infer either full variety from the other.

For a homogeneous cubic, the six two-coordinate directions impose six independent conditions. Their kernel is the four-dimensional span of

`x(x^2-y^2-z^2), y(y^2-x^2-z^2), z(z^2-x^2-y^2), xyz`.

The values of a linear combination at (1,s,t) are -A-Bs-Ct+Dst. The four sign characters 1,s,t,st independently kill its four coefficients. Hence cubic evaluation at the ten directions is injective. The author's exact row and column order has determinant -128. The exact ranks in homogeneous degrees 0,1,2,3 are 1,3,6,10. Multiplication of a degree-d form, d<=3, by x^(3-d) is legitimate: the product vanishes at all ten representatives, and the polynomial ring has no zero divisors. The two representatives with x=0 cause no difficulty.

## 3. Universal argument, including constants and arbitrary degrees

Fix c>=0. Suppose R+c=sum_j q_j^2+h, where h vanishes on V_R(L). If h belongs only to sqrt(L), there exists an N>=1 with h^N in L; at each real common zero h(w)^N=0, so h(w)=0. Thus the stronger vanishing-ideal setup includes the requested ordinary radical. It also includes the real radical, directly by its defining sum-of-squares identity.

On any of the ten zero lines,

`sum_j q_j(tv)^2=c` for every real t.

Every summand is nonnegative, so |q_j(tv)|<=sqrt(c). A nonconstant real univariate polynomial is unbounded on the whole real axis, by its nonzero leading term. Each restriction q_j(tv) is therefore constant. For c>0 the constants need not be zero. They are retained throughout, and in fact their values are q_j(0) on every line.

Write q_j as the finite sum of its homogeneous parts q_{j,d}. The coefficient of t^d in q_j(tv) is q_{j,d}(v). Since the restriction is a polynomial constant for every t, q_{j,d}(v)=0 for every d>=1 at every listed direction. Cubic injectivity and its lower-degree consequence give q_{j,1}=q_{j,2}=q_{j,3}=0 as polynomials. No claim is made that all higher components vanish.

Now restrict to the extra axis:

`sum_j q_j(t,0,0)^2=t^6+c` for every real t.

There are two independent justifications of the necessary degree bound. The author's proof chooses the maximal nonzero univariate degree D among the finitely many restrictions. If D>3, the coefficient of t^(2D) is the positive sum of squares of the degree-D leading coefficients. Cross terms within a square have smaller degree; lower-degree summands cannot contribute; the ideal term has already vanished on the axis. Cancellation is impossible over the reals.

Alternatively, each individual square is bounded above by t^6+c. If a restriction has degree D>3, dividing by t^(2D) and letting t tend to positive infinity gives a positive squared leading coefficient on its left and zero on the upper bound. This is a contradiction. This argument verifies the degree bound without choosing a maximal ambient degree.

Thus every axis restriction has degree at most three. Its coefficients in degrees one through three are zero because the corresponding homogeneous components already vanished. Every restriction is constant, so their squared sum is constant. The nonzero t^6 coefficient contradicts that conclusion.

This proves nonmembership for every c>=0, with arbitrary allowed SOS size and degrees. An empty sum also cannot equal t^6+c on the axis. The argument even excludes c<0 by evaluating at the origin, although the author theorem requires only c>=0. There is no passage from an epsilon=0 failure to a positive-epsilon failure; the positive-epsilon contradiction is proved directly.

## 4. A second exact proof of the critical interpolation step

The axis can be tested without the full cubic determinant. For every homogeneous p of degree d<=3,

`p(1,0,0) = (1/2) sum_{s=+-1} [p(1,s,0)+p(1,0,s)] - (1/4) sum_{s,t=+-1} p(1,s,t)`.

For cubics this follows by expanding the ten monomials: sign summation removes odd y or z powers, and the x*y^2 and x*z^2 contributions cancel between the two sums, leaving the x^3 coefficient. For smaller degrees, apply that cubic identity to x^(3-d)p. All representatives appearing in this stencil have x=1. The checker verifies the formula on every monomial in degrees zero through three, with rational weights.

Consequently, the eight zero lines with x=1 already force q_{j,d}(1,0,0)=0 for d=1,2,3. Combined with the individually established axis degree bound, this gives the same constant-axis contradiction. It is an independent algebraic cross-check of the author's decisive inference, not a reliance on its reported determinant. No novelty is claimed for this interpolation identity.

## 5. Deliberate attacks and sharp boundaries

| Attack | Check and disposition |
|---|---|
| Discard constants when c>0 | Invalid shortcut. The proof explicitly retains q_j(0). Constancy on a line, rather than zero value, is what kills positive-degree components. |
| Arbitrarily large c | Each fixed c is still a finite bound on the entire real line. A nonconstant polynomial cannot satisfy that bound; no uniform bound in c is needed. |
| Infer homogeneous vanishing from ten point values | Invalid shortcut. The quadratic (x-1)(y-1) vanishes at all ten chosen representatives, but restricts to (t-1)^2 on the (1,1,1) line. The proof uses all real t. |
| Infer all homogeneous components vanish from the cubic lemma | Invalid shortcut. The quartic (x^2-y^2)(x^2+y^2-z^2) vanishes on all ten zero lines but is nonzero, with axis value t^4. Degree-four evaluation has rank 10 in a 15-dimensional space. The author kills only degrees one through three. |
| Use only the zero lines | Insufficient by themselves: R vanishes there, so R+c coincides with a constant square on that restricted set. The extra axis is genuinely needed. |
| Bound the degrees of the ambient q_j by three | Unsupported and unnecessary. High components may survive globally or vanish on the axis. The degree bound is on the univariate restriction only and is deduced from the assumed equality. |
| Cancel high-degree axis terms against h | Impossible after evaluation, because h vanishes identically on the axis. No degree constraint on h is needed. |
| Cancel leading terms among squares | Impossible over R: their maximal-degree coefficient is a positive sum of nonzero squares. Cross terms have smaller degree. Complex or signed sums are different cones. |
| Need the ideals to be radical or their varieties reduced | False. Only h(w)=0 at real common zeros is used; ordinary radical membership implies this by one elementary power identity. |
| Need all real or complex tangency directions | False. The explicitly verified eleven lines suffice. The interpolation cross-check needs only nine of them. |
| Empty sum, zero restrictions, vanishing leading coefficients | Included. Zero restrictions are harmless; the leading coefficient of a nonzero degree-D restriction is nonzero by definition; an empty squared sum is already impossible on the axis. |
| Reuse the actual gradient ideal theorem | Inapplicable. Exact Euler identity gives 6R=xR_x+yR_y+zR_z, so R belongs to its gradient ideal and is trivially certifiable there. J and K are different ideals. |
| Add inequality multipliers or rational denominators | Different representation. Such terms need not vanish on the axis or be polynomial squares with the used restriction properties. The author makes no claim excluding those certificates. |

These attacks falsify several tempting weaker arguments, but none falsifies the argument actually in the frozen proof. The quartic and representative-only controls are explicit counterexamples to shortcuts, not counterexamples to the theorem.

## 6. Sphere minimization: all boundary cases checked

For a real polynomial f in n>=1 variables, the asserted equivalence between global nonnegativity and nonnegativity on its real tangency-minor variety is correct. The forward implication is restriction. For the reverse, suppose f(x_0)<0. If x_0=0, the origin belongs to the variety because each minor has a coordinate factor.

Otherwise set r=||x_0||>0. The radius-r sphere is nonempty and compact, so the continuous f has a minimizer u on it. It satisfies f(u)<=f(x_0)<0. The constraint ||u||^2-r^2=0 has nonzero gradient 2u, so the Lagrange multiplier theorem applies and yields grad f(u)=lambda*u after absorbing the factor two. All x_j f_i-x_i f_j vanish at u, giving a negative point in the variety.

This uses attainment only on a fixed compact sphere, never a global infimum. It works for f unbounded below, constant f, and n=1. In n=1 the tangency ideal has no generators and its variety is the whole line; equivalence is immediate, and the sphere argument still has a regular constraint. No assumption that the tangency variety is smooth is needed; the smooth object used for minimization is the sphere.

The Robinson example does attain zero. Dropping an attainment requirement from a conjecture that quantifies over all polynomials includes such an example. It does not demand a nonattaining example. If the target were instead restricted exclusively to nonattaining polynomials, the main example would not refute that different claim; the supplied exact target makes no such restriction.

## 7. Literal-product nonattainment diagnostic

Independently expand Q=(1-xy)^2+y^2-1/2. The literal generators are

`yQ_x=2y^2(xy-1)` and `xQ_y=2x(x(xy-1)+y)`.

At a real common zero, the first equation gives y=0 or xy=1. If y=0, the second is -2x^2, hence x=0. If xy=1, the second is 2, a contradiction. Therefore its real literal-product variety is exactly {(0,0)}. Q(0,0)=1/2, while Q(2,1/2)=-1/4. Thus nonnegativity on this variety fails to imply global nonnegativity.

Q+1/2=(1-xy)^2+y^2>=0. Equality would force both y=0 and xy=1, which is impossible. For every nonzero real t, Q(1/t,t)=t^2-1/2. Taking t to zero proves that the infimum is -1/2 and is not attained. The missing value t=0 on the path is explicitly excluded; the path is an infimum sequence, not an asserted finite minimizer.

The diagnostic must not be transferred to the tangency-minor variety. An additional independent exact witness makes this distinction concrete: choose x=sqrt(44/15), y=x/4. Then xy=11/15 and y^2=11/60. The tangency minor divided by two equals (y^2-x^2)(xy-1)-xy=0, but Q=-221/900<0. This is consistent with the sphere-minimization theorem, since Q is also negative on its tangency variety. The frozen candidate correctly limits the diagnostic to literal products.

## 8. Reproducibility, evidence classification and remaining scope

Run `python3 check_exact.py` from this review directory. No third-party packages are needed. The checker recognizes a standalone archive's `original_packet` directory when present, otherwise the supplied frozen snapshot layout; in either case it explicitly requires the fixed author proof file and its exact SHA256 above. A missing or changed proof raises an error. Its result is saved as RESULTS.json.

The final checker passes 133 exact controls: two fixed-input guards and 131 algebraic/interpolation controls. Arithmetic uses Python integers and fractions, with no floating point. It constructs the form, derivatives, generators, matrices and witnesses itself. The cubic determinant is -128 in the author's exact declared ordering; ranks are 1,3,6,10,10 in degrees zero through four. The 20 low-degree monomial checks independently validate the interpolation stencil. The Q derivatives, literal branches, values, infimum path and negative tangency witness also check exactly.

Finite controls establish those specific polynomial and linear-algebra facts. The universal nonmembership conclusion is the deduction in Sections 3 and 4, not a computational search over epsilon, degrees or summand count. The sphere proof and nonattainment conclusion are likewise deductions. There are no empirical measurements or model assumptions in this audit.

The original snapshot is preserved and its full recorded file set and hashes are checked in the accompanying manifest. No original file was edited, and this reviewer performed no Git operation, external contact or publication. The historical author and audit verifier programs were not replayed by this family; the new dependency-free controls and written reconstruction provide its independent mathematical evidence.

Reproducibility checks produced byte-identical RESULTS.json under ordinary Python, optimized Python and the standalone `original_packet` layout. The portable fixed-input guard rejected both an altered proof and a missing proof. The workspace snapshot check confirmed all 30 original files and their exact hashes, with no added or missing original file.

Packaging follow-up, 2026-10-13T04:39:38Z: `verify_review.py` and `seal_manifest.py` also support the standalone layout containing root/ORIGINAL_SNAPSHOT.json unchanged, root/original_packet and reviews/proof_family. They select original_packet when present and compare its file table with the snapshot after stripping the fixed `unsolved_math_prioritization/attempts/30000717/` prefix. They retain fixed SHA256 anchors for the snapshot record, author proof, author manifest and public manifest. Both utilities passed in a disposable archive containing all 30 original files and no workspace `original` directory; all normalized input hashes and sealed artifact hashes matched. UTILITY_PORTABILITY.json records the test. The pre-adjustment seal is preserved byte-for-byte as MANIFEST.before_portable_utilities.json. No mathematics, checker bytes, RESULTS.json bytes or original payload changed. The supported publication wrapper runs only check_exact.py; these two utilities remain optional audit tools.

No mathematical gap remains for the explicitly defined J and K claims. Primary-source wording and historical priority are separate scope checks: the supplied reports say the catalogue uses differences while the publisher has comma-separated products and an ellipsis, and the author already preserves that distinction. This family did not retrieve primary sources afresh or perform a full priority search. It accepts no claim of unique intended meaning, first historical discovery, a newly discovered Robinson polynomial, conventional human peer review or formal proof-assistant certification. Those limits do not weaken the self-contained counterexample to the explicit conjecture formulations.
