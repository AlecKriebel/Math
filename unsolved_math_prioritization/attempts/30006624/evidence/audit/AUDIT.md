# Independent full audit: local-to-global medianity, 30006624

Audit date: 8 October 2026. Outcome: **PASS as an UNSOLVED partial report**, with the separate source-normalization addendum. There is no proof or counterexample to the full target, and no novelty claim is warranted.

Public derivative of the independent audit. Nonpublication provenance material is excluded. The original complete audit is retained privately. The mathematical findings, source-normalization warning, source checks and historical verification counts below are unchanged; portable verification authenticates the separate public files directly and does not replay the original complete bundle.

## 1. Exact question and source boundary

The target is Problem 12 on printed page 533 of [Oberwolfach Report 8/2026](https://ems.press/content/serial-article-files/53603), DOI [10.4171/owr/2026/8](https://doi.org/10.4171/owr/2026/8). The source page was visually inspected. The question concerns complete, simply connected path-metric spaces with pointwise good neighborhoods and no uniform local radius. A good triple has exactly one ambient interval median. Neither intrinsic-neighborhood medianity nor closure of the neighborhood under medians is a substitute.

The normalized corpus identity is uniquely `30006624 / OWR-14299911-026`. Only the local-median component of `30006622 / OWR-14299911-024` is the same problem. Its group questions and the distinct normalized target of record 30006623 are outside this audit. The neighboring raw extraction does not enlarge the mathematical assignment. Five approach families remain charged once to the shared target; this audit and its tests add no discovery attempt.

The [2023 manuscript](https://bhbowditch.com/papers/ch-median.pdf) supplies the credited special-case boundaries: Theorem 1.1 requires uniform local medianity; Proposition 9.1 adds modularity to completeness, connectedness, and local medianity; Lemma 9.2 requires bounded-set uniformity; Proposition 9.3 adds local compactness; Proposition 9.4 adds USC. The [finite-rank metrization paper](https://bhbowditch.com/papers/medianmetrics.pdf) requires an established complete connected median space, and its restriction statement uses closed interval-convex subsets. The packet preserves these restrictions.

The current [author listing](https://bhbowditch.com/preprints.html) still identifies the May 2023 manuscript. Two independent targeted searches found no verified resolution. This is limited negative literature evidence, not an exhaustive present-status theorem. Existing source PDF bytes were independently hashed; current web inspection verifies statements but is not claimed as an independent byte download.

## 2. Almost modular implies modular: valid

The operative definition is:

For every `a,b,c` in the whole space and every positive `eta`, there exists one point simultaneously satisfying all three pair inequalities

`d(a,y)+d(y,b) <= d(a,b)+eta`, and the cyclic versions.

This is arbitrary additive accuracy, not a fixed coarse error, not an error depending only on the diameter, and not approximate existence restricted to small triples. The separate addendum documents the manuscript's repeated-pair printing error. The frozen definition is already the correct three-pair definition.

Fix `a,b,c`; let `P` be their perimeter, `F(x)` their sum of distances to `x`, and `f(x)=F(x)-P/2`. The triangle inequalities make the three pair defects nonnegative and give their sum as `2f(x)`. Thus `f=0` is equivalent to actual median membership, not merely to minimizing `F`.

At a point with `f>0`, choose a largest pair defect `2s`. Then `f/3 <= s <= f`. With `eta=s/10`, an eta-median of `(a,b,x)` exists by the global definition. Set `r=d(x,y)` and `Delta=f(x)-f(y)`.

The following are direct nonnegative-slack calculations, independently rederived:

- `r >= s-eta/2`, by adding the two endpoint-to-x triangle inequalities and the a-to-b approximate-interval inequality.
- `r <= s+eta`, by adding the other two approximate-interval inequalities and the a-to-b triangle inequality.
- `Delta >= r-2eta`, by adding the two approximate-interval inequalities involving x and `d(c,y)<=d(c,x)+r`.

Consequently `r>=19s/20` and `Delta>=3s/4>=f/4`. Therefore `f(y)<=3f(x)/4`. The sharper travel control is genuine:

`19Delta-15r = 19(Delta-r+s/5)+4(r-19s/20) >= 0`.

Iterating until an exact median is reached, or indefinitely otherwise, yields

`f(x_n) <= (3/4)^n f(x_0)` and

`sum_{n=M}^{N-1} d(x_n,x_{n+1}) <= (19/15)(f(x_M)-f(x_N))`.

This is a true summable-displacement estimate, not an unsupported extraction of a convergent subsequence. Completeness supplies the limit; distance continuity makes its three nonnegative defects vanish. The claimed distance bound `(19/15)f(x_0)` also follows. A stopping step with `f=0` is handled without requesting a zero-tolerance approximate median.

No connectedness, path-metric hypothesis, compactness, local medianity, finite rank, or uniform choice of approximants is hidden in this lemma. At each countable step any point satisfying the requested three inequalities works. Repeated target points and relabeling the largest pair cause no difficulty. Standard countable recursive choice is the only selection involved.

The tolerance control is substantive. In the l1 plane take `a=b=(0,0)`, `c=x=(1,0)`, and `y=(0,1/2)`. Then `s=1`; y is a 1-median of `(a,b,x)`, but the target defect increases by `1/2`. Replacing `eta=s/10` by `eta=s` invalidates the descent.

## 3. Uniqueness and the exact unresolved gap

The descent establishes existence only. For example, the finite vertex metric of `K_{2,3}` is complete and modular, yet the triple in its three-vertex part has two medians. This is a useful control, not a connected path-metric counterexample to the target.

Once global modularity is obtained, the target satisfies all hypotheses of Proposition 9.1: completeness is given; simple connectivity includes connectedness; local medianity is given. Its nonuniform uniqueness mechanism is valid. An audit of the local halving step gives the following explicit version.

A bad quintuple of size R consists of three points y1,y2,y3 and two median points m,m', with `d(yi,m)=d(yi,m')=R` and all within-part distances `2R`. A connected modular metric space has midpoints: a continuous Gromov-product coordinate takes all intermediate values, and a median turns its halfway value into an actual midpoint.

Choose midpoints z,z' from y3 to m,m'. Their distance is R. Choose wi in `Med(yi,z,z')`, i=1,2. Then `d(wi,z)=d(wi,z')=R/2`, `d(wi,yi)=R`, and `d(wi,y3)=R`.

If w1 differs from w2, let `D=d(w1,w2)<=R`. Medians p and q of `(z,w1,w2)` and `(z',w1,w2)` satisfy `d(p,q)=D` and both are medians of `(y3,w1,w2)`. If w1=w2=w, then w is a median of the original y-triple; at least one of `(w,m)` and `(w,m')` is a distinct pair of medians at distance at most R. In either case, a nonunique median pair at distance at most R produces a new bad quintuple of size at most R/2. One new median can be chosen within R of the old m, and the whole new quintuple is within 2R of m.

Thus repeated halving has summable anchor travel and shrinking quintuple diameter. Completeness forces all five vertices toward one limit. Eventually they lie in its good neighborhood, contradiction. This verifies why no uniform approximate-median uniqueness estimate is an extra missing premise after modularity has been proved.

The unsolved implication is still **pointwise local medianity plus the other target hypotheses implies global almost modularity**. The descent requests eta-medians of `(a,b,x)` with potentially distant a,b. A compact first nullhomotopy, local stationarity, or existence of local medians does not supply them. The report neither proves this implication nor conceals it.

## 4. Good-radius and compact control

The capped supremum radius is positive, and the inclusion `B(q,t) subset B(p,s)` for `t<s-d(p,q)` gives `r(q)>=r(p)-d(p,q)` after passing to the supremum. Interchanging p,q proves 1-Lipschitz continuity. The cap at 1 respects the estimate.

The proof correctly uses a radius strictly below the supremum; it does not assume that the supremum ball itself is good. On nonempty compact K, positivity and continuity give `eta=min_K r>0`. If `d(a,K)<eta/4` and the triple diameter is less than eta/4, an appropriate k in K places all three vertices in `B(k,eta/2)`, a good ball.

This proves the stated compact-neighborhood exclusion of shrinking bad triples. It does not yield a lower bound on bounded noncompact sets. The union of infinitely many compact images need not be compact, and completeness alone does not make the anchors of shrinking triples Cauchy. These are exactly the continuation gaps stated in the report.

## 5. Conformal obstruction

The weight `1+x` on `[0,1] x R` is between 1 and 2. Accordingly the weighted length metric is bilipschitz to the complete l1 strip and retains its simply connected topology. The minimum horizontal coordinate of a rectifiable connecting path is attained. Weighted horizontal variation is bounded below by `F(x)+F(u)-2F(z)`, and vertical variation by `(1+z)|y-v|`, where `F(t)=t+t^2/2`.

For vertical separation k<2, the derivative of that lower bound with respect to z is `k-2(1+z)<0`; the attaining horizontal/vertical path proves the exact distance formula. Every use of the formula in the bad triple stays inside this stated range.

The proof of the horizontal interval also supplies a lower bound valid for arbitrary W, so it does not assume that all path infima are attained. On the horizontal segment the B-to-C interval defect is `(b-x)(2+b+x-k)`, whose second factor is positive. Its only zero is B, and B has A-to-C defect `(b-a)k>0`. Therefore the triple has no median. Translated and arbitrarily small triples fit both interior and relative-boundary neighborhoods.

The obstruction is to automatic preservation of local medianity under bounded smooth conformal changes. It is not a counterexample to the original question. No error was found.

## 6. Counterexample controls and filling

**Spokes with shrinking circles.** Cross-branch distances add through the root; individual branches are compact. For a Cauchy tail meeting infinitely many branches, every point of the tail is close to the root by comparison with a tail point in another branch. Otherwise the tail lies in a finite union of compact branches. This establishes completeness, including the non-locally-compact root. The construction is bounded and geodesic.

The small local trees are ambient-good: any alternative circuit route is strictly longer. At a circle attachment a radius less than one eighth of its circumference is more than sufficient. Equally spaced circle triples have three short pair arcs with empty intersection. Their diameters tend to zero while attachment points remain pairwise distance 2. A 1-Lipschitz retraction onto any chosen circle confirms the failure of simple connectivity. Thus the example cannot refute the target.

**Filled squares.** Filling with entire l1 squares changes the old boundary metric, as the report explicitly acknowledges. Each spoke-plus-square is a compact median factor. Point wedges of median spaces have unique medians by the location of the three points; an off-factor candidate cannot lie in an interval with both endpoints in one factor because its excursion adds twice its distance to the wedge point. The infinite wedge inherits this three-point argument. The same branchwise Cauchy proof yields completeness. Shrink squares to their corners, then spokes to the root; the bounded branch diameters give joint continuity of the indicated contraction. The resulting space is globally median and contractible.

**Slit plane.** Small rectangles avoiding the slit have ordinary l1 distance; ambient interval points are forced into their coordinate rectangles by the l1 lower bound. Hence local medianity is ambient, not merely intrinsic to the charts. The metric topology is the usual slit-plane topology, and the polar-coordinate description establishes simple connectivity. Every B-to-C path crosses the negative horizontal axis; its length exceeds 4, while crossing at `-epsilon` gives infimum 4. The first two intervals force a prospective median to `[-1,0) x {0}`, where its B-to-C two-leg length exceeds 4. The Cauchy sequence approaching the removed origin verifies precisely the missing completeness hypothesis.

All three controls have the stated scope. None meets all full-target hypotheses while possessing a bad triple.

## 7. Auxiliary CAT(0) condition and overlap cautions

For `a*d<=rho<=b*d`, interpolation between matching points of two endpoint-compatible paths along rho-geodesics is continuous and fixes endpoints. CAT(0) convexity, summed over partitions, gives a slice rho-length bounded by the convex combination of the endpoint path lengths. Comparing lengths yields the claimed d-length factor `b/a`. Taking `delta=(a/b)*epsilon` supplies USC uniformly over all endpoints. The conclusion is conditional on this global auxiliary metric, which has not been constructed from the target hypotheses.

The finite-dimensional ball example correctly separates goodness from median closure. In infinite-dimensional l1, the interval-convex hull of the points `epsilon*e_i` contains all finite coordinate sums and is unbounded; this rules out assuming bounded convex neighborhoods.

The diagonal in the l1 plane is a closed complete connected median subalgebra but is not interval-convex. Its intrinsic rank-one metric is `2|s-t|`, whereas the plane's Euclidean auxiliary metric restricts to `sqrt(2)|s-t|`. Thus agreement of median operations does not supply the required auxiliary metric compatibility. A global rank bound and uniform distortion/completeness control remain absent. No conditional result is overclaimed as a resolution.

## 8. Independent computational and byte verification

All original controls were replayed by a fresh harness under genuine UID and EUID 1000. Frozen files had mode 0444 and their directory mode 0555. Attempts to open an existing member for writing and to create a directory member both raised PermissionError. The hashes of every frozen member matched before and after.

Normal, `-O`, and `-OO` modes each passed all three positive programs: bundle validation, exact mathematics, and external input checks. Total: 9 positive runs. Each mathematics run checked 3654 cube triples, 840 exact-median descent cases, and 129 weighted interval cases, plus the other stated finite controls.

All six specified mathematical mutations rejected in each mode. Independent byte alteration, a semantically false SOLVED/full-candidate budget with its manifest hash updated, and PDF corruption also rejected in each mode. Total: 27 expected negative runs. Failures were checked for their intended RuntimeError messages, rather than treating arbitrary crashes as success.

The frozen descent tests only use exact medians. This is explicitly limited coverage, not a flaw in the written proof. The additional `verify_descent.py` checks seven exact rational linear identities and 5040 genuinely inexact eta-median witnesses per mode. These witnesses have a strictly positive approximate-interval error. Three supplemental mutations independently reject omission of the lower-bound error, an oversized tolerance permitting actual defect ascent, and the repeated-source-pair definition. These checks were also run from a read-only copy under UID/EUID 1000: 3 positive runs and 9 expected rejections.

No Python assertion is used for substantive guards. Optimization does not erase their checks. The extension check in the original bundle program is only a file-type filter; source-freedom was also established by direct content inspection. All three PDFs and both external corpus files matched the declared sizes and SHA-256 values. Exact corpus IDs/codes and absent exact research joins were rechecked against the full loaded objects, without copying their contents into this audit.

## 9. Disposition

- Accept the frozen packet as a source-free, carefully scoped partial report, with full-target status UNSOLVED and the shared five-family budget unchanged.
- Retain the separate source-normalization addendum with any future use. No mathematical correction patch to the frozen files is needed.
- Preserve the distinction between a correct approximate-to-exact reduction and the missing construction of global approximate medians.
- Keep credited global special-case theorems as dependencies; this audit does not certify every line of the entire external manuscripts.
- No publication, global queue modification, source-body copying, or new discovery family was undertaken.

Public verification metadata: `HISTORICAL_REPLAY.json` (a scoped public derivative) and `DESCENT_REPLAY.json`. The fresh `AUDIT_MANIFEST.json` authenticates the actual public files. These records describe historical computations and inputs, not a fresh complete-bundle replay or the unresolved globalization assertion.
