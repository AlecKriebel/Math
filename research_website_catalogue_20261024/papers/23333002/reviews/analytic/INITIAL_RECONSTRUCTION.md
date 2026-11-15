# Paper-first independent analytic reconstruction: row125 /23333002

This checkpoint follows my personal complete reading of the actual four-page PDF, all238 controlling TeX lines and all four fresh individual page images. It precedes every row125 foreign scientific body, supplied scientific program/result, bundled/current scientific opinion and sibling/root review finding. Root's initial gate is closed; scientific conclusions remain local. This is a resumed agent with earlier unrelated reviews, not a newly created blind-agent claim.

Printed identity is12October2026, Version1.0, unrefereed research note. PDF SHA-256eac73f8c53ece8ef5825258327b98fb9e5eda161a0cc9ad18afdd0d3cd61d05c; controllingTeX SHA-2564b7d8c6e3ae68db1d77687f2ae11a41811451588234ca7bd6fc2d32e108cb86f. SOURCE_READY SHA-25691a2924e8c97f248e5ac8c9d5b61f6623c93df30b40d71cdbf852284bb294d1b. Native declared12October and created13October fields are distinct. Sources are unchanged.

Before this initial seal I received ownership metadata only from the independent scope agent: original_packet/author/verify.py,3832B,SHA-25633a61bf0727ff1e9ba80a43bb58a8d03cf8c86cb8d6898e3642fdb59d5fa5709; scope owns its isolated reproduction. Its runtime/dependency availability was mentioned. I did not open that code, any expected result, its isolated copy or any review body. No scientific finding was exchanged. I will not duplicate that native campaign.

## Exact original target and success criteria

Work over the real polynomial ring S=R[x,y,z], with SOS meaning a FINITE sum of squares of real polynomials. For f define J_f by the three tangency minors y f_x-x f_y, z f_x-x f_z, z f_y-y f_z; define K_f by the six separate products y f_x,x f_y,z f_x,x f_z,z f_y,y f_z. The symbol I_R(L) denotes all polynomials vanishing on V_R(L); this is not silently the ordinary radical sqrt(L). The inclusions L subset sqrt(L) subset I_R(L) follow by evaluating powers at real zeros and require no Real Nullstellensatz.

For the explicit homogeneous Robinson sextic R, the full theorem is R>=0 globally and, for BOTH L=J_R,K_R and EVERY real epsilon>=0,

R+epsilon not in SOS+I_R(L).

This is stronger than the two stated consequences: R not in SOS+sqrt(L), and for every epsilon>0, R+epsilon not in SOS+L. The result allows every finite number of summands, each of arbitrary finite polynomial degree. It is not an SDP/Gram failure at a fixed degree. No claim is made about rational sums of squares, denominator multipliers, extra semialgebraic inequalities, truncated tangency certificates or infinite/analytic series of squares.

Additional assertions are: nonnegativity on a real tangency-minor variety is equivalent to global nonnegativity for EVERY polynomial in n variables; the separate-product reading fails even this equivalence for an explicit nonattaining shifted example Q; R itself belongs to its actual gradient ideal by Euler; the zero-line/cubic method is classical; and literal report/catalogue readings and prior positive results must be kept distinct. The exact original Conjecture2/Theorem1 statement and current-paper credit require actual primary reading after this seal.

## Family1: nonnegativity, symmetry and the complete zero pattern

Let a=x²,b=y²,c=z². The displayed F is symmetric and equals

(a-b)²(a+b-c)+c(a-c)(b-c).

Expansion gives a³+b³+c³-a²b-ab²-a²c-ac²-b²c-bc²+3abc, exactly the Robinson form. Ordering a>=b>=c>=0 is legitimate by symmetry. Then a+b-c>=0, a-c>=0,b-c>=0,c>=0, so both terms are nonnegative.

This also supplies an independent zero classification useful for controls. If a>b, then a+b-c>=a>0 and the first term is positive. Thus zero requires a=b. The remaining term is c(a-c)², which vanishes iff c=0 or a=c (including the origin). Undoing the ordering, zeros have either all three squared coordinates equal or two equal nonzero squares and third0. These give precisely four projective all-nonzero directions and six projective coordinate-plane directions, plus the origin. The main proof only needs their inclusion, so no variety-exhaustion claim is being used prematurely.

There are ten DISTINCT real lines, not merely ten isolated test points. Homogeneity makes every u v a zero for realu. Because R is differentiable and globally nonnegative, every such point is a global minimizer and all partial derivatives vanish there. This proves line membership in V_R(K_R) and hence V_R(J_R) for all realu, not just a finite sample.

## Family2: cubic evaluation injectivity without relying on a numerical determinant

Homogeneous ternary cubics have ten monomials. Start with arbitrary coefficients of x³,y³,z³,x²y,x²z,xy²,y²z,xz²,yz²,xyz. Evaluating at (1,±1,0) forces coeff(xy²)=-coeff(x³) and coeff(x²y)=-coeff(y³). Evaluating at(1,0,±1) gives the analogous two relations for xz²,x²z; at(0,1,±1) gives those for yz²,y²z. Therefore any cubic vanishing on those six directions is

A x(x²-y²-z²)+B y(y²-x²-z²)+C z(z²-x²-y²)+D xyz.

At (1,s,t), s,t=±1, this is -A-Bs-Ct+Dst. The four Walsh sign characters1,s,t,st are linearly independent overR; summing against them gives-4A,-4B,-4C,4D. Hence all vanish. This proves rank10 exactly, independent of a determinant sign or monomial-order convention. Multiplying a degree-d homogeneous polynomial, d<3, by x^(3-d) reduces its vanishing to the cubic case; the polynomial ring is a domain, so the original polynomial is zero.

The manuscript's auxiliary determinant value-128 refers to an order in its original proof, not explicitly printed in the note. That literal row/monomial order still needs checking after this initial seal. A determinant under my own different order may change sign; the rank proof above does not assume the stated value.

## Family3: all-degree obstruction from zero lines and axis, retaining constants

Suppose R+epsilon=sum_(j=1)^m q_j²+h with epsilon>=0 and h vanishing on the real variety for either ideal. On each zero line, epsilon=sum q_j(u v)² for EVERY realu. Each summand is nonnegative, so |q_j(u v)|<=sqrt(epsilon). A real univariate polynomial bounded on the full real line is constant. No statement that the constant is0 is justified when epsilon>0.

Write q_j=sum_d q_(j,d) into homogeneous parts. Since q_j(u v) is constant as a polynomial inu, q_(j,d)(v)=0 for everyd>=1 and each of the tenv. Family2 implies that the global degree1,2,3 parts of EVERY q_j are identicallyzero. Higher homogeneous parts may exist and may vanish on all ten lines; they are not assumedzero globally.

The axis(u,0,0) lies in both real varieties because gradientR there is(6u^5,0,0), making every displayed product/minorzero, while R=u^6. Restriction gives u^6+epsilon=sum q_j(u,0,0)². If any restriction has degreeD>3, take maximalD among the finitely many nonzero restrictions. Its u^(2D) coefficient is a nonempty sum of positive squares of real leading coefficients; lower-degree terms cannot cancel it. Hence every nonzero restriction has degree<=3. But its global homogeneous parts in degrees1,2,3 already vanished; each restriction must beconstant. This contradicts u^6+epsilon. If no restriction is nonzero the contradiction is immediate as well.

This is a genuine all-finite-degree/all-finite-m proof. It does not globally truncate q_j or assume they are cubic because R is sextic; an ideal remainder could invalidate such a shortcut. It needs no equality of a radical with a real vanishing ideal, no finite zero variety, and no full primary decomposition of J_R or K_R. The full real vanishing ideal is already the largest allowed remainder in the theorem, so its nonmembership gives every smaller-ideal conclusion directly.

## Family4: analytic/algebraic distinction between the two ideals and actual gradient ideal

Always J_R subset K_R subset G_R, where G_R=(R_x,R_y,R_z). Thus V_R(G_R) subset V_R(K_R) subset V_R(J_R), and the real vanishing ideals reverse these containments. One must not replace either J or K by the gradient ideal in the axis argument: nonzero axis points are NOT gradient zeros.

A concrete independent distinction is v=(2,2,1). Directly R(v)=9 and gradientR(v)=(12,12,6)=6v. Therefore all tangency minors vanish, but the product yR_x=24 does not. So the two real varieties are genuinely different even though the common zero-lines/axis mechanism defeats both certificate readings. No author-intended correction from one ideal to the other follows.

Euler's degree6 identity gives6R=xR_x+yR_y+zR_z, so R belongs to G_R. In fact for epsilon>=0, R+epsilon is SOS modulo G_R by using the constant square sqrt(epsilon)² and remainderR. This is a useful positive control showing the note does not contradict the actual gradient-ideal theorem.

The zero-set classification in Family1 also suggests V_R(K_R) is exactly the ten zero lines plus the three axes: at a point with at least two nonzero coordinates, the separate products force all gradient components0, hence Euler forces R=0; with at most one nonzero coordinate one is on an axis. This is an independently checkable optional classification, not a premise needed by the deposited theorem. J_R has additional positive-value critical directions, as the examplev shows.

## Family5: useful weakening countercertificate and field/degree boundaries

The tenth line is substantive. Remove only the line through(1,1,1) from the ten-zero spine, but keep the x-axis. Define

p=x(x²-y²-z²)+y(y²-x²-z²)+z(z²-x²-y²)-xyz.

It vanishes on all six coordinate-plane zero directions and the other three sign directions, because its all-nonzero values are -(1+s)(1+t). On the x-axis p=u³. Thus h=R-p² vanishes on those nine lines and the x-axis, and R+epsilon=p²+(sqrt(epsilon))²+h is a valid certificate on that WEAKENED spine for every epsilon>=0. At the omitted line, p(u,u,u)=-4u³ and h=-16u^6, so h fails to vanish on the actual required variety. This is a precise falsifier for omitting a zero line or relying on a rank9 evaluation test. It is not a counterexample to the original theorem or a proposed repair.

OverC, a sum of polynomial squares need not be nonnegative and leading-square coefficients may cancel. Indeed anyf is ((f+1)/2)²+((f-1)/(2i))². The real-coefficient hypothesis is essential. Infinite/analytic square series likewise need not have a largest degree; for epsilon>0, sqrt(epsilon+u^6) has a local analytic series, so the polynomial finite-sum condition must remain explicit. The theorem does not cover arbitrary nonconstant perturbations or denominator/SOS multiplier certificates.

Negative epsilon is outside the stated range but would be rejected immediately at the origin; it is not a missing case that can refute the claim. Positive epsilon may force constant values on zero lines, not zero values, which is why the proof retains q_(j,0). These are essential adversarial boundaries, not harmless stylistic distinctions.

## Family6: global nonnegativity versus tangency, all n and no infimum assumption

The implication globalnonnegative=>nonnegativeonanyrealvariety is immediate. Conversely take f(w)<0. If w=0, all tangency minors vanish at0 and one is done, even if gradientf(0) is nonzero. If w!=0, the real sphere of radius||w|| is compact and has nonzero constraint gradient at every point. A minimizerv exists and Lagrange multipliers give gradientf(v)=lambda v; hence ALL minors vanish and f(v)<=f(w)<0. This works for every polynomial and does not assume a globally attained or even finite infimum. In one variable there are no minors, so the variety is the whole line and the equivalence is immediate.

This argument uses tangency MINORS. It cannot be applied to the stricter separate-product equations; their real variety can omit all negative sphere minima. The original report and later primary formulations still require reading to confirm which ideal and certificate equivalence was actually proposed.

## Family7: separate-product diagnostic Q and explicit tangency contrast

For Q=(1-xy)²+y²-1/2, yQ_x=2y²(xy-1), xQ_y=2x[x(xy-1)+y]. The first equation gives y0 or xy1. If y0, the second becomes-2x², forcing x0. If xy1, the second is2, impossible. Thus V_R(K_Q)={0}, where Q=1/2, but Q(2,1/2)=-1/4. The sum-of-two-squares expression before the constant gives infimum>=-1/2; equality would require y0 andxy1 simultaneously. Along(1/u,u), u!=0, Q=u²-1/2 approaches the lower bound. Hence it is genuinely nonattaining.

For an explicit check against conflating the ideals, take positive x,y with x²=15/8,y²=5/24,xy=5/8. Then y/x=1/3, gradientQ=-(1/4)(x,y), so the tangency minor vanishes, while Q=9/64+5/24-1/2=-29/192<0. Thus J_Q does see a negative value, as Family6 requires, whereas K_Q does not. This exact algebraic witness supplies a distinct analytic falsification mechanism and is not borrowed from another reviewer.

## Family8: source identification, prior credit and reproducibility gaps

The actual OWR2007 Conjecture2/811 and Theorem1/810 must be personally read after the initial seal, including the printed replacement formula and original attainment quantifier. Removing an assumption normally enlarges a universal domain to include attaining cases; R is an attaining example and may validly refute an unrestricted statement. But I must not infer an author's intended corrected formula from a catalogue. The manuscript expressly treats the two literal readings and asserts no author-approved correction.

Robinson's form/non-SOS property and Reznick's ten-zero/cubic method are credited classical inputs. The new asserted use is the stronger ideal-remainder and positive-constant obstruction. Exact primary bodies should verify Reznick§4(b)/259 and the same-report Robinson equation798. Sphere/tangency claims are tied to Laurent's UPDATED6February2010 manuscript117–118/Lemma7.21, not casually to the differently paginated2009chapter. Positive gradient-tentacle and truncated tangency results use extra inequalities/multipliers; their actual statements are needed before claiming no conflict. Access to full2008/2009Hà–Pham texts is explicitly limited by the target, and must not be invented here.

Meaningful independent controls can use exact rational polynomial expansion/differentiation, exact evaluation ranks/nullspaces in degrees0–3, explicit omitted-line countercertificate, the positive-value J-not-K point, Q's real product-variety case split and algebraic negative tangency point, and Euler identity. These support the universal elementary proof without using numerical SDP failure or a fixed SOS cutoff. Scope owns the native3832B author verifier; this lane will not duplicate it or execute package-wide historical campaigns/builders.

## Initial exact status/gap table

| Mechanism | Independent support now | Exact remaining check |
|---|---|---|
| GlobalR>=0 and ten whole zero lines | Symmetric ordered identity; zero classification above | Exact coefficient/differentiation controls; classical source credit |
| Cubic and lower-degree injectivity | Six coordinate-zero evaluations plus four sign characters | Exact matrix under explicit own order; literal original determinant order |
| All degrees/all finite m/all epsilon>=0 | Whole-line bounded-polynomial argument and axis leading-square contradiction | No degree-bound search is a premise |
| J/K/G distinction | Inclusion chain, point(2,2,1), Euler positive control | Exact polynomial evaluation controls; actual source printed ideal |
| Hypothesis sensitivity | Explicit nine-line countercertificate and complex-square identity | Exact polynomial checks, not source repair |
| All-n tangency equivalence | Compact sphere/Lagrange proof with origin case | Actual Laurent updated-body interface |
| Q nonattainment/product failure/J contrast | Complete case split and exact algebraic witness | Exact Q expansion; actual prior source and positive-result statements |
| Original question/contribution/priority | Unverified citation and version locators explicitly identified | Actual OWR/Reznick/tentacle/Laurent/GCV bodies; honest access and historical limits |

No substantive defect is established at this initial checkpoint. The universal algebraic argument is independently reconstructed, but acceptance of the full original source-framing claim awaits actual primary interfaces and checkable exact artifacts. If a substantive defect is found, preserve it precisely and defer that promotion; do not undertake extended repair or replace the original claim with a narrower one.
