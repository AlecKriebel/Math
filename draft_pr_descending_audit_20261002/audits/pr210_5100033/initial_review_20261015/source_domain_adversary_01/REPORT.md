# PR210 independent source, domain, geometry and full-proof audit

Audit of head `2180d64b648b81ac660a792f7823d0b715f9cf12`, problem 5100033 / AMR-050-0033. Author: source/domain adversary 01. UTC evidence freeze began 2026-10-15T11:57:03Z. The immutable original is the sibling `submitted/unsolved_math_prioritization/attempts/5100033` tree.

## Disposition and strongest verified result

**The exact source identification is verified, and the submitted proof establishes the stated invariant for every real noncircular ellipse with a strictly nested nondegenerate confocal elliptical caustic and an odd least period, including every primitive star turning number. No mathematical counterexample or unresolved central proof gap was found in this audit.** This is a mathematical/source recommendation to the parent reviewer, not a promotion of the PR or a novelty certification. All numerical results below are explicitly uncertified.

The exact target is the product of the two **signed, ordered, outer tangent polygon focal-pedal areas**. It is arXiv 2004.12497v11 Table 7, printed p. 9, `k605,a`, and published Table 7, printed p. 349, `k606`. Published `k605` is the original-orbit/unprimed product. All three source PDFs hash-match the immutable submission's `source_manifest.json`; see `SOURCE_HASHES.json`.

Two wording improvements would make the source audit more precise, without changing the theorem or its proof:

1. The source articles do not explicitly impose least-period/primitive/repetition conventions or discuss stars. Primitive star coverage is a consequence of Stachel's theorem plus the submitted argument; exclusion of relabelled repetitions is a stated scope convention of the submitted theorem. Avoid presenting all those choices as explicit source exclusions in the phrase “restored source scope.” Repetition is harmless: a path traversed r times has each signed pedal area multiplied by r and the product by r².
2. The invariant articles' outer tangent polygon construction appears in Figure 1 and its caption in the introduction, and in the pedal sections and figures. `SOURCES.md` attributes the outer construction to Section 2 too broadly. Section 2 supplies signed-area conventions, while Figure 1/Sections 3.4 and 3.7 establish the outer/prime construction. This is a locator correction, not a wrong invariant.

## Independence, scope and artifacts

Before any verification code or inherited review was inspected, I read only `INTAKE.json`, the original `PROOF.md`, `SOURCES.md`, and `source_manifest.json`, then froze `FROZEN_CLAIM_MAP.md`. I have **not read** the original `verify.py`, `verification.json`, any original `independent_review` file, readiness report or other agent's mathematical report. The fresh control program has no imports or reads from those materials. This preserves independence throughout this audit.

Authored public artifacts are this report, the frozen map, the log, source hashes, `fresh_control.py`, `FRESH_CONTROL.json`, `.gitignore`, and the authored manifest. Source PDFs, extracted text and rendered pages reside only in ignored `private_reading/`; no paper is redistributed by these authored artifacts. No Git/provider mutation, SQLite write, outside communication or other audit-shard communication was performed. Parent coordination used the team channel only.

## Primary-source verification

The following locators were checked in the exact hash-bound reading copies. The critical pages were rendered and viewed, including complete table headings, parity and proven columns, primes, explanatory text, captions, and equations.

| Source | Exact primary evidence | Finding |
|---|---|---|
| [Reznik–Garcia–Koiller, arXiv v11](https://arxiv.org/pdf/2004.12497v11) | Printed/PDF p. 1, introduction and Figure 1; pp. 2–3, Section 2 and (1); pp. 7–8, Section 3.7; p. 9 Table 7 | Two confocal ellipses; noncircular a>b>0; signed cross-product area; prime means outer polygon; `k605,a` is the primed focal-pedal area product for odd N, proven column `?`. |
| [Published companion](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf) | Printed p. 341 introduction; p. 342 Figure 1; p. 343 Section 2/(1); p. 346 Section 3.4; p. 349 Table 7/Section 3.7 | Same geometric primed product, now `k606`, odd N and proven column `?`; `k605` is unprimed. PDF page 9 is printed p. 349. |
| [Stachel, published article](https://doi.org/10.1007/s40879-021-00524-2) | Printed p. 1604 domain restriction; p. 1606 turning-number definition; p. 1613 canonical amplitude/modulus context; p. 1614 Theorem 4.3/(4.9); p. 1615 Corollary 4.5 | Theorem 4.3 covers all confocal outer ellipses with the given elliptical caustic, arbitrary initial phase, and coprime turning numbers. The restriction tau=1 belongs to Corollary 4.5, not Theorem 4.3. |
| [DLMF 22.4](https://dlmf.nist.gov/22.4), especially Tables 22.4.1 and 22.4.3 | Official online primary reference, accessed 2026-10-15 | Periods, simple poles and exact real/imaginary/quarter translations agree with the proof. |
| [DLMF 22.8](https://dlmf.nist.gov/22.8), equations 22.8.1–3; [22.13](https://dlmf.nist.gov/22.13), Table 22.13.1 | Official online primary reference, accessed 2026-10-15 | Addition and derivative identities agree with the proof. |

The original invariant papers do not supply a formal domain discussion of all winding numbers. Their experimental descriptions mainly illustrate simple polygons and even contain a simplification suggesting a unique caustic per N. That does not defeat a proof for the stronger primitive-star domain; it does mean star coverage should be stated as proved coverage rather than an explicit quote from the invariant table. The rows themselves say odd N without an explicit least-period qualifier.

I also checked a typographical issue in Stachel's source: printed p. 1613 displays `dn(u+2kK)=(-1)^k dn(u)`, which is false for odd k. The correct real shift is `dn(u+2K)=dn(u)`, as in DLMF 22.4.3. The submitted proof does not use that erroneous line; its required Jacobi translations come from DLMF and are correct. Theorem 4.3/(4.9) uses `dn²=1-m² sn²` and is unaffected by that nearby typo.

## Canonical coverage of every asserted real physical family

Let the real outer semiaxes be a>b>0, the strictly nested caustic semiaxes alpha>beta>0, and

    c² = a²-b² = alpha²-beta² > 0,
    k=c/alpha in (0,1), k'=beta/alpha.

Because beta/b is strictly between 0 and 1, there is a unique v in (0,K) with `cn(v)=beta/b`; cn is continuous and strictly decreasing from 1 to 0 there. The confocal relation gives

    alpha² dn²(v)
      = alpha²-c²(1-beta²/b²)
      = beta²(1+c²/b²)
      = beta² a²/b².

All quantities are positive, so Stachel's semiaxis formulas follow:

    a=alpha dn(v)/cn(v), b=beta/cn(v).

Thus an arbitrary physical family in the theorem's domain is covered; this is not merely a construction of some example families. Stachel's first part gives the orbit phase `w+j delta`, `delta=2v`, for every initial real phase. The real parametrization `P(w)=(-a sn(w), b cn(w))` is injective modulo 4K: the pair sn,cn fixes the real amplitude modulo 2pi. Closure of least period N therefore means

    N delta=4K tau, gcd(N,tau)=1.

Since `0<delta<2K`, `0<tau<N/2`; reversing physical orientation changes the sign of the shift and both signed areas. The canonical ellipse map winds once per 4K, so tau is the ordinary winding number, including stars. Distinct phase vertices and the pole-index counting used later follow directly from coprimality. No unsupported extension to hyperbolic caustics, collapsed caustics, or a circular analytic torus is required.

## Independent real geometry and side correspondence

For a real ellipse point `P=(x,y)`, the tangent is

    n.X=1, n=(x/a²,y/b²).

The orthogonal foot from `(c,0)` is

    Q=(c,0)+(1-cx/a²)n/(n.n)
     =(a²(c+x)/(a²+cx), a²y/(a²+cx)).

Substitution `x=-a sn(w), y=b cn(w)` is precisely the submitted formula (3). Deriving it starts with Euclidean orthogonal projection, rather than presupposing a pedal formula. The denominator `a²+cx >= a(a-c)>0` for real points. Substitution of `y²=b²(1-x²/a²)`, `b²=a²-c²`, gives both the tangent equation and `Q.Q=a²` exactly. The program checks those polynomial identities by symbolic numerator reduction modulo the ellipse equation. The other focus formula follows by c→−c, or by antipodal translation `Q_-(w)=-Q_+(w+2K)`.

Let `l_j` be the tangent at `P_j` and `V_j=l_j intersect l_(j+1)`. Then the ordered outer side `V_(j-1)V_j` lies on `l_j`. Consecutive real tangents would be parallel only if their ellipse points were antipodal. Injectivity of the real canonical parametrization would then force `delta=2K mod 4K`, impossible for `0<delta<2K`. They therefore intersect finitely for every real phase, including stars. A side cannot collapse to zero length: that would put three distinct tangents through one point, whereas a nonsingular real conic admits at most two tangents through a point. This last noncollapse detail is implicit rather than spelled out in the original proof; it is an elementary completion, not an additional substantive hypothesis.

Consequently outer-side pedal feet are exactly the feet on `l_j` in the billiard's cyclic order, possibly after a cyclic shift. The argument does not reorder vertices by polar angle or take the boundary of the union of star regions. Reversal multiplies each signed shoelace area by −1. Winding-weighted cross-product area is the source convention; geometric unsigned region area is a different definition and is not claimed here.

## Full complex-analytic proof review

I checked every step of the original proof, independently of its code.

### Meromorphic continuation and all possible poles

On the common period lattice `(4K,4iK')`, both sn and cn are meromorphic and the displayed Q formula is meromorphic. At their shared simple poles, the denominator has a nonzero leading coefficient proportional to −c, so the numerator/denominator ratios extend holomorphically; there is no overlooked singularity at a Jacobi pole.

The only remaining possible poles solve `sn(w)=a/c=dn(v)/(k cn(v))`. With `r=K+iK'`, DLMF Table 22.4.3 gives

    sn(r+u)=dn(u)/(k cn(u)),
    cn(r+u)=-i k'/(k cn(u)),
    dn(r+u)= i k' sn(u)/cn(u).

Hence the roots are `z_-=r-v`, `z_+=r+v`. They are distinct because `0<v<K`. The derivative `cn(w)dn(w)` is nonzero at each: `cn(v)>0`, `sn(v)>0`, `k'>0`. sn has two simple poles on its `(4K,2iK')` torus, hence degree two, so these exhaust its preimages of a/c there. Doubling the imaginary period gives exactly their two translates by `2iK'`, without extra roots. The degree statement follows from the simple pole list and the elementary equality of zero/pole multiplicities for a nonconstant elliptic function applied to `sn-a/c`; it does not assume the area invariant.

At both roots, `sn=a/c`, `cn=-ib/c`, so the numerator vector of Q is the same nonzero vector

    (-ab²/c, -iab²/c).

The denominator derivatives are opposite because dn at `r±v` has opposite sign. Thus the residues are nonzero, opposite and collinear. Their imaginary translates are reflected by `J=diag(1,-1)`, preserving collinearity.

### Singular area terms and reduced torus

At a fixed singular phase, exactly two vertex indices are singular. Indeed one pole is obtained from the other by `delta=2v`; coprimality ensures each of the two distinct root classes occurs at a unique orbit index. For phase `w=z_-`, they are indices 0 and 1. No other root is hidden in an imaginary translate because the phase step is real. The simultaneous singularities therefore lie on one adjacent edge, including after cyclic reindexing across the final edge.

If the two singular endpoints expand as `R/eps+A+O(eps)` and `-R/eps+B+O(eps)`, the only possible eps^−2 coefficient of their determinant is `det(R,-R)=0`. Every incident term thus has at most a simple pole. This covers the potentially dangerous adjacent two-pole term; merely assuming at most one singular endpoint per term would have been false.

The full cyclic sum T has periods 4K and delta: translating by delta permutes all N edges, and the closing edge is legitimate because `N delta=4K tau` is a true period of Q. Bezout gives real period `L=4K/N` from `delta=tau L` and `4K=N L`. All real translates of the possible poles collapse to

    b+iK', b+3iK', b=K-v,

on `C/(L Z+4iK' Z)`, with orders at most one. The two points remain distinct, since `2iK'` is not in that selected lattice. The argument works equally for primitive stars and ordinary primitive orbits.

### Symmetry and zero divisor

DLMF gives `Q(w+2iK')=JQ(w)` and `Q(2K-w)=JQ(w)`. The first yields `T(w+2iK')=-T(w)`. For the second, reversal of the cyclic edge order adds a second minus sign to `det(J)=-1`, giving `T(2K-w)=T(w)`. Since T has period `2v`, the centered function `F(z)=T(K-v+z)` is even. I checked this reindexing explicitly; neither sign is omitted.

If T has no poles, it is constant on a compact torus, and its anti-period forces zero. Otherwise the anti-period forces both candidate poles to be present and simple, giving total pole multiplicity two. At `z0=iK'+L/2`, evenness and real periodicity identify `F(z0)` with `F(z0-2iK')`, while the anti-period makes it its negative. This is a regular point because `L/2` is not zero modulo L, so `F(z0)=0`. Its anti-period translate is a second distinct regular zero. Equality of total zero and pole multiplicities makes both zeros simple and exhaustive.

Every possible pole of `F(z)F(z+L/2)` is therefore canceled by the translated zero of the other factor. The product is a holomorphic elliptic function, hence constant. This includes the zero-function branch and introduces no division by an area or residue. No hidden nonvanishing assumption is needed.

### Odd-period focus switch

For odd N, `2K=(N/2)L` equals `L/2` modulo L. Thus the two actual focal signed areas `T(w)` and `T(w+2K)` have the product just proved constant. For even primitive N, the focus shift is an integer multiple of L, giving equality of the two areas but no constancy conclusion. Both the logic and the fresh even controls distinguish this parity. This verifies the submitted conclusion in its entire stated real domain.

## Boundary and limiting-case ledger

| Case | Status and reason |
|---|---|
| Odd N=3 | Covered: only one primitive winding; the adjacent singular edge still has the stated cancellation and all other terms have at most one singular endpoint. |
| Odd composite N | Covered when gcd(N,tau)=1; N=9 controls include tau=1,2,4. Noncoprime labelling is a repetition of a shorter orbit. |
| Stars close to half winding | Covered for tau=(N−1)/2; delta remains strictly below 2K, so no outer side intersection is infinite. Tested through N=13. |
| Repeated path | Outside the theorem's least-period wording but extends immediately: repeat r times gives B±→r B±, product→r² product. No new invariant proof is needed. Odd labelled N implies an odd least divisor. |
| Even primitive period | Product constancy is not established and is numerically false in all four controls; equality of the focal areas does follow. |
| Circle c=0 | Excluded from the meromorphic argument, which divides by c and changes its elliptic torus. Separately: regular star polygons rotate rigidly, both foci are the center, tangent feet are the original boundary vertices, and their areas are constant. |
| k→0 or k→1 | Interior values remain covered; near both ends were tested. No step sets k to an endpoint. k=1 would collapse the caustic minor axis and is excluded. |
| v→0 | For fixed finite N and positive primitive tau, v=2K tau/N is positive; v=0 is a limiting collapsed step/coincident ellipses and is outside the theorem. |
| v→K | Corresponds to an infinite outer ellipse in fixed-caustic scaling or a degenerate boundary in other normalizations; v=K is excluded. For finite real families, cn(v)>0. |
| Hyperbolic or collapsed caustic | Excluded by both the exact theorem and the source articles' two-ellipse setting. Stachel mentions other correspondence results, but no extension is invoked here. |
| Axial vertices | Included: real projection denominators remain positive; numerical phases include an axis. |
| Vanishing signed pedal area | The analytic proof never divides by it and has an explicit no-pole/zero branch. No extra assumption is introduced. |
| Units/scaling | P,Q,outer vertices have length units; B has length² and its product length⁴. Controls include alpha=10^−5 and 10^5 and compare products normalized by a⁴. |

## Fresh standalone computation

Reproduce from this folder with:

```text
/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python -B fresh_control.py > FRESH_CONTROL.json
```

`fresh_control.py` deterministically prints JSON, uses mpmath 1.3.0 at 75 decimal digits and SymPy 1.14.0, and reads no other artifact. It chooses outer semiaxes from the source canonical closure formula, starts at five ordinary eccentric-angle phases, and then constructs the entire actual billiard **without using Jacobi functions in the stepping routine**. The two tangent contact points are solved after mapping the caustic to a unit circle; the positive-winding tangent is continued to its second intersection with the outer ellipse. It independently verifies the reflection law, closure, winding, caustic tangency, and agreement with the canonical vertex formula. Tangent intersections give outer vertices; Euclidean line projection onto their actual ordered sides gives the feet. The closed foot expression is used only for a comparison check afterward.

Results in `FRESH_CONTROL.json`:

- 86 real family cases: 82 odd cases, four even controls. Every coprime winding for N=3,5,7,9,11,13 is tested for k=0.000001, 0.37, 0.97, 0.999999, plus two independent scale cases. Each has five phases.
- Largest odd normalized product span: `3.4366147344e-70`. Largest recorded real dimensionless error: `2.6874871627e-70`. These are arbitrary-precision residuals, **not certified bounds**.
- Four even normalized product spans, N=4,6,8,10 respectively: approximately `0.0506839`, `0.00649298`, `0.000390272`, `0.0000418301`. Thus a program silently imposing constancy on all parities would fail these controls.
- Reversal, cyclic indexing, threefold repetitions, auxiliary-circle property, and the focus switch pass. The actual outer-side feet differ materially from chord feet, so the construction check would detect that target substitution even though the unprimed odd product has its own separate source invariant.
- Symmetric **nonfocal** points `(±c/2,0)` give varying products; the largest tested odd span is about `0.3860`, distinguishing a focal-specific invariant from a generic symmetric-pair assertion.
- Three independent complex parameter cases check the exact quarter-shift identities, opposite/collinear residues, real reduced period, imaginary anti-period, reflection, forced zero and constant half-period product numerically. The maximum of those residuals is `3.5626523511e-74`. Near-pole samples show eps*T stabilizing while eps²*T tends to zero. This is supportive evidence only; the proof establishes orders and exhaustiveness.
- 236 exact integer lattice cases for N<40 check coprime orbit cardinality, the exactly two adjacent pole indices and odd/even half-period character. The universal reason is the modular arithmetic argument above, rather than the finite enumeration.

The computation is a deterministic falsification aid and control artifact. It is not an interval certificate, a proof of the source theorem, or a substitute for the analytic review. A fresh subprocess replay matched `FRESH_CONTROL.json` byte for byte; `CONTROL_REPRODUCTION.json` records both hashes and the exact interpreter. The same final check rehashed all 20 immutable original files against `INTAKE.json`; every file matched.

## Remaining gaps and fixes

**No unresolved mathematical gap within the exact stated theorem was found.** Recommended locator/scope wording fixes are the two small source-precision edits at the start of this report. The elementary noncollapse justification for the outer sides can also be added for completeness.

This shard does not resolve exhaustive historical priority, all later literature, novelty, author metadata, packaging policy, or the final repository promotion decision. Those were outside this source/domain family audit. The proof correctly credits Stachel and classical Jacobi/elliptic-function facts and does not itself claim novelty. No present result establishes anything for arbitrary unsigned star-region areas, hyperbolic/degenerate caustics, or an even-period product invariant.
