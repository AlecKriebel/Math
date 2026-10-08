# Verification and scope audit

Result: the written partial theorem and supporting calculations pass the checks described below. This is an author self-audit, not an independent referee report. The unrestricted conjecture is unresolved.

## Claims checked

1. Coefficients are R=Z localized at 2, and cyclic generator orders are part of the basis claim. No free integral basis is asserted for positive-degree finite-group cohomology.
2. The S4 first Bockstein is computed in the published ring F2[x,y,z]/(xz), and E2 is derived by explicit monomial cancellation. The source classes v^k z are individual skyline classes, not arbitrary linear combinations.
3. C4 restriction detects the secondary differential. The integral lifting paragraph distinguishes a corrected lift from the canonical Fox-Neuwirth representative and does not iterate Sq^1.
4. The primary generators are a pivot subset of primary Bocksteins of skyline classes. Their reductions and the secondary reduction give a basis of H/2H; cyclic-order counts then prove direct-sum independence.
5. The extension n=5,6,7 uses odd indices 5,15,35, field Kunneth at the first Bockstein page, and primitive degree-positive gathered classes. It does not assume an integral tensor-product Hopf-ring presentation.
6. On S8, the two unequal gathered columns form one skyline class. The d2 target transfers to an equal-column square with even divided-power coefficient. C8 orbit stabilizers and the zero contribution of the C2 orbit are stated explicitly. Third-page detection proves exact order 8 but does not prove a full basis for S8.
7. The preferred-basis counterexample concerns an artificial complex, not any symmetric group.

## Computation

The complete `verify.py` run returned PASS on October 7, 2026. It checks 81 degrees of the S4 algebra and all 70 four-subsets used in the C8 Mackey decomposition, plus the elementary checks listed in the proof. One missing standard-library import in the initial augmented test was corrected; all mathematical assertions then passed unchanged. A byte-for-byte rerun of the JSON output is required by the freeze procedure.

## Literature and provenance

The primary report was inspected at the exact conjecture location. The mod-2 Hopf-ring paper, integral Fox-Neuwirth model, 2023 extended-power paper and 2025 Curtis-Wellington paper were inspected at the sections recorded in `SOURCE_METADATA.json`. No inspected source provided a complete integral skyline-basis theorem. This is a bounded search statement and no novelty is claimed for the partial results.

No copied source text, downloaded paper, public dataset contents, private source-gate record or private coordination file is included in this packet. Bibliographic citations, URLs, public source byte metadata and authored mathematics are included.
