# Independent adversarial review: common tangent loci

## Verdict

**PASS for the stated measure-zero theorem.** No substantive mathematical gap was found in the final candidate after checking its source scope, its nonsmooth cap-chart construction, its density-point argument, all affine-dimensional cases, and the area-formula application. This is an independent mathematical review of a candidate, not a certification of historical novelty or a substitute for external peer review.

- Problem: **30001075 / OWR-2090-028**, Conjecture 4, Oberwolfach Report 44/2008, printed p. 2552.
- Reviewed artifact: `CANDIDATE.md`.
- Final SHA-256: `b04aaf0b5a42d79ad26daf27880774a3f126858ef545b3f366a2b8b62e277252`.
- Review date: 2026-09-30 UTC.
- Reviewer: separate `gpt-6-astra` agent, reasoning effort `xhigh`.
- Scope: arbitrary pairwise disjoint convex subsets of three-dimensional Euclidean space, with a tangent line required to meet the set and lie in a supporting plane. The union of common tangent lines is contained in a Lebesgue-null set.
- Excluded claim: the stronger Conjecture 3 concerning a countable union of two-manifolds is **not** established or endorsed here.

One wording clarification was requested and incorporated before this final hash: all rational balls must come from one fixed countable base in ambient Cartesian coordinates, independent of the line-dependent coordinate changes. There are no unresolved mandatory corrections.

## 1. Exact source and scope

The original [Oberwolfach Report 44/2008](https://ems.press/content/serial-article-files/46191), section 13, printed p. 2552, distinguishes the manifold-cover assertion from Conjecture 4's measure-zero assertion. The candidate addresses the latter. The source's tangency definition does not require smoothness, a unique supporting plane, or point contact. Its recorded closedness/empty-interior result cannot by itself imply measure zero.

The relevant underlying geometric material was checked in [Julien Demouth's 2008 thesis](https://theses.hal.science/tel-00342717/document), chapter 4. The terminology on printed p. 48 uses closed convex objects; Theorem 3 on p. 51 and Lemma 20 on p. 66 concern nowhere density. The candidate supplies its own proof and does not silently upgrade that conclusion. The review did not find source support for treating nowhere density as the desired theorem.

The problem-site endpoint was attempted first, but did not furnish an accessible statement. The original report supplies the controlling formulation. Historical priority remains unconfirmed: the review validates the submitted mathematical implication, not an exhaustive literature search.

## 2. Reduction from arbitrary convex sets

The reduction to countably many compact cases is valid even when the original sets are unbounded or not closed. For any common tangent, choose one contact in each set. The contacts are distinct because the sets are disjoint. Pairwise disjoint small closed balls from a fixed rational base can contain those contacts in their interiors. Intersecting each ball with the corresponding closure produces three disjoint compact convex sets, retaining both the contacts and their supporting planes.

It is important that the closures themselves need not be disjoint: separation of the selected balls, rather than separation of the closures, supplies disjointness in each compact triple. It is also important that the countable family of balls is fixed before any local rotation or shear. The final candidate expressly states this. Every original line belongs to at least one compact-case locus, and countably many null envelopes therefore give the required outer-measure conclusion. No measurability of the original tangent locus is assumed.

## 3. The cap-chart lemma

The central assertion is that common tangents to two disjoint compact convex sets of affine dimension at least two have a countable cover by Lipschitz two-parameter line families, apart from lines contained in a planar set's affine plane.

### Support gap and normal cones

In line coordinates $L(u,v)=\{(u+zv,z):z\in\mathbb R\}$, the candidate's support-gap function is Lipschitz by compactness. When the projected set has interior, its zero set is exactly the boundary of that projection, hence exactly the tangent-line condition. A full-dimensional body always has such a projection. For a planar body, the retained transverse directions do; a line meeting that plane with parallel direction is contained in the plane and is legitimately discarded as a null swept locus.

At a boundary point of a planar convex projection having interior, all outward normals lie in one strict hemisphere. Indeed, any interior disk gives a positive uniform scalar-product margin. This remains true at corners and along flat exposed faces; no differentiability or unique normal is needed.

The cap operation preserves the supporting normals at the chosen line. If a functional supports the cap but not the original set, a segment from the chosen contact to a point violating the support inequality would already violate it inside the cap, since the contact is interior to the cutting ball. Caps retain the affine dimension of the original convex sets. Compactness then ensures that nearby maximizing normals retain a positive scalar-product margin.

### Quantitative implicit construction

The two line motions are independent because their values at the two contact heights are respectively $(e_A,0)$ and $(0,e_B)$. Height-localization of the caps gives positive own-coordinate monotonicity and arbitrarily small cross-coordinate Lipschitz constants. The support-function increment bounds apply to all normals; applying a maximizing normal at the initial point proves the required one-sided own-coordinate estimate. Maxima can switch and the estimate still holds.

Strict monotonicity and the intermediate value theorem give the two scalar root maps on a sufficiently small neighborhood. Their cross-coordinate Lipschitz constants are less than $1/4$. Shrinking the free-parameter ball makes the coupled root map preserve a fixed small square, so contraction gives a unique simultaneous root and Lipschitz dependence on the two free parameters. This is a valid nonsmooth argument; it does not invoke an unavailable smooth implicit-function theorem.

### Countability

A nearby tangent to an original body need not meet the cap selected at the original line. The candidate does not assume otherwise. For each fixed pair of rational cutting balls, it considers the lines for which the construction is available for those fixed caps. The associated open line-space neighborhoods have a countable subcover because line space is second countable. Every selected line is a zero of the same fixed-cap equations in whichever selected neighborhood covers it, so it lies on that neighborhood's graph. Taking a countable union over fixed cap pairs proves the claim.

This fixed-cap extraction is essential and was specifically checked. Allowing the graph to contain additional lines is harmless, since the actual tritangent parameters are selected later.

## 4. Density-point rank restriction

For a Lipschitz family $q\mapsto(u(q),v(q))$, the parameter set $E$ of retained tritangents is Borel. For compact sets, contact points and unit supporting-plane normals have convergent subsequences along convergent tangent lines, proving closedness of tangency; the exclusions are Borel as well.

At almost every point of $E$, the point is a density point and the line map is differentiable. Density one implies that every infinitesimal direction can be approached along points of $E$ with an error of smaller order than the displacement. This justifies testing derivatives in arbitrary directions even when $E$ contains no open neighborhood and no suitable curve.

At a contact height $z_i$, the review checked all four affine dimensions:

1. **Dimension three.** If $Du+z_iDv$ were onto, one could choose a parameter direction toward the transverse component of an interior-ball center. At the appropriately interpolated height, nearby selected tangent lines would enter a convex-combination interior ball. The error is smaller than the ball's linearly shrinking radius, a contradiction.
2. **Dimension two.** Transversality makes intersection with the affine plane a smooth function of the line coordinates. Its derivative is exactly the one displayed in the candidate. Choosing the same transverse displacement therefore enters a relative interior disk. A supporting plane through a relative interior point must equal the body's affine plane, and a transverse line cannot be contained in it. This handles all non-discarded planar cases.
3. **Dimension one.** The retained line is not identical to the body's affine supporting line. Its transverse direction vector is consequently nonzero. The intersection equation bounds the line parameter by the size of $(u,v)$; projection perpendicular to that transverse vector has quadratic error. Differentiating along density sequences restricts the derivative image to a one-dimensional subspace.
4. **Dimension zero.** Passing through the fixed point forces $Du+z_iDv=0$ directly along the density sequences.

These arguments allow flat faces, multiple contacts, and nonunique supporting planes. Any contact may be chosen at a differentiability/density point; no measurable contact selection is required.

## 5. Three contacts and the area formula

Pairwise disjointness ensures three distinct contact heights on the line. Thus the quadratic polynomial $\det(Du+zDv)$ has three distinct roots and vanishes identically. This is the precise reason that the proof uses three sets. An independent negative-control check confirms that two roots alone do not suffice.

The sweep map $G(q,z)=(u(q)+zv(q),z)$ is Lipschitz on bounded coordinate patches and bounded height intervals. Its three-dimensional Jacobian determinant is exactly $\det(Du+zDv)$. The exceptional two-dimensional parameter set is null; its product with a bounded height interval is three-dimensional null. The equal-dimensional area formula, or its image-measure inequality, therefore gives a null image of the retained parameter set times that interval. Injectivity of the chart or the sweep is unnecessary, since the formula counts multiplicity and its image bound remains valid. Countably many bounded patches and height intervals cover the whole sweep.

The use of the area formula is within its Lipschitz hypotheses. No unproved dimension estimate, Sard theorem for a nonsmooth map, or inference from nowhere density is used.

## 6. Remaining dimensional configurations

If two sets have affine dimension at least two, the cap lemma supplies the charts. If one set is a point, ordinary direction charts parametrize all lines through that point. Otherwise at least two sets are compact nondegenerate intervals. Their positive separation makes the map from a pair of points, one in each interval, to the joining line locally Lipschitz in ordinary line coordinates; local open extensions provide the required two-parameter domains. Collinear configurations cause no difficulty: identical supporting lines were discarded, or the joining-line map simply has smaller rank.

All discarded lines lie in finitely many fixed planes or lines, so their entire union is null. Empty sets make the theorem immediate. These cases exhaust the possible affine dimensions.

## 7. Reproducible checks and limits

The independent script `independent_checks.py` runs 36 exact diagnostics:

- the quadratic determinant, three-root Vandermonde, and swept-Jacobian identities;
- a two-contact negative control;
- the moving-line/fixed-plane derivative;
- 25 rational cap-margin and contraction tests, including narrow normal cones;
- six nonsmooth polyhedral support-increment checks.

Run from the directory containing this review:

```sh
python3 independent_checks.py
```

It writes `independent_results.json` and reports `PASS 36 independent exact diagnostics`. The only nonstandard dependency is SymPy, tested with version 1.14.0. These tests verify algebra and quantitative estimates. The analytic coverage, density, compactness, and area-formula arguments were reviewed separately above; finite tests are not presented as a proof of those statements.

**Final disposition:** the reviewed snapshot supports the exact Conjecture 4 claim and is suitable for a draft mathematical-candidate PR with explicit novelty and review qualifications. It must not be described as establishing Conjecture 3 or as externally peer reviewed.
