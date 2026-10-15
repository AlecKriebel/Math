# Independent derivation: PR 630 prior-example implication

Recorded UTC: 2026-10-15T03:58:47.628610+00:00
Pinned original PR head: `810cd5c148bbae7c7c5a47423c375ada98e903b6`
Independence: This derivation was saved before reading any other new priority review. Inputs read were the pinned scope and proof, the root candidate, primary source text and page images, and the primary retrieval receipts. No other agent was contacted; no Git or remote mutation occurred.
Checkpoint completion estimate: 70% of this assigned falsification review. The mathematical implication is complete; repair analysis and final source bindings remain.

## Exact proposition and falsification criterion

For fixed k>=2 and a,b in C with b!=0, let H(f,k,a,b) mean that f is nonconstant entire, the sets f^(-1)(a) and (f')^(-1)(a) agree, and every point of (f')^(-1)(b) satisfies f^(k)=b. Let E(f,k,a) mean that f(z)=d exp(cz)+((c-1)/c)a for nonzero c,d satisfying c^(k-1)=1.

The literal universal assertion is U: for every allowed (f,k,a,b), H implies E. The printed 2007 source explicitly supplies b!=0 and k>=2, with no restriction a!=0. The preceding Theorem G and later Theorem 3 have separate a!=0 hypotheses; those do not grammatically bind the independently stated Theorem H. A counterexample with a=0 and k=2 therefore disproves U. It does not disprove a strengthened assertion restricted to a!=0.

The priority candidate would fail if the 2009 example were not a parameterized nonzero quadratic, if the substitution required B=0, if the target b-condition failed, if IM really meant CM here, or if k=2 or a=0 were forbidden. Direct page-image checks and the calculation below rule out each of those possibilities.

## Source predicate and target predicate remain distinct

Printed 2009 p.68 Example 1 uses g_B(z)=B z^2/4 as an IM zero-sharing obstruction in a neighboring theorem. Its extra condition is S_B: g_B'=B implies g_B=B. This is verified because g_B'=B forces z=2 and g_B(2)=B. It is NOT the target condition T_b: g_B'=b implies g_B''=b. In particular, naively setting B=b makes g_B''=b/2, so T_b fails at the nonempty b-fiber. The parameter adjustment is mathematically necessary.

## Direct proof after parameter selection

Fix arbitrary b!=0 and select the source parameter B=2b. The source then literally supplies

    g(z)=b z^2/2, g'(z)=b z, g''(z)=b.

Take k=2 and a=0. The function g is entire and nonconstant. Both g and g' vanish precisely at 0, with respective multiplicities 2 and 1. Hence they share 0 IM and do not share it CM. The required target implication holds at every point because g'' is the constant b. Its antecedent is attained at z=1; thus it is nonvacuous. Also b!=a.

At k=2, the equation c^(k-1)=1 forces c=1; at a=0, E reduces to g=d exp(z). The right-hand side is zero-free, whereas g(0)=0. Therefore E fails. This is an exact counterexample to U, and for b=1 it is exactly the PR's smallest exhibited function.

The source's S_B is neither equated to T_b nor used to infer T_b. The inference uses its explicit formula, an admissible choice of its parameter, and direct differentiation. This is stronger evidence than formula resemblance: a dated explicit IM-sharing counterexample in the same uniqueness-of-an-entire-function-and-its-derivative setting instantiates to the identical target witness, and every target predicate is independently checked. It remains weaker than a source explicitly naming and answering the identical 2007 question.

## Quantifier attack

Disproving U requires only one admissible tuple. The 2009 formula after B=2b already does so for every b!=0 at k=2. The PR additionally proves the stronger assertion that for every fixed k>=2 and every b!=0 there is a polynomial target counterexample. The latter is not supplied verbatim by 2009 Example 1 and must not be attributed to it. Its new strength does not restore novelty to the already implied Boolean assertion not-U.

For fixed k>2 the selected quadratic does not satisfy the target hypothesis: its k-th derivative is 0, while its b-fiber is nonempty. Thus a claim that Example 1 alone refutes the target at every derivative order would be false. The candidate correctly limits its direct implication to k=2 and the universal assertion.

## Independent check of the PR's supporting polynomial claim

Let f be a nonconstant polynomial with H. If a!=0, every root of f-a is simple because at that root f'=a!=0. For degree n>=2, its n distinct roots cannot all be roots of the degree n-1 polynomial f'-a. A linear polynomial has a one-point a-fiber, while the derivative's a-fiber is either empty or all C; it also fails. Hence a=0 and n>=2.

If f and f' have the same zero set, every root of f has multiplicity at least 2. If r is the number of distinct roots, the derivative's roots contributed by those roots have total multiplicity n-r. Since all derivative roots are among them, n-1=n-r, so r=1. Thus f=A(z-z0)^n, A!=0. The b-fiber of f' consists of n-1 distinct nonzero x=z-z0 satisfying x^(n-1)=b/(An).

If k>n, f^(k)=0 fails the condition. If 2<=k<=n, comparing the (n-k)-th powers over that entire root-of-unity fiber requires n-1 to divide n-k. But 0<=n-k<n-1, so n=k. The value condition gives A k!=b. Conversely f=b(z-z0)^k/k! plainly works. This proves the claimed classification independently.

Consequently the all-order polynomial family and its complete polynomial classification are mathematically real additional statements, not false padding. Their historical priority is a separate question; this derivation does not assume a result is old because elementary.

## Later primary-source supplement: known polynomial structure

Recorded UTC: 2026-10-15T04:01:59.933996+00:00. This supplement follows the saved independent checkpoint. The root supplied only a new primary-source lead; I independently retrieved the author manuscript and visually inspected its p.27. No other new priority review has been read.

Novikov and Yakovenko's author manuscript, dated January 19, 2000, contains Proposition 7, attributed there to Chademan [5]. Its relevant univariate statement is: a complex polynomial with sole critical value 0 has the form A(z-z0)^n. The statement and proof impose no monic restriction on the conclusion, no reality assumption, and no distinct-critical-point assumption; monicity is introduced only without loss of generality in the proof. The proof counts derivative-root multiplicities and forces one distinct critical point.

For a polynomial satisfying IM zero sharing, every critical point is a zero of the polynomial, so all critical values are 0. Degree >=2 ensures that a critical point exists. Hence this published structural theorem applies directly. The nonzero-a exclusion is a separate degree argument, and the target derivative-value condition is then a root-of-unity/degree count selecting n=k and A=b/k!. Consequently the target classification is a direct application of a specifically matching earlier structural theorem plus the target-condition computation. This does not show that the exact target classification or all-k counterexample was stated verbatim earlier.

## Later independent check of the known transcendental template

The 2009 paper's printed pp.68-69 exhibit, within different hypotheses, the form B((A/2)exp(z/4)+1)^2. With B=1, A=-2 and coordinate replacement z -> 4 lambda z, this gives the PR's shape (exp(lambda z)-1)^2. Such coordinate replacement is not assumed to preserve the source's pointwise derivative-value predicate. It does preserve the explicit shape and lets its zero-sharing property be checked directly.

Writing t=exp(lambda z), differentiation gives f^(k)=lambda^k(2^k t^2-2t). Taking the target b=-lambda/2 gives f'-b=2lambda(t-1/2)^2. At the target b-fiber, the value equation becomes lambda^(k-1)(2^(k-2)-1)=-1/2. For k>=3 this is exactly lambda^(k-1)=-1/(2^(k-1)-2), an equation with nonzero complex solutions. For k=2 it has no solution. The PR's calibration is correct. This is an exact adaptation of a documented shape, while priority of the particular derivative-order calibration remains undetermined.

Final review checkpoint: assigned falsification review 100% complete. No new evidence of a mathematical error in the central implication was found. Exact originality of all target refinements remains outside the proved priority conclusion.

## Final supplement: 2004 exact all-order formula lead, limited provenance

Recorded UTC: 2026-10-15T04:03:19.355514+00:00. Following completion of the central review, the root supplied another primary-source lead. I independently opened the author-uploaded 2004 article through the web PDF reader and inspected its extracted Lemma 5 on printed pp.323-324 (the browser reported a 19-page article, Spring 2004, volume 48, pp.319-337). The article is Chang-Fang-Zalcman, Normal families of holomorphic functions. Its Lemma 5 assumes an entire function of order at most 1, zeros of multiplicity at least k, a nonzero parameter B, and implications g=0 => g^(k)=B and g^(k)=B => g^(k+1)=0. It prints g=B(z-z0)^k/k! for k!=2 and the quadratic B(z-z0)^2/2 among the alternatives for k=2.

These lemma hypotheses differ from the target's hypotheses and the lemma is not invoked as a target necessity theorem. The displayed formula itself, with B=b, gives the same all-order polynomial family. For every k>=2 its zero set and its derivative's zero set are {z0}, its kth derivative is identically b, and its derivative's b-fiber has k-1 distinct points. Thus the same direct checks already given above make each displayed prior formula a target counterexample. This is an additional prior-explicit-formula implication for the all-order construction, beyond the independently byte-bound 2009 quadratic implication. It does not establish that the exact target theorem/classification or target application was published verbatim.

Provenance limitation: direct downloading through the local HTTP client returned403; no complete 2004 PDF bytes or SHA256 were obtained. Web PDF text was independently accessible; screenshot requests returned references without usable image pixels in this tool bridge, so this review does not claim an independent visual or byte-level check of the 2004 source. URL: https://www.researchgate.net/profile/Lawrence-Zalcman/publication/258233263_Normal_families_of_holomorphic_functions/links/555b0fb008ae6fd2d828632a/Normal-families-of-holomorphic-functions.pdf . The central disposition and final comment do not rely on this supplementary lead. I made one bounded source check and stopped.
