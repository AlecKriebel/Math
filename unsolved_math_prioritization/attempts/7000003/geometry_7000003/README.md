# Ghomi Problem 1.3: fixed-boundary negatively curved annuli

Problem ID: 7000003 / AMR-069-0003. Assessment date: 2026-10-05.

## Disposition

**No resolution. Five substantive approaches completed. No novelty claim.**

The retained results are elementary restricted theorems and exact obstruction controls. They do not establish global isometric rigidity, produce a counterexample with the required boundary, or establish that the original problem has been solved elsewhere. Fresh independent audit is pending at this author freeze.

The most useful negative control is an explicit smooth embedded closed curve with nowhere-zero torsion. Its normal ribbon has strictly negative Gaussian curvature, a closed asymptotic core, and neutral first-return multiplier. Both ribbon boundaries are nonplanar. Thus it does not answer the question, but blocks an attempted deduction from negative curvature alone.

## Identity and scope

The original source is Mohammad Ghomi, *Open Problems in Geometry of Curves and Surfaces*, revised September 2, 2019, printed page 6, Problem 1.3:

“Are negatively curved annuli bounded by a pair of fixed convex planar curves rigid?”

Source: https://people.math.gatech.edu/~ghomi/Papers/op.pdf

This is a question about extrinsic isometric rigidity in Euclidean three-space. It is not marked-boundary-distance rigidity of intrinsic metrics. The short problem does not itself give a precise differentiability threshold, say that the boundary planes are parallel, impose rotational symmetry, or explicitly say that the planes are tangent to the surface. Its surrounding smooth tight-surface discussion supplies the motivation, not permission to silently append hypotheses.

We distinguish the literal question from the narrower Nirenberg setting documented in the 2025 paper below: a smooth annulus with negative curvature in its interior whose boundary curves lie in tangent planes. In that setting Gaussian curvature vanishes on the boundary under C² regularity, as proved below. The short sentence does not separately settle whether immersed annuli are allowed; the later paper explicitly distinguishes immersed and embedded cases. We also distinguish pointwise-fixed boundary parametrizations, as used in our infinitesimal theorem, from merely fixing the two boundary sets.

The 2019 manuscript's nearby total-positive-curvature normalization is inconsistent with the conventional 4π normalization used in Han–Khuri and the 2026 paper. No argument here uses that nearby numerical statement.

## Current literature check

- Ghomi–Raffaelli, *Topology of closed asymptotic curves on negatively curved surfaces*, J. Geom. Anal. 35, article 381 (2025), published October 9, 2025, DOI https://doi.org/10.1007/s12220-025-02200-3. Its introduction still poses the relevant injective-Gauss-map/zero-linking obstruction as a problem. Its results constrain projections and exhibit examples satisfying either injectivity or zero linking without settling their conjunction. The tangent-boundary and embeddedness qualifications matter. We inspected the author's September 19, 2025 manuscript and the publisher's article.
- Han–Khuri, *Rigidity in the class of orientable compact surfaces of minimal total absolute curvature*, Differential Geom. Appl. 29 (2011), 463–472, DOI https://doi.org/10.1016/j.difgeo.2011.04.035. This proves conditional global rigidity of closed tight surfaces, with boundary-degeneracy conditions and a nonzero integral along every closed asymptotic curve. It does not supply those hypotheses for arbitrary annuli. Its equation (2.3) relates that integral to the transverse derivative of the second fundamental form. The conditional theorem is not a full resolution.
- Ghomi–Hoisington–Raffaelli–Stavroulakis, *Total absolute curvature and rigidity of surfaces in Cartan-Hadamard manifolds*, https://arxiv.org/abs/2604.25024, inspected introduction and §6.3.2. Its equality theorem concerns the 4π absolute-curvature lower bound and flat convex bodies. The extension concerning tight surfaces places them inside flat convex bodies. It does not prove uniqueness of all Euclidean tight-surface embeddings or the annular boundary-value question.

The 2025 paper is affirmative evidence that a central obstruction was still unresolved then. Bounded searches through 2026-10-05 did not locate a later complete resolution; absence of a search result is not a theorem of open status. Bibliographic metadata and retrieval limits are in SOURCES.json.

The current repository queue was read directly and still listed this ID as queued, 0/5. Repository code and all-state PR searches for the ID and relevant terms found no matching prior mathematical attempt. Existing local material found for the ID consisted of queue/catalog records. These bounded checks do not prove that no unindexed or otherwise unavailable prior work exists.

## Five approaches and retained outcomes

1. **Boundary Cauchy data:** the infinitesimal rotation field vanishes on a fixed boundary wherever its normal curvature is nonzero. Tangent planar boundary has zero Gaussian curvature and defeats this noncharacteristic argument. See PROOFS.md, §1.
2. **Rotational reduction:** all Fourier modes of an infinitesimal bending vanish when one parallel is fixed and the meridian height derivative is nowhere zero. This is a complete restricted infinitesimal theorem, not nonlinear rigidity. See §2.
3. **Associate-family construction:** the catenoid–helicoid family preserves the local metric, but every nontrivial associate has a nonzero period around the proposed annulus. It cannot provide the desired closed-boundary counterexample. See §3.
4. **Projection/support-function route:** a negative-curvature graph admits no closed asymptotic curve whose projected tangent lines avoid a point. The proof does not make arbitrary annuli graphs or give every projected loop that property. See §4.
5. **Closed-characteristic monodromy and construction:** derive the return multiplier and exhibit the explicit neutral negatively curved ribbon above. Exact nonplanarity excludes it from the target class. Extending such a ribbon to convex planar boundaries while preserving the required geometry remains unproved. See §5.

## Exact replay

Run from this directory:

    python3 verify.py

The verifier uses Python's standard library and exact rational/polynomial arithmetic. It checks the torsion numerator, speed, a positivity certificate, Fourier-mode elimination, associate metric and period, ribbon curvature algebra, and return-map linearization. It also requires intentionally corrupted variants to fail. These are identity checks and controls, not a formal proof assistant and not a certificate of the full open problem.

EXPECTED_RESULTS.json records the deterministic output. MANIFEST.json records the safe file hashes and sizes. Source PDFs, text extracts, catalog data and private retrieval files are excluded.

## Remaining obstruction

None of these arguments bridges the global gap from fixed convex planar boundary data to uniqueness across all characteristic regions, including degenerate boundary and neutral closed-asymptotic behavior. In the embedded tangent-boundary route one must also respect the injective Gauss map and zero normal-linking constraints identified in the literature. The explicit ribbon does not meet the boundary requirement and cannot be promoted to a counterexample. No queue status of solved/already_solved is justified.
