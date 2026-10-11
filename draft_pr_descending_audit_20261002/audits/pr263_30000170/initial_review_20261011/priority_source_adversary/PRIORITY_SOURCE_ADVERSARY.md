# PR263 independent priority and source adversary

## Verdict and exact boundary

**BOUNDED GO for a direct, carefully credited proof note about nonunique nearest stable complex quadratics. No unconditional novelty clearance.** No essential source or attribution hold was found for that narrow framing. This is not permission to claim a first result, a newly solved presently open problem, a novel Whitney-umbrella geometry, or a disproof of standard function prox-regularity at a fixed finite subgradient.

The comparison target is exactly the accepted claim in `ROOT_SCOPED_MATH_SOURCE_ACCEPTANCE.json`, tied to original PR263 head `c4eff3253932a504f8e558c8b5f5b1b5e155de0f`: for **every fixed positive-definite real coefficient inner product**, arbitrarily near `z^2` in monic or full exact-degree **complex quadratic** coefficient space there is an unstable polynomial with at least two attained global nearest closed-left-half-plane stable quadratics; the abscissa epigraph fails **set** prox-regularity. No explicit unstable input or nearest pair is asserted. Root mathematical acceptance is an input to this source gate, not independently replaced by this report.

The earlier Cross and broad priority reports were treated as hypotheses. I first read actual Cross chapter 5 completely and actual Kirillov–Overton pp1–3 before consulting those reports, then extended the primary reading and recovered the original Bottema paper. The parent’s separate tentative positive finite-subgradient function lemma was neither assumed nor used.

For the historical framing, Lewis 2003 §8 is stronger than the short OWR question: it explicitly discusses a complex Euclidean monic coefficient space, the stable polynomial set, and whether that set is prox-regular. The accepted theorem gives a negative answer in complex degree two to that historical set question. OWR’s omitted field/metric/monicity still must be disclosed when OWR is named. A historical question does not establish that it remained open in 2026.

## Cross 2010: actual chapter, not an abstract substitute

Primary: Jonathan A. Cross, *Spectral Abscissa Optimization using Polynomial Stability Conditions*, University of Washington PhD dissertation, 2010, UMI 3406832; [ProQuest record](https://www.proquest.com/docview/288328008). The recovered 222-page PDF SHA-256 is `f4d8e02b8393d9497144c32680f4fdc388ad7fb59c47a3d5743dafb74ea195d7`. I read chapter 5 in full, printed pp80–133, PDF pp101–154, including definitions, examples, the one-variable result, conjecture and reductions, and real-quadratic conclusion. Printed pp103,122–123 were additionally checked as rendered pages. The PDF page offset is 21, not 23. A mistakenly named preliminary private image actually shows printed p125 and is not used as p123 evidence. I searched the full extracted body for projection/closest/nearest and regularity terms; this does not claim a complete reading of unrelated chapters.

Definition 5.22 on printed p103 is standard **function** prox-regularity relative to a fixed finite limiting subgradient `vbar`, with nearby finite subgradients and function-attentive localization. “For every vbar” permits the constants to depend on vbar. It is not uniform control over the entire unit-normal bundle of the epigraph. The adjacent prose identifies it with single-valued epigraph projection near the graph point too broadly. The formal definition, not that prose, fixes the claim’s scope. The accepted theorem’s limiting horizontal normals can escape every fixed finite `(v,-1)` slice because the unscaled abscissa gradients diverge.

Theorem 5.26, printed pp105–117, concerns one real parameter with smooth complex coefficients and concludes function prox-regularity. Its argument uses Puiseux/Taylor structure; I do not independently certify that proof for all smooth families. Either way, its parameter dimension and finite-subgradient conclusion do not state the accepted full complex coefficient projection theorem. Example 5.37, pp118–120, warns that good restrictions to all lines are insufficient; it supplies no nearest-coefficient theorem.

### The actual counterexample and its printed arithmetic error

Example 5.38, printed pp120–123, uses the real two-parameter family

`A(x1,x2) = [[0,x1+x2],[x1-x2,0]]`, with characteristic polynomial `z^2-x1^2+x2^2` and abscissa

`h(x1,x2)=sqrt(max(x1^2-x2^2,0))`.

At `(5/k,4/k)`, `h=3/k` and `grad h=(5/3,-4/3)`. The finite vector is consequently a limiting subgradient at the origin. The printed comparison at `x'=(c,0)`, `c>0`, uses `h(x')=0`; the correct value is **c**. The conclusion nevertheless survives:

- For `rho=0`, the proposed lower support is `5c/3 > c`.
- For `rho>0`, choose `c=min(epsilon/2,1/rho)`. Then `5c/3-rho*c^2/2 >= 7c/6 > c`.

Thus the corrected computation still proves non-proximality of that finite subgradient and the failure of function prox-regularity for this restricted family. The error is real, visually present in the primary PDF, and does not invalidate its conclusion.

The coefficient map is `F(x)=(a=0,b=-x1^2+x2^2)`. It is nonlinear, has `DF(0)=0`, and only reaches a real constant-coefficient slice of the full complex quadratic space. Euclidean parameter projection through it does not become coefficient projection.

In particular, the parameter stable set is `K={|x1|<=|x2|}`. For the unstable parameter `(c,0)`, minimization first gives `x2=+/-|x1|`, and then

`(c-x1)^2+x1^2 = c^2/2 + 2*(x1-c/2)^2`.

The two global nearest parameters are `(c/2,c/2)` and `(c/2,-c/2)`, both with squared distance `c^2/2`. **Both give the same characteristic polynomial `z^2`.** They are not two distinct nearest coefficient polynomials. This exact check defeats an apparent priority match based on parameter nonuniqueness alone.

### Richness and the real/complex boundary

Printed pp123–131 conjecture function prox-regularity for a versal/rich parameterization and give smooth-coordinate/projection reductions. The displayed coefficient family has `aj:R^n->C` and an independence condition on gradients; the next reduction uses real coordinates with an index/dimension inconsistency. Those displays do not certify full `C^n ~= R^(2n)` quantifiers, and their finite-subgradient function notion is still the decisive distinction. The accepted whole-epigraph result should not be described as refuting this conjecture.

Printed pp131–133 explicitly restrict to the real quadratic coefficient map `f:R^2->R` for `z^2+a1*z+a0`. They show that each limiting subgradient `(v0,-1/2)`, `v0<=0`, at the origin is proximal. This is neither uniform function prox-regularity nor the complex whole-epigraph or nearest-coefficient theorem.

The complete archived primary abstracts of Cross’s 10 November 2009 talk and 9 March 2010 defense were also read. The 2009 talk describes Puiseux/Newton techniques and a one-real-variable function result; the defense describes polynomial stability criteria, epigraphic variational analysis, and an algorithm. Slides, a recording, or a full 2009 talk body remain unavailable and **unread**. Neither abstract supplies the exact accepted theorem, but neither is an absence certificate for a missing talk body. No contact or request for a copy was made.

## The geometry is classical: Kirillov–Overton and original Bottema

Primary: O. N. Kirillov and M. L. Overton, *Robust stability at the Swallowtail singularity*, Frontiers in Physics 1:24, published 3 December 2013, [actual author PDF](https://cs.nyu.edu/~overton/papers/pdffiles/swallowtail.pdf), DOI `10.3389/fphy.2013.00024`. I read actual text pp1–8 and the relevant p9 bibliography; I did not audit every decorative/footer item. The nine-page PDF SHA-256 is `cf380dbf397c8d3474f61daf5dd42dcbcdefd32db540d4453883eb92a88e95a9`.

Actual pp1–2, equations (4)/(6), give the real quartic family `lambda^4+a1*lambda^3+a2*lambda^2+a3*lambda+1` and its strict stable region

`a1,a3>0`, `a2>2+(a1-a3)^2/(a1*a3)`.

They describe the Whitney umbrella at `(a1,a3,a2)=(0,0,2)`, corresponding to double imaginary roots, the tangent cone, and the general-matrix/versal context. Later sections discuss constrained abscissa minimization and the swallowtail; an explicitly complex affine abscissa-minimization result is not nearest-stable coefficient projection. I found no accepted A–C theorem in the body read or focused term search.

I independently recovered the original O. Bottema, *The Routh-Hurwitz condition for the biquadratic equation*, Indagationes Mathematicae 18 (1956), pp403–406, DOI `10.1016/S1385-7258(56)50054-6`, through Kirillov’s primary publication bibliography. The [original PDF](https://onkirillov.narod.ru/1956-IM-Bottema-WhitneyUmbrella-ZieglerParadox.pdf) SHA-256 is `9b0a56120c48f6dd6899c1105dc84e33b9eaf5d6a35806e7478435746197bc55`. I read and visually checked all four actual printed body pages; the fifth PDF page is a journal cover. Bottema derives the real quartic stability conditions and studies the normalized boundary `a1*a2*a3=a1^2+a3^2`, including the ruled surface, double line and collapsing generators at `(0,2,0)`. Its mechanical-stability summary excludes repeated roots; do not repurpose it as a complete closed-set theorem including all repeated roots. It contains no complex-quadratic nearest-projection or prox-regularity result. Recovery resolves this particular original-body gap, not all original geometry sources.

The overlap is exact at the shape level. With `a1=x+v`, `a3=x-v`, `a2=u+2`,

`a1*a2*a3-a1^2-a3^2 = u*x^2-(u+4)*v^2`.

The smooth substitution `V=v*sqrt(u+4)` near `u=0` produces the positive Whitney-umbrella solid. Independently, for a complex quadratic `z^2+a*z+b`, write `a=x+iy`, `b=r+iv`; the imaginary root shift gives `U=r+y^2/4`, `V=v-xy/2`. The closed-half-plane stable set is exactly

`x>=0`, `U>=0`, `V^2<=x^2*U`, with `y` free.

To check the last equivalence, shift `z=w-iy/2`, so the roots are `-x/2 +/- sqrt(x^2/4-U-iV)`. Their real parts are nonpositive exactly when `x>=0` and the square-root real part has magnitude at most `x/2`. Squaring gives the displayed solid, including `x=0 => V=0,U>=0`. Therefore the cusp mechanism must be credited as classical. A nonlinear coordinate equivalence alone does not transfer exact projection in a fixed coefficient metric; the accepted normal/support and projection argument supplies that additional step. Its application priority is **not** established merely by exhibiting the chart.

## Remaining bodies: actual metadata and exact relevance

No row labelled unknown is cleared. “Not essential” below means that a fully proved, carefully credited note without firstness/current-openness claims does not logically depend on resolving that body; it does not mean the body cannot contain the theorem.

| Source | Primary evidence actually inspected | Exact relevance and remaining gap |
|---|---|---|
| Orban de Xivry–Nesterov–Van Dooren, *Nearest stable system using successive convex approximations*, Automatica 49(5) (2013),1195–1203, DOI `10.1016/j.automatica.2013.01.053` | Primary UCLouvain DIAL record and publisher preview/abstract | The abstract explicitly includes **matrices and polynomials**, in continuous and discrete time, stable iterates via inner convex approximations, and companion-matrix first-order conditions. Matrix-only dismissal is incorrect. Full body is restricted/unrecovered; no request-copy action. Unknown exact field, metric and possible uniqueness/counterexample remarks. Strong application-priority gap; not essential under bounded framing. |
| Orban de Xivry, *Nearest stable system*, UCLouvain thesis, July 2013 | Primary supervisor’s thesis list identifies title, date and supervisors; no thesis PDF link | Broad nearest-stability title is directly relevant. Full body unknown. Cannot infer its contents from the article. Strong application-priority gap; not essential under bounded framing. |
| Moses–Liu, *Determining the closest stable polynomial to an unstable one*, IEEE TSP 39(4) (1991),901–906, DOI `10.1109/78.80912` | IEEE landing page attempted; robot challenge. Primary Crossref registration supplies title/authors/date/pages, **no abstract** | Exact nearest-polynomial title makes this a high-priority unresolved body. Field, metric, unit-circle/half-plane, repeated-root behavior and nonuniqueness remain unknown. Later summaries cannot settle these. Not essential only if no novelty guarantee. |
| Combettes–Trussell, *Best stable and invertible approximations for ARMA systems*, IEEE TSP 40(12) (1992),3066–3069, DOI `10.1109/78.175751` | Primary author publication list and Crossref registration; IEEE robot challenge; no primary abstract | Stable/invertible approximation is directly relevant; original body unknown. Secondary abstract descriptions are not treated as primary proof of field or metric. No real-only or matrix-only dismissal. Not essential only under bounded framing. |
| Fam, *On the geometry of stable polynomials of one and two variables*, in *Information Linkage Between Applied Mathematics and Industry* (1979),397–407 | Primary publisher book/title/author metadata; body access failed | Broad geometry title is relevant to classical shape priority; no primary abstract/body recovered. Unknown field/geometry extent. Credit known classical shape without claiming its first characterization here. |
| Levantovskii, *On singularities of the boundary of a stability region*, Moscow University Mathematics Bulletin 35(6) (1980),19–22 | Actual Burke–Lewis–Overton 2004 pp267–268 attribution and cited metadata | The cited mechanism is stable-polynomial tangent-cone calculus. Original body unknown, so possible stronger statements are unknown. Not an independently cleared body. |
| Levantovskii, *The boundary of a set of stable matrices*, Russian Mathematical Surveys 35(2) (1980),249–250, DOI `10.1070/RM1980v035n02ABEH001651` | Actual primary Math-Net metadata and primary indexed beginning (real matrices/tangent cones); PDF retrieval failed | Distinct item from the 19–22 polynomial paper. No actual complete body read. Do not collapse them into one cleared source. |
| Arnold, *On matrices depending on parameters*, Russian Mathematical Surveys 26(2) (1971),29–43, DOI `10.1070/RM1971v026n02ABEH003827` | Primary Math-Net metadata and Cambridge reprint chapter record; summary unavailable | Versal-deformation mechanism is attributed by actual Cross/Kirillov–Overton, but the original Arnold body remains unread. Directly credit only the source actually used, or verify any newly imported theorem. Not essential for the direct coefficient proof. |
| Colombo–Marigonda–Wolenski, *The Clarke Generalized Gradient for Functions Whose Epigraph Has Positive Reach*, MOR 38(3) (2013),451–468, DOI `10.1287/moor.1120.0580` | Primary publisher abstract | It **assumes** positive epigraph reach plus an additional property to derive gradient representations and Hamilton–Jacobi applications. It does not state in its abstract that polynomial abscissa has positive reach. Original body/examples unknown. Not used as a premise of this note. |
| Cross 2009 full talk body | Complete primary archived talk abstract | One-real-variable function result in abstract; missing slides/recording/notes remain unknown. No absence certificate for the delivered talk. |

A unit-circle result cannot be dismissed solely because the accepted theorem concerns a half-plane: Cayley/root transformations can connect the stable regions, but field, finite-degree charts, and coefficient metrics require an explicit transfer argument. The unread 1991/1992 papers thus remain material to any firstness or new-application claim.

## Credits, reproducibility and gate use

The note should plainly credit Bottema’s original real quartic boundary and Kirillov–Overton’s stability-region presentation of the Whitney umbrella, Lewis’s historical complex monic stable-set question, prior Burke–Overton/Lewis first-order root/abscissa analysis as actually used, and Poliquin–Rockafellar–Thibault’s local projection/prox-regular-set equivalence. Ordinary root differentiation and fixed-inner-product norm equivalence are not novel mechanisms here. If the final proof introduces an additional theorem from an unread source, that source becomes a new verification prerequisite.

I independently read Lewis 2003 §8, printed pp166–168, PRT 2000 Definition 1.1/Proposition 1.2/Theorem 1.3, printed pp5233–5235 with the preceding introduction, and Burke–Lewis–Overton 2004 pp267–268 on tangent cones. The real/unit-disc AR setup and relevant references of Cruces–Pérez-González–Docampo, *Determination of the Optimal Stable Projection for AR Systems*, author-hosted COST94 copy, were also inspected; full proceedings metadata was not checked. These are bounded read extents, not whole-paper certifications.

`exact_source_checks.py` and `EXACT_SOURCE_CHECKS.json` reproduce exact rational/polynomial checks of the corrected Cross support, its parameter projection collapse, and the quartic chart identity. The displayed complex quadratic chart is proved above; it is not represented as a numerical test. Passing these checks establishes no literature absence. `SOURCE_PROVENANCE.json` binds the actual source versions, read extents, public metadata receipts and input reports. Reading PDFs/HTML remain ignored private files; no copyrighted full-body material is promoted into authored public artifacts.

**The essential decision is separate from novelty:** the scope and attribution permit the parent to continue to a direct proof-note stage. Claims that this is a novel contribution or that the projection application is first require a priority hold, with the Moses–Liu and Combettes–Trussell originals plus Orban article/thesis the most directly identified missing bodies. A comprehensive claim would also need the geometry and Cross-talk gaps. No external communication was prepared or initiated, and no Git/provider/DOI/Sheet mutation was performed by this agent.

Completion estimate: **100% of this bounded source-adversary task**, not 100% of all historical priority research or publication. Final UTC and machine-readable boundary are in `VERDICT.json` and `RESEARCH_LOG.md`.
