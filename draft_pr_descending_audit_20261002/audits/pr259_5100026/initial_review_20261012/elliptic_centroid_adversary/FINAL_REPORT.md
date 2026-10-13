# Independent analytic audit of PR259 / k407

UTC 2026-10-12T11:57:19.861545+00:00; checkpoint completion **95%** (analytic-family audit). Input head **0524ed734ee8185681d030af98088259134a6af7**; submitted PROOF SHA256 **77afb7626fd4685b9ce7537aa2de3141df8bf087c5eff0698bb1f7834bc0ad7c**. No priority/novelty judgment. Existing AI audits were not treated as premises or human peer review.

## Mathematical conclusion and exact scope

The submitted PROOF is mathematically supported for its stated domain: strict confocal elliptical caustic, a>b>0, original-ellipse focus, and **least even** period, with all coprime primitive stars included. The proof establishes finite unique real outer/antipedal intersections, phase-independent arithmetic vertex centroid, focal-axis location, negation between the two focus choices, and the separate N=4 zero case. No central mathematical gap was found. This is an analytic-family conclusion; Root decides overall disposition after independent families and source-scope assessment.

The primary k407 Table5 cells literally say **even**, not **least even** or **primitive**. The submitted theorem supplies that needed qualification explicitly. An arbitrary even-length vertex list cannot be included: an exact repeated-odd witness below falsifies that reading. This is a source-scope issue to state explicitly, not a reason to assert the least-even proof false.

The extra hypothesis “the centroid points opposite M and lies between the foci” was an attack target supplied at family intake. It is **absent** from submitted PROOF lines7–15 and from the primary k407 value cell, which is unspecified. An exact primitive8/3 witness refutes only that strengthening. Preserve the pre-proof derivation as historical evidence of independent work; do not present the witness as a failure of the submitted theorem.

## Independence and mechanism

Read only INTAKE plus permitted SOURCES/SOURCE_GATE/metadata/README before constructing PLAN, INDEPENDENT_DERIVATION, and independent exact/numeric scripts. INDEPENDENCE_FREEZE.json pins all those bytes before the first PROOF read; HASH_REPLAY_RECEIPT confirms they remain unchanged. No historical review, submitted verification script, other new-family verdict, or Root odd-repeat certificate was read.

The independent route differs from the submitted residue-vector computation. In Jacobi uniformization P(u)=(a sn u,b cn u), derive R(u)=(a dn(v) sn u/cn(v),b cn u/cn(v)). Solve normal equations and remove the common dn(u) factor from the difference equation. Then U(u) depends rationally on sn u,cn u and obeys the involution

    U(2K+2iK'−u)=U(u).

Exhaustively classify its endpoint/focal possible poles, prove they are at most simple except the separately handled v=K/2 case, and show every involution partner lies in the same real delta orbit for primitive even N. Their residues cancel in the trace. A holomorphic elliptic trace is constant; real focal-axis reflection forces its y coordinate to zero. The complete derivation and direct N4 polynomial control are in INDEPENDENT_DERIVATION.md. The initial wrong-coordinate parametrization was rejected by the confocal support check and retained in the log; no blocked route was reopened by assuming a cyclic identity equivalent to the target.

## Line-by-line audit of submitted PROOF

| Submitted lines | Status | Check and implication |
|---|---|---|
| 7–15 | Supported, scope explicit | Strict ellipse/elliptical caustic, original focus, least-even period, arithmetic mean, primitive stars. Two focal centroids are negatives of each other; no inside-segment or direction claim. Repeated odd excluded explicitly. |
| 19–29 | Supported by primary source and direct geometry | Stachel Theorem4.3/(4.9), printed1614, gives P=(−a sn,b cn), a=d/c,b=k'/c, v=2K tau/N with gcd. a²−b²=k² and even primitive tau odd. Our b=1 normalization rescales this exactly. |
| 31–40 | Independently derived | Jacobi addition and the two original tangent equations give actual R=(−a d sn/c,b cn/c). No assumption that the outer locus is confocal with the original ellipse. |
| 42–51 | Supported | Equation(3) is equivalent to (R−M)·U=|R|²−M·R. Cramer determinant(4) has positive real factors and a+kS≥a−k>0. Tangent intersections also stay finite in0<v<K. |
| 55–60 | Supported | Common lattice4K,4iK'; sn/cn poles, dn zeros, antiperiods and dn real period2K agree with DLMF22.4. Bilinear, rather than Hermitian, continuation is required and supplied. |
| 62–64 | Supported | At dn zeros the endpoints coincide, D0=c²≠0, a±1≠0, determinant has simple zero, and both analytic Cramer numerators vanish. Quotients are removable. Our independent difference-equation cancellation proves the same removability. |
| 66–68 | Supported | At phase Jacobi poles endpoints are regular; the product D(a+kS)/D0 has a finite nonzero limit. No residual pole. |
| 70–80 | Supported | Focal roots S=−a/k are simple. Common tangent passes through original M and has isotropic normal n·n=0, so both q endpoint vectors have bilinear square0. Numerators vanish. Endpoint overlap equation identifies only v=K/2, hence leastN=4. The independent route allowed potential focal simple poles and canceled their trace partners; individual removability here is a valid stronger local fact. |
| 82–86 | Supported, exhaustive | Single singular endpoint, determinant order−1, right-side order at most−2, numerator order at most−2, quotient order at most−1. Q/D0 roots are precisely endpoint locations. All other determinant zeros were covered; no extra dn/focal/phase-pole class omitted. |
| 90–98 | Supported for all coprime stars | Primitive even tau odd supplies antipodal indexN/2. A real delta orbit has precisely two outer-vertex poles separated2K. Pole neighbors Q,−Q follow from the imaginary shift plus parity. |
| 100–112 | Independently checked exact algebra | V satisfies L·V=L·L and(Q−M)·V=0; V=−(L·L)J(Q−M)/det(L,Q−M). The four incident residues cancel exactly. Edge indices are distinct forN≥6, avoiding N4 collision. POSTFREEZE_EXACT checks the unrestricted vector identities and8,156 integer star cases. |
| 114–116 | Supported | Pole-free coordinates on compact torus are constant. Focal-axis reflection fixes M and reverses endpoint order; central reflection changes focus and negates centroid. No dependence on signed-area denominators. |
| 120–131 | Supported independently | v=K/2 yields outercircle, antipodal cyclic quadrilateral hence rectangle. Ellipse support matrixb²I+MMᵀ givesh²−m²=l²−n²=b². Generic rectangle mean formula independently checked symbolically. Our independent four-circle Jacobi control also yields both coordinates0. |
| 133 | Supported as additional model | Circular original focus isO; even primitive orbit and outer polygon are centrally symmetric and real normal determinant nonzero. This is a direct circle argument, not an invalid k=0 substitution in formulas dividing byk. |
| 137–141 | Mathematics/source credit supported; no priority judgment | Classical input is explicitly credited. Primary table matches outer focal antipedal vertex centroid and parityeven. The arXiv-v11/final-title distinction is already recorded in SOURCE_TITLE_CORRECTION; no mathematical change follows. Historical/provenance claims outside this family's remit were not certified. |

## Exact boundary witnesses

### Extra sign/segment hypothesis, primitive8/3

Set b=1,k=3/5,v=3K/4,lambda=(25−10sqrt5)/3,a²=(−25+15sqrt5)/8,f²=(−33+15sqrt5)/8. This is strict confocal elliptical and gcd(8,3)=1. The independently derived antipodal identity gives

    [Ux(t)+Ux(t+2K)]/(2f)
       =[D²sn²t−C²]/[C²(1−k²S²sn²t)].

For t=0 its four pair phases have sn² values0,5/9,1,5/9. Therefore centroid_x/f=(11+5sqrt5)/8>1 and centroid_y=0. This refutes the extra location hypothesis, not k407 or the submitted theorem.

### Odd least period repeated to an even list

Set b²=1,a²=8/5,lambda=8/9,k²=27/32. Choose sn v=2sqrt2/3,cn v=1/3,dn v=1/2. Exact duplication gives sn2v=sn v,cn2v=−cn v,dn2v=dn v; real0<v<K impliesv=2K/3 and least period3. For original M=(sqrt15/5,0), one outer triangle is

    (−4/sqrt5,1), (4/sqrt5,1), (0,−3).

Its three antipedal vertices have arithmetic centroid(sqrt15/3,−6/5). The focal-axis reflected phase has centroid(sqrt15/3,+6/5). Doubling each triangle's traversal produces a six-entry even list with these same two different centroids. All real normals remain nonsingular. The numerical grid alone is not needed for this conclusion; POSTFREEZE_EXACT gives exact algebra and parameter certificates.

## Reproducibility, source receipts, and remaining gap

Use Python3 with SymPy1.14.0 and mpmath1.3.0. From this folder install dependencies with `python3 -m pip install --target vendor sympy==1.14.0 mpmath==1.3.0`, then run `python3 independent_exact.py`, `python3 independent_numeric.py`, and `python3 postfreeze_exact.py`. The scripts prefer local vendor and do not read source PDFs, submitted scripts, private credentials, or unrelated workspace files. Installed vendor and source-reading bodies are excluded from the packet. Recorded execution used bundled Python3.12.14.

All pre- and post-freeze exact controls passed. The independent direct tangent/normal numeric construction covers32 cells (k=.01,.6,.95,.999; low/large even periods and coprime stars) at70 digits. Maximum phase spread4.54e−68 and maximum |y|5.55e−69; these are diagnostic support, not an all-period proof. Tiny/near-separatrix moduli stress the strict-domain limits without claiming excluded lambda=0,b² endpoints.

Primary references actually inspected: [Stachel, Theorem4.3/(4.9)](https://repositum.tuwien.at/bitstream/20.500.12708/136087/1/Stachel-2022-European%20Journal%20of%20Applied%20Mathematics-vor.pdf), [DLMF periods/poles/zeros](https://dlmf.nist.gov/22.4), [DLMF addition formulas](https://dlmf.nist.gov/22.8), [arXiv-v11 Section3.5/Table5](https://arxiv.org/pdf/2004.12497v11), and [final paper Table5](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf). SOURCE_GET_RECEIPT hashes the three successfully downloaded primary PDFs; DLMF command-lineGET returned403, while web-tool readings succeeded. No outside individual was contacted or messaged.

**Exact remaining gap:** none found in the stated least-even mathematical theorem. A broader literal even-list interpretation is false by the exact repeated-odd certificate; primary source wording does not explicitly resolve that qualification. Priority/novelty, human peer review, and overall acceptance remain outside this report. No Git/provider/ref/index/checkout/shared-file mutation was performed.
