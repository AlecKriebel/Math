# Exact-target candidate comparison after the independent freeze

The independent search and derivation were frozen at 2026-10-12T12:31:07.550095+00:00. This separate comparison was performed afterward. The eight original frozen artifacts remain unchanged and their SHA-256 hashes were reverified. Root's mathematical acceptance and its candidate review are not premises of the proof judgment here. No candidate checker was imported or executed by this family.

## Finding and recommendation

Alper Ferudun, *Stationary Focal Antipedal Centroids for Even Elliptic Billiard Periods*, DOI [10.5281/zenodo.23071366](https://doi.org/10.5281/zenodo.23071366), currently supplies a complete proof of the same focal outer-antipedal arithmetic vertex-mean constancy target. Its [primary manuscript page](https://eulersolve.org/papers/amr-050-0026/) explicitly identifies k407. The proof's geometric pair calculation and compact-curve trace argument check out globally under the exact strict elliptic-caustic hypotheses. This is substantially stronger evidence against a claim of an unproved or newly solved basic k407 constancy assertion than the older general analytic tools found in the independent search.

The independent bridge G1/G2 is the same geometric paired-chord identity as this manuscript's equations (7)–(10), expressed through outer semiaxes rather than the inverse conic matrix. It must not be described as a new basic geometric bridge in light of that match. The independent Jacobi route adds an explicit zeta evaluation of the trace and thus an explicit all-period centroid formula absent from this candidate's presentation. That is a possible exposition or value-formula contribution, with no priority claim from this audit alone. The classical analytic identity itself is prior work and must be credited accordingly.

For the audit's priority decision, preserve the accepted mathematical result but treat basic constancy novelty as unsupported in view of the authenticated exact-target complete manuscript. Root controls paper/PR/disposition decisions. This family issues no publication or absolute-priority verdict.

## Primary-body binding and temporal limits

The full six-page PDF, extracted source `main.tex`, and compact-curve certificate were read. The PDF is 82690 bytes, SHA-256 `317178430532655300d12aff19391751a3dc32ab6913b5062a4df803d56355b6`; its source ZIP is 47229 bytes, SHA-256 `b43108ae779b1f403e7e0f4c7d632b0ef49c2eb61c6be50178e5da3ce86e0183`. The extracted `main.tex` is byte-identical to its ZIP member. Independently authenticated Root website bodies equal the actual archive-family Zenodo PDF and source ZIP bytes. I separately checked all three actual Zenodo attachments against the official record's size and MD5: PDF, source ZIP and verification report. These local body checks do not rely on a missing archive-agent final verdict. `COMPARISON_INPUT_PINS.json` records the individual hashes and exact input locations; all full third-party bodies remain private reading material.

The currently returned Zenodo record has publication date 2026-09-30, creation 2026-09-30T22:04:12.260164+00:00 and modification 2026-09-30T22:04:12.820855+00:00. The independently returned DataCite body binds the exact title, author and DOI and records registration 2026-09-30T22:04:13.000Z. The PDF and TeX print 1 October 2026; the landing page metadata prints 30 September 2026. Those facts describe current recorded metadata. They do not certify earliest worldwide visibility, intellectual causal order, copying, or absolute priority. Submitted PR creation/head timestamps are likewise not causal evidence. The date discrepancy is preserved rather than silently reconciled.

## Exact scope and finiteness

PDF pp.1–2, equation (1) and Theorem 1 define the exact construction: original ellipse `x²/a²+y²/b²=1`, original focus `F=(±c,0)`, `c²=a²−b²`, strict confocal elliptic caustic with `0<lambda<b²`; outer vertices are actual intersections of consecutive original tangents; each antipedal side is `(X_i−F)·(Y−X_i)=0`; the mean is the uniform vertex sum. Least/effective even period N>=4 and coprime winding are explicit. Equation (2) gives the actual antipodal pairing and the text explicitly includes genuine even stars. Neither triangle results, padded odd periods, inner antipedals, a focus of the outer locus, area weights, nor arbitrary center M are substituted.

The construction is globally real and finite. Original consecutive vertices cannot be antipodal: their diameter chord would cross the strict caustic instead of being tangent, so their original tangents do not become parallel. Consecutive outer vertices are distinct: equality would make three original tangents concurrent, which a nondegenerate conic permits only by repeating an original vertex and retracing, contrary to a positive-flight elliptic-caustic billiard. The outer conic, PDF p.2 equations (3)–(5), has semiaxes strictly exceeding the corresponding original ones, so every original tangent cuts it in two distinct real points. In the shared tangent coordinates, equation (6) gives `h²−f²=b²>0`; equation (7)'s determinant is `(h−f)(r−s)`, hence nonzero. This proves the full-line antipedal intersections finite even when the resulting polygon is self-intersected or has coincident nonconsecutive antipedal vertices. The theorem has no signed-area denominator.

## The paired-chord bridge is identical

Use this candidate's `alpha=(b²−lambda)/b⁴`, `gamma=(a²−lambda)/a⁴`, `beta=(gamma−alpha)/c²`, `kappa=alpha+lambda/(a²b²)`, `Lx²=1/gamma`, `Ly²=1/alpha`. This comparison's symbols are distinct from frozen G2's coefficient alpha.

The candidate's equation (7) and the frozen G1 are identical, with the names `(f,g)` replacing `(m,p)` and `(r,s)` interchanged harmlessly. Both take a genuine arithmetic opposite-vertex pair. Equation (9) gives

```
(Q+Qopp)/2 = −F + kappa (F·n)n/[alpha+beta(F·t)²].
```

For `n=(x,y)` and `t=(-y,x)`, exact identities are

```
alpha+beta(F·t)² = (Lx² x²+Ly² y²)/(Lx² Ly²),
kappa Lx² Ly² = (Lx² Ly²+Lx² b²−Ly² a²)/b².
```

These are precisely frozen G2 with `A=Lx`, `B=Ly`. Thus the candidate already contains the central focal/support/Vieta simplification that the independent audit rediscovered. The reduction is not an appeal to projective invariance of Euclidean means: equation (12) explicitly calculates how the normals and coordinate weights transform.

## Independent global check of the trace proof

PDF p.3 equations (11)–(13) take the outer ellipse to the unit circle and the original ellipse to a strict concentric ellipse with squared semiaxes `0<V<U<1`. Its circle vertices `z_i` have the exact trace `S_N=sum z_i z_(i+1)`. The target centroid is an affine expression in the real and imaginary parts of this trace.

PDF pp.4–5, Lemma 2 and equations (14)–(18), prove constancy rather than citing it as an unsupported extension of a dot-product theorem. All required compact-curve issues check:

1. Set `d=U−V`, `eta=U+V−1`; the strict range gives `0<d<1` and `|eta|<1−d`. The chord relation `d z²w²−z²−w²+2eta zw+d=0` follows without a square-root branch choice.
2. Completing the square gives `Q(z)=d[z⁴−2chi z²+1]`, `chi=(1+d²−eta²)/(2d)>1`. Its four distinct nonzero roots give irreducibility and smoothness where the quadratic coefficient is nonzero. At `dz²=1`, the finite derivative is nonzero when eta is nonzero, and no finite point exists when eta is zero. At infinity the chart is `(d−x²)w²+2eta xw+d x²−1=0`, so `w=±1/sqrt(d)` has nonzero derivative. The `(infinity,infinity)` point is absent. The symmetric chart covers the remaining boundary. This is a connected smooth compact curve; no missing singularity or discarded branch is used.
3. The degree-two deck involution and coordinate exchange extend to a global automorphism, including apparent affine coefficient zeros. The physical unit-circle branch has two distinct tangent choices; the actual nonbacktracking step chooses the other root. Infinitely many oriented pairs from the prescribed family satisfy `T^N=id`, forcing the two meromorphic coordinate differences to vanish globally. One sampled orbit alone is not substituted for the infinite family.
4. At a pole of `z_j`, both adjacent coordinates are finite because `(infinity,infinity)` is absent. Their two incident products combine exactly into `−2eta/(d−z_j^(-2))`, holomorphic there. Simultaneous pole indices are nonadjacent, so their incident cyclic edge-label sets are disjoint. Every singular term is counted once; all remaining terms have finite coordinates. The eta=0 case is included, where `T(z,w)=(w,−z)` and four-step trace vanishes. Hence the whole trace is pole-free, and compact connectedness makes it constant.
5. Conjugation preserves the curve and commutes with the real-coefficient automorphism, so the global constant is real. Equation (13) therefore gives the original focal-axis mean. Orientation reversal preserves the symmetric cyclic edge products. Focus swap negates the centroid by central symmetry (equivalently reflect the whole family in the minor axis).

The trace lemma itself needs neither evenness nor primitivity, but the geometric pair formula requires the actual even least-period antipodes. This distinction is correct and does not admit a padded odd primitive orbit. No fixed-conic centroid theorem was invoked for the inverse-ellipse quartic.

N=4 zero follows within this framework as well. A centrally symmetric cyclic four-gon is a rectangle; its two perpendicular support distances to the concentric inner ellipse have squared sum `U+V=1`, so eta=0 and `S_4=0`. Substitution `lambda=a²b²/(a²+b²)` gives `kappa Ly²/2=1`, and equation (13) gives the zero centroid. The candidate's basic theorem does not list N4zero as a newly separate result, but its equations imply it. The frozen G7 independently checks the same value.

## What the classical formula contributes

Retain the frozen normalization: caustic semiaxes `1,q`, `q=sqrt(1−k²)`, `v=2K tau/N`, `s=sn(v)`, `c=cn(v)`, `d=dn(v)`, original axes `a=d/c`, `b=q/c`, focus `(k,0)`, and `lambda=q²s²/c²`. Here `d` denotes Jacobi dn(v), not the compact curve's U−V.

The actual affine outer coordinates are

```
z(u)=−sn(u)+i cn(u).
```

Direct addition gives, with `D0=1−k²s²sn²(u)`,

```
Re[z(u−v)z(u+v)] = 2d² sn²(u)/D0−1,
Im[z(u−v)z(u+v)] = −2d sn(u)cn(u)/D0.
```

The frozen dn difference identity makes the imaginary sum telescope. The frozen exact match to Khare–Lakshminarayan–Sukhatme (2003), main equation (5), or directly their independently pinned local zeta addition (12), gives

```
S_N/N = 2d²/(1−k²s⁴) · [s²+Z(2v)/(k² sn(2v))]−1,
Im S_N=0.
```

Since `kappa Ly² d² = H0/c²`, with `H0=1−2k²s²+k²s⁴`, candidate equation (13) is exactly frozen G7. This provides a simpler real telescoping proof and a closed analytic value, while agreeing with the candidate's complete constancy proof. The main paper leaves the general value as a real circle trace and gives six- and eight-period examples; it does not present this zeta evaluation. An alternate derivation/value expression can be useful without establishing a new basic result or historical anticipation of the application.

The old general-theorem search remains useful and accurately qualified. The cyclic sn trace was already an established theorem. The geometric bridge was still required to apply it to k407. Schwartz–Tabachnikov centroid conics, weighted CCM, Weill's homothetic construction, circle adjacent dot-product invariants, focal-polar perimeter invariants and pedal-foot sums did not directly supply that bridge. Ferudun's exact current manuscript does supply it and proves its specific complex-bilinear trace, with attribution to earlier compactification methods. Neither this manuscript nor this audit proves an absolute-firstness claim.

## Reproducible checks and remaining limits

`verify_comparison.py` independently checks 12 exact identities, including coefficient equality, compact-curve completion/cancellation, the N4 case, and both parts of the actual circle-product trace. It checks 276 configurations at 80 decimal digits over the same noncircular moduli, even N and all tested coprime star steps as the frozen derivation. Maximum observed discrepancy is `8.258336181e−77`. These are diagnostics, not interval proofs. The algebra and global arguments supply the general result; finite tests do not replace them. Frozen own diagnostics separately cover 552 actual original tangent/antipedal configurations, both original foci, at 90 digits.

The finite historical search cannot rule out unindexed literature or a different prior formula. No direct claim that this value formula is historically novel is warranted. The independent freeze establishes this audit's chronology and separation from the candidate body, not intellectual priority. No external individual was contacted, and no Git/provider/paper/disposition record was changed.
