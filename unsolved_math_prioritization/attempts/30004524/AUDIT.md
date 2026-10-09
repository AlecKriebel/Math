# Proof-only edition notice for the independent audit

The independent AI audit accepted the stated partial results, with the original problem **UNRESOLVED after approach 1 (1/5)**. The complete mathematical review in Sections 1–8, all substantive source findings in Section 9, and the exact accepted stopping point are preserved. No mathematical correction was required. This is AI-assisted review, not human peer review or formal proof-assistant verification.

The original audit also reviewed auxiliary programs and finite outputs. This edition omits those files and their frozen-input inventories, hashes, local paths and reproduction commands. Section 10 retains the original supplementary check history and its limitations; it does not claim executable reproduction from the included files. No omitted script or fixture has been transcribed into a new prose artifact. Packaging did not rerun those checks or inspect the source PDFs afresh.

The source PDF identities and historical source-check disposition remain in [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json); complete authored source analysis is in [SOURCE_AUDIT.md](SOURCE_AUDIT.md). See [PROVENANCE.md](PROVENANCE.md) for the narrow editorial changes. The original audit's mathematical discussion begins below.

---

# Independent audit: continuous PL extension selection, approach 1

Audit date: 2026-10-09 UTC. Problem: 30004524 / OWR1703876-018.

## Verdict

**ACCEPTED AS PARTIAL RESULTS, WITH THE ORIGINAL PROBLEM STILL UNRESOLVED.**

The audited report proves its stated local-to-global equivalence, fiber contraction and interpolation, convex-image selector, radial-cone obstruction, and necessary unbounded triangulation complexity under its explicitly chosen uniform topology. No correction to those claims is required. It neither supplies nor disproves the missing PL-valued local section on a full uniform neighborhood of the inclusion. Acceptance does not certify a solution, a new approach, or a current literature-wide open-status claim.

The original audit included full mathematical review of `APPROACH1.md`, review of the author's status and source records, source-statement verification, replay of the original rational checker in a temporary directory, and separately implemented rational checks. Its inputs were unchanged. Those auxiliary materials are not distributed in this edition. No publication or queue modification was part of the original audit.

## Input and edition boundary

The original frozen-input inventory is omitted because it identified excluded auxiliary materials. The included `ACCEPTANCE.json` preserves the mathematical verdict, accepted and unproved claims, source caveats, and historical supplementary-check disposition. This edition's `MANIFEST.json` identifies the included publication bytes; it is not a substitute for the omitted reproduction packet. A later mathematical change requires renewed review before reusing this acceptance.

## 1. Topology and scope

The report studies finite PL embeddings of a closed triangle and its boundary, each as a subspace of the corresponding uniform continuous mapping space. This matches the report's formulas and continuity proofs. The original short OWR and Rote statements do not explicitly specify these mapping-space topologies, and the report correctly marks uniform/compact-open topology as an interpretation. There is no substitution of a fixed triangulation, a bounded-complexity stratum, or a direct-limit topology.

The boundary embedding space is separable metrizable: it is a subspace of the separable metric space of continuous maps from a compact polygonal circle into the plane. Hence the partition-of-unity and sequential continuity arguments used later are applicable.

## 2. Lemma 1: fibers and Alexander contraction

**Accepted.** A planar disk embedding with boundary image a fixed Jordan polygon has image equal to the closure of that polygon's bounded complementary component. Compactness, the Jordan theorem, and invariance of domain justify the common-image assertion. Therefore, after choosing a single finite PL extension F of f, the maps H ↦ F⁻¹H and u ↦ Fu identify the entire fiber with the finite PL disk homeomorphism group fixing the boundary.

The Alexander formula is valid after translating the triangle so that the origin is interior. Convexity gives tT ⊂ T. On the inner boundary the two formulas agree because u fixes ∂T. For each positive t, scaling a finite triangulation inside tT and finitely triangulating the complementary polygonal annulus gives a finite PL homeomorphism. There is no infinite mesh or PL-limit argument here.

The estimate

‖A_t(u) − id‖∞ ≤ t‖u − id‖∞ ≤ t diam(T)

is uniform over the entire group and proves joint continuity at t = 0. For t bounded away from zero, extend u by the identity outside T. If u_n → u uniformly on T, these extended maps converge uniformly on the plane, and the arguments x/t_n range over a fixed compact set. Uniform continuity of the fixed limiting extension proves joint continuity in (u,t). The identities at t = 0 and t = 1 and fixation of the identity are correct.

## 3. Lemma 2: continuity with varying images

**Accepted.** The relative change of coordinates u_n = F_n⁻¹H_n is well-defined because F_n and H_n have exactly the same image. One can strengthen the report's correct compactness argument to a direct estimate. Put u = F⁻¹H. For every x ∈ T,

|F(u_n(x)) − F(u(x))| ≤ ‖F − F_n‖∞ + ‖H_n − H‖∞.

Both F(u_n(x)) and F(u(x)) lie in the single fixed compact set F(T), so uniform continuity of F⁻¹ on F(T) gives u_n → u uniformly. This avoids treating inverses with different domains as if they were maps on a common ambient open set.

The interpolation C(F,H,t) = F A_t(F⁻¹H) is thus jointly continuous. Every individual operation is finite PL, each output is injective, and the boundary remains exactly f. The two endpoint identities are correct.

## 4. Proposition 3: finite weighted gluing

**Accepted, including zero weights and support boundaries.** These are the potentially delicate parts of the report, and neither uses local compactness of the embedding space.

For a fixed finite list of maps with common boundary, define the weighted combination recursively in index order. When the sum s of the earlier weights is positive, combine the normalized earlier weights first and interpolate to the last map with parameter λ_last/(s + λ_last). When s = 0, take the last positive-weight map. Delete zero-weight entries.

The endpoint identities show that deleting a zero-weight entry changes no output. To prove continuity, induct on list length on the finite weight simplex, jointly with the list of input maps. At a point where s remains positive, ordinary composition and induction suffice. At a point where s → 0 and the last weight tends to 1, normalized earlier weights may vary, but every sequence of them has a convergent subsequence in their finite simplex. Along that subsequence the earlier combination converges by the inductive assertion, since every input map converges. Continuity of C at its second endpoint then gives the last input as the output limit. Every subsequence admits this refinement, so the whole sequence converges to that endpoint. No uniform endpoint control over the noncompact whole fiber is being assumed.

The partition of unity can be chosen countable, locally finite, and with each closed support contained in the corresponding local-section domain. To make the support-boundary argument explicit, at f choose an open neighborhood meeting only finitely many closed supports. For each of those supports not containing f, further shrink the neighborhood to avoid it. The remaining finite supports all contain f; their assigned local-section domains therefore contain f. Intersect the neighborhood with all of those domains. Every local-section value that can enter the combination on the resulting neighborhood is now defined and continuous there, even when its weight is zero at f. The fixed finite-list continuity argument applies.

At each input the actual output uses finitely many PL inverses, compositions, and Alexander rescalings. Finite common refinements suffice for these individual operations. Nothing requires a locally bounded mesh size or a single triangulation shared by nearby inputs.

## 5. Proposition 4: reduction to the inclusion

**Accepted.** If L restricts to the inclusion at i, then L(i)(T) = T and L(i) fixes ∂T pointwise. Thus replacing L(g) by L(g)L(i)⁻¹ is well-defined and normalizes L(i) to id without changing the boundary.

The pointwise ambient PL Schoenflies step legitimately extends the prescribed boundary parametrization, not merely its unparametrized curve. To spell out that distinction: a polygonal Schoenflies homeomorphism can first match the boundary images as sets. Its residual boundary map q is a finite PL self-homeomorphism of the standard triangle boundary. Radially extending q from an interior point, homogeneously on the entire plane, yields a PL plane homeomorphism after a finite fan subdivision that includes all source corners, breakpoints, and preimages of target corners. Composing this adjustment with the first ambient homeomorphism matches the given parametrization exactly. Orientation reversal is allowed.

Only a fixed ambient extension P_f is used for each center f. No continuous choice f ↦ P_f is asserted. For g close to f, compactness bounds g(∂T) inside a fixed compact neighborhood of f(∂T); uniform continuity of P_f⁻¹ there gives continuity of g ↦ P_f⁻¹g. The same compact-set argument proves continuity of postcomposition with P_f on nearby extension maps. The transported local section has exactly the required restriction, and Proposition 3 applies.

Accordingly, global section existence is equivalent to local section existence on a full uniform neighborhood of the triangle inclusion, under the stated topology.

## 6. Convex-image selector

**Accepted.** The full-support averaging measure puts p(f) strictly inside every convex Jordan polygon. If it lay on a supporting line, the associated continuous nonnegative function on ∂T would have zero integral and hence vanish everywhere by full support. That would place the whole Jordan boundary on a line, which is impossible.

Coning a finite subdivision containing the original corners and all breakpoints gives affine maps on finitely many source triangles. From an interior apex, the convex target polygon is covered by a nonoverlapping fan with the prescribed boundary parametrization, in either orientation. This proves injectivity and finite PL structure.

For the same source point, the radial coefficient t is independent of f. The averaging map has norm bound ‖p(f) − p(g)‖ ≤ ‖f − g‖∞, so the stated 1-Lipschitz estimate follows directly. No bound on the number or placement of boundary breakpoints is involved.

## 7. Hairpin family and universal continuous-apex quantifier

**Accepted.** The inserted path is simple for the stated 0 < δ ≤ 1/10. The old and new subdivisions give the exact squared uniform discrepancy 8δ²; on an affine segment the norm of the displacement is convex, so its maximum occurs at an endpoint. The polygon's oriented double area is 4 − 9δ², which is positive. The reversed fan determinant is −4δ/3 + 3δ², which is negative throughout the allowed interval.

The report's two source boundary points, their images, the parameters t_j, and their common cone image are all correct. The two resulting source points are distinct and lie strictly between the source apex and their respective boundary points. Direct evaluation of the full cone map, recovering the boundary point from each source ray, confirms the collision independently.

The continuous-apex statement has the required order of quantifiers. Start with any proposed continuous target apex rule on a full neighborhood, whose cone maps are asserted to be embeddings. At the identity its apex p₀ = (a,b) must be an interior point of T, so b > 0 and −1 < a < 1. Center the shrinking hairpin at (a,0), choosing δ small enough that its entire support lies on the bottom edge and its new vertices lie inside T. The corresponding boundary maps still converge uniformly to the inclusion. Continuity of the proposed apex rule forces p_δ → p₀. Its reversed-edge determinant is exactly

−δ((p_δ,x − a) + 2p_δ,y − 3δ).

The factor in parentheses tends to 2b > 0. For example, eventually |p_δ,x − a| < b/4, |p_δ,y − b| < b/4, and δ < b/12, making the factor at least b > 0. Thus sufficiently small members defeat this particular rule. Since the proposed rule was arbitrary, every continuous apex rule fails on some shrinking family tailored to its value at the identity.

A negative fan determinant is a genuine obstruction: an injective piecewise-affine map of a disk has a coherent orientation on its nondegenerate triangles, and the unchanged counterclockwise boundary orientation forces the positive orientation. The reversed triangle cannot occur in such an embedding. This argument concerns the radial-cone class only and leaves unrestricted PL extension selectors untouched.

## 8. Necessary complexity and limiting repairs

**Accepted.** Inside the image of any one linear boundary segment, choose a compact subsegment away from its endpoints. It has a thin neighborhood disjoint from the rest of the polygon. Arbitrarily many disjoint, arbitrarily small triangular teeth can be inserted there, preserving boundary injectivity and making the uniform perturbation as small as desired. Each noncollinear bend requires a boundary vertex in any triangulation on which an exact extension is affine. Thus even the minimum necessary output triangulation complexity is unbounded on every full uniform neighborhood.

This lower bound is compatible with uniform continuity of a selector and is correctly not used as a nonexistence proof. The report also correctly refuses to infer finite PL structure from an infinite uniform limit of finite PL approximants. The scalar polygonal approximation example suffices to demonstrate that logical failure; it does not preclude a different construction with a separate finite-structure argument.

## 9. Primary-source audit

The original source audit verified all five public source PDFs against the byte counts and SHA-256 hashes now retained in the sanitized `SOURCE_MANIFEST.json`. It checked the full original problem statements and relevant theorem hypotheses in the PDFs/text, including visual checks of source pages with important formulas. Details are preserved in the authored `SOURCE_AUDIT.md`. These are historical inspection records; packaging did not repeat the source reading or hash verification.

- The [OWR problem statement](https://ems.press/content/serial-article-files/46867), printed page 1523, and [Rote's problem list](https://page.mi.fu-berlin.de/rote/Kram/Problems-Discrete-Geometry-2020.pdf), page 4, ask for continuous selection but leave the mapping-space topology unstated.
- [Yagasaki's Theorem 1.1](https://arxiv.org/abs/math/0010222) supplies ambient homeomorphisms, without a PL codomain assertion. Theorem 1.2 and Lemma 4.4 concern PL subspaces and homotopy density; they do not preserve an arbitrary moving boundary map during the deformation. A nearby genuine PL local extension statement, Fact 4.2(4), concerns maps into a fixed ambient manifold boundary. It does not apply to a moving Jordan curve in the interior of the plane. The report's gap survives this additional check.
- [Gauld's theorem](https://www.numdam.org/item/CM_1976__32_1_3_0/) provides PL-preserving local contractions of homeomorphism groups. Its final warning concerns a different localized limiting construction that can lose PL structure. The report accurately distinguishes these claims.
- [Dobbins's Theorem 3.1.7](https://jep.centre-mersenne.org/articles/10.5802/jep.171/) provides continuously varying normalized conformal parametrizations. It does not assert finite PL outputs with arbitrary prescribed PL boundary parametrizations.

These conclusions are statements about the inspected sources. They are not an exhaustive assertion about every possible deduction from the literature or the present-day status of the problem.

## 10. Historical supplementary verification

The original audit checker imported no code from the original checker. It used exact rational arithmetic, independently computed segment contacts by solving the two segment parameters, checked adjacent contacts as well as nonadjacent contacts, and evaluated cone outputs by recovering the actual source-ray boundary points. This description is retained from the written audit; the checker, fixtures and standalone outputs are omitted.

The original audit recorded the following results:

- Original checker replay: output bytes identical to the frozen JSON.
- Original fixture rows independently matched: 4 of 4.
- Unshifted shrinking-hairpin cases: 194 passed, including every δ = 1/n for 10 ≤ n ≤ 200 and δ = 1/1000, 1/10000, 1/1000000.
- Translated hairpins and perturbed apex cases: 150 passed, covering five horizontal positions, two positive apex heights, three scales, and five apex perturbations per configuration.

The finite computations check the stated fixtures and help detect algebra or implementation mistakes. The analytical arguments above, not the sample count, establish the universal conclusions. No computer calculation settles the missing local-section lemma.

## Exact accepted stopping point

The original task remains **UNRESOLVED after approach 1**. The missing statement is a continuous finite-PL-valued map L on some full uniform neighborhood of the triangle boundary inclusion with exact boundary restriction L(f)|∂T = f. This audit accepts the listed partials, requires no correction patch, and supplies no additional approach or resolution.
