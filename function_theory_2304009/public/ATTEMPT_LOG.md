# Research log: 2304009

## 2026-10-04 08:41 UTC — source gate

Completion estimate: 20% toward verifying the exact target's disposition.

The catalogue URL was unavailable. The selected immutable dataset record and prior report were recovered. The 2018 source gives the exact problem and immediately records its disproof. The upstream “open” report is therefore an incorrect status assessment. The main queue has no earlier recorded attempt for this target.

## 2026-10-04 08:44 UTC — primary resolution and novelty check

Completion estimate: 65% toward verification; no new-discovery claim.

Huang's v2 full text proves the arbitrary-many-large-components theorem and explicitly acknowledges Pommerenke's prior resolution. The original 1961 publisher PDF was inaccessible, so its proof is not counted as directly inspected. Erdős's own 1976 retrospective provides primary historical corroboration. Hilbert's exact approximation statement was checked in Bloom–Levenberg–Lyubarskii.

## Substantive response 1/5 — complete verification reconstruction

Mechanism: place arbitrarily many long, separated horizontal segments inside a capacity-one ellipse; use Hilbert's theorem to trap a polynomial lemniscate in their separated neighborhoods; capacity forces its leading coefficient to have modulus at least one; a dilation-and-rotation normalizes that coefficient without shortening components.

The exact theorem, explicit constants, separation argument, capacity identity, and counterexample quantifier deduction are in PROOF.md. This is one complete verification response, not five artificial attempts at an already resolved problem.

Checks targeting potential failure:

- Capacity sign: `cap(E(q)) = |alpha|^(-1/n)`; inverting this would reverse the scaling argument.
- Correct normalization: `p(z) = q(z/w)`, `w^n = alpha`; division of q by its leading coefficient would change the selected sublevel set and would not preserve the geometry.
- Boundary conventions: all segment sets and lemniscates are closed; the containing ellipse is replaced by its closure for capacity.
- Component count: inclusion of N segments alone does not imply N components; the outer inclusion in N positively separated neighborhoods is essential.
- Diameter strictness: the segment length is `L > d`; with `d = 2`, the target's strict `> 1+c^2` at `c = 1` is met.
- Degree quantifier: degree may depend on N; no bounded-degree construction or growth-rate claim is inferred.
- Source transcription: the erroneous reciprocal-log energy display in Huang is not used.

Completion estimate at freeze: 100% of the author verification and artifact preparation; independent review is pending. The exact original claim is known false. The separate asymptotic update remains outside this deliverable's scope.

No new external communication, repository publication, merge, release, or DOI was undertaken by this author stage.
