UTC: 2026-11-15T00:48:54.800050+00:00

# Independent initial exact reconstruction and adversarial attack ledger

I personally read all three actual PDF pages, every one of the 200 controlling TeX lines (8651 bytes), then visually inspected all three freshly rendered page images. This substantive reconstruction is written and sealed BEFORE any target foreign primary body, support code/results, inventory triage, archived/current review opinion or sibling finding. SOURCE_READY was used only for raw custody/identity and source locators. None of the previously assigned papers' mathematics is used as evidence here.

## Literal full original claim and assumptions

The finite index n is an integer at least 3, F0=0,F1=F2=1, q=Fn and p=Fn-1. For exactly the q indices 0<=k<q, put a=k/q, radial component2sqrt(a(1-a)), longitude2pi pk/q and height1-2a. The theorem claims minimum AMBIENT EUCLIDEAN CHORD2/sqrt(q), for EVERY such n, with unique minimizing UNORDERED pair{z0,z1}. It additionally gives minimum intrinsic sphere distance2arcsin(1/sqrt(q)). There is no asymptotic replacement of an exact finite claim. The singleton n=2 is excluded; the formula has a north pole, no south pole and no half-step offset. Irrational golden angles, midpoint heights, arbitrary cardinalities, general coprime p/q, discrepancy and optimal packing among all configurations are not included.

The native version is 1.0. The paper prints 5 October 2026 but no separate version number in its controlling source. Native creation/update dates remain metadata facts, not proof assumptions. Exact agreement with the original Brauchart displayed definition/conjecture and its inconsistent-looking endpoint notation must be checked from the actual primary AFTER this seal, rather than assumed from the present paper's account.

## A. Whole arithmetic argument, including small indices and arbitrary ell

For each integer 1<=m<Fn, choose j>=2 with Fj<=m<Fj+1. This is unique despite F1=F2 because Fj is strictly increasing starting at j=2. Also j<=n-1, so h=n-j>=1. The basis vectors(Fj,Fj-1),(Fj+1,Fj) have determinant Fj²-Fj-1Fj+1=(-1)^(j-1), hence give unique INTEGER S,T for every(m,ell).

S=0 is impossible because0<m<Fj+1. If S,T are both positive, m>=Fj+Fj+1>Fj+1, impossible. If both negative, m<0. The cases T=0,S<0 and S=0 are excluded separately. Thus T=0,S>0 or S,T have opposite signs; no hidden sign case is missing.

The recurrence gives

    p Fj-q Fj-1=(-1)^(j-1) Fh,
    p Fj+1-q Fj=(-1)^j Fh-1.

Therefore mp-ell q has absolute value |S Fh-T Fh-1|>=Fh: opposite signs make the two summands agree in sign, and |S|>=1; when T=0 the same conclusion holds. The terminal h=1 needs explicit care because Fh-1=F0=0, but still |S|F1>=1. Nothing requires ell to be a nearest integer at this stage.

The addition identity Fn=Fj Fh+1+Fj-1 Fh, together with Fh+1<=2Fh and Fj-1<=Fj, yields q<=3FjFh<=3m|mp-ell q|. Thus the displayed weaker arithmetic lemma follows for all ell, independently of the cited exact hyperbolic-cross theorem. Consecutive-Fibonacci coprimeness follows by Euclidean recurrence. The cited stronger product index Fn-2 and its indexing convention still need direct primary inspection; they are not necessary assumptions of this proof.

## B. Geometry and degenerate latitudes

For 0<=a<b<=1, d=b-a>0, longitude cosine c, define U=2(a+b-2ab), V=4sqrt(a(1-a)b(1-b))>=0. Direct expansion gives D²=2(U-cV), U-2d=4a(1-b)>=0 and V²=U²-4d². Since d>0, U>V. Thus U-cV>0 for 0<c<1. The identity

    (U-cV)²-4d²(1-c²)=(V-cU)²

is algebraically exact. If c<=0, D²>=2U>=4d. If 0<c<1, taking positive square roots gives D²>=4d sqrt(1-c²). Neither estimate assumes planar distances are preserved by the equal-area map. The poles a=0 and b=1 cause V=0 but no singular denominator. In the actual configuration b=j/q<1, the excluded south endpoint will matter for uniqueness.

The points lie exactly on the unit sphere because radial²+(1-2a)²=1; their strictly different heights prove distinctness regardless of longitude. Latitude labels at a pole are harmless because the radial coordinate is zero.

## C. Main all-pair lower bound and equality

For i<j, m=j-i is in[1,q-1]. Choose a centered residue r=mp-ell q with0<|r|<=q/2; gcd(p,q)=1 excludes r=0. A tie at |r|=q/2 has two possible signed representatives but the same cosine and product. It is not claimed unique. Since0<2pi|r|/q<=pi, c=1 is impossible.

If4|r|>=q then c<=0 EXACTLY, including the r=q/4 boundary. Geometry gives D²>=4m/q>=4/q. Otherwise0<4|r|<q, so c>0 and sin(2pi|r|/q)>0. Concavity of sine on[0,pi/2] gives sin(2pi|r|/q)>=4|r|/q. Combined with the arithmetic lemma,

    D²>=16m|r|/q²>=16/(3q)>4/q.

The gap is a strict factor4/3, not a vague asymptotic statement. The case split should be implemented by exact integer residue comparisons; floating cos(pi/2) may have an incorrect tiny positive sign. In particular q=8 can have |r|=q/4 and is a useful rounding control.

The north-pole witness gives D²(z0,z1)=4/q directly, independent of azimuth. Any equality in the nonpositive-cosine chain forces m=1 and U=2d. Then a(1-b)=0, and actual b<1 forces a=0, hence i=0,j=1. The omitted condition cV=0 holds automatically for this pole witness. The strict positive-cosine branch has no equality. This appears to establish uniqueness as stated. For q=2 there is only one pair; q=3 and5 should be tested independently rather than silently omitted by a large-n loop.

Chordal and geodesic distances on the unit sphere satisfy D=2sin(theta/2) for theta in[0,pi], a strictly increasing relation. Thus the stated geodesic minimum follows without a second packing theorem.

## D. Scope/convention attacks and strongest simple outside controls

Including BOTH endpoints0<=k<=q creates q+1 points and immediately destroys the unique-pair statement: at q=2 the north/equator/south configuration has two minimizing unordered pairs. This is outside the published half-open index range and tests a dangerous convention change.

Using midpoint heights at q=2 instead gives two antipodal points and distance2, whereas2/sqrt(q)=sqrt2. It is not the same finite configuration. These simplest cases are exact and require no transcendental rounding.

Coprimeness alone cannot replace the Fibonacci arithmetic. For q=12,p=1, the two indices5,6 have D²=2-sqrt(105)/6<1/3=4/q, because105>100. This is an exact counterexample to an illicit general-coprime extension, not an in-scope counterexample. I will actively search in-scope small indices and all arithmetic residue classes using exact controls after sealing, and will not call an outside-hypothesis example a defect of the paper.

The one-based range1<=k<=q is isometric to the half-open range: k->q-k changes longitude sign and height sign, giving the rigid rotation(x,y,z)->(x,-y,-z). The reversed planar coordinate ordering is also plausibly equivalent: if k= p j modq, then j=(-1)^n p k modq by p²=(-1)^n modq, so odd n requires longitude reflection. The actual cited planar definition must be read before accepting that source-comparison claim.

## Initial status and next independent checks

The main self-contained proof appears internally coherent on this first reconstruction. No in-hypothesis counterexample is yet identified. Still pending: actual Brauchart primary definition/conjecture and endpoint notation; actual modern/Zaremba arithmetic index conventions; reversed-coordinate primary interface; inspected source certificate/code domains and numerical rounding controls; own exact algebra and small-index/degeneracy checks with explicit certificates rather than floating samples.

Priority and present-worldwide-open status are NOT inferred from an archived search or the fact a2012 source states a conjecture. The paper itself labels those limits. If a substantive defect is found, I will preserve its precise evidence, stop the repair route and not substitute a narrower promoted result. Root 114 initial gate is pending: scientific conclusions will remain in local files until that gate opens.
