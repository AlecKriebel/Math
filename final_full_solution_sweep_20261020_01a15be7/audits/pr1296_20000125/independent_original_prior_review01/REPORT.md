# Independent full-candidate review: PR1296 / 20000125

The full pinned mathematical theorem passes adversarial review: for every prime p, n≥2 and d≥n+1 there is a geometrically smooth, geometrically integral degree-d hypersurface over the original field Fp whose Fp-point count is not1 modulo p. The same-equation coefficient selection and every characteristic/degree branch are justified below. Credit belongs to Alper Ferudun's existing unrefereed, AI-assisted preprint *Smooth Hypersurfaces Beyond the Chevalley-Warning Range over Prime Fields*, version1.0, 6 September2026, [DOI10.5281/zenodo.22514087](https://doi.org/10.5281/zenodo.22514087), concept **10.5281/zenodo.22514086**. This is an AI-only mathematical/source audit, not a new theorem, earliest-priority finding, human-referee certification or publication approval.

There are two source/package qualifications. The current official AIM page could not be fetched, and its historical HTML body is unavailable: it is not claimed read here. The original AIM wording is bound to the actual cached statement and the task's supplied source context; the separate original2015 smooth question was directly read. Also, the source ZIP contains a historical workdir manifest rather than a closed inventory of that ZIP. Its actual21 entries are intact; additional historical build files are absent. These limits are kept distinct from the mathematical proof.

## Exact original scope and immutable PR

The actual read-only catalog/cache record20000125, AIM-ALGEBRAIC_GEOMETRY-0125, asks for each p,d with d≥n+1 a degree-d hypersurface over Fp with either point count not1 modulo p or failure of rational connectedness. Its statement has no explicit smoothness hypothesis. Its SHA256 `ded9781b5f46cc78236d8003698f575ee8de3dc5868eb145e2e52dabe595002a` matches the current catalog digest. The literal numerical disjunct has classical norm-form witnesses, so the stronger smooth theorem must not be marketed as discovering that elementary literal answer.

The current official [AIM9.5 endpoint](http://aimpl.org/ratsubvarpos/9/) gave HTTP/HTTPS timeouts and a web-tool502. The historical44,968-byte HTML identified in the PR's old source pins was not located, and its body was not inspected. This is the exact remaining original-source-access limit. No current official-page fetch or old HTML reinspection is manufactured from the cached record.

The original [MathOverflow question220163](https://mathoverflow.net/questions/220163/smooth-complete-intersections-and-sharpness-of-the-chevalley-warning-theorem), asked6 October2015 and edited8 October2015, was read directly through the web tool. Its edit explicitly asks for a smooth hypersurface for each d,p,n in the same degree range, over the specified prime field; the post acknowledges unsmoothed norm examples. Its listed answers give partial Fermat/pencil examples, not an all-triples theorem. Its opening also discusses more general complete intersections and prime-power fields; the present theorem makes no claim to cover all those generalizations.

The theorem proves the numerical AIM alternative and the explicitly smooth hypersurface question for n≥2. The separate n=1 classical example is smooth and point-free but is not geometrically integral; no n=0 assertion is imported. No identification of rational connectedness with separable rational connectedness or an unproved implication from a canonical divisor is required, since the numerical disjunct already holds.

The full live PR body and all ten immutable head files were read. Read-only object retrieval independently binds head `691b2614be70c450bb14b81fc990379d14cddbad` against base `5c5d4c9d7a2ea547fdf8a35cf874f604cec27bed`: exactly ten additions,46,785 bytes, no QUEUE change, and live head/base agreement. Full `PROOF.md` has15,125 bytes, SHA256 `94e5e97292aa9b3c8eaa37500a2749bc85a9c462f7a99c24e6a69569c7793182`. The PR's own nine-payload manifest also matches every supplied byte and digest. Its historical aggregate diagnostic claims are not called newly reproduced here.

## Actual prior paper, DOI family and support inventory

Fresh Zenodo/API and DataCite records authenticate Alper Ferudun, Mercury Software GmbH, the exact title, version1.0 and publication date2026-09-06. Both version and concept DOIs are findable and resolve200 to record22514087. The reciprocal version/concept relations and live versions endpoint show one current version,22514087. The actual [publisher page](https://eulersolve.org/papers/aim-algebraic-geometry-0125/) was read through the web tool and explicitly calls the paper an unrefereed AI-assisted preprint. Direct publisher-byte capture failed403; no local HTML hash is invented.

Following the disk-allocation constraint, the three already downloaded immutable root payloads were reused read only and independently rehashed against fresh record checksums. No duplicate large body was downloaded. All sizes and MD5 checks match:

| Payload | Bytes | SHA256 |
|---|---:|---|
| Source ZIP |178,599|`8a74df8b764a199cee3821597d0f95fdb69b46bc9d864332ab8c06150a60bebd`|
| Verification report |6,524|`3af22b5495852b4f2a738b2833a87d464de3fe11f8b2016c7effaf467b49d9c0`|
| Paper PDF |110,570|`97c4f88da7fd9e70bb50e4679209ba2c5d5483be2648a31b54e274da0e3d0fb4`|

All nine actual PDF pages were read. Theorem1.1 is on p.1; moment selection is pp.2–3; odd-characteristic selection is pp.3–4; the chain and its boundary analysis are pp.4–5; the equal-prime and binary cases are pp.6–7; completion, scope and disclosure are pp.7–8. Pages6 and7 were visually inspected. The full archived verification report and source/novelty note were read as source claims, not authority for correctness or priority.

All21 ZIP entries are regular files and were read with CRC and SHA256 checks; `testzip()` reports no bad entry. Their uncompressed total is13,240,287 bytes. The whole ZIP was not expanded onto disk. All20 non-manifest payloads match their entries in the included historical manifest; its final source and PDF hashes match the actual release source and separately supplied paper, and the embedded report equals the standalone report.

The historical manifest declares42 workdir files,22 of which are absent from this slim archive, including renderings, build logs/receipts, submission material and a PDF that is supplied separately by the record. It also retains `UNPUBLISHED` and a null DOI from preparation. Thus it is **not** a closed archive inventory, and its historical lifecycle labels are not current publication metadata. The actual21-member source/reproducibility selection is intact and independently inventoried in this packet. No absent build artifact is represented as supplied or replayed. Source-author programs, recorded chart computations and manuscript builds were never executed. Byte completeness of the supplied selection does not certify those historical execution claims.

The source credits classical moment identities, prior diagonal-deformation families and smoothness criteria, and Gabber's undeformed chain. Its generic-prior and related-literature comparisons are not an exhaustive priority proof. The construction is derived below without importing those papers' more specialized theorems; only standard finite-field facts, Jacobian/tangent-space criterion and the two-generator height bound are needed. No broader literature claim or non-uniruledness application is certified.

## Independent universal verification

Put m=n+1≥3 and let K be an algebraic closure of Fp. All singularity arguments below take place over K. For a homogeneous hypersurface a singular point must satisfy both F=0 and every homogeneous partial derivative=0. In dividing characteristic Euler's identity does not permit dropping F. The usual affine-chart tangent-space criterion gives this test over K; over the perfect base Fp it verifies geometric smoothness.

### Moment and nonzero-grid selection

Let v have positive integer entries summing to d and Q be the monomial x^v. Let every degree-d monomial Hj omit at least one coordinate. With formal coefficient parameters A define

```
FA=Q+sum_j Aj Hj,
C(A)=(-1)^m sum_{x in Fp^m} FA(x)^(p-1).
```

The power sum of u^e over Fp is0 for e=0,−1 for a positive multiple of p−1, and0 otherwise, in Fp. The e=0 case is0 because there are p summands; replacing it by−1 would be wrong. Hence the constant coefficient of C is1, from Q^(p−1). A term Aj^(p−1) can only select Hj in all factors and vanishes because Hj misses a coordinate. Thus every individual parameter degree is at most p−2.

Evaluation on the nonzero grid is injective under these strict individual bounds: fixing all but one parameter gives a univariate polynomial of degree less than p−1 with p−1 roots, and induction applies to its coefficient polynomials. Therefore some tuple with all Aj nonzero has C≠0. At p=2, C is simply constant1.

The affine zero count is `Na=1+(p−1)Np`, while the zero indicator is `1−F^(p−1)`. Summing gives `Na=−sum F^(p−1)` modulo p, and therefore

```
Np = 1+(-1)^m C(A) modulo p.
```

Nonzero C proves the required numerical failure. The origin, scalar representatives and sign are all retained.

### Odd p not dividing d

Set t=d−m+1 and use `F=sum_i Ai xi^d+Q`, with `Q=x0^t x1...x(m−1)`. In the final parameter, the degree improves from p−2 to p−3. A would-be degree-p−2 contribution consists of p−2 copies of the last pure power and one other summand. Another pure power leaves some coordinate missing because m≥3. A Q contribution has exponent1 in a coordinate indexed1 through m−2, whose power sum is0 for odd p. These exhaust the possibilities.

No common derivative zero lies on the coordinate boundary. Two zero coordinates kill all Q derivatives, leaving a nonzero pure-power derivative at any nonzero coordinate. With exactly one zero xj, j≠0, the x0 derivative remains nonzero. With only x0=0, the derivative at any nonzero other coordinate remains nonzero. These arguments also cover t=1.

On the torus the derivative equations imply `d Ai xi^d=−vi Q`, with v=(t,1,...,1). If p divides t, the first equation is impossible. Otherwise raise equation i to its positive integer exponent vi, multiply and cancel Q^d. A necessary singularity condition is

```
d^d A0^t A1...A(m−1)=(-1)^d t^t.
```

For fixed first m−1 nonzero coefficients this excludes at most one final nonzero value. First take a count-good tuple, freeze those first coefficients, and vary the last. The nonzero univariate C has degree≤p−3, so at least two of the p−1 possible values remain count-good. One avoids the necessary singularity condition. This proves smoothness and the point-count condition for the same equation over Fp, without a generic-open-set or coefficient-field-extension assumption. At p=3 the polynomial is constant in the last parameter, and its two nonzero values still suffice.

### Chain family when p divides d: torus and every boundary stratum

For any positive v of sum d use

```
Ti=xi^(d-1) x(i+1),
F=sum_{i=0}^{m-2} Ai Ti + A(m−1) x(m−1)^d + Q,
si=v0+...+vi,
B=1+sum_{i=0}^{m-2} si in Fp.
```

All coefficients are nonzero. Every non-Q term misses a coordinate, so moment selection applies. On the torus, `d−1=−1` in Fp makes the derivative equations triangular:

```
A0 T0=v0 Q,
Ai Ti=A(i−1) T(i−1)+vi Q=si Q.
```

The last derivative equation is consistent because the full exponent sum is d=0 in Fp. A zero proper prefix si rules out a torus critical point outright. If all prefixes are nonzero, the equation's value at a torus critical point is `BQ+A(m−1)x(m−1)^d`. For B=0 this is nonzero, so the critical point is off the hypersurface. This is exactly where retaining F is indispensable.

The boundary exclusion does not require either prefix condition. With at least two zero coordinates, all Q derivatives vanish. The last derivative forces x(m−2)=0. Descending derivatives force x0 through x(m−2) all zero, using d−2≥1; the remaining axis point has nonzero F. If there is exactly one zero xj and vj≥2, the same argument applies because every Q derivative again vanishes.

For exactly one zero xj with vj=1, consider the remaining cases. If j=m−1, the first chain derivative is nonzero since m≥3 and x0,x1 are nonzero. Otherwise the last derivative forces x(m−2)=0, so j=m−2. For m≥4 the derivative indexed m−3 is the nonzero preceding pure chain contribution; its other chain and Q terms vanish, a contradiction. For m=3,j=1 all chain terms and Q vanish in F, but the nonzero final pure power remains. Thus no boundary singularity exists.

If d>p and p divides d, choose

```
max(1,m−d+p) ≤ k ≤ min(p,m−1).
```

The interval is nonempty: each lower bound is at most p and m−1, since m≤d and d−p≥1. Choose k positive entries summing to p and the other m−k summing to d−p, for example `(p−k+1,1,...,1 ; d−p−(m−k)+1,1,...,1)`. The same bounds guarantee positivity. The proper prefix p gives smoothness for every nonzero coefficient tuple, so select a count-good tuple. This includes every allowed even degree at p=2.

If d=p>m, then p≥5. Put vj=1+ej and L=p−m, so sum ej=L. Directly counting how often ej enters the proper prefixes gives

```
B=1+m(m−1)/2 + sum_j (m−1−j)ej modulo p.
```

The weighted extra term attains every integer from0 through(m−1)L: it is a sum of L weights in0,...,m−1. Quotient and remainder by m−1 construct each required sum with at most L nonzero weights. At m=p−1, the base term is2 modulo p and the available extra p−2 makes B=0. For3≤m≤p−2,

```
(m−1)(p−m)−2(p−3)=(m−3)(p−m−2)≥0,
2(p−3)≥p−1.
```

Thus the interval contains every residue modulo p and a B-zero vector exists. Again every nonzero tuple is smooth, and one is count-good. The independently coded bounded test uses residue dynamic programming rather than this interval formula.

### Equal-prime boundary d=m=p

Here p is odd. Set P equal to the product of all p coordinates, take any a in Fp* except1 (a=2 suffices), and put `F=sum_{i=0}^{p-2} xi^(p−1)x(i+1)+a x(p−1)^p+P`. The preceding boundary proof applies unchanged.

At a torus singularity, `Ti=(i+1)P`. Since the sum of1 through p−1 is0, F=0 implies `P=−a x(p−1)^p`. Multiplication and Wilson's theorem give

```
−P^(p−1)=product_i Ti=P^p/(x0 x(p−1)^(p−1)).
```

Combining gives `x0=a x(p−1)`. Normalize x(p−1)=1. Then x0=a and P=−a, and

```
x(i+1)=−(i+1)a/xi^(p−1).
```

This recurrence first proves, inductively, that every coordinate is in Fp*. Only after that descent is Fermat's identity legitimate. Its final step gives x(p−1)=a, contradicting1 and a≠1. This proves geometric smoothness over K, not merely absence of rational singularities.

For the count, every surviving monomial of F^(p−1) must have positive exponents divisible by p−1. Total degree p(p−1) in p variables forces each exponent to equal p−1. If T0 is selected e0 times and P is selected b times, the x0 equation is `(p−1)e0+b=p−1`. Either only P is selected, giving coefficient1, or e0=1,b=0. The latter requires `1+(p−1)e1=p−1` at x1, impossible for p≥3. Thus C=1 and Np=0 modulo p.

### Characteristic two, odd degree

Take t=d−m+1, `Q=x0^t x1...x(m−1)` and `F=sum_i xi^d+x0^(d−1)x1+Q`. The only full-support summand is Q, so C=1 at p=2 and the point count is even. The derivative of the repair term vanishes in x0 and contributes x0^(d−1) in x1. Consequently

```
F0=x0^(d−1)+t x0^(t−1) product_{j>0} xj,
F1=x1^(d−1)+x0^(d−1)+Q/x1,
Fi=xi^(d−1)+Q/xi for i≥2.
```

The quotients denote lowered-exponent monomials, not divisions at boundary points. If t is even, F0=0 forces x0=0, and t≥2 kills all remaining Q derivatives; every coordinate is then0. If t is odd, at least two zero coordinates kill Q derivatives and again force the zero vector. A sole zero xj with j≠0 leaves F0 nonzero. A sole x0=0 leaves F0 nonzero when t=1, and F1 nonzero when t≥3.

A projective common derivative zero must therefore be on the torus. Normalize x0=1. F0=0 gives Q=1. For i≥2, multiplying Fi by xi gives xi^d=1. The product of all remaining coordinates is1, hence x1^d=1 also. But `x1 F1=x1^d+x1+Q=x1≠0`. No rationality assumption on K-coordinates is used.

### Exhaustion, nonzero equations and geometric integrality

These branches cover all p,d≥m≥3: odd p not dividing d; p dividing d with d>p, d=p>m or d=p=m; and p=2 in odd degree. Each equation has degree d and a unique noncancelling pure-power term. All coefficient selections take place in Fp and are finite deterministic searches, with no efficient complexity claim.

Geometric integrality follows from the proved smoothness and m≥3. A repeated factor gives singularities along a projective component. If two distinct positive-degree factors G,H occur, their ideal has height at most2 in K[x0,...,x(m−1)]. Its zero locus cannot consist only of the origin, whose maximal ideal has height m≥3; thus they have a common nonzero zero. There F and every partial vanish by the product rule. This contradicts smoothness. Hence F is irreducible and squarefree over K, and its projective hypersurface is integral. The only standard dimension import is the two-generator height bound (with the algebraically closed zero-locus correspondence); no specialized Frobenius or rational-connectedness theorem is needed.

For the literal unsmoothed question, inject Fp^(n+1) linearly into F(p^d), possible when n+1≤d, and restrict the field norm. It is a nonzero homogeneous degree-d form over Fp with no nonzero rational zero. Its projective hypersurface is point-free, while over K it splits into linear factors and does not provide the main positive-dimensional smooth theorem. For n=1,d≥2, homogenize an irreducible degree-d polynomial. Finite fields are perfect, so this gives d distinct geometric points, no rational point, and a smooth finite-étale degree-d hypersurface. It is integral over Fp but not geometrically integral for d>1. No n=0 claim is made.

## Newly authored finite falsification and limits

`verify_independent.py` is new standard-library code, with no author program or external solver imported. It checks11,414 prefix compositions,240 independent residue-DP compositions,61 formal moment families and159,522 prime-field projective points. Exact equations, chosen coefficients, exponent vectors, moment polynomials and counts are retained. Eight bounded extension checks examine17,327 more projective points over F4,F9 orF25. These finite scans supplement the universal K-argument; they do not certify geometric smoothness by exhausting a finite extension.

The controls deliberately falsify tempting stronger or weakened arguments:

- Over F3, `x0^4+x1^4+x2^4+x0^2 x1 x2` has no rational singularity, but is singular at `[1,1+u,2+u]` over F9 with u²=−1. This is an explicit counterexample to rational scanning as geometric authority and to declaring all nonzero diagonal tuples smooth.
- With p=5,m=4,d=5,v=(2,1,1,1), all chain coefficients1, the point `[2,3,2,1]` has every homogeneous partial zero but F=1. Omitting F would incorrectly mark it singular.
- The forbidden a=1 equal-prime family has explicit rational singularities `[1,−1,−2,...,−(p−1)]`, checked at p=3,5,7. An arbitrary K* element need not have (p−1)-st power1; the F9 element1+u checks that the coordinate-descent step cannot be skipped.
- Dropping the binary repair gives a singular cubic at `[1,1,1]` over F2. Allowing a zero chain tail coefficient creates a boundary singularity. Wrong support/compositions, missing prefix/B conditions and wrong p/m/d domains are rejected.
- The nonzero-grid bound cannot be weakened to degree p−1: `1−A^(p−1)` vanishes on the whole grid. A degree-p−2 one-variable polynomial may have just one good value, which could be forbidden; the sharper bound is needed for the two-choice argument.
- A separately constructed F8 cubic norm has no F2 points but is geometrically singular. The binary F4 norm has two smooth geometric points, showing why smoothness does not imply geometric integrality at n=1.

All16 controls are rejected in each of normal, `-O` and `-OO`,48 total; outputs are byte-identical, SHA256 `ec6afd3fa40831bd968c07d0cee1bb270f549a85db3df450b2d7f7cbf902eeb0`. Explicit exceptions remain active under optimization. No floating-point arithmetic, author CAS scripts, historic chart bases or old raw witness files supply authority. No all-extension-fields congruence, exact point count, smooth point-freeness, efficient coefficient search or general complete-intersection result is claimed.

## Accounting, remaining gap and research status

The mandatory fresh read-only numeric-gid check preceded mathematics at10:45:23 UTC:191 nonempty rows,43 columns, no target ID or solution DOI match. The broad response-row49 concerns complex cubic KE/GIT compactifications, DOI23204952; response-row50 concerns finite-field factorization, DOI23205034. Both are distinct. A fresh28-release inventory has no exact alias lead; the current structured repository inventory contains only PR1296 for this exact source family. The bounded local search preserves raw leads privately and does not prove global absence of older packages or earliest priority.

One qualified four-literal-cell existing-publication row, B blank, is proposed in `proposed_row.json` and `.tsv`. It credits the actual Ferudun paper and retains the literal-AIM/classical-norm distinction, the main n≥2 scope and n=1 caveat, AIM source-access limit, source-manifest qualification and unrefereed AI status. Version/concept/site aliases are one paper, not extra solutions.

There is no unresolved mathematical branch in the full pinned theorem. The exact remaining original-source gap is access to the official AIM HTML body, separate from the actual cached statement and directly read2015 primary question. Historical source software/build claims and exhaustive priority remain unadjudicated. This review has no external human or formal proof-kernel certification. All earlier closed review trees are preserved. The assigned audit is complete; the parent sweep remains80%. No service/Git/CASE/readiness state, publication, DOI reservation, merge or external contact was changed or initiated.
