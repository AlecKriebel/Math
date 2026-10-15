# Cross primary-source priority audit for PR263

Audit checkpoint: 2026-10-11 21:57 UTC. Completion estimate: 95% of the Cross-specific audit; the dissertation comparison is complete, while the full 2009 talk body remains unrecovered. This is an authored comparison, not a redistribution of source texts. Primary PDFs, extracted text, retrieval records, and rendered pages remain in the ignored `private_reading` directory.

## Disposition

**HOLD on an unqualified novelty or first-solution claim. GO for reporting the accepted scoped theorem with an explicit Cross comparison. No “already known” match was verified in the recovered primary bodies.**

The central dissertation access gap is resolved. Jonathan A. Cross's 2010 University of Washington dissertation was recovered in full from its public open-access ProQuest record. Its complete regularity chapter establishes and discusses materially different claims. The closest negative example concerns the abscissa after a nonlinear, rank-deficient real parameterization of a matrix family. The closest positive calculation concerns individual proximal subgradients for real quadratic coefficients. Neither is the accepted complex coefficient nearest-stability theorem. The dissertation's conjecture uses standard finite-subgradient function prox-regularity and is not settled by the accepted whole-epigraph set conclusion.

The full slides, notes, or recording of Cross's 10 November 2009 talk were not recovered. Its archived abstract is available and has been read completely; it announces a one-real-parameter function result. An abstract cannot prove that the delivered talk contained no additional material. This remaining gap and the bounded search scope preclude an unconditional firstness certificate. The broader priority audit must make the publication decision.

## Exact candidate used for matching

The parent acceptance record, `ROOT_SCOPED_MATH_SOURCE_ACCEPTANCE.json`, accepts the following statement for this audit: for each fixed SPD real inner product on complex quadratic coefficient space, every neighborhood of the coefficient vector of `z²` contains an unstable quadratic with at least two attained global nearest quadratics whose roots lie in the closed left half-plane. Both the monic ambient space and the full exact-degree quadratic ambient space are included. The entire abscissa epigraph fails set prox-regularity near `(z²,0)`.

The comparison excludes a real-only result, an all-degree result, an explicit nearest pair, and a disproof of standard function prox-regularity for a fixed finite subgradient. This audit does not independently reapprove the candidate proof; the parent's accepted mathematical scope controls the target.

The candidate mechanism is an ambient coefficient-space obstruction. On the stable boundary,

`p_t(z) = z² + t²z + t² + i t³ = (z+it)(z+t²-it)`,

the bounded coefficient normal `n_t=(-t,-t²/2,-t/2,1)` has a positive secant pairing of order `t³`, against a squared coefficient displacement of order `t⁴`. Its associated unscaled abscissa gradients diverge. The epigraph normals approach a horizontal imaginary-constant-coefficient direction. These distinctions are essential when matching Cross's statements.

## Dissertation recovery, version, and read extent

Primary record: [Cross dissertation, ProQuest document 288328008](https://www.proquest.com/docview/288328008). The public record labels the graduate work open access. UW's live catalog supplied both the ProQuest record and the local dissertation record `alma99112805780001452`, with the Math Research Library call number `QA3 Th60430`. UMI publication number: `3406832`.

The canonical public record was opened without the UW institutional-account query parameter. Its own embedded PDF was retrieved through an ordinary public read request. No authentication barrier, payment barrier, CAPTCHA, access control, or protected download was bypassed. The initial UW-account link redirected to an identity provider and was abandoned. The transient signed PDF URL is omitted from this authored report and its public provenance manifest.

Recovered PDF: 222 pages, 3,250,316 bytes, SHA-256 `f4d8e02b8393d9497144c32680f4fdc388ad7fb59c47a3d5743dafb74ea195d7`. Retrieval: `2026-10-11T21:50:34.950430+00:00`. PDF creation metadata: 19 March 2010; modification metadata: 18 May 2010. The body title is *Spectral Abscissa Optimization using Polynomial Stability Conditions*. The PDF title metadata contains a spelling error in “Polynomial”; this does not identify a different work. These metadata dates identify this file version, not the date each mathematical claim was first circulated.

Read extent: title, rights page, contents, theorem/example lists; chapter 5 in full, printed pp80–133 (PDF pp101–154); the chapter-1 scope account, printed pp6–8; the stability definition on printed p19; the complete bibliography, printed pp179–185; and the prox-regularity appendix, printed pp190–191 (PDF pp211–212). The full extracted dissertation was searched for prox-regularity, projection, nearest/closest, and the related conjecture/versal-deformation language. Search hits in the algorithm chapter concern search-direction convex cones or projection to a graph, rather than nearest closed-half-plane stable coefficient polynomials. Those checks do not constitute a claim that every unrelated chapter was read line by line.

Visual checks against the original PDF confirmed printed pp103, 105, 122, 123, 124, and 132. In particular, the counterexample's erroneous evaluation on pp122–123 is present in the actual PDF and is not an extraction artifact.

## Claim matching

| Primary body and locator | Exact mathematical content and domain | Match to accepted candidate | Priority consequence |
|---|---|---|---|
| Definition 5.22, printed p103; repeated Appendix A.4, p191 | Local quadratic minorants with subgradients restricted to a neighborhood of a fixed finite `v̄`; function prox-regularity at the point means this for each finite `v̄` separately. | Different quantified condition from set prox-regularity of the whole epigraph, which includes horizontal normal directions. | Cross's use of “prox-regular” must be read through this definition. The accepted candidate cannot be promoted as resolving this function question. |
| Theorem 5.26 and its proof, pp105–117 | Stated positive function result for a monic polynomial with smooth complex coefficient functions of one real parameter. The proof uses Puiseux expansions, root clusters, and finite-subgradient localization. | Does not address full coefficient-space nearest stable points. A one-dimensional parameter result does not establish a multi-dimensional ambient result. | Prior related positive claim. Its proof is not required by the candidate or by this mismatch conclusion. The stated smooth hypothesis and Puiseux use should not silently be reinterpreted as a separately validated analytic theorem. |
| Example 5.37, pp118–120 | General function example intended to separate prox-regularity of every line restriction from the multi-variable function property. | No stable-polynomial nearest-point theorem. | Prior warning against restriction-to-lines arguments. |
| Example 5.38, pp120–123 | Negative standard function result for `A(x₁,x₂)=[[0,x₁+x₂],[x₁−x₂,0]]`, with characteristic polynomial `z²−x₁²+x₂²`, at real parameter origin and finite `v̄=(5/3,−4/3)`. | The coefficient map is `F(x)=(a=0,b=−x₁²+x₂²)`, with `DF(0)=0`. It is not a full complex coefficient parameterization. | The broad claim “an abscissa map need not be function prox-regular” was already known by 2010. This example does not predate the accepted ambient complex nearest-stability theorem as stated. |
| Conjecture and reduction, pp123–131 | Positive function conjecture for sufficiently rich/versal coefficient families; smooth invertible or full-rank composition statements, with function prox-regularity of the target assumed. | The candidate has diverging gradients and horizontal limiting normals, not a finite `v̄` counterexample. | The candidate is compatible with the conjecture's finite-subgradient scope. Neither the candidate nor Cross's reduction settles that conjecture. |
| Real quadratic calculation, pp131–133, equation (5.31) | Explicitly `f:R²→R` for `z²+a₁z+a₀`. Establishes each subgradient `(v₀,−1/2)`, `v₀≤0`, is a proximal subgradient at the origin. | Real coefficients; pointwise proximality, without the neighborhood-uniform subgradient condition or full complex ambient geometry. | Prior related positive calculation, not the accepted negative theorem. |
| First-order formulas, pp81–87, Theorems 5.1–5.6 | Complex polynomial abscissa tangent cones, normals, finite and horizon subgradients, explicitly attributed to earlier Burke/Overton/Lewis work. | Relevant background, but no quadratic-support blowup or all-SPD nearest-stability conclusion in these statements. | These first-order facts must not be claimed novel. They are dependencies to inspect in the broader audit. |

The conjecture's coefficient-field wording requires care. Printed p123 writes smooth `a_j:R^n→C` and independent coefficient gradients, whereas p124's reduced map uses real coefficient coordinates, with an index/dimension inconsistency as printed. This is insufficient to certify a precisely quantified conjecture on all `C^n≅R^(2n)` coefficient directions. It is sufficient to identify its subject as the function condition in Definition 5.22. The explicit quadratic example at p131 unambiguously uses a real two-dimensional domain.

Cross's explanatory prose at p103 broadly associates function prox-regularity with uniqueness of epigraph projections near the graph point. That prose does not supply a theorem replacing Definition 5.22 by whole-epigraph set prox-regularity. Reading it as such would erase the horizontal-normal distinction and make the comparison circular. The definition, the localization theorem on p104, and the fixed-subgradient proofs control the claimed scope.

## Checkable repair and geometry of Cross's negative example

Cross's characteristic polynomial gives

`h(x₁,x₂)=sqrt(max(x₁²−x₂²,0))`.

At `x_k=(5/k,4/k)`, `h(x_k)=3/k` and `∇h(x_k)=(5/3,−4/3)`. Thus the finite limiting subgradient used by Cross is valid. The text then chooses `x'= (c,0)`, `c>0`, but prints `h(x')=0`. The correct value is `c`. The conclusion survives: for `ρ=0`, the support value is `(5/3)c>c`; for `ρ>0` and `0<c≤1/ρ`,

`(5/3)c − (ρ/2)c² ≥ (7/6)c > c = h(c,0)`.

Taking `c≤ε/2` meets the required neighborhood bound. This independently repairs the specific arithmetic in the prior counterexample. It does not extend the example's domain.

There is also a nearest-stability statement immediately derivable in Cross's **parameter** metric, rather than asserted as the candidate coefficient result. The closed stable parameter set is `K={|x₁|≤|x₂|}`. For an input `(c,0)`, the two Euclidean nearest points are `(c/2,c/2)` and `(c/2,−c/2)`, both at squared distance `c²/2`. To check globality, for each fixed `x₁` the best feasible `|x₂|` is `|x₁|`, reducing the minimum to `(c−x₁)²+x₁²`. However, both parameter minimizers map to exactly the same coefficient polynomial `z²`. Consequently even this derived parameter nonuniqueness is not coefficient-polynomial nonuniqueness. It provides no counterexample or priority match to the accepted theorem.

## Other recovered primary evidence

- [UW optimization seminar archive](https://sites.math.washington.edu/~thomas/optsem/archives/2009-2010/optsem2009-2010.html), complete page read: dates the Cross talk to 10 November 2009 and his dissertation defense to 9 March 2010. Both titles link to separate archived abstracts. An early checkpoint had overlooked those relative links; that error is corrected here and in the log.
- [Cross 2009 talk abstract](https://sites.math.washington.edu/~thomas/optsem/archives/2009-2010/cross.html), complete two-paragraph body read: announces Puiseux/Newton-polytope techniques applied to one-real-parameter function prox-regularity. SHA-256 `c8aec166da1831f6c1b4a1232d7c9fded601cc4ca6e4365bdb00ef81ffaa80ff`; retrieved 21:54:10 UTC. It contains no link to full slides, notes, or recording. Its body is an abstract, not the delivered talk.
- [Cross defense abstract](https://sites.math.washington.edu/~thomas/optsem/archives/2009-2010/cross2.html), complete body read: describes parameterized-polynomial abscissa optimization, stability criteria, epigraph geometry, variational properties, and an algorithm. SHA-256 `712fc43cb68248adb3b643d57c90aba2927792606f1a992e9222fb62ddaffb4b`; retrieved 21:54:10 UTC. It is identity/scope evidence, not evidence of the absence of an unstated theorem.
- [UW 2010 mathematics newsletter](https://math.washington.edu/sites/math/files/documents/newsletters/1011nl.pdf), p17 read and visually checked: confirms author, dissertation title, Jim Burke as advisor, and the 2009–2010 doctoral year. Used only for identity and chronology.
- [Heß, Henrion, Lasserre, Pham 2015 author preprint](https://optimization-online.org/wp-content/uploads/2015/07/5040.pdf), July 30 version, 26 pages: full relevant body read, with pages2–3,8–10,24–26 especially checked and pages3,8,26 visually inspected. Cross is cited as a survey and for a damped-oscillator example. The defined parameter family has real polynomial coefficients over real parameters. The main statements concern semidefinite approximations of abscissa, not nearest stable polynomials. SHA-256 `c825c11e41322a8a9f0b5671ce3cc377bfa7e88d660ccc84fac82761b67ee755`.
- [Roxana Heß 2017 dissertation](https://utheme.utoulouse.fr/access/files/original/ecc40897faf3dbbb0583c40ab0438ac6eb534cd4.pdf), *Some approximation schemes in polynomial optimization*, defended28 September 2017: complete Cross-bearing passages on printed pp16 and21 and bibliography entry on p91 read, the first two visually checked; full body searched for Cross/prox/nearest/Puiseux. These passages again use Cross as survey/example evidence. SHA-256 `584d80800d64768e1c6715f069881d685c62a023148ef2ecf9a80616526b7a82`. Unrelated thesis chapters were not read line by line.
- [Lelkes, Bak, Kalmár-Nagy 2024 rod-vibration paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC10838305/), *Scientific Reports*14,2846: the complete Cross-bearing optimal-damping paragraph and reference 56 read from the public article body. This is an applications citation for spectral-abscissa minimization; it does not attribute a projection/prox-regularity theorem to Cross. Article body privately preserved, SHA-256 `03693f5ba791f1c34d3664bdf68a2e4d2f5f141ee7b7724ebf78be3e634cac57`. Other mathematical claims in that article are outside this audit.

Searches for additional Cross papers or a separate full talk body found the dissertation, these citations, and identity records, rather than an additional primary Cross theorem. Burke's complete public by-year bibliography was searched without finding Cross as an author. That bounded negative search is not a complete Cross publication bibliography and does not prove no such work exists.

## Dependency and remaining-gap ledger

The primary dissertation attributes its relevant background to Burke–Overton 1993 (proximal spectral subgradients), Burke–Overton 2001 and Burke–Lewis–Overton 2004 (polynomial first-order variational geometry), Daniilidis–Lewis–Malick–Sendov 2008 (symmetric-matrix spectral function/set prox-regularity), Arnold 1971 (versal deformation), Hare–Lewis 2004 (partial smoothness/identification), and Rockafellar–Wets 1998 (function prox-regularity and its localization). This Cross audit documents those attributions; it does not claim an independent full-body priority review of each dependency. They belong to the broader priority audit and must not be treated as new candidate contributions.

Resolved gap: the dissertation's relevant primary body is now accessible, read, and checkably distinguished from the candidate.

Unresolved exact body: the delivered 10 November 2009 talk's full slides, written notes, audio, or video. No full body was located through the UW archive, its Cross abstract, the linked defense abstract, catalog/ResearchWorks searches, or exact-title/author searches. No individual was contacted. If later legally available materials are found, compare their theorem quantifiers and coefficient domain directly; do not infer a match or nonmatch from the title.

Strongest verified conclusion: the recovered Cross dissertation chapter contains a prior restricted-parameter function counterexample and positive real-quadratic proximal-subgradient evidence, but no verified instance of the accepted full complex coefficient, all-fixed-SPD attained-nearest-stability theorem or its whole-epigraph set conclusion. It does not support calling the accepted result a solution of Cross's fixed-finite-subgradient function conjecture. A broader absence-of-prior-work conclusion remains unsupported.

No external communications, provider changes, Git reference changes, commit/push, release, DOI, or publication operation was performed by this audit agent. The source files remain ignored and the authored report is available for the parent's independent adversarial checkpoint.
