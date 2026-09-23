# Verification report

Target: Kurose's printed Question 3(e), Furuhata–Matsuzoe–Urakawa (1998), p.126. Version 1.0.0, audited 22 September 2026 (local time).

## Verdict

**The candidate is a complete counterexample to the printed implication.** No mathematical gap was found in the source check, intrinsic proof review, or independent coordinate computation. The extension with nonzero cubic tensor is also valid. This is a negative answer to a universally stated yes/no question; it does not require classifying every statistical manifold satisfying the premise.

**Priority:** no earlier explicit answer was located in the bounded audit. This is not a guarantee of first discovery or verified current open status. The exact prior construction behind the extension is credited to the divisible-cubic-form literature. See `reviews/priority_audit.md` for the searches, known ingredients, inaccessible sources, and remaining historical gaps.

## Checkable chain of reasoning

| Claim | Evidence | Remaining mathematical gap |
| --- | --- | --- |
| The original question admits Levi–Civita structures | Visual inspection of original 3(a) and 3(e); Kurose's definitions | None found |
| Product is statistical and self-dual | Torsion-free metric connection; defining duality identity | None found |
| Every required distribution is integrable | First variation: radial covector equals dE; positive definiteness gives regularity off the center | None found |
| Conformal flatness forces the stated pointwise identity | Derived difference-tensor curvature formula; independently recomputed all 81 components | None found |
| Cylinder violates that identity everywhere | Sphere plane forces A(e1)=e1; mixed plane forces A(e1)=0 | None found |
| Algebra checker is not hardwired to reject | Flat and constant-curvature controls pass; dimension-two boundary accepted | None found in tested algebra |
| Non-self-dual extension remains statistical | All cubic components symmetric, C_ttt=−3 exp(t); all duality components checked | None found |
| Extension preserves radial distributions | Explicit positive reparametrization and conformal preservation of orthogonality | None found |
| Extension's dual cannot be flattened | A putative factor psi would flatten the original with factor t+psi | None found |
| All dimensions n≥3 are covered | Add Euclidean factors without changing the three-vector contradiction | None found |

The pointwise standard-library checker supplies an exact rational certificate in dimensions 3, 4 and 5. In dimension three its linear system has coefficient rank 9 and augmented rank 10. The independently implemented coordinate checker passes 403 symbolic checks. It derives the tensors from the metric rather than assuming the product formula. Both scripts retain failure checks under Python optimization.

## Limits, source distinction, and boundary cases

- The written first-variation proof supplies the universal center/neighborhood quantifiers; the scripts check tensor algebra, not that analytic theorem.
- The center is explicitly excluded in the original problem. No smooth foliation through the center or across global cut loci is claimed.
- Statistical 1-conformal flatness is a connection condition. Ordinary Riemannian conformal flatness would be a different question.
- The higher-dimensional claim is proved symbolically in the paper; checking three dimensions numerically would not establish it.
- The standard-library solver intentionally accepts the two-dimensional sphere tensor. This does not decide the original implication restricted to dimension two.
- The live database was inaccessible; a local catalog records `partially_solved` without an inspected supporting result. The original printed formulation controls the claim.
- `gradient_path_counterexample.py` and its output refer to discrete Morse theory, not statistical geometry, and contribute no evidence here.
- These are AI-assisted mathematical and computational checks, not human peer review or a formal proof-assistant certification.

## Approach-family record

| Family | Mechanism | Status | Exact gap |
| --- | --- | --- | --- |
| Intrinsic geometry | First variation and connection-difference tensor | Complete direct proof | None found |
| Projective curvature | Independent Ricci/Weyl contraction and Kurose criterion | Confirms obstruction | Not needed for primary proof |
| Coordinate algebra | Derive Christoffel symbols and all tensor components from metric | 403 checks pass | Does not formalize analytic integrability |
| Literature/source audit | Printed definitions, targeted source and citation searches | No direct priority conflict located | Historical priority and inaccessible source coverage remain unproved |

No equivalent unsupported reformulation was used to bridge the core argument, so no proof route is marked blocked. The exact strongest verified result is the two explicit counterexamples and the n≥3 product extension.
