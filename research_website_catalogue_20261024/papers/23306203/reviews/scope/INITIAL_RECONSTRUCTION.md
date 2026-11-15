# Row129 paper-first scope reconstruction

This checkpoint follows my personal reading of all5 actual published PDF pages, every307 controlling TeX line and all5 own fresh individual page rasters. No target supporting scientific code/results, current sibling/root findings, archived inventory/audit opinions or newly opened foreign primary body were used. Earlier source acquisition was neutral metadata/opaque custody only. Prior related row116 focal-pedal-area scientific/literature work is disclosed; this is a fresh target reconstruction, not a claim of wholly new blind background. Parent supplied only native-checker ownership metadata: sol_110_adversarial owns any selected replay. Root129 gate remains CLOSED, so findings remain local.

## Exact hypothesis, identity and success conditions

The actual title is An exact period criterion for focal-distance products in elliptic billiards. The PDF prints Alec Kriebel and11October2026, declares unrefereed/AI-assisted status, and prints no version identifier in any of its5 pages; the entire controlling TeX likewise dates the paper without a version. Native API version1.0.0 is a separate metadata fact. SourceREADY, all raw objects/headers and historical unread flags remain immutable.

Fix a>b>0,A>B>0,a>A,b>B and a²−b²=A²−B²=c²>0. Boundary and caustic are strictly nested confocal ellipses, not hyperbolas, degenerate segments or a circular boundary. Fix a periodic family of genuine elastic billiard trajectories tangent to the caustic, with least vertex period n. Products D_n^± multiply ordinary positive Euclidean distances to one fixed focus F±=(±c,0) over the complete n vertices. This is neither a product of squared distances, signed distances, distances to a moving focus, nor an arbitrary nominal return length.

The full asserted theorem is constancy in phase iff n≡2 mod4, including all admissible primitive star windings and both orientations. For every even n the products at the two fixed foci agree at each phase, even when they are nonconstant. Every r-fold traversal,r≥1,gives (D_n^±)^r and preserves the same primitive-period constancy class. The separate circular case has coincident center foci and product a^N for every listed length. If N≡2 mod4 is only a return length, invariance holds exactly when its least period is even. A specific doubled primitive triangle supplies a physical failure of the unqualified return-length reading. Positive constant value and complete divisor inventories are also asserted.

The target source interface is the unproved k114 entry in RGK's exact2020 preprint/2021 article, whose period convention is stated to be ambiguous. The paper claims a proof/classification within this ordinary strictly nested elliptic setting, not novelty of Jacobi parametrization, divisor/pole-removal methods, an arbitrary-caustic theorem, validated numerics, formalization or exclusive historical priority. Every such distinction must survive final review.

## Family1 — real parameter and dimensional/category checks

Set k=c/A, so0<k<1 because A²=c²+B² with B>0. Let K=K(k),K'=K(sqrt(1−k²)). Since0<B/b<1 and cn decreases from1 to0 on(0,K), there is a unique v with cn v=B/b. The claimed axis formulas b=B/cn v,a=A dn v/cn v respect confocality:
(A² dn²v−B²)/cn²v=A²k²(1−sn²v)/cn²v=c².
They also yield strict nesting since dn v>cn v>0. P(u)=(-a sn u,b cn u) parametrizes all real boundary points exactly modulo4K, using the strictly increasing real amplitude. All Jacobi functions here use modulus k; a numerical library's parameter m would be k². This square is a required falsifier, not a harmless convention change.

The focal squared-distance identity follows without elliptic identities: for x=−a sn u,y=b cn u and c²=a²−b², (x∓c)²+y²=(a±c sn u)². Since a>c and |sn u|≤1, the factors g±=a±c sn u are strictly positive, so no sign/square-root ambiguity survives. D_n has physical length dimension n and the paired formula has m factors of dimension2 when n=2m. Uniform scaling of all axes/focal distances multiplies D_n by scale^n, preserving phase constancy.

## Family2 — actual tangency and elastic reflection, not only Poncelet closure

At Q(U)=(-A sn U,B cn U), the caustic tangent is −x sn U/A+y cn U/B=1. Substituting P(U±v) with the addition formulas cancels odd terms and leaves [dn²v sn²U+cn²U]/[1−k²sn²U sn²v]=1. The denominator is strictly positive on the real locus. Strict nesting puts the tangency point inside the boundary chord, so these are actual chord endpoints rather than unrelated intersections with a complex line.

For a direction d at an exterior-caustic point P=(x,y), discriminant-zero tangency gives dᵀMd=0, M=[[B²−y²,xy],[xy,A²−x²]]. The outer normal ν=(x/a²,y/b²) and tangent t=(-y/b²,x/a²) should satisfy the displayed νᵀMt=xyc²/(a²b²)(1−x²/a²−y²/b²). On the boundary this vanishes; det M=A²B²−A²y²−B²x²<0 because P lies outside the strictly nested caustic. Thus normal/tangent axes diagonalize an indefinite direction quadratic form. Reflection in the normal interchanges its two distinct null lines; selecting the inward rays gives the actual billiard reflection law. This is an independent geometric bridge to audit by polynomial expansion and an explicit physical example. Merely asserting a Poncelet translation would not suffice.

## Family3 — least period, winding and orientation

The step is δ=2v. Real injectivity modulo4K means exact order n iff δ/(4K)=τ/n in lowest terms. Here0<τ<n/2,gcd(τ,n)=1; n1 and2 are excluded. This is the primitive class, not an arbitrary label N. Reversing orientation uses−δ and the same finite subgroup, so the unordered cyclic set and product at a starting phase are unchanged. Nonconvex/star windings with admissible coprime τ must not be replaced by τ=1 alone.

An implementation should test both signs of the step and several nontrivial coprime τ, and should deliberately include noncoprime data such as N6,τ2: its actual subgroup order is3, not6. The source theorem's gcd hypothesis is essential to the stated modular criterion.

## Family4 — complete meromorphic divisor and zero multiplicities

Use T=C/(4K Z+2iK' Z), not a torus with incorrectly halved real or imaginary periods. The claimed standard facts are sn poles p=iK',p+2K, simple and exhaustive, and sn(u+2K)=−sn u. The imaginary shift sn(p+u)=1/(k sn u), together with sn(K±v)=cn v/dn v, would give sn(p+K±v)=a/c and hence g+ zeros q±=p−K±v. These facts are recalled from standard theory/prior related work but must be checked against actual primary formulas after this seal.

For0<v<K, q+−q−=2v lies strictly between0 and2K, so the zeros are distinct on T and nonpolar. c≠0 prevents removal of either simple sn pole. Elliptic degree balance then proves there are exactly these two zeros, both simple. Locating two roots without proving exhaustion/multiplicity would leave the argument incomplete; that is a specific falsifier.

## Family5 — exact rational coset arithmetic and universal necessity/sufficiency

H=⟨δ⟩ has exact order n. Normalize real offsets after subtracting p by4K. The product divisor is the sum of all H translates. Both zeros differ by δ, so the zero divisor is one coset with multiplicity2, represented by z=−1/4+τ/(2n). Pole cosets are H and1/2+H.

If n is odd, pole cosets are disjoint. nz=(−n+2τ)/4 and n(z−1/2)=(−3n+2τ)/4 have odd numerators, so the zero coset misses both. Exactly2n simple poles remain. If n is even, τ is odd and1/2∈H; pole cosets coincide, giving n double poles. Zero cancellation occurs iff nz∈Z, equivalently n≡2 mod4. Otherwise n double poles remain. This proof is for every coprime τ,n, not a finite period scan.

A materially independent exact check can sum Fraction-valued point divisors on Q/Z directly for many n/τ, rather than implement the paper's already-simplified congruence. It should compare positive/negative steps, complete pole/zero degrees and overlap multiplicities, then deliberately drop gcd restrictions and recover the smaller primitive denominator. It will corroborate, not prove, the all-integer statement above. The native checker belongs to the other lane and will not be duplicated.

## Family6 — complex-to-real nonconstancy and both-focus assertion

A zero total divisor makes the product holomorphic everywhere on compact connected T and therefore constant. If poles remain, meromorphic nonconstancy alone is not yet the physical statement: the product is holomorphic in an open neighborhood of the real parameter axis because its zeros/poles are off that line. A constant real-phase restriction would have a nonisolated zero set for product−constant and the identity theorem would force the meromorphic function constant, contradiction. This closes the real-family necessity, not just complex nonconstancy.

Since g−(u)=g+(u+2K), both foci have the same phase-constancy classification. If n is even, 2K∈H and the cyclic product is H-invariant, so D_n^+=D_n^- pointwise. This pointwise equality does not imply phase constancy: n4 is the immediate attack. For n=2m≡2 mod4, pairing antipodal vertices gives D_n^±=∏_(j=0)^(m−1)[a²−c²sn²(2jv)] evaluated at phase0; every factor is positive. No particular normalization of the constant is needed for the classification.

## Family7 — repetitions, circle and singular limits

An r-fold traversal multiplies the same positive primitive factors r times, so D_(rn)=(D_n)^r. The map x↦x^r is injective on positive reals, proving both directions of constancy transfer. If N≡2 mod4, its2-adic valuation is1; any divisor n is odd or2 mod4. Therefore in that return-length class constancy iff least n is even. A return6 built by repeating a primitive triangle is outside the primitive6 invariant class.

At c=0 the coefficient of sn disappears and the torus degenerates as k→0; all focal distances equal a, so all periods are constant. This is a separate expressly stated boundary, not a contradiction to the c>0 iff theorem. At B→0,k→1 or v→K, zeros can coalesce with excluded points and a degenerate two-bounce limit may appear; neither the strict-caustic divisor proof nor a period claim should be extended there without new analysis. The caustic touching the outer boundary, v→0, is also excluded. Hyperbolic caustics are not silently included. No uniform quantitative oscillation bound in these limits is claimed.

## Family8 — exact physical triangle and return-length falsification

For a²15,b²7,c²8,A²135/16,B²7/16, confocality holds and A=3a/4,B=b/4, so nesting is strict. Vertices (a,0),(-3a/4,±7/4) lie on E since9/16+(49/16)/7=1. The vertical side is x=−A; the other sides x±ay=a are tangent because A²+a²B²=a². At the upper off-axis point the inward unit directions are(a/4,−1/4),(0,−1); their sum5(a/20,−1/4) agrees with the inward normal because3/(4a)=a/20. At the right axis point the symmetric unit rays also sum to a positive multiple of its inward normal. Thus the two centrally reflected triangles are genuine primitive three-bounce members of the same caustic family, not only points satisfying closure.

At F+ the products expand, using a²15,c²8, to15a/2+3c and15a/2−3c. Both are positive and differ. Squaring yields difference4(15a/2)(3c)=90ac=180sqrt30>0 for six events. The example also falsifies pointwise equality of the two focal products in a primitive odd period, while agreeing with the theorem's even-period-only equality assertion.

## Family9 — independent four-bounce geometric attack on an even-only interpretation

A separate exact counterexample to “every even primitive period is invariant” can be derived without Jacobi functions. For any a>b>0 put s²=a²+b², A=a²/s,B=b²/s. This gives strict nested confocal ellipses since A²−B²=a²−b². The axis diamond (a,0),(0,b),(-a,0),(0,-b) is caustic-tangent because A²/a²+B²/b²=1, and its reflection law follows from axis symmetry. The axis-parallel rectangle(±A,±B) is also inscribed because the same identity holds; its vertical/horizontal sides touch the caustic, and at each corner its outer normal has equal component magnitudes A/a²=B/b²=1/s, so it obeys the billiard law.

Both are primitive four-bounce members of that confocal family. Their fixed-focus products are respectively a²b² and [2a²b²/(a²+b²)]². The difference is a²b²(a²−b²)²/(a²+b²)²>0. For a=2,b=1 they are4 and64/25, difference36/25. This proposed own control directly distinguishes even period from2 mod4 and separates focus symmetry from invariance. Its complete geometric/arithmetic implementation is pending; it was derived before any native code/results or new foreign body.

## Family10 — source interfaces, credit and exact pending gaps

After this seal, personally inspect the actual RGK exactv11 and published Table2/p345 for k114 definition, ordinary distance and period convention. Inspect Stachel Theorem4.3/(4.9) and exact axis/modulus/shift conventions, DLMF22.4 periods/poles and22.8 addition/shift identities. Check actual bodies of Schwartz/AST/Roitman–Garcia–Reznik for antecedent pole-removal/Poncelet methods rather than describing that method as new. Ferudun23093258 concerns k115 outer tangent polygons according to the target; this must be verified in the actual body, without inventing an independence/influence or firstness conclusion. Dragović–Gajić full-text unavailability is a disclosed target historical coverage gap; I have not newly tried to obtain/read it at this checkpoint and must not claim a fresh failure or absence of an earlier proof.

| Family | Independent mechanism/status | Exact remaining check |
|---|---|---|
| Physical category | Positive ordinary distances, correct modulus/axes and dimension reconstructed | Symbolic polynomial identities and actual canonical-parameter primary |
| Billiard bridge | Tangency discriminant/normal diagonalization reconstructed | Exact algebra expansion and line/reflection controls |
| Primitive denominator | Rational translation order/gcd proof | Direct point-divisor Fraction inventories and noncoprime attacks |
| Complete divisor | Two simple poles/two exhaustive zeros conditional on standard Jacobi facts | Actual period/shift primary formulas; no omitted zero/pole |
| Coset theorem | Odd/even multiplicities and mod4 cancellation proved arithmetically | Independent direct-divisor finite corroboration, not native replay |
| Real family | Identity theorem and positive focus factor close physical implication | Check no real singularity/partial-phase substitution |
| Repeats/limits | Positive-power injectivity and circle/degenerate exclusions | Exact return-length and circle controls |
| Triangle | Full physical geometry and radical arithmetic derived | Own exact arithmetic check, not solver output |
| Four-bounce control | New direct diamond/rectangle comparison derived | Own bounded implementation and scaling/reversal check |
| Source contribution | Scope/credit hypotheses explicit, no firstness assumed | Actual primary bodies/versions and honest access limits |

Initial assessment: no substantive defect found in the proof reconstruction conditional on its stated standard Jacobi imports. Primary-interface verification and independent controls remain pending; this is not a final verdict. No repair, narrower replacement, extra theorem promotion or follow-up is proposed. Scientific findings remain withheld from parent until its explicit gate opens.
