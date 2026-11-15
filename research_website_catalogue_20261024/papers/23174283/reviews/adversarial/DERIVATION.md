# Independent adversarial derivation — record 23174283

This is the final expansion of the argument first reconstructed in the immutable INITIAL_RECONSTRUCTION.md before any foreign body, code, result, triage or peer opinion was read. It checks the published claim, including its unique-pair conclusion, without assuming either the archived review verdict or a finite computation. The finite exact controls are supplementary and separately identified.

## Exact claim and hypotheses

Let F0=0, F1=F2=1 and F(n+1)=Fn+F(n−1). For each integer n≥3, q=Fn≥2, p=F(n−1), and **exactly** 0≤k<q, define

z_k=(2√[(k/q)(1−k/q)] cos(2πpk/q), 2√[(k/q)(1−k/q)] sin(2πpk/q), 1−2k/q).

The ambient Euclidean minimum is 2/√q, and its only minimizing unordered pair is {z0,z1}. There is no asymptotic qualifier. The geodesic minimum is 2 arcsin(1/√q). Neither an irrational golden angle, midpoint heights, all integer q, nor q+1 endpoints is included. All points have unit norm by 4a(1−a)+(1−2a)²=1; different indices have different third coordinates. The longitude at the north pole need not have geometric meaning for its formula to define that point.

## Universal arithmetic reconstruction, including arbitrary integer ℓ

Consecutive Fibonacci numbers are coprime: applying gcd(Fn,F(n−1))=gcd(F(n−1),F(n−2)) repeatedly gives gcd(1,1)=1. Thus no nonzero m<q has mp divisible by q.

For any 1≤m<q, choose the unique j≥2 with Fj≤m<F(j+1); uniqueness starts at j=2, after the duplicate initial 1. Then j≤n−1 and h=n−j≥1. The determinant

D_j=Fj²−F(j−1)F(j+1)=(−1)^(j−1)

is ±1. It follows first from D2=−1 and D(j+1)=−D_j, so the columns (Fj,F(j−1)), (F(j+1),Fj) are an integer basis. For **every** integer ℓ, there are integers S,T with

(m,ℓ)=S(Fj,F(j−1))+T(F(j+1),Fj).

S cannot vanish, since 0<m<F(j+1). If T=0, S>0. Otherwise S and T have opposite signs: both positive violate m<F(j+1), both negative give m<0. This classification includes very large positive and negative ℓ; there is no hidden restriction to a nearest integer.

For fixed j, E_n=F(n−1)Fj−FnF(j−1) obeys the Fibonacci recurrence in n. Its values at n=j,j+1 are 0,D_j. Therefore

pFj−qF(j−1)=(−1)^(j−1)Fh,

pF(j+1)−qFj=(−1)^j F(h−1).

The error is consequently

|mp−ℓq|=|S Fh−T F(h−1)|≥Fh.

When S,T have opposite signs their two displayed terms cannot cancel. When T=0 the inequality follows from |S|≥1. In particular h=1 is valid, with F(h−1)=F0=0; discarding this terminal term would be an error, but the proof does not do so.

The addition formula

q=Fj F(h+1)+F(j−1)Fh

follows by recurrence from h=0,1. Since h≥1, F(h+1)≤2Fh and F(j−1)≤Fj. Thus

q≤3 Fj Fh≤3m |mp−ℓq|.                                       (A)

This establishes the manuscript's weaker bound for all stated indices and all ℓ. No primary-literature index theorem is necessary for (A). The sharper classical index F(n−2), and the credit for it, are separately checked in PRIMARY_EVIDENCE.md.

## Geometry: no distance-preservation assumption

For two actual latitude parameters 0≤a<b≤1, let d=b−a>0 and c be the cosine of the longitude difference. Define

U=2(a+b−2ab),  V=4√[a(1−a)b(1−b)].

Dot products give D²=2(U−cV). Exact expansion gives

U−2d=4a(1−b)≥0,     U²−V²=4d².

In particular U≥2d>0, V≥0, and U>V. If c≤0, D²≥2U≥4d. If 0<c<1 then U−cV>0, and

(U−cV)²−4d²(1−c²)=(V−cU)²≥0.

Taking the nonnegative square root is justified and yields D²≥4d√(1−c²). This works at the pole (V=0), at the equator, and even at b=1 in the lemma. It does not transfer planar distances through an equal-area map. Exact symbolic coefficient expansion of both identities is supplied by own_exact_controls.py.

## Universal pair bound and uniqueness

For 0≤i<j<q let m=j−i, a=i/q, b=j/q, d=m/q. By coprimality choose a centered nonzero residue r=mp−ℓq with 0<|r|≤q/2. At a half-period tie either sign gives the same cosine and product. Its absolute angle θ=2π|r|/q is in (0,π].

If 4|r|≥q, c=cos θ≤0 exactly, so D²≥4m/q≥4/q. This classification can be implemented with integer comparison; a rounded positive value of cos(π/2) would not be an appropriate branch test.

If 4|r|<q then 0<θ<π/2 and 0<c<1. The concave function sin θ lies above its chord from 0 to π/2, giving sin θ≥2θ/π=4|r|/q. Therefore geometry and (A) give

D²≥(4m/q)sin θ≥16m|r|/q²≥16/(3q)>4/q.              (B)

There is no uncovered c=1 case, because a centered nonzero residue has θ>0 and θ≤π. All q=2,3,5 are covered by these same arguments. For the pole z0, direct calculation gives ||z0−zk||²=4k/q, hence ||z0−z1||²=4/q.

Equality cannot occur in (B). In the nonpositive-cosine branch it forces m=1 and U=2d. Since b=j/q<1, U−2d=4a(1−b)=0 forces a=0. Hence i=0,j=1. Conversely that pair attains the bound. The open upper endpoint is load-bearing for uniqueness: the geometric lemma itself also allows b=1, but the theorem does not include that endpoint.

On the unit sphere D=2 sin(γ/2) for the intrinsic shorter angle γ∈[0,π], and this is strictly increasing. The minimum geodesic distance and the minimizing pair follow exactly; chord and arc values have not been equated.

## Direct finite radical certificate, separate from the proof

For actual integer indices i<j, put

H=q(i+j−1)−2ij=q(j−i−1)+2i(q−j)≥0,

P=i(q−i)j(q−j)≥0.

The exact chord inequality D²≥4/q is equivalent to H≥2√P c. For q=2,3 all nonzero cosines are negative. For q=5 the only positive residue class has c=(√5−1)/4, so squaring reduces the comparison to

H²−3P/2+(P/2)√5≥0.

If its rational term A is negative, its sign is determined exactly by 5B²−A² for B=P/2≥0; otherwise it is nonnegative immediately. For q=8 the only positive residue class has c=√2/2, giving the integer gap H²−2P. Residue |r|=q/4 gives exactly c=0. These facts enumerate **all 42 unordered pairs for q=2,3,5,8**, with explicit H,P,radical gaps and strict/equality decisions retained in own-exact-controls-v2.stdout.json. The sole equality at each cardinality is (0,1). No decimal sine, cosine, square root, tolerance or interval heuristic enters these certificates.

The same read-only program checks 6,746 exact centered-residue offsets through n=18, full integer permutation congruences and terminal/half-period/quarter-turn cases. Those bounded tests diagnose mistakes; the universal deductions above establish the infinite claim. The separate deposited proof_controls.py was run once, without optimization or bytecode writes, as supporting reproduction. Its finite basis checks are not substituted for (A) or (B).

## Falsification boundaries with exact witnesses

* n=2 has q=1 and no pair, so a numerical minimum should be undefined; it is expressly excluded.
* If both endpoints are included at q=2, the north pole, equator point and south pole have squared pair distances 2,2,4. The minimum has two unordered minimizers. This falsifies an endpoint-expanded unique-pair claim, not the actual half-open theorem.
* At q=2 with midpoint heights (k+1/2)/q, the two longitudes differ by π and the heights are ±1/2. The points are antipodal, giving chord 2 rather than the original √2. Thus retaining the original formula after changing the heights is false.
* Coprimality alone does not suffice. For q=12,p=1 and i=5,j=6 in the displayed formula, exact substitution yields D²=2−√105/6<1/3=4/q, since 105>100. These parameters are outside the Fibonacci hypotheses. This is an exact witness against replacing that arithmetic condition by general coprimality.
* At the genuine q=8,p=5,m=2 boundary, |r|=2=q/4 and c=0 exactly. The nonpositive branch is valid, with strict slack for m=2. No floating-point sign decision is needed.
* For the coordinate-reversed primary lattice, set k≡pj (mod q). Its longitude is j/q while the target longitude is pk/q≡(−1)^n j/q. Reflecting the second spherical coordinate when n is odd gives equality. At n=4 parity no reflection is needed; at odd n=5,q=5,p=3,j=1,k=3 the two longitude residues 1 and 4 have opposite nonzero sines, so omission of that reflection is a concrete false identity. The exceptional smallest odd n=3 has q=2, so reflection acts trivially on its two meridian points and cannot supply that witness.
* Replacing the half-open range by 1≤k≤q gives an isometric set: k↦q−k and (x,y,z)↦(x,−y,−z). This does not create a defect in either convention when the correct pair is relabelled.

No tested boundary supplies a counterexample within the published hypotheses. There is no repair route or narrowed substitute theorem proposed here.
