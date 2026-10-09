# Independent audit: uniform intrinsic detours in Teichmüller balls

**Audit date:** 2026-10-09 UTC.

**Reviewed manuscript:** *Uniform intrinsic detours in Teichmüller balls*, 6,998 bytes, SHA-256 `e941b4ee875fe9585ca22979169f855f54c705046d7c3b62bb0fee79c4325d9b`.

**Verdict: PASS.** The manuscript proves the claimed exact-ball path theorem, and therefore both the distance-two and every-fixed-distance almost-convexity contracts, for every fixed closed oriented genus at least two. No mathematical correction or further proof turn is required. The conclusion relies on established Teichmüller geodesic existence and Lenzhen–Rafi's published theorem; this audit verifies the application and the entire additional metric argument, rather than reproving those published foundations. Historical novelty is not certified or needed for this verdict.

## 1. What has been established

For each fixed closed surface \(S=\Sigma_g\), \(g\ge2\), there is \(c_g\ge0\), depending only on the topology, such that every two points \(x,y\) in every closed ball \(\overline B_T(o,r)\), \(r\ge0\), admit a continuous rectifiable path in that same ball of length at most
\[
d_T(x,y)+4c_g.
\]
All distances and lengths use the actual Teichmüller metric with the factor \(1/2\) in the logarithmic dilatation formula. There is no change of metric or enlargement of the final ball.

Consequently, for same-sphere endpoints at separation \(k>0\), one can take \(N_g(k)=k+4c_g\). In particular, the distance-two constant is \(C_g=2+4c_g\). The proof also covers endpoints anywhere in the ball with separation at most \(k\), with that same upper bound. This last assertion follows directly from the stronger path theorem, rather than from an assumed equivalence of exact-distance formulations.

The order of quantifiers is correct: fix \(g\), obtain \(c_g\), then choose any center, radius, and endpoints. If the formulation fixes \(k\) first, \(N_g(k)\) is available before the center and radius are chosen. No thickness, injectivity-radius, center, radius, curve, or foliation dependence is hidden in this constant. Uniformity over all genera and a numerical universal value of \(c_g\) are not asserted.

Farb's original definition uses same-sphere separation two before posing Question 3.5; the generalization to spaces is abbreviated there. The audit does not assume that this wording alone proves equivalence with all variants. The manuscript proves the stronger explicit contract directly. Source: [Farb, printed pp. 24–25](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf#page=31). His closed-surface notation is specified on printed p. 10, PDF p. 17.

## 2. Independent check of the metric lemma

The hypothesis needs one constant \(c\ge0\) and, for each center \(o\) and pair \(a,b\), a geodesic joining that pair whose points satisfy
\[
d(o,z)\le \max\{d(o,a),d(o,b)\}+c.
\]
The geodesic may depend on the center. Simultaneous consistent choices, uniqueness, properness, completeness, and geodesic extension are unnecessary for the lemma.

### Small radius

If \(r<c\), radial geodesics from \(x\) to \(o\) and from \(o\) to \(y\) remain within the original closed ball: the distance from \(o\) along either is bounded by its endpoint distance. Their combined length is \(d(o,x)+d(o,y)\le2r<2c\le d(x,y)+4c\). The argument uses no convexity hypothesis for arbitrary geodesics between points of the ball.

### Radius at least the additive constant

Write \(s=d(o,x)\) and \(t=d(o,y)\). A geodesic from \(o\) to \(x\) contains the point \(a\) at distance \(\max\{s-c,0\}\) from \(o\). Its subsegment back to \(x\) has length \(\alpha=\min\{s,c\}\). Define \(b\) and \(\beta\) in the same way using \(y\).

Because \(s,t\le r\) and \(r\ge c\), both retreat points have center distance at most \(r-c\). This remains true when an endpoint is less than \(c\) from the center: its retreat point is exactly the center, and \(0\le r-c\).

Apply the hypothesis to this new pair \(a,b\), with the original center \(o\). It gives a middle geodesic whose entire image has center distance at most \((r-c)+c=r\). The two radial pieces also remain in the original ball. Their finite concatenation is a continuous rectifiable path; its length is the sum of the three piece lengths even if some pieces retrace one another.

The triangle inequality gives
\[
d(a,b)\le\alpha+d(x,y)+\beta.
\]
Thus the total length is at most
\[
\alpha+d(a,b)+\beta
\le d(x,y)+2\alpha+2\beta
\le d(x,y)+4c.
\]
Every estimate is non-strict where boundary containment is needed. No limiting argument, radial Lipschitz estimate, projection map, or fellow-travelling estimate is used. In particular, the retreat does not need to preserve the original endpoint separation; its possible increase by \(2c\) is already charged in the bound.

### Degenerate cases

- \(r=c\): both retreat points are the center; the middle segment is constant.
- \(c=0\): the retreat points are the endpoints, and the hypothesized geodesic is already in the ball. The bound becomes the exact ambient distance.
- \(r=0\): the ball has just the center, and a constant path works, including when \(c=0\).
- \(x=y\): the displayed construction remains within its stated bound; a constant path is also available.
- \(x=o\), \(y=o\), or \(a=b\): zero-length pieces cause no discontinuity or length issue.
- Empty same-sphere endpoint configurations, such as separation \(k>2r\), make the corresponding universal assertion vacuous; the proof never assumes such points exist.

These checks cover manuscript lines 26–60 without a missing case.

## 3. Verification of the Teichmüller input

The metric normalization and minimizing geodesics are recalled in [Fortier Bourque–Rafi, arXiv v3, §2, pp. 4–5](https://arxiv.org/pdf/1606.05170v3#page=4). In particular, any two distinct points lie on a Teichmüller line, so Lenzhen–Rafi's theorem for ordered points on a line applies to the required middle segment. Constant segments handle coincident points.

[Lenzhen–Rafi, Theorem C, printed p. 268](https://www.math.toronto.edu/rafi/Papers/Convexity.pdf#page=2), quantifies over every center and radius. Their notation convention on pp. 268–269 makes the comparison constants topology-dependent only. The extremal-length statement is Theorem 15, p. 282. Most importantly, Theorem 17's proof, pp. 284–285, establishes the pointwise, non-strict distance inequality required by the metric lemma. Thus the application does not depend on deciding whether their unadorned ball symbol denotes an open or closed ball. The theorem has no thick-part restriction.

The conversion of constants is correct. Taking \(K_S\ge1\) in the extremal-length inequality and using Kerckhoff's distance formula gives \(c_S=(\log K_S)/2\). Indeed, for any nonzero measured foliation, the ratio with the extremal length at \(o\) is bounded by \(K_S\) times the maximum of the two endpoint ratios. Taking the supremum, then half the logarithm, yields the required additive inequality. This also avoids needing to select a maximizing foliation. The published proof alternates the symbols \(\mu\) and \(\gamma\) for its extremal-length argument; that notational inconsistency does not alter the inequality.

No converse to the published theorem is invoked. The additional contribution in the reviewed manuscript is the fully written retreat-and-concatenate deduction that removes the additive radial allowance while keeping bounded length.

## 4. Compatibility with nearby results

The nonconvexity theorem in [Fortier Bourque–Rafi](https://arxiv.org/pdf/1606.05170v3) concerns failure of containment of the direct geodesic. It does not prohibit short alternative paths. There is therefore no conflict with the audited theorem. Their introduction, p. 3, also explicitly recalls Lenzhen–Rafi's topology-dependent uniform quasiconvexity.

[Petyt–Zalloum, published PDF p. 7, Theorem I](https://link.springer.com/content/pdf/10.1007/s00208-026-03534-1.pdf#page=7), supplies an almost-convexity theorem for a wall model and a \(k+6\) bound in that model. The accompanying disclaimer concerns the reach of that theorem. It does not contradict the separate deduction from Lenzhen–Rafi. No wall-model path, discrete interpolation, quasiisometry, or \(k+6\) constant is imported into the audited argument.

## 5. Prior-art scope and editorial observations

A bounded web search on 2026-10-09 used accented and unaccented Teichmüller queries with almost-convexity, Farb Question 3.5, intrinsic ball distance, and combinations of uniform/additive ball quasiconvexity and radial retreat. Relevant primary sections of Farb, Lenzhen–Rafi, Fortier Bourque–Rafi, and Petyt–Zalloum were inspected directly. No primary source explicitly stating this general exact-ball metric lemma or the exact Teichmüller corollary was located. Lenzhen–Rafi expressly states the enlarged-ball theorem; the other inspected sources do not supply the missing exact-ball deduction in the inspected relevant sections. This is a bounded negative search result, not a proof of priority or absence from the literature. The manuscript's disclaimer of historical novelty is appropriate.

Two optional editorial improvements would increase precision without changing any mathematical claim or the acceptance verdict:

1. In manuscript line 66, replace “Their Theorem A, equivalently Theorem 15” with “The extremal-length part of their Theorem A, stated as Theorem 15.” Theorem A additionally includes hyperbolic length.
2. In line 82, introduce the intrinsic-distance inequality with “Consequently” rather than “Equivalently.” The explicit path construction proves it immediately; in a general metric space an inequality for an infimum alone need not produce a path attaining its upper bound. The audited proof never makes that invalid reverse inference.

No computational experiments are required for this finite symbolic argument, and none are used as evidence of mathematical validity. File hashing and PDF rendering only identify and inspect the reviewed materials.

## 6. Source identity pins

The following byte counts and SHA-256 values were independently recomputed from the inspected PDFs. They identify the exact editions consulted; the source documents themselves are not reproduced here.

- **Farb:** *Some problems on mapping class groups and moduli space*, in *Problems on Mapping Class Groups and Related Topics*. Source: https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf . 2,724,624 bytes; SHA-256 `f37c6a1dbc875105c2b294196de1a03a88595b75e8705e6077e9d48f066e402a`. Definition and question: PDF pp. 31–32, printed pp. 24–25.
- **Lenzhen–Rafi:** *Length of a curve is quasi-convex along a Teichmüller geodesic*, JDG 88 (2011), 267–295. Source: https://www.math.toronto.edu/rafi/Papers/Convexity.pdf . 267,927 bytes; SHA-256 `179455d195b0f24cac238283063bc82d34db1d529a9b26f0f0193b7f14aaa409`. Theorem C and constants convention: PDF pp. 2–3; Theorem 15: PDF p. 16; Theorem 17 and proof: PDF pp. 18–19. All these page images were inspected.
- **Fortier Bourque–Rafi:** *Non-convex balls in the Teichmüller metric*, arXiv:1606.05170v3, 29 August 2017; published JDG 110 (2018), 379–412. Source: https://arxiv.org/pdf/1606.05170v3 . 519,853 bytes; SHA-256 `a49397b9921f675846f396a38bec398794b4b470dc0226c66f58ecacd02d0376`. Normalization and geodesic existence: §2, PDF pp. 4–5, images inspected; related-results discussion: PDF p. 3, text inspected.
- **Petyt–Zalloum:** *Constructing metric spaces from systems of walls*, Mathematische Annalen 396, article 38 (2026). Source: https://link.springer.com/content/pdf/10.1007/s00208-026-03534-1.pdf . 1,496,964 bytes; SHA-256 `114c0b088c9bb8b9cf34f71789c3c6d2d88e192e3b4906e5a2b3fb83eca56e6d`. Definition, Theorem I, and scope disclaimer: published PDF p. 7, image inspected.

**Final acceptance:** the reviewed manuscript supplies the exact-original-closed-ball bridge, with the uniform additive length bound \(4c_g\), and proves both requested almost-convexity formulations throughout the fixed-closed-genus range \(g\ge2\).
