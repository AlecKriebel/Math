# Proof-only edition notice

The original question remains **UNRESOLVED after approach 1 (1/5)**. All mathematical statements, proofs, source analysis and remaining-gap discussion from the original approach-1 report are preserved below. Uniform/compact-open topology is an explicit interpretation of the short source statements, which leave the mapping-space topology unstated.

Only the auxiliary reproduction section has been edited: executable commands, omitted-file references and original inventory language have been removed or replaced with an edition boundary. Its supplementary check history is retained as history. The programs, fixtures and standalone outputs are not included, were not rerun during packaging, and have not been converted into replacement prose. The displayed shrinking-family construction and collision proof were already part of the authored report and remain unchanged.

The mathematical proofs, rather than finite sample checks, establish the stated partial results. No PL-valued section on a full uniform neighborhood is constructed or ruled out. See [PROVENANCE.md](PROVENANCE.md) for the exact editorial boundary and [AUDIT.md](AUDIT.md) for the independent mathematical audit. This edition is not a new proof-search approach.

---

# Continuous PL extension selection for a triangle

## Conclusion and scope

**Status: unresolved after approach 1.** This report does not prove or disprove the existence of the requested selector. It proves a local-to-global reduction, gives an explicit selector on the convex-image subspace, and exhibits an exact obstruction to extending the radial-cone construction to a full uniform neighborhood. The remaining issue is a genuinely PL-valued local extension operator for arbitrarily subdivided boundary maps.

Problem identifier: 30004524, OWR1703876-018, Michael Dobbins, Problem 14 in the 2020 Discrete Geometry problem session. This is one substantive approach: continuous local selection and its globalization. No claim of a new resolution or current literature-wide open status is made.

## The question and its topology

Fix a nondegenerate closed triangle T in the plane. Put

- B = Emb_PL(∂T, R²), the injective maps that are affine on the intervals of some finite boundary subdivision;
- E = Emb_PL(T, R²), the injective maps that are affine on the triangles of some finite triangulation of T;
- r : E → B, r(F) = F restricted to ∂T.

The problem asks whether r has a continuous right inverse S. The triangulation may depend on the input and there is no bound on its size.

Here B and E carry their **uniform topologies**, equivalently the compact-open topologies, since their source spaces are compact. This is the natural interpretation used in this report. The short primary statements do not explicitly specify mapping-space topologies. No stronger topology defined by a fixed triangulation, a uniform vertex bound, derivative bounds, or a direct limit of triangulation strata is substituted.

The source is [OWR 30/2020, printed page 1523, Problem 14](https://ems.press/content/serial-article-files/46867), corroborated by [Günter Rote's public problem list, page 4](https://page.mi.fu-berlin.de/rote/Kram/Problems-Discrete-Geometry-2020.pdf). Both distinguish individual PL extension existence from a continuously varying assignment. The Rote page was inspected visually as well as through extracted text. The OWR statement and its surrounding hypotheses were inspected in the full report.

## What the adjacent literature supplies

[Yagasaki, Spaces of embeddings of compact polyhedra into 2-manifolds, 2000](https://arxiv.org/abs/math/0010222), Theorem 1.1, gives continuous local ambient **topological** extensions in the compact-open topology. Its codomain is a homeomorphism group, not its PL subgroup. Theorem 1.2 and Lemma 4.4 study the PL embedding subspace and homotopies into it; this does not say that such a homotopy fixes an arbitrary moving boundary map. These results therefore do not establish a section of r. This distinction is essential even though the paper starts with PL source and target manifolds.

[Gauld, Local contractibility of spaces of homeomorphisms, 1976](https://www.numdam.org/item/CM_1976__32_1_3_0/), proves local contractibility with PL preservation for homeomorphism groups. The discussion on printed page 11 expressly notes that a localized limiting deformation can cease to be PL. A limiting argument cannot simply import PL-valued output from finite intermediate stages.

[Dobbins, Grassmannians and pseudosphere arrangements, 2021](https://jep.centre-mersenne.org/articles/10.5802/jep.171/), Theorem 3.1.7, supplies continuously varying normalized conformal parametrizations. It does not supply finite PL extensions of the prescribed boundary parametrizations. Individual PL Schoenflies existence and canonical topological/conformal extension are not the missing parameter-dependent PL result.

## A local section at one boundary map would suffice

The reduction below isolates the exact local statement whose proof would settle the question positively. Its globalization uses finite PL operations at each input; no infinite limit of PL maps is taken.

### Lemma 1  The fiber and its explicit contraction

Let G be the group of PL self-homeomorphisms of T that fix ∂T pointwise, with its uniform topology. For every f in B, the fiber r⁻¹(f) is homeomorphic to G.

Indeed, choose one PL extension F of f. Every other extension H has the same image as F, namely the closed Jordan region bounded by f(∂T). Thus u = F⁻¹ ∘ H belongs to G. Conversely, F ∘ u is an extension of f for every u in G. Composition with fixed F and F⁻¹ is uniformly continuous on the relevant compact sets, establishing the asserted homeomorphism.

Translate T so that 0 is an interior point. For u in G and 0 < t ≤ 1 define

A_t(u)(x) = t u(x/t) for x in tT,

A_t(u)(x) = x for x in T outside tT,

and define A_0(u) = id_T.

The formulas agree on ∂(tT), since u fixes ∂T. For each t > 0 the map is a PL homeomorphism: rescale a triangulation for u inside tT and triangulate the remaining polygonal annulus, where the map is the identity. It follows that A_1(u) = u and A_t(id_T) = id_T. Further,

‖A_t(u) − id_T‖∞ ≤ t ‖u − id_T‖∞ ≤ t diam(T).

This proves joint continuity at t = 0, uniformly in u. For t > 0, extend u to R² by the identity outside T and use the formula t u(x/t); uniform continuity on compact sets proves joint continuity there. Hence A is a contraction of G through PL homeomorphisms. For fixed t it also respects composition, though that additional fact is not needed below.

### Lemma 2  A continuous interpolation inside each fiber

For F,H in E with r(F) = r(H), set

C(F,H,t) = F ∘ A_t(F⁻¹ ∘ H),  0 ≤ t ≤ 1.

Then C(F,H,0) = F, C(F,H,1) = H, and r(C(F,H,t)) = r(F). Every value is PL and injective.

The transition F⁻¹ ∘ H is continuous even when the common image varies. To check this, suppose F_n → F and H_n → H uniformly and r(F_n) = r(H_n). If x_n → x and y_n = F_n⁻¹(H_n(x_n)), any convergent subsequence y_n → y satisfies F(y) = H(x). Injectivity determines y uniquely as F⁻¹(H(x)). Compactness of T turns this sequential statement into uniform convergence of the transitions. Joint continuity of composition and Lemma 1 now prove continuity of C on the fiber product E ×_B E × [0,1].

### Proposition 3  Local sections everywhere imply a global section

Assume every f in B has an open neighborhood U on which a continuous PL-valued section of r exists. Since B is a separable metric space, select a countable locally finite partition of unity (λ_i) subordinate to such neighborhoods U_i, with closed support of λ_i contained in U_i. Let s_i be the corresponding local sections.

At each f only finitely many weights are nonzero. Combine the values s_i(f), in the fixed index order, with C. For two values use C(a,b,β/(α+β)); for a finite list, first combine the earlier values using normalized earlier weights, then interpolate to the last value with its weight. If all earlier weights vanish, use the last value directly. Zero-weight entries are omitted.

This finite weighted combination is continuous, including at zero weights. Here is a sequential verification that does not assume local compactness. Induct on the list length. If the total earlier weight tends to zero, pass to a subsequence on which the normalized earlier weights converge in their finite simplex. The input values also converge along any convergent base sequence. By induction their earlier combination converges, and the final interpolation tends to its second endpoint, the last value, independently of that subsequence. Every subsequence has this property, proving continuity at the zero-weight face. The other faces follow from the endpoint identities for C. In particular, deletion of zero-weight entries does not change the combination.

For completeness, near a fixed f the local finiteness and support condition allow one to discard supports not containing f and to shrink the neighborhood into every U_i that remains. All local section values used there are therefore defined and continuous. The preceding finite-list argument applies on that neighborhood. The resulting S is consequently continuous on B. Every S(f) is obtained by finitely many PL compositions and rescalings, so it lies in E and restricts to f.

This is also the usual contractible-fiber principal-bundle argument, but the explicit gluing avoids relying on an unproved claim that r is already a PL principal bundle.

### Proposition 4  It is enough to construct the section near the inclusion

Let i : ∂T → R² be the inclusion. Suppose a continuous section L exists on some uniform neighborhood U of i in B. Normalize it, if necessary, by replacing L(g) with L(g) ∘ L(i)⁻¹; then L(i) = id_T.

For any f in B, the classical ambient PL Schoenflies theorem gives a fixed PL homeomorphism P_f of the plane with P_f restricted to ∂T equal to f. This is a pointwise choice only; no continuity of f ↦ P_f is assumed. The map g ↦ P_f⁻¹ ∘ g sends a neighborhood V_f of f into U. On V_f define

s_f(g) = P_f ∘ L(P_f⁻¹ ∘ g).

This is a continuous PL-valued section. Continuity of the compositions follows from uniform continuity of the fixed ambient homeomorphism and its inverse on compact neighborhoods of the relevant images. Proposition 3 globalizes these local sections.

Therefore the following two assertions are equivalent:

1. The original global PL extension selector exists.
2. There is a continuous PL extension selector on a full uniform neighborhood of the standard triangle boundary inclusion.

The implication from 1 to 2 is restriction. The preceding proofs establish the reverse implication. No assumption on shared triangulations or bounded complexity has been inserted.

## A complete partial result on convex image curves

Let B_conv be the subspace of B whose image bounds a convex polygon. Fix c in the interior of T, and fix a probability measure μ of full support on ∂T, for example normalized source arclength. Define

p(f) = ∫_(∂T) f(x) dμ(x).

For f in B_conv, p(f) lies in the interior of its polygon. Otherwise, a supporting affine functional would be nonnegative everywhere on the image and have zero average. Full support and continuity would make it identically zero on the entire boundary, contradicting a nondegenerate Jordan polygon.

Each z in T other than c has a unique representation z = (1−t)c + t x, with x in ∂T and 0 < t ≤ 1. Set

S_conv(f)(z) = (1−t)p(f) + t f(x),

and S_conv(f)(c) = p(f).

This is a PL embedding extending f. To see the PL property, include the three original corners and every breakpoint of f in a finite subdivision of ∂T, then cone those intervals to c. The formula is affine on each resulting triangle. Convexity and the interior position of p(f) make the image a nonoverlapping fan of the target polygon, so the map is injective. Both orientations are allowed.

Moreover, for f,g in B_conv,

‖p(f) − p(g)‖ ≤ ‖f − g‖∞,

and therefore

‖S_conv(f) − S_conv(g)‖∞ ≤ ‖f − g‖∞.

Thus **the convex-image subproblem has a 1-Lipschitz selector**, with no fixed input subdivision or output vertex bound. The same cone formula works on any family furnished with a continuously chosen point in the interior of each polygon's visibility kernel.

## Why coning does not establish the required local lemma

Even arbitrarily small uniform perturbations of the triangular boundary can invalidate the cone fan. Here is an exact shrinking example.

Take T with vertices A = (−1,0), B = (1,0), C = (0,2), and c = (0,2/3). Let 0 < δ ≤ 1/10. On the bottom source edge keep the map unchanged except on the interval from (−4δ,0) to (4δ,0). At the four successive source positions

(−4δ,0), (−δ,0), (δ,0), (4δ,0),

prescribe respectively the values

P_0 = (−4δ,0), P_1 = (δ,δ), P_2 = (−δ,2δ), P_3 = (4δ,0),

and interpolate linearly. Keep the other two triangle edges unchanged. Call the resulting boundary map f_δ.

This is a simple polygonal boundary. The three inserted edges intersect only at adjacent endpoints; their interiors lie above the bottom edge and strictly inside the original triangle. The first and third inserted segments, whose supporting lines meet at x = 4δ/3, do not intersect because the first has x ≤ δ. Its uniform distance from the inclusion is exactly 2√2 δ, since the maximum of the norm of the piecewise affine displacement occurs at a subdivision vertex.

The fan triangle adjacent to the reversed middle edge has determinant

det(P_2−P_1, c−P_1) = −4δ/3 + 3δ² < 0.

Thus c is on the wrong side of this oriented boundary edge to be a visibility-kernel point.

There is an explicit failure of injectivity. The two source boundary points

b_1 = (−8δ/5,0),  b_2 = (0,0)

have images

q_1 = (0,4δ/5),  q_2 = (0,3δ/2).

Let z = (0,1/3), and choose

t_j = (2/3−1/3)/(2/3−(q_j)_y),  j = 1,2.

Both t_j lie strictly between zero and one. The distinct source points x_j = (1−t_j)c + t_j b_j have the same cone image z. Hence the radial-cone map is not injective for every such δ, despite f_δ → i uniformly.

Allowing the target cone apex to depend continuously on f does not repair this class of construction on a full neighborhood. If its value at i is a point p_0 = (a,b) in the interior, move the small construction horizontally so it is centered at (a,0). For a nearby chosen apex p = (p_x,p_y), the determinant of the reversed middle edge becomes

−δ((p_x−a) + 2p_y − 3δ).

As δ → 0 and p → p_0, the expression in parentheses tends to 2b > 0. Thus the determinant remains negative. Every continuous cone-apex choice fails on some members of this shrinking family.

This rules out **radial-cone selectors near the identity**. It is not a counterexample to the unrestricted selector problem: a general PL extension may introduce and move interior vertices and need not preserve straight source rays.

## Why finite mesh and limiting repairs remain insufficient

A single finite triangulation of T cannot extend all boundary maps in any uniform neighborhood: its boundary edges have only finitely many possible breakpoints, while one can insert a genuine small bend at another boundary position.

There is a stronger necessary complexity fact. Every uniform neighborhood of every f in B contains maps with arbitrarily many genuine boundary bends. Insert as many sufficiently small disjoint triangular teeth as desired in the interior of one linear boundary segment, using a thin neighborhood disjoint from the rest of the polygon. Any triangulation on which an exact extension is affine must include these noncollinear boundary bends among its boundary vertices. Consequently, **the triangulation size of an exact selector cannot be uniformly bounded on any full uniform neighborhood**. This is compatible with continuity in the uniform topology; it is not itself a nonexistence argument.

Similarly, selecting successively finer PL approximations to a canonical topological extension only gives a possible topological limit. Even the scalar example of polygonal interpolants converging uniformly to x² shows that finite piecewise affinity is not preserved under uniform limits. A successful limiting construction would need a separate mechanism proving finite termination or finite PL structure for each input, together with continuous dependence and exact boundary preservation. No such mechanism has been established here.

## Exact remaining gap

The missing statement is:

> There are ε > 0 and a continuous map L : {f in B : ‖f−i‖∞ < ε} → E such that L(f) restricted to ∂T equals f.

Normalization L(i) = id_T is harmless. The neighborhood must include all finite PL subdivisions, arbitrarily steep small features, and arbitrarily many boundary bends. Output triangulations may vary without a local size bound.

The approach establishes that this one local PL selection lemma would settle the entire problem, and that contractibility of the extension fiber is not the unresolved step. It does **not** establish that lemma. The checked topological extension, PL homotopy-density, and local-contractibility results do not provide the required boundary-preserving PL-valued operation as stated. No genuine counterexample to such an operation was found.

## Historical supplementary checks and claim boundaries

The original work recorded exact rational-arithmetic checks. For δ = 1/10, 1/100, 1/1000, and 1/10000 those checks verified:

- no nonadjacent polygon edges intersect;
- positive polygon orientation;
- the exact squared uniform displacement 8δ²;
- the negative fan determinant;
- two distinct source points with exactly the same radial-cone image.

All original checks were reported as passed. The symbolic arguments above, rather than these finitely many checks, establish the shrinking-family conclusions. The auxiliary checker and its output are omitted from this edition; their results are retained only as historical supplementary verification.

The sanitized source manifest records scholarly titles, public URLs, raw public PDF identities and historical inspection details. Source PDFs and extracted texts are not distributed. This edition supplies the written proofs and mathematical audit without an executable reproduction packet. No queue edit or additional approach is part of this edition.
