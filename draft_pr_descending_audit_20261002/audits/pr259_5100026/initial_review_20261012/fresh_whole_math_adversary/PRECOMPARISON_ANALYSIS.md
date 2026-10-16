# Frozen independent proof and source analysis

This file is written before historical reviewer narratives, current-family reports or Root's witness/mechanism are read. The imported target's published/open fields and intake queue's claimed-solved prose have no mathematical evidentiary force. Novelty is unaudited.

## Exact source-qualified claim

The inspected source is the actual *Eighty New Invariants in the Elliptic Billiard*, arXiv:2004.12497v11 (29 October 2020), and the published *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, DOI 10.1007/s40598-021-00174-y. Their §3.5/Table 5 specifies k407, vertex centroid C0*′, even N, M=f1 or f2, value ?, proof ?. The final definition is on printed p347 and table on p348; arXiv table is PDF p7. Visual inspection confirms the prime/star mark and does not rely on text extraction's ambiguous order of glyphs. §3.4 explicitly defines the vertex mean as a sum divided by N, whereas signed-area centroid has an area denominator. The antipedal diagram, imported target and conventional polygon definition correspond to complete perpendicular lines. A literal one-sided-ray orientation is not specified by §3.5 and has not been proved by the submission; the imported statement explicitly says sides through vertices and is handled by lines.

Both introductions restrict the billiard model to a confocal ellipse pair, with a>b>0 in §2. Strict nested nondegenerate elliptical caustics are the submitted theorem's domain. Neither Table 5 nor these paragraphs explicitly states “least period” or “primitive.” Stachel's published Theorem 4.3/eq4.9 states the coprime turning-number parameterization and covers primitive star orbits. The supplied source does not by itself prove that every usage of N-periodic excludes repetitions. This matters mathematically, not just linguistically: see the exact counterexample below.

## Independent real construction

Normalize caustic semiaxes to 1,k′, with k′²=1−k² and 0<k<1. The published Stachel theorem yields v=2Kτ/N, δ=2v, a=dn(v)/cn(v), b=k′/cn(v), P(t)=(−a sn(t), b cn(t)). With 0<τ<N/2 and gcd(N,τ)=1, 0<v<K and a>b>0, a>1, a²−b²=k²; the original foci are (±k,0). Reversal supplies the other orientation. For an even least period τ is odd and (N/2)δ=2Kτ, so P and all tangent intersections are antipodal.

Put s=sn(v),c=cn(v),d=dn(v), and S=sn(u),C=cn(u),D=dn(u), D0=1−k²s²S². Solve the two actual tangent equations at P(u−v),P(u+v), whose normals are (−sn(t)/a,cn(t)/b). Jacobi addition gives R(u)=(−A S,B C), A=d²/c², B=k′/c². This is verified from raw tangent equations in independent_exact.py; independent_numeric.py separately constructs each outer vertex by a 2×2 tangent solve, not by assuming R.

For M=(k,0), q±=R(u±v)−M. A perpendicular side through R has q·(U−M)=q·q, equivalently q·U=q·R. The determinant derived from the raw endpoint vectors is

Δ(u)=2Bsd D(a+kS)/D0.

For every real u, D≥k′>0, D0≥1−k²s²=d²>0, a+kS≥a−k>0, so Δ>0. Thus all real antipedal vertices exist and are unique in every real phase, including coprime stars. Tangent intersections likewise exist: their real tangent determinant is 2scD/D0>0. No signed-area or winding-area argument is used. The negative focus is handled by central symmetry.

## Complete divisor classification on the common torus

The common lattice Λ=4K Z+4p Z, p=iK′, is valid; using a nonminimal common lattice does not affect compactness. DLMF22.4 gives the poles/zeros and shifts. On C/Λ there are four copolar Jacobi points p+2mK+2np (m,n=0,1), four simple dn zeros K+p+2mK+2np, eight endpoint-pole points p±v+2mK+2np, and four focal roots −K+p±v+2np. This explicitly lists all translates rather than inspecting only one representative.

The last list follows from sn(p+t)=1/(k sn(t)) and sn(K±v)=c/d. At each focal root sn=−a/k. Since cn²=1−a²/k² and dn²=1−a² are nonzero, all four roots are simple. These four are all roots: sn on the sn-period torus has degree two and the common torus doubles it. dn zeros and unshifted poles are disjoint from focal roots since a>1 and a>k.

D0 has exactly the eight endpoint zeros: at p±v+2mK+2np, sn=±1/(ks), with sn′=cn dn nonzero because sn²=1/(k²s²)>1/k². The endpoint lists each contain four points; they are disjoint for 0<2v<2K. The polynomial D0 of the degree-four sn map has at most eight zeros, so this exhausts them. None equals a dn zero (there D0=c²≠0), or an unshifted Jacobi pole. The sole possible focal/endpoint overlap occurs when s a=1, equivalently sd=c. For x=s² this is k²x²−2x+1=0. The only solution in (0,1) is x=1/(1+k′), the unique v=K/2. Coprimality then forces (N,τ)=(4,1). This exception is removed before using the meromorphic proof.

At dn zeros, the finite endpoints coincide (addition terms proportional to D vanish); Δ has a simple zero, since a±1≠0. The two raw equations agree, both Cramer numerators vanish, so division by that simple zero is removable.

At unshifted Jacobi poles the endpoints u±v are regular. At p+z, S=1/(kz)+O(z), D=−i/z+O(z), D0=−s²/z²+O(1). Thus Δ→2iBd/s≠0; translated signs change without producing a zero. U is regular.

At a focal root, the original tangent n·X=1, n=(−S/a,C/b), passes through M because n·M=−kS/a=1. Moreover n²=S²/a²+C²/b²=1/k²−1/k²=0. In a nondegenerate complex bilinear plane this tangent's direction is its isotropic normal. Hence each finite q± is a multiple of n, q±²=0, and both right sides in q·(U−M)=q² vanish. Both Cramer numerators vanish at Δ's simple zero; U is removable. This is a focal-specific fact and does not hold for generic M or the outer-locus foci.

At an endpoint pole, exactly one R(u±v)=L/z+O(1). The other endpoint is holomorphic. For N≥6 the factor a+kS is nonzero, and Δ has a simple pole. Each Cramer numerator is at most order two: the squared singular row's RHS has order two and its coefficient in the numerator comes from the regular row; the other RHS is regular and multiplies a simple-pole row. Dividing by Δ gives at most a simple pole. There can be no z^-2 term in U. This controls all candidates: away from endpoint poles and the unshifted Jacobi poles, coefficients are holomorphic and Δ has only the listed factors.

## Actual four-edge cancellation and compactness

For F(w)=Σ I_M(R(w+iδ),R(w+(i+1)δ)), a pole of R_j forces exactly one opposite index j+N/2 to be a pole. The congruence is τ(i−j)≡0 mod N/2; coprimality and odd τ give precisely i=j,j+N/2. The real separation of Jacobi pole classes is 2K. No other simultaneous singular vertex can occur.

At a pole, R_j=L/z+O(1), its neighbors Q and −Q because R(p+t)=−R(p−t); this survives every pole translate. R_(j+N/2)=−L/z+O(1) has neighbors −Q,Q. A raw incident residue T(L,Q,M) solves

L·T=L², (Q−M)·T=0,

and equals −L² J(Q−M)/det(L,Q−M), J(x,y)=(−y,x). The determinant is nonzero by the endpoint-pole leading coefficient above. Using the actual opposite leading vector −L, all four residues are

T(L,Q,M), T(L,−Q,M), T(−L,−Q,M), T(−L,Q,M).

Their sum is zero algebraically (checked directly in independent_exact.py); the latter two pair with the former two after changing the signs in both rows. This is cancellation of four actual edge terms, not a heuristic that two opposite antipedal vertices cancel for fixed M. For N≥6 the four edges j−1,j,j+N/2−1,j+N/2 are distinct. Together with the one-pole bound, zero residue makes every possible F singularity removable. F is then coordinatewise holomorphic on the compact connected torus C/Λ, so constant.

Reflection in the focal axis satisfies R(2K−w)=reflection(R(w)) and reverses cyclic order. I_M is symmetric in its input pair and M is fixed. The proven constant must have zero transverse coordinate. Central inversion sends a positive-focus construction to a negative-focus construction and negates its centroid; phase independence makes these constants opposite. Reversal merely reorders the same pair intersections; a repeated even primitive traversal duplicates all U's and preserves the arithmetic mean.

## N4 and circle

At v=K/2, d²=k′ and c²=k′/(1+k′), so A=B=1+k′. Four outer vertices on a circle in two antipodal pairs form a rectangle in their cyclic ordering. Each side is an original-ellipse tangent. In its orthonormal side axes write vertices (±h,±l), M=(m,n). The ellipse's support function gives h²−m²=l²−n²=b²>0, since h_E(e)²=b²+(M·e)² for a unit direction e.

Directly solving the four perpendicular-line intersections gives their mean

(m/2[(l²−n²)/(h²−m²)−1], n/2[(h²−m²)/(l²−n²)−1]).

The unrestricted raw-line algebra is verified independently; the support identities force both entries to zero. h>|m| and l>|n| ensure each denominator is nonzero. This is a direct real proof, and does not pretend the N≥6 singularity classification also applies at N4.

For a circular billiard with a strict concentric circular caustic, the foci coincide at O. A primitive even orbit has antipodal pairs; its tangent intersections are antipodal and finite. The adjacent antipedal normal determinant is R² sin(δ)≠0 for 0<δ<π, and intersections occur in opposite pairs. The arithmetic centroid is O. No k→0 complex limit is needed. The circular case is supplementary because the actual source assumes a>b.

## Exact counterexample to literal even N

Take E: x²/4+y²=1, M=(√3,0), q=(4−√13)/3∈(0,1/3), and vertices P0=(0,1), P1=(2√(1−q²),−q), P2=(−2√(1−q²),−q). These are distinct and their triangle is tangent to the same strict confocal caustic x²/(3+q²)+y²/q²=1: the bottom side is y=−q, and the slanted sides have normalized normals ((1+q)/(2√(1−q²)),±1), with support residual proportional to 3q²−8q+1=0. The caustic axes are less than the outer axes and positive. Confocal tangency gives the genuine period-3 billiard family.

The outer tangent triangle has vertices (H,1),(−H,1),(0,−1/q), H²=4(1+q)/(1−q). All three focal-antipedal determinants are nonzero: 2H, H/q+√3(1+1/q), H/q−√3(1+1/q); the latter is positive because H²−3(1+q)²=(1+q)(1+3q²)/(1−q)>0.

Raw antipedal line solving, without Jacobi functions, yields

Cx=√3(2−q)/(3q)=(7√3+2√39)/3,
Cy=−2(2q−1)(3q+1)/(3q(q−1))=−6.

Reflect the triangle in the x-axis; the same original ellipse, focus and caustic remain fixed, and the centroid becomes (Cx,+6). Double either three-period traversal to an N=6 list. Every P,R,U is repeated twice, so the six-entry arithmetic mean is unchanged. Thus a literal “even listed traversal length N” statement is false despite perfectly finite vertices. This is not a counterexample to the submission's explicit “least even period” theorem, but that hypothesis is essential.

## Independent computation limits and preliminary conclusion

INDEPENDENT_EXACT.json reports zero residuals for raw tangent intersection, focal determinant, unrestricted rectangle mean, all four actual-pole residue algebra and the exact odd-repeat witness. The high-precision script constructs actual tangents and antipedals for all coprime turns in N=4,6,8,10,12,14,18 for k=.15,.63,.97 and four real phases, both original foci; its maximum centroid/symmetry error is 2.86e−83. It probes every one of the 20 single-vertex singularity classes and every pole translate's four actual incident edges. These finite probes corroborate the derivation; they neither provide interval certification nor substitute for the divisor proof.

Preliminary strongest verified result: the submitted theorem for every strict elliptical-caustic, primitive even least period, including coprime stars, with original-focus outer-antipedal arithmetic vertex centroid, is mathematically supported. No fatal proof defect has been found. Exact remaining source gap: both source Table5 and imported target say merely even N; promotion as the unrestricted imported statement needs an explicit least/primitive convention or a corrected source-qualified statement. The literal repeated-odd extension is disproved. Historical originality and later-literature status have not been audited and are not implied by this proof/source audit.
