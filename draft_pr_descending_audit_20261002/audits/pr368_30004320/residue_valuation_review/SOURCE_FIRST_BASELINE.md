# Independent primary-source baseline: residue and ramification family

Recorded UTC: 2026-10-03T12:51:49.285682+00:00

## Access and independence

Before this baseline I read only the source-routing manifest (URLs, names, hashes and lengths), the assigned problem identifier and frozen path/head/base/scope, and primary sources acquired directly from their publisher/author/arXiv URLs. I have not read any candidate TURN prose, programs, recorded results, statuses, final narrative, historical review, Git history, or root/sibling conclusions. All five fresh PDFs match the historical length and SHA-256 exactly; PRIMARY_SOURCE_RECEIPT.json records retrieval intervals. PDFs/text/renderings remain private. A web screenshot of OWR page 23 timed out; a local Poppler rendering was then inspected successfully. The PDF skill was read and disclosed for read-only visual inspection; no installation was needed.

Read primary portions: OWR printed pp.3264–3265 (PDF22–23), with PDF23 visually inspected; Florence–Gille November2019 introduction pp.1–2 and initial index construction pp.2–3; v3 introduction and index setup pp.2–3, residue definition/functoriality/Theorem3.4/Corollary3.5, torsor Proposition4.1/Corollary4.2/Theorem4.3, pseudo-complete definition/Lemma5.1/Proposition5.2/Th5.4 and its nearby proof; Florence compactifications introduction/definitions (perfect-field convention), Proposition4.7/Lemma4.8, full section5 through Theorem5.6 (pp.12–15), with PDF15 visually inspected; Gille Pisa introduction and initial three pages. This is a targeted primary-source read, not a claim to have read every page of every PDF.

## Exact target and already established boundaries

The OWR statement asks whether existence of a k((t))-point of a homogeneous space over a field entails a k-point. Its immediately preceding theorem establishes this implication for torsors under affine algebraic groups over arbitrary fields. This is a point-existence implication, not descent of the given individual Laurent-series point, not extension of every point to k[[t]], and not cohomological bijectivity over all Laurent-series extensions. A homogeneous space need not be a torsor: a point over an extension can have a nontrivial stabilizer and an obstruction to a k-defined torsor dominating the space.

The OWR/v3 introductions mention the characteristic-zero homogeneous-space case. The actual Florence compactifications primary paper works throughout over a perfect field, proves K_infinity/k acyclic (H1 bijections for all k-groups), and Proposition4.7 explicitly descends rational points of homogeneous spaces over any acyclic extension; K_infinity contains k((t)). Thus the homogeneous-space implication is established there for perfect k, including perfect positive characteristic, under that paper's group/variety/homogeneous-space conventions. The imperfection boundary cannot be removed from the proof: reduction of stabilizers, the perfect extension K_infinity, separability/dominance and coefficient-field identifications are used.

Florence–Gille v3 Theorem5.4 asserts injectivity H1(k,G)→H1(k((t)),G); Proposition5.2 proves affine torsor point existence, allowing non-smooth groups through the largest geometrically reduced subscheme. Injectivity kills torsors that become trivial; it does not automatically assert surjectivity of H1 or descent of an arbitrary homogeneous-space gerbe.

## Independent residue reconstruction

For a nonintegral loop g in a closed subgroup G of SL_N over a ring A, take σ_r(t)=t(1+u t^r), adjoining rational powers when necessary. The least r for which g^{-1}σ_r(g) becomes integral is the nonnegative rational index. At positive index, specialization at t=0 yields a nonconstant Ga→G group homomorphism; at index0 one inverts 1+u and gets Gm→G. This multiplicative localization at r=0 is essential. The homomorphism identity follows from composition of parameter perturbations and their leading term, not merely from a first derivative in the Lie algebra. In positive characteristic denominators can be p-powers and Frobenius can force all ordinary derivatives to vanish while the group morphism is nontrivial. In integral characteristic0 the index is integral. Wound groups prohibit these nontrivial residues and therefore force integral loops/torsor points.

For a torsor X, the element g_r is uniquely defined by σ_r(x)=x g_r, and faithful-flat local triviality allows construction and descent of its residue. For a homogeneous space with nontrivial stabilizer, uniqueness is lost: transporters form stabilizer torsors. Treating that transporter as a canonical group element or assuming a rational lift to G would beg the central question. Any candidate residue extension must make this gap explicit or prove a new lifting mechanism.

## Falsifiable checks for the assigned approach

1. Distinguish existence of one k-point from integrality of every Laurent point; isotropic groups and affine space provide immediate negative controls for universal integrality.
2. Track scheme-theoretic stabilizers in characteristic p; Ga action by pth powers is transitive fppf with nonreduced alpha_p stabilizer, despite having zero differential.
3. Verify each claimed change of parameter as a genuine field/ring automorphism with correct coefficient action. A substitution with constant coefficient t-dependent cannot be silently k-linear. Tame t=T^d scales index/residue by d; pure p-power reparametrization can preserve the index and compose the residue with Frobenius, so tame and wild formulas cannot be conflated.
4. A leading Laurent coefficient or residue invariant only proves a local obstruction; no arbitrary homogeneous-space point descent follows without a global lift, gerbe-neutrality or an acyclic-extension theorem within its hypotheses.
5. Test cancellation, pole orders divisible by p, purely inseparable constants and sums of negative Laurent terms, where differentiation or maximal pole alone may miss cancellations.
6. Check that residue formulas and claimed descent remain valid after unit changes in a uniformizer; canonical claims must survive the specified equivalence relation.

## Success criterion and current assessment

A full solution would prove the universal homogeneous-space implication over the intended arbitrary field and group hypotheses, or construct a fully checked counterexample satisfying those hypotheses. Proper varieties descend a K-point by valuative properness; torsors and perfect-field homogeneous spaces already have source theorems. Recovering these cases or constructing a valid obstruction to an attempted method is partial evidence. No candidate-specific result or status has been assessed yet. Workflow completion estimate: 15%. Original problem resolution: unassessed.
