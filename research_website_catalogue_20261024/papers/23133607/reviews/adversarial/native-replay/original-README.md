# Verification supplement: Takao's self-duality question

Companion to Alec Kriebel's unrefereed research note, version1.0, dated4 October2026.
For every p>3 and n>=3 the theorem gives a p-killed finite flat commutative
W(closure of F_p)-group of rank p^(2n) whose special fiber is qss and for
which both the special fiber and the lift fail Cartier self-duality.
The original target is the unnumbered question after Takao Proposition2,
OWR42/2023, printed2479. The qss hypothesis is on the special fiber.

Use Python3.10 or later, without optimization or extra dependencies:

    python3 -B verify_supplement.py
    python3 -B verify_supplement.py --full

Default mode checks the complete inventory and every SHA256 payload,
then runs the portable priority convention verifier. Full mode also runs
four mathematical controls and compares each complete stdout to the
actual package-build execution. Both modes require empty stderr and
unchanged package bytes and inventory. They make no network requests,
install nothing, and write no package files.

The controls were developed in distinct adversarial families: the Honda
control checks exact basis/splitting data and higher ranks; the semilinear
control uses F_125 and F_343, intrinsic and forced-column obstructions,
and wrong-twist mutants; the intrinsic control uses dual annihilators,
odd-degree semilinearity and a self-dual rank-four comparison; the integral
flag control checks the stronger classical supersingular realization and
71 formal Laurent identities. construction.json is a reviewed input to
the intrinsic control. Each public source and its reviewed original are
pinned in SOURCE_IDENTITY.json, with exact literal derivations recorded.
The intrinsic public derivative omits interpreter identity from its
deterministic mathematical stdout; actual execution provenance is retained
separately in native build receipts. Public document references point to
the included manuscript or classical mechanism. Sealed originals remain
unchanged. The corrected public intrinsic derivative also repairs a generic
semilinear dual-kernel formula: opposite squared Frobenius twists are essential.
CONTROL_FORMULA_CORRECTION.md derives the formula and its exact counterexample.
New actual-kernel/minimal/dense controls cover F125, F343 and a Frobenius-order-five
F32 sample. The latter checks only generic linear algebra and does not extend
the group-scheme theorem beyond p>3. Its public mathematical code and assertions
are intentionally corrected/extended, with original input data preserved.

manuscript.tex is the standalone source. CLASSICAL_MECHANISM.md gives
the supplemental saturated integral flag and its mathematical scope.
priority/ contains the bounded primary-source audit, search inventory,
version/access limits and public verifier. That verifier's false sealed
flag describes its prepared immutable payload; the external root decision
is in PRIORITY_DECISION.json. No first-discovery, first-application or
continuing-openness certificate is supplied. Raw primary PDFs/PS,
screenshots and full private process/provenance records are omitted.
Hashes establish integrity relative to the supplied records, not an
independent authenticity or human peer-review certificate.

Finite controls corroborate the all-p symbolic proof; they do not prove
the named Dieudonne/finite-Honda classification inputs. The result does
not assert W-qss, perfect-field descent, polarization, a Jacobian
realization, or a resolution of the surrounding Coleman conjecture.
AI tools were used extensively in solving, verification, literature
research, writing, computation and adversarial review. This is an
unrefereed preprint; automated reviews are not independent external
human peer review and no such human review is claimed.
