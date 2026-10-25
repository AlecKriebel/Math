# Complete bounded adversarial review — Quadratic convergence of SOS-density bounds on convex bodies

The complete actual manuscript survives this independent adversarial review. I found no counterexample or indispensable unsupported step in its whole quantitative upper theorem, all-integer explicit constant, single-global-square construction, C2 extension, or worst-case lower proposition. Historical first priority and current worldwide openness remain unknown. That is a distinct limitation, and the manuscript explicitly avoids firstness or new-method claims.

## Target, edition and independence

The target is row95, [Zenodo23442760](https://doi.org/10.5281/zenodo.23442760), version1.0: actual five-page PDF, 77,950 bytes, SHA256 `f8cbd7733bc63f4918df3b18007d3087ae5cd862a4318c6bddd6f75d58385240`. Controlling TeX is the complete 15,887-byte `published-source/manuscript/main.tex`, SHA256 `5508a2a2bf9079573b29b4be8b5cdf638b2c2003e4536e5c0e1518c591db7c59`. Complete original ZIP is 413,706 bytes, SHA256 `52d8ba4dd670ab77184ea6706aacaac0233997c44ad16b041c357f6b5070d38a`.

I read all five actual PDF pages by complete layout-preserving extraction and the full controlling TeX before consulting external mathematical bodies or earlier reviewing opinions. The parent supplied only identity/custody data. `EARLY_LEDGER.md` fixed eight materially distinct attack families; its SHA256 is `e936bf7594d517948f2be5e6c417f8a5a3df484a82804fce9c2872e24d4b5d5b`, and the read-only `EARLY_SEAL.json` SHA256 is `3689eca607c5eb8a172f49526ad8b75fccf5cc7cef7e83ab590e91c6771ea0aa`.

No historical package, sibling, analytic, scope or root scientific opinions were read. After the seal, the source worker supplied raw cited-primary paths/hashes only. I independently inspected their pertinent interfaces. Both previously completed discotope/CFH packets were rehashed against their own seals without consuming their substantive opinions and remain unchanged.

The manuscript declares17October2026, while actual record creation is17October2026 at22:06:29.417068UTC. The reviewed current edition is1.0, with a single version in source-ready metadata. Custody and declared dates do not independently certify historical priority.

## Literal verified theorem and mechanism

For every n>=1, every compact convex K in R^n with nonempty interior, every polynomial f and any chosen minimizer a, define H, gamma, g and G exactly as in the manuscript. Then 0<G<infinity and the normalized *Lebesgue* hierarchy of *global sums of squares* of degree<=2r obeys

`0<=H_r(f,K)-min_K f <= [4(n+2)^2(pi/2)^(2n+4)(1+2^(n+2))]G/r^2`

for every integer r>=1. One global square supplies the upper bound. The hierarchy does not require f convex or a semialgebraic/smooth boundary. The conclusion is existential and does not give an efficient procedure to locate a.

The independently reconstructed proof is complete in DERIVATIONS.md. Its critical steps survive the following attacks. Convexity at the actual minimizer gives the nonnegative constrained linear gradient term even at the boundary, and the Hessian bound on each actual segment gives a quadratic upper proxy. Homothety then bounds every sublevel-shell volume by a power of the *same* local mass F(h). A normalized odd-length Dirichlet polynomial has both a positive endpoint core of width h=(2m+1)^-2 and a controlled absolute tail. Raising it to an even power2L, L=n+2, supplies a global square. The dyadic shell majorant has exact ratio1/2 and cancels F(h) against the denominator. No boundary cone/curvature constant, derivative of F, sign cancellation, complex branch, or unproved approximation theorem is inserted.

Composition costs total degree2mL in the square root and4mL in the density. Taking m=floor(r/(2L)) covers r>=2L with exactly the advertised4L^2 constant loss; the normalized constant square handles every smaller positive integer. C2 extension remains valid because only bounded Hessian/Taylor constants are used and the density is polynomial in the quadratic proxy.

The lower proposition also survives independently: shifted Legendre orthogonality and its uniform bound give q(t)<=(r+1)^2 for every normalized interval SOS density. At least half its mass is above1/[2(r+1)^2], yielding mean>=1/[4(r+1)^2]. Applying the polynomial inequality with the other variables fixed and then integrating gives the product-body statement without an extra volume factor. This proves worst-case sharpness through one fixed instance in each dimension, not a positive lower rate for every objective.

## Exact diagnostics and falsifiable controls

I inspected `checks.py` before execution and used only the existing Python3.12.14/SymPy1.14.0 runtime. No original supplied program was run. All exact assertions passed. The retained checks include six finite kernel identities, exact shell-series constants, 297 degree/floor cases, interval and square-pyramid global-square densities with exact normalizers and total degrees, a nonconvex interior-minimum proxy identity, five exact Legendre Gram checks, and the degree-one interval generalized-eigenvalue polynomial. These corroborate formulas, not the universal quantifiers.

On [0,1] with f=t, m=1,L=3,r=6, the actual quadratic-proxy construction has normalizer52981/312741 and objective98459/741734, with root degree6 and density degree12. On the nonsimple square-pyramid apex `0<=z<=1, |x|,|y|<=z`, f=z gives g=z+x^2+y^2+z^2 and G=4. With m=1,L=5,r=10 the normalizer is5158228776049/198460298701665 and the objective is6547688036885/20632915104196, with root degree10 and density degree20. Both normalize exactly to unit mass on the whole body.

Controls reject specific tempting errors: the core bound one is false since A_1(1/9)=23/27; an odd density power is negative at t=1; choosing L=n+1 makes the shell majorant diverge. Without mass normalization, q=0 for f=1+t violates even the claimed lower bound by f_*=1. With arbitrary reference measure delta_1, f=t on [0,1] has error one forever. Constant objectives have zero error. These are controls outside the stated theorem, not defects or narrower replacements.

## Primary interfaces and novelty limits

The actual [2018 OWR report](https://ems.press/content/serial-article-files/46772?nt=1), Laurent's complete contribution printed2991–2993, asks about the convex-body regime. I visually confirmed that displayed density constraints(3)–(4) omit the integral's value. Their probability context supports the normalized interpretation, independently explicit in [Slot–Laurent arXiv v2 Eq.(3)](https://arxiv.org/abs/1905.08142v2). That exact edition's Theorem11 and concluding question match the logarithm-removal target; Lemmas1/4 credit the gradient and quadratic proxy.

The specified [annealing v1](https://arxiv.org/abs/1703.00744v1), Corollary4.3, already uses a quadratic upper estimator. The specified [worst-case v1](https://arxiv.org/abs/1804.05524v1), Theorem3.1 and Corollaries3.2/3.3, support the credited interval/product quadratic lower exponent. These inspected preprint editions are distinguished from their later publisher editions; no byte-equivalence assertion is made.

The actual published-layout [Totik–Varga body](https://www.math.u-szeged.hu/pot/5fdp.pdf), Theorem2.1, admits endpoint parameter0 and psi(v)=sqrt(v). Its integrability and doubling hypotheses are satisfied, and its exponent becomes exactly(m^2t)^(1/4). Its later Christoffel-function argument explicitly compares shell mass with core mass. DERIVATIONS.md independently verifies the manuscript's acknowledged alternative deduction using those polynomials, Markov's inequality and the relative-mass argument. The main finite-trigonometric proof does not need that external theorem.

The actual [final2026 overview](https://ir.cwi.nl/pub/36052/36052.pdf), Table1 and surrounding discussion, records the weaker log-squared rate for arbitrary convex bodies; Section2.4 also distinguishes densities polynomial in f. Its contents support that limited source claim, not worldwide openness. No specific source mismatch or bibliographic omission was discovered. Our six-interface review does not independently audit every historical search claim in the deposited package and does not establish absence of an earlier printed equivalent theorem or later resolution. The proxy, endpoint localization, broad relative-mass mechanism and lower exponent all have credited antecedents; a new-method or historical firstness claim is not warranted by this review.

## Custody, disposition and exact remaining gap

`ORIGINAL_BINDING_RECEIPT.json` rehashes all161 original objects against the authenticated readiness manifest and CRC-reads all152 original ZIP members, checking equality to their frozen extracted counterparts. The original readiness manifest and seal remain SHA256 `445d0532cc31dfca48ade7cf207d5439d83a0da13dc66f4c0451a12db3912c79` and `002b8324c97eb11428fa6b747f7b749ea4a1301c953acdb425f19dc168b87da5`. `PRIMARY_INTERFACES.json` binds raw primary editions, exact passages, extractions, visual inspections and access limits. Complete foreign texts are confined to preignored caches.

Strongest surviving original result: the complete quantitative main theorem, all positive integer orders, single global square, C2 extension and full worst-case lower proposition. Exact mathematical gap found: none in this bounded review. Historical firstness/current openness remain unknown, distinct from a proof defect. No substantive-defect deferral trigger arose; no source repair, theorem repair, extended replacement search or narrowed public result was attempted. Root retains disposition authority.

The bounded audit is complete; the203-paper goal remains ongoing. No external contact or outreach draft, new environment, source/config/shared-core/site/native-sheet/UI/Git/deploy/redirect/release change occurred. All authored work is in this new adversarial namespace. Final receipts and immutable manifest/seal bind the packet and a final unchanged-original recheck.
