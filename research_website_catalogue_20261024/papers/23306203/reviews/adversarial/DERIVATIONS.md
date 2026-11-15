# Independent adversarial derivations — row 129

This is the completed proof and boundary assessment of the original theorem, not a substitute theorem or a repair. Its central mechanisms were already reconstructed in `INITIAL_RECONSTRUCTION.md` before foreign bodies, supplied code/results or opinions. The separate exact controls and their results were frozen before those exposures. No peer/root scientific report was read.

## 1. Scope, exact period and physical geometry

Fix the strictly nested confocal ellipses with a>b>0, A>B>0, a>A, b>B and a²−b²=A²−B²=c²>0. The theorem concerns a fixed periodic physical billiard family and its least period n, every admissible coprime star winding, either orientation, either fixed focus, and the product of ordinary distances over the primitive vertices. It does not assert existence of a periodic family for every fixed pair or arbitrary n.

Set k=c/A in (0,1). Since cn is strictly decreasing from 1 to 0 on (0,K), cn(v)=B/b has a unique v in that interval. Confocality gives a=A dn(v)/cn(v). The real map P(u)=(-a sn(u),b cn(u)) covers the outer ellipse once modulo 4K: the real Jacobi amplitude is strictly increasing, and its sine/cosine pair is injective modulo one full turn. In particular, using 2K as the vertex period would identify antipodal distinct points and is invalid.

The chord between P(U−v) and P(U+v) lies on the tangent at Q(U)=(-A sn(U),B cn(U)). Substitution in −x sn(U)/A+y cn(U)/B=1 using the addition formulas gives a numerator dn²(v) sn²(U)+cn²(U), equal to the denominator 1−k² sn²(U)sn²(v). This denominator is positive for real U,v and k<1. The two endpoints are distinct because 0<2v<2K. A point on the inner ellipse lies strictly inside the outer ellipse; therefore its tangent contact is inside the segment cut out by that line, rather than on an exterior extension.

An independent algebraic check of the elastic bridge is useful because Poncelet tangency alone should not be silently identified with physical reflection. A direction d of a line through P=(x,y) tangent to the caustic satisfies dᵀMd=0 for M=[[B²−y²,xy],[xy,A²−x²]]. The determinant is A²B²(1−x²/A²−y²/B²)<0, so there are two distinct real tangent lines. For the outer normal ν=(x/a²,y/b²) and its perpendicular t=(-y/b²,x/a²), expansion gives

νᵀMt = xy c²/(a²b²) · (1−x²/a²−y²/b²) = 0.

Thus M is diagonal in this orthogonal frame; reflection across the normal interchanges its two null lines. Both contacts lie inward from P, so the two inward unit rays have the same negative normal component and opposite tangential components. They are exchanged by this reflection. This argument also covers x=0 or y=0 without dividing by an axis coordinate. It verifies the physical billiard law globally.

The vertex shift is δ=2v. By real injectivity, exact closure is δ/(4K)=τ/n in lowest terms, with 0<τ<n/2. Consequently n is the order of δ, the n vertices are distinct, and n=1,2 cannot occur. Reversing orientation negates δ but gives the same cyclic subgroup and the same vertex product. No convex-only or winding-one restriction was introduced.

## 2. Ordinary positive distances and the correct complex torus

On the real boundary, direct expansion using a²−b²=c² gives

|P(u)−F±|²=(a±c sn(u))².

Since a>c and |sn(u)|≤1 on the real axis, a±c sn(u)>0. Hence g±(u)=a±c sn(u) is the ordinary Euclidean distance itself on that line. There is no signed-distance, squared-distance or absolute-value branch substitution.

Use T=ℂ/(4Kℤ+2iK′ℤ) for sn and g±. This choice does not assert that the full complex map P descends to T: cn changes sign under 2iK′. Only the real period 4K was used to count physical vertices. The separation of these two roles removes a potentially consequential hidden quotient assumption.

On T, sn has simple poles p=iK′ and p+2K. Because c≠0, neither pole disappears in g+. The standard shifts give sn(p+K±v)=dn(v)/(k cn(v))=a/c and sn(u+2K)=−sn(u), so g+ has zeros q±=p−K±v. They are distinct because their difference is 2v in (0,2K), and neither is a pole. A meromorphic function on a compact torus has equal total zero and pole degrees. Since the pole degree is two, the two exhibited zeros are simple and exhaustive. This rules out exceptional interior parameter values producing an uncounted zero, double zero or removable pole.

## 3. Complete divisor arithmetic for every primitive period

Let H=⟨δ⟩ have exact order n. Divisors of the cyclic product are the sums of the translated single-factor divisors. Translation signs are immaterial at the coset level because −H=H, but their multiplicities are not discarded.

Subtract p and measure real offsets in units of 4K. Coprimality identifies H with {j/n mod 1}. The two zero orbits coincide because q+−q−=δ; the zero divisor is one coset of multiplicity two, represented by z=−1/4+τ/(2n). The poles are H and 1/2+H.

For odd n these pole cosets are disjoint. Neither nz=(−n+2τ)/4 nor n(z−1/2)=(−3n+2τ)/4 is integral: both numerators are odd. The zero coset meets neither pole coset. Exactly 2n simple poles remain.

For even n, τ is odd and 1/2 belongs to H. The two pole cosets coincide with multiplicity two. The zero coset cancels them precisely when nz is integral, equivalently −n+2τ is divisible by four, equivalently n≡2 mod 4. In that class the entire divisor is zero. For n≡0 mod 4 the zero coset is disjoint and n double poles remain.

When the divisor is zero the product extends holomorphically to the compact connected torus, hence is constant. When poles remain the product cannot be constant as a meromorphic function. It is holomorphic on a neighborhood of the real line. If it were constant on the physical phase family, the identity theorem would force its connected meromorphic continuation to be that constant, contradicting those poles. Thus the complex calculation proves nonconstancy of the actual real Euclidean product, not merely of an unrelated complex expression.

This proves the full all-period iff assertion. The finite inventory is an independent falsifier for arithmetic errors, not an induction hypothesis or an inference to all n.

## 4. Both foci, repetitions and limiting boundaries

The other factor is g−(u)=g+(u+2K). It therefore has the same constancy class. For even n, 2K is in H, so a permutation of the factors gives equality of the two focal products at every phase, including the nonconstant n divisible by four class. Equality of these two functions is not a claim that either is constant.

For n=2m≡2 mod 4, τ is odd. Pairing indices separated by m negates sn and gives the positive constant at phase zero:

∏(j=0,…,m−1) [a²−c² sn²(2jv)].

For any integer r≥1, an r-fold traversal multiplies each primitive factor r times and gives D_n(u)^r. A positive real power with positive integer exponent is injective, so a nonconstant primitive product cannot become constant through repetition. If a listed return length N≡2 mod 4 is given instead, its least period divides N and is either odd or 2 mod 4; precisely the even least-period case is constant. A gcd reduction of the rotation number is essential.

At c=0 the focal factors have no poles and are identically a; every listed product is a^N. The noncircular divisor argument is not passed unchanged through that limit. At k→1, v→0 or v→K, the strict positive-axis/nesting assumptions may cease to hold or the period class changes; these singular endpoints do not create admissible counterexamples inside 0<k<1 and 0<v<K. No uniform numerical conditioning or extension to degenerate or hyperbolic caustics is claimed.

## 5. Exact smallest return-length boundary witness

Use a²=15, b²=7, c²=8, A²=135/16 and B²=7/16. The three vertices (a,0), (−3a/4,7/4), (−3a/4,−7/4) are distinct points on the outer ellipse. The side lines are x=−A and x±ay=a. Their contacts with the caustic are (−3a/4,0) and (9a/16,±7/16). The latter contacts divide the slanted chords in ratios 1/4 and 3/4; the vertical contact is the midpoint. Thus all contacts lie strictly inside their actual segments.

At the upper off-axis vertex the inward unit directions (a/4,−1/4) and (0,−1) sum to five times the inward normal (a/20,−1/4). At the other two vertices the same identity follows by explicit sign changes or symmetry; the own exact biquadratic calculation checked all three. These are physical primitive three-bounce orbits. Central reflection stays within the same fixed confocal family; the global parameter established above makes it another phase.

At F+=(c,0) the two primitive products are 15a/2+3c and 15a/2−3c. Their two-traversal products differ by 90ac=180√30>0. This is an exact counterexample to an unrestricted six-event return-length rule. It agrees with, and is required by, the original theorem's least-period formulation; it is not a defect in that theorem.

## 6. Independent checkable artifacts and limits

`independent_controls.py` uses signed integer multiplicity counters over ℚ/ℤ, exact rational polynomial normal-frame checks, and explicit arithmetic in ℚ(√15,√8). Its frozen result contains 2,800 exact predicates across 289 return/winding pairs for return lengths 3–35, including 191 primitive pairs, nonprimitive gcd reductions, reversed orientations, exact vertex/segment/reflection/focal identities and excluded-boundary controls. No supplied scientific code or expected results were imported or read before this freeze.

The selected native `verify_exact.py` adds a separate finite inventory through n=101, exact triangle arithmetic in ℚ(√(8/15)), and a physical four-period diamond/rectangle control. Its normal and optimized executions match the entire original expected object and all 932 output bytes. Optional theta-series diagnostics were inspected but not executed and are not validated numerics.

The actual Stachel theorem and DLMF formulas were read after the independent seals. Exact RGK v11 gives the historical k114 observation, not a proof or a present-day openness certificate. The 2021 final article body was not obtained in this lane; other cited method/priority papers were not independently audited in full. Those are attribution/coverage limits, not missing mathematical inputs to the derivation above. No firstness or exclusive priority verdict follows.
